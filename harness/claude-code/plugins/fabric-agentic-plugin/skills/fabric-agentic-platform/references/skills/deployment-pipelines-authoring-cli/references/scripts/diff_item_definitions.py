#!/usr/bin/env python3
"""Diff two Fabric item definitions and emit ONLY the differences.

Token-efficient change comparison for deployment-pipeline promotion. Fabric has
no "what changed" / compare REST API, so to deploy only changed items you must
diff the source- and target-stage item definitions yourself. Streaming both full
`getDefinition` payloads into an LLM is expensive (dozens of KB per item). This
tool decodes both payloads locally, normalizes the fields Fabric auto-rebinds on
deploy (so unedited items don't look "changed"), matches parts by path, and
prints only the resulting diffs -- which is all the model needs to reason about
the semantics of a change.

Input: two `getDefinition` responses (JSON). Each may be either the raw response
`{ "definition": { "parts": [...] } }` or just `{ "parts": [...] }`. Each part is
`{ "path": "...", "payload": "<base64>", "payloadType": "InlineBase64" }`.

Exit codes (mirroring POSIX `diff`):
  0  definitions are identical (after normalization) -> item UNCHANGED
  1  definitions differ                              -> item CHANGED
  2  usage / input error

Examples:
  # Fetch both sides, then diff (only the diff reaches the agent's context):
  diff_item_definitions.py source.json target.json
  # Text (unified-diff) output instead of structured JSON:
  diff_item_definitions.py source.json target.json --format text
  # Read one side from stdin:
  getDefinition ... | diff_item_definitions.py - target.json
  # Verify the tool itself:
  diff_item_definitions.py --selftest
"""

import argparse
import base64
import binascii
import difflib
import json
import sys


# Fields Fabric AUTO-REBINDS in the target stage on deploy (pipeline notebook /
# workspace ids, report->model binding, Direct Lake server/db, connections, etc).
# A paired target's definition legitimately differs from the source in these even
# when nothing was edited -- blank them on both sides so they never show as a diff.
DEFAULT_NORMALIZE_KEYS = [
    "workspaceId",
    "notebookId",
    "datasetId",
    "connectionId",
    "defaultLakehouseId",
    "defaultLakehouseWorkspaceId",
    "lakehouseId",
    "artifactId",
    "objectId",
    "server",
    "database",
    "logicalId",
]

_PLACEHOLDER = "<normalized>"


class InputError(Exception):
    """Signals an input/usage error -> process exit code 2."""


def load_definition(source):
    """Load a getDefinition JSON from a file path or '-' for stdin."""
    try:
        if source == "-":
            raw = sys.stdin.read()
        else:
            with open(source, encoding="utf-8") as handle:
                raw = handle.read()
    except OSError as exc:
        raise InputError(f"cannot read '{source}': {exc}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputError(f"'{source}' is not valid JSON: {exc}")


def extract_parts(defn):
    """Return { path: decoded_bytes } from a getDefinition response.

    Accepts either the raw response ({"definition": {"parts": [...]}}) or the
    bare definition ({"parts": [...]}).
    """
    if not isinstance(defn, dict):
        raise InputError("definition must be a JSON object")
    container = defn.get("definition", defn)
    parts = container.get("parts") if isinstance(container, dict) else None
    if parts is None:
        raise InputError("no 'parts' array found (expected getDefinition output)")

    out = {}
    for part in parts:
        path = part.get("path")
        if path is None:
            raise InputError("a part is missing its 'path'")
        payload = part.get("payload", "")
        ptype = part.get("payloadType", "InlineBase64")
        if ptype == "InlineBase64":
            try:
                data = base64.b64decode(payload, validate=True)
            except (binascii.Error, ValueError) as exc:
                raise InputError(f"part '{path}' has invalid base64 payload: {exc}")
        else:
            # VOID / unsupported payload types carry no inline content to diff.
            data = payload.encode("utf-8") if isinstance(payload, str) else b""
        out[path] = data
    return out


def decode_text(data):
    """Best-effort UTF-8 decode; returns None for binary content."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def normalize_json(obj, keys):
    """Recursively blank auto-rebound binding fields so they don't show as diffs."""
    if isinstance(obj, dict):
        return {
            k: (_PLACEHOLDER if k in keys else normalize_json(v, keys))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [normalize_json(v, keys) for v in obj]
    return obj


def _truncate(value, limit):
    if not limit:
        return value
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    if len(text) > limit:
        return text[:limit] + f"...(+{len(text) - limit} chars)"
    return value


def json_diff(a, b, limit, path="$"):
    """Structural diff of two JSON values -> list of {op, path, old?, new?}."""
    changes = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(a.keys() - b.keys()):
            changes.append({"op": "remove", "path": f"{path}.{k}", "old": _truncate(a[k], limit)})
        for k in sorted(b.keys() - a.keys()):
            changes.append({"op": "add", "path": f"{path}.{k}", "new": _truncate(b[k], limit)})
        for k in sorted(a.keys() & b.keys()):
            changes.extend(json_diff(a[k], b[k], limit, f"{path}.{k}"))
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(min(len(a), len(b))):
            changes.extend(json_diff(a[i], b[i], limit, f"{path}[{i}]"))
        for i in range(len(b), len(a)):
            changes.append({"op": "remove", "path": f"{path}[{i}]", "old": _truncate(a[i], limit)})
        for i in range(len(a), len(b)):
            changes.append({"op": "add", "path": f"{path}[{i}]", "new": _truncate(b[i], limit)})
    elif a != b:
        changes.append({"op": "change", "path": path,
                        "old": _truncate(a, limit), "new": _truncate(b, limit)})
    return changes


def diff_part(name, src_bytes, tgt_bytes, keys, normalize, context, limit):
    """Diff a single part present in both sides. Returns a diff record or None."""
    src_text = decode_text(src_bytes)
    tgt_text = decode_text(tgt_bytes)

    if src_text is None or tgt_text is None:
        if src_bytes == tgt_bytes:
            return None
        return {"path": name, "kind": "binary", "note": "binary content differs",
                "oldBytes": len(src_bytes), "newBytes": len(tgt_bytes)}

    try:
        src_obj = json.loads(src_text)
        tgt_obj = json.loads(tgt_text)
        is_json = True
    except json.JSONDecodeError:
        is_json = False

    if is_json:
        a = normalize_json(src_obj, keys) if normalize else src_obj
        b = normalize_json(tgt_obj, keys) if normalize else tgt_obj
        changes = json_diff(a, b, limit)
        if not changes:
            return None
        return {"path": name, "kind": "json", "changes": changes}

    # Text (TMDL, .py notebook, .pq, etc.) -> compact unified diff.
    if src_text == tgt_text:
        return None
    hunks = list(difflib.unified_diff(
        src_text.splitlines(), tgt_text.splitlines(),
        fromfile=f"a/{name}", tofile=f"b/{name}", n=context, lineterm=""))
    if not hunks:
        return None
    return {"path": name, "kind": "text", "unifiedDiff": "\n".join(hunks)}


def diff_definitions(src_def, tgt_def, keys=None, normalize=True, context=3, limit=200):
    """Compare two getDefinition responses; return a result dict with only diffs."""
    keys = set(DEFAULT_NORMALIZE_KEYS if keys is None else keys)
    src_parts = extract_parts(src_def)
    tgt_parts = extract_parts(tgt_def)

    diffs = []
    for path in sorted(src_parts.keys() - tgt_parts.keys()):
        diffs.append({"path": path, "kind": "removed-part", "note": "part present in source only"})
    for path in sorted(tgt_parts.keys() - src_parts.keys()):
        diffs.append({"path": path, "kind": "added-part", "note": "part present in target only"})
    for path in sorted(src_parts.keys() & tgt_parts.keys()):
        rec = diff_part(path, src_parts[path], tgt_parts[path], keys, normalize, context, limit)
        if rec is not None:
            diffs.append(rec)

    return {
        "changed": bool(diffs),
        "normalized": normalize,
        "summary": {
            "sourceParts": len(src_parts),
            "targetParts": len(tgt_parts),
            "changedParts": len(diffs),
        },
        "diffs": diffs,
    }


def render_text(result):
    """Human/agent-readable rendering of a diff result."""
    if not result["changed"]:
        return "No differences (item unchanged)."
    lines = [f"CHANGED: {result['summary']['changedParts']} part(s) differ "
             f"(normalized={result['normalized']}).", ""]
    for d in result["diffs"]:
        lines.append(f"# {d['path']}  [{d['kind']}]")
        if d["kind"] == "json":
            for c in d["changes"]:
                if c["op"] == "change":
                    lines.append(f"  ~ {c['path']}: {c['old']!r} -> {c['new']!r}")
                elif c["op"] == "add":
                    lines.append(f"  + {c['path']}: {c['new']!r}")
                else:
                    lines.append(f"  - {c['path']}: {c['old']!r}")
        elif d["kind"] == "text":
            lines.append(d["unifiedDiff"])
        else:
            lines.append(f"  {d.get('note', '')}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _selftest():
    """Built-in regression checks. Returns True on success."""
    def defn(parts):
        return {"definition": {"parts": [
            {"path": p, "payload": base64.b64encode(c.encode()).decode(),
             "payloadType": "InlineBase64"} for p, c in parts.items()]}}

    ok = True

    def check(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  {'PASS' if cond else 'FAIL'}  {name}")

    # 1. Identical -> unchanged.
    a = defn({"a.json": '{"x": 1, "y": 2}'})
    check("identical -> not changed", diff_definitions(a, a)["changed"] is False)

    # 2. Auto-rebound field only -> normalized away.
    src = defn({"pipeline.json": '{"notebookId": "AAA", "cmd": "run"}'})
    tgt = defn({"pipeline.json": '{"notebookId": "BBB", "cmd": "run"}'})
    check("rebound-only -> not changed (normalized)", diff_definitions(src, tgt)["changed"] is False)
    check("rebound-only -> changed when --no-normalize",
          diff_definitions(src, tgt, normalize=False)["changed"] is True)

    # 3. Real JSON edit -> reported, and only the edited leaf.
    src = defn({"m.json": '{"notebookId": "AAA", "rows": 10}'})
    tgt = defn({"m.json": '{"notebookId": "BBB", "rows": 20}'})
    r = diff_definitions(src, tgt)
    changes = r["diffs"][0]["changes"] if r["changed"] else []
    check("real edit -> exactly one change", len(changes) == 1)
    check("real edit -> correct path/values",
          bool(changes) and changes[0]["path"] == "$.rows"
          and changes[0]["old"] == 10 and changes[0]["new"] == 20)

    # 4. Text part -> unified diff.
    src = defn({"nb.py": "print('a')\nprint('b')\n"})
    tgt = defn({"nb.py": "print('a')\nprint('c')\n"})
    r = diff_definitions(src, tgt)
    check("text edit -> changed", r["changed"] is True)
    check("text edit -> unified diff emitted",
          bool(r["diffs"]) and "unifiedDiff" in r["diffs"][0])

    # 5. Added / removed parts.
    r = diff_definitions(defn({"a.json": "{}"}), defn({"a.json": "{}", "b.json": "{}"}))
    check("added part detected", any(d["kind"] == "added-part" for d in r["diffs"]))

    # 6. Bare-definition shape (no top-level 'definition') is accepted.
    bare = {"parts": a["definition"]["parts"]}
    check("bare {parts:[...]} shape accepted", diff_definitions(bare, bare)["changed"] is False)

    print("SELFTEST:", "OK" if ok else "FAILED")
    return ok


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Diff two Fabric item definitions, emitting only the differences.")
    parser.add_argument("source", nargs="?", help="source-stage getDefinition JSON (file or '-')")
    parser.add_argument("target", nargs="?", help="target-stage getDefinition JSON (file or '-')")
    parser.add_argument("--format", choices=["json", "text"], default="json",
                        help="output format (default: json)")
    parser.add_argument("--context", type=int, default=3,
                        help="unified-diff context lines for text parts (default: 3)")
    parser.add_argument("--max-value", type=int, default=200,
                        help="truncate JSON diff values longer than N chars (0 = no limit)")
    parser.add_argument("--no-normalize", action="store_true",
                        help="do NOT blank auto-rebound binding fields (may cause false positives)")
    parser.add_argument("--normalize-keys",
                        help="comma-separated override of the fields to normalize")
    parser.add_argument("--quiet", action="store_true",
                        help="print nothing; rely on the exit code (0=same, 1=differ)")
    parser.add_argument("--selftest", action="store_true", help="run built-in tests and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return 0 if _selftest() else 1

    if not args.source or not args.target:
        parser.error("source and target are required (unless --selftest)")
    if args.source == "-" and args.target == "-":
        parser.error("only one of source/target may read from stdin ('-')")

    keys = None
    if args.normalize_keys:
        keys = [k.strip() for k in args.normalize_keys.split(",") if k.strip()]

    try:
        result = diff_definitions(
            load_definition(args.source),
            load_definition(args.target),
            keys=keys,
            normalize=not args.no_normalize,
            context=args.context,
            limit=args.max_value,
        )
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not args.quiet:
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(render_text(result))

    return 1 if result["changed"] else 0


if __name__ == "__main__":
    sys.exit(main())

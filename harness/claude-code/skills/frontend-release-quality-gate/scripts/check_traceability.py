#!/usr/bin/env python3
"""Validate frontend acceptance traceability and safe evidence references."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ID_PATTERNS = {
    "id": re.compile(r"^TR-[0-9]{3,}$"),
    "story_id": re.compile(r"^US-[0-9]{3,}$"),
    "acceptance_id": re.compile(r"^AC-[0-9]{3,}$"),
    "scenario_id": re.compile(r"^SC-[0-9]{3,}$"),
}
RISKS = {"critical", "high", "medium", "low"}
LAYERS = {
    "static",
    "unit",
    "component",
    "mocked-integration",
    "contract",
    "service-integration",
    "end-to-end",
    "visual-regression",
    "accessibility",
    "performance",
    "discoverability",
    "mobile-desktop",
    "manual",
}
RESULTS = {"pass", "fail", "manual", "not-applicable", "blocked"}
EVIDENCE_TYPES = {"path", "command", "manual"}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"traceability file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def safe_evidence_path(root: Path, reference: str) -> Path:
    candidate = Path(reference)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe evidence path: {reference}")
    resolved_root = root.resolve(strict=True)
    unresolved = resolved_root / candidate
    current = resolved_root
    for part in candidate.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"symlinked evidence path is not allowed: {reference}")
    try:
        resolved = unresolved.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"evidence path does not exist: {reference}") from exc
    if resolved_root != resolved and resolved_root not in resolved.parents:
        raise ValueError(f"evidence path escapes root: {reference}")
    if not resolved.is_file():
        raise ValueError(f"evidence path is not a regular file: {reference}")
    return resolved


def required_string(
    entry: dict[str, Any], field: str, index: int, errors: list[str]
) -> str | None:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"entry {index}: missing non-empty {field}")
        return None
    return value.strip()


def validate_entry(
    entry: Any, index: int, root: Path, seen_ids: set[str], seen_pairs: set[tuple[str, str]]
) -> list[str]:
    errors: list[str] = []
    if not isinstance(entry, dict):
        return [f"entry {index}: must be an object"]

    values: dict[str, str] = {}
    for field, pattern in ID_PATTERNS.items():
        value = required_string(entry, field, index, errors)
        if value is not None:
            values[field] = value
            if not pattern.fullmatch(value):
                errors.append(f"entry {index}: invalid {field} {value!r}")

    trace_id = values.get("id")
    if trace_id is not None:
        if trace_id in seen_ids:
            errors.append(f"entry {index}: duplicate trace id {trace_id}")
        seen_ids.add(trace_id)

    acceptance = values.get("acceptance_id")
    scenario = values.get("scenario_id")
    if acceptance is not None and scenario is not None:
        pair = (acceptance, scenario)
        if pair in seen_pairs:
            errors.append(
                f"entry {index}: duplicate acceptance/scenario mapping {acceptance}/{scenario}"
            )
        seen_pairs.add(pair)

    risk = required_string(entry, "risk", index, errors)
    if risk is not None and risk not in RISKS:
        errors.append(f"entry {index}: unsupported risk {risk!r}")

    layer = required_string(entry, "test_layer", index, errors)
    if layer is not None and layer not in LAYERS:
        errors.append(f"entry {index}: unsupported test_layer {layer!r}")

    result = required_string(entry, "result", index, errors)
    if result is not None and result not in RESULTS:
        errors.append(f"entry {index}: unsupported result {result!r}")

    evidence = entry.get("evidence")
    if not isinstance(evidence, dict):
        errors.append(f"entry {index}: evidence must be an object")
    else:
        evidence_type = evidence.get("type")
        reference = evidence.get("reference")
        if evidence_type not in EVIDENCE_TYPES:
            errors.append(f"entry {index}: unsupported evidence type {evidence_type!r}")
        if not isinstance(reference, str) or not reference.strip():
            errors.append(f"entry {index}: evidence reference must be non-empty")
        elif evidence_type == "path":
            try:
                safe_evidence_path(root, reference.strip())
            except (OSError, ValueError) as exc:
                errors.append(f"entry {index}: {exc}")

    if result == "manual":
        required_string(entry, "manual_procedure", index, errors)
        if isinstance(evidence, dict) and evidence.get("type") != "manual":
            errors.append(f"entry {index}: manual result requires manual evidence")
    if result == "fail":
        required_string(entry, "defect_id", index, errors)
        required_string(entry, "retest", index, errors)
    if result in {"blocked", "not-applicable"}:
        required_string(entry, "limitation", index, errors)

    return errors


def validate_traceability(data: Any, root: Path) -> tuple[list[str], Counter[str]]:
    errors: list[str] = []
    results: Counter[str] = Counter()
    if not isinstance(data, dict):
        return ["traceability root must be an object"], results
    if data.get("version") != 1:
        errors.append("version must equal 1")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries must be a non-empty array")
        return errors, results

    seen_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    for index, entry in enumerate(entries, start=1):
        errors.extend(validate_entry(entry, index, root, seen_ids, seen_pairs))
        if isinstance(entry, dict) and isinstance(entry.get("result"), str):
            results[entry["result"]] += 1
    return errors, results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traceability", type=Path, help="Traceability JSON file")
    parser.add_argument(
        "--root",
        type=Path,
        help="Root for path evidence (default: traceability file directory)",
    )
    parser.add_argument("--json", action="store_true", help="Emit a JSON summary")
    args = parser.parse_args(argv)

    traceability = args.traceability.resolve()
    root = (args.root or traceability.parent).resolve()
    try:
        data = load_json(traceability)
        if not root.is_dir() or root.is_symlink():
            raise ValueError(f"evidence root is not a regular directory: {root}")
        errors, results = validate_traceability(data, root)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
        results = Counter()

    payload = {
        "status": "valid" if not errors else "invalid",
        "traceability": str(traceability),
        "evidence_root": str(root),
        "results": dict(sorted(results.items())),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        summary = ", ".join(f"{key}={value}" for key, value in sorted(results.items()))
        print(f"Traceability valid: {summary}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

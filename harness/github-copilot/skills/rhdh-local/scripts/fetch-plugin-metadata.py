#!/usr/bin/env python3
"""Fetch RHDH plugin metadata from the plugin-export-overlays repository.

Replaces the manual 3-step curl chain in the enable-plugin workflow.
Fetches plugin definition YAML + per-package metadata and outputs
a structured summary (human-readable or JSON).

Uses only Python stdlib (no PyYAML, no external deps).
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any

# ---------------------------------------------------------------------------
# GitHub URLs
# ---------------------------------------------------------------------------
_CONTENTS_URL = (
    "https://api.github.com/repos/redhat-developer/rhdh-plugin-export-overlays"
    "/contents/catalog-entities/extensions/plugins"
)
_RAW_BASE = "https://raw.githubusercontent.com/redhat-developer/rhdh-plugin-export-overlays/main"

# ANSI helpers
_RED = "\033[0;31m"
_GREEN = "\033[0;32m"
_YELLOW = "\033[1;33m"
_BLUE = "\033[0;34m"
_BOLD = "\033[1m"
_NC = "\033[0m"


# ---------------------------------------------------------------------------
# Minimal YAML parser (stdlib-only)
# ---------------------------------------------------------------------------


def _parse_yaml(text: str) -> dict[str, Any]:
    """Parse the subset of YAML used in plugin-export-overlays files.

    Handles:
      - key: value scalars (strings, numbers, booleans)
      - Nested mappings (indentation-based)
      - Lists with ``- item`` syntax (scalar items and mapping items)
      - Block scalars following a bare ``key:`` line (collected as string)
      - Quoted strings (single and double)
      - YAML document separators (``---``)

    Does NOT handle: anchors/aliases, flow sequences ``[a, b]``,
    multi-document streams, merge keys, complex keys, tags.
    """
    lines = text.splitlines()
    return _parse_mapping(lines, 0, 0)[0]


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def _strip_quotes(val: str) -> str:
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
        return val[1:-1]
    return val


def _strip_inline_comment(val: str) -> str:
    """Remove a trailing ``# comment`` from a scalar value.

    Respects quoted strings - only strips if the ``#`` is preceded by
    whitespace and is outside of quotes.
    """
    in_single = False
    in_double = False
    prev_space = False
    for i, ch in enumerate(val):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double and prev_space:
            return val[:i].rstrip()
        prev_space = ch == " "
    return val


def _scalar(val: str) -> Any:
    """Convert a YAML scalar string to a Python object."""
    v = _strip_inline_comment(val).strip()
    if v in ("true", "True", "yes"):
        return True
    if v in ("false", "False", "no"):
        return False
    if v in ("null", "~", ""):
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    # Handle flow sequences/mappings (minimal)
    if v == "[]":
        return []
    if v == "{}":
        return {}
    return _strip_quotes(v)


def _parse_mapping(lines: list[str], idx: int, base_indent: int) -> tuple[dict[str, Any], int]:
    """Parse a YAML mapping starting at *idx* with indentation *base_indent*."""
    result: dict[str, Any] = {}

    while idx < len(lines):
        line = lines[idx]

        # Skip blanks, comments, document separators
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "---":
            idx += 1
            continue

        cur_indent = _indent_of(line)

        # Done with this mapping if we've dedented
        if cur_indent < base_indent:
            break

        # Skip lines at deeper indent (shouldn't happen in well-formed input
        # since we consume children, but guard anyway)
        if cur_indent > base_indent:
            idx += 1
            continue

        # List item at mapping level? This happens when the mapping value
        # is implicitly a list.  We shouldn't get here normally because
        # lists are consumed by _parse_list, but be safe.
        if stripped.startswith("- "):
            idx += 1
            continue

        # Must be a key line
        colon_pos = stripped.find(":")
        if colon_pos == -1:
            idx += 1
            continue

        key = stripped[:colon_pos].strip()
        after_colon = stripped[colon_pos + 1 :].strip()

        if after_colon and not after_colon.startswith("#"):
            # Inline scalar value
            result[key] = _scalar(after_colon)
            idx += 1
        else:
            # Look ahead for child content
            child_indent = None
            peek = idx + 1
            while peek < len(lines):
                pl = lines[peek]
                ps = pl.strip()
                if ps and not ps.startswith("#") and ps != "---":
                    child_indent = _indent_of(pl)
                    break
                peek += 1

            if child_indent is None or child_indent <= cur_indent:
                # No child block → null / empty
                result[key] = None
                idx += 1
            elif lines[peek].strip().startswith("- "):
                # Child is a list
                result[key], idx = _parse_list(lines, peek, child_indent)
            else:
                # Check if it looks like a block scalar (no colon in children)
                first_child = lines[peek].strip()
                if ":" in first_child:
                    # Nested mapping
                    result[key], idx = _parse_mapping(lines, peek, child_indent)
                else:
                    # Block scalar – collect all indented lines
                    block_lines: list[str] = []
                    bi = peek
                    while bi < len(lines):
                        bl = lines[bi]
                        bs = bl.strip()
                        if not bs or bs.startswith("#"):
                            block_lines.append("")
                            bi += 1
                            continue
                        if _indent_of(bl) < child_indent:
                            break
                        block_lines.append(bl.strip())
                        bi += 1
                    # Trim trailing blanks
                    while block_lines and not block_lines[-1]:
                        block_lines.pop()
                    result[key] = "\n".join(block_lines)
                    idx = bi

    return result, idx


def _parse_list(lines: list[str], idx: int, base_indent: int) -> tuple[list[Any], int]:
    """Parse a YAML list starting at *idx*."""
    result: list[Any] = []

    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        if not stripped or stripped.startswith("#") or stripped == "---":
            idx += 1
            continue

        cur_indent = _indent_of(line)
        if cur_indent < base_indent:
            break
        if cur_indent > base_indent:
            # Continuation of previous item (nested) – skip, already consumed
            idx += 1
            continue

        if not stripped.startswith("- "):
            # Not a list item – end of list
            break

        item_text = stripped[2:].strip()

        # Check if item is a mapping (has a colon)
        if ":" in item_text:
            # Inline mapping item – first key:value is on this line
            colon_pos = item_text.find(":")
            first_key = item_text[:colon_pos].strip()
            first_val_str = item_text[colon_pos + 1 :].strip()

            item_dict: dict[str, Any] = {}

            # The effective indent for continuation keys is dash_indent + 2
            item_indent = cur_indent + 2

            if first_val_str and not first_val_str.startswith("#"):
                item_dict[first_key] = _scalar(first_val_str)
                idx += 1
            else:
                # Value on subsequent lines
                peek = idx + 1
                child_indent = None
                while peek < len(lines):
                    pl = lines[peek]
                    ps = pl.strip()
                    if ps and not ps.startswith("#") and ps != "---":
                        child_indent = _indent_of(pl)
                        break
                    peek += 1

                if child_indent is not None and child_indent > item_indent:
                    if lines[peek].strip().startswith("- "):
                        item_dict[first_key], idx = _parse_list(lines, peek, child_indent)
                    else:
                        first_child = lines[peek].strip()
                        if ":" in first_child:
                            item_dict[first_key], idx = _parse_mapping(lines, peek, child_indent)
                        else:
                            item_dict[first_key] = _scalar(first_child)
                            idx = peek + 1
                else:
                    item_dict[first_key] = None
                    idx += 1

            # Continue reading sibling keys at item_indent
            rest, idx = _parse_mapping(lines, idx, item_indent)
            item_dict.update(rest)
            result.append(item_dict)
        else:
            # Simple scalar item
            result.append(_scalar(item_text))
            idx += 1

    return result, idx


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _fetch(url: str) -> bytes:
    """Fetch *url* and return the response body bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": "rhdh-skill/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def _fetch_json(url: str) -> Any:
    return json.loads(_fetch(url))


def _fetch_yaml(url: str) -> dict[str, Any]:
    return _parse_yaml(_fetch(url).decode("utf-8"))


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def list_plugins() -> list[str]:
    """Return sorted list of available plugin names."""
    entries = _fetch_json(_CONTENTS_URL)
    names: list[str] = []
    for entry in entries:
        name = entry.get("name", "")
        if name.endswith(".yaml"):
            names.append(name[: -len(".yaml")])
    names.sort()
    return names


def _get(d: dict, *keys: str, default: Any = None) -> Any:
    """Nested dict get."""
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k, default)
    return cur


def _list_workspace_metadata(workspace: str) -> list[str]:
    """List metadata file names (without .yaml) in a workspace.

    Returns an empty list if the workspace or metadata dir doesn't exist.
    """
    url = (
        f"https://api.github.com/repos/redhat-developer/"
        f"rhdh-plugin-export-overlays/contents/workspaces/{workspace}/metadata"
    )
    try:
        entries = _fetch_json(url)
    except urllib.error.HTTPError:
        return []
    names: list[str] = []
    for entry in entries:
        fname = entry.get("name", "")
        if fname.endswith(".yaml"):
            names.append(fname[: -len(".yaml")])
    return names


def _normalize_pkg_name(name: str) -> str:
    """Normalize a package name for fuzzy matching.

    Strips common prefixes/vendor names and suffixes so that
    ``backstage-community-plugin-redhat-argocd-backend`` and
    ``backstage-community-plugin-argocd-backend`` produce the same
    core identifier.
    """
    n = name
    # Strip common prefixes
    for pfx in (
        "backstage-community-plugin-",
        "backstage-plugin-",
        "janus-idp-backstage-plugin-",
        "@backstage-community/plugin-",
        "@backstage/plugin-",
        "@janus-idp/",
        "@red-hat-developer-hub/",
    ):
        if n.startswith(pfx):
            n = n[len(pfx) :]
            break

    # Strip vendor insertions (e.g. "redhat-") that appear before
    # the plugin's core name
    for vendor in ("redhat-", "red-hat-"):
        if n.startswith(vendor):
            n = n[len(vendor) :]
            break

    return n


def _find_metadata_file(
    pkg_name: str,
    workspace: str,
    available: list[str],
) -> tuple[str, str] | None:
    """Find the metadata file for *pkg_name* in *workspace*.

    Tries exact match first, then normalizes both sides and picks the
    best fuzzy match (handles the redhat-argocd → argocd mapping where
    metadata file is ``backstage-community-plugin-argocd`` but the
    package is ``backstage-community-plugin-redhat-argocd``).

    Returns ``(workspace, matched_file_name)`` or ``None``.
    """
    if pkg_name in available:
        return workspace, pkg_name

    # Normalize and match
    norm_pkg = _normalize_pkg_name(pkg_name)
    best: str | None = None
    best_len = 0
    for candidate in available:
        norm_cand = _normalize_pkg_name(candidate)
        if norm_cand == norm_pkg:
            return workspace, candidate
        # Partial: one contains the other after normalization
        if norm_cand in norm_pkg or norm_pkg in norm_cand:
            if len(candidate) > best_len:
                best = candidate
                best_len = len(candidate)
    if best:
        return workspace, best

    return None


def fetch_plugin_metadata(plugin_name: str) -> dict[str, Any]:
    """Fetch plugin definition + per-package metadata.

    Returns a structured dict with plugin info and package details.
    """
    # Step 1: plugin definition
    plugin_url = f"{_RAW_BASE}/catalog-entities/extensions/plugins/{plugin_name}.yaml"
    try:
        plugin_def = _fetch_yaml(plugin_url)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {"error": "not_found", "plugin": plugin_name}
        raise

    metadata_name = _get(plugin_def, "metadata", "name", default=plugin_name)
    packages = _get(plugin_def, "spec", "packages", default=[])
    categories = _get(plugin_def, "spec", "categories", default=[])

    # Detect pre-installed
    annotations = _get(plugin_def, "metadata", "annotations", default={})
    pre_installed = False
    if isinstance(annotations, dict):
        pre_installed = annotations.get("extensions.backstage.io/pre-installed", "") in (
            "true",
            "True",
            True,
        )

    # Step 2: per-package metadata
    # Pre-fetch the workspace metadata directory listing for the primary workspace
    primary_available = _list_workspace_metadata(plugin_name)

    package_results: list[dict[str, Any]] = []
    for pkg in packages:
        pkg_name = pkg if isinstance(pkg, str) else str(pkg)
        pkg_def: dict[str, Any] = {}

        # Try to find the metadata file in the primary workspace
        match = _find_metadata_file(pkg_name, plugin_name, primary_available)

        # Fallback: try workspaces derived from the package name,
        # plus the "backstage" workspace (home of many core plugins)
        if match is None:
            fallback_workspaces: list[str] = []
            alt_ws = _derive_workspace(pkg_name)
            if alt_ws and alt_ws != plugin_name:
                fallback_workspaces.append(alt_ws)
            if "backstage" not in (plugin_name, alt_ws):
                fallback_workspaces.append("backstage")
            for ws in fallback_workspaces:
                alt_available = _list_workspace_metadata(ws)
                match = _find_metadata_file(pkg_name, ws, alt_available)
                if match is not None:
                    break

        if match is not None:
            ws, file_name = match
            pkg_url = f"{_RAW_BASE}/workspaces/{ws}/metadata/{file_name}.yaml"
            try:
                pkg_def = _fetch_yaml(pkg_url)
            except urllib.error.HTTPError:
                pkg_def = {}

        dynamic_artifact = _get(pkg_def, "spec", "dynamicArtifact", default=None)
        role = _get(pkg_def, "spec", "backstage", "role", default=None)
        app_config_examples = _get(pkg_def, "spec", "appConfigExamples", default=None)
        part_of = _get(pkg_def, "spec", "partOf", default=None)

        pkg_result: dict[str, Any] = {"name": pkg_name}
        if dynamic_artifact:
            pkg_result["dynamicArtifact"] = dynamic_artifact
        if role:
            pkg_result["role"] = role
        if app_config_examples:
            pkg_result["appConfigExamples"] = app_config_examples
        if part_of:
            pkg_result["partOf"] = part_of

        package_results.append(pkg_result)

    return {
        "plugin": metadata_name,
        "categories": categories,
        "preInstalled": pre_installed,
        "packages": package_results,
    }


def _derive_workspace(package_name: str) -> str | None:
    """Best-effort workspace name from a package name.

    Strips common prefixes like ``backstage-plugin-`` and suffixes like
    ``-backend``, ``-common``, ``-react`` to guess the workspace directory.
    """
    name = package_name
    for prefix in (
        "@red-hat-developer-hub/",
        "@backstage-community/plugin-",
        "@backstage/plugin-",
        "@janus-idp/",
        "backstage-community-plugin-",
        "backstage-plugin-",
        "janus-idp-backstage-plugin-",
    ):
        if name.startswith(prefix):
            name = name[len(prefix) :]
            break
    # Strip vendor insertions
    for vendor in ("redhat-", "red-hat-"):
        if name.startswith(vendor):
            name = name[len(vendor) :]
            break
    for suffix in ("-backend", "-common", "-react", "-module", "-node"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name or None


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def _print_human_list(plugins: list[str]) -> None:
    print(f"{_BOLD}Available plugins ({len(plugins)}):{_NC}\n")
    for name in plugins:
        print(f"  {name}")


def _print_human_metadata(data: dict[str, Any]) -> None:
    if "error" in data:
        print(
            f"{_RED}Plugin not found:{_NC} {data['plugin']}",
            file=sys.stderr,
        )
        return

    print(f"{_BOLD}Plugin:{_NC} {data['plugin']}")
    if data.get("categories"):
        cats = data["categories"]
        if isinstance(cats, list):
            print(f"{_BOLD}Categories:{_NC} {', '.join(str(c) for c in cats)}")
        else:
            print(f"{_BOLD}Categories:{_NC} {cats}")

    if data.get("preInstalled"):
        print(f"{_YELLOW}! Pre-installed (bundled with RHDH){_NC}")

    print(f"\n{_BOLD}Packages ({len(data.get('packages', []))}):{_NC}")
    for pkg in data.get("packages", []):
        role = pkg.get("role", "unknown")
        role_color = _BLUE if "frontend" in str(role) else _GREEN
        print(f"\n  {_BOLD}{pkg['name']}{_NC}")
        print(f"    Role: {role_color}{role}{_NC}")
        artifact = pkg.get("dynamicArtifact")
        if artifact:
            print(f"    Artifact: {artifact}")
        part_of = pkg.get("partOf")
        if part_of:
            if isinstance(part_of, list):
                print(f"    Part of: {', '.join(str(p) for p in part_of)}")
            else:
                print(f"    Part of: {part_of}")
        examples = pkg.get("appConfigExamples")
        if examples:
            print(f"    {_YELLOW}Has appConfigExamples{_NC}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fetch-plugin-metadata",
        description=(
            "Fetch RHDH plugin metadata from the plugin-export-overlays "
            "repository. Lists available plugins or retrieves detailed "
            "metadata (OCI artifacts, roles, config examples) for a "
            "specific plugin."
        ),
    )
    parser.add_argument(
        "plugin",
        nargs="?",
        help="Plugin name to fetch metadata for (e.g. argocd, kubernetes)",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output structured JSON instead of human-readable text",
    )
    parser.add_argument(
        "--list",
        dest="list_plugins",
        action="store_true",
        default=False,
        help="List all available plugins",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_plugins:
        try:
            plugins = list_plugins()
        except (urllib.error.URLError, OSError) as exc:
            if args.json_output:
                print(json.dumps({"success": False, "error": str(exc)}, indent=2))
            else:
                print(f"{_RED}Error:{_NC} {exc}", file=sys.stderr)
            return 1

        if args.json_output:
            print(json.dumps({"success": True, "plugins": plugins}, indent=2))
        else:
            _print_human_list(plugins)
        return 0

    if not args.plugin:
        parser.error("plugin name is required (or use --list)")
        return 2  # argparse exits on error, but be explicit

    try:
        data = fetch_plugin_metadata(args.plugin)
    except (urllib.error.URLError, OSError) as exc:
        if args.json_output:
            print(json.dumps({"success": False, "error": str(exc)}, indent=2))
        else:
            print(f"{_RED}Error:{_NC} {exc}", file=sys.stderr)
        return 1

    if "error" in data:
        if args.json_output:
            print(json.dumps({"success": False, **data}, indent=2))
        else:
            _print_human_metadata(data)
        return 1

    if args.json_output:
        print(json.dumps({"success": True, **data}, indent=2))
    else:
        _print_human_metadata(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())

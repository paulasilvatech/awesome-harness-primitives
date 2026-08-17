#!/usr/bin/env python3
"""Generate docs/CATALOG.md from the primitive manifests in this repository."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from library.scripts.validate_primitives import PLUGIN_MANIFESTS, parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "docs" / "CATALOG.md"
DESCRIPTION_WIDTH = 180
HOOK_EVENT_ORDER = [
    "sessionStart",
    "sessionEnd",
    "userPromptSubmitted",
    "userPromptTransformed",
    "preToolUse",
    "postToolUse",
    "postToolUseFailure",
    "preMcpToolCall",
    "permissionRequest",
    "preCompact",
    "errorOccurred",
    "agentStop",
    "subagentStart",
    "subagentStop",
    "notification",
    "postResult",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def one_line(value: Any, default: str = "—") -> str:
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    if value is None:
        return default
    text = " ".join(str(value).split())
    return text or default


def truncate(value: Any, width: int = DESCRIPTION_WIDTH) -> str:
    text = one_line(value)
    if text == "—" or len(text) <= width:
        return text
    return text[: max(0, width - 1)].rstrip() + "…"


def escape_cell(value: Any) -> str:
    return one_line(value).replace("|", "\\|")


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(cell)
                     for cell in row) + " |")
    return "\n".join(lines)


def frontmatter(path: Path, required: bool = True) -> dict[str, Any]:
    fm, _body, present, err = parse_frontmatter(
        read_text(path), required=required)
    if not present or err or not isinstance(fm, dict):
        return {}
    return fm


def sort_rows(rows: list[list[str]]) -> list[list[str]]:
    return sorted(rows, key=lambda row: tuple(cell.casefold() for cell in row))


def agent_rows() -> list[list[str]]:
    rows = []
    for path in sorted((ROOT / "agents").glob("*.agent.md"), key=lambda p: p.name.casefold()):
        fm = frontmatter(path)
        name = fm.get("name") or path.name.removesuffix(".agent.md")
        rows.append([one_line(name), truncate(fm.get("description"))])
    return sort_rows(rows)


def instruction_rows() -> list[list[str]]:
    rows = []
    for path in sorted((ROOT / "instructions").glob("*.instructions.md"), key=lambda p: p.name.casefold()):
        fm = frontmatter(path, required=False)
        name = fm.get("name") or path.name.removesuffix(".instructions.md")
        rows.append([one_line(name), one_line(fm.get("applyTo")),
                    truncate(fm.get("description"))])
    return sort_rows(rows)


def skill_rows() -> list[list[str]]:
    rows = []
    for path in sorted((ROOT / "skills").glob("*/SKILL.md"), key=lambda p: p.parent.name.casefold()):
        fm = frontmatter(path)
        name = fm.get("name") or path.parent.name
        rows.append([one_line(name), truncate(fm.get("description"))])
    return sort_rows(rows)


def plugin_manifest(plugin_dir: Path) -> Path | None:
    for rel in PLUGIN_MANIFESTS:
        path = plugin_dir / rel
        if path.exists():
            return path
    return None


def plugin_rows() -> list[list[str]]:
    rows = []
    plugin_dirs = [p for p in (ROOT / "plugins").iterdir()
                   if p.is_dir()] if (ROOT / "plugins").is_dir() else []
    for plugin_dir in sorted(plugin_dirs, key=lambda p: p.name.casefold()):
        manifest = plugin_manifest(plugin_dir)
        data: dict[str, Any] = {}
        if manifest is not None:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        rows.append([
            one_line(data.get("name") or plugin_dir.name),
            one_line(data.get("version")),
            truncate(data.get("description")),
        ])
    return sort_rows(rows)


def hook_rows() -> list[list[str]]:
    rows = []
    event_order = {event: idx for idx, event in enumerate(HOOK_EVENT_ORDER)}
    for path in sorted((ROOT / "hooks").glob("*/hooks.json"), key=lambda p: p.parent.name.casefold()):
        data = json.loads(path.read_text(encoding="utf-8"))
        hooks = data.get("hooks", {})
        events = sorted(hooks, key=lambda e: (event_order.get(
            e, len(event_order)), e.casefold())) if isinstance(hooks, dict) else []
        rows.append([path.parent.name, ", ".join(events) if events else "—"])
    return sort_rows(rows)


def build_catalog() -> str:
    agents = agent_rows()
    instructions = instruction_rows()
    skills = skill_rows()
    plugins = plugin_rows()
    hooks = hook_rows()

    return f"""# Copilot Primitives Catalog

Generated from the current repository contents by `python3 scripts/generate_catalog.py`.
Regenerate this file after changing files under `agents/`, `instructions/`, `skills/`, `plugins/`, or `hooks/`.

## Summary

| Primitive type | Count |
| --- | ---: |
| Agents | {len(agents)} |
| Instructions | {len(instructions)} |
| Skills | {len(skills)} |
| Plugins | {len(plugins)} |
| Hooks | {len(hooks)} |

## Agents

{md_table(["Agent", "Description"], agents)}

## Instructions

{md_table(["Instruction", "applyTo", "Description"], instructions)}

## Skills

{md_table(["Skill", "Description"], skills)}

## Plugins

{md_table(["Plugin", "Version", "Description"], plugins)}

## Hooks

{md_table(["Hook package", "Events"], hooks)}
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the Copilot primitives catalog.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="output path (default: docs/CATALOG.md)")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if the output file is stale; do not write")
    args = parser.parse_args(argv)

    out = args.out if args.out.is_absolute() else ROOT / args.out
    content = build_catalog()
    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != content:
            print(
                f"{out.relative_to(ROOT)} is stale; run python3 scripts/generate_catalog.py", file=sys.stderr)
            return 1
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate docs/CATALOG.md from the primitive manifests in this repository."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    from _layout import HARNESS_ROOT, REPO_ROOT
    from _plugin_governance import classify
    from _plugin_sources import load_plugin_sources
    from validate_primitives import PLUGIN_MANIFESTS, parse_frontmatter
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._layout import HARNESS_ROOT, REPO_ROOT
    from ._plugin_governance import classify
    from ._plugin_sources import load_plugin_sources
    from .validate_primitives import PLUGIN_MANIFESTS, parse_frontmatter

DEFAULT_OUT = REPO_ROOT / "docs" / "CATALOG.md"
SOURCE_ROOT = HARNESS_ROOT
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
    for path in sorted((SOURCE_ROOT / "agents").glob("*.agent.md"), key=lambda p: p.name.casefold()):
        fm = frontmatter(path)
        name = fm.get("name") or path.name.removesuffix(".agent.md")
        rows.append([one_line(name), truncate(fm.get("description"))])
    return sort_rows(rows)


def instruction_rows() -> list[list[str]]:
    rows = []
    for path in sorted((SOURCE_ROOT / "instructions").glob("*.instructions.md"), key=lambda p: p.name.casefold()):
        fm = frontmatter(path, required=False)
        name = fm.get("name") or path.name.removesuffix(".instructions.md")
        rows.append([one_line(name), one_line(fm.get("applyTo")),
                    truncate(fm.get("description"))])
    return sort_rows(rows)


def skill_rows() -> list[list[str]]:
    rows = []
    for path in sorted((SOURCE_ROOT / "skills").glob("*/SKILL.md"), key=lambda p: p.parent.name.casefold()):
        fm = frontmatter(path)
        name = fm.get("name") or path.parent.name
        rows.append([one_line(name), truncate(fm.get("description"))])
    return sort_rows(rows)


def prompt_rows() -> list[list[str]]:
    rows = []
    for path in sorted(
        (SOURCE_ROOT / "prompts").glob("*.prompt.md"),
        key=lambda p: p.name.casefold(),
    ):
        fm = frontmatter(path)
        name = fm.get("name") or path.name.removesuffix(".prompt.md")
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
    source_map = load_plugin_sources()
    as_of = date.today()
    plugin_dirs = [p for p in (SOURCE_ROOT / "plugins").iterdir()
                   if p.is_dir()] if (SOURCE_ROOT / "plugins").is_dir() else []
    for plugin_dir in sorted(plugin_dirs, key=lambda p: p.name.casefold()):
        manifest = plugin_manifest(plugin_dir)
        data: dict[str, Any] = {}
        if manifest is not None:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        mcp_path = plugin_dir / "mcp.json"
        mcp_servers = 0
        if mcp_path.is_file():
            mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
            servers = mcp.get("mcpServers")
            mcp_servers = len(servers) if isinstance(servers, dict) else 0
        source_config = source_map.get(plugin_dir.name, {})
        extensions = source_config.get("extensionSources") or []
        classification = classify(
            version=data.get("version"),
            source_config=source_config,
            mcp_servers=mcp_servers,
            hooks=1 if source_config.get("hookSource") else 0,
            extensions=len(extensions),
            as_of=as_of,
        )
        rows.append([
            one_line(data.get("name") or plugin_dir.name),
            one_line(data.get("version")),
            classification.lifecycle,
            classification.assurance,
            classification.provenance,
            truncate(data.get("description")),
        ])
    return sort_rows(rows)


def hook_rows() -> list[list[str]]:
    rows = []
    event_order = {event: idx for idx, event in enumerate(HOOK_EVENT_ORDER)}
    for path in sorted((SOURCE_ROOT / "hooks").glob("*/hooks.json"), key=lambda p: p.parent.name.casefold()):
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
    prompts = prompt_rows()
    plugins = plugin_rows()
    hooks = hook_rows()

    return f"""# Copilot Primitives Catalog

Generated from the current repository contents by `python3 harness/github-copilot/scripts/generate_catalog.py`.
Regenerate this file after changing files under `harness/github-copilot/agents/`, `harness/github-copilot/instructions/`, `harness/github-copilot/skills/`, `harness/github-copilot/prompts/`, `harness/github-copilot/plugins/`, or `harness/github-copilot/hooks/`.

## Summary

| Primitive type | Count |
| --- | ---: |
| Agents | {len(agents)} |
| Instructions | {len(instructions)} |
| Skills | {len(skills)} |
| VS Code prompts | {len(prompts)} |
| Plugins | {len(plugins)} |
| Hooks | {len(hooks)} |

## Agents

{md_table(["Agent", "Description"], agents)}

## Instructions

{md_table(["Instruction", "applyTo", "Description"], instructions)}

## Skills

{md_table(["Skill", "Description"], skills)}

## VS Code Prompts

{md_table(["Prompt", "Description"], prompts)}

## Plugins

Lifecycle, assurance, and provenance are descriptive classifications generated from repository evidence.
They exist to filter a large marketplace and never remove, hide, or block a package.

{md_table(["Plugin", "Version", "Lifecycle", "Assurance", "Provenance", "Description"], plugins)}

## Hooks

{md_table(["Hook package", "Events"], hooks)}
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the Copilot primitives catalog.")
    parser.add_argument(
        "--root",
        type=Path,
        default=HARNESS_ROOT,
        help="canonical harness root (default: <repo>/harness/github-copilot)",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="output path (default: docs/CATALOG.md)")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if the output file is stale; do not write")
    args = parser.parse_args(argv)

    global SOURCE_ROOT
    SOURCE_ROOT = args.root.resolve()
    out = args.out if args.out.is_absolute() else REPO_ROOT / args.out
    content = build_catalog()
    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != content:
            print(
                f"{out.relative_to(REPO_ROOT)} is stale; run python3 harness/github-copilot/scripts/generate_catalog.py", file=sys.stderr)
            return 1
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

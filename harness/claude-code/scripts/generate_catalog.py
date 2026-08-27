#!/usr/bin/env python3
"""Generate the Claude Code harness catalog.

Writes ``CLAUDE-CODE-CATALOG.md`` at the repository root with one row per
generated Claude Code primitive. ``--check`` fails when the committed catalog has
drifted from the harness.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from _convert import parse_frontmatter
    from _layout import (
        AGENTS_ROOT,
        COMMANDS_ROOT,
        HOOKS_ROOT,
        PLUGINS_ROOT,
        REPO_ROOT,
        RULES_ROOT,
        SKILLS_ROOT,
    )
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._convert import parse_frontmatter  # type: ignore
    from ._layout import (  # type: ignore
        AGENTS_ROOT,
        COMMANDS_ROOT,
        HOOKS_ROOT,
        PLUGINS_ROOT,
        REPO_ROOT,
        RULES_ROOT,
        SKILLS_ROOT,
    )

DEFAULT_INDEX = REPO_ROOT / "CLAUDE-CODE-CATALOG.md"

HEADER = """# Claude Code Primitives Catalog

This is the generated inventory of every Claude Code primitive in
`harness/claude-code/`. The harness is generated from the canonical Copilot
sources in `harness/github-copilot/`; see
[docs/CLAUDE-CODE-HARNESS-SPEC.md](docs/CLAUDE-CODE-HARNESS-SPEC.md) for the
runtime contract and the type routing table.

## Maintenance contract

- Do not hand-edit this file. Regenerate it with
  `python3 harness/claude-code/scripts/generate_catalog.py`.
- Do not hand-edit `harness/claude-code/`. Change the canonical Copilot source
  and re-run `python3 harness/claude-code/scripts/convert_from_copilot.py`.
- CI runs `python3 harness/claude-code/scripts/generate_catalog.py --check` and
  blocks a stale catalog.

## Primitive type guide

| Type | What it does | Discovery path | Canonical source |
| --- | --- | --- | --- |
| Subagent | Specialist persona with its own context window, tool scope, and model. | `.claude/agents/*.md`, `~/.claude/agents/*.md`, `<plugin>/agents/*.md` | `harness/claude-code/agents/` |
| Rule | Passive instructions loaded at launch or when Claude touches matching files. | `.claude/rules/**/*.md`, `~/.claude/rules/**/*.md` | `harness/claude-code/rules/` |
| Skill | Reusable procedure with optional scripts, references, and assets. | `.claude/skills/<name>/SKILL.md`, `~/.claude/skills/`, `<plugin>/skills/` | `harness/claude-code/skills/` |
| Command | Explicit `/name` action a user invokes. | `.claude/commands/*.md`, `<plugin>/commands/*.md` | `harness/claude-code/commands/` |
| Plugin | Installable bundle of skills, agents, commands, hooks, and MCP servers. | `.claude-plugin/plugin.json` | `harness/claude-code/plugins/` |
| Hook | Deterministic automation bound to a Claude Code lifecycle event. | `.claude/settings.json`, `<plugin>/hooks/hooks.json` | `harness/claude-code/hooks/` |
"""


def _flatten(value: Any, limit: int = 200) -> str:
    text = " ".join(str(value or "").split())
    text = text.replace("|", "\\|")
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def _link(path: Path, label: str | None = None) -> str:
    relative = path.relative_to(REPO_ROOT).as_posix()
    return f"[{label or relative}]({relative})"


def _frontmatter(path: Path) -> dict[str, Any]:
    data, _ = parse_frontmatter(path.read_text(encoding="utf-8"), source=str(path))
    return data


def collect() -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}

    data["agents"] = [
        {
            "name": path.stem,
            "description": _flatten(_frontmatter(path).get("description")),
            "tools": _flatten(_frontmatter(path).get("tools") or "inherits all tools", 120),
            "path": path,
        }
        for path in sorted(AGENTS_ROOT.glob("*.md"))
    ]

    rules = []
    for path in sorted(RULES_ROOT.rglob("*.md")):
        meta = _frontmatter(path)
        patterns = meta.get("paths") or []
        rules.append(
            {
                "name": path.stem,
                "paths": _flatten(", ".join(patterns) if patterns else "all files", 120),
                "path": path,
            }
        )
    data["rules"] = rules

    data["skills"] = [
        {
            "name": path.parent.name,
            "description": _flatten(_frontmatter(path).get("description")),
            "resources": sum(1 for item in path.parent.rglob("*") if item.is_file()) - 1,
            "path": path.parent,
        }
        for path in sorted(SKILLS_ROOT.glob("*/SKILL.md"))
    ]

    data["commands"] = [
        {
            "name": path.stem,
            "description": _flatten(_frontmatter(path).get("description")),
            "path": path,
        }
        for path in sorted(COMMANDS_ROOT.glob("*.md"))
    ]

    hooks = []
    for path in sorted(HOOKS_ROOT.glob("*/hooks.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        hooks.append(
            {
                "name": path.parent.name,
                "events": ", ".join(sorted(document.get("hooks", {}))),
                "path": path.parent,
            }
        )
    data["hooks"] = hooks

    plugins = []
    for plugin_dir in sorted(p for p in PLUGINS_ROOT.iterdir() if p.is_dir()):
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        hooks_json = plugin_dir / "hooks" / "hooks.json"
        components = {
            "agents": len(list((plugin_dir / "agents").glob("*.md"))),
            "skills": len(list((plugin_dir / "skills").glob("*/SKILL.md"))),
            "commands": len(list((plugin_dir / "commands").glob("*.md"))),
            "hooks": 1 if hooks_json.is_file() else 0,
            "mcp": 1 if (plugin_dir / ".mcp.json").is_file() else 0,
        }
        plugins.append(
            {
                "name": manifest.get("name", plugin_dir.name),
                "version": manifest.get("version", ""),
                "description": _flatten(manifest.get("description")),
                "components": components,
                "path": plugin_dir,
            }
        )
    data["plugins"] = plugins
    return data


def render(data: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = [HEADER, "## Summary", "", "| Primitive type | Count |", "| --- | ---: |"]
    labels = [
        ("Subagents", "agents"),
        ("Rules", "rules"),
        ("Skills", "skills"),
        ("Commands", "commands"),
        ("Plugins", "plugins"),
        ("Hooks", "hooks"),
    ]
    for label, key in labels:
        lines.append(f"| {label} | {len(data[key])} |")

    lines += ["", "## Subagents", "", "| Name | Purpose | Tools | Source |", "| --- | --- | --- | --- |"]
    for entry in data["agents"]:
        lines.append(f"| `{entry['name']}` | {entry['description']} | `{entry['tools']}` | {_link(entry['path'], 'file')} |")

    lines += ["", "## Rules", "", "| Name | Applies to | Source |", "| --- | --- | --- |"]
    for entry in data["rules"]:
        lines.append(f"| `{entry['name']}` | `{entry['paths']}` | {_link(entry['path'], 'file')} |")

    lines += ["", "## Skills", "", "| Name | Purpose | Bundled files | Source |", "| --- | --- | ---: | --- |"]
    for entry in data["skills"]:
        lines.append(
            f"| `{entry['name']}` | {entry['description']} | {entry['resources']} | {_link(entry['path'], 'directory')} |"
        )

    lines += ["", "## Commands", "", "| Command | Purpose | Source |", "| --- | --- | --- |"]
    for entry in data["commands"]:
        lines.append(f"| `/{entry['name']}` | {entry['description']} | {_link(entry['path'], 'file')} |")

    lines += [
        "",
        "## Plugins",
        "",
        "| Name | Version | Purpose | Agents | Skills | Commands | Hooks | MCP | Source |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for entry in data["plugins"]:
        components = entry["components"]
        lines.append(
            f"| `{entry['name']}` | {entry['version']} | {entry['description']} | {components['agents']} | "
            f"{components['skills']} | {components['commands']} | {components['hooks']} | {components['mcp']} | "
            f"{_link(entry['path'], 'directory')} |"
        )

    lines += ["", "## Hooks", "", "| Name | Events | Source |", "| --- | --- | --- |"]
    for entry in data["hooks"]:
        lines.append(f"| `{entry['name']}` | `{entry['events']}` | {_link(entry['path'], 'directory')} |")

    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail when the catalog has drifted")
    parser.add_argument("--output", type=Path, default=DEFAULT_INDEX, help="catalog path")
    args = parser.parse_args(argv)

    content = render(collect())
    if args.check:
        if not args.output.is_file():
            print(f"missing catalog: {args.output}", file=sys.stderr)
            return 1
        if args.output.read_text(encoding="utf-8") != content:
            print(
                f"{args.output.relative_to(REPO_ROOT)} is out of date. "
                "Run: python3 harness/claude-code/scripts/generate_catalog.py",
                file=sys.stderr,
            )
            return 1
        print("Claude Code catalog is up to date.")
        return 0

    args.output.write_text(content, encoding="utf-8")
    print(f"Wrote {args.output.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

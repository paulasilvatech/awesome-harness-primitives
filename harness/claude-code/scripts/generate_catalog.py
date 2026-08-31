#!/usr/bin/env python3
"""Generate the Claude Code harness catalog under docs/catalog/.

The catalog lists standalone primitives, plugins, and every plugin component.
``--check`` fails when the committed catalog has drifted from the harness.
"""

from __future__ import annotations

import argparse
import json
import os
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

DEFAULT_INDEX = REPO_ROOT / "docs" / "catalog" / "claude-code.md"
DEFAULT_PAGES_DIR = REPO_ROOT / "docs" / "catalog" / "claude-code"
LINK_BASE = REPO_ROOT
AWESOME_COPILOT_URL = "https://github.com/github/awesome-copilot"
PLUGIN_PROVENANCE_PATH = (
    REPO_ROOT
    / "harness"
    / "github-copilot"
    / "manifests"
    / "plugin-sources.json"
)

HEADER = """# Claude Code Primitives Catalog

This is the generated inventory of every Claude Code primitive in
`harness/claude-code/`. The harness is generated from the canonical Copilot
sources in `harness/github-copilot/`; see
[the Claude Code harness specification](../CLAUDE-CODE-HARNESS-SPEC.md) for the
runtime contract and the type routing table.

## Browse

[Subagents](#subagents) · [Rules](#rules) · [Skills](#skills) ·
[Commands](#commands) · [Plugin components](#plugin-components) ·
[Plugins](#plugins) · [Hooks](#hooks)

## Maintenance contract

- Do not hand-edit this file. Regenerate it with
  `python3 harness/claude-code/scripts/generate_catalog.py`.
- Do not hand-edit `harness/claude-code/`. Change the canonical Copilot source
  and re-run `python3 harness/claude-code/scripts/convert_from_copilot.py`.
- Generate declared `CLAUDE.md` and `.claude/` copies with
  `python3 harness/github-copilot/scripts/sync_installed_primitives.py --manifest
  harness/claude-code/manifests/installed-primitives.json`.
- CI checks conversion drift, strict validation, catalog drift, and installed
  Claude copy drift.

## Primitive type guide

| Type | What it does | Discovery path | Generated output |
| --- | --- | --- | --- |
| Subagent | Specialist persona with its own context window, tool scope, and model. | `.claude/agents/*.md`, `~/.claude/agents/*.md`, `<plugin>/agents/*.md` | `harness/claude-code/agents/` |
| Rule | Passive instructions loaded at launch or when Claude touches matching files. | `.claude/rules/**/*.md`, `~/.claude/rules/**/*.md` | `harness/claude-code/rules/` |
| Skill | Reusable procedure with optional scripts, references, and assets. | `.claude/skills/<name>/SKILL.md`, `~/.claude/skills/`, `<plugin>/skills/` | `harness/claude-code/skills/` |
| Command | Legacy-compatible explicit `/name` action; new reusable procedures should prefer skills. | `.claude/commands/*.md`, `<plugin>/commands/*.md` | `harness/claude-code/commands/` |
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
    relative = Path(os.path.relpath(path, LINK_BASE)).as_posix()
    return f"[{label or relative}]({relative})"


def _frontmatter(path: Path) -> dict[str, Any]:
    data, _ = parse_frontmatter(path.read_text(encoding="utf-8"), source=str(path))
    return data


def load_plugin_provenance() -> dict[str, dict[str, Any]]:
    document = json.loads(
        PLUGIN_PROVENANCE_PATH.read_text(encoding="utf-8")
    )
    plugins = document.get("plugins")
    return plugins if isinstance(plugins, dict) else {}


def collect() -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}
    provenance = load_plugin_provenance()

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
    plugin_components = []
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
                "upstream": provenance.get(
                    plugin_dir.name,
                    {},
                ).get("upstreamRepository"),
                "path": plugin_dir,
            }
        )
        for path in sorted((plugin_dir / "agents").glob("*.md")):
            meta = _frontmatter(path)
            plugin_components.append(
                {
                    "name": meta.get("name") or path.stem,
                    "type": "Subagent",
                    "plugin": plugin_dir.name,
                    "support": "Claude runtime",
                    "description": _flatten(meta.get("description")),
                    "path": path,
                }
            )
        for path in sorted((plugin_dir / "skills").glob("*/SKILL.md")):
            meta = _frontmatter(path)
            plugin_components.append(
                {
                    "name": meta.get("name") or path.parent.name,
                    "type": "Skill",
                    "plugin": plugin_dir.name,
                    "support": "Claude runtime",
                    "description": _flatten(meta.get("description")),
                    "path": path,
                }
            )
        for path in sorted((plugin_dir / "commands").glob("*.md")):
            meta = _frontmatter(path)
            plugin_components.append(
                {
                    "name": path.stem,
                    "type": "Command",
                    "plugin": plugin_dir.name,
                    "support": "Claude runtime",
                    "description": _flatten(meta.get("description")),
                    "path": path,
                }
            )
        if hooks_json.is_file():
            document = json.loads(hooks_json.read_text(encoding="utf-8"))
            events = ", ".join(sorted(document.get("hooks", {})))
            plugin_components.append(
                {
                    "name": "hooks",
                    "type": "Hook package",
                    "plugin": plugin_dir.name,
                    "support": "Claude runtime",
                    "description": _flatten(
                        f"Runs plugin automation for {events}."
                    ),
                    "path": hooks_json,
                }
            )
        mcp_path = plugin_dir / ".mcp.json"
        if mcp_path.is_file():
            document = json.loads(mcp_path.read_text(encoding="utf-8"))
            for name, config in sorted(
                document.get("mcpServers", {}).items()
            ):
                transport = (
                    config.get("type")
                    if isinstance(config, dict)
                    else None
                )
                detail = (
                    f"MCP server using the {transport} transport."
                    if transport
                    else "MCP server configuration."
                )
                plugin_components.append(
                    {
                        "name": name,
                        "type": "MCP server",
                        "plugin": plugin_dir.name,
                        "support": "Claude runtime",
                        "description": _flatten(detail),
                        "path": mcp_path,
                    }
                )
        for path in sorted(
            (plugin_dir / "extensions").glob("*/package.json")
        ):
            document = json.loads(path.read_text(encoding="utf-8"))
            plugin_components.append(
                {
                    "name": (
                        document.get("displayName")
                        or document.get("name")
                        or path.parent.name
                    ),
                    "type": "Client extension payload",
                    "plugin": plugin_dir.name,
                    "support": "Copied payload; not a Claude component",
                    "description": _flatten(document.get("description")),
                    "path": path,
                }
            )
        compatibility = plugin_dir / "copilot-components"
        if compatibility.is_dir():
            plugin_components.append(
                {
                    "name": "copilot-components",
                    "type": "Workspace-kit compatibility payload",
                    "plugin": plugin_dir.name,
                    "support": "Publisher data; not Claude-discovered",
                    "description": (
                        "Preserves Copilot customizations published by the "
                        "plugin workspace kit."
                    ),
                    "path": compatibility,
                }
            )
    data["plugins"] = plugins
    data["plugin-components"] = sorted(
        plugin_components,
        key=lambda item: (
            str(item["plugin"]).casefold(),
            str(item["type"]).casefold(),
            str(item["name"]).casefold(),
        ),
    )
    return data


def render(data: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = [HEADER, "## Summary", "", "| Primitive type | Count |", "| --- | ---: |"]
    labels = [
        ("Subagents", "agents"),
        ("Rules", "rules"),
        ("Skills", "skills"),
        ("Commands", "commands"),
        ("Plugin components", "plugin-components"),
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
        "## Plugin Components",
        "",
        "Every component bundled by a plugin is listed separately. Runtime support distinguishes Claude-discovered components from compatibility payloads.",
        "",
        "| Qualified item | Type | Plugin | Runtime support | Purpose | Source |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in data["plugin-components"]:
        qualified = f"{entry['plugin']}:{entry['name']}"
        lines.append(
            f"| `{qualified}` | {entry['type']} | `{entry['plugin']}` | "
            f"{entry['support']} | {entry['description']} | "
            f"{_link(entry['path'], 'source')} |"
        )

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


def _table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(_flatten(value, 500) for value in row)
            + " |"
        )
    return "\n".join(lines)


def page_definitions(
    data: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    agent_rows = [
        [
            f"`{entry['name']}`",
            entry["description"],
            f"`{entry['tools']}`",
            _link(entry["path"], "source"),
        ]
        for entry in data["agents"]
    ]
    rule_rows = [
        [
            f"`{entry['name']}`",
            f"`{entry['paths']}`",
            _link(entry["path"], "source"),
        ]
        for entry in data["rules"]
    ]
    skill_rows = [
        [
            f"`{entry['name']}`",
            entry["description"],
            str(entry["resources"]),
            _link(entry["path"], "source"),
        ]
        for entry in data["skills"]
    ]
    command_rows = [
        [
            f"`/{entry['name']}`",
            entry["description"],
            _link(entry["path"], "source"),
        ]
        for entry in data["commands"]
    ]
    component_rows = [
        [
            f"`{entry['plugin']}:{entry['name']}`",
            entry["type"],
            f"`{entry['plugin']}`",
            entry["support"],
            entry["description"],
            _link(entry["path"], "source"),
        ]
        for entry in data["plugin-components"]
    ]
    plugin_rows = []
    for entry in data["plugins"]:
        components = entry["components"]
        plugin_rows.append(
            [
                f"`{entry['name']}`",
                entry["version"],
                entry["description"],
                str(components["agents"]),
                str(components["skills"]),
                str(components["commands"]),
                str(components["hooks"]),
                str(components["mcp"]),
                (
                    f"[github/awesome-copilot]({AWESOME_COPILOT_URL})"
                    if entry.get("upstream") == AWESOME_COPILOT_URL
                    else (
                        f"[upstream]({entry['upstream']})"
                        if entry.get("upstream")
                        else "—"
                    )
                ),
                _link(entry["path"], "source"),
            ]
        )
    hook_rows = [
        [
            f"`{entry['name']}`",
            f"`{entry['events']}`",
            _link(entry["path"], "source"),
        ]
        for entry in data["hooks"]
    ]
    return [
        {
            "slug": "subagents",
            "title": "Subagents",
            "purpose": "Specialist personas with isolated context and tool scope.",
            "headers": ["Name", "Purpose", "Tools", "Source"],
            "rows": agent_rows,
        },
        {
            "slug": "rules",
            "title": "Rules",
            "purpose": "Passive project guidance, optionally scoped by paths.",
            "headers": ["Name", "Applies to", "Source"],
            "rows": rule_rows,
        },
        {
            "slug": "skills",
            "title": "Skills",
            "purpose": "Reusable procedures with optional bundled resources.",
            "headers": ["Name", "Purpose", "Bundled files", "Source"],
            "rows": skill_rows,
        },
        {
            "slug": "commands",
            "title": "Commands",
            "purpose": "Explicit legacy-compatible slash-command actions.",
            "headers": ["Command", "Purpose", "Source"],
            "rows": command_rows,
        },
        {
            "slug": "plugin-components",
            "title": "Plugin Components",
            "purpose": (
                "Every component bundled by a plugin, listed separately with "
                "its runtime support."
            ),
            "headers": [
                "Qualified item",
                "Type",
                "Plugin",
                "Runtime support",
                "Purpose",
                "Source",
            ],
            "rows": component_rows,
        },
        {
            "slug": "plugins",
            "title": "Plugins",
            "purpose": "Installable, self-contained Claude Code packages.",
            "headers": [
                "Name",
                "Version",
                "Purpose",
                "Agents",
                "Skills",
                "Commands",
                "Hooks",
                "MCP",
                "Upstream",
                "Source",
            ],
            "rows": plugin_rows,
        },
        {
            "slug": "hooks",
            "title": "Hooks",
            "purpose": "Reusable deterministic lifecycle automation packages.",
            "headers": ["Name", "Events", "Source"],
            "rows": hook_rows,
        },
    ]


def render_page(
    page: dict[str, Any],
    index_path: Path,
    page_path: Path,
) -> str:
    index_link = Path(
        os.path.relpath(index_path, page_path.parent)
    ).as_posix()
    return f"""# Claude Code Catalog - {page['title']}

{page['purpose']}

Part of the [Claude Code catalog]({index_link}). Generated file: do not
hand-edit it. Regenerate with
`python3 harness/claude-code/scripts/generate_catalog.py`.

## Credits and provenance

Some entries are adapted from
[github/awesome-copilot]({AWESOME_COPILOT_URL}) and have been updated and
improved for this repository's validation, packaging, and cross-harness
contracts. Plugin rows preserve their upstream source link when applicable.

## Overview

| Field | Value |
| --- | --- |
| Entries | {len(page['rows'])} |
| Generated source | `harness/claude-code/` |

## Entries

{_table(page['headers'], page['rows'])}
"""


def render_index(
    pages: list[dict[str, Any]],
    index_path: Path,
    pages_dir: Path,
) -> str:
    rows = []
    for page in pages:
        page_path = pages_dir / f"{page['slug']}.md"
        relative = Path(
            os.path.relpath(page_path, index_path.parent)
        ).as_posix()
        rows.append(
            [
                f"[{page['title']}]({relative})",
                page["purpose"],
                str(len(page["rows"])),
            ]
        )
    return f"""# Claude Code Primitives Catalog

Generated inventory for `harness/claude-code/`.

[Catalog hub](README.md) · [Plugin versus standalone](../USAGE.md) ·
[Repository home](../../README.md)

## Credits and provenance

This catalog includes multiple plugins, components, and references adapted from
[github/awesome-copilot]({AWESOME_COPILOT_URL}). They have been updated and
improved for current harness contracts, stricter validation, self-contained
packaging, and GitHub Copilot plus Claude Code compatibility. Applicable plugin
rows link back to the upstream repository.

## Catalog pages

{_table(["Page", "Contents", "Entries"], rows)}

## Maintenance contract

- Do not hand-edit the index or generated catalog pages.
- Regenerate with `python3 harness/claude-code/scripts/generate_catalog.py`.
- Change canonical primitive content under `harness/github-copilot/`, then run
  `harness/claude-code/scripts/convert_from_copilot.py`.
- Plugin components use qualified `plugin:item` names and distinguish native
  Claude runtime components from compatibility payloads.
"""


def build_outputs(
    index_path: Path,
    pages_dir: Path,
) -> dict[Path, str]:
    global LINK_BASE
    LINK_BASE = pages_dir
    data = collect()
    pages = page_definitions(data)
    outputs = {}
    for page in pages:
        page_path = pages_dir / f"{page['slug']}.md"
        outputs[page_path] = render_page(page, index_path, page_path)
    outputs[index_path] = render_index(pages, index_path, pages_dir)
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail when the catalog has drifted")
    parser.add_argument("--output", type=Path, default=DEFAULT_INDEX, help="catalog path")
    parser.add_argument(
        "--pages-dir",
        type=Path,
        default=DEFAULT_PAGES_DIR,
        help="directory for per-type catalog pages",
    )
    args = parser.parse_args(argv)

    output = args.output.resolve()
    pages_dir = args.pages_dir.resolve()
    outputs = build_outputs(output, pages_dir)
    if args.check:
        stale = [
            path
            for path, content in outputs.items()
            if not path.is_file()
            or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            for path in stale:
                print(
                    f"{path.relative_to(REPO_ROOT)} is out of date.",
                    file=sys.stderr,
                )
            print(
                "Run: python3 harness/claude-code/scripts/generate_catalog.py",
                file=sys.stderr,
            )
            return 1
        print("Claude Code catalog is up to date.")
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(
        f"Wrote {output.relative_to(REPO_ROOT)} and "
        f"{len(outputs) - 1} catalog pages"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

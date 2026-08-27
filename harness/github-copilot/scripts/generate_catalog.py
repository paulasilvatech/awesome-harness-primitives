#!/usr/bin/env python3
"""Generate the root catalog from the repository's primitive sources."""
from __future__ import annotations

import argparse
import json
import re
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

DEFAULT_OUT = REPO_ROOT / "CATALOG.md"
SOURCE_ROOT = HARNESS_ROOT
DESCRIPTION_WIDTH = 140
USE_CASE_WIDTH = 180
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
ACTIVATION_MARKER = re.compile(
    r"\b(?:use (?:this )?when|use for|use to|invoke when|choose when|"
    r"ideal for|best for|applies when)\b",
    re.IGNORECASE,
)
ACTIVATION_HEADINGS = {
    "activation",
    "activation and scope",
    "scope",
    "use cases",
    "when to invoke",
}
PLUGIN_COMPONENTS = (
    ("agents", "agent", "agents"),
    ("skills", "skill", "skills"),
    ("commands", "command", "commands"),
    ("mcpServers", "MCP server", "MCP servers"),
    ("lspServers", "LSP server", "LSP servers"),
    ("outputStyles", "output style", "output styles"),
    ("hooks", "hook package", "hook packages"),
    ("extensions", "client extension", "client extensions"),
)


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


def ensure_sentence(value: str) -> str:
    text = value.strip()
    if text and text[-1] not in ".!?":
        return text + "."
    return text


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
    fm, _body = document_parts(path, required=required)
    return fm


def document_parts(
    path: Path,
    required: bool = True,
) -> tuple[dict[str, Any], str]:
    fm, body, present, err = parse_frontmatter(
        read_text(path), required=required)
    if not present or err or not isinstance(fm, dict):
        return {}, body
    return fm, body


def split_description(value: Any) -> tuple[str, str]:
    description = one_line(value)
    if description == "—":
        return description, ""
    match = ACTIVATION_MARKER.search(description)
    if match is None:
        return description, ""
    use_case = ensure_sentence(description[match.start():])
    if match.start() == 0:
        return description, use_case
    summary = ensure_sentence(description[:match.start()].rstrip(" ,;:."))
    return summary, use_case


def markdown_heading(line: str) -> tuple[int, str] | None:
    level = len(line) - len(line.lstrip("#"))
    if level < 2 or level > 6 or len(line) <= level:
        return None
    if line[level] != " ":
        return None
    title = line[level + 1:].strip().rstrip("#").strip().casefold()
    return level, title


def activation_section(body: str) -> list[str]:
    lines = body.splitlines()
    section: list[str] = []
    section_level = 0
    collecting = False
    for line in lines:
        heading = markdown_heading(line)
        if heading:
            level, title = heading
            if collecting and level <= section_level:
                break
            if title in ACTIVATION_HEADINGS:
                collecting = True
                section_level = level
                continue
        if collecting:
            section.append(line)
    return section


def first_section_paragraph(section: list[str]) -> str:
    paragraph: list[str] = []
    for line in section:
        stripped = line.strip()
        if not stripped:
            if paragraph:
                return ensure_sentence(" ".join(paragraph))
            continue
        if len(stripped) > 1 and stripped[0] in "-*" and stripped[1].isspace():
            break
        if stripped.startswith(("```", "|", ">", "#")):
            continue
        paragraph.append(stripped)
    return ensure_sentence(" ".join(paragraph))


def first_section_bullets(section: list[str]) -> str:
    bullets = []
    for line in section:
        stripped = line.strip()
        if len(stripped) > 1 and stripped[0] in "-*" and stripped[1].isspace():
            bullets.append(ensure_sentence(stripped[2:].strip()))
        if len(bullets) == 2:
            return " ".join(bullets)
    return " ".join(bullets)


def activation_from_body(body: str) -> str:
    section = activation_section(body)
    return first_section_paragraph(section) or first_section_bullets(section)


def catalog_description(
    description: Any,
    body: str = "",
    fallback_use_case: str = "",
) -> tuple[str, str]:
    summary, description_use_case = split_description(description)
    use_case = (
        description_use_case
        or activation_from_body(body)
        or ensure_sentence(fallback_use_case)
        or f"Typical use: {summary}"
    )
    return truncate(summary), truncate(use_case, USE_CASE_WIDTH)


def source_link(path: Path, label: str = "source") -> str:
    try:
        target = path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        target = path.as_posix()
    return f"[{label}]({target})"


def sort_rows(rows: list[list[str]]) -> list[list[str]]:
    return sorted(rows, key=lambda row: tuple(cell.casefold() for cell in row))


def agent_rows() -> list[list[str]]:
    rows = []
    paths = (SOURCE_ROOT / "agents").glob("*.agent.md")
    for path in sorted(paths, key=lambda p: p.name.casefold()):
        fm, body = document_parts(path)
        name = fm.get("name") or path.name.removesuffix(".agent.md")
        description, use_case = catalog_description(
            fm.get("description"), body)
        rows.append([one_line(name), description,
                    use_case, source_link(path)])
    return sort_rows(rows)


def instruction_rows() -> list[list[str]]:
    rows = []
    paths = (SOURCE_ROOT / "instructions").glob("*.instructions.md")
    for path in sorted(paths, key=lambda p: p.name.casefold()):
        fm, body = document_parts(path, required=False)
        name = fm.get("name") or path.name.removesuffix(".instructions.md")
        apply_to = one_line(fm.get("applyTo"))
        fallback = (
            f"Applies automatically to files matching `{apply_to}`."
            if apply_to != "—"
            else (
                "Use as passive repository guidance when its conventions "
                "are relevant."
            )
        )
        description, use_case = catalog_description(
            fm.get("description"), body, fallback)
        rows.append([one_line(name), apply_to, description,
                    use_case, source_link(path)])
    return sort_rows(rows)


def skill_rows() -> list[list[str]]:
    rows = []
    paths = (SOURCE_ROOT / "skills").glob("*/SKILL.md")
    for path in sorted(paths, key=lambda p: p.parent.name.casefold()):
        fm, body = document_parts(path)
        name = fm.get("name") or path.parent.name
        description, use_case = catalog_description(
            fm.get("description"), body)
        rows.append([one_line(name), description,
                    use_case, source_link(path)])
    return sort_rows(rows)


def prompt_rows() -> list[list[str]]:
    rows = []
    for path in sorted(
        (SOURCE_ROOT / "prompts").glob("*.prompt.md"),
        key=lambda p: p.name.casefold(),
    ):
        fm, body = document_parts(path)
        name = fm.get("name") or path.name.removesuffix(".prompt.md")
        description, use_case = catalog_description(
            fm.get("description"), body)
        rows.append([one_line(name), description,
                    use_case, source_link(path)])
    return sort_rows(rows)


def plugin_manifest(plugin_dir: Path) -> Path | None:
    for rel in PLUGIN_MANIFESTS:
        path = plugin_dir / rel
        if path.exists():
            return path
    return None


def count_path_component(plugin_dir: Path, key: str, value: str) -> int:
    target = plugin_dir / value.removeprefix("./")
    if not target.exists():
        return 0
    if target.is_file():
        if key in {"mcpServers", "lspServers"}:
            data = json.loads(target.read_text(encoding="utf-8"))
            servers = data.get(key)
            return len(servers) if isinstance(servers, dict) else 0
        return 1
    patterns = {
        "agents": "*.agent.md",
        "skills": "*/SKILL.md",
        "commands": "*.md",
        "outputStyles": "*.md",
    }
    pattern = patterns.get(key, "*")
    return sum(1 for path in target.glob(pattern) if path.is_file())


def component_count(plugin_dir: Path, key: str, value: Any) -> int:
    if isinstance(value, str):
        return count_path_component(plugin_dir, key, value)
    if isinstance(value, (list, dict)):
        return len(value)
    return 0


def plugin_contents(plugin_dir: Path, data: dict[str, Any]) -> str:
    parts = []
    for key, singular, plural in PLUGIN_COMPONENTS:
        if key not in data:
            continue
        count = component_count(plugin_dir, key, data[key])
        if count:
            parts.append(f"{count} {singular if count == 1 else plural}")
    return ", ".join(parts) if parts else "Manifest-only package"


def plugin_use_case(data: dict[str, Any], contents: str) -> str:
    keywords = data.get("keywords")
    if isinstance(keywords, list) and keywords:
        topics = ", ".join(
            f"`{one_line(keyword)}`" for keyword in keywords[:6]
        )
        return f"Use for workflows involving {topics}; bundles {contents}."
    return f"Use when a project needs the bundled capabilities: {contents}."


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
        contents = plugin_contents(plugin_dir, data)
        description, use_case = catalog_description(
            data.get("description"),
            fallback_use_case=plugin_use_case(data, contents),
        )
        rows.append([
            one_line(data.get("name") or plugin_dir.name),
            one_line(data.get("version")),
            classification.lifecycle,
            classification.assurance,
            classification.provenance,
            contents,
            description,
            use_case,
            source_link(manifest) if manifest is not None else "—",
        ])
    return sort_rows(rows)


def hook_rows() -> list[list[str]]:
    rows = []
    event_order = {event: idx for idx, event in enumerate(HOOK_EVENT_ORDER)}
    paths = (SOURCE_ROOT / "hooks").glob("*/hooks.json")
    for path in sorted(paths, key=lambda p: p.parent.name.casefold()):
        data = json.loads(path.read_text(encoding="utf-8"))
        hooks = data.get("hooks", {})
        events = (
            sorted(
                hooks,
                key=lambda event: (
                    event_order.get(event, len(event_order)),
                    event.casefold(),
                ),
            )
            if isinstance(hooks, dict)
            else []
        )
        readme = path.parent / "README.md"
        fm, body = document_parts(readme) if readme.is_file() else ({}, "")
        name = fm.get("name") or path.parent.name
        description, use_case = catalog_description(
            fm.get("description"),
            body,
            f"Typical use: {one_line(fm.get('description'))}",
        )
        source = source_link(path, "manifest")
        if readme.is_file():
            source += f" · {source_link(readme, 'docs')}"
        rows.append([
            one_line(name),
            description,
            ", ".join(events) if events else "—",
            use_case,
            source,
        ])
    return sort_rows(rows)


def build_catalog() -> str:
    agents = agent_rows()
    instructions = instruction_rows()
    skills = skill_rows()
    prompts = prompt_rows()
    plugins = plugin_rows()
    hooks = hook_rows()

    type_guide = [
        [
            "Agent",
            "Defines a specialist persona, judgment boundary, and tool posture.",
            (
                "Delegated implementation, review, diagnosis, architecture, "
                "or domain-specific decisions."
            ),
            "`harness/github-copilot/agents/`",
        ],
        [
            "Instructions",
            "Applies passive conventions to matching files or repository work.",
            (
                "Coding standards, governance, path-specific rules, and "
                "verification requirements."
            ),
            "`harness/github-copilot/instructions/`",
        ],
        [
            "Skill",
            (
                "Packages a reusable workflow with optional scripts, "
                "references, and assets."
            ),
            (
                "Repeatable procedures that need ordered steps, domain "
                "knowledge, or bundled resources."
            ),
            "`harness/github-copilot/skills/`",
        ],
        [
            "VS Code prompt",
            "Defines an explicit action a user runs from VS Code Chat.",
            (
                "Guided generation, transformation, review, and interactive "
                "workspace tasks."
            ),
            "`harness/github-copilot/prompts/`",
        ],
        [
            "Plugin",
            (
                "Bundles installable Copilot capabilities and optional MCP, "
                "hook, or client-extension surfaces."
            ),
            (
                "Distributing cohesive capability suites through a plugin "
                "or marketplace."
            ),
            "`harness/github-copilot/plugins/`",
        ],
        [
            "Hook",
            (
                "Runs deterministic checks or automation at Copilot "
                "lifecycle events."
            ),
            (
                "Guardrails, compliance checks, logging, and opt-in session "
                "automation."
            ),
            "`harness/github-copilot/hooks/`",
        ],
    ]
    type_guide_table = md_table(
        ["Type", "What it does", "Typical use cases", "Canonical source"],
        type_guide,
    )
    agent_table = md_table(
        ["Agent", "Description", "Use cases", "Source"],
        agents,
    )
    instruction_table = md_table(
        ["Instruction", "applyTo", "Description", "Use cases", "Source"],
        instructions,
    )
    skill_table = md_table(
        ["Skill", "Description", "Use cases", "Source"],
        skills,
    )
    prompt_table = md_table(
        ["Prompt", "Description", "Use cases", "Source"],
        prompts,
    )
    plugin_table = md_table(
        [
            "Plugin",
            "Version",
            "Lifecycle",
            "Assurance",
            "Provenance",
            "Contents",
            "Description",
            "Use cases",
            "Source",
        ],
        plugins,
    )
    hook_table = md_table(
        [
            "Hook package",
            "Description",
            "Trigger events",
            "Use cases",
            "Source",
        ],
        hooks,
    )

    return f"""# Copilot Primitives Catalog

This is the generated root inventory of every canonical Copilot primitive
package in this repository. Each entry includes a concise purpose, a typical
use case, and a link to its source.

## Maintenance contract

- Do not hand-edit this file. Regenerate it with
  `python3 harness/github-copilot/scripts/generate_catalog.py`.
- Regenerate after changing canonical agents, instructions, skills, prompts,
  plugins, or hooks under `harness/github-copilot/`.
- CI runs `python3 harness/github-copilot/scripts/generate_catalog.py --check`
  and blocks stale catalog changes.
- Shared primitives copied into plugins or `.github/` are listed once at their
  canonical source. Plugin rows summarize bundled capabilities without
  duplicating generated copies.

## Primitive type guide

{type_guide_table}

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

{agent_table}

## Instructions

{instruction_table}

## Skills

{skill_table}

## VS Code Prompts

These prompts are explicit VS Code Chat actions; GitHub Copilot CLI does not
discover or execute them.

{prompt_table}

## Plugins

Lifecycle, assurance, and provenance are descriptive classifications generated
from repository evidence. They exist to filter a large marketplace and never
remove, hide, or block a package.

{plugin_table}

## Hooks

{hook_table}
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
                        help="output path (default: CATALOG.md)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if the output file is stale; do not write",
    )
    args = parser.parse_args(argv)

    global SOURCE_ROOT
    SOURCE_ROOT = args.root.resolve()
    out = args.out if args.out.is_absolute() else REPO_ROOT / args.out
    content = build_catalog()
    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != content:
            print(
                f"{out.relative_to(REPO_ROOT)} is stale; run "
                "python3 harness/github-copilot/scripts/generate_catalog.py",
                file=sys.stderr,
            )
            return 1
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

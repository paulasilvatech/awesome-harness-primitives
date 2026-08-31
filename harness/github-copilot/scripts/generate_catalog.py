#!/usr/bin/env python3
"""Generate the split primitive catalog from the repository's sources."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
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

DEFAULT_INDEX = REPO_ROOT / "docs" / "catalog" / "github-copilot.md"
DEFAULT_PAGES_DIR = REPO_ROOT / "docs" / "catalog" / "github-copilot"
SOURCE_ROOT = HARNESS_ROOT
LINK_BASE = REPO_ROOT
DESCRIPTION_WIDTH = 140
USE_CASE_WIDTH = 180
REGENERATE_COMMAND = (
    "python3 harness/github-copilot/scripts/generate_catalog.py"
)
AWESOME_COPILOT_URL = "https://github.com/github/awesome-copilot"
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
PLUGIN_ITEM_FIELDS = (
    "agents",
    "skills",
    "commands",
    "hooks",
    "mcpServers",
    "lspServers",
    "outputStyles",
    "extensions",
)
PLUGIN_ITEM_LABELS = {
    "agents": "Agent",
    "skills": "Skill",
    "commands": "Command",
    "hooks": "Hook package",
    "mcpServers": "MCP server",
    "lspServers": "LSP server",
    "outputStyles": "Output style",
    "extensions": "Client extension",
}


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


def relative_link_target(path: Path, base: Path | None = None) -> str:
    origin = LINK_BASE if base is None else base
    return Path(os.path.relpath(path, origin)).as_posix()


def source_link(path: Path, label: str = "source") -> str:
    return f"[{label}]({relative_link_target(path)})"


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
            (
                f"[github/awesome-copilot]({AWESOME_COPILOT_URL})"
                if source_config.get("upstreamRepository")
                == AWESOME_COPILOT_URL
                else (
                    f"[upstream]({source_config['upstreamRepository']})"
                    if source_config.get("upstreamRepository")
                    else "—"
                )
            ),
            source_link(manifest) if manifest is not None else "—",
        ])
    return sort_rows(rows)


def component_paths(
    plugin_dir: Path,
    key: str,
    value: Any,
) -> list[Path]:
    values = [value] if isinstance(value, str) else value
    if not isinstance(values, list):
        return []
    paths: list[Path] = []
    for item in values:
        if not isinstance(item, str):
            continue
        target = plugin_dir / item.removeprefix("./")
        if target.is_file():
            paths.append(target)
            continue
        if not target.is_dir():
            continue
        patterns = {
            "agents": "*.agent.md",
            "skills": "*/SKILL.md",
            "commands": "*.md",
            "hooks": "hooks.json",
            "outputStyles": "*.md",
        }
        if key == "extensions":
            package = target / "package.json"
            if package.is_file():
                paths.append(package)
            else:
                paths.extend(sorted(target.glob("*/package.json")))
            continue
        pattern = patterns.get(key)
        if pattern:
            paths.extend(sorted(target.glob(pattern)))
    return paths


def server_items(
    plugin_dir: Path,
    key: str,
    value: Any,
    manifest: Path,
) -> list[tuple[str, str, Path]]:
    source = manifest
    servers: Any = value
    if isinstance(value, str):
        source = plugin_dir / value.removeprefix("./")
        if not source.is_file():
            return []
        document = json.loads(source.read_text(encoding="utf-8"))
        servers = document.get(key)
    if not isinstance(servers, dict):
        return []
    items = []
    for name, config in sorted(servers.items()):
        transport = config.get("type") if isinstance(config, dict) else None
        detail = (
            f"{PLUGIN_ITEM_LABELS[key]} using the `{transport}` transport."
            if transport
            else f"{PLUGIN_ITEM_LABELS[key]} configuration."
        )
        items.append((str(name), detail, source))
    return items


def component_details(
    key: str,
    path: Path,
) -> tuple[str, str, str]:
    if key in {"agents", "skills", "commands", "outputStyles"}:
        required = key != "outputStyles"
        fm, body = document_parts(path, required=required)
        if key == "skills":
            name = fm.get("name") or path.parent.name
        elif key == "agents":
            name = path.name.removesuffix(".agent.md")
        else:
            name = fm.get("name") or path.stem
        description, use_case = catalog_description(
            fm.get("description"),
            body,
            f"Use the plugin-provided {PLUGIN_ITEM_LABELS[key].lower()} `{name}`.",
        )
        return one_line(name), description, use_case
    if key == "extensions":
        data = json.loads(path.read_text(encoding="utf-8"))
        name = data.get("displayName") or data.get("name") or path.parent.name
        description, use_case = catalog_description(
            data.get("description"),
            fallback_use_case=(
                f"Use the `{name}` client extension included by this plugin."
            ),
        )
        return one_line(name), description, use_case
    if key == "hooks":
        data = json.loads(path.read_text(encoding="utf-8"))
        events = data.get("hooks")
        event_names = ", ".join(events) if isinstance(events, dict) else ""
        name = path.parent.name
        description = (
            f"Runs plugin automation for {event_names}."
            if event_names
            else "Runs plugin lifecycle automation."
        )
        return name, description, f"Use with the `{name}` plugin guardrails."
    return path.stem, PLUGIN_ITEM_LABELS[key], ""


def component_ownership(
    plugin_dir: Path,
    key: str,
    path: Path,
    source_config: dict[str, Any],
) -> str:
    shared_refs: set[str] = set()
    if key == "skills":
        shared_refs.update(source_config.get("sharedSkills") or [])
        if source_config.get("componentSource") == "library":
            shared_refs.update(source_config.get("skills") or [])
        relative = f"./skills/{path.parent.name}/"
    elif key == "agents":
        if source_config.get("componentSource") == "library":
            shared_refs.update(source_config.get("agents") or [])
        relative = f"./agents/{path.name}"
    else:
        return "Plugin-owned"
    normalized = {
        f"./{value.removeprefix('./')}"
        for value in shared_refs
        if isinstance(value, str)
    }
    return (
        "Shared library copy"
        if relative in normalized
        else "Plugin-owned"
    )


def plugin_component_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    source_map = load_plugin_sources()
    plugins_root = SOURCE_ROOT / "plugins"
    plugin_dirs = (
        [path for path in plugins_root.iterdir() if path.is_dir()]
        if plugins_root.is_dir()
        else []
    )
    for plugin_dir in sorted(plugin_dirs, key=lambda path: path.name.casefold()):
        manifest = plugin_manifest(plugin_dir)
        if manifest is None:
            continue
        data = json.loads(manifest.read_text(encoding="utf-8"))
        source_config = source_map.get(plugin_dir.name, {})
        for key in PLUGIN_ITEM_FIELDS:
            value = data.get(key)
            if value is None:
                continue
            if key in {"mcpServers", "lspServers"}:
                for name, description, source in server_items(
                    plugin_dir,
                    key,
                    value,
                    manifest,
                ):
                    rows.append([
                        f"{plugin_dir.name}:{name}",
                        PLUGIN_ITEM_LABELS[key],
                        plugin_dir.name,
                        "Plugin-owned",
                        description,
                        f"Use the `{name}` integration installed with this plugin.",
                        source_link(source),
                    ])
                continue
            for path in component_paths(plugin_dir, key, value):
                name, description, use_case = component_details(key, path)
                ownership = component_ownership(
                    plugin_dir,
                    key,
                    path,
                    source_config,
                )
                rows.append([
                    f"{plugin_dir.name}:{name}",
                    PLUGIN_ITEM_LABELS[key],
                    plugin_dir.name,
                    ownership,
                    description,
                    use_case,
                    source_link(path),
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


@dataclass
class CatalogPage:
    slug: str
    title: str
    type_label: str
    purpose: str
    use_cases: str
    canonical: str
    headers: list[str]
    rows: list[list[str]] = field(default_factory=list)
    note: str = ""
    path: Path = REPO_ROOT


def collect_pages() -> list[CatalogPage]:
    return [
        CatalogPage(
            slug="agents",
            title="Agents",
            type_label="Agent",
            purpose=(
                "Defines a specialist persona, judgment boundary, and tool "
                "posture."
            ),
            use_cases=(
                "Delegated implementation, review, diagnosis, architecture, "
                "or domain-specific decisions."
            ),
            canonical="harness/github-copilot/agents/",
            headers=["Agent", "Description", "Use cases", "Source"],
            rows=agent_rows(),
        ),
        CatalogPage(
            slug="instructions",
            title="Instructions",
            type_label="Instructions",
            purpose=(
                "Applies passive conventions to matching files or repository "
                "work."
            ),
            use_cases=(
                "Coding standards, governance, path-specific rules, and "
                "verification requirements."
            ),
            canonical="harness/github-copilot/instructions/",
            headers=[
                "Instruction",
                "applyTo",
                "Description",
                "Use cases",
                "Upstream",
                "Source",
            ],
            rows=instruction_rows(),
            note=(
                "An `applyTo` glob makes the file auto-apply to matching "
                "paths. Entries without one are loaded as general repository "
                "guidance."
            ),
        ),
        CatalogPage(
            slug="skills",
            title="Skills",
            type_label="Skill",
            purpose=(
                "Packages a reusable workflow with optional scripts, "
                "references, and assets."
            ),
            use_cases=(
                "Repeatable procedures that need ordered steps, domain "
                "knowledge, or bundled resources."
            ),
            canonical="harness/github-copilot/skills/",
            headers=["Skill", "Description", "Use cases", "Source"],
            rows=skill_rows(),
        ),
        CatalogPage(
            slug="prompts",
            title="VS Code Prompts",
            type_label="VS Code prompt",
            purpose="Defines an explicit action a user runs from VS Code Chat.",
            use_cases=(
                "Guided generation, transformation, review, and interactive "
                "workspace tasks."
            ),
            canonical="harness/github-copilot/prompts/",
            headers=["Prompt", "Description", "Use cases", "Source"],
            rows=prompt_rows(),
            note=(
                "These prompts are explicit VS Code Chat actions; GitHub "
                "Copilot CLI does not discover or execute them."
            ),
        ),
        CatalogPage(
            slug="plugin-components",
            title="Plugin Components",
            type_label="Plugin component",
            purpose=(
                "Lists every runtime component declared by every plugin as an "
                "individually discoverable item."
            ),
            use_cases=(
                "Finding a specific agent, skill, hook, MCP or LSP server, "
                "output style, or client extension without browsing package trees."
            ),
            canonical="harness/github-copilot/plugins/*/",
            headers=[
                "Qualified item",
                "Type",
                "Plugin",
                "Ownership",
                "Description",
                "Use cases",
                "Source",
            ],
            rows=plugin_component_rows(),
            note=(
                "Qualified names use `plugin:item`. Shared library copies remain "
                "listed here to show plugin membership; their standalone source "
                "also appears on the matching primitive page."
            ),
        ),
        CatalogPage(
            slug="plugins",
            title="Plugins",
            type_label="Plugin",
            purpose=(
                "Bundles installable Copilot capabilities and optional MCP, "
                "hook, or client-extension surfaces."
            ),
            use_cases=(
                "Distributing cohesive capability suites through a plugin "
                "or marketplace."
            ),
            canonical="harness/github-copilot/plugins/",
            headers=[
                "Plugin",
                "Version",
                "Lifecycle",
                "Assurance",
                "Provenance",
                "Contents",
                "Description",
                "Use cases",
                "Upstream",
                "Source",
            ],
            rows=plugin_rows(),
            note=(
                "Lifecycle, assurance, and provenance are descriptive "
                "classifications generated from repository evidence. They "
                "exist to filter a large marketplace and never remove, hide, "
                "or block a package. Open [Plugin Components](plugin-components.md) "
                "to browse every bundled runtime item separately."
            ),
        ),
        CatalogPage(
            slug="hooks",
            title="Hooks",
            type_label="Hook",
            purpose=(
                "Runs deterministic checks or automation at Copilot "
                "lifecycle events."
            ),
            use_cases=(
                "Guardrails, compliance checks, logging, and opt-in session "
                "automation."
            ),
            canonical="harness/github-copilot/hooks/",
            headers=[
                "Hook package",
                "Description",
                "Trigger events",
                "Use cases",
                "Source",
            ],
            rows=hook_rows(),
        ),
    ]


def render_page(page: CatalogPage, index_path: Path, page_path: Path) -> str:
    index_link = relative_link_target(index_path, page_path.parent)
    note = f"\n{page.note}\n" if page.note else ""
    overview = md_table(
        ["Field", "Value"],
        [
            ["Primitive type", page.type_label],
            ["Entries", str(len(page.rows))],
            ["Canonical source", f"`{page.canonical}`"],
            ["Typical use cases", page.use_cases],
        ],
    )
    return f"""# Copilot Primitives Catalog — {page.title}

{page.purpose}

Part of the [Copilot primitives catalog]({index_link}). Generated file: do not
hand-edit it. Regenerate with `{REGENERATE_COMMAND}`.

## Overview

{overview}
{note}
## Credits and provenance

Some catalog entries are adapted from
[github/awesome-copilot]({AWESOME_COPILOT_URL}) and have been updated and
improved for this repository's validation, packaging, and cross-harness
contracts. Plugin rows preserve their upstream source link when applicable.

## Entries

{md_table(page.headers, page.rows)}
"""


def render_index(pages: list[CatalogPage], index_path: Path) -> str:
    guide_rows = [
        [
            f"[{page.title}]({relative_link_target(page.path, index_path.parent)})",
            page.purpose,
            page.use_cases,
            f"`{page.canonical}`",
        ]
        for page in pages
    ]
    summary_rows = [
        [
            f"[{page.title}]({relative_link_target(page.path, index_path.parent)})",
            str(len(page.rows)),
        ]
        for page in pages
    ]
    return f"""# Copilot Primitives Catalog

This is the generated index of every canonical Copilot primitive package in
this repository. Each primitive type has its own page listing every entry with
a concise purpose, a typical use case, and a link to its source.

[Catalog hub](README.md) · [Plugin versus standalone](../USAGE.md) ·
[Repository home](../../README.md)

## Credits and provenance

This catalog includes multiple plugins, components, and references adapted from
[github/awesome-copilot]({AWESOME_COPILOT_URL}). They have been updated and
improved for current harness contracts, stricter validation, self-contained
packaging, and GitHub Copilot plus Claude Code compatibility. Applicable plugin
rows link back to the upstream repository.

## Catalog pages

{md_table(["Page", "What the type does", "Typical use cases", "Canonical source"], guide_rows)}

## Summary

{md_table(["Primitive type", "Entries"], summary_rows)}

## Maintenance contract

- Do not hand-edit the index or any catalog page. Regenerate them with
  `{REGENERATE_COMMAND}`.
- Regenerate after changing canonical agents, instructions, skills, prompts,
  plugins, or hooks under `harness/github-copilot/`.
- CI runs `{REGENERATE_COMMAND} --check` and blocks a stale index or page.
- Standalone pages list shared primitives once at their canonical source.
- The Plugin Components page intentionally repeats package membership with
  qualified `plugin:item` names so every bundled runtime item is discoverable.
"""


def build_catalog() -> str:
    """Build a single-document catalog for API consumers and focused tests."""
    global LINK_BASE
    LINK_BASE = REPO_ROOT
    pages = collect_pages()
    sections = ["# Copilot Primitives Catalog"]
    for page in pages:
        count_label = page.type_label.lower()
        if len(page.rows) != 1:
            count_label += "s"
        sections.extend(
            [
                f"## {page.title}",
                "",
                page.purpose,
                "",
                f"{len(page.rows)} {count_label}. Use cases: {page.use_cases}",
                "",
                md_table(page.headers, page.rows),
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def build_outputs(index_path: Path, pages_dir: Path) -> dict[Path, str]:
    global LINK_BASE
    LINK_BASE = pages_dir
    pages = collect_pages()
    outputs: dict[Path, str] = {}
    for page in pages:
        page.path = pages_dir / f"{page.slug}.md"
        outputs[page.path] = render_page(page, index_path, page.path)
    LINK_BASE = index_path.parent
    outputs[index_path] = render_index(pages, index_path)
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the Copilot primitives catalog.")
    parser.add_argument(
        "--root",
        type=Path,
        default=HARNESS_ROOT,
        help="canonical harness root (default: <repo>/harness/github-copilot)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_INDEX,
        help="index path (default: docs/catalog/github-copilot.md)",
    )
    parser.add_argument(
        "--pages-dir",
        type=Path,
        default=DEFAULT_PAGES_DIR,
        help=(
            "per-type page directory "
            "(default: docs/catalog/github-copilot)"
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if any generated file is stale; do not write",
    )
    args = parser.parse_args(argv)

    global SOURCE_ROOT
    SOURCE_ROOT = args.root.resolve()
    index_path = args.out if args.out.is_absolute() else REPO_ROOT / args.out
    pages_dir = (
        args.pages_dir
        if args.pages_dir.is_absolute()
        else REPO_ROOT / args.pages_dir
    )
    outputs = build_outputs(index_path, pages_dir)

    if args.check:
        stale = [
            path
            for path, content in outputs.items()
            if not path.exists()
            or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            for path in sorted(stale):
                print(
                    f"{relative_link_target(path, REPO_ROOT)} is stale",
                    file=sys.stderr,
                )
            print(f"run {REGENERATE_COMMAND}", file=sys.stderr)
            return 1
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate the Claude Code harness from the canonical Copilot primitive sources.

``harness/claude-code/`` is generated. Edit the canonical sources under
``harness/github-copilot/`` and re-run this script; ``--check`` fails when the
generated tree has drifted.

Type routing (see ``docs/CLAUDE-CODE-HARNESS-SPEC.md``):

======================================  ====================================
Copilot source                          Claude Code output
======================================  ====================================
``agents/<name>.agent.md``              ``agents/<name>.md`` (subagent)
``instructions/<name>.instructions.md`` ``rules/<name>.md`` (path-scoped rule)
``skills/<name>/SKILL.md``              ``skills/<name>/SKILL.md``
``prompts/<name>.prompt.md``            ``commands/<name>.md`` (slash command)
``plugins/<name>/plugin.json``          ``plugins/<name>/.claude-plugin/plugin.json``
``hooks/<name>/hooks.json``             ``hooks/<name>/hooks.json``
======================================  ====================================
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from _convert import (
        AGENT_FIELDS,
        ConversionError,
        HOOK_EVENT_MAP,
        PLUGIN_AGENT_FIELDS,
        PLUGIN_MANIFEST_FIELDS,
        SLUG_PATTERN,
        convert_tools,
        flatten,
        is_universal,
        normalize_mcp_servers,
        parse_frontmatter,
        render_document,
        slugify,
        split_globs,
    )
    from _layout import (
        HARNESS_ROOT,
        MARKETPLACE_PATH,
        REPO_ROOT,
        SOURCE_AGENTS_ROOT,
        SOURCE_HOOKS_ROOT,
        SOURCE_INSTRUCTIONS_ROOT,
        SOURCE_PLUGINS_ROOT,
        SOURCE_PROMPTS_ROOT,
        SOURCE_SKILLS_ROOT,
    )
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._convert import (  # type: ignore
        AGENT_FIELDS,
        ConversionError,
        HOOK_EVENT_MAP,
        PLUGIN_AGENT_FIELDS,
        PLUGIN_MANIFEST_FIELDS,
        SLUG_PATTERN,
        convert_tools,
        flatten,
        is_universal,
        normalize_mcp_servers,
        parse_frontmatter,
        render_document,
        slugify,
        split_globs,
    )
    from ._layout import (  # type: ignore
        HARNESS_ROOT,
        MARKETPLACE_PATH,
        REPO_ROOT,
        SOURCE_AGENTS_ROOT,
        SOURCE_HOOKS_ROOT,
        SOURCE_INSTRUCTIONS_ROOT,
        SOURCE_PLUGINS_ROOT,
        SOURCE_PROMPTS_ROOT,
        SOURCE_SKILLS_ROOT,
    )

GENERATED_BANNER = (
    "<!-- Generated from {source} by harness/claude-code/scripts/convert_from_copilot.py. "
    "Edit the source, not this file. -->"
)

MARKETPLACE_OWNER = {"name": "paulasilvatech"}
MARKETPLACE_NAME = "copilot-primitives-claude"
MARKETPLACE_DESCRIPTION = (
    "Spec-validated Claude Code primitives generated from the copilot-primitives harness."
)
DEFAULT_AUTHOR = {"name": "paulasilvatech"}
DEFAULT_VERSION = "1.0.0"

# Copilot-only frontmatter that has no Claude Code equivalent on the target type.
DROPPED_AGENT_KEYS = ("user-invocable", "disable-model-invocation", "argument-hint", "target", "handoffs")
DROPPED_COMMAND_KEYS = ("agent", "mode", "name")

# Copilot-only tool identifiers dropped during conversion, reported at the end of a run.
DROPPED_TOOLS: list[str] = []

# Hook features with no Claude Code equivalent, reported at the end of a run.
DROPPED_HOOK_FEATURES: list[str] = []


class Stats(Counter):
    def bump(self, key: str, amount: int = 1) -> None:
        self[key] += amount


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if os.access(source, os.X_OK):
        target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


# ---------------------------------------------------------------------------
# Agents -> subagents
# ---------------------------------------------------------------------------


def convert_agent(source: Path, *, plugin_scoped: bool, dropped: list[str] | None = None) -> str:
    dropped = DROPPED_TOOLS if dropped is None else dropped
    text = read(source)
    data, body = parse_frontmatter(text, source=str(source))
    slug = source.name[: -len(".agent.md")] if source.name.endswith(".agent.md") else source.stem
    if not SLUG_PATTERN.match(slug):
        slug = slugify(slug)

    description = flatten(data.get("description") or data.get("name") or slug)
    if not description:
        raise ConversionError(f"{source}: agent has no description")

    allowed = PLUGIN_AGENT_FIELDS if plugin_scoped else AGENT_FIELDS
    fields: list[tuple[str, Any]] = [("name", slug), ("description", description)]

    tools = convert_tools(data.get("tools"), source=str(source), dropped=dropped)
    if tools:
        fields.append(("tools", ", ".join(tools)))

    for key in ("model", "effort", "maxTurns", "memory", "background", "isolation", "disallowedTools"):
        if key in data and key in allowed:
            fields.append((key, data[key]))

    if "mcp-servers" in data and "mcpServers" in allowed:
        servers = normalize_mcp_servers(data["mcp-servers"])
        if servers:
            fields.append(("mcpServers", servers))

    banner = GENERATED_BANNER.format(source=source.relative_to(REPO_ROOT).as_posix())
    return render_document(fields, f"{banner}\n\n{body.lstrip()}")


# ---------------------------------------------------------------------------
# Instructions -> rules
# ---------------------------------------------------------------------------


def convert_instruction(source: Path) -> str:
    text = read(source)
    data, body = parse_frontmatter(text, source=str(source))
    patterns = split_globs(data.get("applyTo", "**"))
    description = flatten(data.get("description", ""))

    fields: list[tuple[str, Any]] = []
    if not is_universal(patterns):
        fields.append(("paths", patterns))

    banner = GENERATED_BANNER.format(source=source.relative_to(REPO_ROOT).as_posix())
    header = banner
    if description:
        # Rule frontmatter documents only `paths`, so the Copilot description is
        # preserved in the body where it stays visible to Claude.
        header += f"\n\n> **Scope.** {description}"
    if not fields:
        return f"{header}\n\n{body.lstrip()}".rstrip() + "\n"
    return render_document(fields, f"{header}\n\n{body.lstrip()}")


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

SKILL_PASSTHROUGH = (
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "model",
    "effort",
    "paths",
    "shell",
    "license",
    "compatibility",
)


def convert_skill(source: Path, skill_name: str, dropped: list[str] | None = None) -> str:
    dropped = DROPPED_TOOLS if dropped is None else dropped
    text = read(source)
    data, body = parse_frontmatter(text, source=str(source))
    name = str(data.get("name") or skill_name).strip()
    if not SLUG_PATTERN.match(name):
        name = slugify(name)
    description = flatten(data.get("description", ""))
    if not description:
        raise ConversionError(f"{source}: skill has no description")

    fields: list[tuple[str, Any]] = [("name", name), ("description", description)]
    allowed = convert_tools(data.get("allowed-tools"), source=str(source), dropped=dropped)
    if allowed:
        fields.append(("allowed-tools", ", ".join(allowed)))
    disallowed = convert_tools(data.get("disallowed-tools"), source=str(source), dropped=dropped)
    if disallowed:
        fields.append(("disallowed-tools", ", ".join(disallowed)))
    for key in SKILL_PASSTHROUGH:
        if key in data and data[key] is not None:
            fields.append((key, data[key]))
    metadata = data.get("metadata")
    if isinstance(metadata, dict) and metadata:
        fields.append(("metadata", metadata))

    banner = GENERATED_BANNER.format(source=source.relative_to(REPO_ROOT).as_posix())
    return render_document(fields, f"{banner}\n\n{body.lstrip()}")


def convert_skill_dir(source_dir: Path, target_dir: Path, stats: Stats) -> None:
    skill_md = source_dir / "SKILL.md"
    if not skill_md.is_file():
        raise ConversionError(f"{source_dir}: missing SKILL.md")
    write(target_dir / "SKILL.md", convert_skill(skill_md, source_dir.name))
    for path in sorted(source_dir.rglob("*")):
        if path.is_dir() or path == skill_md:
            continue
        if path.name == ".DS_Store" or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        copy_file(path, target_dir / path.relative_to(source_dir))
        stats.bump("skill-resources")


# ---------------------------------------------------------------------------
# Prompts -> commands
# ---------------------------------------------------------------------------


def convert_prompt(source: Path, dropped: list[str] | None = None) -> str:
    dropped = DROPPED_TOOLS if dropped is None else dropped
    text = read(source)
    data, body = parse_frontmatter(text, source=str(source))
    description = flatten(data.get("description", ""))
    if not description:
        raise ConversionError(f"{source}: prompt has no description")

    fields: list[tuple[str, Any]] = [("description", description)]
    hint = data.get("argument-hint")
    if hint:
        fields.append(("argument-hint", flatten(hint)))
    allowed = convert_tools(data.get("tools"), source=str(source), dropped=dropped)
    if allowed:
        fields.append(("allowed-tools", ", ".join(allowed)))
    if data.get("model"):
        fields.append(("model", data["model"]))

    banner = GENERATED_BANNER.format(source=source.relative_to(REPO_ROOT).as_posix())
    return render_document(fields, f"{banner}\n\n{body.lstrip()}")


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------


def _shell_quote(value: str) -> str:
    if value and all(char.isalnum() or char in "-_./:=" for char in value):
        return value
    return "'" + value.replace("'", "'\"'\"'") + "'"


def convert_hook_handler(
    handler: dict[str, Any], *, root_variable: str, package: str | None
) -> tuple[dict[str, Any], list[str]]:
    kind = handler.get("type", "command")
    if kind != "command":
        raise ConversionError(f"unsupported hook handler type {kind!r}")

    notes: list[str] = []
    command = handler.get("bash") or handler.get("command")
    if not command:
        raise ConversionError("hook handler has no command")
    command = str(command).strip()
    if handler.get("powershell"):
        # A Claude Code command hook carries one command string and selects the
        # interpreter with `shell`, so the PowerShell variant cannot be preserved.
        notes.append("powershell-variant")

    # Claude Code resolves plugin hook scripts through ${CLAUDE_PLUGIN_ROOT} and
    # project hook scripts through ${CLAUDE_PROJECT_DIR}. Copilot stores a
    # repository-relative path instead, so rewrite the leading path segment.
    patterns = [rf"(?:\./)?hooks/{re.escape(package)}/(\S+)"] if package else []
    patterns.append(r"(?:\./)?hooks/(\S+)")
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            command = command[: match.start()] + f'"{root_variable}/{match.group(1)}"' + command[match.end() :]
            break

    env = handler.get("env") or {}
    if env:
        # Command hooks accept no `env` field, so environment values are inlined.
        prefix = " ".join(f"{key}={_shell_quote(str(value))}" for key, value in sorted(env.items()))
        command = f"{prefix} {command}"

    cwd = handler.get("cwd")
    if cwd and cwd not in (".", "./"):
        command = f"cd {_shell_quote(str(cwd))} && {command}"

    converted: dict[str, Any] = {"type": "command", "command": command}
    timeout = handler.get("timeoutSec", handler.get("timeout"))
    if timeout:
        converted["timeout"] = int(timeout)
    if handler.get("statusMessage"):
        converted["statusMessage"] = handler["statusMessage"]
    return converted, notes


def convert_hooks(document: dict[str, Any], *, root_variable: str, package: str | None) -> dict[str, Any]:
    events = document.get("hooks") or {}
    converted: dict[str, Any] = {}
    for event, handlers in events.items():
        mapping = HOOK_EVENT_MAP.get(event)
        if mapping is None:
            raise ConversionError(f"unmapped hook event {event!r}")
        claude_event, matcher = mapping
        if not isinstance(handlers, list):
            raise ConversionError(f"hook event {event!r} must hold a list")
        entries = []
        for handler in handlers:
            entry, notes = convert_hook_handler(handler, root_variable=root_variable, package=package)
            entries.append(entry)
            DROPPED_HOOK_FEATURES.extend(notes)
        group: dict[str, Any] = {}
        if matcher is not None:
            group["matcher"] = matcher
        group["hooks"] = entries
        converted.setdefault(claude_event, []).append(group)
    return {"hooks": converted}


def convert_hook_package(source_dir: Path, target_dir: Path, stats: Stats) -> None:
    document = json.loads(read(source_dir / "hooks.json"))
    converted = convert_hooks(
        document, root_variable="${CLAUDE_PROJECT_DIR}/.claude/hooks/" + source_dir.name, package=source_dir.name
    )
    write(target_dir / "hooks.json", json.dumps(converted, indent=2, ensure_ascii=False) + "\n")
    for path in sorted(source_dir.rglob("*")):
        if path.is_dir() or path.name == "hooks.json":
            continue
        if path.name == ".DS_Store" or "__pycache__" in path.parts:
            continue
        copy_file(path, target_dir / path.relative_to(source_dir))
        stats.bump("hook-resources")


# ---------------------------------------------------------------------------
# Plugins
# ---------------------------------------------------------------------------

PLUGIN_COMPONENT_DIRS = {"agents", "skills", "instructions", "prompts", "hooks", "commands", "rules"}


def convert_plugin_manifest(data: dict[str, Any], plugin_name: str) -> dict[str, Any]:
    manifest: dict[str, Any] = {}
    for field in PLUGIN_MANIFEST_FIELDS:
        if field in data and data[field] not in (None, "", [], {}):
            manifest[field] = data[field]
    manifest["name"] = data.get("name") or plugin_name
    manifest.setdefault("version", DEFAULT_VERSION)
    manifest.setdefault("author", DEFAULT_AUTHOR)
    if not manifest.get("description"):
        manifest["description"] = f"Claude Code plugin generated from the {plugin_name} Copilot plugin."
    # Component paths are omitted: Claude Code scans agents/, skills/, commands/,
    # hooks/hooks.json and .mcp.json in the plugin root by default.
    ordered = {field: manifest[field] for field in PLUGIN_MANIFEST_FIELDS if field in manifest}
    return ordered


def convert_plugin(source_dir: Path, target_dir: Path, stats: Stats) -> dict[str, Any]:
    manifest_path = source_dir / "plugin.json"
    raw = json.loads(read(manifest_path)) if manifest_path.is_file() else {}
    manifest = convert_plugin_manifest(raw, source_dir.name)
    write(
        target_dir / ".claude-plugin" / "plugin.json",
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    )

    for entry in sorted(source_dir.iterdir()):
        name = entry.name
        if name in {"plugin.json", ".DS_Store"}:
            continue
        if entry.is_file():
            if name == "mcp.json":
                copy_file(entry, target_dir / ".mcp.json")
                stats.bump("plugin-mcp")
            else:
                copy_file(entry, target_dir / name)
            continue
        if name == "agents":
            for path in sorted(entry.rglob("*.agent.md")):
                relative = path.relative_to(entry).with_suffix("")
                out = target_dir / "agents" / relative.with_suffix("").name
                write(out.with_suffix(".md"), convert_agent(path, plugin_scoped=True))
                stats.bump("plugin-agents")
        elif name == "skills":
            for skill_md in sorted(entry.glob("*/SKILL.md")):
                convert_skill_dir(skill_md.parent, target_dir / "skills" / skill_md.parent.name, stats)
                stats.bump("plugin-skills")
        elif name == "prompts":
            for path in sorted(entry.glob("*.prompt.md")):
                slug = path.name[: -len(".prompt.md")]
                write(target_dir / "commands" / f"{slug}.md", convert_prompt(path))
                stats.bump("plugin-commands")
        elif name == "instructions":
            # Claude Code plugins cannot ship rules, so a plugin-owned instruction
            # file becomes a path-scoped skill, the documented alternative.
            for path in sorted(entry.glob("*.instructions.md")):
                slug = path.name[: -len(".instructions.md")]
                convert_instruction_to_skill(path, target_dir / "skills" / slug)
                stats.bump("plugin-rule-skills")
        elif name == "hooks":
            for hooks_json in sorted(entry.rglob("hooks.json")):
                package_dir = hooks_json.parent
                document = json.loads(read(hooks_json))
                converted = convert_hooks(
                    document, root_variable="${CLAUDE_PLUGIN_ROOT}/hooks", package=package_dir.name
                )
                write(
                    target_dir / "hooks" / "hooks.json",
                    json.dumps(converted, indent=2, ensure_ascii=False) + "\n",
                )
                for path in sorted(package_dir.rglob("*")):
                    if path.is_dir() or path.name == "hooks.json" or "__pycache__" in path.parts:
                        continue
                    copy_file(path, target_dir / "hooks" / path.relative_to(package_dir))
                stats.bump("plugin-hooks")
        else:
            for path in sorted(entry.rglob("*")):
                if path.is_dir() or path.name == ".DS_Store" or "__pycache__" in path.parts:
                    continue
                copy_file(path, target_dir / name / path.relative_to(entry))
                stats.bump("plugin-payload")
    return manifest


def convert_instruction_to_skill(source: Path, target_dir: Path) -> None:
    text = read(source)
    data, body = parse_frontmatter(text, source=str(source))
    slug = source.name[: -len(".instructions.md")]
    if not SLUG_PATTERN.match(slug):
        slug = slugify(slug)
    patterns = split_globs(data.get("applyTo", "**"))
    description = flatten(data.get("description", "")) or f"Conventions from the {slug} instruction file."

    fields: list[tuple[str, Any]] = [("name", slug), ("description", description)]
    if not is_universal(patterns):
        fields.append(("paths", patterns))
    fields.append(("user-invocable", False))

    banner = GENERATED_BANNER.format(source=source.relative_to(REPO_ROOT).as_posix())
    write(target_dir / "SKILL.md", render_document(fields, f"{banner}\n\n{body.lstrip()}"))


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def build(destination: Path, marketplace_path: Path) -> Stats:
    stats = Stats()
    DROPPED_TOOLS.clear()
    DROPPED_HOOK_FEATURES.clear()

    for path in sorted(SOURCE_AGENTS_ROOT.glob("*.agent.md")):
        slug = path.name[: -len(".agent.md")]
        write(destination / "agents" / f"{slug}.md", convert_agent(path, plugin_scoped=False))
        stats.bump("agents")

    for path in sorted(SOURCE_INSTRUCTIONS_ROOT.glob("*.instructions.md")):
        slug = path.name[: -len(".instructions.md")]
        write(destination / "rules" / f"{slug}.md", convert_instruction(path))
        stats.bump("rules")

    for skill_md in sorted(SOURCE_SKILLS_ROOT.glob("*/SKILL.md")):
        convert_skill_dir(skill_md.parent, destination / "skills" / skill_md.parent.name, stats)
        stats.bump("skills")

    for path in sorted(SOURCE_PROMPTS_ROOT.glob("*.prompt.md")):
        slug = path.name[: -len(".prompt.md")]
        write(destination / "commands" / f"{slug}.md", convert_prompt(path))
        stats.bump("commands")

    for hooks_json in sorted(SOURCE_HOOKS_ROOT.glob("*/hooks.json")):
        convert_hook_package(hooks_json.parent, destination / "hooks" / hooks_json.parent.name, stats)
        stats.bump("hooks")

    entries: list[dict[str, Any]] = []
    for plugin_dir in sorted(p for p in SOURCE_PLUGINS_ROOT.iterdir() if p.is_dir()):
        manifest = convert_plugin(plugin_dir, destination / "plugins" / plugin_dir.name, stats)
        stats.bump("plugins")
        entry = {
            "name": manifest["name"],
            "source": f"./harness/claude-code/plugins/{plugin_dir.name}",
            "description": manifest.get("description", ""),
        }
        if manifest.get("version"):
            entry["version"] = manifest["version"]
        entries.append(entry)

    marketplace = {
        "name": MARKETPLACE_NAME,
        "description": MARKETPLACE_DESCRIPTION,
        "owner": MARKETPLACE_OWNER,
        "plugins": entries,
    }
    write(marketplace_path, json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n")
    stats.bump("marketplace-entries", len(entries))
    return stats


def tree_files(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def diff_trees(expected_root: Path, actual_root: Path) -> list[str]:
    problems: list[str] = []
    expected = tree_files(expected_root) if expected_root.exists() else set()
    actual = tree_files(actual_root) if actual_root.exists() else set()
    for missing in sorted(expected - actual):
        problems.append(f"missing: {missing.as_posix()}")
    for extra in sorted(actual - expected):
        problems.append(f"unexpected: {extra.as_posix()}")
    for shared in sorted(expected & actual):
        if not filecmp.cmp(expected_root / shared, actual_root / shared, shallow=False):
            problems.append(f"out of date: {shared.as_posix()}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail when the generated harness has drifted")
    args = parser.parse_args(argv)

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp) / "claude-code"
            staged_marketplace = Path(tmp) / "marketplace.json"
            try:
                build(staging, staged_marketplace)
            except ConversionError as error:
                print(f"conversion error: {error}", file=sys.stderr)
                return 1
            problems: list[str] = []
            for name in ("agents", "rules", "skills", "commands", "hooks", "plugins"):
                problems.extend(
                    f"{name}/{issue}" for issue in diff_trees(staging / name, HARNESS_ROOT / name)
                )
            if not MARKETPLACE_PATH.is_file():
                problems.append(f"missing: {MARKETPLACE_PATH.relative_to(REPO_ROOT).as_posix()}")
            elif not filecmp.cmp(staged_marketplace, MARKETPLACE_PATH, shallow=False):
                problems.append(f"out of date: {MARKETPLACE_PATH.relative_to(REPO_ROOT).as_posix()}")
            if problems:
                print(f"Claude Code harness is out of date ({len(problems)} problems):", file=sys.stderr)
                for problem in problems[:40]:
                    print(f"  {problem}", file=sys.stderr)
                if len(problems) > 40:
                    print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
                print(
                    "Run: python3 harness/claude-code/scripts/convert_from_copilot.py",
                    file=sys.stderr,
                )
                return 1
            print("Claude Code harness is up to date.")
            return 0

    for name in ("agents", "rules", "skills", "commands", "hooks", "plugins"):
        target = HARNESS_ROOT / name
        if target.exists():
            shutil.rmtree(target)
    try:
        stats = build(HARNESS_ROOT, MARKETPLACE_PATH)
    except ConversionError as error:
        print(f"conversion error: {error}", file=sys.stderr)
        return 1

    print("Generated the Claude Code harness:")
    for key in sorted(stats):
        print(f"  {key}: {stats[key]}")
    if DROPPED_TOOLS:
        print("  dropped Copilot-only tool identifiers:")
        for name, count in sorted(Counter(DROPPED_TOOLS).items()):
            print(f"    {name}: {count}")
    if DROPPED_HOOK_FEATURES:
        print("  dropped hook features:")
        for name, count in sorted(Counter(DROPPED_HOOK_FEATURES).items()):
            print(f"    {name}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

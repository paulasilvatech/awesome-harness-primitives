#!/usr/bin/env python3
"""Validate the Claude Code harness against the documented Claude Code contract.

The checks mirror ``docs/CLAUDE-CODE-HARNESS-SPEC.md``: subagent, rule, skill,
command, plugin, and hook files must use only fields and identifiers that Claude
Code documents for that primitive type.

Exit codes: 0 when clean, 1 when an error is found, 1 with ``--strict`` when a
warning is found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from _convert import (
        AGENT_FIELDS,
        CLAUDE_TOOLS,
        PLUGIN_AGENT_FIELDS,
        PLUGIN_MANIFEST_FIELDS,
        RULE_FIELDS,
        SKILL_FIELDS,
        SLUG_PATTERN,
        parse_frontmatter,
    )
    from _layout import (
        AGENTS_ROOT,
        COMMANDS_ROOT,
        HARNESS_ROOT,
        HOOKS_ROOT,
        MARKETPLACE_PATH,
        PLUGINS_ROOT,
        REPO_ROOT,
        RULES_ROOT,
        SKILLS_ROOT,
    )
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._convert import (  # type: ignore
        AGENT_FIELDS,
        CLAUDE_TOOLS,
        PLUGIN_AGENT_FIELDS,
        PLUGIN_MANIFEST_FIELDS,
        RULE_FIELDS,
        SKILL_FIELDS,
        SLUG_PATTERN,
        parse_frontmatter,
    )
    from ._layout import (  # type: ignore
        AGENTS_ROOT,
        COMMANDS_ROOT,
        HARNESS_ROOT,
        HOOKS_ROOT,
        MARKETPLACE_PATH,
        PLUGINS_ROOT,
        REPO_ROOT,
        RULES_ROOT,
        SKILLS_ROOT,
    )

HOOK_EVENTS = frozenset(
    {
        "SessionStart",
        "Setup",
        "UserPromptSubmit",
        "UserPromptExpansion",
        "PreToolUse",
        "PermissionRequest",
        "PermissionDenied",
        "PostToolUse",
        "PostToolUseFailure",
        "PostToolBatch",
        "Notification",
        "MessageDisplay",
        "SubagentStart",
        "SubagentStop",
        "TaskCreated",
        "TaskCompleted",
        "Stop",
        "StopFailure",
        "TeammateIdle",
        "InstructionsLoaded",
        "ConfigChange",
        "CwdChanged",
        "DirectoryAdded",
        "FileChanged",
        "WorktreeCreate",
        "WorktreeRemove",
        "PreCompact",
        "PostCompact",
        "Elicitation",
        "ElicitationResult",
        "SessionEnd",
    }
)
MATCHER_EVENTS = frozenset(
    {"PreToolUse", "PostToolUse", "PostToolUseFailure", "PermissionRequest", "PermissionDenied",
     "SessionStart", "Setup", "SessionEnd", "Notification", "FileChanged"}
)
HOOK_HANDLER_TYPES = frozenset({"command", "http", "mcp_tool", "prompt", "agent"})
COMMAND_HOOK_FIELDS = frozenset(
    {"type", "command", "args", "timeout", "if", "statusMessage", "once", "async", "asyncRewake", "shell"}
)
MODEL_VALUES = frozenset({"sonnet", "opus", "haiku", "fable", "inherit"})
EFFORT_VALUES = frozenset({"low", "medium", "high", "xhigh", "max"})
MCP_TOOL_PATTERN = re.compile(r"^mcp__[A-Za-z0-9_-]+(?:__[A-Za-z0-9_.-]+)?$")
PERMISSION_RULE_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9_]*)\((.*)\)$")
DESCRIPTION_LIMIT = 1536


@dataclass
class Finding:
    level: str
    path: str
    message: str

    def render(self) -> str:
        return f"[{self.level.upper()}] {self.path}: {self.message}"


class Report:
    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self.counts: Counter[str] = Counter()

    def error(self, path: Path | str, message: str) -> None:
        self.findings.append(Finding("error", _rel(path), message))

    def warn(self, path: Path | str, message: str) -> None:
        self.findings.append(Finding("warning", _rel(path), message))

    @property
    def errors(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.level == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.level == "warning"]


def _rel(path: Path | str) -> str:
    if isinstance(path, str):
        return path
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _tokens(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        tokens: list[str] = []
        for item in value:
            tokens.extend(_tokens(item))
        return tokens
    tokens = []
    depth = 0
    current = ""
    for char in str(value):
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        if depth == 0 and (char == "," or char.isspace()):
            if current.strip():
                tokens.append(current.strip())
            current = ""
            continue
        current += char
    if current.strip():
        tokens.append(current.strip())
    return tokens


def check_tools(report: Report, path: Path, field: str, value: Any) -> None:
    for token in _tokens(value):
        if token in CLAUDE_TOOLS or MCP_TOOL_PATTERN.match(token):
            continue
        rule = PERMISSION_RULE_PATTERN.match(token)
        if rule and (rule.group(1) in CLAUDE_TOOLS or MCP_TOOL_PATTERN.match(rule.group(1))):
            continue
        report.error(path, f"{field} references unknown Claude Code tool {token!r}")


def check_description(report: Report, path: Path, data: dict[str, Any]) -> None:
    description = data.get("description")
    if not description or not str(description).strip():
        report.error(path, "description is required")
        return
    combined = len(str(description)) + len(str(data.get("when_to_use", "")))
    if combined > DESCRIPTION_LIMIT:
        report.warn(
            path,
            f"description and when_to_use total {combined} characters and are truncated at {DESCRIPTION_LIMIT}",
        )


def check_enum(report: Report, path: Path, field: str, value: Any, allowed: Iterable[str]) -> None:
    if value is None:
        return
    text = str(value).strip()
    allowed = set(allowed)
    if text in allowed:
        return
    if field == "model" and re.match(r"^claude-[a-z0-9.-]+$", text):
        return
    report.error(path, f"{field} value {text!r} is not one of {sorted(allowed)}")


# ---------------------------------------------------------------------------
# Primitive checks
# ---------------------------------------------------------------------------


def validate_agent(report: Report, path: Path, *, plugin_scoped: bool) -> None:
    data, body = parse_frontmatter(path.read_text(encoding="utf-8"), source=str(path))
    allowed = PLUGIN_AGENT_FIELDS if plugin_scoped else AGENT_FIELDS

    name = str(data.get("name", "")).strip()
    if not name:
        report.error(path, "name is required")
    elif ":" in name:
        report.error(path, "name cannot contain ':', which is reserved for plugin-scoped identifiers")
    elif not SLUG_PATTERN.match(name):
        report.error(path, f"name {name!r} must use lowercase letters, digits, and hyphens")
    elif name != path.stem:
        report.warn(path, f"name {name!r} does not match the file name {path.stem!r}")

    check_description(report, path, data)
    for key in data:
        if key not in allowed:
            reason = "is not supported for plugin-shipped subagents" if key in AGENT_FIELDS else "is not a subagent field"
            report.error(path, f"frontmatter key {key!r} {reason}")
    check_tools(report, path, "tools", data.get("tools"))
    check_tools(report, path, "disallowedTools", data.get("disallowedTools"))
    check_enum(report, path, "model", data.get("model"), MODEL_VALUES)
    check_enum(report, path, "effort", data.get("effort"), EFFORT_VALUES)
    if data.get("isolation") not in (None, "worktree"):
        report.error(path, "isolation only accepts 'worktree'")
    if not body.strip():
        report.error(path, "subagent has an empty system prompt body")


def validate_rule(report: Report, path: Path) -> None:
    data, body = parse_frontmatter(path.read_text(encoding="utf-8"), source=str(path))
    for key in data:
        if key not in RULE_FIELDS:
            report.error(path, f"frontmatter key {key!r} is not a rule field; rules document only 'paths'")
    paths = data.get("paths")
    if paths is not None:
        if not isinstance(paths, list) or not paths:
            report.error(path, "paths must be a non-empty list of glob patterns")
        else:
            for pattern in paths:
                if not isinstance(pattern, str) or not pattern.strip():
                    report.error(path, f"invalid glob pattern {pattern!r}")
                elif "[" in pattern and "]" not in pattern:
                    report.error(path, f"glob pattern {pattern!r} has an unterminated bracket expression")
    if not body.strip():
        report.error(path, "rule body is empty")


def validate_skill(report: Report, path: Path, *, expected_name: str) -> None:
    data, body = parse_frontmatter(path.read_text(encoding="utf-8"), source=str(path))
    for key in data:
        if key not in SKILL_FIELDS:
            report.error(path, f"frontmatter key {key!r} is not a skill field")
    name = str(data.get("name", "")).strip()
    if name and not SLUG_PATTERN.match(name):
        report.error(path, f"name {name!r} must use lowercase letters, digits, and hyphens")
    if name and name != expected_name:
        report.warn(path, f"name {name!r} does not match the directory name {expected_name!r}")
    check_description(report, path, data)
    check_tools(report, path, "allowed-tools", data.get("allowed-tools"))
    check_tools(report, path, "disallowed-tools", data.get("disallowed-tools"))
    check_enum(report, path, "effort", data.get("effort"), EFFORT_VALUES)
    if data.get("context") not in (None, "fork"):
        report.error(path, "context only accepts 'fork'")
    if data.get("agent") is not None and data.get("context") != "fork":
        report.error(path, "agent only applies when context is 'fork'")
    metadata = data.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        report.error(path, "metadata must be a map")
    compatibility = data.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > 500:
        report.error(path, "compatibility accepts at most 500 characters")
    if not body.strip():
        report.error(path, "skill body is empty")


def validate_command(report: Report, path: Path) -> None:
    data, body = parse_frontmatter(path.read_text(encoding="utf-8"), source=str(path))
    for key in data:
        if key not in SKILL_FIELDS:
            report.error(path, f"frontmatter key {key!r} is not a command field")
    check_description(report, path, data)
    check_tools(report, path, "allowed-tools", data.get("allowed-tools"))
    check_tools(report, path, "disallowed-tools", data.get("disallowed-tools"))
    if not body.strip():
        report.error(path, "command body is empty")


def validate_hooks_document(report: Report, path: Path, *, plugin_scoped: bool) -> None:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        report.error(path, f"invalid JSON: {error}")
        return
    if not isinstance(document, dict) or "hooks" not in document:
        report.error(path, "hook configuration must be an object with a 'hooks' key")
        return
    for key in document:
        if key != "hooks":
            report.error(path, f"unknown key {key!r}; Claude Code hook files declare only 'hooks'")
    events = document["hooks"]
    if not isinstance(events, dict) or not events:
        report.error(path, "'hooks' must be a non-empty object keyed by event name")
        return
    root_variable = "${CLAUDE_PLUGIN_ROOT}" if plugin_scoped else "${CLAUDE_PROJECT_DIR}"
    for event, groups in events.items():
        if event not in HOOK_EVENTS:
            report.error(path, f"unknown hook event {event!r}")
            continue
        if not isinstance(groups, list):
            report.error(path, f"event {event!r} must hold a list of matcher groups")
            continue
        for group in groups:
            if not isinstance(group, dict) or "hooks" not in group:
                report.error(path, f"event {event!r} group must be an object with a 'hooks' list")
                continue
            if "matcher" in group and event not in MATCHER_EVENTS:
                report.warn(path, f"event {event!r} ignores 'matcher'")
            for handler in group.get("hooks", []):
                if not isinstance(handler, dict):
                    report.error(path, f"event {event!r} handler must be an object")
                    continue
                kind = handler.get("type")
                if kind not in HOOK_HANDLER_TYPES:
                    report.error(path, f"unknown hook handler type {kind!r}")
                    continue
                if kind != "command":
                    continue
                for key in handler:
                    if key not in COMMAND_HOOK_FIELDS:
                        report.error(path, f"command hook does not support field {key!r}")
                command = handler.get("command")
                if not command:
                    report.error(path, "command hook has no command")
                elif "hooks/" in str(command) and root_variable not in str(command):
                    report.warn(
                        path,
                        f"command uses a relative script path; prefer {root_variable} so it resolves at runtime",
                    )
                timeout = handler.get("timeout")
                if timeout is not None and (not isinstance(timeout, int) or timeout <= 0):
                    report.error(path, "timeout must be a positive number of seconds")


def validate_plugin(report: Report, plugin_dir: Path) -> None:
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.is_file():
        report.error(plugin_dir, "missing .claude-plugin/plugin.json")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        report.error(manifest_path, f"invalid JSON: {error}")
        return

    name = str(manifest.get("name", "")).strip()
    if not name:
        report.error(manifest_path, "name is required")
    elif " " in name:
        report.error(manifest_path, "name cannot contain spaces; use kebab-case")
    elif not SLUG_PATTERN.match(name):
        report.error(manifest_path, f"name {name!r} must use lowercase letters, digits, and hyphens")
    elif name != plugin_dir.name:
        report.error(manifest_path, f"name {name!r} does not match the directory name {plugin_dir.name!r}")

    for key in manifest:
        if key not in PLUGIN_MANIFEST_FIELDS:
            report.error(manifest_path, f"unknown manifest field {key!r}; Claude Code ignores it at load time")
    if not manifest.get("version"):
        report.error(manifest_path, "version is required by 'claude plugin validate --strict'")
    if not manifest.get("author"):
        report.error(manifest_path, "author is required by 'claude plugin validate --strict'")
    if not manifest.get("description"):
        report.error(manifest_path, "description is required")

    for agent in sorted((plugin_dir / "agents").glob("*.md")):
        validate_agent(report, agent, plugin_scoped=True)
        report.counts["plugin-agents"] += 1
    for skill in sorted((plugin_dir / "skills").glob("*/SKILL.md")):
        validate_skill(report, skill, expected_name=skill.parent.name)
        report.counts["plugin-skills"] += 1
    for command in sorted((plugin_dir / "commands").glob("*.md")):
        validate_command(report, command)
        report.counts["plugin-commands"] += 1
    hooks_json = plugin_dir / "hooks" / "hooks.json"
    if hooks_json.is_file():
        validate_hooks_document(report, hooks_json, plugin_scoped=True)
        report.counts["plugin-hooks"] += 1
    mcp_json = plugin_dir / ".mcp.json"
    if mcp_json.is_file():
        try:
            mcp = json.loads(mcp_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            report.error(mcp_json, f"invalid JSON: {error}")
        else:
            if not isinstance(mcp, dict) or "mcpServers" not in mcp:
                report.error(mcp_json, "MCP configuration must define 'mcpServers'")
        report.counts["plugin-mcp"] += 1
    if plugin_dir.joinpath("instructions").is_dir():
        report.error(plugin_dir, "plugins cannot ship rules; convert instructions to path-scoped skills")
    report.counts["plugins"] += 1


def validate_marketplace(report: Report) -> None:
    if not MARKETPLACE_PATH.is_file():
        report.error(MARKETPLACE_PATH, "marketplace manifest is missing")
        return
    try:
        marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        report.error(MARKETPLACE_PATH, f"invalid JSON: {error}")
        return
    for field in ("name", "owner", "plugins"):
        if field not in marketplace:
            report.error(MARKETPLACE_PATH, f"{field} is required")
    owner = marketplace.get("owner")
    if isinstance(owner, dict) and not owner.get("name"):
        report.error(MARKETPLACE_PATH, "owner.name is required")
    seen: set[str] = set()
    for entry in marketplace.get("plugins", []):
        name = entry.get("name")
        source = entry.get("source")
        if not name or not source:
            report.error(MARKETPLACE_PATH, f"plugin entry {entry!r} needs a name and a source")
            continue
        if name in seen:
            report.error(MARKETPLACE_PATH, f"duplicate plugin entry {name!r}")
        seen.add(name)
        if isinstance(source, str) and source.startswith("./"):
            target = REPO_ROOT / source[2:]
            if not (target / ".claude-plugin" / "plugin.json").is_file():
                report.error(MARKETPLACE_PATH, f"plugin entry {name!r} points at {source}, which has no manifest")
    report.counts["marketplace-entries"] += len(marketplace.get("plugins", []))


def run(report: Report) -> None:
    for path in sorted(AGENTS_ROOT.glob("*.md")):
        validate_agent(report, path, plugin_scoped=False)
        report.counts["agents"] += 1
    for path in sorted(RULES_ROOT.rglob("*.md")):
        validate_rule(report, path)
        report.counts["rules"] += 1
    for path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        validate_skill(report, path, expected_name=path.parent.name)
        report.counts["skills"] += 1
    for path in sorted(COMMANDS_ROOT.glob("*.md")):
        validate_command(report, path)
        report.counts["commands"] += 1
    for path in sorted(HOOKS_ROOT.glob("*/hooks.json")):
        validate_hooks_document(report, path, plugin_scoped=False)
        report.counts["hooks"] += 1
    for plugin_dir in sorted(p for p in PLUGINS_ROOT.iterdir() if p.is_dir()):
        validate_plugin(report, plugin_dir)
    validate_marketplace(report)

    names = Counter(path.stem for path in AGENTS_ROOT.glob("*.md"))
    for name, count in names.items():
        if count > 1:
            report.error(AGENTS_ROOT, f"duplicate subagent name {name!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = parser.parse_args(argv)

    if not HARNESS_ROOT.is_dir():
        print(f"missing harness directory: {HARNESS_ROOT}", file=sys.stderr)
        return 1

    report = Report()
    run(report)

    if args.json:
        print(
            json.dumps(
                {
                    "counts": dict(sorted(report.counts.items())),
                    "errors": [finding.__dict__ for finding in report.errors],
                    "warnings": [finding.__dict__ for finding in report.warnings],
                },
                indent=2,
            )
        )
    else:
        for finding in report.findings:
            print(finding.render())
        summary = ", ".join(f"{key}: {value}" for key, value in sorted(report.counts.items()))
        print(f"Validated Claude Code harness ({summary})")
        print(f"errors: {len(report.errors)}, warnings: {len(report.warnings)}")

    if report.errors:
        return 1
    if args.strict and report.warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

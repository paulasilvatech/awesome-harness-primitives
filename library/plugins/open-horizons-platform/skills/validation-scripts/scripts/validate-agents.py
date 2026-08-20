#!/usr/bin/env python3
"""Validate Open Horizons GitHub Copilot customization primitives."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - CI installs PyYAML; local fallback is limited.
    yaml = None


CUSTOMIZATION_DIR = Path(__file__).resolve().parents[3]
REPO_ROOT = (
    CUSTOMIZATION_DIR.parent
    if CUSTOMIZATION_DIR.name == ".github"
    else CUSTOMIZATION_DIR
)
GITHUB_DIR = CUSTOMIZATION_DIR
AGENTS_DIR = GITHUB_DIR / "agents"
PROMPTS_DIR = GITHUB_DIR / "prompts"
SKILLS_DIR = GITHUB_DIR / "skills"
INSTRUCTIONS_DIR = GITHUB_DIR / "instructions"
ISSUE_TEMPLATE_DIR = GITHUB_DIR / "ISSUE_TEMPLATE"
DOCS_DIR = GITHUB_DIR / "docs"
MCP_CONFIG = next(
    (
        path
        for path in (GITHUB_DIR / "mcp.json", GITHUB_DIR / ".mcp.json")
        if path.exists()
    ),
    GITHUB_DIR / "mcp.json",
)

VALID_AGENT_FIELDS = {
    "description",
    "name",
    "argument-hint",
    "tools",
    "model",
    "target",
    "user-invocable",
    "disable-model-invocation",
    "handoffs",
    "mcp-servers",
    "metadata",
}
VALID_PROMPT_FIELDS = {"description", "name", "mode", "agent", "model", "tools", "argument-hint"}
VALID_SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "user-invocable",
    "disable-model-invocation",
    "argument-hint",
    "metadata",
    "tags",
}
VALID_INSTRUCTION_FIELDS = {"description", "applyTo", "excludeAgent", "name"}
VALID_SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
AGENT_LABEL = re.compile(r"agent:([a-zA-Z0-9_.-]+)")
ISSUE_FORM_ID = re.compile(r"^[A-Za-z0-9_-]+$")
PROMPT_TEMPLATE_VAR = re.compile(r"\{\{[^}]+\}\}")
SKILL_NAME_TOKEN = re.compile(r"\b[a-z0-9]+(?:-[a-z0-9]+)+\b")
SKILL_PATH = re.compile(r"\.\./skills/([a-z0-9]+(?:-[a-z0-9]+)*)/SKILL\.md")
H2_HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
AGENT_REQUIRED_SECTIONS = (
    "Mission",
    "Activation and Scope",
    "Operating Principles",
    "What This Agent Knows",
    "What This Agent Does NOT Know",
    "Output Format",
    "Definition of Done",
    "Anti-Patterns This Agent Rejects",
)
INSTRUCTION_REQUIRED_SECTIONS = (
    "Conventions",
    "Do / Do Not",
    "Checklist Before Opening a PR",
)
VALID_TOOL_TOKENS = {
    "*",
    "read",
    "view",
    "notebookread",
    "create",
    "edit",
    "editfiles",
    "multiedit",
    "write",
    "notebookedit",
    "execute",
    "bash",
    "shell",
    "runcommands",
    "agent",
    "custom-agent",
    "task",
    "grep",
    "glob",
    "lsp",
    "powershell",
    "read_powershell",
    "stop_powershell",
    "read_bash",
    "stop_bash",
    "list_bash",
    "web_fetch",
    "web_search",
    "session_store_sql",
    "fetch_copilot_cli_documentation",
    "context_board",
    "write_agent",
    "read_agent",
    "list_agents",
    "webfetch",
    "websearch",
    "todowrite",
}
VS_CODE_NAMESPACED_TOOL_IDS = {
    "search/codebase",
    "search/usages",
    "search/changes",
    "read/problems",
    "read/terminallastcommand",
    "web/fetch",
}
UNVERIFIED_TOOL_TOKENS = {
    "all": "unknown tool names are ignored; use `*` or omit `tools` to enable all tools",
    "terminal": "unknown tool names are ignored; use `bash`, `execute`, or `shell`",
    "run": "unknown tool names are ignored; use `bash`, `execute`, `shell`, or `runCommands`",
    "codebase": "use `search/codebase` for VS Code or `grep` and `glob` for CLI",
    "changes": "use `search/changes` for VS Code or `grep`, `glob`, and `view` for CLI",
    "fetch": "use `web/fetch` for VS Code or `web_fetch` for CLI",
    "githubrepo": "use a configured GitHub MCP tool such as `github/*`",
}
REDUNDANT_FLOOR_TOOL_TOKENS = {"sql", "skill"}
MCP_TOOL = re.compile(r"^([a-zA-Z0-9_.-]+/(?:\*|[a-zA-Z0-9_.-]+))(?::(.+))?$")
TOOLS_BLOAT_THRESHOLD = 25
MAX_AGENT_BODY_CHARS = 30_000
MAX_SKILL_BODY_LINES = 500


class ValidationReport:
    def __init__(self) -> None:
        self.infos: list[str] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def info(self, path: Path, message: str) -> None:
        self.infos.append(f"{display_path(path)}: {message}")

    def error(self, path: Path, message: str) -> None:
        self.errors.append(f"{display_path(path)}: {message}")

    def warn(self, path: Path, message: str) -> None:
        self.warnings.append(f"{display_path(path)}: {message}")

    def print(self) -> None:
        if self.infos:
            print("\nInfo")
            for info in self.infos:
                print(f"  - {info}")
        if self.errors:
            print("\nErrors")
            for error in self.errors:
                print(f"  - {error}")
        if self.warnings:
            print("\nWarnings")
            for warning in self.warnings:
                print(f"  - {warning}")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def is_installable_primitive(path: Path) -> bool:
    """Exclude documentation samples from installed primitive validation."""
    try:
        path.relative_to(DOCS_DIR)
        return False
    except ValueError:
        return True


def installable_paths(pattern: str, base: Path) -> list[Path]:
    return sorted(path for path in base.glob(pattern) if is_installable_primitive(path))


def parse_frontmatter_fallback(frontmatter: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith(" "):
            continue
        key, sep, value = line.partition(":")
        if sep:
            metadata[key.strip()] = value.strip().strip("\"'")
    return metadata


def split_frontmatter(path: Path, report: ValidationReport) -> tuple[dict[str, Any], str] | None:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        report.error(path, "missing YAML frontmatter")
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        report.error(path, "unterminated YAML frontmatter")
        return None

    try:
        if yaml is None:
            metadata = parse_frontmatter_fallback(parts[1])
        else:
            loaded = yaml.safe_load(parts[1]) or {}
            if not isinstance(loaded, dict):
                report.error(path, "frontmatter must be a YAML mapping")
                return None
            metadata = loaded
    except Exception as exc:  # noqa: BLE001 - include parser detail in validation output.
        report.error(path, f"invalid YAML frontmatter: {exc}")
        return None

    return metadata, parts[2].strip()


def require_string(path: Path, metadata: dict[str, Any], key: str, report: ValidationReport) -> None:
    value = metadata.get(key)
    if not isinstance(value, str) or not value.strip():
        report.error(path, f"missing or empty `{key}`")


def validate_required_sections(
    path: Path,
    body: str,
    required: tuple[str, ...],
    report: ValidationReport,
) -> None:
    headings = H2_HEADING.findall(body)
    missing = [heading for heading in required if heading not in headings]
    duplicates = [heading for heading in required if headings.count(heading) > 1]
    if missing:
        report.error(path, f"missing required sections: {', '.join(missing)}")
    if duplicates:
        report.error(path, f"duplicate required sections: {', '.join(duplicates)}")
    if not missing and not duplicates:
        positions = [headings.index(heading) for heading in required]
        if positions != sorted(positions):
            report.error(path, "required sections are out of template order")


def error_unknown_agent_fields(
    path: Path,
    metadata: dict[str, Any],
    report: ValidationReport,
) -> None:
    for field in sorted(set(metadata) - VALID_AGENT_FIELDS):
        if field == "infer":
            report.error(path, "retired frontmatter field `infer`; remove it")
        elif field == "infer_tools":
            report.error(path, "invalid frontmatter field `infer_tools`; use `tools`")
        elif field == "user-invokable":
            report.error(
                path,
                "unsupported frontmatter field `user-invokable`; use `user-invocable`",
            )
        elif field in {"mode", "hidden", "agents", "agent", "title"}:
            report.error(path, f"invalid agent frontmatter field `{field}`; remove it")
        else:
            report.error(path, f"unknown frontmatter field `{field}`")


def warn_unknown_fields(
    path: Path,
    metadata: dict[str, Any],
    allowed_fields: set[str],
    report: ValidationReport,
) -> None:
    for field in sorted(set(metadata) - allowed_fields):
        if field in {"infer", "user-invokable", "mode"}:
            replacement = "user-invocable" if field == "user-invokable" else "a supported field"
            report.error(path, f"unsupported frontmatter field `{field}`; use `{replacement}`")
        else:
            report.warn(path, f"unknown frontmatter field `{field}`")


def git_tracked_files(report: ValidationReport) -> list[str]:
    if GITHUB_DIR.name != ".github":
        return []
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files"],
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        report.warn(REPO_ROOT, f"could not list tracked files for `applyTo` validation: {exc}")
        return []
    return [line for line in result.stdout.splitlines() if line]


def matches_apply_to(pattern: str, tracked_file: str) -> bool:
    """Match Copilot-style globs where `*` stays local and `**` is recursive."""
    pattern_parts = tuple(part for part in pattern.split("/") if part)
    path_parts = tuple(part for part in tracked_file.split("/") if part)

    def match(pattern_index: int, path_index: int) -> bool:
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        current = pattern_parts[pattern_index]
        if current == "**":
            return match(pattern_index + 1, path_index) or (
                path_index < len(path_parts) and match(pattern_index, path_index + 1)
            )
        return (
            path_index < len(path_parts)
            and fnmatch.fnmatchcase(path_parts[path_index], current)
            and match(pattern_index + 1, path_index + 1)
        )

    return match(0, 0)


def collect_agent_names(report: ValidationReport) -> set[str]:
    agent_names = {"ask", "agent", "plan"}
    for path in installable_paths("*.agent.md", AGENTS_DIR):
        parsed = split_frontmatter(path, report)
        if not parsed:
            continue
        metadata, _ = parsed
        name = metadata.get("name")
        if isinstance(name, str) and name.strip():
            agent_names.add(name.strip())
        agent_names.add(path.name.removesuffix(".agent.md"))
    return agent_names


def collect_skill_names() -> set[str]:
    return {path.parent.name for path in installable_paths("*/SKILL.md", SKILLS_DIR)}


def collect_mcp_server_keys(report: ValidationReport) -> set[str]:
    if not MCP_CONFIG.exists():
        return set()
    try:
        loaded = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(MCP_CONFIG, f"invalid JSON: {exc}")
        return set()
    if not isinstance(loaded, dict):
        report.error(MCP_CONFIG, "root must be a JSON object")
        return set()
    servers = loaded.get("mcpServers", {})
    if not isinstance(servers, dict):
        report.error(MCP_CONFIG, "`mcpServers` must be an object")
        return set()
    return set(servers)


def validate_agents(
    agent_names: set[str],
    skill_names: set[str],
    mcp_server_keys: set[str],
    report: ValidationReport,
) -> None:
    for path in installable_paths("*.agent.md", AGENTS_DIR):
        parsed = split_frontmatter(path, report)
        if not parsed:
            continue
        metadata, body = parsed
        error_unknown_agent_fields(path, metadata, report)
        require_string(path, metadata, "description", report)
        validate_agent_tools(path, metadata, mcp_server_keys, report)
        validate_agent_handoffs(path, metadata, agent_names, report)
        validate_agent_skill_references(path, body, skill_names, report)

        if not body:
            report.error(path, "empty agent body")
        validate_required_sections(path, body, AGENT_REQUIRED_SECTIONS, report)
        if len(body) > MAX_AGENT_BODY_CHARS:
            report.error(
                path,
                f"agent body is {len(body)} chars; maximum is {MAX_AGENT_BODY_CHARS}",
            )


def validate_agent_tools(
    path: Path,
    metadata: dict[str, Any],
    mcp_server_keys: set[str],
    report: ValidationReport,
) -> None:
    tools = metadata.get("tools")
    if tools is not None and not isinstance(tools, (list, str)):
        report.error(path, "`tools` must be a list or comma-separated string")
        return
    if tools is None:
        return

    tool_names = [tools] if isinstance(tools, str) else tools
    if len(tool_names) > TOOLS_BLOAT_THRESHOLD:
        report.warn(
            path,
            f"`tools` has {len(tool_names)} entries; consider <= {TOOLS_BLOAT_THRESHOLD} "
            "portable aliases plus required MCP tools to avoid copy-paste bloat",
        )

    for tool in tool_names:
        if not isinstance(tool, str) or not tool.strip():
            report.error(path, "`tools` entries must be non-empty strings")
            continue
        tool = tool.strip()
        normalized_tool = tool.lower()
        if normalized_tool == "search":
            report.error(
                path,
                f"AG017: `tools` token `{tool}` grants no Copilot CLI capability; "
                "use `grep` and `glob`",
            )
            continue
        if normalized_tool == "web":
            report.error(
                path,
                f"AG017: `tools` token `{tool}` grants no Copilot CLI capability; "
                "use `web_fetch` and `web_search`",
            )
            continue
        if normalized_tool == "todo":
            report.error(
                path,
                f"AG017: `tools` token `{tool}` grants no Copilot CLI capability; remove it",
            )
            continue
        if normalized_tool in UNVERIFIED_TOOL_TOKENS:
            report.warn(
                path,
                f"AG017: `tools` token `{tool}` is not verified in VS Code or Copilot CLI; "
                f"{UNVERIFIED_TOOL_TOKENS[normalized_tool]}",
            )
            continue
        if normalized_tool in REDUNDANT_FLOOR_TOOL_TOKENS:
            report.warn(
                path,
                f"AG017: `tools` token `{tool}` is always available; listing it is harmless but pointless",
            )
            continue
        if normalized_tool in VALID_TOOL_TOKENS or normalized_tool in VS_CODE_NAMESPACED_TOOL_IDS:
            continue

        mcp_match = MCP_TOOL.match(tool)
        if mcp_match:
            server_key = mcp_match.group(1).split("/", 1)[0]
            if server_key not in mcp_server_keys:
                report.error(
                    path,
                    f"AG017: MCP `tools` token `{tool}` uses unknown server `{server_key}`; "
                    f"add it to `{display_path(MCP_CONFIG)}` or fix the token",
                )
            continue

        report.warn(
            path,
            f"AG017: `tools` entry `{tool}` is not a recognized Copilot token or MCP "
            "tool form `server/*`/`server/tool`",
        )


def validate_agent_handoffs(
    path: Path,
    metadata: dict[str, Any],
    agent_names: set[str],
    report: ValidationReport,
) -> None:
    handoffs = metadata.get("handoffs", [])
    if handoffs is not None and not isinstance(handoffs, list):
        report.error(path, "`handoffs` must be a list")
        return
    if not isinstance(handoffs, list):
        return
    if handoffs:
        report.warn(path, "`handoffs` is VS Code-only and may not be portable to GitHub Copilot")

    for index, handoff in enumerate(handoffs, start=1):
        if not isinstance(handoff, dict):
            report.error(path, f"handoff #{index} must be a mapping")
            continue
        target = handoff.get("agent")
        if target not in agent_names:
            report.error(path, f"handoff #{index} references unknown agent `{target}`")


def validate_agent_skill_references(
    path: Path,
    body: str,
    skill_names: set[str],
    report: ValidationReport,
) -> None:
    in_skill_section = False
    for line_number, line in enumerate(body.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            in_skill_section = bool(re.search(r"\bskills?\b", stripped, re.IGNORECASE))

        candidates = set(SKILL_PATH.findall(line))
        explicit_skill_context = bool(
            re.search(r"(?:^|[./])skills?/|SKILL\.md|\bskills?\b", line, re.IGNORECASE)
        )
        if in_skill_section and explicit_skill_context:
            candidates.update(SKILL_NAME_TOKEN.findall(line))

        for candidate in sorted(candidates):
            if candidate in skill_names:
                continue
            if candidate in SKILL_PATH.findall(line) or explicit_skill_context:
                report.error(
                    path,
                    f"line {line_number}: references unknown skill `{candidate}`; "
                    "create `<customization-root>/skills/<name>/SKILL.md` or fix the reference",
                )


def validate_prompts(agent_names: set[str], report: ValidationReport) -> None:
    for path in installable_paths("*.prompt.md", PROMPTS_DIR):
        parsed = split_frontmatter(path, report)
        if not parsed:
            continue
        metadata, body = parsed
        warn_unknown_fields(path, metadata, VALID_PROMPT_FIELDS, report)
        if "mode" in metadata:
            report.info(path, "`mode` is a legacy alias; `agent` is the current documented key")
        require_string(path, metadata, "description", report)
        target_agent = metadata.get("agent")
        if target_agent is not None and target_agent not in agent_names:
            report.error(path, f"references unknown agent `{target_agent}`")
        if ":latest" in body:
            report.error(path, "contains forbidden deployment tag `:latest`")
        if "@master" in body:
            report.error(path, "references mutable GitHub Action ref `@master`")
        for line_number, line in enumerate(body.splitlines(), start=1):
            if PROMPT_TEMPLATE_VAR.search(line):
                report.error(
                    path,
                    f"line {line_number}: uses unsupported `{{{{var}}}}` syntax; "
                    "use `${input:name}` instead",
                )


def validate_skills(report: ValidationReport) -> None:
    for path in installable_paths("*/SKILL.md", SKILLS_DIR):
        parsed = split_frontmatter(path, report)
        if not parsed:
            continue
        metadata, body = parsed
        warn_unknown_fields(path, metadata, VALID_SKILL_FIELDS, report)
        require_string(path, metadata, "name", report)
        require_string(path, metadata, "description", report)
        name = metadata.get("name")
        if isinstance(name, str):
            if name != path.parent.name:
                report.error(
                    path,
                    f"skill name `{name}` must match parent directory `{path.parent.name}`",
                )
            if not 1 <= len(name) <= 64:
                report.error(path, "skill name must be 1-64 characters long")
            if not VALID_SKILL_NAME.match(name):
                report.error(
                    path,
                    "skill name must use lowercase letters, numbers, and single hyphens "
                    "between alphanumeric groups",
                )
        description = metadata.get("description")
        if isinstance(description, str) and not 1 <= len(description) <= 1024:
            report.error(path, "`description` must be 1-1024 characters long")
        if not body:
            report.error(path, "empty skill body")
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > MAX_SKILL_BODY_LINES:
            report.warn(
                path,
                f"SKILL.md is {line_count} lines; keep SKILL.md under {MAX_SKILL_BODY_LINES} "
                "lines and move bulk content to resources",
            )


def validate_instructions(tracked_files: list[str], report: ValidationReport) -> None:
    for path in installable_paths("*.instructions.md", INSTRUCTIONS_DIR):
        parsed = split_frontmatter(path, report)
        if not parsed:
            continue
        metadata, body = parsed
        warn_unknown_fields(path, metadata, VALID_INSTRUCTION_FIELDS, report)
        apply_to = metadata.get("applyTo")
        if not isinstance(apply_to, str) or not apply_to.strip():
            report.warn(
                path,
                "missing or empty `applyTo`; optional by spec, but repo convention expects it "
                "so instructions auto-apply",
            )
        elif apply_to.strip() in {"**", "**/*"}:
            report.error(path, "`applyTo` is too broad")
        else:
            patterns = [pattern.strip() for pattern in apply_to.split(",")]
            if any(not pattern for pattern in patterns):
                report.error(path, "`applyTo` contains an empty glob")
                continue
            if tracked_files:
                validate_apply_to_liveness(path, apply_to, tracked_files, report)
        validate_required_sections(path, body, INSTRUCTION_REQUIRED_SECTIONS, report)


def validate_apply_to_liveness(
    path: Path,
    apply_to: str,
    tracked_files: list[str],
    report: ValidationReport,
) -> None:
    patterns = [pattern.strip() for pattern in apply_to.split(",")]
    for pattern in patterns:
        if not pattern:
            report.error(path, "`applyTo` contains an empty glob")
            continue
        if not any(matches_apply_to(pattern, tracked_file) for tracked_file in tracked_files):
            report.error(
                path,
                f"`applyTo` glob `{pattern}` matches zero tracked files; "
                "fix the glob or remove the dead instruction",
            )


def validate_issue_templates(agent_names: set[str], report: ValidationReport, strict: bool) -> None:
    for path in sorted(ISSUE_TEMPLATE_DIR.glob("*.yml")) + sorted(ISSUE_TEMPLATE_DIR.glob("*.yaml")):
        content = path.read_text(encoding="utf-8")
        for label in AGENT_LABEL.findall(content):
            if label == "executing":
                continue
            if label not in agent_names:
                message = f"issue template uses unknown agent label `agent:{label}`"
                if strict:
                    report.error(path, message)
                else:
                    report.warn(path, message)
        if yaml is None:
            report.warn(path, "PyYAML is unavailable; issue form structure was not validated")
            continue
        try:
            data = yaml.safe_load(content)
        except Exception as exc:  # noqa: BLE001 - parser details belong in validation output.
            report.error(path, f"invalid issue template YAML: {exc}")
            continue
        if not isinstance(data, dict):
            report.error(path, "issue template root must be a mapping")
            continue
        if path.stem == "config":
            validate_issue_config(path, data, report)
        else:
            validate_issue_form(path, data, report)


def validate_issue_config(
    path: Path,
    data: dict[str, Any],
    report: ValidationReport,
) -> None:
    blank = data.get("blank_issues_enabled")
    if blank is not None and not isinstance(blank, bool):
        report.error(path, "`blank_issues_enabled` must be a boolean")
    links = data.get("contact_links")
    if links is not None and not isinstance(links, list):
        report.error(path, "`contact_links` must be a list")
    elif isinstance(links, list):
        for index, link in enumerate(links, start=1):
            if not isinstance(link, dict):
                report.error(path, f"contact link #{index} must be a mapping")
                continue
            for field in ("name", "url", "about"):
                if not isinstance(link.get(field), str) or not link[field].strip():
                    report.error(path, f"contact link #{index} requires non-empty `{field}`")


def validate_issue_form(
    path: Path,
    data: dict[str, Any],
    report: ValidationReport,
) -> None:
    for field in ("name", "description"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            report.error(path, f"issue form requires non-empty `{field}`")
    for field in ("labels", "assignees"):
        value = data.get(field)
        if value is not None and not (
            isinstance(value, str)
            or (isinstance(value, list) and all(isinstance(item, str) for item in value))
        ):
            report.error(path, f"`{field}` must be a string or a list of strings")

    body = data.get("body")
    if not isinstance(body, list) or not body:
        report.error(path, "issue form `body` must be a non-empty list")
        return

    seen_ids: set[str] = set()
    valid_types = {"markdown", "input", "textarea", "dropdown", "checkboxes"}
    for index, item in enumerate(body, start=1):
        if not isinstance(item, dict):
            report.error(path, f"body item #{index} must be a mapping")
            continue
        item_type = item.get("type")
        if item_type not in valid_types:
            report.error(path, f"body item #{index} has unknown type `{item_type}`")
            continue
        attributes = item.get("attributes")
        if not isinstance(attributes, dict):
            report.error(path, f"body item #{index} requires an `attributes` mapping")
            continue
        if item_type == "markdown":
            if not isinstance(attributes.get("value"), str) or not attributes["value"].strip():
                report.error(path, f"markdown body item #{index} requires non-empty `attributes.value`")
            continue

        item_id = item.get("id")
        if not isinstance(item_id, str) or not ISSUE_FORM_ID.fullmatch(item_id):
            report.error(path, f"body item #{index} requires a valid alphanumeric, `_`, or `-` id")
        elif item_id in seen_ids:
            report.error(path, f"body item #{index} duplicates id `{item_id}`")
        else:
            seen_ids.add(item_id)
        if not isinstance(attributes.get("label"), str) or not attributes["label"].strip():
            report.error(path, f"body item #{index} requires non-empty `attributes.label`")
        validations = item.get("validations")
        if validations is not None and not isinstance(validations, dict):
            report.error(path, f"body item #{index} `validations` must be a mapping")
        if item_type in {"dropdown", "checkboxes"}:
            options = attributes.get("options")
            if not isinstance(options, list) or not options:
                report.error(path, f"{item_type} body item #{index} requires non-empty options")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Open Horizons GitHub Copilot primitives")
    parser.add_argument("--strict", action="store_true", help="fail on issue-template agent label drift")
    args = parser.parse_args()

    report = ValidationReport()
    agent_names = collect_agent_names(report)
    skill_names = collect_skill_names()
    mcp_server_keys = collect_mcp_server_keys(report)
    tracked_files = git_tracked_files(report)
    validate_agents(agent_names, skill_names, mcp_server_keys, report)
    validate_prompts(agent_names, report)
    validate_skills(report)
    validate_instructions(tracked_files, report)
    validate_issue_templates(agent_names, report, args.strict)

    print("Validated customization primitives:")
    print(f"  Agents: {len(installable_paths('*.agent.md', AGENTS_DIR))}")
    print(f"  Prompts: {len(installable_paths('*.prompt.md', PROMPTS_DIR))}")
    print(f"  Skills: {len(installable_paths('*/SKILL.md', SKILLS_DIR))}")
    print(f"  Instructions: {len(installable_paths('*.instructions.md', INSTRUCTIONS_DIR))}")
    report.print()

    if report.errors:
        return 1

    print("\nAll GitHub Copilot customization primitives passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

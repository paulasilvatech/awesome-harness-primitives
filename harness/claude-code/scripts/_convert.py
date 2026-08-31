"""Shared conversion helpers that translate Copilot primitives into Claude Code primitives.

Every mapping in this module is traceable to first-party Claude Code documentation
recorded in ``docs/CLAUDE-CODE-VALIDATION.md``. The module is dependency-light and
prefers PyYAML when available, falling back to a small parser for the YAML subset
used by primitive frontmatter.
"""

from __future__ import annotations

import ast
import json
import re
from typing import Any, Iterable

try:  # pragma: no cover - environment dependent
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - environment dependent
    yaml = None

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Built-in Claude Code tool names, from https://code.claude.com/docs/en/tools-reference
CLAUDE_TOOLS = frozenset(
    {
        "Agent",
        "Artifact",
        "AskUserQuestion",
        "Bash",
        "CronCreate",
        "CronDelete",
        "CronList",
        "Edit",
        "EndConversation",
        "EnterPlanMode",
        "EnterWorktree",
        "ExitPlanMode",
        "ExitWorktree",
        "Glob",
        "Grep",
        "LSP",
        "ListAgents",
        "ListMcpResourcesTool",
        "Monitor",
        "NotebookEdit",
        "PowerShell",
        "PushNotification",
        "Read",
        "ReadMcpResourceTool",
        "RemoteTrigger",
        "ReportFindings",
        "ScheduleWakeup",
        "SendFeedback",
        "SendMessage",
        "SendUserFile",
        "ShareOnboardingGuide",
        "Skill",
        "TaskCreate",
        "TaskGet",
        "TaskList",
        "TaskOutput",
        "TaskStop",
        "TaskUpdate",
        "TodoWrite",
        "ToolSearch",
        "WaitForMcpServers",
        "WebFetch",
        "WebSearch",
        "Workflow",
        "Write",
    }
)

# Copilot CLI and VS Code tool identifiers mapped onto Claude Code tool names.
TOOL_MAP: dict[str, tuple[str, ...]] = {
    "read": ("Read",),
    "grep": ("Grep",),
    "glob": ("Glob",),
    "search": ("Grep", "Glob"),
    "edit": ("Edit", "Write"),
    "write": ("Write",),
    "execute": ("Bash",),
    "runcommands": ("Bash",),
    "terminal": ("Bash",),
    "web_fetch": ("WebFetch",),
    "web_search": ("WebSearch",),
    "web": ("WebFetch", "WebSearch"),
    "fetch": ("WebFetch",),
    "agent": ("Agent",),
    "todo": ("TodoWrite",),
    "ask": ("AskUserQuestion",),
    "notebook": ("NotebookEdit",),
    "skill": ("Skill",),
}

# Wildcards that mean "every tool"; Claude Code inherits all tools when `tools` is omitted.
TOOL_WILDCARDS = frozenset({"*", "all"})

# Copilot CLI and VS Code tools with no Claude Code equivalent. They are dropped
# during conversion and reported so the loss stays visible.
UNSUPPORTED_TOOLS = frozenset(
    {
        "sql",
        "fetch_copilot_cli_documentation",
        "runtests",
        "problems",
        "usages",
        "changes",
        "codebase",
        "extensions",
        "vscodeapi",
        "githubrepo",
        "openSimpleBrowser",
    }
)

# Copilot hook events mapped onto Claude Code hook events and their matcher.
# A matcher of ``None`` means the event takes no matcher.
# https://code.claude.com/docs/en/hooks
HOOK_EVENT_MAP: dict[str, tuple[str, str | None]] = {
    "preToolUse": ("PreToolUse", "*"),
    "postToolUse": ("PostToolUse", "*"),
    "preMcpToolCall": ("PreToolUse", "mcp__.*"),
    "postMcpToolCall": ("PostToolUse", "mcp__.*"),
    "sessionStart": ("SessionStart", None),
    "sessionEnd": ("SessionEnd", None),
    "userPromptSubmitted": ("UserPromptSubmit", None),
    "userPromptSubmit": ("UserPromptSubmit", None),
    "stop": ("Stop", None),
    "notification": ("Notification", None),
    "preCompact": ("PreCompact", None),
    "postCompact": ("PostCompact", None),
    "subagentStart": ("SubagentStart", None),
    "subagentStop": ("SubagentStop", None),
}

# Fields accepted by `claude plugin validate --strict` on a plugin manifest.
PLUGIN_MANIFEST_FIELDS = (
    "name",
    "displayName",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)

# Frontmatter fields documented for Claude Code subagents.
AGENT_FIELDS = frozenset(
    {
        "name",
        "description",
        "tools",
        "disallowedTools",
        "model",
        "permissionMode",
        "maxTurns",
        "skills",
        "mcpServers",
        "hooks",
        "memory",
        "background",
        "effort",
        "isolation",
    }
)

# Frontmatter fields plugin-shipped subagents may declare.
PLUGIN_AGENT_FIELDS = AGENT_FIELDS - {"permissionMode", "mcpServers", "hooks"}

# Frontmatter fields documented for Claude Code skills and commands.
SKILL_FIELDS = frozenset(
    {
        "name",
        "description",
        "when_to_use",
        "argument-hint",
        "arguments",
        "disable-model-invocation",
        "user-invocable",
        "allowed-tools",
        "disallowed-tools",
        "model",
        "effort",
        "context",
        "agent",
        "background",
        "hooks",
        "paths",
        "shell",
        "metadata",
        "license",
        "compatibility",
    }
)

# Frontmatter fields documented for Claude Code rules.
RULE_FIELDS = frozenset({"paths"})


class ConversionError(ValueError):
    """Raised when a source primitive cannot be converted without losing meaning."""


# ---------------------------------------------------------------------------
# Frontmatter parsing and emission
# ---------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return the raw frontmatter block and the body of a markdown document."""
    normalized = text.lstrip("\ufeff")
    if not normalized.startswith("---"):
        return None, normalized
    match = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", normalized, re.DOTALL)
    if not match:
        return None, normalized
    return match.group(1), normalized[match.end() :]


def parse_frontmatter(text: str, *, source: str) -> tuple[dict[str, Any], str]:
    raw, body = split_frontmatter(text)
    if raw is None:
        return {}, body
    try:
        data = (
            yaml.safe_load(raw)
            if yaml is not None
            else fallback_yaml_parse(raw)
        )
    except Exception as error:  # pragma: no cover - malformed source
        raise ConversionError(f"{source}: invalid YAML frontmatter: {error}") from error
    if data is None:
        return {}, body
    if not isinstance(data, dict):
        raise ConversionError(f"{source}: frontmatter must be a mapping")
    return data, body


def fallback_yaml_parse(raw: str) -> dict[str, Any]:
    src = raw.splitlines()
    first = _next_yaml_content(src, 0)
    if first >= len(src):
        return {}
    value, end = _parse_yaml_node(src, first, _yaml_indent(src[first]))
    trailing = _next_yaml_content(src, end)
    if trailing != len(src):
        raise ValueError(f"cannot parse line: {src[trailing]}")
    if not isinstance(value, dict):
        raise ValueError("frontmatter is not a map")
    return value


def _next_yaml_content(src: list[str], index: int) -> int:
    while index < len(src):
        stripped = src[index].strip()
        if stripped and not stripped.startswith("#"):
            return index
        index += 1
    return index


def _yaml_indent(line: str) -> int:
    if "\t" in line[: len(line) - len(line.lstrip())]:
        raise ValueError("tabs are not supported in YAML indentation")
    return len(line) - len(line.lstrip(" "))


def _parse_yaml_node(
    src: list[str],
    index: int,
    indent: int,
) -> tuple[Any, int]:
    stripped = src[index].strip()
    if stripped.startswith("- "):
        return _parse_yaml_sequence(src, index, indent)
    if re.match(r"^[A-Za-z0-9_.-]+\s*:", stripped):
        return _parse_yaml_mapping(src, index, indent)
    return parse_scalar(stripped), index + 1


def _parse_yaml_mapping(
    src: list[str],
    index: int,
    indent: int,
) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while True:
        index = _next_yaml_content(src, index)
        if index >= len(src):
            break
        line = src[index]
        current_indent = _yaml_indent(line)
        stripped = line.strip()
        if (
            current_indent < indent
            or current_indent != indent
            or stripped.startswith("- ")
        ):
            break
        if ":" not in stripped:
            raise ValueError(f"cannot parse mapping line: {line}")
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise ValueError("empty key")
        index += 1
        if raw_value in {"|", ">", "|-", ">-"}:
            result[key], index = _parse_yaml_block_scalar(
                src,
                index,
                indent,
                raw_value,
            )
            continue
        if raw_value:
            result[key] = parse_scalar(raw_value)
            continue
        child = _next_yaml_content(src, index)
        if child >= len(src) or _yaml_indent(src[child]) <= indent:
            result[key] = {}
            index = child
            continue
        result[key], index = _parse_yaml_node(
            src,
            child,
            _yaml_indent(src[child]),
        )
    return result, index


def _parse_yaml_sequence(
    src: list[str],
    index: int,
    indent: int,
) -> tuple[list[Any], int]:
    result: list[Any] = []
    mapping_item = re.compile(r"^([A-Za-z0-9_.-]+)\s*:(.*)$")
    while True:
        index = _next_yaml_content(src, index)
        if index >= len(src):
            break
        line = src[index]
        if (
            _yaml_indent(line) != indent
            or not line.strip().startswith("- ")
        ):
            break
        raw_item = line.strip()[2:].strip()
        index += 1
        match = mapping_item.match(raw_item)
        if match is None:
            result.append(parse_scalar(raw_item))
            continue
        key, raw_value = match.groups()
        item: dict[str, Any] = {
            key: (
                parse_scalar(raw_value.strip())
                if raw_value.strip()
                else {}
            )
        }
        child = _next_yaml_content(src, index)
        if child < len(src) and _yaml_indent(src[child]) > indent:
            child_indent = _yaml_indent(src[child])
            if raw_value.strip():
                remainder, index = _parse_yaml_mapping(
                    src,
                    child,
                    child_indent,
                )
                item.update(remainder)
            else:
                item[key], index = _parse_yaml_node(
                    src,
                    child,
                    child_indent,
                )
        result.append(item)
    return result, index


def _parse_yaml_block_scalar(
    src: list[str],
    index: int,
    parent_indent: int,
    marker: str,
) -> tuple[str, int]:
    block: list[str] = []
    content_indent: int | None = None
    while index < len(src):
        line = src[index]
        if line.strip():
            indent = _yaml_indent(line)
            if indent <= parent_indent:
                break
            content_indent = (
                indent
                if content_indent is None
                else min(content_indent, indent)
            )
        block.append(line)
        index += 1
    base_indent = (
        content_indent
        if content_indent is not None
        else parent_indent + 2
    )
    dedented = [
        line[base_indent:] if line.strip() else ""
        for line in block
    ]
    text = "\n".join(dedented)
    if marker.startswith(">"):
        text = " ".join(line.strip() for line in dedented)
    if not marker.endswith("-"):
        text += "\n"
    return text, index


def parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except Exception:
            inner = value[1:-1].strip()
            return (
                []
                if not inner
                else [parse_scalar(item.strip()) for item in inner.split(",")]
            )
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if value.startswith('"') and value.endswith('"'):
        try:
            return ast.literal_eval(value)
        except Exception:
            return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except Exception:
            pass
    return value.split(" #", 1)[0].strip()


_PLAIN_SCALAR = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _./+,()*|=-]*$")
_YAML_RESERVED = re.compile(r":(?:\s|$)|\s#")


def _quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if (
        text
        and _PLAIN_SCALAR.match(text)
        and not _YAML_RESERVED.search(text)
        and not text.endswith(" ")
    ):
        return text
    return _quote(text)


def _fold(text: str, width: int = 96) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def _emit(key: str, value: Any, indent: int, out: list[str]) -> None:
    pad = " " * indent
    if isinstance(value, dict):
        out.append(f"{pad}{key}:")
        for sub_key, sub_value in value.items():
            _emit(str(sub_key), sub_value, indent + 2, out)
        return
    if isinstance(value, (list, tuple)):
        if not value:
            out.append(f"{pad}{key}: []")
            return
        out.append(f"{pad}{key}:")
        for item in value:
            if isinstance(item, (dict, list, tuple)):
                raise ConversionError(f"nested sequences are not emitted for key {key!r}")
            out.append(f"{pad}  - {_scalar(item)}")
        return
    if isinstance(value, str) and len(value) > 96 and "\n" not in value:
        folded = _fold(value)
        out.append(f"{pad}{key}: >-")
        for line in folded:
            out.append(f"{pad}  {line}")
        return
    if isinstance(value, str) and "\n" in value:
        out.append(f"{pad}{key}: |-")
        for line in value.rstrip("\n").split("\n"):
            out.append(f"{pad}  {line}" if line else pad)
        return
    out.append(f"{pad}{key}: {_scalar(value)}")


def dump_frontmatter(fields: Iterable[tuple[str, Any]]) -> str:
    """Render an ordered mapping as a deterministic YAML frontmatter block."""
    out: list[str] = ["---"]
    for key, value in fields:
        if value is None:
            continue
        _emit(key, value, 0, out)
    out.append("---")
    return "\n".join(out) + "\n"


def render_document(fields: Iterable[tuple[str, Any]], body: str) -> str:
    text = dump_frontmatter(fields)
    body = body.lstrip("\n")
    if body:
        text += "\n" + body
    if not text.endswith("\n"):
        text += "\n"
    return text


# ---------------------------------------------------------------------------
# Value conversion
# ---------------------------------------------------------------------------


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not SLUG_PATTERN.match(slug):
        raise ConversionError(f"cannot derive a Claude Code name from {value!r}")
    return slug


def flatten(value: Any) -> str:
    return " ".join(str(value).split())


def _tool_tokens(value: Any) -> list[str]:
    """Split a tool declaration into tokens.

    Separators inside parentheses belong to a Claude Code permission rule such as
    ``Bash(gh issue:*)`` and must not split the token.
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        tokens: list[str] = []
        for item in value:
            tokens.extend(_tool_tokens(item))
        return tokens
    if not isinstance(value, str):
        raise ConversionError(f"unsupported tool list: {value!r}")

    tokens = []
    depth = 0
    current = ""
    for char in value:
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
    return [token.strip("'\"") for token in tokens if token.strip("'\"")]


def _sanitize_server(name: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_")
    if not sanitized:
        raise ConversionError(f"unsupported MCP server name {name!r}")
    return sanitized


def _mcp_reference(token: str) -> str:
    server, _, tool = token.rpartition("/")
    server = server.strip()
    tool = tool.strip()
    if not server:
        raise ConversionError(f"unsupported MCP tool reference {token!r}")
    server = _sanitize_server(server)
    if tool in ("", "*"):
        return f"mcp__{server}"
    return f"mcp__{server}__{tool}"


def convert_tools(value: Any, *, source: str, dropped: list[str] | None = None) -> list[str] | None:
    """Map Copilot tool identifiers to Claude Code tool names.

    Returns ``None`` when the source grants every tool, which Claude Code expresses
    by omitting the field so the subagent inherits the full tool set.
    """
    tokens = _tool_tokens(value)
    if not tokens:
        return None
    mapped: list[str] = []
    for token in tokens:
        lowered = token.lower()
        if lowered in TOOL_WILDCARDS:
            return None
        rule = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*)\((.*)\)", token)
        if rule and rule.group(1) in CLAUDE_TOOLS:
            # Already a Claude Code permission rule such as `Bash(git:*)`.
            mapped.append(token)
            continue
        if token in CLAUDE_TOOLS:
            mapped.append(token)
            continue
        if lowered in TOOL_MAP:
            mapped.extend(TOOL_MAP[lowered])
            continue
        if lowered in UNSUPPORTED_TOOLS:
            if dropped is not None:
                dropped.append(token)
            continue
        if "/" in token:
            mapped.append(_mcp_reference(token))
            continue
        if re.fullmatch(r"[A-Za-z0-9_.-]+", token):
            # A bare MCP server name, such as `playwright`.
            mapped.append(f"mcp__{_sanitize_server(token)}")
            continue
        raise ConversionError(f"{source}: unmapped tool identifier {token!r}")
    seen: set[str] = set()
    ordered: list[str] = []
    for name in mapped:
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered or None


def split_globs(value: Any) -> list[str]:
    """Split a Copilot ``applyTo`` value into individual glob patterns.

    Commas inside brace groups belong to the pattern and must not split it.
    """
    if isinstance(value, (list, tuple)):
        patterns: list[str] = []
        for item in value:
            patterns.extend(split_globs(item))
        return patterns
    text = str(value).strip()
    if not text:
        return []
    patterns = []
    depth = 0
    current = ""
    for char in text:
        if char == "{":
            depth += 1
        elif char == "}":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            patterns.append(current.strip())
            current = ""
            continue
        current += char
    patterns.append(current.strip())
    return [pattern.strip("'\" ") for pattern in patterns if pattern.strip("'\" ")]


UNIVERSAL_GLOBS = frozenset({"**", "**/*", "*", "**/**"})


def is_universal(patterns: Iterable[str]) -> bool:
    patterns = list(patterns)
    return not patterns or all(pattern in UNIVERSAL_GLOBS for pattern in patterns)


def normalize_mcp_servers(value: Any) -> list[str] | dict[str, Any] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        names = [part for part in re.split(r"[,\s]+", value.strip()) if part]
    elif isinstance(value, (list, tuple)):
        names = [str(item).strip() for item in value if str(item).strip()]
    else:
        raise ConversionError(f"unsupported mcp-servers value: {value!r}")
    return names or None

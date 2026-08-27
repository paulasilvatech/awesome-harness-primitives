#!/usr/bin/env python3
"""Request approval before high-impact Backstage tool operations."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

MAX_PAYLOAD_BYTES = 1_000_000
MAX_TEXT_CHARS = 100_000
EXECUTION_TOOL_MARKERS = (
    "bash",
    "execute",
    "powershell",
    "runcommand",
    "shell",
    "terminal",
)
EDIT_TOOL_MARKERS = ("edit", "write", "create", "patch")
GENERAL_RISKS = (
    (
        re.compile(
            r"\b(?:npx|npm\s+exec|yarn\s+dlx|pnpm\s+dlx)\s+"
            r"@backstage/create-app(?:@[\w.+-]+)?\b",
            re.IGNORECASE,
        ),
        "creating a Backstage application",
    ),
    (
        re.compile(r"\bbackstage-cli\s+versions:bump\b", re.IGNORECASE),
        "changing Backstage package versions",
    ),
    (
        re.compile(
            r"\b(?:npx\s+)?@techdocs/cli\s+publish\b|\btechdocs-cli\s+publish\b",
            re.IGNORECASE,
        ),
        "publishing TechDocs content",
    ),
    (
        re.compile(r"\b(?:npm|yarn|pnpm)\s+publish\b", re.IGNORECASE),
        "publishing a package",
    ),
    (
        re.compile(r"\bkubectl\s+apply\b", re.IGNORECASE),
        "applying a Kubernetes deployment",
    ),
    (
        re.compile(r"\bhelm\s+(?:install|upgrade)\b", re.IGNORECASE),
        "installing or upgrading a Helm release",
    ),
    (
        re.compile(r"\bdocker\s+push\b", re.IGNORECASE),
        "publishing a container image",
    ),
)
CORE_RISKS = (
    (
        re.compile(r"\byarn\s+(?:run\s+)?build(?=\s|$|[;&])", re.IGNORECASE),
        "running a Backstage core root build",
    ),
    (
        re.compile(r"\byarn\s+(?:run\s+)?release\b", re.IGNORECASE),
        "running a Backstage core release",
    ),
    (
        re.compile(r"\b(?:yarn\s+)?changeset\s+version\b", re.IGNORECASE),
        "versioning Backstage core changesets",
    ),
)


def emit_ask(reason: str) -> None:
    json.dump(
        {
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        },
        sys.stdout,
        separators=(",", ":"),
    )
    sys.stdout.write("\n")


def read_payload() -> tuple[dict[str, Any] | None, str | None]:
    raw = sys.stdin.buffer.read(MAX_PAYLOAD_BYTES + 1)
    if len(raw) > MAX_PAYLOAD_BYTES:
        return None, "Backstage safety hook received an oversized payload."
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "Backstage safety hook could not decode the tool payload."
    try:
        payload = json.loads(decoded)
    except json.JSONDecodeError:
        return None, "Backstage safety hook could not parse the tool payload."
    if not isinstance(payload, dict):
        return None, "Backstage safety hook expected a JSON object payload."
    return payload, None


def first_string(payload: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    calls = payload.get("toolCalls")
    if isinstance(calls, list) and calls and isinstance(calls[0], dict):
        for key in keys:
            value = calls[0].get(key)
            if isinstance(value, str) and value:
                return value
    return ""


def flatten_strings(value: Any, *, depth: int = 0) -> list[str]:
    if depth > 8:
        return []
    if isinstance(value, str):
        return [value[:MAX_TEXT_CHARS]]
    if isinstance(value, dict):
        output: list[str] = []
        for nested in value.values():
            output.extend(flatten_strings(nested, depth=depth + 1))
            if sum(len(item) for item in output) >= MAX_TEXT_CHARS:
                break
        return output
    if isinstance(value, list):
        output = []
        for nested in value:
            output.extend(flatten_strings(nested, depth=depth + 1))
            if sum(len(item) for item in output) >= MAX_TEXT_CHARS:
                break
        return output
    return []


def tool_context(payload: dict[str, Any]) -> tuple[str, str]:
    name = first_string(
        payload,
        ("toolName", "tool_name", "mcpToolName", "mcp_tool_name", "name"),
    )
    values: list[str] = []
    for key in (
        "toolInput",
        "tool_input",
        "toolArgs",
        "tool_args",
        "input",
        "args",
    ):
        values.extend(flatten_strings(payload.get(key)))
    calls = payload.get("toolCalls")
    if isinstance(calls, list) and calls and isinstance(calls[0], dict):
        values.extend(flatten_strings(calls[0]))
    return name, " ".join(values)[:MAX_TEXT_CHARS]


def normalized_tool_name(name: str) -> str:
    return name.casefold().replace("_", "").replace("-", "")


def is_tool(name: str, markers: tuple[str, ...]) -> bool:
    normalized = normalized_tool_name(name)
    return any(marker in normalized for marker in markers)


def repository_url(package: dict[str, Any]) -> str:
    value = package.get("repository")
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and isinstance(value.get("url"), str):
        return value["url"]
    return ""


def is_backstage_core(root: Path) -> bool:
    package_file = root / "package.json"
    if not package_file.is_file():
        return False
    try:
        package = json.loads(package_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    if not isinstance(package, dict):
        return False
    repo = repository_url(package).casefold()
    return (
        "backstage/backstage" in repo
        and (root / ".changeset").is_dir()
        and (root / "packages/frontend-plugin-api").is_dir()
        and (root / "packages/backend-plugin-api").is_dir()
    )


def invalid_core_tsc(command_text: str) -> bool:
    for match in re.finditer(r"\byarn\s+(?:run\s+)?tsc\b([^;&\n]*)", command_text, re.IGNORECASE):
        if match.group(1).strip():
            return True
    return False


def risk_reason(tool_name: str, tool_text: str, *, core_root: bool) -> str | None:
    if is_tool(tool_name, EXECUTION_TOOL_MARKERS):
        for pattern, reason in GENERAL_RISKS:
            if pattern.search(tool_text):
                return reason
        if core_root:
            for pattern, reason in CORE_RISKS:
                if pattern.search(tool_text):
                    return reason
            if invalid_core_tsc(tool_text):
                return "running Backstage core root typechecking with unsupported arguments"
    if is_tool(tool_name, EDIT_TOOL_MARKERS):
        if "backstage.json" in tool_text and re.search(
            r"[\"']version[\"']\s*:", tool_text, re.IGNORECASE
        ):
            return "changing the Backstage version recorded in backstage.json"
    return None


def main() -> int:
    mode = os.environ.get("BACKSTAGE_EXPERT_HOOK_MODE", "ask").casefold()
    if mode == "off":
        sys.stdin.buffer.read()
        return 0
    if mode not in {"ask", "audit"}:
        mode = "ask"

    payload, error = read_payload()
    if error is not None:
        if mode == "ask":
            emit_ask(error)
        return 0
    assert payload is not None

    name, text = tool_context(payload)
    reason = risk_reason(name, text, core_root=is_backstage_core(Path.cwd()))
    if reason is not None and mode == "ask":
        emit_ask(
            f"Backstage Expert requires explicit approval before {reason}. "
            "Review scope, impact, validation, and rollback before continuing."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

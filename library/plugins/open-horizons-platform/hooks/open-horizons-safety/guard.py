#!/usr/bin/env python3
"""Request confirmation before destructive Open Horizons tool operations."""

from __future__ import annotations

import json
import os
import re
import sys
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
RISK_PATTERNS = (
    (
        re.compile(r"\bterraform(?:[\s/_.:-]+)(?:apply|destroy)\b", re.IGNORECASE),
        "Terraform apply or destroy",
    ),
    (
        re.compile(
            r"\b(?:az|azure)(?:[\s/_.:-]+)(?:group|resource|aks)"
            r"(?:[\s/_.:-]+)(?:delete|remove)\b",
            re.IGNORECASE,
        ),
        "Azure resource deletion",
    ),
    (
        re.compile(r"\bkubectl(?:[\s/_.:-]+)(?:delete|drain)\b", re.IGNORECASE),
        "Kubernetes deletion or node drain",
    ),
    (
        re.compile(r"\bhelm(?:[\s/_.:-]+)uninstall\b", re.IGNORECASE),
        "Helm release removal",
    ),
    (
        re.compile(r"\bargocd(?:[\s/_.:-]+)app(?:[\s/_.:-]+)delete\b", re.IGNORECASE),
        "Argo CD application deletion",
    ),
    (
        re.compile(r"\bgh(?:[\s/_.:-]+)repo(?:[\s/_.:-]+)delete\b", re.IGNORECASE),
        "GitHub repository deletion",
    ),
    (
        re.compile(
            r"\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|\s-f(?:\s|$))",
            re.IGNORECASE,
        ),
        "forced Git push",
    ),
    (
        re.compile(
            r"\brm\s+(?:-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r)\s+(?:/|~|\.\.?)(?:\s|$)",
            re.IGNORECASE,
        ),
        "broad recursive file deletion",
    ),
    (
        re.compile(r"\b(?:drop\s+(?:database|table)|truncate\s+table)\b", re.IGNORECASE),
        "destructive database operation",
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
        return None, "Open Horizons safety hook received an oversized payload."
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "Open Horizons safety hook could not decode the tool payload."
    try:
        payload = json.loads(decoded)
    except json.JSONDecodeError:
        return None, "Open Horizons safety hook could not parse the tool payload."
    if not isinstance(payload, dict):
        return None, "Open Horizons safety hook expected a JSON object payload."
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
        flattened: list[str] = []
        for nested in value.values():
            flattened.extend(flatten_strings(nested, depth=depth + 1))
            if sum(len(item) for item in flattened) >= MAX_TEXT_CHARS:
                break
        return flattened
    if isinstance(value, list):
        flattened = []
        for nested in value:
            flattened.extend(flatten_strings(nested, depth=depth + 1))
            if sum(len(item) for item in flattened) >= MAX_TEXT_CHARS:
                break
        return flattened
    return []


def tool_text(payload: dict[str, Any]) -> tuple[str, str, str]:
    event = first_string(payload, ("hook_event_name", "hookEventName", "event"))
    name = first_string(
        payload,
        (
            "toolName",
            "tool_name",
            "mcpToolName",
            "mcp_tool_name",
            "name",
        ),
    )
    values: list[str] = [name]
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
    return event, name, " ".join(values)[:MAX_TEXT_CHARS]


def is_execution_tool(name: str) -> bool:
    normalized = name.casefold().replace("_", "").replace("-", "")
    return not normalized or any(marker in normalized for marker in EXECUTION_TOOL_MARKERS)


def main() -> int:
    mode = os.environ.get("OPEN_HORIZONS_HOOK_MODE", "ask").casefold()
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

    event, name, combined = tool_text(payload)
    normalized_event = event.casefold().replace("_", "")
    if "premcptoolcall" not in normalized_event and not is_execution_tool(name):
        return 0

    for pattern, category in RISK_PATTERNS:
        if pattern.search(combined):
            if mode == "ask":
                emit_ask(
                    f"Open Horizons requires explicit approval before {category}. "
                    "Review scope, impact, cost, and rollback before continuing."
                )
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit agent and VS Code prompt capability metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from _layout import HARNESS_ROOT, PLUGIN_ROOT, REPO_ROOT, SHARED_COMPONENT_SOURCE
    from validate_primitives import (
        LEGACY_PROMPT_TOOLS,
        MCP_TOOL_RE,
        NOOP_TOOLS,
        VSCODE_PROMPT_TOOL_ALIASES,
        VSCODE_PROMPT_TOOL_SETS,
        parse_frontmatter,
    )
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._layout import HARNESS_ROOT, PLUGIN_ROOT, REPO_ROOT, SHARED_COMPONENT_SOURCE
    from .validate_primitives import (
        LEGACY_PROMPT_TOOLS,
        MCP_TOOL_RE,
        NOOP_TOOLS,
        VSCODE_PROMPT_TOOL_ALIASES,
        VSCODE_PROMPT_TOOL_SETS,
        parse_frontmatter,
    )

REPORT_PATH = REPO_ROOT / "docs" / "PRIMITIVE-CAPABILITIES.md"
LEDGER_PATH = REPO_ROOT / "docs" / "PRIMITIVE-CAPABILITIES.json"
VERIFICATION_DATE = "2026-08-21"
FIRST_PARTY_SOURCES = [
    "https://code.visualstudio.com/docs/agent-customization/custom-agents",
    "https://code.visualstudio.com/docs/agent-customization/prompt-files",
    "https://code.visualstudio.com/docs/agents/run/tools",
    "https://code.visualstudio.com/docs/agents/run/approvals",
    "https://docs.github.com/en/copilot/reference/custom-agents-configuration",
]
GENERIC_AGENT_TOOLS = {
    "*",
    "read",
    "view",
    "grep",
    "glob",
    "edit",
    "create",
    "execute",
    "bash",
    "shell",
    "agent",
    "task",
    "web_fetch",
    "web_search",
}
READ_ONLY_RE = re.compile(r"\bread-only (?:policy|reviewer)\b", re.IGNORECASE)
EDIT_POLICY_RE = re.compile(r"\b(?:editing|write) policy\b", re.IGNORECASE)


@dataclass(frozen=True)
class CapabilityRow:
    kind: str
    name: str
    path: str
    ownership: str
    package: str | None
    target: str
    authority: str
    tools_mode: str
    tools: list[str]
    selected_agent: str | None
    model: str | list[str] | None
    status: str
    notes: list[str]


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def read_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def metadata(path: Path, *, required: bool = True) -> tuple[dict[str, Any], str]:
    data, body, present, error = parse_frontmatter(
        path.read_text(encoding="utf-8"),
        required=required,
    )
    if not present or error:
        raise ValueError(f"{path}: invalid frontmatter: {error or 'missing'}")
    return data, body


def tool_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    return []


def authority(body: str) -> str:
    if READ_ONLY_RE.search(body):
        if re.search(r"read-only policy.*source files", body, re.IGNORECASE):
            return "source-read-only"
        return "read-only"
    if EDIT_POLICY_RE.search(body):
        return "bounded-write"
    return "unspecified"


def shared_sources(kind: str) -> Iterable[tuple[Path, str, str | None]]:
    if kind == "agent":
        for path in sorted((HARNESS_ROOT / "agents").glob("*.agent.md")):
            yield path, "shared", None
    else:
        for path in sorted((HARNESS_ROOT / "prompts").glob("*.prompt.md")):
            yield path, "shared", None


def plugin_sources(kind: str) -> Iterable[tuple[Path, str, str | None]]:
    folder = "agents" if kind == "agent" else "prompts"
    pattern = "*.agent.md" if kind == "agent" else "*.prompt.md"
    for plugin_dir in sorted(path for path in PLUGIN_ROOT.iterdir() if path.is_dir()):
        manifest = plugin_dir / "plugin.json"
        if not manifest.is_file():
            continue
        config = read_manifest(manifest).get("extensions", {})
        repository = (
            config.get("com.paulasilvatech.copilot-primitives", {})
            if isinstance(config, dict)
            else {}
        )
        if not (
            isinstance(repository, dict)
            and repository.get("componentSource") == "plugin"
        ):
            continue
        for path in sorted((plugin_dir / folder).glob(pattern)):
            yield path, "plugin", plugin_dir.name


def source_name(path: Path, kind: str, data: dict[str, Any]) -> str:
    name = data.get("name")
    if isinstance(name, str) and name.strip():
        return name.strip()
    suffix = ".agent.md" if kind == "agent" else ".prompt.md"
    return path.name.removesuffix(suffix)


def agent_row(
    path: Path,
    ownership: str,
    package: str | None,
) -> CapabilityRow:
    data, body = metadata(path)
    tools = tool_list(data.get("tools"))
    mode = "inherit-all" if "tools" not in data else ("disabled" if not tools else "allow-list")
    target = str(data.get("target", "vscode+github-copilot"))
    agent_authority = authority(body)
    notes: list[str] = []
    blocking = False
    if data.get("model") is not None:
        notes.append("fixed-model")
        blocking = True
    if agent_authority == "read-only" and mode == "inherit-all":
        notes.append("read-only-inherits-all-tools")
        blocking = True
    if agent_authority == "read-only" and any(
        tool.casefold() in {"edit", "create", "write"} for tool in tools
    ):
        notes.append("read-only-allows-editing")
        blocking = True
    for tool in tools:
        normalized = tool.casefold()
        if normalized in NOOP_TOOLS and target != "vscode":
            notes.append(f"cli-no-op:{tool}")
            blocking = True
        elif normalized not in GENERIC_AGENT_TOOLS and MCP_TOOL_RE.fullmatch(tool):
            notes.append(f"runtime-tool:{tool}")
        elif normalized not in GENERIC_AGENT_TOOLS:
            notes.append(f"environment-tool:{tool}")
    status = "blocked" if blocking else (
        "runtime-verification-required"
        if any(note.startswith(("runtime-tool:", "environment-tool:")) for note in notes)
        else "current-static"
    )
    return CapabilityRow(
        kind="agent",
        name=source_name(path, "agent", data),
        path=relative(path),
        ownership=ownership,
        package=package,
        target=target,
        authority=agent_authority,
        tools_mode=mode,
        tools=tools,
        selected_agent=None,
        model=data.get("model"),
        status=status,
        notes=sorted(set(notes)),
    )


def prompt_row(
    path: Path,
    ownership: str,
    package: str | None,
    agent_ids: set[str],
) -> CapabilityRow:
    data, body = metadata(path)
    tools = tool_list(data.get("tools"))
    mode = "inherit-agent" if "tools" not in data else ("disabled" if not tools else "allow-list")
    selected_agent = data.get("agent")
    notes: list[str] = []
    blocking = False
    if data.get("model") is not None:
        notes.append("fixed-model")
        blocking = True
    if isinstance(selected_agent, str) and selected_agent not in {"ask", "agent", "plan"}:
        if selected_agent not in agent_ids:
            notes.append(f"unknown-agent:{selected_agent}")
            blocking = True
    for tool in tools:
        normalized = tool.casefold()
        if normalized in LEGACY_PROMPT_TOOLS:
            notes.append(f"legacy-tool:{tool}")
            blocking = True
        elif normalized in VSCODE_PROMPT_TOOL_SETS or MCP_TOOL_RE.fullmatch(tool):
            notes.append(f"runtime-tool:{tool}")
        elif normalized not in VSCODE_PROMPT_TOOL_ALIASES:
            notes.append(f"environment-tool:{tool}")
    status = "blocked" if blocking else (
        "runtime-verification-required"
        if any(note.startswith(("runtime-tool:", "environment-tool:")) for note in notes)
        else "current-static"
    )
    return CapabilityRow(
        kind="prompt",
        name=source_name(path, "prompt", data),
        path=relative(path),
        ownership=ownership,
        package=package,
        target="vscode",
        authority=authority(body),
        tools_mode=mode,
        tools=tools,
        selected_agent=selected_agent if isinstance(selected_agent, str) else None,
        model=data.get("model"),
        status=status,
        notes=sorted(set(notes)),
    )


def build_audit() -> dict[str, Any]:
    agent_sources = [*shared_sources("agent"), *plugin_sources("agent")]
    prompt_sources = [*shared_sources("prompt"), *plugin_sources("prompt")]
    agents = [agent_row(*source) for source in agent_sources]
    agent_ids = {
        path.name.removesuffix(".agent.md")
        for path, _ownership, _package in agent_sources
    }
    prompts = [prompt_row(*source, agent_ids) for source in prompt_sources]
    rows = sorted(
        [*agents, *prompts],
        key=lambda row: (row.kind, row.name.casefold(), row.path.casefold()),
    )
    status_counts = Counter(row.status for row in rows)
    return {
        "schemaVersion": 1,
        "verificationDate": VERIFICATION_DATE,
        "firstPartySources": FIRST_PARTY_SOURCES,
        "permissionBoundary": {
            "frontmatterControls": "tool availability and agent/model selection",
            "sessionControls": [
                "chat.permissions.default",
                "chat.tools.eligibleForAutoApproval",
                "chat.tools.urls.autoApprove",
                "chat.tools.terminal.autoApprove",
                "chat.agent.sandbox.enabled",
            ],
            "note": (
                "Default Approvals, Assisted permissions, Bypass Approvals, Autopilot, "
                "managed rules, URL approval, terminal approval, and sandboxing are VS Code "
                "session or policy controls and are not primitive frontmatter fields."
            ),
        },
        "compatibility": {
            "componentSourceCompatibilityValue": SHARED_COMPONENT_SOURCE,
            "copilotCliEvidence": "docs/HARNESS-VALIDATION.md",
        },
        "summary": {
            "agents": len(agents),
            "prompts": len(prompts),
            "blocked": status_counts["blocked"],
            "currentStatic": status_counts["current-static"],
            "runtimeVerificationRequired": status_counts["runtime-verification-required"],
            "fixedModels": sum(row.model is not None for row in rows),
            "readOnlyAgentsInheritingAll": sum(
                row.kind == "agent"
                and row.authority == "read-only"
                and row.tools_mode == "inherit-all"
                for row in rows
            ),
        },
        "rows": [asdict(row) for row in rows],
    }


def table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(str(value).replace("|", "\\|") for value in row)
            + " |"
        )
    return "\n".join(lines)


def render_report(audit: dict[str, Any]) -> str:
    rows = audit["rows"]
    summary = audit["summary"]
    by_kind_mode = Counter((row["kind"], row["tools_mode"]) for row in rows)
    by_kind_status = Counter((row["kind"], row["status"]) for row in rows)
    summary_rows = [
        [
            kind,
            sum(row["kind"] == kind for row in rows),
            by_kind_mode[(kind, "inherit-all")]
            + by_kind_mode[(kind, "inherit-agent")],
            by_kind_mode[(kind, "allow-list")],
            by_kind_mode[(kind, "disabled")],
            by_kind_status[(kind, "current-static")],
            by_kind_status[(kind, "runtime-verification-required")],
            by_kind_status[(kind, "blocked")],
        ]
        for kind in ("agent", "prompt")
    ]
    runtime_rows = [
        [
            row["kind"],
            row["name"],
            row["path"],
            ", ".join(row["notes"]) or "—",
        ]
        for row in rows
        if row["status"] == "runtime-verification-required"
    ]
    runtime_table = (
        table(["Type", "Name", "Path", "Reason"], runtime_rows)
        if runtime_rows
        else "None."
    )
    return f"""# Primitive Capability Audit

Generated by `python3 harness/github-copilot/scripts/audit_primitive_capabilities.py`.

Verification date: **{audit["verificationDate"]}**

## Scope and permission boundary

This audit covers every canonical agent and VS Code prompt, including plugin-owned sources while excluding
generated mirrors. Frontmatter controls tool availability and agent/model selection. VS Code permission
levels and approvals are separate session or organization controls; they must not be expressed as
unsupported primitive frontmatter.

VS Code documents **Default Approvals**, **Assisted permissions**, **Bypass Approvals**, and **Autopilot**.
Fine-grained tool, URL, terminal-command, sandbox, and managed-policy controls can still change whether an
enabled tool runs.

## Summary

{table(
    [
        "Type",
        "Sources",
        "Inherited tools",
        "Allow-lists",
        "Tools disabled",
        "Current static",
        "Runtime check",
        "Blocked",
    ],
    summary_rows,
)}

- Fixed model pins: {summary["fixedModels"]}.
- Read-only agents inheriting all tools: {summary["readOnlyAgentsInheritingAll"]}.
- Blocking capability findings: {summary["blocked"]}.
- Full machine-readable ledger: `docs/PRIMITIVE-CAPABILITIES.json`.

## Runtime verification queue

Environment-specific MCP, extension, and tool-set entries are syntactically valid but require the named
server or extension in the target profile.

{runtime_table}

## Acceptance

Static capability policy passes only when:

1. No fixed model remains without a dated, explicit exception.
2. No Copilot CLI no-op token appears in a cross-surface agent.
3. No legacy VS Code prompt tool name remains.
4. Read-only agents do not silently inherit all tools.
5. Prompt agent references resolve to a built-in role or canonical custom-agent identifier.
6. Environment-specific tools stay in the runtime verification queue until exercised in that environment.

Static validation does not replace **Configure Tools**, **Chat: Run Prompt**, approval-policy review, or an
interactive test in the target VS Code profile.
"""


def stale_outputs(ledger: str, report: str) -> list[Path]:
    stale = []
    if not LEDGER_PATH.is_file() or LEDGER_PATH.read_text(encoding="utf-8") != ledger:
        stale.append(LEDGER_PATH)
    if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != report:
        stale.append(REPORT_PATH)
    return stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when reports are stale")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    audit = build_audit()
    ledger = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    report = render_report(audit)
    if args.json_output:
        print(ledger, end="")
        return 1 if audit["summary"]["blocked"] else 0
    if args.check:
        stale = stale_outputs(ledger, report)
        if stale:
            print(
                "Primitive capability audit is stale; run "
                "python3 harness/github-copilot/scripts/audit_primitive_capabilities.py",
                file=sys.stderr,
            )
            for path in stale:
                print(f"  - {relative(path)}", file=sys.stderr)
            return 1
        return 1 if audit["summary"]["blocked"] else 0

    LEDGER_PATH.write_text(ledger, encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(
        f"Audited {len(audit['rows'])} agent/prompt capability sources and wrote "
        f"{relative(REPORT_PATH)} plus {relative(LEDGER_PATH)}."
    )
    return 1 if audit["summary"]["blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

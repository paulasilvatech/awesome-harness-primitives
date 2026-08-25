#!/usr/bin/env python3
"""Dispatch the read-only commands supported by the IssueOps workflow."""

from __future__ import annotations

import html
import os
from dataclasses import dataclass
from pathlib import Path
import re
import shlex
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
AGENT_VALIDATOR = (
    REPO_ROOT
    / ".github"
    / "skills"
    / "validation-scripts"
    / "scripts"
    / "validate-agents.py"
)
SUPPORTED_COMMANDS = ("/check-agents", "/help")
UNSUPPORTED_COMMANDS = {
    "/onboard": "team onboarding requires an approved deployment workflow",
    "/validate": "deployment validation requires an authenticated cluster context",
}
COMMAND_NAME_RE = re.compile(r"^/[a-z][a-z0-9-]*$")
MAX_COMMENT_LENGTH = 65_536
MAX_COMMAND_LENGTH = 1_000
MAX_OUTPUT_LENGTH = 55_000

HELP_TEXT = """Supported IssueOps commands:

- /check-agents — run the repository agent validator in strict mode
- /help — show this help

Commands must begin the first line of an issue comment. Arguments are not
accepted. Only repository owners, members, and collaborators are authorized by
the workflow. /onboard and /validate are intentionally unsupported because this
workflow has no cloud credentials or cluster context."""


@dataclass(frozen=True)
class DispatchResult:
    """A command result suitable for both process status and issue output."""

    command_name: str
    exit_code: int
    summary: str
    output: str = ""


def parse_comment(comment_body: str) -> str | None:
    """Return a command from the first line, or None when it is not a command."""
    if len(comment_body) > MAX_COMMENT_LENGTH:
        raise ValueError("Comment exceeds the maximum supported length.")
    if not comment_body:
        return None

    first_line = comment_body.splitlines()[0].rstrip()
    if not first_line.startswith("/"):
        return None
    if len(first_line) > MAX_COMMAND_LENGTH:
        raise ValueError("Command exceeds the maximum supported length.")
    return first_line


def _split_command(command_line: str) -> tuple[str, list[str]]:
    try:
        parts = shlex.split(command_line, posix=True)
    except ValueError as error:
        raise ValueError(f"Unable to parse command: {error}") from error

    if not parts:
        raise ValueError("Command is empty.")
    command_name = parts[0]
    if not COMMAND_NAME_RE.fullmatch(command_name):
        raise ValueError(
            "Command names must start with '/' and contain only lowercase "
            "letters, digits, and hyphens."
        )
    return command_name, parts[1:]


def _process_exit_code(return_code: int) -> int:
    """Convert signal return codes to their conventional shell exit status."""
    if return_code < 0:
        return min(128 + abs(return_code), 255)
    return min(return_code, 255)


def execute_command(command_line: str) -> DispatchResult:
    """Execute an allow-listed command without invoking a shell."""
    try:
        command_name, arguments = _split_command(command_line)
    except ValueError as error:
        return DispatchResult("invalid", 2, str(error))

    if command_name in UNSUPPORTED_COMMANDS:
        return DispatchResult(
            command_name,
            2,
            f"Unsupported command: {UNSUPPORTED_COMMANDS[command_name]}.",
            HELP_TEXT,
        )
    if command_name not in SUPPORTED_COMMANDS:
        return DispatchResult(
            command_name,
            2,
            f"Unknown command: {command_name}.",
            HELP_TEXT,
        )
    if arguments:
        return DispatchResult(
            command_name,
            2,
            f"{command_name} does not accept arguments.",
            HELP_TEXT,
        )
    if command_name == "/help":
        return DispatchResult(command_name, 0, "IssueOps help.", HELP_TEXT)

    if not AGENT_VALIDATOR.is_file():
        return DispatchResult(
            command_name,
            2,
            "The repository agent validator is unavailable.",
        )

    try:
        completed = subprocess.run(
            [sys.executable, str(AGENT_VALIDATOR), "--strict"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return DispatchResult(
            command_name,
            124,
            "Agent validation timed out after 300 seconds.",
        )
    except OSError as error:
        return DispatchResult(
            command_name,
            126,
            f"Agent validation could not start: {error}.",
        )

    output = (completed.stdout + completed.stderr).strip()
    if len(output) > MAX_OUTPUT_LENGTH:
        output = f"{output[:MAX_OUTPUT_LENGTH]}\n[output truncated]"
    exit_code = _process_exit_code(completed.returncode)
    summary = (
        "Agent validation passed."
        if exit_code == 0
        else f"Agent validation failed with exit code {exit_code}."
    )
    return DispatchResult(command_name, exit_code, summary, output)


def format_result(result: DispatchResult) -> str:
    """Format a result as GitHub-flavored Markdown without rendering output."""
    safe_command = html.escape(result.command_name).replace("`", "&#96;")
    lines = [
        "## IssueOps command result",
        "",
        f"**Command:** `{safe_command}`",
        f"**Status:** {'PASS' if result.exit_code == 0 else 'FAIL'}",
        f"**Exit code:** `{result.exit_code}`",
        "",
        result.summary,
    ]
    if result.output:
        lines.extend(
            [
                "",
                "### Output",
                "",
                *(f"    {line}" for line in result.output.splitlines()),
            ]
        )
    return "\n".join(lines)


def main() -> int:
    """Read the issue comment from the environment and return command status."""
    if sys.argv[1:] in (["-h"], ["--help"]):
        print(HELP_TEXT)
        return 0
    if sys.argv[1:]:
        print("dispatcher.py accepts no arguments; use ISSUE_COMMENT.", file=sys.stderr)
        return 2

    comment_body = os.environ.get("ISSUE_COMMENT", "")
    try:
        command_line = parse_comment(comment_body)
    except ValueError as error:
        result = DispatchResult("invalid", 2, str(error), HELP_TEXT)
    else:
        if command_line is None:
            result = DispatchResult(
                "none",
                2,
                "The first line does not contain an IssueOps command.",
                HELP_TEXT,
            )
        else:
            result = execute_command(command_line)

    print(format_result(result))
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

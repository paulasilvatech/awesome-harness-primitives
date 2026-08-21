#!/usr/bin/env python3
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parent.parent
UNSAFE_ARGUMENT = re.compile(r"[;&|`<>]|\$\(")

COMMAND_MAP = {
    "/validate": {
        "script": SKILLS_ROOT / "validation-scripts/scripts/validate-deployment.sh",
        "description": "Validate deployment status",
        "allowed_flags": ["--environment", "--horizon"]
    },
    "/check-agents": {
        "script": SKILLS_ROOT / "validation-scripts/scripts/validate-agents.py",
        "description": "Validate agent definitions"
    }
}


def parse_comment(comment_body):
    """Parses the first line of an issue comment for slash commands."""
    lines = comment_body.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("/"):
            return line
    return None


def validate_arguments(command_name, config, args):
    """Validate dispatcher arguments before invoking a mapped script."""
    if any(UNSAFE_ARGUMENT.search(arg) for arg in args):
        return False, "Arguments contain unsupported shell metacharacters."

    allowed_flags = set(config.get("allowed_flags", []))
    if not allowed_flags and args:
        return False, f"`{command_name}` does not accept arguments."

    index = 0
    while index < len(args):
        flag, separator, inline_value = args[index].partition("=")
        if flag not in allowed_flags:
            return False, f"Unsupported flag for `{command_name}`: {flag}"
        if separator:
            if not inline_value:
                return False, f"Missing value for `{flag}`."
            index += 1
            continue
        if index + 1 >= len(args) or args[index + 1].startswith("--"):
            return False, f"Missing value for `{flag}`."
        index += 2
    return True, ""


def execute_command(full_command):
    """Executes the mapped script for the given command."""
    try:
        parts = shlex.split(full_command)
        command_name = parts[0]
        args = parts[1:]
    except (ValueError, IndexError) as exc:
        return False, f"Error parsing command: {exc}"

    if command_name not in COMMAND_MAP:
        return False, f"Unknown command: `{command_name}`. Available commands: {', '.join(COMMAND_MAP.keys())}"

    config = COMMAND_MAP[command_name]
    script_path = config["script"]
    valid, message = validate_arguments(command_name, config, args)
    if not valid:
        return False, message

    if not script_path.is_file():
        return False, f"Internal Error: Script not found at {script_path}"

    launcher = [sys.executable] if script_path.suffix == ".py" else []
    cmd = [*launcher, str(script_path), *args]
    print(f"[RUN] Executing: {shlex.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except OSError as exc:
        return False, f"Execution failed: {exc}"
    return result.returncode == 0, result.stdout


def main():
    comment_body = os.environ.get("ISSUE_BODY", "")
    if not comment_body:
        print("No issue body found.")
        sys.exit(0)

    command_line = parse_comment(comment_body)
    if not command_line:
        print("No slash command found.")
        sys.exit(0)

    print(f"Processing command: {command_line}")
    success, output = execute_command(command_line)

    status_icon = "[OK]" if success else "[FAIL]"

    print("EOF_OUTPUT<<EOF")
    print(f"## {status_icon} Command Execution Result")
    print(f"**Command:** `{command_line}`")
    print("")
    print("```bash")
    print(output)
    print("```")
    print("EOF")

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import sys
import re
import shlex
import subprocess

# ==============================================================================
# CONFIGURATION: Command to Script Mapping
# ==============================================================================
COMMAND_MAP = {
    "/onboard": {
        "script": ".github/skills/backstage-deployment/scripts/onboard-team.sh",
        "description": "Onboard a new team",
        "required_args": ["team_name"]
    },
    "/validate": {
        "script": ".github/skills/validation-scripts/scripts/validate-deployment.sh",
        "description": "Validate deployment status",
        "allowed_flags": ["--environment", "--horizon"]
    },
    "/check-agents": {
        "script": ".github/skills/validation-scripts/scripts/validate-agents.py",
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

def execute_command(full_command):
    """Executes the mapped script for the given command."""
    try:
        parts = shlex.split(full_command)
        command_name = parts[0]
        args = parts[1:]
    except Exception as e:
        return False, f"Error parsing command: {e}"

    if command_name not in COMMAND_MAP:
        return False, f"Unknown command: `{command_name}`. Available commands: {', '.join(COMMAND_MAP.keys())}"

    config = COMMAND_MAP[command_name]
    script_path = config["script"]

    # Security Check: Ensure script exists and is executable
    if not os.path.isfile(script_path):
        return False, f"Internal Error: Script not found at {script_path}"
    
    # Construct Execution Command
    # We pass arguments exactly as they were parsed
    cmd = [script_path] + args
    
    print(f"[RUN] Executing: {' '.join(cmd)}")
    
    try:
        # Run the script and capture output
        result = subprocess.run(
            cmd, 
            check=False, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        
        success = result.returncode == 0
        output = result.stdout
        
        return success, output

    except Exception as e:
        return False, f"Execution failed: {str(e)}"

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

    # Format Output for GitHub Comment
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

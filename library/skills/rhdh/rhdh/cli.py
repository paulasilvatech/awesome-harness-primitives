"""CLI for rhdh (RHDH plugin development orchestrator).

Follows agentic CLI patterns:
- Auto-detects output format: JSON when piped or agent-consumed, human when TTY
- No-arg default shows orientation (status + needs_setup flag)
- Dry-run by default, --force for destructive actions
- Non-interactive (all input via flags)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

from . import __version__
from .config import (
    SUBMODULE_REPOS,
    get_data_dir,
    get_github_username,
    get_local_setup_dir,
    get_repo,
    list_submodule_repos,
    save_github_username,
    setup_submodule,
)
from .formatters import OutputFormatter
from .todo import (
    add_note as todo_add_note,
)
from .todo import (
    add_todo,
    get_todo_file_path,
    list_todos,
    mark_done,
)
from .todo import (
    show_raw as todo_show_raw,
)
from .worklog import (
    add_entry as worklog_add_entry,
)
from .worklog import (
    format_entry_human,
    read_entries,
    search_entries,
)
from .workspace import get_workspace, list_workspaces

# =============================================================================
# Helper Functions
# =============================================================================


def run_command(cmd: list[str], cwd: Optional[Path] = None) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"


def check_tool(name: str) -> bool:
    """Check if a tool is available in PATH."""
    return shutil.which(name) is not None


def get_git_branch(repo_path: Path) -> str:
    """Get current git branch for a repo."""
    rc, stdout, _ = run_command(["git", "branch", "--show-current"], cwd=repo_path)
    return stdout.strip() if rc == 0 else "unknown"


def has_uncommitted_changes(repo_path: Path) -> bool:
    """Check if repo has uncommitted changes."""
    rc, stdout, _ = run_command(["git", "status", "--porcelain"], cwd=repo_path)
    return rc == 0 and bool(stdout.strip())


# =============================================================================
# Status/Orientation Command
# =============================================================================


def cmd_status(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """Show environment status (orientation).

    Returns structured data with needs_setup flag for agentic use.
    """
    fmt.header("RHDH Plugin Environment")

    checks: list[dict[str, Any]] = []
    next_steps: list[str] = []
    needs_setup = False

    # Check all configured repos
    for info in SUBMODULE_REPOS.values():
        config_key = info["config_key"]
        required = info["required"]
        repo_path = get_repo(config_key)

        if repo_path:
            branch = get_git_branch(repo_path)
            status = "uncommitted" if has_uncommitted_changes(repo_path) else "clean"
            checks.append(
                {
                    "name": config_key,
                    "status": "pass",
                    "message": f"{repo_path} ({branch}, {status})",
                    "path": str(repo_path),
                    "branch": branch,
                    "clean": status == "clean",
                }
            )
            fmt.log_ok(f"{config_key}: {repo_path} ({branch}, {status})")
        elif required:
            checks.append(
                {
                    "name": config_key,
                    "status": "fail",
                    "message": "not found",
                }
            )
            fmt.log_fail(f"{config_key}: not found")
            needs_setup = True
        else:
            checks.append(
                {
                    "name": config_key,
                    "status": "info",
                    "message": "not configured (optional)",
                }
            )
            fmt.log_info(f"{config_key}: not configured (optional)")

    # Check tools
    fmt.header("Tools")

    if check_tool("gh"):
        rc, _, _ = run_command(["gh", "auth", "status"])
        if rc == 0:
            checks.append({"name": "gh_cli", "status": "pass", "message": "authenticated"})
            fmt.log_ok("gh CLI: authenticated")
        else:
            checks.append({"name": "gh_cli", "status": "warn", "message": "not authenticated"})
            fmt.log_warn("gh CLI: installed but not authenticated")
            next_steps.append("gh auth login")
    else:
        checks.append({"name": "gh_cli", "status": "fail", "message": "not installed"})
        fmt.log_fail("gh CLI: not installed")
        next_steps.append("Install gh CLI: https://cli.github.com/")

    if check_tool("podman"):
        rc, stdout, _ = run_command(["podman", "--version"])
        version = stdout.strip() if rc == 0 else "unknown"
        checks.append({"name": "podman", "status": "pass", "message": version})
        fmt.log_ok(f"podman: {version}")
    elif check_tool("docker"):
        rc, stdout, _ = run_command(["docker", "--version"])
        version = stdout.strip() if rc == 0 else "unknown"
        checks.append({"name": "docker", "status": "pass", "message": version})
        fmt.log_ok(f"docker: {version}")
    else:
        checks.append({"name": "container_runtime", "status": "warn", "message": "not found"})
        fmt.log_warn("container runtime: not found (needed for rhdh-local)")

    if check_tool("jq"):
        checks.append({"name": "jq", "status": "pass", "message": "installed"})
        fmt.log_ok("jq: installed")
    else:
        checks.append({"name": "jq", "status": "warn", "message": "not installed"})
        fmt.log_warn("jq: not installed (recommended)")

    if check_tool("jira"):
        rc, _, _ = run_command(["jira", "me"])
        if rc == 0:
            checks.append({"name": "jira", "status": "pass", "message": "authenticated"})
            fmt.log_ok("jira: authenticated")
        else:
            checks.append(
                {
                    "name": "jira",
                    "status": "warn",
                    "message": "not authenticated",
                    "reference": "references/jira-reference.md",
                }
            )
            fmt.log_warn("jira: not authenticated (see references/jira-reference.md)")
    else:
        checks.append(
            {
                "name": "jira",
                "status": "info",
                "message": "not installed (optional)",
                "reference": "references/jira-reference.md",
            }
        )
        fmt.log_info("jira: not installed (optional)")

    # Build output based on state
    data: dict[str, Any] = {
        "needs_setup": needs_setup,
        "checks": checks,
    }

    if needs_setup:
        # Just point to doctor - it has all the setup guidance
        next_steps.append("rhdh doctor")
        fmt.render_banner("Configuration needed. Run:", call_to_action="rhdh doctor")
    else:
        next_steps.extend(
            [
                "rhdh workspace list",
                "rhdh doctor",
            ]
        )

    fmt.success(data, next_steps=next_steps)
    return 0


# =============================================================================
# Doctor Command
# =============================================================================


def cmd_doctor(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """Run full environment check."""
    fmt.header("Environment Check")

    checks: list[dict[str, Any]] = []
    issues: list[str] = []

    # Check all repos
    for info in SUBMODULE_REPOS.values():
        config_key = info["config_key"]
        required = info["required"]
        repo_path = get_repo(config_key)

        if repo_path:
            checks.append({"name": config_key, "status": "pass", "message": str(repo_path)})
            fmt.log_ok(f"{config_key} found: {repo_path}")

            # Check it's a git repo
            rc, _, _ = run_command(["git", "rev-parse", "--git-dir"], cwd=repo_path)
            if rc == 0:
                checks.append({"name": f"{config_key}_git", "status": "pass", "message": "valid"})
                fmt.log_ok("  Git repository valid")
            else:
                checks.append({"name": f"{config_key}_git", "status": "fail", "message": "invalid"})
                fmt.log_fail("  Not a valid git repository")
                issues.append(f"{config_key} is not a git repository")
        elif required:
            checks.append({"name": config_key, "status": "fail", "message": "not found"})
            fmt.log_fail(f"{config_key} not found")
            issues.append(f"Configure {config_key}: rhdh config set {config_key} /path/to/repo")
        else:
            checks.append(
                {"name": config_key, "status": "info", "message": "not configured (optional)"}
            )
            fmt.log_info(f"{config_key}: not configured (optional)")

    fmt.header("GitHub CLI")

    if check_tool("gh"):
        checks.append({"name": "gh_installed", "status": "pass", "message": "installed"})
        fmt.log_ok("gh CLI installed")

        rc, _, _ = run_command(["gh", "auth", "status"])
        if rc == 0:
            checks.append({"name": "gh_auth", "status": "pass", "message": "authenticated"})
            fmt.log_ok("  Authenticated")

            # Check repo access
            rc, _, _ = run_command(
                ["gh", "api", "repos/redhat-developer/rhdh-plugin-export-overlays", "--silent"]
            )
            if rc == 0:
                checks.append(
                    {"name": "gh_access", "status": "pass", "message": "can access overlay repo"}
                )
                fmt.log_ok("  Can access overlay repo")
            else:
                checks.append(
                    {"name": "gh_access", "status": "warn", "message": "cannot access overlay repo"}
                )
                fmt.log_warn("  Cannot access overlay repo (may need permissions)")
        else:
            checks.append({"name": "gh_auth", "status": "fail", "message": "not authenticated"})
            fmt.log_fail("  Not authenticated")
            issues.append("Run: gh auth login")
    else:
        checks.append({"name": "gh_installed", "status": "fail", "message": "not installed"})
        fmt.log_fail("gh CLI not installed")
        issues.append("Install gh CLI: https://cli.github.com/")

    fmt.header("Container Runtime")

    if check_tool("podman"):
        checks.append({"name": "podman", "status": "pass", "message": "installed"})
        fmt.log_ok("podman installed")

        rc, _, _ = run_command(["podman", "ps"])
        if rc == 0:
            checks.append({"name": "podman_running", "status": "pass", "message": "running"})
            fmt.log_ok("  Podman running")
        else:
            checks.append({"name": "podman_running", "status": "warn", "message": "not running"})
            fmt.log_warn("  Podman not running or not accessible")
    elif check_tool("docker"):
        checks.append({"name": "docker", "status": "pass", "message": "installed"})
        fmt.log_ok("docker installed")
    else:
        checks.append({"name": "container_runtime", "status": "fail", "message": "not found"})
        fmt.log_fail("No container runtime found")
        issues.append("Install podman or docker for local testing")

    # JIRA CLI (optional)
    fmt.header("JIRA CLI")

    if check_tool("jira"):
        checks.append({"name": "jira_installed", "status": "pass", "message": "installed"})
        fmt.log_ok("jira CLI installed")

        rc, _, _ = run_command(["jira", "me"])
        if rc == 0:
            checks.append({"name": "jira_auth", "status": "pass", "message": "authenticated"})
            fmt.log_ok("  Authenticated")
        else:
            checks.append(
                {
                    "name": "jira_auth",
                    "status": "warn",
                    "message": "not authenticated",
                    "reference": "references/jira-reference.md",
                }
            )
            fmt.log_warn("  Not authenticated (see references/jira-reference.md)")
    else:
        checks.append(
            {
                "name": "jira_installed",
                "status": "info",
                "message": "not installed (optional)",
                "reference": "references/jira-reference.md",
            }
        )
        fmt.log_info("jira: not installed (optional, see references/jira-reference.md)")

    # Local Setup (rhdh-local-setup customization system)
    fmt.header("Local Setup (rhdh-local-setup)")

    local_setup = get_local_setup_dir()
    if local_setup:
        checks.append({"name": "local_setup", "status": "pass", "message": str(local_setup)})
        fmt.log_ok(f"rhdh-local-setup found: {local_setup}")

        # Check rhdh-local is present inside it
        local_dir = local_setup / "rhdh-local"
        if local_dir.is_dir():
            checks.append(
                {"name": "local_setup_rhdh_local", "status": "pass", "message": str(local_dir)}
            )
            fmt.log_ok("  rhdh-local: found")
        else:
            checks.append(
                {"name": "local_setup_rhdh_local", "status": "warn", "message": "not found"}
            )
            fmt.log_warn(f"  rhdh-local not found inside {local_setup}")

        # Check customizations dir
        customizations_dir = local_setup / "rhdh-customizations"
        if customizations_dir.is_dir():
            checks.append(
                {"name": "customizations_dir", "status": "pass", "message": str(customizations_dir)}
            )
            fmt.log_ok("  rhdh-customizations: found")
        else:
            checks.append({"name": "customizations_dir", "status": "warn", "message": "not found"})
            fmt.log_warn(f"  rhdh-customizations not found inside {local_setup}")

        # Check if customizations are synced (only meaningful when rhdh-local exists)
        if local_dir.is_dir():
            override_yaml = (
                local_dir / "configs" / "dynamic-plugins" / "dynamic-plugins.override.yaml"
            )
            if override_yaml.exists():
                checks.append(
                    {"name": "customizations_synced", "status": "pass", "message": "synced"}
                )
                fmt.log_ok("  customizations: synced to rhdh-local")
            else:
                checks.append(
                    {"name": "customizations_synced", "status": "info", "message": "not synced"}
                )
                fmt.log_info("  customizations: not synced (run rhdh local apply)")

        # Check if RHDH is running on port 7007
        import socket

        rhdh_running = False
        try:
            with socket.create_connection(("localhost", 7007), timeout=1):
                rhdh_running = True
        except OSError:
            pass

        if rhdh_running:
            checks.append({"name": "rhdh_port_7007", "status": "pass", "message": "running"})
            fmt.log_ok("  RHDH: running on http://localhost:7007")
        else:
            checks.append({"name": "rhdh_port_7007", "status": "info", "message": "not running"})
            fmt.log_info("  RHDH: not running (start with rhdh local up --customized)")
    else:
        checks.append(
            {"name": "local_setup", "status": "info", "message": "not configured (optional)"}
        )
        fmt.log_info("rhdh-local-setup: not configured (optional for local testing)")
        fmt.log_info("  Configure with: rhdh config set local_setup /path/to/rhdh-local-setup")
        fmt.log_info("  Or set env: RHDH_LOCAL_SETUP_DIR=/path/to/rhdh-local-setup")

    # Data Storage
    fmt.header("Data Storage")
    data_dir = get_data_dir()
    checks.append({"name": "data_dir", "status": "info", "message": str(data_dir)})
    fmt.log_info(f"Data directory: {data_dir}")
    fmt.log_info("  (worklog.jsonl, TODO.md)")
    fmt.log_info("  Override with RHDH_SKILL_DATA_DIR env var")

    # Summary
    fmt.header("Summary")

    all_passed = len(issues) == 0
    next_steps = []

    needs_setup = not all_passed

    if all_passed:
        fmt.log_ok("All checks passed!")
        next_steps = ["rhdh workspace list", "/onboard-plugin"]
        data: dict[str, Any] = {
            "needs_setup": needs_setup,
            "all_passed": all_passed,
            "checks": checks,
            "issues": issues,
        }
    else:
        fmt.log_warn(f"{len(issues)} issue(s) found")
        next_steps = ["Read workflows/doctor.md for setup instructions"]
        data = {
            "needs_setup": needs_setup,
            "all_passed": all_passed,
            "checks": checks,
            "issues": issues,
            "workflow": "workflows/doctor.md",
            "agent_instruction": "Read the workflow file for detailed setup steps",
        }

    fmt.success(data, next_steps=next_steps)
    return 0 if all_passed else 1


# =============================================================================
# Local Commands - thin delegation to rhdh_local.cli
# =============================================================================

from rhdh_local.cli import (  # noqa: E402
    cmd_local_apply,
    cmd_local_backup,
    cmd_local_backup_list,
    cmd_local_down,
    cmd_local_health,
    cmd_local_plugins_list,
    cmd_local_remove,
    cmd_local_restore,
    cmd_local_status,
    cmd_local_up,
)

# =============================================================================
# Config Commands
# =============================================================================


def cmd_config_init(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Initialize configuration file."""
    from .config import run_config

    force = getattr(args, "force", False)
    global_ = getattr(args, "global_", False)
    scope = "user" if global_ else "project"

    fmt.header(f"Initializing {scope.title()} Configuration")

    success, data, next_steps = run_config("init", force=force, global_=global_)

    if success and isinstance(data, dict):
        fmt.log_ok(f"Created: {data.get('created', '')}")
        config = data.get("config", {})
        repos = config.get("repos", {})
        for info in SUBMODULE_REPOS.values():
            key = info["config_key"]
            if repos.get(key):
                fmt.log_ok(f"Auto-detected {key}: {repos[key]}")
            elif info["required"]:
                fmt.log_info(f"{key}: not found (configure with: rhdh config set {key} /path)")
        fmt.success(data, next_steps=next_steps)
        return 0
    else:
        fmt.error("CONFIG_INIT_FAILED", str(data), next_steps=next_steps)
        return 1


def cmd_config_show(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Show current configuration."""
    from .config import run_config

    global_ = getattr(args, "global_", False)

    fmt.header("Configuration")

    success, data, next_steps = run_config("show", global_=global_)

    if success and isinstance(data, dict):
        # Human-readable output
        fmt.log_info(f"User config: {data.get('user_config_path', '')}")
        fmt.log_info(f"Project config: {data.get('project_config_path', '')}")

        fmt.header("Resolved Paths")
        resolved = data.get("resolved", {})
        for info in SUBMODULE_REPOS.values():
            key = info["config_key"]
            if resolved.get(key):
                fmt.log_ok(f"{key}: {resolved[key]}")
            elif info["required"]:
                fmt.log_fail(f"{key}: not found")
            else:
                fmt.log_info(f"{key}: not configured")

        fmt.success(data, next_steps=next_steps)
        return 0
    else:
        fmt.error("CONFIG_SHOW_FAILED", str(data), next_steps=next_steps)
        return 1


def cmd_config_keys(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """List all config keys."""
    from .config import run_config

    global_ = getattr(args, "global_", False)

    success, data, next_steps = run_config("keys", global_=global_)

    if success and isinstance(data, dict):
        keys = data.get("keys", [])
        scope = data.get("scope", "merged")
        fmt.header(f"Config Keys ({scope})")
        for key in keys:
            fmt.log_info(key)
        fmt.success(data, next_steps=next_steps)
        return 0
    else:
        fmt.error("CONFIG_KEYS_FAILED", str(data), next_steps=next_steps)
        return 1


def cmd_config_get(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Get a config value."""
    from .config import run_config

    key = getattr(args, "key", None)

    success, data, next_steps = run_config("get", key=key)

    if success and isinstance(data, dict):
        fmt.log_ok(f"{data.get('key')}: {data.get('value')}")
        fmt.success(data, next_steps=next_steps)
        return 0
    else:
        fmt.error("CONFIG_GET_FAILED", str(data), next_steps=next_steps)
        return 1


def cmd_config_set(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Set a config value."""
    from .config import run_config

    key = getattr(args, "key", None)
    value = getattr(args, "value", None)
    global_ = getattr(args, "global_", False)

    success, data, next_steps = run_config("set", key=key, value=value, global_=global_)

    if success and isinstance(data, dict):
        scope = data.get("scope", "project")
        fmt.log_ok(f"Set {data.get('key')} = {data.get('value')} ({scope} config)")
        fmt.success(data, next_steps=next_steps)
        return 0
    else:
        fmt.error("CONFIG_SET_FAILED", str(data), next_steps=next_steps)
        return 1


# =============================================================================
# Setup Commands
# =============================================================================


def cmd_setup_submodule_list(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """List available repositories for submodule setup."""
    fmt.header("Available Repositories")

    repos = list_submodule_repos()
    github_username = get_github_username()

    # Check if any repos need username
    needs_username = any(r.get("needs_username") for r in repos)

    from .formatters import BLUE, GREEN, NC, RED, YELLOW

    # Show GitHub username status
    if github_username:
        fmt.log_info(f"GitHub user: {BLUE}{github_username}{NC}")
    elif needs_username:
        fmt.log_warn("GitHub user: not detected (needed for fork repos)")
        fmt.log_info("Run: gh auth login")

    def format_repo(repo: dict) -> str:
        status = repo["status"]
        required = " (required)" if repo["required"] else " (optional)"

        if status == "submodule":
            color = GREEN
            status_text = "✓ submodule"
        elif status == "configured":
            color = GREEN
            status_text = "✓ configured"
        elif status == "directory_exists":
            color = YELLOW
            status_text = "⚠ directory exists"
        else:
            color = RED if repo["required"] else YELLOW
            status_text = "✗ not configured"

        lines = [f"{color}{repo['name']:<35}{NC} {status_text}{required}"]
        lines.append(f"    {repo['description']}")
        if repo["path"]:
            lines.append(f"    Path: {repo['path']}")
        if repo.get("has_fork"):
            if repo.get("origin"):
                lines.append(f"    Fork: {repo['origin']}")
            else:
                lines.append(f"    {YELLOW}Fork: requires GitHub username{NC}")
        return "\n".join(lines)

    fmt.render_list(repos, format_repo)

    data = {
        "github_username": github_username,
        "repos": repos,
    }

    # Determine next steps based on status
    unconfigured_required = [r for r in repos if r["status"] == "not_configured" and r["required"]]
    if needs_username and not github_username:
        next_steps = [
            "gh auth login",
            "rhdh config set github.username <your-username>",
        ]
    elif unconfigured_required:
        next_steps = [
            "rhdh setup submodule add --all",
            f"rhdh setup submodule add {unconfigured_required[0]['name']}",
        ]
    else:
        next_steps = ["rhdh", "rhdh workspace list"]

    fmt.success(data, next_steps=next_steps)
    return 0


def cmd_setup_submodule_add(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Add repository as submodule."""
    add_all = getattr(args, "all", False)
    name = getattr(args, "name", None)
    dry_run = getattr(args, "dry_run", False)

    # Detect GitHub username (needed for repos with forks)
    github_username = get_github_username()
    if github_username:
        fmt.log_info(f"GitHub user: {github_username}")
        # Save to config if not already saved
        save_github_username(github_username)

    if add_all:
        # Add all required repos
        fmt.header("Setting up all required repositories")

        results = []
        all_success = True

        for repo_name, repo_info in SUBMODULE_REPOS.items():
            if not repo_info["required"]:
                continue

            fmt.log_info(f"Setting up: {repo_name}")
            success, data, _ = setup_submodule(
                repo_name, dry_run=dry_run, github_username=github_username
            )

            if success:
                if isinstance(data, dict):
                    status = data.get("status", "unknown")
                    if status == "already_configured":
                        fmt.log_ok("  Already configured")
                    elif dry_run:
                        fmt.log_info("  Would create submodule")
                    else:
                        fmt.log_ok(f"  Created at: {data.get('path')}")
            else:
                fmt.log_fail(f"  Failed: {data}")
                all_success = False

            results.append({"name": repo_name, "success": success, "data": data})

        output_data: dict[str, Any] = {
            "github_username": github_username,
            "results": results,
            "all_success": all_success,
        }

        if all_success:
            fmt.success(output_data, next_steps=["rhdh", "rhdh doctor"])
            return 0
        else:
            fmt.success(output_data, next_steps=["rhdh setup submodule list"])
            return 1

    elif name:
        # Add single repo
        fmt.header(f"Setting up: {name}")

        success, data, next_steps = setup_submodule(
            name, dry_run=dry_run, github_username=github_username
        )

        if success:
            if isinstance(data, dict):
                status = data.get("status", "unknown")
                if status == "already_configured":
                    fmt.log_ok("Already configured as submodule")
                elif dry_run:
                    for action in data.get("actions", []):
                        fmt.log_info(action)
                else:
                    fmt.log_ok(f"Created at: {data.get('path')}")
                    if data.get("upstream"):
                        fmt.log_ok(f"Upstream: {data.get('upstream')}")
            fmt.success(data, next_steps=next_steps)
            return 0
        else:
            fmt.error("SUBMODULE_SETUP_FAILED", str(data), next_steps=next_steps)
            return 1

    else:
        fmt.error(
            "MISSING_ARGUMENT",
            "Specify repository name or use --all",
            next_steps=[
                "rhdh setup submodule list",
                "rhdh setup submodule add --all",
            ],
        )
        return 1


# =============================================================================
# Workspace Commands
# =============================================================================


def cmd_workspace_list(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """List plugin workspaces."""
    overlay_repo, workspaces = list_workspaces()

    if overlay_repo is None:
        fmt.error(
            "OVERLAY_NOT_FOUND",
            "Overlay repo not found",
            next_steps=["rhdh config init", "rhdh doctor"],
        )
        return 1

    fmt.header("Plugin Workspaces")
    fmt.log_info(f"Location: {overlay_repo}/workspaces/")

    items = []
    for ws in workspaces:
        items.append(
            {
                "name": ws.name,
                "detail": ws.repo_ref or "(no source.json)",
                "repo": ws.repo,
                "repo_ref": ws.repo_ref,
            }
        )

    # Render items in human mode
    from .formatters import BLUE, NC

    fmt.render_list(
        items,
        lambda i: f"{BLUE}{i['name']:<30}{NC} {i['detail']}",
        summary=f"Total: {len(items)} workspaces",
    )

    data = {
        "overlay_repo": str(overlay_repo),
        "count": len(workspaces),
        "items": items,
    }

    fmt.success(data, next_steps=["rhdh workspace status <name>", "/onboard-plugin"])
    return 0


def cmd_workspace_status(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Show workspace details."""
    found, ws, error = get_workspace(args.name)

    if not found:
        fmt.error(
            "WORKSPACE_NOT_FOUND",
            error,
            next_steps=["rhdh workspace list"],
        )
        return 1

    assert ws is not None  # Type narrowing

    fmt.header(f"Workspace: {ws.name}")

    # Files check
    files = []
    files.append({"name": "source.json", "exists": ws.has_source_json, "required": True})
    files.append({"name": "plugins-list.yaml", "exists": ws.has_plugins_list, "required": True})
    files.append({"name": "backstage.json", "exists": ws.has_backstage_json, "required": False})

    for f in files:
        if f["exists"]:
            fmt.log_ok(f["name"])
        elif f["required"]:
            fmt.log_fail(f"{f['name']} (required)")
        else:
            fmt.log_info(f"{f['name']} (optional)")

    data = {
        "name": ws.name,
        "path": str(ws.path),
        "files": files,
        "source": {
            "repo": ws.repo,
            "repo_ref": ws.repo_ref,
            "backstage_version": ws.repo_backstage_version,
        }
        if ws.has_source_json
        else None,
        "metadata_files": ws.metadata_files,
    }

    fmt.success(data, next_steps=[f"cd {ws.path}", "rhdh workspace list"])
    return 0


# =============================================================================
# Worklog Commands
# =============================================================================


def cmd_log_add(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Add a worklog entry."""
    message = args.message
    tags = args.tag if args.tag else None

    entry = worklog_add_entry(message, tags)

    fmt.log_ok(f"Added: {format_entry_human(entry)}")
    fmt.success(
        {"entry": entry},
        next_steps=["rhdh log show", "rhdh log search <query>"],
    )
    return 0


def cmd_log_show(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Show recent worklog entries."""
    limit = args.limit
    since = args.since

    entries = read_entries(limit=limit, since=since)

    if not entries:
        fmt.log_info("No entries found")
        fmt.success(
            {"count": 0, "entries": []},
            next_steps=["rhdh log add <message>"],
        )
        return 0

    fmt.header("Worklog")

    fmt.render_list(
        entries,
        lambda e: format_entry_human(e),
        summary=f"Showing {len(entries)} entries",
    )

    fmt.success(
        {"count": len(entries), "entries": entries},
        next_steps=["rhdh log add <message>", "rhdh log search <query>"],
    )
    return 0


def cmd_log_search(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Search worklog entries."""
    query = args.query
    limit = args.limit

    matches = search_entries(query, limit=limit)

    if not matches:
        fmt.log_info(f"No entries matching '{query}'")
        fmt.success(
            {"query": query, "count": 0, "entries": []},
            next_steps=["rhdh log show", "rhdh log add <message>"],
        )
        return 0

    fmt.header(f"Search: {query}")

    fmt.render_list(
        matches,
        lambda e: format_entry_human(e),
        summary=f"Found {len(matches)} matches",
    )

    fmt.success(
        {"query": query, "count": len(matches), "entries": matches},
        next_steps=["rhdh log show", "rhdh log add <message>"],
    )
    return 0


# =============================================================================
# Todo Commands
# =============================================================================


def cmd_todo_add(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Add a new todo item."""
    title = args.title
    context = args.context

    todo = add_todo(title, context)

    fmt.log_ok(f"Added: {todo.title}")
    fmt.log_info(f"Slug: {todo.slug}")
    fmt.success(
        {
            "slug": todo.slug,
            "title": todo.title,
            "created": todo.created,
            "context": todo.context,
        },
        next_steps=["rhdh todo list", f"rhdh todo note {todo.slug} <text>"],
    )
    return 0


def cmd_todo_list(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """List todo items."""
    include_done = not args.pending

    todos = list_todos(include_done=include_done)

    if not todos:
        fmt.log_info("No todos found")
        fmt.success(
            {"count": 0, "items": []},
            next_steps=["rhdh todo add <title>"],
        )
        return 0

    fmt.header("Todos")

    from .formatters import GREEN, NC, YELLOW

    items = []
    for todo in todos:
        items.append(
            {
                "slug": todo.slug,
                "title": todo.title,
                "done": todo.done,
                "created": todo.created,
                "context": todo.context,
            }
        )

    def format_todo(item: dict) -> str:
        status = "[x]" if item["done"] else "[ ]"
        color = GREEN if item["done"] else YELLOW
        context_str = f" ({item['context']})" if item["context"] else ""
        return f"{color}{status}{NC} {item['title']}{context_str}\n      slug: {item['slug']}"

    pending = sum(1 for t in todos if not t.done)
    done = sum(1 for t in todos if t.done)
    fmt.render_list(items, format_todo, summary=f"{pending} pending, {done} done")

    fmt.success(
        {"count": len(todos), "items": items},
        next_steps=["rhdh todo add <title>", "rhdh todo done <slug>"],
    )
    return 0


def cmd_todo_done(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Mark a todo as done."""
    slug = args.slug

    todo = mark_done(slug)

    if not todo:
        fmt.error(
            "TODO_NOT_FOUND",
            f"No todo matching '{slug}'",
            next_steps=["rhdh todo list"],
        )
        return 1

    if todo.completed:
        fmt.log_ok(f"Marked done: {todo.title}")
    else:
        fmt.log_info(f"Already done: {todo.title}")

    fmt.success(
        {"slug": todo.slug, "title": todo.title, "completed": todo.completed},
        next_steps=["rhdh todo list"],
    )
    return 0


def cmd_todo_note(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Add a note to a todo."""
    slug = args.slug
    note = args.note

    todo = todo_add_note(slug, note)

    if not todo:
        fmt.error(
            "TODO_NOT_FOUND",
            f"No todo matching '{slug}'",
            next_steps=["rhdh todo list"],
        )
        return 1

    fmt.log_ok(f"Added note to: {todo.title}")
    fmt.success(
        {"slug": todo.slug, "title": todo.title, "note": note},
        next_steps=["rhdh todo show", "rhdh todo list"],
    )
    return 0


def cmd_todo_show(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """Show the raw TODO.md file."""
    content = todo_show_raw()
    file_path = get_todo_file_path()

    fmt.render_raw(content)

    # In JSON mode, also output structured data
    if not fmt.is_human:
        fmt.success(
            {"file": str(file_path), "content": content},
            next_steps=["rhdh todo list", "rhdh todo add <title>"],
        )

    return 0


# =============================================================================
# CLI Setup
# =============================================================================


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="rhdh",
        description="CLI helper for RHDH plugin management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
OUTPUT FORMAT:
    Auto-detected: JSON when piped or agent-consumed, human-readable in terminal.
    Override with --json or --human flags.

ENVIRONMENT VARIABLES:
    RHDH_OVERLAY_REPO   Path to rhdh-plugin-export-overlays
    RHDH_LOCAL_REPO     Path to rhdh-local
    RHDH_FACTORY_REPO   Path to rhdh-dynamic-plugin-factory

EXAMPLES:
    rhdh                           # Show status (orientation)
    rhdh doctor                    # Check setup
    rhdh config init               # Create config
    rhdh workspace list            # List workspaces
    rhdh --json workspace list     # Force JSON output

    # Worklog
    rhdh log add "Started onboarding aws-appsync" --tag onboard
    rhdh log show --limit 10
    rhdh log search "aws"

    # Todos
    rhdh todo add "Check license with legal" --context aws-appsync
    rhdh todo list
    rhdh todo done check-license
    rhdh todo note check-license "Sent email to legal@"
    rhdh todo show
""",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # Output format flags
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument(
        "--json",
        action="store_true",
        help="Force JSON output (default when piped)",
    )
    format_group.add_argument(
        "--human",
        action="store_true",
        help="Force human-readable output (default in terminal)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include debug information",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # Status (also default when no command)
    status_parser = subparsers.add_parser("status", help="Show environment status")
    status_parser.set_defaults(func=cmd_status)

    # Doctor
    doctor_parser = subparsers.add_parser("doctor", help="Full environment check")
    doctor_parser.set_defaults(func=cmd_doctor)

    # Config
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(dest="config_command", metavar="SUBCOMMAND")

    # config init
    config_init_parser = config_subparsers.add_parser("init", help="Initialize configuration file")
    config_init_parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing config"
    )
    config_init_parser.add_argument(
        "--global",
        "-g",
        dest="global_",
        action="store_true",
        help="Initialize user config instead of project",
    )
    config_init_parser.set_defaults(func=cmd_config_init)

    # config show
    config_show_parser = config_subparsers.add_parser("show", help="Show current configuration")
    config_show_parser.add_argument(
        "--global", "-g", dest="global_", action="store_true", help="Show only user config"
    )
    config_show_parser.set_defaults(func=cmd_config_show)

    # config keys
    config_keys_parser = config_subparsers.add_parser("keys", help="List all config keys")
    config_keys_parser.add_argument(
        "--global", "-g", dest="global_", action="store_true", help="Show only user config keys"
    )
    config_keys_parser.set_defaults(func=cmd_config_keys)

    # config get
    config_get_parser = config_subparsers.add_parser("get", help="Get a config value")
    config_get_parser.add_argument("key", help="Key in dot notation (e.g., repos.overlay)")
    config_get_parser.set_defaults(func=cmd_config_get)

    # config set
    config_set_parser = config_subparsers.add_parser("set", help="Set config value")
    config_set_parser.add_argument("key", help="Key in dot notation (e.g., repos.overlay)")
    config_set_parser.add_argument("value", help="Value to set (JSON parsed if valid)")
    config_set_parser.add_argument(
        "--global",
        "-g",
        dest="global_",
        action="store_true",
        help="Set in user config instead of project",
    )
    config_set_parser.set_defaults(func=cmd_config_set)

    # Setup
    setup_parser = subparsers.add_parser("setup", help="Environment setup commands")
    setup_subparsers = setup_parser.add_subparsers(dest="setup_command", metavar="SUBCOMMAND")

    # setup submodule
    submodule_parser = setup_subparsers.add_parser("submodule", help="Manage repository submodules")
    submodule_subparsers = submodule_parser.add_subparsers(
        dest="submodule_command", metavar="SUBCOMMAND"
    )

    # setup submodule list
    submodule_list_parser = submodule_subparsers.add_parser(
        "list", help="List available repositories"
    )
    submodule_list_parser.set_defaults(func=cmd_setup_submodule_list)

    # setup submodule add
    submodule_add_parser = submodule_subparsers.add_parser(
        "add", help="Add repository as submodule"
    )
    submodule_add_parser.add_argument(
        "name", nargs="?", help="Repository name (e.g., rhdh-plugin-export-overlays)"
    )
    submodule_add_parser.add_argument(
        "--all", "-a", action="store_true", help="Add all required repositories"
    )
    submodule_add_parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be done without making changes",
    )
    submodule_add_parser.set_defaults(func=cmd_setup_submodule_add)

    # Workspace
    workspace_parser = subparsers.add_parser("workspace", help="Workspace operations")
    workspace_subparsers = workspace_parser.add_subparsers(
        dest="workspace_command", metavar="SUBCOMMAND"
    )

    workspace_list_parser = workspace_subparsers.add_parser("list", help="List plugin workspaces")
    workspace_list_parser.set_defaults(func=cmd_workspace_list)

    workspace_status_parser = workspace_subparsers.add_parser(
        "status", help="Show workspace details"
    )
    workspace_status_parser.add_argument("name", help="Workspace name")
    workspace_status_parser.set_defaults(func=cmd_workspace_status)

    # Log (worklog)
    log_parser = subparsers.add_parser("log", help="Worklog operations")
    log_subparsers = log_parser.add_subparsers(dest="log_command", metavar="SUBCOMMAND")

    log_add_parser = log_subparsers.add_parser("add", help="Add a worklog entry")
    log_add_parser.add_argument("message", help="Log message")
    log_add_parser.add_argument("--tag", "-t", action="append", help="Tag (repeatable)")
    log_add_parser.set_defaults(func=cmd_log_add)

    log_show_parser = log_subparsers.add_parser("show", help="Show recent entries")
    log_show_parser.add_argument(
        "--limit", "-n", type=int, default=20, help="Number of entries (default: 20)"
    )
    log_show_parser.add_argument("--since", "-s", help="Show entries since date (YYYY-MM-DD)")
    log_show_parser.set_defaults(func=cmd_log_show)

    log_search_parser = log_subparsers.add_parser("search", help="Search entries")
    log_search_parser.add_argument("query", help="Search query")
    log_search_parser.add_argument("--limit", "-n", type=int, help="Max results")
    log_search_parser.set_defaults(func=cmd_log_search)

    # Todo
    todo_parser = subparsers.add_parser("todo", help="Todo operations")
    todo_subparsers = todo_parser.add_subparsers(dest="todo_command", metavar="SUBCOMMAND")

    todo_add_parser = todo_subparsers.add_parser("add", help="Add a new todo")
    todo_add_parser.add_argument("title", help="Todo title")
    todo_add_parser.add_argument("--context", "-c", help="Context (workspace, PR, etc.)")
    todo_add_parser.set_defaults(func=cmd_todo_add)

    todo_list_parser = todo_subparsers.add_parser("list", help="List todos")
    todo_list_parser.add_argument(
        "--pending", "-p", action="store_true", help="Show only pending todos"
    )
    todo_list_parser.set_defaults(func=cmd_todo_list)

    todo_done_parser = todo_subparsers.add_parser("done", help="Mark todo as done")
    todo_done_parser.add_argument("slug", help="Todo slug (or partial match)")
    todo_done_parser.set_defaults(func=cmd_todo_done)

    todo_note_parser = todo_subparsers.add_parser("note", help="Add note to todo")
    todo_note_parser.add_argument("slug", help="Todo slug")
    todo_note_parser.add_argument("note", help="Note text")
    todo_note_parser.set_defaults(func=cmd_todo_note)

    todo_show_parser = todo_subparsers.add_parser("show", help="Show raw TODO.md")
    todo_show_parser.set_defaults(func=cmd_todo_show)

    # Local (rhdh-local-setup customization system)
    local_parser = subparsers.add_parser("local", help="Local RHDH customization operations")
    local_subparsers = local_parser.add_subparsers(dest="local_command", metavar="SUBCOMMAND")

    # local status
    local_status_parser = local_subparsers.add_parser(
        "status", help="Show customization sync status"
    )
    local_status_parser.set_defaults(func=cmd_local_status)

    # local apply
    local_apply_parser = local_subparsers.add_parser(
        "apply", help="Apply customizations from rhdh-customizations/ to rhdh-local/"
    )
    local_apply_parser.set_defaults(func=cmd_local_apply)

    # local remove
    local_remove_parser = local_subparsers.add_parser(
        "remove", help="Remove customizations (restore pristine state)"
    )
    local_remove_parser.add_argument(
        "--force", "-f", action="store_true", help="Confirm removal without prompting"
    )
    local_remove_parser.set_defaults(func=cmd_local_remove)

    # local up
    local_up_parser = local_subparsers.add_parser("up", help="Start RHDH Local containers")
    local_up_parser.add_argument(
        "--baseline", action="store_true", help="Start without customizations (pristine RHDH)"
    )
    local_up_parser.add_argument(
        "--customized", action="store_true", help="Start with customizations applied (default)"
    )
    local_up_parser.add_argument(
        "--lightspeed", action="store_true", help="Include Lightspeed compose file"
    )
    local_up_parser.add_argument(
        "--orchestrator", action="store_true", help="Include Orchestrator compose file"
    )
    local_up_parser.add_argument(
        "--both", action="store_true", help="Include both Lightspeed and Orchestrator"
    )
    local_up_parser.add_argument(
        "--ollama",
        action="store_true",
        help="Use Ollama as Lightspeed provider (implies --lightspeed)",
    )
    local_up_parser.add_argument(
        "--safety-guard",
        action="store_true",
        dest="safety_guard",
        help="Enable Llama Guard safety filtering (implies --lightspeed)",
    )
    local_up_parser.add_argument(
        "--follow-logs",
        "-f",
        action="store_true",
        dest="follow_logs",
        help="Follow logs after start",
    )
    local_up_parser.add_argument(
        "--last",
        action="store_true",
        help="Replay last successful run settings",
    )
    local_up_parser.set_defaults(func=cmd_local_up)

    # local down
    local_down_parser = local_subparsers.add_parser("down", help="Stop RHDH Local containers")
    local_down_parser.add_argument(
        "--volumes", "-v", action="store_true", help="Remove named volumes on stop"
    )
    local_down_parser.add_argument(
        "--keep-volumes",
        action="store_true",
        dest="keep_volumes",
        help="Keep volumes on stop (default)",
    )
    local_down_parser.set_defaults(func=cmd_local_down)

    # local plugins
    local_plugins_parser = local_subparsers.add_parser("plugins", help="Plugin operations")
    local_plugins_subparsers = local_plugins_parser.add_subparsers(
        dest="local_plugins_command", metavar="SUBCOMMAND"
    )
    local_plugins_list_parser = local_plugins_subparsers.add_parser(
        "list", help="List plugins from dynamic-plugins.override.yaml"
    )
    local_plugins_list_parser.set_defaults(func=cmd_local_plugins_list)

    # local health
    local_health_parser = local_subparsers.add_parser(
        "health", help="Check health of running RHDH instance"
    )
    local_health_parser.set_defaults(func=cmd_local_health)

    # local backup
    local_backup_parser = local_subparsers.add_parser("backup", help="Backup rhdh-customizations/")
    local_backup_subparsers = local_backup_parser.add_subparsers(
        dest="local_backup_command", metavar="SUBCOMMAND"
    )
    local_backup_parser.set_defaults(func=cmd_local_backup)

    # local backup list
    local_backup_list_parser = local_backup_subparsers.add_parser(
        "list", help="List available backups"
    )
    local_backup_list_parser.set_defaults(func=cmd_local_backup_list)

    # local restore
    local_restore_parser = local_subparsers.add_parser(
        "restore", help="Restore customizations from backup"
    )
    local_restore_parser.add_argument("archive", help="Path to backup .tar.gz file")
    local_restore_parser.add_argument("--force", action="store_true", help=argparse.SUPPRESS)
    local_restore_parser.set_defaults(func=cmd_local_restore)

    # Help command (for compatibility with bash version)
    help_parser = subparsers.add_parser("help", help="Show help")
    help_parser.set_defaults(func=lambda f, a: parser.print_help() or 0)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point.

    Args:
        argv: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0=success, 1=fixable, 2=critical)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Determine output mode
    if args.json:
        mode = "json"
    elif args.human:
        mode = "human"
    else:
        mode = "auto"  # Will auto-detect based on TTY

    # Create formatter
    fmt = OutputFormatter(mode=mode, verbose=getattr(args, "verbose", False))

    # No command = show status (orientation)
    if args.command is None:
        return cmd_status(fmt, args)

    # Config without subcommand
    if args.command == "config" and args.config_command is None:
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Config subcommand required",
            next_steps=[
                "rhdh config init",
                "rhdh config show",
                "rhdh config set <key> <path>",
            ],
        )
        return 1

    # Workspace without subcommand
    if args.command == "workspace" and args.workspace_command is None:
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Workspace subcommand required",
            next_steps=["rhdh workspace list", "rhdh workspace status <name>"],
        )
        return 1

    # Log without subcommand
    if args.command == "log" and args.log_command is None:
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Log subcommand required",
            next_steps=[
                "rhdh log add <message>",
                "rhdh log show",
                "rhdh log search <query>",
            ],
        )
        return 1

    # Todo without subcommand
    if args.command == "todo" and args.todo_command is None:
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Todo subcommand required",
            next_steps=[
                "rhdh todo list",
                "rhdh todo add <title>",
                "rhdh todo show",
            ],
        )
        return 1

    # Local without subcommand
    if args.command == "local" and getattr(args, "local_command", None) is None:
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Local subcommand required",
            next_steps=[
                "rhdh local status",
                "rhdh local up",
                "rhdh local down",
                "rhdh local apply",
                "rhdh local remove --force",
                "rhdh local health",
                "rhdh local backup",
                "rhdh local plugins list",
            ],
        )
        return 1

    # Local plugins without subcommand
    if (
        args.command == "local"
        and getattr(args, "local_command", None) == "plugins"
        and getattr(args, "local_plugins_command", None) is None
    ):
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Local plugins subcommand required",
            next_steps=["rhdh local plugins list"],
        )
        return 1

    # Setup without subcommand
    if args.command == "setup" and getattr(args, "setup_command", None) is None:
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Setup subcommand required",
            next_steps=[
                "rhdh setup submodule list",
                "rhdh setup submodule add --all",
            ],
        )
        return 1

    # Setup submodule without subcommand
    if (
        args.command == "setup"
        and getattr(args, "setup_command", None) == "submodule"
        and getattr(args, "submodule_command", None) is None
    ):
        fmt.error(
            "MISSING_SUBCOMMAND",
            "Submodule subcommand required",
            next_steps=[
                "rhdh setup submodule list",
                "rhdh setup submodule add --all",
                "rhdh setup submodule add <name>",
            ],
        )
        return 1

    # Run the command
    if hasattr(args, "func"):
        return args.func(fmt, args)

    # Fallback
    parser.print_help()
    return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())

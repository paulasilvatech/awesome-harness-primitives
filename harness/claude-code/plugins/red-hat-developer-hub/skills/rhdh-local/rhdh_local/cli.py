"""Standalone CLI for rhdh-local operations.

Provides the command handlers for local RHDH customization management.
Can be used standalone via `rhdh-local` or via the orchestrator `rhdh local`.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Optional

from rhdh.config import get_local_setup_dir
from rhdh.formatters import OutputFormatter

from .backup import (
    backup_customizations,
    list_backups,
    preview_restore,
    restore_customizations,
)
from .compose import local_down, local_up
from .health import check_local_health
from .settings import LastRunSettings, load_last_run, save_last_run
from .sync import apply_customizations, remove_customizations

# =============================================================================
# Helper Functions
# =============================================================================


def _get_local_setup_or_fail(fmt: OutputFormatter) -> Optional[Path]:
    """Get local-setup dir, printing error if not found. Returns None on failure."""
    local_setup = get_local_setup_dir()
    if not local_setup:
        fmt.log_fail("rhdh-local-setup not found")
        fmt.log_info("Configure with: rhdh config set local_setup /path/to/rhdh-local-setup")
        fmt.log_info("Or set env var: RHDH_LOCAL_SETUP_DIR=/path")
        fmt.error(
            "LOCAL_SETUP_NOT_FOUND",
            "rhdh-local-setup directory not configured",
            next_steps=[
                "rhdh config set local_setup /path/to/rhdh-local-setup",
                "export RHDH_LOCAL_SETUP_DIR=/path/to/rhdh-local-setup",
            ],
        )
    return local_setup


def _log_sync_result(fmt: OutputFormatter, result: Any) -> None:
    """Log the results of a copy-sync operation."""
    for path in result.copied:
        fmt.log_ok(f"  Copied: {path}")
    for path in result.removed:
        fmt.log_ok(f"  Removed: {path}")
    for path in result.skipped:
        fmt.log_info(f"  Skipped: {path}")
    for err in result.errors:
        fmt.log_fail(f"  Error: {err}")


# =============================================================================
# Command Handlers
# =============================================================================


def cmd_local_status(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """Show local RHDH customization sync status."""
    from rhdh.cli import run_command

    fmt.header("Local RHDH Status")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    customizations_dir = local_setup / "rhdh-customizations"
    local_dir = local_setup / "rhdh-local"

    checks: list[dict[str, Any]] = []

    # Check rhdh-local exists
    if local_dir.is_dir():
        checks.append({"name": "rhdh_local_dir", "status": "pass", "message": str(local_dir)})
        fmt.log_ok(f"rhdh-local: {local_dir}")

        # Check it is a full checkout (has compose.yaml)
        compose_yaml = local_dir / "compose.yaml"
        if compose_yaml.exists():
            checks.append({"name": "rhdh_local_compose", "status": "pass", "message": "found"})
            fmt.log_ok("  compose.yaml: found (full checkout)")
        else:
            checks.append(
                {
                    "name": "rhdh_local_compose",
                    "status": "warn",
                    "message": "compose.yaml missing - this looks like an overlay copy, not a full rhdh-local checkout",
                }
            )
            fmt.log_warn(
                "  compose.yaml not found - rhdh-local/ appears to be a partial overlay directory, not a full checkout"
            )
            fmt.log_warn("  The detected rhdh-local-setup may not match the running RHDH instance.")
            fmt.log_warn(
                "  Set RHDH_LOCAL_SETUP_DIR or run: rhdh config set local_setup /path/to/correct/setup"
            )

        # Check git status
        rc, stdout, _ = run_command(["git", "status", "--porcelain"], cwd=local_dir)
        if rc == 0:
            if stdout.strip():
                checks.append(
                    {
                        "name": "rhdh_local_git",
                        "status": "warn",
                        "message": "unexpected tracked modifications (check .gitignore)",
                    }
                )
                fmt.log_warn(
                    "  git status: unexpected modifications (override files should be gitignored)"
                )
            else:
                checks.append({"name": "rhdh_local_git", "status": "pass", "message": "clean"})
                fmt.log_ok("  git status: clean")

    else:
        checks.append({"name": "rhdh_local_dir", "status": "fail", "message": "not found"})
        fmt.log_fail(f"rhdh-local not found at: {local_dir}")

    # Check customizations dir
    if customizations_dir.is_dir():
        checks.append(
            {"name": "customizations_dir", "status": "pass", "message": str(customizations_dir)}
        )
        fmt.log_ok(f"rhdh-customizations: {customizations_dir}")

        # Check if customizations are synced
        if local_dir.is_dir():
            override_yaml = (
                local_dir / "configs" / "dynamic-plugins" / "dynamic-plugins.override.yaml"
            )
            if override_yaml.exists():
                checks.append(
                    {"name": "sync_status", "status": "pass", "message": "customizations synced"}
                )
                fmt.log_ok("  sync status: customizations applied to rhdh-local")
            else:
                checks.append(
                    {
                        "name": "sync_status",
                        "status": "info",
                        "message": "customizations not synced",
                    }
                )
                fmt.log_info("  sync status: not synced (run rhdh local apply)")
    else:
        checks.append({"name": "customizations_dir", "status": "fail", "message": "not found"})
        fmt.log_fail(f"rhdh-customizations not found at: {customizations_dir}")

    # Check if RHDH is running on port 7007
    import socket

    rhdh_running = False
    try:
        with socket.create_connection(("localhost", 7007), timeout=1):
            rhdh_running = True
    except OSError:
        pass

    if rhdh_running:
        checks.append({"name": "rhdh_running", "status": "pass", "message": "running on :7007"})
        fmt.log_ok("RHDH: running on http://localhost:7007")
    else:
        checks.append({"name": "rhdh_running", "status": "info", "message": "not running"})
        fmt.log_info("RHDH: not running (port 7007 not open)")

    data: dict[str, Any] = {
        "local_setup": str(local_setup),
        "checks": checks,
        "rhdh_running": rhdh_running,
    }

    next_steps = [
        "rhdh local apply",
        "rhdh local up --customized",
        "rhdh local plugins list",
    ]
    fmt.success(data, next_steps=next_steps)
    return 0


def cmd_local_apply(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """Apply customizations from rhdh-customizations/ to rhdh-local/."""
    fmt.header("Apply Customizations")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    result = apply_customizations(local_setup)
    _log_sync_result(fmt, result)

    if result.errors:
        fmt.error("APPLY_FAILED", "\n".join(result.errors), next_steps=[])
        return 1

    fmt.log_ok("Customizations applied successfully")
    data: dict[str, Any] = {"status": "applied", "copied": result.copied}
    fmt.success(data, next_steps=["rhdh local up --customized"])
    return 0


def cmd_local_remove(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Remove customization copies from rhdh-local/ (restore pristine state)."""
    fmt.header("Remove Customizations")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    force = getattr(args, "force", False)
    if not force:
        fmt.log_warn(
            "This removes customization copies from rhdh-local/ (restores pristine state)."
        )
        fmt.log_warn("Use --force to confirm.")
        fmt.error(
            "CONFIRMATION_REQUIRED",
            "Use --force to remove customizations",
            next_steps=["rhdh local remove --force"],
        )
        return 1

    result = remove_customizations(local_setup)
    _log_sync_result(fmt, result)

    if result.errors:
        fmt.error("REMOVE_FAILED", "\n".join(result.errors), next_steps=[])
        return 1

    fmt.log_ok("Customizations removed (rhdh-local/ is now pristine)")
    data: dict[str, Any] = {"status": "removed", "removed": result.removed}
    fmt.success(data, next_steps=["rhdh local up --baseline"])
    return 0


def cmd_local_up(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Start RHDH Local containers."""
    fmt.header("RHDH Local Up")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    baseline = getattr(args, "baseline", False)
    lightspeed = getattr(args, "lightspeed", False)
    orchestrator_flag = getattr(args, "orchestrator", False)
    both = getattr(args, "both", False)
    follow_logs = getattr(args, "follow_logs", False)
    use_last = getattr(args, "last", False)
    ollama = getattr(args, "ollama", False)
    safety_guard = getattr(args, "safety_guard", False)

    # --ollama implies --lightspeed
    if ollama:
        lightspeed = True

    # --safety-guard implies --lightspeed
    if safety_guard:
        lightspeed = True

    lightspeed_provider = "ollama" if ollama else "base"

    # --last: replay previous settings
    if use_last:
        if any([baseline, lightspeed, orchestrator_flag, both]):
            fmt.error(
                "INVALID_FLAGS",
                "--last cannot be combined with --baseline, --lightspeed, --orchestrator, --both, --ollama, or --safety-guard",
                next_steps=["rhdh local up --last"],
            )
            return 1
        last = load_last_run(local_setup)
        if not last:
            fmt.error(
                "NO_LAST_RUN",
                "No previous run settings found",
                next_steps=["rhdh local up --customized"],
            )
            return 1
        baseline = last.mode == "baseline"
        lightspeed = last.lightspeed
        orchestrator_flag = last.orchestrator
        follow_logs = last.follow_logs
        lightspeed_provider = last.lightspeed_provider
        safety_guard = last.safety_guard

    if both:
        lightspeed = True
        orchestrator_flag = True

    mode = "baseline" if baseline else "customized"
    fmt.log_info(f"Starting RHDH ({mode} mode)...")

    try:
        sync, rc, stdout, stderr = local_up(
            local_setup,
            baseline=baseline,
            lightspeed=lightspeed,
            orchestrator=orchestrator_flag,
            follow_logs=follow_logs,
            lightspeed_provider=lightspeed_provider,
            safety_guard=safety_guard,
        )
    except RuntimeError as e:
        fmt.log_fail(str(e))
        fmt.error("RUNTIME_ERROR", str(e), next_steps=["Install podman or docker"])
        return 1

    _log_sync_result(fmt, sync)

    if stdout:
        for line in stdout.splitlines():
            fmt.log_info(line)
    if stderr:
        for line in stderr.splitlines():
            fmt.log_warn(line)

    if rc == 0:
        # Save settings for --last replay
        save_last_run(
            local_setup,
            LastRunSettings(
                mode=mode,
                lightspeed=lightspeed,
                orchestrator=orchestrator_flag,
                follow_logs=follow_logs,
                lightspeed_provider=lightspeed_provider,
                safety_guard=safety_guard,
            ),
        )
        data: dict[str, Any] = {"status": "started", "mode": mode}
        fmt.success(data, next_steps=["rhdh local status", "rhdh local health"])
        return 0
    else:
        fmt.log_fail(f"Container start failed (exit {rc})")
        fmt.error("UP_FAILED", f"Compose exited with {rc}", next_steps=["rhdh local status"])
        return 1


def cmd_local_down(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Stop RHDH Local containers."""
    fmt.header("RHDH Local Down")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    volumes = getattr(args, "volumes", False)

    try:
        sync, rc, stdout, stderr = local_down(local_setup, volumes=volumes)
    except RuntimeError as e:
        fmt.log_fail(str(e))
        fmt.error("RUNTIME_ERROR", str(e), next_steps=["Install podman or docker"])
        return 1

    if stdout:
        for line in stdout.splitlines():
            fmt.log_info(line)
    if stderr:
        for line in stderr.splitlines():
            fmt.log_warn(line)

    _log_sync_result(fmt, sync)

    if rc == 0:
        data: dict[str, Any] = {"status": "stopped"}
        fmt.success(data, next_steps=["rhdh local status"])
        return 0
    else:
        fmt.log_fail(f"Container stop failed (exit {rc})")
        fmt.error("DOWN_FAILED", f"Compose exited with {rc}", next_steps=[])
        return 1


def cmd_local_health(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """Check health of the local RHDH instance."""
    fmt.header("RHDH Local Health")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    checks = check_local_health(local_setup)

    for check in checks:
        if check.status == "pass":
            fmt.log_ok(f"{check.name}: {check.message}")
        elif check.status == "fail":
            fmt.log_fail(f"{check.name}: {check.message}")
        elif check.status == "warn":
            fmt.log_warn(f"{check.name}: {check.message}")
        else:
            fmt.log_info(f"{check.name}: {check.message}")

    has_failures = any(c.status == "fail" for c in checks)
    data: dict[str, Any] = {
        "checks": [{"name": c.name, "status": c.status, "message": c.message} for c in checks],
        "healthy": not has_failures,
    }
    fmt.success(data, next_steps=["rhdh local status", "rhdh local up --last"])
    return 0 if not has_failures else 1


def cmd_local_backup(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """Create a backup of rhdh-customizations/."""
    fmt.header("Backup Customizations")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    try:
        info = backup_customizations(local_setup)
    except FileNotFoundError as e:
        fmt.log_fail(str(e))
        fmt.error("BACKUP_FAILED", str(e), next_steps=[])
        return 1

    size_kb = info.size_bytes / 1024
    fmt.log_ok(f"Backup created: {info.path}")
    fmt.log_info(f"  Size: {size_kb:.1f} KB")
    fmt.log_info(f"  Timestamp: {info.timestamp}")

    # Warn about credentials
    env_file = local_setup / "rhdh-customizations" / ".env"
    if env_file.is_file():
        fmt.log_warn("  Archive contains .env (may include credentials)")

    data: dict[str, Any] = {
        "path": str(info.path),
        "timestamp": info.timestamp,
        "size_bytes": info.size_bytes,
    }
    fmt.success(data, next_steps=["rhdh local backup list"])
    return 0


def cmd_local_backup_list(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """List available backups."""
    fmt.header("Available Backups")

    backups = list_backups()

    if not backups:
        fmt.log_info("No backups found")
        fmt.success({"count": 0, "backups": []}, next_steps=["rhdh local backup"])
        return 0

    for b in backups:
        size_kb = b.size_bytes / 1024
        fmt.log_info(f"  {b.timestamp}  {size_kb:>8.1f} KB  {b.path}")

    data: dict[str, Any] = {
        "count": len(backups),
        "backups": [
            {"path": str(b.path), "timestamp": b.timestamp, "size_bytes": b.size_bytes}
            for b in backups
        ],
    }
    fmt.success(data, next_steps=["rhdh local restore <archive>"])
    return 0


def cmd_local_restore(fmt: OutputFormatter, args: argparse.Namespace) -> int:
    """Restore customizations from a backup archive."""
    fmt.header("Restore Customizations")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    archive = Path(getattr(args, "archive", ""))
    force = getattr(args, "force", False)

    if not archive.is_file():
        fmt.log_fail(f"Archive not found: {archive}")
        fmt.error("ARCHIVE_NOT_FOUND", str(archive), next_steps=["rhdh local backup list"])
        return 1

    if not force:
        # Dry-run: show what would be restored
        try:
            files = preview_restore(archive)
        except FileNotFoundError as e:
            fmt.log_fail(str(e))
            fmt.error("PREVIEW_FAILED", str(e), next_steps=[])
            return 1

        fmt.log_info(f"Would restore {len(files)} files from: {archive}")
        for f in files:
            fmt.log_info(f"  {f}")

        fmt.error(
            "CONFIRMATION_REQUIRED",
            "Use --force to restore",
            next_steps=[f"rhdh local restore {archive} --force"],
        )
        return 1

    result = restore_customizations(local_setup, archive)

    if result.errors:
        for err in result.errors:
            fmt.log_fail(err)
        fmt.error("RESTORE_FAILED", "\n".join(result.errors), next_steps=[])
        return 1

    fmt.log_ok(f"Restored {len(result.copied)} files from {archive}")
    data: dict[str, Any] = {"status": "restored", "files": result.copied}
    fmt.success(data, next_steps=["rhdh local apply", "rhdh local status"])
    return 0


def cmd_local_plugins_list(fmt: OutputFormatter, _args: argparse.Namespace) -> int:
    """List plugins from dynamic-plugins.override.yaml."""
    fmt.header("Dynamic Plugins (Override)")

    local_setup = _get_local_setup_or_fail(fmt)
    if not local_setup:
        return 1

    override_yaml = (
        local_setup
        / "rhdh-customizations"
        / "configs"
        / "dynamic-plugins"
        / "dynamic-plugins.override.yaml"
    )

    if not override_yaml.exists():
        fmt.log_info("dynamic-plugins.override.yaml not found")
        fmt.log_info(f"Expected: {override_yaml}")
        data: dict[str, Any] = {"plugins": [], "override_yaml": str(override_yaml)}
        fmt.success(
            data,
            next_steps=[
                "Create the file to add plugins",
                "See skills/rhdh-local/workflows/enable-plugin.md",
            ],
        )
        return 0

    # Parse YAML (simple line-by-line -- stdlib only, no yaml dependency)
    try:
        content = override_yaml.read_text()
        plugin_entries: list[dict[str, Any]] = []
        current: dict[str, Any] = {}

        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- package:"):
                if current:
                    plugin_entries.append(current)
                package = stripped[len("- package:") :].strip().strip("'\"")
                current = {"package": package, "disabled": False}
            elif stripped.startswith("disabled:") and current:
                val = stripped[len("disabled:") :].strip().lower()
                current["disabled"] = val in ("true", "yes", "1")

        if current:
            plugin_entries.append(current)

    except Exception as e:
        fmt.log_fail(f"Failed to parse {override_yaml}: {e}")
        fmt.error("PARSE_ERROR", str(e), next_steps=[])
        return 1

    enabled = [p for p in plugin_entries if not p["disabled"]]
    disabled = [p for p in plugin_entries if p["disabled"]]

    fmt.log_info(f"File: {override_yaml}")
    fmt.log_info(
        f"Total: {len(plugin_entries)} packages ({len(enabled)} enabled, {len(disabled)} disabled)"
    )

    if enabled:
        fmt.header(f"Enabled ({len(enabled)})")
        for p in enabled:
            fmt.log_ok(p["package"])

    if disabled:
        fmt.header(f"Disabled ({len(disabled)})")
        for p in disabled:
            fmt.log_warn(p["package"])

    data = {
        "override_yaml": str(override_yaml),
        "plugins": plugin_entries,
        "enabled_count": len(enabled),
        "disabled_count": len(disabled),
    }
    fmt.success(data, next_steps=["rhdh local status"])
    return 0


# =============================================================================
# Standalone CLI
# =============================================================================


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for standalone rhdh-local CLI."""
    parser = argparse.ArgumentParser(
        prog="rhdh-local",
        description="CLI for local RHDH customization management",
    )

    # Output format flags
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument("--json", action="store_true", help="Force JSON output")
    format_group.add_argument("--human", action="store_true", help="Force human-readable output")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # status
    status_parser = subparsers.add_parser("status", help="Show customization sync status")
    status_parser.set_defaults(func=cmd_local_status)

    # apply
    apply_parser = subparsers.add_parser("apply", help="Apply customizations")
    apply_parser.set_defaults(func=cmd_local_apply)

    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove customizations")
    remove_parser.add_argument("--force", "-f", action="store_true", help="Confirm removal")
    remove_parser.set_defaults(func=cmd_local_remove)

    # up
    up_parser = subparsers.add_parser("up", help="Start RHDH Local containers")
    up_parser.add_argument("--baseline", action="store_true", help="Start without customizations")
    up_parser.add_argument(
        "--customized", action="store_true", help="Start with customizations (default)"
    )
    up_parser.add_argument(
        "--lightspeed", action="store_true", help="Include Lightspeed compose file"
    )
    up_parser.add_argument(
        "--orchestrator", action="store_true", help="Include Orchestrator compose file"
    )
    up_parser.add_argument(
        "--both", action="store_true", help="Include both Lightspeed and Orchestrator"
    )
    up_parser.add_argument(
        "--ollama",
        action="store_true",
        help="Use Ollama as Lightspeed provider (implies --lightspeed)",
    )
    up_parser.add_argument(
        "--safety-guard",
        action="store_true",
        dest="safety_guard",
        help="Enable Llama Guard safety filtering (implies --lightspeed)",
    )
    up_parser.add_argument(
        "--follow-logs",
        "-f",
        action="store_true",
        dest="follow_logs",
        help="Follow logs after start",
    )
    up_parser.add_argument(
        "--last", action="store_true", help="Replay last successful run settings"
    )
    up_parser.set_defaults(func=cmd_local_up)

    # down
    down_parser = subparsers.add_parser("down", help="Stop RHDH Local containers")
    down_parser.add_argument("--volumes", "-v", action="store_true", help="Remove named volumes")
    down_parser.set_defaults(func=cmd_local_down)

    # health
    health_parser = subparsers.add_parser("health", help="Check health of running RHDH instance")
    health_parser.set_defaults(func=cmd_local_health)

    # backup
    backup_parser = subparsers.add_parser("backup", help="Backup rhdh-customizations/")
    backup_subparsers = backup_parser.add_subparsers(dest="backup_command", metavar="SUBCOMMAND")
    backup_parser.set_defaults(func=cmd_local_backup)

    backup_list_parser = backup_subparsers.add_parser("list", help="List available backups")
    backup_list_parser.set_defaults(func=cmd_local_backup_list)

    # restore
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("archive", help="Path to backup .tar.gz file")
    restore_parser.add_argument("--force", action="store_true", help=argparse.SUPPRESS)
    restore_parser.set_defaults(func=cmd_local_restore)

    # plugins
    plugins_parser = subparsers.add_parser("plugins", help="Plugin operations")
    plugins_subparsers = plugins_parser.add_subparsers(dest="plugins_command", metavar="SUBCOMMAND")
    plugins_list_parser = plugins_subparsers.add_parser("list", help="List plugins")
    plugins_list_parser.set_defaults(func=cmd_local_plugins_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for standalone rhdh-local CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Determine output mode
    if args.json:
        mode = "json"
    elif args.human:
        mode = "human"
    else:
        mode = "auto"

    fmt = OutputFormatter(mode=mode)

    if args.command is None:
        return cmd_local_status(fmt, args)

    if hasattr(args, "func"):
        return args.func(fmt, args)

    parser.print_help()
    return 1

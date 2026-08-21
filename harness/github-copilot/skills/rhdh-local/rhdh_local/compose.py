"""Container runtime detection and compose command builder.

Handles podman/docker detection, compose file selection (including
Lightspeed and Orchestrator variants), and container lifecycle.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .sync import apply_customizations, remove_customizations


def detect_compose_command() -> list[str]:
    """Auto-detect container runtime and return compose command parts.

    Returns:
        ["podman", "compose"] or ["docker", "compose"]

    Raises:
        RuntimeError: If neither podman nor docker is found.
    """
    if shutil.which("podman"):
        return ["podman", "compose"]
    if shutil.which("docker"):
        return ["docker", "compose"]
    raise RuntimeError("Neither podman nor docker found in PATH")


# Compose files to include, checked in order. Both our naming convention
# and rhdh-lab's naming convention are supported.
_LIGHTSPEED_COMPOSE_FILES = [
    "developer-lightspeed/compose.lightspeed.yaml",  # our convention
    "developer-lightspeed/compose.yaml",  # rhdh-lab convention
]
_LIGHTSPEED_OLLAMA_COMPOSE_FILES = [
    "developer-lightspeed/compose-with-ollama.yaml",  # rhdh-lab convention
]
_SAFETY_GUARD_COMPOSE_FILES = [
    "developer-lightspeed/compose-with-safety-guard.yaml",  # base provider
]
_SAFETY_GUARD_OLLAMA_COMPOSE_FILES = [
    "developer-lightspeed/compose-with-safety-guard-ollama.yaml",  # ollama provider
]
_ORCHESTRATOR_COMPOSE_FILES = [
    "developer-ai-orchestrator/compose.orchestrator.yaml",  # our convention
    "orchestrator/compose.yaml",  # rhdh-lab convention
]


def build_compose_args(
    rhdh_local: Path,
    lightspeed: bool = False,
    orchestrator: bool = False,
    lightspeed_provider: str = "base",
    safety_guard: bool = False,
) -> list[str]:
    """Build the compose -f flag chain from available files.

    Args:
        rhdh_local: Path to rhdh-local/ directory.
        lightspeed: Include Lightspeed compose file.
        orchestrator: Include Orchestrator compose file.
        lightspeed_provider: LLM provider - "base" (BYOM) or "ollama".
        safety_guard: Include Llama Guard safety guard compose file.

    Returns:
        List of args like ["-f", "compose.yaml", "-f", "compose.override.yaml", ...].
    """
    args = ["-f", "compose.yaml"]

    if (rhdh_local / "compose.override.yaml").is_file():
        args.extend(["-f", "compose.override.yaml"])

    if lightspeed:
        if lightspeed_provider == "ollama":
            # Ollama-specific compose file
            for candidate in _LIGHTSPEED_OLLAMA_COMPOSE_FILES:
                if (rhdh_local / candidate).is_file():
                    args.extend(["-f", candidate])
                    break
        else:
            # Base (BYOM) compose file
            for candidate in _LIGHTSPEED_COMPOSE_FILES:
                if (rhdh_local / candidate).is_file():
                    args.extend(["-f", candidate])
                    break

        # Safety guard overlay (depends on provider)
        if safety_guard:
            guard_files = (
                _SAFETY_GUARD_OLLAMA_COMPOSE_FILES
                if lightspeed_provider == "ollama"
                else _SAFETY_GUARD_COMPOSE_FILES
            )
            for candidate in guard_files:
                if (rhdh_local / candidate).is_file():
                    args.extend(["-f", candidate])
                    break

    if orchestrator:
        for candidate in _ORCHESTRATOR_COMPOSE_FILES:
            if (rhdh_local / candidate).is_file():
                args.extend(["-f", candidate])
                break

    return args


def _run_compose(
    compose_cmd: list[str],
    compose_args: list[str],
    action_args: list[str],
    cwd: Path,
) -> tuple[int, str, str]:
    """Run a compose command and return (returncode, stdout, stderr)."""
    full_cmd = [*compose_cmd, *compose_args, *action_args]
    if not cwd.is_dir():
        return -1, "", f"Working directory not found: {cwd}"
    try:
        proc = subprocess.run(full_cmd, capture_output=True, text=True, cwd=cwd)
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return -1, "", f"Command not found: {full_cmd[0]}"


def local_up(
    workspace: Path,
    baseline: bool = False,
    lightspeed: bool = False,
    orchestrator: bool = False,
    follow_logs: bool = False,
    lightspeed_provider: str = "base",
    safety_guard: bool = False,
) -> tuple:
    """Apply customizations (or remove if baseline) and start containers.

    Returns:
        Tuple of (sync_result, compose_returncode, stdout, stderr).
    """
    rhdh_local = workspace / "rhdh-local"

    # Step 1: sync customizations
    if baseline:
        sync = remove_customizations(workspace)
    else:
        sync = apply_customizations(workspace)

    if sync.errors:
        return sync, 1, "", "\n".join(sync.errors)

    # Step 2: detect runtime and build command
    compose_cmd = detect_compose_command()
    compose_args = build_compose_args(
        rhdh_local,
        lightspeed=lightspeed,
        orchestrator=orchestrator,
        lightspeed_provider=lightspeed_provider,
        safety_guard=safety_guard,
    )

    # Step 3: start containers
    rc, stdout, stderr = _run_compose(compose_cmd, compose_args, ["up", "-d"], cwd=rhdh_local)

    # Step 4: follow logs if requested (blocking)
    if rc == 0 and follow_logs:
        # Run logs in foreground -- this blocks until Ctrl+C
        try:
            subprocess.run(
                [*compose_cmd, *compose_args, "logs", "-f"],
                cwd=rhdh_local,
            )
        except KeyboardInterrupt:
            pass

    return sync, rc, stdout, stderr


def local_down(
    workspace: Path,
    volumes: bool = False,
) -> tuple:
    """Stop containers and remove customizations.

    Returns:
        Tuple of (sync_result, compose_returncode, stdout, stderr).
    """
    rhdh_local = workspace / "rhdh-local"

    # Step 1: detect runtime and build command (include all available files)
    compose_cmd = detect_compose_command()
    compose_args = build_compose_args(rhdh_local, lightspeed=True, orchestrator=True)

    # Step 2: stop containers
    action_args = ["down", "-v"] if volumes else ["down"]
    rc, stdout, stderr = _run_compose(compose_cmd, compose_args, action_args, cwd=rhdh_local)

    # Step 3: always remove customizations after shutdown
    sync = remove_customizations(workspace)

    return sync, rc, stdout, stderr

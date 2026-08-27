"""Health checks for the local RHDH instance.

Checks container runtime, port availability, container status,
and backend health endpoints.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from .compose import (
    _run_compose,
    build_compose_args,
    detect_compose_command,
)


@dataclass
class HealthCheck:
    """Result of a single health check."""

    name: str
    status: str  # "pass", "fail", "warn", "info"
    message: str
    detail: str = ""


def check_local_health(workspace: Path) -> list[HealthCheck]:
    """Run health checks on the local RHDH instance.

    Checks: container runtime, port 7007, container status,
    backend health endpoint, plugin install log.
    """
    checks: list[HealthCheck] = []
    rhdh_local = workspace / "rhdh-local"

    # 1. Container runtime
    try:
        compose_cmd = detect_compose_command()
        checks.append(
            HealthCheck(
                name="container_runtime",
                status="pass",
                message=f"{compose_cmd[0]} found",
            )
        )
    except RuntimeError as e:
        checks.append(
            HealthCheck(
                name="container_runtime",
                status="fail",
                message=str(e),
            )
        )
        return checks  # can't continue without runtime

    # 2. Port 7007 reachable
    port_open = False
    try:
        with socket.create_connection(("localhost", 7007), timeout=2):
            port_open = True
    except OSError:
        pass

    if port_open:
        checks.append(
            HealthCheck(
                name="rhdh_port",
                status="pass",
                message="RHDH reachable on http://localhost:7007",
            )
        )
    else:
        checks.append(
            HealthCheck(
                name="rhdh_port",
                status="fail",
                message="Port 7007 not reachable (RHDH not running?)",
            )
        )

    # 3. Container status via compose ps
    if rhdh_local.is_dir():
        compose_args = build_compose_args(rhdh_local, lightspeed=True, orchestrator=True)
        rc, stdout, _ = _run_compose(
            compose_cmd, compose_args, ["ps", "--format", "json"], cwd=rhdh_local
        )
        if rc == 0 and stdout.strip():
            checks.append(
                HealthCheck(
                    name="containers",
                    status="pass",
                    message="Containers running",
                    detail=stdout.strip(),
                )
            )
        else:
            checks.append(
                HealthCheck(
                    name="containers",
                    status="fail",
                    message="No containers found or compose ps failed",
                )
            )

    # 4. Backend health endpoint
    if port_open:
        try:
            with urlopen("http://localhost:7007/api/catalog/health", timeout=5) as resp:
                body = resp.read().decode()
                if "ok" in body.lower():
                    checks.append(
                        HealthCheck(
                            name="backend_health",
                            status="pass",
                            message="Catalog backend healthy",
                        )
                    )
                else:
                    checks.append(
                        HealthCheck(
                            name="backend_health",
                            status="warn",
                            message=f"Unexpected response: {body[:100]}",
                        )
                    )
        except HTTPError as e:
            if e.code in (401, 403):
                checks.append(
                    HealthCheck(
                        name="backend_health",
                        status="pass",
                        message="Backend responding (auth required)",
                    )
                )
            else:
                checks.append(
                    HealthCheck(
                        name="backend_health",
                        status="warn",
                        message=f"Health endpoint returned HTTP {e.code}",
                    )
                )
        except (URLError, OSError) as e:
            checks.append(
                HealthCheck(
                    name="backend_health",
                    status="warn",
                    message=f"Health endpoint not reachable: {e}",
                )
            )

    return checks

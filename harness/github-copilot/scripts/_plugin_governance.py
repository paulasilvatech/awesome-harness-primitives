"""Deterministic plugin classification shared by the audit and the catalog.

Classification is descriptive, never destructive: it records lifecycle, runtime
assurance, and provenance so consumers can filter a large marketplace without
any package being altered or withheld.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Any

SEMVER_PREFIX_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")
# Matches the repository freshness policy for dated evidence.
PROBE_FRESHNESS_DAYS = 90

LIFECYCLE_ACTIVE = "active"
LIFECYCLE_INCUBATING = "incubating"
LIFECYCLE_DEPRECATED = "deprecated"

ASSURANCE_RUNTIME_VERIFIED = "runtime-verified"
ASSURANCE_RUNTIME_STALE = "runtime-stale"
ASSURANCE_RUNTIME_REQUIRED = "runtime-required"
ASSURANCE_STATIC = "static-validated"

PROVENANCE_REPOSITORY = "repository"
PROVENANCE_UPSTREAM = "upstream-mirror"


@dataclass(frozen=True)
class Classification:
    lifecycle: str
    assurance: str
    provenance: str
    last_runtime_probe: str | None


def parse_probe_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def lifecycle_of(version: Any, governance: dict[str, Any]) -> str:
    override = governance.get("lifecycle")
    if isinstance(override, str) and override:
        return override
    match = SEMVER_PREFIX_RE.match(version if isinstance(version, str) else "")
    if match is not None and match.group(1) == "0":
        return LIFECYCLE_INCUBATING
    return LIFECYCLE_ACTIVE


def provenance_of(source_config: dict[str, Any]) -> str:
    upstream_repository = source_config.get("upstreamRepository")
    upstream_commit = source_config.get("upstreamCommit")
    if isinstance(upstream_repository, str) and isinstance(upstream_commit, str):
        if upstream_repository.strip() and upstream_commit.strip():
            return PROVENANCE_UPSTREAM
    return PROVENANCE_REPOSITORY


def assurance_of(
    governance: dict[str, Any],
    *,
    has_runtime_surface: bool,
    as_of: date,
) -> str:
    """Classify how far validation went beyond static checks.

    A package that ships MCP servers, hooks, or client extensions cannot be called
    statically validated, because static checks never exercise those surfaces.
    """
    probe_date = parse_probe_date(governance.get("lastRuntimeProbe"))
    if probe_date is not None:
        if (as_of - probe_date).days <= PROBE_FRESHNESS_DAYS:
            return ASSURANCE_RUNTIME_VERIFIED
        return ASSURANCE_RUNTIME_STALE
    if has_runtime_surface:
        return ASSURANCE_RUNTIME_REQUIRED
    return ASSURANCE_STATIC


def classify(
    *,
    version: Any,
    source_config: dict[str, Any],
    mcp_servers: int = 0,
    hooks: int = 0,
    extensions: int = 0,
    as_of: date,
) -> Classification:
    governance = source_config.get("governance")
    governance = governance if isinstance(governance, dict) else {}
    probe = governance.get("lastRuntimeProbe")
    return Classification(
        lifecycle=lifecycle_of(version, governance),
        assurance=assurance_of(
            governance,
            has_runtime_surface=bool(mcp_servers or hooks or extensions),
            as_of=as_of,
        ),
        provenance=provenance_of(source_config),
        last_runtime_probe=probe if isinstance(probe, str) else None,
    )

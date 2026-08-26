"""Last run settings persistence for --last flag replay.

Saves and loads the settings from the most recent successful
`rhdh local up` invocation so they can be replayed with --last.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

LAST_RUN_FILE = ".last-run-settings"
_LAST_RUN_VERSION = "1"
_KEY_PATTERN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$")


@dataclass
class LastRunSettings:
    """Persisted settings from the last successful rhdh local up."""

    mode: str = "customized"
    lightspeed: bool = False
    orchestrator: bool = False
    follow_logs: bool = False
    lightspeed_provider: str = "base"
    safety_guard: bool = False


def save_last_run(workspace: Path, settings: LastRunSettings) -> Path:
    """Save settings atomically after successful container start.

    Returns:
        Path to the saved settings file.
    """
    path = workspace / LAST_RUN_FILE
    tmp_path = workspace / f"{LAST_RUN_FILE}.tmp"

    content = (
        f"# Last successful rhdh local up configuration (auto-generated)\n"
        f"VERSION={_LAST_RUN_VERSION}\n"
        f"MODE={settings.mode}\n"
        f"INCLUDE_LIGHTSPEED={'true' if settings.lightspeed else 'false'}\n"
        f"INCLUDE_ORCHESTRATOR={'true' if settings.orchestrator else 'false'}\n"
        f"FOLLOW_LOGS={'true' if settings.follow_logs else 'false'}\n"
        f"LIGHTSPEED_PROVIDER={settings.lightspeed_provider}\n"
        f"SAFETY_GUARD={'true' if settings.safety_guard else 'false'}\n"
    )

    tmp_path.write_text(content)
    os.replace(tmp_path, path)
    return path


def load_last_run(workspace: Path) -> Optional[LastRunSettings]:
    """Load and validate last run settings.

    Returns:
        LastRunSettings if valid, None if file missing or invalid.
    """
    path = workspace / LAST_RUN_FILE
    if not path.is_file():
        return None

    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _KEY_PATTERN.match(line)
        if not m:
            return None  # malformed line
        values[m.group(1)] = m.group(2).strip()

    # Validate version
    if values.get("VERSION") != _LAST_RUN_VERSION:
        return None

    # Validate mode
    mode = values.get("MODE", "")
    if mode not in ("customized", "baseline"):
        return None

    def _parse_bool(key: str) -> bool:
        return values.get(key, "false").lower() == "true"

    # Validate lightspeed_provider
    provider = values.get("LIGHTSPEED_PROVIDER", "base")
    if provider not in ("base", "ollama"):
        provider = "base"

    return LastRunSettings(
        mode=mode,
        lightspeed=_parse_bool("INCLUDE_LIGHTSPEED"),
        orchestrator=_parse_bool("INCLUDE_ORCHESTRATOR"),
        follow_logs=_parse_bool("FOLLOW_LOGS"),
        lightspeed_provider=provider,
        safety_guard=_parse_bool("SAFETY_GUARD"),
    )

"""Copy-sync operations for rhdh-local customizations.

Manages the file mapping between rhdh-customizations/ and rhdh-local/,
including apply (copy) and remove operations.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

# Single source of truth for the customization file mapping.
# These are relative paths within the workspace (rhdh-customizations/ -> rhdh-local/).
CUSTOMIZATION_FILES = [
    "compose.override.yaml",
    ".env",
    "configs/app-config/app-config.local.yaml",
    "configs/dynamic-plugins/dynamic-plugins.override.yaml",
    "developer-lightspeed/configs/app-config/app-config.lightspeed.local.yaml",
]

CUSTOMIZATION_GLOBS = [
    "configs/catalog-entities/*.override.yaml",
    "configs/extra-files/*",
    "configs/translations/*.json",
]


@dataclass
class SyncResult:
    """Result of a copy-sync operation."""

    copied: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def apply_customizations(workspace: Path) -> SyncResult:
    """Copy override files from rhdh-customizations/ into rhdh-local/.

    Args:
        workspace: Path to rhdh-local-setup workspace root.

    Returns:
        SyncResult with lists of copied, skipped, and errored paths.
    """
    src = workspace / "rhdh-customizations"
    dst = workspace / "rhdh-local"
    result = SyncResult()

    if not src.is_dir():
        result.errors.append(f"rhdh-customizations not found: {src}")
        return result
    if not dst.is_dir():
        result.errors.append(f"rhdh-local not found: {dst}")
        return result

    # Fixed files
    for rel in CUSTOMIZATION_FILES:
        _copy_file(src / rel, dst / rel, rel, result)

    # Glob patterns
    for pattern in CUSTOMIZATION_GLOBS:
        for src_file in src.glob(pattern):
            if not src_file.is_file():
                continue
            rel = src_file.relative_to(src).as_posix()
            _copy_file(src_file, dst / rel, rel, result)

    return result


def remove_customizations(workspace: Path) -> SyncResult:
    """Remove copied override files from rhdh-local/.

    Uses rhdh-customizations/ as the reference for wildcard removals,
    so only files that were actually copied get removed.

    Args:
        workspace: Path to rhdh-local-setup workspace root.

    Returns:
        SyncResult with lists of removed and skipped paths.
    """
    src = workspace / "rhdh-customizations"
    dst = workspace / "rhdh-local"
    result = SyncResult()

    # Fixed files -- remove from dst regardless of src existence
    for rel in CUSTOMIZATION_FILES:
        _remove_file(dst / rel, rel, result)

    # Glob patterns -- use src as reference for what to remove
    if src.is_dir():
        for pattern in CUSTOMIZATION_GLOBS:
            for src_file in src.glob(pattern):
                if not src_file.is_file():
                    continue
                rel = src_file.relative_to(src).as_posix()
                _remove_file(dst / rel, rel, result)

    return result


def _copy_file(src: Path, dst: Path, rel: str, result: SyncResult) -> None:
    """Copy a single file, updating the SyncResult."""
    if not src.is_file():
        result.skipped.append(rel)
        return
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        result.copied.append(rel)
    except OSError as e:
        result.errors.append(f"{rel}: {e}")


def _remove_file(dst: Path, rel: str, result: SyncResult) -> None:
    """Remove a single file, updating the SyncResult."""
    if dst.is_file():
        try:
            dst.unlink()
            result.removed.append(rel)
        except OSError as e:
            result.errors.append(f"{rel}: {e}")
    else:
        result.skipped.append(rel)

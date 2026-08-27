"""Backup and restore operations for rhdh-customizations/.

Creates timestamped tar.gz archives and supports listing,
previewing, and restoring from backups.
"""

from __future__ import annotations

import re
import tarfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .sync import SyncResult

DEFAULT_BACKUP_DIR = Path.home() / "rhdh-local-backups"


@dataclass
class BackupInfo:
    """Information about a backup archive."""

    path: Path
    timestamp: str
    size_bytes: int


def backup_customizations(
    workspace: Path,
    backup_dir: Optional[Path] = None,
) -> BackupInfo:
    """Create a timestamped tar.gz archive of rhdh-customizations/.

    Args:
        workspace: Path to rhdh-local-setup workspace root.
        backup_dir: Where to store backups (default: ~/rhdh-local-backups/).

    Returns:
        BackupInfo with path, timestamp, and size.

    Raises:
        FileNotFoundError: If rhdh-customizations/ doesn't exist.
    """
    if backup_dir is None:
        backup_dir = DEFAULT_BACKUP_DIR

    customizations = workspace / "rhdh-customizations"
    if not customizations.is_dir():
        raise FileNotFoundError(f"rhdh-customizations not found: {customizations}")

    backup_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f"rhdh-customizations-backup_{ts}.tar.gz"
    archive_path = backup_dir / archive_name

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(customizations, arcname="rhdh-customizations")

    return BackupInfo(
        path=archive_path,
        timestamp=ts,
        size_bytes=archive_path.stat().st_size,
    )


def list_backups(backup_dir: Optional[Path] = None) -> list[BackupInfo]:
    """List available backup archives, newest first."""
    if backup_dir is None:
        backup_dir = DEFAULT_BACKUP_DIR

    if not backup_dir.is_dir():
        return []

    backups = []
    for f in sorted(backup_dir.glob("rhdh-customizations-backup_*.tar.gz"), reverse=True):
        # Extract timestamp from filename
        m = re.search(r"backup_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", f.name)
        ts = m.group(1) if m else "unknown"
        backups.append(
            BackupInfo(
                path=f,
                timestamp=ts,
                size_bytes=f.stat().st_size,
            )
        )

    return backups


def preview_restore(archive: Path) -> list[str]:
    """List files that would be extracted from a backup archive.

    Returns:
        List of relative paths in the archive.
    """
    if not archive.is_file():
        raise FileNotFoundError(f"Archive not found: {archive}")

    with tarfile.open(archive, "r:gz") as tar:
        return [m.name for m in tar.getmembers() if m.isfile()]


def restore_customizations(
    workspace: Path,
    archive: Path,
) -> SyncResult:
    """Extract backup archive into the workspace.

    Extracts rhdh-customizations/ from the archive, overwriting existing files.

    Args:
        workspace: Path to rhdh-local-setup workspace root.
        archive: Path to the backup .tar.gz file.

    Returns:
        SyncResult with extracted files listed in 'copied'.
    """
    result = SyncResult()

    if not archive.is_file():
        result.errors.append(f"Archive not found: {archive}")
        return result

    workspace_root = workspace.resolve()

    try:
        with tarfile.open(archive, "r:gz") as tar:
            # Security: allow only regular files/directories whose final
            # extraction path stays within the target workspace.
            members = []
            for m in tar.getmembers():
                member_path = Path(m.name)

                if member_path.is_absolute() or ".." in member_path.parts:
                    result.errors.append(f"Skipping unsafe path: {m.name}")
                    continue

                if m.issym() or m.islnk():
                    result.errors.append(f"Skipping unsupported link entry: {m.name}")
                    continue

                if not (m.isdir() or m.isfile()):
                    result.errors.append(f"Skipping unsupported archive entry: {m.name}")
                    continue

                destination = (workspace_root / member_path).resolve()
                try:
                    destination.relative_to(workspace_root)
                except ValueError:
                    result.errors.append(f"Skipping unsafe path: {m.name}")
                    continue

                members.append(m)

            for m in members:
                tar.extract(m, path=workspace_root)
            result.copied = [m.name for m in members if m.isfile()]
    except (tarfile.TarError, OSError) as e:
        result.errors.append(str(e))

    return result

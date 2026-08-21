"""Workspace operations for the overlay repository.

Handles listing, querying, and inspecting plugin workspaces in
rhdh-plugin-export-overlays.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .config import get_overlay_repo


@dataclass
class WorkspaceInfo:
    """Information about a plugin workspace."""

    name: str
    path: Path
    repo: Optional[str] = None
    repo_ref: Optional[str] = None
    repo_backstage_version: Optional[str] = None
    has_source_json: bool = False
    has_plugins_list: bool = False
    has_backstage_json: bool = False
    metadata_files: list[str] | None = None

    @classmethod
    def from_path(cls, path: Path) -> "WorkspaceInfo":
        """Create WorkspaceInfo from a workspace directory path."""
        name = path.name

        # Check which files exist
        has_source_json = (path / "source.json").exists()
        has_plugins_list = (path / "plugins-list.yaml").exists()
        has_backstage_json = (path / "backstage.json").exists()

        # Parse source.json if it exists
        repo = None
        repo_ref = None
        repo_backstage_version = None

        if has_source_json:
            try:
                source = json.loads((path / "source.json").read_text())
                repo = source.get("repo")
                repo_ref = source.get("repo-ref")
                repo_backstage_version = source.get("repo-backstage-version")
            except (json.JSONDecodeError, OSError):
                pass

        # List metadata files
        metadata_files = None
        metadata_dir = path / "metadata"
        if metadata_dir.is_dir():
            metadata_files = [f.name for f in metadata_dir.iterdir() if f.is_file()]

        return cls(
            name=name,
            path=path,
            repo=repo,
            repo_ref=repo_ref,
            repo_backstage_version=repo_backstage_version,
            has_source_json=has_source_json,
            has_plugins_list=has_plugins_list,
            has_backstage_json=has_backstage_json,
            metadata_files=metadata_files,
        )


def list_workspaces() -> tuple[Optional[Path], list[WorkspaceInfo]]:
    """List all plugin workspaces in the overlay repo.

    Returns:
        Tuple of (overlay_repo_path or None, list of WorkspaceInfo)
    """
    overlay_repo = get_overlay_repo()
    if overlay_repo is None:
        return None, []

    workspaces_dir = overlay_repo / "workspaces"
    if not workspaces_dir.is_dir():
        return overlay_repo, []

    workspaces = []
    for workspace_path in sorted(workspaces_dir.iterdir()):
        if workspace_path.is_dir():
            workspaces.append(WorkspaceInfo.from_path(workspace_path))

    return overlay_repo, workspaces


def get_workspace(name: str) -> tuple[bool, Optional[WorkspaceInfo], str]:
    """Get a specific workspace by name.

    Args:
        name: Workspace name (directory name)

    Returns:
        Tuple of (found: bool, workspace: WorkspaceInfo or None, error_message: str)
    """
    overlay_repo = get_overlay_repo()
    if overlay_repo is None:
        return False, None, "Overlay repo not found"

    workspace_path = overlay_repo / "workspaces" / name
    if not workspace_path.is_dir():
        return False, None, f"Workspace not found: {name}"

    return True, WorkspaceInfo.from_path(workspace_path), ""

#!/usr/bin/env python3
"""Normalize all marketplace packages to the flat GitHub Copilot plugin layout."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from _layout import MARKETPLACE_PATH, PLUGIN_ROOT, PLUGIN_SOURCES_PATH, REPO_ROOT
    from _plugin_sources import (
        extract_source_manifest,
        load_source_manifest,
        render_json,
        validate_source_manifest,
    )
    from validate_primitives import OPEN_PLUGIN_SCHEMA, PLUGIN_MANIFESTS
except ModuleNotFoundError:  # pragma: no cover
    from ._layout import MARKETPLACE_PATH, PLUGIN_ROOT, PLUGIN_SOURCES_PATH, REPO_ROOT
    from ._plugin_sources import (
        extract_source_manifest,
        load_source_manifest,
        render_json,
        validate_source_manifest,
    )
    from .validate_primitives import OPEN_PLUGIN_SCHEMA, PLUGIN_MANIFESTS

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(.*)$")
METADATA_KEYS = (
    "name",
    "description",
    "version",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "category",
    "tags",
    "postInstallMessage",
)


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def manifest_path(plugin_dir: Path) -> Path | None:
    for relative in PLUGIN_MANIFESTS:
        candidate = plugin_dir / relative
        if candidate.is_file():
            return candidate
    return None


def bump_patch(version: Any) -> str:
    if not isinstance(version, str):
        return "1.0.0"
    match = SEMVER.fullmatch(version)
    if match is None:
        return version
    major, minor, patch, suffix = match.groups()
    return f"{major}.{minor}.{int(patch) + 1}{suffix}"


def stripped_ref(ref: str) -> str:
    return ref.removeprefix("./")


def plugin_owned_agents(plugin_dir: Path) -> bool:
    return any((plugin_dir / "agents").glob("*.agent.md"))


def plugin_owned_skills(plugin_dir: Path) -> bool:
    skills = plugin_dir / "skills"
    return skills.is_dir() and any(
        path.is_dir() and (path / "SKILL.md").is_file()
        for path in skills.iterdir()
    )


def normalize_manifest(
    plugin_dir: Path,
    data: dict[str, Any],
    source: dict[str, Any],
) -> dict[str, Any]:
    migrating = (
        data.get("$schema") == OPEN_PLUGIN_SCHEMA
        or isinstance(data.get("extensions"), dict)
    )
    normalized = {
        key: data[key]
        for key in METADATA_KEYS
        if key in data
    }
    if migrating:
        normalized["version"] = bump_patch(normalized.get("version"))

    component_source = source.get("componentSource")
    has_agents = bool(source.get("agents")) if component_source == "library" else plugin_owned_agents(plugin_dir)
    has_skills = (
        bool(source.get("skills"))
        if component_source == "library"
        else plugin_owned_skills(plugin_dir) or bool(source.get("sharedSkills"))
    )
    if has_agents:
        normalized["agents"] = "agents/"
    if has_skills:
        normalized["skills"] = "skills/"

    hook_source = source.get("hookSource")
    if isinstance(hook_source, str):
        normalized["hooks"] = stripped_ref(hook_source)

    extension_sources = source.get("extensionSources", [])
    if extension_sources:
        normalized["extensions"] = [
            stripped_ref(ref)
            for ref in extension_sources
            if isinstance(ref, str)
        ]

    if (plugin_dir / "mcp.json").is_file():
        normalized["mcpServers"] = "mcp.json"
    return normalized


def normalize_marketplace(
    marketplace: dict[str, Any],
    manifests: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        raise ValueError(f"{MARKETPLACE_PATH}: plugins must be a list")
    normalized = dict(marketplace)
    normalized_plugins: list[dict[str, Any]] = []
    for entry in plugins:
        if not isinstance(entry, dict):
            raise ValueError(f"{MARKETPLACE_PATH}: plugin entries must be objects")
        name = entry.get("name")
        manifest = manifests.get(name) if isinstance(name, str) else None
        updated = dict(entry)
        if manifest is not None:
            updated["description"] = manifest.get(
                "description", updated.get("description", "")
            )
            updated["version"] = manifest.get(
                "version", updated.get("version", "1.0.0")
            )
        normalized_plugins.append(updated)
    normalized["plugins"] = normalized_plugins
    return normalized


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Normalize marketplace packages to direct plugin-root components."
    )
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)

    source_manifest = (
        load_source_manifest()
        if PLUGIN_SOURCES_PATH.is_file()
        else extract_source_manifest()
    )
    validate_source_manifest(source_manifest)
    source_plugins = source_manifest["plugins"]

    drift: list[str] = []
    writes: list[tuple[Path, str]] = []
    normalized_manifests: dict[str, dict[str, Any]] = {}

    rendered_sources = render_json(source_manifest)
    if (
        not PLUGIN_SOURCES_PATH.is_file()
        or PLUGIN_SOURCES_PATH.read_text(encoding="utf-8") != rendered_sources
    ):
        drift.append(PLUGIN_SOURCES_PATH.relative_to(REPO_ROOT).as_posix())
        writes.append((PLUGIN_SOURCES_PATH, rendered_sources))

    plugin_dirs = sorted(
        (path for path in PLUGIN_ROOT.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    )
    manifest_names = {
        plugin_dir.name
        for plugin_dir in plugin_dirs
        if manifest_path(plugin_dir) is not None
    }
    if set(source_plugins) != manifest_names:
        missing = sorted(manifest_names - set(source_plugins))
        extra = sorted(set(source_plugins) - manifest_names)
        raise ValueError(
            f"plugin source metadata mismatch; missing={missing}, extra={extra}"
        )

    for plugin_dir in plugin_dirs:
        path = manifest_path(plugin_dir)
        if path is None:
            continue
        original = read_json(path)
        normalized = normalize_manifest(
            plugin_dir,
            original,
            source_plugins[plugin_dir.name],
        )
        name = normalized.get("name")
        if not isinstance(name, str):
            raise ValueError(f"{path}: plugin name is required")
        normalized_manifests[name] = normalized
        rendered = render_json(normalized)
        if path.read_text(encoding="utf-8") != rendered:
            drift.append(path.relative_to(REPO_ROOT).as_posix())
            writes.append((path, rendered))

    marketplace = read_json(MARKETPLACE_PATH)
    normalized_marketplace = normalize_marketplace(
        marketplace, normalized_manifests
    )
    rendered_marketplace = render_json(normalized_marketplace)
    if MARKETPLACE_PATH.read_text(encoding="utf-8") != rendered_marketplace:
        drift.append(MARKETPLACE_PATH.relative_to(REPO_ROOT).as_posix())
        writes.append((MARKETPLACE_PATH, rendered_marketplace))

    if args.check:
        if drift:
            print("Plugin manifests require flat-layout normalization:", file=sys.stderr)
            for path in drift:
                print(f"  - {path}", file=sys.stderr)
            return 1
        return 0

    for path, rendered in writes:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    print(f"Normalized {len(normalized_manifests)} flat plugin manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

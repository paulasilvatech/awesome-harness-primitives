#!/usr/bin/env python3
"""Normalize shared-library plugin packages to Agent Plugins 1.0 layout."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from validate_primitives import OPEN_PLUGIN_SCHEMA, PLUGIN_MANIFESTS, find_repo_root
except ModuleNotFoundError:  # pragma: no cover
    from .validate_primitives import OPEN_PLUGIN_SCHEMA, PLUGIN_MANIFESTS, find_repo_root

REPO_ROOT = find_repo_root(Path(__file__).resolve())
LIBRARY_ROOT = REPO_ROOT / "library"
PLUGIN_ROOT = LIBRARY_ROOT / "plugins"
MARKETPLACE_PATH = REPO_ROOT / ".github" / "plugin" / "marketplace.json"
REPOSITORY_EXTENSION = "com.paulasilvatech.copilot-primitives"
LAYOUT_VERSION = 1
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(.*)$")
OPEN_KEYS = (
    "$schema",
    "name",
    "description",
    "version",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
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


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def component_refs(data: dict[str, Any], prefix: str) -> list[str]:
    return sorted(
        {
            value
            for value in iter_strings(data)
            if value.startswith(prefix)
        }
    )


def bump_patch(version: Any) -> str:
    if not isinstance(version, str):
        return "1.0.0"
    match = SEMVER.fullmatch(version)
    if match is None:
        return version
    major, minor, patch, suffix = match.groups()
    return f"{major}.{minor}.{int(patch) + 1}{suffix}"


def normalize_manifest(
    plugin_dir: Path,
    data: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    agents = component_refs(data, "./agents/")
    skills = component_refs(data, "./skills/")
    if not agents and not skills:
        return data, False

    for ref in (*agents, *skills):
        source = LIBRARY_ROOT / ref[2:].rstrip("/")
        if not source.exists():
            raise ValueError(f"{plugin_dir.name}: canonical component source not found: {source}")

    extensions = data.get("extensions")
    if not isinstance(extensions, dict):
        extensions = {}
    extensions = dict(extensions)
    extensions.pop("com.github.awesome-copilot", None)
    extensions.setdefault("com.github.copilot", {})
    if not isinstance(extensions["com.github.copilot"], dict):
        raise ValueError(f"{plugin_dir.name}: extensions.com.github.copilot must be an object")

    repository_config = extensions.get(REPOSITORY_EXTENSION)
    if not isinstance(repository_config, dict):
        repository_config = {}
    repository_config = dict(repository_config)
    already_normalized = (
        repository_config.get("componentSource") == "library"
        and repository_config.get("layoutVersion") == LAYOUT_VERSION
    )
    repository_config.update(
        {
            "componentSource": "library",
            "layoutVersion": LAYOUT_VERSION,
            "agents": agents,
            "skills": skills,
        }
    )
    extensions[REPOSITORY_EXTENSION] = repository_config

    normalized: dict[str, Any] = {}
    for key in OPEN_KEYS:
        if key == "$schema":
            normalized[key] = OPEN_PLUGIN_SCHEMA
        elif key == "extensions":
            normalized[key] = extensions
        elif key in data:
            normalized[key] = data[key]
    if not already_normalized:
        normalized["version"] = bump_patch(normalized.get("version"))
    return normalized, True


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
        if manifest is None:
            normalized_plugins.append(entry)
            continue
        updated = dict(entry)
        updated["description"] = manifest.get("description", updated.get("description", ""))
        updated["version"] = manifest.get("version", updated.get("version", "1.0.0"))
        normalized_plugins.append(updated)
    normalized["plugins"] = normalized_plugins
    return normalized


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Normalize shared-library plugins to strict Agent Plugins 1.0 manifests."
    )
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)

    drift: list[str] = []
    normalized_manifests: dict[str, dict[str, Any]] = {}
    writes: list[tuple[Path, str]] = []

    for plugin_dir in sorted(
        (path for path in PLUGIN_ROOT.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    ):
        path = manifest_path(plugin_dir)
        if path is None:
            continue
        original = read_json(path)
        normalized, managed = normalize_manifest(plugin_dir, original)
        if not managed:
            continue
        name = normalized.get("name")
        if not isinstance(name, str):
            raise ValueError(f"{path}: plugin name is required")
        normalized_manifests[name] = normalized
        rendered = render_json(normalized)
        if path.read_text(encoding="utf-8") != rendered:
            drift.append(path.relative_to(REPO_ROOT).as_posix())
            writes.append((path, rendered))

    marketplace = read_json(MARKETPLACE_PATH)
    normalized_marketplace = normalize_marketplace(marketplace, normalized_manifests)
    rendered_marketplace = render_json(normalized_marketplace)
    if MARKETPLACE_PATH.read_text(encoding="utf-8") != rendered_marketplace:
        drift.append(MARKETPLACE_PATH.relative_to(REPO_ROOT).as_posix())
        writes.append((MARKETPLACE_PATH, rendered_marketplace))

    if args.check:
        if drift:
            print("Plugin manifests require normalization:", file=sys.stderr)
            for path in drift:
                print(f"  - {path}", file=sys.stderr)
            return 1
        return 0

    for path, rendered in writes:
        path.write_text(rendered, encoding="utf-8")
    print(f"Normalized {len(normalized_manifests)} shared-library plugin manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Import and materialize current Awesome Copilot client extensions."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

try:
    from _layout import MARKETPLACE_PATH, PLUGIN_ROOT, PLUGIN_SOURCES_PATH
    from _plugin_sources import load_source_manifest, render_json
except ModuleNotFoundError:  # pragma: no cover
    from ._layout import MARKETPLACE_PATH, PLUGIN_ROOT, PLUGIN_SOURCES_PATH
    from ._plugin_sources import load_source_manifest, render_json
AWESOME_NAMESPACE = "com.github.awesome-copilot"
COPILOT_NAMESPACE = "com.github.copilot"
UPSTREAM_REPOSITORY = "https://github.com/github/awesome-copilot"
EXTENSION_LAYOUT_VERSION = 1
COPILOT_SDK_VERSION = "1.0.11-preview.2"
PLAYWRIGHT_VERSION = "1.62.1"
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(.*)$")


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def git_output(source: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(source), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def verify_source(source: Path) -> str:
    if not (source / ".git").exists():
        raise ValueError(f"upstream source is not a Git checkout: {source}")
    remote = git_output(source, "remote", "get-url", "origin")
    if "github/awesome-copilot" not in remote:
        raise ValueError(f"unexpected upstream repository: {remote}")
    if git_output(source, "status", "--porcelain"):
        raise ValueError("upstream checkout must be clean")
    return git_output(source, "rev-parse", "HEAD")


def bump_patch(version: Any) -> str:
    if not isinstance(version, str):
        return "1.0.0"
    match = SEMVER.fullmatch(version)
    if match is None:
        return version
    major, minor, patch, suffix = match.groups()
    return f"{major}.{minor}.{int(patch) + 1}{suffix}"


def extension_names(upstream: Path, plugin_name: str, manifest: dict[str, Any]) -> list[str]:
    extensions = manifest.get("extensions")
    awesome = extensions.get(AWESOME_NAMESPACE) if isinstance(extensions, dict) else None
    refs = awesome.get("extensions", []) if isinstance(awesome, dict) else []
    if not isinstance(refs, list) or not all(
        isinstance(ref, str) and ref.startswith("./extensions/") for ref in refs
    ):
        raise ValueError(f"{plugin_name}: invalid Awesome Copilot extension references")
    names = {
        ref.removeprefix("./extensions/").rstrip("/")
        for ref in refs
    }
    if (upstream / "extensions" / plugin_name / "extension.mjs").is_file():
        names.add(plugin_name)
    return sorted(names)


def pin_package_dependencies(extension_dir: Path) -> None:
    package_path = extension_dir / "package.json"
    if not package_path.is_file():
        return
    package = read_json(package_path)
    dependencies = package.get("dependencies")
    if not isinstance(dependencies, dict):
        return
    dependencies = dict(dependencies)
    if "@github/copilot-sdk" in dependencies:
        dependencies["@github/copilot-sdk"] = COPILOT_SDK_VERSION
    if "playwright" in dependencies:
        dependencies["playwright"] = PLAYWRIGHT_VERSION
    package["dependencies"] = dependencies
    package_path.write_text(render_json(package), encoding="utf-8")


def import_extensions(
    source: Path,
    commit: str,
    source_manifest: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    plugin_sources = source_manifest["plugins"]
    upstream_plugins = source / "plugins"
    for upstream_dir in sorted(
        (path for path in upstream_plugins.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    ):
        upstream_manifest_path = upstream_dir / "plugin.json"
        local_manifest_path = PLUGIN_ROOT / upstream_dir.name / "plugin.json"
        if not upstream_manifest_path.is_file() or not local_manifest_path.is_file():
            continue
        upstream_manifest = read_json(upstream_manifest_path)
        names = extension_names(source, upstream_dir.name, upstream_manifest)
        if not names:
            continue

        local_plugin = local_manifest_path.parent
        canonical_root = local_plugin / "extensions"
        for name in names:
            upstream_extension = source / "extensions" / name
            if not upstream_extension.is_dir():
                raise ValueError(f"{upstream_dir.name}: extension source not found: {name}")
            destination = canonical_root / name
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(upstream_extension, destination, copy_function=shutil.copy2)
            pin_package_dependencies(destination)

        local_manifest = read_json(local_manifest_path)
        upstream_extensions = upstream_manifest.get("extensions")
        upstream_copilot = (
            upstream_extensions.get(COPILOT_NAMESPACE)
            if isinstance(upstream_extensions, dict)
            else None
        )
        repository = plugin_sources.get(upstream_dir.name)
        if not isinstance(repository, dict):
            raise ValueError(f"{upstream_dir.name}: source metadata is missing")
        already_imported = (
            repository.get("extensionLayoutVersion") == EXTENSION_LAYOUT_VERSION
            and repository.get("upstreamCommit") == commit
        )
        repository.setdefault("componentSource", "plugin")
        repository.update(
            {
                "extensionLayoutVersion": EXTENSION_LAYOUT_VERSION,
                "extensionSources": [f"./extensions/{name}" for name in names],
                "upstreamRepository": UPSTREAM_REPOSITORY,
                "upstreamCommit": commit,
            }
        )
        if isinstance(upstream_copilot, dict) and upstream_copilot:
            repository["client"] = dict(upstream_copilot)
        local_manifest["extensions"] = [
            f"extensions/{name}" for name in names
        ]
        if not already_imported:
            local_manifest["version"] = bump_patch(local_manifest.get("version"))
        local_manifest_path.write_text(render_json(local_manifest), encoding="utf-8")
        manifests[upstream_dir.name] = local_manifest
    return manifests


def update_marketplace(manifests: dict[str, dict[str, Any]]) -> None:
    marketplace = read_json(MARKETPLACE_PATH)
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        raise ValueError("marketplace plugins must be a list")
    by_name = {
        entry["name"]: dict(entry)
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    for name, manifest in manifests.items():
        entry = by_name.get(name, {})
        entry.update(
            {
                "name": name,
                "source": f"./harness/github-copilot/plugins/{name}",
                "description": manifest.get("description", ""),
                "version": manifest.get("version", "1.0.0"),
            }
        )
        by_name[name] = entry
    marketplace["plugins"] = [by_name[name] for name in sorted(by_name, key=str.casefold)]
    MARKETPLACE_PATH.write_text(render_json(marketplace), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Import current Awesome Copilot extension sources into self-contained plugins."
    )
    parser.add_argument("--source", type=Path, required=True, help="clean github/awesome-copilot checkout")
    args = parser.parse_args(argv)

    source = args.source.resolve()
    commit = verify_source(source)
    source_manifest = load_source_manifest()
    manifests = import_extensions(source, commit, source_manifest)
    PLUGIN_SOURCES_PATH.write_text(render_json(source_manifest), encoding="utf-8")
    update_marketplace(manifests)
    print(f"Imported {len(manifests)} extension-backed plugins from {commit}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Canonical source ownership metadata for flat GitHub Copilot plugin packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from _layout import PLUGIN_ROOT, PLUGIN_SOURCES_PATH
except ModuleNotFoundError:  # pragma: no cover
    from ._layout import PLUGIN_ROOT, PLUGIN_SOURCES_PATH

SOURCE_LAYOUT_VERSION = 2
REPOSITORY_EXTENSION = "com.paulasilvatech.copilot-primitives"
COPILOT_EXTENSION = "com.github.copilot"
SOURCE_CONFIG_KEYS = {
    "componentSource",
    "agents",
    "skills",
    "sharedSkills",
    "hookSource",
    "extensionSources",
    "extensionLayoutVersion",
    "upstreamRepository",
    "upstreamCommit",
    "client",
}


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def extract_source_manifest(plugin_root: Path = PLUGIN_ROOT) -> dict[str, Any]:
    """Extract layout-v2 source metadata from the previous schema manifests."""
    plugins: dict[str, dict[str, Any]] = {}
    for plugin_dir in sorted(
        (path for path in plugin_root.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    ):
        manifest_path = plugin_dir / "plugin.json"
        if not manifest_path.is_file():
            continue
        manifest = read_json(manifest_path)
        extensions = manifest.get("extensions")
        if not isinstance(extensions, dict):
            raise ValueError(
                f"{plugin_dir.name}: cannot extract source metadata from a flat manifest"
            )
        repository = extensions.get(REPOSITORY_EXTENSION)
        if not isinstance(repository, dict):
            raise ValueError(f"{plugin_dir.name}: repository source metadata is missing")
        config = {
            key: value
            for key, value in repository.items()
            if key in SOURCE_CONFIG_KEYS and key != "client"
        }
        config.pop("layoutVersion", None)
        client = extensions.get(COPILOT_EXTENSION)
        if isinstance(client, dict) and client:
            config["client"] = client
        plugins[plugin_dir.name] = config
    return {
        "version": SOURCE_LAYOUT_VERSION,
        "plugins": plugins,
    }


def validate_source_manifest(data: dict[str, Any], path: Path = PLUGIN_SOURCES_PATH) -> None:
    if data.get("version") != SOURCE_LAYOUT_VERSION:
        raise ValueError(
            f"{path}: version must equal {SOURCE_LAYOUT_VERSION}"
        )
    plugins = data.get("plugins")
    if not isinstance(plugins, dict):
        raise ValueError(f"{path}: plugins must be an object")
    for name, config in plugins.items():
        if not isinstance(name, str) or not isinstance(config, dict):
            raise ValueError(f"{path}: plugin source entries must map names to objects")
        extra = sorted(set(config) - SOURCE_CONFIG_KEYS)
        if extra:
            raise ValueError(
                f"{path}: {name} has unsupported source keys: {', '.join(extra)}"
            )
        if config.get("componentSource") not in {"library", "plugin"}:
            raise ValueError(
                f"{path}: {name} componentSource must be library or plugin"
            )


def load_source_manifest(path: Path = PLUGIN_SOURCES_PATH) -> dict[str, Any]:
    data = read_json(path)
    validate_source_manifest(data, path)
    return data


def load_plugin_sources(path: Path = PLUGIN_SOURCES_PATH) -> dict[str, dict[str, Any]]:
    return load_source_manifest(path)["plugins"]

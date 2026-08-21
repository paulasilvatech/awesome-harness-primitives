#!/usr/bin/env python3
"""Regenerate shared-source component copies inside plugin packages.

The shared `harness/github-copilot/agents` and `harness/github-copilot/skills` trees are the source of truth.
Marketplace installation currently requires plugin packages to be self-contained,
so plugin manifests may reference generated copies under each plugin directory
(`./agents/...`, `./skills/...`). Do not hand-edit those plugin-local copies;
edit the shared primitive, then run this script.

Self-contained plugins can instead own their components by declaring
`extensions.com.paulasilvatech.copilot-primitives.componentSource` as `plugin`.
Those component directories are canonical package content and this script leaves
them unchanged. When such a package also declares the `com.github.copilot`
extension, canonical `agents/` files are mirrored into the Agent Plugins 1.0
runtime directory `com.github.copilot/agents/`. An optional repository extension
`hookSource` is mirrored to `com.github.copilot/hooks/hooks.json`.
"""
from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from _layout import HARNESS_ROOT
    from validate_primitives import PLUGIN_MANIFESTS
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._layout import HARNESS_ROOT
    from .validate_primitives import PLUGIN_MANIFESTS

REPOSITORY_EXTENSION = "com.paulasilvatech.copilot-primitives"


@dataclass(frozen=True)
class ComponentCopy:
    plugin: str
    ref: str
    source: Path
    target: Path


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} manifest root must be an object")
    return data


def plugin_manifest(plugin_dir: Path) -> Path | None:
    for rel in PLUGIN_MANIFESTS:
        path = plugin_dir / rel
        if path.exists():
            return path
    return None


def iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)


def repository_extension_config(data: dict[str, Any]) -> dict[str, Any]:
    extensions = data.get("extensions")
    if not isinstance(extensions, dict):
        return {}
    repository_config = extensions.get(REPOSITORY_EXTENSION)
    return repository_config if isinstance(repository_config, dict) else {}


def owns_plugin_components(data: dict[str, Any]) -> bool:
    return repository_extension_config(data).get("componentSource") == "plugin"


def shared_skill_refs(data: dict[str, Any]) -> list[str]:
    refs = repository_extension_config(data).get("sharedSkills", [])
    if not isinstance(refs, list):
        raise ValueError("sharedSkills must be a list")
    if not all(
        isinstance(ref, str)
        and ref.startswith("./skills/")
        and ref.endswith("/")
        for ref in refs
    ):
        raise ValueError("sharedSkills must contain ./skills/<name>/ references")
    return refs


def uses_github_extension(data: dict[str, Any]) -> bool:
    extensions = data.get("extensions")
    return isinstance(extensions, dict) and isinstance(
        extensions.get("com.github.copilot"), dict
    )


def resolve_plugin_source(plugin_dir: Path, ref: str) -> Path:
    if not ref.startswith("./"):
        raise ValueError(f"{plugin_dir.name}: component source must start with './': {ref}")
    source = (plugin_dir / ref[2:]).resolve()
    try:
        source.relative_to(plugin_dir.resolve())
    except ValueError as exc:
        raise ValueError(f"{plugin_dir.name}: component source escapes plugin root: {ref}") from exc
    return source


def collect_component_copies(root: Path) -> list[ComponentCopy]:
    plugin_root = root / "plugins"
    copies: list[ComponentCopy] = []
    if not plugin_root.is_dir():
        return copies

    for plugin_dir in sorted((p for p in plugin_root.iterdir() if p.is_dir()), key=lambda p: p.name.casefold()):
        manifest = plugin_manifest(plugin_dir)
        if manifest is None:
            continue
        data = read_json(manifest)
        repository_config = repository_extension_config(data)
        if owns_plugin_components(data):
            extension_agents = plugin_dir / "com.github.copilot" / "agents"
            source_agents = plugin_dir / "agents"
            if source_agents.is_dir() and uses_github_extension(data):
                for source in sorted(source_agents.glob("*.agent.md")):
                    copies.append(
                        ComponentCopy(
                            plugin_dir.name,
                            f"./com.github.copilot/agents/{source.name}",
                            source,
                            extension_agents / source.name,
                        )
                    )
            for ref in shared_skill_refs(data):
                relative = ref[2:].rstrip("/")
                copies.append(
                    ComponentCopy(
                        plugin_dir.name,
                        ref,
                        root / relative,
                        plugin_dir / relative,
                    )
                )
        else:
            refs = {
                ref
                for ref in iter_strings(data)
                if ref.startswith("./agents/") or ref.startswith("./skills/")
            }
            for ref in sorted(refs):
                rel = ref[2:].rstrip("/")
                source = root / rel
                if ref.startswith("./skills/"):
                    copies.append(ComponentCopy(plugin_dir.name, ref, source, plugin_dir / rel))
                if ref.startswith("./agents/") and uses_github_extension(data):
                    copies.append(
                        ComponentCopy(
                            plugin_dir.name,
                            f"./com.github.copilot/agents/{Path(rel).name}",
                            source,
                            plugin_dir / "com.github.copilot" / "agents" / Path(rel).name,
                        )
                    )

        hook_ref = repository_config.get("hookSource")
        if isinstance(hook_ref, str):
            copies.append(
                ComponentCopy(
                    plugin_dir.name,
                    "./com.github.copilot/hooks/hooks.json",
                    resolve_plugin_source(plugin_dir, hook_ref),
                    plugin_dir / "com.github.copilot" / "hooks" / "hooks.json",
                )
            )
        extension_refs = repository_config.get("extensionSources", [])
        if isinstance(extension_refs, list):
            for ref in extension_refs:
                if not isinstance(ref, str):
                    continue
                source = resolve_plugin_source(plugin_dir, ref)
                copies.append(
                    ComponentCopy(
                        plugin_dir.name,
                        f"./com.github.copilot/extensions/{source.name}",
                        source,
                        plugin_dir / "com.github.copilot" / "extensions" / source.name,
                    )
                )
    return copies


def remove_generated_dirs(root: Path) -> None:
    plugin_root = root / "plugins"
    if not plugin_root.is_dir():
        return
    for plugin_dir in plugin_root.iterdir():
        if not plugin_dir.is_dir():
            continue
        manifest = plugin_manifest(plugin_dir)
        if manifest is None:
            continue
        data = read_json(manifest)
        if owns_plugin_components(data):
            for name in ("agents", "hooks", "extensions"):
                extension_path = plugin_dir / "com.github.copilot" / name
                if extension_path.exists():
                    shutil.rmtree(extension_path)
            for ref in shared_skill_refs(data):
                target = plugin_dir / ref[2:].rstrip("/")
                if target.exists():
                    shutil.rmtree(target)
            continue
        for name in ("agents", "skills"):
            path = plugin_dir / name
            if path.exists():
                shutil.rmtree(path)
        extension_agents = plugin_dir / "com.github.copilot" / "agents"
        if extension_agents.exists():
            shutil.rmtree(extension_agents)
        extension_packages = plugin_dir / "com.github.copilot" / "extensions"
        if extension_packages.exists():
            shutil.rmtree(extension_packages)


def copy_component(copy: ComponentCopy) -> None:
    if not copy.source.exists():
        raise FileNotFoundError(f"{copy.plugin}: {copy.ref} source not found: {copy.source}")
    copy.target.parent.mkdir(parents=True, exist_ok=True)
    if copy.source.is_dir():
        shutil.copytree(copy.source, copy.target)
    else:
        shutil.copy2(copy.source, copy.target)


def dircmp_differences(left: Path, right: Path) -> list[str]:
    cmp = filecmp.dircmp(left, right)
    diffs = [str(left / name) for name in cmp.left_only]
    diffs.extend(str(right / name) for name in cmp.right_only)
    diffs.extend(str(left / name) for name in cmp.diff_files)
    diffs.extend(str(left / name) for name in cmp.funny_files)
    for subdir in cmp.common_dirs:
        diffs.extend(dircmp_differences(left / subdir, right / subdir))
    return diffs


def check_component(copy: ComponentCopy) -> list[str]:
    if not copy.source.exists():
        return [f"{copy.plugin}: {copy.ref} source not found: {copy.source}"]
    if not copy.target.exists():
        return [f"{copy.plugin}: {copy.ref} generated copy is missing: {copy.target}"]
    if copy.source.is_dir() != copy.target.is_dir():
        return [f"{copy.plugin}: {copy.ref} source/copy type mismatch"]
    if copy.source.is_dir():
        diffs = dircmp_differences(copy.source, copy.target)
        return [f"{copy.plugin}: {copy.ref} differs at {path}" for path in diffs]
    if not filecmp.cmp(copy.source, copy.target, shallow=False):
        return [f"{copy.plugin}: {copy.ref} differs: {copy.target}"]
    return []


def find_extra_generated_paths(root: Path, copies: list[ComponentCopy]) -> list[Path]:
    expected = {copy.target.resolve() for copy in copies}
    extras: list[Path] = []
    plugin_root = root / "plugins"
    if not plugin_root.is_dir():
        return extras
    for plugin_dir in plugin_root.iterdir():
        if not plugin_dir.is_dir():
            continue
        manifest = plugin_manifest(plugin_dir)
        if manifest is None:
            continue
        if owns_plugin_components(read_json(manifest)):
            extension_root = plugin_dir / "com.github.copilot"
            agents = extension_root / "agents"
            if agents.is_dir():
                for child in agents.glob("*.agent.md"):
                    if child.resolve() not in expected:
                        extras.append(child)
            hook = extension_root / "hooks" / "hooks.json"
            if hook.exists() and hook.resolve() not in expected:
                extras.append(hook)
            extensions = extension_root / "extensions"
            if extensions.is_dir():
                for child in extensions.iterdir():
                    if child.is_dir() and child.resolve() not in expected:
                        extras.append(child)
            continue
        for name in ("agents", "skills"):
            base = plugin_dir / name
            if not base.exists():
                continue
            children = list(base.glob("*.agent.md")) if name == "agents" else [p for p in base.iterdir() if p.is_dir()]
            for child in children:
                if child.resolve() not in expected:
                    extras.append(child)
        extension_agents = plugin_dir / "com.github.copilot" / "agents"
        if extension_agents.is_dir():
            for child in extension_agents.glob("*.agent.md"):
                if child.resolve() not in expected:
                    extras.append(child)
        extension_packages = plugin_dir / "com.github.copilot" / "extensions"
        if extension_packages.is_dir():
            for child in extension_packages.iterdir():
                if child.is_dir() and child.resolve() not in expected:
                    extras.append(child)
    return sorted(extras)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate plugin-local agent and skill copies from shared harness sources.")
    parser.add_argument(
        "--root",
        type=Path,
        default=HARNESS_ROOT,
        help="canonical harness root (default: <repo>/harness/github-copilot)",
    )
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if plugin-local copies are stale; do not write")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    copies = collect_component_copies(root)
    if args.check:
        findings: list[str] = []
        for copy in copies:
            findings.extend(check_component(copy))
        for extra in find_extra_generated_paths(root, copies):
            findings.append(f"unreferenced generated component copy: {extra}")
        if findings:
            print("Plugin component copies are stale; run python3 harness/github-copilot/scripts/sync_plugin_components.py", file=sys.stderr)
            for finding in findings:
                print(f"  - {finding}", file=sys.stderr)
            return 1
        return 0

    remove_generated_dirs(root)
    for copy in copies:
        copy_component(copy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

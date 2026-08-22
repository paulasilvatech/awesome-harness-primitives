#!/usr/bin/env python3
"""Synchronize canonical components into flat GitHub Copilot plugin packages.

Every distributed plugin keeps runtime components directly at its root:
`agents/`, `skills/`, `hooks/`, `extensions/`, and `mcp.json`. The
`com.github.copilot/` directory is prohibited.

Shared source ownership is recorded centrally in
`harness/github-copilot/manifests/plugin-sources.json`. Plugin-owned components
remain canonical inside their package; selected `sharedSkills` are generated
from the shared harness into that package.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from _layout import HARNESS_ROOT
    from _plugin_sources import load_plugin_sources
except ModuleNotFoundError:  # pragma: no cover
    from ._layout import HARNESS_ROOT
    from ._plugin_sources import load_plugin_sources


@dataclass(frozen=True)
class ComponentCopy:
    plugin: str
    ref: str
    source: Path
    target: Path


def refs(config: dict, key: str) -> list[str]:
    value = config.get(key, [])
    if not isinstance(value, list) or not all(isinstance(ref, str) for ref in value):
        raise ValueError(f"{key} must be a list of strings")
    return value


def relative_ref(ref: str, prefix: str, *, directory: bool) -> str:
    if not ref.startswith(prefix):
        raise ValueError(f"component ref must start with {prefix}: {ref}")
    if directory and not ref.endswith("/"):
        raise ValueError(f"directory component ref must end with '/': {ref}")
    if not directory and ref.endswith("/"):
        raise ValueError(f"file component ref must not end with '/': {ref}")
    return ref.removeprefix("./").rstrip("/")


def collect_component_copies(
    root: Path,
    source_map: dict[str, dict],
) -> list[ComponentCopy]:
    plugin_root = root / "plugins"
    copies: list[ComponentCopy] = []
    for plugin_name, config in sorted(source_map.items(), key=lambda item: item[0].casefold()):
        plugin_dir = plugin_root / plugin_name
        if not plugin_dir.is_dir():
            raise FileNotFoundError(f"{plugin_name}: plugin directory is missing")
        source_mode = config.get("componentSource")
        if source_mode == "library":
            for ref in refs(config, "agents"):
                relative = relative_ref(ref, "./agents/", directory=False)
                copies.append(
                    ComponentCopy(
                        plugin_name,
                        ref,
                        root / relative,
                        plugin_dir / relative,
                    )
                )
            for ref in refs(config, "skills"):
                relative = relative_ref(ref, "./skills/", directory=True)
                copies.append(
                    ComponentCopy(
                        plugin_name,
                        ref,
                        root / relative,
                        plugin_dir / relative,
                    )
                )
        elif source_mode == "plugin":
            for ref in refs(config, "sharedSkills"):
                relative = relative_ref(ref, "./skills/", directory=True)
                copies.append(
                    ComponentCopy(
                        plugin_name,
                        ref,
                        root / relative,
                        plugin_dir / relative,
                    )
                )
        else:
            raise ValueError(
                f"{plugin_name}: componentSource must be library or plugin"
            )
    return copies


def remove_generated_paths(root: Path, source_map: dict[str, dict]) -> None:
    plugin_root = root / "plugins"
    for plugin_name, config in source_map.items():
        plugin_dir = plugin_root / plugin_name
        namespace = plugin_dir / "com.github.copilot"
        if namespace.exists():
            shutil.rmtree(namespace)
        if config.get("componentSource") == "library":
            for folder in ("agents", "skills"):
                target = plugin_dir / folder
                if target.exists():
                    shutil.rmtree(target)
            continue
        for ref in refs(config, "sharedSkills"):
            relative = relative_ref(ref, "./skills/", directory=True)
            target = plugin_dir / relative
            if target.exists():
                shutil.rmtree(target)


def copy_component(copy: ComponentCopy) -> None:
    if not copy.source.exists():
        raise FileNotFoundError(
            f"{copy.plugin}: {copy.ref} source not found: {copy.source}"
        )
    copy.target.parent.mkdir(parents=True, exist_ok=True)
    if copy.source.is_dir():
        shutil.copytree(copy.source, copy.target, copy_function=shutil.copy2)
    else:
        shutil.copy2(copy.source, copy.target)


def dircmp_differences(left: Path, right: Path) -> list[str]:
    comparison = filecmp.dircmp(left, right)
    differences = [str(left / name) for name in comparison.left_only]
    differences.extend(str(right / name) for name in comparison.right_only)
    differences.extend(str(left / name) for name in comparison.diff_files)
    differences.extend(str(left / name) for name in comparison.funny_files)
    for subdir in comparison.common_dirs:
        differences.extend(dircmp_differences(left / subdir, right / subdir))
    return differences


def check_component(copy: ComponentCopy) -> list[str]:
    if not copy.source.exists():
        return [f"{copy.plugin}: {copy.ref} source not found: {copy.source}"]
    if not copy.target.exists():
        return [
            f"{copy.plugin}: {copy.ref} generated copy is missing: {copy.target}"
        ]
    if copy.source.is_dir() != copy.target.is_dir():
        return [f"{copy.plugin}: {copy.ref} source/copy type mismatch"]
    if copy.source.is_dir():
        return [
            f"{copy.plugin}: {copy.ref} differs at {path}"
            for path in dircmp_differences(copy.source, copy.target)
        ]
    if not filecmp.cmp(copy.source, copy.target, shallow=False):
        return [f"{copy.plugin}: {copy.ref} differs: {copy.target}"]
    return []


def find_extra_generated_paths(
    root: Path,
    source_map: dict[str, dict],
    copies: list[ComponentCopy],
) -> list[Path]:
    expected = {copy.target.resolve() for copy in copies}
    extras: list[Path] = []
    plugin_root = root / "plugins"
    for plugin_name, config in source_map.items():
        plugin_dir = plugin_root / plugin_name
        namespace = plugin_dir / "com.github.copilot"
        if namespace.exists():
            extras.append(namespace)
        if config.get("componentSource") != "library":
            continue
        for folder in ("agents", "skills"):
            base = plugin_dir / folder
            if not base.is_dir():
                continue
            children = (
                list(base.glob("*.agent.md"))
                if folder == "agents"
                else [path for path in base.iterdir() if path.is_dir()]
            )
            for child in children:
                if child.resolve() not in expected:
                    extras.append(child)
    return sorted(extras)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize direct plugin-root agents and skills."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=HARNESS_ROOT,
        help="canonical harness root (default: <repo>/harness/github-copilot)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if plugin-local copies are stale; do not write",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    source_map = load_plugin_sources()
    copies = collect_component_copies(root, source_map)
    if args.check:
        findings: list[str] = []
        for copy in copies:
            findings.extend(check_component(copy))
        for extra in find_extra_generated_paths(root, source_map, copies):
            findings.append(f"unreferenced generated component copy: {extra}")
        if findings:
            print(
                "Plugin component copies are stale; run "
                "python3 harness/github-copilot/scripts/sync_plugin_components.py",
                file=sys.stderr,
            )
            for finding in findings:
                print(f"  - {finding}", file=sys.stderr)
            return 1
        return 0

    remove_generated_paths(root, source_map)
    for copy in copies:
        copy_component(copy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

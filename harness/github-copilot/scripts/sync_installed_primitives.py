#!/usr/bin/env python3
"""Synchronize declared repository customizations from canonical harness sources."""
from __future__ import annotations

import argparse
import json
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from _layout import INSTALLED_MANIFEST_PATH, REPO_ROOT
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._layout import INSTALLED_MANIFEST_PATH, REPO_ROOT

DEFAULT_MANIFEST = INSTALLED_MANIFEST_PATH
ALLOWED_TARGET_ROOTS = (Path(".github"), Path("docs/templates"))
SUPPORTED_MODES = {"copy", "strip-frontmatter"}
IGNORED_SOURCE_NAMES = {"__pycache__", ".DS_Store"}


@dataclass(frozen=True)
class InstalledCopy:
    source: Path
    target: Path
    mode: str


def read_manifest(path: Path, repo_root: Path) -> list[InstalledCopy]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError(f"{path}: manifest root must be an object with version 1")
    raw_copies = data.get("copies")
    if not isinstance(raw_copies, list):
        raise ValueError(f"{path}: copies must be a list")

    copies: list[InstalledCopy] = []
    seen_targets: set[Path] = set()
    for index, raw in enumerate(raw_copies):
        if not isinstance(raw, dict):
            raise ValueError(f"{path}: copies[{index}] must be an object")
        source_value = raw.get("source")
        target_value = raw.get("target")
        mode = raw.get("mode", "copy")
        if not isinstance(source_value, str) or not source_value:
            raise ValueError(f"{path}: copies[{index}].source must be a non-empty string")
        if not isinstance(target_value, str) or not target_value:
            raise ValueError(f"{path}: copies[{index}].target must be a non-empty string")
        if mode not in SUPPORTED_MODES:
            raise ValueError(f"{path}: copies[{index}].mode must be one of {sorted(SUPPORTED_MODES)}")

        source_rel = safe_relative_path(source_value, f"copies[{index}].source")
        target_rel = safe_relative_path(target_value, f"copies[{index}].target")
        if not is_within(target_rel, ALLOWED_TARGET_ROOTS):
            raise ValueError(
                f"{path}: target must be under .github/ or docs/templates/: {target_rel}"
            )

        source = (repo_root / source_rel).resolve()
        target = (repo_root / target_rel).resolve()
        ensure_inside(repo_root, source, f"copies[{index}].source")
        ensure_inside(repo_root, target, f"copies[{index}].target")
        if target in seen_targets:
            raise ValueError(f"{path}: duplicate target: {target_rel}")
        if source == target:
            raise ValueError(f"{path}: source and target must differ: {source_rel}")
        if mode == "strip-frontmatter" and source.is_dir():
            raise ValueError(f"{path}: strip-frontmatter requires a file source: {source_rel}")

        seen_targets.add(target)
        copies.append(InstalledCopy(source, target, mode))
    return copies


def safe_relative_path(value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"{label} must be a repository-relative path without '..': {value}")
    return path


def is_within(path: Path, roots: tuple[Path, ...]) -> bool:
    return any(path == root or root in path.parents for root in roots)


def ensure_inside(repo_root: Path, path: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"{label} resolves outside the repository: {path}") from exc


def strip_frontmatter(text: str, source: Path) -> str:
    if not text.startswith("---\n"):
        raise ValueError(f"{source}: strip-frontmatter source must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{source}: frontmatter closing delimiter not found")
    body = text[end + len("\n---\n"):].lstrip("\n")
    if not body.strip():
        raise ValueError(f"{source}: strip-frontmatter source has an empty body")
    return body


def expected_file_bytes(copy: InstalledCopy) -> bytes:
    if copy.mode == "strip-frontmatter":
        text = copy.source.read_text(encoding="utf-8")
        return strip_frontmatter(text, copy.source).encode("utf-8")
    return copy.source.read_bytes()


def ignored_source_path(path: Path) -> bool:
    return any(part in IGNORED_SOURCE_NAMES for part in path.parts) or path.suffix == ".pyc"


def directory_entries(root: Path, *, ignore_generated: bool) -> dict[Path, Path]:
    entries: dict[Path, Path] = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ignore_generated and ignored_source_path(relative):
            continue
        entries[relative] = path
    return entries


def executable_bits(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode) & 0o111


def directory_differences(source: Path, target: Path) -> list[str]:
    source_entries = directory_entries(source, ignore_generated=True)
    target_entries = directory_entries(target, ignore_generated=False)
    findings = [
        f"missing from target: {source / relative}"
        for relative in sorted(set(source_entries) - set(target_entries))
    ]
    findings.extend(
        f"unexpected target path: {target / relative}"
        for relative in sorted(set(target_entries) - set(source_entries))
    )
    for relative in sorted(set(source_entries).intersection(target_entries)):
        source_path = source_entries[relative]
        target_path = target_entries[relative]
        if source_path.is_dir() != target_path.is_dir():
            findings.append(f"source/copy type mismatch: {target_path}")
            continue
        if source_path.is_file() != target_path.is_file():
            findings.append(f"source/copy type mismatch: {target_path}")
            continue
        if source_path.is_file():
            if source_path.read_bytes() != target_path.read_bytes():
                findings.append(f"content differs: {target_path}")
            if executable_bits(source_path) != executable_bits(target_path):
                findings.append(f"executable mode differs: {target_path}")
    return findings


def check_copy(copy: InstalledCopy) -> list[str]:
    if not copy.source.exists():
        return [f"source is missing: {copy.source}"]
    if not copy.target.exists():
        return [f"installed copy is missing: {copy.target}"]
    if copy.source.is_dir() != copy.target.is_dir():
        return [f"source/copy type mismatch: {copy.target}"]
    if copy.source.is_dir():
        if copy.mode != "copy":
            return [f"directory copy uses unsupported mode {copy.mode}: {copy.source}"]
        return directory_differences(copy.source, copy.target)
    findings = []
    if copy.target.read_bytes() != expected_file_bytes(copy):
        findings.append(f"content differs: {copy.target}")
    if executable_bits(copy.source) != executable_bits(copy.target):
        findings.append(f"executable mode differs: {copy.target}")
    return findings


def remove_target(target: Path) -> None:
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()


def synchronize(copy: InstalledCopy) -> None:
    if not copy.source.exists():
        raise FileNotFoundError(f"source is missing: {copy.source}")
    remove_target(copy.target)
    copy.target.parent.mkdir(parents=True, exist_ok=True)
    if copy.source.is_dir():
        if copy.mode != "copy":
            raise ValueError(f"directory copy uses unsupported mode {copy.mode}: {copy.source}")
        shutil.copytree(
            copy.source,
            copy.target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
    else:
        copy.target.write_bytes(expected_file_bytes(copy))
        shutil.copymode(copy.source, copy.target)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize declared .github and compatibility copies from canonical sources."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="copy manifest (default: harness/github-copilot/manifests/installed-primitives.json)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if a declared installed copy is stale; do not write",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = args.manifest.resolve()
    try:
        copies = read_manifest(manifest, REPO_ROOT)
        if args.check:
            findings = [
                finding
                for copy in copies
                for finding in check_copy(copy)
            ]
            if findings:
                print(
                    "Installed primitive copies are stale; run "
                    "python3 harness/github-copilot/scripts/sync_installed_primitives.py",
                    file=sys.stderr,
                )
                for finding in findings:
                    print(f"  - {finding}", file=sys.stderr)
                return 1
            return 0

        for copy in copies:
            synchronize(copy)
        print(f"Synchronized {len(copies)} installed primitive copies.")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"sync_installed_primitives.py: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

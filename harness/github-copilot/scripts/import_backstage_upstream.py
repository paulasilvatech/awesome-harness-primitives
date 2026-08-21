#!/usr/bin/env python3
"""Deterministically import allow-listed Backstage upstream references.

This importer feeds the (not-yet-authored) ``backstage-expert`` plugin. It
owns exactly the license/provenance/upstream-snapshot files copied verbatim
from a pinned, offline ``backstage/backstage`` checkout:

- Six official Backstage skill guides under
  ``docs/.well-known/skills/<name>/SKILL.md`` are copied to
  ``skills/<name>/references/upstream/SKILL.md``.
- The optional skills index ``docs/.well-known/skills/index.md`` (if present)
  is copied to ``references/upstream/skills-index.md``.
- The catalog database performance battery guide
  ``.claude/skills/catalog-db-performance.md`` is copied to
  ``skills/backstage-catalog-db-performance/references/upstream/catalog-db-performance.md``.
- The upstream ``LICENSE`` is copied to the plugin root.
- The upstream ``NOTICE`` is copied to the plugin root when present; when the
  pinned commit has no ``NOTICE`` file this script instead writes a
  deterministic *local* NOTICE that clearly identifies itself as generated
  (never as upstream content).
- A deterministic ``PROVENANCE.json`` records the source path, destination,
  SHA-256, source repository, commit, import date, and license for every
  imported file.

This script does not create a plugin manifest, agent, prompt, hook, or any
other plugin content; those remain out of scope until the ``backstage-expert``
plugin is authored separately.

Usage:
    python3 harness/github-copilot/scripts/import_backstage_upstream.py \
        --source /path/to/backstage-upstream-checkout
    python3 harness/github-copilot/scripts/import_backstage_upstream.py \
        --source /path/to/backstage-upstream-checkout --check
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from _layout import PLUGIN_ROOT
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._layout import PLUGIN_ROOT

SCRIPT_RELATIVE_PATH = "harness/github-copilot/scripts/import_backstage_upstream.py"
PLUGIN_NAME = "backstage-expert"
UPSTREAM_REPOSITORY = "https://github.com/backstage/backstage"
EXPECTED_COMMIT = "eeac444a9aba7c107525d2a726851e907418c181"
IMPORT_DATE = "2026-08-21"
LICENSE_ID = "Apache-2.0"
PROVENANCE_FILENAME = "PROVENANCE.json"

SKILL_NAMES = (
    "app-frontend-system-migration",
    "plugin-new-frontend-system-support",
    "plugin-full-frontend-system-migration",
    "mui-to-bui-migration",
    "plugin-analytics-instrumentation",
    "onboard-to-openapi-server",
)
PERFORMANCE_SNAPSHOT_SKILL = "backstage-catalog-db-performance"


@dataclass(frozen=True)
class Entry:
    """One allow-listed file the importer owns end to end."""

    source_rel: PurePosixPath | None  # None only for a generated fallback (missing upstream NOTICE)
    dest_rel: PurePosixPath
    data: bytes
    origin: str  # "upstream" or "generated"


class ImportError_(ValueError):
    """Raised for any verification or allow-list failure."""


def git_output(source: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(source), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def normalize_repo_url(url: str) -> str:
    url = url.strip()
    if url.startswith("git+"):
        url = url[len("git+") :]
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url[len("git@github.com:") :]
    if url.endswith(".git"):
        url = url[: -len(".git")]
    return url.rstrip("/")


def verify_commit(source: Path, expected_commit: str) -> str:
    if not (source / ".git").exists():
        raise ImportError_(f"upstream source is not a Git checkout: {source}")
    head = git_output(source, "rev-parse", "HEAD")
    if head != expected_commit:
        raise ImportError_(f"unexpected upstream commit: {head} (expected {expected_commit})")
    status = git_output(source, "status", "--porcelain")
    if status:
        raise ImportError_("upstream checkout must be clean (uncommitted changes found)")
    return head


def verify_repository_identity(source: Path, expected_repository: str) -> None:
    package_path = source / "package.json"
    if not package_path.is_file():
        raise ImportError_("upstream package.json not found; cannot verify repository identity")
    try:
        data: Any = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ImportError_(f"upstream package.json is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ImportError_("upstream package.json root must be an object")
    repository = data.get("repository")
    url: Any = None
    if isinstance(repository, str):
        url = repository
    elif isinstance(repository, dict):
        url = repository.get("url")
    if not isinstance(url, str) or not url.strip():
        raise ImportError_("upstream package.json is missing repository.url")
    if normalize_repo_url(url) != expected_repository:
        raise ImportError_(f"unexpected upstream repository: {url} (expected {expected_repository})")


def verify_license(source: Path) -> str:
    license_path = source / "LICENSE"
    if not license_path.is_file():
        raise ImportError_("upstream LICENSE not found")
    text = license_path.read_text(encoding="utf-8", errors="replace")
    if "Apache License" not in text or "Version 2.0" not in text:
        raise ImportError_("upstream LICENSE is not Apache License, Version 2.0")
    return LICENSE_ID


def verify_source(source: Path) -> None:
    """Verify repo identity, pinned commit, and Apache-2.0 license."""
    verify_commit(source, EXPECTED_COMMIT)
    verify_repository_identity(source, UPSTREAM_REPOSITORY)
    verify_license(source)


def assert_no_symlink_in_path(root: Path, rel: PurePosixPath, label: str) -> None:
    if ".." in rel.parts or rel.is_absolute():
        raise ImportError_(f"{label}: refuses to escape root: {rel}")
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ImportError_(f"{label}: refusing to follow symlink at {current}")


def resolve_within(root: Path, rel: PurePosixPath, label: str) -> Path:
    assert_no_symlink_in_path(root, rel, label)
    root_resolved = root.resolve()
    candidate = (root / Path(*rel.parts)).resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise ImportError_(f"{label} path escapes root: {rel}") from exc
    return candidate


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_notice_text() -> bytes:
    text = (
        "This directory contains reference material imported from the upstream\n"
        f"Backstage project ({UPSTREAM_REPOSITORY}) at commit {EXPECTED_COMMIT}.\n"
        "\n"
        "The pinned upstream checkout used for this import did not include a\n"
        f"NOTICE file. This file is generated locally by {SCRIPT_RELATIVE_PATH}\n"
        "to record attribution; it is NOT upstream content and must not be\n"
        "represented as such.\n"
        "\n"
        f"Upstream project: Backstage ({UPSTREAM_REPOSITORY})\n"
        f"Upstream commit: {EXPECTED_COMMIT}\n"
        f"Upstream license: {LICENSE_ID}\n"
        f"Import date: {IMPORT_DATE}\n"
    )
    return text.encode("utf-8")


def skill_entries() -> list[tuple[PurePosixPath, PurePosixPath, bool]]:
    """Return (source_rel, dest_rel, required) triples for the allow-list."""
    entries: list[tuple[PurePosixPath, PurePosixPath, bool]] = []
    for name in SKILL_NAMES:
        entries.append(
            (
                PurePosixPath(f"docs/.well-known/skills/{name}/SKILL.md"),
                PurePosixPath(f"skills/{name}/references/upstream/SKILL.md"),
                True,
            )
        )
    entries.append(
        (
            PurePosixPath("docs/.well-known/skills/index.md"),
            PurePosixPath("references/upstream/skills-index.md"),
            False,
        )
    )
    entries.append(
        (
            PurePosixPath(".claude/skills/catalog-db-performance.md"),
            PurePosixPath(f"skills/{PERFORMANCE_SNAPSHOT_SKILL}/references/upstream/catalog-db-performance.md"),
            True,
        )
    )
    entries.append((PurePosixPath("LICENSE"), PurePosixPath("LICENSE"), True))
    return entries


def build_entries(source: Path) -> list[Entry]:
    """Resolve the allow-list against ``source``, enforcing required files exist."""
    entries: list[Entry] = []
    missing_required: list[str] = []

    for source_rel, dest_rel, required in skill_entries():
        resolved = resolve_within(source, source_rel, "source")
        if not resolved.is_file():
            if required:
                missing_required.append(str(source_rel))
            continue
        entries.append(Entry(source_rel, dest_rel, resolved.read_bytes(), "upstream"))

    # NOTICE: copy upstream content when present, else generate a local
    # deterministic fallback that clearly names its source and commit.
    notice_rel = PurePosixPath("NOTICE")
    notice_dest = PurePosixPath("NOTICE")
    notice_path = resolve_within(source, notice_rel, "source")
    if notice_path.is_file():
        entries.append(Entry(notice_rel, notice_dest, notice_path.read_bytes(), "upstream"))
    else:
        entries.append(Entry(None, notice_dest, local_notice_text(), "generated"))

    if missing_required:
        joined = ", ".join(sorted(missing_required))
        raise ImportError_(f"required upstream files are missing from the allow-list: {joined}")

    entries.sort(key=lambda entry: str(entry.dest_rel))
    return entries


def build_provenance(entries: list[Entry]) -> dict[str, Any]:
    files = [
        {
            "source": str(entry.source_rel) if entry.source_rel is not None else None,
            "destination": str(entry.dest_rel),
            "sha256": sha256_hex(entry.data),
            "origin": entry.origin,
        }
        for entry in entries
    ]
    return {
        "generator": SCRIPT_RELATIVE_PATH,
        "sourceRepository": UPSTREAM_REPOSITORY,
        "sourceCommit": EXPECTED_COMMIT,
        "importDate": IMPORT_DATE,
        "license": LICENSE_ID,
        "files": files,
    }


def render_provenance(entries: list[Entry]) -> bytes:
    return (json.dumps(build_provenance(entries), indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def owned_destinations(entries: list[Entry]) -> list[Entry]:
    """Every destination this script fully owns, including PROVENANCE.json."""
    provenance_entry = Entry(None, PurePosixPath(PROVENANCE_FILENAME), render_provenance(entries), "generated")
    return [*entries, provenance_entry]


def owned_directories() -> set[PurePosixPath]:
    """Leaf directories fully generated by this script (safe to prune).

    Derive ownership from the static allow-list so a previously imported optional
    file remains inside the checked and prunable scope after it disappears from
    a later source checkout.
    """
    dirs: set[PurePosixPath] = set()
    for _source_rel, dest_rel, _required in skill_entries():
        parent = dest_rel.parent
        if parent.name == "upstream" and parent.parent.name == "references":
            dirs.add(parent)
    return dirs


def atomic_write_bytes(dest: Path, data: bytes) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(dest.parent), prefix=f".{dest.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, dest)
    except BaseException:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def check_import(plugin_dir: Path, entries: list[Entry]) -> list[str]:
    findings: list[str] = []
    all_owned = owned_destinations(entries)
    expected_dest_paths: set[Path] = set()
    for entry in all_owned:
        dest = resolve_within(plugin_dir, entry.dest_rel, "destination")
        expected_dest_paths.add(dest)
        if not dest.is_file():
            findings.append(f"missing imported file: {entry.dest_rel}")
            continue
        if dest.is_symlink():
            findings.append(f"imported destination must not be a symlink: {entry.dest_rel}")
            continue
        if dest.read_bytes() != entry.data:
            findings.append(f"imported file differs from source: {entry.dest_rel}")

    for owned_dir_rel in owned_directories():
        owned_dir = plugin_dir / Path(*owned_dir_rel.parts)
        if not owned_dir.is_dir():
            continue
        for path in sorted(owned_dir.rglob("*")):
            if path.is_file() and path.resolve() not in {p.resolve() for p in expected_dest_paths}:
                findings.append(f"unreferenced imported file: {path.relative_to(plugin_dir)}")

    return findings


def apply_import(plugin_dir: Path, entries: list[Entry]) -> None:
    all_owned = owned_destinations(entries)
    expected_dest_paths = set()
    for entry in all_owned:
        dest = resolve_within(plugin_dir, entry.dest_rel, "destination")
        expected_dest_paths.add(dest.resolve())
        atomic_write_bytes(dest, entry.data)

    # Preserve only owned destinations: prune stray files inside the
    # importer-owned reference directories without touching any other
    # plugin content (e.g. a future skill adapter's own SKILL.md).
    for owned_dir_rel in owned_directories():
        owned_dir = plugin_dir / Path(*owned_dir_rel.parts)
        if not owned_dir.is_dir():
            continue
        for path in sorted(owned_dir.rglob("*"), reverse=True):
            if path.is_file() and path.resolve() not in expected_dest_paths:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministically import allow-listed Backstage upstream skill references."
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="clean, offline backstage/backstage checkout pinned to the expected commit",
    )
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        default=None,
        help=f"destination plugin directory (default: harness/github-copilot/plugins/{PLUGIN_NAME})",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify imported files match the source without writing; exit 1 on drift",
    )
    args = parser.parse_args(argv)

    source = args.source.resolve()
    plugin_dir = (args.plugin_dir or (PLUGIN_ROOT / PLUGIN_NAME)).resolve()

    try:
        verify_source(source)
        entries = build_entries(source)
    except ImportError_ as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        findings = check_import(plugin_dir, entries)
        if findings:
            print(
                "Backstage upstream import is stale; run "
                f"python3 {SCRIPT_RELATIVE_PATH} --source <checkout>",
                file=sys.stderr,
            )
            for finding in findings:
                print(f"  - {finding}", file=sys.stderr)
            return 1
        print(f"Backstage upstream import is current ({len(entries)} files, commit {EXPECTED_COMMIT}).")
        return 0

    apply_import(plugin_dir, entries)
    print(f"Imported {len(entries)} files from {UPSTREAM_REPOSITORY}@{EXPECTED_COMMIT} into {plugin_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

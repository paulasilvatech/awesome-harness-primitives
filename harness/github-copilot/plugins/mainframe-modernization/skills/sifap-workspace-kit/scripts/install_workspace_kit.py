#!/usr/bin/env python3
"""Plan, apply, or archive SIFAP repository customizations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
PACKAGE_NAME = PACKAGE_ROOT.name
STATE_RELATIVE = Path(".github/.sifap-workspace-kit.json")
BACKUP_RELATIVE = Path(".github/.sifap-workspace-kit-backup")
PROFILES = ("core", "workshop", "automation", "full")
STAGE_AGENTS = (
    "sifap-archaeologist.agent.md",
    "sifap-architect.agent.md",
    "sifap-builder.agent.md",
    "sifap-quality.agent.md",
    "sifap-operations.agent.md",
)
STAGE_PROMPTS = (
    "sifap-archaeology.prompt.md",
    "sifap-specify.prompt.md",
    "sifap-build-slice.prompt.md",
    "sifap-verify.prompt.md",
    "sifap-operate.prompt.md",
)
PROJECT_SKILLS = (
    "sifap-modernization-context",
    "sifap-requirements-traceability",
    "sifap-workshop-orchestration",
    "sifap-loop",
    "sifap-workspace-kit",
)
CORE_INSTRUCTIONS = (
    "sifap-natural-adabas.instructions.md",
    "sifap-requirements.instructions.md",
    "sifap-security.instructions.md",
)
WORKSHOP_INSTRUCTIONS = (
    "sifap-backend.instructions.md",
    "sifap-cicd.instructions.md",
    "sifap-database.instructions.md",
    "sifap-frontend.instructions.md",
    "sifap-infrastructure.instructions.md",
    "sifap-tests.instructions.md",
)
GLOBAL_TEMPLATE = (
    PACKAGE_ROOT
    / "skills/sifap-workspace-kit/templates/copilot-instructions.md"
)
WORKFLOW_TEMPLATE = (
    PACKAGE_ROOT
    / "skills/sifap-workspace-kit/templates/sifap-traceability.yml"
)
TRACEABILITY_SCRIPT = (
    PACKAGE_ROOT
    / "skills/sifap-requirements-traceability/scripts/validate_traceability.py"
)


@dataclass(frozen=True)
class CopyItem:
    source: Path
    relative_destination: str


@dataclass(frozen=True)
class PlanEntry:
    source: str | None
    destination: str
    status: str
    sha256: str | None


@dataclass
class StateMutation:
    destination: Path
    backup: Path | None = None
    touched: bool = False


def digest_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_relative(relative: str) -> PurePosixPath:
    value = PurePosixPath(relative)
    if value.is_absolute() or not value.parts or ".." in value.parts:
        raise ValueError(f"unsafe workspace-kit destination: {relative}")
    return value


def safe_destination(target: Path, relative: str) -> Path:
    value = checked_relative(relative)
    candidate = target.joinpath(*value.parts)
    current = target
    for part in value.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"destination parent is a symlink: {current}")
    if candidate.is_symlink():
        raise ValueError(f"destination is a symlink: {candidate}")
    try:
        candidate.resolve().relative_to(target.resolve())
    except ValueError as exc:
        raise ValueError(
            f"destination escapes target repository: {candidate}"
        ) from exc
    return candidate


def checked_source(relative: str) -> Path:
    source = PACKAGE_ROOT / relative
    if source.is_symlink():
        raise ValueError(f"source symlink is not allowed: {source}")
    if not source.is_file():
        raise FileNotFoundError(
            f"workspace-kit source does not exist: {source}"
        )
    resolved = source.resolve()
    try:
        resolved.relative_to(PACKAGE_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"source escapes package root: {source}") from exc
    return resolved


def iter_tree(source_relative: str, destination: str) -> Iterable[CopyItem]:
    source_root = PACKAGE_ROOT / source_relative
    if source_root.is_symlink() or not source_root.is_dir():
        raise ValueError(f"invalid workspace-kit source tree: {source_root}")
    for source in sorted(source_root.rglob("*")):
        if source.is_symlink():
            raise ValueError(f"source symlink is not allowed: {source}")
        if not source.is_file() or "__pycache__" in source.parts:
            continue
        relative = source.relative_to(source_root).as_posix()
        yield CopyItem(source.resolve(), f"{destination}/{relative}")


def file_item(source: str, destination: str) -> CopyItem:
    return CopyItem(checked_source(source), destination)


def stage_agent_items() -> Iterable[CopyItem]:
    for name in STAGE_AGENTS:
        yield file_item(f"agents/{name}", f".github/agents/{name}")


def stage_prompt_items() -> Iterable[CopyItem]:
    for name in STAGE_PROMPTS:
        yield file_item(f"prompts/{name}", f".github/prompts/{name}")


def instruction_items(names: Iterable[str]) -> Iterable[CopyItem]:
    for name in names:
        yield file_item(
            f"instructions/{name}",
            f".github/instructions/{name}",
        )


def project_skill_items() -> Iterable[CopyItem]:
    for name in PROJECT_SKILLS:
        yield from iter_tree(
            f"skills/{name}",
            f".github/skills/{name}",
        )


def core_items() -> Iterable[CopyItem]:
    yield CopyItem(
        GLOBAL_TEMPLATE.resolve(),
        ".github/copilot-instructions.md",
    )
    yield from stage_agent_items()
    yield from project_skill_items()
    yield from instruction_items(CORE_INSTRUCTIONS)


def workshop_items() -> Iterable[CopyItem]:
    yield from core_items()
    yield from instruction_items(WORKSHOP_INSTRUCTIONS)
    yield from stage_prompt_items()


def automation_items() -> Iterable[CopyItem]:
    yield CopyItem(
        WORKFLOW_TEMPLATE.resolve(),
        ".github/workflows/sifap-traceability.yml",
    )
    yield CopyItem(
        TRACEABILITY_SCRIPT.resolve(),
        ".github/scripts/validate_sifap_traceability.py",
    )


def source_items(profile: str) -> list[CopyItem]:
    if profile == "core":
        candidates = list(core_items())
    elif profile == "workshop":
        candidates = list(workshop_items())
    elif profile == "automation":
        candidates = list(automation_items())
    elif profile == "full":
        candidates = [*workshop_items(), *automation_items()]
    else:
        raise ValueError(f"unsupported profile: {profile}")
    items: dict[str, CopyItem] = {}
    for item in candidates:
        if item.relative_destination in items:
            existing = items[item.relative_destination]
            if existing.source != item.source:
                raise ValueError(
                    "duplicate workspace-kit destination: "
                    f"{item.relative_destination}"
                )
            continue
        items[item.relative_destination] = item
    return [items[name] for name in sorted(items)]


def state_path(target: Path) -> Path:
    return safe_destination(target, STATE_RELATIVE.as_posix())


def backup_path(target: Path, relative: str) -> Path:
    return safe_destination(
        target,
        f"{BACKUP_RELATIVE.as_posix()}/{relative}",
    )


def load_state(target: Path) -> dict:
    path = state_path(target)
    if not path.exists():
        return {}
    if not path.is_file():
        raise ValueError(f"workspace-kit state is not a file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    managed = data.get("managed") if isinstance(data, dict) else None
    if (
        data.get("version") != 1
        or data.get("package") != PACKAGE_NAME
        or data.get("profile") not in PROFILES
        or not isinstance(managed, dict)
        or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in managed.items()
        )
    ):
        raise ValueError(f"invalid workspace-kit state: {path}")
    return data


def ensure_compatible_state(state: dict, profile: str) -> None:
    if state and state["profile"] != profile:
        raise ValueError(
            "workspace kit is managed with a different profile; "
            "preview and uninstall it before switching"
        )


def current_plan_entry(
    target: Path,
    item: CopyItem,
    managed: dict[str, str],
) -> PlanEntry:
    destination = safe_destination(target, item.relative_destination)
    source_hash = digest_file(item.source)
    previous_hash = managed.get(item.relative_destination)
    if not destination.exists():
        status = "create"
    elif not destination.is_file():
        status = "conflict"
    else:
        current_hash = digest_file(destination)
        if current_hash == source_hash:
            status = "unchanged" if previous_hash else "unmanaged-identical"
        elif previous_hash and current_hash == previous_hash:
            status = "update"
        else:
            status = "conflict"
    return PlanEntry(
        str(item.source),
        item.relative_destination,
        status,
        source_hash,
    )


def retired_plan_entry(
    target: Path,
    relative: str,
    installed_hash: str,
) -> PlanEntry:
    destination = safe_destination(target, relative)
    archive = backup_path(target, relative)
    if not destination.exists():
        status = "retired-missing"
    elif not destination.is_file():
        status = "retired-modified-preserve"
    elif digest_file(destination) != installed_hash:
        status = "retired-modified-preserve"
    elif archive.exists():
        status = "retired-backup-conflict"
    else:
        status = "retired-archive"
    return PlanEntry(None, relative, status, installed_hash)


def build_install_plan(
    target: Path,
    profile: str,
    state: dict,
) -> list[PlanEntry]:
    ensure_compatible_state(state, profile)
    managed = state.get("managed", {})
    plan: list[PlanEntry] = []
    items = source_items(profile)
    expected = {item.relative_destination for item in items}
    for item in items:
        plan.append(current_plan_entry(target, item, managed))
    for relative, installed_hash in sorted(managed.items()):
        if relative in expected:
            continue
        plan.append(retired_plan_entry(target, relative, installed_hash))
    return plan


def build_uninstall_plan(target: Path, state: dict) -> list[PlanEntry]:
    plan: list[PlanEntry] = []
    for relative, installed_hash in sorted(state.get("managed", {}).items()):
        destination = safe_destination(target, relative)
        archive = backup_path(target, relative)
        if not destination.exists():
            status = "missing"
        elif not destination.is_file():
            status = "modified-preserve"
        elif digest_file(destination) != installed_hash:
            status = "modified-preserve"
        elif archive.exists():
            status = "backup-conflict"
        else:
            status = "archive"
        plan.append(PlanEntry(None, relative, status, installed_hash))
    return plan


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent.is_symlink():
        raise ValueError(f"destination parent is a symlink: {path.parent}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def install_staged_file(staged: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.is_symlink():
        raise ValueError(
            f"destination parent is a symlink: {destination.parent}"
        )
    os.replace(staged, destination)


def rollback_state(
    destination: Path,
    backup: Path | None,
    touched: bool,
) -> str | None:
    if not touched:
        return None
    try:
        if destination.exists():
            destination.unlink()
        if backup is not None and backup.exists():
            os.replace(backup, destination)
    except OSError as exc:
        return f"state rollback failed: {exc}"
    return None


def rollback_write(destination: Path, backup: Path | None) -> str | None:
    try:
        if destination.exists():
            destination.unlink()
        if backup is not None and backup.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(backup, destination)
    except OSError as exc:
        return f"file rollback failed for {destination}: {exc}"
    return None


def rollback_archive(archive: Path, destination: Path) -> str | None:
    try:
        if archive.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(archive, destination)
    except OSError as exc:
        return f"archive rollback failed for {destination}: {exc}"
    return None


def rollback_install(
    writes: list[tuple[Path, Path | None]],
    archives: list[tuple[Path, Path]],
    state_destination: Path,
    state_backup: Path | None,
    state_touched: bool,
) -> list[str]:
    errors: list[str] = []
    state_error = rollback_state(
        state_destination,
        state_backup,
        state_touched,
    )
    if state_error:
        errors.append(state_error)
    for destination, backup in reversed(writes):
        error = rollback_write(destination, backup)
        if error:
            errors.append(error)
    for archive, destination in reversed(archives):
        error = rollback_archive(archive, destination)
        if error:
            errors.append(error)
    return errors


def managed_after_plan(state: dict, plan: list[PlanEntry]) -> dict[str, str]:
    managed = dict(state.get("managed", {}))
    for entry in plan:
        if entry.status in {"create", "update", "unchanged"}:
            assert entry.sha256 is not None
            managed[entry.destination] = entry.sha256
        elif entry.status in {"retired-archive", "retired-missing"}:
            managed.pop(entry.destination, None)
    return managed


def prepare_install(
    transaction: Path,
    write_entries: list[PlanEntry],
    payload: dict,
) -> tuple[list[tuple[PlanEntry, Path]], Path]:
    prepared: list[tuple[PlanEntry, Path]] = []
    for index, entry in enumerate(write_entries):
        assert entry.source is not None and entry.sha256 is not None
        content = Path(entry.source).read_bytes()
        if digest_bytes(content) != entry.sha256:
            raise ValueError(f"source changed while applying: {entry.source}")
        staged = transaction / f"new-{index}"
        atomic_write(staged, content)
        prepared.append((entry, staged))
    staged_state = transaction / "new-state"
    atomic_write(
        staged_state,
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return prepared, staged_state


def archive_retired_entries(
    target: Path,
    entries: list[PlanEntry],
    archives: list[tuple[Path, Path]],
) -> None:
    for entry in entries:
        assert entry.sha256 is not None
        destination = safe_destination(target, entry.destination)
        archive = backup_path(target, entry.destination)
        if (
            not destination.is_file()
            or digest_file(destination) != entry.sha256
            or archive.exists()
        ):
            raise OSError(
                f"retired destination changed: {entry.destination}"
            )
        archive.parent.mkdir(parents=True, exist_ok=True)
        os.replace(destination, archive)
        archives.append((archive, destination))


def commit_prepared_entries(
    target: Path,
    transaction: Path,
    prepared: list[tuple[PlanEntry, Path]],
    writes: list[tuple[Path, Path | None]],
) -> None:
    for index, (entry, staged) in enumerate(prepared):
        destination = safe_destination(target, entry.destination)
        backup: Path | None = None
        if destination.exists():
            backup = transaction / f"old-{index}"
            os.replace(destination, backup)
        writes.append((destination, backup))
        install_staged_file(staged, destination)


def apply_install(
    target: Path,
    profile: str,
    state: dict,
    plan: list[PlanEntry],
) -> None:
    blocking = {"conflict", "retired-backup-conflict"}
    if any(entry.status in blocking for entry in plan):
        raise ValueError("workspace kit has conflicts; no files were written")
    write_entries = [
        entry for entry in plan if entry.status in {"create", "update"}
    ]
    retired_entries = [
        entry for entry in plan if entry.status == "retired-archive"
    ]
    managed = managed_after_plan(state, plan)
    payload = {
        "version": 1,
        "package": PACKAGE_NAME,
        "profile": profile,
        "managed": dict(sorted(managed.items())),
    }
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".sifap-workspace-kit-",
        dir=target,
    ) as temporary_name:
        transaction = Path(temporary_name)
        prepared, staged_state = prepare_install(
            transaction,
            write_entries,
            payload,
        )

        writes: list[tuple[Path, Path | None]] = []
        archives: list[tuple[Path, Path]] = []
        state_destination = state_path(target)
        state_backup: Path | None = None
        state_touched = False
        try:
            archive_retired_entries(target, retired_entries, archives)
            commit_prepared_entries(
                target,
                transaction,
                prepared,
                writes,
            )

            if state_destination.exists():
                state_backup = transaction / "old-state"
                os.replace(state_destination, state_backup)
            state_touched = True
            install_staged_file(staged_state, state_destination)
        except (OSError, ValueError) as exc:
            rollback_errors = rollback_install(
                writes,
                archives,
                state_destination,
                state_backup,
                state_touched,
            )
            detail = "; ".join(rollback_errors)
            message = "workspace kit transaction failed; changes rolled back"
            if detail:
                message = f"{message}; {detail}"
            raise RuntimeError(message) from exc


def remaining_after_uninstall(
    state: dict,
    plan: list[PlanEntry],
) -> dict[str, str]:
    remaining = dict(state.get("managed", {}))
    for entry in plan:
        if entry.status in {"archive", "missing"}:
            remaining.pop(entry.destination, None)
    return remaining


def prepare_uninstall_state(
    transaction: Path,
    state: dict,
    remaining: dict[str, str],
) -> Path | None:
    if not remaining:
        return None
    payload = dict(state)
    payload["managed"] = dict(sorted(remaining.items()))
    staged_state = transaction / "new-state"
    atomic_write(
        staged_state,
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        ),
    )
    return staged_state


def archive_managed_file(source: Path, destination: Path) -> None:
    os.replace(source, destination)


def archive_uninstall_entries(
    target: Path,
    plan: list[PlanEntry],
    archives: list[tuple[Path, Path]],
) -> None:
    for entry in plan:
        if entry.status != "archive":
            continue
        assert entry.sha256 is not None
        destination = safe_destination(target, entry.destination)
        archive = backup_path(target, entry.destination)
        if (
            not destination.is_file()
            or digest_file(destination) != entry.sha256
            or archive.exists()
        ):
            raise OSError(
                f"uninstall destination changed: {entry.destination}"
            )
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive_managed_file(destination, archive)
        archives.append((archive, destination))


def commit_uninstall_state(
    target: Path,
    transaction: Path,
    remaining: dict[str, str],
    staged_state: Path | None,
    archives: list[tuple[Path, Path]],
    mutation: StateMutation,
) -> None:
    state_destination = mutation.destination
    if remaining:
        assert staged_state is not None
        if state_destination.exists():
            mutation.backup = transaction / "old-state"
            os.replace(state_destination, mutation.backup)
        mutation.touched = True
        install_staged_file(staged_state, state_destination)
        return
    if state_destination.exists():
        state_archive = backup_path(target, "workspace-kit-state.json")
        state_archive.parent.mkdir(parents=True, exist_ok=True)
        archive_managed_file(state_destination, state_archive)
        archives.append((state_archive, state_destination))


def apply_uninstall(target: Path, state: dict, plan: list[PlanEntry]) -> None:
    if any(entry.status == "backup-conflict" for entry in plan):
        raise ValueError(
            "workspace kit backup conflicts; no files were archived"
        )
    remaining = remaining_after_uninstall(state, plan)
    state_destination = state_path(target)
    state_archive = backup_path(target, "workspace-kit-state.json")
    if not remaining and state_destination.exists() and state_archive.exists():
        raise ValueError(
            "workspace kit state backup exists; no files were archived"
        )
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".sifap-workspace-kit-",
        dir=target,
    ) as temporary_name:
        transaction = Path(temporary_name)
        staged_state = prepare_uninstall_state(
            transaction,
            state,
            remaining,
        )

        archives: list[tuple[Path, Path]] = []
        mutation = StateMutation(state_destination)
        try:
            archive_uninstall_entries(target, plan, archives)
            commit_uninstall_state(
                target,
                transaction,
                remaining,
                staged_state,
                archives,
                mutation,
            )
        except (OSError, ValueError) as exc:
            rollback_errors = rollback_install(
                [],
                archives,
                mutation.destination,
                mutation.backup,
                mutation.touched,
            )
            detail = "; ".join(rollback_errors)
            message = (
                "workspace kit uninstall transaction failed; "
                "changes rolled back"
            )
            if detail:
                message = f"{message}; {detail}"
            raise RuntimeError(message) from exc


def validate_package_root() -> None:
    manifest = json.loads(
        (PACKAGE_ROOT / "plugin.json").read_text(encoding="utf-8")
    )
    if manifest.get("name") != PACKAGE_NAME:
        raise ValueError(f"unexpected package at {PACKAGE_ROOT}")


def print_report(
    target: Path,
    profile: str,
    plan: list[PlanEntry],
    *,
    action: str,
    applied: bool,
    json_output: bool,
) -> None:
    counts = Counter(entry.status for entry in plan)
    payload = {
        "mode": f"{action}{'-applied' if applied else '-plan'}",
        "target": str(target),
        "profile": profile,
        "summary": dict(sorted(counts.items())),
        "entries": [asdict(entry) for entry in plan],
    }
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(f"SIFAP workspace kit: {payload['mode']}")
    print(f"Target: {target}")
    print(f"Profile: {profile}")
    summary = ", ".join(
        f"{name}={count}" for name, count in sorted(counts.items())
    )
    print(f"Summary: {summary or 'empty'}")
    for entry in plan:
        if entry.status != "unchanged":
            print(f"  {entry.status}: {entry.destination}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan, apply, or uninstall the SIFAP workspace kit."
    )
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--profile", required=True, choices=PROFILES)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--allow-non-git", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_package_root()
        target = args.target.resolve()
        if not target.is_dir():
            raise ValueError(f"target must be an existing directory: {target}")
        if not args.allow_non_git and not (target / ".git").exists():
            raise ValueError(f"target is not a Git repository: {target}")
        state = load_state(target)
        ensure_compatible_state(state, args.profile)
        if args.uninstall:
            plan = build_uninstall_plan(target, state)
            if args.apply:
                apply_uninstall(target, state, plan)
            action = "uninstall"
        else:
            plan = build_install_plan(target, args.profile, state)
            if args.apply:
                apply_install(target, args.profile, state, plan)
            action = "install"
        print_report(
            target,
            args.profile,
            plan,
            action=action,
            applied=args.apply,
            json_output=args.json_output,
        )
        blocked = {
            "conflict",
            "backup-conflict",
            "retired-backup-conflict",
        }
        return 2 if any(entry.status in blocked for entry in plan) else 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"workspace-kit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

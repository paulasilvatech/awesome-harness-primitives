#!/usr/bin/env python3
"""Plan, apply, or archive Open Horizons repository customizations."""

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
STATE_RELATIVE = Path(".github/.open-horizons-workspace-kit.json")
BACKUP_RELATIVE = Path(".github/.open-horizons-workspace-kit-backup")
PROFILES = ("aeg", "core", "automation", "full")
AEG_AGENTS = (
    "open-horizons-aeg-analyst.agent.md",
    "open-horizons-aeg-concierge.agent.md",
    "open-horizons-aeg-gatekeeper.agent.md",
    "open-horizons-aeg-harvester.agent.md",
)
AEG_PROMPTS = (
    "open-horizons-aeg-approve.prompt.md",
    "open-horizons-aeg-harvest.prompt.md",
    "open-horizons-aeg-modernize.prompt.md",
    "open-horizons-aeg-start.prompt.md",
    "open-horizons-aeg-status.prompt.md",
)
WORKSPACE_MCP_TEMPLATE = (
    PACKAGE_ROOT / "skills/open-horizons-workspace-kit/templates/mcp.json"
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
        raise FileNotFoundError(f"workspace-kit source does not exist: {source}")
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


def hook_items() -> Iterable[CopyItem]:
    yield from iter_tree(
        "hooks/open-horizons-safety",
        "hooks/open-horizons-safety",
    )
    yield file_item(
        "hooks/open-horizons-safety/hooks.json",
        ".github/hooks/open-horizons-safety.json",
    )


def aeg_items() -> Iterable[CopyItem]:
    for name in AEG_AGENTS:
        yield file_item(f"agents/{name}", f".github/agents/{name}")
    for name in AEG_PROMPTS:
        yield file_item(f"prompts/{name}", f".github/prompts/{name}")
    yield file_item(
        "instructions/open-horizons-backstage-aeg.instructions.md",
        ".github/instructions/open-horizons-backstage-aeg.instructions.md",
    )
    yield from iter_tree(
        "skills/open-horizons-backstage-aeg-feature",
        ".github/skills/open-horizons-backstage-aeg-feature",
    )
    yield from hook_items()


def core_items() -> Iterable[CopyItem]:
    yield file_item("AGENTS.md", "AGENTS.md")
    yield file_item(
        "copilot-instructions.md",
        ".github/copilot-instructions.md",
    )
    yield from iter_tree("agents", ".github/agents")
    yield from iter_tree("skills", ".github/skills")
    yield from iter_tree("instructions", ".github/instructions")
    yield from iter_tree("prompts", ".github/prompts")
    yield from hook_items()
    yield CopyItem(WORKSPACE_MCP_TEMPLATE.resolve(), ".github/mcp.json")


def automation_items() -> Iterable[CopyItem]:
    yield from iter_tree("workflows", ".github/workflows")
    yield from iter_tree("ISSUE_TEMPLATE", ".github/ISSUE_TEMPLATE")


def source_items(profile: str) -> list[CopyItem]:
    if profile == "aeg":
        candidates = list(aeg_items())
    elif profile == "core":
        candidates = list(core_items())
    elif profile == "automation":
        candidates = list(automation_items())
    elif profile == "full":
        candidates = [*core_items(), *automation_items()]
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


def build_install_plan(
    target: Path,
    profile: str,
    state: dict,
) -> list[PlanEntry]:
    ensure_compatible_state(state, profile)
    managed = state.get("managed", {})
    plan: list[PlanEntry] = []
    for item in source_items(profile):
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
        plan.append(
            PlanEntry(
                str(item.source),
                item.relative_destination,
                status,
                source_hash,
            )
        )
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


def apply_install(
    target: Path,
    profile: str,
    state: dict,
    plan: list[PlanEntry],
) -> None:
    if any(entry.status == "conflict" for entry in plan):
        raise ValueError("workspace kit has conflicts; no files were written")
    managed = dict(state.get("managed", {}))
    for entry in plan:
        if entry.status not in {"create", "update"}:
            continue
        assert entry.source is not None and entry.sha256 is not None
        content = Path(entry.source).read_bytes()
        if digest_bytes(content) != entry.sha256:
            raise ValueError(f"source changed while applying: {entry.source}")
        atomic_write(safe_destination(target, entry.destination), content)
        managed[entry.destination] = entry.sha256
    for entry in plan:
        if entry.status == "unchanged" and entry.sha256 is not None:
            managed[entry.destination] = entry.sha256
    payload = {
        "version": 1,
        "package": PACKAGE_NAME,
        "profile": profile,
        "managed": dict(sorted(managed.items())),
    }
    atomic_write(
        state_path(target),
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def apply_uninstall(target: Path, state: dict, plan: list[PlanEntry]) -> None:
    if any(entry.status == "backup-conflict" for entry in plan):
        raise ValueError("workspace kit backup conflicts; no files were archived")
    remaining = dict(state.get("managed", {}))
    for entry in plan:
        if entry.status == "archive":
            destination = safe_destination(target, entry.destination)
            archive = backup_path(target, entry.destination)
            archive.parent.mkdir(parents=True, exist_ok=True)
            os.replace(destination, archive)
            remaining.pop(entry.destination, None)
        elif entry.status == "missing":
            remaining.pop(entry.destination, None)
    path = state_path(target)
    payload = dict(state)
    payload["managed"] = dict(sorted(remaining.items()))
    if remaining:
        atomic_write(
            path,
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
    elif path.exists():
        archive = backup_path(target, "workspace-kit-state.json")
        archive.parent.mkdir(parents=True, exist_ok=True)
        os.replace(path, archive)


def validate_workspace_mcp_template() -> None:
    package = json.loads((PACKAGE_ROOT / "mcp.json").read_text(encoding="utf-8"))
    workspace = json.loads(WORKSPACE_MCP_TEMPLATE.read_text(encoding="utf-8"))
    expected: dict[str, dict[str, object]] = {}
    for name, server in package.get("mcpServers", {}).items():
        if server.get("type") == "stdio":
            converted = {
                key: value
                for key, value in server.items()
                if key in {"command", "args", "env", "cwd"}
            }
            converted["type"] = "local"
        elif server.get("type") == "streamable-http":
            converted = {
                key: value
                for key, value in server.items()
                if key in {"url", "headers"}
            }
            converted["type"] = "http"
        elif server.get("type") == "sse":
            converted = {
                key: value
                for key, value in server.items()
                if key in {"url", "headers"}
            }
            converted["type"] = "sse"
        else:
            raise ValueError(f"unsupported MCP transport for {name}")
        converted["tools"] = ["*"]
        expected[name] = converted
    if workspace.get("mcpServers") != expected:
        raise ValueError("templates/mcp.json is stale")


def validate_package_root() -> None:
    manifest = json.loads(
        (PACKAGE_ROOT / "plugin.json").read_text(encoding="utf-8")
    )
    if manifest.get("name") != PACKAGE_NAME:
        raise ValueError(f"unexpected package at {PACKAGE_ROOT}")
    validate_workspace_mcp_template()


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
    print(f"Open Horizons workspace kit: {payload['mode']}")
    print(f"Target: {target}")
    print(f"Profile: {profile}")
    summary = ", ".join(
        f"{name}={count}" for name, count in payload["summary"].items()
    )
    print(f"Summary: {summary or 'empty'}")
    for entry in plan:
        if entry.status != "unchanged":
            print(f"  {entry.status}: {entry.destination}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan, apply, or uninstall the Open Horizons workspace kit."
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
        blocked = {"conflict", "backup-conflict"}
        return 2 if any(entry.status in blocked for entry in plan) else 0
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"workspace-kit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

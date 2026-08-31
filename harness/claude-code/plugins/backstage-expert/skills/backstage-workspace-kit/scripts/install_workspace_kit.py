#!/usr/bin/env python3
"""Plan, apply, or uninstall Backstage Expert repository customizations."""

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

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
COPILOT_SOURCE_ROOT = PLUGIN_ROOT / "copilot-components"
STATE_RELATIVE = Path(".github/.backstage-expert-workspace-kit.json")
PROFILE_FILES = {
    "adopter": {
        "instructions": (
            "backstage-app.instructions.md",
            "backstage-ai.instructions.md",
            "backstage-auth.instructions.md",
            "backstage-catalog.instructions.md",
            "backstage-integrations.instructions.md",
            "backstage-software-templates.instructions.md",
            "backstage-plugins.instructions.md",
            "backstage-techdocs.instructions.md",
        ),
        "prompts": (
            "backstage-assess.prompt.md",
            "backstage-change.prompt.md",
        ),
    },
    "core": {
        "instructions": (
            "backstage-ai.instructions.md",
            "backstage-auth.instructions.md",
            "backstage-integrations.instructions.md",
            "backstage-plugins.instructions.md",
            "backstage-techdocs.instructions.md",
        ),
        "prompts": (
            "backstage-assess.prompt.md",
            "backstage-change.prompt.md",
        ),
    },
}


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


def validate_relative(relative: str) -> PurePosixPath:
    value = PurePosixPath(relative)
    if value.is_absolute() or not value.parts or ".." in value.parts:
        raise ValueError(f"unsafe workspace-kit destination: {relative}")
    if value.as_posix() in {"AGENTS.md", ".github/copilot-instructions.md"}:
        raise ValueError(f"protected destination is not publishable: {relative}")
    return value


def safe_destination(target: Path, relative: str) -> Path:
    value = validate_relative(relative)
    candidate = target.joinpath(*value.parts)
    current = target
    for part in value.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"destination parent is a symlink: {current}")
    if candidate.is_symlink():
        raise ValueError(f"destination is a symlink: {candidate}")
    resolved_target = target.resolve()
    resolved_candidate = candidate.resolve()
    try:
        resolved_candidate.relative_to(resolved_target)
    except ValueError as exc:
        raise ValueError(f"destination escapes target repository: {candidate}") from exc
    return candidate


def checked_source(relative: str) -> Path:
    source = COPILOT_SOURCE_ROOT / relative
    if source.is_symlink():
        raise ValueError(f"source symlink is not allowed: {source}")
    if not source.is_file():
        raise FileNotFoundError(f"workspace-kit source does not exist: {source}")
    resolved = source.resolve()
    try:
        resolved.relative_to(COPILOT_SOURCE_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"source escapes plugin root: {source}") from exc
    return resolved


def source_items(profile: str, include_hook: bool) -> list[CopyItem]:
    config = PROFILE_FILES[profile]
    items: list[CopyItem] = []
    for name in config["instructions"]:
        items.append(
            CopyItem(
                checked_source(f"instructions/{name}"),
                f".github/instructions/{name}",
            )
        )
    for name in config["prompts"]:
        items.append(
            CopyItem(
                checked_source(f"prompts/{name}"),
                f".github/prompts/{name}",
            )
        )
    if include_hook:
        for name in ("guard.py", "README.md"):
            items.append(
                CopyItem(
                    checked_source(f"hooks/backstage-safety/{name}"),
                    f"hooks/backstage-safety/{name}",
                )
            )
        items.append(
            CopyItem(
                checked_source("hooks/backstage-safety/hooks.json"),
                ".github/hooks/backstage-safety.json",
            )
        )
    destinations = [item.relative_destination for item in items]
    if len(destinations) != len(set(destinations)):
        raise ValueError("workspace kit contains duplicate destinations")
    return sorted(items, key=lambda item: item.relative_destination)


def state_path(target: Path) -> Path:
    return safe_destination(target, STATE_RELATIVE.as_posix())


def load_state(target: Path) -> dict:
    path = state_path(target)
    if not path.exists():
        return {}
    if not path.is_file():
        raise ValueError(f"workspace-kit state is not a file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError(f"unsupported workspace-kit state: {path}")
    managed = data.get("managed")
    if not isinstance(managed, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in managed.items()
    ):
        raise ValueError(f"invalid managed-file map in workspace-kit state: {path}")
    if data.get("profile") not in PROFILE_FILES or not isinstance(
        data.get("includeHook"), bool
    ):
        raise ValueError(f"invalid workspace-kit profile state: {path}")
    return data


def ensure_compatible_state(state: dict, profile: str, include_hook: bool) -> None:
    if not state:
        return
    if state["profile"] != profile or state["includeHook"] != include_hook:
        raise ValueError(
            "workspace kit is already managed with a different profile or hook setting; "
            "preview and uninstall it before switching"
        )


def build_install_plan(
    target: Path, profile: str, include_hook: bool, state: dict
) -> list[PlanEntry]:
    ensure_compatible_state(state, profile, include_hook)
    managed = state.get("managed", {})
    plan: list[PlanEntry] = []
    for item in source_items(profile, include_hook):
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
    if not state:
        return []
    plan: list[PlanEntry] = []
    for relative, installed_hash in sorted(state["managed"].items()):
        destination = safe_destination(target, relative)
        if not destination.exists():
            status = "missing"
        elif not destination.is_file():
            status = "modified-preserve"
        elif digest_file(destination) == installed_hash:
            status = "remove"
        else:
            status = "modified-preserve"
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
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply_install(
    target: Path,
    profile: str,
    include_hook: bool,
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
        destination = safe_destination(target, entry.destination)
        content = Path(entry.source).read_bytes()
        if digest_bytes(content) != entry.sha256:
            raise ValueError(f"source changed while applying: {entry.source}")
        atomic_write(destination, content)
        managed[entry.destination] = entry.sha256
    for entry in plan:
        if entry.status == "unchanged" and entry.sha256 is not None:
            managed[entry.destination] = entry.sha256
    payload = {
        "version": 1,
        "plugin": "backstage-expert",
        "profile": profile,
        "includeHook": include_hook,
        "managed": dict(sorted(managed.items())),
    }
    atomic_write(
        state_path(target),
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def apply_uninstall(target: Path, state: dict, plan: list[PlanEntry]) -> None:
    remaining = dict(state.get("managed", {}))
    for entry in plan:
        if entry.status == "remove":
            safe_destination(target, entry.destination).unlink()
            remaining.pop(entry.destination, None)
        elif entry.status == "missing":
            remaining.pop(entry.destination, None)
    path = state_path(target)
    if remaining:
        payload = dict(state)
        payload["managed"] = dict(sorted(remaining.items()))
        atomic_write(
            path,
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
    elif path.exists():
        path.unlink()


def print_report(
    target: Path,
    profile: str,
    include_hook: bool,
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
        "includeHook": include_hook,
        "summary": dict(sorted(counts.items())),
        "entries": [asdict(entry) for entry in plan],
    }
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(f"Backstage Expert workspace kit: {payload['mode']}")
    print(f"Target: {target}")
    print(f"Profile: {profile}")
    print(f"Repository hook: {'included' if include_hook else 'not included'}")
    print(
        "Summary: "
        + (", ".join(f"{key}={value}" for key, value in payload["summary"].items()) or "empty")
    )
    for entry in plan:
        if entry.status not in {"unchanged"}:
            print(f"  {entry.status}: {entry.destination}")


def validate_plugin_root() -> None:
    manifest = COPILOT_SOURCE_ROOT / "plugin.json"
    if not manifest.is_file():
        raise FileNotFoundError(f"plugin manifest not found: {manifest}")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("name") != "backstage-expert":
        raise ValueError(f"unexpected plugin package at {PLUGIN_ROOT}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan, apply, or uninstall the Backstage Expert workspace kit."
    )
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--profile", required=True, choices=sorted(PROFILE_FILES))
    parser.add_argument("--include-hook", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--allow-non-git", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        validate_plugin_root()
        target = args.target.resolve()
        if not target.is_dir():
            raise ValueError(f"target must be an existing directory: {target}")
        if not args.allow_non_git and not (target / ".git").exists():
            raise ValueError(f"target is not a Git repository: {target}")
        state = load_state(target)
        if args.uninstall:
            if state:
                ensure_compatible_state(state, args.profile, args.include_hook)
            plan = build_uninstall_plan(target, state)
            if args.apply:
                apply_uninstall(target, state, plan)
            print_report(
                target,
                args.profile,
                args.include_hook,
                plan,
                action="uninstall",
                applied=args.apply,
                json_output=args.json_output,
            )
            return 0

        plan = build_install_plan(target, args.profile, args.include_hook, state)
        if args.apply and any(entry.status == "conflict" for entry in plan):
            print_report(
                target,
                args.profile,
                args.include_hook,
                plan,
                action="install",
                applied=False,
                json_output=args.json_output,
            )
            print("workspace-kit error: conflicts detected; no files were written", file=sys.stderr)
            return 2
        if args.apply:
            apply_install(target, args.profile, args.include_hook, state, plan)
        print_report(
            target,
            args.profile,
            args.include_hook,
            plan,
            action="install",
            applied=args.apply,
            json_output=args.json_output,
        )
        return 2 if any(entry.status == "conflict" for entry in plan) else 0
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"workspace-kit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Safely preview, install, update, or uninstall frontend workspace companions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


EDITION = "1"
PLUGIN_NAME = "frontend-experience"
SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "templates"
METADATA_REL = Path(".github/frontend-experience-companions.json")
MCP_REL = Path(".vscode/mcp.json")
MCP_SERVER = "playwright"
DISCOVERABILITY_PATHS = {
    Path(".github/instructions/frontend-discoverability.instructions.md"),
    Path(".github/prompts/frontend-assets.prompt.md"),
}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".venv",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}
FRONTEND_PACKAGES = {
    "@angular/core": "Angular",
    "@tauri-apps/api": "Tauri",
    "astro": "Astro",
    "electron": "Electron",
    "expo": "Expo",
    "next": "Next.js",
    "nuxt": "Nuxt",
    "react": "React",
    "react-native": "React Native",
    "svelte": "Svelte",
    "vue": "Vue",
}


@dataclass
class PlannedAction:
    path: str
    kind: str
    action: str
    reason: str
    content: bytes | None = None
    record: dict[str, Any] | None = None

    def public(self) -> dict[str, str]:
        return {
            "path": self.path,
            "kind": self.kind,
            "action": self.action,
            "reason": self.reason,
        }


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def json_value_hash(value: Any) -> str:
    compact = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def resolve_workspace(raw: str | Path) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    if os.path.lexists(path) and path.is_symlink():
        raise ValueError(f"workspace root must not be a symlink: {path}")
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"workspace does not exist: {path}") from exc
    if not resolved.is_dir():
        raise ValueError(f"workspace is not a directory: {resolved}")
    return resolved


def safe_target(workspace: Path, relative: Path) -> Path:
    workspace = workspace.resolve(strict=True)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe destination path: {relative}")
    current = workspace
    for part in relative.parts:
        current /= part
        if os.path.lexists(current) and current.is_symlink():
            raise ValueError(f"symlinked destination is not allowed: {current}")
    resolved_parent = current.parent.resolve(strict=False)
    if workspace != resolved_parent and workspace not in resolved_parent.parents:
        raise ValueError(f"destination escapes workspace: {relative}")
    return current


def walk_package_manifests(workspace: Path) -> list[Path]:
    manifests: list[Path] = []
    for current, dirs, files in os.walk(workspace, followlinks=False):
        current_path = Path(current)
        safe_dirs: list[str] = []
        for dirname in sorted(dirs):
            path = current_path / dirname
            if dirname in SKIP_DIRS or path.is_symlink():
                continue
            safe_dirs.append(dirname)
        dirs[:] = safe_dirs
        if "package.json" in files:
            manifests.append(current_path / "package.json")
    return sorted(manifests)


def relative_label(path: Path, workspace: Path) -> str:
    relative = path.relative_to(workspace)
    return "." if not relative.parts else relative.as_posix()


def detect_context(workspace: Path) -> dict[str, Any]:
    roots: set[str] = set()
    frameworks: set[str] = set()
    manifests: list[str] = []
    for manifest in walk_package_manifests(workspace):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        dependencies: dict[str, Any] = {}
        for key in ("dependencies", "devDependencies", "peerDependencies"):
            value = data.get(key)
            if isinstance(value, dict):
                dependencies.update(value)
        detected = {
            label
            for package, label in FRONTEND_PACKAGES.items()
            if package in dependencies
        }
        if detected:
            roots.add(relative_label(manifest.parent, workspace))
            frameworks.update(detected)
            manifests.append(relative_label(manifest, workspace))

    if not roots:
        for candidate in ("frontend", "client", "web", "ui", "app", "src"):
            path = workspace / candidate
            if path.is_dir() and not path.is_symlink():
                roots.add(candidate)
        if not roots:
            roots.add(".")

    test_roots: set[str] = set()
    public_roots: set[str] = set()
    for root_label in roots:
        root = workspace if root_label == "." else workspace / root_label
        for candidate in ("test", "tests", "e2e", "__tests__"):
            path = root / candidate
            if path.is_dir() and not path.is_symlink():
                test_roots.add(relative_label(path, workspace))
        for candidate in ("public",):
            path = root / candidate
            if path.is_dir() and not path.is_symlink():
                public_roots.add(relative_label(path, workspace))
    if not test_roots:
        test_roots.update(roots)

    customization_candidates = [
        ".github/copilot-instructions.md",
        ".github/instructions",
        ".github/prompts",
        ".github/agents",
        ".github/skills",
        ".vscode/mcp.json",
    ]
    existing_customizations = [
        item for item in customization_candidates if (workspace / item).exists()
    ]

    scripts: list[str] = []
    for manifest_label in manifests:
        manifest_path = workspace / manifest_label
        try:
            package = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(package, dict) and isinstance(package.get("scripts"), dict):
            scripts.extend(
                f"{manifest_label}:{name}" for name in sorted(package["scripts"])
            )

    return {
        "frontend_roots": sorted(roots),
        "test_roots": sorted(test_roots),
        "public_roots": sorted(public_roots),
        "discoverability_applicable": bool(public_roots),
        "frameworks": sorted(frameworks),
        "package_manifests": sorted(manifests),
        "scripts": sorted(scripts),
        "existing_customizations": existing_customizations,
    }


def scoped(root: str, pattern: str) -> str:
    return pattern if root == "." else f"{root}/{pattern}"


def render_values(context: dict[str, Any]) -> dict[str, str]:
    frontend_patterns = [
        scoped(root, "**/*.{js,jsx,ts,tsx,vue,svelte,astro,html,css,scss,sass,less}")
        for root in context["frontend_roots"]
    ]
    test_patterns: list[str] = []
    for root in context["test_roots"]:
        test_patterns.extend(
            [
                scoped(root, "**/*.{test,spec}.{js,jsx,ts,tsx}"),
                scoped(root, "**/*.{e2e,pw}.{js,jsx,ts,tsx}"),
            ]
        )
    discoverability_patterns: list[str] = []
    discoverability_roots = sorted(
        set(context["frontend_roots"]) | set(context["public_roots"])
    )
    for root in discoverability_roots:
        discoverability_patterns.extend(
            [
                scoped(root, "**/*.{html,jsx,tsx,vue,svelte,astro}"),
                scoped(
                    root,
                    "**/*.{webmanifest,json,xml,txt,svg,png,ico}",
                ),
            ]
        )
    return {
        "__FRONTEND_APPLY_TO__": ",".join(sorted(set(frontend_patterns))),
        "__FRONTEND_TEST_APPLY_TO__": ",".join(sorted(set(test_patterns))),
        "__FRONTEND_DISCOVERABILITY_APPLY_TO__": ",".join(
            sorted(set(discoverability_patterns))
        ),
    }


def render_template(path: Path, replacements: dict[str, str]) -> bytes:
    text = path.read_text(encoding="utf-8")
    for marker, value in replacements.items():
        text = text.replace(marker, value)
    unresolved = [marker for marker in replacements if marker in text]
    if unresolved:
        raise ValueError(
            f"unresolved template markers in {path}: {', '.join(unresolved)}"
        )
    return text.encode("utf-8")


def collect_templates(
    template_root: Path,
    replacements: dict[str, str],
    include_mcp: bool,
    include_discoverability: bool,
) -> list[tuple[Path, bytes]]:
    if template_root.is_symlink() or not template_root.is_dir():
        raise ValueError(f"template root is not a regular directory: {template_root}")
    files: list[tuple[Path, bytes]] = []
    for current, dirs, filenames in os.walk(template_root, followlinks=False):
        current_path = Path(current)
        for dirname in dirs:
            if (current_path / dirname).is_symlink():
                raise ValueError(
                    f"symlinked template directory is not allowed: {current_path / dirname}"
                )
        for filename in sorted(filenames):
            path = current_path / filename
            if path.is_symlink() or not path.is_file():
                raise ValueError(f"invalid template file: {path}")
            relative = path.relative_to(template_root)
            if relative == MCP_REL:
                if include_mcp:
                    files.append((relative, path.read_bytes()))
                continue
            if relative in DISCOVERABILITY_PATHS and not include_discoverability:
                continue
            files.append((relative, render_template(path, replacements)))
    return sorted(files, key=lambda item: item[0].as_posix())


def metadata_path(workspace: Path) -> Path:
    return safe_target(workspace, METADATA_REL)


def load_metadata(workspace: Path) -> dict[str, Any] | None:
    path = metadata_path(workspace)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid ownership metadata at line {exc.lineno}: {exc.msg}"
        ) from exc
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise ValueError("ownership metadata schema must equal 1")
    if data.get("plugin") != PLUGIN_NAME:
        raise ValueError("ownership metadata belongs to another publisher")
    files = data.get("files")
    if not isinstance(files, list) or not all(isinstance(item, dict) for item in files):
        raise ValueError("ownership metadata files must be an array of objects")
    return data


def metadata_records(metadata: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if metadata is None:
        return {}
    return {
        str(item["path"]): item
        for item in metadata["files"]
        if isinstance(item.get("path"), str)
    }


def parse_mcp_template(content: bytes) -> dict[str, Any]:
    try:
        data = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid VS Code MCP template: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("servers"), dict):
        raise ValueError("VS Code MCP template must contain a servers object")
    server = data["servers"].get(MCP_SERVER)
    if not isinstance(server, dict):
        raise ValueError(f"VS Code MCP template is missing server {MCP_SERVER}")
    return server


def plan_regular_file(
    workspace: Path,
    relative: Path,
    content: bytes,
    prior: dict[str, Any] | None,
    force: bool,
) -> PlannedAction:
    target = safe_target(workspace, relative)
    desired_hash = sha256_bytes(content)
    record = {
        "path": relative.as_posix(),
        "kind": "file",
        "sha256": desired_hash,
    }
    if not target.exists():
        return PlannedAction(
            relative.as_posix(), "file", "create", "target does not exist", content, record
        )
    current = target.read_bytes()
    current_hash = sha256_bytes(current)
    if current_hash == desired_hash:
        return PlannedAction(
            relative.as_posix(), "file", "unchanged", "content already matches", None, record
        )
    if (
        prior
        and prior.get("kind") == "file"
        and prior.get("sha256") == current_hash
    ):
        return PlannedAction(
            relative.as_posix(),
            "file",
            "update",
            "owned file is unmodified and template changed",
            content,
            record,
        )
    if force:
        return PlannedAction(
            relative.as_posix(),
            "file",
            "update",
            "explicit force selected for conflicting file",
            content,
            record,
        )
    return PlannedAction(
        relative.as_posix(),
        "file",
        "conflict",
        "existing file is unowned or modified",
        None,
        record,
    )


def plan_mcp_file(
    workspace: Path,
    content: bytes,
    prior: dict[str, Any] | None,
    force: bool,
) -> PlannedAction:
    target = safe_target(workspace, MCP_REL)
    server = parse_mcp_template(content)
    server_hash = json_value_hash(server)
    created_file = bool(prior.get("created_file")) if prior else not target.exists()
    record = {
        "path": MCP_REL.as_posix(),
        "kind": "json-server",
        "server_name": MCP_SERVER,
        "server_sha256": server_hash,
        "created_file": created_file,
    }
    if not target.exists():
        merged = {"servers": {MCP_SERVER: server}}
        return PlannedAction(
            MCP_REL.as_posix(),
            "json-server",
            "create",
            "VS Code MCP file does not exist",
            canonical_json(merged),
            record,
        )
    try:
        current = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return PlannedAction(
            MCP_REL.as_posix(),
            "json-server",
            "conflict",
            f"existing VS Code MCP JSON is invalid at line {exc.lineno}",
            None,
            record,
        )
    if not isinstance(current, dict):
        return PlannedAction(
            MCP_REL.as_posix(),
            "json-server",
            "conflict",
            "existing VS Code MCP root is not an object",
            None,
            record,
        )
    servers = current.get("servers")
    if servers is None:
        servers = {}
        current["servers"] = servers
    if not isinstance(servers, dict):
        return PlannedAction(
            MCP_REL.as_posix(),
            "json-server",
            "conflict",
            "existing VS Code MCP servers value is not an object",
            None,
            record,
        )
    existing = servers.get(MCP_SERVER)
    if existing == server:
        return PlannedAction(
            MCP_REL.as_posix(),
            "json-server",
            "unchanged",
            "named Playwright server already matches",
            None,
            record,
        )
    if existing is not None and not force:
        return PlannedAction(
            MCP_REL.as_posix(),
            "json-server",
            "conflict",
            "named Playwright server already exists with different content",
            None,
            record,
        )
    servers[MCP_SERVER] = server
    reason = (
        "explicit force selected for conflicting named server"
        if existing is not None
        else "merge named Playwright server into existing VS Code MCP file"
    )
    return PlannedAction(
        MCP_REL.as_posix(),
        "json-server",
        "update",
        reason,
        canonical_json(current),
        record,
    )


def build_install_plan(
    workspace: Path,
    template_root: Path = TEMPLATE_ROOT,
    *,
    include_mcp: bool,
    force: bool,
    discoverability: str = "auto",
) -> tuple[dict[str, Any], list[PlannedAction], dict[str, Any]]:
    context = detect_context(workspace)
    replacements = render_values(context)
    include_discoverability = (
        bool(context["discoverability_applicable"])
        if discoverability == "auto"
        else discoverability == "include"
    )
    context["discoverability_selected"] = include_discoverability
    prior_metadata = load_metadata(workspace)
    prior_records = metadata_records(prior_metadata)
    actions: list[PlannedAction] = []
    selected_records: dict[str, dict[str, Any]] = dict(prior_records)
    for relative, content in collect_templates(
        template_root,
        replacements,
        include_mcp,
        include_discoverability,
    ):
        prior = prior_records.get(relative.as_posix())
        action = (
            plan_mcp_file(workspace, content, prior, force)
            if relative == MCP_REL
            else plan_regular_file(workspace, relative, content, prior, force)
        )
        actions.append(action)
        if action.record is not None:
            selected_records[action.path] = action.record
    if not include_mcp:
        actions.append(
            PlannedAction(
                MCP_REL.as_posix(),
                "json-server",
                "skipped",
                "optional VS Code MCP publication was not selected",
            )
        )
    if not include_discoverability:
        reason = (
            "no public web route evidence was detected"
            if discoverability == "auto"
            else "discoverability companions were explicitly excluded"
        )
        for relative in sorted(
            DISCOVERABILITY_PATHS, key=lambda item: item.as_posix()
        ):
            actions.append(
                PlannedAction(
                    relative.as_posix(),
                    "file",
                    "skipped",
                    reason,
                )
            )
    metadata = {
        "schema": 1,
        "plugin": PLUGIN_NAME,
        "edition": EDITION,
        "files": [
            selected_records[key] for key in sorted(selected_records)
        ],
    }
    return context, actions, metadata


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def prune_empty_parents(path: Path, workspace: Path) -> None:
    current = path
    while current != workspace and workspace in current.parents:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def apply_install(
    workspace: Path,
    actions: list[PlannedAction],
    metadata: dict[str, Any],
    writer: Callable[[Path, bytes], None] = atomic_write,
) -> None:
    write_actions = [item for item in actions if item.action in {"create", "update"}]
    metadata_target = metadata_path(workspace)
    backups: list[tuple[Path, bytes | None]] = []
    try:
        for action in write_actions:
            target = safe_target(workspace, Path(action.path))
            backups.append((target, target.read_bytes() if target.exists() else None))
            if action.content is None:
                raise RuntimeError(f"planned write has no content: {action.path}")
            writer(target, action.content)
        backups.append(
            (
                metadata_target,
                metadata_target.read_bytes() if metadata_target.exists() else None,
            )
        )
        writer(metadata_target, canonical_json(metadata))
    except Exception:
        for target, original in reversed(backups):
            if original is None:
                if target.exists() and not target.is_symlink():
                    target.unlink()
                    prune_empty_parents(target.parent, workspace)
            else:
                atomic_write(target, original)
        raise


def build_uninstall_plan(
    workspace: Path,
) -> tuple[list[PlannedAction], dict[str, Any] | None]:
    metadata = load_metadata(workspace)
    if metadata is None:
        return [], None
    actions: list[PlannedAction] = []
    for record in metadata["files"]:
        relative = Path(str(record["path"]))
        try:
            target = safe_target(workspace, relative)
        except ValueError as exc:
            actions.append(
                PlannedAction(relative.as_posix(), str(record.get("kind")), "preserve", str(exc))
            )
            continue
        if not target.exists():
            actions.append(
                PlannedAction(relative.as_posix(), str(record.get("kind")), "missing", "owned target is already absent")
            )
            continue
        if record.get("kind") == "file":
            if sha256_bytes(target.read_bytes()) == record.get("sha256"):
                actions.append(
                    PlannedAction(relative.as_posix(), "file", "remove", "owned file is unmodified")
                )
            else:
                actions.append(
                    PlannedAction(relative.as_posix(), "file", "preserve", "owned file was modified")
                )
            continue
        if record.get("kind") != "json-server":
            actions.append(
                PlannedAction(relative.as_posix(), "unknown", "preserve", "unknown ownership record kind")
            )
            continue
        try:
            current = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            actions.append(
                PlannedAction(relative.as_posix(), "json-server", "preserve", "VS Code MCP JSON is now invalid")
            )
            continue
        servers = current.get("servers") if isinstance(current, dict) else None
        server = servers.get(MCP_SERVER) if isinstance(servers, dict) else None
        if server is None:
            actions.append(
                PlannedAction(relative.as_posix(), "json-server", "missing", "owned server entry is already absent")
            )
        elif json_value_hash(server) != record.get("server_sha256"):
            actions.append(
                PlannedAction(relative.as_posix(), "json-server", "preserve", "owned server entry was modified")
            )
        else:
            del servers[MCP_SERVER]
            removable_keys = set(current) <= {"servers", "inputs"}
            empty_inputs = current.get("inputs", []) == []
            if record.get("created_file") and not servers and removable_keys and empty_inputs:
                actions.append(
                    PlannedAction(relative.as_posix(), "json-server", "remove", "remove MCP file created by this setup")
                )
            else:
                actions.append(
                    PlannedAction(
                        relative.as_posix(),
                        "json-server",
                        "update",
                        "remove only the owned Playwright server entry",
                        canonical_json(current),
                    )
                )
    return actions, metadata


def apply_uninstall(
    workspace: Path,
    actions: list[PlannedAction],
    writer: Callable[[Path, bytes], None] = atomic_write,
) -> None:
    metadata_target = metadata_path(workspace)
    backups: list[tuple[Path, bytes | None]] = []
    try:
        for action in actions:
            if action.action not in {"remove", "update"}:
                continue
            target = safe_target(workspace, Path(action.path))
            backups.append((target, target.read_bytes() if target.exists() else None))
            if action.action == "remove":
                if target.exists():
                    target.unlink()
                    prune_empty_parents(target.parent, workspace)
            else:
                if action.content is None:
                    raise RuntimeError(f"planned update has no content: {action.path}")
                writer(target, action.content)
        backups.append(
            (
                metadata_target,
                metadata_target.read_bytes() if metadata_target.exists() else None,
            )
        )
        if metadata_target.exists():
            metadata_target.unlink()
            prune_empty_parents(metadata_target.parent, workspace)
    except Exception:
        for target, original in reversed(backups):
            if original is None:
                if target.exists() and not target.is_symlink():
                    target.unlink()
                    prune_empty_parents(target.parent, workspace)
            else:
                atomic_write(target, original)
        raise


def render_result(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print(f"Status: {payload['status']}")
    print(f"Workspace: {payload['workspace']}")
    if "detection" in payload:
        detection = payload["detection"]
        print(f"Frameworks: {', '.join(detection['frameworks']) or 'not detected'}")
        print(f"Frontend roots: {', '.join(detection['frontend_roots'])}")
    for action in payload.get("actions", []):
        print(f"- {action['action']}: {action['path']} ({action['reason']})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, help="Selected workspace root")
    parser.add_argument(
        "--action",
        choices=("plan", "apply", "uninstall"),
        default="plan",
        help="Operation; plan is the no-write default",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Explicitly approve apply or uninstall writes",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace conflicting companion files or the named server entry",
    )
    parser.add_argument(
        "--include-vscode-mcp",
        action="store_true",
        help="Publish or update only the named Playwright server entry",
    )
    parser.add_argument(
        "--discoverability",
        choices=("auto", "include", "exclude"),
        default="auto",
        help="Publish discoverability companions automatically from public-route evidence, or override explicitly",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args(argv)

    try:
        workspace = resolve_workspace(args.workspace)
        if args.action == "uninstall":
            if args.force:
                raise ValueError("--force applies only to installation updates")
            actions, metadata = build_uninstall_plan(workspace)
            status = "not-installed" if metadata is None else "planned"
            if args.approve and metadata is not None:
                apply_uninstall(workspace, actions)
                status = "uninstalled"
            elif metadata is not None and not args.approve:
                status = "approval-required"
            payload = {
                "status": status,
                "workspace": str(workspace),
                "edition": metadata.get("edition") if metadata else None,
                "actions": [item.public() for item in actions],
            }
            render_result(payload, args.json)
            return 2 if status == "approval-required" else 0

        context, actions, metadata = build_install_plan(
            workspace,
            include_mcp=args.include_vscode_mcp,
            force=args.force,
            discoverability=args.discoverability,
        )
        conflicts = [item for item in actions if item.action == "conflict"]
        status = "planned"
        exit_code = 0
        if conflicts:
            status = "conflict"
            exit_code = 2
        elif args.action == "apply":
            if not args.approve:
                status = "approval-required"
                exit_code = 2
            else:
                apply_install(workspace, actions, metadata)
                status = "applied"
        payload = {
            "status": status,
            "workspace": str(workspace),
            "edition": EDITION,
            "detection": context,
            "actions": [item.public() for item in actions],
        }
        render_result(payload, args.json)
        return exit_code
    except (OSError, ValueError, RuntimeError) as exc:
        payload = {
            "status": "blocked",
            "workspace": str(args.workspace),
            "error": str(exc),
            "actions": [],
        }
        render_result(payload, args.json)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Plan or publish Open Horizons repository-scoped customization assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_COMPONENTS = (
    "governance",
    "instructions",
    "prompts",
    "automation",
    "hooks",
    "mcp",
    "runtime",
)
VALID_COMPONENTS = DEFAULT_COMPONENTS
WORKSPACE_MCP_TEMPLATE = (
    PLUGIN_ROOT / "skills/open-horizons-workspace-kit/templates/mcp.json"
)


@dataclass(frozen=True)
class CopyItem:
    source: Path
    destination: Path
    relative_destination: str


@dataclass(frozen=True)
class PlanEntry:
    source: str
    destination: str
    status: str


def iter_files(source: Path, destination: Path, target: Path) -> Iterable[CopyItem]:
    if source.is_symlink():
        raise ValueError(f"source symlink is not allowed: {source}")
    if source.is_file():
        yield copy_item(source, destination, target)
        return
    if not source.is_dir():
        raise FileNotFoundError(f"workspace-kit source does not exist: {source}")
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"source symlink is not allowed: {path}")
        if path.is_file():
            yield copy_item(path, destination / path.relative_to(source), target)


def copy_item(source: Path, destination: Path, target: Path) -> CopyItem:
    resolved_target = target.resolve()
    resolved_destination = destination.resolve()
    try:
        relative = resolved_destination.relative_to(resolved_target)
    except ValueError as exc:
        raise ValueError(f"destination escapes target repository: {destination}") from exc
    return CopyItem(source.resolve(), resolved_destination, relative.as_posix())


def component_sources(component: str, target: Path) -> Iterable[CopyItem]:
    github = target / ".github"
    if component == "governance":
        yield from iter_files(PLUGIN_ROOT / "AGENTS.md", target / "AGENTS.md", target)
        yield from iter_files(
            PLUGIN_ROOT / "copilot-instructions.md",
            github / "copilot-instructions.md",
            target,
        )
        yield from iter_files(
            PLUGIN_ROOT / "model-routing.yaml",
            github / "model-routing.yaml",
            target,
        )
        yield from iter_files(PLUGIN_ROOT / "docs", github / "docs", target)
    elif component == "instructions":
        yield from iter_files(PLUGIN_ROOT / "instructions", github / "instructions", target)
    elif component == "prompts":
        yield from iter_files(PLUGIN_ROOT / "prompts", github / "prompts", target)
    elif component == "automation":
        yield from iter_files(PLUGIN_ROOT / "workflows", github / "workflows", target)
        yield from iter_files(
            PLUGIN_ROOT / "ISSUE_TEMPLATE",
            github / "ISSUE_TEMPLATE",
            target,
        )
        yield from iter_files(
            PLUGIN_ROOT / "PULL_REQUEST_TEMPLATE.md",
            github / "PULL_REQUEST_TEMPLATE.md",
            target,
        )
        yield from iter_files(
            PLUGIN_ROOT / "dependabot.yml",
            github / "dependabot.yml",
            target,
        )
    elif component == "hooks":
        yield from iter_files(PLUGIN_ROOT / "hooks", target / "hooks", target)
        yield from iter_files(
            PLUGIN_ROOT / "hooks/open-horizons-safety/hooks.json",
            github / "hooks/open-horizons-safety.json",
            target,
        )
    elif component == "mcp":
        yield from iter_files(WORKSPACE_MCP_TEMPLATE, github / "mcp.json", target)
    elif component == "runtime":
        yield from iter_files(PLUGIN_ROOT / "agents", github / "agents", target)
        yield from iter_files(PLUGIN_ROOT / "skills", github / "skills", target)
    else:
        raise ValueError(f"unknown component group: {component}")


def parse_components(raw: str) -> tuple[str, ...]:
    values = tuple(part.strip() for part in raw.split(",") if part.strip())
    if not values:
        raise ValueError("at least one component group is required")
    invalid = sorted(set(values) - set(VALID_COMPONENTS))
    if invalid:
        raise ValueError(
            f"unknown component group(s): {', '.join(invalid)}; "
            f"choose from {', '.join(VALID_COMPONENTS)}"
        )
    if len(values) != len(set(values)):
        raise ValueError("component groups must not be repeated")
    return values


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_plan(target: Path, components: tuple[str, ...], force: bool) -> list[PlanEntry]:
    items: dict[str, CopyItem] = {}
    for component in components:
        for item in component_sources(component, target):
            if item.relative_destination in items:
                raise ValueError(f"duplicate destination in workspace kit: {item.relative_destination}")
            items[item.relative_destination] = item

    plan: list[PlanEntry] = []
    for relative, item in sorted(items.items()):
        if not item.destination.exists():
            status = "create"
        elif not item.destination.is_file():
            status = "conflict"
        elif file_digest(item.source) == file_digest(item.destination):
            status = "unchanged"
        else:
            status = "overwrite" if force else "conflict"
        plan.append(PlanEntry(str(item.source), relative, status))
    return plan


def apply_plan(target: Path, plan: list[PlanEntry]) -> None:
    conflicts = [entry for entry in plan if entry.status == "conflict"]
    if conflicts:
        raise ValueError("workspace kit has conflicts; no files were written")
    for entry in plan:
        if entry.status not in {"create", "overwrite"}:
            continue
        source = Path(entry.source)
        destination = target / entry.destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def print_report(
    target: Path,
    components: tuple[str, ...],
    plan: list[PlanEntry],
    *,
    applied: bool,
    json_output: bool,
) -> None:
    counts = Counter(entry.status for entry in plan)
    payload = {
        "mode": "applied" if applied else "plan",
        "target": str(target),
        "components": list(components),
        "summary": {
            status: counts.get(status, 0)
            for status in ("create", "overwrite", "unchanged", "conflict")
        },
        "entries": [asdict(entry) for entry in plan],
    }
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(f"Open Horizons workspace kit: {payload['mode']}")
    print(f"Target: {target}")
    print(f"Components: {', '.join(components)}")
    print(
        "Summary: "
        + ", ".join(f"{name}={count}" for name, count in payload["summary"].items())
    )
    for entry in plan:
        if entry.status != "unchanged":
            print(f"  {entry.status}: {entry.destination}")


def validate_plugin_root() -> None:
    manifest = PLUGIN_ROOT / "plugin.json"
    if not manifest.is_file():
        raise FileNotFoundError(f"plugin manifest not found: {manifest}")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("name") != "open-horizons-platform":
        raise ValueError(f"unexpected plugin package at {PLUGIN_ROOT}")
    validate_workspace_mcp_template()


def validate_workspace_mcp_template() -> None:
    plugin_config = json.loads((PLUGIN_ROOT / "mcp.json").read_text(encoding="utf-8"))
    workspace_config = json.loads(WORKSPACE_MCP_TEMPLATE.read_text(encoding="utf-8"))
    plugin_servers = plugin_config.get("mcpServers")
    workspace_servers = workspace_config.get("mcpServers")
    if not isinstance(plugin_servers, dict) or not isinstance(workspace_servers, dict):
        raise ValueError("plugin and workspace MCP configurations require `mcpServers` objects")

    expected: dict[str, dict[str, object]] = {}
    for name, server in plugin_servers.items():
        if not isinstance(name, str) or not isinstance(server, dict):
            raise ValueError("plugin MCP server entries must be named objects")
        server_type = server.get("type")
        if server_type == "stdio":
            converted = {
                key: value
                for key, value in server.items()
                if key in {"command", "args", "env", "cwd"}
            }
            converted["type"] = "local"
        elif server_type == "streamable-http":
            converted = {
                key: value for key, value in server.items() if key in {"url", "headers"}
            }
            converted["type"] = "http"
        elif server_type == "sse":
            converted = {
                key: value for key, value in server.items() if key in {"url", "headers"}
            }
            converted["type"] = "sse"
        else:
            raise ValueError(f"unsupported plugin MCP transport for `{name}`: {server_type}")
        converted["tools"] = ["*"]
        expected[name] = converted

    if workspace_servers != expected:
        raise ValueError(
            "templates/mcp.json is stale; update it from the plugin-root mcp.json transport mapping"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plan or publish the Open Horizons repository workspace kit."
    )
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument(
        "--components",
        default=",".join(DEFAULT_COMPONENTS),
        help=f"comma-separated groups: {', '.join(VALID_COMPONENTS)}",
    )
    parser.add_argument("--apply", action="store_true", help="write the planned files")
    parser.add_argument("--force", action="store_true", help="overwrite differing files")
    parser.add_argument(
        "--allow-non-git",
        action="store_true",
        help="allow a target without a .git directory",
    )
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    try:
        validate_plugin_root()
        target = args.target.resolve()
        if not target.is_dir():
            raise ValueError(f"target must be an existing directory: {target}")
        if not args.allow_non_git and not (target / ".git").exists():
            raise ValueError(f"target is not a Git repository: {target}")
        components = parse_components(args.components)
        plan = build_plan(target, components, args.force)
        if args.apply and any(entry.status == "conflict" for entry in plan):
            print_report(
                target,
                components,
                plan,
                applied=False,
                json_output=args.json_output,
            )
            print("workspace-kit error: conflicts detected; no files were written", file=sys.stderr)
            return 2
        if args.apply:
            apply_plan(target, plan)
        print_report(
            target,
            components,
            plan,
            applied=args.apply,
            json_output=args.json_output,
        )
        if any(entry.status == "conflict" for entry in plan):
            return 2
        return 0
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"workspace-kit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

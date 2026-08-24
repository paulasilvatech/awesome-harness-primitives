#!/usr/bin/env python3
"""Audit the complete plugin marketplace and generate a deterministic report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

try:
    from _layout import HARNESS_ROOT, MARKETPLACE_PATH, PLUGIN_ROOT, REPO_ROOT, SHARED_COMPONENT_SOURCE
    from _plugin_governance import classify
    from _plugin_sources import load_plugin_sources
    from validate_primitives import (
        OPEN_MCP_SCHEMA,
        PL_VALID_KEYS,
    )
except ModuleNotFoundError:  # pragma: no cover
    from ._layout import HARNESS_ROOT, MARKETPLACE_PATH, PLUGIN_ROOT, REPO_ROOT, SHARED_COMPONENT_SOURCE
    from ._plugin_governance import classify
    from ._plugin_sources import load_plugin_sources
    from .validate_primitives import (
        OPEN_MCP_SCHEMA,
        PL_VALID_KEYS,
    )

REPORT_PATH = REPO_ROOT / "docs" / "PLUGIN-AUDIT.md"
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
COPILOT_SDK_VERSION = "1.0.11-preview.2"
PLAYWRIGHT_VERSION = "1.62.1"


@dataclass(frozen=True)
class PluginRow:
    name: str
    version: str
    source: str
    lifecycle: str
    assurance: str
    provenance: str
    last_runtime_probe: str
    agents: int
    skills: int
    hooks: int
    mcp_servers: int
    extensions: int


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def string_list(value: Any, *, field: str, errors: list[str], plugin: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{plugin}: `{field}` must be a list of strings")
        return []
    if len(value) != len(set(value)):
        errors.append(f"{plugin}: `{field}` contains duplicates")
    return value


def names_from_refs(refs: list[str]) -> set[str]:
    return {Path(ref.rstrip("/")).name for ref in refs}


def audit_plugin(
    plugin_dir: Path,
    marketplace: dict[str, dict[str, Any]],
    source_config: dict[str, Any],
    as_of: date,
) -> tuple[PluginRow, list[str]]:
    errors: list[str] = []
    manifest_path = plugin_dir / "plugin.json"
    if not manifest_path.is_file():
        raise ValueError(f"{plugin_dir.name}: plugin.json is missing")
    manifest = read_json(manifest_path)
    name = manifest.get("name")
    if name != plugin_dir.name:
        errors.append(f"{plugin_dir.name}: manifest name must match directory")
    name = name if isinstance(name, str) else plugin_dir.name
    version = manifest.get("version")
    version = version if isinstance(version, str) else ""
    if "$schema" in manifest:
        errors.append(
            f"{name}: flat GitHub Copilot manifests must not declare $schema")
    extra_keys = sorted(set(manifest) - PL_VALID_KEYS)
    if extra_keys:
        errors.append(
            f"{name}: unsupported top-level fields: {', '.join(extra_keys)}")
    if (plugin_dir / ".mcp.json").exists():
        errors.append(f"{name}: legacy .mcp.json must be migrated to mcp.json")

    if (plugin_dir / "com.github.copilot").exists():
        errors.append(f"{name}: com.github.copilot directory is prohibited")

    source = source_config.get("componentSource")
    if source not in {SHARED_COMPONENT_SOURCE, "plugin"}:
        errors.append(
            f"{name}: componentSource must be {SHARED_COMPONENT_SOURCE} or plugin")
        source = "unknown"
    runtime_agents = {
        path.name
        for path in (plugin_dir / "agents").glob("*.agent.md")
    }
    runtime_skills = {
        path.name
        for path in (plugin_dir / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    } if (plugin_dir / "skills").is_dir() else set()

    if source == SHARED_COMPONENT_SOURCE:
        agent_refs = string_list(
            source_config.get("agents"), field="agents", errors=errors, plugin=name
        )
        skill_refs = string_list(
            source_config.get("skills"), field="skills", errors=errors, plugin=name
        )
        if runtime_agents != names_from_refs(agent_refs):
            errors.append(
                f"{name}: runtime agent mirror differs from library references")
        if runtime_skills != names_from_refs(skill_refs):
            errors.append(
                f"{name}: runtime skills differ from shared-source references")
        for ref in (*agent_refs, *skill_refs):
            source_path = HARNESS_ROOT / ref.removeprefix("./").rstrip("/")
            if not source_path.exists():
                errors.append(
                    f"{name}: canonical shared source is missing: {ref}")
    elif source == "plugin":
        shared_skill_refs = string_list(
            source_config.get("sharedSkills", []),
            field="sharedSkills",
            errors=errors,
            plugin=name,
        )
        if not all(
            ref.startswith("./skills/") and ref.endswith("/")
            for ref in shared_skill_refs
        ):
            errors.append(
                f"{name}: sharedSkills must contain ./skills/<name>/ references"
            )
        shared_skill_names = names_from_refs(shared_skill_refs)
        canonical_agents = {path.name for path in (
            plugin_dir / "agents").glob("*.agent.md")}
        canonical_skills = {
            path.name
            for path in (plugin_dir / "skills").iterdir()
            if path.is_dir()
            and (path / "SKILL.md").is_file()
            and path.name not in shared_skill_names
        } if (plugin_dir / "skills").is_dir() else set()
        if runtime_agents != canonical_agents:
            errors.append(
                f"{name}: runtime agent mirror differs from plugin sources")
        if runtime_skills != canonical_skills | shared_skill_names:
            errors.append(
                f"{name}: runtime skills differ from plugin and shared sources"
            )
        for ref in shared_skill_refs:
            source_path = HARNESS_ROOT / ref.removeprefix("./").rstrip("/")
            if not (source_path / "SKILL.md").is_file():
                errors.append(
                    f"{name}: shared canonical skill is missing: {ref}")

    extension_refs = string_list(
        source_config.get("extensionSources", []),
        field="extensionSources",
        errors=errors,
        plugin=name,
    )
    runtime_extensions = {
        path.name
        for path in (plugin_dir / "extensions").iterdir()
        if path.is_dir()
    } if (plugin_dir / "extensions").is_dir() else set()
    if runtime_extensions != names_from_refs(extension_refs):
        errors.append(
            f"{name}: runtime extension mirror differs from canonical extensions")
    if extension_refs:
        if source_config.get("extensionLayoutVersion") != 1:
            errors.append(f"{name}: extensionLayoutVersion must equal 1")
        if source_config.get("upstreamRepository") != "https://github.com/github/awesome-copilot":
            errors.append(
                f"{name}: extension upstreamRepository is missing or unexpected")
        upstream_commit = source_config.get("upstreamCommit")
        if not isinstance(upstream_commit, str) or not COMMIT_SHA.fullmatch(upstream_commit):
            errors.append(
                f"{name}: extension upstreamCommit must be a full Git commit SHA")
    for ref in extension_refs:
        source_path = plugin_dir / ref.removeprefix("./").rstrip("/")
        if not source_path.is_dir():
            errors.append(
                f"{name}: canonical extension source is missing: {ref}")
            continue
        package_path = source_path / "package.json"
        if package_path.is_file():
            package = read_json(package_path)
            dependencies = package.get("dependencies")
            if isinstance(dependencies, dict):
                if (
                    "@github/copilot-sdk" in dependencies
                    and dependencies["@github/copilot-sdk"] != COPILOT_SDK_VERSION
                ):
                    errors.append(
                        f"{name}: @github/copilot-sdk must be pinned")
                if "playwright" in dependencies and dependencies["playwright"] != PLAYWRIGHT_VERSION:
                    errors.append(f"{name}: Playwright must be pinned")

    hook_count = 0
    hook_source = source_config.get("hookSource")
    if hook_source is not None:
        if not isinstance(hook_source, str) or not (
            plugin_dir / hook_source.removeprefix("./")
        ).is_file():
            errors.append(f"{name}: hookSource is invalid or missing")
        expected_hook = hook_source.removeprefix(
            "./") if isinstance(hook_source, str) else ""
        if manifest.get("hooks") != expected_hook:
            errors.append(
                f"{name}: hooks manifest field differs from canonical source")
        if isinstance(hook_source, str) and (plugin_dir / expected_hook).is_file():
            hook_count = 1

    if runtime_agents:
        if manifest.get("agents") != "agents/":
            errors.append(f"{name}: agents manifest field must equal agents/")
    elif "agents" in manifest:
        errors.append(
            f"{name}: agents manifest field exists but agents/ is empty")
    if runtime_skills:
        if manifest.get("skills") != "skills/":
            errors.append(f"{name}: skills manifest field must equal skills/")
    elif "skills" in manifest:
        errors.append(
            f"{name}: skills manifest field exists but skills/ is empty")
    expected_extension_paths = [
        ref.removeprefix("./") for ref in extension_refs
    ]
    manifest_extensions = manifest.get("extensions", [])
    manifest_extension_paths = (
        [manifest_extensions]
        if isinstance(manifest_extensions, str)
        else manifest_extensions
    )
    if manifest_extension_paths != expected_extension_paths:
        errors.append(
            f"{name}: extensions manifest field differs from canonical sources")

    mcp_count = 0
    mcp_path = plugin_dir / "mcp.json"
    if mcp_path.is_file():
        if manifest.get("mcpServers") != "mcp.json":
            errors.append(
                f"{name}: mcpServers manifest field must equal mcp.json")
        mcp = read_json(mcp_path)
        if mcp.get("$schema") != OPEN_MCP_SCHEMA:
            errors.append(
                f"{name}: mcp.json requires the Agent Plugins 1.0 MCP schema")
        servers = mcp.get("mcpServers")
        if not isinstance(servers, dict):
            errors.append(f"{name}: mcpServers must be an object")
        else:
            mcp_count = len(servers)
    elif "mcpServers" in manifest:
        errors.append(
            f"{name}: mcpServers field exists but mcp.json is missing")

    if not (runtime_agents or runtime_skills or runtime_extensions or hook_count or mcp_count):
        errors.append(f"{name}: plugin has no installable component")

    entry = marketplace.get(name)
    if entry is None:
        errors.append(f"{name}: marketplace entry is missing")
    else:
        if entry.get("source") != f"./harness/github-copilot/plugins/{name}":
            errors.append(f"{name}: marketplace source is incorrect")
        if entry.get("version") != version:
            errors.append(f"{name}: marketplace version differs from manifest")
        if entry.get("description") != manifest.get("description"):
            errors.append(
                f"{name}: marketplace description differs from manifest")

    classification = classify(
        version=version,
        source_config=source_config,
        mcp_servers=mcp_count,
        hooks=hook_count,
        extensions=len(runtime_extensions),
        as_of=as_of,
    )

    return (
        PluginRow(
            name=name,
            version=version,
            source=str(source),
            lifecycle=classification.lifecycle,
            assurance=classification.assurance,
            provenance=classification.provenance,
            last_runtime_probe=classification.last_runtime_probe or "—",
            agents=len(runtime_agents),
            skills=len(runtime_skills),
            hooks=hook_count,
            mcp_servers=mcp_count,
            extensions=len(runtime_extensions),
        ),
        errors,
    )


def render_report(rows: list[PluginRow]) -> str:
    totals: Counter[str] = Counter()
    modes = Counter(row.source for row in rows)
    lifecycles = Counter(row.lifecycle for row in rows)
    assurances = Counter(row.assurance for row in rows)
    provenances = Counter(row.provenance for row in rows)
    for row in rows:
        totals["agents"] += row.agents
        totals["skills"] += row.skills
        totals["hooks"] += row.hooks
        totals["mcp"] += row.mcp_servers
        totals["extensions"] += row.extensions
    lines = [
        "# Plugin Marketplace Audit",
        "",
        "Generated by `python3 harness/github-copilot/scripts/audit_plugins.py` from the committed marketplace and self-contained plugin packages.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Plugin packages | {len(rows)} |",
        f"| Marketplace entries | {len(rows)} |",
        f"| Shared-source packages | {modes[SHARED_COMPONENT_SOURCE]} |",
        f"| Plugin-owned packages | {modes['plugin']} |",
        f"| Active lifecycle | {lifecycles['active']} |",
        f"| Incubating lifecycle | {lifecycles['incubating']} |",
        f"| Deprecated lifecycle | {lifecycles['deprecated']} |",
        f"| Runtime-verified assurance | {assurances['runtime-verified']} |",
        f"| Runtime-stale assurance | {assurances['runtime-stale']} |",
        f"| Runtime-required assurance | {assurances['runtime-required']} |",
        f"| Static-validated assurance | {assurances['static-validated']} |",
        f"| Repository provenance | {provenances['repository']} |",
        f"| Upstream-mirror provenance | {provenances['upstream-mirror']} |",
        f"| Packaged agents | {totals['agents']} |",
        f"| Installed skills | {totals['skills']} |",
        f"| Hook packages | {totals['hooks']} |",
        f"| MCP servers | {totals['mcp']} |",
        f"| Client extensions | {totals['extensions']} |",
        "",
        "## Policy",
        "",
        "- Every package uses the flat GitHub Copilot manifest documented for direct `agents/`, `skills/`, `hooks/`, `extensions/`, and MCP paths.",
        "- Shared agents and skills are materialized directly under each package's `agents/` and `skills/` directories.",
        "- Plugin-owned agents, hooks, and client extensions remain canonical at the plugin root; `com.github.copilot/` directories are prohibited.",
        "- Root `mcp.json` uses the portable MCP schema and is declared through `mcpServers`; `.mcp.json` is rejected.",
        "- Marketplace source, version, description, coverage, uniqueness, and ordering are validated.",
        "- Lifecycle, assurance, and provenance are descriptive classifications: they never remove, hide, or block a package.",
        "- `incubating` is derived from a `0.x` manifest version; `deprecated` requires recorded evidence.",
        "- `runtime-verified` requires a dated representative probe within 90 days; older probes become `runtime-stale`.",
        "- Packages shipping MCP servers, hooks, or client extensions are never `static-validated`, because static checks do not exercise those surfaces.",
        "- `python3 harness/github-copilot/scripts/normalize_plugin_manifests.py --check` and `python3 harness/github-copilot/scripts/sync_plugin_components.py --check` are required drift gates.",
        "- Awesome Copilot client extensions record their exact upstream commit and pin runtime dependencies; refreshes use `import_awesome_copilot_extensions.py` with a clean checkout.",
        "",
        "Current platform and upstream verification evidence is recorded in `docs/HARNESS-VALIDATION.md`.",
        "",
        "## Packages",
        "",
        "| Plugin | Version | Source | Lifecycle | Assurance | Provenance | Last probe | Agents | Skills | Hooks | MCP | Extensions |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row.name} | {row.version} | {row.source} | {row.lifecycle} | "
            f"{row.assurance} | {row.provenance} | {row.last_runtime_probe} | "
            f"{row.agents} | {row.skills} | {row.hooks} | {row.mcp_servers} | "
            f"{row.extensions} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit plugin manifests, components, and marketplace.")
    parser.add_argument("--check", action="store_true",
                        help="fail if the report is stale")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    marketplace_data = read_json(MARKETPLACE_PATH)
    entries = marketplace_data.get("plugins")
    if not isinstance(entries, list):
        print("marketplace plugins must be a list", file=sys.stderr)
        return 1
    marketplace: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    names: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            errors.append("marketplace entries must be named objects")
            continue
        name = entry["name"]
        names.append(name)
        if name in marketplace:
            errors.append(f"{name}: duplicate marketplace entry")
        marketplace[name] = entry
    if names != sorted(names, key=str.casefold):
        errors.append("marketplace entries must be alphabetized")

    rows: list[PluginRow] = []
    source_map = load_plugin_sources()
    as_of = date.today()
    plugin_dirs = sorted(
        (path for path in PLUGIN_ROOT.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    )
    for plugin_dir in plugin_dirs:
        try:
            source_config = source_map.get(plugin_dir.name)
            if source_config is None:
                raise ValueError(
                    f"{plugin_dir.name}: source metadata is missing")
            row, findings = audit_plugin(
                plugin_dir, marketplace, source_config, as_of)
            rows.append(row)
            errors.extend(findings)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    extra_entries = sorted(set(marketplace) - {row.name for row in rows})
    errors.extend(
        f"{name}: marketplace source directory is missing" for name in extra_entries)
    extra_sources = sorted(set(source_map) - {row.name for row in rows})
    errors.extend(
        f"{name}: source metadata directory is missing" for name in extra_sources)

    if errors:
        print("Plugin audit failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    report = render_report(rows)
    if args.json_output:
        print(json.dumps([asdict(row)
              for row in rows], indent=2, sort_keys=True))
        return 0
    if args.check:
        if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != report:
            print(
                "docs/PLUGIN-AUDIT.md is stale; run python3 harness/github-copilot/scripts/audit_plugins.py",
                file=sys.stderr,
            )
            return 1
        return 0
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(
        f"Audited {len(rows)} plugins and wrote {REPORT_PATH.relative_to(REPO_ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

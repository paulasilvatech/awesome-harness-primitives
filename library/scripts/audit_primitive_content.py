#!/usr/bin/env python3
"""Inventory primitive content, freshness risks, and plugin distribution coverage."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

try:
    from validate_primitives import (
        ALL_KINDS,
        REPOSITORY_EXTENSION,
        Validator,
        find_repo_root,
        parse_frontmatter,
    )
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from .validate_primitives import (
        ALL_KINDS,
        REPOSITORY_EXTENSION,
        Validator,
        find_repo_root,
        parse_frontmatter,
    )

REPO_ROOT = find_repo_root(Path(__file__).resolve())
LIBRARY_ROOT = REPO_ROOT / "library"
PLUGIN_ROOT = LIBRARY_ROOT / "plugins"
MARKETPLACE_PATH = REPO_ROOT / ".github" / "plugin" / "marketplace.json"
EVIDENCE_PATH = REPO_ROOT / "docs" / "HARNESS-VALIDATION.md"
REPORT_PATH = REPO_ROOT / "docs" / "PRIMITIVE-CONTENT-AUDIT.md"
LEDGER_PATH = REPO_ROOT / "docs" / "PRIMITIVE-CONTENT-AUDIT.json"
PLUGIN_MANIFEST_NAME = "plugin.json"
AGENT_GLOB = "*.agent.md"

TEXT_SUFFIXES = {
    ".bicep",
    ".c",
    ".cs",
    ".css",
    ".go",
    ".h",
    ".hcl",
    ".html",
    ".java",
    ".js",
    ".json",
    ".jsonc",
    ".jsx",
    ".md",
    ".mjs",
    ".ps1",
    ".py",
    ".rs",
    ".sh",
    ".sql",
    ".tf",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "bin",
    "build",
    "dist",
    "node_modules",
    "obj",
    "venv",
}
URL_RE = re.compile(r"https?://[^\s<>)\]}'\"]+")
CURRENCY_RE = re.compile(
    r"\b(?:current|currently|latest|newest|most recent|up-to-date)\b",
    re.IGNORECASE,
)
LIFECYCLE_RE = re.compile(
    r"\b(?:alpha|beta|preview|prerelease|release candidate|deprecated|obsolete|"
    r"removed|retired|end[- ]of[- ]life|eol)\b",
    re.IGNORECASE,
)
VERSION_RE = re.compile(
    r"\b(?:v?\d+\.\d+(?:\.\d+)?(?:[-+][0-9A-Za-z.-]+)?|"
    r"(?:Java|JDK|Python|Node(?:\.js)?|React|Angular|Vue|Spring Boot|"
    r"\.NET|TypeScript|Terraform|Kubernetes|GitHub Copilot CLI)\s+v?\d+(?:\.\d+){0,2})\b",
    re.IGNORECASE,
)
DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")


@dataclass(frozen=True)
class ContentUnit:
    kind: str
    name: str
    path: str
    ownership: str
    package: str | None
    files_scanned: int
    characters_scanned: int
    external_url_count: int
    source_domains: list[str]
    signals: list[str]
    review_status: str
    local_evidence_mention: bool
    packaged_by: list[str]


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def plugin_manifest_dirs() -> list[Path]:
    return sorted(
        (
            path
            for path in PLUGIN_ROOT.iterdir()
            if path.is_dir() and (path / PLUGIN_MANIFEST_NAME).is_file()
        ),
        key=lambda path: path.name.casefold(),
    )


def repository_config(data: dict[str, Any]) -> dict[str, Any]:
    extensions = data.get("extensions")
    if not isinstance(extensions, dict):
        return {}
    config = extensions.get(REPOSITORY_EXTENSION)
    return config if isinstance(config, dict) else {}


def text_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path
        return
    if not path.is_dir():
        return
    for candidate in sorted(path.rglob("*")):
        if not candidate.is_file():
            continue
        rel_parts = candidate.relative_to(path).parts
        if any(part in EXCLUDED_PARTS for part in rel_parts):
            continue
        if candidate.suffix.lower() in TEXT_SUFFIXES:
            yield candidate


def collect_text(paths: Iterable[Path], unreadable: list[str]) -> tuple[str, int]:
    files: dict[str, Path] = {}
    for path in paths:
        for candidate in text_files(path):
            files[candidate.as_posix()] = candidate
    chunks: list[str] = []
    for key in sorted(files):
        path = files[key]
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            unreadable.append(f"{relative(path)}: {exc}")
    return "\n".join(chunks), len(files)


def clean_urls(text: str) -> list[str]:
    return sorted({url.rstrip(".,;:") for url in URL_RE.findall(text)})


def review_signals(text: str, urls: list[str]) -> list[str]:
    signals: list[str] = []
    if CURRENCY_RE.search(text):
        signals.append("currency-language")
    if LIFECYCLE_RE.search(text):
        signals.append("lifecycle-language")
    if VERSION_RE.search(text):
        signals.append("version-claim")
    if DATE_RE.search(text):
        signals.append("date-claim")
    if urls:
        signals.append("external-source")
    return signals


def review_status(signals: list[str]) -> str:
    if any(
        signal in signals
        for signal in ("currency-language", "lifecycle-language", "version-claim", "date-claim")
    ):
        return "needs-current-source-review"
    if "external-source" in signals:
        return "needs-source-review"
    return "needs-semantic-review"


def parse_name(path: Path, kind: str) -> str:
    required = kind != "instruction"
    metadata, _body, present, error = parse_frontmatter(
        path.read_text(encoding="utf-8"),
        required=required,
    )
    if present and not error:
        name = metadata.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    if kind == "agent":
        return path.name.removesuffix(".agent.md")
    if kind == "instruction":
        return path.name.removesuffix(".instructions.md")
    if kind == "prompt":
        return path.name.removesuffix(".prompt.md")
    return path.parent.name


def evidence_mentions(path: str, name: str, evidence: str) -> bool:
    return path in evidence or f"`{name}`" in evidence


def make_unit(
    *,
    kind: str,
    name: str,
    path: Path,
    ownership: str,
    package: str | None,
    scan_paths: Iterable[Path],
    evidence: str,
    packaged_by: Iterable[str] = (),
    unreadable: list[str],
) -> ContentUnit:
    text, files_scanned = collect_text(scan_paths, unreadable)
    urls = clean_urls(text)
    signals = review_signals(text, urls)
    domains = sorted(
        {
            parsed.netloc.casefold()
            for url in urls
            if (parsed := urlparse(url)).netloc
        }
    )
    rel_path = relative(path)
    return ContentUnit(
        kind=kind,
        name=name,
        path=rel_path,
        ownership=ownership,
        package=package,
        files_scanned=files_scanned,
        characters_scanned=len(text),
        external_url_count=len(urls),
        source_domains=domains,
        signals=signals,
        review_status=review_status(signals),
        local_evidence_mention=evidence_mentions(rel_path, name, evidence),
        packaged_by=sorted(set(packaged_by), key=str.casefold),
    )


def shared_packaging() -> tuple[
    dict[str, list[str]],
    dict[str, list[str]],
    dict[str, dict[str, Any]],
]:
    agents: dict[str, list[str]] = defaultdict(list)
    skills: dict[str, list[str]] = defaultdict(list)
    manifests: dict[str, dict[str, Any]] = {}
    for plugin_dir in plugin_manifest_dirs():
        data = read_json(plugin_dir / PLUGIN_MANIFEST_NAME)
        manifests[plugin_dir.name] = data
        config = repository_config(data)
        if config.get("componentSource") != "library":
            continue
        for ref in config.get("agents", []):
            if isinstance(ref, str):
                agents[Path(ref.rstrip("/")).name].append(plugin_dir.name)
        for ref in config.get("skills", []):
            if isinstance(ref, str):
                skills[Path(ref.rstrip("/")).name].append(plugin_dir.name)
    return agents, skills, manifests


def plugin_owned_components(plugin_dir: Path) -> dict[str, list[Path]]:
    return {
        "agent": sorted((plugin_dir / "agents").glob(AGENT_GLOB)),
        "skill": sorted(
            path
            for path in (plugin_dir / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )
        if (plugin_dir / "skills").is_dir()
        else [],
        "instruction": sorted((plugin_dir / "instructions").glob("*.instructions.md")),
        "prompt": sorted((plugin_dir / "prompts").glob("*.prompt.md")),
    }


def plugin_scan_paths(
    plugin_dir: Path,
    data: dict[str, Any],
    components: dict[str, list[Path]],
) -> list[Path]:
    paths = [
        path
        for path in (
            plugin_dir / PLUGIN_MANIFEST_NAME,
            plugin_dir / "mcp.json",
            plugin_dir / "README.md",
            plugin_dir / "LICENSE",
        )
        if path.exists()
    ]
    config = repository_config(data)
    if config.get("componentSource") == "plugin":
        paths.extend(path for values in components.values() for path in values)
        hook_source = config.get("hookSource")
        if isinstance(hook_source, str) and hook_source.startswith("./"):
            hook_path = plugin_dir / hook_source.removeprefix("./")
            paths.append(hook_path.parent)
    extension_sources = config.get("extensionSources")
    if isinstance(extension_sources, list):
        for ref in extension_sources:
            if isinstance(ref, str) and ref.startswith("./"):
                paths.append(plugin_dir / ref.removeprefix("./").rstrip("/"))
    return paths


def validate_plugin_owned(manifests: dict[str, dict[str, Any]]) -> dict[str, int]:
    totals = Counter()
    issue_counts = Counter()
    for plugin_dir in plugin_manifest_dirs():
        data = manifests[plugin_dir.name]
        if repository_config(data).get("componentSource") != "plugin":
            continue
        components = plugin_owned_components(plugin_dir)
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for plural in ("agents", "skills", "instructions", "prompts"):
                (root / plural).mkdir()
            for kind, paths in components.items():
                plural = f"{kind}s"
                for source in paths:
                    target = root / plural / source.name
                    target.symlink_to(source, target_is_directory=source.is_dir())
                    totals[kind] += 1
            validator = Validator(root, quiet=True)
            validator.validate(["agents", "instructions", "skills", "prompts"])
            for finding in validator.findings:
                if finding.severity in {"ERROR", "WARNING"}:
                    issue_counts[finding.severity.casefold()] += 1
    return {
        "agents": totals["agent"],
        "instructions": totals["instruction"],
        "skills": totals["skill"],
        "prompts": totals["prompt"],
        "errors": issue_counts["error"],
        "warnings": issue_counts["warning"],
    }


def strict_validation() -> dict[str, Any]:
    validator = Validator(LIBRARY_ROOT, quiet=True)
    validator.validate(ALL_KINDS)
    return {
        "summary": [
            {
                "kind": kind,
                "files": validator.file_counts.get(kind, 0),
                "errors": sum(
                    finding.kind == kind and finding.severity == "ERROR"
                    for finding in validator.findings
                ),
                "warnings": sum(
                    finding.kind == kind and finding.severity == "WARNING"
                    for finding in validator.findings
                ),
            }
            for kind in ALL_KINDS
        ],
        "errors": sum(finding.severity == "ERROR" for finding in validator.findings),
        "warnings": sum(finding.severity == "WARNING" for finding in validator.findings),
    }


def library_content_units(
    evidence: str,
    agent_packages: dict[str, list[str]],
    skill_packages: dict[str, list[str]],
    unreadable: list[str],
) -> list[ContentUnit]:
    units: list[ContentUnit] = []
    specs = (
        ("agent", sorted((LIBRARY_ROOT / "agents").glob(AGENT_GLOB)), False, agent_packages),
        (
            "instruction",
            sorted((LIBRARY_ROOT / "instructions").glob("*.instructions.md")),
            False,
            {},
        ),
        ("skill", sorted((LIBRARY_ROOT / "skills").glob("*/SKILL.md")), True, skill_packages),
        ("prompt", sorted((LIBRARY_ROOT / "prompts").glob("*.prompt.md")), False, {}),
    )
    for kind, sources, scan_directory, package_map in specs:
        for source in sources:
            unit_path = source.parent if scan_directory else source
            package_key = unit_path.name if scan_directory else source.name
            units.append(
                make_unit(
                    kind=kind,
                    name=parse_name(source, kind),
                    path=unit_path,
                    ownership="library",
                    package=None,
                    scan_paths=[unit_path],
                    evidence=evidence,
                    packaged_by=package_map.get(package_key, []),
                    unreadable=unreadable,
                )
            )
    for path in sorted((LIBRARY_ROOT / "hooks").glob("*/hooks.json")):
        units.append(
            make_unit(
                kind="hook",
                name=path.parent.name,
                path=path.parent,
                ownership="library",
                package=None,
                scan_paths=[path.parent],
                evidence=evidence,
                unreadable=unreadable,
            )
        )
    return units


def plugin_primitive_units(
    plugin_dir: Path,
    components: dict[str, list[Path]],
    evidence: str,
    unreadable: list[str],
) -> list[ContentUnit]:
    units: list[ContentUnit] = []
    for kind, paths in components.items():
        for path in paths:
            source = path / "SKILL.md" if kind == "skill" else path
            units.append(
                make_unit(
                    kind=kind,
                    name=parse_name(source, kind),
                    path=path,
                    ownership="plugin",
                    package=plugin_dir.name,
                    scan_paths=[path],
                    evidence=evidence,
                    packaged_by=[plugin_dir.name],
                    unreadable=unreadable,
                )
            )
    return units


def plugin_hook_unit(
    plugin_dir: Path,
    config: dict[str, Any],
    evidence: str,
    unreadable: list[str],
) -> ContentUnit | None:
    hook_source = config.get("hookSource")
    if not isinstance(hook_source, str) or not hook_source.startswith("./"):
        return None
    hook_path = plugin_dir / hook_source.removeprefix("./")
    return make_unit(
        kind="hook",
        name=f"{plugin_dir.name}:{hook_path.parent.name}",
        path=hook_path.parent,
        ownership="plugin",
        package=plugin_dir.name,
        scan_paths=[hook_path.parent],
        evidence=evidence,
        packaged_by=[plugin_dir.name],
        unreadable=unreadable,
    )


def plugin_content_units(
    evidence: str,
    manifests: dict[str, dict[str, Any]],
    unreadable: list[str],
) -> tuple[list[ContentUnit], int]:
    units: list[ContentUnit] = []
    active_hook_count = 0
    for plugin_dir in plugin_manifest_dirs():
        data = manifests[plugin_dir.name]
        config = repository_config(data)
        components = plugin_owned_components(plugin_dir)
        if config.get("componentSource") == "plugin":
            units.extend(plugin_primitive_units(plugin_dir, components, evidence, unreadable))
        hook_unit = plugin_hook_unit(plugin_dir, config, evidence, unreadable)
        if hook_unit is not None:
            active_hook_count += 1
            units.append(hook_unit)
        units.append(
            make_unit(
                kind="plugin",
                name=plugin_dir.name,
                path=plugin_dir,
                ownership=str(config.get("componentSource", "unknown")),
                package=plugin_dir.name,
                scan_paths=plugin_scan_paths(plugin_dir, data, components),
                evidence=evidence,
                packaged_by=[plugin_dir.name],
                unreadable=unreadable,
            )
        )
    return units, active_hook_count


def build_audit() -> dict[str, Any]:
    evidence = EVIDENCE_PATH.read_text(encoding="utf-8")
    agent_packages, skill_packages, manifests = shared_packaging()
    unreadable: list[str] = []
    units = library_content_units(
        evidence,
        agent_packages,
        skill_packages,
        unreadable,
    )
    plugin_units, active_plugin_hooks = plugin_content_units(
        evidence,
        manifests,
        unreadable,
    )
    units.extend(plugin_units)

    units.sort(key=lambda unit: (unit.kind, unit.name.casefold(), unit.path.casefold()))
    shared_agents = sorted(path.name for path in (LIBRARY_ROOT / "agents").glob(AGENT_GLOB))
    shared_skills = sorted(path.parent.name for path in (LIBRARY_ROOT / "skills").glob("*/SKILL.md"))
    marketplace = read_json(MARKETPLACE_PATH).get("plugins", [])
    validation = strict_validation()
    plugin_owned_validation = validate_plugin_owned(manifests)
    return {
        "schemaVersion": 1,
        "claim": {
            "proves": [
                "all canonical and plugin-owned primitive sources were inventoried",
                "strict structural validation has no errors or warnings",
                "freshness-risk language, version/date claims, and external source domains were indexed",
                "existing plugin and marketplace distribution coverage was measured",
            ],
            "doesNotProve": [
                "every domain statement is semantically correct or current",
                "every external source still resolves or is authoritative",
                "VS Code prompts executed successfully",
                "every client extension was exercised interactively",
                "every technically possible plugin would be coherent or useful",
            ],
        },
        "validation": {
            "sharedLibrary": validation,
            "pluginOwned": plugin_owned_validation,
        },
        "packaging": {
            "pluginPackages": len(manifests),
            "marketplaceEntries": len(marketplace) if isinstance(marketplace, list) else 0,
            "sharedAgents": {
                "total": len(shared_agents),
                "packaged": sum(name in agent_packages for name in shared_agents),
                "unpackaged": sorted(
                    name for name in shared_agents if name not in agent_packages
                ),
            },
            "sharedSkills": {
                "total": len(shared_skills),
                "packaged": sum(name in skill_packages for name in shared_skills),
                "unpackaged": sorted(
                    name for name in shared_skills if name not in skill_packages
                ),
            },
            "pluginOwned": plugin_owned_validation,
            "activePluginHookPackages": active_plugin_hooks,
        },
        "unreadableFiles": sorted(unreadable),
        "units": [asdict(unit) for unit in units],
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(str(value).replace("|", "\\|") for value in row)
            + " |"
        )
    return "\n".join(lines)


def render_report(audit: dict[str, Any]) -> str:
    units = audit["units"]
    by_kind = Counter(unit["kind"] for unit in units)
    by_ownership = Counter((unit["kind"], unit["ownership"]) for unit in units)
    signals = Counter()
    statuses = Counter()
    evidence = Counter()
    for unit in units:
        statuses[(unit["kind"], unit["review_status"])] += 1
        evidence[unit["kind"]] += bool(unit["local_evidence_mention"])
        for signal in unit["signals"]:
            signals[(unit["kind"], signal)] += 1

    kind_order = ("agent", "instruction", "skill", "prompt", "hook", "plugin")
    source_rows = [
        [
            kind,
            by_kind[kind],
            by_ownership[(kind, "library")],
            by_ownership[(kind, "plugin")],
            evidence[kind],
        ]
        for kind in kind_order
    ]
    risk_rows = [
        [
            kind,
            signals[(kind, "currency-language")],
            signals[(kind, "lifecycle-language")],
            signals[(kind, "version-claim")],
            signals[(kind, "date-claim")],
            signals[(kind, "external-source")],
            statuses[(kind, "needs-current-source-review")],
            statuses[(kind, "needs-source-review")],
            statuses[(kind, "needs-semantic-review")],
        ]
        for kind in kind_order
    ]
    packaging = audit["packaging"]
    shared_agents = packaging["sharedAgents"]
    shared_skills = packaging["sharedSkills"]
    plugin_owned = packaging["pluginOwned"]
    shared_validation = audit["validation"]["sharedLibrary"]

    return f"""# Primitive Content Audit

Generated by `python3 library/scripts/audit_primitive_content.py`.

## Audit claim

This is a complete deterministic inventory of shared-library primitives, plugin-owned primitives, and
plugin package surfaces. It proves structural validity, distribution coverage, and which content contains
freshness-risk signals. It does **not** certify that every domain statement is semantically correct or
current. A file remains in a semantic review state until its relevant claims are checked against dated
first-party evidence and its runtime surface is exercised where applicable.

## Structural coverage

{markdown_table(
    ["Content type", "Sources", "Library-owned", "Plugin-owned", "Mentioned in dated evidence"],
    source_rows,
)}

- Shared-library strict validation: {shared_validation["errors"]} errors, {shared_validation["warnings"]} warnings.
- Plugin-owned primitive validation: {plugin_owned["errors"]} errors, {plugin_owned["warnings"]} warnings.
- Unreadable text files: {len(audit["unreadableFiles"])}.
- Full per-source ledger: `docs/PRIMITIVE-CONTENT-AUDIT.json`.

The “mentioned in dated evidence” column is only an index hint. A mention in
`docs/HARNESS-VALIDATION.md` does not certify every statement in that source.

## Freshness review inventory

{markdown_table(
    [
        "Content type",
        "Currency wording",
        "Lifecycle wording",
        "Version claims",
        "Date claims",
        "External sources",
        "Current-source review",
        "Source review",
        "Semantic review",
    ],
    risk_rows,
)}

These are review signals, not automatic defects. Code samples naturally contain versions and URLs, while
words such as “latest”, “preview”, “deprecated”, and “current” require dated evidence before delivery.

## Plugin composition coverage

| Metric | Count |
| --- | ---: |
| Existing plugin packages | {packaging["pluginPackages"]} |
| Marketplace entries | {packaging["marketplaceEntries"]} |
| Shared agents packaged | {shared_agents["packaged"]} / {shared_agents["total"]} |
| Shared agents not packaged | {len(shared_agents["unpackaged"])} |
| Shared skills packaged | {shared_skills["packaged"]} / {shared_skills["total"]} |
| Shared skills not packaged | {len(shared_skills["unpackaged"])} |
| Plugin-owned agents | {plugin_owned["agents"]} |
| Plugin-owned skills | {plugin_owned["skills"]} |
| Plugin-owned workspace instructions | {plugin_owned["instructions"]} |
| Plugin-owned VS Code prompts | {plugin_owned["prompts"]} |
| Active plugin hook packages | {packaging["activePluginHookPackages"]} |

The {len(shared_agents["unpackaged"]) + len(shared_skills["unpackaged"])} unreferenced shared agents and
skills are **composition candidates**, not missing plugins by definition. A new plugin is justified only
when those components form one coherent installable capability without duplicating an existing package.
Instructions and VS Code prompts are not portable core Agent Plugins 1.0 components; publish them through
an explicit workspace kit when a plugin genuinely depends on them. Hook packaging also requires an
explicit safety and side-effect review.

## Completion criteria for semantic currency

1. Review each `needs-current-source-review` row in the JSON ledger against a dated first-party source.
2. Review each `needs-source-review` row for source authority, link health, and scope.
3. Review each remaining `needs-semantic-review` row for domain correctness even when no volatile phrase
   was detected.
4. Exercise changed prompts with **Chat: Run Prompt**, hook packages with representative JSON payloads,
   agents and skills with representative invocations, and client extensions interactively when supported.
5. Record only repeated, relevant verification in `docs/HARNESS-VALIDATION.md`; never convert this risk
   inventory into a blanket “all content is current” claim.
"""


def has_strict_issues(audit: dict[str, Any]) -> bool:
    shared = audit["validation"]["sharedLibrary"]
    plugin_owned = audit["validation"]["pluginOwned"]
    return bool(
        shared["errors"]
        or shared["warnings"]
        or plugin_owned["errors"]
        or plugin_owned["warnings"]
        or audit["unreadableFiles"]
    )


def stale_outputs(ledger: str, report: str) -> list[str]:
    stale: list[str] = []
    if not LEDGER_PATH.is_file() or LEDGER_PATH.read_text(encoding="utf-8") != ledger:
        stale.append(relative(LEDGER_PATH))
    if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != report:
        stale.append(relative(REPORT_PATH))
    return stale


def report_stale_outputs(stale: list[str]) -> None:
    print(
        "Primitive content audit is stale; run "
        "python3 library/scripts/audit_primitive_content.py",
        file=sys.stderr,
    )
    for path in stale:
        print(f"  - {path}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit primitive content risks and plugin distribution coverage."
    )
    parser.add_argument("--check", action="store_true", help="fail if committed reports are stale")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    audit = build_audit()
    ledger = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    report = render_report(audit)
    if args.json_output:
        print(ledger, end="")
        return 1 if has_strict_issues(audit) else 0
    if args.check:
        stale = stale_outputs(ledger, report)
        if stale:
            report_stale_outputs(stale)
            return 1
        return 1 if has_strict_issues(audit) else 0

    LEDGER_PATH.write_text(ledger, encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(
        f"Audited {len(audit['units'])} content units and wrote "
        f"{relative(REPORT_PATH)} plus {relative(LEDGER_PATH)}."
    )
    return 1 if has_strict_issues(audit) else 0


if __name__ == "__main__":
    raise SystemExit(main())

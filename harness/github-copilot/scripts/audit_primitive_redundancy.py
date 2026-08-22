#!/usr/bin/env python3
"""Detect exact and high-similarity canonical primitive redundancy."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from _layout import HARNESS_ROOT, PLUGIN_ROOT, REPO_ROOT
    from _plugin_sources import load_plugin_sources
    from validate_primitives import parse_frontmatter
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._layout import HARNESS_ROOT, PLUGIN_ROOT, REPO_ROOT
    from ._plugin_sources import load_plugin_sources
    from .validate_primitives import parse_frontmatter

REPORT_PATH = REPO_ROOT / "docs" / "PRIMITIVE-REDUNDANCY.md"
LEDGER_PATH = REPO_ROOT / "docs" / "PRIMITIVE-REDUNDANCY.json"
SIMILARITY_THRESHOLD = 0.72
PLUGIN_SOURCES = load_plugin_sources()
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "user",
    "users",
    "using",
    "when",
    "with",
    "agent",
    "instructions",
    "prompt",
    "skill",
}


@dataclass(frozen=True)
class Primitive:
    kind: str
    name: str
    description: str
    path: str
    ownership: str
    package: str | None
    body_hash: str
    tokens: list[str]


@dataclass(frozen=True)
class Candidate:
    kind: str
    left: str
    right: str
    similarity: float
    classification: str
    rationale: str


CLASSIFICATIONS: dict[frozenset[str], tuple[str, str]] = {
    frozenset(
        {
            "agents/csharp-mcp-expert.agent.md",
            "agents/typescript-mcp-expert.agent.md",
        }
    ): ("language-variant", "Different MCP SDK, runtime, examples, and build/test conventions."),
    frozenset(
        {
            "agents/csharp-mcp-expert.agent.md",
            "agents/python-mcp-expert.agent.md",
        }
    ): ("language-variant", "Different MCP SDK, runtime, examples, and build/test conventions."),
    frozenset(
        {
            "agents/python-mcp-expert.agent.md",
            "agents/typescript-mcp-expert.agent.md",
        }
    ): ("language-variant", "Different MCP SDK, runtime, examples, and build/test conventions."),
    frozenset(
        {
            "agents/azure-verified-modules-bicep.agent.md",
            "agents/azure-verified-modules-terraform.agent.md",
        }
    ): ("language-variant", "Bicep and Terraform use different providers, tooling, and module contracts."),
    frozenset(
        {
            "instructions/convert-cassandra-to-spring-data-cosmos.instructions.md",
            "instructions/convert-jpa-to-spring-data-cosmos.instructions.md",
        }
    ): ("source-framework-variant", "Migration sources, mappings, dependencies, and validation differ."),
    frozenset(
        {
            "instructions/python-mcp-server.instructions.md",
            "instructions/typescript-mcp-server.instructions.md",
        }
    ): ("language-variant", "Different MCP SDK and language-specific implementation conventions."),
    frozenset(
        {
            "skills/create-implementation-plan/SKILL.md",
            "skills/update-implementation-plan/SKILL.md",
        }
    ): ("lifecycle-variant", "Creation and mutation have different inputs, preservation rules, and outputs."),
    frozenset(
        {
            "skills/create-llms/SKILL.md",
            "skills/update-llms/SKILL.md",
        }
    ): ("lifecycle-variant", "Creation and synchronization of an existing llms.txt are distinct operations."),
    frozenset(
        {
            "skills/create-spring-boot-java-project/SKILL.md",
            "skills/create-spring-boot-kotlin-project/SKILL.md",
        }
    ): ("language-variant", "Java and Kotlin project generators use different source and build conventions."),
    frozenset(
        {
            "skills/mcp-copilot-studio-server-generator/SKILL.md",
            "skills/power-platform-mcp-connector-suite/SKILL.md",
        }
    ): (
        "specialization",
        "One generates the MCP server plus connector; the other focuses on connector packaging and validation.",
    ),
    frozenset(
        {
            "prompts/containerize-aspnet-framework.prompt.md",
            "prompts/containerize-aspnetcore.prompt.md",
        }
    ): ("framework-variant", ".NET Framework and ASP.NET Core require different Windows/Linux artifacts."),
}


def relative(path: Path) -> str:
    return path.relative_to(HARNESS_ROOT).as_posix()


def tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.casefold())
        if token not in STOP_WORDS and len(token) > 1
    ]


def cosine(left: list[str], right: list[str]) -> float:
    left_counts = Counter(left)
    right_counts = Counter(right)
    if not left_counts or not right_counts:
        return 0.0
    dot = sum(
        left_counts[token] * right_counts[token]
        for token in left_counts.keys() & right_counts.keys()
    )
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return dot / (left_norm * right_norm)


def normalized_body(body: str) -> str:
    return re.sub(r"\s+", " ", body).strip().casefold()


def primitive(
    path: Path,
    kind: str,
    ownership: str,
    package: str | None,
) -> Primitive:
    required = kind != "instruction"
    data, body, present, error = parse_frontmatter(
        path.read_text(encoding="utf-8"),
        required=required,
    )
    if not present or error:
        raise ValueError(f"{path}: invalid frontmatter: {error or 'missing'}")
    fallback_name = path.parent.name if kind == "skill" else path.name.split(".", 1)[0]
    name = str(data.get("name") or fallback_name)
    description = str(data.get("description") or "")
    normalized = normalized_body(body)
    return Primitive(
        kind=kind,
        name=name,
        description=description,
        path=relative(path),
        ownership=ownership,
        package=package,
        body_hash=hashlib.sha256(normalized.encode()).hexdigest(),
        tokens=tokens(f"{name} {description}"),
    )


def shared_primitives() -> Iterable[Primitive]:
    specs = (
        ("agent", (HARNESS_ROOT / "agents").glob("*.agent.md")),
        ("instruction", (HARNESS_ROOT / "instructions").glob("*.instructions.md")),
        ("skill", (HARNESS_ROOT / "skills").glob("*/SKILL.md")),
        ("prompt", (HARNESS_ROOT / "prompts").glob("*.prompt.md")),
    )
    for kind, paths in specs:
        for path in sorted(paths):
            yield primitive(path, kind, "shared", None)


def plugin_primitives() -> Iterable[Primitive]:
    specs = (
        ("agent", "agents", "*.agent.md"),
        ("instruction", "instructions", "*.instructions.md"),
        ("skill", "skills", "*/SKILL.md"),
        ("prompt", "prompts", "*.prompt.md"),
    )
    for plugin_dir in sorted(path for path in PLUGIN_ROOT.iterdir() if path.is_dir()):
        manifest = plugin_dir / "plugin.json"
        if not manifest.is_file():
            continue
        repository = PLUGIN_SOURCES.get(plugin_dir.name, {})
        if repository.get("componentSource") != "plugin":
            continue
        shared_skill_names = {
            Path(ref.rstrip("/")).name
            for ref in repository.get("sharedSkills", [])
            if isinstance(ref, str)
        }
        for kind, folder, pattern in specs:
            for path in sorted((plugin_dir / folder).glob(pattern)):
                if kind == "skill" and path.parent.name in shared_skill_names:
                    continue
                yield primitive(path, kind, "plugin", plugin_dir.name)


def classify(left: Primitive, right: Primitive) -> tuple[str, str]:
    key = frozenset({left.path, right.path})
    if key in CLASSIFICATIONS:
        return CLASSIFICATIONS[key]
    names = {Path(left.path).name, Path(right.path).name}
    if all(name.startswith("copilot-sdk-") for name in names):
        return (
            "language-variant",
            "GitHub Copilot SDK guidance is intentionally specialized by programming language.",
        )
    return "unclassified", "Requires responsibility-boundary review."


def build_audit() -> dict[str, Any]:
    primitives = sorted(
        [*shared_primitives(), *plugin_primitives()],
        key=lambda item: (item.kind, item.path.casefold()),
    )
    hashes: dict[tuple[str, str], list[str]] = defaultdict(list)
    for item in primitives:
        hashes[(item.kind, item.body_hash)].append(item.path)
    exact_groups = sorted(
        sorted(paths)
        for paths in hashes.values()
        if len(paths) > 1
    )

    candidates: list[Candidate] = []
    by_kind: dict[str, list[Primitive]] = defaultdict(list)
    for item in primitives:
        by_kind[item.kind].append(item)
    for kind, items in by_kind.items():
        for index, left in enumerate(items):
            for right in items[index + 1 :]:
                similarity = cosine(left.tokens, right.tokens)
                if similarity < SIMILARITY_THRESHOLD:
                    continue
                classification, rationale = classify(left, right)
                candidates.append(
                    Candidate(
                        kind=kind,
                        left=left.path,
                        right=right.path,
                        similarity=round(similarity, 3),
                        classification=classification,
                        rationale=rationale,
                    )
                )
    candidates.sort(
        key=lambda item: (
            item.kind,
            -item.similarity,
            item.left.casefold(),
            item.right.casefold(),
        )
    )
    unclassified = sum(
        candidate.classification == "unclassified"
        for candidate in candidates
    )
    return {
        "schemaVersion": 1,
        "threshold": SIMILARITY_THRESHOLD,
        "summary": {
            "sources": len(primitives),
            "exactDuplicateGroups": len(exact_groups),
            "similarityCandidates": len(candidates),
            "unclassifiedCandidates": unclassified,
            "confirmedDuplicates": 0,
        },
        "policy": {
            "classifications": [
                "duplicate",
                "specialization",
                "language-variant",
                "framework-variant",
                "lifecycle-variant",
                "source-framework-variant",
                "complement",
                "supersedes",
                "unclassified",
            ],
            "note": (
                "Similarity only creates a review candidate. Deletion requires an exact duplicate "
                "or an explicit responsibility-boundary decision."
            ),
        },
        "exactDuplicateGroups": exact_groups,
        "candidates": [asdict(candidate) for candidate in candidates],
    }


def table(headers: list[str], rows: list[list[Any]]) -> str:
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
    summary = audit["summary"]
    rows = [
        [
            candidate["kind"],
            candidate["left"],
            candidate["right"],
            candidate["similarity"],
            candidate["classification"],
            candidate["rationale"],
        ]
        for candidate in audit["candidates"]
    ]
    candidate_table = (
        table(
            ["Type", "Left", "Right", "Score", "Classification", "Rationale"],
            rows,
        )
        if rows
        else "No high-similarity candidates."
    )
    return f"""# Primitive Redundancy Audit

Generated by `python3 harness/github-copilot/scripts/audit_primitive_redundancy.py`.

## Summary

| Metric | Count |
| --- | ---: |
| Canonical sources | {summary["sources"]} |
| Exact duplicate groups | {summary["exactDuplicateGroups"]} |
| High-similarity candidates | {summary["similarityCandidates"]} |
| Unclassified candidates | {summary["unclassifiedCandidates"]} |
| Confirmed duplicates remaining | {summary["confirmedDuplicates"]} |

Similarity is a review signal, not deletion authority. Candidates are compared only within the same
primitive type and classified by responsibility boundary. The complete ledger is
`docs/PRIMITIVE-REDUNDANCY.json`.

## Candidate decisions

{candidate_table}

## Policy

- `language-variant`, `framework-variant`, `lifecycle-variant`, and `source-framework-variant` preserve
  different implementation contracts.
- `specialization` and `complement` remain separate only while inputs, authority, or outputs differ.
- `duplicate` and `supersedes` require consolidation and reference migration.
- `unclassified` blocks the audit until a human-readable rationale is recorded.
- Same-name primitives across different types are composition, not automatic duplication.
"""


def stale_outputs(ledger: str, report: str) -> list[Path]:
    stale = []
    if not LEDGER_PATH.is_file() or LEDGER_PATH.read_text(encoding="utf-8") != ledger:
        stale.append(LEDGER_PATH)
    if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != report:
        stale.append(REPORT_PATH)
    return stale


def has_blockers(audit: dict[str, Any]) -> bool:
    summary = audit["summary"]
    return bool(
        summary["exactDuplicateGroups"]
        or summary["unclassifiedCandidates"]
        or summary["confirmedDuplicates"]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when reports are stale")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)

    audit = build_audit()
    ledger = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    report = render_report(audit)
    if args.json_output:
        print(ledger, end="")
        return 1 if has_blockers(audit) else 0
    if args.check:
        stale = stale_outputs(ledger, report)
        if stale:
            print(
                "Primitive redundancy audit is stale; run "
                "python3 harness/github-copilot/scripts/audit_primitive_redundancy.py",
                file=sys.stderr,
            )
            for path in stale:
                print(f"  - {path.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1
        return 1 if has_blockers(audit) else 0

    LEDGER_PATH.write_text(ledger, encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(
        f"Audited {audit['summary']['sources']} canonical sources and wrote "
        f"{REPORT_PATH.relative_to(REPO_ROOT)} plus {LEDGER_PATH.relative_to(REPO_ROOT)}."
    )
    return 1 if has_blockers(audit) else 0


if __name__ == "__main__":
    raise SystemExit(main())

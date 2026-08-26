#!/usr/bin/env python3
"""Extract, validate, and gate the COBOL/DB2 modernization graph.

Read-only against the corpus: the tool reads members and writes one JSON
document to stdout or to --out, and never edits legacy source.

Exit codes: 0 success, 1 findings or unresolved with --strict, 2 input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SUPPORTED_VERSION = 1

MEMBER_TYPES = {
    ".CBL": "CobolProgram",
    ".COB": "CobolProgram",
    ".CPY": "Copybook",
    ".JCL": "JclJob",
    ".PRC": "JclProc",
    ".SQL": "Db2Ddl",
    ".DDL": "Db2Ddl",
}

LEGACY_CODE_TYPES = frozenset({
    "CobolProgram", "Copybook", "JclJob", "JclProc",
})
LEGACY_DATA_TYPES = frozenset({
    "Db2Ddl", "Db2Table", "Db2Column", "Cursor", "VsamDataset",
})
BRIDGE_TYPES = frozenset({"BusinessRule", "Requirement", "Decision"})
TARGET_TYPES = frozenset({
    "JavaType", "Endpoint", "PgTable", "PgColumn", "Test", "Workflow",
    "InfraResource", "Runbook",
})
NODE_TYPES = (
    LEGACY_CODE_TYPES | LEGACY_DATA_TYPES | BRIDGE_TYPES | TARGET_TYPES
)

STATUS_VALUES = frozenset({"open", "accepted", "rejected", "deferred"})
CALLERS = frozenset({"CobolProgram"})
JOBS = frozenset({"JclJob", "JclProc"})
DB2_TABLE = frozenset({"Db2Table"})
REQUIREMENT = frozenset({"Requirement"})
DATA_CONTAINERS = frozenset({"Db2Table", "VsamDataset"})

EdgeRule = tuple[frozenset[str], frozenset[str]]

EDGE_RULES: dict[str, tuple[EdgeRule, ...]] = {
    "CALLS": ((CALLERS, CALLERS),),
    "COPIES": ((CALLERS | frozenset({"Copybook"}), frozenset({"Copybook"})),),
    "RUNS": ((JOBS, CALLERS),),
    "INCLUDES_PROC": ((frozenset({"JclJob"}), frozenset({"JclProc"})),),
    "SELECTS": ((CALLERS, DB2_TABLE),),
    "INSERTS": ((CALLERS, DB2_TABLE),),
    "UPDATES": ((CALLERS, DB2_TABLE),),
    "DELETES": ((CALLERS, DB2_TABLE),),
    "DECLARES_CURSOR": ((CALLERS, frozenset({"Cursor"})),),
    "CURSOR_READS": ((frozenset({"Cursor"}), DB2_TABLE),),
    "READS_DATASET": ((CALLERS, frozenset({"VsamDataset"})),),
    "WRITES_DATASET": ((CALLERS, frozenset({"VsamDataset"})),),
    "DEFINED_BY": ((DB2_TABLE, frozenset({"Db2Ddl"})),),
    "HAS_COLUMN": ((DB2_TABLE, frozenset({"Db2Column"})),),
    "DERIVES_RULE": (
        (LEGACY_CODE_TYPES | LEGACY_DATA_TYPES, frozenset({"BusinessRule"})),
    ),
    "SATISFIED_BY": ((frozenset({"BusinessRule"}), REQUIREMENT),),
    "DECIDED_BY": ((REQUIREMENT, frozenset({"Decision"})),),
    "IMPLEMENTED_BY": (
        (REQUIREMENT, frozenset({"JavaType", "Endpoint", "PgTable"})),
    ),
    "VERIFIED_BY": ((REQUIREMENT, frozenset({"Test"})),),
    "MIGRATES_TO": (
        (DATA_CONTAINERS, frozenset({"PgTable"})),
        (frozenset({"Db2Column"}), frozenset({"PgColumn"})),
    ),
    "EXPOSED_BY": ((frozenset({"JavaType"}), frozenset({"Endpoint"})),),
    "DEPLOYED_BY": (
        (frozenset({"Endpoint", "InfraResource"}), frozenset({"Workflow"})),
    ),
    "DOCUMENTED_BY": ((frozenset({"Decision"}), frozenset({"Runbook"})),),
}

CALL_EDGE_TYPES = frozenset({
    "CALLS", "COPIES", "RUNS", "INCLUDES_PROC",
})

NAME = r"[A-Z][A-Z0-9$#@-]*"

CALL_LITERAL_RE = re.compile(rf"\bCALL\s+'({NAME})'", re.I)
CALL_DYNAMIC_RE = re.compile(rf"\bCALL\s+({NAME})\s*(?:USING|\.|$)", re.I)
COPY_RE = re.compile(rf"\bCOPY\s+({NAME})", re.I)
EXEC_SQL_RE = re.compile(r"\bEXEC\s+SQL\b(.*?)\bEND-EXEC\b", re.I | re.S)
SQL_FROM_RE = re.compile(rf"\b(?:FROM|JOIN)\s+(?:[A-Z0-9_]+\.)?({NAME})", re.I)
SQL_INSERT_RE = re.compile(
    rf"\bINSERT\s+INTO\s+(?:[A-Z0-9_]+\.)?({NAME})", re.I)
SQL_UPDATE_RE = re.compile(
    rf"\bUPDATE\s+(?:[A-Z0-9_]+\.)?({NAME})\s+SET", re.I)
SQL_DELETE_RE = re.compile(
    rf"\bDELETE\s+FROM\s+(?:[A-Z0-9_]+\.)?({NAME})", re.I)
CURSOR_RE = re.compile(rf"\bDECLARE\s+({NAME})\s+CURSOR\b", re.I)
DDL_TABLE_RE = re.compile(
    rf"\bCREATE\s+TABLE\s+(?:[A-Z0-9_]+\.)?({NAME})", re.I)
JCL_EXEC_PGM_RE = re.compile(rf"\bEXEC\s+PGM=({NAME})", re.I)
JCL_EXEC_PROC_RE = re.compile(rf"\bEXEC\s+(?:PROC=)?({NAME})\s*(?:,|$)", re.I)
SELECT_DATASET_RE = re.compile(
    rf"\bSELECT\s+({NAME})\s+ASSIGN\s+TO\s+({NAME})", re.I)


class GraphError(Exception):
    """Raised when the corpus or graph document cannot be read."""


@dataclass
class Corpus:
    members: dict[str, tuple[str, Path]] = field(default_factory=dict)
    duplicates: list[str] = field(default_factory=list)


def code_area(raw: str) -> str:
    """Return the COBOL code area, dropping sequence and identification."""
    if len(raw) > 6 and raw[:6].strip().isdigit():
        return raw[6:72] if len(raw) > 72 else raw[6:]
    return raw


def strip_cobol(text: str) -> list[str]:
    """Blank comment lines and sequence areas, preserving line numbers."""
    lines: list[str] = []
    for raw in text.splitlines():
        candidate = code_area(raw)
        if candidate.lstrip().startswith(("*", "/")):
            lines.append("")
            continue
        lines.append(candidate)
    return lines


def scan_corpus(root: Path) -> Corpus:
    if not root.is_dir():
        raise GraphError(f"corpus is not a directory: {root}")
    corpus = Corpus()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        member_type = MEMBER_TYPES.get(path.suffix.upper())
        if member_type is None:
            continue
        name = path.stem.upper()
        key = f"{member_type}:{name}"
        if key in corpus.members:
            corpus.duplicates.append(name)
            continue
        corpus.members[key] = (member_type, path)
    if not corpus.members:
        raise GraphError(f"no COBOL, JCL, or DB2 members found under {root}")
    return corpus


@dataclass(frozen=True)
class GateRule:
    rule_id: str
    subject_type: str
    requirement: str
    kind: str
    edge_type: str | None = None
    exempt_attribute: str | None = None


GATES: dict[str, tuple[GateRule, ...]] = {
    "archaeology": (
        GateRule("A3", "BusinessRule",
                 "derives from an inspected legacy artifact",
                 "incoming", "DERIVES_RULE"),
    ),
    "vision": (
        GateRule("V1", "BusinessRule",
                 "is decided, owned when accepted and noted otherwise",
                 "decided"),
    ),
    "architecture": (
        GateRule("C1", "Requirement",
                 "has a rule source or an explicit greenfield flag",
                 "incoming", "SATISFIED_BY", "greenfield"),
        GateRule("C3", "Decision",
                 "is referenced by at least one requirement",
                 "incoming", "DECIDED_BY"),
    ),
    "implementation": (
        GateRule("I1", "Requirement", "has an implementation",
                 "outgoing", "IMPLEMENTED_BY"),
    ),
    "quality": (
        GateRule("Q1", "Requirement", "is verified by a test",
                 "outgoing", "VERIFIED_BY"),
        GateRule("Q2", "Db2Table", "has a target migration mapping",
                 "outgoing", "MIGRATES_TO"),
        GateRule("Q3", "VsamDataset", "has a target migration mapping",
                 "outgoing", "MIGRATES_TO"),
    ),
    "operations": (
        GateRule("O1", "Endpoint", "is deployed by a pipeline",
                 "outgoing", "DEPLOYED_BY"),
        GateRule("O2", "Decision", "is documented in a published record",
                 "outgoing", "DOCUMENTED_BY"),
    ),
}


class Graph:
    """Indexed view over a graph document of any validity."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self.document = payload
        self.version = payload.get("version")
        raw_nodes = payload.get("nodes", [])
        raw_edges = payload.get("edges", [])
        self.raw_nodes = raw_nodes if isinstance(raw_nodes, list) else []
        self.raw_edges = raw_edges if isinstance(raw_edges, list) else []
        self.nodes: dict[str, dict[str, Any]] = {}
        for node in self.raw_nodes:
            if isinstance(node, dict) and isinstance(node.get("id"), str):
                self.nodes.setdefault(node["id"], node)
        self.edges = [e for e in self.raw_edges if isinstance(e, dict)]
        self.outgoing: dict[str, list[dict[str, Any]]] = {}
        self.incoming: dict[str, list[dict[str, Any]]] = {}
        for edge in self.edges:
            source = edge.get("from")
            target = edge.get("to")
            if isinstance(source, str):
                self.outgoing.setdefault(source, []).append(edge)
            if isinstance(target, str):
                self.incoming.setdefault(target, []).append(edge)

    def node_type(self, identifier: str) -> str | None:
        node = self.nodes.get(identifier)
        return node.get("type") if isinstance(node, dict) else None

    def subjects(
        self, node_type: str, slice_id: str | None
    ) -> list[dict[str, Any]]:
        found = [
            node for node in self.nodes.values()
            if node.get("type") == node_type
        ]
        if slice_id is not None:
            found = [node for node in found if node.get("slice") == slice_id]
        return sorted(found, key=lambda node: node["id"])

    def has_edge(self, identifier: str, edge_type: str, way: str) -> bool:
        index = self.outgoing if way == "outgoing" else self.incoming
        return any(
            edge.get("type") == edge_type for edge in index.get(identifier, [])
        )

    def neighbors(
        self, identifier: str, way: str,
        edge_types: frozenset[str] | None = None,
    ) -> list[str]:
        index = self.outgoing if way == "outgoing" else self.incoming
        key = "to" if way == "outgoing" else "from"
        found: list[str] = []
        for edge in index.get(identifier, []):
            if edge_types is not None and edge.get("type") not in edge_types:
                continue
            other = edge.get(key)
            if isinstance(other, str) and other in self.nodes:
                found.append(other)
        return found


class GraphBuilder:
    def __init__(self, root: Path, slice_id: str | None) -> None:
        self.root = root
        self.slice_id = slice_id
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: dict[tuple[str, str, str], dict[str, Any]] = {}
        self.unresolved: list[str] = []
        self.recognized_files = 0

    def evidence(self, path: Path, line: int | None = None) -> str:
        relative = path.relative_to(self.root).as_posix()
        return f"{relative}#L{line}" if line else relative

    def add_node(
        self, identifier: str, node_type: str, label: str, evidence: str
    ) -> None:
        if identifier in self.nodes:
            return
        node: dict[str, Any] = {
            "id": identifier,
            "type": node_type,
            "label": label,
            "evidence": evidence,
        }
        if self.slice_id:
            node["slice"] = self.slice_id
        self.nodes[identifier] = node

    def add_edge(
        self, source: str, edge_type: str, target: str, evidence: str
    ) -> None:
        self.edges.setdefault(
            (source, edge_type, target),
            {
                "from": source,
                "type": edge_type,
                "to": target,
                "evidence": evidence,
            },
        )

    def note(self, path: Path, line: int, message: str) -> None:
        self.unresolved.append(f"{self.evidence(path, line)}: {message}")


def node_id(name: str, node_type: str) -> str:
    prefix = {
        "CobolProgram": "cobol",
        "Copybook": "copybook",
        "JclJob": "jcl",
        "JclProc": "proc",
        "Db2Ddl": "ddl",
        "Db2Table": "db2",
        "VsamDataset": "vsam",
        "Cursor": "cursor",
    }.get(node_type, "legacy")
    return f"{prefix}:{name}"


def register_members(builder: GraphBuilder, corpus: Corpus) -> None:
    for member_type, path in corpus.members.values():
        name = path.stem.upper()
        builder.add_node(
            node_id(name, member_type), member_type, name,
            builder.evidence(path),
        )


def register_ddl(builder: GraphBuilder, corpus: Corpus) -> None:
    for member_type, path in corpus.members.values():
        if member_type != "Db2Ddl":
            continue
        ddl_id = node_id(path.stem.upper(), "Db2Ddl")
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for index, raw in enumerate(lines, start=1):
            for match in DDL_TABLE_RE.finditer(raw):
                table = match.group(1).upper()
                builder.add_node(
                    node_id(table, "Db2Table"), "Db2Table", table,
                    builder.evidence(path, index),
                )
                builder.add_edge(
                    node_id(table, "Db2Table"), "DEFINED_BY", ddl_id,
                    builder.evidence(path, index),
                )


def link_member(
    builder: GraphBuilder, corpus: Corpus, source_id: str, target_name: str,
    edge_type: str, expected: str, path: Path, line: int,
) -> None:
    if f"{expected}:{target_name}" not in corpus.members:
        builder.note(path, line, f"{edge_type} target {target_name} not found")
        return
    builder.add_edge(
        source_id, edge_type, node_id(target_name, expected),
        builder.evidence(path, line),
    )


def sql_access(
    builder: GraphBuilder, source_id: str, path: Path, text: str
) -> None:
    pairs = (
        (SQL_INSERT_RE, "INSERTS"),
        (SQL_UPDATE_RE, "UPDATES"),
        (SQL_DELETE_RE, "DELETES"),
        (SQL_FROM_RE, "SELECTS"),
    )
    for block in EXEC_SQL_RE.finditer(text):
        statement = block.group(1)
        line = text[: block.start()].count("\n") + 1
        for pattern, edge_type in pairs:
            for match in pattern.finditer(statement):
                table = match.group(1).upper()
                builder.add_node(
                    node_id(table, "Db2Table"), "Db2Table", table,
                    builder.evidence(path, line),
                )
                builder.add_edge(
                    source_id, edge_type, node_id(table, "Db2Table"),
                    builder.evidence(path, line),
                )
        for match in CURSOR_RE.finditer(statement):
            cursor = match.group(1).upper()
            builder.add_node(
                node_id(cursor, "Cursor"), "Cursor", cursor,
                builder.evidence(path, line),
            )
            builder.add_edge(
                source_id, "DECLARES_CURSOR", node_id(cursor, "Cursor"),
                builder.evidence(path, line),
            )


def parse_program(builder: GraphBuilder, corpus: Corpus, path: Path) -> None:
    source_id = node_id(path.stem.upper(), "CobolProgram")
    lines = strip_cobol(
        path.read_text(encoding="utf-8", errors="replace"))
    for index, raw in enumerate(lines, start=1):
        for match in CALL_LITERAL_RE.finditer(raw):
            link_member(
                builder, corpus, source_id, match.group(1).upper(),
                "CALLS", "CobolProgram", path, index,
            )
        for match in COPY_RE.finditer(raw):
            link_member(
                builder, corpus, source_id, match.group(1).upper(),
                "COPIES", "Copybook", path, index,
            )
        for match in SELECT_DATASET_RE.finditer(raw):
            dataset = match.group(2).upper()
            builder.add_node(
                node_id(dataset, "VsamDataset"), "VsamDataset", dataset,
                builder.evidence(path, index),
            )
            builder.add_edge(
                source_id, "READS_DATASET", node_id(dataset, "VsamDataset"),
                builder.evidence(path, index),
            )
        if CALL_LITERAL_RE.search(raw) is None:
            for match in CALL_DYNAMIC_RE.finditer(raw):
                builder.note(
                    path, index,
                    f"dynamic CALL {match.group(1).upper()} is unresolved",
                )
    sql_access(builder, source_id, path, "\n".join(lines))


def parse_job(builder: GraphBuilder, corpus: Corpus, path: Path) -> None:
    member_type = "JclJob" if path.suffix.upper() == ".JCL" else "JclProc"
    source_id = node_id(path.stem.upper(), member_type)
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for index, raw in enumerate(lines, start=1):
        if raw.lstrip().startswith("//*"):
            continue
        for match in JCL_EXEC_PGM_RE.finditer(raw):
            link_member(
                builder, corpus, source_id, match.group(1).upper(),
                "RUNS", "CobolProgram", path, index,
            )
        if JCL_EXEC_PGM_RE.search(raw) is not None:
            continue
        for match in JCL_EXEC_PROC_RE.finditer(raw):
            candidate = match.group(1).upper()
            if f"JclProc:{candidate}" in corpus.members:
                builder.add_edge(
                    source_id, "INCLUDES_PROC",
                    node_id(candidate, "JclProc"),
                    builder.evidence(path, index),
                )


def extract(root: Path, slice_id: str | None) -> GraphBuilder:
    corpus = scan_corpus(root)
    builder = GraphBuilder(root, slice_id)
    builder.recognized_files = len(corpus.members)
    register_members(builder, corpus)
    register_ddl(builder, corpus)
    for member_type, path in corpus.members.values():
        if member_type == "CobolProgram":
            parse_program(builder, corpus, path)
        elif member_type in {"JclJob", "JclProc"}:
            parse_job(builder, corpus, path)
    for duplicate in sorted(set(corpus.duplicates)):
        builder.unresolved.append(
            f"{duplicate}: more than one member shares this name")
    return builder


def node_findings(node: Any, position: int, seen: set[str]) -> list[str]:
    if not isinstance(node, dict):
        return [f"node[{position}]: must be an object"]
    identifier = node.get("id")
    if not isinstance(identifier, str) or not identifier.strip():
        return [f"node[{position}]: id must be a non-empty string"]
    findings: list[str] = []
    if identifier in seen:
        findings.append(f"{identifier}: duplicate node id")
    seen.add(identifier)
    if node.get("type") not in NODE_TYPES:
        findings.append(
            f"{identifier}: unknown node type {node.get('type')!r}")
    evidence = node.get("evidence")
    if not isinstance(evidence, str) or not evidence.strip():
        findings.append(f"{identifier}: evidence is required")
    status = node.get("status")
    if status is not None and status not in STATUS_VALUES:
        findings.append(f"{identifier}: unknown status {status!r}")
    return findings


def endpoint_findings(
    graph: Graph, source: Any, target: Any, edge_type: Any, name: str
) -> list[str]:
    rules = EDGE_RULES.get(edge_type) if isinstance(edge_type, str) else None
    if rules is None:
        return [f"{name}: unknown edge type {edge_type!r}"]
    if source not in graph.nodes or target not in graph.nodes:
        return []
    source_type = graph.node_type(source)
    target_type = graph.node_type(target)
    allowed = any(
        source_type in allowed_from and target_type in allowed_to
        for allowed_from, allowed_to in rules
    )
    if allowed:
        return []
    return [
        f"{name}: {edge_type} does not allow {source_type} to {target_type}"
    ]


def edge_findings(graph: Graph, edge: Any, position: int) -> list[str]:
    if not isinstance(edge, dict):
        return [f"edge[{position}]: must be an object"]
    source = edge.get("from")
    target = edge.get("to")
    edge_type = edge.get("type")
    name = f"{source} -{edge_type}-> {target}"
    findings: list[str] = []
    evidence = edge.get("evidence")
    if not isinstance(evidence, str) or not evidence.strip():
        findings.append(f"{name}: evidence is required")
    if source not in graph.nodes:
        findings.append(f"{name}: unknown source node {source!r}")
    if target not in graph.nodes:
        findings.append(f"{name}: unknown target node {target!r}")
    findings.extend(endpoint_findings(graph, source, target, edge_type, name))
    return findings


def validate(graph: Graph) -> list[str]:
    findings: list[str] = []
    if graph.version != SUPPORTED_VERSION:
        findings.append(f"version must equal {SUPPORTED_VERSION}")
    seen: set[str] = set()
    for position, node in enumerate(graph.raw_nodes):
        findings.extend(node_findings(node, position, seen))
    for position, edge in enumerate(graph.raw_edges):
        findings.extend(edge_findings(graph, edge, position))
    return findings


def check_decided(node: dict[str, Any]) -> str | None:
    status = node.get("status")
    if status not in STATUS_VALUES or status == "open":
        return "status is undecided"
    if status == "accepted" and not str(node.get("owner", "")).strip():
        return "accepted without an owner"
    if status in {"rejected", "deferred"}:
        if not str(node.get("note", "")).strip():
            return f"{status} without a note"
    return None


def check_rule(
    graph: Graph, rule: GateRule, slice_id: str | None
) -> tuple[list[str], list[str]]:
    satisfied: list[str] = []
    missing: list[str] = []
    for node in graph.subjects(rule.subject_type, slice_id):
        identifier = node["id"]
        if rule.kind == "decided":
            problem = check_decided(node)
            if problem is None:
                satisfied.append(identifier)
            else:
                missing.append(f"{identifier}: {problem}")
            continue
        if rule.exempt_attribute and node.get(rule.exempt_attribute) is True:
            satisfied.append(identifier)
            continue
        if rule.edge_type is None:
            continue
        if graph.has_edge(identifier, rule.edge_type, rule.kind):
            satisfied.append(identifier)
        else:
            missing.append(f"{identifier}: no {rule.kind} {rule.edge_type}")
    return satisfied, missing


def gate(graph: Graph, phase: str, slice_id: str | None) -> dict[str, Any]:
    rules: list[dict[str, Any]] = []
    for rule in GATES[phase]:
        satisfied, missing = check_rule(graph, rule, slice_id)
        rules.append({
            "rule": rule.rule_id,
            "subject": rule.subject_type,
            "requirement": rule.requirement,
            "subjects": len(satisfied) + len(missing),
            "satisfied": len(satisfied),
            "missing": missing,
        })
    return {
        "phase": phase,
        "slice": slice_id or "unscoped",
        "passed": all(not entry["missing"] for entry in rules),
        "rules": rules,
    }


def slice_order(graph: Graph) -> list[list[str]]:
    """Leaf-first order over call edges, with cycles grouped together."""
    order: list[list[str]] = []
    visiting: list[str] = []
    done: set[str] = set()

    def visit(node: str) -> None:
        if node in done:
            return
        if node in visiting:
            cycle = sorted(set(visiting[visiting.index(node):]))
            order.append(cycle)
            done.update(cycle)
            return
        visiting.append(node)
        for child in sorted(set(
                graph.neighbors(node, "outgoing", CALL_EDGE_TYPES))):
            visit(child)
        visiting.pop()
        if node not in done:
            order.append([node])
            done.add(node)

    for root in sorted(graph.nodes):
        if graph.node_type(root) in LEGACY_CODE_TYPES:
            visit(root)
    return order


def dead_legacy(graph: Graph) -> list[str]:
    return sorted(
        node["id"] for node in graph.nodes.values()
        if node.get("type") in LEGACY_CODE_TYPES
        and node.get("type") != "JclJob"
        and not graph.neighbors(node["id"], "incoming", CALL_EDGE_TYPES)
    )


def extraction_summary(builder: GraphBuilder) -> dict[str, Any]:
    return {
        "recognizedFiles": builder.recognized_files,
        "unresolved": list(builder.unresolved),
    }


def document(builder: GraphBuilder) -> dict[str, Any]:
    return {
        "version": 1,
        "extraction": extraction_summary(builder),
        "nodes": list(builder.nodes.values()),
        "edges": list(builder.edges.values()),
    }


def merge(existing: dict[str, Any], builder: GraphBuilder) -> dict[str, Any]:
    """Keep authored nodes and edges; add only what is missing."""
    nodes = [n for n in existing.get("nodes", []) if isinstance(n, dict)]
    edges = [e for e in existing.get("edges", []) if isinstance(e, dict)]
    known_nodes = {n.get("id") for n in nodes}
    known_edges = {(e.get("from"), e.get("type"), e.get("to")) for e in edges}
    for identifier, node in builder.nodes.items():
        if identifier not in known_nodes:
            nodes.append(node)
    for key, edge in builder.edges.items():
        if key not in known_edges:
            edges.append(edge)
    return {
        "version": 1,
        "extraction": extraction_summary(builder),
        "nodes": nodes,
        "edges": edges,
    }


def load_graph(path: Path) -> Graph:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise GraphError(f"cannot read graph: {error}") from error
    except json.JSONDecodeError as error:
        raise GraphError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(payload, dict):
        raise GraphError(f"{path}: graph root must be a JSON object")
    return Graph(payload)


def render_gate(payload: dict[str, Any]) -> str:
    result = "pass" if payload["passed"] else "fail"
    lines = [
        f"phase: {payload['phase']}  slice: {payload['slice']}  "
        f"result: {result}"
    ]
    for entry in payload["rules"]:
        lines.append(
            f"  {entry['rule']} {entry['subject']} {entry['requirement']}: "
            f"{entry['satisfied']}/{entry['subjects']} subjects"
        )
        lines.extend(f"    missing: {item}" for item in entry["missing"])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cobol_db2_graph.py",
        description="Extract, validate, and gate the COBOL/DB2 graph.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser(
        "extract", help="build the legacy layer from a corpus")
    extract_parser.add_argument("--corpus", required=True, type=Path)
    extract_parser.add_argument("--slice", dest="slice_id")
    extract_parser.add_argument("--merge", type=Path)
    extract_parser.add_argument("--out", type=Path)
    extract_parser.add_argument("--strict", action="store_true")

    validate_parser = subparsers.add_parser(
        "validate", help="check shape, vocabulary, and evidence")
    validate_parser.add_argument("--graph", required=True, type=Path)

    gate_parser = subparsers.add_parser(
        "gate", help="evaluate one phase gate over the graph")
    gate_parser.add_argument("--graph", required=True, type=Path)
    gate_parser.add_argument("--phase", required=True, choices=sorted(GATES))
    gate_parser.add_argument("--slice", dest="slice_id")

    query_parser = subparsers.add_parser("query", help="run an analysis query")
    query_parser.add_argument("--graph", required=True, type=Path)
    query_parser.add_argument(
        "--query", required=True, choices=("slice-order", "dead-legacy"))
    return parser


def run_extract(args: argparse.Namespace) -> int:
    builder = extract(args.corpus.resolve(), args.slice_id)
    if args.merge is not None:
        payload = merge(load_graph(args.merge).document, builder)
    else:
        payload = document(builder)
    text = json.dumps(payload, indent=2) + "\n"
    if args.out is not None:
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    for note in builder.unresolved:
        print(f"unresolved: {note}", file=sys.stderr)
    print(
        f"scanned {builder.recognized_files} recognized files; "
        f"extracted {len(builder.nodes)} nodes, {len(builder.edges)} edges, "
        f"{len(builder.unresolved)} unresolved",
        file=sys.stderr,
    )
    return 1 if args.strict and builder.unresolved else 0


def run_query(graph: Graph, name: str) -> None:
    if name == "slice-order":
        for position, group in enumerate(slice_order(graph), start=1):
            print(f"{position}. {', '.join(group)}")
        return
    print("\n".join(dead_legacy(graph)) or "no unreferenced code")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "extract":
            return run_extract(args)
        graph = load_graph(args.graph)
        if args.command == "validate":
            findings = validate(graph)
            if findings:
                print("\n".join(findings))
                return 1
            print(
                f"graph valid: {len(graph.nodes)} nodes, "
                f"{len(graph.edges)} edges"
            )
            return 0
        if args.command == "gate":
            payload = gate(graph, args.phase, args.slice_id)
            print(render_gate(payload))
            return 0 if payload["passed"] else 1
        run_query(graph, args.query)
        return 0
    except (GraphError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

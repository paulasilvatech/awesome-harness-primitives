#!/usr/bin/env python3
"""Validate, gate, query, and render the SIFAP modernization graph.

The tool is read-only: it reads one JSON graph document and writes stdout.
Exit codes: 0 no findings, 1 findings reported, 2 usage or input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SUPPORTED_VERSION = 1

LEGACY_CODE_TYPES = frozenset({
    "NaturalProgram", "NaturalSubprogram", "NaturalSubroutine",
    "Copycode", "Map", "DataArea", "JclJob",
})
LEGACY_DATA_TYPES = frozenset({
    "Ddm", "AdabasFile", "AdabasField", "Descriptor",
})
BRIDGE_TYPES = frozenset({"BusinessRule", "Requirement", "Decision"})
TARGET_TYPES = frozenset({
    "JavaType", "Endpoint", "PgTable", "PgColumn", "Test", "Workflow",
    "InfraResource", "Runbook",
})
LEGACY_TYPES = LEGACY_CODE_TYPES | LEGACY_DATA_TYPES
NODE_TYPES = LEGACY_TYPES | BRIDGE_TYPES | TARGET_TYPES

STATUS_VALUES = frozenset({"open", "accepted", "rejected", "deferred"})
CALLERS = frozenset({"NaturalProgram", "NaturalSubprogram"})
COPYCODE = frozenset({"Copycode"})
ADABAS_FILE = frozenset({"AdabasFile"})
REQUIREMENT = frozenset({"Requirement"})

EdgeRule = tuple[frozenset[str], frozenset[str]]

EDGE_RULES: dict[str, tuple[EdgeRule, ...]] = {
    "CALLNAT": ((CALLERS, CALLERS),),
    "PERFORM": ((CALLERS, frozenset({"NaturalSubroutine"})),),
    "INCLUDE": ((CALLERS, COPYCODE),),
    "USES_MAP": ((CALLERS, frozenset({"Map"})),),
    "USES_DATA_AREA": ((CALLERS | COPYCODE, frozenset({"DataArea"})),),
    "RUNS": ((frozenset({"JclJob"}), frozenset({"NaturalProgram"})),),
    "READS": ((CALLERS, ADABAS_FILE),),
    "UPDATES": ((CALLERS, ADABAS_FILE),),
    "STORES": ((CALLERS, ADABAS_FILE),),
    "DELETES": ((CALLERS, ADABAS_FILE),),
    "DEFINED_BY": ((ADABAS_FILE, frozenset({"Ddm"})),),
    "HAS_FIELD": ((ADABAS_FILE, frozenset({"AdabasField"})),),
    "INDEXED_BY": ((ADABAS_FILE, frozenset({"Descriptor"})),),
    "DERIVES_RULE": ((LEGACY_TYPES, frozenset({"BusinessRule"})),),
    "SATISFIED_BY": ((frozenset({"BusinessRule"}), REQUIREMENT),),
    "DECIDED_BY": ((REQUIREMENT, frozenset({"Decision"})),),
    "IMPLEMENTED_BY": (
        (REQUIREMENT, frozenset({"JavaType", "Endpoint", "PgTable"})),
    ),
    "VERIFIED_BY": ((REQUIREMENT, frozenset({"Test"})),),
    "MIGRATES_TO": (
        (ADABAS_FILE, frozenset({"PgTable"})),
        (frozenset({"AdabasField"}), frozenset({"PgColumn"})),
    ),
    "EXPOSED_BY": ((frozenset({"JavaType"}), frozenset({"Endpoint"})),),
    "DEPLOYED_BY": (
        (frozenset({"Endpoint", "InfraResource"}), frozenset({"Workflow"})),
    ),
    "DOCUMENTED_BY": ((frozenset({"Decision"}), frozenset({"Runbook"})),),
}

CALL_EDGE_TYPES = frozenset({
    "CALLNAT", "PERFORM", "INCLUDE", "USES_MAP", "USES_DATA_AREA", "RUNS",
})

MERMAID_CLASSES = (
    ("legacyCode", LEGACY_CODE_TYPES,
     "fill:#F25022,stroke:#8a2d12,color:#ffffff"),
    ("legacyData", LEGACY_DATA_TYPES,
     "fill:#FFB900,stroke:#8a6500,color:#1B1B1F"),
    ("bridge", BRIDGE_TYPES,
     "fill:#00A4EF,stroke:#005a85,color:#ffffff"),
    ("target", TARGET_TYPES,
     "fill:#7FBA00,stroke:#456600,color:#1B1B1F"),
)

UNSAFE_ID = re.compile(r"\W", re.ASCII)


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
        GateRule("Q2", "AdabasFile", "has a target migration mapping",
                 "outgoing", "MIGRATES_TO"),
    ),
    "operations": (
        GateRule("O1", "Endpoint", "is deployed by a pipeline",
                 "outgoing", "DEPLOYED_BY"),
        GateRule("O2", "Decision", "is documented in a published record",
                 "outgoing", "DOCUMENTED_BY"),
    ),
}


class GraphError(Exception):
    """Raised when the graph document cannot be read, parsed, or queried."""


class Graph:
    """Indexed view over a graph document of any validity."""

    def __init__(self, document: dict[str, Any]) -> None:
        self.version = document.get("version")
        raw_nodes = document.get("nodes", [])
        raw_edges = document.get("edges", [])
        self.raw_nodes = raw_nodes if isinstance(raw_nodes, list) else []
        self.raw_edges = raw_edges if isinstance(raw_edges, list) else []
        self.nodes: dict[str, dict[str, Any]] = {}
        for node in self.raw_nodes:
            if isinstance(node, dict) and isinstance(node.get("id"), str):
                self.nodes.setdefault(node["id"], node)
        self.edges: list[dict[str, Any]] = [
            edge for edge in self.raw_edges if isinstance(edge, dict)
        ]
        self.outgoing: dict[str, list[dict[str, Any]]] = {}
        self.incoming: dict[str, list[dict[str, Any]]] = {}
        for edge in self.edges:
            source = edge.get("from")
            target = edge.get("to")
            if isinstance(source, str):
                self.outgoing.setdefault(source, []).append(edge)
            if isinstance(target, str):
                self.incoming.setdefault(target, []).append(edge)

    def node_type(self, node_id: str) -> str | None:
        node = self.nodes.get(node_id)
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

    def has_edge(self, node_id: str, edge_type: str, direction: str) -> bool:
        index = self.outgoing if direction == "outgoing" else self.incoming
        return any(
            edge.get("type") == edge_type for edge in index.get(node_id, [])
        )

    def neighbors(
        self,
        node_id: str,
        direction: str,
        edge_types: frozenset[str] | None = None,
    ) -> list[str]:
        index = self.outgoing if direction == "outgoing" else self.incoming
        key = "to" if direction == "outgoing" else "from"
        found: list[str] = []
        for edge in index.get(node_id, []):
            if edge_types is not None and edge.get("type") not in edge_types:
                continue
            other = edge.get(key)
            if isinstance(other, str) and other in self.nodes:
                found.append(other)
        return found


def load_graph(path: Path) -> Graph:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise GraphError(f"cannot read graph: {error}") from error
    try:
        document = json.loads(text)
    except json.JSONDecodeError as error:
        raise GraphError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(document, dict):
        raise GraphError(f"{path}: graph root must be a JSON object")
    return Graph(document)


def node_findings(node: Any, position: int, seen: set[str]) -> list[str]:
    if not isinstance(node, dict):
        return [f"node[{position}]: must be an object"]
    node_id = node.get("id")
    if not isinstance(node_id, str) or not node_id.strip():
        return [f"node[{position}]: id must be a non-empty string"]
    findings: list[str] = []
    if node_id in seen:
        findings.append(f"{node_id}: duplicate node id")
    seen.add(node_id)
    if node.get("type") not in NODE_TYPES:
        findings.append(f"{node_id}: unknown node type {node.get('type')!r}")
    evidence = node.get("evidence")
    if not isinstance(evidence, str) or not evidence.strip():
        findings.append(f"{node_id}: evidence is required")
    status = node.get("status")
    if status is not None and status not in STATUS_VALUES:
        findings.append(f"{node_id}: unknown status {status!r}")
    return findings


def validate_nodes(graph: Graph) -> list[str]:
    seen: set[str] = set()
    findings: list[str] = []
    for position, node in enumerate(graph.raw_nodes):
        findings.extend(node_findings(node, position, seen))
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
        f"{name}: {edge_type} does not allow "
        f"{source_type} to {target_type}"
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
    findings.extend(
        endpoint_findings(graph, source, target, edge_type, name))
    return findings


def validate_edges(graph: Graph) -> list[str]:
    findings: list[str] = []
    for position, edge in enumerate(graph.raw_edges):
        findings.extend(edge_findings(graph, edge, position))
    return findings


def validate(graph: Graph) -> list[str]:
    findings: list[str] = []
    if graph.version != SUPPORTED_VERSION:
        findings.append(f"version must equal {SUPPORTED_VERSION}")
    findings.extend(validate_nodes(graph))
    findings.extend(validate_edges(graph))
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
        node_id = node["id"]
        if rule.kind == "decided":
            problem = check_decided(node)
            if problem is None:
                satisfied.append(node_id)
            else:
                missing.append(f"{node_id}: {problem}")
            continue
        if rule.exempt_attribute and node.get(rule.exempt_attribute) is True:
            satisfied.append(node_id)
            continue
        if rule.edge_type is None:
            continue
        if graph.has_edge(node_id, rule.edge_type, rule.kind):
            satisfied.append(node_id)
        else:
            missing.append(f"{node_id}: no {rule.kind} {rule.edge_type}")
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


@dataclass
class SccState:
    index: dict[str, int]
    low: dict[str, int]
    on_stack: set[str]
    stack: list[str]
    components: list[list[str]]
    counter: int = 0


def _open(state: SccState, node: str) -> None:
    state.index[node] = state.counter
    state.low[node] = state.counter
    state.counter += 1
    state.stack.append(node)
    state.on_stack.add(node)


def _descend(
    state: SccState, work: list[tuple[str, int]], node: str, child: str
) -> None:
    if child not in state.index:
        work.append((child, 0))
    elif child in state.on_stack:
        state.low[node] = min(state.low[node], state.index[child])


def _pop_component(state: SccState, node: str) -> list[str]:
    component: list[str] = []
    while True:
        member = state.stack.pop()
        state.on_stack.discard(member)
        component.append(member)
        if member == node:
            return sorted(component)


def _ascend(
    state: SccState, work: list[tuple[str, int]], node: str
) -> None:
    if work:
        parent = work[-1][0]
        state.low[parent] = min(state.low[parent], state.low[node])
    if state.low[node] == state.index[node]:
        state.components.append(_pop_component(state, node))


def _walk(graph: Graph, state: SccState, root: str) -> None:
    work: list[tuple[str, int]] = [(root, 0)]
    while work:
        node, position = work[-1]
        if position == 0:
            _open(state, node)
        children = sorted(
            set(graph.neighbors(node, "outgoing", CALL_EDGE_TYPES))
        )
        if position < len(children):
            work[-1] = (node, position + 1)
            _descend(state, work, node, children[position])
            continue
        work.pop()
        _ascend(state, work, node)


def strongly_connected_components(graph: Graph) -> list[list[str]]:
    """Iterative Tarjan; components are emitted in dependency order."""
    state = SccState({}, {}, set(), [], [])
    for root in sorted(graph.nodes):
        if root not in state.index:
            _walk(graph, state, root)
    return state.components


def reachable(graph: Graph, start: str, direction: str) -> list[str]:
    seen: set[str] = set()
    queue = [start]
    while queue:
        current = queue.pop()
        for neighbor in graph.neighbors(current, direction):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    seen.discard(start)
    return sorted(seen)


def query_coverage(graph: Graph, slice_id: str | None) -> dict[str, Any]:
    coverage: list[dict[str, Any]] = []
    for phase, rules in GATES.items():
        for rule in rules:
            satisfied, missing = check_rule(graph, rule, slice_id)
            coverage.append({
                "phase": phase,
                "rule": rule.rule_id,
                "subjects": len(satisfied) + len(missing),
                "satisfied": len(satisfied),
                "missing": len(missing),
            })
    return {
        "query": "coverage",
        "slice": slice_id or "unscoped",
        "coverage": coverage,
    }


def query(
    graph: Graph, name: str, node_id: str | None, slice_id: str | None
) -> dict[str, Any]:
    if name == "slice-order":
        components = [
            component for component in strongly_connected_components(graph)
            if any(
                graph.node_type(member) in LEGACY_CODE_TYPES
                for member in component
            )
        ]
        return {"query": name, "components": components}
    if name == "dead-legacy":
        dead = sorted(
            node["id"] for node in graph.nodes.values()
            if node.get("type") in LEGACY_CODE_TYPES
            and node.get("type") != "JclJob"
            and not graph.neighbors(node["id"], "incoming", CALL_EDGE_TYPES)
        )
        return {"query": name, "unreferenced": dead}
    if name == "blast-radius":
        if node_id is None or node_id not in graph.nodes:
            raise GraphError(
                "blast-radius requires --node with a known node id")
        return {
            "query": name,
            "node": node_id,
            "depends_on": reachable(graph, node_id, "outgoing"),
            "depended_on_by": reachable(graph, node_id, "incoming"),
        }
    return query_coverage(graph, slice_id)


def neighborhood(graph: Graph, focus: str, depth: int) -> set[str]:
    seen = {focus}
    frontier = {focus}
    for _ in range(max(depth, 0)):
        following: set[str] = set()
        for node_id in frontier:
            following.update(graph.neighbors(node_id, "outgoing"))
            following.update(graph.neighbors(node_id, "incoming"))
        frontier = following - seen
        seen.update(frontier)
    return seen


def safe_id(node_id: str) -> str:
    return "n_" + UNSAFE_ID.sub("_", node_id)


def mermaid(graph: Graph, focus: str | None, depth: int) -> str:
    if focus is not None and focus not in graph.nodes:
        raise GraphError(f"unknown focus node {focus!r}")
    visible = neighborhood(graph, focus, depth) if focus else set(graph.nodes)
    lines = ["flowchart LR"]
    for class_name, _types, style in MERMAID_CLASSES:
        lines.append(f"    classDef {class_name} {style}")
    for node_id in sorted(visible):
        node = graph.nodes[node_id]
        label = str(node.get("label") or node_id).replace('"', "#quot;")
        lines.append(f'    {safe_id(node_id)}["{label}"]')
    for edge in graph.edges:
        source = edge.get("from")
        target = edge.get("to")
        if source in visible and target in visible:
            arrow = f"-->|{edge.get('type')}|"
            lines.append(f"    {safe_id(source)} {arrow} {safe_id(target)}")
    for class_name, types, _style in MERMAID_CLASSES:
        members = sorted(
            safe_id(node_id) for node_id in visible
            if graph.node_type(node_id) in types
        )
        if members:
            lines.append(f"    class {','.join(members)} {class_name}")
    return "\n".join(lines)


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


def render_query(payload: dict[str, Any]) -> str:
    name = payload.get("query")
    if name == "slice-order":
        rows = [
            f"{position}. {', '.join(component)}"
            for position, component in enumerate(
                payload["components"], start=1)
        ]
        return "\n".join(rows) or "no legacy components"
    if name == "dead-legacy":
        return "\n".join(payload["unreferenced"]) or "no unreferenced code"
    if name == "blast-radius":
        depends = ", ".join(payload["depends_on"]) or "none"
        dependents = ", ".join(payload["depended_on_by"]) or "none"
        return "\n".join([
            f"node: {payload['node']}",
            f"depends on: {depends}",
            f"depended on by: {dependents}",
        ])
    lines = [f"slice: {payload['slice']}"]
    for row in payload["coverage"]:
        lines.append(
            f"  {row['phase']:<15} {row['rule']:<3} "
            f"{row['satisfied']}/{row['subjects']} satisfied, "
            f"{row['missing']} missing"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sifap_loop_graph.py",
        description="Validate, gate, query, and render the SIFAP graph.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_graph_argument(sub: argparse.ArgumentParser) -> None:
        sub.add_argument(
            "--graph", required=True, type=Path,
            help="path to the JSON graph document",
        )

    validate_parser = subparsers.add_parser(
        "validate", help="check shape, vocabulary, and evidence")
    add_graph_argument(validate_parser)

    gate_parser = subparsers.add_parser(
        "gate", help="evaluate one phase gate over the graph")
    add_graph_argument(gate_parser)
    gate_parser.add_argument("--phase", required=True, choices=sorted(GATES))
    gate_parser.add_argument(
        "--slice", dest="slice_id", help="restrict subjects to this slice")
    gate_parser.add_argument(
        "--format", choices=("text", "json"), default="text")

    query_parser = subparsers.add_parser("query", help="run an analysis query")
    add_graph_argument(query_parser)
    query_parser.add_argument(
        "--query", required=True,
        choices=("slice-order", "dead-legacy", "blast-radius", "coverage"),
    )
    query_parser.add_argument("--node", help="node id for blast-radius")
    query_parser.add_argument(
        "--slice", dest="slice_id", help="restrict coverage to this slice")
    query_parser.add_argument(
        "--format", choices=("text", "json"), default="text")

    mermaid_parser = subparsers.add_parser(
        "mermaid", help="render a Mermaid flowchart")
    add_graph_argument(mermaid_parser)
    mermaid_parser.add_argument(
        "--focus", help="render this neighborhood only")
    mermaid_parser.add_argument(
        "--depth", type=int, default=1,
        help="neighborhood depth used with --focus",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
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
            if args.format == "json":
                print(json.dumps(payload, indent=2))
            else:
                print(render_gate(payload))
            return 0 if payload["passed"] else 1
        if args.command == "query":
            payload = query(graph, args.query, args.node, args.slice_id)
            if args.format == "json":
                print(json.dumps(payload, indent=2))
            else:
                print(render_query(payload))
            return 0
        print(mermaid(graph, args.focus, args.depth))
        return 0
    except GraphError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

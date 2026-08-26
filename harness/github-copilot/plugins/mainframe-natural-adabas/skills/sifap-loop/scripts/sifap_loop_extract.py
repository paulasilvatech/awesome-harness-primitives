#!/usr/bin/env python3
"""Extract the legacy layer of the SIFAP graph from Natural and DDM sources.

Read-only against the corpus: the tool reads members and writes one JSON
document to stdout or to --out. It emits only nodes and edges it can cite;
business rules, requirements, and target nodes stay authored by humans.

Exit codes: 0 extracted, 1 unresolved references with --strict, 2 input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

MEMBER_TYPES = {
    ".NSP": "NaturalProgram",
    ".NSN": "NaturalSubprogram",
    ".NSS": "NaturalSubroutine",
    ".NSC": "Copycode",
    ".NSM": "Map",
    ".NSA": "DataArea",
    ".NSL": "DataArea",
    ".NSG": "DataArea",
    ".JCL": "JclJob",
}
DDM_SUFFIXES = {".NSD", ".DDM"}

NAMESPACE = {
    "NaturalProgram": "natural",
    "NaturalSubprogram": "natural",
    "NaturalSubroutine": "natural",
    "Copycode": "natural",
    "Map": "natural",
    "DataArea": "natural",
    "JclJob": "jcl",
}

NAME = r"[A-Z][A-Z0-9$#&_-]*"

CALLNAT_RE = re.compile(rf"\bCALLNAT\s+'({NAME})'", re.I)
PERFORM_RE = re.compile(rf"\bPERFORM\s+({NAME})", re.I)
INCLUDE_RE = re.compile(rf"\bINCLUDE\s+({NAME})", re.I)
USING_RE = re.compile(
    rf"\b(?:LOCAL|PARAMETER|GLOBAL|INDEPENDENT)\s+USING\s+({NAME})", re.I)
MAP_RE = re.compile(rf"\bUSING\s+MAP\s+'({NAME})'", re.I)
VIEW_RE = re.compile(rf"\b\d+\s+({NAME})\s+VIEW\s+OF\s+({NAME})", re.I)
SUBROUTINE_RE = re.compile(rf"\bDEFINE\s+SUBROUTINE\s+({NAME})", re.I)
ACCESS_RE = re.compile(
    rf"\b(READ|FIND|GET|STORE|UPDATE|DELETE)\b"
    rf"(?:\s*\(\s*\d+\s*\))?\s+({NAME})",
    re.I,
)
BARE_ACCESS_RE = re.compile(r"\b(UPDATE|DELETE)\s*(?:$|\.)", re.I)
DDM_FILE_RE = re.compile(rf"\bFILE\s*:\s*\d*\s*-?\s*({NAME})", re.I)

ACCESS_EDGE = {
    "READ": "READS",
    "FIND": "READS",
    "GET": "READS",
    "STORE": "STORES",
    "UPDATE": "UPDATES",
    "DELETE": "DELETES",
}
# Natural statement words that follow PERFORM but never name a subroutine.
PERFORM_KEYWORDS = {"BREAK", "PROCESSING"}


class ExtractError(Exception):
    """Raised when the corpus or an existing graph cannot be read."""


@dataclass
class Corpus:
    members: dict[str, tuple[str, Path]] = field(default_factory=dict)
    ddms: dict[str, Path] = field(default_factory=dict)
    duplicates: list[str] = field(default_factory=list)


def strip_comments(text: str) -> list[str]:
    """Blank Natural comments while preserving one entry per source line."""
    lines: list[str] = []
    for raw in text.splitlines():
        if raw.lstrip().startswith("*"):
            lines.append("")
            continue
        lines.append(raw.split("/*", 1)[0])
    return lines


def scan_corpus(root: Path) -> Corpus:
    if not root.is_dir():
        raise ExtractError(f"corpus is not a directory: {root}")
    corpus = Corpus()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.upper()
        name = path.stem.upper()
        if suffix in DDM_SUFFIXES:
            corpus.ddms.setdefault(name, path)
            continue
        member_type = MEMBER_TYPES.get(suffix)
        if member_type is None:
            continue
        if name in corpus.members:
            corpus.duplicates.append(name)
            continue
        corpus.members[name] = (member_type, path)
    if not corpus.members and not corpus.ddms:
        raise ExtractError(f"no Natural or DDM members found under {root}")
    return corpus


def node_id(name: str, member_type: str) -> str:
    return f"{NAMESPACE.get(member_type, 'natural')}:{name}"


class GraphBuilder:
    def __init__(self, root: Path, slice_id: str | None) -> None:
        self.root = root
        self.slice_id = slice_id
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: dict[tuple[str, str, str], dict[str, Any]] = {}
        self.unresolved: list[str] = []
        self.member_files = 0
        self.ddm_files = 0

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


def register_members(builder: GraphBuilder, corpus: Corpus) -> None:
    for name, (member_type, path) in corpus.members.items():
        builder.add_node(
            node_id(name, member_type), member_type, name,
            builder.evidence(path),
        )
    for name, path in corpus.ddms.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        match = DDM_FILE_RE.search(text)
        file_name = match.group(1).upper() if match else name
        builder.add_node(
            f"ddm:{name}", "Ddm", f"{name} DDM", builder.evidence(path))
        builder.add_node(
            f"adabas:{file_name}", "AdabasFile", file_name,
            builder.evidence(path),
        )
        builder.add_edge(
            f"adabas:{file_name}", "DEFINED_BY", f"ddm:{name}",
            builder.evidence(path),
        )


def link_member(
    builder: GraphBuilder,
    corpus: Corpus,
    source_id: str,
    target_name: str,
    edge_type: str,
    expected: set[str],
    path: Path,
    line: int,
) -> None:
    entry = corpus.members.get(target_name)
    if entry is None:
        builder.note(path, line, f"{edge_type} target {target_name} not found")
        return
    target_type, _ = entry
    if target_type not in expected:
        builder.note(
            path, line,
            f"{edge_type} target {target_name} is {target_type}",
        )
        return
    builder.add_edge(
        source_id, edge_type, node_id(target_name, target_type),
        builder.evidence(path, line),
    )


def views_in(lines: list[str]) -> dict[str, str]:
    views: dict[str, str] = {}
    for raw in lines:
        for match in VIEW_RE.finditer(raw):
            views[match.group(1).upper()] = match.group(2).upper()
    return views


def data_access(
    builder: GraphBuilder,
    source_id: str,
    views: dict[str, str],
    path: Path,
    line: int,
    raw: str,
) -> None:
    for match in ACCESS_RE.finditer(raw):
        keyword = match.group(1).upper()
        operand = match.group(2).upper()
        file_name = views.get(operand)
        if file_name is None:
            builder.note(
                path, line,
                f"{keyword} operand {operand} has no VIEW OF declaration",
            )
            continue
        builder.add_node(
            f"adabas:{file_name}", "AdabasFile", file_name,
            builder.evidence(path, line),
        )
        builder.add_edge(
            source_id, ACCESS_EDGE[keyword], f"adabas:{file_name}",
            builder.evidence(path, line),
        )
    if BARE_ACCESS_RE.search(raw):
        builder.note(
            path, line,
            "bare UPDATE or DELETE has no operand; attribute it by hand",
        )


def parse_caller(
    builder: GraphBuilder,
    corpus: Corpus,
    name: str,
    member_type: str,
    path: Path,
) -> None:
    source_id = node_id(name, member_type)
    lines = strip_comments(
        path.read_text(encoding="utf-8", errors="replace"))
    views = views_in(lines)
    internal = {
        match.group(1).upper()
        for raw in lines for match in SUBROUTINE_RE.finditer(raw)
    }
    for index, raw in enumerate(lines, start=1):
        for match in CALLNAT_RE.finditer(raw):
            link_member(
                builder, corpus, source_id,
                match.group(1).upper(), "CALLNAT",
                {"NaturalProgram", "NaturalSubprogram"}, path, index,
            )
        for match in PERFORM_RE.finditer(raw):
            target = match.group(1).upper()
            if target in internal or target in PERFORM_KEYWORDS:
                continue
            link_member(
                builder, corpus, source_id, target, "PERFORM",
                {"NaturalSubroutine"}, path, index,
            )
        for match in INCLUDE_RE.finditer(raw):
            link_member(
                builder, corpus, source_id,
                match.group(1).upper(), "INCLUDE", {"Copycode"}, path, index,
            )
        for match in USING_RE.finditer(raw):
            link_member(
                builder, corpus, source_id,
                match.group(1).upper(), "USES_DATA_AREA", {"DataArea"},
                path, index,
            )
        for match in MAP_RE.finditer(raw):
            link_member(
                builder, corpus, source_id,
                match.group(1).upper(), "USES_MAP", {"Map"}, path, index,
            )
        data_access(builder, source_id, views, path, index, raw)


def parse_job(
    builder: GraphBuilder, corpus: Corpus, name: str, path: Path
) -> None:
    source_id = node_id(name, "JclJob")
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    programs = {
        member for member, (member_type, _) in corpus.members.items()
        if member_type == "NaturalProgram"
    }
    for index, raw in enumerate(lines, start=1):
        for word in re.findall(NAME, raw.upper()):
            if word in programs:
                builder.add_edge(
                    source_id, "RUNS", node_id(word, "NaturalProgram"),
                    builder.evidence(path, index),
                )


def extract(root: Path, slice_id: str | None) -> GraphBuilder:
    corpus = scan_corpus(root)
    builder = GraphBuilder(root, slice_id)
    builder.member_files = len(corpus.members)
    builder.ddm_files = len(corpus.ddms)
    register_members(builder, corpus)
    for name, (member_type, path) in corpus.members.items():
        if member_type == "JclJob":
            parse_job(builder, corpus, name, path)
        elif member_type in {"NaturalProgram", "NaturalSubprogram"}:
            parse_caller(builder, corpus, name, member_type, path)
        elif member_type == "Copycode":
            parse_caller(builder, corpus, name, member_type, path)
    for duplicate in sorted(set(corpus.duplicates)):
        builder.unresolved.append(
            f"{duplicate}: more than one member shares this name")
    return builder


def load_existing(path: Path) -> dict[str, Any]:
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ExtractError(f"cannot read graph: {error}") from error
    except json.JSONDecodeError as error:
        raise ExtractError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(existing, dict):
        raise ExtractError(f"{path}: graph root must be a JSON object")
    return existing


def merge(existing: dict[str, Any], builder: GraphBuilder) -> dict[str, Any]:
    """Keep authored nodes and edges; add only what is missing."""
    nodes = [n for n in existing.get("nodes", []) if isinstance(n, dict)]
    edges = [e for e in existing.get("edges", []) if isinstance(e, dict)]
    known_nodes = {n.get("id") for n in nodes}
    known_edges = {
        (e.get("from"), e.get("type"), e.get("to")) for e in edges
    }
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


def extraction_summary(builder: GraphBuilder) -> dict[str, Any]:
    return {
        "memberFiles": builder.member_files,
        "ddmFiles": builder.ddm_files,
        "recognizedFiles": builder.member_files + builder.ddm_files,
        "unresolved": list(builder.unresolved),
    }


def document(builder: GraphBuilder) -> dict[str, Any]:
    return {
        "version": 1,
        "extraction": extraction_summary(builder),
        "nodes": list(builder.nodes.values()),
        "edges": list(builder.edges.values()),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sifap_loop_extract.py",
        description="Extract the legacy layer of the SIFAP graph.",
    )
    parser.add_argument(
        "--corpus", required=True, type=Path,
        help="directory holding Natural members and DDM definitions",
    )
    parser.add_argument(
        "--slice", dest="slice_id", help="slice value applied to new nodes")
    parser.add_argument(
        "--merge", type=Path,
        help="existing graph to extend without overwriting authored content",
    )
    parser.add_argument(
        "--out", type=Path, help="write the graph here instead of stdout")
    parser.add_argument(
        "--strict", action="store_true",
        help="exit 1 when any reference could not be resolved",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        builder = extract(args.corpus.resolve(), args.slice_id)
        if args.merge is not None:
            payload = merge(load_existing(args.merge), builder)
        else:
            payload = document(builder)
    except ExtractError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    text = json.dumps(payload, indent=2) + "\n"
    if args.out is not None:
        try:
            args.out.write_text(text, encoding="utf-8")
        except OSError as error:
            print(f"error: cannot write graph: {error}", file=sys.stderr)
            return 2
    else:
        sys.stdout.write(text)

    for note in builder.unresolved:
        print(f"unresolved: {note}", file=sys.stderr)
    print(
        "scanned "
        f"{builder.member_files + builder.ddm_files} recognized files; "
        f"extracted {len(builder.nodes)} nodes, {len(builder.edges)} edges, "
        f"{len(builder.unresolved)} unresolved",
        file=sys.stderr,
    )
    return 1 if args.strict and builder.unresolved else 0


if __name__ == "__main__":
    sys.exit(main())

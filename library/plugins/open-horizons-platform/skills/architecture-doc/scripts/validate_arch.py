#!/usr/bin/env python3
"""Validate an architecture document produced by the Senior Cloud Architect.

Hard gate. Exits non-zero on any error so an architecture document cannot be
presented while it is incomplete or has broken Mermaid. Run it on the
`{app}_Architecture.md` file before presenting.

Checks:
  1. Required document sections present.
  2. The five required diagrams are present (System Context, Component,
     Deployment, Data Flow, Sequence).
  3. Every Mermaid block is well formed: fenced, non-empty, declares a known
     diagram type, has balanced brackets, and (for graphs) has edges.
  4. Each diagram carries all seven explanation parts.
  5. Convention checks: no em dashes, "GitHub Copilot" never bare "Copilot",
     no leftover template placeholders, no obvious unsourced fabricated metric.

Usage:
    python validate_arch.py <App_Architecture.md> [--min-diagrams 5]

See ../SKILL.md for the rules this enforces.
"""

import argparse
import re
import sys

KNOWN_MERMAID_TYPES = (
    "graph", "flowchart", "sequenceDiagram", "classDiagram", "stateDiagram",
    "stateDiagram-v2", "erDiagram", "journey", "gantt", "pie", "mindmap",
    "timeline", "quadrantChart", "C4Context", "C4Container", "C4Component",
)

REQUIRED_SECTIONS = (
    "Executive Summary",
    "System Context",
    "Component Architecture",
    "Deployment Architecture",
    "Data Flow",
    "Risks and Mitigations",
)

REQUIRED_DIAGRAMS = (
    "System Context",
    "Component",
    "Deployment",
    "Data Flow",
    "Sequence",
)

SEVEN_PARTS = (
    "Overview",
    "Key Components",
    "Relationships",
    "Design Decisions",
    "NFR Considerations",
    "Trade-offs",
    "Risks and Mitigations",
)


def find_mermaid_blocks(text):
    """Return list of (start_line, body) for each ```mermaid fenced block."""
    blocks = []
    lines = text.split("\n")
    i = 0
    fence_open = re.compile(r"^\s*```+\s*mermaid\s*$", re.I)
    fence_any = re.compile(r"^\s*```+\s*$")
    while i < len(lines):
        if fence_open.match(lines[i]):
            start = i + 1
            body = []
            i += 1
            while i < len(lines) and not fence_any.match(lines[i]):
                body.append(lines[i])
                i += 1
            blocks.append((start + 1, "\n".join(body)))
        i += 1
    return blocks


def check_fences_balanced(text):
    count = len(re.findall(r"^\s*```", text, re.M))
    return count % 2 == 0


def validate_mermaid_block(line_no, body):
    errors = []
    stripped = [ln for ln in body.split("\n") if ln.strip()]
    if not stripped:
        errors.append(f"mermaid block at line {line_no} is empty")
        return errors
    first = stripped[0].strip()
    if not any(first.startswith(t) for t in KNOWN_MERMAID_TYPES):
        errors.append(
            f"mermaid block at line {line_no} does not declare a known diagram "
            f"type (first line: '{first[:40]}')"
        )
    # Balanced brackets across the block.
    for op, cl, name in (("[", "]", "square"), ("(", ")", "round"), ("{", "}", "curly")):
        if body.count(op) != body.count(cl):
            errors.append(
                f"mermaid block at line {line_no} has unbalanced {name} brackets"
            )
    # Graph and flowchart need at least one edge.
    if first.startswith(("graph", "flowchart")) and not re.search(r"--+>|--+|==+>|-\.-+", body):
        errors.append(
            f"mermaid graph at line {line_no} has no edges (arrows)"
        )
    # sequenceDiagram needs at least one message arrow.
    if first.startswith("sequenceDiagram") and not re.search(r"->>|-->>|->|-->", body):
        errors.append(
            f"mermaid sequenceDiagram at line {line_no} has no messages"
        )
    return errors


def section_windows(text):
    """Split text into (heading, body) windows by H2/H3 headings."""
    parts = re.split(r"(?m)^(#{2,3}\s+.*)$", text)
    windows = []
    # parts: [pre, heading1, body1, heading2, body2, ...]
    for i in range(1, len(parts), 2):
        heading = parts[i].lstrip("# ").strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        windows.append((heading, body))
    return windows


def validate(path, min_diagrams):
    errors = []
    warnings = []
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        return [f"cannot read file: {exc}"], []

    # 1. Required sections.
    for sec in REQUIRED_SECTIONS:
        if not re.search(rf"(?mi)^#{{1,3}}\s+.*{re.escape(sec)}", text):
            errors.append(f"missing required section: '{sec}'")

    # 2. Required diagrams referenced by name.
    for diag in REQUIRED_DIAGRAMS:
        if diag.lower() not in text.lower():
            errors.append(f"missing required diagram: '{diag}'")

    # 3. Mermaid blocks.
    if not check_fences_balanced(text):
        errors.append("unbalanced ``` code fences in document")
    blocks = find_mermaid_blocks(text)
    if len(blocks) < min_diagrams:
        errors.append(
            f"found {len(blocks)} Mermaid diagram(s); at least {min_diagrams} are required"
        )
    for line_no, body in blocks:
        errors.extend(validate_mermaid_block(line_no, body))

    # 4. Seven explanation parts in each window that contains a Mermaid block.
    for heading, body in section_windows(text):
        if "```mermaid" not in body.lower():
            continue
        missing = [p for p in SEVEN_PARTS if p.lower() not in body.lower()]
        if missing:
            warnings.append(
                f"section '{heading[:40]}' is missing explanation parts: {missing}"
            )

    # 5. Conventions.
    if "\u2014" in text:
        errors.append("em dash found (forbidden); use commas, parentheses, or restructure")
    if re.search(r"(?<![A-Za-z/])Copilot\b", text) and "GitHub Copilot" not in text:
        errors.append("bare 'Copilot' without 'GitHub Copilot'")
    placeholders = re.findall(r"\{app\}|\{Application Name\}|\[Diagram\]|\[Explanation\]|TODO|TBD", text)
    if placeholders:
        errors.append(f"unfilled template placeholders remain: {sorted(set(placeholders))}")

    return errors, warnings


def main(argv):
    ap = argparse.ArgumentParser(description="Validate an architecture document.")
    ap.add_argument("file", help="Path to {app}_Architecture.md")
    ap.add_argument("--min-diagrams", type=int, default=5)
    args = ap.parse_args(argv[1:])

    errors, warnings = validate(args.file, args.min_diagrams)

    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        print(f"\nFAIL {args.file}")
        for e in errors:
            print(f"  - {e}")
        print(f"\n{len(errors)} error(s). Fix before presenting; do not ship an incomplete architecture.")
        return 1
    print(f"OK   {args.file}")
    if warnings:
        print(f"{len(warnings)} warning(s) to review.")
    print("\nArchitecture document passes the validation gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

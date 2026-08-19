#!/usr/bin/env python3
"""Validate a draw.io (.drawio) architecture diagram.

This gate is intentionally dependency-free. It checks that the file is valid XML,
contains at least one diagram page, has a valid mxGraph root, has drawable cells,
and uses either official-style icon references or embedded SVG image cells for
product nodes.
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

OFFICIAL_STYLE_HINTS = (
    "mxgraph.azure",
    "mxgraph.mscae",
    "mscae",
    "mxgraph.gcp2.github",
    "data:image/svg+xml",
)

GENERIC_ALLOWED = (
    "rounded=1",
    "ellipse",
    "shape=cloud",
    "shape=cylinder",
    "shape=cylinder3",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def styles(cells) -> list[str]:
    return [cell.get("style", "") for cell in cells]


def is_icon_style(style: str) -> bool:
    return any(token in style for token in OFFICIAL_STYLE_HINTS + GENERIC_ALLOWED)


def validate_page(diagram: ET.Element) -> tuple[int, int, int]:
    graph_root = diagram.find(".//mxGraphModel/root")
    if graph_root is None:
        fail(f"diagram page {diagram.get('name', '<unnamed>')} has no mxGraphModel/root")
    cells = graph_root.findall("mxCell")
    ids = {cell.get("id") for cell in cells}
    if "0" not in ids:
        fail("missing mxCell id=0")
    if "1" not in ids:
        fail("missing mxCell id=1")
    vertices = [cell for cell in cells if cell.get("vertex") == "1"]
    edges = [cell for cell in cells if cell.get("edge") == "1"]
    icon_count = sum(1 for style in styles(vertices) if is_icon_style(style))
    return len(vertices), len(edges), icon_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a draw.io architecture diagram")
    parser.add_argument("diagram", help="Path to a .drawio file")
    parser.add_argument("--require-icon", action="store_true", help="Require at least one official-style or embedded SVG icon")
    parser.add_argument("--require-edge", action="store_true", help="Require at least one connector edge")
    args = parser.parse_args()

    path = Path(args.diagram)
    if not path.is_file() or path.stat().st_size == 0:
        fail(f"diagram missing or empty: {path}")

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        fail(f"invalid XML: {exc}")

    root = tree.getroot()
    if root.tag != "mxfile":
        fail("root element is not <mxfile>")
    diagrams = root.findall("diagram")
    if not diagrams:
        fail("no <diagram> page found")

    total_vertices = 0
    total_edges = 0
    iconish = 0
    for diagram in diagrams:
        vertex_count, edge_count, icon_count = validate_page(diagram)
        total_vertices += vertex_count
        total_edges += edge_count
        iconish += icon_count

    if total_vertices == 0:
        fail("diagram has no vertex nodes")
    if args.require_edge and total_edges == 0:
        fail("diagram has no connector edges")
    if args.require_icon and iconish == 0:
        fail("diagram has no recognized icon or embedded SVG node styles")

    print(
        f"OK: {path} has {len(diagrams)} page(s), {total_vertices} vertex node(s), "
        f"{total_edges} edge(s), {iconish} icon/generic node style(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

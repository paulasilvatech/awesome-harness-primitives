#!/usr/bin/env python3
"""Embed a local official SVG in a draw.io diagram with provenance metadata."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path


MAX_SVG_BYTES = 2_000_000
PROVIDERS = ("azure", "microsoft", "github")
USAGE_BASES = (
    "microsoft-architecture-terms",
    "github-octicons-mit",
    "github-brand-permission",
    "explicit-license",
)


def _local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def _validate_https_url(value: str, field: str) -> None:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"{field} must be an absolute HTTPS URL")


def _validate_date(value: str) -> None:
    try:
        retrieved = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("--retrieved must use YYYY-MM-DD") from exc
    if retrieved > date.today():
        raise ValueError("--retrieved cannot be in the future")


def _validate_usage_basis(provider: str, usage_basis: str) -> None:
    if provider in {"azure", "microsoft"} and usage_basis not in {
        "microsoft-architecture-terms",
        "explicit-license",
    }:
        raise ValueError(
            "Azure and Microsoft assets require microsoft-architecture-terms "
            "or explicit-license"
        )
    if provider == "github" and usage_basis not in {
        "github-octicons-mit",
        "github-brand-permission",
        "explicit-license",
    }:
        raise ValueError(
            "GitHub assets require github-octicons-mit, "
            "github-brand-permission, or explicit-license"
        )


def _validate_svg(path: Path) -> bytes:
    data = path.read_bytes()
    if not data:
        raise ValueError(f"SVG is empty: {path}")
    if len(data) > MAX_SVG_BYTES:
        raise ValueError(
            f"SVG exceeds the {MAX_SVG_BYTES}-byte safety limit: {path}"
        )

    upper = data.upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        raise ValueError("SVG must not contain a DOCTYPE or entity declaration")

    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f"SVG is not well-formed XML: {exc}") from exc

    if _local_name(root.tag).lower() != "svg":
        raise ValueError("SVG root element must be <svg>")

    forbidden_tags = {"script", "foreignobject", "iframe", "object", "embed"}
    for element in root.iter():
        if _local_name(element.tag).lower() in forbidden_tags:
            raise ValueError(
                f"SVG contains forbidden <{_local_name(element.tag)}> content"
            )
        for raw_name, raw_value in element.attrib.items():
            name = _local_name(raw_name).lower()
            value = raw_value.strip()
            lowered = value.lower()
            if name.startswith("on"):
                raise ValueError(f"SVG contains forbidden event handler '{name}'")
            if name in {"href", "src"} and value and not value.startswith("#"):
                raise ValueError(f"SVG contains external reference '{value}'")
            if "@import" in lowered or re.search(r"url\(\s*['\"]?(?:https?:)?//", lowered):
                raise ValueError("SVG contains an external stylesheet or URL")

    return data


def _indent_xml(element: ET.Element, level: int = 0) -> None:
    indentation = "\n" + "  " * level
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indentation + "  "
        for child in element:
            _indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indentation
    if level and (not element.tail or not element.tail.strip()):
        element.tail = indentation


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:40] or "official-icon"


def _load_page(
    diagram_path: Path, diagram_index: int
) -> tuple[ET.ElementTree, ET.Element]:
    try:
        tree = ET.parse(diagram_path)
    except ET.ParseError as exc:
        raise ValueError(f"draw.io XML is invalid: {exc}") from exc

    if tree.getroot().tag != "mxfile":
        raise ValueError("draw.io root element must be <mxfile>")

    diagrams = tree.getroot().findall("diagram")
    if not 0 <= diagram_index < len(diagrams):
        raise ValueError(
            f"--diagram-index {diagram_index} is outside 0..{len(diagrams) - 1}"
        )

    graph_root = diagrams[diagram_index].find("mxGraphModel/root")
    if graph_root is None:
        raise ValueError("compressed diagrams are not supported")
    return tree, graph_root


def add_icon(args: argparse.Namespace) -> str:
    diagram_path = Path(args.diagram)
    svg_path = Path(args.svg)
    if not diagram_path.is_file():
        raise ValueError(f"draw.io file not found: {diagram_path}")
    if not svg_path.is_file():
        raise ValueError(f"SVG file not found: {svg_path}")
    if args.width <= 0 or args.height <= 0:
        raise ValueError("--width and --height must be positive")

    _validate_https_url(args.source_url, "--source-url")
    _validate_https_url(args.terms_url, "--terms-url")
    _validate_date(args.retrieved)
    _validate_usage_basis(args.provider, args.usage_basis)
    svg_data = _validate_svg(svg_path)
    svg_sha256 = hashlib.sha256(svg_data).hexdigest()

    tree, graph_root = _load_page(diagram_path, args.diagram_index)
    existing_ids = {
        cell.get("id")
        for cell in graph_root.findall("mxCell")
        if cell.get("id")
    }
    if args.parent not in existing_ids:
        raise ValueError(f"parent cell does not exist: {args.parent}")

    node_id = args.node_id or (
        f"icon-{_slug(args.product)}-"
        f"{hashlib.sha256(f'{args.product}:{args.x}:{args.y}:{svg_sha256}'.encode()).hexdigest()[:8]}"
    )
    if node_id in existing_ids:
        raise ValueError(
            f"cell id already exists: {node_id}; choose a unique --node-id"
        )

    encoded_svg = urllib.parse.quote_from_bytes(svg_data, safe="")
    style = (
        "shape=image;html=1;imageAspect=1;aspect=fixed;"
        "verticalLabelPosition=bottom;verticalAlign=top;align=center;"
        f"spacingTop=4;image=data:image/svg+xml,{encoded_svg};"
    )
    attributes = {
        "id": node_id,
        "value": args.product,
        "style": style,
        "vertex": "1",
        "parent": args.parent,
        "iconOfficial": "true",
        "iconProvider": args.provider,
        "iconProduct": args.product,
        "iconSource": args.source_url,
        "iconTerms": args.terms_url,
        "iconRetrieved": args.retrieved,
        "iconUsageBasis": args.usage_basis,
        "iconMethod": "embedded-svg",
        "iconSha256": svg_sha256,
    }
    cell = ET.Element("mxCell", attributes)
    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "x": str(args.x),
            "y": str(args.y),
            "width": str(args.width),
            "height": str(args.height),
            "as": "geometry",
        },
    )

    if not args.dry_run:
        graph_root.append(cell)
        _indent_xml(tree.getroot())
        tree.write(diagram_path, encoding="utf-8", xml_declaration=True)

    action = "Would add" if args.dry_run else "Added"
    return (
        f"{action} official icon '{args.product}' as cell '{node_id}' "
        f"(provider={args.provider}, sha256={svg_sha256})"
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Embed a local official SVG in an uncompressed .drawio file "
            "with provenance metadata."
        )
    )
    parser.add_argument("diagram", help="Path to the .drawio file")
    parser.add_argument("svg", help="Path to the local official SVG")
    parser.add_argument("product", help="Exact official product or service name")
    parser.add_argument("x", type=int, help="X coordinate")
    parser.add_argument("y", type=int, help="Y coordinate")
    parser.add_argument("--provider", required=True, choices=PROVIDERS)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--terms-url", required=True)
    parser.add_argument("--retrieved", required=True, help="Retrieval date YYYY-MM-DD")
    parser.add_argument("--usage-basis", required=True, choices=USAGE_BASES)
    parser.add_argument("--node-id")
    parser.add_argument("--parent", default="1")
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--height", type=int, default=64)
    parser.add_argument("--diagram-index", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        print(add_icon(_parse_args(argv)))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

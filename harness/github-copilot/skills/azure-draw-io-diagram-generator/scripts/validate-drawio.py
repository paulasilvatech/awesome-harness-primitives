#!/usr/bin/env python3
"""Validate draw.io structure, self-containment, and official icon provenance."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path


PROVIDERS = {"azure", "microsoft", "github"}
USAGE_BASES = {
    "microsoft-architecture-terms",
    "github-octicons-mit",
    "github-brand-permission",
    "explicit-license",
}
PROVENANCE_FIELDS = (
    "iconProvider",
    "iconProduct",
    "iconSource",
    "iconTerms",
    "iconRetrieved",
    "iconUsageBasis",
    "iconMethod",
    "iconSha256",
)
VENDOR_STENCIL_HINTS = ("mxgraph.azure", "mxgraph.mscae", "mscae/", "mxgraph.gcp2.github")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _https_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _style_image(style: str) -> str | None:
    marker = "image="
    start = style.find(marker)
    if start < 0:
        return None
    value = style[start + len(marker) :]
    if value.startswith("data:image/svg+xml;base64,"):
        payload = value[len("data:image/svg+xml;base64,") :].split(";", 1)[0]
        return f"data:image/svg+xml;base64,{payload}"
    return value.split(";", 1)[0]


def _embedded_svg_bytes(image: str) -> bytes | None:
    base64_prefix = "data:image/svg+xml;base64,"
    plain_prefix = "data:image/svg+xml,"
    try:
        if image.startswith(base64_prefix):
            return base64.b64decode(image[len(base64_prefix) :], validate=True)
        if image.startswith(plain_prefix):
            return urllib.parse.unquote_to_bytes(image[len(plain_prefix) :])
    except (ValueError, binascii.Error):
        return None
    return None


def _is_title_style(style: str) -> bool:
    return (
        (style.startswith("text;") or ";text;" in style)
        and "fontSize=18" in style
    )


def _validate_usage(provider: str, usage_basis: str) -> bool:
    if usage_basis not in USAGE_BASES:
        return False
    if provider in {"azure", "microsoft"}:
        return usage_basis in {"microsoft-architecture-terms", "explicit-license"}
    if provider == "github":
        return usage_basis in {
            "github-octicons-mit",
            "github-brand-permission",
            "explicit-license",
        }
    return False


def _validate_official_icon(
    cell: ET.Element, prefix: str, errors: list[str]
) -> None:
    cell_id = cell.get("id", "<unknown>")
    for field in PROVENANCE_FIELDS:
        if not cell.get(field):
            errors.append(f"{prefix} Official icon '{cell_id}' lacks {field}")

    if any(not cell.get(field) for field in PROVENANCE_FIELDS):
        return

    provider = cell.get("iconProvider", "")
    usage_basis = cell.get("iconUsageBasis", "")
    if provider not in PROVIDERS:
        errors.append(
            f"{prefix} Official icon '{cell_id}' has unsupported provider '{provider}'"
        )
    if not _validate_usage(provider, usage_basis):
        errors.append(
            f"{prefix} Official icon '{cell_id}' has incompatible usage basis "
            f"'{usage_basis}' for provider '{provider}'"
        )

    for field in ("iconSource", "iconTerms"):
        if not _https_url(cell.get(field, "")):
            errors.append(
                f"{prefix} Official icon '{cell_id}' {field} must be an HTTPS URL"
            )

    try:
        retrieved = date.fromisoformat(cell.get("iconRetrieved", ""))
        if retrieved > date.today():
            errors.append(
                f"{prefix} Official icon '{cell_id}' retrieval date is in the future"
            )
    except ValueError:
        errors.append(
            f"{prefix} Official icon '{cell_id}' iconRetrieved must use YYYY-MM-DD"
        )

    product = cell.get("iconProduct", "")
    if cell.get("value", "").strip() != product:
        errors.append(
            f"{prefix} Official icon '{cell_id}' label must equal iconProduct "
            f"('{product}')"
        )

    style = cell.get("style", "")
    if "aspect=fixed" not in style or "imageAspect=1" not in style:
        errors.append(
            f"{prefix} Official icon '{cell_id}' must preserve its aspect ratio"
        )

    method = cell.get("iconMethod", "")
    image = _style_image(style)
    if method == "embedded-svg":
        if image is None:
            errors.append(
                f"{prefix} Official icon '{cell_id}' has no embedded SVG image"
            )
            return
        svg_bytes = _embedded_svg_bytes(image)
        if svg_bytes is None:
            errors.append(
                f"{prefix} Official icon '{cell_id}' has an invalid SVG data URI"
            )
            return
        expected = cell.get("iconSha256", "")
        if not SHA256_PATTERN.fullmatch(expected):
            errors.append(
                f"{prefix} Official icon '{cell_id}' has an invalid SHA-256 value"
            )
        elif hashlib.sha256(svg_bytes).hexdigest() != expected:
            errors.append(
                f"{prefix} Official icon '{cell_id}' SVG does not match iconSha256"
            )
    elif method == "drawio-stencil":
        if not cell.get("iconLibraryVersion"):
            errors.append(
                f"{prefix} Stencil icon '{cell_id}' lacks iconLibraryVersion"
            )
    else:
        errors.append(
            f"{prefix} Official icon '{cell_id}' has unsupported method '{method}'"
        )


def validate_file(
    path: Path,
    require_official_icons: bool = False,
    require_icon_provenance: bool = False,
) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    counts = {"pages": 0, "vertices": 0, "edges": 0, "official_icons": 0}

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"XML parse error: {exc}"], counts

    root = tree.getroot()
    if root.tag != "mxfile":
        return [f"Root element must be <mxfile>, got <{root.tag}>"], counts

    diagrams = root.findall("diagram")
    if not diagrams:
        return ["No <diagram> elements found inside <mxfile>"], counts
    counts["pages"] = len(diagrams)

    for index, diagram in enumerate(diagrams):
        page_name = diagram.get("name", f"page-{index}")
        prefix = f"[diagram '{page_name}']"
        graph_root = diagram.find("mxGraphModel/root")
        if graph_root is None:
            errors.append(
                f"{prefix} Compressed or malformed page cannot be validated; "
                "save as uncompressed mxGraph XML"
            )
            continue

        cells = graph_root.findall("mxCell")
        ids: dict[str, ET.Element] = {}
        for cell in cells:
            cell_id = cell.get("id")
            if not cell_id:
                errors.append(f"{prefix} Found <mxCell> without an id")
                continue
            if cell_id in ids:
                errors.append(f"{prefix} Duplicate cell id='{cell_id}'")
            ids[cell_id] = cell

        if not cells or cells[0].get("id") != "0":
            errors.append(f"{prefix} First <mxCell> must have id='0'")
        if len(cells) < 2 or cells[1].get("id") != "1":
            errors.append(f"{prefix} Second <mxCell> must have id='1'")
        if "1" in ids and ids["1"].get("parent") != "0":
            errors.append(f"{prefix} Cell id='1' must have parent='0'")

        if not any(
            cell.get("vertex") == "1"
            and _is_title_style(cell.get("style", ""))
            for cell in cells
        ):
            errors.append(
                f"{prefix} No title cell with text style and fontSize=18"
            )

        for cell in cells:
            cell_id = cell.get("id", "<unknown>")
            if cell_id != "0":
                parent = cell.get("parent")
                if parent is None:
                    errors.append(f"{prefix} Cell '{cell_id}' lacks a parent")
                elif parent not in ids:
                    errors.append(
                        f"{prefix} Cell '{cell_id}' references unknown parent '{parent}'"
                    )

            is_vertex = cell.get("vertex") == "1"
            is_edge = cell.get("edge") == "1"
            if is_vertex:
                counts["vertices"] += 1
                geometry = cell.find("mxGeometry")
                if geometry is None:
                    errors.append(f"{prefix} Vertex '{cell_id}' lacks mxGeometry")
                style = cell.get("style", "")
                if not style:
                    errors.append(f"{prefix} Vertex '{cell_id}' lacks a style")
                image = _style_image(style)
                if image and (
                    image.startswith("http://")
                    or image.startswith("https://")
                    or image.startswith("//")
                ):
                    errors.append(
                        f"{prefix} Vertex '{cell_id}' uses an external image URL"
                    )

                official = cell.get("iconOfficial") == "true"
                embedded_svg = image is not None and image.startswith(
                    "data:image/svg+xml"
                )
                vendor_stencil = any(
                    hint in style for hint in VENDOR_STENCIL_HINTS
                )
                if official:
                    counts["official_icons"] += 1
                    _validate_official_icon(cell, prefix, errors)
                elif require_icon_provenance and (embedded_svg or vendor_stencil):
                    errors.append(
                        f"{prefix} Icon-like vertex '{cell_id}' lacks official "
                        "provenance metadata"
                    )

            if is_edge:
                counts["edges"] += 1
                source = cell.get("source")
                target = cell.get("target")
                geometry = cell.find("mxGeometry")
                has_source_point = geometry is not None and any(
                    point.get("as") == "sourcePoint"
                    for point in geometry.findall("mxPoint")
                )
                has_target_point = geometry is not None and any(
                    point.get("as") == "targetPoint"
                    for point in geometry.findall("mxPoint")
                )
                if source is None and not has_source_point:
                    errors.append(f"{prefix} Edge '{cell_id}' lacks a source")
                elif source is not None and source not in ids:
                    errors.append(
                        f"{prefix} Edge '{cell_id}' has unknown source '{source}'"
                    )
                if target is None and not has_target_point:
                    errors.append(f"{prefix} Edge '{cell_id}' lacks a target")
                elif target is not None and target not in ids:
                    errors.append(
                        f"{prefix} Edge '{cell_id}' has unknown target '{target}'"
                    )

    if require_official_icons and counts["official_icons"] == 0:
        errors.append("Diagram contains no provenance-marked official icon")
    return errors, counts


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate draw.io structure, self-containment, and official icon provenance."
        )
    )
    parser.add_argument("diagram", help="Path to a .drawio file")
    parser.add_argument("--require-official-icons", action="store_true")
    parser.add_argument("--require-icon-provenance", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    path = Path(args.diagram)
    if not path.is_file():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        return 1

    errors, counts = validate_file(
        path,
        require_official_icons=args.require_official_icons,
        require_icon_provenance=args.require_icon_provenance,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(
        "PASS: "
        f"{counts['pages']} page(s), "
        f"{counts['vertices']} vertex node(s), "
        f"{counts['edges']} edge(s), "
        f"{counts['official_icons']} official icon(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

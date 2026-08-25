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


BASE64_SVG_PREFIX = "data:image/svg+xml;base64,"
PLAIN_SVG_PREFIX = "data:image/svg+xml,"
DATA_SVG_PREFIX = "data:image/svg+xml"
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
VENDOR_STENCIL_HINTS = (
    "mxgraph.azure",
    "mxgraph.mscae",
    "mscae/",
    "mxgraph.gcp2.github",
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _https_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _provider_owns_url(provider: str, value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()
    if provider in {"azure", "microsoft"}:
        microsoft_host = host == "microsoft.com" or host.endswith(".microsoft.com")
        azure_icon_host = host == "arch-center.azureedge.net"
        microsoft_github = host == "github.com" and path.startswith("/microsoft/")
        return microsoft_host or azure_icon_host or microsoft_github
    if provider == "github":
        return host in {"brand.github.com", "primer.style"} or host == "github.com"
    return False


def _style_image(style: str) -> str | None:
    marker = "image="
    start = style.find(marker)
    if start < 0:
        return None
    value = style[start + len(marker) :]
    if value.startswith(BASE64_SVG_PREFIX):
        payload = value[len(BASE64_SVG_PREFIX) :].split(";", 1)[0]
        return f"{BASE64_SVG_PREFIX}{payload}"
    return value.split(";", 1)[0]


def _embedded_svg_bytes(image: str) -> bytes | None:
    if image.startswith(BASE64_SVG_PREFIX):
        try:
            return base64.b64decode(
                image[len(BASE64_SVG_PREFIX) :],
                validate=True,
            )
        except binascii.Error:
            return None
    if image.startswith(PLAIN_SVG_PREFIX):
        return urllib.parse.unquote_to_bytes(image[len(PLAIN_SVG_PREFIX) :])
    return None


def _is_external_image(image: str) -> bool:
    parsed = urllib.parse.urlparse(image)
    return parsed.scheme.lower() in {"http", "https"} or image.startswith("//")


def _is_title_style(style: str) -> bool:
    text_style = style.startswith("text;") or ";text;" in style
    return text_style and "fontSize=18" in style


def _validate_usage(provider: str, usage_basis: str) -> bool:
    if usage_basis not in USAGE_BASES:
        return False
    allowed = {
        "azure": {"microsoft-architecture-terms", "explicit-license"},
        "microsoft": {"microsoft-architecture-terms", "explicit-license"},
        "github": {
            "github-octicons-mit",
            "github-brand-permission",
            "explicit-license",
        },
    }
    return usage_basis in allowed.get(provider, set())


def _required_provenance_errors(
    cell: ET.Element,
    prefix: str,
) -> list[str]:
    cell_id = cell.get("id", "<unknown>")
    return [
        f"{prefix} Official icon '{cell_id}' lacks {field}"
        for field in PROVENANCE_FIELDS
        if not cell.get(field)
    ]


def _provider_errors(cell: ET.Element, prefix: str) -> list[str]:
    errors: list[str] = []
    cell_id = cell.get("id", "<unknown>")
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
    return errors


def _source_errors(cell: ET.Element, prefix: str) -> list[str]:
    errors: list[str] = []
    cell_id = cell.get("id", "<unknown>")
    provider = cell.get("iconProvider", "")
    for field in ("iconSource", "iconTerms"):
        value = cell.get(field, "")
        if not _https_url(value):
            errors.append(
                f"{prefix} Official icon '{cell_id}' {field} must be an HTTPS URL"
            )
        elif not _provider_owns_url(provider, value):
            errors.append(
                f"{prefix} Official icon '{cell_id}' {field} is not a recognized "
                f"first-party {provider} URL"
            )
    return errors


def _retrieval_date_errors(cell: ET.Element, prefix: str) -> list[str]:
    cell_id = cell.get("id", "<unknown>")
    try:
        retrieved = date.fromisoformat(cell.get("iconRetrieved", ""))
    except ValueError:
        return [
            f"{prefix} Official icon '{cell_id}' iconRetrieved must use YYYY-MM-DD"
        ]
    if retrieved > date.today():
        return [
            f"{prefix} Official icon '{cell_id}' retrieval date is in the future"
        ]
    return []


def _label_and_style_errors(cell: ET.Element, prefix: str) -> list[str]:
    errors: list[str] = []
    cell_id = cell.get("id", "<unknown>")
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
    return errors


def _embedded_method_errors(cell: ET.Element, prefix: str) -> list[str]:
    cell_id = cell.get("id", "<unknown>")
    image = _style_image(cell.get("style", ""))
    if image is None:
        return [f"{prefix} Official icon '{cell_id}' has no embedded SVG image"]
    svg_bytes = _embedded_svg_bytes(image)
    if svg_bytes is None:
        return [f"{prefix} Official icon '{cell_id}' has an invalid SVG data URI"]

    expected = cell.get("iconSha256", "")
    if not SHA256_PATTERN.fullmatch(expected):
        return [f"{prefix} Official icon '{cell_id}' has an invalid SHA-256 value"]
    if hashlib.sha256(svg_bytes).hexdigest() != expected:
        return [
            f"{prefix} Official icon '{cell_id}' SVG does not match iconSha256"
        ]
    return []


def _stencil_method_errors(cell: ET.Element, prefix: str) -> list[str]:
    if cell.get("iconLibraryVersion"):
        return []
    cell_id = cell.get("id", "<unknown>")
    return [f"{prefix} Stencil icon '{cell_id}' lacks iconLibraryVersion"]


def _method_errors(cell: ET.Element, prefix: str) -> list[str]:
    method = cell.get("iconMethod", "")
    if method == "embedded-svg":
        return _embedded_method_errors(cell, prefix)
    if method == "drawio-stencil":
        return _stencil_method_errors(cell, prefix)
    cell_id = cell.get("id", "<unknown>")
    return [
        f"{prefix} Official icon '{cell_id}' has unsupported method '{method}'"
    ]


def _official_icon_errors(cell: ET.Element, prefix: str) -> list[str]:
    errors = _required_provenance_errors(cell, prefix)
    if errors:
        return errors
    errors.extend(_provider_errors(cell, prefix))
    errors.extend(_source_errors(cell, prefix))
    errors.extend(_retrieval_date_errors(cell, prefix))
    errors.extend(_label_and_style_errors(cell, prefix))
    errors.extend(_method_errors(cell, prefix))
    return errors


def _collect_ids(
    cells: list[ET.Element],
    prefix: str,
) -> tuple[dict[str, ET.Element], list[str]]:
    ids: dict[str, ET.Element] = {}
    errors: list[str] = []
    for cell in cells:
        cell_id = cell.get("id")
        if not cell_id:
            errors.append(f"{prefix} Found <mxCell> without an id")
        elif cell_id in ids:
            errors.append(f"{prefix} Duplicate cell id='{cell_id}'")
        else:
            ids[cell_id] = cell
    return ids, errors


def _root_errors(
    cells: list[ET.Element],
    ids: dict[str, ET.Element],
    prefix: str,
) -> list[str]:
    errors: list[str] = []
    if not cells or cells[0].get("id") != "0":
        errors.append(f"{prefix} First <mxCell> must have id='0'")
    if len(cells) < 2 or cells[1].get("id") != "1":
        errors.append(f"{prefix} Second <mxCell> must have id='1'")
    if "1" in ids and ids["1"].get("parent") != "0":
        errors.append(f"{prefix} Cell id='1' must have parent='0'")
    return errors


def _title_errors(cells: list[ET.Element], prefix: str) -> list[str]:
    has_title = any(
        cell.get("vertex") == "1"
        and _is_title_style(cell.get("style", ""))
        for cell in cells
    )
    if has_title:
        return []
    return [f"{prefix} No title cell with text style and fontSize=18"]


def _parent_errors(
    cell: ET.Element,
    ids: dict[str, ET.Element],
    prefix: str,
) -> list[str]:
    cell_id = cell.get("id", "<unknown>")
    if cell_id == "0":
        return []
    parent = cell.get("parent")
    if parent is None:
        return [f"{prefix} Cell '{cell_id}' lacks a parent"]
    if parent not in ids:
        return [f"{prefix} Cell '{cell_id}' references unknown parent '{parent}'"]
    return []


def _icon_like(style: str, image: str | None) -> bool:
    embedded_svg = image is not None and image.startswith(DATA_SVG_PREFIX)
    vendor_stencil = any(hint in style for hint in VENDOR_STENCIL_HINTS)
    return embedded_svg or vendor_stencil


def _vertex_errors(
    cell: ET.Element,
    prefix: str,
    require_icon_provenance: bool,
) -> tuple[list[str], int]:
    errors: list[str] = []
    cell_id = cell.get("id", "<unknown>")
    if cell.find("mxGeometry") is None:
        errors.append(f"{prefix} Vertex '{cell_id}' lacks mxGeometry")

    style = cell.get("style", "")
    if not style:
        errors.append(f"{prefix} Vertex '{cell_id}' lacks a style")
    image = _style_image(style)
    if image and _is_external_image(image):
        errors.append(f"{prefix} Vertex '{cell_id}' uses an external image URL")

    official = cell.get("iconOfficial") == "true"
    if official:
        errors.extend(_official_icon_errors(cell, prefix))
        return errors, 1
    if require_icon_provenance and _icon_like(style, image):
        errors.append(
            f"{prefix} Icon-like vertex '{cell_id}' lacks official provenance metadata"
        )
    return errors, 0


def _has_endpoint_point(
    geometry: ET.Element | None,
    point_type: str,
) -> bool:
    return geometry is not None and any(
        point.get("as") == point_type
        for point in geometry.findall("mxPoint")
    )


def _endpoint_errors(
    cell_id: str,
    endpoint_name: str,
    endpoint: str | None,
    has_point: bool,
    ids: dict[str, ET.Element],
    prefix: str,
) -> list[str]:
    if endpoint is None and not has_point:
        return [f"{prefix} Edge '{cell_id}' lacks a {endpoint_name}"]
    if endpoint is not None and endpoint not in ids:
        return [
            f"{prefix} Edge '{cell_id}' has unknown {endpoint_name} '{endpoint}'"
        ]
    return []


def _edge_errors(
    cell: ET.Element,
    ids: dict[str, ET.Element],
    prefix: str,
) -> list[str]:
    cell_id = cell.get("id", "<unknown>")
    geometry = cell.find("mxGeometry")
    errors = _endpoint_errors(
        cell_id,
        "source",
        cell.get("source"),
        _has_endpoint_point(geometry, "sourcePoint"),
        ids,
        prefix,
    )
    errors.extend(
        _endpoint_errors(
            cell_id,
            "target",
            cell.get("target"),
            _has_endpoint_point(geometry, "targetPoint"),
            ids,
            prefix,
        )
    )
    return errors


def _cell_errors(
    cell: ET.Element,
    ids: dict[str, ET.Element],
    prefix: str,
    require_icon_provenance: bool,
) -> tuple[list[str], int, int]:
    errors = _parent_errors(cell, ids, prefix)
    if cell.get("vertex") == "1":
        vertex_errors, official_icons = _vertex_errors(
            cell,
            prefix,
            require_icon_provenance,
        )
        errors.extend(vertex_errors)
        return errors, 1, official_icons
    if cell.get("edge") == "1":
        errors.extend(_edge_errors(cell, ids, prefix))
        return errors, 0, 0
    return errors, 0, 0


def _validate_page(
    diagram: ET.Element,
    index: int,
    require_icon_provenance: bool,
) -> tuple[list[str], dict[str, int]]:
    counts = {"vertices": 0, "edges": 0, "official_icons": 0}
    page_name = diagram.get("name", f"page-{index}")
    prefix = f"[diagram '{page_name}']"
    graph_root = diagram.find("mxGraphModel/root")
    if graph_root is None:
        return [
            f"{prefix} Compressed or malformed page cannot be validated; "
            "save as uncompressed mxGraph XML"
        ], counts

    cells = graph_root.findall("mxCell")
    ids, errors = _collect_ids(cells, prefix)
    errors.extend(_root_errors(cells, ids, prefix))
    errors.extend(_title_errors(cells, prefix))

    for cell in cells:
        cell_errors, vertex_count, official_count = _cell_errors(
            cell,
            ids,
            prefix,
            require_icon_provenance,
        )
        errors.extend(cell_errors)
        counts["vertices"] += vertex_count
        counts["official_icons"] += official_count
        counts["edges"] += int(cell.get("edge") == "1")
    return errors, counts


def _empty_counts() -> dict[str, int]:
    return {"pages": 0, "vertices": 0, "edges": 0, "official_icons": 0}


def _merge_counts(total: dict[str, int], page: dict[str, int]) -> None:
    for key, value in page.items():
        total[key] += value


def validate_file(
    path: Path,
    require_official_icons: bool = False,
    require_icon_provenance: bool = False,
) -> tuple[list[str], dict[str, int]]:
    counts = _empty_counts()
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
    errors: list[str] = []
    for index, diagram in enumerate(diagrams):
        page_errors, page_counts = _validate_page(
            diagram,
            index,
            require_icon_provenance,
        )
        errors.extend(page_errors)
        _merge_counts(counts, page_counts)
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

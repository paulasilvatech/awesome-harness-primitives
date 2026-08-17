#!/usr/bin/env python3
"""Draw.io MCP server.

A Model Context Protocol server that creates and edits draw.io (.drawio)
architecture diagrams programmatically: create a diagram, add nodes with
official-style icons, group nodes in boundary containers, connect nodes with
orthogonal edges, apply a simple layered layout, and read the resulting XML.

Built with FastMCP. Diagram manipulation uses only the Python standard library
(xml.etree.ElementTree), so the only dependency is the MCP SDK.

The .drawio format is mxGraph XML. See the azure-architecture-diagrams skill
references for the format and the official icon catalogs. Icon style strings for
Azure and Microsoft stencils vary by draw.io version; verify them in your
target viewer, or embed an official SVG via a data URI for a self-contained file.

Run:
    pip install -r requirements.txt
    python drawio_mcp_server.py            # stdio transport (default)

Register the server with your MCP host (for example a "drawio" entry pointing at
this file) so an agent or GitHub Copilot can call its tools.
"""
from __future__ import annotations

import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    sys.exit(
        f"ERROR: missing dependency ({exc.name}).\n"
        "Install the MCP SDK first:\n"
        "  pip install -r .github/skills/azure-architecture-diagrams/scripts/requirements.txt"
    )

mcp = FastMCP("drawio")

# ---------------------------------------------------------------------------
# Icon catalog: friendly name -> draw.io style fragment.
#
# These are representative style fragments. Azure and Microsoft stencil names
# depend on the draw.io shape libraries installed in the viewer; verify the
# exact style string in your version, or use add_node_svg() to embed an official
# SVG inline for a fully self-contained file. GitHub marks can be embedded the
# same way from the MIT-licensed Octicons set.
# ---------------------------------------------------------------------------
ICON_STYLES: dict[str, str] = {
    # Generic shapes (always available in any draw.io viewer).
    "box": "rounded=1;whiteSpace=wrap;html=1;",
    "user": "shape=mxgraph.basic.user;html=1;",
    "internet": "ellipse;shape=cloud;whiteSpace=wrap;html=1;",
    "database": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;",
    "queue": "shape=mxgraph.flowchart.delay;html=1;",
    # Azure stencils (mscae / mxgraph.azure family). Verify per draw.io version.
    "azure.foundry": "sketch=0;html=1;shape=mxgraph.azure.machine_learning;",
    "azure.openai": "sketch=0;html=1;shape=mxgraph.azure.cognitive_services;",
    "azure.apim": "sketch=0;html=1;shape=mxgraph.azure.api_management_services;",
    "azure.redis": "sketch=0;html=1;shape=mxgraph.azure.azure_cache_redis;",
    "azure.search": "sketch=0;html=1;shape=mxgraph.azure.azure_search;",
    "azure.aks": "sketch=0;html=1;shape=mxgraph.azure.kubernetes_services;",
    "azure.containerapps": "sketch=0;html=1;shape=mxgraph.azure.app_services;",
    "azure.keyvault": "sketch=0;html=1;shape=mxgraph.azure.key_vaults;",
    "azure.monitor": "sketch=0;html=1;shape=mxgraph.azure.monitor;",
    "azure.apicenter": "sketch=0;html=1;shape=mxgraph.azure.api_management_services;",
    "azure.entra": "sketch=0;html=1;shape=mxgraph.azure.azure_active_directory;",
    # GitHub (use embedded Octicons via add_node_svg for the official mark).
    "github": "shape=mxgraph.gcp2.github;html=1;",
}

# Boundary container styles, keyed by friendly name.
CONTAINER_STYLES: dict[str, str] = {
    "default": "rounded=0;dashed=1;verticalAlign=top;align=left;spacingLeft=8;html=1;fillColor=none;",
    "subscription": "rounded=0;dashed=1;verticalAlign=top;align=left;spacingLeft=8;html=1;fillColor=#F2FBFF;strokeColor=#00A4EF;",
    "resourcegroup": "rounded=0;dashed=1;verticalAlign=top;align=left;spacingLeft=8;html=1;fillColor=#FFFDF2;strokeColor=#FFB900;",
    "vnet": "rounded=0;dashed=1;verticalAlign=top;align=left;spacingLeft=8;html=1;fillColor=#F6FFF2;strokeColor=#7FBA00;",
    "trustzone": "rounded=0;dashed=1;verticalAlign=top;align=left;spacingLeft=8;html=1;fillColor=#FFF6F2;strokeColor=#F25022;",
}

EMPTY_DIAGRAM = (
    '<mxfile host="app.diagrams.net">'
    '<diagram name="{name}" id="page1">'
    '<mxGraphModel dx="1024" dy="768" grid="1" gridSize="10" guides="1" '
    'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageWidth="1169" '
    'pageHeight="826" math="0" shadow="0">'
    "<root>"
    '<mxCell id="0" />'
    '<mxCell id="1" parent="0" />'
    "</root>"
    "</mxGraphModel>"
    "</diagram>"
    "</mxfile>"
)


def _load(path: str) -> ET.ElementTree:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Diagram not found: {path}. Call create_diagram first.")
    return ET.parse(path)


def _root_cell(tree: ET.ElementTree) -> ET.Element:
    root = tree.getroot().find(".//mxGraphModel/root")
    if root is None:
        raise ValueError("Malformed .drawio file: no <root> element.")
    return root


def _exists(root: ET.Element, cell_id: str) -> bool:
    return any(c.get("id") == cell_id for c in root.findall("mxCell"))


def _save(tree: ET.ElementTree, path: str) -> None:
    tree.write(path, encoding="utf-8", xml_declaration=True)


@mcp.tool()
def create_diagram(path: str, name: str = "Architecture") -> str:
    """Create a new empty .drawio diagram file.

    Args:
        path: Absolute or workspace-relative path ending in .drawio.
        name: The diagram page name.

    Returns:
        A confirmation message with the path.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>' + EMPTY_DIAGRAM.format(name=name))
    return f"Created diagram '{name}' at {path}"


@mcp.tool()
def list_icons(filter: str = "") -> str:
    """List the built-in icon keys usable as the 'icon' argument of add_node.

    Args:
        filter: Optional substring to filter icon keys (for example 'azure').

    Returns:
        A newline-separated list of icon keys.
    """
    keys = sorted(k for k in ICON_STYLES if filter.lower() in k.lower())
    return "\n".join(keys) if keys else "No icons match the filter."


@mcp.tool()
def add_node(
    path: str,
    node_id: str,
    label: str,
    icon: str = "box",
    x: int = 40,
    y: int = 40,
    width: int = 80,
    height: int = 80,
    parent: str = "1",
) -> str:
    """Add a node (vertex) to the diagram.

    Args:
        path: Path to the .drawio file.
        node_id: Unique id for the node.
        label: The visible label (use the exact service name).
        icon: An icon key from list_icons (for example 'azure.apim'), or 'box'.
        x, y: Top-left position.
        width, height: Node size.
        parent: Parent cell id ('1' for the base layer, or a container id).

    Returns:
        A confirmation message.
    """
    tree = _load(path)
    root = _root_cell(tree)
    if _exists(root, node_id):
        raise ValueError(f"Node id '{node_id}' already exists.")
    style = ICON_STYLES.get(icon)
    if style is None:
        raise ValueError(f"Unknown icon '{icon}'. Call list_icons to see options.")
    style = f"{style}verticalLabelPosition=bottom;verticalAlign=top;"
    cell = ET.SubElement(
        root,
        "mxCell",
        {"id": node_id, "value": label, "style": style, "vertex": "1", "parent": parent},
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
    )
    _save(tree, path)
    return f"Added node '{node_id}' ({label}) with icon '{icon}'."


@mcp.tool()
def add_node_svg(
    path: str,
    node_id: str,
    label: str,
    svg_markup: str,
    x: int = 40,
    y: int = 40,
    width: int = 80,
    height: int = 80,
    parent: str = "1",
) -> str:
    """Add a node whose icon is an official SVG embedded inline (data URI).

    Use this to place an official Azure, Microsoft, or GitHub (Octicons) SVG so
    the .drawio file is self-contained and the icon resolves in any viewer. Do
    not modify or re-color official product icons.

    Args:
        path: Path to the .drawio file.
        node_id: Unique id for the node.
        label: The visible label.
        svg_markup: The full <svg>...</svg> markup of the official icon.
        x, y, width, height: Position and size.
        parent: Parent cell id.

    Returns:
        A confirmation message.
    """
    tree = _load(path)
    root = _root_cell(tree)
    if _exists(root, node_id):
        raise ValueError(f"Node id '{node_id}' already exists.")
    encoded = urllib.parse.quote(svg_markup.strip())
    style = (
        f"shape=image;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
        f"image=data:image/svg+xml,{encoded};"
    )
    cell = ET.SubElement(
        root,
        "mxCell",
        {"id": node_id, "value": label, "style": style, "vertex": "1", "parent": parent},
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
    )
    _save(tree, path)
    return f"Added SVG node '{node_id}' ({label})."


@mcp.tool()
def add_container(
    path: str,
    node_id: str,
    label: str,
    x: int = 20,
    y: int = 20,
    width: int = 480,
    height: int = 320,
    kind: str = "default",
) -> str:
    """Add a boundary container (subscription, resource group, VNet, trust zone).

    Place nodes inside it by passing parent=node_id to add_node, with x and y
    relative to the container.

    Args:
        path: Path to the .drawio file.
        node_id: Unique id for the container.
        label: The boundary label.
        x, y, width, height: Position and size.
        kind: One of 'default', 'subscription', 'resourcegroup', 'vnet', 'trustzone'.

    Returns:
        A confirmation message.
    """
    tree = _load(path)
    root = _root_cell(tree)
    if _exists(root, node_id):
        raise ValueError(f"Container id '{node_id}' already exists.")
    style = CONTAINER_STYLES.get(kind, CONTAINER_STYLES["default"])
    cell = ET.SubElement(
        root,
        "mxCell",
        {"id": node_id, "value": label, "style": style, "vertex": "1", "parent": "1"},
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"},
    )
    _save(tree, path)
    return f"Added container '{node_id}' ({label}, kind={kind})."


@mcp.tool()
def connect_nodes(
    path: str,
    edge_id: str,
    source_id: str,
    target_id: str,
    label: str = "",
    dashed: bool = False,
) -> str:
    """Connect two nodes with an orthogonal edge.

    Args:
        path: Path to the .drawio file.
        edge_id: Unique id for the edge.
        source_id: Source node id.
        target_id: Target node id.
        label: Optional edge label (for example a protocol like HTTPS).
        dashed: Whether the edge is dashed.

    Returns:
        A confirmation message.
    """
    tree = _load(path)
    root = _root_cell(tree)
    for ref in (source_id, target_id):
        if not _exists(root, ref):
            raise ValueError(f"Node id '{ref}' does not exist.")
    if _exists(root, edge_id):
        raise ValueError(f"Edge id '{edge_id}' already exists.")
    style = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;"
    if dashed:
        style += "dashed=1;"
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": edge_id,
            "value": label,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source_id,
            "target": target_id,
        },
    )
    geo = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    geo.text = ""
    _save(tree, path)
    return f"Connected '{source_id}' to '{target_id}' as edge '{edge_id}'."


@mcp.tool()
def auto_layout(path: str, direction: str = "horizontal", spacing: int = 160, start_x: int = 40, start_y: int = 80) -> str:
    """Apply a simple layered layout to top-level nodes.

    Positions top-level vertices (parent='1', excluding containers and edges) in
    a single row or column. For complex layouts, position nodes explicitly or
    open the file in draw.io and run its tree or organic layout.

    Args:
        path: Path to the .drawio file.
        direction: 'horizontal' or 'vertical'.
        spacing: Distance between node origins.
        start_x, start_y: Origin of the first node.

    Returns:
        A confirmation message with the count of positioned nodes.
    """
    tree = _load(path)
    root = _root_cell(tree)
    n = 0
    for cell in root.findall("mxCell"):
        if cell.get("vertex") != "1" or cell.get("parent") != "1":
            continue
        style = cell.get("style", "")
        if "dashed=1" in style and "fillColor=none" in style:
            continue  # skip boundary containers
        geo = cell.find("mxGeometry")
        if geo is None:
            continue
        if direction == "vertical":
            geo.set("x", str(start_x))
            geo.set("y", str(start_y + n * spacing))
        else:
            geo.set("x", str(start_x + n * spacing))
            geo.set("y", str(start_y))
        n += 1
    _save(tree, path)
    return f"Laid out {n} node(s) {direction}ly with spacing {spacing}."


@mcp.tool()
def get_diagram_xml(path: str) -> str:
    """Return the raw .drawio XML so the result can be inspected or embedded.

    Args:
        path: Path to the .drawio file.

    Returns:
        The file contents as a string.
    """
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


@mcp.tool()
def export_hint(path: str) -> str:
    """Return instructions to export the diagram to SVG.

    Programmatic SVG export needs the draw.io desktop CLI or the diagrams.net
    export service, which may not be present in every environment. This returns
    the portable steps.

    Args:
        path: Path to the .drawio file.

    Returns:
        Export guidance.
    """
    return (
        "To export to SVG:\n"
        f"1. Open {path} in draw.io / diagrams.net or the VS Code Draw.io extension.\n"
        "2. File > Export as > SVG, and enable 'Embed Images' for a self-contained file.\n"
        "3. Or use the draw.io desktop CLI: "
        f"drawio --export --format svg --embed-svg-images --output diagram.svg {path}\n"
        "Verify the CLI flags for your draw.io desktop version."
    )


if __name__ == "__main__":
    mcp.run()

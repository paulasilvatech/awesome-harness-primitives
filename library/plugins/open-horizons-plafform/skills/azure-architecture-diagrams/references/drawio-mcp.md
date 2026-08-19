# Draw.io MCP Server Usage

A Model Context Protocol server that creates and edits `.drawio` diagrams programmatically. It lets an agent (or GitHub Copilot) build architecture diagrams with official-style icons, group them by boundary, connect them, and lay them out, producing an editable file.

The server is at [../scripts/drawio_mcp_server.py](../scripts/drawio_mcp_server.py).

## Install and run

```bash
cd .github/skills/azure-architecture-diagrams/scripts
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python drawio_mcp_server.py        # stdio transport
```

If the MCP SDK is missing, the server exits with an install message instead of a Python traceback. The XML validator does not need MCP and can be run before the server is registered:

```bash
python scripts/validate_drawio.py assets/example-agentic.drawio --require-icon --require-edge
```

## Register with an MCP host

Add an entry so your host launches the server. Example shape (adapt paths and the config location to your host):

```json
{
  "mcpServers": {
    "drawio": {
      "command": "python",
      "args": [".github/skills/azure-architecture-diagrams/scripts/drawio_mcp_server.py"]
    }
  }
}
```

For VS Code MCP configuration, place an equivalent entry in your MCP settings and start the server from the MCP view. Verify the exact configuration format for your client version.

## Tools

| Tool | Purpose |
| --- | --- |
| `create_diagram(path, name)` | Create a new empty `.drawio` file. |
| `list_icons(filter)` | List built-in icon keys (for example `azure.apim`, `azure.redis`, `github`). |
| `add_node(path, node_id, label, icon, x, y, width, height, parent)` | Add a node with a built-in icon style. |
| `add_node_svg(path, node_id, label, svg_markup, ...)` | Add a node whose icon is an official SVG embedded inline (self-contained, resolves anywhere). |
| `add_container(path, node_id, label, x, y, width, height, kind)` | Add a boundary (subscription, resource group, VNet, trust zone). |
| `connect_nodes(path, edge_id, source_id, target_id, label, dashed)` | Connect two nodes with an orthogonal edge. |
| `auto_layout(path, direction, spacing, start_x, start_y)` | Lay out top-level nodes in a row or column. |
| `get_diagram_xml(path)` | Return the raw XML to inspect or embed. |
| `export_hint(path)` | Return the steps to export SVG. |

## Typical flow

1. `create_diagram("output/agentic-context.drawio", "System Context")`
2. `add_container(... kind="subscription")` for each boundary.
3. `add_node(... icon="azure.foundry")`, `add_node(... icon="azure.redis")`, `add_node(... icon="github")`, and so on. Use `add_node_svg` to embed the official Azure or GitHub SVG for a self-contained file.
4. `connect_nodes(...)` for each relationship, labeling protocols.
5. `auto_layout(...)` for a quick arrangement, or set positions explicitly for precise layouts.
6. `export_hint(...)` then export SVG from draw.io, and embed the SVG in the Markdown deliverable.

## Notes on icons

- The built-in icon keys map to draw.io Azure stencil styles whose names vary by version. For guaranteed resolution and a self-contained file, prefer `add_node_svg` with the official Azure, Microsoft, or GitHub (Octicons) SVG markup.
- Never modify or re-color official product icons. Color the containers and connectors instead. See [icon-catalogs.md](icon-catalogs.md).

## Sources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP in the MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [draw.io file format](https://www.drawio.com/doc/faq/format-of-files)

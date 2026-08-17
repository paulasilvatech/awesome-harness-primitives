---
name: azure-architecture-diagrams
description: "Produce complete, professional architecture diagrams that use the official Azure, Microsoft, and GitHub (Octicons) icon sets, output as editable draw.io (.drawio) files and exported SVG. Covers the official icon catalogs and their terms of use, the draw.io mxGraph file format, layout and connector conventions, and a bundled draw.io MCP server (Python FastMCP) that creates and edits .drawio diagrams programmatically (add nodes with official icons, connect edges, group, and lay out). Use whenever the deliverable includes an architecture diagram, a system context, a component or deployment diagram, or any cloud diagram that must use official vendor icons. Pairs with ai-native-engineer and agentic-architecture-patterns, and complements svg-professional for hand-crafted SVG."
argument-hint: "what to diagram, for example an agentic platform on Foundry with Redis, APIM, and API Center"
---

# Azure Architecture Diagrams

Build complete architecture diagrams with the **official Azure, Microsoft, and GitHub icons**, delivered as editable `.drawio` files plus exported SVG. This skill provides the icon catalogs, the file format, the layout conventions, and a draw.io MCP server that creates and edits diagrams programmatically.

> Respect icon terms of use. Azure and Microsoft icons may be used to depict their products in architecture diagrams and must not be modified or re-colored. GitHub Octicons are MIT licensed; the GitHub logos follow the GitHub brand guidelines. See [references/icon-catalogs.md](references/icon-catalogs.md).

## What this skill produces

- **`.drawio` source** (editable in draw.io / diagrams.net and the VS Code extension).
- **Exported SVG** for embedding in Markdown and the paulasilva-ms documents and decks.
- Diagrams that use official vendor shapes, with consistent layout, grouping, and connector routing.

## Professional baseline from assets

Use the bundled showcase as the visual quality baseline for enterprise diagrams that mix technical and executive audiences. Do not force every architecture into one layout; choose the diagram shape that answers the question.

- Showcase gallery: [assets/showcase-diagrams.drawio](assets/showcase-diagrams.drawio)
- Selection guide: [references/diagram-showcase.md](references/diagram-showcase.md)

The gallery includes system context, component map, deployment topology, critical path flow, routing decision, and enterprise registry plane examples. Use these as starting points, then adapt the service map and icon set.

For dense enterprise registry diagrams, use the bundled Contoso MCP registry example as the quality baseline:

- Source baseline: [assets/example-agentic.drawio](assets/example-agentic.drawio)
- Production-ready baseline copy: [output/contoso-mcp-registry-production-baseline.drawio](output/contoso-mcp-registry-production-baseline.drawio)

When following this baseline, keep these style contracts:

- Horizontal planes (client, private access, discovery, use, governance) as clear grouped boundaries.
- Orthogonal connector routing with numbered callouts where sequence matters.
- Official Azure, Microsoft, and GitHub icons without recoloring product marks.
- High-contrast typography and short, executive-readable labels per node.
- One narrative title and one subtitle at the top, then protocol labels on edges.

## Diagram set for an AI-native system

Produce these as the default set (add or remove based on the audience and the question):

1. **System context**: actors (users, GitHub Copilot, GitHub Actions) and the system boundary.
2. **Component**: agent runtime, model router, cache and memory, retrieval, tools and MCP, gateway, guardrails, observability.
3. **Deployment**: subscriptions, resource groups, VNets, private endpoints, regions.
4. **Sequence or data and control flow**: the critical path of one agent run, including cache hit and miss.
5. **Decision or routing flow**: routing by risk, cost, data sensitivity, approval need, model class, or fallback.
6. **Enterprise plane view**: only for multi-plane architectures where access, discovery, use, and governance must fit on one canvas.

## Two ways to build

### A. Draw.io MCP server (preferred, programmatic)

A bundled Python MCP server creates and edits `.drawio` files through tools: create a diagram, add a node with an official icon, connect nodes, group, auto-lay out, and export. Register it with your MCP host and drive it from the agent. See [references/drawio-mcp.md](references/drawio-mcp.md) and the server at [scripts/drawio_mcp_server.py](scripts/drawio_mcp_server.py).

### B. Hand-authored mxGraph XML

For precise control, write the `.drawio` mxGraph XML directly using the icon styles. See [references/drawio-format.md](references/drawio-format.md).

For hand-crafted, non-icon SVG (quadrants, charts, bespoke infographics), use the `svg-professional` skill instead.

## Icon sources (official only)

- **Azure architecture icons**: the official downloadable SVG set. draw.io also ships an Azure shape library.
- **Microsoft product icons**: official sets for Microsoft 365, Entra, Power Platform, and more.
- **GitHub Octicons and logos**: Octicons (MIT) for GitHub UI marks; the GitHub mark and wordmark per brand guidelines.

Catalog details, download locations, and the draw.io shape style strings are in [references/icon-catalogs.md](references/icon-catalogs.md).

## Layout conventions

- Left to right or top to bottom flow; keep the primary path on one axis.
- Group by boundary (subscription, resource group, VNet, trust zone) with labeled containers.
- Orthogonal connectors, no crossings where avoidable, labels on edges for protocols.
- One accent color per boundary; do not re-color official product icons.
- Apply the paulasilva-ms palette to containers, labels, and connectors, never to the vendor icons themselves.

## Workflow

1. Take the service map from the design (from `ai-native-engineer` or `agentic-architecture-patterns`).
2. Choose the diagram types to produce using [references/diagram-showcase.md](references/diagram-showcase.md).
3. Build with the draw.io MCP (preferred) or hand-authored XML, placing official icons for each service.
4. Lay out, group by boundary, route connectors, and label.
5. Export SVG and embed it; keep the `.drawio` source under `output/`.
6. Run `scripts/validate_drawio.py` on the `.drawio` source, then verify the diagram opens and every icon resolves.
7. Walk `references/first-run-checklist.md` before delivery.
8. For enterprise registry layouts, compare against the Contoso baseline in `assets/example-agentic.drawio` before final export.

## References

- [Icon catalogs and terms of use](references/icon-catalogs.md)
- [Draw.io mxGraph file format](references/drawio-format.md)
- [Draw.io MCP server usage](references/drawio-mcp.md)
- [Diagram showcase and selection guide](references/diagram-showcase.md)
- [First-run checklist](references/first-run-checklist.md)
- [Azure architecture icons](https://learn.microsoft.com/azure/architecture/icons/)
- [GitHub Octicons](https://primer.style/octicons/)

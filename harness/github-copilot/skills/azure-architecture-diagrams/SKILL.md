---
name: azure-architecture-diagrams
description: >-
  Produce professional Azure, Microsoft, and GitHub architecture diagrams as editable draw.io source and exported SVG. Use when the user asks for an architecture diagram, system context diagram, component or deployment view, AI-native platform diagram, official vendor icons, mxGraph XML, or draw.io MCP-based diagram generation.
argument-hint: "what to diagram, for example an agentic platform on Foundry with Redis, APIM, and API Center"
---

# Azure architecture diagrams

Build complete architecture diagrams from a service map or written design, using official Azure, Microsoft, and GitHub icons, consistent layout, editable `.drawio` source, and exported SVG that can be embedded in documentation or decks.

## When to invoke

- "Create an Azure architecture diagram for this system."
- "Generate a draw.io component and deployment diagram with official icons."
- "Show the system context for this AI platform."
- "Export an editable .drawio and SVG for this cloud architecture."
- "Use the Contoso MCP registry diagram as a baseline."

## Inputs

Use `$ARGUMENTS` as the diagram brief: system purpose, audience, services, trust boundaries, regions, flows, and required output formats. If `$ARGUMENTS` is thin, infer only from provided repository or design context; do not invent products, regions, subscriptions, or compliance boundaries.

## Prerequisites and context

- Respect icon terms of use. Azure and Microsoft icons may be used to depict their products in architecture diagrams and must not be modified or re-colored.
- GitHub Octicons are MIT licensed; GitHub marks and wordmarks must follow GitHub brand guidelines.
- Use draw.io / diagrams.net-compatible `mxGraphModel` XML for `.drawio` source.
- Use `scripts/drawio_mcp_server.py` for programmatic creation when an MCP host can register the bundled Python FastMCP server; otherwise hand-author mxGraph XML.
- Keep editable source under `output/` when this skill produces files.

## Diagram deliverables

| Deliverable | Required content | Acceptance rule |
| --- | --- | --- |
| `.drawio` source | Valid draw.io XML with named pages, grouped boundaries, official icon styles, and routed connectors. | Opens in draw.io / diagrams.net without broken shapes. |
| Exported SVG | Same diagram exported for Markdown, docs, and paulasilva-ms documents and decks. | Embeds cleanly and preserves text legibility. |
| Narrative labels | One title, one subtitle, short node names, edge labels for protocol or data type. | Executive-readable at normal document size. |
| Icon attribution | Official Azure, Microsoft, and GitHub icons only for vendor products. | No recolored product marks and no generic substitute when an official icon exists. |

## Diagram set for AI-native systems

Produce the smallest set that answers the user's question. Default to these views for broad platform requests:

| View | Use when | Required elements |
| --- | --- | --- |
| System context | The audience needs actors and boundaries. | Users, GitHub Copilot, GitHub Actions, external systems, and the system boundary. |
| Component map | The audience needs runtime internals. | Agent runtime, model router, cache and memory, retrieval, tools and MCP, gateway, guardrails, observability. |
| Deployment topology | The audience needs infrastructure shape. | Subscriptions, resource groups, VNets, private endpoints, regions, and managed services. |
| Sequence or data/control flow | A critical path must be explained. | One agent run, cache hit and miss, approval, tool call, and observable result. |
| Decision or routing flow | A policy choice must be justified. | Risk, cost, data sensitivity, approval need, model class, fallback, and outcome. |
| Enterprise plane view | Multi-plane governance must fit on one canvas. | Access, discovery, use, governance, and shared registry/control planes. |

## Professional baseline

Use the bundled showcase as the quality bar, not as a rigid template.

| Resource | Use it for |
| --- | --- |
| `assets/showcase-diagrams.drawio` | Gallery of system context, component map, deployment topology, critical path flow, routing decision, and enterprise registry plane examples. |
| `references/diagram-showcase.md` | Selection guide for choosing the right diagram shape. |
| `assets/example-agentic.drawio` | Dense enterprise registry baseline. |
| `output/contoso-mcp-registry-production-baseline.drawio` | Production-ready baseline copy for comparison. |

For the Contoso MCP registry baseline, preserve horizontal planes for client, private access, discovery, use, and governance; use orthogonal connector routing; add numbered callouts only where sequence matters; keep official Azure, Microsoft, and GitHub icons unchanged; and use one narrative title plus one subtitle.

## Build paths

### Draw.io MCP server

Prefer the bundled MCP server for repeatable, programmatic work. It creates diagrams, adds nodes with official icons, connects edges, groups boundaries, applies layout, and exports files. Read `references/drawio-mcp.md` before registering or driving `scripts/drawio_mcp_server.py`.

### Hand-authored mxGraph XML

Use hand-authored XML when precise control matters or no MCP host is available. Follow `references/drawio-format.md`; keep pages valid `mxGraphModel`; use draw.io style strings from `references/icon-catalogs.md`; keep geometry, containers, and connectors explicit.

## Layout conventions

| Area | Rule |
| --- | --- |
| Flow | Use left-to-right or top-to-bottom flow; keep the primary path on one axis. |
| Boundaries | Group by subscription, resource group, VNet, trust zone, plane, or region. |
| Connectors | Use orthogonal connectors, avoid crossings, and label edges with protocol or intent. |
| Color | Apply the paulasilva-ms palette to containers, labels, and connectors, never to vendor icons. |
| Density | Prefer short labels and grouped zones over crowded explanatory text inside nodes. |
| Sequence | Use numbered callouts only when the order changes the interpretation. |

## Procedure

1. Inventory the actors, systems, services, data stores, trust boundaries, deployment units, and critical flows from the user brief or source material.
2. Choose the diagram types using `references/diagram-showcase.md`; remove views that do not answer the audience's question.
3. Choose the build path: draw.io MCP server for repeatable generation, or hand-authored mxGraph XML for exact control.
4. Place official icons for each service from `references/icon-catalogs.md`; use generic shapes only for non-vendor concepts.
5. Lay out the diagram, group boundaries, route connectors, label protocols, and add a narrative title/subtitle.
6. Save `.drawio` source under `output/`, export SVG, and keep the source editable.
7. Run `scripts/validate_drawio.py` on the `.drawio` source, verify it opens, and walk `references/first-run-checklist.md`.
8. For enterprise registry layouts, compare against `assets/example-agentic.drawio` and `output/contoso-mcp-registry-production-baseline.drawio` before delivery.

## Limits

- Use `svg-professional` for hand-crafted, non-icon SVG such as quadrants, charts, and bespoke infographics.
- Do not use this skill to invent architecture. If the service map is missing, produce a clearly marked draft with assumptions.
- Do not recolor, crop, distort, or alter official product icons.

## Progressive disclosure and bundled resources

- `references/icon-catalogs.md`: official icon sources, terms of use, download locations, and draw.io style strings.
- `references/drawio-format.md`: draw.io mxGraph file format for hand-authored XML.
- `references/drawio-mcp.md`: bundled draw.io MCP server usage.
- `references/diagram-showcase.md`: diagram type selection guide.
- `references/first-run-checklist.md`: final delivery checklist.
- `references/example-architecture.md`: example architecture source material.
- `scripts/drawio_mcp_server.py`: Python FastMCP diagram server.
- `scripts/validate_drawio.py`: draw.io validation script.
- `scripts/build_showcase_drawio.py`: showcase builder.
- `assets/showcase-diagrams.drawio` and `assets/example-agentic.drawio`: editable baselines.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `ai-native-engineer` | skill | You need to design the AI-native service map before diagramming it. |
| `agentic-architecture-patterns` | skill | You need agent architecture patterns before choosing diagram components. |
| `svg-professional` | skill | You need bespoke SVG rather than official-icon architecture diagrams. |

## Terminology preservation

Use `auto-lay` behavior only through the MCP server when it can preserve boundaries. Keep labels `executive-readable`, represent `multi-plane` enterprise views clearly, and never `re-color` official icons.

## Output template

```markdown
## Architecture diagram package - <system name>

**Status:** complete | draft | blocked
**Audience:** <executive | engineering | operations | mixed>
**Source files:**
- `output/<diagram>.drawio`
- `output/<diagram>.svg`

| View | Purpose | File | Validation |
| --- | --- | --- | --- |
| System context | <why included> | `output/<name>.drawio` | opens in draw.io; SVG exported |
| Component | <why included> | `output/<name>.drawio` | official icons verified |

### Assumptions
- <assumption or "none">

### Validation
- `scripts/validate_drawio.py output/<diagram>.drawio`: pass | fail
- Draw.io open check: pass | fail
- Official icon and no-recolor check: pass | fail
```

## Quality gate

- [ ] The diagram package includes editable `.drawio` source and exported SVG unless explicitly blocked.
- [ ] Every vendor product uses an official Azure, Microsoft, or GitHub icon where one exists.
- [ ] Official product icons are not recolored, distorted, or modified.
- [ ] Boundaries, regions, planes, and trust zones are labeled.
- [ ] Connectors are routed orthogonally, labeled, and avoid unnecessary crossings.
- [ ] The selected views match the user's audience and question.
- [ ] `scripts/validate_drawio.py` was run or a concrete blocker is reported.
- [ ] Bundled references used above exist and are read only when needed.

## References

- [Azure architecture icons](https://learn.microsoft.com/azure/architecture/icons/)
- [GitHub Octicons](https://primer.style/octicons/)

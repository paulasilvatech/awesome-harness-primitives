# Worked Example: Agentic Platform System Context

A complete, opening `.drawio` example for an AI-native system, to use as a starting point and as proof the format and the draw.io MCP server produce valid output.

The source is at [../assets/example-agentic.drawio](../assets/example-agentic.drawio). Open it in draw.io / diagrams.net or the VS Code Draw.io extension.

## What it shows

A system context diagram for an agentic platform on the GitHub platform and Azure AI Foundry, mapping the seven decisions from `agentic-architecture-patterns` to services:

- **Callers** (boundary): GitHub Copilot, GitHub Actions, and a developer.
- **Azure subscription** (boundary) with:
  - API Management as the AI gateway (token limit and semantic cache).
  - Agent runtime on Azure AI Foundry Agent Service.
  - Model router (mini to frontier).
  - Azure Managed Redis (semantic cache and memory).
  - Azure AI Search (RAG retrieval).
  - Azure API Center (tool and MCP registry) governing the MCP servers and tools.
  - Content Safety and Prompt Shields (guardrails).
  - Entra Agent ID and managed identity.
  - Application Insights with OpenTelemetry GenAI, and Foundry evaluation as a CI gate.

Edges are labeled with the relationship (HTTPS, token limit plus semantic cache, route, cache plus memory, retrieve, discover, govern, screen, authN, trace). Boundaries use the paulasilva-ms accent colors; the boxes are neutral placeholders.

## How it was built

This example uses neutral boxes colored by boundary so it opens in any viewer without an icon library. To make a client-ready version, replace each box with the official product icon:

- Use `add_node_svg` from the draw.io MCP server (see [drawio-mcp.md](drawio-mcp.md)) to embed the official Azure, Microsoft, or GitHub (Octicons) SVG inline, so the file stays self-contained.
- Or enable the draw.io Azure shape library and swap each box style for the matching Azure stencil.

Do not modify or re-color the official product icons; keep the color on the containers and connectors. See [icon-catalogs.md](icon-catalogs.md).

## Reproduce with the MCP server

The same diagram can be generated programmatically:

1. `create_diagram("output/agentic-context.drawio", "System Context")`
2. `add_container(... kind="subscription")` for the callers and the platform boundaries.
3. `add_node(...)` (or `add_node_svg(...)`) for each service, with `parent` set to its boundary.
4. `connect_nodes(...)` for each labeled relationship.
5. `export_hint(...)`, then export SVG from draw.io and embed it in the deliverable.

## Sources

- [draw.io file format](https://www.drawio.com/doc/faq/format-of-files)
- [Azure architecture icons](https://learn.microsoft.com/azure/architecture/icons/)
- [GitHub Octicons](https://primer.style/octicons/)

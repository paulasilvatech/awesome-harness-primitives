---
description: "Produce a complete architecture diagram with the official Azure, Microsoft, and GitHub (Octicons) icon sets, output as an editable draw.io (.drawio) file plus exported SVG. Uses the bundled draw.io MCP server or hand-authored mxGraph XML, with boundary grouping, orthogonal connectors, and the icon terms of use respected."
agent: agent
argument-hint: "what to diagram, for example an agentic platform on Foundry with Redis, APIM, and API Center"
---

# Diagram Architecture

Create an architecture diagram for `${input:target:what to diagram, for example an agentic platform on Foundry}` using official vendor icons.

## First step, always

Load `azure-architecture-diagrams` before deriving the diagram or editing any output. For an AI-native system, also load `agentic-architecture-patterns` to get the service map first. Apply the `paulasilva-ms` palette to containers, labels, and connectors, never to the vendor icons themselves.

## Steps

1. Take or derive the service map (services, boundaries, and relationships).
2. Choose the diagram types to produce. Default set: system context, component, deployment, and a sequence or data and control flow for the critical path.
3. Build the diagram with the bundled draw.io MCP server (preferred) or hand-authored mxGraph XML. Place an official icon for each service: Azure architecture icons for Azure services, Microsoft product icons for Microsoft products, GitHub Octicons or the GitHub logo for GitHub platform elements.
4. Group nodes by boundary (subscription, resource group, VNet, trust zone), route orthogonal connectors, and label edges with protocols.
5. Export SVG (embed images for a self-contained file) and keep the `.drawio` source under `output/`.
6. Verify the diagram opens and every icon resolves.

## Rules

- Use only official icon sets and respect their terms: do not modify, distort, or re-color product icons; keep clear space around the GitHub mark.
- Label every icon with the exact service name. One icon set per product family, no look-alike third-party icons.
- Write "GitHub Copilot", never "Copilot" alone. No em dashes.

## Done when

- The `.drawio` source and an exported SVG exist under `output/`.
- Every node uses an official icon and is labeled with the exact service name.
- Boundaries are grouped and connectors are clean, and the diagram opens without missing icons.

## Output

Output concisely: return only the `.drawio` and SVG artifact path(s), validation status, and any critical findings or blockers. Do not narrate the process steps.

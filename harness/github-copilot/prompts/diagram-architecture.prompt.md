---
name: 'diagram-architecture'
description: 'Produce an editable draw.io architecture diagram and exported SVG using official Azure, Microsoft, and GitHub icons.'
agent: 'agent'
argument-hint: 'what to diagram, for example an agentic platform on Foundry with Redis, APIM, and API Center'
---

# /diagram-architecture

## Objective

Create an editable draw.io architecture diagram and exported SVG for the requested system using official Azure, Microsoft, and GitHub icon sets, grouped boundaries, clean connectors, and the `paulasilva-ms` palette applied only to containers, labels, and connectors.

## When to Invoke

Use this prompt when a user asks for an architecture diagram, draw.io source, exported SVG, system context, component, deployment, sequence, data flow, or control-flow view for a technical system.

## Preconditions

- The target system or diagram subject is provided through `${input:target:what to diagram, for example an agentic platform on Foundry}` or the prompt argument.
- The `azure-architecture-diagrams` skill is available.
- For an AI-native system, `agentic-architecture-patterns` is available.
- Output under `output/` is permitted.

## Inputs the Team Must Provide

- `target` — what to diagram, for example an agentic platform on Foundry.
- Known services, boundaries, relationships, protocols, trust zones, and critical paths.
- Required diagram types if the default set is not sufficient.
- Ask the user for anything missing that prevents accurate service mapping or icon selection.

## What I Will Do

- Load `azure-architecture-diagrams` before deriving the diagram or editing output.
- Load `agentic-architecture-patterns` first for AI-native systems to get the service map.
- Apply the `paulasilva-ms` palette to containers, labels, and connectors, never to vendor icons.
- Produce default diagram types: system context, component, deployment, and a sequence or data and control flow for the critical path.
- Use official Azure architecture icons, Microsoft product icons, and GitHub Octicons or the GitHub logo as appropriate.
- Save `.drawio` sources under `output/`, export self-contained SVG with embedded images, and verify the diagram opens with every icon resolved.

## What I Will NOT Do

- Modify, distort, recolor, or crowd official product icons.
- Use look-alike third-party icons or mix product families incorrectly.
- Label a node with an imprecise service name or write “Copilot” without “GitHub Copilot”.
- Put generated artifacts outside `output/` unless explicitly requested.
- Narrate process details in the final response when artifact paths and validation status are sufficient.

## Output Format

Return only the concise artifact report:

```markdown
### Diagram Architecture Result

### Artifacts
- Draw.io source: `output/<diagram-name>.drawio`
- SVG export: `output/<diagram-name>.svg`

### Diagram Types
- System context
- Component
- Deployment
- Sequence or data and control flow for the critical path

### Validation Status
- `azure-architecture-diagrams` loaded: `<passed|failed>`
- `agentic-architecture-patterns` loaded for AI-native system: `<passed|failed|not applicable>`
- Official icons used and labeled with exact service names: `<passed|failed>`
- Boundaries grouped by subscription, resource group, VNet, or trust zone: `<passed|failed>`
- Orthogonal connectors routed and labeled with protocols: `<passed|failed>`
- SVG embeds images and `.drawio` opens without missing icons: `<passed|failed>`

### Critical Findings or Blockers
- `<finding or none>`
```

## Definition of Done

- [ ] The `.drawio` source and exported SVG exist under `output/`.
- [ ] Every node uses an official icon and is labeled with the exact service name.
- [ ] Containers, labels, and connectors use the `paulasilva-ms` palette; vendor icons are not modified.
- [ ] Boundaries are grouped and connectors are clean, orthogonal, and protocol-labeled.
- [ ] The diagram opens and every icon resolves.
- [ ] Final response lists only artifact paths, validation status, and critical findings or blockers.

## Prompt Body

Follow these steps in order. Do not derive or edit diagram output before loading the required diagram skill.

**Step 1 — Load required skills.** Load `azure-architecture-diagrams` before deriving the diagram or editing any output. For an AI-native system, also load `agentic-architecture-patterns` to get the service map first. Apply the `paulasilva-ms` palette to containers, labels, and connectors, never to vendor icons themselves.

**Step 2 — Build or confirm the service map.** Take or derive services, boundaries, and relationships from the user input and inspected context. Ask only for missing information that prevents correct service mapping.

**Step 3 — Choose diagram views.** Produce the default set unless the user asks otherwise: system context, component, deployment, and a sequence or data and control flow for the critical path.

**Step 4 — Build the draw.io diagram.** Use the bundled draw.io MCP server when available, or hand-authored mxGraph XML otherwise. Place an official icon for each service: Azure architecture icons for Azure services, Microsoft product icons for Microsoft products, and GitHub Octicons or the GitHub logo for GitHub platform elements.

**Step 5 — Apply layout and branding rules.** Group nodes by boundary such as subscription, resource group, VNet, or trust zone. Route orthogonal connectors and label edges with protocols. Use only official icon sets and respect their terms. Do not modify, distort, or re-color product icons. Keep clear space around the GitHub mark. Label every icon with the exact service name. Use one icon set per product family and no look-alike third-party icons. Write “GitHub Copilot”, never “Copilot” alone. Do not use em dashes.

**Step 6 — Export and verify.** Export SVG with embedded images for a self-contained file and keep the `.drawio` source under `output/`. Verify that the diagram opens and every icon resolves.

**Step 7 — Report concisely.** Return only the `.drawio` and SVG artifact paths, validation status, and critical findings or blockers.

## Invocation Example

```
/diagram-architecture target="agentic platform on Foundry with Redis, APIM, and API Center"
```

---
name: azure-architecture-diagrams
description: "Use when creating professional Azure, Microsoft, or GitHub architecture diagrams as editable draw.io files and exported SVG; produces diagram source, exports, validation results, and embedding guidance. DO NOT USE FOR: validating Mermaid architecture documents (use architecture-doc), writing Markdown documents or PPTX conversions (use markdown-writer), or hand-crafted non-icon SVG infographics (use svg-professional). Triggers include \"create an Azure architecture diagram\", \"make a draw.io deployment diagram\", \"export an architecture SVG\"."
---

# Azure Architecture Diagrams

This workflow creates official-icon architecture diagrams for Open Horizons, delivered as `.drawio` source plus SVG export guidance. It uses the bundled draw.io MCP server and validation script when programmatic diagram creation is appropriate.

> [!NOTE]
> This skill may shell out to bundled Python scripts in `scripts/` and may use a draw.io MCP server. Resolve bundled paths relative to this `SKILL.md`. Official Azure, Microsoft, and GitHub icon terms must be respected; do not recolor or modify official product icons.

## When to invoke
- "Create an Azure architecture diagram for the Open Horizons deployment."
- "Make a draw.io component diagram with official Microsoft and GitHub icons."
- "Export a deployment diagram as SVG and keep the source editable."
- "Show the system context for the Foundry, Redis, Backstage, and AKS design."

## Prerequisites and context
- A verified service map or architecture scope.
- Output location agreed with the user before creating files.
- Reference files available in `references/`.
- Scripts available at `scripts/drawio_mcp_server.py` and `scripts/validate_drawio.py`.
- Official icon sources confirmed through `references/icon-catalogs.md`.

## Procedure

### Step 1: Confirm diagram scope and output files
```text
Diagram request summary:
- Diagram type: system context | component | deployment | sequence | data flow
- Source evidence:
- Output .drawio path:
- Output SVG path:
Proceed with creating or updating diagram artifacts? (y/n)
```

> [!IMPORTANT]
> Only create or overwrite `.drawio` or SVG artifacts if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the diagram plan and stop.

### Step 2: Load diagram references
- Read `references/icon-catalogs.md` for official icon usage.
- Read `references/drawio-format.md` for mxGraph structure.
- Read `references/drawio-mcp.md` for MCP tool flow.
- Read `references/first-run-checklist.md` before delivery.

### Step 3: Choose the diagram set
- [ ] System context: actors, Backstage, GitHub, Azure boundary, and platform boundary.
- [ ] Component: AKS, Backstage, agent APIs, Foundry gateway, Redis, AI Search, observability, and tools/MCP.
- [ ] Deployment: subscriptions, resource groups, VNets, private endpoints, AKS namespaces, and regions.
- [ ] Sequence or data flow: one critical path, cache hit and miss, tool invocation, telemetry, and guardrails.

### Step 4: Build with the MCP server or hand-authored mxGraph
Run the MCP server only when the host can connect to it:

```bash
scripts/run-drawio-mcp.sh
```

For manual validation of a `.drawio` file:

```bash
python scripts/validate_drawio.py <diagram.drawio> --require-icon --require-edge
```

### Step 5: Validate and prepare delivery
- [ ] Official icon references are used only for the products they represent.
- [ ] Boundaries are labeled by subscription, resource group, VNet, namespace, or trust zone.
- [ ] Connectors are orthogonal and labeled with protocols or data/control meaning.
- [ ] The `.drawio` source opens in diagrams.net or the VS Code draw.io extension.
- [ ] SVG export is created from the same source and can be embedded in Markdown.

## Risk classification
| Severity | Meaning |
|---|---|
| High | Diagram misrepresents trust boundaries, data flow, identity, or public/private exposure. |
| Medium | Icons, grouping, or connector labels can confuse implementation or review decisions. |
| Low | Layout readability, naming, or export quality issues. |

## Limits

- Do not use this skill for: validating Mermaid architecture documents (use architecture-doc), writing Markdown documents or PPTX conversions (use markdown-writer), or hand-crafted non-icon SVG infographics (use svg-professional).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| MCP server cannot start | Fall back to hand-authored `.drawio` using `references/drawio-format.md`. |
| Icon style is unavailable | Use embedded official SVG if permitted, or label the node without an icon. |
| Validator fails | Fix malformed XML, missing vertices, missing edges, or missing official icon evidence. |
| Output path is unclear | Ask for the target path and do not create files until confirmed. |

## Output template

Return exactly this structure:
~~~markdown
# Architecture Diagram Delivery

## Files
- Source: `path/to/diagram.drawio`
- Export: `path/to/diagram.svg`

## Diagram Scope
- Type:
- Boundaries:
- Main flow:

## Validation
| Check | Result |
|---|---|

## Embedding
```markdown
![Architecture diagram](path/to/diagram.svg)
```
~~~

## Quality gate
- [ ] `.drawio` source and SVG export are both produced or clearly planned.
- [ ] Official icon usage follows repository references.
- [ ] Validation script passes for the `.drawio` source.
- [ ] Boundaries, connectors, labels, and trust zones are readable.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.

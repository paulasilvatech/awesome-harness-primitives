# Diagram Showcase and Selection Guide

Use this guide to choose the right draw.io diagram format for the architectural question. Do not force every system into the enterprise registry plane layout. The `paulasilva-ms` design system provides the visual language; this skill chooses the diagram shape, canvas, icon treatment, and validation path.

## Showcase assets

| Example | File | Best for | Canvas |
| --- | --- | --- | --- |
| System context | `assets/showcase-diagrams.drawio`, page 01 | Explaining actors, boundaries, and external dependencies to a mixed audience. | 16:9 landscape |
| Component map | `assets/showcase-diagrams.drawio`, page 02 | Showing runtime responsibilities and service interactions without deployment noise. | 16:9 landscape |
| Deployment topology | `assets/showcase-diagrams.drawio`, page 03 | Showing subscription, resource group, VNet, private endpoints, and managed identity posture. | 16:9 landscape |
| Critical path flow | `assets/showcase-diagrams.drawio`, page 04 | Explaining one request or one agent run end to end, with control points. | 16:9 landscape |
| Routing decision | `assets/showcase-diagrams.drawio`, page 05 | Explaining model routing, approvals, fallback, or cost and risk decisions. | Portrait |
| Enterprise registry planes | `assets/showcase-diagrams.drawio`, page 06 | Executive plus technical reviews where network, policy, registry, use plane, and governance must fit together. | Wide landscape |
| Production baseline | `output/contoso-mcp-registry-production-baseline.drawio` | Deep-dive MCP registry architecture with numbered flows and dense implementation notes. | Wide landscape |

## Selection rules

- Use **system context** when the audience asks who uses the system, where the boundary is, or which systems are external.
- Use **component map** when the audience asks how runtime pieces collaborate.
- Use **deployment topology** when the audience asks where services run, how private access works, or how identity crosses boundaries.
- Use **critical path flow** when the audience asks what happens first, second, third in one user or agent interaction.
- Use **routing decision** when the audience asks why the architecture chooses one path, model, approval, or fallback over another.
- Use **enterprise registry planes** only when the architecture genuinely spans multiple planes. It is powerful, but too dense for simple systems.

## Visual contracts

- Apply the `paulasilva-ms` palette to containers, stripes, connectors, headings, and boundary accents.
- Do not recolor official Azure, Microsoft, or GitHub product icons. Color the surrounding container instead.
- Keep labels executive-readable first, with implementation detail in the second line.
- Use numbered markers only when sequence matters.
- Prefer multiple focused diagrams over one everything diagram.

## Build and validate

```bash
python3 .github/skills/azure-architecture-diagrams/scripts/build_showcase_drawio.py
python3 .github/skills/azure-architecture-diagrams/scripts/validate_drawio.py \
  .github/skills/azure-architecture-diagrams/assets/showcase-diagrams.drawio \
  --require-icon --require-edge
```

Optional SVG export, when draw.io desktop CLI is available:

```bash
drawio --export --format svg --embed-images \
  --output .github/skills/azure-architecture-diagrams/assets/showcase-diagrams.svg \
  .github/skills/azure-architecture-diagrams/assets/showcase-diagrams.drawio
```

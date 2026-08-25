# Professional diagram quality standard

This standard follows the Microsoft Azure Well-Architected Framework guidance for architecture design diagrams and applies it to editable draw.io artifacts.

Verification date: 2026-08-25. Primary source: [Create architecture design diagrams](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-diagrams).

## Intent and lifecycle

- Name the audience and the question each view answers.
- Choose the diagram type and abstraction level for that question.
- Maintain multiple focused views across envisioning, design, threat modeling, implementation, operations, and governance when one view would be overloaded.
- Retire or update diagrams that no longer describe the implemented or planned system accurately.
- Link diagrams to governing requirements, decisions, risks, or source evidence.

## Required metadata

Every delivered diagram or companion document records:

| Field | Purpose |
| --- | --- |
| Title and subtitle | Identify the system and question answered |
| Purpose | Explain why the view exists |
| Audience | Define the intended reader |
| Scope and exclusions | Prevent false assumptions |
| Owner | Identify the maintainer |
| Version and updated date | Show freshness |
| Status | Draft, ready for review, approved, implemented, or retired |
| Sources | Link evidence, requirements, decisions, and official icon pages |
| Legend | Explain non-obvious notation |

Do not claim approval or implementation without evidence.

## Layout

- Use one primary left-to-right or top-to-bottom flow axis.
- Place supporting flows around the primary path rather than crossing it.
- Use alignment, equal spacing, and consistent dimensions for peer nodes.
- Preserve whitespace around boundaries, labels, and official marks.
- Keep hierarchy visible through containers and nesting, not arbitrary size changes.
- Use separate pages or views for context, components, deployment, trust boundaries, sequence, data flow, or operations when combining them reduces clarity.

## Notation and connectors

- Use standard notation consistently.
- Use directional single-ended arrows. Prefer two annotated flows over one bidirectional arrow when requests and responses must be distinguished.
- Use orthogonal routing for architecture and process flows unless another notation requires otherwise.
- Label relationships when protocol, data, control intent, trust transition, or direction is not obvious.
- Avoid crossings; use waypoints, ports, or another view rather than ambiguous lines.
- Include a legend for line color, dash patterns, arrowheads, numbered callouts, or boundary styles.

## Accuracy

- Depict only components and relationships supported by evidence or marked assumptions.
- Represent managed-service network placement accurately. For example, do not draw a platform service inside a subnet when access actually occurs through a private endpoint.
- Distinguish logical ownership from physical deployment and network reachability.
- Identify regions, subscriptions, resource groups, virtual networks, trust zones, external systems, and shared services only when relevant and evidenced.
- Use exact current product and service names.
- Do not use a vendor icon to suggest a deployment or integration that has not been established.

## Visual system

- Keep official product artwork unchanged.
- Apply semantic colors to containers, connectors, annotations, and generic shapes.
- Use consistent icon dimensions for peers and preserve every icon's aspect ratio.
- Use concise labels and place explanatory prose in callouts or companion documentation.
- Keep titles, section labels, node labels, edge labels, and annotations typographically distinct and consistent.
- Avoid decorative effects, gradients, shadows, and excessive color unless the selected notation requires them.

## Accessibility

- Pair icons with text labels.
- Pair colors with labels, patterns, line styles, or symbols.
- Maintain readable contrast for text, connectors, and boundaries in the intended light or dark background.
- Verify reading order and meaning at normal publication size and at reduced zoom.
- Do not encode status or risk solely through red, green, or another color.
- Provide a textual summary or component inventory for readers who cannot consume the visual.

## Review passes

1. **Semantic pass**: products, boundaries, direction, labels, and relationships match evidence.
2. **Brand pass**: official assets, usage rights, current names, proportions, colors, and provenance pass.
3. **Structural pass**: mxGraph roots, IDs, parents, geometry, edges, and embedded assets validate.
4. **Accessibility pass**: labels, contrast, redundant semantics, legend, and textual summary pass.
5. **Visual pass**: alignment, spacing, crossings, density, hierarchy, and export fidelity pass.
6. **Lifecycle pass**: owner, version, date, status, sources, and change context are present.

XML validation cannot replace semantic, brand, accessibility, or visual review.

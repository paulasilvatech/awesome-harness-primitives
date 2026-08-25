---
name: azure-draw-io-diagram-generator
description: >-
  Creates and validates editable draw.io mxGraph diagrams for architecture, flow, sequence, ER, UML, and network views. Use when generating or updating .drawio files with deterministic layout, valid cells, reusable styles, and optional SVG export.
---

# Azure Draw.io Diagram Generator

Generate valid, editable mxGraph XML after planning the diagram structure and layout.

## When to invoke

- Create an architecture, flowchart, sequence, ER, UML, or network diagram.
- Update an existing `.drawio` file without flattening it to an image.
- Validate mxGraph cell structure, IDs, geometry, and edge references.
- Export a reviewed diagram to SVG.

## Prerequisites and context

Confirm diagram type, audience, entities, relationships, grouping boundaries, labels, output path,
and whether a repository template should be used. Plan the layout before writing XML.

## Procedure

1. Inventory nodes, groups, relationships, cardinality/direction, legends, and required pages.
2. Select an existing template or start with required root cells `0` and `1` in that order.
3. Assign globally unique IDs and plan stable rows, tiers, lanes, spacing, and dimensions.
4. Create vertices with `vertex="1"`, a valid parent, style, and `<mxGeometry>` containing position
   and size.
5. Create edges with `edge="1"`, valid source and target, and relative geometry. Sequence lifelines
   may use explicit source/target points instead.
6. Use `html=1` only with XML-escaped label content. Keep labels concise and inspect long text.
7. Save the `.drawio`, run the validator, open it in draw.io/VS Code, and verify readability.
8. Export SVG only after the editable source passes validation.

## Criteria

| Element | Required invariant |
| --- | --- |
| Root | Cell IDs `0` and `1` exist first |
| Identity | Every cell ID is globally unique |
| Parent | Every parent references an existing cell |
| Vertex | Geometry has `x`, `y`, `width`, and `height` |
| Edge | Source and target exist, except point-based sequence lifelines |
| HTML label | Style contains `html=1` and XML characters are escaped |

Semantic palette:

| Meaning | Fill | Stroke |
| --- | --- | --- |
| Information | `#dae8fc` | `#6c8ebf` |
| Success | `#d5e8d4` | `#82b366` |
| Warning | `#fff2cc` | `#d6b656` |
| Error | `#f8cecc` | `#b85450` |

Validation:

```bash
python .github/skills/draw-io-diagram-generator/scripts/validate-drawio.py <file.drawio>
```

## Output template

```markdown
## draw.io diagram result

**Status:** CREATED | UPDATED | BLOCKED
**Source:** `<path.drawio>`
**Export:** `<path.svg or not requested>`

### Diagram
- Type/pages: <type and count>
- Nodes/edges/groups: <counts>
- Layout: <tiers, lanes, or grouping>

### Validation
- XML/cell validation: <pass/fail>
- Visual inspection: <pass/fail/not run>
```

## Limits

- Do not replace editable source with only SVG or PNG.
- Do not generate XML before planning layout and IDs.
- Do not use external image URLs when a self-contained artifact is required.
- Do not claim visual quality from XML validation alone.

## Progressive disclosure and bundled resources

- [mxGraph schema](references/drawio-xml-schema.md): detailed cell and geometry structure.
- [Style reference](references/style-reference.md): reusable style strings and palettes.
- [Shape libraries](references/shape-libraries.md): available shape namespaces.
- `assets/templates/`: architecture, flowchart, sequence, ER, and UML starter diagrams.
- `scripts/add-shape.py`: deterministic shape insertion helper.
- `scripts/validate-drawio.py`: structural validator.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-architecture-diagrams` | `skill` | Official Azure, Microsoft, or GitHub service icons are required. |
| `architecture-doc` | `skill` | The diagram belongs to an Open Horizons architecture document. |

## Quality gate

- [ ] IDs `0` and `1` exist first and all IDs are unique.
- [ ] Parent, vertex geometry, and edge references are valid.
- [ ] HTML labels are escaped.
- [ ] Structural validation passes.
- [ ] Editable source was visually inspected before export.
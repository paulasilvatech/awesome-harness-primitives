---
applyTo: "**/*.drawio,**/*.drawio.svg,**/*.drawio.png"
description: "Enforces draw.io and mxGraph XML conventions for diagram structure, styles, layout, naming, validation, and rendering."
---

# draw.io Diagram Conventions — mxGraph XML Quality

These instructions apply to `.drawio`, `.drawio.svg`, and `.drawio.png` files containing draw.io mxGraph XML. They are authoritative for XML structure, semantic palette, diagram-type patterns, layout, naming, validation, and renderability; the `draw-io` skill owns detailed workflow recipes, troubleshooting, and helper scripts when a full diagram-generation task is required.

## Diagram Planning and Type Selection

Identify the diagram type before writing XML: flowchart, architecture, sequence, ER, UML, network, or BPMN. Plan tiers, actors, entities, pages, containers, and connector direction before generating cells. Use an appropriate template or minimal skeleton from the `draw-io` skill when one exists, but keep the final XML self-contained and valid after installation.

## mxGraph XML Structure

Every generated file uses an `mxfile` with one or more `diagram` elements. Set `modified` to the current ISO 8601 timestamp when generating a new file and keep a current draw.io version such as `26.0.0` when produced by the editor.

```xml
<mxfile host="Electron" modified="" version="26.0.0">
  <diagram id="unique-id" name="Page Name">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

`<mxCell id="0" />` and `<mxCell id="1" parent="0" />` must be the first two cells. Every cell `id` is unique within the diagram. Every vertex with `vertex="1"` has `<mxGeometry x="..." y="..." width="..." height="..." as="geometry" />`. Every edge with `edge="1"` has `source` and `target` pointing to existing vertex ids; floating sequence lifeline edges instead use `<mxPoint as="sourcePoint">` and `<mxPoint as="targetPoint">` inside `<mxGeometry>`. Every cell except id `0` has a valid `parent`. Children of swimlane containers use coordinates relative to the parent, not the canvas. Escape bare `&`, `<`, and `>` in attribute values.

## Style and Semantic Palette

Use `whiteSpace=wrap;html=1;` on vertex shapes. Use `html=1` when labels contain HTML tags such as `<b>`, `<i>`, or `<br>`. Use `edgeStyle=orthogonalEdgeStyle;html=1;` for standard connectors.

| Role | fillColor | strokeColor |
|---|---|---|
| Primary / Info (default) | `#dae8fc` | `#6c8ebf` |
| Success / Start / Positive | `#d5e8d4` | `#82b366` |
| Warning / Decision | `#fff2cc` | `#d6b656` |
| Error / End / Danger | `#f8cecc` | `#b85450` |
| Neutral / Interface | `#f5f5f5` | `#666666` |
| External / Partner | `#e1d5e7` | `#9673a6` |

## Diagram-Type Patterns

| Type | Container | Key shapes | Connector style |
|---|---|---|---|
| Flowchart | None | `ellipse` start/end, `rounded=1` process, `rhombus` decision | `orthogonalEdgeStyle` |
| Architecture | `swimlane` per tier | `rounded=1` services, cloud and DB shapes | `orthogonalEdgeStyle` with labels |
| Sequence | None | `mxgraph.uml.actor`, dashed lifeline edges | `endArrow=block` sync, `endArrow=open;dashed=1` return |
| ER Diagram | `shape=table;childLayout=tableLayout` | `shape=tableRow`, `shape=partialRectangle` | `entityRelationEdgeStyle;endArrow=ERmany;startArrow=ERone` |
| UML Class | `swimlane` per class | text rows for attributes and methods | `endArrow=block;endFill=0` inherit, `dashed=1` realize |

## Layout, Files, and Validation

Align coordinates to a 10 px grid. Keep 40–60 px gaps between same-row shapes and 80–120 px gaps between tier rows. Use standard sizes of `120 × 60` px for process shapes and `200 × 100` px for decision diamonds. Default canvas is A4 landscape `1169 × 827` px. Keep pages under 40 cells; split larger diagrams into multiple pages. Add a title text cell to every page with `style="text;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;align=center;"`.

Use `.drawio` for version-controlled diagrams and `.drawio.svg` for diagrams embedded in Markdown. Name files in kebab-case, such as `order-flow.drawio` and `database-schema.drawio`. Store diagrams under `docs/` or `architecture/` near the code they explain. Use one `<diagram>` element per logical view within a multi-page `<mxfile>`.

Validate with the draw.io validator provided by the `draw-io` skill and confirm rendering in VS Code with the draw.io extension `hediet.vscode-drawio`.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `.github/skills/draw-io/SKILL.md` `.github/skills/draw-io/references/drawio-xml-schema.md` `.github/skills/draw-io/references/shape-libraries.md` `.github/skills/draw-io/references/style-reference.md` `.github/skills/draw-io/scripts/add-shape.py` `.github/skills/draw-io/scripts/validate-drawio.py` `.github/skills/draw-io/templates/` `<mxGeometry x y width height as="geometry">` `REQUIRED` `SKILL` `add-shape` `attributes/methods` `cloud/DB` `drawio-xml-schema` `edge="1"` `github/skills/draw-io/SKILL.md` `github/skills/draw-io/references/drawio-xml-schema.md` `github/skills/draw-io/references/shape-libraries.md` `github/skills/draw-io/references/style-reference.md` `github/skills/draw-io/scripts/add-shape.py` `github/skills/draw-io/scripts/validate-drawio.py` `github/skills/draw-io/templates/` `shape-libraries` `style-reference` `to-use` `validate-drawio`.

## Good / Bad Examples

The examples below show required root cell ordering.

**Good:**

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <mxCell id="start" value="Start" vertex="1" parent="1">
    <mxGeometry x="40" y="40" width="120" height="60" as="geometry" />
  </mxCell>
</root>
```

Why: Root cells are first, the vertex has geometry, and coordinates align to the grid.

**Bad:**

```xml
<root>
  <mxCell id="start" value="Start" vertex="1" parent="1" />
  <mxCell id="1" parent="0" />
</root>
```

Why: The required root cells are missing or out of order and the vertex has no geometry.

## Conventions

| Rule | Rationale |
|---|---|
| Keep `id="0"` and `id="1"` as the first two cells | draw.io expects the root hierarchy in that order |
| Give every vertex geometry and every edge resolvable endpoints or points | Diagrams cannot render or route correctly without geometry and references |
| Use the semantic color palette consistently | Colors communicate meaning across diagrams |
| Align to the 10 px grid and keep standard gaps | Layout remains readable and easy to edit |
| Keep pages under 40 cells and split complex diagrams | Large pages become unreadable and hard to maintain |
| Use kebab-case diagram filenames near related docs or architecture | Files remain discoverable and portable |
| Validate XML and render in the editor before review | Structural validity does not guarantee visual correctness |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `whiteSpace=wrap;html=1;` on vertex styles | Let long labels overflow shapes |
| Use `edgeStyle=orthogonalEdgeStyle;html=1;` for standard connectors | Mix connector styles without semantic reason |
| Use swimlane-relative coordinates for children | Position container children using canvas coordinates |
| Use `mxPoint` source/target points for floating sequence lifelines | Add broken `source` or `target` ids to floating edges |
| Use `.drawio.svg` for Markdown embeds | Embed editor-only `.drawio` files directly in Markdown |
| Escape XML attribute special characters | Leave bare `&`, `<`, or `>` in labels |

## Checklist Before Opening a PR

- [ ] `<mxCell id="0" />` and `<mxCell id="1" parent="0" />` are the first two cells.
- [ ] Cell ids are unique and every non-root cell has a valid `parent`.
- [ ] Edge `source` and `target` ids resolve, or floating sequence edges use `mxPoint` geometry.
- [ ] Every vertex has `<mxGeometry as="geometry">`.
- [ ] XML is well-formed with escaped special characters.
- [ ] Palette, shape styles, connector styles, 10 px grid, gaps, page size, title cell, and cell count limits are satisfied.
- [ ] The diagram validates and renders in `hediet.vscode-drawio`.

---
description: "Use when creating, editing, or reviewing draw.io diagrams and mxGraph XML in .drawio, .drawio.svg, or .drawio.png files."
applyTo: "**/*.drawio,**/*.drawio.svg,**/*.drawio.png"
---

# draw.io Diagrams — Conventions and Constraints

This file activates when you open or edit a `.drawio`, `.drawio.svg`, or `.drawio.png` file. It defines the structural, style, and naming constraints every diagram in this repo must satisfy so that files render on the first try in VS Code with the `hediet.vscode-drawio` extension and stay consistent across the kit. It teaches you the invariants a diagram file must hold — it does not walk you through building one. The authoring procedure, per-type XML recipes, templates, and the validation script live in the [`draw-io-diagram-generator` skill](../skills/draw-io-diagram-generator/SKILL.md); read that before generating or restructuring a diagram, and do not duplicate its steps here.

## Structure Invariants

These invariants are non-negotiable; a diagram that breaks any of them renders blank or corrupt.

- `id="0"` and `id="1"` are the **first two cells** of every `<diagram>`, in that order, and are never reused for content.
- Every cell `id` is **unique within its diagram** page (ids may repeat across separate pages).
- Every vertex (`vertex="1"`) has a child `<mxGeometry ... as="geometry">` carrying `x`, `y`, `width`, and `height`.
- Every edge (`edge="1"`) either points `source`/`target` at existing vertex ids, **or** — for floating edges such as sequence-diagram lifelines — carries `<mxPoint as="sourcePoint">` and `<mxPoint as="targetPoint">` inside its `<mxGeometry>`.
- Every cell except `id="0"` has a `parent` that resolves to an existing id.
- Children of a container (swimlane, table) use coordinates **relative to the parent**, not the canvas.

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <!-- every other cell sets parent to an existing id -->
</root>
```

> [!WARNING]
> A file that opens blank in VS Code is almost always missing the `id="0"`/`id="1"` root cells or has an edge whose `source`/`target` id does not resolve. Check those two invariants first.

## Semantic Color Palette

Use one palette across the whole repo so a shape's color always means the same thing. `fillColor` pairs with its matching `strokeColor`.

| Role | fillColor | strokeColor |
|---|---|---|
| Primary / Info (default) | `#dae8fc` | `#6c8ebf` |
| Success / Start / Positive | `#d5e8d4` | `#82b366` |
| Warning / Decision | `#fff2cc` | `#d6b656` |
| Error / End / Danger | `#f8cecc` | `#b85450` |
| Neutral / Interface | `#f5f5f5` | `#666666` |
| External / Partner | `#e1d5e7` | `#9673a6` |

## File, Naming, and Layout Conventions

| Concern | Convention |
|---|---|
| Extension | `.drawio` for version-controlled diagrams; `.drawio.svg` when the file is embedded in Markdown |
| File name | `kebab-case`, e.g. `payment-flow.drawio`, `database-schema.drawio` |
| Location | Alongside the code the diagram documents, under `docs/` or `architecture/` |
| Grid | Align every coordinate to the 10 px grid (values divisible by 10) |
| Spacing | 40–60 px between same-row shapes; 80–120 px between tier rows |
| Page size | Default A4 landscape `1169 × 827` px |
| Density | 40 cells per page maximum; split larger systems into multiple `<diagram>` pages |
| Title | Add a title text cell at the top of every page |

## Validation

Before committing, run the `validate-drawio.py` checker documented in the [`draw-io-diagram-generator` skill](../skills/draw-io-diagram-generator/SKILL.md), then open the file in VS Code to confirm it renders. The skill owns the exact invocation and troubleshooting table; this file owns the invariants the checker enforces.

## Conventions

| Rule | Rationale |
|---|---|
| `id="0"` and `id="1"` are the first two cells of every page | draw.io treats them as the reserved root; without them the file will not render |
| Every vertex style includes `whiteSpace=wrap;html=1` | Labels wrap and render HTML consistently instead of overflowing |
| Connectors use `edgeStyle=orthogonalEdgeStyle` | Clean right-angle routing keeps diagrams readable |
| The semantic color palette is used consistently | A color carries the same meaning in every diagram |
| Diagram file names are `kebab-case` and live beside the code | Diagrams are discoverable and diff-friendly in version control |
| Authoring steps and recipes stay in the skill, not here | One source of procedure avoids two copies drifting apart |

## Do / Do Not

| Do | Do not |
|---|---|
| Place `id="0"` and `id="1"` first, then content cells | Reuse `0` or `1` for a shape, or omit them |
| Point every edge at existing vertex ids or use floating points | Leave an edge `source`/`target` dangling |
| Reuse the semantic color palette | Invent ad-hoc colors per diagram |
| Link to the skill for the authoring workflow | Copy the skill's step-by-step recipes into this file |
| Keep child coordinates relative to their container | Use canvas coordinates for cells inside a swimlane |
| Split a busy diagram across pages | Cram more than 40 cells onto one page |

## Checklist Before Opening a PR

- [ ] `<mxCell id="0" />` and `<mxCell id="1" parent="0" />` are the first two cells of every page
- [ ] All cell ids are unique within their diagram and every `parent` resolves
- [ ] Every edge `source`/`target` resolves, or the edge uses `sourcePoint`/`targetPoint`
- [ ] Every vertex has an `<mxGeometry as="geometry">` and container children use relative coordinates
- [ ] The semantic color palette and `whiteSpace=wrap;html=1` vertex style are applied consistently
- [ ] The file is `kebab-case`, lives under `docs/` or `architecture/`, and has a title cell per page
- [ ] The `validate-drawio.py` checker from the skill passes and the file renders in VS Code

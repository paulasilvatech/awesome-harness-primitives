---
name: drawio
description: >-
  Generate draw.io diagrams as native .drawio files and export them to PNG, SVG, or PDF with embedded XML. Use when the user asks for draw.io diagrams, diagrams.net XML, mxGraphModel, editable diagram source, or exporting .drawio files for documents.
---

# Draw.io diagrams

Create native `.drawio` files in `mxGraphModel` format, apply consistent diagram styles, and export to PNG, SVG, or PDF with embedded XML so the result remains editable in draw.io / diagrams.net.

## When to invoke

- "Generate a draw.io diagram for this workflow."
- "Create an editable .drawio file and export PNG."
- "Write mxGraphModel XML for this architecture."
- "Export all .drawio files in this directory."
- "Make a PNG/SVG/PDF that can be reopened in draw.io."

## Prerequisites and context

- Use `.drawio` source as the canonical artifact.
- Use the bundled Node.js export script when exporting images.
- Install script dependencies once from the `scripts` folder when needed.
- Prefer embedded XML for exported `png`, `svg`, and `pdf` so exported files remain editable.

## Draw.io creation rules

| Step | Required action |
| --- | --- |
| Generate XML | Create valid draw.io XML in `mxGraphModel` format. |
| Save source | Write the XML to a `.drawio` file. |
| Export | Use the bundled exporter or draw.io CLI to create PNG/SVG/PDF. |
| Verify | Open or validate the source and confirm exported file exists. |

## Export script

The bundled `scripts/drawio-to-png.mjs` (`drawio-to-png.mjs`) has two rendering backends:

| Renderer | When used | Notes |
| --- | --- | --- |
| draw.io CLI | Automatically when draw.io desktop CLI is installed. | Pixel-perfect and fastest. |
| Official draw.io viewer in headless browser | Fallback when CLI is unavailable. | Pixel-perfect; needs Chromium/Edge through `puppeteer-core`. |
| `auto` | Default. | Try CLI first, then viewer. |

```bash
# Install dependencies once, from the scripts folder
cd skills/drawio/scripts && npm install

# Export a single diagram
node skills/drawio/scripts/drawio-to-png.mjs <input.drawio> [output.png]

# Export all .drawio files in a directory
node skills/drawio/scripts/drawio-to-png.mjs --dir <directory>

# Force a specific renderer
node skills/drawio/scripts/drawio-to-png.mjs --renderer=cli|viewer|auto <input.drawio>
```

## Supported export formats

| Format | Embed XML | Notes |
| --- | --- | --- |
| `png` | Yes | Viewable everywhere and editable in draw.io. |
| `svg` | Yes | Scalable and editable in draw.io. |
| `pdf` | Yes | Printable and editable in draw.io. |

## Style conventions

Use these mxGraph style strings for consistent professional diagrams.

```xml
<!-- Primary service (highlighted) -->
<mxCell style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;strokeWidth=2;arcSize=12;shadow=1;" />

<!-- External system -->
<mxCell style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" />

<!-- Success/processing stage -->
<mxCell style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" />

<!-- Warning/quality gate -->
<mxCell style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" />

<!-- Error/failure path -->
<mxCell style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" />

<!-- Data store (cylinder) -->
<mxCell style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" />

<!-- Arrow -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#6c8ebf;strokeWidth=2;" />
```

## CLI locations and command

Try `drawio` from `PATH` first, then common desktop locations.

| Platform | Candidate |
| --- | --- |
| Windows | `"C:\Program Files\draw.io\draw.io.exe"` |
| macOS | `/Applications/draw.io.app/Contents/MacOS/draw.io` |
| Linux | `drawio` from snap, apt, or flatpak |

```bash
drawio -x -f png -e -b 10 -o <output.png> <input.drawio>
```

Flags: `-x` exports, `-f` selects format, `-e` embeds diagram XML, `-b` sets border, and `-o` sets the output path.

## Procedure

1. Translate the requested diagram into nodes, groups, edges, labels, and layout direction.
2. Generate valid `mxGraphModel` XML and save it as `<name>.drawio`.
3. Choose styles from the style convention table and keep colors semantically consistent.
4. Export with `scripts/drawio-to-png.mjs` or the draw.io CLI.
5. Verify the source opens and the exported file exists.
6. Report source and export paths.

## Progressive disclosure and bundled resources

- `scripts/drawio-to-png.mjs`: Node.js exporter with CLI and headless viewer renderers.
- `scripts/package.json`: script dependencies including `puppeteer-core`.

## Package contents

The skill folder contains `SKILL.md`, `scripts/drawio-to-png.mjs`, and `scripts/package.json`. Use create/edit tooling to write diagram source. Install dependencies `one-time` for the exporter. Both renderers are `pixel-perfect`; Linux installs may come from `snap/apt/flatpak`.

## Output template

```markdown
## Draw.io diagram result

**Status:** complete | blocked | failed
**Source:** `<diagram>.drawio`
**Exports:** `<diagram>.png` | `<diagram>.svg` | `<diagram>.pdf`

### Diagram contents
| Element | Count | Notes |
| --- | --- | --- |
| Nodes | <count> | <main groups> |
| Edges | <count> | <routing/labels> |

### Validation
- `.drawio` source written: pass | fail
- Export command: `<command>`
- Exported file exists: pass | fail
- Embedded XML requested: pass | fail
```

## Quality gate

- [ ] The source artifact is a native `.drawio` file containing valid `mxGraphModel` XML.
- [ ] Exported PNG, SVG, or PDF uses embedded XML when the format supports it.
- [ ] The bundled exporter or draw.io CLI command was used when an export was requested.
- [ ] Styles are consistent with primary, external, success, warning, error, data store, and arrow conventions.
- [ ] The diagram opens in draw.io / diagrams.net or a concrete blocker is reported.
- [ ] Every generated output path is reported.

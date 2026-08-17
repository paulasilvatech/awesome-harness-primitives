# First-run checklist

Use this gate before delivering any architecture diagram generated with this skill. The `.drawio` source is the editable source of truth, and exported SVG is a derivative.

## Scope and sources

- [ ] The service map is explicit: services, actors, boundaries, and relationships are named before drawing.
- [ ] The diagram archetype was chosen from `references/diagram-showcase.md` based on the question being answered.
- [ ] Every product node uses the exact service name.
- [ ] Azure, Microsoft, and GitHub product icons come from official icon sets or an official embedded SVG.
- [ ] Official product icons are not recolored, stretched, distorted, or used to imply endorsement.
- [ ] Generic concepts use generic draw.io shapes only when no product icon applies.

## Layout and readability

- [ ] Diagram type is clear: system context, component, deployment, sequence, data/control flow, or topology.
- [ ] The canvas and layout fit the type: 16:9 for executive context, portrait for decision flows, wide landscape for enterprise plane views.
- [ ] Boundaries are grouped and labelled (subscription, resource group, VNet, trust zone, tenant, environment).
- [ ] Main flow reads left to right or top to bottom.
- [ ] Connectors are orthogonal where possible and labelled with protocol or intent.
- [ ] Labels are short enough to fit, and every icon has a text label.
- [ ] Containers use the paulasilva-ms palette, not recolored product icons.
- [ ] If this is an enterprise registry style diagram, compare composition against `assets/example-agentic.drawio` (planes, numbered flow markers, and top narrative title).

## File output

- [ ] `.drawio` source is saved under an `output/` folder for the current task or deliverable.
- [ ] SVG export is saved next to the source or in the requested deliverable folder.
- [ ] Exported SVG embeds images so it remains portable.
- [ ] The `.drawio` file opens in draw.io / diagrams.net without missing shapes or broken images.

## Validation

- [ ] Python scripts compile: `python3 -m py_compile scripts/*.py`.
- [ ] Showcase gallery rebuilds when edited: `python3 scripts/build_showcase_drawio.py`.
- [ ] Draw.io XML validates: `python3 scripts/validate_drawio.py <diagram.drawio> --require-icon --require-edge`.
- [ ] For MCP usage, dependencies are installed: `pip install -r scripts/requirements.txt`.
- [ ] MCP server starts or gives actionable install guidance if dependencies are missing.
- [ ] If using built-in draw.io stencil style strings, the output was opened once in the target viewer to confirm icons resolve.

## Delivery

- [ ] Deliver both `.drawio` and exported SVG when the user asks for a diagram deliverable.
- [ ] Mention any assumption, missing official icon, or viewer-specific stencil limitation.
- [ ] For Contoso-style anonymized outputs, keep a validated production copy under `output/` and confirm it passes `scripts/validate_drawio.py`.

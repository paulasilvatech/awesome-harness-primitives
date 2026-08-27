---
name: azure-draw-io-diagram-generator
description: >-
  Creates and validates professional, accessible, editable draw.io diagrams with official
  Microsoft, Azure, and GitHub product or service icons plus recorded provenance. Use when
  generating or updating architecture, deployment, network, flow, sequence, ER, UML,
  trust-boundary, or branded product diagrams as self-contained .drawio source with optional SVG
  export.
---

<!-- Generated from harness/github-copilot/skills/azure-draw-io-diagram-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Professional Draw.io Diagram Generator

Turn an evidenced system model into an accurate, self-contained, reviewable `.drawio` package. Use official vendor assets only for the products they represent, preserve their appearance, and keep neutral concepts vendor-neutral.

## When to invoke

- "Create an Azure architecture diagram with official service icons."
- "Generate an editable draw.io diagram for Microsoft and GitHub services."
- "Update this .drawio file and preserve official logos and provenance."
- "Create a professional deployment, network, flow, sequence, ER, or UML diagram with official vendor icons."
- "Validate this diagram for icon integrity, layout, accessibility, and mxGraph structure."

## Professional diagram contract

| Concern | Required result |
| --- | --- |
| Intent | Each view answers one named audience question at an appropriate abstraction level. |
| Accuracy | Products, boundaries, regions, networks, dependencies, and flow direction match source evidence. |
| Source | Editable `.drawio` remains authoritative; exports never replace it. |
| Icons | Named vendor products use current official assets where permitted; generic concepts use neutral shapes. |
| Provenance | Each official icon records provider, product, source, terms, retrieval date, usage basis, and SHA-256. |
| Brand integrity | Official marks are not recolored, cropped, flipped, rotated, stretched, redrawn, combined, or used to imply endorsement. |
| Accessibility | Every icon has a nearby text label; meaning never depends on icon or color alone. |
| Portability | Official SVGs are embedded as data URIs; external image URLs are not allowed. |
| Maintainability | Title, purpose, scope, audience, version, updated date, owner, legend, and external references are visible or documented. |

## Icon decision model

Read the [official icon and logo policy](references/official-icon-policy.md) whenever a diagram names Microsoft, Azure, or GitHub products.

1. Use a product-family architecture icon set with explicit diagram-use terms when one exists.
2. Use an official open-source icon set only for the concepts covered by its license.
3. Use a corporate or product logo only when the requested use is allowed by current brand guidance or explicit permission.
4. Use a neutral draw.io shape for users, generic systems, protocols, abstract capabilities, and unbranded components.
5. If no permitted official asset is available, use a labeled neutral shape and report the icon as blocked. Never use an unofficial look-alike.

Do not treat GitHub Octicons as GitHub product logos. Do not use a deprecated GitHub Copilot standalone mark. Do not use a Microsoft product icon to represent the user's product.

## Procedure

1. Establish the diagram brief.
   - Confirm audience, decision or question, lifecycle stage, scope, source evidence, output path, required formats, and review owner.
   - Choose the smallest useful view set. Use progressive disclosure rather than one overloaded canvas.

2. Build a semantic inventory before drawing.
   - List actors, vendor products, generic components, data stores, boundaries, regions, flows, protocols, trust transitions, and requirement or decision IDs.
   - For every vendor node, record its exact current product or service name and authoritative source.
   - Do not infer deployment inside a subnet, region, or trust boundary merely for visual convenience.

3. Select assets and usage rights.
   - Consult the provider-specific source registry in the [official icon and logo policy](references/official-icon-policy.md).
   - Obtain assets only from a first-party page or official first-party repository after satisfying its terms or permission gate.
   - Record retrieval date and usage basis. Recheck the source when evidence is older than 90 days, the provider changed branding, or the requested use differs from architecture, training, or documentation.
   - Never download from third-party icon aggregators, search-result image URLs, or unverified packages.

4. Plan the visual system.
   - Apply the [professional diagram standard](references/diagram-quality-standard.md).
   - Use one primary flow axis, stable spacing, consistent icon sizes, orthogonal directed connectors, concise labels, named boundaries, and a compact legend.
   - Use containers, connector colors, line patterns, and annotations for semantics; never recolor official icons.

5. Create the editable source.
   - Start from an appropriate file in `assets/templates/` or create valid root cells `0` and `1`.
   - Use `scripts/add-shape.py` for generic shapes.
   - Use `scripts/add-icon.py` for a local official SVG. Supply provider, exact product name, official source URL, terms URL, retrieval date, and usage basis.
   - Use version-specific draw.io vendor stencils only when the exact stencil and viewer version were visually verified. Embedded official SVG is the portable default.
   - Keep globally unique IDs, valid parents, explicit geometry, and valid source/target references.

6. Add diagram metadata and traceability.
   - Include title, purpose, audience, scope, owner, version, updated date, and source references.
   - Label every product icon with its exact service name.
   - Trace design elements to requirement, decision, risk, or source IDs when the diagram belongs to an SDD or architecture package.
   - Record non-obvious connector semantics in a legend.

7. Validate and review.
   - Run `scripts/validate-drawio.py <file.drawio>`.
   - For branded diagrams, also pass `--require-official-icons --require-icon-provenance`.
   - Open the source in draw.io or the VS Code draw.io editor. Inspect icon rendering, aspect ratio, labels, overlap, crossings, reading order, zoomed-out legibility, and light/dark export contrast.
   - Correct every structural, provenance, brand, accessibility, and accuracy defect before export.

8. Export only after source approval.
   - Export SVG with images embedded.
   - Compare the export with the editable source and verify that labels and icons remain legible.
   - Deliver the editable source, export, icon provenance summary, validation results, and any blocked assets.

## Validation criteria

### Structure

- Root cells `0` and `1` exist first on every page.
- IDs are unique; parents, geometry, and edge endpoints resolve.
- HTML labels are XML-escaped and external image URLs are absent.

### Official assets

- Every branded node maps to an official current product or service asset, or to a documented neutral fallback.
- Embedded official SVG nodes include complete provenance metadata and a matching SHA-256.
- Icon aspect ratio and original colors are preserved.
- GitHub logos, product lockups, and Octicons are used according to their distinct permissions.

### Professional quality

- The view, abstraction level, and density fit the audience question.
- Boundaries and directional flows are accurate, labeled, and visually consistent.
- A legend explains non-obvious colors, patterns, or line styles.
- Labels, not color or icon recognition alone, communicate meaning.
- Diagram metadata and source references support review and maintenance.

## Limits

- Do not use unofficial icon libraries when an official source exists.
- Do not bundle downloaded Microsoft or GitHub brand assets into this skill.
- Do not bypass license, terms-acceptance, or permission requirements.
- Do not modify official icon artwork or use product marks as decoration.
- Do not use an icon as proof that a product is deployed; architecture evidence controls diagram content.
- Do not generate external-image dependencies in a self-contained diagram.
- Do not claim visual quality or brand compliance from XML validation alone.

## Progressive disclosure and bundled resources

- [Official icon and logo policy](references/official-icon-policy.md): source hierarchy, provider terms, provenance schema, and brand restrictions.
- [Professional diagram standard](references/diagram-quality-standard.md): audience, layout, accuracy, accessibility, metadata, and review rules.
- [mxGraph schema](references/drawio-xml-schema.md): cells, geometry, embedded images, and diagram structure.
- [Style reference](references/style-reference.md): generic shapes, edges, containers, and semantic palettes.
- [Shape libraries](references/shape-libraries.md): built-in non-brand notation and library compatibility.
- `assets/templates/`: editable architecture, flowchart, sequence, ER, and UML baselines.
- `scripts/add-icon.py`: safely embeds a local official SVG and writes provenance metadata.
- `scripts/add-shape.py`: adds generic shapes.
- `scripts/validate-drawio.py`: validates structure, self-containment, and official-icon provenance.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `sdd-requirements-engineer` | `skill` | The diagram must trace to EARS requirements, design decisions, tasks, and verification. |

## Output template

```markdown
## Professional draw.io diagram result

**Status:** completed | ready-for-review | blocked
**Audience and question:** <audience; question answered>
**Editable source:** `<path.drawio>`
**Export:** `<path.svg or not requested>`

### Views and evidence
| View | Purpose | Source IDs | Nodes/edges/boundaries |
| --- | --- | --- | --- |
| <view> | <question answered> | <IDs> | <counts> |

### Official icon provenance
| Provider | Product or service | Source | Retrieved | SHA-256 | Usage basis |
| --- | --- | --- | --- | --- | --- |
| <provider> | <exact name> | <official URL> | <date> | <hash> | <basis> |

### Validation
- Structure and self-containment: <pass|fail>
- Official icon provenance: <pass|fail|not applicable>
- Brand and accessibility review: <pass|fail>
- Visual inspection and export comparison: <pass|fail|not run>
- Blocked or substituted assets: <none or details>
```

## Quality gate

- [ ] The diagram answers a named audience question with the smallest useful view set.
- [ ] Architecture content is sourced and semantically accurate.
- [ ] Every vendor product uses a permitted official asset or a documented neutral fallback.
- [ ] Every official icon preserves artwork and carries complete, hash-verified provenance.
- [ ] No third-party, deprecated, altered, externally linked, or misleading brand asset remains.
- [ ] Exact product labels, directed flows, boundaries, legend, and metadata are present.
- [ ] Accessibility does not depend on color or icon recognition alone.
- [ ] Structural and official-icon validation commands pass.
- [ ] Editable source was visually inspected before a matching embedded-image SVG export.
- [ ] The response follows `## Output template` exactly.

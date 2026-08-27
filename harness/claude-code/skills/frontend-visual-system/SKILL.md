---
name: frontend-visual-system
description: >-
  Define evidence-based typography, semantic color, layout, density, imagery, iconography, themes,
  and motion within an existing product system. Use this skill when frontend visual direction,
  design tokens, theming, composition, or visual-quality review is requested.
---

<!-- Generated from harness/github-copilot/skills/frontend-visual-system/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend visual system

Translate product evidence and an established design system into a concrete visual grammar without substituting trends for information hierarchy.

## When to invoke

- "Define the visual direction for this product screen."
- "Review our typography, color, spacing, and density."
- "Create semantic frontend tokens without replacing our design system."
- "Make this interface less generic while preserving the brand."
- "Audit motion, themes, icons, and visual hierarchy."

## Criteria

### Typography

- Reuse the brand type system when it exists.
- Select roles by language coverage, readability, hierarchy, loading, and product character.
- Use a bounded semantic scale and support long content, localization, text resizing, dynamic type, and user font preferences where applicable.
- Avoid arbitrary per-component sizes, unpredictable viewport-width scaling, and unjustified letter spacing.

Read [references/typography.md](references/typography.md) for the decision record.

### Color and themes

- Start from semantic roles for surfaces, text, borders, actions, focus, status, and data series.
- Preserve meaning without color and check text, icons, controls, focus, charts, dark mode, high contrast, and forced colors.
- Preserve brand colors through accessible pairings and fallbacks rather than flattening the product into one hue.

Read [references/color-and-contrast.md](references/color-and-contrast.md).

### Layout, density, and assets

- Let the workflow choose density and composition.
- Use cards for repeated comparable items, modals, or genuinely framed tools, not every section.
- Establish stable dimensions for data regions, media, controls, and content that would otherwise shift.
- Prefer alignment, grouping, rhythm, contrast, and whitespace over ornamental containers.
- Use icons and imagery with a clear information, brand, or state purpose.

Read [references/layout-and-density.md](references/layout-and-density.md).

### Motion and feedback

- Use motion to explain state, continuity, progress, hierarchy, or spatial relationships.
- Prefer transform and opacity when appropriate, honor reduced motion, and provide non-motion comprehension.
- Avoid scroll hijacking, custom cursors, continuous parallax, and decorative animation without an approved reason.

Read [references/motion.md](references/motion.md).

## Trend applicability gate

Use a trend only when it supports the primary job, fits the brand and trust context, works across required conditions, preserves hierarchy and budgets, integrates with the existing system, and beats a simpler established pattern.

Use [assets/human-review-checklist.md](assets/human-review-checklist.md) and record evidence for `pass`, `needs revision`, `blocked`, or `not applicable`.

## Limits

- Do not create a brand identity or replace an approved design system.
- Do not copy proprietary assets, exact layouts, text, or branding from reference products.
- Do not treat Apple, Material, Fluent, or a current trend as a universal standard.
- Do not approve contrast, runtime rendering, or motion behavior without applicable evidence.

## Output template

```markdown
## Visual system result
**Status:** ready | needs revision | blocked

### Evidence
| Source | Existing rule | Gap |
| --- | --- | --- |

### Visual contract
| Area | Semantic decision | Product rationale | Token/component impact |
| --- | --- | --- | --- |

### Runtime and accessibility evidence required
- <check>

### Rejected generic defaults
- <default and reason>
```

## Quality gate

- [ ] Decisions start from product and repository evidence.
- [ ] Typography, semantic color, layout, density, assets, themes, and motion are considered when applicable.
- [ ] Every addition fits or deliberately extends the existing system.
- [ ] Hierarchy and product purpose justify decorative choices.
- [ ] Long content, localization, zoom, contrast modes, and reduced motion have defined behavior.
- [ ] The human review checklist has no unresolved blocked item.

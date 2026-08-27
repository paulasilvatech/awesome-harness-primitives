---
name: frontend-dashboard-visualization
description: >-
  Design and review dashboards, KPI surfaces, operational consoles, tables, chart selection,
  analytical interaction, and accessible data visualization from real questions and data
  properties. Use this skill when frontend work involves metrics, charts, monitoring, reporting,
  or data storytelling.
---

<!-- Generated from harness/github-copilot/skills/frontend-dashboard-visualization/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend dashboard visualization

Start with the user's analytical question and the real data shape, then choose the simplest encoding that supports an accurate decision.

## When to invoke

- "Design an operational dashboard from these real metrics."
- "Choose the right chart for this analytical question."
- "Review this KPI page for misleading or inaccessible visualization."
- "Define dashboard filters, tables, drilldowns, and failure states."
- "Test a chart-heavy frontend with realistic edge cases."

## Analytical contract

For every metric or visualization, record:

- question or decision supported;
- metric name, definition, unit, time window, comparison baseline, update time, and provenance;
- dimensions, cardinality, ordering, missingness, precision, and uncertainty;
- target audience and required scanning or exact-value behavior;
- filters, drilldowns, exports, annotations, thresholds, and access limits;
- loading, empty, delayed, partial, stale, unavailable, error, and recovery states.

Never invent a metric or use fictional production values unless the user explicitly requests labeled synthetic fixture data.

## Chart and table selection

Read [references/chart-selection.md](references/chart-selection.md). Prefer tables for exact values and operational scanning. Use charts only when position, length, area, color, or another encoding improves the stated question.

Read [references/dashboard-patterns.md](references/dashboard-patterns.md) for filter, provenance, density, and state behavior. Read [references/accessible-data-visualization.md](references/accessible-data-visualization.md) for summaries, tables, keyboard, focus, and non-color alternatives.

## Criteria

- Titles and summaries reflect active filters, time windows, and comparison context.
- Zero, missing, delayed, partial, stale, and unavailable data remain distinct.
- Dates, timezones, currency, percentages, precision, and large values are consistent.
- Dense labels, negative values, outliers, long series, empty ranges, and loading do not create misleading output.
- Interactive controls have accessible names, keyboard behavior, visible state, and reversible outcomes.
- Color is not the only series, threshold, selection, or status cue.
- Download or underlying tables appear only when product and data policy permit them.
- Rendering cost, large collections, and update frequency fit the product's runtime budget.

Use [assets/operational-dashboard-review.md](assets/operational-dashboard-review.md) and [assets/human-review-checklist.md](assets/human-review-checklist.md).

## Limits

- Do not select a chart because it is fashionable or available in a library.
- Do not infer causation from correlation or precision from decorative animation.
- Do not add a new chart library when the installed one satisfies the contract.
- Do not expose restricted raw data or enable exports without product policy.

## Output template

```markdown
## Dashboard visualization result
**Status:** ready | needs revision | blocked

### Analytical contract
| Question | Metric/data | Context and provenance | Audience action |
| --- | --- | --- | --- |

### Encodings and interactions
| Need | Selected table/chart | Why | Accessible alternative | Edge states |
| --- | --- | --- | --- | --- |

### Validation
| Fixture/state | Behavioral check | Visual/a11y check | Result |
| --- | --- | --- | --- |
```

## Quality gate

- [ ] Every visualization traces to a real analytical question and data shape.
- [ ] Metrics include units, windows, baselines, freshness, and provenance.
- [ ] Zero, missing, partial, delayed, stale, unavailable, and error states remain distinguishable.
- [ ] Exact-value, accessible-summary, keyboard, color-independent, and edge-data behavior is defined.
- [ ] Library and rendering-cost decisions use repository evidence.
- [ ] The human review checklist has no unresolved blocked item.

---
name: power-bi-report-design-consultation
description: >-
  Design effective Power BI report layouts, chart selections, interactions, accessibility, mobile
  views, and implementation guidance. Use when asked for Power BI visualization design, dashboard
  layout, chart choice, KPI report structure, slicer/navigation design, accessibility review,
  mobile report design, or report UX consultation.
---

<!-- Generated from harness/github-copilot/skills/power-bi-report-design-consultation/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power BI report design consultation

Guide Power BI report design by gathering business, data, and technical context; selecting visuals by analytical relationship and audience; specifying layout, color, typography, interactions, mobile behavior, accessibility, and validation criteria; and returning an implementation-ready design specification.

## When to invoke

- "Design a Power BI dashboard for these KPIs."
- "Which charts should I use in this report?"
- "Review this Power BI layout for accessibility."
- "Create a mobile-friendly Power BI report design."
- "Plan slicers, drill-through, and navigation for this report."

## Initial requirements

| Assessment | Questions |
| --- | --- |
| Business context | What problem are you solving? Who is the audience: executives, analysts, or operators? What decisions will the report support? What are the KPIs? How will it be accessed: desktop, mobile, or presentation? |
| Data context | What data types exist: categorical, numerical, temporal? What volume and granularity? Are there hierarchies? What comparisons, trends, or drill-downs matter most? |
| Technical requirements | Performance constraints, accessibility requirements, brand guidelines, color restrictions, mobile needs, responsive design, integrations, and report dependencies. |

## Chart selection methodology

| Relationship | Visuals | Use when |
| --- | --- | --- |
| Comparison Analysis | Bar/Column Charts, Horizontal Bars, Bullet Charts, Dot Plots. | Comparing categories, ranking items, long labels, targets, or precise values with minimal ink. |
| Trend Analysis | Line Charts, Area Charts, Stepped Lines, Sparklines. | Continuous time series, cumulative values, composition over time, discrete changes, or inline trend indicators. |
| Composition Analysis | Stacked Bars, Donut/Pie Charts, Treemaps, Waterfall. | Parts of whole, simple composition with max `5-7` categories, hierarchy, or sequential bridge analysis. |
| Distribution Analysis | Histograms, Box Plots, Scatter Plots, Heat Maps. | Frequency, statistical spread, correlation, outliers, or two-dimensional patterns. |

Avoid dense matrices, complex scatter plots, multi-series area charts, and small multiple visuals on mobile unless the user specifically needs analytical detail.

## Audience-specific patterns

| Audience | Design pattern |
| --- | --- |
| Executive Dashboard Design | High-level KPIs, exception-based red/yellow/green highlighting, trend indicators, minimal text, maximum insight density, clean layout, and white space. |
| Analytical Report Design | Drill-down capability, period-over-period comparisons, interactive filtering, detailed data tables when needed, and comprehensive legends/context. |
| Operational Report Design | Real-time or near-real-time display, action-oriented status indicators, exception alerts, mobile optimization for field use, and quick refresh. |

## Information architecture and visual specifications

Prioritize content in this order: Critical Metrics; Supporting Context; Detailed Analysis; Navigation & Filters.

```text
┌─────────────────────────────────────────┐
│ Header: Title, Key KPIs, Date Range     │
├─────────────────────────────────────────┤
│ Primary Insight Area                    │
│ ┌─────────────┐  ┌─────────────────────┐│
│ │   Main      │  │   Supporting        ││
│ │   Visual    │  │   Context           ││
│ │             │  │   (2-3 smaller      ││
│ │             │  │    visuals)         ││
│ └─────────────┘  └─────────────────────┘│
├─────────────────────────────────────────┤
│ Secondary Analysis (Details/Drill-down) │
├─────────────────────────────────────────┤
│ Filters & Navigation Controls           │
└─────────────────────────────────────────┘
```

| Color | Use |
| --- | --- |
| Green `#2E8B57` | Positive performance, on-target, growth. |
| Red `#DC143C` | Negative performance, alerts, below-target. |
| Blue `#4682B4` | Neutral information and base metrics. |
| Orange `#FF8C00` | Warnings and attention needed. |
| Gray `#708090` | Inactive, reference, and disabled states. |

Accessibility rules: text contrast at least `4.5:1`, colorblind-friendly palette, avoid red-green-only distinctions, include pattern or shape alternatives, support high contrast mode, and provide alternative text for screen readers.

Typography hierarchy: Report Title `20-24pt` Bold Brand Font; Page Titles `16-18pt` Semi-bold Sans-serif; Section Headers `14-16pt` Semi-bold; Visual Titles `12-14pt` Medium; Data Labels `10-12pt` Regular; Footnotes/Captions `9-10pt` Light. Use at most two font families, adequate spacing, left-aligned body text, and centered alignment only for titles.

## Interaction and responsive design

| Pattern | Best for | Implementation rules |
| --- | --- | --- |
| Tab Navigation | Related areas and time periods. | Max 7 tabs, active-state indication, consistent layouts, logical order. |
| Drill-through Design | Detail exploration and context switching. | Clear drill cues, contextual page filters, back button, consistent styling. |
| Button Navigation | Guided workflows and external links. | Action labels, consistent sizing, clear hierarchy, touch target minimum `44px`. |
| Slicers | User-controlled filtering. | Logical grouping, search for high-cardinality fields, single/multi-select by use case, applied-filter indicators, reset/clear all. |
| Filters | Scoped constraints. | Use page-level for common scenarios, visual-level for specific needs, report-level for global constraints, drill-through filters for detail pages. |

Mobile-first rules: use portrait orientation, touch-friendly `44px` targets, simplified navigation with hamburger menus, stacked layout instead of side-by-side, larger fonts, and increased spacing. Prefer Card visuals for KPIs, simple bar and column charts, line charts with minimal data points, and large gauge/KPI visuals.

## Design validation

| Validation area | Checks |
| --- | --- |
| Visual Clarity | Hierarchy, contrast, readability, logical eye movement, minimal cognitive load, and white space. |
| Functional Design | Interactions, navigation, filters, mobile experience, and performance across devices. |
| Accessibility Compliance | Screen reader compatibility, keyboard navigation, high contrast, alternative text, and color not being the only carrier. |
| User Testing | Initial orientation `30 seconds`, finding information `2 minutes`, comparing data `3 minutes`, drilling down `2 minutes`, and mobile simulation `5 minutes`. |
| Success Criteria | Task completion rates `>80%`, time to insight `<2 minutes`, satisfaction `>4/5`, no critical usability issues, and accessibility validation passed. |

## Implementation plan

| Phase | Target |
| --- | --- |
| Phase 1 (Week 1) | Core dashboard with KPIs and primary visual. |
| Phase 2 (Week 2) | Supporting visuals and basic interactions. |
| Phase 3 (Week 3) | Advanced interactions and drill-through. |
| Phase 4 (Week 4) | Mobile optimization and final polish. |

Quality assurance covers visual accuracy validation, interaction testing across browsers, mobile device testing, accessibility compliance check, performance validation, and user acceptance testing. Success metrics include engagement/adoption, time to insight, decision-making improvement, satisfaction, and performance benchmarks.


## Design vocabulary and non-obvious constraints

Use plain design language the requester recognizes: reports should be `user-friendly`, `data-driven`, and able to support `drill-down` when the audience needs detail. Operational pages may need `real-time` or near-real-time refresh. Treemaps are `space-efficient` but can hide small categories. Accessibility requires avoiding `red-green` only encodings. Slicers need `Reset/clear` affordances so users can recover from filter states.

## Output template

```markdown
## Power BI design recommendation — <report name>

**Status:** recommended | needs input | blocked
**Audience:** executives | analysts | operators | mixed
**Primary decisions supported:** <decisions>

### Executive summary
- Report purpose: <purpose>
- Design principles: <principles>
- Primary visual selections: <summary>
- Expected user experience outcomes: <outcomes>

### Visual architecture
Page 1: Dashboard Overview
├─ Header KPI Cards (4-5 key metrics)
├─ Primary Chart: [Chart Type] showing [Data Story]
├─ Supporting Visuals: [2-3 context charts]
└─ Filter Panel: [Key filter controls]

Page 2: Detailed Analysis
├─ Comparative Analysis: [Chart selection]
├─ Trend Analysis: [Time-based visuals]
├─ Distribution Analysis: [Statistical charts]
└─ Navigation: Drill-through to operational data

### Interaction design
- Cross-filtering strategy: <strategy>
- Drill-through implementation: <pages and filters>
- Navigation flow: <tabs/buttons/back paths>
- Mobile optimization: <layout and visual substitutions>

### Accessibility and style
| Area | Specification |
| --- | --- |
| Color | <semantic palette and contrast notes> |
| Typography | <title/page/header/label sizes> |
| Keyboard and screen reader | <requirements> |

### Implementation priority
| Phase | Scope | Validation |
| --- | --- | --- |
| Week 1 | <core dashboard> | <checks> |
| Week 2 | <supporting visuals> | <checks> |
| Week 3 | <interactions> | <checks> |
| Week 4 | <mobile and polish> | <checks> |
```

## Quality gate

- [ ] Business, data, and technical context were gathered or missing inputs were listed.
- [ ] Chart recommendations match the analytical relationship and audience.
- [ ] Layout prioritizes KPIs, primary insight, supporting context, details, and filters.
- [ ] Color, typography, and interaction specifications include accessibility requirements.
- [ ] Mobile behavior is explicitly addressed with `44px` touch targets and simplified visuals.
- [ ] Validation includes clarity, functional behavior, accessibility, user testing, and performance.
- [ ] Implementation phases and success metrics are concrete enough for a Power BI developer to execute.

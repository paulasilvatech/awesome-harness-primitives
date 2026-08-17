---
applyTo: "**/*.{pbix,md,json,txt}"
description: "Enforces Power BI report design, visualization, accessibility, interaction, performance, mobile, testing, and governance conventions for report artifacts and supporting documentation."
---

# Power BI Report Design Conventions — Effective Reports and Dashboards

These instructions apply to Power BI report files and supporting report-design documentation matched by `**/*.{pbix,md,json,txt}`. They are authoritative for visual selection, page layout, interactions, formatting, accessibility, performance, mobile behavior, testing, and custom visual governance in Power BI reports and dashboards; source-system modeling, DAX semantics, deployment pipelines, and tenant administration win where they define stricter project rules.

## Information Architecture and User Experience

Design every report around the decision the user must make, then make the most important insight easiest to find.

| Concern | Convention | Rationale |
| --- | --- | --- |
| Visual hierarchy | Put primary KPIs, key metrics, and critical insights in the `top-left` or header area; place secondary trends and comparisons in the body; place tertiary filters, navigation, and notes in sidebars or footers. | Users scan reports before reading details, so the most important information must appear first. |
| Content structure | Use a header for title and KPIs, a main content area for primary and supporting visuals, and a footer for filters, navigation, and notes. | A predictable report page layout reduces cognitive load and supports repeat use. |
| Clarity | Give every visual, slicer, button, and note a clear purpose. | Decorative or ambiguous elements distract from decisions. |
| Consistency | Reuse styling, colors, terminology, and interactions across pages and reports. | Consistency lets users transfer learning between views. |
| Context | Include time periods, definitions, units, methodology notes, and data caveats where interpretation depends on them. | Users need enough context to trust the numbers. |
| Action | Prefer action-oriented titles, subtitles, and callouts that identify what changed and what to do next. | Reports should guide data-driven decisions rather than merely display data. |

Use this canonical layout shape unless the audience or device constraints require a different composition:

```text
Report Page Layout:
┌─────────────────────────────────────┐
│ Header: Title, KPIs, Key Metrics    │
├─────────────────────────────────────┤
│ Main Content Area                   │
│ ┌─────────────┐ ┌─────────────────┐ │
│ │  Primary    │ │  Supporting     │ │
│ │  Visual     │ │  Visuals        │ │
│ └─────────────┘ └─────────────────┘ │
├─────────────────────────────────────┤
│ Footer: Filters, Navigation, Notes  │
└─────────────────────────────────────┘
```

## Chart Selection

Choose the visual that matches the analytical question, not the one that looks most impressive.

| Question | Preferred visual | Rules |
| --- | --- | --- |
| Compare categories, rank items, compare entities, or show discrete period changes | `Bar/Column` charts | Start axes at zero for comparison, sort by value for ranking, use consistent colors within groups, limit to 7-10 categories, and prefer horizontal bars when category names are long. |
| Show continuous trends, seasonality, cycles, patterns, forecasting, projections, or multiple metrics over time | Line charts | Use consistent time intervals, start the Y-axis at zero for absolute values, use different line styles for multiple series, and add data point markers for sparse data. |
| Show simple parts-of-whole composition where percentages matter more than absolutes | `Pie/Donut` charts | Limit to 5-7 categories; avoid them for similar-sized segments, many categories, or change over time. Use stacked bars when readability matters more than circular composition. |
| Show composition and totals together | Stacked charts | Use regular stacked charts for absolute plus relative values, 100% stacked charts for proportions, and clustered charts for side-by-side sub-categories. |
| Show correlation, outliers, clustering, quadrant analysis, risk vs. return, or performance vs. cost efficiency | Scatter plots or bubble charts | Use size for a third dimension, color for categories, trend lines when appropriate, and labels for outliers or key points. |
| Show dense patterns across two categorical dimensions | Heat maps and conditional formatting | Use colorblind-friendly scales, data labels when space permits, clear legends, and map-style background colors only when values remain readable. |
| Show transaction-level detail | Tables or matrices | Keep columns purposeful, support drill-through instead of crowding overview pages, and verify performance with realistic data. |
| Show high-level status or simple aggregations | Card, KPI, or Gauge | Use for landing-page summaries and real-time monitoring when the measure is simple and interpretation is immediate. |

## Page Layout and Navigation

Use page patterns deliberately.

| Pattern | Use when | Required conventions |
| --- | --- | --- |
| Single page dashboard | Executive summaries, simple KPI tracking, real-time monitoring, mobile-first scenarios. | Limit to 6-8 visuals, group related content, maintain clear hierarchy, and test responsive design. |
| Multi-page report | Complex analytics, different personas, detailed drill-down analysis, comprehensive business reporting. | Organize pages as executive summary, detailed analysis, operational details, and appendix when those layers exist. |
| Tab navigation | Related content areas, different views of the same data, role-based sections, or daily/weekly/monthly analysis. | Use descriptive tab names, consistent layouts, clear active-tab styling, and importance-based tab order. |
| Bookmark navigation | Predefined scenarios, filtered views, story-telling sequences, and guided analysis paths. | Name bookmarks descriptively, group related bookmarks, and test restored filter and visual state thoroughly. |
| Button navigation | Custom flows, action-oriented interactions, drill-down paths, or external links. | Use consistent styling, clear labels, touch-appropriate sizing, and visible interaction feedback. |

Do not create circular navigation loops, hidden navigation, or broken drill-through behavior. Hide drillthrough pages from main navigation when they exist only as contextual targets.

## Interaction Design

Make interactions discoverable, purposeful, and performant.

| Interaction | Convention | Rationale |
| --- | --- | --- |
| Default tooltips | Include relevant dimensions, formatted values, related metrics not shown in the visual, and concise explanatory text. | Tooltips add context without cluttering the canvas. |
| Report page tooltips | Use a dedicated tooltip page of about 320x240 pixels, match main report styling, filter it correctly, and test fast loading. | Mini-dashboard tooltips help users inspect detail without leaving the source visual. |
| Drillthrough | Use for summary-to-detail and contextual analysis, such as monthly sales summary to transaction-level detail or product performance to product analysis. | Drillthrough preserves overview pages while supporting detailed exploration. |
| Cross-filtering | Enable it only when visuals have a clear logical relationship and the performance impact is acceptable. | Thoughtful cross-filtering improves analysis; indiscriminate cross-highlighting confuses users and slows pages. |
| Disabled interactions | Disable cross-filtering for independent analysis, misleading relationships, high-cardinality slicers, large datasets, or pages with too many visuals. | Users should not infer a relationship the data model does not support. |

Use Edit interactions for each visual pair, test with realistic data volumes and user scenarios, provide clear selection feedback, consider mobile touch behavior, and document non-obvious interaction decisions.

## Visual Design and Formatting

Color, typography, and spacing must communicate meaning before decoration.

| Area | Convention | Rationale |
| --- | --- | --- |
| Semantic colors | Use green for positive performance, growth, success, and on-target status; red for negative performance, decline, alerts, and over-budget status; blue for neutral information and corporate branding; orange for warnings; gray for inactive or reference information. | Stable color meaning improves recognition across reports. |
| Brand integration | Use the corporate palette consistently, keep at least a 4.5:1 contrast ratio for normal text, and test projectors, mobile, print, and colorblind contexts. | Reports must remain legible beyond the designer's screen. |
| Color accessibility | Do not rely only on color; pair color with labels, icons, patterns, shapes, or data labels. Avoid red-green combinations without alternatives and test with tools such as Colour Oracle. | About 8% of males have colorblindness; color alone excludes users. |
| Typography | Use 18-24pt bold report titles, 16-20pt semi-bold page titles, 14-16pt semi-bold section headers, 12-14pt visual titles, 10-12pt body text, 9-11pt data labels, and 8-10pt `Captions/Legends`. | A consistent hierarchy makes reports scannable. |
| Font choice | Use clear sans-serif fonts, a maximum of two font families, high contrast, adequate white space, and left-aligned body text. | Readability matters more than visual novelty. |
| Titles and labels | Use clear, descriptive, action-oriented language; avoid unexplained jargon and abbreviations such as `CSAT`; include time periods and units. | Users should understand a visual without asking the author. |
| Spacing | Use consistent grid multiples such as 8px, 16px, and 24px; align visuals; group related content; separate unrelated areas with white space. | Layout discipline keeps pages professional and reduces overload. |

## Performance and Data Volume

Prefer focused pages and server-side reduction over crowded canvases and expensive interactions.

| Performance area | Convention | Rationale |
| --- | --- | --- |
| Visual count | Keep most pages to 6-8 visuals and split complex stories across tabs, drill-through, or focused pages. | Fewer visuals reduce query fan-out and improve readability. |
| Query reduction | Apply filters early, use page-level filters for common scenarios, avoid high-cardinality fields in slicers, and pre-filter large datasets. | Smaller result sets improve load and interaction time. |
| Initial load | Put summary views on landing pages, use default filters, minimize landing-page visuals, and progressively disclose detail. | Users get useful information before expensive detail loads. |
| Interaction load | Optimize slicer combinations, efficient cross-filtering, calculated visuals, and caching strategies. | Fast interaction keeps exploration fluid. |
| Visual performance | Prefer Card, KPI, and Gauge for simple aggregations; expect bar, column, and line charts to be moderate; treat scatter plots, maps, custom visuals, matrix, and wide tables as heavier. | Visual choice affects rendering and query cost. |
| Testing | Use Performance Analyzer, realistic data volumes, concurrent user scenarios, mobile performance checks, and different network conditions. | Performance must be measured under representative use. |

## Mobile and Responsive Design

Design mobile layouts intentionally instead of trusting the desktop canvas to shrink.

| Mobile concern | Convention | Rationale |
| --- | --- | --- |
| Layout | Use portrait orientation as the primary mobile layout and design for the smallest target screen first. | Mobile users need a focused reading path. |
| Touch | Use touch-friendly targets of at least 44px and make buttons and slicers easy to tap. | Small controls cause interaction errors. |
| Density | Reduce visual density, prioritize key metrics, hide or consolidate less critical visuals, and use drill-through for detail. | Mobile screens cannot carry desktop complexity. |
| Scrolling | Prefer vertical scrolling; avoid horizontal scrolling. | Horizontal scrolling hides context and breaks comparison. |
| Implementation | Use Power BI Desktop Mobile layout view, rearrange visuals for portrait, resize for mobile screens, and test key interactions with touch. | Mobile layout is a separate design surface. |
| Testing | Test actual iOS and Android devices, the Power BI Mobile app, slower networks, battery impact, mobile refresh, and offline needs where applicable. | Emulators do not catch all device and network issues. |

## Accessibility and Inclusive Design

Meet inclusive design requirements as report design constraints, not post-build cleanup.

| Requirement | Convention | Rationale |
| --- | --- | --- |
| Visual accessibility | Use high contrast, alternative text for images and icons, clear hierarchy, and colorblind-friendly schemes. | Users must perceive and understand the report without relying on one sensory channel. |
| Interaction accessibility | Support keyboard navigation, screen readers, clear focus indicators, logical tab order, and descriptive link and button labels. | Reports must be operable without a mouse. |
| Content accessibility | Use plain language, consistent terminology, context for abbreviations and acronyms, and alternative formats when needed. | Cognitive accessibility improves comprehension for all users. |
| Multi-sensory design | Use patterns, shapes, text labels, and data tables alongside color; add audio descriptions for complex visuals only when the delivery channel supports them. | Redundant cues make meaning resilient. |
| Testing | Use screen readers, keyboard-only navigation, colorblind simulation, disability feedback, and regular accessibility audits. | Accessibility defects are easiest to find by using assistive paths. |

## Conditional Formatting and Custom Visuals

Use advanced visuals only when they add interpretable signal.

| Technique | Convention | Rationale |
| --- | --- | --- |
| Data bars | Use consistent scale across rows and colors that remain visible on mobile. | Data bars support quick comparison inside tables. |
| Background colors | Use heat map-style or red/yellow/green status thresholds only when the legend and values make the rule clear. | Conditional colors should explain status, not hide data. |
| Font formatting | Use size, color, bold, and italics sparingly to mark importance, performance, emphasis, and secondary information. | Too much formatting becomes chart junk. |
| Thresholds | Document rules such as green `>110% of target`, yellow `90-110% of target`, and red `<90% of target`. | Users need to understand status calculations. |
| Custom visuals | Prefer Microsoft AppSource certified visuals with active support, regular updates, clear documentation, acceptable performance, accessibility compliance, and known security and data handling. | Custom visuals add supply-chain and maintenance risk. |
| Governance | Require approval, maintain an approved list, document use cases, monitor maintenance, and define fallback strategies if a custom visual becomes unavailable. | Reports should not depend on unmanaged extensions. |

## Testing and Quality Assurance

Validate reports as products, not screenshots.

| Test area | Required checks |
| --- | --- |
| Visual functionality | Charts display data correctly, filters work, cross-filtering behaves as intended, drill-through works, tooltips are relevant, bookmarks restore state, and export functions work. |
| Interaction | Button navigation works, slicer combinations behave correctly, pages load within acceptable time, mobile layouts display properly, responsive design adapts, and print layouts remain readable. |
| Data accuracy | Totals match source systems, calculations produce expected results, filters do not accidentally exclude data, date ranges are correct, business rules are implemented, and edge cases are handled. |
| Usability | Test with actual business users, observe pain points, time common tasks, gather feedback on clarity and usefulness, and include different user skill levels. |
| Performance | Test realistic volumes, concurrent users, network variations, mobile devices, and refresh behavior during peak usage. |
| Cross-platform | Test Chrome, Firefox, Edge, Safari, iOS, Android, Power BI Mobile app, different resolutions, and network speeds. |
| Review process | Include developer testing, peer review, business review, user acceptance, performance review, and accessibility review. |
| Documentation | Maintain report purpose, target audience, data sources, refresh schedule, business rules, calculation explanations, user guide, training material, limitations, workarounds, maintenance, and update procedures. |
| Continuous improvement | Review usage analytics, collect feedback, monitor performance, update content relevance and accuracy, and adopt useful platform features deliberately. |

## Anti-Patterns

Remove or redesign patterns that create confusion, exclusion, or slow performance.

| Anti-pattern | Avoid | Rationale |
| --- | --- | --- |
| Chart junk | Unnecessary 3D effects, excessive animation, decorative elements, and over-complicated effects. | Decoration steals attention from insight. |
| Information overload | Too many visuals, cluttered layouts, insufficient white space, competing focal points, and overwhelming color. | Users cannot act when every element demands attention. |
| Poor color choices | Red-green meaning without alternatives, low contrast, inconsistent meanings, and over-use of bright saturated colors. | Color misuse causes errors and accessibility failures. |
| Navigation confusion | Inconsistent patterns, hidden options, unexpected drill-through, and circular loops. | Users lose orientation and trust. |
| Performance problems | Too many visuals, inefficient cross-filtering, unnecessary real-time refresh, and large unfiltered datasets. | Slow reports discourage use and hide insights. |
| Mobile unfriendly design | Small touch targets, horizontal scrolling, unreadable text, and non-functional interactions. | Mobile users need a usable report, not a shrunken desktop page. |

## Good / Bad Examples

The examples below illustrate page design density and interaction discipline.

**Good:**

```text
Executive Summary page
- Header: report title, date range, 3 KPI cards
- Body: one ranked bar chart, one trend line, one supporting composition chart
- Footer: page-level filters, notes, and a drill-through button to transaction-level detail
- Interactions: cross-filtering only between related visuals; tooltip page sized 320x240 pixels
```

Why: The page uses visual hierarchy, limits the visual count, keeps detail behind drill-through, and makes interactions purposeful.

**Bad:**

```text
Executive Summary page
- 16 visuals, 5 slicers, 3 custom visuals, 2 maps, 4 tables, and decorative shapes
- Red/green status only, no labels, low contrast, tiny text, and horizontal mobile scrolling
- Every visual cross-filters every other visual, including unrelated metrics
```

Why: The page creates information overload, accessibility failures, confusing cross-filtering, weak mobile usability, and likely performance problems.

## Conventions

| Rule | Rationale |
|---|---|
| Put primary insights in the header or top-left area and organize secondary and tertiary content around them. | Users scan pages before interpreting detail. |
| Match chart types to comparison, trend, composition, relationship, distribution, or detail questions. | Visual mismatch leads to misinterpretation. |
| Keep most pages to 6-8 visuals and move details into drill-through or separate pages. | Focused pages are easier to read and faster to load. |
| Use semantic, accessible colors and never rely on color alone. | Reports must work for colorblind and assistive-technology users. |
| Use consistent typography, spacing, labels, and terminology. | Consistency reduces cognitive load and review friction. |
| Configure tooltips, bookmarks, buttons, and cross-filtering intentionally. | Interactions must explain data rather than surprise users. |
| Test reports with realistic data, users, devices, networks, and accessibility paths. | Report quality depends on behavior under real conditions. |
| Govern custom visuals before adopting them. | Custom visuals can add performance, security, accessibility, and maintenance risk. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use bar or column charts for category comparison and ranking. | Use pie or donut charts for many categories or similar-sized segments. |
| Use line charts for continuous time trends. | Mix inconsistent time intervals in one trend visual. |
| Use stacked charts when composition and totals both matter. | Force parts-of-whole or `of-whole` analysis into hard-to-read circular charts. |
| Enable drill-through for detail pages and hide those pages from main navigation. | Cram transaction-level detail onto overview pages. |
| Use labels, icons, patterns, and text with color. | Rely on red/yellow/green or red-green color alone. |
| Use Performance Analyzer and realistic volumes. | Guess at performance from a tiny sample dataset. |
| Design and test the Power BI Mobile layout separately. | Assume the desktop canvas is automatically mobile-friendly. |
| Approve and document custom visuals. | Add unsupported custom visuals because they look impressive. |

## Checklist Before Opening a PR

- [ ] The report has clear primary, secondary, and tertiary information hierarchy.
- [ ] Chart choices match the analytical questions and avoid chart junk.
- [ ] Each page stays focused, usually within 6-8 visuals, with detail moved to drill-through or separate pages.
- [ ] Navigation, bookmarks, buttons, tooltips, and cross-filtering are tested with realistic scenarios.
- [ ] Colors, typography, spacing, labels, legends, and notes meet accessibility and readability conventions.
- [ ] Mobile layout is designed in Power BI Desktop and tested with touch interactions.
- [ ] Performance is checked with realistic data volumes, slicers, cross-filtering, and network conditions.
- [ ] Data accuracy, filters, calculations, date ranges, exports, and edge cases are verified.
- [ ] Custom visuals are approved, documented, accessible, performant, and have fallback plans.
- [ ] Documentation covers purpose, audience, data sources, refresh schedule, business rules, limitations, and maintenance.

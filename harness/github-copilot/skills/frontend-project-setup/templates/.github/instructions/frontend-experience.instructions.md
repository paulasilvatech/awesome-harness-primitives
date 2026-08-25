---
description: "Applies product-specific frontend implementation, state-completeness, responsive, and accessibility conventions. Use when editing detected frontend application files."
applyTo: "__FRONTEND_APPLY_TO__"
---

# Frontend Experience Conventions — Product-Specific Implementation

These instructions apply to detected frontend application files. They are authoritative for evidence, design-system reuse, interaction completeness, responsive adaptation, and implementation validation in the matched files; explicit product requirements, repository-wide instructions, stricter security or accessibility policy, and approved design-system rules win on conflict.

## Evidence and Scope

- Inspect the approved story and acceptance IDs, local framework, versions, components, tokens, data clients, tests, and supported surfaces before editing.
- Preserve the approved file scope and return requirement gaps instead of inventing product behavior.
- Reuse existing components, tokens, libraries, content patterns, and state conventions before adding alternatives.

## Interaction and State

- Implement every visible control or make it honestly unavailable with an explanation.
- Cover applicable loading, empty, partial, error, offline, success, disabled, permission, cancellation, retry, and recovery states.
- Preserve input and user context after recoverable failures.
- Keep API, authentication, event, and generated-client boundaries typed; do not redefine backend contracts silently.

## Responsive and Accessible Behavior

- Adapt information priority, navigation, content, and controls at actual layout transitions instead of only stacking desktop regions.
- Prefer semantic HTML and native controls, then current platform patterns for genuine gaps.
- Preserve keyboard completion, visible focus, labels, names, states, zoom/reflow, color-independent meaning, reduced motion, touch, and long localized content.
- Treat automated accessibility findings as partial evidence, not certification.

## Conventions

| Rule | Rationale |
| --- | --- |
| Ground visual decisions in the product job and real content. | Generic layout defaults erase product identity and hierarchy. |
| Keep changes inside the established frontend system. | Parallel design systems and libraries create drift and maintenance cost. |
| Map acceptance IDs to focused evidence. | Completion remains observable and independently verifiable. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Reuse local primitives and implement complete behavior. | Fill the interface with interchangeable cards or inert controls. |
| Surface unknowns and contract conflicts. | Invent users, metrics, rules, permissions, or service behavior. |
| Run existing targeted checks and report unrun runtime evidence. | Claim browser, device, accessibility, or integration success from static checks. |

## Checklist Before Opening a PR

- [ ] Product evidence, stable IDs, approved scope, and local conventions were inspected.
- [ ] Applicable states, controls, data boundaries, and recovery behavior are complete.
- [ ] Responsive, keyboard, focus, zoom, localization, contrast, and motion behavior is addressed.
- [ ] Focused existing type, lint, build, and test commands pass.
- [ ] Required browser, device, accessibility, and backend checks ran or are explicit gaps.
- [ ] The diff contains no unrelated edits, secrets, personal data, or placeholders.

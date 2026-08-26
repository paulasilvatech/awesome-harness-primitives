---
description: "Applies frontend test structure, selectors, fixtures, repeatability, evidence hygiene, and acceptance traceability conventions. Use when editing detected frontend test files."
applyTo: "__FRONTEND_TEST_APPLY_TO__"
---

# Frontend Testing Conventions — Risk-Based Evidence

These instructions apply to detected frontend tests. They are authoritative for selector quality, deterministic fixtures, risk-based layer selection, runtime evidence hygiene, and acceptance traceability in the matched files; the project's established runner and stricter quality or security policies win on conflict.

## Test Contract

- Map each test to observable user behavior and stable acceptance/scenario IDs when the project records them.
- Use the smallest layer that proves the behavior, then add contract, service, E2E, visual, accessibility, performance, or device evidence only for real boundaries and risk.
- Prefer roles, labels, accessible names, visible text, and established stable IDs over styling, DOM order, framework internals, or arbitrary sleeps.

## Repeatability and Evidence

- Reuse local render helpers, fixtures, factories, auth state, seed, cleanup, browser projects, and commands.
- Freeze dates, randomness, locale, timezone, feature flags, data, fonts, and animation when they affect results.
- Record first-attempt status and retries; do not turn unexplained flakiness into a pass.
- Keep secrets, credentials, personal data, customer content, and private URLs out of fixtures and artifacts.

## Runtime Boundaries

- Keep mocks, schemas, consumer/provider contracts, real-service integration, E2E, screenshots, accessibility, and device checks distinct.
- Pair visual comparisons with behavioral assertions and review baseline changes as product changes.
- Report unavailable browsers, services, devices, assistive technologies, or environments as evidence gaps.

## Conventions

| Rule | Rationale |
| --- | --- |
| Test public behavior and semantics. | Implementation-detail tests fail during safe refactors and miss user regressions. |
| Make data and environments deterministic. | Stable evidence reduces false failures and hidden ordering dependencies. |
| Preserve evidence-category boundaries. | One passing layer cannot prove an unexecuted runtime boundary. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use web-first and event-aware assertions. | Add sleeps to hide readiness or race problems. |
| Exercise success, failure, access, cancellation, and recovery by risk. | Test only the happy path or duplicate every assertion at every layer. |
| Redact and retain artifacts according to project policy. | Commit production secrets, personal data, or uncontrolled screenshots. |

## Checklist Before Opening a PR

- [ ] Tests map to user-visible behavior and applicable acceptance/scenario IDs.
- [ ] Existing runner, helpers, fixtures, selectors, and commands are reused.
- [ ] Data, time, locale, services, browser/device, and cleanup are deterministic.
- [ ] Relevant states, accessibility, console/network, and contract behavior are covered.
- [ ] Changed tests pass with first-attempt and retry status recorded.
- [ ] Unrun evidence categories and artifact limitations are explicit.

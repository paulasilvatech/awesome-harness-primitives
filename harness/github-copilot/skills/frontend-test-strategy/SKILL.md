---
name: frontend-test-strategy
description: "Select risk-based frontend test layers, environments, fixtures, acceptance coverage, and release evidence without mandating every layer. Use this skill when planning QA scope, Definition of Done, regression coverage, test data, or frontend release criteria."
---

# Frontend test strategy

Map user risk and acceptance criteria to the smallest test layers that prove behavior, then add integration or end-to-end evidence for critical boundaries.

## When to invoke

- "Create a risk-based test strategy for this frontend feature."
- "Choose unit, component, integration, E2E, visual, and manual coverage."
- "Map acceptance criteria to tests and environments."
- "Define frontend fixtures and release evidence."
- "Review whether our test pyramid fits this change."

## Procedure

1. Inventory story and acceptance IDs, changed behavior, access, money, identity, destructive actions, regulated data, contracts, devices, and traffic risk.
2. Detect existing test runners, fixtures, browser/device projects, contracts, services, CI commands, and artifact policy.
3. Read [references/test-layer-selection.md](references/test-layer-selection.md) and select only layers that prove the risks.
4. Assign stable `SC-NNN` scenarios and map every applicable acceptance ID to automated evidence or a documented manual procedure.
5. Define deterministic data, environment, browser/device, locale, timezone, feature flags, service revisions, seed, and cleanup.
6. Define flaky-test handling, artifact redaction, ownership, and release blockers.
7. Deliver [assets/test-strategy.md](assets/test-strategy.md) and [assets/traceability-matrix.md](assets/traceability-matrix.md) when the project has no equivalent.

## Layer policy

Static, unit, component, mocked integration, contract, service integration, end-to-end, visual, accessibility, performance, discoverability, and device testing are distinct evidence categories. Do not mandate every layer.

Explain why each layer is applicable or not applicable. Coverage percentages diagnose gaps but are not universal release targets.

## Repeatability and evidence

- Use synthetic or properly anonymized data.
- Freeze dates, randomness, locale, timezone, and feature flags when they affect results.
- Isolate tests from order and shared mutable state.
- Record runtime, browser, OS/device, dependency and service revisions, build ID, data fixture, first-attempt status, and retries.
- Keep screenshots, traces, videos, and network logs in test artifact storage unless policy requires committed evidence.
- Redact credentials, tokens, personal data, customer content, and private URLs.

## Limits

- Do not add a new test runner when the established tool can prove the behavior.
- Do not use retries to convert unexplained intermittent failure into a pass.
- Do not treat mocks as proof of real service compatibility.
- Do not mark a required unavailable environment as passed.

## Progressive disclosure and bundled resources

- [references/test-layer-selection.md](references/test-layer-selection.md): layer decision matrix.
- [assets/test-strategy.md](assets/test-strategy.md): fallback strategy template.
- [assets/traceability-matrix.md](assets/traceability-matrix.md): QA-oriented traceability template.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Frontend test strategy result
**Status:** ready | needs decision | blocked

### Risk and layer matrix
| Scenario | Acceptance | Risk | Layer | Environment | Reason |
| --- | --- | --- | --- | --- | --- |

### Data and repeatability
- <fixture, seed, cleanup, frozen inputs>

### Release evidence
- <required automated/manual evidence and blocker>
```

## Quality gate

- [ ] Every applicable acceptance ID maps to a scenario and evidence.
- [ ] Test layers are selected by behavior and risk, with applicability rationale.
- [ ] Data, environment, seed, cleanup, locale, time, feature flags, and revisions are reproducible.
- [ ] Mock, contract, real-service, E2E, visual, accessibility, performance, and device evidence remain distinct.
- [ ] Flaky-test and retry policy records first-attempt status and ownership.
- [ ] Evidence hygiene and unavailable required checks are explicit.

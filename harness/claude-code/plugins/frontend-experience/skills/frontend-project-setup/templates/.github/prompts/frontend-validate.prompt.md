---
name: 'frontend-validate'
description: 'Run independent risk-based frontend QA across acceptance traceability, browser behavior, visual quality, accessibility, backend integration, and release readiness.'
argument-hint: 'Provide acceptance IDs, implementation handoff, target environment, and destination.'
---

# /frontend-validate

## Objective

Independently verify an implemented frontend slice and issue an evidence-backed `Ready`, `Ready with follow-ups`, or `Blocked` verdict.

Deliver the result to `${input:destination:response, edit, or file path}`. Do not edit application source.

## When to Invoke

Run after implementation and targeted developer checks are complete, or when a frontend regression requires independent reproduction.

## Preconditions

- `${input:topic}` identifies stories, acceptance criteria, changed scope, and target environment.
- Startup, fixtures, supported browsers/devices, contracts, and known evidence gaps are available or can be inspected.
- Any edit/file destination is limited to an approved QA artifact.

If required runtime evidence cannot be produced, identify its release impact and do not infer a pass.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| QA scope | `${input:topic}` | Yes | Preserve IDs and required environments. |
| Implementation handoff | `${selection}` | No | Treat empty selection as absent; inspect changed code and tests only as needed. |
| Destination | `${input:destination:response, edit, or file path}` | Yes | Response or approved QA artifact only; never application source. |
| Startup/data/environment | Prompt/repository | Yes for runtime | Report missing prerequisites as blocked evidence. |

## What I Will Do

- Use `frontend-test-strategy`, `frontend-visual-e2e-testing`, `frontend-backend-integration`, `frontend-accessibility`, applicable mobile/desktop guidance, and `frontend-release-quality-gate`.
- Map each applicable acceptance ID to executed automated or documented manual evidence.
- Inspect representative states, boundary viewports, keyboard/focus, console, network, service, and recovery behavior.
- Record reproducible defects, first-attempt status, retries, redacted evidence, and exact retest.
- Run the deterministic traceability gate before issuing a verdict.

## What I Will NOT Do

- Fix application code while acting as independent QA.
- Treat installation, screenshots, automated accessibility, mocks, or a checklist as complete runtime proof.
- Enter real credentials, payment data, personal data, or customer content.
- Mark unavailable required evidence as passed or not applicable without evidence.

## Output Format

- **Response:** return the QA report in Chat.
- **Edit:** update only an approved QA report or traceability artifact.
- **File path:** write only the exact approved QA path.

```markdown
## Frontend Validation Result

### Environment and Risk Plan
| Build | Browser/device | State | Scenario/acceptance | Risk/layer |
| --- | --- | --- | --- | --- |

### Traceability and Results
| Story | Acceptance | Scenario | Evidence | Result |
| --- | --- | --- | --- | --- |

### Defects
| Severity | Steps | Expected | Actual | Evidence | Retest |
| --- | --- | --- | --- | --- | --- |

### Verdict
**Ready | Ready with follow-ups | Blocked**
```

## Definition of Done

- [ ] Applicable acceptance criteria map to executed or documented manual evidence.
- [ ] Environment, data, build, browser/device, viewport, locale, and services are reproducible.
- [ ] Relevant states, responsive boundaries, keyboard/focus, console/network, accessibility, and integration behavior were checked.
- [ ] Defects include severity, evidence, scope, and exact retest.
- [ ] The traceability checker passes and evidence is redacted.
- [ ] The verdict uses one exact allowed value and names every follow-up or blocker.

## Prompt Body

Validate:

- **Topic:** `${input:topic}`
- **Destination:** `${input:destination:response, edit, or file path}`
- **Selected context:**
  ```text
  ${selection}
  ```

Follow these steps in order:

1. **Validate the handoff.** Confirm IDs, scope, environments, startup, fixtures, and safety constraints.
2. **Select risk-based layers.** Explain why each static, component, contract, service, E2E, visual, accessibility, performance, discoverability, or device check applies.
3. **Execute evidence.** Run existing commands and safe runtime flows; inspect states, viewports, keyboard/focus, console, network, services, and recovery.
4. **Record traceability and defects.** Preserve first-attempt results, retries, evidence, severity, owner, and retest.
5. **Run the release gate.** Validate the machine-checkable traceability record and issue one supported verdict.

Unavailable required evidence must remain a blocker unless an accountable owner explicitly accepts the gap.

## Invocation Example

1. Select the implementation handoff and acceptance matrix.
2. Run **Chat: Run Prompt** and choose `/frontend-validate`.
3. Enter `Validate US-004 on Chromium at mobile and desktop boundaries against the local API` for `topic`.
4. Enter `response` for `destination`.
5. Verify the report cites executed evidence and no application source changed.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `frontend-qa-engineer` | agent | Owns independent evidence and verdict. |
| `frontend-release-quality-gate` | skill | Validates traceability and verdict rules. |
| `accessibility-runtime-tester` | agent | Provides deeper keyboard and focus evidence when needed. |

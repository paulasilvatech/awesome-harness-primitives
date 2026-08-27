---
name: 'frontend-build'
description: 'Implement an approved frontend slice in the repository stack with complete states, accessible behavior, focused tests, and bounded file scope.'
argument-hint: 'Provide approved story IDs, design contract, target files, and destination.'
---

# /frontend-build

## Objective

Implement the approved frontend acceptance criteria in the consuming repository's existing framework, design system, and test ecosystem.

Deliver the result to `${input:destination:response, edit, or file path}`. Workspace edits are allowed only for the approved frontend source, tests, assets, and directly required frontend configuration.

## When to Invoke

Run after stable stories, acceptance criteria, design decisions, file scope, and non-goals are available.

## Preconditions

- `${input:topic}` includes approved story/acceptance IDs and observable behavior.
- The design contract, target files, local stack, API contracts, and validation commands can be inspected.
- The selected destination authorizes the intended write scope.

If a required precondition is not met, return the exact requirement or scope gap and stop before editing.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Approved slice | `${input:topic}` | Yes | Preserve stable IDs and non-goals; stop if behavior is ambiguous. |
| Contract/context | `${selection}` | No | Treat empty selection as absent and inspect only necessary repository files. |
| Destination | `${input:destination:response, edit, or file path}` | Yes | Use `edit` for bounded implementation; use response/file only when explicitly requested. |
| Target files and validation | Prompt/repository | Yes for edits | Detect existing conventions and commands; do not invent them. |

## What I Will Do

- Detect framework, versions, routing, tokens, components, data clients, tests, and existing helpers before editing.
- Use `frontend-experience-core`, applicable domain skills, `frontend-accessibility`, `frontend-component-testing`, and `frontend-backend-integration` when services participate.
- Implement complete accepted states and typed boundaries within the approved scope.
- Run the smallest existing validation commands that prove the change.
- Produce an independent QA handoff with unverified checks.

## What I Will NOT Do

- Change product requirements, backend contracts, unrelated code, deployment infrastructure, or design-system foundations silently.
- Add or upgrade dependencies unless explicitly approved.
- Replace the established framework, component library, state library, or test runner by preference.
- Claim browser, device, visual, accessibility, or service success when those checks did not run.

## Output Format

- **Response:** provide an implementation plan or blocked handoff; do not edit.
- **Edit:** modify only approved frontend files, then report changed paths and validation.
- **File path:** write only the exact requested frontend artifact when that is the approved task.

```markdown
## Frontend Build Result

### Scope and Stack
- IDs, files, framework, versions, and non-goals

### Changes
| File | Behavior | Acceptance IDs |
| --- | --- | --- |

### State and Integration Coverage
| State/boundary | Implementation | Evidence |
| --- | --- | --- |

### Validation and QA Handoff
- Commands/results
- Startup, fixtures, viewports, risks, and unverified checks
```

## Definition of Done

- [ ] The implementation stays inside approved frontend files and behavior.
- [ ] Local framework, design-system, state, data, and test conventions are reused.
- [ ] Applicable states, controls, errors, access, cancellation, retry, and recovery are complete.
- [ ] Acceptance IDs map to focused tests or explicit manual evidence.
- [ ] Existing targeted commands pass and failures caused by the change are fixed.
- [ ] Independent QA receives reproducible startup, fixtures, risk, and evidence-gap details.

## Prompt Body

Implement:

- **Topic:** `${input:topic}`
- **Destination:** `${input:destination:response, edit, or file path}`
- **Selected context:**
  ```text
  ${selection}
  ```

Follow these steps in order:

1. **Validate the handoff.** Confirm stable IDs, approved behavior, files, non-goals, and destination. Return ambiguous requirements to design.
2. **Inspect the stack and change surface.** Detect versions, routes, components, tokens, helpers, data contracts, tests, and validation commands.
3. **Implement the smallest coherent slice.** Reuse local primitives and relevant frontend skills; preserve typed backend boundaries and complete states.
4. **Add proving tests.** Use the narrowest existing test layer for changed acceptance criteria.
5. **Validate and hand off.** Run targeted commands, inspect the diff, and report unverified runtime checks for independent QA.

Never use an attractive happy path to hide missing failure, access, or recovery behavior.

## Invocation Example

1. Select the approved design contract.
2. Run **Chat: Run Prompt** and choose `/frontend-build`.
3. Enter `Implement US-004 / AC-011 through AC-015 in src/account-recovery` for `topic`.
4. Enter `edit` for `destination`.
5. Verify only approved files changed and targeted tests ran.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `frontend-experience-engineer` | agent | Owns bounded implementation and QA handoff. |
| `frontend-component-testing` | skill | Supplies focused component evidence. |
| `frontend-backend-integration` | skill | Supplies service and contract boundary evidence. |

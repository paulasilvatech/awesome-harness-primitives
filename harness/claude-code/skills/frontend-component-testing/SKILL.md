---
name: frontend-component-testing
description: >-
  Create or review focused frontend tests for components, hooks, composables, stores, validation,
  state machines, callbacks, and Storybook interactions using the repository's existing runner.
  Use this skill when isolated UI behavior and semantics need executable evidence.
---

<!-- Generated from harness/github-copilot/skills/frontend-component-testing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend component testing

Prove user-visible component behavior and state transitions through the consuming repository's established test tools and conventions.

## When to invoke

- "Write component tests for this React or Vue component."
- "Test this hook, composable, store, validator, or state machine."
- "Add Storybook interaction coverage for these states."
- "Review selectors and assertions in this UI test."
- "Test loading, empty, error, and permission states in isolation."

## Procedure

1. Detect the framework, versions, runner, DOM/native environment, Testing Library or framework utilities, Storybook, fixtures, and local test conventions.
2. Read [references/component-contracts.md](references/component-contracts.md) and map the changed acceptance IDs to render, interaction, semantics, callbacks, and state.
3. Use [references/react-testing.md](references/react-testing.md) or [references/vue-testing.md](references/vue-testing.md) only when that adapter matches the repository.
4. Reuse existing render helpers, providers, factories, mocks, fake timers, and cleanup.
5. Prefer roles, labels, visible names, state, and user-visible outcomes over DOM structure or implementation detail.
6. Execute the narrowest existing command for the changed tests and fix failures caused by the change.

## Test contract

- Test behavior and semantics, not CSS class chains, internal state, hook order, or component implementation.
- Include relevant initial, loading, empty, partial, success, invalid, error, disabled, access, and recovery states.
- Use controlled time and async behavior; prefer user-event and web-first waits over sleeps.
- Mock at owned boundaries. Do not mock the behavior under test.
- Verify callbacks, navigation, state transitions, announcements, and focus when they are observable contract.

## Limits

- Do not add or replace a test runner without approval.
- Do not use React guidance for Vue or vice versa.
- Do not treat component tests as proof of real browser layout, network, backend, or device behavior.
- Do not add test IDs when accessible selectors or established project conventions suffice.

## Progressive disclosure and bundled resources

- [references/component-contracts.md](references/component-contracts.md): behavior and state selection.
- [references/react-testing.md](references/react-testing.md): React adapter.
- [references/vue-testing.md](references/vue-testing.md): Vue adapter.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Component testing result
**Status:** passed | blocked
**Framework/runner:** <detected versions>

### Coverage
| Acceptance/state | Test | Observable assertions |
| --- | --- | --- |

### Execution
- Command:
- Result:
- Remaining browser/integration evidence:
```

## Quality gate

- [ ] Framework, versions, runner, helpers, and conventions were detected.
- [ ] Tests map to acceptance IDs and observable component contracts.
- [ ] Selectors prefer roles, labels, names, text, or established stable IDs.
- [ ] Async behavior uses deterministic events and assertions rather than sleeps.
- [ ] Relevant states, semantics, focus, announcements, and callbacks are covered.
- [ ] The changed tests ran; unproven browser, service, and device behavior is explicit.

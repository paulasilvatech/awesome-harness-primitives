---
name: react18-lifecycle-patterns
description: >-
  Migrate unsafe React class component lifecycle methods to React 18.3.1-safe patterns. Use when
  fixing `componentWillMount`, `componentWillReceiveProps`, `componentWillUpdate`, `UNSAFE_`
  lifecycle warnings, choosing `getDerivedStateFromProps` versus `componentDidUpdate`, or adding
  `getSnapshotBeforeUpdate`.
---

<!-- Generated from harness/github-copilot/plugins/react18-upgrade/skills/react18-lifecycle-patterns/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# React 18 lifecycle patterns

Classify the semantics of unsafe class lifecycle methods before changing code, then apply the matching React 18.3.1 migration pattern from the bundled references.

## When to invoke

- "Migrate `componentWillMount` in this component."
- "Fix React 18 UNSAFE lifecycle warnings."
- "Should this use `getDerivedStateFromProps` or `componentDidUpdate`?"
- "Add `getSnapshotBeforeUpdate` for scroll position."
- "Replace `componentWillReceiveProps` safely."

## Procedure

1. Identify which unsafe lifecycle appears: `componentWillMount`, `componentWillReceiveProps`, or `componentWillUpdate`.
2. Classify what the method does semantically before editing.
3. Read the matching bundled reference file and case section.
4. Apply the before/after pattern exactly enough to preserve behavior.
5. Avoid permanent `UNSAFE_` prefixes; if a temporary prefix is unavoidable, add the required TODO.
6. Validate behavior with existing React tests or targeted component checks.

## Quick decision guide

### componentWillMount

| What it does | Correct migration | Reference |
| --- | --- | --- |
| Sets initial state with `this.setState(...)` | Move to `constructor`. | `references/componentWillMount.md#case-a` |
| Runs a side effect such as fetch, subscription, or DOM access | Move to `componentDidMount`. | `references/componentWillMount.md#case-b` |
| Derives initial state from props | Move to `constructor` with props. | `references/componentWillMount.md#case-c` |

### componentWillReceiveProps

| What it does | Correct migration | Reference |
| --- | --- | --- |
| Async side effect triggered by prop change, such as fetch or cancel | Use `componentDidUpdate` with previous-prop comparison. | `references/componentWillReceiveProps.md#case-a` |
| Pure state derivation from new props with no side effects | Use `getDerivedStateFromProps`. | `references/componentWillReceiveProps.md#case-b` |

### componentWillUpdate

| What it does | Correct migration | Reference |
| --- | --- | --- |
| Reads DOM state before update, such as scroll, size, or position | Use `getSnapshotBeforeUpdate` and consume the snapshot in `componentDidUpdate`. | `references/componentWillUpdate.md#case-a` |
| Cancels requests or runs effects before update | Use `componentDidUpdate` with previous-value comparison. | `references/componentWillUpdate.md#case-b` |

## UNSAFE prefix rule

Never use `UNSAFE_componentWillMount`, `UNSAFE_componentWillReceiveProps`, or `UNSAFE_componentWillUpdate` as a permanent fix. Prefixing suppresses React 18.3.1 warnings but does not fix concurrent mode safety issues, does not prepare for React 19 removal, and does not address the semantic migration.

If a temporary prefix is explicitly chosen as a stopgap, mark it with this exact intent:

```jsx
// TODO: React 19 will remove this. Migrate before React 19 upgrade.
// UNSAFE_ prefix added temporarily - replace with componentDidMount / getDerivedStateFromProps / etc.
```

## Progressive disclosure and bundled resources

- `references/componentWillMount.md`: three cases for initial state, side effects, and props-derived initial state.
- `references/componentWillReceiveProps.md`: `componentDidUpdate` versus `getDerivedStateFromProps`, including trap warnings.
- `references/componentWillUpdate.md`: `getSnapshotBeforeUpdate` plus `componentDidUpdate` pairing.

## Gotchas

- **Wrong category means wrong migration**: a side effect in `componentWillReceiveProps` belongs in `componentDidUpdate`, not `getDerivedStateFromProps`.
- **`getSnapshotBeforeUpdate` is paired**: DOM snapshots are returned before commit and consumed in `componentDidUpdate`.
- **`UNSAFE_` is not a migration**: treat it only as a temporary scheduling marker.

## Output template

```markdown
## React lifecycle migration

**Status:** complete | needs changes | blocked
**Component:** `<component name or path>`
**Original lifecycle:** `componentWillMount` | `componentWillReceiveProps` | `componentWillUpdate`
**Migration pattern:** `constructor` | `componentDidMount` | `componentDidUpdate` | `getDerivedStateFromProps` | `getSnapshotBeforeUpdate`

| Behavior found | Pattern applied | Reference | Validation |
| --- | --- | --- | --- |
| <state, side effect, DOM read, or cancel> | <new lifecycle/API> | `references/<file>.md#case-x` | <test/check> |
```

## Quality gate

- [ ] The original lifecycle method and semantic category were identified before editing.
- [ ] The matching bundled reference file was consulted.
- [ ] `componentWillMount`, `componentWillReceiveProps`, and `componentWillUpdate` are removed or explicitly justified as temporary `UNSAFE_` stopgaps.
- [ ] `getDerivedStateFromProps` is used only for pure state derivation from props.
- [ ] DOM reads before update use `getSnapshotBeforeUpdate` with `componentDidUpdate`.
- [ ] Existing tests or targeted checks validate preserved behavior.

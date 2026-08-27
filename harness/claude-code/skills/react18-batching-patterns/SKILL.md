---
name: react18-batching-patterns
description: >-
  Diagnose and fix React 18 automatic batching regressions in class components. Use when multiple
  setState calls occur after await, inside setTimeout, Promise .then() or .catch(), native
  addEventListener callbacks, or when tests fail because they assert intermediate state after a
  React 18 upgrade.
---

<!-- Generated from harness/github-copilot/skills/react18-batching-patterns/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# React 18 automatic batching patterns

Classify React 18 batching regressions, choose refactor versus `flushSync`, and update tests so class components no longer depend on React 17 intermediate renders in class-component `async/await` flows.

## When to invoke

- "Fix this React 18 batching regression in a class component."
- "This async method calls setState twice and reads this.state after await."
- "Should I use flushSync here?"
- "Our React 18 tests fail because intermediate state no longer renders."
- "Multiple setState calls in setTimeout or Promise .then() behave differently after upgrade."

## Batching change matrix

| Location of `setState` | React 17 behavior | React 18 behavior | Review action |
| --- | --- | --- | --- |
| React event handler | Batched | Batched | Usually no change. |
| `setTimeout` | Immediate re-render | Batched | Check for code or tests that expect intermediate state. |
| `Promise .then()` / `Promise .catch()` | Immediate re-render | Batched | Refactor state reads and assertions. |
| `async` / `await` continuation | Immediate re-render | Batched | Treat `this.state` reads after `await` as high-risk. |
| Native `addEventListener` callback | Immediate re-render | Batched | Use React state rules even outside React synthetic events. |

`Batched` means all `setState` calls in that execution context flush together in one render at the end; no intermediate render is visible.

## Diagnosis categories

| Category | Signal | Default fix | Read next |
| --- | --- | --- | --- |
| A: silent state-read bug | Code reads `this.state` after `await`, `setTimeout`, or a Promise callback and uses it for a decision. | Compute the next value locally, use functional `setState`, or move dependent work into the callback. | `references/batching-categories.md` |
| B: refactor, no `flushSync` | Intermediate render is not user-visible; only code structure or tests assume React 17 timing. | Collapse updates, assert final state, and remove timing assumptions. | `references/batching-categories.md` |
| C: `flushSync` justified | User must see a loading/spinner/progress state, including a spinner/loading transition, before expensive sync work or an async operation begins. | Wrap only the minimum state update in `flushSync`. | `references/flushSync-guide.md` |

## flushSync decision rule

Use `flushSync` sparingly. It forces a synchronous render and bypasses React 18's concurrent scheduler, so overuse removes the performance benefit of automatic batching.

| Use `flushSync` only when | Do not use `flushSync` when |
| --- | --- |
| A spinner or loading state must render before a fetch or expensive operation starts. | The next line merely needs a value; store it in a local variable instead. |
| Sequential UI steps must be visibly distinct, such as a progress wizard or multi-step flow. | A test asserts an intermediate render that users cannot observe. |
| Browser measurement must happen after a specific state update reaches the DOM. | Multiple state updates can be represented as one final state. |

## Progressive disclosure and bundled resources

- `references/batching-categories.md`: Category A, B, and C explanations with full before/after code.
- `references/flushSync-guide.md`: `flushSync` import syntax, permitted use cases, and anti-patterns.

Read these references only when the active file matches the category or the user is about to add `flushSync`.

## Output template

```markdown
## React 18 batching result - <component or file>

**Status:** fixed | recommendation only | blocked
**Category:** A state-read bug | B refactor/no flushSync | C flushSync justified

| Evidence | Decision | Change |
| --- | --- | --- |
| `<setState location and state read>` | `<why React 18 batching matters>` | `<refactor, test update, or flushSync>` |

### Validation
- Tests run: `<command or not run>`
- Intermediate state dependency removed or justified: `<yes/no>`
- `flushSync` used: `<no or minimal location and reason>`
```

## Quality gate

- [ ] Every async class method and callback with multiple `setState` calls was classified as Category A, B, or C.
- [ ] Code after `await` was checked for `this.state` reads that drive decisions.
- [ ] `flushSync` was not used unless an intermediate UI state, spinner, progress step, or DOM measurement truly requires a synchronous render.
- [ ] Tests assert user-observable final behavior unless an intermediate state is deliberately visible.
- [ ] The relevant bundled reference was read when adding or rejecting `flushSync`.

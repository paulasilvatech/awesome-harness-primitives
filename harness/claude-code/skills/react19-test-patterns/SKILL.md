---
name: react19-test-patterns
description: >-
  Provide before-and-after migration patterns for React 19 test compatibility, including act()
  imports, react-dom/test-utils removal, Simulate to fireEvent conversion, StrictMode call count
  changes, async act warnings, and custom render helper checks. Use when updating React test files
  for React 19.
---

<!-- Generated from harness/github-copilot/skills/react19-test-patterns/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# React 19 test migration patterns

Convert React test files to React 19-compatible APIs in dependency order, preserving test intent while replacing removed `react-dom/test-utils` patterns and measuring StrictMode behavior instead of guessing call counts.

## When to invoke

- "Migrate these tests for React 19."
- "Replace react-dom/test-utils imports in my test files."
- "Convert Simulate calls to Testing Library fireEvent."
- "Fix React 19 StrictMode call count failures."
- "Resolve not wrapped in act warnings after the React 19 upgrade."

## Procedure

Fix test files in this order because each layer unblocks the next:

1. Fix `act` imports first.
2. Replace `Simulate` with `fireEvent`.
3. Remove all remaining `react-dom/test-utils` imports.
4. Measure and update StrictMode call counts.
5. Add async `act` or `await` only for remaining warnings.
6. Verify the custom render helper once per codebase, not separately in every test.

## API migration map

| Old `react-dom/test-utils` API | React 19-compatible replacement | Notes |
| --- | --- | --- |
| `act` | `import { act } from 'react'` | Fix this before other test-utils cleanup. |
| `Simulate` | `fireEvent` from `@testing-harness/github-copilot/react` | Keep event payloads such as `{ target: { value: 'hello' } }`. |
| `renderIntoDocument` | `render` from `@testing-harness/github-copilot/react` | Prefer queries from the returned render result. |
| `findRenderedDOMComponentWithTag` | `getByRole`, `getByTestId` from RTL | Prefer accessible role queries. |
| `findRenderedDOMComponentWithClass` | `getByRole` or `container.querySelector` | Use class selectors only when no accessible query exists. |
| `scryRenderedDOMComponentsWithTag` | `getAllByRole` from RTL | Assert count and accessible names where possible. |
| `isElement` | Remove | RTL tests should assert user-visible behavior. |
| `isCompositeComponent` | Remove | Avoid implementation-detail assertions. |
| `isDOMComponent` | Remove | Assert DOM output or accessible behavior instead. |

## `before/after` patterns

### `act()` import

```jsx
// Before: `REMOVED` in React 19
import { act } from 'react-dom/test-utils';

// After
import { act } from 'react';
```

When mixed with other test-utils imports, split the imports and replace the removed helpers:

```jsx
// Before
import { act, Simulate, renderIntoDocument } from 'react-dom/test-utils';

// After
import { act } from 'react';
import { fireEvent, render } from '@testing-harness/github-copilot/react';
```

### `Simulate` to `fireEvent`

```jsx
// Before: Simulate is removed in React 19
import { Simulate } from 'react-dom/test-utils';
Simulate.click(element);
Simulate.change(input, { target: { value: 'hello' } });
Simulate.submit(form);
Simulate.keyDown(element, { key: 'Enter', keyCode: 13 });

// After
import { fireEvent } from '@testing-harness/github-copilot/react';
fireEvent.click(element);
fireEvent.change(input, { target: { value: 'hello' } });
fireEvent.submit(form);
fireEvent.keyDown(element, { key: 'Enter', keyCode: 13 });
```

### StrictMode call counts

React 19 StrictMode no longer `double-invoke`s `useEffect` in development, but render-phase calls such as component body spies can still be double-invoked. Measure actual failures.

```bash
npm test -- --watchAll=false --testPathPattern="[filename]" --forceExit 2>&1 | grep -E "Expected|Received"
```

```jsx
// Before: React 18 StrictMode effects ran twice
expect(mockFn).toHaveBeenCalledTimes(2);

// After: React 19 StrictMode effects run once
expect(mockFn).toHaveBeenCalledTimes(1);

// Render-phase calls can still be double-invoked
expect(renderSpy).toHaveBeenCalledTimes(2);
```

## Gotchas

- **Measure StrictMode counts**: do not globally replace `2` with `1`; effect calls and render-phase calls differ.
- **Do not leave partial test-utils imports**: any remaining `react-dom/test-utils` import can hide removed APIs.
- **Prefer user-event for user flows**: use `fireEvent` for direct mechanical replacement, but preserve existing higher-level `userEvent` patterns when present.
- **Async warnings often need awaited user actions**: after upgrading `@testing-harness/github-copilot/user-event`, many calls require `await` before assertions.


- **StrictMode wording matters**: React 18 `double-invokes` effects; React 19 changes effect behavior but can still double-invoke render-phase work.

## Output template

```markdown
## React 19 test migration result

**Status:** migrated | changes required | blocked
**Files reviewed:** <test files>
**Primary pattern:** act import | Simulate removal | test-utils cleanup | StrictMode counts | async act

| File | Old API or failure | Change made | Validation |
| --- | --- | --- | --- |
| `<test file>` | `<old pattern>` | `<new pattern>` | `<test command/result>` |
```

## Quality gate

- [ ] `act` imports come from `react`, not `react-dom/test-utils`.
- [ ] `Simulate` calls are replaced with `fireEvent` or an existing `userEvent` pattern.
- [ ] No remaining `react-dom/test-utils` imports exist in migrated files.
- [ ] StrictMode call counts are based on observed test output, not guessing.
- [ ] Async user interactions and act warnings are awaited or wrapped correctly.
- [ ] The output follows `## Output template` exactly.

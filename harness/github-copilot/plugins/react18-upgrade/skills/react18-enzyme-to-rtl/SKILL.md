---
name: react18-enzyme-to-rtl
description: >-
  Rewrite Enzyme tests for React 18 into React Testing Library behavior tests. Use when a test imports enzyme, uses shallow, mount, wrapper.find(), wrapper.simulate(), wrapper.prop(), wrapper.state(), wrapper.instance(), Enzyme configure/Adapter, or needs React 18-compatible RTL migration patterns.
---

# React 18 Enzyme to RTL migration

Migrate unsupported Enzyme tests to React Testing Library by replacing implementation assertions with user-visible behavior, accessible queries, provider-aware renders, and async-safe interactions.

## When to invoke

- "Rewrite this Enzyme test for React 18."
- "Migrate shallow and mount tests to React Testing Library."
- "Replace wrapper.find() and simulate() in this test."
- "This file imports enzyme and blocks our React 18 upgrade."
- "Convert wrapper.state(), wrapper.prop(), or wrapper.instance() assertions."

## Prerequisites and context

- Enzyme has no React 18 adapter and no supported React 18 migration path.
- Use React Testing Library imports such as `render`, `screen`, `fireEvent`, and `waitFor` from `@testing-harness/github-copilot/react`.
- Prefer `userEvent` from `@testing-harness/github-copilot/user-event` for real user interactions.
- Use project-specific `customRender` helpers when they already wrap providers.

## Philosophy shift

Enzyme tests component internals; RTL tests observable behavior. Do not translate APIs 1:1.

| Enzyme habit | Why it fails in RTL | Replacement mindset |
| --- | --- | --- |
| `wrapper.state('count')` | RTL does not expose component state. | Assert visible count, enabled state, submitted text, or emitted output. |
| `wrapper.instance().handleClick` | Function components have no instance and internals are not user behavior. | Click the control and assert the result. |
| `wrapper.find('Button').prop('disabled')` | Props are implementation details. | Query by role and assert `toBeDisabled()`. |
| `shallow(<Component />)` | Shallow rendering hides integrated behavior. | Render the component with required providers and assert user-visible output. |

```jsx
// Enzyme: tests internals
expect(wrapper.state('count')).toBe(3);
expect(wrapper.instance().handleClick).toBeDefined();
expect(wrapper.find('Button').prop('disabled')).toBe(true);

// RTL: tests behavior
expect(screen.getByText('Count: 3')).toBeInTheDocument();
expect(screen.getByRole('button', { name: /submit/i })).toBeDisabled();
```

## Core rewrite template

```jsx
import { render, screen, fireEvent, waitFor } from '@testing-harness/github-copilot/react';
import userEvent from '@testing-harness/github-copilot/user-event';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  it('does the thing', async () => {
    render(<MyComponent prop="value" />);

    const button = screen.getByRole('button', { name: /submit/i });
    await userEvent.setup().click(button);

    expect(screen.getByText('Submitted!')).toBeInTheDocument();
  });
});
```

## API migration map

Read `references/enzyme-api-map.md` for full before/after examples covering `shallow`, `mount`, `find`, `simulate`, `prop`, `state`, `instance`, `configure`, and `Adapter` setup.

| Enzyme API | RTL direction |
| --- | --- |
| `shallow(<Component />)` | `render(<Component />)` with dependencies mocked only at module boundaries. |
| `mount(<Component />)` | `render(<Component />)` wrapped in required providers. |
| `wrapper.find(selector)` | `screen.getByRole`, `getByLabelText`, `getByText`, or another user-facing query. |
| `wrapper.simulate('click')` | `await userEvent.setup().click(element)`; use `fireEvent` for low-level events only. |
| `wrapper.prop('x')` | Assert visible output or child behavior caused by the prop. |
| `wrapper.state('x')` | Assert the DOM, callback, network mock, or side effect that reflects the state. |
| `wrapper.instance()` | Remove direct instance testing; exercise the public UI. |
| `Enzyme.configure({ adapter })` | Delete Enzyme setup and use RTL/Jest setup such as `@testing-harness/github-copilot/jest-dom`. |

## RTL query priority

Use queries in this order; `getByTestId` is the last resort.

1. `getByRole` for accessible roles such as button, textbox, heading, checkbox.
2. `getByLabelText` for form fields linked to labels.
3. `getByPlaceholderText` for input placeholders.
4. `getByText` for visible text content.
5. `getByDisplayValue` for current `input`, `select`, or `textarea` value.
6. `getByAltText` for image alt text.
7. `getByTitle` for title attributes.
8. `getByTestId` for `data-testid` only when accessible queries cannot express the behavior.

## Providers and async behavior

```jsx
// Enzyme with context
const wrapper = mount(
  <ApolloProvider client={client}>
    <ThemeProvider theme={theme}>
      <MyComponent />
    </ThemeProvider>
  </ApolloProvider>
);

// RTL equivalent
render(
  <MockedProvider mocks={mocks} addTypename={false}>
    <ThemeProvider theme={theme}>
      <MyComponent />
    </ThemeProvider>
  </MockedProvider>
);
```

Use the project's custom render helper if it wraps `MockedProvider`, `ThemeProvider`, routing, store, or i18n context. Read `references/async-patterns.md` for `waitFor`, `findBy`, `act()`, Apollo `MockedProvider`, loading states, and error states.

## Criteria

- [ ] Replace every Enzyme import and adapter setup; no test file still imports `enzyme`.
- [ ] Rewrite internal state, instance, and prop assertions as visible behavior or observable side effects.
- [ ] Prefer accessible RTL queries over selectors and `data-testid`.
- [ ] Use `userEvent` for user interactions and await async interactions.
- [ ] Preserve provider context through project `customRender` or inline wrappers.
- [ ] Cover loading, success, and error states where the Enzyme test previously relied on implementation timing.

## Gotchas

- **No 1:1 translation**: replacing `wrapper.find()` with `container.querySelector()` preserves brittle implementation testing.
- **Do not assert child props directly**: mock the child only when the child is an external boundary; otherwise assert what the user sees.
- **Use `findBy` or `waitFor` for async UI**: immediate `getBy*` assertions can race React 18 updates.
- **Delete Enzyme configure/Adapter calls**: keeping them can hide migration incompleteness.

## Progressive disclosure and bundled resources

- `references/enzyme-api-map.md`: complete Enzyme API mapping for `shallow`, `mount`, `find`, `simulate`, `prop`, `state`, `instance`, `configure`, and `Adapter`.
- `references/async-patterns.md`: async RTL patterns for `waitFor`, `findBy`, `act()`, Apollo `MockedProvider`, loading states, and error states.

## Migration shorthand

Treat `shallow/mount` as the signal to rewrite render strategy. Use `getByDisplayValue` for current `input/select/textarea` values.

## Output template

```markdown
## Enzyme to RTL migration result

**Status:** complete | partial | blocked
**Files changed:** <count>
**React 18 readiness:** pass | fail

| File | Enzyme APIs removed | RTL patterns used | Remaining blockers |
| --- | --- | --- | --- |
| `<test file>` | `shallow`, `wrapper.find()` | `render`, `screen.getByRole`, `userEvent` | <none or blocker> |

### Validation
- Enzyme imports removed: pass | fail
- Targeted test command: pass | fail | not run (<reason>)
```

## Quality gate

- [ ] No migrated file imports `enzyme` or configures an Enzyme `Adapter`.
- [ ] `shallow`, `mount`, `wrapper.find()`, `wrapper.simulate()`, `wrapper.prop()`, `wrapper.state()`, and `wrapper.instance()` are removed or explicitly reported as remaining blockers.
- [ ] Assertions target user-visible DOM, accessibility state, callbacks, or externally observable effects.
- [ ] Query priority favors `getByRole` and avoids `getByTestId` unless justified.
- [ ] Async behavior uses `findBy`, `waitFor`, or awaited `userEvent` as appropriate.
- [ ] Provider context is preserved with `customRender` or equivalent wrappers.
- [ ] Targeted tests were run or a concrete blocker is reported.

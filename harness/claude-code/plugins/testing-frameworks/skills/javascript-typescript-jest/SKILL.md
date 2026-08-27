---
name: javascript-typescript-jest
description: >-
  Write and review JavaScript and TypeScript Jest tests with strong structure, mocks, async
  handling, snapshots, and React Testing Library patterns. Use this skill when the user asks to
  add Jest tests, improve test structure, mock APIs or databases, test async code, update
  snapshots, or test React components.
---

<!-- Generated from harness/github-copilot/plugins/testing-frameworks/skills/javascript-typescript-jest/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# JavaScript TypeScript Jest

Write focused JavaScript and TypeScript Jest tests by selecting file placement, isolation boundaries, matcher style, async handling, and React Testing Library queries, then return a runnable test plan or test implementation summary.

Use this for JavaScript/TypeScript test work where Jest is the runner.

## When to invoke

- "Add Jest tests for this TypeScript module."
- "How should I mock this API in Jest?"
- "Review this test structure and matchers."
- "Fix this async Jest test."
- "Write React component tests with Testing Library."

## Test placement and structure

| Concern | Rule | Example |
| --- | --- | --- |
| File names | Name test files with `.test.ts` or `.test.js` suffix. Use `.test.tsx` or `.test.jsx` for JSX when the project uses those extensions. | `calculator.test.ts`, `SearchBox.test.tsx` |
| Location | Place tests next to the code they test or in a dedicated `__tests__` directory; follow the repository's existing convention. | `src/foo.test.ts` or `src/__tests__/foo.test.ts` |
| Names | Use descriptive test names that explain expected behavior, not implementation mechanics. | `it('returns an empty list when the API has no results', ...)` |
| Grouping | Use nested `describe` blocks only when they add signal around a component, function, class, method, or state. | `describe('UserService', () => { describe('createUser', () => { ... }) })` |
| Shape | Follow `describe('Component/Function/Class', () => { it('should do something', () => {}) })` when no local style is stronger. | Keep setup near the assertions it supports. |

Prefer arrange-act-assert within each test. Keep one behavioral reason to fail per test; split tests when the assertion list starts describing multiple scenarios.

## Mocking and isolation

| Need | Jest primitive | Guidance |
| --- | --- | --- |
| Replace a module for the whole file | `jest.mock()` | Mock external dependencies such as APIs, databases, queues, file systems, clocks, and network clients to isolate the unit under test. |
| Observe or override one exported function or object method | `jest.spyOn()` | Restore spies after the test, especially for globals such as `Date`, `console`, `fetch`, or `Math.random`. |
| Define dynamic behavior | `mockImplementation()` | Use when return values depend on arguments or call order. |
| Define a simple fixed value | `mockReturnValue()` | Use for deterministic sync collaborators. |
| Reset cross-test state | `jest.resetAllMocks()` in `afterEach` | Reset mocks between tests when implementations or call histories are test-specific. Use `jest.clearAllMocks()` when implementations should remain but call counts should reset. |

Mock at the boundary you own. Do not mock the function under test. If a mock becomes more complex than the behavior it replaces, prefer an in-memory fake or a higher-level integration test.

Treat `jest.mock()` as the module-level replacement tool; use narrower spies only when the real module should remain loaded.

## Async code and timers

| Pattern | Correct test style | Failure to avoid |
| --- | --- | --- |
| Promise resolves | `await expect(promise).resolves.toEqual(value)` | Missing `return` or `await`, which lets the test pass before the promise settles. |
| Promise rejects | `await expect(promise).rejects.toThrow(Error)` | Wrapping an async call in `expect(() => asyncFn()).toThrow()`. |
| Async arrange/act | `const result = await subject()` | Mixing `done` callbacks with promises unless testing callback APIs. |
| Slow integration path | `jest.setTimeout(ms)` | Raising timeouts for unit tests instead of removing real I/O. |
| Timers | Use fake timers only when the behavior depends on time. | Forgetting to advance timers and flush pending promises. |

Always return promises or use async/await syntax in tests. A test that schedules work without awaiting it is not testing the scheduled behavior.

Use `jest.setTimeout()` deliberately and document why the test is legitimately slow.

## Snapshots and React components

- Use snapshot tests for UI components or complex objects that change infrequently and are hard to assert field-by-field.
- Keep snapshots small and focused; avoid snapshotting entire application trees.
- Review snapshot changes carefully before committing; a snapshot update is an assertion change.
- Use React Testing Library over Enzyme for testing components.
- Test user behavior and component accessibility instead of component internals.
- Query elements by accessibility roles, labels, or text content before falling back to test IDs.
- Use `userEvent` over `fireEvent` for realistic user interactions.

## Common Jest matchers

| Category | Matchers |
| --- | --- |
| Basic identity and equality | `expect(value).toBe(expected)`, `expect(value).toEqual(expected)` |
| Truthiness | `expect(value).toBeTruthy()`, `expect(value).toBeFalsy()` |
| Numbers | `expect(value).toBeGreaterThan(3)`, `expect(value).toBeLessThanOrEqual(3)` |
| Strings | `expect(value).toMatch(/pattern/)`, `expect(value).toContain('substring')` |
| Arrays | `expect(array).toContain(item)`, `expect(array).toHaveLength(3)` |
| Objects | `expect(object).toHaveProperty('key', value)` |
| Exceptions | `expect(fn).toThrow()`, `expect(fn).toThrow(Error)` |
| Mock functions | `expect(mockFn).toHaveBeenCalled()`, `expect(mockFn).toHaveBeenCalledWith(arg1, arg2)` |

## Output template

```markdown
## Jest test result

**Status:** implemented | reviewed | blocked
**Target:** `<file, component, function, or class>`

| Area | Decision | Evidence |
| --- | --- | --- |
| Structure | `<placement and describe/it shape>` | `<test path or planned path>` |
| Mocking | `<jest.mock / jest.spyOn / fake / none>` | `<dependency boundary>` |
| Async | `<await/resolves/rejects/timers/not applicable>` | `<specific behavior>` |
| Assertions | `<matcher choices>` | `<key expectations>` |

**Validation**
- `<test command>`: pass | fail | not run
```

## Quality gate

- [ ] Test files use the repository's placement convention and a valid `.test.ts`, `.test.js`, `.test.tsx`, or `.test.jsx` suffix.
- [ ] Test names describe observable behavior.
- [ ] External dependencies are mocked or faked at the boundary, not inside the subject.
- [ ] Mocks are reset, cleared, or restored between tests according to how they are configured.
- [ ] Promise-based behavior is returned or awaited, including `resolves` and `rejects` assertions.
- [ ] Snapshot tests are small, intentional, and reviewed as assertion changes.
- [ ] React component tests prefer React Testing Library, accessible queries, and `userEvent`.
- [ ] The output reports the command run or states why validation was not run.

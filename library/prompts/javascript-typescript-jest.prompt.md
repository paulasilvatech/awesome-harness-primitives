---
name: 'javascript-typescript-jest'
description: 'Guide JavaScript and TypeScript Jest testing with structure, mocking, async, snapshot, React component, and matcher practices.'
---

# /javascript-typescript-jest

## Objective

Guide JavaScript and TypeScript Jest test creation or review so tests are well named, organized, isolated with appropriate mocks, reliable for async code, careful with snapshots, user-focused for React components, and written with precise Jest matchers.

## When to Invoke

Use this prompt when adding, refactoring, or reviewing Jest tests for JavaScript, TypeScript, Node.js, React, functions, classes, modules, components, or selected code.

## Preconditions

- The code under test or existing Jest test file is available.
- The project uses or intends to use Jest for JavaScript or TypeScript tests.
- React Testing Library is available or preferred when testing React components.
- Test edits are permitted when implementation is requested.

## Inputs the Team Must Provide

- `target` — the function, class, module, component, selected code, or test file.
- Test scope — unit, component, integration-like, or review-only.
- Existing test command and project conventions for test locations.
- Required edge cases, async behavior, mocked dependencies, and snapshot expectations.
- Ask the user for anything that is missing, especially target and test scope.

## What I Will Do

- Name test files with `.test.ts` or `.test.js` and place them next to the code or in `__tests__` according to project convention.
- Use descriptive `describe` and `it` names and nested describe blocks for related behavior.
- Mock external dependencies with `jest.mock()`, `jest.spyOn()`, `mockImplementation()`, `mockReturnValue()`, and `jest.resetAllMocks()` in `afterEach` where needed.
- Use async/await, returned promises, `resolves`, `rejects`, and `jest.setTimeout()` appropriately.
- Use snapshots sparingly, React Testing Library over Enzyme, accessible queries, `userEvent`, and precise matchers.

## What I Will NOT Do

- Test implementation details when observable behavior, public APIs, or user interactions can be tested.
- Leave mocks leaking between tests or rely on test execution order.
- Use broad snapshots for frequently changing output without explaining the review burden.
- Use Enzyme for new React tests when React Testing Library is available and suitable.
- Mark tests passing without running the relevant command or reporting why it was not run.

## Output Format

Return or apply the Jest changes with this structure:

```markdown
### Jest Test Result

### Target
- `<function, component, module, or test file>`

### Tests Added or Updated
- `describe('Component/Function/Class', () => { it('should do something', () => {}) })`
- `<test name>`

### Practices Applied
- Test files use `.test.ts` or `.test.js` and the repository location convention.
- Mocks use `jest.mock()`, `jest.spyOn()`, `mockImplementation()`, or `mockReturnValue()` with `jest.resetAllMocks()` in `afterEach`.
- Async code uses async/await, returned promises, `resolves`, `rejects`, or `jest.setTimeout()` when appropriate.
- React tests use React Testing Library, accessibility roles, labels, text content, and `userEvent` instead of `fireEvent` where realistic interaction matters.
- Snapshot tests are small, focused, and reviewed deliberately.

### Matcher Examples Used
- Basic: `expect(value).toBe(expected)`, `expect(value).toEqual(expected)`
- Truthiness: `expect(value).toBeTruthy()`, `expect(value).toBeFalsy()`
- Numbers: `expect(value).toBeGreaterThan(3)`, `expect(value).toBeLessThanOrEqual(3)`
- Strings: `expect(value).toMatch(/pattern/)`, `expect(value).toContain('substring')`
- Arrays: `expect(array).toContain(item)`, `expect(array).toHaveLength(3)`
- Objects: `expect(object).toHaveProperty('key', value)`
- Exceptions: `expect(fn).toThrow()`, `expect(fn).toThrow(Error)`
- Mock functions: `expect(mockFn).toHaveBeenCalled()`, `expect(mockFn).toHaveBeenCalledWith(arg1, arg2)`

### Validation
- Command: `<npm test, jest target, or not run>`
- Result: `<passed, failed, or not run with reason>`
```

## Definition of Done

- [ ] Tests are named, located, and grouped according to project conventions.
- [ ] Mocks isolate external dependencies and reset between tests.
- [ ] Async behavior is tested with reliable promise handling.
- [ ] Snapshots are small and justified, or avoided when explicit assertions are clearer.
- [ ] React tests focus on user behavior and accessibility.
- [ ] Validation evidence or a precise not-run reason is reported.

## Prompt Body

Follow these steps in order. Preserve existing project test style unless it creates unreliable tests.

**Step 1 — Identify the target and test location.** Determine whether the target is JavaScript or TypeScript and whether tests belong next to the code or in a dedicated `__tests__` directory. Use `.test.ts` or `.test.js` suffixes.

**Step 2 — Structure the suite.** Use descriptive names that explain expected behavior. Use nested describe blocks to organize related tests. Follow the pattern `describe('Component/Function/Class', () => { it('should do something', () => {}) })`.

**Step 3 — Mock external dependencies.** Mock APIs, databases, and other external dependencies to isolate tests. Use `jest.mock()` for module-level mocks, `jest.spyOn()` for specific functions, `mockImplementation()` or `mockReturnValue()` to define behavior, and `jest.resetAllMocks()` in `afterEach` to reset mocks between tests.

**Step 4 — Test async code reliably.** Always return promises or use async/await in tests. Use `resolves` and `rejects` matchers for promises. Set appropriate timeouts for slow tests with `jest.setTimeout()` only when needed.

**Step 5 — Use snapshots carefully.** Use snapshot tests for UI components or complex objects that change infrequently. Keep snapshots small and focused. Review snapshot changes carefully before committing.

**Step 6 — Test React components through users.** Use React Testing Library over Enzyme. Test user behavior and component accessibility. Query elements by accessibility roles, labels, or text content. Use `userEvent` over `fireEvent` for realistic user interactions.

**Step 7 — Choose precise matchers.** Use the common Jest matchers listed in the output format. Prefer the matcher that communicates the behavior directly, including basic, truthiness, number, string, array, object, exception, and mock-function assertions.

**Step 8 — Validate and report.** Run the smallest existing Jest command that covers the target when available. Report tests added or updated, practices applied, and validation results.

## Invocation Example

```
/javascript-typescript-jest target=src/components/LoginForm.test.tsx scope=component
```

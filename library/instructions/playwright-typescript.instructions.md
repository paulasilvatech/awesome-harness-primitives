---
applyTo: '**/*.spec.ts,**/*.test.ts,**/*.spec.tsx,**/*.test.tsx,**/playwright.config.ts,tests/**/*.ts,tests/**/*.tsx'
description: 'Conventions for Playwright tests in TypeScript covering structure, locators, assertions, fixtures, execution, and quality checks.'
---

# Playwright TypeScript Conventions — Reliable Browser Tests

These instructions apply to Playwright TypeScript test files, TSX test files, and Playwright configuration matched by the `applyTo` globs. They are authoritative for test structure, selectors, assertions, fixtures, execution defaults, and browser-test quality in those files; product behavior, accessibility standards, and project test-runner configuration win where they define stricter requirements.

## Test Structure and File Organization

Keep Playwright tests organized around user-visible features and pages so failures explain behavior rather than implementation details.

| Concern | Convention |
| --- | --- |
| Imports | Start tests with `import { test, expect } from '@playwright/test';` |
| Grouping | Put related scenarios in a `test.describe()` block |
| Setup | Use `test.beforeEach()` for shared navigation or state within a `describe` block |
| Titles | Use descriptive titles such as `Feature - Specific action or scenario` |
| Location | Store browser tests in `tests/` |
| Naming | Name files `<feature-or-page>.spec.ts`, for example `login.spec.ts` or `search.spec.ts` |
| Scope | Prefer one test file per major application feature or page |

Preserve the Playwright hook name `beforeEach` when documenting shared setup, even when examples use `test.beforeEach()`.

Use fixtures instead of global mutable state when setup grows beyond simple navigation. Keep test data deterministic and isolate scenarios so tests can run in parallel.

## Locators and User Interaction

- Prefer user-facing, role-based locators such as `getByRole`, `getByLabel`, and `getByText` because they reflect accessibility and survive DOM refactors.
- Use `test.step()` to group interactions and make reports readable.
- Avoid strict mode violations by making locators specific enough to identify one intended element.
- Rely on Playwright auto-waiting instead of `waitForTimeout`, sleeps, or broad timeout increases.
- Use descriptive step names that state the user intent, not the implementation action.
- Add comments only for complex logic or non-obvious interactions.

## Assertions and Accessibility Snapshots

Use Playwright's built-in auto-waiting and auto-retrying web-first assertions, always awaited with `await`, so tests wait for the browser state Playwright already understands.

| Assertion | Use for |
| --- | --- |
| `await expect(locator).toHaveText()` | Exact visible text |
| `await expect(locator).toContainText()` | Partial visible text |
| `await expect(locator).toHaveCount()` | Element counts from a locator |
| `await expect(page).toHaveURL()` | Navigation results |
| `await expect(page.getByRole('main')).toMatchAriaSnapshot()` | Accessibility tree structure |
| `await expect(locator).toBeVisible()` | Visibility changes when visibility itself is the behavior under test |
| `expect(locator).toBeVisible()` | Legacy spelling; still await it as `await expect(locator).toBeVisible()` |

Prefer assertions that express what the user observes. Use `toMatchAriaSnapshot` for stable accessibility structure and keep snapshots focused enough to review.

## Execution and Debugging

Run the smallest project that covers the change, then expand only when behavior is shared across browsers or projects. `npx playwright test --project=chromium` is the default targeted run for Chromium coverage. When failures occur, inspect the trace, refine locators or assertions, and rerun until the test passes consistently without hard-coded waits.

## Good / Bad Examples

The examples below illustrate resilient locators, `test.step()`, and web-first assertions.

**Good:**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Movie Search Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://debs-obrien.github.io/playwright-movies-app');
  });

  test('Search for a movie by title', async ({ page }) => {
    await test.step('Activate and perform search', async () => {
      await page.getByRole('search').click();
      const searchInput = page.getByRole('textbox', { name: 'Search Input' });
      await searchInput.fill('Garfield');
      await searchInput.press('Enter');
    });

    await test.step('Verify search results', async () => {
      await expect(page.getByRole('main')).toMatchAriaSnapshot(`
        - main:
          - heading "Garfield" [level=1]
          - heading "search results" [level=2]
          - link "poster of The Garfield Movie The Garfield Movie rating":
            - /url: /playwright-movies-app/movie?id=tt5779228&page=1
      `);
    });
  });
});
```

Why: The test uses accessible locators, grouped steps, deterministic navigation, and an awaited accessibility assertion.

**Bad:**

```typescript
test('search', async ({ page }) => {
  await page.goto('https://debs-obrien.github.io/playwright-movies-app');
  await page.waitForTimeout(5000);
  await page.locator('.search input').fill('Garfield');
  expect(await page.locator('.result').count()).toBe(1);
});
```

Why: The test relies on sleeps, CSS implementation details, a vague title, and a non-retrying assertion.

## Conventions

| Rule | Rationale |
|---|---|
| Start tests with `import { test, expect } from '@playwright/test';` | Consistent imports keep Playwright fixtures and assertions explicit |
| Group feature scenarios with `test.describe()` and shared setup with `test.beforeEach()` | Test reports stay navigable and setup remains local |
| Prefer `getByRole`, `getByLabel`, `getByText`, and specific accessible locators | Tests validate user-facing semantics and avoid brittle selectors |
| Use `test.step()` for meaningful interaction groups | Trace and report output explain the scenario |
| Use awaited web-first assertions such as `toHaveText`, `toContainText`, `toHaveCount`, `toHaveURL`, and `toMatchAriaSnapshot` | Assertions retry until the browser reaches the expected state |
| Avoid hard-coded waits and unnecessary timeout increases | Auto-waiting produces faster and less flaky tests |
| Store tests in `tests/` with `<feature-or-page>.spec.ts` names | Test files are predictable and easy to discover |
| Run `npx playwright test --project=chromium` for targeted validation | The default run covers changed browser behavior without unnecessary matrix cost |

## Do / Do Not

| Do | Do not |
|---|---|
| Use role, label, and text locators that describe the UI | Reach first for CSS selectors tied to implementation |
| Await `expect(locator)` web-first assertions | Assert on raw values when Playwright can retry the browser state |
| Keep test and step titles descriptive | Use vague names such as `search` or `works` |
| Let Playwright auto-wait for actions and assertions | Add `waitForTimeout` sleeps or raise default timeouts reflexively |
| Use `toMatchAriaSnapshot` for accessible structure | Snapshot large unstable DOM fragments |
| Keep comments for non-obvious test logic | Comment every ordinary navigation or click |
| Use `test.beforeEach()` for shared setup | Hide setup in unrelated global state |

## Checklist Before Opening a PR

- [ ] Test files live in `tests/` and use `<feature-or-page>.spec.ts` or matching TSX test names.
- [ ] Tests import `test` and `expect` from `@playwright/test`.
- [ ] Related scenarios are grouped with `test.describe()` and shared setup uses `test.beforeEach()`.
- [ ] Locators are accessible, specific, and free of strict mode violations.
- [ ] Assertions are meaningful, awaited, and web-first.
- [ ] Tests avoid hard-coded waits and unnecessary timeout increases.
- [ ] `test.step()` names make reports and traces readable.
- [ ] `npx playwright test --project=chromium` or the relevant project run passes consistently.

## References

- Playwright movies demo used in examples: https://debs-obrien.github.io/playwright-movies-app

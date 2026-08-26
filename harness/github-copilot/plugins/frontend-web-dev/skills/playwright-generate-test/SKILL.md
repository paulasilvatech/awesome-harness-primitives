---
name: "playwright-generate-test"
description: >-
  Generate, save, run, and stabilize Playwright TypeScript tests from a user scenario using Playwright MCP exploration evidence. Use this skill when the user asks to create a Playwright test, generate an @playwright/test spec from a scenario, automate a browser flow, or turn Playwright MCP history into a passing test.
---

# Playwright test generation

Generate a Playwright TypeScript test from a user scenario by first exercising the scenario with Playwright MCP, then writing the spec into the `tests` directory, executing it, and iterating until it passes.

## When to invoke

- "Generate a Playwright test for this checkout flow."
- "Use Playwright MCP to create a test from this scenario."
- "Turn the browser interactions into an @playwright/test spec."
- "Save a Playwright test in the tests directory and make it pass."
- "Automate this UI scenario with Playwright."

## Prerequisites and context

- A concrete scenario is required: target URL or route, starting state, actions, and expected result. If the user provides no scenario, request one before generating code.
- Use Playwright MCP for browser navigation and interaction evidence before writing test code.
- Use the project's existing Playwright setup; do not add a new runner when `@playwright/test` is already present.
- Save generated specs under the existing `tests` directory. If the repository uses a nested Playwright convention such as `tests/e2e`, follow the existing convention inside `tests`.

## Procedure

1. Parse the scenario into preconditions, actions, assertions, and any data dependencies.
2. Open the app with Playwright MCP and perform the scenario one step at a time. Do not generate test code prematurely or solely from the written scenario.
3. Capture durable selector evidence from the explored UI: accessible roles, labels, text, test ids, URLs, and visible state changes.
4. Convert the completed interaction history into a Playwright TypeScript test using `@playwright/test`.
5. Save the generated test file in the `tests` directory with a descriptive `.spec.ts` name.
6. Execute the new test file with the existing project command when available, or with `npx playwright test <test-file>` when the project has Playwright installed.
7. Fix selector, timing, setup, or assertion issues and rerun the same test until it passes or a real product defect blocks it.

## Scenario extraction

| Scenario part | Capture | Test representation |
| --- | --- | --- |
| Entry point | URL, route, fixture, auth state, viewport if relevant | `await page.goto('<url>')` or existing test fixture setup |
| User action | Clicks, fills, selections, keyboard input, uploads, navigation | `page.getByRole`, `getByLabel`, `getByText`, `locator`, `selectOption`, `press` |
| Observable result | URL change, visible message, table row, enabled control, network-driven UI state | `await expect(...).toBeVisible()`, `toHaveURL`, `toContainText`, `toBeEnabled` |
| Required wait | UI transition, navigation, async rendering | Prefer web-first assertions; avoid arbitrary sleeps |
| Test data | Unique names, emails, IDs, clean-up needs | Generate deterministic or unique data inside the test without hardcoded shared secrets |

## Selector strategy

| Preference | Use | Avoid |
| --- | --- | --- |
| Accessible role | `page.getByRole('button', { name: 'Save' })` | CSS class chains tied to styling |
| Form labels | `page.getByLabel('Email')` | Index-based selectors like `locator('input').nth(2)` |
| Stable test ids | `page.getByTestId('submit-order')` when the project uses them | Adding test ids without user approval unless already conventional |
| Visible text | `page.getByText('Order submitted')` for user-facing outcomes | Text that is dynamic, localized, or incidental |
| Structural locator | Scoped `locator()` only when accessible selectors are unavailable | XPath copied from browser devtools |

## Test construction

- Import from `@playwright/test`: `import { test, expect } from '@playwright/test';`.
- Name the test after the user-visible behavior, not the implementation detail.
- Keep the generated file focused on the requested scenario unless the user asks for a suite.
- Use `test.describe` only when grouping multiple related tests in the same file.
- Assert the final business outcome and at least one intermediate state when it prevents false positives.
- Prefer Playwright web-first assertions over `page.waitForTimeout`.
- Keep credentials, tokens, and private data out of the test. Use existing fixtures or environment-driven auth when the project already provides them.

## Common defects

| Defect | Why it fails | Correction |
| --- | --- | --- |
| Code before exploration | The test encodes assumptions and misses actual labels, routing, or timing | Complete all Playwright MCP steps before emitting code |
| Brittle selector | Styling or DOM order changes break the test without behavior changing | Use role, label, text, or test id selectors |
| Missing assertion | The test only clicks through the flow and can pass while the feature is broken | Assert visible outcome, URL, or persisted UI state |
| Arbitrary sleep | Slow or fast environments make `waitForTimeout` flaky | Use `await expect(locator).to...` |
| Unscoped data | Shared fixed values collide across runs | Generate unique data or clean up through existing helpers |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Test cannot find a locator | The selected locator was not stable or the element appears later | Re-open the page with Playwright MCP, inspect accessible names, and replace with a web-first locator plus assertion |
| Test passes locally but fails in CI | Timing, viewport, auth state, or test data differs | Remove sleeps, assert readiness, use existing storage state or fixtures, and avoid shared data |
| Navigation assertion times out | The action does not navigate or the URL pattern is too strict | Assert the actual post-action UI state, or use a looser `toHaveURL` pattern backed by exploration evidence |
| Browser is not installed | Playwright dependency exists but browsers are missing | Run the project's documented install command, commonly `npx playwright install`, only when dependency setup is expected |

## Output template

```markdown
## Playwright test generation result

**Status:** passed | blocked
**Scenario:** <one-sentence scenario summary>
**Test file:** `tests/<name>.spec.ts`

### Exploration evidence
| Step | Interaction | Selector or URL | Observed outcome |
| --- | --- | --- | --- |
| 1 | <action> | `<selector-or-url>` | <visible result> |

### Generated test
- Framework: `@playwright/test`
- Command: `<test command>`
- Result: pass | fail

### Remaining work
- <none, or blocker with evidence>
```

## Quality gate

- [ ] A user scenario was provided or explicitly requested before code generation.
- [ ] Playwright MCP was used step by step before emitting the test.
- [ ] The emitted test imports from `@playwright/test`.
- [ ] The test file is saved under the `tests` directory.
- [ ] Selectors prefer roles, labels, text, or stable test ids over brittle DOM structure.
- [ ] Assertions verify the user-visible outcome of the scenario.
- [ ] The generated test file was executed.
- [ ] Failures were iterated until the test passed or a blocker was reported with evidence.

---
name: "webapp-testing"
description: >-
  Test and debug local or accessible web applications in a real browser using Playwright automation. Use when asked to verify frontend functionality, UI behavior, forms, navigation, console logs, screenshots, network activity, responsive viewports, or user flows.
---

# Web application testing

Drive a local or accessible web application through Playwright, verify user-visible behavior, capture diagnostics, and report the browser evidence behind each finding.

## When to invoke

- "Test this web app in a browser."
- "Verify this form submission flow."
- "Capture screenshots for this UI bug."
- "Inspect browser console logs and network requests."
- "Check the responsive layout across viewports."

## Prerequisites and context

- A locally running web application or accessible URL is required.
- Node.js is required when falling back to local Playwright code.
- Prefer the Playwright MCP server when available; otherwise run local Node.js with Playwright installed.
- Playwright can be installed automatically if not present.
- This skill does not test native mobile apps; use React Native Testing Library for those.

## Browser testing capabilities

| Capability | Examples |
| --- | --- |
| Browser automation | Navigate to URLs, click buttons and links, fill fields, select dropdowns, handle dialogs and alerts. |
| Verification | Assert element presence, verify text content, check visibility, validate URLs, and test responsive behavior. |
| Debugging | Capture screenshots, view console logs, inspect network requests, and debug failed tests. |

Prefer user-facing selectors: roles, labels, text, and `data-testid`. Use role-based selectors before CSS classes when no stable semantic selector exists.

## Procedure

1. Confirm the application is running and the target URL is reachable.
2. Start with a small navigation or smoke test before complex flows.
3. Use explicit waits for elements or navigation before interacting.
4. Exercise the requested user flow with realistic input.
5. Capture screenshots on failure and collect console or network evidence when debugging.
6. Close browsers and clean up resources when using local Playwright code.
7. Report actions, observations, evidence, and remaining gaps.

## Playwright patterns

```javascript
// Navigate to a page and verify title
await page.goto("http://localhost:3000");
const title = await page.title();
console.log("Page title:", title);
```

```javascript
// Fill out and submit a form
await page.fill("#username", "testuser");
await page.fill("#password", "password123");
await page.click('button[type="submit"]');
await page.waitForURL("**/dashboard");
```

```javascript
// Capture a screenshot for debugging
await page.screenshot({ path: "debug.png", fullPage: true });
```

```javascript
await page.waitForSelector("#element-id", { state: "visible" });
const exists = (await page.locator("#element-id").count()) > 0;
page.on("console", (msg) => console.log("Browser log:", msg.text()));
```

```javascript
try {
  await page.click("#button");
} catch (error) {
  await page.screenshot({ path: "error.png" });
  throw error;
}
```

## Gotchas

- **Always verify the app is running first**: failing browser actions against a dead server hides the actual setup problem.
- **Use explicit waits**: interact only after the element or navigation target is ready.
- **Capture screenshots on failure**: visual evidence usually shortens UI debugging.
- **Set reasonable timeouts**: slow local builds and API calls need bounded waiting, not infinite hangs.
- **Test incrementally**: one small verified step is easier to debug than a long failing script.
- **Complex authentication may need setup**: use existing test accounts, storage state, or documented login helpers rather than bypassing auth.

## Progressive disclosure and bundled resources

- `assets/test-helper.js` / `test-helper.js`: helper functions for waiting for elements, capturing screenshots, and handling errors. Import it when writing reusable local Playwright tests.

## Output template

```markdown
## Web application test result

**Status:** pass | fail | blocked
**URL:** `<tested URL>`
**Browser path:** Playwright MCP | local Playwright

| Flow | Action | Expected | Observed | Evidence |
| --- | --- | --- | --- | --- |
| <flow name> | <click/fill/navigate/assert> | <expected behavior> | <actual behavior> | <screenshot, console log, network request, or selector> |

### Diagnostics
- Console: <errors, warnings, or none>
- Network: <failed requests or none>
- Screenshots: <paths or not captured>
```

## Quality gate

- [ ] The target app or URL was verified reachable before testing.
- [ ] Browser interactions used explicit waits or locator assertions.
- [ ] Selectors prefer roles, labels, text, or `data-testid` over fragile CSS classes.
- [ ] Failures include screenshot, console, network, or DOM evidence.
- [ ] Browser resources were closed when local Playwright was used.
- [ ] The final result states pass, fail, or blocked for each requested flow.

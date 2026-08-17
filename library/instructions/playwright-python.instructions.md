---
applyTo: "**/*.py"
description: "Enforces Playwright Python test conventions for Pytest structure, resilient locators, web-first assertions, synchronization, and execution."
name: "Playwright Python Conventions"
---

# Playwright Python Conventions — Pytest Browser Tests

These instructions apply to Python files that create or maintain Playwright tests with Pytest. They are authoritative for Playwright Python test structure, locator choice, assertion style, synchronization, file naming, and execution conventions in matched files; project-specific test layout, fixtures, and CI commands win when they define stricter local rules.

## Test Structure and Imports

Use Pytest conventions and Playwright's synchronous API consistently so generated tests are discoverable, typed, and easy to debug.

| Concern | Convention |
| --- | --- |
| Imports | Start Playwright test files with `from playwright.sync_api import Page, expect`; add `import re` or `import pytest` only when the test uses them. |
| Browser fixture | Accept the `page: Page` fixture in each test function that drives the browser. |
| Test names | Use descriptive `test_<feature_or_page>.py` file names and `def test_navigation_link_works(page: Page):`-style function names. |
| Navigation | Put `page.goto()` at the beginning of the test or in a standard Pytest fixture when setup is shared. |
| Shared setup | Use `@pytest.fixture(scope="function", autouse=True)` only when every test in the file requires the same browser state. |
| Organization | Store tests under `tests/` or the existing project test structure, with one file per major feature or page. |

Keep comments for non-obvious flow only. Do not comment obvious actions such as clicking a button.

## Locators and User-Facing Behavior

Prioritize role-based locators that describe how users and assistive technologies find elements.

- Prefer `page.get_by_role()`, `page.get_by_label()`, and `page.get_by_text()` before CSS or XPath selectors.
- Include accessible names in role locators, for example `page.get_by_role("link", name="Get started")`.
- Use specific locators that survive layout changes and validate accessibility assumptions.
- Scope locators when repeated text or roles exist on the page instead of relying on the first match by accident.
- Avoid implementation selectors unless the application has no accessible surface for the interaction being tested.

## Assertions and Synchronization

Use Playwright's auto-waiting and web-first assertions instead of manual timing.

| Scenario | Preferred assertion |
| --- | --- |
| Page title | `expect(page).to_have_title(...)` |
| Page URL | `expect(page).to_have_url(...)` |
| Element count | `expect(locator).to_have_count(...)` |
| Exact text | `expect(locator).to_have_text(...)` |
| Partial text | `expect(locator).to_contain_text(...)` |
| Visibility transition | `expect(locator).to_be_visible()` only when visibility itself is the behavior under test |

Prefer `expect` over raw `assert` for UI state because Playwright retries until the condition is met or the timeout expires. Rely on Playwright's built-in auto-waiting and avoid hard-coded waits, sleeps, or increased default timeouts unless the application has a documented timing boundary.

## Execution and Failure Analysis

Run tests from the terminal with `pytest` or the repository's existing Pytest command. When a test fails, inspect the failure output, screenshot or trace artifacts if configured, the selected locator, and the intended user behavior before changing timeouts. Use `pytest -k <name>` for focused reruns and keep failure fixes tied to the root cause.

## Good / Bad Examples

The examples below illustrate resilient locators, setup through Pytest, and web-first assertions.

**Good:**

```python
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    page.goto("https://playwright.dev/")

def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")

def test_has_title(page: Page):
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.get_by_role("link", name="Get started").click()
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
```

Why: The test uses the `page: Page` fixture, typed imports, user-facing locators, auto-retrying `expect` assertions, and shared navigation only where every test needs it.

**Bad:**

```python
import time


def test_get_started_link(page):
    page.goto("https://playwright.dev/")
    time.sleep(5)
    page.locator(".navbar a:nth-child(1)").click()
    assert page.locator("h1").inner_text() == "Installation"
```

Why: The test omits typing, waits with a hard-coded sleep, uses brittle implementation selectors, and replaces web-first assertions with a non-retrying `assert`.

## Conventions

| Rule | Rationale |
| --- | --- |
| Import `Page` and `expect` from `playwright.sync_api` in test files | Tests stay typed and use Playwright's retrying assertion model. |
| Use the `page: Page` fixture instead of constructing browser objects manually | Pytest and Playwright manage browser lifecycle consistently. |
| Prefer role, label, and text locators | Tests validate user-facing behavior and are resilient to DOM refactors. |
| Use `expect` assertions such as `to_have_title`, `to_have_url`, `to_have_count`, `to_have_text`, and `to_contain_text` | Assertions wait for the UI to reach the expected state. |
| Avoid hard-coded waits and default timeout inflation | Auto-waiting exposes real synchronization issues instead of hiding them. |
| Keep tests organized as `test_<feature-or-page>.py` under `tests/` or the existing structure | Pytest discovery remains predictable. |
| Debug failures by identifying root cause before editing assertions or timeouts | Tests remain meaningful instead of becoming flaky acceptance of any behavior. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `page.get_by_role("button", name="Save")` or another user-facing locator | Use CSS or XPath selectors when an accessible locator exists. |
| Put `page.goto()` at the start of a test or shared fixture | Hide navigation in unrelated helper code. |
| Use `expect(page).to_have_url()` for navigation checks | Compare `page.url` with raw `assert` for asynchronous navigation. |
| Use `expect(locator).to_have_text()` or `to_contain_text()` for text | Read `inner_text()` and assert immediately. |
| Use `expect(locator).to_be_visible()` when visibility is the behavior | Use visibility as a vague substitute for a more specific assertion. |
| Run focused tests with `pytest -k <name>` while debugging | Increase global timeouts to compensate for unknown failures. |

## Checklist Before Opening a PR

- [ ] Test files use `test_<feature-or-page>.py` names and live under `tests/` or the existing test structure.
- [ ] Playwright tests import `Page` and `expect` from `playwright.sync_api`.
- [ ] Browser-driving tests accept the `page: Page` fixture.
- [ ] Navigation setup uses `page.goto()` directly in the test or a justified Pytest fixture.
- [ ] Locators prefer `get_by_role`, `get_by_label`, or `get_by_text` with accessible names where possible.
- [ ] Assertions use Playwright `expect` web-first assertions instead of raw UI `assert` checks.
- [ ] No hard-coded sleeps or unjustified timeout increases were introduced.
- [ ] Failing tests were debugged to root cause before changing locator or assertion behavior.

## References

- Playwright documentation site: https://playwright.dev/

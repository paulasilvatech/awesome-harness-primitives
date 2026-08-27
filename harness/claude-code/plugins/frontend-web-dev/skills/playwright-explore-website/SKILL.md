---
name: playwright-explore-website
description: >-
  Explore a website with Playwright MCP, identify 3-5 core user flows, capture locators and
  expected outcomes, close the browser context, and propose test cases. Use this skill when the
  user asks to explore a site for testing, map UI functionality, discover test scenarios, or
  produce Playwright-ready interaction notes.
---

<!-- Generated from harness/github-copilot/plugins/frontend-web-dev/skills/playwright-explore-website/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Website exploration for testing

Explore a provided website with Playwright MCP, exercise 3-5 core features or user flows, document interactions and locators, then summarize findings and propose test cases.

## When to invoke

- "Explore this website and identify key test flows."
- "Use Playwright MCP to map the core functionality."
- "Find important UI interactions and locators for tests."
- "Explore this app and propose Playwright test cases."
- "Document expected outcomes for the main user flows."

## Prerequisites and context

- A URL is required. If no URL is provided, request one before opening a browser.
- Use Playwright MCP for navigation, interaction, snapshots, and browser-context cleanup.
- Explore as a tester, not as a crawler: prioritize user-visible workflows over exhaustive link traversal.
- Do not enter real secrets, payment data, or private personal data. Use safe dummy values for forms.

## Procedure

1. Navigate to the provided URL using the Playwright MCP Server.
2. Establish the page purpose, primary navigation, authentication requirements, and any modal or cookie banner that blocks interaction.
3. Identify and interact with 3-5 core features or user flows.
4. For each flow, document user interactions, relevant UI elements, locators, and expected outcomes.
5. Capture failed, blocked, or ambiguous behavior with evidence instead of guessing.
6. Close the browser context upon completion.
7. Provide a concise summary and propose test cases based on the exploration.

## Exploration priorities

| Priority | Look for | Evidence to capture |
| --- | --- | --- |
| Navigation | Header links, menus, breadcrumbs, search, route changes | URL, accessible link names, selected state |
| Forms | Required fields, validation, submit buttons, success or error messages | Labels, roles, validation text, disabled/enabled states |
| Authentication | Login, logout, registration, gated content, session persistence | Safe dummy credentials, redirects, visible account state |
| Data views | Tables, filters, sorting, pagination, detail pages | Column names, filter controls, row changes |
| Commerce or workflow | Cart, checkout, upload, wizard, approval, save/publish actions | Step labels, state transitions, confirmation messages |
| Accessibility signals | Roles, labels, keyboard focus, visible names | `getByRole`, `getByLabel`, `getByText` candidates |

## Locator capture guide

| Element type | Preferred locator note | Expected outcome note |
| --- | --- | --- |
| Button | Role and accessible name, for example `button: "Submit"` | State change after click, disabled state, or validation |
| Link | Role/name plus destination URL or route | Navigates to expected route or content section |
| Input | Label, placeholder only as fallback, required state | Accepted value, validation message, or formatted output |
| Select/listbox | Label and option text | Selected value appears or filters data |
| Alert/toast | Role when available, otherwise visible text | Message content and disappearance/persistence |
| Table/list item | Header/row text and scoping container | New, removed, sorted, or filtered item |

## Test case design

- Convert each explored flow into a test with preconditions, steps, assertions, and data needs.
- Prefer one happy-path test plus focused validation or error-path tests for high-risk forms.
- Anchor assertions on user-visible outcomes: confirmation text, URL, rendered data, enabled controls, or persisted state.
- Mark flows as blocked when authentication, unavailable services, CAPTCHA, or missing test data prevents safe exploration.
- Keep generated cases Playwright-ready by naming selectors and expected outcomes precisely.

## Gotchas

- **Do not stop at screenshots**: exploration must include interactions and expected outcomes, not just visual observations.
- **Do not overfit to CSS**: locator notes should favor accessible roles, labels, text, and stable test ids.
- **Close the browser context**: leaving the context open can leak state into later exploration.
- **Limit to 3-5 core flows**: broad crawling produces shallow notes; prioritize flows that represent real user value.

## Output template

```markdown
## Website exploration result

**Status:** complete | blocked
**URL:** <provided URL>
**Flows explored:** <count>

### Summary
<concise description of the site purpose and main risks>

### Interaction notes
| Flow | Steps | Locators captured | Expected outcome | Status |
| --- | --- | --- | --- | --- |
| <flow name> | <ordered user actions> | `<role/label/text/test-id notes>` | <observable result> | pass | blocked |

### Proposed test cases
| Test | Preconditions | Steps | Assertions | Priority |
| --- | --- | --- | --- | --- |
| <test name> | <state/data> | <actions> | <expected checks> | P0/P1/P2 |

### Cleanup
- Browser context closed: yes | no
```

## Quality gate

- [ ] A URL was provided or explicitly requested before navigation.
- [ ] The site was explored with Playwright MCP.
- [ ] 3-5 core features or user flows were identified unless blocked.
- [ ] Each explored flow includes interactions, relevant UI elements, locators, and expected outcomes.
- [ ] Proposed test cases are grounded in observed behavior.
- [ ] Unsafe real credentials, payment data, and private personal data were not entered.
- [ ] The browser context was closed upon completion.
- [ ] The final summary is concise and includes blockers when present.

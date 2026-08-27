---
description: Explore a website with Playwright MCP, document core user flows, and propose test cases.
argument-hint: "url=<website-url>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch, mcp__playwright
---

<!-- Generated from harness/github-copilot/prompts/playwright-explore-website.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /playwright-explore-website

## Objective

Explore a provided website URL with the Playwright MCP Server, identify 3-5 core features or user flows, document interactions, UI elements, locators, expected outcomes, and proposed Playwright test cases that can guide later test generation.

## When to Invoke

Use this prompt when a team needs exploratory testing notes for a website before generating automated Playwright tests, validating core flows, or deciding which scenarios deserve coverage.

## Preconditions

- A reachable website URL is provided or can be requested from the user.
- The Playwright MCP Server and `playwright` tool are available in the VS Code agent environment.
- Browser interaction is permitted for the target site.
- Test-case proposals may be returned in Chat or written only when file edits are explicitly appropriate.

## Inputs the Team Must Provide

- `url` — the website URL to explore.
- Authentication details, test data, or environment notes when a flow requires them.
- Any priority areas, accessibility needs, or flows that must not be executed.
- Ask the user for the URL if no URL is provided, and stop until it is available.

## What I Will Do

- Navigate to the provided URL using the Playwright MCP Server.
- Identify and interact with 3-5 core features or user flows.
- Document user interactions, relevant UI elements and their locators, and expected outcomes.
- Close the browser context upon completion.
- Provide a concise summary of findings.
- Propose test cases based on the exploration.
- Generate test cases only when the requested destination and available tools make that appropriate.

## What I Will NOT Do

- Explore without a user-provided URL.
- Perform destructive actions such as purchases, irreversible submissions, account deletion, or production data changes.
- Bypass authentication, rate limits, access controls, or terms of use.
- Guess locators without inspecting the UI.
- Leave the browser context open after exploration.
- Generate final test code when the task is only exploratory; `playwright-generate-test` owns validated test generation.

## Output Format

Return exploration notes and proposed tests in this shape:

```markdown
## Website Exploration Result

### Target
- URL: `<website-url>`

### Core Flows Explored
| Flow | Steps performed | Key UI elements and locators | Expected outcome | Observed result |
| --- | --- | --- | --- | --- |
| Sign in |  | `getByRole('button', { name: 'Sign in' })` |  |  |

### Proposed Test Cases
| Priority | Scenario | Preconditions | Assertions | Notes |
| --- | --- | --- | --- | --- |

### Findings
- 

### Browser Cleanup
- Browser context closed: yes | no

### Blockers
- 
```

## Definition of Done

- [ ] A website URL was provided before browser navigation began.
- [ ] The Playwright MCP Server was used to navigate to the provided URL.
- [ ] 3-5 core features or user flows were identified and interacted with when available.
- [ ] User interactions, UI elements, locators, and expected outcomes are documented.
- [ ] Proposed test cases are based on observed flows, not guesses.
- [ ] The browser context is closed upon completion.
- [ ] The response provides a concise summary of findings.

## Prompt Body

Follow these steps in order. Explore safely and record evidence for test design.

**Step 1 — Confirm the URL.**
Read `${input:url:<website-url>}`. If no URL is provided, ask the user to provide one and stop before using browser tools.

**Step 2 — Navigate with Playwright MCP.**
Use the Playwright MCP Server to navigate to the provided URL. Wait for the page to be ready before interacting.

**Step 3 — Identify core flows.**
Identify 3-5 core features or user flows from visible navigation, primary calls to action, forms, search, account flows, or other prominent UI.

**Step 4 — Interact with each flow.**
Perform safe interactions one flow at a time. Record each user interaction, relevant UI element, locator, and expected outcome. Avoid destructive actions.

**Step 5 — Summarize observations.**
Document observed results, blockers, surprising behavior, inaccessible states, or missing test data.

**Step 6 — Propose test cases.**
Convert the explored flows into proposed test cases with preconditions, assertions, and priority. Keep proposals grounded in observed UI and locators.

**Step 7 — Close the browser context.**
Close the browser context upon completion and record whether cleanup succeeded.

**Step 8 — Report concisely.**
Provide the exploration result, concise findings summary, proposed test cases, cleanup status, and blockers.

## Invocation Example

```
/playwright-explore-website url=https://example.com
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `playwright-generate-test` | prompt | Generates and validates a Playwright TypeScript test from an explored scenario. |

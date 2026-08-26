---
name: "playwright-generate-test"
description: "Generate a Playwright end-to-end test from a scenario using Playwright MCP, deferring the procedure to the playwright-generate-test skill."
argument-hint: "scenario=\"<user flow to test>\""
agent: "qa-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /playwright-generate-test

## Objective

Explore a described user flow with Playwright MCP and emit a passing `@playwright/test` TypeScript end-to-end test for the SIFAP 2.0 frontend. The full procedure lives in the [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md) skill; this prompt applies it to the Next.js 15 frontend without restating it.

> [!IMPORTANT]
> Do not write test code from the scenario alone — run the flow step by step with Playwright MCP first, then generate the test from the observed steps.

## When to Invoke

During Stage 3/4, when the team wants an end-to-end regression test for a user-facing flow in the Next.js 15 frontend.

## Preconditions

- The `frontend/` app is running and reachable
- Playwright and the Playwright MCP server are available
- The scenario to test is described (or will be provided on request)

## Inputs the Team Must Provide

- `scenario` — the user flow to test (ask for one if it is missing)
- The base URL of the running frontend
- Ask the user for anything that is missing.

## What I Will Do

- Follow the explore-then-generate procedure in the [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md) skill
- Drive the scenario one step at a time through Playwright MCP before writing code
- Emit a `@playwright/test` TypeScript spec into the frontend's `tests/` directory
- Run the test and iterate until it passes

## What I Will NOT Do

- Generate test code prematurely from the scenario alone
- Cover unit/component behavior here (that stays in Vitest + Testing Library)
- Leave a failing or flaky test behind
- Hardcode secrets or environment-specific data into the spec

## Output Format

```markdown
### Generated
`frontend/tests/payment-approval.spec.ts` — @playwright/test

### Run
`npx playwright test payment-approval` → 1 passed
```

## Definition of Done

- [ ] The flow was explored step by step with Playwright MCP before code was written
- [ ] The spec uses `@playwright/test` and lives in the frontend `tests/` directory
- [ ] The test runs green and is not flaky
- [ ] Unit/component coverage remains in Vitest + Testing Library

## Prompt Body

The [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md) skill owns the MCP-driven exploration and generation procedure — read it, then apply it to the scenario.

**Step 1 — Get the scenario.**
If none was provided, ask for one. Confirm the frontend URL.

**Step 2 — Apply the skill.**
Run the scenario one step at a time with Playwright MCP, then emit the `@playwright/test` spec from the recorded steps.

**Step 3 — Respect the kit rules.**
Target the Next.js 15 App Router frontend, save the spec under `frontend/tests/`, and keep secrets out of the file.

**Step 4 — Verify.**
Execute the test and iterate until it passes.

## Invocation Example

```
/playwright-generate-test scenario="approve a pending payment as an analyst"
```

---
name: 'playwright-generate-test'
description: 'Generate and validate a Playwright test from a provided scenario after browser exploration.'
agent: 'agent'
model: 'Claude Sonnet 4'
tools: ['changes', 'codebase', 'editFiles', 'fetch', 'findTestFiles', 'problems', 'runCommands', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'playwright']
argument-hint: 'scenario=<tested-flow-or-scenario>'
---

# /playwright-generate-test

## Objective

Generate a Playwright TypeScript test for a provided scenario only after completing the prescribed browser exploration steps with the Playwright MCP tools, then save the generated test file in the tests directory, execute it, and iterate until it passes or a blocker is documented.

## When to Invoke

Use this prompt after a scenario is known, ideally from `playwright-explore-website`, and the team wants executable Playwright test code based on actual browser interaction rather than the scenario text alone.

## Preconditions

- A concrete scenario is provided by the user.
- The Playwright MCP Server and `playwright` tool are available in the VS Code agent environment.
- A Playwright project exists or the repository has an established tests directory for generated tests.
- Test file creation under the tests directory is permitted.
- Test execution through existing commands or VS Code test tools is permitted.

## Inputs the Team Must Provide

- `scenario` — the user flow or scenario to automate.
- Target URL, test data, authentication instructions, and any constraints needed to execute the scenario.
- Preferred tests directory or naming convention when the repository has more than one.
- Ask the user for the scenario if it is not provided, and stop until it is available.

## What I Will Do

- Ask for a scenario when none is provided.
- Run the prescribed scenario steps one by one using the tools provided by the Playwright MCP.
- Avoid generating test code prematurely or based solely on the scenario.
- After all steps are completed, emit a Playwright TypeScript test that uses `@playwright/test` based on message history and observed browser behavior.
- Save the generated test file in the tests directory.
- Execute the test file and iterate until the test passes or a clear blocker remains.

## What I Will NOT Do

- Generate test code before completing the browser steps.
- Base final locators, assertions, or navigation solely on the written scenario when browser evidence is available.
- Save tests outside the tests directory unless the repository's established Playwright test tree is explicitly different.
- Add new Playwright infrastructure when an existing project and command are available.
- Run destructive flows, bypass authentication, or mutate production data.
- Claim the test passes without executing it or recording why execution could not run.

## Output Format

Return generated test and validation evidence in this shape:

```markdown
## Playwright Test Generation Result

### Scenario
- 

### Exploration Evidence
| Step | Browser action | Locator | Observed result |
| --- | --- | --- | --- |

### Generated Test File
- `tests/<scenario>.spec.ts`

### Test Summary
- Framework: `@playwright/test`
- Main assertions:
- Test data:

### Execution
| Command | Result | Notes |
| --- | --- | --- |

### Iterations
- 

### Blockers
- 
```

## Definition of Done

- [ ] A scenario was provided before work began.
- [ ] The prescribed steps were run one by one using Playwright MCP tools.
- [ ] Test code was not emitted until browser exploration completed.
- [ ] The generated Playwright TypeScript test uses `@playwright/test`.
- [ ] The test file is saved in the tests directory or the repository's established Playwright test tree.
- [ ] The test file was executed and iterated until it passed, or blockers are documented.
- [ ] The response reports generated file, command, result, iterations, and blockers.

## Prompt Body

Follow these steps in order. Do not generate test code prematurely.

**Step 1 — Confirm the scenario.**
Read `${input:scenario:<tested-flow-or-scenario>}`. If the user does not provide a scenario, ask them to provide one and stop.

**Step 2 — Prepare browser execution.**
Identify the target URL, test data, authentication requirements, and repository tests directory. Do not write code yet.

**Step 3 — Execute the scenario with Playwright MCP.**
Run the scenario steps one by one using the tools provided by the Playwright MCP. Observe page states, reliable locators, and expected outcomes.

**Step 4 — Record evidence.**
Capture the browser action, locator, observed result, and any timing or data dependency for each step. Use message history as evidence for the generated test.

**Step 5 — Generate the test.**
Only after all steps are completed, emit a Playwright TypeScript test that uses `@playwright/test` and reflects the observed flow.

**Step 6 — Save the test file.**
Save the generated test file in the tests directory or the repository's established Playwright test tree, following local naming conventions.

**Step 7 — Execute and iterate.**
Execute the test file using the repository's existing Playwright command or VS Code test tools. Iterate on locators, waits, and assertions until the test passes or a blocker is documented.

**Step 8 — Report concisely.**
Return generated file, execution command, pass/fail result, iterations, and blockers.

## Invocation Example

```
/playwright-generate-test scenario="user searches for a product and opens the first result"
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `playwright-explore-website` | prompt | Explores a website first and proposes scenarios grounded in observed flows. |

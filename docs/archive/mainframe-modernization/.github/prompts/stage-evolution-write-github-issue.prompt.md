---
name: "write-github-issue"
description: "Writes a high-quality GitHub issue ready for the Copilot Agent in the cloud."
argument-hint: "feature=\"<scoped-work>\" context=<context> reqs=REQ-XXX"
agent: "evolution"
tools: ["read", "search", "edit", "github/*"]
---
# /write-github-issue

## Objective

Create a well-structured GitHub issue optimized for autonomous execution by the Copilot Agent (cloud). The issue has clear acceptance criteria, file path guidance, and REQ-ID traceability.

## When to Invoke

At the beginning of Stage 4, when the team identifies work that can be delegated to the Copilot Agent.

## Preconditions

- The team has a working Stage 3 prototype
- `specs/<NNN>-<feature>/spec.md` exists with EARS requirements
- The team identified a specific piece of work to delegate

## Inputs the Team Must Provide

- A description of the desired feature or fix
- Related REQ-IDs (if any)
- The bounded context and files likely to be affected

## What I Will Do

- Structure the issue with five required sections: Context, Acceptance Criteria, Affected Files, Testing Approach, and Out of Scope
- Reference existing REQ-IDs and criteria without inventing EARS requirements or behavior
- Suggest labels and an assignee

## What I Will NOT Do

- Post the issue directly — the team reviews and posts it manually
- Write vague issues — every issue has specific acceptance criteria
- Create issues for work the team must do itself (architectural decisions, security fixes)
- Skip the testing approach section — the Copilot Agent needs to know how to verify its work

## Output Format

A draft file at `04-evolution/issues/<slug>.md`:

```markdown
# Issue: [Title]
## Context
## Acceptance Criteria
## Files Likely Affected
## Testing Approach
## Out of Scope
## Labels
## Related Requirements
```

## Definition of Done

- [ ] The issue draft has all five content sections
- [ ] Acceptance criteria are specific and testable
- [ ] At least one REQ-ID is referenced, or "new behavior" is declared with a rationale
- [ ] Files likely to be affected are listed with relative paths
- [ ] The testing approach describes which tests to add or modify
- [ ] The issue is small enough for a single PR (if it is too large, split it)

## Prompt Body

You are the `@evolution`. The team wants to delegate work to the Copilot Agent through a GitHub issue.

**Step 1 — Understand the request.**
Ask the team:

1. What do you want done? (1-2 sentences)
2. Which bounded context does this affect?
3. Does this implement an existing `REQ-NNN` or new behavior?
4. Which files are likely involved?

**Step 2 — Write the Context section.**
Describe why this work is necessary. Reference the current state of the codebase (what exists) and the desired state (what should exist afterward). Link to the EARS specification if relevant.

**Step 3 — Copy the Acceptance Criteria.**
Copy the verifiable criteria from `spec.md` for the provided REQ-IDs. If
they are missing, record the gap and do not invent a ready-made answer.

**Step 4 — List Affected Files.**
Based on the team's input and a codebase search, list:

- Files to modify (with relative paths)
- Files to create (with suggested paths following the package structure)
- Files to reference but not modify (for example, the OpenAPI specification or existing interfaces)

**Step 5 — Define the Testing Approach.**
Describe which tests the Copilot Agent should write:

- Unit tests for new service methods
- Integration tests for new endpoints
- Existing tests that may need updates

If the bounded context already has testing patterns, reference them so the Copilot Agent follows the same style.

**Step 6 — Mark Out of Scope.**
Explicitly state what this issue does NOT cover. This prevents scope creep in the AI-generated PR. Examples:

- "Does not change the database schema"
- "Does not modify the authentication flow"
- "Frontend changes are tracked in a separate issue"

**Step 7 — Add metadata.**
Suggest labels: `enhancement` or `bug`, the bounded context name, and `copilot-agent`.

**Step 8 — Write the draft.**
Generate the output at `04-evolution/issues/<slug>.md`, where `<slug>` is a kebab-case version of the title. The team reviews this draft before posting it as an actual GitHub issue.

Remind the team: this is a draft. Review it, adjust the scope if necessary, then post it manually through the GitHub UI or `gh issue create`.

## Invocation Example

```
/write-github-issue feature="<scoped-work>" context=<context> reqs=REQ-XXX
```

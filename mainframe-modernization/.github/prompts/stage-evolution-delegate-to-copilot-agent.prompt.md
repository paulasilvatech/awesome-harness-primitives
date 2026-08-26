---
name: "delegate-to-copilot-agent"
description: "Delegates an issue to the GitHub Copilot Agent in the cloud and tracks the resulting PR."
argument-hint: "issue=04-evolution/issues/<slug>.md"
agent: "evolution"
tools: ["read", "search", "edit", "github/*"]
---
# /delegate-to-copilot-agent

## Objective

Guide the team in posting a reviewed issue on GitHub and preparing a watch list to monitor the AI-generated PR. This is a delegation workflow — the team owns the review and merge.

## When to Invoke

After the team has reviewed and approved an issue draft from `/write-github-issue`.

## Preconditions

- An issue draft exists at `04-evolution/issues/<slug>.md`
- The team reviewed and approved the draft
- The team has push access to the GitHub repository

## Inputs the Team Must Provide

- The file path of the issue draft
- Confirmation that the draft is ready to post

## What I Will Do

- Guide the team through posting the issue on GitHub
- Prepare a watch-list document with expected results
- Provide a review guide for when the PR arrives

## What I Will NOT Do

- Post the issue for the team — they do it manually to understand the workflow
- Assume the AI PR will be correct — I prepare the team to review it critically
- Merge any PR — the team makes the merge decision
- Skip the review guide — every delegated PR requires human review

## Output Format

A delegation tracking file at `04-evolution/delegations/<issue-slug>.md`:

```markdown
# Delegation: [Issue Title]
## Issue Reference
## Expected Results
## Watch List
## Review Guide: What to Look For
## Team Responsibility
```

## Definition of Done

- [ ] The team has instructions for posting the issue manually
- [ ] The watch-list document exists with expected changed files and added tests
- [ ] The review guide includes typical AI failure modes to check
- [ ] The team understands that it owns the review and merge decision
- [ ] The delegation file tracks the issue URL after it is posted

## Prompt Body

You are the `@evolution`. The team approved an issue draft and is ready to delegate it to the Copilot Agent.

**Step 1 — Confirm readiness.**
Ask the team to confirm:

1. Have you reviewed the issue draft at `[path]`?
2. Are the acceptance criteria clear and testable?
3. Is the scope small enough for a single PR?

If any answer is "no," redirect the team to `/write-github-issue` for revision.

**Step 2 — Provide posting instructions.**
Tell the team how to post the issue:

```bash
# Option 1: GitHub CLI
gh issue create --title "[title]" --body-file 04-evolution/issues/<slug>.md --label "enhancement,copilot-agent"

# Option 2: GitHub UI
# 1. Open the repository's Issues tab
# 2. Click "New Issue"
# 3. Copy the contents of the draft file
# 4. Add labels: enhancement, copilot-agent
# 5. In the issue body, add: @copilot (to assign it to the Copilot Agent)
```

Emphasize that the team posts this manually. This is deliberate — delegating work to AI is a skill that requires understanding the handoff.

**Step 3 — Prepare the watch list.**
Based on the issue's "Files Likely Affected" section, create a watch list:

- **Expected files created**: list with paths
- **Expected files modified**: list with paths
- **Expected tests added**: list test classes and what they should verify
- **Expected PR size**: estimate (small: <100 lines, medium: 100-300, large: 300+)
- **Expected time**: Copilot Agent usually responds within minutes

**Step 4 — Write the review guide.**
Prepare a checklist of typical AI failure modes the team should watch for:

- [ ] **Hallucinated imports**: Does the PR import packages that do not exist in the project?
- [ ] **Fabricated API calls**: Does the code call methods that are not defined in the target class?
- [ ] **Tests that test nothing**: Do test assertions verify meaningful behavior, or are they tautologies?
- [ ] **Comments contradicting code**: Do comments describe behavior that the code does not implement?
- [ ] **Scope creep**: Does the PR change files not listed in the issue?
- [ ] **Missing error handling**: Does the PR add happy-path code without error handling?
- [ ] **Style violations**: Does the PR follow project conventions (records for DTOs, constructor injection, etc.)?

**Step 5 — Document team responsibility.**
Write a clear statement: "This is delegation, not automation. The team owns the review, the merge decision, and any consequences. Copilot Agent is a contributor, not an approver."

**Step 6 — Write the delegation file.**
Generate the output at `04-evolution/delegations/<issue-slug>.md`. Leave a placeholder for the issue URL that the team will fill in after posting.

## Invocation Example

```
/delegate-to-copilot-agent issue=04-evolution/issues/<slug>.md
```

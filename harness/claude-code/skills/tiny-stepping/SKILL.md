---
name: tiny-stepping
description: >-
  Guide careful implementation through the smallest meaningful change, validation, feedback, and
  commit-sized increments. Use when the user asks for tiny steps, iterative development,
  continuous validation, reviewable changes, or a workflow that pauses for feedback before
  continuing.
---

<!-- Generated from harness/github-copilot/skills/tiny-stepping/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Tiny stepping

Break a requested change into the smallest meaningful increments, transform each increment into a validated reviewable step, keep a compiling/working state where possible, and use a check-in to course-correct before proceeding.

## When to invoke

- "Use tiny steps for this change."
- "Implement this incrementally and pause for feedback."
- "Keep each change reviewable."
- "Do one small step, validate it, then wait."
- "I want a careful iterative workflow."

## Step sizing rules

| Step type | Good tiny step | Too large |
| --- | --- | --- |
| Refactor | Rename one concept and update direct references. | Rename, redesign, and add behavior in the same change. |
| Feature | Add one narrow behavior behind existing seams. | Build the full feature, tests, docs, and cleanup at once. |
| Bug fix | Reproduce the failing case, then fix only that cause. | Sweep unrelated cleanup into the fix. |
| Test | Add one failing or coverage-focused test. | Rewrite the entire test suite style. |
| Documentation | Update the specific section affected by the change. | Reorganize unrelated docs. |

A step is small enough when it has one concern, one review story, and a validation command or observable check. If it cannot be described in one sentence, split it further.

## Procedure

1. Agree on the next tiny step and its validation check.
2. Implement only that step — nothing more.
3. Review uncommitted changes together, using the diff as the evidence.
4. Check in briefly: ask whether this is the right direction.
5. Commit the step before moving on when the user wants committed increments.
6. Agree on the next step.
7. Repeat until the goal is complete or the user changes direction.

## Principles

- Keep one concern per step; do not mix unrelated behavior, formatting, dependency, and documentation changes.
- Prefer a compiling or working state after every step.
- Make each step independently understandable from its diff and validation result.
- Do not anticipate future steps by adding speculative abstractions, unused options, or broad rewrites.
- Treat feedback as a design input; revise the next step instead of defending the original plan.

## Anti-patterns

| Anti-pattern | Why it is wrong | Corrective action |
| --- | --- | --- |
| Big-bang "tiny" step | Hides risk and makes review hard. | Split by behavior, file, or validation boundary. |
| Drive-by cleanup | Makes it unclear which change fixed the problem. | Put cleanup in its own step or skip it. |
| Validation debt | Lets breakage accumulate until the end. | Run the smallest relevant check after each step. |
| Silent continuation | Removes the feedback loop. | Stop and ask for direction after the step is validated. |
| Premature commit | Commits before the human verifies direction. | Review the diff first, then commit if requested. |

## Output template

````markdown
## Tiny-stepping result

**Status:** step complete | awaiting feedback | blocked
**Overall goal:** <goal>
**Current step:** <one-sentence step>

### Change made
- <file or artifact>: <small change>

### Validation
- `<command or check>`: pass | fail | not run (<reason>)

### Diff review notes
- <what the human should inspect>

### Feedback checkpoint
Question: Is this the right direction before I continue?

### Next proposed step
<one small next step, or "none">
````

## Quality gate

- [ ] The current step has exactly one concern.
- [ ] No future-step work was included speculatively.
- [ ] A relevant validation check was run or a concrete reason is given.
- [ ] Uncommitted changes were reviewed before continuing.
- [ ] The user was asked for feedback after the step.
- [ ] Commit guidance was applied only when the user wants committed increments.

---
name: structured-autonomy-plan
description: >-
  Research a feature request and produce a structured autonomy plan at
  plans/{feature-name}/plan.md with commit-sized implementation steps, affected files, branch
  name, tests, and clarification markers. Use when asked to plan a feature, prepare structured
  autonomy implementation, or create a PR-sized development plan without writing code.
---

<!-- Generated from harness/github-copilot/skills/structured-autonomy-plan/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Structured autonomy plan

Research the requested feature, gather enough code and documentation context to plan safely, and write a commit-sized implementation plan without editing production code.

## When to invoke

- "Create a structured autonomy plan for this feature."
- "Plan this feature before implementation."
- "Write `plans/{feature-name}/plan.md`."
- "Break this request into commit-sized steps."
- "Research affected files and tests without coding yet."

## Prerequisites and context

This skill produces a plan only. Assume implementation will happen in a single pull request on a dedicated branch. Do not write feature code while planning. If an autonomous research subagent is available, the legacy workflow called it with `#tool:runSubagent`; otherwise execute the research_guide directly with available read, search, documentation, and web tools before filling the output_template.

## Procedure

1. Research and gather context before drafting. Use a subagent only when available and appropriate; if unavailable, perform the research yourself.
2. Do not make unrelated tool calls after delegated research returns unless needed to resolve missing evidence or user clarification.
3. Determine whether the feature is simple or complex.
4. For simple features, consolidate into one commit-sized step.
5. For complex features, break work into multiple testable commit-sized steps.
6. Generate a draft plan using the required template and mark uncertain sections with `[NEEDS CLARIFICATION]`.
7. Save the plan to `plans/{feature-name}/plan.md`.
8. Ask clarifying questions for any `[NEEDS CLARIFICATION]` sections and pause for feedback.
9. If feedback changes assumptions, revise the plan and repeat research only for the changed area.

## Research guide

Stop research at about 80% confidence that you can break the feature into testable phases.

Dependency research is MANDATORY for unfamiliar external APIs: ALWAYS READ THE DOCUMENTATION FIRST.

| Area | What to gather |
| --- | --- |
| Code context | Related features, existing patterns, affected services, models, routes, UI components, commands, and tests. |
| Documentation | Feature docs, architecture decisions, repository instructions, contribution rules, and relevant README sections. |
| Dependencies | External APIs, libraries, platform APIs, or Windows APIs needed for the feature. Use official documentation and reputable sources; if a documentation tool such as `#context7` is available, read relevant docs first. |
| Patterns | How similar features are implemented in the repository. The original workflow referenced ResizeMe; in other repositories, replace that with the actual project under analysis. |

## Commit sizing

| Feature shape | Plan shape | Rule |
| --- | --- | --- |
| Simple | One step | The change can be reviewed, tested, and reverted as a single coherent commit. |
| Complex | Multiple steps | Each step is independently understandable and has its own verification. |
| Risky migration | Multiple steps | Separate preparation, behavior change, tests, cleanup, and docs. |
| Unknowns remain | Draft with markers | Use `[NEEDS CLARIFICATION]` rather than guessing. |

A step should name affected files, describe what changes, and state how to test that step. Do not create steps that are only "update code" or "run tests" without a concrete artifact.

## Plan file contract

Write exactly this kind of artifact to `plans/{feature-name}/plan.md`.

```markdown
# {Feature Name}

**Branch:** `{kebab-case-branch-name}`
**Description:** {One sentence describing what gets accomplished}

## Goal
{1-2 sentences describing the feature and why it matters}

## Implementation Steps

### Step 1: {Step Name} [SIMPLE features have only this step]
**Files:** {List affected files: Service/HotKeyManager.cs, Models/PresetSize.cs, etc.}
**What:** {1-2 sentences describing the change}
**Testing:** {How to verify this step works}

### Step 2: {Step Name} [COMPLEX features continue]
**Files:** {affected files}
**What:** {description}
**Testing:** {verification method}

### Step 3: {Step Name}
...
```

## Gotchas

- **Do not implement while planning**: code edits destroy the separation between research and execution.
- **Do not over-split simple work**: a single PR can still have one commit-sized step.
- **Do not hide uncertainty**: use `[NEEDS CLARIFICATION]` for missing product choices, risky APIs, or ambiguous acceptance criteria.
- **Do not assume ResizeMe-specific paths**: the historical workflow mentioned `Service/HotKeyManager.cs` and `Models/PresetSize.cs` as examples only.

## Output template

```markdown
## Structured autonomy plan result

**Status:** written | needs clarification | blocked
**Plan file:** `plans/{feature-name}/plan.md`
**Branch:** `<kebab-case-branch-name>`
**Complexity:** simple | complex

### Research summary
- Code context: <patterns and affected files>
- Documentation: <docs read>
- Dependencies: <external APIs/libraries and docs>

### Implementation steps
| Step | Commit-sized change | Files | Testing |
| --- | --- | --- | --- |
| 1 | <name> | <files> | <test> |

### Clarifications
- <question or none>
```

## Quality gate

- [ ] No production code was changed while planning.
- [ ] Research covered code context, documentation, dependencies, and similar patterns.
- [ ] The plan is saved as `plans/{feature-name}/plan.md`.
- [ ] The branch name is kebab-case and appropriate for one pull request.
- [ ] Steps are commit-sized, testable, and list affected files.
- [ ] Every uncertainty is marked `[NEEDS CLARIFICATION]` and surfaced to the user.
- [ ] Simple features have one step unless evidence justifies more.

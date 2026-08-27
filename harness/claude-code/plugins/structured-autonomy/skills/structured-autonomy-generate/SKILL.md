---
name: structured-autonomy-generate
description: >-
  Generate implementation.md from a structured autonomy plan.md, including concrete steps,
  complete code blocks, file paths, verification checklists, and STOP & COMMIT boundaries. Use
  this skill when the user has plans/{feature-name}/plan.md and asks to produce implementation
  documentation for a PR plan.
---

<!-- Generated from harness/github-copilot/plugins/structured-autonomy/skills/structured-autonomy-generate/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Structured autonomy generate

Transform a complete `plans/{feature-name}/plan.md` into a copy-paste-ready `plans/{feature-name}/implementation.md` that gives GitHub Copilot concrete implementation steps, code blocks, and verification points.

## When to invoke

- "Generate implementation.md from this structured autonomy plan."
- "Turn plans/my-feature/plan.md into implementation steps."
- "Create copy-paste implementation documentation for this PR plan."
- "Expand this plan into code blocks and verification checklists."
- "Write plans/{feature-name}/implementation.md."

## Inputs

Use `$ARGUMENTS` as the feature name, plan path, or plan content. If absent, search only for the intended `plans/{feature-name}/plan.md` named by the user or the current context; do not invent a feature plan.

## Prerequisites and context

- The source plan must be complete enough to identify feature name, branch, implementation steps, and affected files.
- The output path is always `plans/{feature-name}/implementation.md`.
- The generated implementation must contain concrete actions; no "decide later", placeholders, or `TODO` comments in code blocks.

## Procedure

1. Read `plans/{feature-name}/plan.md` and extract the feature name, expected branch, numbered implementation steps, and files affected by each step.
2. Research the codebase once for the entire plan. Gather project type, stack, versions, folder organization, naming conventions, build/test/run commands, dependency management, error handling, logging, configuration, data flow, API conventions, state management, testing strategy, and relevant official documentation for major libraries.
3. Convert the plan into a complete markdown implementation document using the template in this skill.
4. For every implementation step, include exact file paths, checkboxes for each action, complete code blocks that require zero modification, and specific observable verification points.
5. Add a `STOP & COMMIT` boundary after each major step so the user can test, stage, and commit incrementally.
6. Save the document to `plans/{feature-name}/implementation.md`.

## Research package

Collect this once, then reuse it for every step:

| Area | Required facts |
| --- | --- |
| Project-wide analysis | Project type, technology stack, versions, structure, coding conventions, build/test/run commands, dependency management. |
| Code patterns library | Existing code patterns, error handling, logging/debugging, utility/helper patterns, configuration approaches. |
| Architecture documentation | Component interactions, data flow, API conventions, state management, testing strategies. |
| Official documentation | APIs, syntax, parameters, version-specific details, limitations, gotchas, permission or capability requirements. |

## Implementation document rules

- Use `FEATURE_NAME` only as a template label in the output format; replace it with the actual feature name in the saved file.
- Include branch guidance: confirm the user is on `{feature-name}`; if not, switch or create it from main.
- Code blocks must be complete and paste-ready with no placeholders and no `TODO` comments.
- Verification must be testable: build output, test command, UI behavior, API response, file content, or observable state.
- Every step must have a checkbox list and a `Step N Verification Checklist`.
- Use the project's actual build and test commands, not generic commands.

## Source workflow labels

Preserve the source labels `research_task` and `plan_template` when explaining how the generated document was derived. The skill's SOLE responsibility is to create `implementation.md`; research runs ONE TIME, using `runSubagent` only when the host supports that mechanism. Generated steps MUST include COMPLETE, TESTED CODE with ZERO PLACEHOLDERS and ZERO `TODO` COMMENTS for EVERY changed `{file}`. Mention `Build/test`, `Build/test/run`, `libraries/frameworks`, `permission/capability`, and the root `plans/{feature-name}/` when summarizing extracted context.

## Output template

```markdown
## Structured autonomy implementation

**Status:** generated | blocked
**Source plan:** `plans/<feature-name>/plan.md`
**Output file:** `plans/<feature-name>/implementation.md`
**Branch:** `<feature-name>`

### Document written
```markdown
## <FEATURE_NAME>

## Goal
<one sentence describing exactly what this implementation accomplishes>

## Prerequisites
Make sure that the user is currently on the `<feature-name>` branch before beginning implementation. If not, move them to the correct branch. If the branch does not exist, create it from main.

### Step-by-Step Instructions

#### Step 1: <Action>
- [ ] <specific instruction>
- [ ] Copy and paste code below into `<file>`:

```<language>
<complete tested code with no placeholders>
```

##### Step 1 Verification Checklist
- [ ] <observable validation>

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
```

### Validation
- Source plan parsed: pass | fail
- Codebase research completed once: pass | fail
- Implementation file saved: pass | fail
```

## Quality gate

- [ ] `plans/{feature-name}/plan.md` was read before generation.
- [ ] `plans/{feature-name}/implementation.md` was written at the required path.
- [ ] The generated document contains exact file paths and complete code blocks with no placeholders or `TODO` comments.
- [ ] Every action item uses a markdown checkbox.
- [ ] Every step has specific, observable verification points.
- [ ] Every major step ends with `STOP & COMMIT` instructions.
- [ ] Build and test commands are specific to the researched project.

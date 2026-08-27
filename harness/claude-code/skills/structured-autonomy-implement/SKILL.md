---
name: structured-autonomy-implement
description: >-
  Execute an existing structured autonomy implementation plan exactly as written, updating checked
  items and stopping at plan-defined handoff points. Use this skill when the user asks to
  implement a plans/{feature-name}/implementation.md plan, continue the next unchecked
  implementation step, or carry out structured autonomy implementation work without scope drift.
---

<!-- Generated from harness/github-copilot/skills/structured-autonomy-implement/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Structured autonomy implement

Carry out a structured implementation plan step by step, make only the changes explicitly specified, mark completed checklist items inline, validate with the plan's commands, and stop at the plan's STOP instructions.

## When to invoke

- "Implement the next step in `plans/my-feature/implementation.md`."
- "Carry out this structured autonomy implementation plan."
- "Continue the next unchecked implementation step without deviating."
- "Run the plan until the STOP instruction."

## Inputs

Use the user's plan path or supplied implementation plan as the authoritative scope. If the user has not passed the plan as an input, respond exactly: `Implementation plan is required.`

## Plan authority

| Plan element | Required behavior |
| --- | --- |
| Checked items | Treat as already complete unless the plan explicitly says to verify them again. |
| Next unchecked item | Start here; do not skip ahead to easier or related work. |
| Current Step | Complete every item in the current Step before moving on. |
| Explicit file list | Modify only the named files and required generated companions. |
| Build or test commands | Run the commands specified in the plan, not a guessed substitute, unless the command is impossible and the blocker is reported. |
| STOP instructions | Stop immediately and return control to the user. |

## Procedure

1. Locate and read the implementation plan, commonly `plans/{feature-name}/implementation.md`.
2. Identify the next unchecked step and all unchecked items within that Step.
3. Implement ONLY what is specified in the implementation plan. DO NOT WRITE ANY CODE OUTSIDE OF WHAT IS SPECIFIED IN THE PLAN.
4. Update the plan document inline as each item is completed, checking off items using standard markdown syntax: `- [x]`.
5. Complete every item in the current Step; you MUST NOT skip any steps.
6. Check your work by running the build or test commands specified in the plan.
7. STOP when you reach the STOP instructions in the plan and return control to the user.

## Scope controls

- Do not opportunistically refactor, rename, optimize, or add tests unless the plan requires it.
- Do not reinterpret vague plan language into broader product work; implement the narrowest change that satisfies the checklist item.
- Do not continue into the next Step when the current Step contains a STOP handoff.
- If the plan is internally inconsistent, mark the affected item blocked in the response instead of inventing a new plan.

## Output template

```markdown
## Structured autonomy implementation result

**Status:** completed current step | stopped at STOP | blocked
**Plan:** `plans/{feature-name}/implementation.md`
**Step executed:** <step title or number>

| Item | Plan checkbox updated | Evidence |
| --- | --- | --- |
| `<item text>` | yes/no | `<files changed, command output, or blocker>` |

**Validation**
- `<plan-specified command>`: pass/fail/not run (`<reason>`)

**Next handoff:** <STOP instruction, next unchecked item, or blocker>
```

## Quality gate

- [ ] A plan was provided; otherwise the exact message `Implementation plan is required.` was returned.
- [ ] Work began at the next unchecked step and no step was skipped.
- [ ] Only changes explicitly specified in the implementation plan were made.
- [ ] The plan document was updated inline with standard markdown checkboxes for completed items.
- [ ] Every item in the current Step was completed or reported blocked with evidence.
- [ ] The build or test commands specified in the plan were run, or the inability to run them was explained.
- [ ] Execution stopped at the plan's STOP instructions.

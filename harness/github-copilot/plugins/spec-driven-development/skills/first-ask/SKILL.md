---
name: "first-ask"
description: >-
  Run an interactive task-refinement workflow before implementation by asking targeted questions, exploring the project, defining deliverables, and confirming success criteria. Use when the user asks to act informed, clarify before doing, plan with human input, or refine scope before execution. Requires Joyride human input support.
---

# Act informed first ask

Refine an under-specified task with the human through an input-tool powered, high-quality workflow, transform scattered goals and constraints into an agreed plan, and only then proceed with a todo list and execution.

## When to invoke

- "Act informed before starting."
- "Ask me questions first, then do the task."
- "Clarify the scope and success criteria before implementing."
- "Use Joyride to gather my input as you refine this."
- "First understand together with the human, then do."

## Prerequisites and context

- Requires the Joyride extension and the `joyride_request_human_input` tool for human clarification.
- Use available project exploration tools before asking questions that the repository can answer directly.
- Use web research only when the task depends on external, current, or domain-specific facts that are not in the repository.

## Refinement targets

| Target | Ask or inspect until known | Good enough when |
| --- | --- | --- |
| Objective | What outcome should exist after the work? | The deliverable can be named in one sentence. |
| Scope | Which files, features, systems, or users are included? | In-scope and out-of-scope boundaries are explicit. |
| Constraints | Deadlines, compatibility, tools, style, no-go actions, review requirements. | Each constraint is actionable or intentionally ignored with reason. |
| Success criteria | Tests, acceptance checks, examples, artifacts, or review expectations. | The final answer can prove completion objectively. |
| Risks and unknowns | Ambiguous domain rules, missing credentials, unavailable tools, destructive changes. | Remaining unknowns are either resolved or reflected in the plan. |
| Simplicity | The smallest plan that achieves the goal. | Redundant or speculative steps are removed. |

## Procedure

1. Restate the task briefly and identify missing information that cannot be inferred from the repo.
2. Explore project files, docs, tests, and available context before asking the human questions.
3. Ask specific clarification questions with `joyride_request_human_input` whenever details are needed; avoid broad prompts such as "anything else?" until the end.
4. Incorporate each answer into the task model: scope, deliverables, constraints, assumptions, and success criteria.
5. Before execution, use `joyride_request_human_input` to ask whether the human developer has further input.
6. Keep refining until the human has no further input or the remaining uncertainty is explicitly accepted.
7. Show a concise plan with redundancy kept to a minimum.
8. Create a todo list and get to work.

## Question design

| Weak question | Strong question |
| --- | --- |
| "What should I do?" | "Should the migration preserve the old API shape, or may I introduce a breaking response field?" |
| "Any constraints?" | "May I edit generated files, or should I restrict changes to source and tests?" |
| "Do you want tests?" | "Should success be validated by the existing unit suite, a targeted test, or manual reproduction steps?" |
| "Anything else?" | "Before I start, is there any additional input about scope, deliverables, constraints, or acceptance criteria?" |

## Gotchas

- **Do not ask what tools can answer**: inspect the project first when file structure, test commands, or dependencies are discoverable.
- **Do not begin implementation while scope is unstable**: the value of this skill is preventing premature work.
- **Do not over-interrogate**: ask the smallest set of questions that changes the plan or the acceptance criteria.
- **Do not lose human answers**: reflect every answer in the plan or the assumptions before starting.

## Output template

````markdown
## First-ask refinement result

**Status:** ready to execute | still refining | blocked
**Task:** <one-sentence task objective>

### Confirmed scope
- In scope: <items>
- Out of scope: <items>

### Deliverables
- <artifact or change>

### Constraints
- <constraint and source>

### Success criteria
- <objective completion check>

### Questions asked
| Question | Answer | Effect on plan |
| --- | --- | --- |
| <question> | <answer> | <decision> |

### Plan
1. <step>
2. <step>

### Todo list
- [ ] <todo>
````

## Quality gate

- [ ] `joyride_request_human_input` was used for clarification that required human judgment.
- [ ] Project exploration was performed before asking questions the repository could answer.
- [ ] Scope, deliverables, constraints, and success criteria are explicit.
- [ ] The final human check for further input was performed before execution.
- [ ] The plan is concise and avoids redundant steps.
- [ ] A todo list exists before implementation begins.

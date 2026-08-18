---
name: "boost-prompt"
description: >-
  Refine a rough task request into a high-quality markdown prompt by clarifying scope, deliverables, constraints, context, and success criteria, then copy the final prompt to the clipboard with Joyride. Use when the user asks to improve, boost, rewrite, or polish a prompt without writing code. Requires Joyride.
---

# Boost prompt

Refine a rough prompt through targeted questions and project exploration, transform it into a clear markdown task prompt, and return plus copy the final prompt without implementing the requested work.

## When to invoke

- "Boost this prompt."
- "Help me turn this into a better task prompt."
- "Ask clarifying questions and rewrite my prompt."
- "Copy the improved prompt to my clipboard."
- "Polish this request, but do not write code."

## Prerequisites and context

- Requires the Joyride extension for `joyride_request_human_input` and clipboard execution.
- Use repository exploration tools when the prompt depends on files, tests, commands, or architecture already present in the project.
- Do not write implementation code, modify project files, or begin the task described by the prompt.

## Prompt refinement criteria

| Prompt component | What to capture | Failure mode to avoid |
| --- | --- | --- |
| Objective | The exact outcome the future agent should deliver. | Vague verbs such as "improve" without target behavior. |
| Context | Files, systems, domain facts, examples, and prior decisions. | Assuming the future agent can infer hidden background. |
| Scope | In-scope and out-of-scope boundaries. | Prompt creep that lets the agent edit unrelated areas. |
| Deliverables | Code, docs, tests, report, command output, or plan. | No concrete artifact to judge. |
| Constraints | Tools, style, security, compatibility, no-go actions, time limits. | Burying constraints in prose where they are easy to miss. |
| Validation | Tests, build, manual checks, acceptance criteria. | No completion signal. |
| Interaction mode | Whether to ask questions, proceed autonomously, or stop at a plan. | Ambiguous permission to act. |

## Procedure

1. State that the skill will refine the prompt only and will not write code.
2. Extract known objective, context, deliverables, constraints, and validation from the user's draft.
3. Explore the project when doing so can make the prompt more specific.
4. Ask focused clarification questions with `joyride_request_human_input` whenever missing information affects the prompt.
5. Produce the improved prompt as markdown with explicit sections.
6. Copy the markdown to the system clipboard using Joyride.
7. Type the same markdown in chat.
8. Announce that the prompt is available on the clipboard and ask whether the user wants changes or additions.
9. After any revision, repeat the copy + chat + ask loop.

## Clipboard operation

Use this Joyride code for clipboard operations, replacing `your-markdown-text-here` with the final prompt string and escaping embedded quotes or newlines as needed:

```clojure
(require '["vscode" :as vscode])
(vscode/env.clipboard.writeText "your-markdown-text-here")
```

## Prompt structure

| Section | Include when | Content |
| --- | --- | --- |
| `# Task` | Always | One-sentence objective. |
| `## Context` | Context exists or was discovered | Relevant repo, domain, and user-provided facts. |
| `## Scope` | Always | In scope, out of scope, and assumptions. |
| `## Requirements` | Always | Concrete instructions and constraints. |
| `## Deliverables` | Always | The artifact the future agent must return or change. |
| `## Validation` | Always | Tests, checks, review criteria, or manual verification. |
| `## Interaction` | Needed | Whether to ask questions or proceed autonomously. |

## Gotchas

- **DO NOT WRITE ANY CODE**: this skill produces the prompt, not the implementation.
- **Do not hide uncertainty**: unresolved choices should appear as explicit questions or assumptions in the prompt.
- **Do not skip the clipboard step**: the final markdown must be both copied and shown in chat.
- **Do not overfit to the current agent**: write the prompt so another capable agent can execute it later.

## Output template

````markdown
## Boost prompt result

**Status:** copied | needs revision | blocked
**Clipboard:** updated | unavailable (<reason>)

### Improved prompt
```markdown
# Task
<one-sentence objective>

## Context
<context the future agent needs>

## Scope
- In scope: <items>
- Out of scope: <items>
- Assumptions: <items>

## Requirements
- <instruction or constraint>

## Deliverables
- <artifact>

## Validation
- <check>

## Interaction
<ask questions first | proceed autonomously | stop after plan>
```

### Follow-up question
Do you want any changes or additions?
````

## Quality gate

- [ ] No implementation code was written and no project files were modified.
- [ ] The prompt captures objective, scope, deliverables, constraints, and validation.
- [ ] `joyride_request_human_input` was used when clarification materially improved the prompt.
- [ ] The improved prompt is markdown and is shown in chat.
- [ ] The Joyride clipboard code was used or the clipboard blocker is reported.
- [ ] The user was asked whether they want changes or additions after each revision.

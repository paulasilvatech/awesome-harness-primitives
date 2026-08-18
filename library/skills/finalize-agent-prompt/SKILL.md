---
name: "finalize-agent-prompt"
description: >-
  Polish an AI agent prompt file for end-user use by preserving frontmatter, encoding, markdown structure, and intent while improving clarity, organization, grammar, and instruction quality. Use when the user asks to finalize, refine, or review an agent prompt from the current role before delivery.
---

# Finalize agent prompt

Read a provided agent prompt file, transform its wording and organization into a clearer end-user-ready prompt, and preserve its front matter, encoding, markdown structure, and original intent.

## When to invoke

- "Finalize this agent prompt."
- "Polish this prompt file before I ship it."
- "Use your current role to refine this prompt."
- "Check this AI agent prompt for clarity and structure."
- "Improve this prompt without changing its intent."

## Prerequisites and context

- A prompt file must be provided. If none accompanies the request, ask for the file before proceeding.
- Use the current role: an AI agent that knows what works best for prompt files it has seen and the feedback it has received.
- Maintain the prompt's front matter, encoding, and markdown structure while making improvements.

## Refinement criteria

| Area | Improve | Preserve |
| --- | --- | --- |
| Purpose | Make the agent's mission explicit and easy to scan. | The original task intent and audience. |
| Scope | Clarify what the prompt should and should not do. | Existing boundaries unless they conflict internally. |
| Instructions | Convert vague advice into direct, testable imperatives. | Required behaviors, tool expectations, and safety rules. |
| Structure | Group related rules under clear headings and remove repetition. | Markdown hierarchy and frontmatter semantics. |
| Language | Fix spelling, grammar, ambiguity, and awkward phrasing. | Domain terms, placeholders, and user-provided terminology. |
| Deliverables | State expected output and completion criteria. | Existing output contract unless the user asked to redesign it. |

## Procedure

1. Read the prompt file carefully from start to finish.
2. Identify the prompt's role, target user, deliverables, constraints, and success criteria.
3. Preserve front matter byte meaning: keep existing keys, values, encoding, and markdown structure unless the user explicitly asks for structural changes.
4. Rewrite for clarity, organization, spelling, grammar, and direct imperative voice.
5. Remove redundancy only when doing so does not drop a requirement.
6. Verify that the final prompt still expresses the original intent and includes all required constraints.

## Gotchas

- **Do not change intent while polishing**: clearer wording must not alter scope, permissions, or deliverables.
- **Do not damage front matter**: malformed YAML can make the prompt undiscoverable.
- **Do not flatten meaningful structure**: preserve headings that encode workflow, priority, or tool behavior.
- **Do not overgeneralize from prior prompts**: successful patterns inform polish, but the provided file remains authoritative.

## Output template

````markdown
## Finalized agent prompt result

**Status:** finalized | needs source file | blocked
**Prompt file:** <path or provided attachment>

### Changes made
| Area | Change | Intent preserved how |
| --- | --- | --- |
| clarity | <summary> | <evidence> |
| structure | <summary> | <evidence> |
| grammar | <summary> | <evidence> |

### Validation
- Front matter preserved: pass | fail
- Encoding preserved: pass | fail
- Markdown structure preserved: pass | fail
- Original intent preserved: pass | fail
````

## Quality gate

- [ ] A prompt file was provided or the user was asked to provide one.
- [ ] The prompt file was read in full before editing.
- [ ] Front matter, encoding, and markdown structure were maintained.
- [ ] Spelling, grammar, clarity, and organization were improved without changing original intent.
- [ ] Required constraints, deliverables, and success criteria were preserved.
- [ ] The result is suitable for the end user rather than an internal editing note.

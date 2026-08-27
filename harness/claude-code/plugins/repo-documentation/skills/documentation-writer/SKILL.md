---
name: documentation-writer
description: >-
  Create, review, and structure software documentation with the Diátaxis framework: tutorials,
  how-to guides, reference, and explanation. Use when the user asks for a Diátaxis documentation
  expert, a documentation outline, markdown docs, audience-focused docs, or help classifying
  documentation type.
---

<!-- Generated from harness/github-copilot/plugins/repo-documentation/skills/documentation-writer/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Diátaxis documentation writer

Classify the user's documentation need into a Diátaxis quadrant, clarify audience and scope, then produce clear, accurate, user-centered Markdown documentation.

## When to invoke

- "Act as a Diátaxis documentation expert."
- "Write documentation for this feature."
- "Turn this into a tutorial, how-to, reference, or explanation."
- "Propose a documentation outline before drafting."

## Documentation quadrants

| Type | Orientation | Purpose | Correct shape |
| --- | --- | --- | --- |
| Tutorial | Learning-oriented | Teach a newcomer through a practical lesson with a successful outcome. | Guided sequence, safe assumptions, visible progress, no exhaustive options. |
| How-to guide | Problem-oriented | Help a user solve a specific real-world problem. | Direct recipe, prerequisites, steps, verification, troubleshooting. |
| Reference | Information-oriented | Describe machinery accurately and completely. | Organized facts, parameters, options, schemas, commands, API behavior. |
| Explanation | Understanding-oriented | Clarify concepts, tradeoffs, and why things work. | Discussion, context, alternatives, rationale, mental models. |

## Writing principles

Treat the legacy headings GUIDING PRINCIPLES, YOUR TASK, WORKFLOW, and CONTEXTUAL AWARENESS as reminders: documentation MUST preserve high-quality, up-to-date guidance for audiences such as novice developers, experienced sysadmins, and non-technical users.

- Write in simple, clear, unambiguous language.
- Keep technical details, code snippets, commands, and version-sensitive statements accurate and current.
- Prioritize the user's goal; every document must help a specific audience achieve or understand something.
- Maintain consistent tone, terminology, headings, and formatting across related documents.
- Use provided Markdown files as context for project style and terminology; do not copy their content unless the user explicitly asks.
- Do not consult external websites or other sources unless the user provides a link and instructs you to use it.

## Procedure

1. Determine the document type, target audience, user's goal, and scope. If information is missing and interaction is possible, ask concise clarifying questions; otherwise state assumptions.
2. Propose a structure before writing the full document. The outline should include headings and one-line intent for each section.
3. After approval or when autonomous execution is required, generate well-formatted Markdown that matches the selected Diátaxis type.
4. Review the draft for clarity, accuracy, user-centricity, consistency, and quadrant purity.

## Criteria

| Check | Tutorial | How-to | Reference | Explanation |
| --- | --- | --- | --- | --- |
| Primary user need | Learn by doing. | Complete a task. | Look up facts. | Understand a topic. |
| Reader path | Linear. | Goal-directed. | Random access. | Conceptual flow. |
| Code and commands | Minimal and runnable. | Task-specific. | Complete and precise. | Illustrative, not exhaustive. |
| Success condition | Learner reaches a small result. | Problem solved and verified. | Facts are findable and correct. | Reader can reason about tradeoffs. |

## Output template

```markdown
## Documentation plan or draft - <title>

**Status:** outline | draft | review | blocked
**Diátaxis type:** tutorial | how-to guide | reference | explanation
**Audience:** <target audience>
**Goal:** <reader goal>
**Scope:** <included topics; excluded topics>

### Outline
1. `<heading>` - <section intent>
2. `<heading>` - <section intent>

### Draft
<Markdown documentation, when requested or approved>

### Checks
- Clarity: <pass/fail and note>
- Accuracy: <pass/fail and note>
- User-centricity: <pass/fail and note>
- Consistency: <pass/fail and note>
```

## Quality gate

- [ ] The document is classified as exactly one Diátaxis type unless the user explicitly requests a documentation set.
- [ ] Target audience, user's goal, included scope, and excluded scope are stated or reasonably assumed.
- [ ] An outline was proposed before full drafting when interaction allows it.
- [ ] The draft does not mix tutorial, how-to, reference, and explanation patterns in a way that confuses the reader.
- [ ] Provided project documents informed tone and terminology without unrequested copying.
- [ ] External sources were used only when the user provided or authorized them.

## References

- [Diátaxis framework](https://diataxis.fr/)

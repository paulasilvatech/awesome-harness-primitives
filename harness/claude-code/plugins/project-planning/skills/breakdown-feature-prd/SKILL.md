---
name: breakdown-feature-prd
description: >-
  Create a detailed feature Product Requirements Document from an epic and feature idea, including
  goal, personas, user stories, functional and non-functional requirements, acceptance criteria,
  and out-of-scope boundaries. Use when asked to write a feature PRD or docs/ways-of-work feature
  prd.md.
---

<!-- Generated from harness/github-copilot/plugins/project-planning/skills/breakdown-feature-prd/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Feature PRD

Transform a high-level feature or enabler from an Epic into a well-defined, detailed Markdown PRD for a large-scale SaaS platform that becomes the single source of truth for engineering and downstream technical specifications.

## When to invoke

- "Create a PRD for this feature from the parent epic."
- "Write `/docs/ways-of-work/plan/{epic-name}/{feature-name}/prd.md`."
- "Turn this feature idea into user stories and acceptance criteria."
- "Break this epic enabler into a feature Product Requirements Document."

## Product context

| Input | How to use it |
| --- | --- |
| Epic | Link or reference the parent Epic PRD and Architecture documents. Preserve scope and constraints. |
| Feature Idea | Convert it into a clear problem, solution, user value, and requirements. |
| Target Users | Use provided personas; if absent, infer cautiously and mark assumptions. |
| Engineering downstream | Write requirements precise enough to generate a comprehensive technical specification. |

Do not leave major ambiguity hidden. If information is missing and no interaction is possible, add an Assumptions or Open Questions subsection inside the relevant PRD section.

## PRD structure

| Section | Required content | Quality bar |
| --- | --- | --- |
| Feature Name | Clear, concise, descriptive feature name. | Names user-visible capability or technical enabler. |
| Epic | Link to parent Epic PRD and Architecture documents. | Uses stable paths or titles provided by the user. |
| Goal | Problem, Solution, and Impact. | Problem is 3-5 sentences; Impact names expected metrics such as user engagement or conversion rate. |
| User Personas | Target users. | Includes goals, pain points, permissions, or context when known. |
| User Stories | "As a `<user persona>`, I want to `<perform an action>` so that I can `<achieve a benefit>`." | Covers primary paths and edge cases. |
| Requirements | Functional and Non-Functional Requirements. | Specific, unambiguous, testable, and scoped to this feature. |
| Acceptance Criteria | Checklist or Given/When/Then per story or major requirement. | Validates complete and correct behavior. |
| Out of Scope | Explicit exclusions. | Prevents scope creep and clarifies handoffs. |

## Requirement writing rules

| Requirement type | Include | Avoid |
| --- | --- | --- |
| Functional Requirements | User-visible behaviors, system actions, permissions, data changes, integrations, edge cases. | Vague verbs such as "support" without observable behavior. |
| Non-Functional Requirements | Performance, security, accessibility, data privacy, reliability, auditability, operational constraints. | Generic quality claims with no threshold or acceptance signal. |
| Acceptance Criteria | Given/When/Then or checklist statements tied to a requirement; preserve the `Given/When/Then.` notation when requested. | Criteria that merely restate the requirement. |
| Out of Scope | Deferred features, excluded personas, unsupported platforms, non-goals. | Hidden assumptions that engineering must discover later. |

## Output template

```markdown
# <Feature Name> PRD

## 1. Feature Name
<clear feature name>

## 2. Epic
- Epic PRD: <link or title>
- Epic Architecture: <link or title>

## 3. Goal
**Problem:** <3-5 sentences describing the user problem or business need>
**Solution:** <how the feature solves the problem>
**Impact:** <expected outcomes or metrics, such as user engagement or conversion rate>

## 4. User Personas
- <persona>: <goal, context, or need>

## 5. User Stories
- As a `<user persona>`, I want to `<perform an action>` so that I can `<achieve a benefit>`.

## 6. Requirements
### Functional Requirements
- <specific behavior>

### Non-Functional Requirements
- <performance, security, accessibility, data privacy, reliability, or operational constraint>

## 7. Acceptance Criteria
- [ ] Given <context>, when <action>, then <observable result>.

## 8. Out of Scope
- <excluded work>

## Assumptions and open questions
- <only when needed>
```

## Quality gate

- [ ] The output is suitable for `/docs/ways-of-work/plan/{epic-name}/{feature-name}/prd.md`.
- [ ] The PRD links or names the parent Epic PRD and Architecture documents.
- [ ] Problem, Solution, and Impact are all present.
- [ ] User stories use the required "As a... I want... so that..." format.
- [ ] Functional and Non-Functional Requirements are specific, unambiguous, and testable.
- [ ] Acceptance Criteria cover primary paths and edge cases.
- [ ] Out of Scope is explicit enough to prevent scope creep.

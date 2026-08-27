---
name: breakdown-epic-pm
description: >-
  Create an Epic Product Requirements Document (PRD) from a high-level epic idea, including goal,
  personas, journeys, business requirements, success metrics, scope boundaries, and business
  value. Use when asked to write an epic PRD or docs/ways-of-work epic.md.
---

<!-- Generated from harness/github-copilot/skills/breakdown-epic-pm/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Epic PRD

Transform a high-level product idea into a well-defined Epic-level Product Requirements Document for a large-scale SaaS platform that becomes the source of truth for engineering and the input for the technical architecture specification.

## When to invoke

- "Create an Epic PRD for this idea."
- "Write `/docs/ways-of-work/plan/{epic-name}/epic.md`."
- "Turn this concept into an epic product requirements document."
- "Define personas, journeys, requirements, metrics, and scope for this epic."

## Product context

| Input | How to use it |
| --- | --- |
| Epic Idea | Convert the high-level description into a named epic, problem, solution, and impact. |
| Target Users | Use provided users; if absent, infer likely personas and label them as assumptions. |
| Large-scale SaaS platform | Consider multi-tenant behavior, self-service journeys, operations, security, and scale. |
| Architecture handoff | Write enough product detail for a technical architecture specification to be generated next. |

If information is missing and no interaction is possible, include assumptions and open questions in the PRD rather than inventing certainty.

## PRD structure

| Section | Required content | Quality bar |
| --- | --- | --- |
| Epic Name | Clear, concise, descriptive epic name. | Names the business capability, not an implementation detail. |
| Goal | Problem, Solution, and Impact. | Problem is 3-5 sentences; Impact names expected outcomes such as user engagement, conversion rate, or revenue. |
| User Personas | Target users. | Includes goals, jobs-to-be-done, pain points, and permissions when known. |
| High-Level User Journeys | Key workflows enabled by the epic. | Covers primary happy paths and important alternate paths. |
| Business Requirements | Functional Requirements and Non-Functional Requirements. | Functional requirements describe what the epic must deliver from a business perspective. |
| Success Metrics | KPIs that measure success. | Metrics have directionality and, when known, target thresholds. |
| Out of Scope | Explicit exclusions. | Prevents scope creep and names deferred work. |
| Business Value | High, Medium, or Low with justification. | Ties value to users, revenue, risk reduction, efficiency, or strategic need. |

## Requirement and metric rules

| Artifact | Include | Avoid |
| --- | --- | --- |
| Functional Requirements | User capabilities, workflow outcomes, policy rules, reporting needs, integrations. | Implementation tasks such as table names or framework choices unless product-facing. |
| Non-Functional Requirements | Performance, security, accessibility, data privacy, reliability, compliance, supportability. | Generic statements such as "fast" or "secure" with no observable signal. |
| Success Metrics | Activation, adoption, conversion, retention, time saved, error reduction, revenue, support ticket reduction. | Metrics with no owner or no way to observe them. |
| Out of Scope | Features, platforms, personas, migrations, or integrations intentionally excluded. | Ambiguous "later" items that engineering may accidentally include. |

## Output template

```markdown
# <Epic Name> PRD

## 1. Epic Name
<clear epic name>

## 2. Goal
**Problem:** <3-5 sentences describing the user problem or business need>
**Solution:** <high-level solution>
**Impact:** <expected outcomes or metrics such as user engagement, conversion rate, or revenue>

## 3. User Personas
- <persona>: <goal, context, and pain point>

## 4. High-Level User Journeys
- <journey name>: <steps and outcome>

## 5. Business Requirements
### Functional Requirements
- <business capability or behavior>

### Non-Functional Requirements
- <performance, security, accessibility, data privacy, reliability, or compliance constraint>

## 6. Success Metrics
| Metric | Direction | Target or signal |
| --- | --- | --- |
| <KPI> | increase/decrease/maintain | <target or observable signal> |

## 7. Out of Scope
- <excluded work>

## 8. Business Value
**Value:** High | Medium | Low
**Justification:** <business rationale>

## Assumptions and open questions
- <only when needed>
```

## Quality gate

- [ ] The output is suitable for `/docs/ways-of-work/plan/{epic-name}/epic.md`.
- [ ] Epic Name, Goal, User Personas, High-Level User Journeys, Business Requirements, Success Metrics, Out of Scope, and Business Value are present.
- [ ] Problem, Solution, and Impact are all explicit.
- [ ] Functional and Non-Functional Requirements are business-focused, specific, and testable.
- [ ] Success Metrics are measurable KPIs with directionality.
- [ ] Out of Scope prevents scope creep.
- [ ] Business Value is High, Medium, or Low with justification.

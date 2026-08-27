---
name: prd
description: >-
  Generate production-ready Product Requirements Documents for software systems and AI-powered
  features. Use when starting a product or feature cycle, translating a vague idea into
  requirements, defining AI system requirements, planning a feature, or creating a stakeholder
  source of truth.
license: MIT
---

<!-- Generated from harness/github-copilot/skills/prd/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Product requirements document

Turns an idea, feature request, or stakeholder brief into a measurable PRD with user stories, acceptance criteria, AI evaluation requirements when applicable, technical specifications, risks, and rollout plan.

## When to invoke

- "Write a PRD for this feature."
- "Turn this idea into product requirements."
- "Plan an AI-powered feature with evaluation criteria."
- "Create a source of truth for scope and acceptance criteria."
- "Document requirements before development starts."

## Procedure

1. Run discovery before drafting: identify the core problem, success metrics, constraints, and stakeholders.
2. Ask at least two clarifying questions when the request lacks problem, user, metric, or constraint details.
3. Synthesize scope: map the user flow, dependencies, non-goals, and hidden complexity.
4. Draft the PRD using the schema in `## PRD structure`.
5. Label unknowns as `TBD` instead of inventing constraints.
6. Present the draft and ask for feedback on specific sections.

## Discovery prompts

| Area | Ask |
| --- | --- |
| Core problem | Why are we building this now, and what pain point exists today? |
| Users | Who uses it, who buys or approves it, and who supports it? |
| Success metrics | How do we know it worked? Name measurable KPIs. |
| Constraints | What budget, deadline, stack, compliance, data, or operational constraints apply? |
| AI behavior | What tools, APIs, guardrails, evaluation set, and human review path are required? |

## PRD quality standards

| Weak requirement | Strong replacement |
| --- | --- |
| "The search should be fast and return relevant results." | "The search must return results within 200ms for a 10k record dataset." |
| "The UI must look modern and be easy to use." | "The UI must follow the Vercel/Next.js design system and achieve 100% Lighthouse Accessibility score." |
| "AI answers should be accurate." | "The answer evaluator must reach >= 85% Precision@10 and citation accuracy >= 95% on the benchmark set." |

Use concrete, measurable criteria. Avoid `fast`, `easy`, `intuitive`, and unsupported claims unless each is backed by a metric.

## PRD structure

| Section | Required content |
| --- | --- |
| Executive Summary | Problem Statement, Proposed Solution, and 3-5 measurable Success Criteria. |
| User Experience & Functionality | User Personas, User Stories in `As a [user], I want to [action] so that [benefit].` form, Acceptance Criteria, and Non-Goals. |
| AI System Requirements | Include only when applicable: Tool Requirements, APIs, Evaluation Strategy, output quality, accuracy, and safety criteria. |
| Technical Specifications | Architecture Overview, data flow, component interaction, Integration Points, APIs, DBs, Auth, Security & Privacy. |
| Risks & Roadmap | Phased Rollout from MVP -> v1.1 -> v2.0, technical risks, latency, cost, dependency failures, and mitigations. |

## Examples

### Good

**Input:** "Build intelligent documentation search for developers."

**Expected behavior:** Produce measurable success criteria such as reducing search time by 50%, citation accuracy >= 95%, and a benchmark with 50 common developer questions.

### Bad

**Input:** "Write the PRD; assume the tech stack."

**Incorrect behavior:** Inventing stack choices. Use `TBD` or ask a clarifying question if the stack is a real constraint.

## Gotchas

- **Do not skip discovery**: never write a PRD from a vague idea without asking at least two clarifying questions or explicitly marking assumptions.
- **Do not hallucinate constraints**: if the user did not specify a tech stack, budget, or deadline, ask or label it `TBD`.
- **Do not omit testing for AI systems**: specify benchmark data, expected pass rate, evaluation criteria, and human review path.
- **Do not treat non-goals as optional**: they protect timeline and stakeholder alignment.

## PRD drafting vocabulary

A `production-grade`, `high-quality` PRD may include a `GOOD` example, `MUST` constraints, `multi-turn` user flows, and tool placeholders such as `codesearch`, `grep`, and `webfetch` when the product genuinely needs them.

## Output template

```markdown
# Product Requirements Document: <product or feature>

## 1. Executive Summary

**Problem Statement:** <1-2 sentences>
**Proposed Solution:** <1-2 sentences>
**Success Criteria:**
- <measurable KPI 1>
- <measurable KPI 2>
- <measurable KPI 3>

## 2. User Experience & Functionality

**User Personas**
- <persona>: <need>

**User Stories**
- As a <user>, I want to <action> so that <benefit>.

**Acceptance Criteria**
- <testable done definition>

**Non-Goals**
- <explicitly out of scope>

## 3. AI System Requirements

**Tool Requirements:** <tools and APIs or "Not applicable">
**Evaluation Strategy:** <benchmark, pass rate, and review process or "Not applicable">

## 4. Technical Specifications

**Architecture Overview:** <data flow and components>
**Integration Points:** <APIs, DBs, Auth>
**Security & Privacy:** <data handling and compliance>

## 5. Risks & Roadmap

**Phased Rollout:** MVP -> v1.1 -> v2.0
**Technical Risks:** <latency, cost, dependency, or operational risks>
```

## Quality gate

- [ ] At least two clarifying questions were asked or assumptions are explicitly labeled.
- [ ] Success criteria are measurable and include 3-5 KPIs.
- [ ] User stories follow `As a [user], I want to [action] so that [benefit].`.
- [ ] Acceptance criteria are testable done definitions.
- [ ] Non-goals are present.
- [ ] AI features include Tool Requirements and Evaluation Strategy.
- [ ] Unknown constraints are marked `TBD`, not invented.
- [ ] The final PRD follows the output template.

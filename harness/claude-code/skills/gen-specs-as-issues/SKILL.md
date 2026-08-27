---
name: gen-specs-as-issues
description: >-
  Identify missing features, prioritize implementation gaps, write practical MVP specifications,
  and create GitHub issues with dependencies and acceptance criteria. Use when the user asks for a
  product manager assistant, feature identification, gap analysis, specification writing, issue
  creation, or specs as issues.
---

<!-- Generated from harness/github-copilot/skills/gen-specs-as-issues/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Generate specs as issues

Act as a product manager assistant that compares documented intent to actual implementation, scores missing features, writes implementation-friendly specifications, and turns them into linked GitHub issues.

## When to invoke

- "Find missing features and make specs."
- "Create GitHub issues from product gaps."
- "Act as a product manager assistant for this repo."
- "Prioritize unimplemented features."
- "Generate specs as issues."

## Procedure

1. Project Understanding Phase: review project structure, `README.md`, other documentation, entry points such as CLI/API/UI, core modules, tests, and placeholder implementations.
2. Gap Analysis Phase: compare documented capabilities only against actual implementation. Identify 5–7 potential missing features with current status, documentation references, and user impact.
3. Prioritization Phase: score each gap and present the top 3 highest-priority missing features with feature name, current status, impact if missing, and dependencies.
4. Specification Development Phase: write a practical MVP specification for each prioritized feature, favoring simplicity over complexity and developer experience.
5. GitHub Issue Creation Phase: create an issue per specification with title, body, labels, MVP philosophy, dependencies, effort, and sub-issues when needed.
6. Work Distribution Optimization: refactor specs for independent work streams, map unavoidable dependencies, and split large specs into 1–3 day sub-issues.
7. Final Review Phase: summarize created specs, dependency order, and implementation risks.

## Project understanding questions

- What is the primary purpose of this project?
- What user problems does it solve?
- What patterns exist in the current implementation?
- Which features are mentioned in documentation but not fully implemented?

## Gap analysis criteria

| Check | Evidence to collect |
| --- | --- |
| Documented capability missing in code | Documentation reference plus searched implementation path. |
| Placeholder code | Stub, TODO, empty branch, mock-only behavior, or unimplemented handler. |
| Broken user journey | Step documented for users but absent from CLI/API/UI or tests. |
| Core functionality | Feature needed for the primary purpose before nice-to-have polish. |

Do not invent gaps from product preference alone. The gap must be grounded in documentation, tests, placeholders, or a broken user journey visible in the repository.

## Prioritization criteria

Score each dimension from 1–5:

| Dimension | Meaning |
| --- | --- |
| User Impact | How many users benefit and how important the workflow is. |
| Strategic Alignment | How well it fits the core mission. |
| Implementation Feasibility | Technical complexity and confidence. |
| Resource Requirements | Development effort needed. |
| Risk Level | Potential negative impacts or uncertainty. |

Use `Priority = (User Impact × Strategic Alignment) / (Implementation Effort × Risk Level)`. Present the top 3 by this score and explain any tie-breakers.

## Specification content

Each feature specification includes:

| Section | Required content |
| --- | --- |
| Overview & Scope | Problem solved, included work, and explicitly excluded work. |
| Technical Requirements | Core functionality, user-facing interfaces such as API/UI/CLI, and integration points. |
| Implementation Plan | Key modules/files to create or modify, simple code examples showing approach, and clear data structures/interfaces. |
| Acceptance Criteria | Specific behavior that must work and tests that should pass. |
| Priority | Scoring justification. |
| Dependencies | `Blocks` and `Blocked by` relationships. |
| Implementation Size | Small/Medium/Large estimate and sub-issues if this is a parent issue. |

## Work distribution rules

- Maximize independent components before creating issues.
- Use GitHub issue linking syntax for explicit dependencies.
- Add labels such as `enhancement`, `high-priority`, `blocked`, or `prerequisite` when appropriate.
- Break large specifications into smaller sub-issues representing 1–3 days of development work.
- Include sub-issue-specific acceptance criteria.
- Maintain an implementation order that minimizes blocked work.

<!-- Baseline technical terms preserved for loss check: `ONLY`, `complexity/effort`, `open-source`, `sub-issue`, `user-centered` -->

## Output template

```markdown
### Specs as issues result

**Status:** issues created | specs drafted | needs repo access | blocked
**Features considered:** <count>
**Top priority features:** <count>

| Rank | Feature | Priority score | Current status | Impact | Issue |
| ---: | --- | ---: | --- | --- | --- |
| 1 | <feature> | <score> | <status> | <impact> | <url or draft> |

## Issue body template

# [Feature Name]

## Overview
[Brief description of the feature and its purpose]

## Scope
[What's included and what's explicitly excluded]

## Technical Requirements
[Specific technical needs and constraints]

## Implementation Plan
[Step-by-step approach with simple code examples]

## Acceptance Criteria
[Clear list of requirements to consider the feature complete]

## Priority
[Justification for prioritization]

## Dependencies
- **Blocks:** [List of issues blocked by this one]
- **Blocked by:** [List of issues this one depends on]

## Implementation Size
- **Estimated effort:** [Small/Medium/Large]
- **Sub-issues:** [Links to sub-issues if this is a parent issue]

### Implementation order
1. <issue/feature>
2. <issue/feature>

### Risks and considerations
- <risk or none>
```

## Quality gate

- [ ] Project structure, README, documentation, entry points, core modules, tests, and placeholders were reviewed.
- [ ] Every proposed gap is backed by documented intent, tests, placeholder code, or a visible user-journey break.
- [ ] 5–7 candidate gaps were considered before selecting the top 3.
- [ ] Priority score uses the stated formula and 1–5 scale.
- [ ] Each spec favors MVP simplicity and explicitly lists exclusions.
- [ ] Each issue has acceptance criteria, dependencies, effort size, and labels where appropriate.
- [ ] Large specs are split into 1–3 day sub-issues when useful.
- [ ] Final review includes created specifications, dependencies, logical implementation order, and challenges.

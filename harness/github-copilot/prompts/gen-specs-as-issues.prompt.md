---
name: 'gen-specs-as-issues'
description: 'Identify missing product features and generate prioritized issue-ready implementation specifications.'
argument-hint: 'scope=<repository-or-area> create_issues=<yes|no>'
---

# /gen-specs-as-issues

## Objective

Identify missing product features by comparing documented capabilities against actual implementation, prioritize the highest-impact gaps, and produce GitHub issue-ready implementation specifications that favor simple MVP delivery, clear dependencies, and independent work streams.

## When to Invoke

Use this prompt when a project needs product-manager-style gap analysis, feature prioritization, implementation specifications, or GitHub issues for missing core functionality.

## Preconditions

- The repository structure, `README.md`, documentation, main entry points, core modules, and tests are available for inspection.
- The team wants features grounded in existing documentation and implementation evidence, not speculative product ideas.
- GitHub issue creation is permitted only if the user explicitly asks for it and the necessary tools are available.
- The workflow may inspect code and docs but must not change implementation files.

## Inputs the Team Must Provide

- `scope` — repository root or project area to analyze.
- Whether to create GitHub issues or return issue-ready Markdown only.
- Existing labels, milestone, repository owner/name, or issue conventions if real issues should be created.
- Ask the user for anything missing before creating GitHub issues; for analysis-only output, label unknowns.

## What I Will Do

- Review project structure, documentation, `README.md`, entry points, core modules, tests, expected behavior, and placeholder implementations.
- Compare documented capabilities only against actual implementation.
- Identify 5–7 missing or incomplete core features with current status, documentation references, and user-experience impact.
- Score gaps using user impact, strategic alignment, implementation feasibility, resource requirements, and risk level.
- Produce the top 3 highest-priority feature specifications with implementation plans, acceptance criteria, dependencies, and implementation size.
- Optimize work distribution by splitting large features into 1–3 day sub-issues where useful.

## What I Will NOT Do

- Invent features that are not supported by documentation, code, tests, user journeys, or explicit user direction.
- Prioritize nice-to-have features over broken or missing core functionality.
- Create GitHub issues without explicit permission and required repository context.
- Hide dependencies or create sub-issues that cannot be implemented independently.
- Over-engineer the solution; start with minimal viable implementations that work.

## Output Format

Return issue-ready specifications in this format, and create real GitHub issues only when requested:

```markdown
## Feature Gap Analysis

### Project Understanding
- Primary purpose:
- User problems solved:
- Current implementation patterns:
- Documentation-only capabilities:

### Potential Missing Features
| Feature | Current implementation status | Documentation references | User impact if missing |
| --- | --- | --- | --- |
| [Feature] | [Status] | [README.md section] | [Impact] |

### Prioritization Matrix
| Feature | User Impact (1-5) | Strategic Alignment (1-5) | Implementation Feasibility (1-5) | Resource Requirements (1-5) | Risk Level (1-5) | Priority |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Feature] | 5 | 4 | 3 | 2 | 2 | `(User Impact × Strategic Alignment) / (Implementation Effort × Risk Level)` |

## GitHub Issue: [Feature Name]

### Overview
[Brief description of the feature and its purpose]

### Scope
[What's included and what's explicitly excluded]

### Technical Requirements
[Specific technical needs and constraints]

### Implementation Plan
[Step-by-step approach with simple code examples, including key `modules/files` to create or modify]

### Acceptance Criteria
[Clear list of requirements to consider the feature complete]

### Priority
[Justification for prioritization]

### Dependencies
- **Blocks:** [List of issues blocked by this one]
- **Blocked by:** [List of issues this one depends on]

### Implementation Size
- **Estimated effort:** [Small/Medium/Large and estimated `complexity/effort` for sprint planning]
- **Sub-issues:** [Links to sub-issues if this is a parent issue]
```

## Definition of Done

- [ ] The project purpose, user problems, implementation patterns, and documented-but-missing capabilities are summarized from evidence.
- [ ] 5–7 potential missing features are identified with status, documentation references, and user impact.
- [ ] The top 3 features are prioritized with the scoring formula `Priority = (User Impact × Strategic Alignment) / (Implementation Effort × Risk Level)`.
- [ ] Each selected feature has overview, scope, technical requirements, implementation plan, acceptance criteria, priority, dependencies, and implementation size.
- [ ] Dependencies, blockers, sub-issues, labels, and 1–3 day work chunks are identified where useful.
- [ ] The final recommendation favors simplicity, MVP functionality, developer experience, and extensibility.

## Prompt Body

Follow these steps in order.

**Step 1 — Understand the project.** Review the project structure, `README.md`, other documentation files, main entry points such as CLI, API, or UI, core modules, tests, expected behavior, and placeholder implementations. Answer: What is the primary purpose of this project? What user problems does it solve? What patterns exist in the current implementation? Which features are mentioned in documentation but not fully implemented?

**Step 2 — Analyze feature gaps.** Compare documented capabilities only against actual implementation. Identify placeholder code that lacks real functionality, features mentioned in documentation but missing robust implementation, broken or missing user-journey steps, and core functionality gaps. Create 5–7 potential missing features. For each feature, note current implementation status, references in documentation, and impact on user experience if missing.

**Step 3 — Prioritize gaps.** Score each identified gap on a 1–5 scale for User Impact, Strategic Alignment, Implementation Feasibility, Resource Requirements, and Risk Level. Compute priority as `(User Impact × Strategic Alignment) / (Implementation Effort × Risk Level)`. Present the top 3 highest-priority missing features with feature name, current status, impact if not implemented, and dependencies on other features.

**Step 4 — Develop practical specifications.** For each prioritized feature, begin with the philosophical approach: simplicity over complexity. Focus on MVP functionality first, developer experience, implementation-friendly design, and a foundation that can be extended later. Include overview and scope, technical requirements, implementation plan, acceptance criteria, priority, and dependencies.

**Step 5 — Prepare GitHub issue bodies.** For each specification, create an issue-ready body with clear descriptive title, comprehensive specification, appropriate labels such as `enhancement` and `high-priority`, explicit MVP philosophy, dependency relationships, implementation size, and sub-issues if the feature is too large.

**Step 6 — Optimize work distribution.** Review each specification for independence. Refactor specifications to maximize independent work streams. Create clear boundaries between interdependent components. For unavoidable dependencies, establish parent issues and sub-issues, document `blocked by` and `blocks` relationships, use GitHub issue linking syntax, add dependency labels such as `blocked` and `prerequisite`, and keep each sub-issue to 1–3 days of development work with its own acceptance criteria.

**Step 7 — Create issues only if authorized.** If the user requested issue creation and repository context is available, create the GitHub issues with labels and dependency notes. Otherwise return the issue-ready Markdown for manual creation.

**Step 8 — Final review.** Summarize all created specifications, highlight implementation dependencies, suggest a logical implementation order, and note potential challenges or considerations. Keep the open-source community and contribution model in mind.

## Invocation Example

```
/gen-specs-as-issues scope=. create_issues=no
```

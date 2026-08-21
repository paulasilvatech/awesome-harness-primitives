---
applyTo: '**'
description: 'Enforces Specification-Driven Workflow v1 conventions for requirements, design, tasks, documentation, validation, reflection, handoff, troubleshooting, debt, quality metrics, and EARS notation.'
---

# Specification-Driven Workflow Conventions — v1 Artifacts and Evidence

These instructions apply to all files when a task follows Specification-Driven Workflow v1. They are authoritative for maintaining `requirements.md`, `design.md`, `tasks.md`, EARS requirements, detailed action documentation, decision records, adaptive planning by confidence score, validation evidence, reflection, handoff, troubleshooting, technical debt tracking, and quality metrics; narrower language, framework, security, and repository instructions win for implementation details inside their scope.

## Core Artifacts and Source of Truth

Maintain the three workflow artifacts throughout the work.

| Artifact | Required content |
| --- | --- |
| `requirements.md` | User stories and acceptance criteria in structured EARS notation |
| `design.md` | Technical architecture, sequence diagrams, implementation considerations, data flow, interfaces, data models, and error handling |
| `tasks.md` | Detailed, trackable implementation plan with dependencies, status, expected outcomes, and verification notes |

Detailed templates are the primary source of truth for documentation. Summary formats are only for concise artifacts such as changelogs, pull request descriptions, executive summaries, or handoff notes.

## Documentation Records

Use complete action documentation for executions, tests, and meaningful steps. Preserve objective, context, decision, execution details, complete output, validation, and next action.

```text
### [TYPE] - [ACTION] - [TIMESTAMP]
**Objective**: [Goal being accomplished]
**Context**: [Current state, requirements, and reference to prior steps]
**Decision**: [Approach chosen and rationale, referencing the Decision Record if applicable]
**Execution**: [Steps taken with parameters and commands used. For code, include file paths.]
**Output**: [Complete and unabridged results, logs, command outputs, and metrics]
**Validation**: [Success verification method and results. If failed, include a remediation plan.]
**Next**: [Automatic continuation plan to the next specific action]
```

Use decision records for all consequential choices.

```text
### Decision - [TIMESTAMP]
**Decision**: [What was decided]
**Context**: [Situation requiring decision and data driving it]
**Options**: [Alternatives evaluated with brief pros and cons]
**Rationale**: [Why the selected option is superior, with trade-offs explicitly stated]
**Impact**: [Anticipated consequences for implementation, maintainability, and performance]
**Review**: [Conditions or schedule for reassessing this decision]
```

Derive concise reporting from full records. Use the streamlined action log format `[TYPE][TIMESTAMP] Goal: [X] → Action: [Y] → Result: [Z] → Next: [W]` for changelogs. Use the compressed decision record format `Decision: [X] | Rationale: [Y] | Impact: [Z] | Review: [Date]` for pull request summaries and executive summaries.

## Analysis and EARS Requirements

The analysis phase establishes testable intent before design or implementation. Read provided code, documentation, tests, and logs; document file inventory, summaries, and initial analysis results. Convert feature requests to EARS notation, identify dependencies and constraints, document a dependency graph with risks and mitigations, map data flows and interactions, document system diagrams and data models, catalog edge cases and failures in a matrix, and record a Confidence Score from 0-100% with rationale.

Use EARS patterns consistently:

| Pattern | Format |
| --- | --- |
| Ubiquitous | `THE SYSTEM SHALL [expected behavior]` |
| Event-driven | `WHEN [trigger event] THE SYSTEM SHALL [expected behavior]` |
| State-driven | `WHILE [in specific state] THE SYSTEM SHALL [expected behavior]` |
| Unwanted behavior | `IF [unwanted condition] THEN THE SYSTEM SHALL [required response]` |
| Optional | `WHERE [feature is included] THE SYSTEM SHALL [expected behavior]` |
| Complex | Combine patterns only when the requirement remains readable and testable |

Every requirement must be testable, unambiguous, necessary, feasible, and traceable. Do not proceed when requirements remain unclear.

## Design and Adaptive Planning

Use the Confidence Score to select the design depth and risk strategy.

| Confidence | Convention |
| --- | --- |
| High Confidence (`>85%`) | Draft a comprehensive implementation plan, skip proof-of-concept steps, proceed with full automated implementation, and maintain standard comprehensive documentation |
| Medium Confidence (`66–85%`) | Prioritize a Proof-of-Concept (PoC) or Minimum Viable Product (MVP), define success criteria, validate first, then expand incrementally |
| Low Confidence (`<66%`) | Dedicate the next phase to research and knowledge-building, use semantic search and similar implementations, synthesize findings, rerun analysis, and escalate only if confidence remains low |

`design.md` captures architecture, data flow, interfaces, API contracts, schemas, public-facing function signatures, data models, database schemas, error matrix, error procedures, expected responses, and unit testing strategy. `tasks.md` captures each implementation task with description, expected outcome, dependencies, and current status. Do not implement until design and plan are complete and validated.

## Implementation, Validation, Reflection, and Handoff

Implement in small, testable increments from dependencies upward. Document each increment, file creation, status update, adherence to conventions, and any deviation with a decision record. Comments explain intent and rationale, not mechanics.

Validate with automated tests, manual verification when necessary, edge-case and error testing, performance metrics, profile data for critical sections, execution traces, path analysis, runtime behavior, coverage reports, logs, and remediation for failures. Do not proceed with unresolved validation issues.

Reflect by refactoring for maintainability, updating READMEs, diagrams, comments, and project documentation, identifying improvements, documenting a prioritized backlog, validating success criteria in a final matrix, and performing meta-analysis of efficiency, tool usage, and protocol adherence.

Handoff packages the work for review or deployment. Pull request material includes an executive summary, changelog from the streamlined action log, links to validation artifacts and decision records, and links to final `requirements.md`, `design.md`, and `tasks.md`. Intermediate files, logs, and temporary artifacts are archived to `.agent_work/` when the workflow owns those artifacts.

## Troubleshooting, Technical Debt, and Quality Metrics

When errors, ambiguities, or blockers appear, re-analyze requirements and constraints, re-design the affected solution, re-plan `tasks.md`, retry execution with corrected parameters or logic, and escalate only after documented retries. Never proceed with unresolved errors or ambiguities.

Continuously assess technical debt. Record shortcuts and speed-over-quality choices in decision records, monitor workspace organization and naming drift, and track incomplete, outdated, or missing documentation. Use this auto-issue shape for debt records:

```text
**Title**: [Technical Debt] - [Brief Description]
**Priority**: [High/Medium/Low based on business impact and remediation cost]
**Location**: [File paths and line numbers]
**Reason**: [Why the debt was incurred, linking to a Decision Record if available]
**Impact**: [Current and future consequences (e.g., slows development, increases bug risk)]
**Remediation**: [Specific, actionable resolution steps]
**Effort**: [Estimate for resolution (e.g., T-shirt size: S, M, L)]
```

Track quality through static analysis, dynamic analysis, documentation checks, code coverage percentage and gap analysis, cyclomatic complexity per function or method, maintainability index, technical debt ratio, and documentation coverage for public methods with comments.


## Phase Vocabulary and Compatibility Terms

Keep the phase names and reporting terms stable so workflow artifacts remain searchable.

| Vocabulary | Convention |
| --- | --- |
| `ANALYZE`, `DESIGN`, `IMPLEMENT`, `VALIDATE`, `REFLECT`, and `HANDOFF` | Use these exact phase names in workflow artifacts and status reports. |
| `Steps/Executions/Tests` | Use the action documentation template for all meaningful Steps/Executions/Tests. |
| `PoC/MVP` and `PoC/MVP.` | Treat PoC/MVP as the medium-confidence risk-reduction path; punctuation may appear in prose but not in artifact names. |
| `step-by-step` | High-confidence work may use a comprehensive step-by-step plan. |
| `production-quality` | Implementation code remains production-quality even when delivered in small increments. |
| `before/after` | Reflection records before/after comparisons for refactors. |
| `function/method.` | Quality metrics may track cyclomatic complexity per function/method. |

## Good / Bad Examples

The examples below illustrate EARS requirements that are testable and traceable.

**Good:**

```text
WHEN a signed-in user submits a valid export request, THE SYSTEM SHALL create an export job and return the job identifier.
IF export storage is unavailable, THEN THE SYSTEM SHALL return a recoverable error and record the failed dependency in the validation log.
```

Why: Each requirement has a trigger or condition, a single expected behavior, and a result that can be tested.

**Bad:**

```text
Make exports better and handle errors nicely.
```

Why: The statement is ambiguous, not traceable, and cannot drive `design.md`, `tasks.md`, or validation evidence.

## Conventions

| Rule | Rationale |
|---|---|
| Maintain `requirements.md`, `design.md`, and `tasks.md` as living artifacts | Requirements, architecture, and implementation status remain traceable |
| Use detailed action documentation for executions and tests | Future reviewers can reproduce decisions, commands, outputs, and validation |
| Record consequential choices with decision records | Trade-offs and reassessment conditions stay visible |
| Use EARS notation for requirements | Acceptance criteria become testable and unambiguous |
| Adapt planning to the Confidence Score thresholds `>85%`, `66–85%`, and `<66%` | Riskier work receives PoC, MVP, or research before full implementation |
| Implement in small dependency-ordered increments | Failures are isolated and progress remains verifiable |
| Validate automated tests, manual checks, edge cases, errors, performance, and traces as relevant | The implementation is proven against requirements and quality standards |
| Reflect and update documentation before handoff | The codebase and review package stay maintainable |
| Document troubleshooting retries before escalation | Blockers are addressed systematically rather than bypassed |
| Track technical debt and quality metrics explicitly | Deferred work and code health remain visible after delivery |

## Do / Do Not

| Do | Do not |
|---|---|
| Treat detailed templates as the source of truth | Replace evidence with only a PR summary or changelog |
| Write requirements as `THE SYSTEM SHALL`, `WHEN`, `WHILE`, `IF`, or `WHERE` statements | Use vague goals that cannot be tested |
| Use PoC or MVP validation for medium-confidence work | Jump directly to a broad implementation when confidence is only `66–85%` |
| Research and rerun analysis for low-confidence work | Escalate before building knowledge when confidence is `<66%` |
| Update `tasks.md` status in real time | Let the implementation diverge from the plan silently |
| Link validation artifacts, decision records, and final workflow docs in handoff | Ask reviewers to infer what was tested or why decisions were made |
| Archive workflow-owned intermediate files to `.agent_work/` | Leave logs and temporary artifacts scattered through the workspace |
| Create debt records with priority, location, reason, impact, remediation, and effort | Hide speed-over-quality decisions or undocumented shortcuts |

## Checklist Before Opening a PR

- [ ] `requirements.md` contains testable, unambiguous, necessary, feasible, and traceable EARS requirements.
- [ ] `design.md` documents architecture, data flow, interfaces, data models, error handling, and unit testing strategy.
- [ ] `tasks.md` contains dependency-aware tasks with expected outcomes and current status.
- [ ] Action documents include objective, context, decision, execution, complete output, validation, and next action.
- [ ] Decision records capture options, rationale, impact, and review conditions for consequential choices.
- [ ] Confidence Score drove the plan using `>85%`, `66–85%`, or `<66%` thresholds.
- [ ] Implementation increments were dependency-ordered, documented, and tested.
- [ ] Automated tests, manual checks, edge cases, errors, performance, traces, coverage, or logs were captured as relevant.
- [ ] Reflection updated documentation, success criteria, backlog, and technical debt records.
- [ ] Handoff includes executive summary, streamlined changelog, validation links, decision record links, and links to `requirements.md`, `design.md`, and `tasks.md`.
- [ ] Workflow-owned intermediate files are archived to `.agent_work/` when applicable.

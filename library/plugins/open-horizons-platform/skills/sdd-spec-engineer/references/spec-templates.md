# Spec Templates

Artifact templates for Spec-Driven Development. Each feature gets a numbered folder (`001-<slug>/`, `002-<slug>/`) containing the four artifacts below. Keep acceptance criteria in EARS notation (see `ears-notation.md`).

## REQUIREMENTS.md

```markdown
# Requirements: <Feature Name>

- Feature ID: <NNN>
- Status: draft | reviewed | approved
- Author: <name>
- Date: <YYYY-MM-DD>

## Summary

One paragraph describing the problem and the desired outcome.

## User stories

- As a <role>, I want <capability>, so that <benefit>.

## Functional requirements (EARS)

- REQ-001: When <trigger>, the <system> shall <response>.
- REQ-002: While <state>, the <system> shall <response>.
- REQ-003: If <condition>, then the <system> shall <response>.

## Non-functional requirements

- NFR-001: The <system> shall <measurable quality constraint, for example respond within 200 ms at p95>.

## Out of scope

- Items explicitly not covered by this feature.

## Assumptions and dependencies

- Known assumptions, external services, or upstream features required.
```

## DESIGN.md

```markdown
# Design: <Feature Name>

- Feature ID: <NNN>
- Traces: REQ-001, REQ-002, ...

## Architecture overview

Short narrative of the approach and the main components.

## Diagram

\`\`\`mermaid
flowchart TD
  User --> UI[UI Layer]
  UI --> API[API / Service]
  API --> DB[(Data Store)]
\`\`\`

## Components

| Component | Responsibility | Traces |
| --- | --- | --- |
| <name> | <what it does> | REQ-00X |

## Data model

Entities, fields, and relationships (or a link to the schema).

## Interfaces and contracts

API endpoints, events, or function signatures with inputs and outputs.

## Risks and trade-offs

Decisions made, alternatives considered, and known risks.
```

## TASKS.md

Tasks are sequenced. Mark tasks that can run in parallel with `[P]`. Each task traces to one or more requirements.

```markdown
# Tasks: <Feature Name>

- Feature ID: <NNN>

## Pre-implementation gate

- [ ] Requirements approved
- [ ] Design reviewed
- [ ] Constitution checks pass

## Task list

- [ ] T001 Scaffold module and tests (traces REQ-001)
- [ ] T002 [P] Implement data model (traces REQ-002)
- [ ] T003 [P] Implement API endpoint (traces REQ-001, REQ-003)
- [ ] T004 Integrate UI with API (depends on T002, T003)
- [ ] T005 Add error handling for oversize input (traces REQ-003)
- [ ] T006 End-to-end verification (traces all)
```

## ANALYSIS.md (quality gate)

```markdown
# Quality Gate: <Feature Name>

- Feature ID: <NNN>
- Result: pass | fail

## Traceability matrix

| Requirement | Design component | Task(s) | Test(s) |
| --- | --- | --- | --- |
| REQ-001 | <component> | T001, T003 | <test id> |
| REQ-002 | <component> | T002 | <test id> |

## Findings

- Gaps, ambiguities, or untraced requirements found during review.

## Sign-off

- [ ] Every requirement traces to at least one task and one test.
- [ ] No orphan tasks (each task traces to a requirement).
- [ ] All acceptance criteria are in EARS notation.
```

## Conventions

- Number features sequentially: `001-`, `002-`, and so on.
- Keep one requirement per EARS sentence; never bundle.
- Every task traces to a requirement; every requirement traces to a task and a test.
- No em dashes in any artifact. Write "GitHub Copilot", never "Copilot" alone.

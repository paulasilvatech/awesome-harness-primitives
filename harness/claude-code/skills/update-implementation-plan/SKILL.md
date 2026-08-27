---
name: update-implementation-plan
description: >-
  Update an existing implementation plan or create a deterministic machine-readable plan for new
  requirements, features, refactoring, package upgrades, design, architecture, infrastructure,
  data, or process changes. Use when asked to update an implementation plan, revise a plan file,
  add requirements, or produce an AI-executable plan under /plan/.
---

<!-- Generated from harness/github-copilot/skills/update-implementation-plan/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Update implementation plan

Update or create an implementation plan so it is deterministic, self-contained, machine-readable and machine-parseable, and executable by AI agents or humans without hidden interpretation, decision-making, or loss of self-containment.

## When to invoke

- "Update this implementation plan with the new requirements."
- "Revise the plan file for this refactor."
- "Create an AI-executable implementation plan."
- "Add package upgrade tasks to the plan."
- "Generate a phased architecture or infrastructure plan under /plan/."

## Inputs

Use the user's target file, selected file, or `${file}` as the implementation plan to update. If no file exists, create a new plan under `/plan/` using the naming convention `[purpose]-[component]-[version].md`.

Purpose prefixes are `upgrade`, `refactor`, `feature`, `data`, `infrastructure`, `process`, `architecture`, and `design`. Examples: `upgrade-system-command-4.md` and `feature-auth-module-1.md`.

## Plan standards

| Requirement | Rule |
| --- | --- |
| Executability | Every phase and task must be executable by AI agents or humans. |
| Determinism | Use explicit language with zero ambiguity or hidden interpretation. |
| Atomicity | Plans consist of discrete phases and atomic tasks. |
| Dependencies | Cross-phase or task dependencies must be explicitly declared. |
| Specificity | Include file paths, function names, constants, configuration values, and exact implementation details where applicable. |
| Identifiers | Use standardized prefixes such as `REQ-`, `SEC-`, `CON-`, `GUD-`, `PAT-`, `TASK-`, `ALT-`, `DEP-`, `FILE-`, `TEST-`, `RISK-`, and `ASSUMPTION-`. |
| Validation | Include criteria that can be automatically verified. |
| Self-containment | Do not require external context to understand the plan. |

## Procedure

1. Read the existing implementation plan, new or updated requirements, and relevant code references.
2. Preserve valid existing plan content unless it conflicts with new requirements.
3. Normalize phases so each has measurable completion criteria and clear cross-phase dependency boundaries.
4. Convert vague work into atomic tasks with paths, functions, implementation details, completion state, and date fields.
5. Update front matter and status badge consistently.
6. Validate every required section, table column, identifier prefix, and placeholder before saving.

## Template requirements

All implementation plans must use this exact top-level structure and fully populate each section:

| Section | Required content |
| --- | --- |
| Front matter | `goal`, `version`, `date_created`, `last_updated`, `owner`, `status`, and `tags`. |
| `# Introduction` | Status badge and concise goal-oriented introduction. |
| `## 1. Requirements & Constraints` | Requirements, security requirements, constraints, guidelines, and patterns. |
| `## 2. Implementation Steps` | Phases with `GOAL-NNN` and task tables. |
| `## 3. Alternatives` | `ALT-NNN` options and rationale for rejection. |
| `## 4. Dependencies` | `DEP-NNN` dependencies. |
| `## 5. Files` | `FILE-NNN` affected files. |
| `## 6. Testing` | `TEST-NNN` verification tasks. |
| `## 7. Risks & Assumptions` | `RISK-NNN` and `ASSUMPTION-NNN`. |
| `## 8. Related Specifications / Further Reading` | Related specifications or external documentation. |

Allowed statuses are `Completed`, `In progress`, `Planned`, `Deprecated`, and `On Hold`. Use badge colors bright green, yellow, blue, red, and orange respectively.

## Mandatory plan template

```md
---
goal: [Concise Title Describing the Package Implementation Plan's Goal]
version: [Optional: e.g., 1.0, Date]
date_created: [YYYY-MM-DD]
last_updated: [Optional: YYYY-MM-DD]
owner: [Optional: Team/Individual responsible for this spec]
status: 'Completed'|'In progress'|'Planned'|'Deprecated'|'On Hold'
tags: [Optional: List of relevant tags or categories, e.g., `feature`, `upgrade`, `chore`, `architecture`, `migration`, `bug` etc]
---

# Introduction

![Status: <status>](https://img.shields.io/badge/status-<status>-<status_color>)

[A short concise introduction to the plan and the goal it is intended to achieve.]

## 1. Requirements & Constraints

- **REQ-001**: Requirement 1
- **SEC-001**: Security Requirement 1
- **[3 LETTERS]-001**: Other Requirement 1
- **CON-001**: Constraint 1
- **GUD-001**: Guideline 1
- **PAT-001**: Pattern to follow 1

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: [Describe the goal of this phase, e.g., "Implement feature X", "Refactor module Y", etc.]

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Description of task 1 | Yes | 2025-04-25 |
| TASK-002 | Description of task 2 | |  |
| TASK-003 | Description of task 3 | |  |

### Implementation Phase 2

- GOAL-002: [Describe the goal of this phase, e.g., "Implement feature X", "Refactor module Y", etc.]

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-004 | Description of task 4 | |  |
| TASK-005 | Description of task 5 | |  |
| TASK-006 | Description of task 6 | |  |

## 3. Alternatives

- **ALT-001**: Alternative approach 1
- **ALT-002**: Alternative approach 2

## 4. Dependencies

- **DEP-001**: Dependency 1
- **DEP-002**: Dependency 2

## 5. Files

- **FILE-001**: Description of file 1
- **FILE-002**: Description of file 2

## 6. Testing

- **TEST-001**: Description of test 1
- **TEST-002**: Description of test 2

## 7. Risks & Assumptions

- **RISK-001**: Risk 1
- **ASSUMPTION-001**: Assumption 1

## 8. Related Specifications / Further Reading

[Link to related spec 1]
[Link to relevant external documentation]
```

## Template validation rules

- All front matter fields are present and properly formatted.
- Section headers match exactly and are case-sensitive.
- Identifier prefixes follow the specified format.
- Task tables include `Task`, `Description`, `Completed`, and `Date` columns.
- No placeholder text remains in the final output.
- Status in front matter and badge agree.

## Gotchas

- **Do not leave human interpretation tasks**; replace them with explicit decisions, dependencies, or assumptions.
- **Do not omit file paths or function names when code changes are known**; specificity is required for autonomous execution.
- **Do not create plans outside `/plan/`** unless updating an explicitly supplied existing file.
- **Do not mismatch status color and status text**; the badge must reflect the front matter.

## Output template

```markdown
## Implementation plan update

**Status:** updated | created | blocked
**Plan file:** `/plan/<purpose>-<component>-<version>.md`
**Plan status:** `<Completed|In progress|Planned|Deprecated|On Hold>`

### Changes made
| Section | Update |
| --- | --- |
| Requirements & Constraints | <summary> |
| Implementation Steps | <summary> |
| Testing | <summary> |

### Validation
- Required sections: <pass|fail>
- Identifier prefixes: <pass|fail>
- Placeholders removed: <pass|fail>
- Status badge: <pass|fail>
```

## Quality gate

- [ ] The target `${file}` or a new `/plan/[purpose]-[component]-[version].md` path is identified.
- [ ] All required front matter fields and plan sections are present.
- [ ] Status is one of `Completed`, `In progress`, `Planned`, `Deprecated`, or `On Hold` and the badge uses the matching color.
- [ ] Requirements, phases, tasks, dependencies, files, tests, risks, and assumptions use standardized identifiers.
- [ ] Tasks are atomic, deterministic, and include specific paths, functions, or configuration details when known.
- [ ] No placeholder text remains in the final plan.

## References

- [Shields.io status badge](https://img.shields.io/badge/status-<status>-<status_color>)

---
name: create-implementation-plan
description: >-
  Create deterministic implementation plan files for features, refactors, package upgrades,
  design, architecture, infrastructure, data, or process work. Use when the user asks for an
  implementation plan, phased execution plan, AI-executable plan, /plan artifact, or
  machine-readable roadmap for autonomous agents or humans.
---

<!-- Generated from harness/github-copilot/plugins/project-planning/skills/create-implementation-plan/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create implementation plan

Convert a feature, refactor, upgrade, design, architecture, infrastructure, data, or process goal into a deterministic Markdown plan under `/plan/` with atomic phases, unique identifiers, explicit dependencies, files, tests, risks, assumptions, and validation checks.

## When to invoke

- "Create an implementation plan for this feature."
- "Write a phased plan an AI agent can execute."
- "Plan this package upgrade with tasks and validation."
- "Create a /plan artifact for the refactor."
- "Turn this architecture change into implementation steps."

## Inputs

Use the user's requested plan purpose as the source for the file name, goal, phases, and scope. If the purpose is ambiguous, infer the closest prefix from `upgrade`, `refactor`, `feature`, `data`, `infrastructure`, `process`, `architecture`, or `design` and state the assumption in the plan.

## Plan rules

| Area | Requirement |
| --- | --- |
| Audience | AI agents and humans must be able to execute the plan without hidden context. |
| Language | Use deterministic, unambiguous wording with no human interpretation required. |
| Phases | Use discrete atomic phases with measurable completion criteria. |
| Tasks | Include specific file paths, function names, exact implementation details, and dependencies when known. |
| Parallelism | Tasks are parallelizable unless dependencies explicitly say otherwise. |
| Identifiers | Use standardized unique prefixes: `REQ-`, `TASK-`, `SEC-`, `CON-`, `GUD-`, `PAT-`, `GOAL-`, `ALT-`, `DEP-`, `FILE-`, `TEST-`, `RISK-`, `ASSUMPTION-`. |
| Placeholders | No placeholder text may remain in the final output. |

Save implementation plans in `/plan/` using `[purpose]-[component]-[version].md`, for example `upgrade-system-command-4.md` or `feature-auth-module-1.md`.

## Identifier uniqueness

Every declaration identifier must appear exactly once. A declaration is the leading cell in a `TASK` or `GOAL` table row, or a bullet such as `- **REQ-001**: ...`. References to already declared IDs are allowed in task descriptions and dependency text.

Run these checks before finalizing, replacing `PLAN_FILE` with the actual path:

```bash
PLAN_FILE="/plan/<purpose>-<component>-<version>.md"

grep -oE '\| (TASK|GOAL)-[0-9]+ \|' "$PLAN_FILE"   | sed -E 's/.*((TASK|GOAL)-[0-9]+).*//'   | sort | uniq -d

grep -oE '^- \*\*(REQ|SEC|CON|GUD|RISK|ASSUMPTION|TASK|GOAL|FILE|TEST|PAT|ALT|DEP)-[0-9]+\*\*:' "$PLAN_FILE"   | sed -E 's/^- \*\*([A-Z]+-[0-9]+)\*\*:.*//'   | sort | uniq -d

grep -oE '(REQ|SEC|CON|GUD|RISK|ASSUMPTION|TASK|GOAL|FILE|TEST|PAT|ALT|DEP)-[0-9]+' "$PLAN_FILE"   | sort | uniq -d
```

Checks 1 and 2 are gates and must return no rows. Check 3 is diagnostic and may include valid references. Prerequisites are a POSIX-compatible shell (`sh` or `bash`) with `grep`, `sed`, `sort`, and `uniq`; on Windows, use equivalent commands while preserving declaration-vs-reference logic.

## Status and badge

The frontmatter `status` must be exactly one of `Completed`, `In progress`, `Planned`, `Deprecated`, or `On Hold`. The introduction must show a shields badge using `https://img.shields.io/badge/status-<status>-<status_color>`, where status colors are bright green, yellow, blue, red, or orange respectively.

## Required plan template

```markdown
---
goal: <Concise Title Describing the Package Implementation Plan's Goal>
version: <optional version such as 1.0 or date>
date_created: <YYYY-MM-DD>
last_updated: <optional YYYY-MM-DD>
owner: <optional team or individual>
status: 'Completed'|'In progress'|'Planned'|'Deprecated'|'On Hold'
tags: [<feature|upgrade|chore|architecture|migration|bug>]
---

# Introduction

![Status: <status>](https://img.shields.io/badge/status-<status>-<status_color>)

<short introduction and goal>

## 1. Requirements & Constraints

- **REQ-001**: <requirement>
- **SEC-001**: <security requirement>
- **CON-001**: <constraint>
- **GUD-001**: <guideline>
- **PAT-001**: <pattern>

## 2. Implementation Steps

### Implementation Phase 1

- **GOAL-001**: <phase goal>

| Task | Description | Completed | Date |
| --- | --- | --- | --- |
| TASK-001 | <specific executable task> |  |  |
| TASK-002 | <specific executable task> |  |  |

### Implementation Phase 2

- **GOAL-002**: <phase goal>

| Task | Description | Completed | Date |
| --- | --- | --- | --- |
| TASK-003 | <specific executable task> |  |  |

## 3. Alternatives

- **ALT-001**: <alternative and rejection rationale>

## 4. Dependencies

- **DEP-001**: <library, framework, service, or component dependency>

## 5. Files

- **FILE-001**: <file path and planned change>

## 6. Testing

- **TEST-001**: <test or validation command>

## 7. Risks & Assumptions

- **RISK-001**: <risk>
- **ASSUMPTION-001**: <assumption>

## 8. Related Specifications / Further Reading

- <related spec or external documentation>
```

## Procedure

1. Determine the plan purpose prefix, component name, version number, and target file path under `/plan/`.
2. Inventory requirements, security constraints, guidelines, patterns, dependencies, files, tests, alternatives, risks, and assumptions from the user's request and repository context.
3. Break work into phases with `GOAL-NNN` declarations and atomic `TASK-NNN` table rows.
4. Make each task executable by including paths, function names, configuration keys, validation commands, and dependencies.
5. Write the plan file, then run the identifier uniqueness checks with `PLAN_FILE` set to the new path.
6. Re-number duplicates until declaration checks return no rows.

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `${input:PlanPurpose}`
- `- ** REQ-001 **: ...`
- `ALT-NNN`
- `ASSUMPTION-NNN`
- `CON-NNN`
- `DEP-NNN`
- `FILE-NNN`
- `GUD-NNN`
- `LETTERS`
- `PAT-NNN`
- `REQ-NNN`
- `RISK-NNN`
- `SEC-NNN`
- `TASK/GOAL`
- `TEST-NNN`
- `Team/Individual`
- `bullet-style`
- `case-sensitive`
- `chore`
- `cross-phase`
- `decision-making`
- `machine-parseable`
- `migration`
- `platform-native`
- `re-number`
- `re-run`
- `self-containment`
- `PlanPurpose`

## Output template

```markdown
## Implementation plan result

**Status:** created | updated | blocked
**Plan file:** `/plan/<purpose>-<component>-<version>.md`
**Plan status:** Completed | In progress | Planned | Deprecated | On Hold

| Section | Result | Evidence |
| --- | --- | --- |
| Requirements | <count> | <REQ/SEC/CON/GUD/PAT IDs> |
| Tasks | <count> | <TASK IDs and phases> |
| Files | <count> | <FILE IDs> |
| Tests | <count> | <TEST IDs> |
| Validation | pass | Identifier declaration checks returned no rows |
```

## Quality gate

- [ ] The file is saved under `/plan/` with `[purpose]-[component]-[version].md` naming.
- [ ] All required frontmatter fields and required section headers are present.
- [ ] Every task is atomic, executable, and contains enough context for an AI agent or human.
- [ ] Dependencies between tasks are explicit; otherwise tasks are safe to parallelize.
- [ ] No placeholder text remains.
- [ ] Identifier declaration checks for `PLAN_FILE` returned no rows.
- [ ] The broad duplicate scan was reviewed as diagnostic only.
- [ ] The status badge uses the allowed status and color mapping.

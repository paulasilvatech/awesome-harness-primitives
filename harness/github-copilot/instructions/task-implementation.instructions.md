---
applyTo: '**/.copilot-tracking/changes/*.md'
description: 'Enforces conventions for implementing tracked task plans with complete plan/detail reading, progressive checklist updates, change records, validation, and release summaries.'
---

# Task Plan Implementation Conventions — Progressive Tracking

These instructions apply when a change record under `.copilot-tracking/changes/*.md` is active for implementation work driven by `.copilot-tracking/plans/**` and `.copilot-tracking/details/**`. They are authoritative for associating implementation work with plan tasks, reading complete plan and detail context, updating plan checkboxes and change records, and writing release summaries; repository coding standards, build/test instructions, and stricter project-specific implementation rules win for the actual code being changed.

## Plan and Context Reading

Before implementation begins, the complete plan, changes file, details content, referenced files, and workspace conventions must be understood.

- Read and fully understand the complete plan file, including scope, objectives, all phases, and every checklist item.
- Read and fully understand the corresponding changes file completely; if context is missing, read the entire file back in using `read_file`.
- Identify all referenced files mentioned in the plan and examine them for context.
- Understand current project structure and conventions, including standards in the `copilot/` folder when present.
- Keep every implementation associated with a specific task from the plan.
- Before implementing any task, read the entire details section for that task from `.copilot-tracking/details/**` and fully understand all implementation requirements.

## Implementation and Tracking

Implement plan tasks systematically and keep tracking artifacts accurate.

| Concern | Convention |
| --- | --- |
| Task order | Process tasks in the plan sequence exactly, one task at a time. |
| Task association | Ensure every code change maps to a specific plan task. |
| Completeness | Implement complete, working functionality that meets all task requirements from the details. |
| Workspace fit | Follow existing code patterns, naming conventions, dependencies, and structure. |
| Quality | Include proper error handling, validation, documentation, and comments for complex logic. |
| Plan update | After each completed task, update the plan file by changing `[ ]` to `[x]`. |
| Phase update | If all tasks in a phase are complete, mark the phase header complete with `[x]`. |
| Changes update | After every task completion, append to the appropriate Added, Modified, or Removed section with relative file paths and one-sentence summaries. |
| Divergence | If implementation diverges from the plan or details, call it out in the relevant change section with the specific reason. |

## Validation and Problem Resolution

After each task, validate the changes against requirements from the details file and fix problems before moving on. Continue until all plan tasks are marked `[x]`, all specified files have working code, all success criteria are verified, and no implementation errors remain.

When implementation issues occur, document the specific problem clearly, try alternative approaches or search terms, use workspace patterns as the fallback when external references fail, continue with available information rather than stopping completely, and note unresolved issues in the plan file for future reference.

## External References

When gathering external references, prioritize practical implementation examples over theoretical documentation and verify that the source contains usable patterns. Adapt external patterns to match workspace conventions first and external conventions second; integrate dependencies and configuration completely instead of copying isolated snippets.

## Changes File Format

Every changes file starts with `<!-- markdownlint-disable-file -->`, uses release-ready documentation, and keeps file inventory current.

```markdown
<!-- markdownlint-disable-file -->
# Release Changes: {{task name}}

**Related Plan**: {{plan-file-name}}
**Implementation Date**: {{YYYY-MM-DD}}

## Summary

{{Brief description of the overall changes made for this release}}

## Changes

### Added

- {{relative-file-path}} - {{one sentence summary of what was implemented}}

### Modified

- {{relative-file-path}} - {{one sentence summary of what was changed}}

### Removed

- {{relative-file-path}} - {{one sentence summary of what was removed}}

## Release Summary

**Total Files Affected**: {{number}}

### Files Created ({{count}})

- {{file-path}} - {{purpose}}

### Files Modified ({{count}})

- {{file-path}} - {{changes-made}}

### Files Removed ({{count}})

- {{file-path}} - {{reason}}

### Dependencies & Infrastructure

- **New Dependencies**: {{list-of-new-dependencies}}
- **Updated Dependencies**: {{list-of-updated-dependencies}}
- **Infrastructure Changes**: {{infrastructure-updates}}
- **Configuration Updates**: {{configuration-changes}}

### Deployment Notes

{{Any specific deployment considerations or steps}}
```

Create new changes files in `.copilot-tracking/changes/` with filename pattern `YYYYMMDD-task-description-changes.md`. Add `## Release Summary` only after all phases are marked `[x]`.

## Completion Criteria

Implementation is complete only when all plan tasks are marked `[x]`, all specified files exist with working code, all success criteria from the plan are verified, code follows workspace patterns and conventions, the changes file documents every task completion in Added, Modified, or Removed sections, all phases have release-ready documentation, and the final Release Summary is present after completion.

## Good / Bad Examples

The examples below illustrate change-record entries tied to implementation work.

**Good:**

```markdown
### Modified

- src/users/createUser.ts - Added validated email handling for the create-user task.
```

Why: The entry names a relative path and summarizes what changed in one sentence.

**Bad:**

```markdown
### Modified

- Updated some files.
```

Why: The entry lacks a path, task traceability, and release-ready detail.

## Required Tracking Vocabulary

Retain the tracking terms `.copilot-tracking/changes/**`, `./.copilot-tracking/changes/`, `copilot-tracking/changes/**`, `changes-template`, `microsoft/edge-ai`, `edge-ai`, `{{ }}`, `MANDATORY`, `MUST`, `ALWAYS`, `EVERY`, `FULLY`, `IMPORTANT`, `re-read`, and `high-quality` when maintaining existing task-plan records and templates.


## Conventions

| Rule | Rationale |
| --- | --- |
| Read complete plan, changes, details, referenced files, and workspace conventions before implementation | Missing context causes incomplete or inconsistent code |
| Associate every implementation with a specific unchecked plan task | Progress remains auditable and scoped |
| Read the complete task details section before coding | Details often contain constraints not visible in the checklist |
| Update `[ ]` to `[x]` only after working code and validation are complete | Tracking reflects verified progress, not intent |
| Append changes after every task completion | Release documentation stays current and recoverable |
| Record divergences from plan/details with reasons | Reviewers can distinguish intentional adaptation from accidental drift |
| Add Release Summary only after all phases are complete | Release notes do not claim completion early |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Process tasks in plan order | Skip ahead without task context |
| Read `.copilot-tracking/details/**` for the active task | Implement from checklist text alone |
| Use workspace patterns before external examples | Copy external patterns that conflict with the project |
| Validate each task before marking it `[x]` | Mark tasks complete before testing or verification |
| Append relative paths to Added, Modified, and Removed | Leave vague or fileless change summaries |
| Note unresolved issues in the plan file | Stop silently or leave failures undocumented |

## Checklist Before Opening a PR

- [ ] The complete plan file, changes file, relevant details sections, referenced files, and workspace conventions were read.
- [ ] Every implementation change is associated with a specific plan task.
- [ ] Tasks were processed in plan order unless a documented issue required a different order.
- [ ] Completed tasks and phase headers are marked `[x]` only after validation.
- [ ] The changes file starts with `<!-- markdownlint-disable-file -->` and records each completed task under Added, Modified, or Removed with relative paths.
- [ ] Any divergence from the plan or details is documented with a specific reason.
- [ ] All specified files exist with working code and all plan success criteria are verified.
- [ ] `## Release Summary` is present only when all phases are complete and includes file counts, dependencies, infrastructure, configuration, and deployment notes.

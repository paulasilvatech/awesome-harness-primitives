---
name: "create-github-issues-feature-from-implementation-plan"
description: >-
  Create or update GitHub issues from implementation-plan phases using feature_request.yml or chore_request.yml templates when available. Use when the user asks to turn an implementation plan into GitHub issues, file one issue per phase, or deduplicate planned feature/chore work against existing issues.
---

# Create GitHub issues from implementation plan

Analyze an implementation plan, transform each phase into a deduplicated GitHub issue, and return the created or updated feature/chore issue set with validation against existing issues.

## When to invoke

- "Create GitHub issues from this implementation plan."
- "Turn each plan phase into an issue."
- "File feature and chore issues from the plan."
- "Check existing issues before creating plan issues."
- "Use feature_request.yml or chore_request.yml for these phases."

## Plan extraction

Use the implementation plan at `${file}` as the source. Identify phases and create one issue per implementation phase; do not collapse unrelated phases or create extra issues for speculative work.

| Plan signal | Issue mapping | Rule |
| --- | --- | --- |
| Phase heading | Issue title | Use the phase name and sequence when present. |
| Phase objective | Problem or task summary | State why this phase exists. |
| Feature behavior | `feature_request.yml` | Use for user-visible capability or product behavior. |
| Infrastructure, cleanup, tooling, refactor | `chore_request.yml` | Use for enabling or maintenance work with no direct feature request. |
| Requirements and tasks | Issue body | Preserve only changes required by the plan. |
| Dependencies | Issue body context | Note predecessor phases, blockers, and sequencing. |

## Issue workflow

1. Read and analyze `${file}` completely.
2. Identify implementation phases and classify each as feature or chore.
3. Search for duplicates or related work using `search_issues` before creating anything.
4. Use `update_issue` when an existing issue already covers a phase.
5. Use `create_issue` once per uncovered phase.
6. Use `feature_request.yml` for feature phases and `chore_request.yml` for chore phases; fall back to a default body if the template is absent.
7. Verify each issue includes only changes required by its phase and that the whole issue set covers the plan.

## Phase boundaries

| Boundary decision | Use this rule |
| --- | --- |
| One phase has multiple tasks | Keep one issue if the tasks must ship together to complete the phase. |
| One phase mixes unrelated deliverables | Split only when the plan itself defines independent subphases or separate ownership. |
| A task is a prerequisite for a later phase | Keep it in its phase and record the dependency in both issue bodies when useful. |
| A phase is already fully covered by an issue | Update that issue; do not create another. |
| A phase is vague | Preserve the plan's wording and mark unclear acceptance criteria rather than inventing scope. |

## Issue body fields

| Field | Content |
| --- | --- |
| Title | Phase name from implementation plan. |
| Description | Phase details, requirements, and context. |
| Type | Feature or chore based on the phase's user-visible outcome. |
| Acceptance criteria | Testable checks or completion criteria from the plan. |
| Dependencies | Prior phases, blockers, or sequencing notes. |
| Labels | Repository-appropriate labels for issue type, such as `feature` or `chore`. |

## Output template

````markdown
## GitHub plan issue result

**Status:** created | updated | mixed | blocked
**Implementation plan:** `${file}`
**Templates:** `feature_request.yml` / `chore_request.yml` / default

| Phase | Issue type | Action | Issue | Existing issue check |
| --- | --- | --- | --- | --- |
| <phase name> | feature | created | <URL or number> | no duplicate |
| <phase name> | chore | updated | <URL or number> | matched <issue> |

### Coverage check
- Plan phases found: <count>
- Issues created: <count>
- Issues updated: <count>
- Phases not filed: <reason or none>
````

## Quality gate

- [ ] `${file}` was read as the source implementation plan.
- [ ] One issue exists per implementation phase, unless a documented duplicate covers it.
- [ ] Existing issues were checked with `search_issues` before `create_issue`.
- [ ] `update_issue` was used for matching existing issues.
- [ ] `feature_request.yml` or `chore_request.yml` was used according to issue type, with a default fallback otherwise.
- [ ] Every issue includes only changes required by the plan phase.
- [ ] Titles, descriptions, labels, dependencies, and acceptance criteria are clear and phase-specific.

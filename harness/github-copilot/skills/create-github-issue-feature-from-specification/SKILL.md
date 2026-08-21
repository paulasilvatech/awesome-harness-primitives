---
name: "create-github-issue-feature-from-specification"
description: >-
  Create or update one GitHub feature issue from a specification file using a feature_request.yml template when available. Use when the user asks to create a GitHub issue from a specification, turn a spec into a feature request, or file one issue that captures a complete specification.
---

# Create GitHub issue from specification

Analyze a specification file, transform its requirements into one deduplicated GitHub feature issue, and return the created or updated issue with validation against existing issues.

## When to invoke

- "Create a GitHub issue from this specification."
- "Turn this spec file into a feature request issue."
- "File one issue for the complete specification."
- "Check existing issues before creating a feature issue."
- "Use feature_request.yml for this specification."

## Specification extraction

Use the specification at `${file}` as the source. Extract only changes required by that specification; do not add roadmap ideas, inferred epics, or implementation details that are not present.

| Spec signal | Issue field | Rule |
| --- | --- | --- |
| Feature name, heading, or title | Title | Use a concise title that identifies the specification. |
| Problem statement | Description: Problem | State the user or system problem before the solution. |
| Proposed behavior | Description: Proposed solution | Summarize required behavior, not internal speculation. |
| Requirements and acceptance criteria | Description: Requirements | Preserve MUST/SHALL language and measurable checks. |
| Constraints, non-goals, dependencies | Description: Context | Include blockers, compatibility notes, and explicit exclusions. |
| Labels or category hints | Labels | Apply `feature` and `enhancement` when appropriate and supported by the repo. |

## Issue workflow

1. Read and analyze `${file}` completely.
2. Search for duplicates or near-duplicates using `search_issues` before creating anything.
3. If an existing issue covers the same specification, update it with `update_issue` instead of creating a duplicate.
4. If no existing issue covers it, create one issue with `create_issue`.
5. Use the repository's `feature_request.yml` template when it exists; otherwise fall back to a clear default issue body.
6. Verify the resulting issue includes only changes required by the specification.

## Deduplication criteria

| Existing issue match | Action |
| --- | --- |
| Same specification path or title and same requested behavior | Update existing issue. |
| Same feature area but different acceptance criteria | Create a new issue and cross-reference if useful. |
| Closed issue that fully implemented the spec | Do not reopen; report that the request appears complete unless the spec changed. |
| Partial duplicate | Update existing issue when it can absorb the missing spec requirements without changing its intent. |

## Issue body fields

| Field | Content |
| --- | --- |
| Title | Feature name from specification. |
| Problem statement | Why the feature is needed. |
| Proposed solution | What the feature must do. |
| Requirements | Bullet list of required behavior from the spec. |
| Acceptance criteria | Testable completion checks from the spec. |
| Context | Links, constraints, dependencies, and non-goals from the spec. |
| Labels | `feature`, `enhancement`, or repository-appropriate equivalents. |

## Output template

````markdown
## GitHub feature issue result

**Status:** created | updated | duplicate found | blocked
**Specification:** `${file}`
**Template:** `feature_request.yml` | default
**Issue:** <URL or number>

### Title
<feature name from specification>

### Body summary
- Problem: <problem statement>
- Proposed solution: <solution summary>
- Requirements: <count and key bullets>
- Acceptance criteria: <count and key bullets>

### Existing issue check
| Candidate | Match level | Decision |
| --- | --- | --- |
| <issue> | exact | updated instead of duplicate |

### Labels
- `feature`
- `enhancement`
````

## Quality gate

- [ ] `${file}` was read as the source specification.
- [ ] Existing issues were checked with `search_issues` before `create_issue`.
- [ ] `update_issue` was used instead of duplicate creation when a matching issue existed.
- [ ] Exactly one issue represents the complete specification.
- [ ] The body uses `feature_request.yml` when available, with a default fallback otherwise.
- [ ] The issue includes only changes required by the specification.
- [ ] The title, description, labels, and acceptance criteria are clear and traceable to the spec.

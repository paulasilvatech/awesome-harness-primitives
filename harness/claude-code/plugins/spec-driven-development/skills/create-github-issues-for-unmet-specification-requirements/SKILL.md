---
name: create-github-issues-for-unmet-specification-requirements
description: >-
  Create GitHub Issues for unimplemented requirements found in specification files, avoiding
  duplicates and using the feature_request.yml issue template when available. Use this skill when
  asked to turn unmet specs, missing requirements, or unimplemented acceptance criteria into
  GitHub Issues.
---

<!-- Generated from harness/github-copilot/plugins/spec-driven-development/skills/create-github-issues-for-unmet-specification-requirements/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create GitHub issues for unmet specification requirements

Analyze a specification file, verify which requirements are not implemented, search GitHub for existing coverage, and create one actionable GitHub Issue per unmet requirement using the repository's feature request template when possible.

When a caller supplies `${file}`, treat it as the specification source path.

## When to invoke

- "Create GitHub Issues for unmet requirements in this spec."
- "Turn unimplemented specification requirements into issues."
- "File issues for missing acceptance criteria."
- "Check the spec against the codebase and create issues."
- "Use feature_request.yml for these missing requirements."

## Prerequisites and context

- A specification file path or selected specification content is required.
- GitHub repository access must be available for issue search and creation.
- Use `feature_request.yml` when the repository provides it; fall back to a normal issue body only when the template is unavailable.

## Procedure

1. Analyze the specification file to extract all requirement IDs, descriptions, acceptance criteria, and relevant context.
2. Search the codebase for related implementation patterns, route names, types, functions, tests, configuration, and documentation.
3. Check related specification files in `/spec/` when present so the requirement is not already refined or superseded elsewhere.
4. Classify each requirement as implemented, partially implemented, unimplemented, or uncertain. Verify that partial implementation is not enough to satisfy the acceptance criteria.
5. Search existing issues using `search_issues` or the GitHub CLI equivalent before creating anything.
6. Create one new issue per unimplemented requirement using `create_issue` or the GitHub CLI equivalent.
7. Use the `feature_request.yml` template fields when available; otherwise create a markdown body with the same information.
8. Report created issues, skipped duplicates, implemented requirements, and uncertain cases.

## Requirement and issue mapping

| Input fact | Issue placement | Rule |
| --- | --- | --- |
| Requirement ID | Title and body | Keep the exact ID visible, for example `REQ-123: Add export audit trail`. |
| Requirement description | Body summary | Preserve the user's/specification wording unless it is unclear; do not rewrite into a different requirement. |
| Acceptance criteria | Checklist | Convert each criterion into a checkable task. |
| Implementation guidance | Body section | Include likely files, modules, APIs, tests, or data changes discovered during implementation checks. |
| Existing issue match | Skip list | Do not create duplicates; link the existing issue instead. |
| Partial implementation | Body evidence | Explain what exists and what is still missing. |
| Labels | Issue metadata | Use `feature` and `enhancement` as appropriate, following repository label availability. |

## Duplicate and implementation checks

- Search existing issues by requirement ID, key phrases from the requirement, and likely feature names.
- Treat an open issue with the same requirement ID as a duplicate unless the user explicitly asks for a new tracking issue.
- Treat a closed issue as evidence, not proof; inspect whether it actually satisfies the requirement.
- Search the codebase for related code patterns and tests before claiming a requirement is unimplemented.
- If implementation evidence is ambiguous, create an issue only when the missing behavior is clear; otherwise report uncertainty and the evidence needed.

## Output template

````markdown
## GitHub requirement issue creation

**Status:** created | partial | blocked
**Specification:** `<specification file>`

| Requirement | Implementation status | Existing issue search | Action |
| --- | --- | --- | --- |
| `REQ-001` | unimplemented | no duplicate found | created `<issue URL>` |
| `REQ-002` | implemented | not searched | skipped |
| `REQ-003` | partial | duplicate `<issue URL>` | skipped duplicate |

### Issue body used
```markdown
## Requirement
`<REQ-ID>` — <description>

## Implementation guidance
- <files, modules, or approach>

## Acceptance criteria
- [ ] <criterion>

## Evidence
- <implementation search evidence or gap>
```

### Validation
- Existing issues searched: yes | no
- `feature_request.yml` used: yes | fallback
````

## Quality gate

- [ ] Every requirement from the specification was extracted or explicitly marked unparseable.
- [ ] Codebase implementation status was checked before issue creation.
- [ ] Existing issues were searched by requirement ID and key phrases to avoid duplicates.
- [ ] Each new issue maps to exactly one unimplemented requirement.
- [ ] Issue title contains the requirement ID and brief description.
- [ ] Issue body includes detailed requirement context, implementation guidance, and acceptance criteria.
- [ ] `feature_request.yml` was used when available, with fallback noted when not available.
- [ ] Created, skipped, duplicate, implemented, partial, and uncertain requirements are all reported.

---
name: "update-specification"
description: >-
  Update an existing AI-ready specification file in /spec/ from new requirements or code changes, preserving precise requirements, constraints, interfaces, acceptance criteria, and validation structure. Use this skill when the user asks to update a specification, revise requirements, sync a spec with code, or apply best practices for AI-ready specifications.
---

# Update specification

Revise an existing solution specification so it remains clear, unambiguous, machine-readable, self-contained, and aligned with new requirements or implemented code.

## When to invoke

- "Update this specification with the new requirements."
- "Sync the spec with the code changes."
- "Revise /spec/schema-user-profile.md for this interface change."
- "Apply AI-ready specification best practices to this existing spec."
- "Add acceptance criteria and validation to this spec."

## Inputs

Use `$ARGUMENTS` as the target specification path, change request, or code-change summary. If a concrete file is not provided, identify the likely existing `/spec/` file from user context and ask for clarification only when multiple candidates remain.

## AI-ready specification rules

| Rule | Apply it by |
| --- | --- |
| Precise language | Use explicit, testable statements; avoid idioms, metaphors, and context-dependent references. |
| Clear classification | Distinguish requirements, constraints, guidelines, patterns, recommendations, interfaces, and dependencies. |
| Structured formatting | Use headings, lists, tables, and code blocks so Generative AIs can parse the file reliably. |
| Defined terms | Define all acronyms, abbreviations, and domain-specific terms. |
| Self-contained context | Include examples, edge cases, rationale, and dependencies needed to use the spec without hidden context. |
| Well formed Markdown | Keep frontmatter, headings, tables, and fences syntactically valid. |

## File naming

The specification must stay in `/spec/` and use `[a-z0-9-]+.md`. The name should describe the content and start with one high-level purpose: `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`.

## Specification structure

Update the file so these sections are present and filled appropriately:

| Section | Required content |
| --- | --- |
| Frontmatter | `title`, optional `version`, `date_created`, optional `last_updated`, optional `owner`, optional `tags`. |
| `# Introduction` | Short introduction and goal. |
| `## 1. Purpose & Scope` | Purpose, scope, audience, and assumptions. |
| `## 2. Definitions` | Acronyms, abbreviations, and domain terms. |
| `## 3. Requirements, Constraints & Guidelines` | `REQ-001`, `SEC-001`, `[3 LETTERS]-001`, `CON-001`, `GUD-001`, and `PAT-001` style entries as applicable. |
| `## 4. Interfaces & Data Contracts` | Interfaces, APIs, schemas, examples, or integration points. |
| `## 5. Acceptance Criteria` | `AC-001` entries in Given-When-Then format where appropriate. |
| `## 6. Test Automation Strategy` | Test Levels, Frameworks such as MSTest, FluentAssertions, and Moq when applicable, Test Data Management, CI/CD Integration, Coverage Requirements, and Performance Testing. |
| `## 7. Rationale & Context` | Reasoning behind requirements, constraints, and guidelines. |
| `## 8. Dependencies & External Integrations` | External Systems, Third-Party Services, Infrastructure Dependencies, Data Dependencies, Technology Platform Dependencies, and Compliance Dependencies. |
| `## 9. Examples & Edge Cases` | Code or data examples, including edge cases. |
| `## 10. Validation Criteria` | Criteria or tests required for compliance. |
| `## 11. Related Specifications / Further Reading` | Related specs and relevant external documentation. |

Dependencies should focus on architectural and business needs, not package implementation details. For example, specify `OAuth 2.0 authentication library` rather than `Microsoft.AspNetCore.Authentication.JwtBearer v6.0.1` unless a version is an architectural constraint.

## Procedure

1. Read the existing specification file and the new requirement or code-change evidence.
2. Preserve stable identifiers unless the meaning changes. Add new IDs sequentially.
3. Update frontmatter, including `last_updated` when appropriate.
4. Revise affected requirements, constraints, interfaces, acceptance criteria, dependencies, examples, and validation criteria.
5. Ensure every new or changed requirement has acceptance criteria and validation coverage.
6. Save the updated spec in `/spec/` with the required filename convention.
7. Report changed sections and any unresolved assumptions.

## Legacy placeholders

Older invocations may name the target as `${file}` and ask for `ai-ready` specifications. Preserve frontmatter placeholder meanings such as `Team/Individual`, `YYYY-MM-DD`, and `Platform/runtime` while replacing them with concrete values in the updated file.

## Output template

```markdown
## Specification update result

**Status:** updated | needs clarification | blocked
**Specification:** `/spec/<purpose-name>.md`
**Change source:** <requirements, code files, or user request>

### Sections changed
| Section | Change summary | Requirement IDs affected |
| --- | --- | --- |
| `<section>` | `<summary>` | `<REQ/SEC/CON/GUD/PAT/AC IDs>` |

### Validation
- Filename convention `[a-z0-9-]+.md`: pass | fail
- Required sections present: pass | fail
- New or changed requirements have acceptance criteria: pass | fail
- Markdown and frontmatter well formed: pass | fail

### Follow-up
<unresolved assumptions or `None`>
```

## Quality gate

- [ ] The existing specification file was read before editing.
- [ ] The file remains under `/spec/` and follows `[a-z0-9-]+.md` with an approved purpose prefix.
- [ ] All required sections are present and populated.
- [ ] Requirements, constraints, guidelines, patterns, and acceptance criteria use stable IDs.
- [ ] New or changed requirements have testable acceptance criteria and validation criteria.
- [ ] Dependencies describe architectural or business needs rather than unnecessary package versions.
- [ ] The document is self-contained, unambiguous, and well formed Markdown.

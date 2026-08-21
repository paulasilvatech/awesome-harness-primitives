---
name: "creating-oracle-to-postgres-migration-bug-report"
description: >-
  Create structured bug reports for Oracle-to-PostgreSQL migration defects with source-of-truth Oracle behavior, PostgreSQL divergence, severity, root cause, remediation, validation, and filename convention. Use when documenting behavioral differences, failed migration tests, or data-layer defects during an Oracle-to-PostgreSQL migration.
---

# Creating Oracle-to-PostgreSQL migration bug reports

Turn a migration defect into a reproducible report that compares Oracle baseline behavior with PostgreSQL behavior and names the exact remediation and validation path while preserving runtime/language context.

## When to invoke

- "Create a bug report for this Oracle-to-PostgreSQL migration defect."
- "Document this PostgreSQL behavior difference from Oracle."
- "Write a migration bug report with severity and root cause."
- "Save a BUG_REPORT file for this stored procedure issue."

## Prerequisites and context

- Use `references/BUG-REPORT-TEMPLATE.md` as the report template.
- Oracle is the source of truth for expected behavior.
- Save reports to `.github/oracle-to-postgres-migration/Reports/{ProjectName}/BUG_REPORT_<DescriptiveSlug>.md`.
- `{ProjectName}` is the project assembly or folder name with spaces normalized to `-`, for example `MyApp.DataAccess`.
- `<DescriptiveSlug>` is a short PascalCase defect identifier such as `EmptyStringNullHandling` or `RefCursorUnwrapFailure`.
- Preserve search compatibility with legacy migration notes that used `assembly/folder` and ` (e.g. ` wording.

## Bug report fields

| Field | Required content |
| --- | --- |
| Status | `RESOLVED`, `UNRESOLVED`, or `IN PROGRESS`. |
| Component | Affected endpoint, repository, stored procedure, function, package, query, or migration file. |
| Test | Related automated test names or the missing test that should be added. |
| Severity | Low, Medium, High, or Critical based on impact scope. |
| Problem | Expected Oracle behavior versus observed PostgreSQL behavior. |
| Scenario | Ordered reproduction with seed data, operation, expected result, and actual result. |
| Root Cause | The specific Oracle/PostgreSQL behavioral difference causing the defect. |
| Solution | Changes made or required, including explicit file paths. |
| Validation | Steps to confirm the fix on both Oracle and PostgreSQL. |

## Oracle-to-PostgreSQL defect taxonomy

| Difference | Evidence to capture | Typical remediation direction |
| --- | --- | --- |
| Empty string vs. NULL | Input value, stored value, comparison result. | Normalize at data boundary or adjust SQL predicates deliberately. |
| Type coercion strictness | Oracle accepted implicit conversion but PostgreSQL rejected or compared differently. | Add explicit casts or correct parameter types. |
| Collation and sorting | Ordered result differs. | Specify intended PostgreSQL collation or query order. |
| Sequence values | Generated IDs diverge or sequence starts incorrectly. | Align sequence ownership, start value, and next value. |
| Time zones | Timestamp comparison or display differs. | Use the correct timestamp type and explicit timezone handling. |
| Padding | `CHAR`/`VARCHAR` comparisons or trailing spaces differ. | Trim, change type, or preserve Oracle semantics intentionally. |
| Constraints | PostgreSQL rejects data Oracle allowed, or missing constraints allow bad data. | Add, relax, or migrate constraints with justification. |

Client code changes should be avoided unless required for correct behavior; when proposed, document and justify them clearly.

## Writing rules

- Use plain language, short sentences, and clear next actions.
- Use present or past tense consistently.
- Use bullets and numbered lists for reproduction steps and validations.
- Include minimal SQL excerpts and logs as evidence; omit sensitive data and keep snippets reproducible.
- Stick to existing runtime and language versions; avoid speculative fixes.

## Progressive disclosure and bundled resources

- `references/BUG-REPORT-TEMPLATE.md`: canonical report structure to copy before filling evidence.

## Output template

```markdown
## Oracle-to-PostgreSQL migration bug report

**Status:** created | draft | blocked
**File:** `.github/oracle-to-postgres-migration/Reports/<ProjectName>/BUG_REPORT_<DescriptiveSlug>.md`

### Report fields
| Field | Value |
| --- | --- |
| Status | `RESOLVED` / `UNRESOLVED` / `IN PROGRESS` |
| Component | `<endpoint, repository, stored procedure, or file>` |
| Test | `<test names>` |
| Severity | `Low` / `Medium` / `High` / `Critical` |
| Root Cause | `<Oracle/PostgreSQL behavioral difference>` |

### Validation
- Oracle baseline reproduced: <yes/no>
- PostgreSQL divergence reproduced: <yes/no>
- Fix verified on both databases: <yes/no or pending>
```

## Quality gate

- [ ] The report uses `references/BUG-REPORT-TEMPLATE.md`.
- [ ] Oracle behavior is stated as expected behavior and PostgreSQL behavior is stated as observed behavior.
- [ ] Severity is justified by impact scope.
- [ ] Root cause names a concrete Oracle/PostgreSQL behavioral difference, not a vague migration failure.
- [ ] Scenario includes seed data, operation, expected result, and actual result.
- [ ] Solution names explicit file paths and avoids client changes unless justified.
- [ ] Validation covers both Oracle and PostgreSQL.
- [ ] Filename follows `.github/oracle-to-postgres-migration/Reports/{ProjectName}/BUG_REPORT_<DescriptiveSlug>.md`.

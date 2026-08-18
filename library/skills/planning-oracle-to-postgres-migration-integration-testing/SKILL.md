---
name: "planning-oracle-to-postgres-migration-integration-testing"
description: >-
  Create an integration testing plan for one .NET project during Oracle-to-PostgreSQL migration. Use when planning coverage for repositories, DAOs, stored procedure callers, CRUD service layers, Oracle-specific behavior, seed data, or migration validation cases before writing integration tests.
---

# Planning integration testing for Oracle-to-PostgreSQL migration

Analyze one .NET target project for database-touching artifacts, rank Oracle-to-PostgreSQL migration risk, and write a concrete integration testing plan that captures Oracle behavior as the golden source.

## When to invoke

- "Plan integration tests for this Oracle-to-PostgreSQL migrated project."
- "Find data access methods that need migration validation tests."
- "Create the TARGET_PROJECT integration testing plan."
- "Prioritize Oracle-specific repository behavior for PostgreSQL migration."
- "List seed data and test cases for DAOs and stored procedure callers."

## Scope rules

| Boundary | Rule |
| --- | --- |
| Single project scope | Plan only artifacts inside the target project; do not include neighboring applications. |
| Database interactions only | Include repositories, DAOs, stored procedure callers, and service layers performing CRUD operations. Skip business logic with no database touchpoint. |
| Oracle golden source | Tests capture Oracle's expected behavior first, then compare PostgreSQL behavior against it. |
| No multi-connection harnessing | Migrated applications are copied and renamed, for example `MyApp.Postgres`; each instance targets one database. |
| Output path | Write the plan to `.github/oracle-to-postgres-migration/Reports/{TARGET_PROJECT} Integration Testing Plan.md`. |

## Risk classification

| Priority | Database behavior | Examples |
| --- | --- | --- |
| P0 | Oracle-specific semantics likely to differ on PostgreSQL. | refcursors, `TO_CHAR`, implicit type coercion, `NO_DATA_FOUND`, sequence/default behavior, date truncation. |
| P1 | Complex CRUD or query composition with joins, filters, pagination, transactions, or concurrency. | Repository search methods, DAO batch writes, service-layer write flows. |
| P2 | Simple CRUD with straightforward mappings. | Single-row insert, update, read, delete with no Oracle-specific functions. |
| Excluded | No direct database interaction. | Pure calculation, formatting, validation, or orchestration without persistence. |

## Required test-case themes

| Theme | Include cases |
| --- | --- |
| Text parameters | Empty string and `NULL`/missing values; verify Oracle empty-string-as-null differences when relevant. |
| Datetime/timezone | Round-trip and comparison behavior; include explicit timezone-application expectations. |
| PostgreSQL timestamp targets | Destination columns using `timestamp without time zone` or `timestamp(0)`; verify precision and timezone semantics. |
| Oracle exceptions | `NO_DATA_FOUND` and equivalent no-row behavior in PostgreSQL. |
| Formatting and coercion | `TO_CHAR`, implicit numeric/text/date coercion, and formatting-sensitive comparisons. |
| Seed data | Minimal deterministic rows for each method, including boundary and no-match cases. |

## Procedure

1. Identify data access artifacts in the target project: repositories, DAOs, stored procedure callers, and service layers that perform CRUD operations.
2. Record method signatures and database touchpoints for each artifact.
3. Classify each artifact and method by migration risk using the priority table.
4. Define recommended integration test cases, seed data, and expected Oracle behavior for every included database touchpoint.
5. Add known Oracle→PostgreSQL behavioral differences to validate, especially text, datetime/timezone, `TO_CHAR`, implicit coercion, and `NO_DATA_FOUND` cases.
6. Write the markdown plan to `.github/oracle-to-postgres-migration/Reports/{TARGET_PROJECT} Integration Testing Plan.md`.

## Plan contents

| Section | Required detail |
| --- | --- |
| Target project | Project name, path, and scope exclusions. |
| Testable artifacts | Classes and method signatures that touch the database. |
| Priority map | P0/P1/P2 classification with reason. |
| Recommended cases | Positive, no-row, null/empty, boundary, formatting, timezone, and error-path cases as applicable. |
| Seed data | Required tables/entities, rows, and cleanup/rollback assumptions. |
| Oracle→PostgreSQL differences | Behavior that must be asserted during migration validation. |
| Coverage mapping | Every database touchpoint has at least one test case, or high-risk methods have justified multiple cases. |

## Output template

```markdown
# <TARGET_PROJECT> Integration Testing Plan

**Status:** planned | blocked
**Target project:** `<path/to/project.csproj>`
**Output path:** `.github/oracle-to-postgres-migration/Reports/{TARGET_PROJECT} Integration Testing Plan.md`

## Testable artifacts
| Artifact | Method signature | Database touchpoint | Priority | Reason |
| --- | --- | --- | --- | --- |
| `<class>` | `<method>` | `<table/procedure/query>` | P0/P1/P2 | `<migration risk>` |

## Recommended test cases
| Artifact method | Case | Seed data | Oracle behavior to capture | PostgreSQL difference to validate |
| --- | --- | --- | --- | --- |
| `<method>` | `<case name>` | `<rows>` | `<expected Oracle result>` | `<difference>` |

## Coverage mapping
| Database touchpoint | Covered by | Gap or justification |
| --- | --- | --- |
| `<touchpoint>` | `<test case>` | `<none or reason>` |
```

## Quality gate

- [ ] Only one target project is in scope.
- [ ] Every repository, DAO, stored procedure caller, and CRUD service layer in scope was considered.
- [ ] Business logic without database interaction was excluded.
- [ ] Oracle-specific features such as refcursors, `TO_CHAR`, implicit type coercion, and `NO_DATA_FOUND` are prioritized.
- [ ] Text parameter cases include empty string and `NULL`/missing values.
- [ ] Datetime/timezone cases include round-trip and comparison behavior.
- [ ] `timestamp without time zone` and `timestamp(0)` destinations include timezone-application expectations.
- [ ] Every database touchpoint has coverage or a documented justification.
- [ ] The plan is written to `.github/oracle-to-postgres-migration/Reports/{TARGET_PROJECT} Integration Testing Plan.md`.

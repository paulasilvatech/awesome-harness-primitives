---
name: creating-oracle-to-postgres-migration-integration-tests
description: >-
  Create Phase 3 Oracle integration tests for .NET data access artifacts before
  Oracle-to-PostgreSQL migration, capturing Oracle behavior as the golden baseline while keeping
  assertions portable for Phase 6. Use when the user asks to add integration tests for
  repositories, DAOs, stored procedure callers, query builders, seed data, or lookup constants
  before PostgreSQL migration begins.
---

<!-- Generated from harness/github-copilot/skills/creating-oracle-to-postgres-migration-integration-tests/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Creating Oracle-to-PostgreSQL migration integration tests

Generate integration tests for one target .NET project that execute against Oracle, seed only minimal collision-safe data, and preserve expected behavior so the same logical tests can be ported during Phase 6 PostgreSQL migration.

## When to invoke

- "Create Oracle integration tests before migrating this project to PostgreSQL."
- "Add Phase 3 tests for these .NET repositories or DAOs."
- "Capture Oracle behavior as the baseline for migration."
- "Write portable tests for stored procedure callers before Phase 6."
- "Create seed data and LookupConstants for Oracle migration tests."

## Prerequisites and context

- Use only during Phase 3, before any PostgreSQL migration work has begun.
- The test project must already exist and compile; scaffolding the project is a separate task.
- Read the existing base test class, seed manager, seed file conventions, and project file before writing tests.
- Scope all work to the single target project named by the user.

## Procedure

1. Discover the test project conventions.
2. Identify testable data access artifacts in the target project only.
3. Create minimal seed data that does not disturb existing database rows.
4. Write integration test cases for each database-touching method and important branch.
5. Review determinism and portability before considering the tests complete.

## Step 1: Discover conventions

| Inspect | Learn |
| --- | --- |
| Base test class | Inheritance pattern, automatic transaction create/rollback, connection ownership, setup/teardown behavior. |
| Seed manager | How seed data is loaded, verified, isolated, and rolled back. |
| Project file | Test framework, Oracle dependencies, build target, nullable settings, and package conventions. |
| Existing tests | Naming, arrange/act/assert style, fixture boundaries, lookup helpers, and assertion granularity. |

## Step 2: Identify testable artifacts

Scope to data access methods in the target project: repositories, DAOs, stored procedure callers, query builders, direct SQL wrappers, and database-backed services. Exclude artifacts outside the project and code paths that do not touch the database.

| Artifact type | Minimum test target |
| --- | --- |
| Repository or DAO method | One successful query or command per method, plus high-risk branch coverage. |
| Stored procedure caller | Parameter mapping, returned rows/values, output parameters, and expected error type when meaningful. |
| Query builder | Generated behavior through execution, not only string shape, unless string generation is the artifact's contract. |
| Write path | Insert/update/delete effect verified by readback inside the rollback transaction. |

## Step 3: Seed data rules

- Follow existing seed file location and naming conventions.
- Avoid `TRUNCATE TABLE`; preserve existing business rows and lookup rows.
- Assume existing business rows and lookup rows are already present; add only minimal, collision-safe seed records needed for the scenario.
- Do not commit seed data into shared databases; tests run in transactions that roll back.
- Ensure seed data cannot conflict with other tests by using stable unique identifiers or namespaced values.
- Load and verify seed data before assertions depend on it.
- Create or reuse a test `LookupConstants` class for stable lookup IDs/codes used across seed builders and assertions.

## Step 4: Test-writing rules

| Rule | Rationale |
| --- | --- |
| Inherit from the base test class | Reuse automatic transaction create/rollback and project infrastructure. |
| Cover every database-touching method in scope | Phase 3 tests become the Oracle golden source. |
| Assert rows, columns, counts, error types, and returned values | Logical outputs survive PostgreSQL migration better than vendor messages. |
| Assert concrete values from seed data | `not null` or `not empty` assertions miss behavioral regressions. |
| Include empty-string and `NULL`/missing input for text parameters where applicable | Oracle and PostgreSQL differ around empty string semantics. |
| Validate datetime write/read precision | Use the Oracle column's precision, for example seconds-only for date/time columns without fractional seconds. |
| Avoid redundant assertions | Each test should prove a distinct behavior or branch. |
| Avoid impossible behavior | Do not test code paths that cannot occur in the implementation. |

## Migration vocabulary

This skill covers `oracle-to-postgresql` migration preparation only. Prefer additional tests for `higher-risk` behavior branches. Base classes should provide transaction `create/rollback.` behavior, and assertions should avoid weak `non-empty` checks when seed data provides exact expected values.
## Step 5: Determinism review

Re-examine every assertion that checks non-null values. Confirm the value is controlled by seed data, stable lookup rows, or a deterministic database response. Replace environment-dependent assertions with seeded values, explicit counts, or documented gaps.

## Limits

- Do not invoke during Phase 6 or against a project already migrated to PostgreSQL.
- Do not create PostgreSQL-targeting tests in this phase.
- Do not scaffold a missing test project; require the test project to already exist and compile.
- Do not create tests for artifacts outside the target project.
- Do not rewrite or wipe pre-existing business or lookup rows.

## Gotchas

- **Oracle is the golden source**: capture Oracle behavior now, even if PostgreSQL will later implement it differently.
- **Portability is in assertions**: avoid platform-specific SQL syntax and error-message text in assertions.
- **Transactions are the cleanup mechanism**: preserve data with rollback, not destructive setup.
- **Empty string matters**: cover both empty-string and `NULL`/missing text input where the method accepts text parameters.

## Output template

```markdown
## Oracle migration integration tests result — <target project>

**Status:** created | partial | blocked
**Phase:** 3 Oracle baseline
**Target project:** `<project>`
**Test project:** `<test project>`

### Coverage
| Artifact | Methods tested | Seed data | Assertions | Notes |
| --- | --- | --- | --- | --- |
| `<repository/DAO/procedure/query builder>` | `<methods>` | `<seed files or builders>` | rows/columns/counts/error types/readback | <notes> |

### Validation
- Test project compiled: pass | fail | not run
- Integration tests run: pass | fail | not run
- Determinism review complete: yes | no
- PostgreSQL work avoided: yes | no
```

## Quality gate

- [ ] The task is Phase 3 and the project has not begun Phase 6 PostgreSQL migration.
- [ ] The existing base test class, seed manager, seed conventions, and project file were read before writing tests.
- [ ] Work is scoped to one target project and only database-touching artifacts.
- [ ] Seed data is minimal, collision-safe, rollback-friendly, and does not use `TRUNCATE TABLE`.
- [ ] Tests inherit the base class and use existing transaction create/rollback infrastructure.
- [ ] Assertions use deterministic Oracle baseline behavior and concrete seed values.
- [ ] Text inputs include empty-string and `NULL`/missing coverage where applicable.
- [ ] Datetime assertions respect the Oracle column precision.
- [ ] No PostgreSQL-targeting test or Phase 6 behavior was introduced.

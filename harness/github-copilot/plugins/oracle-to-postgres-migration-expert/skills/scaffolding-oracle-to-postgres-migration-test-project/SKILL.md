---
name: "scaffolding-oracle-to-postgres-migration-test-project"
description: >-
  Scaffold a compilable xUnit integration test project for a .NET Oracle application before Oracle-to-PostgreSQL migration testing. Use when Phase 3 requires an Oracle baseline test project, transaction rollback infrastructure, seed data management, or an empty integration-test harness before writing tests.
---

# Scaffolding an integration test project for Oracle-to-PostgreSQL migration

Create an Oracle-targeting xUnit integration test project for oracle-to-postgresql migration for one .NET target project, preserving the application's runtime and package versions while adding rollback-safe database test infrastructure and a seed data convention.

## When to invoke

- "Scaffold the Oracle integration test project for this migration."
- "Create the Phase 3 xUnit test harness before we write Oracle baseline tests."
- "Add transaction rollback and seed data infrastructure for Oracle tests."
- "Prepare an empty integration test project for Oracle-to-PostgreSQL migration."

## Phase boundary

| Phase | Use this skill? | Rule |
| --- | --- | --- |
| Phase 3 Oracle baseline | Yes | Scaffold the Oracle-targeting project once, before writing Oracle behavior tests. |
| Phase 6 PostgreSQL validation | No | Produce the PostgreSQL test project by copying and migrating the Oracle project; do not run this skill again. |
| Ordinary unit testing | No | This skill creates integration infrastructure only, not unit tests or business logic tests. |

Oracle is the golden behavior source. Keep the scaffold pointed at Oracle through `Oracle.ManagedDataAccess.Core`; the migrated PostgreSQL project inherits structure from this baseline later.

## Project shape

| Artifact | Required content | Constraint |
| --- | --- | --- |
| Test `.csproj` | Same target framework as the application, xUnit packages, NuGet package references, `Oracle.ManagedDataAccess.Core`, and one project reference to the target project. | Match existing .NET, C#, and package versions exactly; do not upgrade. |
| `appsettings.json` | Oracle connection configuration suitable for local/test environments. | Do not commit secrets; use placeholders or existing configuration conventions. |
| Rollback base class | Opens a database connection and transaction before each test; rolls back in teardown. | Catch cleanup exceptions without hiding the original test failure; guarantee rollback after every test. |
| Seed data manager | Loads deterministic seed records inside the active transaction. | Do not commit seed data; do not use `TRUNCATE TABLE`; preserve existing database data. |
| Seed file convention | A stable location and naming pattern for downstream tests. | Pick a convention once and document it in the project README or test helper comments. |

## Procedure

1. Inspect the target project's `.csproj` and package references. Record the target framework and versions before creating anything.
2. Create a sibling xUnit test project for the single target project. Add only the target project reference; avoid dragging in unrelated application projects.
3. Add Oracle connectivity with `Oracle.ManagedDataAccess.Core` and configure `appsettings.json` for Oracle database connectivity.
4. Implement the inheritable transaction-rollback base class so each test opens a transaction and teardown always rolls it back.
5. Implement the seed data manager so test data loads within the transaction scope and never persists beyond the test.
6. Build the test project and finish only after compilation succeeds with zero errors.

## Infrastructure rules

| Rule | Why it matters |
| --- | --- |
| No test cases in the scaffold | Phase 3 scaffolding prepares infrastructure; later planning and authoring decide coverage. |
| No `TRUNCATE TABLE` | Tests must not destroy shared Oracle data while establishing baselines. |
| Roll back, do not clean up by delete scripts | Rollback keeps cleanup atomic even when assertions fail. |
| One target project per scaffold | Cross-project references hide ownership and make migration parity harder to prove. |
| Match existing versions | Version drift can create false migration differences unrelated to Oracle/PostgreSQL behavior. |

## Output template

```markdown
### Oracle integration test scaffold

**Status:** complete | blocked
**Target project:** `<path/to/target.csproj>`
**Test project:** `<path/to/test-project.csproj>`

| Artifact | Created | Evidence |
| --- | --- | --- |
| xUnit project | yes/no | `<file path>` |
| Oracle package | yes/no | `Oracle.ManagedDataAccess.Core` |
| Project reference | yes/no | `<referenced project>` |
| Transaction rollback base class | yes/no | `<file path>` |
| Seed data manager | yes/no | `<file path>` |
| Oracle appsettings | yes/no | `<file path>` |

**Validation**
- `dotnet build <test-project.csproj>`: pass | fail
```

## Quality gate

- [ ] The target `.csproj` was inspected before scaffolding.
- [ ] The test project targets the same .NET version as the application under test.
- [ ] `Oracle.ManagedDataAccess.Core` and xUnit are present without unrelated package upgrades.
- [ ] The test project references only the intended target project.
- [ ] The rollback base class guarantees transaction rollback after every test.
- [ ] The seed data manager loads data inside the transaction and never uses `TRUNCATE TABLE`.
- [ ] `appsettings.json` contains Oracle connectivity placeholders without secrets.
- [ ] The scaffold contains infrastructure only and no test cases.
- [ ] The test project builds with zero errors.

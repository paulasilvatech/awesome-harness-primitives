---
name: creating-oracle-to-postgres-master-migration-plan
description: >-
  Discover .NET solution projects, classify Oracle-to-PostgreSQL migration eligibility, detect
  Oracle dependencies, and write
  .github/oracle-to-postgres-migration/Reports/MasterMigrationPlan.md. Use when starting a
  multi-project Oracle-to-PostgreSQL migration, inventorying .NET projects, or assessing Oracle
  dependency scope.
---

<!-- Generated from harness/github-copilot/plugins/oracle-to-postgres-migration-expert/skills/creating-oracle-to-postgres-master-migration-plan/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Creating an Oracle-to-PostgreSQL master migration plan

Analyze a .NET solution, classify every project for Oracle to PostgreSQL migration, and produce a persistent master plan that downstream migration agents and skills can parse.

## When to invoke

- "Create the Oracle to Postgres master migration plan."
- "Inventory this .NET solution for Oracle dependencies."
- "Classify which projects need PostgreSQL migration."
- "Write `.github/oracle-to-postgres-migration/Reports/MasterMigrationPlan.md`."

## Prerequisites and context

Work from the repository root. Find a `.sln` or `.slnx` solution file in the workspace root; if multiple exist, ask the user which solution to plan. The output path is fixed: `.github/oracle-to-postgres-migration/Reports/MasterMigrationPlan.md`.

## Procedure

1. Discover projects in the selected solution.
2. Classify each project from file evidence.
3. Present the classified list and let the user adjust classifications or migration order before finalizing.
4. Write the plan file to `.github/oracle-to-postgres-migration/Reports/MasterMigrationPlan.md`.

Track progress explicitly:

```text
Progress:
- [ ] Step 1: Discover projects in the solution
- [ ] Step 2: Classify each project
- [ ] Step 3: Confirm with user
- [ ] Step 4: Write the plan file
```

## Discovery and classification

For each `.csproj`, record name, relative path, and likely project type such as class library, web API, console, or test. Scan every non-test project for Oracle evidence.

| Evidence source | Indicators |
| --- | --- |
| NuGet references | `Oracle.ManagedDataAccess`, `Oracle.EntityFrameworkCore` in `.csproj` or `packages.config`. |
| Configuration | Oracle connection strings in `appsettings.json`, `web.config`, or `app.config`. |
| Code usage | `OracleConnection`, `OracleCommand`, `OracleDataReader`. |
| DDL references | DDL cross-references under `.github/oracle-to-postgres-migration/DDL/Oracle/` when present. |
| Existing migrated duplicate | A `-postgres` or `.Postgres` project duplicate that appears processed. |
| Test project signals | Test SDK references, test naming, or test-only project type. |

Assign exactly one classification:

| Classification | Meaning | Typical evidence |
| --- | --- | --- |
| `MIGRATE` | Has Oracle interactions requiring conversion. | Oracle NuGet packages, connection strings, `OracleConnection`, `OracleCommand`, `OracleDataReader`, or DDL cross-reference. |
| `SKIP` | No Oracle indicators. | UI-only, shared utility, or unrelated project. |
| `ALREADY_MIGRATED` | A PostgreSQL duplicate exists and appears processed. | `-postgres` or `.Postgres` paired project. |
| `TEST_PROJECT` | Test project handled by the testing workflow. | Test project naming or framework references. |

Order migration so shared/foundational libraries move before dependents.

## Plan file contract

Save this exact structure to `.github/oracle-to-postgres-migration/Reports/MasterMigrationPlan.md` because downstream consumers depend on the headings and tables.

````markdown
# Master Migration Plan

**Solution:** {solution file name}
**Solution Root:** {REPOSITORY_ROOT}
**Created:** {timestamp}
**Last Updated:** {timestamp}

## DDL Artifacts

**Location:** {path to DDL artifacts, e.g., `.github/oracle-to-postgres-migration/DDL/`}
**External tool used:** {Yes / No} — {If Yes, name the tool (e.g., `ora2pg`) and note that Phase 4 (Schema & DDL Migration) can be skipped; PostgreSQL DDL artifacts already exist.}

## Solution Summary

| Metric | Count |
|--------|-------|
| Total projects in solution | {n} |
| Projects requiring migration | {n} |
| Projects already migrated | {n} |
| Projects skipped (no Oracle usage) | {n} |
| Test projects (handled separately) | {n} |

## Project Inventory

| # | Project Name | Path | Classification | Notes |
|---|---|---|---|---|
| 1 | {name} | {relative path} | MIGRATE | {notes} |
| 2 | {name} | {relative path} | SKIP | No Oracle dependencies |

## Migration Order

1. **{ProjectName}** — {rationale, e.g., "Core data access library; other projects depend on it."}
2. **{ProjectName}** — {rationale}
````

## Gotchas

- **Do not classify from project names alone**: require file evidence for `MIGRATE`, `SKIP`, `ALREADY_MIGRATED`, or `TEST_PROJECT`.
- **Do not bury DDL status**: if `.github/oracle-to-postgres-migration/DDL/` exists or an external tool such as `ora2pg` produced PostgreSQL artifacts, record whether Phase 4 can be skipped.
- **Do not migrate dependents first**: shared data access libraries should precede web APIs, console apps, and consumers.

## Output template

```markdown
## Oracle-to-PostgreSQL master migration plan

**Status:** drafted | written | needs confirmation | blocked
**Solution:** `<solution.sln or solution.slnx>`
**Plan file:** `.github/oracle-to-postgres-migration/Reports/MasterMigrationPlan.md`

### Classification summary
| Classification | Count | Projects |
| --- | ---: | --- |
| `MIGRATE` | <n> | <names> |
| `SKIP` | <n> | <names> |
| `ALREADY_MIGRATED` | <n> | <names> |
| `TEST_PROJECT` | <n> | <names> |

### Migration order
1. <ProjectName> — <rationale>

### Confirmation needed
- <classification or ordering question, or none>
```

## Quality gate

- [ ] A single `.sln` or `.slnx` solution was selected or the user was asked to choose.
- [ ] Every `.csproj` reference in the solution appears in the Project Inventory.
- [ ] Each project has exactly one classification: `MIGRATE`, `SKIP`, `ALREADY_MIGRATED`, or `TEST_PROJECT`.
- [ ] Oracle evidence includes NuGet, config, code, DDL references, migrated duplicates, or test indicators.
- [ ] Shared libraries precede dependent projects in Migration Order.
- [ ] The plan was written to `.github/oracle-to-postgres-migration/Reports/MasterMigrationPlan.md` using the required structure.

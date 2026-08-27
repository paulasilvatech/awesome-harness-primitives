---
name: migrating-oracle-to-postgres-data-access-code
description: >-
  Migrate .NET/C# data access code from Oracle.ManagedDataAccess or Oracle.EntityFrameworkCore to
  PostgreSQL with Npgsql. Use when replacing OracleConnection, OracleCommand, OracleDataReader,
  OracleDbType mappings, stored procedure calls, connection strings, inline SQL, and EF Core
  provider configuration during an Oracle-to-PostgreSQL migration.
---

<!-- Generated from harness/github-copilot/plugins/oracle-to-postgres-migration-expert/skills/migrating-oracle-to-postgres-data-access-code/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Migrating Oracle to PostgreSQL data access code

Migrates the C# data access layer of a `.Postgres` project copy from Oracle providers to Npgsql while preserving behavior, using the migration reports as the source of truth, and validating with a build and Oracle-specific searches.

## When to invoke

- "Migrate this .NET data access code from Oracle to PostgreSQL."
- "Replace Oracle.ManagedDataAccess with Npgsql."
- "Fix OracleConnection and OracleCommand usage after migration."
- "Convert Oracle stored procedure calls and RefCursor handling to PostgreSQL."
- "Update Oracle.EntityFrameworkCore code to Npgsql.EntityFrameworkCore.PostgreSQL."

## Prerequisites and context

- Work only within the `.Postgres` project copy; never modify the original Oracle-targeting project.
- `Reports/{ProjectName}/MigrationChecklist.md` exists and is the source of truth for work items.
- `Reports/{ProjectName}/OracleRiskAnalysis.md` exists for behavioral differences.
- Keep existing .NET and C# versions; do not introduce newer language or runtime features.
- Oracle behavior is the source of truth; document behavioral differences as bug reports, not silent changes.

## Procedure

1. Replace Oracle NuGet packages in the `.csproj`.
2. Update connection string configuration without hardcoding credentials.
3. Rewrite Oracle-specific ADO.NET type references and `using` directives.
4. Fix explicit `OracleDbType` mappings to `NpgsqlDbType` or remove unnecessary explicit typing.
5. Migrate stored procedure, refcursor, OUT parameter, sequence, and named parameter patterns.
6. Replace Oracle-specific inline SQL and query-builder syntax.
7. Build and verify; mark completed items in `Reports/{ProjectName}/MigrationChecklist.md`.

## Package and configuration changes

| Oracle dependency or setting | PostgreSQL replacement |
| --- | --- |
| `Oracle.ManagedDataAccess.Core` | `Npgsql` for ADO.NET. |
| `Oracle.EntityFrameworkCore` | `Npgsql.EntityFrameworkCore.PostgreSQL` for EF Core. |
| `Oracle.*` packages | Remove unless another non-data-access feature still requires them. |
| Oracle connection strings in `appsettings.json`, `appsettings.{env}.json`, `web.config`, `app.config`, or environment variable configuration | Npgsql string such as `Host=localhost;Port=5432;Database=mydb;Username=myuser;Password=...`. |
| `OracleConnection` key names | Keep the same key unless Oracle-specific naming forces a change. |
| `IConfiguration` or secrets manager | Continue using the existing mechanism; do not hardcode credentials. |

If `IDbConnection` or `IDbCommand` abstractions are registered through DI, update the DI registration and connection string first; consuming code may need fewer changes.

## ADO.NET type mapping

| Oracle type | Npgsql replacement |
| --- | --- |
| `OracleConnection` | `NpgsqlConnection` |
| `OracleCommand` | `NpgsqlCommand` |
| `OracleDataReader` | `NpgsqlDataReader` |
| `OracleDataAdapter` | `NpgsqlDataAdapter` |
| `OracleParameter` | `NpgsqlParameter` |
| `OracleTransaction` | `NpgsqlTransaction` |
| `OracleException` | `NpgsqlException` |
| `OracleDbType` | `NpgsqlDbType` from the `NpgsqlTypes` namespace |
| `using Oracle.ManagedDataAccess.Client` | `using Npgsql` |
| `OracleRefCursor` | Remove cursor wrapping and use PostgreSQL refcursor or set-returning function handling. |

## DbType and SQL mappings

| Oracle construct | PostgreSQL or Npgsql replacement |
| --- | --- |
| `OracleDbType.Varchar2` | `NpgsqlDbType.Varchar` or omit and let Npgsql infer. |
| `OracleDbType.Clob` | `NpgsqlDbType.Text`. |
| `OracleDbType.Number` | `NpgsqlDbType.Numeric` or `NpgsqlDbType.Integer` depending on precision. |
| `OracleDbType.Date` | `NpgsqlDbType.Date` for date only or `NpgsqlDbType.Timestamp` when time is used. |
| `OracleDbType.TimeStamp` | `NpgsqlDbType.Timestamp`. |
| `OracleDbType.RefCursor` | `NpgsqlDbType.Refcursor`; call inside a transaction and `FETCH ALL IN "<cursor_name>"`. |
| `OracleDbType.Char` | `NpgsqlDbType.Char`. |
| `ROWNUM <= n` | `LIMIT n`. |
| `ROWNUM = 1` | `LIMIT 1`. |
| `NVL(x, y)` | `COALESCE(x, y)`. |
| `DECODE(expr, v1, r1, ...)` | `CASE WHEN expr = v1 THEN r1 ... END`. |
| `SYSDATE` / `SYSTIMESTAMP` | `NOW()` or `CURRENT_TIMESTAMP`. |
| `TO_CHAR(date, fmt)` | Mostly compatible; verify format strings. |
| `TO_DATE(str, fmt)` | Verify format strings. |
| `TO_NUMBER(str)` | `CAST(str AS NUMERIC)` or `str::NUMERIC`. |
| `||` string concat | Compatible. |
| `SELECT {SEQUENCE}.NEXTVAL FROM DUAL` | `SELECT nextval('{sequence_name}')`; remove `FROM DUAL`. |
| `CONNECT BY` hierarchy | Rewrite with recursive CTEs using `WITH RECURSIVE`. |
| `MERGE INTO` | Rewrite as `INSERT ... ON CONFLICT DO UPDATE`. |
| Empty string `''` as NULL | PostgreSQL does not treat `''` as NULL; review comparisons and `IS NULL` guards. |
| `VARCHAR2` | `VARCHAR` or `TEXT`. |
| Oracle named parameter `:param_name` | Npgsql named parameter `@param_name`. |

## Stored procedures and EF Core

| Area | Rule |
| --- | --- |
| `CommandType.StoredProcedure` | Retain for function calls when supported by target Npgsql version. |
| Procedures with `OUT` parameters | PostgreSQL may require `CommandType.Text` with `CALL proc_name(...)`; verify against the target Npgsql version. |
| `RETURNS TABLE` / `RETURNS SETOF` | Use `ExecuteReader()` directly; no cursor parameter needed. |
| `RETURNS refcursor` | Open a transaction, execute function, read cursor name, then `FETCH ALL IN "<cursor_name>"`. |
| `OUT` / `INOUT` | Verify `ParameterDirection` matches the migrated signature. |
| EF Core provider | Replace `.UseOracle(...)` with `.UseNpgsql(...)`. |
| EF Core builder | Remove `OracleDbContextOptionsBuilder` references. |
| `OnModelCreating` | Review Oracle-specific `HasColumnType("NUMBER")` and use `HasColumnType("numeric")` or PostgreSQL type names. |
| Sequences | `modelBuilder.HasSequence<int>("seq_name").StartsAt(1).IncrementsBy(1)` is compatible; verify column defaults. |
| EF migrations | Do not run EF Core migrations; schema is managed externally via DDL scripts from Phase 4. |

## Validation

```bash
dotnet build
grep -R "Oracle.ManagedDataAccess\|OracleConnection\|OracleCommand\|OracleDataReader\|OracleDbType\|OracleRefCursor" <PostgresProject>
grep -R ":[A-Za-z_][A-Za-z0-9_]*" <PostgresProject>
```

Fix compilation errors, then mark completed items in `Reports/{ProjectName}/MigrationChecklist.md`.

## Gotchas

- **Do not migrate outside the `.Postgres` copy**: the Oracle project must remain available for comparison.
- **Do not assume stored procedures map 1:1**: refcursor, `OUT`, `INOUT`, and set-returning functions require different patterns.
- **Do not silently change empty-string behavior**: Oracle treats `''` as NULL; PostgreSQL does not.
- **Do not add newer packages just because they exist**: keep version pinning consistent with the solution and target .NET version.

## Migration compatibility notes

Check `System.Data` abstractions such as `IDbConnection` and `IDbCommand` before broad rewrites; `project-wide`, `surface-level` changes may be enough. In `DbContext` configuration, replace Oracle provider setup. Search for combined patterns such as `OracleConnection/OracleCommand/OracleDataReader`, `:param`, and `cursor-wrapping` code. Use `Reports/{ProjectName}/OracleRiskAnalysis.md` for `cross-referencing`; `SELECT expr` replaces Oracle's dummy table pattern. Use Npgsql ADO.NET and/or EF Core packages as needed.

## Output template

```markdown
### Oracle to PostgreSQL data access migration result

**Status:** migrated | partially migrated | blocked
**Project:** `<.Postgres project>`
**Checklist:** `Reports/{ProjectName}/MigrationChecklist.md`

| Step | Files changed | Notes |
| --- | --- | --- |
| NuGet packages | `<.csproj>` | <removed Oracle packages and added Npgsql packages> |
| Connection strings | `<config file>` | <key and secret handling> |
| ADO.NET types | `<files>` | <type replacements> |
| DbType mappings | `<files>` | <mapping decisions> |
| Stored procedures | `<files>` | <CALL/refcursor/returns handling> |
| SQL syntax | `<files>` | <Oracle constructs replaced> |

**Validation**
- `dotnet build`: pass | fail
- Oracle namespace/type search: pass | fail
- `Reports/{ProjectName}/MigrationChecklist.md` updated: yes | no
```

## Quality gate

- [ ] Only the `.Postgres` copy was modified.
- [ ] `Reports/{ProjectName}/MigrationChecklist.md` drove the work and was updated.
- [ ] Oracle packages were removed and Npgsql packages added consistently.
- [ ] Connection strings use Npgsql format and existing secret mechanisms.
- [ ] `Oracle.ManagedDataAccess`, `OracleConnection`, `OracleCommand`, `OracleDataReader`, `OracleDbType`, and `OracleRefCursor` no longer remain unless justified.
- [ ] Stored procedure, refcursor, `OUT`, `INOUT`, sequence, and `:param_name` patterns were reviewed.
- [ ] `dotnet build` passes or every failure is reported with evidence.

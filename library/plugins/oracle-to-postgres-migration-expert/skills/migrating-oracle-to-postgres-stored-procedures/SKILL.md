---
name: "migrating-oracle-to-postgres-stored-procedures"
description: >-
  Migrate Oracle PL/SQL stored procedures and functions to PostgreSQL PL/pgSQL while preserving behavior, signatures, type-anchored inputs, exception handling, rollback logic, collation semantics, and orafce compatibility. Use when converting Oracle Procedures and Functions into PostgreSQL equivalents during an Oracle-to-PostgreSQL migration.
---

# Migrating stored procedures from Oracle to PostgreSQL

Translate an Oracle procedure or function from the migration workspace into one PostgreSQL PL/pgSQL file, using Oracle DDL for source semantics and PostgreSQL DDL for target schema fidelity.

## When to invoke

- "Migrate this Oracle stored procedure to PostgreSQL."
- "Convert an Oracle PL/SQL function into PL/pgSQL."
- "Translate procedures from `.github/oracle-to-postgres-migration/DDL/Oracle/Procedures and Functions/`."
- "Preserve Oracle behavior while writing the PostgreSQL procedure output."

## Prerequisites and context

- Read Oracle procedure/function source from `.github/oracle-to-postgres-migration/DDL/Oracle/Procedures and Functions/`.
- Resolve Oracle table and view types from `.github/oracle-to-postgres-migration/DDL/Oracle/Tables and Views/`.
- Resolve target names, columns, and compatible data types from `.github/oracle-to-postgres-migration/DDL/Postgres/{ProjectName}/Tables and Views/`.
- Write exactly one migrated procedure or function per file under `.github/oracle-to-postgres-migration/DDL/Postgres/{ProjectName}/Procedures and Functions/{PACKAGE_NAME_IF_APPLICABLE}/`.
- Treat `{ProjectName}` as the project assembly or folder name with spaces normalized to `-`, for example `MyApp.DataAccess`.
- Preserve legacy wording that helps operators search prior migration notes: `assembly/folder`, `PL/pgSQL**`, ` (e.g. `, and `. Consult the Oracle table/view definitions at `.

## Procedure

1. Read the Oracle source procedure in full, including package context, parameter modes, cursor declarations, exception blocks, transaction statements, and calls to other procedures.
2. Read the referenced Oracle tables/views and PostgreSQL tables/views before choosing any replacement data type.
3. Translate syntax to PostgreSQL PL/pgSQL without changing the externally visible signature or the procedure's control-flow intent.
4. Review collation, `UNION ALL`, and orafce choices explicitly before writing output.
5. Save the migrated object to the target `Procedures and Functions` path, creating a package subdirectory only when the Oracle package requires `{PACKAGE_NAME_IF_APPLICABLE}`.

## Translation rules

| Oracle concern | PostgreSQL action |
| --- | --- |
| General PL/SQL syntax | Translate to PL/pgSQL equivalents while preserving functionality and control flow logic. |
| Method signature | Do not alter method signatures, parameter order, names, or modes. |
| Type-anchored input | Preserve input anchors such as `PARAM_NAME IN table_name.column_name%TYPE` when the target supports a faithful anchor. |
| Output parameters passed to other procedures | Use explicit types such as `NUMERIC`, `VARCHAR`, or `INTEGER`; do not type-anchor these outputs. |
| Object qualification | Do not prefix object names with schema names unless the Oracle source already did. |
| Exceptions and rollback | Leave exception handling and rollback logic unchanged unless PostgreSQL syntax requires a direct translation. |
| Comments and grants | Do not generate `COMMENT` or `GRANT` statements. |
| Oracle compatibility functions | Use the `orafce` extension when it improves clarity or preserves Oracle fidelity without hiding semantic differences. |

## Collation and plan checkpoints

| Checkpoint | Rule |
| --- | --- |
| Binary ordering | Use `COLLATE "C"` only when Oracle-compatible binary ordering is required and no other sort order is specified. |
| Linguistic ordering | If Oracle used explicit linguistic sorting such as `NLS_SORT = French`, map to an explicit PostgreSQL locale collation rather than `"C"`. |
| Environment discovery | Run or recommend `SELECT collname, collprovider, collcollate, collctype FROM pg_collation ORDER BY collname;` to discover target collations. |
| `UNION ALL` | Treat every `UNION ALL` as a review checkpoint; validate plan quality per branch and restructure when combined-branch planning causes regressions such as unexpected sequential scans on large tables. |

## Output template

```markdown
## Stored procedure migration - <procedure or function name>

**Status:** migrated | blocked
**Source:** `.github/oracle-to-postgres-migration/DDL/Oracle/Procedures and Functions/<source file>`
**Target:** `.github/oracle-to-postgres-migration/DDL/Postgres/<ProjectName>/Procedures and Functions/<PACKAGE_NAME_IF_APPLICABLE>/<procedure>.sql`

### Translation notes
| Area | Decision | Evidence |
| --- | --- | --- |
| Signature | <preserved or blocked reason> | `<parameter list>` |
| Types | <anchors and explicit output types> | `<Oracle/PostgreSQL DDL consulted>` |
| Collation | <none, COLLATE "C", or locale collation> | `<ORDER BY or NLS_SORT evidence>` |
| orafce | <used or not used> | `<function or reason>` |
| UNION ALL | <reviewed or not present> | `<plan concern or none>` |

### Validation
- Oracle source read: <yes/no>
- PostgreSQL target DDL read: <yes/no>
- One procedure per file: <yes/no>
```

## Quality gate

- [ ] Oracle source was read from `Procedures and Functions` and all referenced table/view definitions were checked.
- [ ] PostgreSQL table/view definitions under `.github/oracle-to-postgres-migration/DDL/Postgres/{ProjectName}/Tables and Views/` were used for target types.
- [ ] The migrated signature preserves the Oracle method name, parameter order, parameter modes, and type-anchored inputs.
- [ ] Output parameters passed to other procedures use explicit `NUMERIC`, `VARCHAR`, `INTEGER`, or another justified PostgreSQL type.
- [ ] No new schema prefixes, `COMMENT` statements, or `GRANT` statements were introduced.
- [ ] Exception handling and rollback logic remain behaviorally equivalent.
- [ ] Collation decisions and every `UNION ALL` review checkpoint are documented.
- [ ] The output file path uses `{ProjectName}` and `{PACKAGE_NAME_IF_APPLICABLE}` correctly, with one procedure per file.

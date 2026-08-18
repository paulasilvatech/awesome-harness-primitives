---
name: sql-server-table-reconciliation
description: >-
  Compare SQL Server tables across source and target instances for migration validation, ETL verification, production versus staging checks, schema drift, missing rows, extra rows, and column mismatches. Use this skill when the user asks for SQL Server reconciliation reports, and use mssql-python with Apache Arrow for fast extraction.
---

# SQL Server table reconciliation

Compare identical SQL Server tables across two instances with Python, `mssql-python`, Apache Arrow, and primary-key based row matching, then produce a reconciliation report for schema drift, missing rows, extra rows, and mismatched values.

## When to invoke

- "Compare these SQL Server tables between production and staging."
- "Validate a data migration with a reconciliation report."
- "Find row mismatches after this ETL load."
- "Detect schema drift between two SQL Server databases."
- "Use mssql-python and Arrow to compare large tables."

## Inputs

Collect these before execution:

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| Source server | Yes | - | Source SQL Server, for example `prod-server.database.windows.net`. |
| Source database | Yes | - | Source database name. |
| Target server | Yes | - | Target SQL Server, for example `staging-server.database.windows.net`. |
| Target database | Yes | - | Target database name. |
| Tables | Yes | - | Comma-separated `schema.table` names or `schema.*`, for example `dbo.Orders,dbo.Items` or `dbo.*`. |
| Auth mode | Yes | - | `sql` for user/password or username/password, or `entra` for Azure `AD/token`. |
| Primary key | Auto-detect | metadata | Column or columns forming row identity. Ask if auto-detect fails. |
| Columns to compare | No | all non-PK | Comma-separated subset. |
| Chunk size | No | `100000` | Rows per batch for large tables. |
| Output format | No | `console` | `console`, `csv`, `parquet`, or `json`. |

## Prerequisites and context

Install runtime packages only when the environment lacks them:

```bash
pip install mssql-python pyarrow pandas
```

The bundled script lives at `scripts/reconcile.py` and must be run from the skill package or with the correct relative path.

## Procedure

1. Collect connection details for source and target.
2. Identify the primary key or composite key; auto-detect from metadata, then ask the user if no key is found.
3. Detect schema differences before row comparison.
4. Extract data through Apache Arrow with `cursor.arrow()`.
5. Compare by primary-key join, never by positional row order.
6. Normalize types, compare columns, and generate the requested report format.

```bash
python scripts/reconcile.py     --source-server <source_server>     --source-database <source_database>     --target-server <target_server>     --target-database <target_database>     --tables "<table_spec>"     --auth <sql|entra>     --chunk-size <chunk_size>     --output <console|csv|json>
```

Optional arguments:

| Argument | Description |
| --- | --- |
| `--primary-key` | Comma-separated PK columns; omit to auto-detect. |
| `--columns` | Comma-separated columns to compare; omit for all non-PK columns. |

Example with SQL auth:

```bash
python scripts/reconcile.py     --source-server prod-server.database.windows.net     --source-database ProdDB     --target-server staging-server.database.windows.net     --target-database StagingDB     --tables "dbo.Orders"     --auth sql     --output console
```

Example wildcard with Entra auth and CSV:

```bash
python scripts/reconcile.py     --source-server prod-server.database.windows.net     --source-database ProdDB     --target-server staging-server.database.windows.net     --target-database StagingDB     --tables "dbo.*"     --auth entra     --output csv
```

## Comparison rules

| Rule | Implementation |
| --- | --- |
| Type normalization | Cast decimals to the same precision, trim strings, and normalize datetimes to UTC. |
| NULL handling | Treat `NULL == NULL` as a match. |
| Row order | Ignore row order; join by primary key. |
| Large tables | Use chunk extraction with `OFFSET/FETCH` or `ROW_NUMBER()` partitioning. |
| Credentials | Never hardcode credentials; read `MSSQL_USER` and `MSSQL_PASSWORD` from `os.environ` or prompt with `getpass`. |
| Query safety | Use parameterized queries with `?` placeholders for metadata lookups; never f-string interpolate user input into SQL. |

For tables above 1M rows, pre-check row hashes and fetch full rows only for mismatches:

```sql
SELECT {pk_cols},
       HASHBYTES('SHA2_256', CONCAT_WS('|', col1, col2, ...)) AS row_hash
FROM {table}
```

## Performance strategy

| Scenario | Strategy |
| --- | --- |
| `< 100K rows` | Single Arrow fetch and in-memory pandas compare. |
| `100K–1M rows` | Chunked extraction using `100000` row batches and streaming comparison. |
| `> 1M rows` | Hash pre-check, then fetch only mismatched rows. |
| Wide tables, `100+` columns | Compare PK plus hash first, then drill into mismatched columns. |
| Network-constrained | Prefer Arrow columnar transfer, commonly 10-50x smaller than row-by-row extraction. |

## Gotchas

- **Use `mssql-python`, not `pyodbc` or `pymssql`**; the workflow depends on Arrow support.
- **Use connection string format**; keyword arguments such as `encrypt=True` throw errors.
- **Never compare without a primary key**; positional comparison produces false mismatches.
- **Do not print credentials** in reports, errors, or logs.
- **Handle connection failures with retry logic** instead of failing silently.

## Progressive disclosure and bundled resources

- `scripts/reconcile.py`: standalone reconciliation script that accepts the source, target, table, auth, chunking, and output arguments described above.

## Report format

For multi-table runs, use compact per-table rows and expand detail only for tables with `FAIL` or `DIFFERENCES FOUND` status. Include examples such as `dbo.JOBS` when showing multiple tables.

```text
Reconciling dbo.EMPLOYEES...
Reconciling dbo.DEPARTMENTS...
Reconciling dbo.JOBS...

=== Summary: 2 passed, 1 failed, 0 skipped / 3 tables ===
```

`MUST` requirements in this skill are hard constraints, not preferences.

## Output template

```markdown
## SQL Server reconciliation

**Status:** identical | differences found | blocked
**Source:** `<source server>/<source database>`
**Target:** `<target server>/<target database>`

| Table | Source rows | Target rows | Missing | Extra | Mismatches | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `dbo.EMPLOYEES` | 107 | 107 | 0 | 0 | 0 | IDENTICAL |
| `dbo.DEPARTMENTS` | 27 | 27 | 0 | 0 | 3 | DIFFERENCES FOUND |

### Detail for failed tables
- `<schema.table>`: <schema drift, sample missing PKs, sample mismatched columns>

### Validation
- Primary key detection: <pass|fail>
- Extraction mode: <single Arrow|chunked|hash pre-check>
- Credentials handling: <environment|getpass|blocked>
```

## Quality gate

- [ ] `mssql-python`, Apache Arrow via `cursor.arrow()`, and pandas comparison are used.
- [ ] Source and target schemas are checked before row comparison.
- [ ] Every table is compared by primary key or explicitly blocked when no key exists.
- [ ] Decimal, string, datetime, and `NULL` comparison rules are applied.
- [ ] Large tables use chunking or `HASHBYTES('SHA2_256', CONCAT_WS(...))` optimization.
- [ ] Credentials come from `MSSQL_USER`, `MSSQL_PASSWORD`, or `getpass` and are never logged.

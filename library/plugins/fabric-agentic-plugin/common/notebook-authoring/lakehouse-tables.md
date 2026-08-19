# Lakehouse Table Operations — SQL References, Discovery, DDL/DML

How to reference, discover, and operate on Lakehouse tables from notebook cells using Spark SQL.

## Spark SQL Table References

Use with `spark.sql()` or `%%sql` cells. Format uses **dotted names**, not file paths.

### Non-Default Lakehouse — Fully-Qualified Names

| Schema-Enabled | Format | Example |
|---|---|---|
| Yes | `{Workspace}.{Lakehouse}.{Schema}.{Table}` | `SELECT * FROM MyWorkspace.MyLakehouse.dbo.sales` |
| No | `{Workspace}.{Lakehouse}.{Table}` | `SELECT * FROM MyWorkspace.MyLakehouse.sales` |

**Special characters** (hyphens, spaces, leading numbers): wrap each segment in backticks:

```sql
SELECT * FROM `Workspace-1`.`Lakehouse-2`.`dbo`.`TableName`
```

### Default Lakehouse — Short Names

| Schema-Enabled | Format Options | Recommended |
|---|---|---|
| Yes | `{lakehouseName}.{Schema}.{Table}` or `{Schema}.{Table}` | Include lakehouse name for clarity |
| No | `{Table}` | Direct table name |

---

## Schema and Table Discovery

### List Schemas

- **Default lakehouse**: `SHOW SCHEMAS` returns all schemas
- **Non-default lakehouse**: `SHOW SCHEMAS IN \`{Workspace}\`.\`{Lakehouse}\``

### List Tables

| Context | SQL Command |
|---|---|
| Default, schema-enabled | `SHOW TABLES IN {schema_name}` (e.g., `SHOW TABLES IN dbo`) |
| Default, non-schema | `SHOW TABLES` |
| Non-default, schema-enabled | `SHOW TABLES IN \`{Workspace}\`.\`{Lakehouse}\`.\`{Schema}\`` |
| Non-default, non-schema | `SHOW TABLES IN \`{Workspace}\`.\`{Lakehouse}\`` |

### Spark Catalog API (Alternative)

`spark.catalog.listTables()` — lists tables in the default schema of the default lakehouse. Only shows the current default schema (usually `dbo`), not all schemas.

---

## Spark SQL DDL/DML Operations

Fabric Lakehouse tables use Delta Lake format. These operations work in `%%sql` cells or via `spark.sql()`.

### DDL — Schema & Table Management

| Operation | Syntax |
|---|---|
| Create schema | `CREATE SCHEMA IF NOT EXISTS {schema}` |
| Create table | `CREATE TABLE IF NOT EXISTS {schema}.{table} (col1 INT, col2 STRING) USING DELTA` |
| Add column | `ALTER TABLE {schema}.{table} ADD COLUMNS (new_col DOUBLE)` |
| Describe table | `DESCRIBE TABLE EXTENDED {schema}.{table}` |
| Drop table | `DROP TABLE IF EXISTS {schema}.{table}` |

### DML — Data Manipulation

| Operation | Syntax |
|---|---|
| Insert | `INSERT INTO {schema}.{table} VALUES (1, 'a')` |
| Insert from query | `INSERT INTO {schema}.{table} SELECT * FROM source_table` |
| Update | `UPDATE {schema}.{table} SET col1 = 'new' WHERE condition` |
| Delete | `DELETE FROM {schema}.{table} WHERE condition` |

### MERGE (Upsert)

```sql
MERGE INTO {schema}.target AS t
USING source AS s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.value = s.value
WHEN NOT MATCHED THEN INSERT (id, value) VALUES (s.id, s.value)
```

### Delta Lake Time Travel

| Operation | Syntax |
|---|---|
| Read by version | `SELECT * FROM {table} VERSION AS OF 3` |
| Read by timestamp | `SELECT * FROM {table} TIMESTAMP AS OF '2024-01-01'` |
| View history | `DESCRIBE HISTORY {schema}.{table}` |
| Restore version | `RESTORE TABLE {schema}.{table} TO VERSION AS OF 3` |

**Note**: All table references follow the same default/non-default, schema-enabled rules from [Spark SQL Table References](#spark-sql-table-references). Use backticks for special characters.

**Note**: `SHOW TABLES` without `IN` clause on a schema-enabled lakehouse only shows tables in the current default schema (usually `dbo`), not all schemas.

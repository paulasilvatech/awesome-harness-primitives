# Lakehouse Path Construction — ABFSS, Relative Paths, OneLake Endpoint

How to construct correct data paths when accessing Lakehouse resources from notebook cells.

## Context Determination

**ALWAYS verify before constructing paths:**

1. **Is the target lakehouse the default lakehouse** for the current notebook?
2. **Is the lakehouse schema-enabled?** — Inspect table metadata, query `SHOW SCHEMAS`, or check lakehouse properties via REST API. Default schema is commonly `dbo`.
3. **What API type is being used?** — PySpark/Delta DataFrame API uses file paths; Spark SQL uses dotted table names. These are NOT interchangeable.
4. **Session restart required after changes** — after pinning a new default lakehouse or renaming it, restart the Spark session for changes to take effect.

---

## API File Paths

Use with `spark` / `pandas` / `duckdb` / `polars` etc. APIs that require file paths.

### Non-Default Lakehouse — Absolute ABFSS Paths Required

Retrieve the OneLake endpoint dynamically (see [OneLake Endpoint Configuration](#onelake-endpoint-configuration)), then construct paths:

| Resource Type | Schema-Enabled | Path Pattern |
|---|---|---|
| Files | N/A | `abfss://{workspace_id}@{onelake_endpoint}/{lakehouse_id}/Files/{file_path}` |
| Tables | Yes | `abfss://{workspace_id}@{onelake_endpoint}/{lakehouse_id}/Tables/{schema_name}/{table_name}` |
| Tables | No | `abfss://{workspace_id}@{onelake_endpoint}/{lakehouse_id}/Tables/{table_name}` |

### Default Lakehouse — Relative Paths (only for Spark API)

| Resource Type | Schema-Enabled | Path Pattern |
|---|---|---|
| Files | N/A | `Files/{file_path}` |
| Tables (load) | Yes | `Tables/{schema_name}/{table_name}` |
| Tables (load) | No | `Tables/{table_name}` |
| Tables (saveAsTable) | Yes | `{schema_name}.{table_name}` |
| Tables (saveAsTable) | No | `{table_name}` |

---

## ABFSS Path Construction Rules

**CRITICAL: Never mix IDs and names in the same ABFSS path.**

| Approach | Workspace Segment | Lakehouse Segment | Recommended? |
|---|---|---|---|
| All GUIDs | `{workspace_id}` | `{lakehouse_id}` | **Yes** — immutable, survives renames |
| All Names | `{workspace_name}` | `{lakehouse_name}.Lakehouse` | OK — note `.Lakehouse` suffix required |
| Mixed | `{workspace_id}` | `{lakehouse_name}.Lakehouse` | **NO — will fail at runtime** |

**Best Practice**: Prefer GUIDs for programmatic access — they are immutable and won't break on resource renames.

---

## OneLake Endpoint Configuration

**Always retrieve the endpoint dynamically** — never hardcode:

```python
onelake_endpoint = notebookutils.conf.get("trident.onelake.endpoint").replace("https://", "")
# Result example: "onelake.dfs.fabric.microsoft.com"
```

The endpoint varies by environment (public, sovereign clouds). Hardcoding causes failures when notebooks run in different environments.

---

## Default Lakehouse Shortcuts

The default lakehouse is mounted at `/lakehouse/default/`:

- **Pandas / Python I/O**: use mount point — `pd.read_parquet("/lakehouse/default/Files/sample.parquet")`
- **Spark API**: use relative paths — `spark.read.parquet("Files/sample.parquet")`
- **Spark SQL**: use table name directly — `SELECT * FROM my_table`

---

## Default Lakehouse Metadata

Use `notebookutils.runtime.context` to retrieve default lakehouse information at runtime:

| Property | Context Key |
|---|---|
| Lakehouse ID | `defaultLakehouseId` |
| Lakehouse Name | `defaultLakehouseName` |
| Lakehouse Workspace ID | `defaultLakehouseWorkspaceId` |
| Lakehouse Workspace Name | `defaultLakehouseWorkspaceName` |

---

## Quick Reference Table

| API Type | Lakehouse | Schema-Enabled | Path Format |
|---|---|---|---|
| PySpark (non-default) / Other SDK | Files | N/A | `abfss://{ws_id}@{endpoint}/{lh_id}/Files/{path}` |
| PySpark (non-default) / Other SDK | Tables | Yes | `abfss://{ws_id}@{endpoint}/{lh_id}/Tables/{schema}/{table}` |
| PySpark (non-default) / Other SDK | Tables | No | `abfss://{ws_id}@{endpoint}/{lh_id}/Tables/{table}` |
| PySpark (default) | Files | N/A | `Files/{path}` |
| PySpark (default) | Tables | Yes | `Tables/{schema}/{table}` |
| PySpark (default) | Tables | No | `Tables/{table}` |

`{endpoint}` = retrieved via `notebookutils.conf.get("trident.onelake.endpoint").replace("https://", "")`

For Spark SQL table references and dotted name syntax, see [lakehouse-tables.md](lakehouse-tables.md).

**Additional Reference:** [Load data in lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data)

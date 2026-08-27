# External Hive Metastore → Fabric Lakehouse Migration

Migrate Synapse workspaces that use an **external Hive Metastore** (backed by Azure SQL Database or Azure Database for MySQL) to Fabric Lakehouses.

> **When to use this guide**: Your Synapse Spark pools are configured with `spark.hadoop.javax.jdo.option.ConnectionURL` pointing to an external database. If your workspace uses the **built-in HMS** (no external connection configured), use [lake-database-migration.md](lake-database-migration.md) instead.
>
> **Deprecation notice**: External HMS support in Synapse is deprecated after Spark 3.4. Fabric does not support connecting to an external Hive Metastore — all metadata must be migrated into the Fabric Lakehouse catalog.
>
> **Auth tokens needed** (see [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) for commands):
> - Synapse ARM audience: `https://management.azure.com` (for detection)
> - HMS database: JDBC credentials (SQL auth or Entra ID) to query the external HMS
> - Fabric audience: `https://api.fabric.microsoft.com`

---

## Migration Workflow

```
External HMS Migration:
├── Step 0: Detect external HMS configuration
├── Step 1: Connect to HMS database and inventory databases & tables
├── Step 2: Select databases to migrate and choose mapping mode
├── Step 3: Create Fabric Lakehouse(es)
├── Step 4: Create schemas (if using schema mapping)
├── Step 5: Create OneLake shortcuts (Delta → Tables/, non-Delta → Files/)
├── Step 6: Handle non-Delta tables — convert to Delta or retain original format
├── Step 7: Validate
└── Step 8: (Optional) Validate before proceeding to Phase 2
```

---

## Step 0: Detect External HMS Configuration

Read the Spark pool configuration from the ARM API to determine if an external HMS is configured.

**Endpoint**:
```
GET https://management.azure.com/subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.Synapse/workspaces/{ws}/bigDataPools/{poolName}?api-version=2021-06-01
```

In the response, check `properties.sparkConfigProperties.content` for these keys:

| Spark Config Key | Present? | Meaning |
|---|---|---|
| `spark.hadoop.javax.jdo.option.ConnectionURL` | Yes | External HMS — this guide applies |
| `spark.hadoop.javax.jdo.option.ConnectionDriverName` | Yes | JDBC driver (e.g., `com.microsoft.sqlserver.jdbc.SQLServerDriver` for Azure SQL, `org.mariadb.jdbc.Driver` for MySQL) |
| `spark.hadoop.javax.jdo.option.ConnectionUserName` | Yes | HMS database username |
| `spark.hadoop.javax.jdo.option.ConnectionPassword` | Yes | HMS database password (may reference Key Vault) |
| `spark.sql.hive.metastore.version` | Optional | HMS version (e.g., `3.1.0`) |
| `spark.sql.hive.metastore.jars` | Optional | Path to HMS client JARs |

**If none of these keys are present**: The workspace uses the built-in HMS → use [lake-database-migration.md](lake-database-migration.md) instead.

### Extract Connection Details

```python
# Parse the JDBC connection URL from pool config
# Azure SQL DB example: jdbc:sqlserver://myserver.database.windows.net:1433;database=hive_metastore;...
# MySQL example: jdbc:mysql://myserver.mysql.database.azure.com:3306/hive_metastore?...

connection_url = spark_config["spark.hadoop.javax.jdo.option.ConnectionURL"]
driver = spark_config["spark.hadoop.javax.jdo.option.ConnectionDriverName"]
username = spark_config["spark.hadoop.javax.jdo.option.ConnectionUserName"]
# password may be a Key Vault reference — resolve before connecting
```

---

## Step 1: Inventory — Query the HMS Database

Connect to the external HMS database via JDBC and extract metadata. The Hive Metastore uses a standard schema (same structure for both Azure SQL DB and MySQL).

> **Namespace**: The external HMS has a **flat namespace** — `Database → Table`. There are no inner schemas. This simplifies mapping to Fabric.

### JDBC Connection Troubleshooting

If the JDBC connection to the external HMS database fails, check these common causes:

| Error | Cause | Fix |
|---|---|---|
| `Login failed for user` / `Access denied for user` | Wrong credentials or expired password | Verify username/password; check if Key Vault secret has rotated |
| `Cannot open server ... requested by the login` | Database name is wrong or database has been deleted | Verify the database name in the JDBC URL |
| `Connection timed out` / `No route to host` | Firewall blocks access from the machine running the migration | Add client IP to Azure SQL / MySQL firewall rules; check VNet/Private Endpoint settings |
| `SSL handshake failed` / `certificate verify failed` | TLS configuration mismatch | Add `encrypt=true;trustServerCertificate=true` (Azure SQL) or `useSSL=true&requireSSL=false` (MySQL) to JDBC URL |
| `com.microsoft.sqlserver.jdbc.SQLServerException: TCP/IP connection ... has failed` | SQL Server is paused or stopped (serverless) | Resume the Azure SQL DB in the Portal |
| `Communications link failure` | Network-level connectivity issue (DNS, proxy, VPN) | Test connectivity with `Test-NetConnection -ComputerName {server} -Port {port}` |

### 1a. List Databases

```sql
SELECT
    d.DB_ID,
    d.NAME           AS database_name,
    d.DB_LOCATION_URI AS location,
    d.OWNER_NAME     AS owner
FROM DBS d
ORDER BY d.NAME;
```

### 1b. List Tables with Storage Info

```sql
SELECT
    d.NAME           AS database_name,
    t.TBL_NAME       AS table_name,
    t.TBL_TYPE       AS table_type,       -- MANAGED_TABLE or EXTERNAL_TABLE
    s.LOCATION       AS data_location,
    s.INPUT_FORMAT   AS input_format,
    s.OUTPUT_FORMAT  AS output_format,
    tp_provider.PARAM_VALUE AS spark_provider,  -- 'delta', 'parquet', etc.
    tp_delta.PARAM_VALUE    AS is_delta          -- non-null if Delta table
FROM TBLS t
JOIN DBS d    ON t.DB_ID = d.DB_ID
JOIN SDS s    ON t.SD_ID = s.SD_ID
LEFT JOIN TABLE_PARAMS tp_provider
    ON t.TBL_ID = tp_provider.TBL_ID AND tp_provider.PARAM_KEY = 'spark.sql.sources.provider'
LEFT JOIN TABLE_PARAMS tp_delta
    ON t.TBL_ID = tp_delta.TBL_ID AND tp_delta.PARAM_KEY = 'delta.lastCommitTimestamp'
ORDER BY d.NAME, t.TBL_NAME;
```

**Detecting table format**:

| How to detect | Condition | Format |
|---|---|---|
| `spark.sql.sources.provider` = `'delta'` | Preferred | Delta |
| `delta.lastCommitTimestamp` is not null | Fallback | Delta |
| `INPUT_FORMAT` contains `parquet` and no delta markers | — | Parquet |
| `INPUT_FORMAT` contains `orc` | — | ORC |
| `INPUT_FORMAT` contains `Text` or `csv` | — | CSV/Text |
| `spark.sql.sources.provider` = `'parquet'` | — | Parquet |
| `spark.sql.sources.provider` = `'orc'` | — | ORC |

### 1c. List Columns

```sql
SELECT
    d.NAME           AS database_name,
    t.TBL_NAME       AS table_name,
    c.COLUMN_NAME,
    c.TYPE_NAME,
    c.INTEGER_IDX    AS ordinal_position
FROM COLUMNS_V2 c
JOIN SDS s    ON c.CD_ID = s.CD_ID
JOIN TBLS t   ON t.SD_ID = s.SD_ID
JOIN DBS d    ON t.DB_ID = d.DB_ID
ORDER BY d.NAME, t.TBL_NAME, c.INTEGER_IDX;
```

### 1d. List Partition Keys

```sql
SELECT
    d.NAME           AS database_name,
    t.TBL_NAME       AS table_name,
    pk.PKEY_NAME     AS partition_column,
    pk.PKEY_TYPE     AS partition_type,
    pk.INTEGER_IDX   AS ordinal_position
FROM PARTITION_KEYS pk
JOIN TBLS t   ON pk.TBL_ID = t.TBL_ID
JOIN DBS d    ON t.DB_ID = d.DB_ID
ORDER BY d.NAME, t.TBL_NAME, pk.INTEGER_IDX;
```

### 1e. List Partitions (for non-Delta tables)

```sql
SELECT
    d.NAME           AS database_name,
    t.TBL_NAME       AS table_name,
    p.PART_ID,
    s.LOCATION       AS partition_location,
    p.CREATE_TIME
FROM PARTITIONS p
JOIN TBLS t   ON p.TBL_ID = t.TBL_ID
JOIN DBS d    ON t.DB_ID = d.DB_ID
JOIN SDS s    ON p.SD_ID = s.SD_ID
ORDER BY d.NAME, t.TBL_NAME, p.CREATE_TIME;
```

> **Delta tables**: Skip partition enumeration — Delta handles partitions internally via `_delta_log`. Only query partitions for non-Delta tables that need `MSCK REPAIR TABLE` after migration.

### 1f. Summary Output

After running the queries, produce an inventory summary:

```
External HMS Inventory:
  HMS Database: jdbc:sqlserver://myserver.database.windows.net;database=hive_metastore
  Total databases: 5
  Total tables: 142

  Database: sales (37 tables)
    Delta tables: 30 (24 managed, 6 external)
    Parquet tables: 5 (all external)
    ORC tables: 2 (all managed)
    Partitioned tables: 8

  Database: marketing (22 tables)
    Delta tables: 22 (all managed)
    Partitioned tables: 3

  Database: staging (45 tables)
    ...
```

---

## Step 2: Select Databases and Choose Mapping Mode

### Database Selection

If the external HMS is **shared with other platforms** (HDInsight, Databricks), not all databases may be Synapse-owned. Ask the user which databases to migrate:

```json
{
  "databasesToMigrate": ["sales", "marketing", "staging"],
  "databasesToSkip": ["hdinsight_etl", "databricks_ml"]
}
```

> If the HMS is **Synapse-only** (being decommissioned), migrate all databases.

### Mapping Mode

Choose one of two modes:

#### Mode A: Schemas in One Lakehouse (Default)

All selected HMS databases → schemas within **one** target Lakehouse.

| HMS Database | Fabric Target |
|---|---|
| `sales` | Schema `sales` in target Lakehouse |
| `marketing` | Schema `marketing` in target Lakehouse |
| `staging` | Schema `staging` in target Lakehouse |
| `default` | Schema `dbo` (Lakehouse default) |

**Advantages**: Fewer items to manage; cross-schema queries via 2-part names; single SQL endpoint.

**Disadvantages**: Less isolation; shared OneLake path; harder to assign per-database permissions.

> **No schema collision risk**: The external HMS has a flat namespace (Database → Table), so each database name maps directly to a Fabric schema name with no composite naming needed.

#### Mode B: Separate Lakehouses

Each selected HMS database → its own Fabric Lakehouse.

| HMS Database | Fabric Target |
|---|---|
| `sales` | Lakehouse `sales` |
| `marketing` | Lakehouse `marketing` |
| `staging` | Lakehouse `staging` |

**Advantages**: Strong isolation; independent security (OneLake RBAC per Lakehouse); independent SQL endpoints.

**Disadvantages**: More items to manage; cross-database queries require 3-part names.

> **Recommended when**: The HMS is shared with other platforms and you want clear isolation for migrated databases, or different databases are owned by different teams.

### Emit Mapping Report

Before creating anything, show the user the planned mapping:

```
External HMS Migration Plan:
  Source: jdbc:sqlserver://myserver.database.windows.net;database=hive_metastore
  Mode: A (schemas in one Lakehouse)
  Target Lakehouse: MigratedData_Lakehouse

  HMS sales.customers         → MigratedData_Lakehouse.sales.customers (Delta, shortcut)
  HMS sales.orders            → MigratedData_Lakehouse.sales.orders (Delta, shortcut)
  HMS sales.legacy_archive    → MigratedData_Lakehouse.sales.legacy_archive (Parquet, Files/)
  HMS marketing.campaigns     → MigratedData_Lakehouse.marketing.campaigns (Delta, shortcut)
  HMS staging.raw_events      → MigratedData_Lakehouse.staging.raw_events (Delta, shortcut)
```

---

## Step 3: Create Fabric Lakehouse(es)

**Endpoint**: `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items`

```json
{
  "displayName": "{lakehouseName}",
  "type": "Lakehouse",
  "description": "Migrated from external Hive Metastore",
  "creationPayload": {
    "enableSchemas": true
  }
}
```

- **Mode A**: Create one Lakehouse with `enableSchemas: true`
- **Mode B**: Create one Lakehouse per selected database (still use `enableSchemas: true`)

> Returns HTTP 202 (LRO). Poll `Location` header until `status == "Succeeded"`. Capture the `id` for subsequent steps.

---

## Step 4: Create Schemas (Mode A Only)

For each selected HMS database, create the corresponding Fabric schema:

```sql
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS marketing;
CREATE SCHEMA IF NOT EXISTS staging;
-- 'default' database maps to the built-in 'dbo' schema — no creation needed
```

Execute via:
- **SQL endpoint**: Connect to the Lakehouse SQL endpoint
- **Fabric notebook**: Run in a notebook cell attached to the Lakehouse
- **Livy session**: `POST /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livySessions`

---

## Step 5: Create OneLake Shortcuts

For each table in the selected databases, create a shortcut based on format and type.

### Shortcut Target Decision

| Table Format | Shortcut Location | Catalog Registration |
|---|---|---|
| **Delta** | `Tables/{schema}/{tableName}` | Auto-registers in Lakehouse catalog |
| **Parquet / ORC / CSV / Avro** | `Files/{schema}/{tableName}` | Not auto-registered — handle in Step 6 |

### Parse Storage Location

The `SDS.LOCATION` (or `data_location` from Step 1b) provides the ADLS Gen2 path. Parse it into shortcut parameters:

**Managed tables** (typical warehouse directory):
```
abfss://{container}@{storage}.dfs.core.windows.net/synapse/workspaces/{workspace}/warehouse/{database}.db/{tableName}
```
- `location`: `https://{storage}.dfs.core.windows.net`
- `subpath`: `/{container}/synapse/workspaces/{workspace}/warehouse/{database}.db/{tableName}`

> **Note**: External HMS managed tables may use `.db` suffix in the warehouse directory (e.g., `sales.db/customers`), unlike built-in HMS which omits it. Check the actual `SDS.LOCATION` value.

**External tables** (arbitrary ADLS path):
```
abfss://{container}@{storage}.dfs.core.windows.net/{custom/path/to/table}
```
- `location`: `https://{storage}.dfs.core.windows.net`
- `subpath`: `/{container}/{custom/path/to/table}`

### Create Shortcut API

**Endpoint**: `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{lakehouseId}/shortcuts`

> **Note**: The endpoint uses `/items/{lakehouseId}/shortcuts`, NOT `/lakehouses/{lakehouseId}/shortcuts` (which returns 404).

```json
{
  "name": "{tableName}",
  "path": "Tables/{schemaName}",
  "target": {
    "type": "AdlsGen2",
    "adlsGen2": {
      "location": "https://{storageAccount}.dfs.core.windows.net",
      "subpath": "/{container}/{path/to/table}",
      "connectionId": "{connectionId}"
    }
  }
}
```

> **`connectionId` is required**. See [lake-database-migration.md § Step 4b](lake-database-migration.md#step-4b-discover-or-create-adls-connection) for how to discover or create the ADLS connection.

> For non-Delta tables, change `"path"` to `"Files/{schemaName}"`.

### Authentication for Shortcuts

The Fabric workspace identity (or creating user) must have **Storage Blob Data Reader** on the target ADLS Gen2 storage account.

---

## Step 6: Handle Non-Delta Tables

For non-Delta tables (Parquet, ORC, CSV, Avro), the shortcut is created under `Files/` but the table is **not auto-registered** in the Lakehouse catalog. Choose one option:

### Option A: Convert to Delta (Recommended)

```python
# Read from the shortcut path
df = spark.read.format("{originalFormat}").load("Files/{schemaName}/{tableName}")

# Write as Delta to the Tables section
df.write.format("delta").mode("overwrite").saveAsTable("{schemaName}.{tableName}")
```

For **partitioned tables** (identified in Step 1d):

```python
df = spark.read.format("parquet").load("Files/{schemaName}/{tableName}")
df.write.format("delta") \
    .partitionBy("{partitionCol}") \
    .mode("overwrite") \
    .saveAsTable("{schemaName}.{tableName}")
```

**Advantages**: Full Lakehouse catalog registration, SQL endpoint queries, Power BI Direct Lake, V-Order, ACID transactions.

### Option B: Retain Original Format

Keep tables in their legacy format under `Files/`. Register them in the catalog manually:

```sql
CREATE TABLE IF NOT EXISTS {schemaName}.{tableName}
USING {format}
LOCATION 'Files/{schemaName}/{tableName}';
```

For **Hive-style partitioned tables**, recover partition metadata:

```sql
CREATE TABLE IF NOT EXISTS {schemaName}.{tableName}
USING PARQUET
PARTITIONED BY ({partitionCols})
LOCATION 'Files/{schemaName}/{tableName}';

MSCK REPAIR TABLE {schemaName}.{tableName};
```

> **Why `MSCK REPAIR TABLE`?** Non-Delta tables rely on HMS partition metadata for partition pruning. Without this step, queries scan all files instead of pruning to relevant partitions.

### Comparison

| Capability | Delta (Option A) | Original Format (Option B) |
|---|---|---|
| Lakehouse catalog registration | Yes | Yes (after `CREATE TABLE`) |
| SQL endpoint queries | Yes | Yes |
| Power BI Direct Lake | Yes | **No** — requires Delta |
| V-Order optimization | Yes | **No** |
| ACID / time travel | Yes | **No** |
| Partition pruning | Automatic | Requires `MSCK REPAIR TABLE` |
| Data duplication | Yes (new copy) | **No** (zero-copy via shortcut) |

---

## Step 7: Validate

After migration, verify:

1. **Lakehouse catalog**: Check that tables appear in the Lakehouse Explorer UI under Tables
2. **SQL endpoint**: Query migrated tables via the SQL endpoint to confirm schema and data
3. **Row counts**: Compare row counts between HMS (via JDBC or Spark SQL on Synapse) and Fabric

    ```sql
    -- On Synapse (or via JDBC to HMS + Spark)
    SELECT COUNT(*) FROM sales.customers;

    -- On Fabric
    SELECT COUNT(*) FROM sales.customers;
    ```

4. **Shortcut health**: Verify shortcuts are accessible

    ```python
    notebookutils.fs.ls("Tables/sales/")
    notebookutils.fs.ls("Files/sales/")  # if non-Delta tables exist
    ```

5. **Partition coverage** (for Option B non-Delta tables): Verify partition counts match

    ```sql
    SHOW PARTITIONS {schemaName}.{tableName};
    ```

---

## Step 8: (Optional) Validate Before Proceeding to Phase 2

Run these checks before migrating Notebooks. Notebooks rely on Lakehouses being healthy — missing shortcuts or unregistered tables cause immediate runtime failures.

| Check | How | Pass Criteria |
|---|---|---|
| Shortcut health | `notebookutils.fs.ls("Tables/{schema}/")` and `Files/{schema}/` | All shortcuts resolve; no `PathNotFound` errors |
| Row counts | Compare `SELECT COUNT(*)` on HMS source (via JDBC/Spark) vs. Fabric for each table | Counts match |
| Schema comparison | Compare column names and types from HMS `COLUMNS_V2` vs. Fabric `DESCRIBE TABLE` | Exact match |
| Non-Delta registration | `SHOW TABLES IN {schema}` | All Option B tables appear in catalog |
| Partition coverage | `SHOW PARTITIONS {schema}.{table}` for Option B partitioned tables | Partition count matches HMS `PARTITIONS` table |

> **Do not proceed to Phase 2** until all shortcuts are healthy and row counts match. A notebook that reads from a missing or broken shortcut will fail silently or produce wrong results.

See [validation-testing.md → V2: Data Validation](validation-testing.md#v2-data-validation) for detailed scripts.

---

## Limitations and Considerations

| Limitation | Impact | Mitigation |
|---|---|---|
| **External HMS is deprecated after Spark 3.4** | No new development; should migrate sooner rather than later | This guide helps you migrate off it |
| **Fabric cannot connect to an external HMS** | Must copy metadata into Lakehouse catalog — no live connection | This guide extracts and recreates all metadata |
| **HMS functions (UDFs) are not migrated** | Custom functions stored in HMS are not extracted by these queries | Recreate manually via `spark.udf.register()` or `CREATE FUNCTION` |
| **HMS views are not migrated** | Views stored in HMS are not extracted | Extract view definitions (see query below), then recreate as Spark SQL views in Fabric |
| **Shared HMS — other platforms still using it** | Migrating databases to Fabric doesn't remove them from the external HMS | Coordinate with other platform teams; HMS remains untouched |
| **Large catalogs (10K+ tables)** | JDBC queries scale well, but shortcut creation is sequential (one API call per table) | Batch shortcut creation; consider parallel requests (respect API rate limits) |
| **Managed table data in Synapse storage** | Workspace-internal storage requires Fabric identity to have read access | Grant Storage Blob Data Reader before creating shortcuts |

**Extracting HMS view definitions**:

```sql
SELECT
    d.NAME AS database_name,
    t.TBL_NAME AS view_name,
    vt.PARAM_VALUE AS view_sql
FROM TBLS t
JOIN DBS d ON t.DB_ID = d.DB_ID
JOIN TABLE_PARAMS vt ON t.TBL_ID = vt.TBL_ID AND vt.PARAM_KEY = 'view.query.text'
WHERE t.TBL_TYPE = 'VIRTUAL_VIEW'
  AND vt.PARAM_VALUE IS NOT NULL
ORDER BY d.NAME, t.TBL_NAME;
```

> The view SQL is stored in the `view.query.text` parameter. Recreate in Fabric: `CREATE OR REPLACE VIEW {schema}.{view_name} AS {view_sql}`.

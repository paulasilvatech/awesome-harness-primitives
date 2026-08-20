# Synapse Lake Database → Fabric Lakehouse Migration

Migrate Synapse Lake Databases and Hive Metastore metadata to Fabric Lakehouses via REST APIs.

> **Hive Metastore Coverage**: Synapse's built-in Hive Metastore (HMS) and Lake Databases share the **same underlying catalog**. Databases, tables, views, and partitions created via Lake Database designer, Spark SQL (`CREATE DATABASE`, `CREATE TABLE`), or notebook code (`df.write.saveAsTable(...)`) are all stored in the built-in HMS and are all visible through the Lake Database REST API used in this guide. This means **HMS migration for managed/built-in metastores is fully covered here** — no separate HMS export/import notebooks are needed.
>
> **External Hive Metastore** (Azure SQL DB / MySQL-backed): If your Synapse workspace uses an external HMS, see [external-hms-migration.md](external-hms-migration.md) for the complete migration guide using JDBC queries. Fabric does not support connecting to an external HMS — all metadata must be migrated into the Fabric Lakehouse catalog. External HMS support in Synapse is deprecated after Spark 3.4.

> **Prerequisite**: Authenticate to both Synapse and Fabric APIs before starting (see [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes)).
> - Synapse data-plane audience: `https://dev.azuresynapse.net`
> - Fabric audience: `https://api.fabric.microsoft.com`

---

## Phase 1 Overview

Lake Databases must be migrated **before** Notebooks and Spark Job Definitions so that Fabric Lakehouses exist for notebook lakehouse binding (Phase 2, Step 4).

```
Phase 1: Lake Database Migration
├── Step 1: Inventory — list databases & tables from Synapse
├── Step 2: Choose mapping mode — schemas vs. separate Lakehouses
├── Step 3: Create Fabric Lakehouse(es)
├── Step 4: Create schemas (if using schema mapping mode)
├── Step 4b: Discover or create ADLS connection (probe-test candidates)
├── Step 5: Create OneLake shortcuts (Delta → Tables/, non-Delta → Files/)
├── Step 6: (Optional) Convert non-Delta tables to Delta
├── Step 7: Validate — verify catalog registration and data accessibility
└── Step 8: (Optional) Validate before proceeding to Phase 2
```

---

## Step 1: Inventory Synapse Lake Databases

### List All Databases

**Endpoint**: `GET {endpoint}/databases?api-version=2021-04-01`

```
GET https://{workspaceName}.dev.azuresynapse.net/databases?api-version=2021-04-01
```

Response contains `items[]` — each item has:
- `name` — database name
- `type` — always `"DATABASE"`
- `properties.source.location` — ADLS Gen2 base path (e.g., `abfss://container@storage.dfs.core.windows.net/dbname`)
- `properties.source.provider` — typically `"ADLS"`
- `properties.origin.type` — `"SPARK"` (Spark-native) or `"SQLOD"` (Serverless SQL-originated)

> **Filter**: Only migrate databases where `origin.type == "SPARK"` or `source.provider == "ADLS"`. Skip `SQLOD`-origin databases — these are Serverless SQL Pool views, not Spark Lake Databases.

### Get Database Details

**Endpoint**: `GET {endpoint}/databases/{databaseName}?api-version=2021-04-01`

Returns `DatabaseEntity` with `properties.source.location` (the warehouse directory path for managed tables).

### List Schemas in a Database

**Endpoint**: `GET {endpoint}/databases/{databaseName}/schemas?api-version=2021-04-01`

Returns `items[]` of schema objects. If only `default`/`dbo` exists, the database has no custom schemas.

### List Tables in a Database

**Endpoint**: `GET {endpoint}/databases/{databaseName}/tables?api-version=2021-04-01`

Each table item contains:
- `name` — table name
- `properties.tableType` — `"MANAGED"` or absent (external)
- `properties.namespace.databaseName` — parent database
- `properties.namespace.schemaName` — parent schema (may be `null` for default)
- `properties.storageDescriptor.columns[]` — column definitions with `name` and `originDataTypeName.typeName`
- `properties.storageDescriptor.format.formatType` — `"delta"`, `"parquet"`, `"csv"`, `"orc"`, `"avro"`, `"textfile"`, etc.
- `properties.storageDescriptor.source.location` — data file path in ADLS Gen2
- `properties.partitioning` — partition columns (if Hive-style partitioned)

### List Views

**Endpoint**: `GET {endpoint}/databases/{databaseName}/VIEWs?api-version=2021-04-01`

Returns view definitions. Extract the SQL for manual recreation in Fabric.

---

## Step 2: Choose Mapping Mode

Ask the user which mapping mode to use. The choice can be made at the **workspace level** (all databases follow the same pattern) or **per database** (hybrid mode).

### Mode A: Schemas (Default)

All Lake Databases → schemas within **one** target Lakehouse.

| Synapse | Fabric |
|---|---|
| Database `sales` | Schema `sales` in target Lakehouse |
| Database `marketing` | Schema `marketing` in target Lakehouse |
| Database `default` | Schema `dbo` (Lakehouse default) |

**Advantages**: Fewer items to manage; cross-schema queries via 2-part names; single SQL endpoint; aligns with Spark Migration Assistant behavior.

**Disadvantages**: Less isolation; shared OneLake path; harder to assign per-database permissions.

> **HMS databases** (created via Spark SQL `CREATE DATABASE`) are ideal candidates for Mode A because they only have a `default`/`dbo` schema — no collision risk, simple 1:1 mapping of database name → Fabric schema name.

### Mode B: Separate Lakehouses

Each Lake Database → its own Fabric Lakehouse.

| Synapse | Fabric |
|---|---|
| Database `sales` | Lakehouse `sales` |
| Database `marketing` | Lakehouse `marketing` |

**Advantages**: Strong isolation; independent security (OneLake RBAC per Lakehouse); independent SQL endpoints.

**Disadvantages**: More items to manage; cross-database queries require 3-part names; more shortcuts to create.

### Mode C: Hybrid (Per-Database Assignment)

Let the user assign each database individually — some go into a shared Lakehouse as schemas, others get their own dedicated Lakehouse. This is the most flexible option for workspaces with mixed ownership or security requirements.

**Example**:

| Synapse Database | Target Lakehouse | Maps As | Reason |
|---|---|---|---|
| `sales` | `Sales_Lakehouse` (dedicated) | Entire Lakehouse | Team-owned, needs own security boundary |
| `marketing` | `Marketing_Lakehouse` (dedicated) | Entire Lakehouse | Separate team, separate SQL endpoint |
| `staging_raw` | `ETL_Lakehouse` (shared) | Schema `staging_raw` | Shared ETL pipeline, same team |
| `staging_curated` | `ETL_Lakehouse` (shared) | Schema `staging_curated` | Shared ETL pipeline, same team |
| `default` | `ETL_Lakehouse` (shared) | Schema `dbo` | HMS default database, ETL workloads |

**When to use Hybrid**:
- Different databases are owned by different teams and need independent access control
- Some databases are tightly related (ETL stages, same domain) and benefit from consolidation
- Some databases need dedicated SQL endpoints for separate downstream consumers (Power BI, APIs)
- Mix of HMS databases (simple, no schemas) and Lake Database designer databases (may have inner schemas)

**User input format** — ask the user to provide an assignment map:

```json
{
  "databaseAssignments": [
    { "database": "sales",           "lakehouse": "Sales_Lakehouse",     "mode": "dedicated" },
    { "database": "marketing",       "lakehouse": "Marketing_Lakehouse", "mode": "dedicated" },
    { "database": "staging_raw",     "lakehouse": "ETL_Lakehouse",       "mode": "schema" },
    { "database": "staging_curated", "lakehouse": "ETL_Lakehouse",       "mode": "schema" },
    { "database": "default",         "lakehouse": "ETL_Lakehouse",       "mode": "schema" }
  ]
}
```

- `"mode": "dedicated"` — create a dedicated Lakehouse for this database; tables go under `dbo` schema (or inner schemas if they exist)
- `"mode": "schema"` — map this database as a schema within the shared Lakehouse; the schema name defaults to the database name

> **Schema collision handling** (for databases assigned as `"schema"` to the same Lakehouse): Apply the same composite naming rules as Mode A — see below.

### Schema Collision Handling (Mode A and Mode C Schema Assignments)

When Synapse databases contain inner schemas beyond `default`/`dbo`, a two-level namespace (`Database.Schema.Table`) must be flattened to one level (`Schema.Table`).

**Naming rules**:

| Synapse Source | Databases Have Inner Schemas? | Fabric Schema Name |
|---|---|---|
| `Database1.dbo.Table1` | No custom schemas in any database | `Database1` |
| `Database1.SchemaA.Table1` | Custom schemas exist | `Database1_SchemaA` |
| `Database1.dbo.Table4` | Custom schemas exist | `Database1` (drop `dbo`, use database name only) |
| `Database2.SchemaA.Table5` | Custom schemas in multiple databases | `Database2_SchemaA` (no collision) |

**Auto-detection logic**:

```
1. List all databases → for each, list schemas
2. If ALL databases have only default/dbo schema:
   → Simple mode: database name = Fabric schema name
3. If ANY database has custom schemas:
   → Composite mode: {database}_{schema} (except dbo → {database})
4. If ONLY ONE database is being migrated with custom schemas:
   → Pass-through mode: inner schema names map 1:1 to Fabric schemas
5. User can always override to Mode B or Mode C
```

> **Note**: In Mode C, collision detection only applies to databases assigned to the **same shared Lakehouse**. Databases with `"mode": "dedicated"` are independent — their inner schemas map directly to Fabric schemas with no collision risk.

**Emit a mapping report** before creating anything so the user can review name translations:

```
Mapping Report:
  Mode C (Hybrid) — 2 Lakehouses + 1 shared Lakehouse

  ETL_Lakehouse (shared):
    Synapse staging_raw.dbo.RawOrders         → ETL_Lakehouse.staging_raw.RawOrders
    Synapse staging_curated.dbo.CleanOrders   → ETL_Lakehouse.staging_curated.CleanOrders
    Synapse default.dbo.TempData              → ETL_Lakehouse.dbo.TempData

  Sales_Lakehouse (dedicated):
    Synapse sales.dbo.FactSales               → Sales_Lakehouse.dbo.FactSales
    Synapse sales.dbo.DimCustomer             → Sales_Lakehouse.dbo.DimCustomer

  Marketing_Lakehouse (dedicated):
    Synapse marketing.dbo.Campaigns           → Marketing_Lakehouse.dbo.Campaigns
```

---

## Step 3: Create Fabric Lakehouse(es)

### Create Lakehouse

**Endpoint**: `POST /v1/workspaces/{workspaceId}/items`

```json
{
  "displayName": "{lakehouseName}",
  "type": "Lakehouse",
  "description": "Migrated from Synapse Lake Database",
  "creationPayload": {
    "enableSchemas": true
  }
}
```

- **Mode A**: Create one Lakehouse with `enableSchemas: true`
- **Mode B**: Create one Lakehouse per database (still use `enableSchemas: true` if database had inner schemas)

> Returns HTTP 202 (LRO). Poll `Location` header until `status == "Succeeded"`. Response includes `id` (lakehouse ID needed for shortcuts and notebook binding).

**Handling name collisions (409)**:

If a Lakehouse with the same name already exists (HTTP 409), reuse it instead of failing:

```python
resp = requests.post(f"{FABRIC_BASE}/workspaces/{ws_id}/items", headers=fab_headers, json=payload)
if resp.status_code == 409:
    # Lakehouse already exists — look it up by name and reuse
    items = requests.get(f"{FABRIC_BASE}/workspaces/{ws_id}/items?type=Lakehouse", headers=fab_headers).json()
    existing = next((i for i in items.get("value", []) if i["displayName"] == lakehouse_name), None)
    if existing:
        lakehouse_id = existing["id"]
        print(f"  Reusing existing Lakehouse: {lakehouse_name} (id={lakehouse_id})")
```

### Capture Lakehouse Details

After creation, record these for later phases:
- `lakehouseId` — needed for OneLake shortcuts (Step 5) and notebook binding (Phase 2)
- `workspaceId` — needed for notebook `metadata.dependencies.lakehouse`
- `displayName` — needed for notebook lakehouse binding

---

## Step 4: Create Schemas (Mode A and Mode C Schema Assignments)

For each Synapse database (and its inner schemas), create the corresponding Fabric schema.

Schemas cannot be created via REST API — they require Spark SQL or the SQL endpoint:

```sql
CREATE SCHEMA IF NOT EXISTS Database1;
CREATE SCHEMA IF NOT EXISTS Database1_staging;
CREATE SCHEMA IF NOT EXISTS Database2;
CREATE SCHEMA IF NOT EXISTS Database2_staging;
```

Execute via:
- **SQL endpoint**: Connect to the Lakehouse SQL endpoint and run T-SQL
- **Fabric notebook**: Run in a notebook cell attached to the Lakehouse
- **Fabric REST API**: Execute via Livy session (`POST /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livySessions`)

---

## Step 4b: Discover or Create ADLS Connection

Shortcuts require a `connectionId` — a Fabric Connection object that holds credentials for accessing the ADLS Gen2 storage. The connection's credential (not the caller's Fabric token) is what Fabric uses to read data from storage.

### Connection Discovery Strategy

1. **List all connections**: `GET /v1/connections` (Fabric API)
2. **Filter by storage account**: Match connections where `connectionDetails.type == "AzureDataLakeStorage"` and `connectionDetails.path` contains the target storage hostname
3. **Filter by container**: Parse the container from the connection path. Skip connections locked to a different container than the one containing Synapse data
4. **Score and rank** candidates:

| Criteria | Score | Reason |
|---|---|---|
| Root path (no container lock) | +10 | Can access any container |
| Matches target container | +5 | Covers the Synapse data |
| OAuth2 credential | +2 | More likely to have current RBAC |
| WorkspaceIdentity credential | +0 | May lack RBAC, be disabled, or be blocked by policy |

5. **Probe-test** each candidate (highest score first): Create a temporary shortcut (`_probe_{tableName}`), check the response, then delete the probe. Use the first connection that succeeds.

### Probe-Test Logic

```python
# Create a probe shortcut with the candidate connection
probe_payload = {
    "name": "_probe_{tableName}",
    "path": "Tables",
    "target": {"type": "AdlsGen2", "adlsGen2": {
        "location": location, "subpath": subpath, "connectionId": candidate_id
    }}
}
resp = POST /v1/workspaces/{wsId}/items/{lhId}/shortcuts (probe_payload)

if resp.status_code in (200, 201, 409):
    # Connection works — delete probe, use this connection
    DELETE /v1/workspaces/{wsId}/items/{lhId}/shortcuts/Tables/_probe_{tableName}
    selected_connection_id = candidate_id
elif resp.status_code in (400, 403):
    # Credential issue — try next candidate
    continue
```

### Creating a New Connection

If no existing connection passes the probe, attempt programmatic creation in this order:

#### Attempt 1: Key-based connection (via ARM `listKeys`)

Use the ARM token to retrieve the storage account key, then create the connection:

```python
# Step 1: Get storage account key via ARM
arm_url = (
    f"https://management.azure.com/subscriptions/{subscription_id}"
    f"/resourceGroups/{resource_group}"
    f"/providers/Microsoft.Storage/storageAccounts/{storage_account_name}"
    f"/listKeys?api-version=2023-05-01"
)
key_resp = requests.post(arm_url, headers=arm_headers)

if key_resp.status_code == 200:
    storage_key = key_resp.json()["keys"][0]["value"]

    # Step 2: Create connection with Key credential
    create_conn = {
        "connectivityType": "ShareableCloud",
        "displayName": f"{storage_account_name}_{container}_migration",
        "connectionDetails": {
            "type": "AzureDataLakeStorage",
            "creationMethod": "AzureDataLakeStorage",
            "parameters": [
                {"dataType": "Text", "name": "server", "value": f"https://{storage_account_name}.dfs.core.windows.net"},
                {"dataType": "Text", "name": "path", "value": f"/{container}"}
            ]
        },
        "privacyLevel": "Organizational",
        "credentialDetails": {
            "singleSignOnType": "None",
            "connectionEncryption": "NotEncrypted",
            "skipTestConnection": False,
            "credentials": {
                "credentialType": "Key",
                "key": storage_key
            }
        }
    }
    conn_resp = requests.post("https://api.fabric.microsoft.com/v1/connections",
                              headers=fab_headers, json=create_conn)
    if conn_resp.status_code == 201:
        selected_connection_id = conn_resp.json()["id"]
```

> **Requires**: The caller must have `Microsoft.Storage/storageAccounts/listKeys/action` on the storage account (typically the `Storage Account Key Operator Service Role` or `Contributor` role).

#### Attempt 2: WorkspaceIdentity connection

If the Key approach fails (403 on `listKeys`), fall back to WorkspaceIdentity:

```python
create_conn = {
    "connectivityType": "ShareableCloud",
    "displayName": f"{storage_account_name}_{container}_migration",
    "connectionDetails": {
        "type": "AzureDataLakeStorage",
        "creationMethod": "AzureDataLakeStorage",
        "parameters": [
            {"dataType": "Text", "name": "server", "value": f"https://{storage_account_name}.dfs.core.windows.net"},
            {"dataType": "Text", "name": "path", "value": f"/{container}"}
        ]
    },
    "privacyLevel": "Organizational",
    "credentialDetails": {
        "singleSignOnType": "None",
        "connectionEncryption": "NotEncrypted",
        "skipTestConnection": False,
        "credentials": {"credentialType": "WorkspaceIdentity"}
    }
}
```

> **Requires**: The workspace's managed identity must have `Storage Blob Data Reader` RBAC on the storage account.

#### Why OAuth2 cannot be created via API

OAuth2 connections require interactive browser consent (authorization code grant flow). The Fabric Connections API explicitly rejects `credentialType: "OAuth2"` with `"CredentialType input is not supported for this API"`.

#### Fallback: Manual Portal creation

If both programmatic approaches fail, display the following manual-setup guidance:

```
No ADLS connection could be created automatically.
Please create one manually:

1. Open Fabric Portal → Settings → Manage connections and gateways
   https://app.fabric.microsoft.com/connections
   (MSIT: https://msit.powerbi.com/connections)
2. Click '+ New' → Cloud → Azure Data Lake Storage Gen2
3. Server: https://{storageAccount}.dfs.core.windows.net
   Path: /{container}
   Authentication: OAuth2 (sign in with credentials that have Storage Blob Data Reader)
4. Re-run the migration script — it will discover and probe-test the new connection.

Documentation: https://learn.microsoft.com/fabric/data-engineering/lakehouse-shortcuts#create-a-shortcut
```

### Common Connection Errors

| Error | Cause | Fix |
|---|---|---|
| 400 `"Stored Credential Operation - PowerBIEntityNotFound"` | Connection's OAuth token expired or was revoked | Re-authenticate the connection in Fabric Portal, or create a new one |
| 400 `"Stored Credential"` (any variant) | Connection credential is invalid, expired, or was rotated | Re-authenticate the connection or create a new one with fresh credentials |
| 403 on shortcut creation | Connection's identity lacks `Storage Blob Data Reader` on the storage account | Grant RBAC to the connection's identity |
| 429 `Retry-After: {N}` | Fabric API rate limit — too many shortcut calls in quick succession | Wait `Retry-After` seconds, then retry the same request |
| Connection reset / `ConnectionError` | Network-level timeout during shortcut creation (large batch) | Retry with exponential backoff; check network connectivity |
| 400 `"Required property 'connectionId' not found"` | Missing `connectionId` in the shortcut payload | Always include `connectionId` in the `adlsGen2` target |

---

## Step 5: Create OneLake Shortcuts

### Shortcut Target Decision

| Table Format | Table Type | Shortcut Location | Result |
|---|---|---|---|
| **Delta** | Managed | `Tables/{schema}/{tableName}` | Auto-registers in Lakehouse catalog |
| **Delta** | External | `Tables/{schema}/{tableName}` | Auto-registers in Lakehouse catalog |
| **Parquet** | Managed or External | `Files/{schema}/{tableName}` | Accessible via Spark; not auto-registered |
| **CSV** | Managed or External | `Files/{schema}/{tableName}` | Accessible via Spark; not auto-registered |
| **JSON** | Managed or External | `Files/{schema}/{tableName}` | Accessible via Spark; not auto-registered |
| **ORC** | Managed or External | `Files/{schema}/{tableName}` | Accessible via Spark; not auto-registered |
| **Avro** | Managed or External | `Files/{schema}/{tableName}` | Accessible via Spark; not auto-registered |

### Create Shortcut API

**Endpoint**: `POST /v1/workspaces/{workspaceId}/items/{lakehouseId}/shortcuts`

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

> **`connectionId` is required**. Without it, the API returns 400 `"Required property 'connectionId' not found"`. See Step 4b above for how to discover or create the connection.

### Shortcut Target Path by Table Type

**Managed tables**: The data path is under the Synapse workspace warehouse directory:
```
abfss://{container}@{storage}.dfs.core.windows.net/synapse/workspaces/{workspace}/warehouse/{database}/{tableName}
```
Split this into:
- `location`: `https://{storage}.dfs.core.windows.net`
- `subpath`: `/{container}/synapse/workspaces/{workspace}/warehouse/{database}/{tableName}`

**External tables**: Use the `storageDescriptor.source.location` path directly:
```
abfss://{container}@{storage}.dfs.core.windows.net/{custom/path/to/table}
```
Split into:
- `location`: `https://{storage}.dfs.core.windows.net`
- `subpath`: `/{container}/{custom/path/to/table}`

### Authentication for Shortcuts

Shortcut creation involves two separate authorization checks:

1. **Fabric API authorization** (your token): Must have Contributor/Admin role on the Fabric workspace to call the Shortcuts API
2. **Storage data access** (connection's credential): The connection's identity must have **Storage Blob Data Reader** (or higher) on the target ADLS Gen2 storage account/container

> The connection credential — not the API caller's token — is what Fabric uses to read data from storage at runtime. See Step 4b for connection discovery.

### Shortcut Granularity Strategy

Choose between per-table shortcuts or per-database shortcuts based on the table format:

| Scenario | Strategy | Shortcuts Created | Catalog Registration |
|---|---|---|---|
| **All Delta tables** | Per-table under `Tables/{schema}/` | One per table | Automatic |
| **All non-Delta tables** | Per-database under `Files/{schema}/` | One per database (with tables) | Requires `CREATE TABLE USING {format}` |
| **Mixed formats** | Per-table for Delta → `Tables/`; per-database for non-Delta → `Files/` | Hybrid | Automatic for Delta; manual for non-Delta |

**Per-database shortcut** (non-Delta): Instead of creating 111 individual shortcuts, create one shortcut per database pointing to the warehouse directory. All tables appear as subfolders.

```json
{
  "name": "{databaseName}",
  "path": "Files/{schemaName}",
  "target": {
    "type": "AdlsGen2",
    "adlsGen2": {
      "location": "https://{storageAccount}.dfs.core.windows.net",
      "subpath": "/{container}/synapse/workspaces/{workspace}/warehouse/{database}",
      "connectionId": "{connectionId}"
    }
  }
}
```

This creates `Files/{schema}/{databaseName}/` containing all table subfolders. Access via:
```python
df = spark.read.parquet("Files/{schema}/{databaseName}/{tableName}")
```

> **When to use per-database shortcuts**: When all tables in the database are non-Delta (parquet, CSV, etc.) and the tables share a common warehouse directory path. This reduces the number of shortcuts from N (tables) to M (databases with tables).

### Shortcut Creation Error Cascade

When creating shortcuts in bulk (many tables across many databases), certain errors indicate that **all remaining shortcuts will also fail**. Abort early to avoid wasting API calls:

| Error | Action | Rationale |
|---|---|---|
| **403** (permission denied) | **Abort all remaining shortcuts** | The connection lacks `Storage Blob Data Reader` on the storage account — every subsequent shortcut to the same account will also fail |
| **400 "Stored Credential"** | **Abort all remaining shortcuts** | The connection's credential is invalid — no shortcut using this connection will succeed |
| **ConnectionError / reset** | **Abort all remaining shortcuts** | Network-level failure — likely a transient outage affecting all requests |
| **429** (rate limit) | **Wait `Retry-After` seconds, then retry** | Transient — the same request will succeed after the cooldown period |
| **409** (conflict) | **Continue** — treat as success | Shortcut already exists (idempotent re-run) |
| **404** (not found) | **Continue** — skip this table | The source path doesn't exist; other tables may still be valid |

**Implementation pattern**:

```python
abort_shortcuts = False
for db_name, tables in db_inventory.items():
    if abort_shortcuts:
        # Record remaining as skipped
        break
    for table in tables:
        resp = create_shortcut(table, connection_id)
        if resp.status_code in (200, 201, 409):
            # Success or already exists — continue
            pass
        elif resp.status_code == 403:
            print(f"403 — connection lacks storage access. Aborting remaining shortcuts.")
            abort_shortcuts = True
            break
        elif resp.status_code == 400 and "Stored Credential" in resp.text:
            print(f"400 — connection credential invalid. Aborting remaining shortcuts.")
            abort_shortcuts = True
            break
        elif resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 30))
            time.sleep(retry_after)
            resp = create_shortcut(table, connection_id)  # retry once
        # else: log and continue
```

> **Why abort on 403/400?** These are not transient — they indicate a systemic permission or credential issue that affects every shortcut using the same connection. Continuing wastes API quota and produces N identical error messages. Fix the root cause, then re-run.

---

## Step 6: Handle Non-Delta Tables

For non-Delta tables (Parquet, CSV, JSON, ORC, Avro), the shortcut is created under `Files/` (Step 5) and data is accessible via Spark. However, these tables are **not auto-registered** in the Lakehouse catalog. Choose one of the two options below.

### Option A: Convert to Delta (Recommended)

Converts the data to Delta format for full catalog registration, SQL endpoint access, and Power BI Direct Lake support.

```python
# Read from the shortcut path
df = spark.read.format("{originalFormat}").load("Files/{schemaName}/{tableName}")

# Write as Delta to the Tables section
df.write.format("delta").mode("overwrite").saveAsTable("{schemaName}.{tableName}")
```

For **partitioned tables**, preserve partition columns:

```python
df = spark.read.format("parquet").load("Files/{schemaName}/{tableName}")
df.write.format("delta") \
    .partitionBy("{partitionCol}") \
    .mode("overwrite") \
    .saveAsTable("{schemaName}.{tableName}")
```

> **Note**: This creates a physical copy of the data in Delta format. The original shortcut under `Files/` remains as a reference.

**Advantages**: Full Lakehouse catalog registration, SQL endpoint queries, Power BI Direct Lake, V-Order optimization, ACID transactions, time travel.

### Option B: Retain Original Format

Keep tables in their legacy format (Parquet, ORC, etc.) under `Files/`. This avoids data duplication and preserves the original file layout.

**Register in the catalog** — create an external table definition so Spark SQL and the SQL endpoint can query the data without converting it:

```sql
-- Register a non-Delta table pointing to the shortcut path
CREATE TABLE IF NOT EXISTS {schemaName}.{tableName}
USING {format}
LOCATION 'Files/{schemaName}/{tableName}';
```

For example:

```sql
-- Parquet table
CREATE TABLE IF NOT EXISTS sales.historical_orders
USING PARQUET
LOCATION 'Files/sales/historical_orders';

-- ORC table
CREATE TABLE IF NOT EXISTS analytics.legacy_events
USING ORC
LOCATION 'Files/analytics/legacy_events';
```

**For Hive-style partitioned tables** (`year=2024/month=01/` directory structure), you must also recover partition metadata after creating the table:

```sql
-- Register the partitioned table
CREATE TABLE IF NOT EXISTS {schemaName}.{tableName}
USING PARQUET
PARTITIONED BY ({partitionCols})
LOCATION 'Files/{schemaName}/{tableName}';

-- Recover partitions from directory structure
MSCK REPAIR TABLE {schemaName}.{tableName};
```

For example:

```sql
CREATE TABLE IF NOT EXISTS sales.transactions
USING PARQUET
PARTITIONED BY (year INT, month INT)
LOCATION 'Files/sales/transactions';

MSCK REPAIR TABLE sales.transactions;
```

> **Why `MSCK REPAIR TABLE`?** Non-Delta tables rely on HMS partition metadata for partition pruning. Unlike Delta (where `_delta_log` is self-describing), Hive-style partitioned tables need the catalog to know which partitions exist. Without this step, queries read all files instead of pruning to the relevant partitions — causing full scans and poor performance.

**After initial registration**, if new partitions are added to the source data (e.g., Synapse continues writing `year=2025/month=05/`), re-run `MSCK REPAIR TABLE` to pick up the new partitions.

**Limitations of retaining original format**:

| Capability | Delta (Option A) | Original Format (Option B) |
|---|---|---|
| Lakehouse Explorer UI (Tables section) | Yes | Yes (after `CREATE TABLE`) |
| SQL endpoint queries | Yes | Yes (after `CREATE TABLE`) |
| Power BI Direct Lake | Yes | **No** — requires Delta |
| V-Order optimization | Yes | **No** |
| ACID transactions / time travel | Yes | **No** |
| Partition pruning | Automatic | Requires `MSCK REPAIR TABLE` |
| Data duplication | Yes (new copy) | **No** (zero-copy via shortcut) |

### Decision Guide

```
Non-Delta table in Synapse:
├── Consumed by Power BI Direct Lake?
│   └── YES → Option A (convert to Delta)
├── Need ACID / time travel / merge operations?
│   └── YES → Option A (convert to Delta)
├── Large table, want to avoid data duplication?
│   └── YES → Option B (retain original format)
├── Read-only / archival data?
│   └── YES → Option B (retain original format)
└── Default recommendation
    └── Option A (convert to Delta) — Fabric is Delta-first
```

---

## Step 7: Validate

After migration, verify:

1. **Lakehouse catalog**: Check that Delta tables appear in the Lakehouse Explorer UI under Tables
2. **SQL endpoint**: Query migrated tables via the SQL endpoint to confirm schema and data
3. **Row counts**: Compare row counts between Synapse and Fabric for each table
4. **Shortcut health**: Verify shortcuts are accessible (`notebookutils.fs.ls("Tables/{schema}/")`)

---

## Object Type Reference

### Full Inventory of Synapse Lake Database Object Types

| Object Type | API Artifact Type | Fabric Support | Migration Action |
|---|---|---|---|
| **Delta table (managed)** | `TABLE` (formatType: delta, tableType: MANAGED) | Lakehouse Tables (shortcut) | Shortcut → auto-registers |
| **Delta table (external)** | `TABLE` (formatType: delta) | Lakehouse Tables (shortcut) | Shortcut → auto-registers |
| **Parquet table (managed)** | `TABLE` (formatType: parquet, tableType: MANAGED) | Lakehouse Files (shortcut) | Shortcut under Files/; Option A (Delta conversion) or Option B (retain + `CREATE TABLE` + `MSCK REPAIR TABLE`) |
| **Parquet table (external)** | `TABLE` (formatType: parquet) | Lakehouse Files (shortcut) | Shortcut under Files/; Option A or Option B |
| **CSV table** | `TABLE` (formatType: csv/textfile) | Lakehouse Files (shortcut) | Shortcut under Files/; Option A (recommended) or Option B |
| **JSON table** | `TABLE` (formatType: json) | Lakehouse Files (shortcut) | Shortcut under Files/; Option A (recommended) or Option B |
| **ORC table** | `TABLE` (formatType: orc) | Lakehouse Files (shortcut) | Shortcut under Files/; Option A or Option B |
| **Avro table** | `TABLE` (formatType: avro) | Lakehouse Files (shortcut) | Shortcut under Files/; Option A or Option B |
| **View** | `VIEW` | Not directly migratable | Extract SQL; recreate as Spark SQL `CREATE VIEW` or SQL endpoint view |
| **Schema** | `SCHEMA` | Lakehouse Schema | `CREATE SCHEMA IF NOT EXISTS {name}` |
| **Function (UDF)** | `FUNCTION` | Not migratable via API | Recreate manually via `spark.udf.register()` or `CREATE FUNCTION` |
| **Partition Info** | `PARTITIONINFO` | Preserved via shortcut | Delta: automatic. Non-Delta: directory structure preserved |
| **Relationship** | `RELATIONSHIP` | No Fabric equivalent | Document for reference only |

### Decision Tree

```
For each table in Synapse Lake Database:
├── Is format Delta?
│   ├── YES → Create shortcut under Tables/{schema}/ → auto-registers in catalog ✅
│   └── NO (Parquet/CSV/JSON/ORC/Avro)
│       ├── Option A: Convert to Delta → Shortcut under Files/ → Spark read → write as Delta to Tables/
│       └── Option B: Retain format → Shortcut under Files/ → CREATE TABLE USING {format} → MSCK REPAIR TABLE (if partitioned)
│
├── Is table Managed?
│   ├── YES → Shortcut target = Synapse warehouse directory path
│   │         (ensure Fabric identity has Storage Blob Data Reader on Synapse primary storage)
│   └── NO (External) → Shortcut target = original ADLS Gen2 path
│
└── Is it a View/Function/Relationship?
    ├── View → Extract SQL, recreate in Fabric
    ├── Function → Recreate via spark.udf.register()
    └── Relationship → Document only (no Fabric equivalent)
```

---

## Step 8: (Optional) Validate Before Proceeding to Phase 2

Run these checks before migrating Notebooks. Notebooks rely on Lakehouses being healthy — missing shortcuts or unregistered tables cause immediate runtime failures.

| Check | How | Pass Criteria |
|---|---|---|
| Shortcut health | `notebookutils.fs.ls("Tables/{schema}/")` and `Files/{schema}/` | All shortcuts resolve; no `PathNotFound` errors |
| Row counts | Compare `SELECT COUNT(*)` on Synapse vs. Fabric for each table | Counts match (or are within acceptable tolerance for streaming tables) |
| Schema comparison | Compare column names, types, and order between Synapse and Fabric | Exact match |
| Non-Delta registration | `SHOW TABLES IN {schema}` | All Option B tables appear in catalog |
| Partition coverage | `SHOW PARTITIONS {schema}.{table}` for Option B partitioned tables | Partition count matches Synapse |

> **Do not proceed to Phase 2** until all shortcuts are healthy and row counts match. A notebook that reads from a missing or broken shortcut will fail silently or produce wrong results.

See [validation-testing.md → V2: Data Validation](validation-testing.md#v2-data-validation) for detailed scripts.

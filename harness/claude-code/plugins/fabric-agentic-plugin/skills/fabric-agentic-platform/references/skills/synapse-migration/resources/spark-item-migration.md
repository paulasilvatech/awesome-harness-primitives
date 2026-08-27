# Synapse Spark Item Migration — Notebooks & Spark Job Definitions

Migrate Synapse Notebooks and Spark Job Definitions (SJDs) to Fabric via REST APIs.

> **Prerequisite**: Complete [Lake Database Migration](lake-database-migration.md) first so Fabric Lakehouses exist for notebook/SJD binding.
>
> **Auth tokens** (see [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) for commands):
> - Synapse data-plane audience: `https://dev.azuresynapse.net`
> - Fabric audience: `https://api.fabric.microsoft.com`

---

## Migration Workflow

```
Phase 2: Notebook Migration
├── Step 1: List/export notebooks from Synapse          (REQUIRED)
├── Step 2: Transform notebook code                     (OPTIONAL — code refactoring)
├── Step 3: Strip Synapse-specific fields                (OPTIONAL — cleanup)
├── Step 4: Add Fabric lakehouse binding                 (OPTIONAL — attach to Phase 1 Lakehouse)
├── Step 5: Base64-encode .ipynb and build payload       (REQUIRED)
├── Step 6: POST to Fabric Items API                     (REQUIRED)
└── Step 7: (Optional) Validate before proceeding to Phase 3

Phase 3: Spark Job Definition Migration
├── Step 1: List/export SJDs from Synapse                (REQUIRED)
├── Step 2: Update file paths and code                   (OPTIONAL — refactoring)
├── Step 3: Remap pool → Environment                     (OPTIONAL — compute binding)
├── Step 4: Create SJD in Fabric                         (REQUIRED)
└── Step 5: (Optional) Validate before cutover
```

**Two migration scenarios**:

| Scenario | Steps Used | When |
|---|---|---|
| **Lift-and-shift** (copy as-is, refactor later) | 1 → 5 → 6 | Fast migration; refactor post-cutover |
| **Migrate-and-modernize** (refactor during migration) | 1 → 2 → 3 → 4 → 5 → 6 | Clean migration; notebooks ready to run in Fabric |

---

## Phase 2: Notebook Migration

### Step 1: Export Notebooks from Synapse

#### List All Notebooks

**Endpoint**: `GET {endpoint}/notebooks?api-version=2020-12-01`

```
GET https://{workspaceName}.dev.azuresynapse.net/notebooks?api-version=2020-12-01
```

Response: `{ "value": [ ...NotebookResource[] ] }` — paginated via `nextLink`.

Each `NotebookResource` contains:
- `name` — notebook name
- `properties` — the notebook content (standard `.ipynb` structure)
  - `properties.nbformat` / `properties.nbformat_minor` — Jupyter format version
  - `properties.metadata` — kernel info, language info
  - `properties.cells[]` — array of notebook cells
  - `properties.bigDataPool` — Synapse Spark pool reference (Synapse-specific). **Can be `null`** — not just absent. Always use `(props.get("bigDataPool") or {}).get("referenceName", "")` to safely extract the pool name.
  - `properties.sessionProperties` — driver/executor config (Synapse-specific)
  - `properties.folder` — folder structure (`{ "name": "path/to/folder" }`)
  - `properties.description` — notebook description
  - `properties.targetSparkConfiguration` — Spark config reference (Synapse-specific)

#### Get Single Notebook

**Endpoint**: `GET {endpoint}/notebooks/{notebookName}?api-version=2020-12-01`

Same response structure as above, for a single notebook.

#### Extract the .ipynb Content

The `properties` object **is** the notebook content in `.ipynb` format. To build a valid `.ipynb` file:

```json
{
  "nbformat": properties.nbformat,
  "nbformat_minor": properties.nbformat_minor,
  "metadata": properties.metadata,
  "cells": properties.cells
}
```

> **Important**: Do NOT include `bigDataPool`, `sessionProperties`, `description`, `folder`, or `targetSparkConfiguration` in the `.ipynb` — these are Synapse envelope fields, not standard Jupyter fields.

---

### Step 2: (Optional) Transform Notebook Code

Apply code refactoring to notebook cells. For each cell in `cells[]` where `cell_type == "code"`, scan `source` lines for Synapse-specific patterns and replace.

See [utility-api-mapping.md](utility-api-mapping.md) for the full `mssparkutils` → `notebookutils` mapping.
See [connectivity-migration.md](connectivity-migration.md) for linked service replacements.
See [code-patterns.md](code-patterns.md) for before/after examples.

#### Pre-Refactoring Audit — Search Patterns

Scan all notebook cell sources for these patterns to identify what needs changing:

| Search Pattern | Category | Action |
|---|---|---|
| `mssparkutils` | Spark Utils | Replace with `notebookutils` |
| `spark.synapse.linkedService` | Linked Services | Remove; replace with Key Vault or Fabric Connection |
| `getSecretWithLS` | Credentials | Replace with `getSecret(vaultUrl, secretName)` |
| `TokenLibrary` | Token/Auth | Remove; use `notebookutils.credentials` or direct OAuth |
| `synapsesql` | SQL Connector | Replace `spark.read.synapsesql()` with Delta reads |
| `spark.catalog.listDatabases` | Catalog API | Replace with `spark.sql("SHOW DATABASES")` |
| `spark.catalog.currentDatabase` | Catalog API | Replace with `spark.sql("SELECT CURRENT_DATABASE()")` |
| `spark.catalog.getDatabase` | Catalog API | Replace with `spark.sql("DESCRIBE DATABASE ...")` |
| `spark.catalog.listFunctions` | Catalog API | Not supported in Fabric — remove |
| `spark.catalog.registerFunction` | Catalog API | Replace with `spark.udf.register()` |
| `spark.catalog.functionExists` | Catalog API | Not supported in Fabric — remove |
| `LinkedServiceBasedTokenProvider` | Auth Provider | Replace with `ClientCredsTokenProvider` |
| `getPropertiesAsMap` | Linked Services | Remove; configure storage directly |
| `spark.storage.synapse` | Linked Services | Remove — not supported in Fabric |
| `/user/trusted-service-user/` | File Paths | Replace with OneLake path or shortcut path |
| `cosmos.oltp` | Cosmos DB | Update to Key Vault for secrets |
| `kusto.spark.synapse` | Kusto/ADX | Replace linked service auth with `accessToken` via `getToken()` |

**Notebooks with zero matches are safe to migrate as-is (lift-and-shift).**

---

### Step 3: (Optional) Strip Synapse-Specific Fields

Remove Synapse-only fields from the notebook `.ipynb` before uploading to Fabric:

**Fields to remove from the notebook JSON**:
- `bigDataPool` — Synapse Spark pool binding (no Fabric equivalent at notebook level)
- `sessionProperties` — driver/executor memory config (use Fabric Environment instead)
- `targetSparkConfiguration` — Synapse Spark config reference

**Fields to preserve**:
- `nbformat`, `nbformat_minor` — required Jupyter fields
- `metadata.kernelspec`, `metadata.language_info` — keep for proper editor rendering
- `cells[]` — all cell content
- Cell-level `metadata`, `outputs`, `execution_count` — preserve for round-trip safety

> **Note**: Fabric will accept the notebook even with Synapse-specific fields present — it ignores unrecognized top-level fields. Stripping is recommended for cleanliness but not strictly required.

---

### Step 4: (Optional) Add Fabric Lakehouse Binding

Inject the `metadata.dependencies.lakehouse` section to bind the notebook to a Fabric Lakehouse created in Phase 1:

```json
{
  "metadata": {
    "dependencies": {
      "lakehouse": {
        "default_lakehouse": "{lakehouseId}",
        "default_lakehouse_workspace_id": "{workspaceId}",
        "default_lakehouse_name": "{lakehouseName}"
      }
    },
    "kernelspec": { ... },
    "language_info": { ... }
  }
}
```

- `default_lakehouse` — the Lakehouse item ID from Phase 1
- `default_lakehouse_workspace_id` — the Fabric workspace ID
- `default_lakehouse_name` — the Lakehouse display name

> **Without this binding**: The notebook will open in Fabric but have no default Lakehouse. Users must manually attach one before running. Relative paths like `Tables/mytable` will fail until a Lakehouse is attached.

---

### Step 5: Base64-Encode and Build Payload

1. Serialize the (optionally transformed) notebook to JSON
2. Base64-encode the JSON string (standard encoding, not URL-safe)
3. Build the Fabric Items API payload:

```json
{
  "displayName": "{notebookName}",
  "type": "Notebook",
  "description": "{description from Synapse}",
  "definition": {
    "format": "ipynb",
    "parts": [
      {
        "path": "notebook-content.ipynb",
        "payload": "{base64-encoded-ipynb-json}",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

#### Fabric .ipynb Nuances

Ensure the notebook JSON follows these Fabric-specific rules before encoding:
- Every code cell must have `outputs` (use `[]` if empty) and `execution_count` (use `null` if not executed)
- Every cell must have a `metadata` object (use `{}` if empty)
- Each source line must end with `\n` except the last line of a cell
- Keep kernel/language metadata consistent with notebook language/runtime

---

### Step 6: POST to Fabric Items API

**Endpoint**: `POST /v1/workspaces/{workspaceId}/items`

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items
Authorization: Bearer {fabricToken}
Content-Type: application/json

{body from Step 5}
```

**Response**: HTTP 202 Accepted (async LRO).

1. Capture the `Location` header URL
2. Poll `GET {Location}` until `status == "Succeeded"`
3. Response includes `id` (the new notebook item ID)

#### Preserving Folder Structure

Synapse notebooks may have folder paths (`properties.folder.name`). Fabric supports up to 10 levels of folder nesting. Include the folder path in `displayName` is **not** supported — Fabric uses a flat namespace per item type. To preserve folder organization:

- After creation, use `PATCH /v1/workspaces/{workspaceId}/items/{itemId}` to update metadata if folder support is added
- Alternatively, prefix notebook names with folder paths: `ETL_Bronze_LoadCustomers` instead of `ETL/Bronze/LoadCustomers`
- Or use Fabric workspace folders if available in the target workspace

#### Batch Migration

For workspaces with many notebooks, process sequentially to avoid API throttling:
- Respect HTTP 429 (Too Many Requests) — retry with the `Retry-After` header value
- Process 5–10 notebooks at a time, waiting for each LRO to complete before starting the next batch
- Log success/failure for each notebook to produce a migration report

---

## Phase 3: Spark Job Definition Migration

### Step 1: Export SJDs from Synapse

#### List All SJDs

**Endpoint**: `GET {endpoint}/sparkJobDefinitions?api-version=2020-12-01`

```
GET https://{workspaceName}.dev.azuresynapse.net/sparkJobDefinitions?api-version=2020-12-01
```

Response: `{ "value": [ ...SparkJobDefinitionResource[] ] }` — paginated via `nextLink`.

Each `SparkJobDefinitionResource` contains:
- `name` — SJD name
- `properties.description` — SJD description
- `properties.targetBigDataPool.referenceName` — Synapse Spark pool name. **Can be `null`** — not just absent. Always use `(props.get("targetBigDataPool") or {}).get("referenceName", "")` to safely extract.
- `properties.requiredSparkVersion` — e.g., `"3.3"`, `"3.4"`, `"3.5"`
- `properties.language` — `"python"`, `"scala"`, `"r"`

> **Language value mapping**: Synapse returns lowercase (`"python"`, `"scala"`, `"r"`). Fabric's `SparkJobDefinitionV1.json` requires: `"Python"`, `"Scala/Java"`, `"R"`. Critically, Synapse `"scala"` must be mapped to `"Scala/Java"` — submitting `"scala"` returns `SparkJobDefinitionInvalid`. Apply this mapping before uploading definitions:
> ```python
> LANGUAGE_MAP = {"python": "Python", "scala": "Scala/Java", "r": "R"}
> fabric_language = LANGUAGE_MAP.get(synapse_language.lower(), synapse_language)
> ```

- `properties.jobProperties`:
  - `className` — main class for Java/Scala (empty for Python)
  - `args[]` — command-line arguments
  - `jars[]` — additional JAR files
  - `pyFiles[]` — additional Python files
  - `files[]` — additional resource files
  - `archives[]` — archive files
  - `conf` — Spark configuration properties
  - `driverMemory`, `driverCores`, `executorMemory`, `executorCores`, `numExecutors` — compute settings

#### Get Single SJD

**Endpoint**: `GET {endpoint}/sparkJobDefinitions/{sparkJobDefinitionName}?api-version=2020-12-01`

---

### Step 2: (Optional) Update File Paths and Code

#### File Path Updates

If `jobProperties.file`, `jars[]`, `pyFiles[]`, or `files[]` reference Synapse workspace-internal storage, update to accessible paths:

| Synapse Path | Action |
|---|---|
| `abfss://.../{workspace}/warehouse/...` (workspace storage) | Re-upload to Fabric Lakehouse Files or accessible ADLS Gen2; update path |
| `abfss://{container}@{storage}.dfs.core.windows.net/...` (external ADLS) | Keep if accessible from Fabric; or update to OneLake path via shortcut |

#### Source Code Changes

If the main `.py`/`.jar` file contains Synapse-specific code, the same refactoring patterns from Phase 2 apply:
- Replace `mssparkutils` with `notebookutils`
- Update hardcoded file paths to OneLake `abfss://` paths
- Replace linked service references with Key Vault secrets or Fabric Connections

> **Note**: DMTS Connections are not yet supported in Fabric Spark Job Definitions (supported in notebooks only). If SJD code uses DMTS, refactor to direct endpoint authentication.

#### Command-Line Argument Updates

If `args[]` contain Synapse-specific paths or connection strings, update them to Fabric equivalents.

---

### Step 3: (Optional) Remap Pool → Environment

Synapse SJDs are bound to a Spark pool (`targetBigDataPool`). In Fabric, SJDs are bound to an Environment.

| Synapse | Fabric |
|---|---|
| `targetBigDataPool.referenceName: "MyPool"` | Fabric Environment item ID |
| `driverMemory`, `executorMemory`, etc. | Configured in Fabric Environment Spark compute settings |
| Pool-level libraries | Configured in Fabric Environment library management |

If no specific Environment is needed, the SJD will use the Fabric workspace default settings (Starter Pool).

---

### Step 4: Create SJD in Fabric

**Endpoint**: `POST /v1/workspaces/{workspaceId}/items`

```json
{
  "displayName": "{sjdName}",
  "type": "SparkJobDefinition",
  "description": "{description}"
}
```

After creation, update the SJD definition with the job properties:

**Endpoint**: `POST /v1/workspaces/{workspaceId}/items/{sjdId}/updateDefinition`

> **Note**: Use the `/items/{id}/updateDefinition` path (not `/sparkJobDefinitions/{id}/`). The `/items/` path is the canonical Fabric endpoint for all item types.

#### SparkJobDefinitionV1.json — Config Structure

Build this JSON from the Synapse SJD's `jobProperties`, then base64-encode it:

```json
{
  "executableFile": "{jobProperties.file}",
  "defaultLakehouseArtifactId": "{lakehouseId from Phase 1, or empty string}",
  "mainClass": "{jobProperties.className, or empty for Python}",
  "additionalLakehouseIds": [],
  "retryPolicy": null,
  "commandLineArguments": "{jobProperties.args joined by spaces}",
  "additionalLibraryUris": ["{jobProperties.jars[] + jobProperties.pyFiles[]}"],
  "language": "{mapped language — see Language value mapping above}",
  "environmentArtifactId": "{Environment ID from Phase 0 poolMappings, or null for default}"
}
```

#### Field Mapping: Synapse → Fabric SJD

| Synapse `jobProperties` Field | Fabric `SparkJobDefinitionV1.json` Field | Transform |
|---|---|---|
| `file` | `executableFile` | Direct copy — keep `abfss://` paths as-is if storage is accessible from Fabric |
| `className` | `mainClass` | Direct copy (empty for Python) |
| `args[]` | `commandLineArguments` | Join array into space-separated string |
| `jars[]` + `pyFiles[]` | `additionalLibraryUris` | Merge into single array; filter out empty strings |
| `language` | `language` | **Map**: `"python"` → `"Python"`, `"scala"` → `"Scala/Java"`, `"r"` → `"R"` |
| Pool reference | `environmentArtifactId` | Use Phase 0 `poolMappings` to resolve Environment ID |
| N/A | `defaultLakehouseArtifactId` | Lakehouse from Phase 1 (required for Fabric SJDs) |

#### Upload Definition Payload

```json
{
  "definition": {
    "format": "SparkJobDefinitionV1",
    "parts": [
      {
        "path": "SparkJobDefinitionV1.json",
        "payload": "{base64-encoded config JSON from above}",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

> Returns HTTP 200 (synchronous) or 202 (LRO). Poll `Location` header until `status == "Succeeded"`.

> **V2 format**: For Python/R SJDs where the source file should be bundled inline (rather than referenced by `abfss://` path), use `format: "SparkJobDefinitionV2"` and add a `Main/{filename}` part. V2 does **not** support JAR files inline.

### Key Differences: Synapse SJD vs. Fabric SJD

| Aspect | Synapse | Fabric |
|---|---|---|
| Lakehouse context | Not required (uses workspace default ADLS) | **Required** — every SJD must have at least one Lakehouse |
| Supported languages | Python, Scala/Java, R, **.NET** | Python, Scala/Java, R — **.NET not supported** |
| Retry policies | Not built-in | Built-in retry (max retries, retry interval) |
| Scheduling | Requires pipeline with Spark Job activity | Built-in scheduling (Settings → Schedule) |
| Pool binding | Spark pool reference | Environment binding |
| Import/Export | UI-based JSON import/export | No UI import/export — REST API only |

> **.NET for Spark**: Synapse SJDs using C#/F# must be rewritten in Python or Scala before migration. There is no Fabric equivalent.

---

## Step 7 (Phase 2): (Optional) Validate Before Proceeding to Phase 3

Run migrated notebooks to catch refactoring issues before moving to SJDs.

| Check | How | Pass Criteria |
|---|---|---|
| Notebook execution | Run each notebook via Job API (`POST /workspaces/{wsId}/items/{itemId}/jobs/instances?jobType=RunNotebook`) | All complete with `status == "Completed"` |
| Common failures | Check error messages against the failure patterns table | All fixable errors resolved and re-tested |
| Output comparison | For notebooks that produce output tables, compare row counts / checksums with Synapse results | Match within tolerance |

> **Do not proceed to Phase 3** until critical notebooks execute successfully. SJDs often depend on tables or files produced by notebooks — a broken notebook means broken SJD inputs.

See [validation-testing.md → V3: Notebook Execution Testing](validation-testing.md#v3-notebook-execution-testing) for batch execution scripts and the common failure patterns table.

---

## Step 5 (Phase 3): (Optional) Validate Before Cutover

Run migrated SJDs and perform final end-to-end verification.

| Check | How | Pass Criteria |
|---|---|---|
| SJD execution | Run each SJD via Job API (`POST /workspaces/{wsId}/items/{itemId}/jobs/instances?jobType=SparkJob`) | All complete with `status == "Completed"` |
| Query result comparison | Compare checksums / sample rows for critical tables between Synapse and Fabric | Match |
| Full validation report | Run the V6 report generator from validation-testing.md | All categories show `PASS`; verdict is `READY FOR CUTOVER` |

See [validation-testing.md → V4–V6](validation-testing.md#v4-sjd-execution-testing) for SJD batch testing, query comparison, and report generation.

---

## Migration Report

After migration, generate a comprehensive report with clickable Fabric portal links for every migrated item.

See **[migration-report.md](migration-report.md)** for:
- Fabric portal URL patterns for all item types (Lakehouse, Notebook, SJD, Environment)
- Python script that queries the Fabric workspace and produces a Markdown report
- Incremental tracking (`log_migrated_item()`) to build the report during migration
- Synapse Studio source links for side-by-side comparison

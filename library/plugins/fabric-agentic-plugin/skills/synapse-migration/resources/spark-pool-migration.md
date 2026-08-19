# Synapse Spark Pool → Fabric Environment Migration

Migrate Synapse Spark pool configurations (compute settings, libraries, Spark properties) to Fabric Environments via REST APIs.

> **Execute as Phase 0** — before Lake Databases, Notebooks, and SJDs — so that Environments exist for notebook and SJD binding in later phases.
>
> **Auth tokens** (see [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) for commands):
> - Synapse ARM audience: `https://management.azure.com`
> - Fabric audience: `https://api.fabric.microsoft.com`

---

## Migration Workflow

```
Phase 0: Spark Pool → Fabric Environment
├── Step 1: Inventory Synapse Spark pools (ARM API)
├── Step 2: Decide per pool — Starter Pool or Custom Environment?
├── Step 3: Create Fabric Environment (if needed)
├── Step 4: Build definition parts (Sparkcompute.yml + libraries)
├── Step 5: Upload definition and publish
├── Step 6: Record pool → Environment mapping for Phase 2/3
└── Step 7: (Optional) Validate before proceeding to Phase 1
```

---

## Step 1: Inventory Synapse Spark Pools

Spark pools use the **ARM (management plane)** API, not the Synapse data-plane API.

### List All Pools

**Endpoint**:
```
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Synapse/workspaces/{workspaceName}/bigDataPools?api-version=2021-06-01
```

Response: `{ "value": [ ...BigDataPoolResourceInfo[] ] }` — paginated via `nextLink`.

### Get Single Pool

**Endpoint**:
```
GET https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Synapse/workspaces/{workspaceName}/bigDataPools/{poolName}?api-version=2021-06-01
```

### Key Properties to Extract

| Property | Field Path | Example |
|---|---|---|
| Pool name | `name` | `"MySparkPool"` |
| Spark version | `properties.sparkVersion` | `"3.3"`, `"3.4"`, `"3.5"` |
| Node size | `properties.nodeSize` | `Small`, `Medium`, `Large`, `XLarge`, `XXLarge` |
| Node size family | `properties.nodeSizeFamily` | `MemoryOptimized`, `HardwareAcceleratedGPU` |
| Node count | `properties.nodeCount` | `4` |
| Autoscale | `properties.autoScale` | `{ enabled, minNodeCount, maxNodeCount }` |
| Auto-pause | `properties.autoPause` | `{ enabled, delayInMinutes }` |
| Dynamic executor alloc | `properties.dynamicExecutorAllocation` | `{ enabled, minExecutors, maxExecutors }` |
| Library requirements | `properties.libraryRequirements` | `{ content, filename }` — pip/conda requirements.txt |
| Custom libraries | `properties.customLibraries[]` | `{ name, type, path, containerName }` — uploaded JARs, wheels |
| Spark config properties | `properties.sparkConfigProperties` | `{ content, filename, configurationType }` — Spark .conf/.yml |
| Compute isolation | `properties.isComputeIsolationEnabled` | `true` / `false` |
| Autotune | `properties.isAutotuneEnabled` | `true` / `false` |

---

## Step 2: Decision — Starter Pool vs. Environment

For each Synapse pool, decide whether a Fabric Environment is needed:

```
Synapse Pool:
├── Has GPU nodes (nodeSizeFamily == "HardwareAcceleratedGPU")?
│   └── YES → MIGRATION BLOCKER — GPU not supported in Fabric. Refactor to CPU or keep on Synapse.
│
├── Has custom libraries OR custom Spark config properties?
│   ├── YES → Create Environment (libraries + config only; compute can still be Starter Pool)
│   └── NO
│       ├── Has non-default node size (not Medium)?
│       │   ├── YES → Create Environment WITH Custom Pool definition
│       │   └── NO  → No Environment needed — use Starter Pool
│       └── Has Managed Private Endpoint requirements?
│           ├── YES → Create Environment WITH Custom Pool (MPE requires Custom Pool)
│           └── NO  → No Environment needed — use Starter Pool
```

### Decision Summary Table

| Synapse Pool Has... | Environment Needed? | Custom Pool Needed? | Action |
|---|---|---|---|
| Default (Medium), no libs, no config | No | No | Use Starter Pool — nothing to create |
| Custom libraries only | **Yes** | No | Environment with libraries; compute = Starter Pool |
| Custom Spark config only | **Yes** | No | Environment with Spark properties; compute = Starter Pool |
| Custom libs + Spark config | **Yes** | No | Environment with both; compute = Starter Pool |
| Non-default node size (Small, Large, XLarge, XXLarge) | **Yes** | **Yes** | Environment with Custom Pool definition |
| Node size + libs + config | **Yes** | **Yes** | Environment with Custom Pool + libs + config |
| GPU nodes | N/A | N/A | **Migration blocker** — no Fabric equivalent |
| Managed Private Endpoints required | **Yes** | **Yes** | Custom Pool required for MPE in Fabric |

> **Pools that need no Environment**: Record them in the mapping as `"StarterPool"` so that Phase 2/3 knows no Environment binding is needed for their notebooks/SJDs.

---

## Step 3: Create Fabric Environment

**Endpoint**: `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments`

```json
{
  "displayName": "{poolName}_env",
  "description": "Migrated from Synapse Spark pool: {poolName}"
}
```

Response: HTTP 201 (or 202 LRO). Capture the Environment `id` for subsequent steps.

---

## Step 4: Build Definition Parts

The Fabric Environment definition consists of file-based parts, each base64-encoded.

### Part 1: `Setting/Sparkcompute.yml` — Compute & Spark Properties

Build this YAML from the Synapse pool properties. The schema follows the canonical Fabric Environment definition — see [common/ITEM-DEFINITIONS-CORE.md § Environment](../../../common/ITEM-DEFINITIONS-CORE.md) for the source of truth.

```yaml
# Sparkcompute.yml
instance_pool_id: "{customPoolId}"      # GUID of a Fabric Custom Pool created at workspace level (omit for Starter Pool)
runtime_version: "1.3"                  # See Spark Version Mapping below

# Spark configuration carried over from Synapse sparkConfigProperties
spark_conf:
  spark.sql.shuffle.partitions: "200"
  spark.sql.adaptive.enabled: "true"
  spark.executor.memory: "8g"
  spark.driver.memory: "4g"
  # ... all valid key=value pairs from Synapse pool config

# Optional — dynamic executor allocation (carried over from Synapse pool)
dynamic_executor_allocation:
  enabled: {dynamicExecutorAllocation.enabled}
  min_executors: {dynamicExecutorAllocation.minExecutors}
  max_executors: {dynamicExecutorAllocation.maxExecutors}

# Optional — Native Execution Engine (Fabric-only, no Synapse equivalent)
enable_native_execution_engine: false
```

> **Pool sizing**: Synapse `nodeFamily`/`nodeSize`/`autoScale` (min/max node count) are not part of the Sparkcompute.yml schema. Instead, create a Fabric **Custom Pool** at the workspace level with the equivalent node family/size and autoscale settings, then reference its GUID via `instance_pool_id`. See `notebookutils.fabricClient` Custom Pool APIs or the workspace settings UI.

> **If no Custom Pool needed** (Starter Pool scenario): Omit the `instance_pool_id` field entirely. Only include `runtime_version` and `spark_conf`.

#### Spark Version Mapping

| Synapse `sparkVersion` | Fabric Runtime | Status |
|---|---|---|
| `"3.3"` | Runtime 1.1 | EOL — upgrade to 1.3 |
| `"3.4"` | Runtime 1.2 | EOL — upgrade to 1.3 |
| `"3.5"` | Runtime 1.3 | GA (recommended) |

> If the Synapse pool uses Spark 3.3 or 3.4, **upgrade to Runtime 1.3** (Spark 3.5). Test for deprecated API warnings after migration.

#### Spark Config Migration Rules

**Direct carryover** — copy these as-is to `spark_conf`:

| Config Key | Notes |
|---|---|
| `spark.sql.shuffle.partitions` | Works identically |
| `spark.executor.memory` | Works identically |
| `spark.executor.cores` | Works identically |
| `spark.driver.memory` | Works identically |
| `spark.driver.cores` | Works identically |
| `spark.dynamicAllocation.*` | Prefer the `dynamic_executor_allocation` section instead |
| `spark.sql.adaptive.enabled` | Enabled by default in Fabric |
| `spark.sql.adaptive.coalescePartitions.enabled` | Works identically |
| `spark.sql.sources.default` | Usually "delta" |
| `spark.databricks.delta.*` | Works identically |
| `spark.sql.parquet.*` | Works identically |
| `spark.serializer` | Works identically |
| `spark.kryoserializer.*` | Works identically |
| `spark.sql.broadcastTimeout` | Works identically |
| `spark.network.timeout` | Works identically |
| `spark.rpc.message.maxSize` | Works identically |
| `spark.hadoop.fs.azure.account.auth.type.*` | Review — may need updated credentials |
| `spark.hadoop.fs.azure.account.oauth.*` | Review — may need new service principal values |

**Strip/remove** — these are Synapse-specific and will cause warnings or errors:

| Config Key | Reason |
|---|---|
| `spark.synapse.linkedService.*` | Linked services don't exist in Fabric |
| `spark.storage.synapse.*` | Synapse internal storage config |
| `spark.synapse.pool.*` | Synapse pool-specific settings |
| `spark.synapse.workspace.*` | Synapse workspace internals |
| `spark.hadoop.fs.azure.account.oauth.provider.type` = `...LinkedServiceBasedTokenProvider` | Replace with `ClientCredsTokenProvider` (see [connectivity-migration.md](connectivity-migration.md)) |

**Add (Fabric-only optimizations)** — consider adding these:

| Config Key | Value | Benefit |
|---|---|---|
| `spark.native.enabled` | `"true"` | Enables Native Execution Engine (Velox/Gluten) — up to 4x on TPC-DS |
| `spark.fabric.delta.vorder.enabled` | `"true"` | Enables V-Order write optimization for Power BI Direct Lake |

### Part 2: `Libraries/PublicLibraries/environment.yml` — PyPI/Conda Packages

Convert the Synapse `libraryRequirements.content` (requirements.txt format) to Fabric's `environment.yml` format:

**Synapse** (`requirements.txt` format):
```
pandas==2.1.0
scikit-learn==1.3.0
azure-storage-blob==12.19.0
```

**Fabric** (`environment.yml` format):
```yaml
dependencies:
  - pip:
    - pandas==2.1.0
    - scikit-learn==1.3.0
    - azure-storage-blob==12.19.0
```

> If the Synapse pool has no `libraryRequirements.content` (empty string), skip this part.

### Part 3: `Libraries/CustomLibraries/*` — JARs, Wheels, Tars

For each entry in `properties.customLibraries[]`:
1. Download the library file from the Synapse workspace storage (the `path` field gives the blob path)
2. Base64-encode the file content
3. Include as a definition part with path `Libraries/CustomLibraries/{filename}`

Supported file types:
- `.jar` — Java/Scala libraries
- `.whl` — Python wheels
- `.tar.gz` — Python/R packages
- `.py` — Python files

> **Downloading custom libraries**: The `path` and `containerName` fields in `customLibraries[]` point to the Synapse workspace's linked storage account. Use the Azure Storage SDK or `az storage blob download` to retrieve each file before uploading to Fabric.

---

## Step 5: Upload Definition and Publish

### Update Environment Definition

**Endpoint**: `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/updateDefinition`

> **Important**: The endpoint is `/updateDefinition` — do NOT add a `/staging/` prefix. The `/staging/` prefix is only used for the `publish` endpoint. Using `/staging/updateDefinition` returns 404.

> **Race condition**: After creating an Environment (`POST /environments` → 201), there is a brief provisioning window during which the `updateDefinition` endpoint may return 404. If `updateDefinition` returns 404 immediately after creation, wait 2–5 seconds and retry (up to 3 attempts). This is a known Fabric API timing issue — the item exists but its definition endpoints are not yet ready.

#### Retry Helper

```python
import time, requests

def update_env_definition(workspace_id, env_id, definition_payload, headers, max_retries=3):
    """Upload Environment definition with retry for post-creation race condition."""
    url = (f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"
           f"/environments/{env_id}/updateDefinition")
    for attempt in range(1, max_retries + 1):
        resp = requests.post(url, headers=headers, json=definition_payload)
        if resp.status_code == 404 and attempt < max_retries:
            time.sleep(3 * attempt)  # 3s, 6s backoff
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()  # raise on final 404
```

#### Definition Payload

```json
{
  "definition": {
    "parts": [
      {
        "path": "Setting/Sparkcompute.yml",
        "payload": "{base64-encoded-sparkcompute-yml}",
        "payloadType": "InlineBase64"
      },
      {
        "path": "Libraries/PublicLibraries/environment.yml",
        "payload": "{base64-encoded-environment-yml}",
        "payloadType": "InlineBase64"
      },
      {
        "path": "Libraries/CustomLibraries/mylib.jar",
        "payload": "{base64-encoded-jar}",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

> Returns HTTP 202 (LRO). Poll `Location` header until `status == "Succeeded"`.

### Publish Environment

**Critical**: Environment changes are **staged** until published. You must explicitly publish:

**Endpoint**: `POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}/staging/publish`

> Returns HTTP 202 (LRO). Poll until `status == "Succeeded"`. Publishing can take several minutes for environments with many libraries.

### Verify Publish Status

**Endpoint**: `GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/environments/{environmentId}`

Check `properties.publishDetails.state` — should be `"Success"`.

---

## Step 6: Record Pool → Environment Mapping

Produce a mapping table for use in Phase 2 (Notebooks) and Phase 3 (SJDs):

```json
{
  "poolMappings": {
    "MySparkPool": {
      "fabricEnvironmentId": "5b218778-e7a5-4d73-8187-f10824047715",
      "fabricEnvironmentName": "MySparkPool_env",
      "mode": "customPool"
    },
    "DevPool": {
      "fabricEnvironmentId": null,
      "fabricEnvironmentName": null,
      "mode": "starterPool"
    },
    "ETLPool": {
      "fabricEnvironmentId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "fabricEnvironmentName": "ETLPool_env",
      "mode": "librariesOnly"
    }
  }
}
```

This mapping is consumed by:
- **Phase 2 (Notebooks)**: When a Synapse notebook references `bigDataPool.referenceName: "MySparkPool"`, bind the Fabric notebook to `MySparkPool_env`
- **Phase 3 (SJDs)**: When a Synapse SJD references `targetBigDataPool.referenceName: "ETLPool"`, bind the Fabric SJD to `ETLPool_env`

---

## Step 7: (Optional) Validate Before Proceeding to Phase 1

Run these checks before moving to Lake Database migration. Catching issues here avoids cascading failures in later phases.

| Check | How | Pass Criteria |
|---|---|---|
| Publish status | `GET /v1/workspaces/{wsId}/environments/{envId}` → `properties.publishDetails.state` | `"Success"` for every Environment |
| Library imports | Run a test notebook that `import`s each required library | No `ImportError` |
| Spark config | Compare `spark_conf` in Environment definition against Synapse pool config | All carried-over keys present; no stripped keys |
| Pool mapping file | Review the JSON mapping from Step 6 | Every Synapse pool has an entry (Environment ID or `"starterPool"`) |

> **Do not proceed to Phase 1** until all Environments publish successfully and libraries import without errors. Notebooks and SJDs in later phases will bind to these Environments — a broken Environment means every notebook fails.

See [validation-testing.md → V1: Environment Validation](validation-testing.md#v1-environment-validation) for detailed scripts.

---

## Migration Blockers & Limitations

| Synapse Feature | Fabric Status | Action |
|---|---|---|
| GPU pools (`HardwareAcceleratedGPU`) | **Not supported** | Refactor to CPU-based alternatives or keep on Synapse |
| Compute isolation (`isComputeIsolationEnabled`) | Not available | Remove; rely on capacity-based isolation |
| Auto-pause | Not needed | Fabric Starter Pool has no idle cost; Custom Pools auto-release |
| Session-level packages (`sessionLevelPackagesEnabled`) | Supported via `%pip install` in notebooks | Not recommended for production — use Environment libraries |
| Workspace-level libraries | **Deprecated** in Fabric | Migrate all to Environment artifacts |
| Autotune (`isAutotuneEnabled`) | Not available | Remove; manually tune or rely on defaults |

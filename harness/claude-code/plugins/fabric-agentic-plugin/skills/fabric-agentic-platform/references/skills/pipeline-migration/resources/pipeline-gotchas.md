# Pipeline Migration Gotchas

Expanded troubleshooting for the gotchas listed in SKILL.md, plus guidance on parked activities and common expression migration issues.

---

## PG1 — Notebooks Must Exist in Fabric Before Pipeline Deploy

**Problem**: Deploying the pipeline before the notebooks are migrated results in a broken `notebookId` reference.

**Symptom**: Pipeline validation or first run fails with "Item not found" or a schema validation error on `notebookId`.

**Resolution**:
1. Run the **synapse-migration** skill to migrate all Synapse notebooks to Fabric *first*
2. Build `notebook_map = {synapseNotebookName: fabricNotebookId}` using `GET /v1/workspaces/{wsId}/notebooks`
3. Verify every notebook referenced in the pipeline exists in the map before running the transformation script
4. Only then deploy the pipeline

**Verification check**:
```python
# Before deploying, confirm all referenced notebooks exist
missing = [name for name in referenced_notebooks if name not in notebook_map]
if missing:
    raise RuntimeError(f"These notebooks are not yet in Fabric: {missing}")
```

---

## PG2 — Timeout Capped at 12 Hours for TridentNotebook

**Problem**: Synapse `SynapseNotebook` activities allow up to 7 days (`7.00:00:00`) timeout. Fabric `TridentNotebook` maximum is 12 hours (`0.12:00:00`).

**Symptom**: Pipeline validation error if `policy.timeout` exceeds 12 hours, or activity silently times out mid-run.

**Resolution**:
- The transformation script in [notebook-activity-migration.md](notebook-activity-migration.md) automatically clamps timeouts to `0.12:00:00`
- If a workload genuinely needs > 12 hours, restructure it as a Fabric Spark Job Definition (SJD), which supports longer runtimes
- For orchestrated long-running jobs, break the notebook into phases and chain `TridentNotebook` activities with intermediate checkpoints

---

## PG3 — `@pipeline().globalParameters` Not Recognized

**Problem**: Fabric pipelines do not support `@pipeline().globalParameters`. The expression returns null or causes a parse error.

**Symptom**: Pipeline activities receive null values where global parameter values were expected. Often surfaces as NullPointerException in downstream notebook code.

**Resolution**:
1. Create a Variable Library — see [global-parameters-to-variable-library.md](global-parameters-to-variable-library.md)
2. Attach the Variable Library to the pipeline via `libraryVariables` in the pipeline definition
3. Replace all expressions:
   - **Before**: `@pipeline().globalParameters.myParam`
   - **After**: `@pipeline().libraryVariables.myParam`

Phase 4 of the inline runner in [pipeline-orchestrator.md](pipeline-orchestrator.md) applies this rewrite by walking the pipeline object tree and replacing the substring **only inside the canonical ADF/Fabric expression dict shape** `{"value": "@...", "type": "Expression"}` immediately before base64-encoding for upload. Bare string fields — descriptions, annotations, and any embedded prose that happens to contain `@pipeline().globalParameters.` literally — are left untouched. No separate script is required.

---

## PG4 — Datasets Are Not Supported as Items

**Problem**: Attempting to create or reference a Fabric Dataset item will fail — the item type does not exist in Fabric Data Factory.

**Symptom**: Deployment error `"Item type 'Dataset' is not supported"` or missing connector settings in activity output.

**Resolution**: All dataset properties must be inlined into each activity's `typeProperties`. See [dataset-inlining.md](dataset-inlining.md) for full inlining patterns and a Python helper.

---

## PG5 — Self-Hosted IR Activities Require On-Premises Data Gateway

**Problem**: Synapse linked services backed by a Self-Hosted Integration Runtime (SHIR) must be backed by an on-premises data gateway in Fabric. Migrating the pipeline without the gateway in place will cause connection failures.

**Symptom**: Activity fails with `"Connection refused"` or `"Gateway not found"` at runtime.

**Resolution**:
1. Install the **on-premises data gateway** on the same machine or network as the SHIR
   - Download: https://aka.ms/odg/download
   - Register under the same tenant as the Fabric workspace
2. In the Fabric workspace: **Settings → Manage connections and gateways → On-premises data gateways**
3. Create the Fabric connection using the gateway for connector types that require it (SQL Server on-premises, Oracle, SAP, file system)
4. Update the connection reference in the inlined dataset / activity `typeProperties`

> **Note**: Gateway setup must be done before pipeline deployment for SHIR-backed activities. Plan this as a prerequisite in the migration timeline.

---

## PG6 — Validation Activity Has No Direct Equivalent

**Problem**: Synapse `Validation` activity type does not exist in Fabric.

**Symptom**: Pipeline upload fails with `"Unknown activity type: Validation"` or pipeline behavior is undefined.

**Resolution**: Replace each `Validation` activity with a `GetMetadata` + `IfCondition` pair. Full before/after JSON is in [activity-mapping.md § Validation](activity-mapping.md#validation-activity--getmetadata--ifcondition).

---

## PG7 — ExecutePipeline Must Include `workspaceId`

**Problem**: In Synapse, `ExecutePipeline` references the child pipeline by name within the same workspace. In Fabric, the `workspaceId` is required even for same-workspace child pipelines, and the `referenceName` should be the Fabric item ID (GUID).

**Symptom**: Child pipeline not found at runtime, or incorrect pipeline executed.

**Resolution**:
1. After deploying all child pipelines to Fabric, build a pipeline name→ID map.
   The list endpoint is paginated by `continuationToken` — large workspaces
   can return partial results in a single page, so always loop until the
   token is absent. (`pipeline-orchestrator.md` exposes a reusable
   `fabric_paginate(path)` helper that wraps this pattern; the snippet below
   inlines it so this gotcha doc stays self-contained.)
   ```python
   import requests
   from urllib.parse import quote

   def get_pipeline_id_map(workspace_id, fabric_token):
       headers = {"Authorization": f"Bearer {fabric_token}"}
       base = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/datapipelines"
       items, url = [], base
       while url:
           r = requests.get(url, headers=headers)
           r.raise_for_status()
           data = r.json()
           items.extend(data.get("value", []))
           cont = data.get("continuationToken")
           # Fabric continuation tokens are base64-like and routinely contain
           # '+', '/', '=' which must be percent-encoded; raw concatenation
           # silently breaks pagination on workspaces with > 1 page.
           url = f"{base}?continuationToken={quote(cont, safe='')}" if cont else None
       return {p["displayName"]: p["id"] for p in items}
   ```
2. Substitute `referenceName` with the child pipeline GUID
3. Add `"workspaceId": "<workspace-guid>"` to `typeProperties`

---

## PG8 — AzureKeyVault Linked Service Is Not Needed

**Problem**: Synapse uses an Azure Key Vault linked service to reference secrets in activity configurations. Fabric pipelines access Key Vault secrets differently.

**Symptom**: Linked service of type `AzureKeyVault` cannot be created as a Fabric connection; activities that use `@linkedService().secret(...)` expression fail.

**Resolution options**:
- Use a `WebActivity` to call the Key Vault REST API to retrieve the secret, store it in a pipeline variable, and pass it to subsequent activities — see the secret-hygiene block below for required `secureInput`/`secureOutput` settings
- Use managed identity with Key Vault access policy — call `GET https://<vault>.vault.azure.net/secrets/<name>?api-version=7.4`
- Store non-sensitive config in Variable Library; store sensitive secrets in Key Vault and fetch via `WebActivity`

> **Secret hygiene — required, not optional**: by default Fabric records every activity's inputs/outputs in run history. A `WebActivity` that returns a Key Vault secret will surface the secret in the activity output, and any downstream `SetVariable`/`Web`/`Copy` activity that touches it will surface it again in its inputs. Mark the boundary activities `secureInput: true` / `secureOutput: true` on `policy` so Fabric redacts the values:
> - On the `WebActivity` that calls Key Vault, set `policy.secureOutput: true` (and `policy.secureInput: true` if the URL contains a secret).
> - On any activity that receives the secret (e.g. `SetVariable`, the `WebActivity` that uses the token), set `policy.secureInput: true`, and `policy.secureOutput: true` if it forwards the secret further.
> - Never concatenate secret expressions into `Fail.message`, `Wait` activity names, error messages, or notebook parameter values that get logged.

```json
{
  "name": "Get Secret From Key Vault",
  "type": "WebActivity",
  "policy": {
    "secureInput": true,
    "secureOutput": true
  },
  "typeProperties": {
    "url": "https://<vault-name>.vault.azure.net/secrets/<secret-name>?api-version=7.4",
    "method": "GET",
    "authentication": {
      "type": "MSI",
      "resource": "https://vault.azure.net"
    }
  }
},
{
  "name": "Set Secret Variable",
  "type": "SetVariable",
  "dependsOn": [{ "activity": "Get Secret From Key Vault", "dependencyConditions": ["Succeeded"] }],
  "policy": {
    "secureInput": true,
    "secureOutput": true
  },
  "typeProperties": {
    "variableName": "secretValue",
    "value": {
      "value": "@activity('Get Secret From Key Vault').output.value",
      "type": "Expression"
    }
  }
}
```

---

## PG9 — Array/Object Global Parameters Have No Direct Equivalent

**Problem**: Synapse supports `array` and `object` typed global parameters. Fabric Variable Library supports only `String`, `Integer`, `Number`, `Boolean`.

**Symptom**: Migration script serializes arrays as JSON strings. Pipeline expressions that index into the array (e.g., `@pipeline().globalParameters.myArray[0]`) no longer work after migration.

**Resolution**:
1. In [global-parameters-to-variable-library.md](global-parameters-to-variable-library.md), arrays are stored as JSON strings
2. Update expressions that access array elements:
   - **Before**: `@pipeline().globalParameters.allowedRegions[0]`
   - **After**: `@json(pipeline().libraryVariables.allowedRegions)[0]`
3. For object properties:
   - **Before**: `@pipeline().globalParameters.config.connectionString`
   - **After**: `@json(pipeline().libraryVariables.config).connectionString`

---

## PG10 — Pipeline Item Must Use `DataPipeline` Type

**Problem**: When creating pipeline items via the Fabric REST API, the `type` must be `DataPipeline` (not `Pipeline` or `AdfPipeline`).

**Symptom**: `POST /v1/workspaces/{wsId}/items` returns `400 Bad Request` with `"Item type 'Pipeline' is not supported"`.

**Resolution**: Always use `"type": "DataPipeline"` in the item creation payload:
```json
{
  "displayName": "MyPipeline",
  "type": "DataPipeline",
  "definition": {
    "format": "DataPipeline",
    "parts": [...]
  }
}
```

---

## Parked Activities — No Fabric Equivalent

These activity types have no viable Fabric Data Factory equivalent. They are logged in the [migration report](migration-report.md) as blockers.

### SSIS (`ExecuteSSISPackage`)

**Situation**: SSIS packages run in Synapse via Azure-SSIS Integration Runtime (Azure-SSIS IR). Fabric has no Azure-SSIS IR.

**Options**:
- Migrate SSIS packages to **Azure Data Factory** (retain SSIS IR there) and invoke via `WebActivity` calling ADF REST API
- Refactor SSIS package logic into Fabric Notebooks or Fabric Dataflows
- Run SSIS in **SQL Server Integration Services** on Azure SQL Managed Instance

```json
{
  "name": "Run SSIS Package",
  "type": "WebActivity",
  "typeProperties": {
    "url": "https://management.azure.com/subscriptions/.../factories/<adf>/pipelines/<pipeline>/createRun?api-version=2018-06-01",
    "method": "POST",
    "authentication": { "type": "MSI", "resource": "https://management.azure.com/" },
    "body": { "runDate": "@pipeline().parameters.runDate" }
  }
}
```

### Databricks (`DatabricksNotebook`, `DatabricksSparkJar`, `DatabricksSparkPython`)

**Situation**: No native Databricks activity type in Fabric.

**Options**:
- Use `WebActivity` to trigger the Databricks Jobs REST API. Fetch the bearer token from Key Vault at run-time and treat it as a secret end-to-end — **do not** put the token in a Variable Library (it is not a secrets store, and library values appear in run history and any exported library JSON):
  ```json
  [
    {
      "name": "Get Databricks Token From Key Vault",
      "type": "WebActivity",
      "policy": {
        "secureInput": true,
        "secureOutput": true
      },
      "typeProperties": {
        "url": "https://<vault-name>.vault.azure.net/secrets/databricks-token?api-version=7.4",
        "method": "GET",
        "authentication": { "type": "MSI", "resource": "https://vault.azure.net" }
      }
    },
    {
      "name": "Set Databricks Token Variable",
      "type": "SetVariable",
      "dependsOn": [
        { "activity": "Get Databricks Token From Key Vault", "dependencyConditions": ["Succeeded"] }
      ],
      "policy": {
        "secureInput": true,
        "secureOutput": true
      },
      "typeProperties": {
        "variableName": "databricksToken",
        "value": {
          "value": "@activity('Get Databricks Token From Key Vault').output.value",
          "type": "Expression"
        }
      }
    },
    {
      "name": "Run Databricks Job",
      "type": "WebActivity",
      "dependsOn": [
        { "activity": "Set Databricks Token Variable", "dependencyConditions": ["Succeeded"] }
      ],
      "policy": {
        "secureInput": true,
        "secureOutput": true
      },
      "typeProperties": {
        "url": "https://<databricks-workspace>.azuredatabricks.net/api/2.1/jobs/run-now",
        "method": "POST",
        "headers": {
          "Authorization": {
            "value": "@concat('Bearer ', variables('databricksToken'))",
            "type": "Expression"
          }
        },
        "body": { "job_id": 12345 }
      }
    }
  ]
  ```
- Migrate the Databricks workload to a Fabric Notebook (if it uses PySpark without Databricks-specific APIs)
- Keep Databricks in ADF and invoke from Fabric via `WebActivity` → ADF REST API

> **Security note**: Always retrieve the Databricks token from Key Vault at run-time using the `WebActivity` pattern above, with `policy.secureInput`/`secureOutput` set on every activity that touches the secret. Never put the token in a Variable Library, never hardcode it in pipeline JSON, and never concatenate it into `Fail.message`, activity names, or notebook parameters that get logged. See [pipeline-gotchas PG8 (AzureKeyVault)](#pg8--azurekeyvault-linked-service-is-not-needed) for the full secret-hygiene pattern.

### Azure Batch / Custom (`AzureBatch`, `Custom`)

**Situation**: No Fabric equivalent. These activities run custom executables on Azure Batch pools.

**Options**:
- Migrate workload to a Fabric Notebook (if it's a Python/Scala data transformation)
- Trigger Azure Batch jobs via `WebActivity` calling the Azure Batch REST API
- Use Azure Container Apps Jobs or Azure Functions for the compute, invoked via `WebActivity`

### HDInsight MapReduce / Pig / Hive

**Situation**: HDInsight cluster types not available in Fabric.

**Options**:
- Migrate MapReduce/Pig logic to PySpark and run as `TridentNotebook`
- Migrate Hive queries to Fabric Warehouse T-SQL or Fabric Notebook using Spark SQL

---

## Expression Migration Reference

| Pattern | Before (Synapse) | After (Fabric) | Notes |
|---|---|---|---|
| Global parameter | `@pipeline().globalParameters.x` | `@pipeline().libraryVariables.x` | Bulk-replaced by transform script |
| Array global parameter element | `@pipeline().globalParameters.arr[0]` | `@json(pipeline().libraryVariables.arr)[0]` | Manual fix required |
| Object global parameter property | `@pipeline().globalParameters.obj.key` | `@json(pipeline().libraryVariables.obj).key` | Manual fix required |
| Pipeline variable | `@variables('x')` | `@variables('x')` | No change |
| Activity output | `@activity('A').output.x` | `@activity('A').output.x` | No change |
| Notebook run output | `@activity('A').output.runOutput` | `@activity('A').output.runOutput` | No change |
| Dataset parameter | `@dataset().paramName` | *(inlined — remove expression)* | Replaced during inlining |
| Linked service parameter | `@linkedService().paramName` | *(inlined or connection reference)* | Replaced during inlining |

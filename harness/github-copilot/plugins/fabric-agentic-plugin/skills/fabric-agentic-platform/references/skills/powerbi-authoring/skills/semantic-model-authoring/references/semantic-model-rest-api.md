# Semantic Model REST API Reference

Fabric and Power BI REST API operations for semantic models via `az rest`. Covers TMDL definition CRUD, refresh, data sources, parameters, permissions, and property retrieval.

Common variables used throughout this guide:

```bash
API_FABRIC="https://api.fabric.microsoft.com/v1"
API_PBI="https://api.powerbi.com/v1.0/myorg"
RESOURCE_PBI="https://analysis.windows.net/powerbi/api"
RESOURCE_FABRIC="https://api.fabric.microsoft.com"
WS_ID="<workspaceId>"
MODEL_ID="<semanticModelId>"   # same value as datasetId
```

---

## Authentication & API Audiences

This skill uses **two distinct API audiences**. Using the wrong audience returns a 401.

| API                   | Audience (`--resource`)                    | Use For                                                                      |
| --------------------- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| Fabric Items API      | `https://api.fabric.microsoft.com`         | Create/get/update/delete semantic model definitions, list items, LRO polling |
| Power BI Datasets API | `https://analysis.windows.net/powerbi/api` | Refresh, data sources, parameters, permissions, operational properties       |

```bash
# Fabric Items API
az rest --method post \
  --resource "$RESOURCE_FABRIC" \
  --url "$API_FABRIC/workspaces/$WS_ID/semanticModels" \
  ...

# Power BI Datasets API
az rest --method post \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$DATASET_ID/refreshes" \
  ...
```
---

## API Rules

- **Always pass `--resource`** to `az rest` - omitting it causes silent auth failures
- **Always pass `--headers "Content-Type=application/json"`** on POST/PATCH/PUT calls with a `--body` to the Power BI Datasets API
- **Include ALL definition parts** in `updateDefinition` - modified + unmodified. The API replaces the entire definition; omitting parts deletes them
- **Never include `.platform`** in `updateDefinition` payloads - it is Git integration metadata and causes errors
- **Poll LRO to completion** - `create semantic model`, `getDefinition`, and `updateDefinition` return `202 Accepted` with an `Operation-Id` header
- **Base64-encode TMDL content** - all `payload` values in definition parts must be base64-encoded
- **Verify workspace has capacity** before creating a semantic model - call `GET /v1/workspaces/{id}` and check `capacityId`
- Prefer `create semantic model` (single POST) over create-then-update for new semantic models
- Get definition before updating - always retrieve the current definition, modify, then POST back to avoid overwriting concurrent changes

---

## TMDL Definition CRUD (Fabric Items API)

For the full definition envelope and part paths, see [ITEM-DEFINITIONS-CORE.md](../../../common/ITEM-DEFINITIONS-CORE.md#semanticmodel).

### TMDL File Structure

Required TMDL parts for `create semantic model` and `updateDefinition`:

| Part Path                            | Content                                           | Required         |
| ------------------------------------ | ------------------------------------------------- | ---------------- |
| `definition.pbism`                   | Semantic model connection settings                | Yes              |
| `definition/database.tmdl`           | Database properties (compatibility level)         | Yes              |
| `definition/model.tmdl`              | Model properties (culture, default summarization) | Yes              |
| `definition/tables/<TableName>.tmdl` | Per-table: columns, measures, partitions          | Yes (at least 1) |

> **Critical**: `updateDefinition` must include ALL parts - modified and unmodified. The API replaces the entire definition. Never include `.platform` in update payloads.

#### Minimal TMDL Content

**definition.pbism:**

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
    "version": "4.2",
    "settings": {
        "qnaEnabled": true
    }
}
```

**database.tmdl:**

```tmdl
database
	compatibilityLevel: 1702
	compatibilityMode: powerBI
```

**model.tmdl:**

```tmdl
model Model
	culture: en-US
	defaultPowerBIDataSourceVersion: powerBI_V3	
```

> **Note**: `defaultPowerBIDataSourceVersion: powerBI_V3` is required for Import-mode models.

### Create Semantic Model

Full lifecycle: author TMDL -> base64-encode -> construct payload -> POST -> poll LRO.

```bash
# 1. Base64-encode each TMDL file
PBISM=$(base64 -w 0 < definition.pbism)
DB=$(base64 -w 0 < definition/database.tmdl)
MODEL=$(base64 -w 0 < definition/model.tmdl)
TABLE=$(base64 -w 0 < definition/tables/Customer.tmdl)

# 2. Construct payload and create - use --verbose to capture HTTP status and LRO headers
cat > /tmp/body.json << EOF
{
  "displayName": "MySalesModel",
  "definition": {
    "format": "TMDL",
    "parts": [
      {"path": "definition.pbism", "payload": "$PBISM", "payloadType": "InlineBase64"},
      {"path": "definition/database.tmdl", "payload": "$DB", "payloadType": "InlineBase64"},
      {"path": "definition/model.tmdl", "payload": "$MODEL", "payloadType": "InlineBase64"},
      {"path": "definition/tables/Customer.tmdl", "payload": "$TABLE", "payloadType": "InlineBase64"}
    ]
  }
}
EOF
az rest --method post --verbose \
  --resource "$RESOURCE_FABRIC" \
  --url "$API_FABRIC/workspaces/$WS_ID/semanticModels" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json
```

> **PowerShell** - use `[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("file"))` instead of `base64 -w 0`.

If the response is `202 Accepted`, poll using the LRO pattern from [COMMON-CLI.md](../../../common/COMMON-CLI.md#long-running-operations-lro-pattern).

### Get/Download Definition

Retrieve TMDL definition for backup, migration, or inspection. `getDefinition` is a **POST** (not GET).

```bash
# 1. Request definition - may return 200 (inline) or 202 (LRO)
RESPONSE=$(az rest --method post --verbose \
  --resource "https://api.fabric.microsoft.com" \
  --url "$API_FABRIC/workspaces/$WS_ID/semanticModels/$MODEL_ID/getDefinition?format=TMDL" \
  --body '{}' \
  --output json 2>/dev/null)

# 2. If 202, poll the Location header URL until Succeeded, then GET /result

# 3. Decode each part
echo "$RESPONSE" | jq -r '.definition.parts[] | .path + " " + .payload' | \
while read -r path payload; do
  mkdir -p "$(dirname "$path")"
  echo "$payload" | base64 -d > "$path"
done
```

### Update Definition

> **Critical rules**: Must include ALL parts (modified + unmodified). Never include `.platform`. The API replaces the entire definition - omitted parts are deleted.

```bash
# 1. Get current definition (see Get/Download Definition above)
# 2. Modify the relevant TMDL files
# 3. Re-encode ALL parts and POST

cat > /tmp/body.json << EOF
{
  "definition": {
    "format": "TMDL",
    "parts": [
      {"path": "definition.pbism", "payload": "$PBISM", "payloadType": "InlineBase64"},
      {"path": "definition/database.tmdl", "payload": "$DB", "payloadType": "InlineBase64"},
      {"path": "definition/model.tmdl", "payload": "$MODEL", "payloadType": "InlineBase64"},
      {"path": "definition/tables/Customer.tmdl", "payload": "$TABLE", "payloadType": "InlineBase64"}
    ]
  }
}
EOF
az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "$API_FABRIC/workspaces/$WS_ID/semanticModels/$MODEL_ID/updateDefinition" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json
```

Use `?updateMetadata=true` query parameter only when the `.platform` file must be included to update display name or description via definition.

---

## Refresh Operations (Power BI Datasets API)

```bash
# Trigger full refresh
cat > /tmp/body.json << 'EOF'
{"notifyOption": "NoNotification"}
EOF
az rest --method post --verbose \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/refreshes" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json

# Get refresh history (latest first)
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/refreshes?\$top=5"

# Get a specific refresh's execution detail
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/refreshes/<refreshId>"

# Cancel an in-progress refresh (only work with `refreshType = ViaEnhancedApi`)
az rest --method delete \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/refreshes/<refreshId>"

# Get refresh schedule (Import models)
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/refreshSchedule"

# Update refresh schedule (Import models)
cat > /tmp/body.json << 'EOF'
{
  "value": {
    "enabled": true,
    "days": ["Monday", "Wednesday", "Friday"],
    "times": ["02:00", "14:00"],
    "localTimeZoneId": "UTC"
  }
}
EOF
az rest --method patch \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/refreshSchedule" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json

# Get DirectQuery / LiveConnection refresh schedule (separate endpoint)
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/directQueryRefreshSchedule"
```

---

## Data Sources & Parameters (Power BI Datasets API)

```bash
# Get data sources for a dataset
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/datasources"

# Get bound gateway data sources
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/Default.GetBoundGatewayDatasources"

# Discover gateways available for a dataset
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/Default.DiscoverGateways"

# Get parameters
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/parameters"

# Update parameters
cat > /tmp/body.json << 'EOF'
{
  "updateDetails": [
    {"name": "Server", "newValue": "newserver.database.windows.net"},
    {"name": "Database", "newValue": "ProductionDB"}
  ]
}
EOF
az rest --method post \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/Default.UpdateParameters" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json
```

> After updating parameters or data source credentials, trigger a refresh for changes to take effect.

---

## Permissions (Power BI Datasets API)

```bash
# List dataset users
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/users"

# Grant dataset permissions to a user
cat > /tmp/body.json << 'EOF'
{
  "identifier": "user@contoso.com",
  "principalType": "User",
  "datasetUserAccessRight": "Read"
}
EOF
az rest --method post \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/users" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json

# Update existing user permissions
cat > /tmp/body.json << 'EOF'
{
  "identifier": "user@contoso.com",
  "principalType": "User",
  "datasetUserAccessRight": "ReadReshare"
}
EOF
az rest --method put \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/users" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json
```

Available permission levels: `Read`, `ReadReshare`, `ReadExplore`, `ReadReshareExplore`, `ReadWrite`, `ReadWriteReshare`, `ReadWriteExplore`, `ReadWriteReshareExplore`, `None`.

---

## Execute DAX Queries (Power BI Datasets API)

Run read-only DAX queries (`EVALUATE`) against a semantic model and get results inline. Useful for validating measures, inspecting data, and post-creation testing.

```bash
# Execute a DAX query
cat > /tmp/body.json << 'EOF'
{
  "queries": [
    {"query": "EVALUATE TOPN(10, 'Customer', 'Customer'[CustomerKey], ASC)"}
  ],
  "serializerSettings": {"includeNulls": true}
}
EOF
az rest --method post \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/executeQueries" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json

# Execute under a specific user's RLS context (required for service principal callers when RLS is defined)
cat > /tmp/body.json << 'EOF'
{
  "queries": [
    {"query": "EVALUATE SUMMARIZECOLUMNS('Date'[Year], \"Total Sales\", [Total Sales])"}
  ],
  "impersonatedUserName": "user@contoso.com",
  "serializerSettings": {"includeNulls": true}
}
EOF
az rest --method post \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID/executeQueries" \
  --headers "Content-Type=application/json" \
  --body @/tmp/body.json
```

> **Limits**: DAX only (no MDX/DMV), 1 query per request, max 100,000 rows / 1,000,000 values / 15 MB response, 120 requests per user per minute. Caller needs Build permission on the dataset. Not supported on PUSH datasets, Excel live-connected datasets, or data sources with SSO enabled.

---

## Properties Retrieval

Semantic model properties are spread across **three API surfaces** due to gaps in the Fabric API. This section maps each property category to the correct retrieval method.

### Operational Metadata (Owner, Storage Mode, Scale-Out)

These properties are **only available** via the Power BI Datasets API:

```bash
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/$MODEL_ID"
```

| Property                           | Description                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| `configuredBy`                     | Owner / last configured by (user principal name)                                     |
| `createdDate`                      | ISO 8601 creation timestamp                                                          |
| `targetStorageMode`                | `Abf` (Direct Lake), `PremiumFiles` (Import on Fabric), `Import`                     |
| `isRefreshable`                    | Whether the model supports refresh (always `false` for DirectQuery/LiveConnection)   |
| `isEffectiveIdentityRequired`      | RLS requires effective identity in embed scenarios                                   |
| `isEffectiveIdentityRolesRequired` | RLS roles must be specified                                                          |
| `isOnPremGatewayRequired`          | On-premises gateway needed for data sources                                          |
| `isInPlaceSharingEnabled`          | Whether the dataset can be shared with external users to consume in their own tenant |
| `addRowsAPIEnabled`                | Push dataset rows API enabled                                                        |
| `queryScaleOutSettings`            | Object: `maxReadOnlyReplicas` (0–64, -1 = auto), `autoSyncReadOnlyReplicas` (bool)   |
| `upstreamDataflows`                | Array of dependent dataflow references (`groupId`, `targetDataflowId`)               |
| `description`                      | Dataset description (also available via Fabric Items API)                            |
| `webUrl`                           | Browser URL to the dataset                                                           |
| `createReportEmbedURL`             | URL for report creation embedding                                                    |
| `qnaEmbedURL`                      | URL for Q&A embedding                                                                |

> **Note**: Callers with only Read permission receive a limited response (`id` and `name` only). Write permission on the dataset is required to get the full property set.

### Refresh History Response Properties

Each refresh entry returned by `GET .../refreshes` (see [Refresh Operations](#3-refresh-operations-power-bi-datasets-api)) contains:

| Property                | Description                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| `requestId`             | Unique request identifier                                            |
| `id`                    | Refresh ID (use for cancel or detail queries)                        |
| `refreshType`           | `ViaEnhancedApi`, `Scheduled`, `OnDemand`, `ViaXmlaEndpoint`         |
| `startTime` / `endTime` | ISO 8601 timestamps                                                  |
| `status`                | `Completed`, `Failed`, `Unknown`, `Disabled`           |
| `extendedStatus`        | Additional status detail                                             |
| `serviceExceptionJson`  | Error details when failed (includes `errorCode`, `errorDescription`) |
| `refreshAttempts[]`     | Per-attempt details with individual start/end times                  |

### Data Source Response Properties

Each entry returned by `GET .../datasources` contains:

| Property            | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `datasourceType`    | e.g., `AzureDataLakeStorage`, `Sql`, `AnalysisServices` |
| `connectionDetails` | Object with `server`, `database`, or `path`             |
| `datasourceId`      | Data source unique identifier                           |
| `gatewayId`         | Associated gateway (if on-premises)                     |

For Direct Lake models, the M expression in the TMDL definition reveals the source Lakehouse/Warehouse connection path. See [tmdl-guidelines.md](./tmdl-guidelines.md).

### DirectQuery / LiveConnection Refresh Schedule Properties

Returned by `GET .../directQueryRefreshSchedule`:

| Property          | Description                                                           |
| ----------------- | --------------------------------------------------------------------- |
| `frequency`       | Interval in minutes between refreshes: `15`, `30`, `60`, `120`, `180` |
| `days[]`          | Days to execute (used with `times` instead of `frequency`)            |
| `times[]`         | Times of day to execute (used with `days` instead of `frequency`)     |
| `localTimeZoneId` | Time zone ID                                                          |

> The schedule uses **either** `frequency` (automatic interval) **or** `days` + `times` (fixed schedule), not both.

### Upstream Dataflow Links

Returns dataflow dependencies for all datasets in a workspace (not per-dataset):

```bash
az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/datasets/upstreamDataflows"
```

| Property            | Description                           |
| ------------------- | ------------------------------------- |
| `datasetObjectId`   | The dataset ID                        |
| `dataflowObjectId`  | The upstream dataflow ID              |
| `workspaceObjectId` | The workspace containing the dataflow |

### Per-Table Storage Mode

The model-level `targetStorageMode` (above) gives the overall mode. For per-table detail, inspect partition definitions in the TMDL:

```bash
# After retrieving TMDL via getDefinition (see Get/Download Definition):
echo "$RESULT" | jq -r '.definition.parts[] | select(.path | startswith("definition/tables/")) | .payload' | base64 -d | grep -i "mode:"
```

Values: `directLake`, `import`, `directQuery`

### Schema Properties (Tables, Columns, Measures, Relationships, Expressions)

Retrieved by decoding the corresponding TMDL parts from `getDefinition` (see [Get/Download Definition](#getdownload-definition)):

| Property Category           | TMDL Part                                |
| --------------------------- | ---------------------------------------- |
| Tables, Columns, Measures   | `definition/tables/*.tmdl`               |
| Relationships               | `definition/relationships.tmdl`          |
| M Expressions / Connections | `definition/expressions*` parts          |
| Name, Compatibility Level   | `definition/database.tmdl`, `model.tmdl` |

---


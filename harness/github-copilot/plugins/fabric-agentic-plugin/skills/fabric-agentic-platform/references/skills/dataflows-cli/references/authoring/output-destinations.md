# Output Destinations

Guide for programmatically creating a Dataflow Gen2 with an **output destination** that writes query results to external storage via `az rest` against the Fabric REST API.

## Supported Destinations

| Destination | Connection Kind | M Function | Output Kind |
|---|---|---|---|
| Lakehouse Table | `Lakehouse` | `Lakehouse.Contents(...)` | Table |
| Lakehouse Files | `Lakehouse` | `Lakehouse.Contents(...)` | File |
| Warehouse | `Warehouse` | `Fabric.Warehouse(...)` | Table |
| Azure Data Explorer | `AzureDataExplorer` | `AzureDataExplorer.Contents(...)` | Table |
| Azure SQL | `Sql` | `Sql.Database(...)` | Table |

> **Relative references (`workspaceId = "."`, `warehouseName`) do NOT work for API-created dataflows.** These are MCP-tool/UI-only features. Always use GUID-based navigation (`workspaceId`, `warehouseId`, `lakehouseId`) when building definitions via REST API.

## Table of Contents

| Section | Notes |
|---|---|
| [Concept: Output Destination Anatomy](#concept-output-destination-anatomy) | Two-query pattern, annotation structure |
| [Required M Components](#required-m-components) | `DataDestinations` annotation + hidden destination query |
| [queryMetadata.json Requirements](#querymetadatajson-requirements) | `loadEnabled` rules for source vs destination queries |
| [Output Destination Steps](#output-destination-steps-added-to-standard-authoring-workflow) | OD-specific steps layered on authoring workflow |
| [Destination Type: Lakehouse Table](#destination-type-lakehouse) | Lakehouse table M pattern and connection binding |
| [Destination Type: Lakehouse Files](#destination-type-lakehouse-files) | CSV/Parquet file output to Lakehouse Files |
| [Destination Type: Warehouse](#destination-type-warehouse) | Fabric Warehouse M pattern and connection binding |
| [Destination Type: Azure Data Explorer](#destination-type-azure-data-explorer) | ADX/Kusto M pattern and connection binding |
| [Destination Type: Azure SQL](#destination-type-azure-sql) | SQL Server M pattern |
| [Why ApplyChangesIfNeeded Is Required](#why-applychangesifneeded-is-required) | Draft state reconciliation |
| [Key Details](#key-details) | Naming conventions, flags, target table behavior |
| [Complete Example: Blank Table to Lakehouse](#complete-example-blank-table-to-lakehouse) | Full PowerShell recipe |
| [Complete Example: Blank Table to Warehouse](#complete-example-blank-table-to-warehouse) | Full PowerShell recipe |
| [Complete Example: Blank Table to ADX](#complete-example-blank-table-to-adx) | Full PowerShell recipe |
| [Connection Creation Limitations](#connection-creation-limitations) | OAuth2 connections require portal |
| [Troubleshooting](#troubleshooting) | Common OD-specific errors |

---

## Concept: Output Destination Anatomy

An output destination in Dataflow Gen2 consists of **two queries** working together:

1. **Source query** — produces the data (e.g., `BlankTable`, `SalesData`). Carries a `[DataDestinations]` annotation pointing to the destination query.
2. **Hidden destination query** — navigates to the target storage location (Lakehouse, ADX, SQL, etc.). Named with the `_DataDestination` suffix convention.

The Fabric refresh engine reads the annotation, evaluates the source query, and writes the result to the location specified by the destination query.

---

## Required M Components

### 1. DataDestinations Annotation

Place immediately **before** the source query's `shared` declaration:

```m
[DataDestinations = {[
  Definition = [Kind = "Reference", QueryName = "MyQuery_DataDestination", IsNewTarget = true],
  Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]
]}]
shared MyQuery = let
    // source query logic
in
    Result;
```

| Field | Value | Notes |
|---|---|---|
| `Kind` (Definition) | `"Reference"` | Always "Reference" for query-based destinations |
| `QueryName` | `"<SourceQuery>_DataDestination"` | Must match the hidden destination query name exactly |
| `IsNewTarget` | `true` | **Always use `true` for API-created dataflows** — even for existing tables (see [Key Details](#key-details)) |
| `Kind` (Settings) | `"Automatic"` | Automatic column mapping; avoids `DestinationColumnNotFound` on new tables |
| `TypeSettings.Kind` | `"Table"` or `"File"` | `"Table"` for table destinations, `"File"` for file destinations (Lakehouse Files, ADLS) |

### 2. Hidden Destination Query

Must use `?` null-safe operators — the table does not exist on first refresh, so direct `[Data]` navigation fails with "The key didn't match any rows in the table."

```m
shared MyQuery_DataDestination = let
    Pattern = Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false]),
    Navigation_1 = Pattern{[workspaceId = "<workspace-id>"]}[Data],
    Navigation_2 = Navigation_1{[lakehouseId = "<lakehouse-id>"]}[Data],
    TableNavigation = Navigation_2{[Id = "MyQuery", ItemKind = "Table"]}?[Data]?
in
    TableNavigation;
```

| Element | Requirement |
|---|---|
| `_DataDestination` suffix | Required naming convention |
| `EnableFolding = false` | Required in destination query pattern |
| `?[Data]?` null-safe operators | Required — table may not exist yet |
| `Id` field value | Must match the source query name (becomes the table name) |

### 3. Complete Section Document

```m
section Section1;

[DataDestinations = {[
  Definition = [Kind = "Reference", QueryName = "MyQuery_DataDestination", IsNewTarget = true],
  Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]
]}]
shared MyQuery = let
    Source = #table({"Col1", "Col2"}, {{"A", "B"}}),
    Typed = Table.TransformColumnTypes(Source, {{"Col1", type text}, {"Col2", type text}})
in
    Typed;

shared MyQuery_DataDestination = let
    Pattern = Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false]),
    Navigation_1 = Pattern{[workspaceId = "<workspace-id>"]}[Data],
    Navigation_2 = Navigation_1{[lakehouseId = "<lakehouse-id>"]}[Data],
    TableNavigation = Navigation_2{[Id = "MyQuery", ItemKind = "Table"]}?[Data]?
in
    TableNavigation;
```

---

## queryMetadata.json Requirements

The `queriesMetadata` section must satisfy these rules for output destinations:

| Query | `loadEnabled` | `isHidden` | `queryName` |
|---|---|---|---|
| Source query (e.g., `BlankTable`) | `true` (or omit — it is the default) | omit | Required |
| Destination query (e.g., `BlankTable_DataDestination`) | **`false`** (mandatory) | `true` | Required |

**Critical:** The destination query **must** have `"loadEnabled": false`. Without it, refresh fails with:
> `ModelBuilderOutputDestinationInvalidOutputDestinationConfiguration: Destination query should have loadEnabled set to false.`

Example `queryMetadata.json`:

```json
{
  "formatVersion": "202502",
  "computeEngineSettings": {},
  "name": "<dataflow-display-name>",
  "allowNativeQueries": false,
  "queriesMetadata": {
    "BlankTable": {
      "queryName": "BlankTable",
      "queryId": "<guid>",
      "loadEnabled": true
    },
    "BlankTable_DataDestination": {
      "queryName": "BlankTable_DataDestination",
      "queryId": "<guid>",
      "isHidden": true,
      "loadEnabled": false
    }
  },
  "connections": [
    {
      "connectionId": "{\"ClusterId\": \"<cluster-guid>\", \"DatasourceId\": \"<connection-guid>\"}",
      "kind": "Lakehouse",
      "path": "Lakehouse"
    }
  ]
}
```

> **Note:** The server may strip `loadEnabled: true` from the source query on round-trip (it is the default). Its absence on read-back is not a bug. However, `loadEnabled: false` on the destination query **is preserved and required**.

> **Multi-connection dataflows:** If your source query also uses a credentialed connector (e.g., reading from a SQL database and writing to a Lakehouse), the `connections[]` array must include **both** the source connection and the destination connection. Missing either causes credential resolution failures at refresh time.

---

## Output Destination Steps (added to standard authoring workflow)

These are the **additional steps** specific to output destinations, layered on top of the standard dataflow authoring workflow (see [SKILL.md § Workflow A](../authoring.md#a-create-a-new-dataflow-end-to-end) for the full create flow).

| Step | Action | API |
|---|---|---|
| 1 | Discover target artifact ID (lakehouse, warehouse, etc.) | `GET /v1/workspaces/{ws}/{itemType}s` |
| 2 | Find the destination connection | `GET /v1/connections` + filter by type |
| 3 | Resolve ClusterId for connection binding | `GET https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources` ⚠️ |

> ⚠️ **Undocumented endpoint:** `gatewayClusterDatasources` is an internal Power BI API (v2.0 is not a public API version). It works in practice but is not in Microsoft's published REST API documentation and may change without notice. There is currently no documented alternative for resolving `ClusterId`.
| 4 | Build mashup with `[DataDestinations]` annotation + hidden `_DataDestination` query | — |
| 5 | Build queryMetadata with `loadEnabled: false` on destination query + connection entry | — |
| 6 | Save complete definition (mashup + queryMetadata + .platform) | `POST .../updateDefinition` |
| 7 | Verify connections survived | `POST .../getDefinition` → decode queryMetadata |
| 8 | Refresh with `ApplyChangesIfNeeded` | `POST .../jobs/instances?jobType=Refresh` |

---

## Destination Type: Lakehouse

### Discovering Lakehouse IDs

Use the Fabric Items API to list lakehouses in a workspace:

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses" \
  --query "value[].{name:displayName, id:id}" -o table
```

### Lakehouse Destination Query Pattern

```m
shared MyQuery_DataDestination = let
    Pattern = Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false]),
    Navigation_1 = Pattern{[workspaceId = "<workspace-id>"]}[Data],
    Navigation_2 = Navigation_1{[lakehouseId = "<lakehouse-id>"]}[Data],
    TableNavigation = Navigation_2{[Id = "MyQuery", ItemKind = "Table"]}?[Data]?
in
    TableNavigation;
```

### Lakehouse Connection Binding

| Field | Value |
|---|---|
| `kind` | `"Lakehouse"` |
| `path` | `"Lakehouse"` |
| Connection type | `Lakehouse` (supports Anonymous-like auto-binding) |
| API-creatable? | Typically pre-exists; reuse via `GET /v1/connections` filter |

---

## Destination Type: Lakehouse Files

Write query results as a CSV or Parquet file to the Lakehouse Files section.

### Key Differences from Lakehouse Table

| Aspect | Table | File |
|---|---|---|
| TypeSettings | `[Kind = "Table"]` | `[Kind = "File"]` |
| Navigation suffix | `?[Data]?` | `?[Content]?` |
| Target navigation | `{[Id = "Name", ItemKind = "Table"]}` | Navigate to Files folder, then `{[Name = "file.csv"]}` |
| IsNewTarget | `true` (always for API) | `true` (always) |

### Lakehouse Files Destination Query Pattern

```m
shared MyQuery_DataDestination = let
    Pattern = Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false]),
    Navigation_1 = Pattern{[workspaceId = "<workspace-id>"]}[Data],
    Navigation_2 = Navigation_1{[lakehouseId = "<lakehouse-id>"]}[Data],
    FilesFolder = Navigation_2{[Id = "Files", ItemKind = "Folder"]}[Data],
    File = FilesFolder{[Name = "MyQuery.csv"]}?[Content]?
in
    File;
```

### DataDestinations Annotation for Files

```m
[DataDestinations = {[
  Definition = [Kind = "Reference", QueryName = "MyQuery_DataDestination", IsNewTarget = true],
  Settings = [Kind = "Automatic", TypeSettings = [Kind = "File"]]
]}]
shared MyQuery = ...
```

> **File format.** The file extension in the navigation step (e.g., `Files{[Name = "MyQuery.csv"]}`) determines the output format. Use `.csv` for CSV and `.parquet` for Parquet.

### Lakehouse Files Connection Binding

Same as Lakehouse Table — use the same Lakehouse connection:

| Field | Value |
|---|---|
| `kind` | `"Lakehouse"` |
| `path` | `"Lakehouse"` |

---

## Destination Type: Warehouse

Write query results to a Fabric Warehouse table.

### Discovering Warehouse IDs

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/warehouses" \
  --query "value[].{name:displayName, id:id}" -o table
```

### Warehouse Destination Query Pattern

```m
shared MyQuery_DataDestination = let
    Source = Fabric.Warehouse([HierarchicalNavigation = false, CreateNavigationProperties = false]),
    Workspace = Source{[workspaceId = "<workspace-id>"]}[Data],
    Warehouse = Workspace{[warehouseId = "<warehouse-id>"]}[Data],
    Table = Warehouse{[Schema = "dbo", Item = "MyQuery"]}?[Data]?
in
    Table;
```

| Element | Requirement |
|---|---|
| `HierarchicalNavigation = false` | Required — flat navigation with `Schema`/`Item` keys |
| `CreateNavigationProperties = false` | Required option |
| `warehouseId` | GUID of the target warehouse (**not** `warehouseName` — name-based keys fail for API-created dataflows) |
| `Schema` | SQL schema (typically `"dbo"`) |
| `Item` | Target table name — matches source query name |
| `?[Data]?` | Null-safe navigation for new tables |

### Warehouse Connection Binding

| Field | Value |
|---|---|
| `kind` | `"Warehouse"` |
| `path` | `"Warehouse"` |
| Connection type | `Warehouse` (typically OAuth2, pre-created) |
| API-creatable? | Typically pre-exists; reuse via `GET /v1/connections` filter |

### Finding Warehouse Connections

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[?connectionDetails.type=='Warehouse'].{id:id, name:displayName, path:connectionDetails.path}" -o table
```

---

## Destination Type: Azure Data Explorer

### ADX Destination Query Pattern

```m
shared MyQuery_DataDestination = let
    Source = AzureDataExplorer.Contents("<cluster-url>", "<database>", null, [CreateNavigationProperties = false]),
    Table = Source{[Name = "MyQuery"]}?[Data]?
in
    Table;
```

| Element | Requirement |
|---|---|
| Cluster URL | Must match **exactly** the connection's `path` (including trailing slash if present) |
| Database | The target ADX database name |
| `null` third parameter | Required positional placeholder (no table/query filter) |
| `CreateNavigationProperties = false` | Required option |
| `{[Name = "..."]}?[Data]?` | Null-safe navigation; `Name` matches the source query name (becomes the table name) |

### ADX Connection Binding

| Field | Value |
|---|---|
| `kind` | `"AzureDataExplorer"` |
| `path` | The cluster URL — **must match the connection's `connectionDetails.path` exactly** |
| Connection type | `AzureDataExplorer` (supports OAuth2, ServicePrincipal, WorkspaceIdentity) |
| API-creatable? | **OAuth2: No** (requires portal). ServicePrincipal/WorkspaceIdentity: Yes |

> **Critical: Path matching.** The `path` value in `queryMetadata.json connections[]` and the URL in the M code must **exactly match** the connection's `connectionDetails.path`. If the connection was created with a trailing slash (e.g., `https://mycluster.kusto.windows.net/`), the M code must also use the trailing slash. A mismatch causes `ActionUserFailure: Data source credentials are missing or invalid`.

### Finding ADX Connections

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[?connectionDetails.type=='AzureDataExplorer'].{id:id, name:displayName, path:connectionDetails.path}" -o table
```

---

## Destination Type: Azure SQL


### Azure SQL Destination Query Pattern

```m
shared MyQuery_DataDestination = let
    Source = Sql.Database("<server>.database.windows.net", "<database>", [HierarchicalNavigation = false, CreateNavigationProperties = false]),
    Table = Source{[Schema = "dbo", Item = "MyQuery"]}?[Data]?
in
    Table;
```

| Element | Requirement |
|---|---|
| Server | Fully qualified server name (e.g., `myserver.database.windows.net`) |
| Database | Database name |
| `HierarchicalNavigation = false` | Required — uses flat `Schema`/`Item` navigation |
| `Schema` | SQL schema (typically `"dbo"`) |
| `Item` | Target table name |
| `?[Data]?` | Null-safe navigation for new tables |

### Azure SQL Connection Binding

| Field | Value |
|---|---|
| `kind` | `"Sql"` |
| `path` | `"<server>;<database>"` (semicolon-separated, matching connection's registered path) |
| Connection type | `SQL` (supports Basic, OAuth2, ServicePrincipal) |
| API-creatable? | Basic/ServicePrincipal: Yes. OAuth2: No (portal) |

### Finding SQL Connections

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[?connectionDetails.type=='SQL'].{id:id, name:displayName, path:connectionDetails.path, cred:credentialDetails.credentialType}" -o table
```

---

## Why ApplyChangesIfNeeded Is Required

API-created dataflows start in an **unpublished draft state**. The platform reconciles the draft on refresh **only** when using `ApplyChangesIfNeeded`:

| Refresh Option | Behavior on API-created dataflow |
|---|---|
| `SkipApplyChanges` (default) | Instant failure — stale metadata, draft never published |
| `ApplyChangesIfNeeded` | Re-parses M annotations, publishes draft, reconciles metadata, then executes |

After the first successful refresh, subsequent refreshes can use either option.

```json
{"executionData": {"executeOption": "ApplyChangesIfNeeded"}}
```

---

## Key Details

| Element | Requirement |
|---|---|
| `_DataDestination` suffix | Required naming convention for hidden query |
| `EnableFolding = false` | Required in Lakehouse destination query `Lakehouse.Contents()` call |
| `isHidden = true` | Set in queryMetadata for destination queries |
| `loadEnabled = false` | **Mandatory** on destination query in queryMetadata |
| Target table name | Uses source query name (table created on first refresh) |
| `IsNewTarget = true` | **Always for API-created dataflows** — even for existing tables |
| `Settings.Kind = "Automatic"` | Required for new tables (avoids column mapping errors) |
| Connection binding | Required in `queryMetadata.json connections[]` with composite `ClusterId`/`DatasourceId` ID |
| Explicit column types | **Required** — source query must produce typed columns (use `Table.TransformColumnTypes`). Untyped (`Any`) columns cause `unsupported by the destination` errors |

### IsNewTarget = true — Always for API-Created Dataflows

For dataflows created via REST API, **always** use `IsNewTarget = true` with `?[Data]?` null-safe operators — even when targeting an existing table. `IsNewTarget = false` with direct `[Data]` navigation fails on first refresh because the engine cannot resolve the table reference before the annotations are published.

**Behavior when targeting an existing table with `IsNewTarget = true`:**
- The table is dropped and recreated with the new schema on each refresh (replace semantics)
- This is equivalent to `UpdateMethod = [Kind = "Replace"]`

### Writing to an Existing Table (UI-published dataflows only)

The `IsNewTarget = false` pattern with `Settings.Kind = "Manual"` is **only** for dataflows already published through the Fabric UI. Do **not** use this for API-created dataflows.

```m
[DataDestinations = {[
  Definition = [Kind = "Reference", QueryName = "MyQuery_DataDestination", IsNewTarget = false],
  Settings = [
    Kind = "Manual",
    AllowCreation = false,
    DynamicSchema = false,
    UpdateMethod = [Kind = "Replace"],
    TypeSettings = [Kind = "Table"]
  ]
]}]
```

| Setting | `Kind = "Automatic"` | `Kind = "Manual"` |
|---|---|---|
| Mapping | Managed by engine | Explicit `ColumnSettings` required |
| Schema changes | Allowed (table dropped/recreated) | Must match exactly |
| Use case | New tables, flexible schema | Existing tables, preserve relationships |

**Update methods** (for `Manual` mode):
- `[Kind = "Replace"]` — data dropped and replaced each refresh
- `[Kind = "Append"]` — output appended to existing data

> **After first successful refresh**, an API-created dataflow is considered "published". Subsequent definition updates can switch to `IsNewTarget = false` with `Manual` settings if precise control is needed. However, `IsNewTarget = true` with `Automatic` continues to work for all refreshes.

---

## Complete Example: Blank Table to Lakehouse

**Prompt**: "Create a dataflow with a blank table that writes to a Lakehouse destination."

**PowerShell implementation:**

```powershell
# Prerequisites: az login, target workspace and lakehouse must exist.
$WS_ID = "<workspaceId>"
$LH_ID = "<lakehouseId>"
$DF_NAME = "my-od-dataflow"
$RESOURCE = "https://api.fabric.microsoft.com"
$API = "$RESOURCE/v1"
$PBI_RESOURCE = "https://analysis.windows.net/powerbi/api"

# Step 1: Create empty dataflow
$createBody = @{ displayName = $DF_NAME } | ConvertTo-Json
$createFile = "$env:TEMP\df_create.json"
[IO.File]::WriteAllText($createFile, $createBody, [Text.UTF8Encoding]::new($false))
$dfResponse = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows" --body "@$createFile" | ConvertFrom-Json
$DF_ID = $dfResponse.id
Remove-Item $createFile

# Step 2: Find Lakehouse connection
$CONN_ID = az rest --method get --resource $RESOURCE `
  --url "$API/connections" `
  --query "value[?connectionDetails.type=='Lakehouse'] | [0].id" --output tsv

# Step 3: Resolve ClusterId
$CLUSTER_ID = az rest --method get --resource $PBI_RESOURCE `
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" `
  --query "value[?id=='$CONN_ID'] | [0].clusterId" --output tsv

# Step 4: Build definition
$mashupPq = @"
section Section1;

[DataDestinations = {[
  Definition = [Kind = "Reference", QueryName = "BlankTable_DataDestination", IsNewTarget = true],
  Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]
]}]
shared BlankTable = let
    Source = #table({"Column1", "Column2", "Column3"}, {{"Value1", "Value2", "Value3"}}),
    Typed = Table.TransformColumnTypes(Source, {{"Column1", type text}, {"Column2", type text}, {"Column3", type text}})
in
    Typed;

shared BlankTable_DataDestination = let
    Pattern = Lakehouse.Contents([HierarchicalNavigation = null, CreateNavigationProperties = false, EnableFolding = false]),
    Navigation_1 = Pattern{[workspaceId = "$WS_ID"]}[Data],
    Navigation_2 = Navigation_1{[lakehouseId = "$LH_ID"]}[Data],
    TableNavigation = Navigation_2{[Id = "BlankTable", ItemKind = "Table"]}?[Data]?
in
    TableNavigation;
"@

$queryMetadataJson = @"
{
  "formatVersion": "202502",
  "computeEngineSettings": {},
  "name": "$DF_NAME",
  "allowNativeQueries": false,
  "queriesMetadata": {
    "BlankTable": {
      "queryName": "BlankTable",
      "queryId": "$([guid]::NewGuid().ToString())",
      "loadEnabled": true
    },
    "BlankTable_DataDestination": {
      "queryName": "BlankTable_DataDestination",
      "queryId": "$([guid]::NewGuid().ToString())",
      "isHidden": true,
      "loadEnabled": false
    }
  },
  "connections": [
    {
      "connectionId": "{\"ClusterId\": \"$CLUSTER_ID\", \"DatasourceId\": \"$CONN_ID\"}",
      "kind": "Lakehouse",
      "path": "Lakehouse"
    }
  ]
}
"@

# Use existing .platform from the dataflow (preserves logicalId)
$defResult = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" `
  --headers "Content-Length=0" | ConvertFrom-Json
$platformB64 = ($defResult.definition.parts | Where-Object { $_.path -eq ".platform" }).payload

$mashupB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($mashupPq))
$qmB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($queryMetadataJson))

# Step 5: Save definition
$updateBody = @"
{
  "definition": {
    "parts": [
      {"path": "mashup.pq", "payload": "$mashupB64", "payloadType": "InlineBase64"},
      {"path": "queryMetadata.json", "payload": "$qmB64", "payloadType": "InlineBase64"},
      {"path": ".platform", "payload": "$platformB64", "payloadType": "InlineBase64"}
    ]
  }
}
"@
$updateFile = "$env:TEMP\df_update.json"
[IO.File]::WriteAllText($updateFile, $updateBody, [Text.UTF8Encoding]::new($false))
az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition" `
  --headers "Content-Type=application/json" --body "@$updateFile"
Remove-Item $updateFile

# Step 6: Verify connections persisted
$verifyResult = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" `
  --headers "Content-Length=0" | ConvertFrom-Json
$qmVerify = [Text.Encoding]::UTF8.GetString(
  [Convert]::FromBase64String(
    ($verifyResult.definition.parts | Where-Object { $_.path -eq "queryMetadata.json" }).payload
  )) | ConvertFrom-Json
if ($qmVerify.connections.Count -gt 0) { Write-Host "OK: connections persisted." }
else { Write-Error "FAIL: connections missing after updateDefinition." }

# Step 7: Refresh with ApplyChangesIfNeeded
$refreshBody = '{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}'
$refreshFile = "$env:TEMP\df_refresh.json"
[IO.File]::WriteAllText($refreshFile, $refreshBody, [Text.UTF8Encoding]::new($false))
az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances?jobType=Refresh" `
  --body "@$refreshFile"
Remove-Item $refreshFile

Write-Host "Refresh triggered. Table 'BlankTable' will be created in lakehouse $LH_ID."
```

---

## Complete Example: Blank Table to Warehouse

**Prompt**: "Create a dataflow with a blank table that writes to a Fabric Warehouse destination."

**PowerShell implementation:**

```powershell
# Prerequisites: az login, target workspace and warehouse must exist.
$WS_ID = "<workspaceId>"
$WH_ID = "<warehouseId>"
$DF_NAME = "my-warehouse-od-dataflow"
$RESOURCE = "https://api.fabric.microsoft.com"
$API = "$RESOURCE/v1"
$PBI_RESOURCE = "https://analysis.windows.net/powerbi/api"

# Step 1: Create empty dataflow
$createBody = @{ displayName = $DF_NAME } | ConvertTo-Json
$createFile = "$env:TEMP\df_create.json"
[IO.File]::WriteAllText($createFile, $createBody, [Text.UTF8Encoding]::new($false))
$dfResponse = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows" --body "@$createFile" | ConvertFrom-Json
$DF_ID = $dfResponse.id
Remove-Item $createFile

# Step 2: Find Warehouse connection
$WH_CONN_ID = az rest --method get --resource $RESOURCE `
  --url "$API/connections" `
  --query "value[?connectionDetails.type=='Warehouse'] | [0].id" --output tsv

# Step 3: Resolve ClusterId
$CLUSTER_ID = az rest --method get --resource $PBI_RESOURCE `
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" `
  --query "value[?id=='$WH_CONN_ID'] | [0].clusterId" --output tsv

# Step 4: Build definition
$mashupPq = @"
section Section1;

[DataDestinations = {[
  Definition = [Kind = "Reference", QueryName = "BlankTable_DataDestination", IsNewTarget = true],
  Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]
]}]
shared BlankTable = let
    Source = #table({"Column1", "Column2", "Column3"}, {{"Value1", "Value2", "Value3"}}),
    Typed = Table.TransformColumnTypes(Source, {{"Column1", type text}, {"Column2", type text}, {"Column3", type text}})
in
    Typed;

shared BlankTable_DataDestination = let
    Source = Fabric.Warehouse([HierarchicalNavigation = false, CreateNavigationProperties = false]),
    Workspace = Source{[workspaceId = "$WS_ID"]}[Data],
    Warehouse = Workspace{[warehouseId = "$WH_ID"]}[Data],
    Table = Warehouse{[Schema = "dbo", Item = "BlankTable"]}?[Data]?
in
    Table;
"@

$q1Id = [guid]::NewGuid().ToString()
$q2Id = [guid]::NewGuid().ToString()
$queryMetadataJson = @"
{
  "formatVersion": "202502",
  "computeEngineSettings": {},
  "name": "$DF_NAME",
  "allowNativeQueries": false,
  "queriesMetadata": {
    "BlankTable": {
      "queryName": "BlankTable",
      "queryId": "$q1Id",
      "loadEnabled": true
    },
    "BlankTable_DataDestination": {
      "queryName": "BlankTable_DataDestination",
      "queryId": "$q2Id",
      "isHidden": true,
      "loadEnabled": false
    }
  },
  "connections": [
    {
      "connectionId": "{\"ClusterId\": \"$CLUSTER_ID\", \"DatasourceId\": \"$WH_CONN_ID\"}",
      "kind": "Warehouse",
      "path": "Warehouse"
    }
  ]
}
"@

# Get existing .platform
$defResult = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" `
  --headers "Content-Length=0" | ConvertFrom-Json
$platformB64 = ($defResult.definition.parts | Where-Object { $_.path -eq ".platform" }).payload

$mashupB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($mashupPq))
$qmB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($queryMetadataJson))

# Step 5: Save definition
$updateBody = @"
{
  "definition": {
    "parts": [
      {"path": "mashup.pq", "payload": "$mashupB64", "payloadType": "InlineBase64"},
      {"path": "queryMetadata.json", "payload": "$qmB64", "payloadType": "InlineBase64"},
      {"path": ".platform", "payload": "$platformB64", "payloadType": "InlineBase64"}
    ]
  }
}
"@
$updateFile = "$env:TEMP\df_update.json"
[IO.File]::WriteAllText($updateFile, $updateBody, [Text.UTF8Encoding]::new($false))
az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition" `
  --headers "Content-Type=application/json" --body "@$updateFile"
Remove-Item $updateFile

# Step 6: Verify connections persisted
$verifyResult = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" `
  --headers "Content-Length=0" | ConvertFrom-Json
$qmVerify = [Text.Encoding]::UTF8.GetString(
  [Convert]::FromBase64String(
    ($verifyResult.definition.parts | Where-Object { $_.path -eq "queryMetadata.json" }).payload
  )) | ConvertFrom-Json
if ($qmVerify.connections.Count -gt 0) { Write-Host "OK: connections persisted." }
else { Write-Error "FAIL: connections missing after updateDefinition." }

# Step 7: Refresh with ApplyChangesIfNeeded
$refreshBody = '{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}'
$refreshFile = "$env:TEMP\df_refresh.json"
[IO.File]::WriteAllText($refreshFile, $refreshBody, [Text.UTF8Encoding]::new($false))
az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances?jobType=Refresh" `
  --body "@$refreshFile"
Remove-Item $refreshFile

Write-Host "Refresh triggered. Table 'BlankTable' will be created in warehouse $WH_ID (schema: dbo)."
```

---

## Complete Example: Blank Table to ADX

**Prompt**: "Create a dataflow with a blank table that writes to an Azure Data Explorer destination."

**Prerequisites:** An ADX connection must already exist (OAuth2 connections require portal creation). The ADX database must be writable.

**PowerShell implementation:**

```powershell
# Prerequisites: az login, ADX connection pre-created in portal, database writable.
$WS_ID = "<workspaceId>"
$ADX_CLUSTER = "https://mycluster.northeurope.kusto.windows.net/"  # Must match connection path EXACTLY
$ADX_DB = "MyDatabase"
$DF_NAME = "my-adx-od-dataflow"
$RESOURCE = "https://api.fabric.microsoft.com"
$API = "$RESOURCE/v1"
$PBI_RESOURCE = "https://analysis.windows.net/powerbi/api"

# Step 1: Create empty dataflow
$createBody = @{ displayName = $DF_NAME } | ConvertTo-Json
$createFile = "$env:TEMP\df_create.json"
[IO.File]::WriteAllText($createFile, $createBody, [Text.UTF8Encoding]::new($false))
$dfResponse = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows" --body "@$createFile" | ConvertFrom-Json
$DF_ID = $dfResponse.id
Remove-Item $createFile

# Step 2: Find existing ADX connection (must be pre-created in portal for OAuth2)
$ADX_CONN_ID = az rest --method get --resource $RESOURCE `
  --url "$API/connections" `
  --query "value[?connectionDetails.type=='AzureDataExplorer' && contains(connectionDetails.path, 'mycluster')] | [0].id" --output tsv

# Step 3: Resolve ClusterId
$ADX_CLUSTER_ID = az rest --method get --resource $PBI_RESOURCE `
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" `
  --query "value[?id=='$ADX_CONN_ID'] | [0].clusterId" --output tsv

# Step 4: Build definition
$mashupPq = @"
section Section1;

[DataDestinations = {[
  Definition = [Kind = "Reference", QueryName = "BlankTable_DataDestination", IsNewTarget = true],
  Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]
]}]
shared BlankTable = let
    Source = #table({"Name", "Value", "Timestamp"}, {{"TestRow", "123", "2024-01-01"}}),
    Typed = Table.TransformColumnTypes(Source, {{"Name", type text}, {"Value", type text}, {"Timestamp", type text}})
in
    Typed;

shared BlankTable_DataDestination = let
    Source = AzureDataExplorer.Contents("$ADX_CLUSTER", "$ADX_DB", null, [CreateNavigationProperties = false]),
    Table = Source{[Name = "BlankTable"]}?[Data]?
in
    Table;
"@

$queryMetadataJson = @"
{
  "formatVersion": "202502",
  "computeEngineSettings": {},
  "name": "$DF_NAME",
  "allowNativeQueries": false,
  "queriesMetadata": {
    "BlankTable": {
      "queryName": "BlankTable",
      "queryId": "$([guid]::NewGuid().ToString())",
      "loadEnabled": true
    },
    "BlankTable_DataDestination": {
      "queryName": "BlankTable_DataDestination",
      "queryId": "$([guid]::NewGuid().ToString())",
      "isHidden": true,
      "loadEnabled": false
    }
  },
  "connections": [
    {
      "connectionId": "{\"ClusterId\": \"$ADX_CLUSTER_ID\", \"DatasourceId\": \"$ADX_CONN_ID\"}",
      "kind": "AzureDataExplorer",
      "path": "$ADX_CLUSTER"
    }
  ]
}
"@

# Get existing .platform
$defResult = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" `
  --headers "Content-Length=0" | ConvertFrom-Json
$platformB64 = ($defResult.definition.parts | Where-Object { $_.path -eq ".platform" }).payload

$mashupB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($mashupPq))
$qmB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($queryMetadataJson))

# Step 5: Save definition
$updateBody = @"
{
  "definition": {
    "parts": [
      {"path": "mashup.pq", "payload": "$mashupB64", "payloadType": "InlineBase64"},
      {"path": "queryMetadata.json", "payload": "$qmB64", "payloadType": "InlineBase64"},
      {"path": ".platform", "payload": "$platformB64", "payloadType": "InlineBase64"}
    ]
  }
}
"@
$updateFile = "$env:TEMP\df_update.json"
[IO.File]::WriteAllText($updateFile, $updateBody, [Text.UTF8Encoding]::new($false))
az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition" `
  --headers "Content-Type=application/json" --body "@$updateFile"
Remove-Item $updateFile

# Step 6: Verify connections persisted
$verifyResult = az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" `
  --headers "Content-Length=0" | ConvertFrom-Json
$qmVerify = [Text.Encoding]::UTF8.GetString(
  [Convert]::FromBase64String(
    ($verifyResult.definition.parts | Where-Object { $_.path -eq "queryMetadata.json" }).payload
  )) | ConvertFrom-Json
if ($qmVerify.connections.Count -gt 0) { Write-Host "OK: connections persisted." }
else { Write-Error "FAIL: connections missing after updateDefinition." }

# Step 7: Refresh with ApplyChangesIfNeeded
$refreshBody = '{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}'
$refreshFile = "$env:TEMP\df_refresh.json"
[IO.File]::WriteAllText($refreshFile, $refreshBody, [Text.UTF8Encoding]::new($false))
az rest --method post --resource $RESOURCE `
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances?jobType=Refresh" `
  --body "@$refreshFile"
Remove-Item $refreshFile

Write-Host "Refresh triggered. Table 'BlankTable' will be created in ADX database $ADX_DB."
```

---

## Connection Creation Limitations

Not all connection types can be created programmatically via `POST /v1/connections`:

| Credential Type | API Creatable? | Notes |
|---|---|---|
| `Anonymous` | ✅ Yes | No user interaction (Web connector) |
| `Key` / `Basic` | ✅ Yes | Credentials passed in body |
| `ServicePrincipal` | ✅ Yes | App ID + secret in body |
| `WorkspaceIdentity` | ✅ Yes | Workspace managed identity |
| **`OAuth2`** | ❌ No | Requires interactive browser consent |

**Implications by destination type:**

| Destination | Connection Type | Supported Credentials | API Path |
|---|---|---|---|
| Lakehouse | `Lakehouse` | OAuth2 | Pre-create in portal, then reuse ID |
| Azure Data Explorer | `AzureDataExplorer` | OAuth2, ServicePrincipal, WorkspaceIdentity | OAuth2: portal. SP/WI: API-creatable |
| Azure SQL | `Sql` | Basic, ServicePrincipal, OAuth2 | Basic/SP: API-creatable. OAuth2: portal |

**Recommended pattern for automation:**
1. Pre-create OAuth2 connections once in the Fabric portal (one-time manual step)
2. List connections via `GET /v1/connections` and filter by type/path
3. Reuse the connection ID in all API-created dataflows

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModelBuilderOutputDestinationInvalidOutputDestinationConfiguration: Destination query should have loadEnabled set to false` | Destination query missing `loadEnabled: false` in queryMetadata | Add `"loadEnabled": false` to the `_DataDestination` entry in `queriesMetadata` |
| `DestinationColumnNotFound` | Using `Settings.Kind = "Manual"` for a new table | Switch to `"Automatic"` — manual mode validates against a table that does not exist yet |
| "The key didn't match any rows in the table" | Destination query uses `[Data]` instead of `?[Data]?` | Add null-safe `?` operators to the final navigation steps |
| Refresh fails with generic "Job instance failed without detail error" | Multiple possible causes: expired OAuth, wrong connection, draft not published | Verify connection via `GET /v1/connections/{id}`; ensure `ApplyChangesIfNeeded`; retry after 30s |
| `IsNewTarget = false` fails on first refresh | API-created dataflow annotations not yet published | Always use `IsNewTarget = true` for API-created dataflows |
| Table not created after successful refresh | Source query `loadEnabled` not set or stripped | Verify source query produces data via `executeQuery` before refresh |
| `Required property 'queryName' not found` on updateDefinition | queryMetadata entries missing `queryName` field | Add `"queryName": "<name>"` to each entry in `queriesMetadata` |
| `A query with a data destination has only columns whose types are not supported by the destination` | Source query produces untyped (`Any`) columns | Add `Table.TransformColumnTypes(Source, {{"Col", type text}, ...})` to cast all columns to supported types (text, Int64.Type, number, logical, datetime, etc.) |
| `ActionUserFailure: Data source credentials are missing or invalid` (error code 999999) | M code URL does not exactly match the connection's registered `path` | Ensure the URL in the M code (including trailing slash) matches `connectionDetails.path` from `GET /v1/connections/{id}` |
| `The CredentialType input is not supported for this API` on `POST /v1/connections` | Attempting to create an OAuth2 connection via API | OAuth2 connections require the Fabric portal (interactive browser consent). Use ServicePrincipal or WorkspaceIdentity for API-creatable connections |
| ADX table not created after refresh success | Table name in destination query `{[Name = "X"]}` does not match source query name | Ensure `Name` value matches the source query's `shared` name exactly |
| `EntityUserFailure` with relative references (`workspaceId = "."` or `warehouseName`) | Name-based and relative navigation keys not supported for API-created dataflows | Always use GUID-based keys: `workspaceId = "<guid>"`, `warehouseId = "<guid>"`, `lakehouseId = "<guid>"` |
| `EntityUserFailure` on Warehouse/SQL destination | Stale connection credentials or wrong connection type (gateway vs cloud) | Verify connection is `ShareableCloud` or `PersonalCloud` type (not `OnPremisesGateway`); check credentials in portal |

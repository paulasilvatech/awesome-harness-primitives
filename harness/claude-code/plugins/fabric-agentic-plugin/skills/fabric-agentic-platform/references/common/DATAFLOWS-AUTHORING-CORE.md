# DATAFLOWS-AUTHORING-CORE.md

> **Scope**: Authoring patterns for **Fabric Dataflows Gen2** — creating, updating, managing dataflow definitions (mashup + metadata), connections, queries, parameters, scheduling, job execution, and CI/CD.
> Language-agnostic — uses Fabric REST API. No C#, Python, CLI, or SDK references.

---

## Authoring Capability Matrix

> **Relationship to other CORE docs**: This document covers Dataflows Gen2 authoring via the Fabric REST API — creating items, managing definitions, running jobs, and CI/CD. For downstream consumption of dataflow outputs (Lakehouse tables, Warehouse staging), see `SQLDW-AUTHORING-CORE.md` or `SPARK-CONSUMPTION-CORE.md`.

| Capability | Dataflow Gen2 |
|---|---|
| Create Dataflow | ✅ |
| Update Definition (mashup + metadata) | ✅ |
| Delete Dataflow | ✅ |
| Discover Parameters | ✅ |
| Run Job (Execute / Refresh) | ✅ |
| Run Job with Parameters | ✅ |
| Get / Update Definition (LRO) | ✅ |
| ALM / Git Integration | ✅ |
| Schedule Refresh | ✅ |
| Sensitivity Labels | ✅ |

**Summary**: Dataflows Gen2 supports full CRUD lifecycle, parameterized refresh, Git-based CI/CD, and scheduled execution — all accessible through the Fabric REST API.

---

## Dataflow Definition Structure

A Dataflow Gen2 definition consists of **3 parts**, each base64-encoded when sent via the REST API.

### queryMetadata.json

Contains dataflow metadata, query declarations, connection references, and engine settings.

```json
{
  "formatVersion": "202502",
  "computeEngineSettings": {
    "allowFastCopy": true,
    "maxConcurrency": 1
  },
  "name": "MyDataflow",
  "queryGroups": [],
  "documentLocale": "en-US",
  "queriesMetadata": {
    "QueryName": {
      "queryId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "queryName": "QueryName",
      "loadEnabled": true,
      "isHidden": false
    }
  },
  "connections": [
    {
      "path": "Lakehouse",
      "kind": "Lakehouse",
      "connectionId": "00000000-0000-0000-0000-000000000000"
    }
  ],
  "fastCombine": false,
  "allowNativeQueries": true,
  "parametric": false
}
```

**Key fields**:
- `formatVersion` — must be `"202502"` (current required version).
- `computeEngineSettings.allowFastCopy` — enables the fast copy engine for high-throughput ingestion.
- `queriesMetadata` — one entry per query; `loadEnabled: true` means the query writes output on refresh.
- `connections` — declares data source connections used by queries (must already exist in user's Fabric connection store).
- `parametric` — set to `true` when the dataflow exposes parameters.

### mashup.pq (Power Query M Section Document)

Contains the actual Power Query M code — one section with all queries.

```powerquery
[StagingDefinition = [Kind = "FastCopy"]]
section Section1;

shared MyQuery = let
    Source = Lakehouse.Contents([]),
    Nav1 = Source{[workspaceId = "your-workspace-id"]}[Data],
    Nav2 = Nav1{[lakehouseId = "your-lakehouse-id"]}[Data],
    Nav3 = Nav2{[Id = "tableName", ItemKind = "Table"]}[Data]
in
    Nav3;
```

**Structure rules**:
- The file is a **section document**: `section Section1;` followed by `shared` query declarations.
- Each query is declared as `shared QueryName = let ... in ...;`.
- The `[StagingDefinition = [Kind = "FastCopy"]]` annotation on the section enables fast copy mode.
- Multiple queries appear as separate `shared` declarations within the same section.
- Queries can reference other queries by name within the section.

### .platform (Item Metadata)

Standard Fabric item metadata file.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Dataflow",
    "displayName": "MyDataflow"
  },
  "config": {
    "version": "2.0",
    "logicalId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }
}
```

**Notes**: `type` is always `"Dataflow"` for Dataflows Gen2. The `logicalId` is a stable identifier used for Git integration and cross-environment mapping.

---

## REST API Surface (Authoring)

All endpoints use `https://api.fabric.microsoft.com/v1` as the base URL. Authenticate with an Entra ID Bearer token.

### Create Dataflow

```http
POST /v1/workspaces/{workspaceId}/dataflows
Content-Type: application/json
Authorization: Bearer {token}
```

**Request body** (with definition):

```json
{
  "displayName": "SalesDataflow",
  "description": "Loads sales data from Lakehouse to staging",
  "definition": {
    "parts": [
      {
        "path": "queryMetadata.json",
        "payload": "<base64-encoded-queryMetadata>",
        "payloadType": "InlineBase64"
      },
      {
        "path": "mashup.pq",
        "payload": "<base64-encoded-mashup>",
        "payloadType": "InlineBase64"
      },
      {
        "path": ".platform",
        "payload": "<base64-encoded-platform>",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

**Request body** (without definition — empty dataflow):

```json
{
  "displayName": "SalesDataflow",
  "description": "Placeholder dataflow"
}
```

| Aspect | Detail |
|---|---|
| Response (simple, no definition) | `201 Created` with item metadata |
| Response (with definition) | `202 Accepted` — LRO; poll via `Location` header |
| Permission | Contributor workspace role |
| Required Scopes | `Dataflow.ReadWrite.All` or `Item.ReadWrite.All` |

### Get Definition (LRO)

```http
POST /v1/workspaces/{workspaceId}/dataflows/{dataflowId}/getDefinition
Authorization: Bearer {token}
```

| Aspect | Detail |
|---|---|
| Response | `200 OK` with definition parts, **or** `202 Accepted` (LRO — poll via `Location` header) |
| Permission | Read + Write on the item |
| Required Scopes | `Dataflow.ReadWrite.All` or `Item.ReadWrite.All` |

**Response body** (200 OK):

```json
{
  "definition": {
    "parts": [
      { "path": "queryMetadata.json", "payload": "<base64>", "payloadType": "InlineBase64" },
      { "path": "mashup.pq", "payload": "<base64>", "payloadType": "InlineBase64" },
      { "path": ".platform", "payload": "<base64>", "payloadType": "InlineBase64" }
    ]
  }
}
```

**Important**: `getDefinition` is a **POST** request, not GET — it follows the Fabric LRO pattern.

### Update Definition (LRO)

```http
POST /v1/workspaces/{workspaceId}/dataflows/{dataflowId}/updateDefinition?updateMetadata=true
Content-Type: application/json
Authorization: Bearer {token}
```

**Request body**:

```json
{
  "definition": {
    "parts": [
      {
        "path": "queryMetadata.json",
        "payload": "<base64-encoded-queryMetadata>",
        "payloadType": "InlineBase64"
      },
      {
        "path": "mashup.pq",
        "payload": "<base64-encoded-mashup>",
        "payloadType": "InlineBase64"
      },
      {
        "path": ".platform",
        "payload": "<base64-encoded-platform>",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

| Aspect | Detail |
|---|---|
| Response | `200 OK` or `202 Accepted` (LRO — poll via `Location` header) |
| Query parameter | `?updateMetadata=true` to also update `.platform` metadata (display name, etc.) |
| Permission | Contributor workspace role |

**Critical**: `updateDefinition` requires **all 3 parts** — it replaces the entire definition, not individual parts. Always `getDefinition` first, modify the needed parts, then send back all 3.

### Update Dataflow (Properties Only)

```http
PATCH /v1/workspaces/{workspaceId}/dataflows/{dataflowId}
Content-Type: application/json
Authorization: Bearer {token}
```

**Request body**:

```json
{
  "displayName": "RenamedDataflow",
  "description": "Updated description"
}
```

| Aspect | Detail |
|---|---|
| Response | `200 OK` |
| Use case | Rename or update description without modifying the definition |

### Delete Dataflow

```http
DELETE /v1/workspaces/{workspaceId}/dataflows/{dataflowId}
Authorization: Bearer {token}
```

| Aspect | Detail |
|---|---|
| Response | `200 OK` |
| Permission | Contributor workspace role |
| Warning | Irreversible — deletes the dataflow and its refresh history |

### Run Job (Execute / Refresh)

```http
POST /v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/Execute/instances
Content-Type: application/json
Authorization: Bearer {token}
```

**Request body** (with execution options and parameters):

```json
{
  "executionData": {
    "executeOption": "ApplyChangesIfNeeded"
  },
  "parameters": [
    {
      "name": "Threshold",
      "value": "start",
      "type": "Automatic"
    }
  ]
}
```

**Request body** (simple refresh — no body needed):

```http
POST /v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/Execute/instances
```

| Aspect | Detail |
|---|---|
| Response | `202 Accepted` with `Location` header for polling |
| Permission | Contributor workspace role |
| executionData.executeOption | `ApplyChangesIfNeeded` (standard) |
| parameters | Optional — override dataflow parameter defaults at runtime |

---

## Power Query M Code Structure

### Section Document Format

All Dataflow Gen2 mashup code uses the **section document** format:

```powerquery
section Section1;

shared QueryName = let
    Step1 = ...,
    Step2 = ...
in
    Step2;
```

- The `section Section1;` header is required.
- Every query is declared with `shared` and terminated with `;`.

### Multiple Queries

```powerquery
section Section1;

shared Customers = let
    Source = Sql.Database("server.database.windows.net", "mydb"),
    Data = Source{[Schema = "dbo", Item = "Customers"]}[Data]
in
    Data;

shared Orders = let
    Source = Sql.Database("server.database.windows.net", "mydb"),
    Data = Source{[Schema = "dbo", Item = "Orders"]}[Data],
    Filtered = Table.SelectRows(Data, each [Status] = "Active")
in
    Filtered;

shared CustomerOrders = let
    Merged = Table.NestedJoin(Customers, {"CustomerID"}, Orders, {"CustomerID"}, "OrderData", JoinKind.Inner),
    Expanded = Table.ExpandTableColumn(Merged, "OrderData", {"OrderID", "Amount"})
in
    Expanded;
```

Queries can **reference other queries by name** within the section (e.g., `CustomerOrders` references `Customers` and `Orders`).

### StagingDefinition Annotation (Fast Copy)

```powerquery
[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
```

The `[StagingDefinition = [Kind = "FastCopy"]]` annotation placed before the section header enables the **fast copy engine** for high-throughput data movement. Without this annotation, queries use the standard mashup engine.

### Parameters

Parameters are declared as `shared` values with metadata annotations:

```powerquery
section Section1;

shared ServerName = "myserver.database.windows.net" meta [IsParameterQuery = true, Type = "Text"];

shared DatabaseName = "mydb" meta [IsParameterQuery = true, Type = "Text"];

shared StartDate = #date(2025, 1, 1) meta [IsParameterQuery = true, Type = "Date"];

shared MyQuery = let
    Source = Sql.Database(ServerName, DatabaseName),
    Data = Source{[Schema = "dbo", Item = "Sales"]}[Data],
    Filtered = Table.SelectRows(Data, each [SaleDate] >= StartDate)
in
    Filtered;
```

**Parameter types**: `Text`, `True/False`, `Decimal Number`, `Date/Time`, `Date`, `Time`, `Date/Time/Timezone`, `Duration`, `Binary`, `Any`.

Parameters declared in `mashup.pq` must also be present in `queriesMetadata` within `queryMetadata.json`.

---

## Connection Model

### Connection Structure in queryMetadata.json

Connections referenced by queries are declared in the `connections` array:

```json
{
  "connections": [
    {
      "path": "Lakehouse",
      "kind": "Lakehouse",
      "connectionId": "00000000-0000-0000-0000-000000000000"
    },
    {
      "path": "myserver.database.windows.net;mydb",
      "kind": "Sql",
      "connectionId": "11111111-1111-1111-1111-111111111111"
    },
    {
      "path": "https://example.com/api/data",
      "kind": "Web",
      "connectionId": "22222222-2222-2222-2222-222222222222"
    }
  ]
}
```

### Connection Properties

| Property | Description |
|---|---|
| `path` | Identifies the data source endpoint (server, URL, item name) |
| `kind` | Connector type — must match the M function used in the query |
| `connectionId` | GUID referencing an existing connection in the user's Fabric connection store |

### Common Connection Kinds

| Kind | M Function | Path Example |
|---|---|---|
| `Lakehouse` | `Lakehouse.Contents()` | `"Lakehouse"` |
| `Sql` | `Sql.Database()` | `"server.database.windows.net;mydb"` |
| `AzureSqlDatabase` | `AzureSql.Database()` | `"server.database.windows.net;mydb"` |
| `Web` | `Web.Contents()` | `"https://example.com/api"` |
| `SharePoint` | `SharePoint.Contents()` | `"https://tenant.sharepoint.com/sites/mysite"` |
| `AzureDataLakeStorage` | `AzureStorage.DataLake()` | `"https://account.dfs.core.windows.net"` |

**Important**: Connections **must already exist** in the user's Fabric connection store before creating or updating a dataflow that references them. Creating a dataflow with a nonexistent `connectionId` will fail at refresh time.

---

## Job Execution Patterns

### Trigger a Refresh

A "refresh" is an **Execute** job type in the Fabric Items API:

```http
POST /v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/Execute/instances
Authorization: Bearer {token}
```

### LRO Polling Pattern

All job executions return `202 Accepted` with a `Location` header pointing to the operation status endpoint:

```
Location: https://api.fabric.microsoft.com/v1/operations/{operationId}
Retry-After: 30
```

**Poll the operation**:

```http
GET /v1/operations/{operationId}
Authorization: Bearer {token}
```

**Response**:

```json
{
  "id": "operation-id",
  "status": "Running",
  "createdTimeUtc": "2025-01-15T10:00:00Z",
  "lastUpdatedTimeUtc": "2025-01-15T10:01:00Z",
  "percentComplete": 50
}
```

| Status Value | Meaning |
|---|---|
| `NotStarted` | Queued but not yet running |
| `Running` | Currently executing |
| `Succeeded` | Completed successfully |
| `Failed` | Completed with error |
| `Cancelled` | Cancelled by user or system |

**Polling rules**:
- Always use the `Location` header URL — do not construct the operation URL manually.
- Respect `Retry-After` header for polling interval.
- Poll until `status` is a terminal value (`Succeeded`, `Failed`, or `Cancelled`).

### Parameterized Refresh

Override parameter defaults at runtime:

```json
{
  "executionData": {
    "executeOption": "ApplyChangesIfNeeded"
  },
  "parameters": [
    { "name": "ServerName", "value": "prod-server.database.windows.net", "type": "Automatic" },
    { "name": "StartDate", "value": "2025-06-01", "type": "Automatic" }
  ]
}
```

**Parameter types for runtime override**: `String`, `Boolean`, `Integer`, `Number`, `DateTime`, `DateTimeZone`, `Date`, `Time`, `Duration`, `Automatic`. Use `Automatic` to let the engine infer the type from the dataflow parameter definition.

---

## ALM / Git Integration

### Git Repository Structure

When a Dataflow Gen2 is synced to Git, it produces **3 files**:

```
MyDataflow.Dataflow/
├── .platform
├── mashup.pq
└── queryMetadata.json
```

All files are stored in **plain text** (not base64) when in Git. Base64 encoding is only used for the REST API `definition.parts[].payload`.

### Export for Git (getDefinition → Git)

1. Call `POST .../getDefinition` to retrieve the definition.
2. Base64-decode each part's `payload`.
3. Write the decoded content to the corresponding file in Git.

### Import from Git (Git → updateDefinition)

1. Read each file from the Git repository.
2. Base64-encode the file content.
3. Call `POST .../updateDefinition` with all 3 encoded parts.

### CI/CD Pattern

```
┌─────────────┐    getDefinition    ┌──────────┐    git push    ┌──────────┐
│ Source       │ ──────────────────> │ Decode + │ ────────────> │   Git    │
│ Workspace    │                     │ Export   │                │   Repo   │
└─────────────┘                     └──────────┘                └──────────┘
                                                                     │
                                                                     │ git pull
                                                                     ▼
┌─────────────┐    updateDefinition ┌──────────┐    read files  ┌──────────┐
│ Target       │ <───────────────── │ Encode + │ <──────────── │   Git    │
│ Workspace    │                     │ Import   │                │   Repo   │
└─────────────┘                     └──────────┘                └──────────┘
                                         │
                                         │  (optional)
                                         ▼
                              POST .../jobs/Execute/instances
                                    (trigger refresh)
```

**Full CI/CD flow**:
1. `getDefinition` from source workspace → decode base64 parts → commit to Git.
2. Pull from Git → base64-encode parts → `updateDefinition` on target workspace.
3. Optionally trigger a refresh on the target to validate the deployment.

### Cross-Environment Parameter Overrides

For environment-specific configuration (e.g., dev vs. prod server names), modify the `mashup.pq` parameter defaults during the CI/CD pipeline before calling `updateDefinition`:

1. Decode `mashup.pq` from base64.
2. Replace parameter default values (e.g., server name, database name).
3. Re-encode and include in the `updateDefinition` call.

---

## Schedule Refresh

Dataflow Gen2 schedules are managed through the Fabric portal or the Fabric REST API (schedule endpoints on the item). Schedules define recurring refresh cadences.

### Schedule Configuration

| Property | Description | Example |
|---|---|---|
| Frequency | How often the refresh runs | Every 30 minutes, Hourly, Daily |
| Time zone | Time zone for the schedule | UTC, Pacific Standard Time |
| Start / End time | Active window for scheduled refreshes | 06:00 – 22:00 |
| Enabled | Whether the schedule is active | `true` / `false` |

### Schedule via REST API

Schedules are managed using the generic Fabric Item Scheduling API:

```http
GET /v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/Execute/schedules
```

```http
POST /v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/Execute/schedules
Content-Type: application/json
Authorization: Bearer {token}
```

**Note**: Schedule configuration details (cron expressions, time slots) follow the standard Fabric scheduling model documented in the Fabric REST API reference.

---

## Gotchas and Troubleshooting

| # | Issue | Cause | Resolution |
|---|---|---|---|
| 1 | Definition parts must be base64-encoded | REST API expects `payloadType: "InlineBase64"` | Always base64-encode each part's content before sending |
| 2 | `getDefinition` returns 405 Method Not Allowed | Used GET instead of POST | `getDefinition` is a **POST** endpoint (LRO pattern) |
| 3 | `updateDefinition` silently drops queries | Sent only 1 or 2 parts instead of all 3 | Always include all 3 parts (`queryMetadata.json`, `mashup.pq`, `.platform`) — update is a full replacement, not incremental |
| 4 | Refresh fails on newly created dataflow | Connections not bound or data source unreachable | Ensure referenced `connectionId` values exist in user's Fabric connection store before creating the dataflow |
| 5 | `formatVersion` mismatch error | Used an outdated or incorrect `formatVersion` | Set `formatVersion` to `"202502"` in `queryMetadata.json` |
| 6 | Query doesn't write output on refresh | `loadEnabled` is `false` in `queriesMetadata` | Set `loadEnabled: true` for queries that should write to the destination on refresh |
| 7 | Fast copy not engaged | Missing `StagingDefinition` annotation | Add `[StagingDefinition = [Kind = "FastCopy"]]` before the `section` declaration in `mashup.pq` |
| 8 | Parameter type mismatch at runtime | Runtime parameter `type` doesn't match definition | Use `"Automatic"` for type in the `parameters` array, or ensure the type matches the parameter's `meta` declaration |
| 9 | Rate limited (429 Too Many Requests) | Exceeded API rate limits | Respect the `Retry-After` response header; implement exponential backoff |
| 10 | LRO polling returns 404 | Constructed operation URL manually instead of using `Location` header | Always use the `Location` header URL returned in the 202 response |
| 11 | Sensitivity labels not in `getDefinition` response | Labels are managed separately from the item definition | Use the Fabric Admin API or portal to manage sensitivity labels — they are not part of definition parts |
| 12 | Duplicate `displayName` causes confusion | `displayName` uniqueness is **not enforced** by the API | Use distinct, descriptive names; consider a naming convention (e.g., prefix with environment) |
| 13 | `folderId` error on create | Invalid folder GUID | `folderId` is optional — omit it to create in workspace root. If provided, the folder must exist |
| 14 | `updateDefinition` doesn't update display name | Forgot `?updateMetadata=true` query parameter | Append `?updateMetadata=true` to also apply changes from the `.platform` file (display name, etc.) |
| 15 | EvaluateQuery fails on new dataflow | Dataflow has never been refreshed | Run a refresh (Execute job) first — `EvaluateQuery` requires at least one successful refresh to operate on |

---

## Quick Reference: Authoring Decision Guide

| Scenario | Recommended Approach |
|---|---|
| Create empty dataflow | `POST /v1/workspaces/{workspaceId}/dataflows` with `displayName` only (no `definition`) |
| Create dataflow with queries | `POST` with full `definition` containing all 3 parts (base64-encoded) |
| Modify query logic | `getDefinition` → decode `mashup.pq` → edit M code → re-encode → `updateDefinition` (all 3 parts) |
| Add new query to existing dataflow | `getDefinition` → add `shared` query to `mashup.pq` + entry to `queriesMetadata` → `updateDefinition` |
| Rename dataflow | `PATCH /v1/workspaces/{workspaceId}/dataflows/{dataflowId}` with new `displayName` |
| Trigger refresh | `POST /v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/Execute/instances` |
| Refresh with parameter override | `POST .../jobs/Execute/instances` with `parameters` array in request body |
| Check refresh status | `GET /v1/operations/{operationId}` (use `Location` header from 202 response) |
| CI/CD: export to Git | `getDefinition` → base64-decode each part → write to repo as plain files |
| CI/CD: deploy from Git | Read files from repo → base64-encode → `updateDefinition` on target workspace |
| Environment-specific deploy | Modify `mashup.pq` parameter defaults before encoding and calling `updateDefinition` |
| Delete dataflow | `DELETE /v1/workspaces/{workspaceId}/dataflows/{dataflowId}` |

# DATAFLOWS-CONSUMPTION-CORE.md

> **Scope**: Consumption patterns for **Fabric Dataflows Gen2** — listing, exploring, monitoring refreshes, discovering parameters, evaluating queries, exploring definitions, and operational monitoring.
> This document is *language-agnostic* — no C#, Python, CLI, or SDK references. It covers Fabric REST API patterns for read-only operations against Dataflows Gen2 items.

---

> **Relationship to DATAFLOWS-AUTHORING-CORE.md**: Authoring topics (creating, updating, deleting dataflows, connection management, job execution, CI/CD) live in `DATAFLOWS-AUTHORING-CORE.md`. This document covers consumption-exclusive topics: listing dataflows, exploring definitions, discovering parameters, monitoring refresh/job status, evaluating queries, and operational troubleshooting.

---

## Consumption Capability Matrix

| Capability | Dataflow Gen2 |
|---|---|
| List Dataflows in workspace | ✅ |
| Get Dataflow properties | ✅ |
| Get Dataflow Definition | ✅ (requires Read+Write) |
| Discover Parameters | ✅ (Read only) |
| Monitor Job/Refresh status | ✅ (via Operations API) |
| Evaluate/Preview Query | ✅ (via Dataflow API) |
| List across workspaces | ✅ (iterate workspaces) |
| Get item job history | ✅ (via Job Scheduler API) |

---

## REST API Surface (Consumption)

All endpoints use the Fabric REST API base URL. Authentication requires a bearer token with audience `https://api.fabric.microsoft.com/.default`.

### List Dataflows

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows
```

**Query Parameters** (optional):

| Parameter | Type | Description |
|---|---|---|
| `continuationToken` | string | Token for next page of results |

**Permission**: Viewer workspace role
**Scopes**: `Workspace.Read.All`

**Response** (200 OK):

```json
{
  "value": [
    {
      "id": "<dataflow-id>",
      "displayName": "Sales Data Pipeline",
      "description": "Loads daily sales from source to lakehouse",
      "type": "Dataflow",
      "workspaceId": "<workspace-id>"
    }
  ],
  "continuationToken": "<next-page-token-or-null>"
}
```

**Pagination**: Repeat the request with `continuationToken` from the previous response until it is absent or null.

### Get Dataflow

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}
```

Returns a single dataflow's properties (not its definition). Same permission model as List.

**Response** (200 OK):

```json
{
  "id": "<dataflow-id>",
  "displayName": "Sales Data Pipeline",
  "description": "Loads daily sales from source to lakehouse",
  "type": "Dataflow",
  "workspaceId": "<workspace-id>"
}
```

### Discover Parameters

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/parameters
```

**Permission**: Read only (`Dataflow.Read.All`)

**Response** (200 OK):

```json
{
  "value": [
    {
      "name": "SourceServer",
      "type": "String",
      "isRequired": true,
      "description": "The hostname of the source SQL server",
      "defaultValue": "sql-prod.database.windows.net"
    },
    {
      "name": "FilterDate",
      "type": "DateTime",
      "isRequired": false,
      "description": "Only load records after this date",
      "defaultValue": "2025-01-01T00:00:00.000Z"
    }
  ],
  "continuationToken": null
}
```

**Supported parameter types**: `String`, `Boolean`, `Integer`, `Number`, `DateTime`, `DateTimeZone`, `Date`, `Time`, `Duration`

**Error**: If the dataflow has no parameters, the API returns a `DataflowNotParametricError`.

### Get Definition (for Exploration)

```http
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/getDefinition
```

**Permission**: Read+Write (`Dataflow.ReadWrite.All`) — **not** Read-only.

**Request Body**: Empty or omitted.

**Response** (200 OK — immediate) or (202 Accepted — long-running operation):

When the definition is large, the API may return `202 Accepted` with a `Location` header. Poll the URL in the `Location` header until the operation completes.

**200 Response**:

```json
{
  "definition": {
    "parts": [
      {
        "path": "mashup.pq",
        "payload": "<base64-encoded-mashup-pq>",
        "payloadType": "InlineBase64"
      },
      {
        "path": "queryMetadata.json",
        "payload": "<base64-encoded-query-metadata>",
        "payloadType": "InlineBase64"
      },
      {
        "path": ".platform",
        "payload": "<base64-encoded-platform-json>",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

### Monitor Job Status (Operations API)

```http
GET https://api.fabric.microsoft.com/v1/operations/{operationId}
```

Poll until the `status` field reaches a terminal state: `Succeeded`, `Failed`, or `Cancelled`.

**Response**:

```json
{
  "id": "<operation-id>",
  "status": "Running",
  "createdTimeUtc": "2025-07-15T10:30:00Z",
  "lastUpdatedTimeUtc": "2025-07-15T10:31:15Z"
}
```

Get detailed result after completion:

```http
GET https://api.fabric.microsoft.com/v1/operations/{operationId}/result
```

### Get Item Job Instances

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/instances
```

Returns job history with status, start/end times, and error details.

**Response**:

```json
{
  "value": [
    {
      "id": "<job-instance-id>",
      "itemId": "<dataflow-id>",
      "jobType": "Execute",
      "invokeType": "Scheduled",
      "status": "Completed",
      "startTimeUtc": "2025-07-15T06:00:00Z",
      "endTimeUtc": "2025-07-15T06:12:34Z",
      "failureReason": null
    }
  ]
}
```

---

## Dataflow Definition Exploration

The definition returned by `getDefinition` contains three base64-encoded parts. Decode and inspect each to understand the dataflow's structure.

### Step-by-Step Decoding

**1. Call getDefinition** — retrieves three base64-encoded parts.

**2. Decode each part**:

```bash
# bash
echo "<base64-payload>" | base64 --decode
```

```powershell
# PowerShell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("<base64-payload>"))
```

**3. Inspect mashup.pq** — the Power Query M code containing all queries and transformations.

**4. Inspect queryMetadata.json** — query names, IDs, staging flags, connections.

**5. Inspect .platform** — item type and display name.

### mashup.pq Structure

The `mashup.pq` file contains the Power Query M expressions for every query in the dataflow. Queries are defined as `shared` members in a `section`.

```powerquery
[StagingDefinition = [Kind = "FastCopy"]]
section Section1;

shared SalesData = let
    Source = Sql.Database("sql-prod.database.windows.net", "SalesDB"),
    Navigation = Source{[Schema="dbo", Item="Orders"]}[Data],
    FilteredRows = Table.SelectRows(Navigation, each [OrderDate] >= #date(2025, 1, 1))
in
    FilteredRows;

shared TransformedSales = let
    Source = SalesData,
    AddedColumn = Table.AddColumn(Source, "Revenue", each [Quantity] * [UnitPrice], type number),
    RemovedColumns = Table.RemoveColumns(AddedColumn, {"InternalNotes"})
in
    RemovedColumns;
```

**Key patterns**:
- `[StagingDefinition = [Kind = "FastCopy"]]` — annotation for staging (Fast Copy via data pipeline)
- `shared QueryName = let ... in ...;` — each query is a shared member
- Queries can reference other queries by name (e.g., `Source = SalesData`)
- The final expression in the `let ... in` block is the query output

### queryMetadata.json Key Fields

```json
{
  "formatVersion": "202502",
  "queriesMetadata": {
    "SalesData": {
      "queryId": "<query-guid>",
      "queryName": "SalesData",
      "loadEnabled": true,
      "isHidden": false
    },
    "TransformedSales": {
      "queryId": "<query-guid>",
      "queryName": "TransformedSales",
      "loadEnabled": true,
      "isHidden": false
    },
    "HelperQuery": {
      "queryId": "<query-guid>",
      "queryName": "HelperQuery",
      "loadEnabled": false,
      "isHidden": true
    }
  },
  "connections": [
    {
      "path": "sql-prod.database.windows.net;SalesDB",
      "kind": "SQL",
      "connectionId": "<connection-guid>"
    }
  ],
  "computeEngineSettings": {
    "allowFastCopy": true,
    "maxConcurrency": 4
  }
}
```

**Important fields**:
- `loadEnabled` — `true` means the query output is written to the destination (lakehouse). `false` means it is a helper/staging query only.
- `isHidden` — hidden queries are not shown in the dataflow editor UI but still execute.
- `connections` — lists all external data sources with their connection IDs.
- `computeEngineSettings` — controls Fast Copy and concurrency behavior.

### .platform File

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Dataflow",
    "displayName": "Sales Data Pipeline"
  },
  "config": {
    "version": "2.0",
    "logicalId": "<logical-id>"
  }
}
```

---

## Parameter Discovery and Analysis

Parameters allow dataflows to accept runtime inputs. The Parameters API returns typed metadata for each parameter.

### Parameter Types and Formats

| Type | Format | Example Value |
|---|---|---|
| String | text | `"test-value"` |
| Boolean | true/false | `true` |
| Integer | int64 | `123456789` |
| Number | double | `3.14` |
| DateTime | yyyy-MM-ddTHH:mm:ss.xxxZ | `"2025-09-15T21:45:00.000Z"` |
| DateTimeZone | yyyy-MM-ddTHH:mm:sszzz | `"2025-09-15T21:45:00+02:00"` |
| Date | yyyy-MM-dd | `"2025-09-15"` |
| Time | HH:mm:ss | `"21:45:00"` |
| Duration | PdDTHHmMsS (ISO 8601) | `"P5DT21H35M30S"` |

### Parameter Discovery Pattern

1. Call `GET .../dataflows/{dataflowId}/parameters`
2. Iterate the `value` array
3. For each parameter, note `name`, `type`, `isRequired`, `defaultValue`
4. Use this metadata to validate values before passing them to a refresh or update operation

### Parameters in mashup.pq

Parameters appear in M code as metadata-annotated expressions:

```powerquery
shared SourceServer = "sql-prod.database.windows.net" meta [IsParameterQuery = true, Type = type text, IsParameterQueryRequired = true];
shared FilterDate = #datetime(2025, 1, 1, 0, 0, 0) meta [IsParameterQuery = true, Type = type datetime, IsParameterQueryRequired = false];
```

---

## Refresh and Job Monitoring

### Job Types

For Dataflows Gen2, the primary job type is `Execute` — this represents a standard dataflow refresh that evaluates all enabled queries and writes results to the configured destination.

### LRO (Long-Running Operation) Pattern

Triggering a dataflow refresh follows the standard Fabric LRO pattern:

1. **Trigger**: `POST .../items/{dataflowId}/jobs/instances?jobType=Execute` → returns `202 Accepted`
2. **Location header**: Contains the operation URL (e.g., `https://api.fabric.microsoft.com/v1/operations/{operationId}`)
3. **Poll**: `GET /v1/operations/{operationId}` until status is terminal
4. **Terminal states**: `Succeeded`, `Failed`, `Cancelled`
5. **Result**: `GET /v1/operations/{operationId}/result` for detailed outcome

### Monitoring with Job Instances API

The Job Instances API provides historical job data without requiring the operation ID:

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/instances
```

**Key fields in each job instance**:

| Field | Description |
|---|---|
| `id` | Unique job instance ID |
| `itemId` | The dataflow ID |
| `jobType` | Always `Execute` for dataflows |
| `invokeType` | `Manual`, `Scheduled`, or `External` |
| `status` | `NotStarted`, `InProgress`, `Completed`, `Failed`, `Cancelled`, `Deduped` |
| `startTimeUtc` | When the job began executing |
| `endTimeUtc` | When the job finished (null if still running) |
| `failureReason` | Error details if status is `Failed` |

### Polling Best Practices

- Start polling after a 5-second initial delay
- Use exponential backoff: 5s → 10s → 20s → 30s (cap at 30s)
- Respect the `Retry-After` header if present in 429 responses
- Set a maximum timeout (e.g., 60 minutes) to avoid infinite polling
- Log each poll response for diagnostics

---

## Agentic Exploration Pattern ("Chat With My Dataflows")

A structured 6-step discovery sequence for agents and automation to fully explore a workspace's dataflows.

### Step 1: List Workspaces → Find Target Workspace

```http
GET https://api.fabric.microsoft.com/v1/workspaces
```

Iterate results to find the workspace by `displayName`. Extract `workspaceId`.

### Step 2: List Dataflows in Workspace → Enumerate All Dataflows

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows
```

Paginate with `continuationToken`. Collect `id`, `displayName`, `description` for each dataflow.

### Step 3: Get Dataflow Properties → Name, Description, Tags

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}
```

Retrieve the full metadata for a specific dataflow.

### Step 4: Discover Parameters → Understand Inputs and Defaults

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/parameters
```

Enumerate all parameters, their types, required flags, and default values. Handle `DataflowNotParametricError` gracefully if the dataflow has no parameters.

### Step 5: Get Definition → Decode and Analyze mashup.pq Queries

```http
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/dataflows/{dataflowId}/getDefinition
```

Decode the three base64 parts. Analyze:
- **mashup.pq**: Query logic, transformations, data sources, inter-query dependencies
- **queryMetadata.json**: Which queries load to destination, connections used, staging config
- **.platform**: Item type confirmation and display name

**Note**: Requires Read+Write permission. If the agent only has Read access, skip this step and rely on parameters and job history for understanding.

### Step 6: Check Job History → Recent Refresh Status and Timing

```http
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{dataflowId}/jobs/instances
```

Review recent job instances for:
- Last successful refresh time
- Average refresh duration
- Failure patterns and error messages
- Invoke types (scheduled vs. manual)

---

## Security and Permissions Model

### Permission Requirements by Operation

| Operation | Minimum Permission | Scope |
|---|---|---|
| List Dataflows | Viewer | `Workspace.Read.All` |
| Get Dataflow | Viewer | `Workspace.Read.All` |
| Discover Parameters | Read | `Dataflow.Read.All` |
| Get Definition | Read+Write | `Dataflow.ReadWrite.All` |
| Monitor Jobs | Viewer | `Item.Read.All` |
| Get Job Instances | Viewer | `Item.Read.All` |

### Token Audience

All Fabric REST API calls require a bearer token with audience:

```
https://api.fabric.microsoft.com/.default
```

### Workspace Role Mapping

| Workspace Role | List | Get | Parameters | Definition | Jobs |
|---|---|---|---|---|---|
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |
| Member | ✅ | ✅ | ✅ | ✅ | ✅ |
| Contributor | ✅ | ✅ | ✅ | ✅ | ✅ |
| Viewer | ✅ | ✅ | ✅ | ❌ | ✅ |

**Key constraint**: Viewers cannot call `getDefinition`. This is a common source of `403 Forbidden` errors for read-only consumers.

---

## Common Errors

| Error Code | Cause | Resolution |
|---|---|---|
| `ItemNotFound` | Dataflow ID doesn't exist or was deleted | Verify the ID with List Dataflows API |
| `DataflowNotParametricError` | Dataflow has no parameters defined | Check the definition for parameter queries; this is not a failure |
| `401 Unauthorized` | Token expired or wrong audience | Refresh token; ensure audience is `https://api.fabric.microsoft.com/.default` |
| `403 Forbidden` | Insufficient permissions for the operation | Check workspace role; `getDefinition` requires Read+Write |
| `429 TooManyRequests` | Rate limited by the Fabric API | Respect the `Retry-After` header; implement exponential backoff |
| `OperationNotSupportedForItem` | Operation called on wrong item type | Verify the item is of type `Dataflow` (not `DataPipeline`, `Notebook`, etc.) |
| `InvalidItemType` | Used a Dataflow-specific endpoint on a non-Dataflow item | Confirm item type via Get Item before calling dataflow-specific APIs |

---

## Gotchas and Troubleshooting Reference

| # | Issue | Cause | Resolution |
|---|---|---|---|
| 1 | `getDefinition` returns `403 Forbidden` | Caller has Read-only (Viewer) permission | `getDefinition` requires Read+Write permission — request Contributor role or higher |
| 2 | `getDefinition` called with GET instead of POST | Wrong HTTP method | `getDefinition` is a **POST** endpoint, not GET — even though it reads data |
| 3 | Parameters API returns empty `value` array | Dataflow has no parameters defined | This is expected behavior, not an error — check the definition's mashup.pq for `IsParameterQuery` metadata |
| 4 | Base64-decoded content has unexpected leading characters | BOM (Byte Order Mark) in encoded content | Strip the UTF-8 BOM (`\xEF\xBB\xBF`) when decoding; use UTF-8 encoding explicitly |
| 5 | Connection IDs in queryMetadata.json appear as JSON strings | Nested JSON serialization | Parse `connectionId` values as strings; they may need additional unquoting depending on the serialization |
| 6 | `loadEnabled: false` but query appears in dataflow | Query is a helper/staging query | `loadEnabled: false` means the query does not write to the destination lakehouse — it is used as an intermediate step by other queries |
| 7 | Job status polling runs indefinitely | No backoff or timeout implemented | Use exponential backoff (5s→10s→20s→30s cap) and set a maximum timeout (e.g., 60 minutes) |
| 8 | Operations API returns `404 Not Found` for operation ID | Operations API is tenant-scoped, not workspace-scoped | Use `GET /v1/operations/{operationId}` without a workspace prefix — the operations endpoint is at the tenant level |
| 9 | Sensitivity labels not present in definition response | Labels are managed separately from item definitions | Use the admin/governance APIs for sensitivity label information, not the definition API |
| 10 | Pagination fails or returns duplicate results | Using offset-based pagination instead of continuationToken | List Dataflows uses `continuationToken` (not offset/skip) — always pass the token from the previous response |
| 11 | `displayName` collision when matching dataflows | Multiple dataflows can share the same display name | Always use the `id` field for programmatic access — `displayName` is not unique |
| 12 | `getDefinition` returns `202 Accepted` unexpectedly | Definition is large or server is under load | This is the LRO pattern — poll the URL in the `Location` header until the operation completes |

---

## Quick Reference: Consumption Decision Guide

| Scenario | Recommended Approach |
|---|---|
| Find all dataflows in a workspace | `GET .../workspaces/{workspaceId}/dataflows` — paginate with `continuationToken` |
| Get dataflow query logic | `POST .../getDefinition` → decode `mashup.pq` from base64 |
| Check what parameters are available | `GET .../dataflows/{dataflowId}/parameters` |
| Check last refresh status | `GET .../items/{dataflowId}/jobs/instances` — inspect most recent entry |
| Understand query dependencies | Decode `mashup.pq` — trace `shared` query references across `let` expressions |
| Find a dataflow by name | List all dataflows, filter by `displayName` client-side |
| Monitor an active refresh | Poll `GET /v1/operations/{operationId}` with exponential backoff |
| Explore connections used by a dataflow | Decode `queryMetadata.json` → inspect the `connections` array |
| Check if a query loads to lakehouse | Decode `queryMetadata.json` → `queriesMetadata` → check `loadEnabled` flag |
| Discover dataflow structure without write access | Use Parameters API (read-only) + Job Instances API for indirect understanding |
| Audit refresh failures over time | Query Job Instances API, filter by `status: "Failed"`, inspect `failureReason` |

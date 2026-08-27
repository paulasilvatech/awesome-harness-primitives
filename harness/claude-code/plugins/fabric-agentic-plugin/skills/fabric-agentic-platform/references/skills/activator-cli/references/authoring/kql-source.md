# KQL Source (`kqlSource-v1`)

Queries a KQL database (Eventhouse or ADX/Kusto cluster) on a configurable schedule. The query runs periodically and feeds results into the Activator pipeline.

> **Design principle:** The KQL query should return ALL relevant data — do NOT pre-filter for the condition in KQL. Let the Activator rule handle the detection logic (thresholds, text conditions, etc.) via its steps. The KQL query is just the data source.

> **Time-axis default:** If the query results include a reasonable datetime column, always configure `eventTimeSettings` and `queryParameters` so the source runs with a time axis. Only fall back to **snapshot mode** when the underlying data has no reasonable timestamp column and each row represents the latest state.

> **Validate first:** Before creating or updating the Activator, run the KQL directly against the target KQL source and confirm the returned columns, timestamp field, and row shape are correct. If the query returns **no rows** (or the table/column does not exist), treat the source as **missing** -- stop and ask for the correct source and fields rather than authoring against an empty source. If the user explicitly instructs authoring against a future / not-yet-emitting source, state that assumption and continue without claiming rows were observed.

```json
{
  "uniqueIdentifier": "<kql-source-guid>",
  "payload": {
    "name": "Sensor telemetry query",
    "runSettings": {
      "executionIntervalInSeconds": 60
    },
    "query": {
      "queryString": "declare query_parameters(startTime:datetime, endTime:datetime);\nSensorData | where Timestamp between (startTime .. endTime) | project Timestamp, DeviceId, Temperature, Building"
    },
    "eventhouseItem": {
      "itemId": "<kql-database-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "KustoDatabase"
    },
    "queryParameters": [
      { "name": "startTime", "type": "DURATION_START", "value": "2025-01-01T00:00:00Z" },
      { "name": "endTime", "type": "DURATION_END", "value": "2025-01-01T00:05:00Z" }
    ],
    "eventTimeSettings": {
      "timeFieldName": "Timestamp",
      "ingestionDelayInSeconds": 120,
      "timeZone": "UTC"
    },
    "metadata": {
      "workspaceId": "<workspace-guid>",
      "measureName": "",
      "querySetId": "",
      "queryId": ""
    },
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "kqlSource-v1"
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | yes | Display name |
| `runSettings.executionIntervalInSeconds` | number | yes | Poll frequency in seconds |
| `query.queryString` | string | yes | KQL query to execute |
| `eventhouseItem.itemId` | GUID | yes | KQL Database item ID (not the Eventhouse ID) |
| `eventhouseItem.workspaceId` | GUID | yes | Workspace containing the KQL Database |
| `eventhouseItem.itemType` | string | yes | Always `"KustoDatabase"` |
| `queryParameters` | array | yes | Query parameters — usually `DURATION_START`/`DURATION_END`; use empty `[]` only for snapshot mode |
| `metadata.workspaceId` | GUID | yes | Workspace ID (same as eventhouseItem.workspaceId) |
| `metadata.measureName` | string | yes | Usually empty string `""` |
| `metadata.querySetId` | string | yes | Usually empty string `""` |
| `metadata.queryId` | string | yes | Usually empty string `""` |
| `eventTimeSettings` | object | no | Time-axis configuration — expected whenever the query results include a reasonable timestamp |
| `parentContainer.targetUniqueIdentifier` | GUID | yes | Container ref |

---

## `eventhouseItem` Reference Shapes

`eventhouseItem` is a union in the schema. Use one of these two shapes:

### 1. Fabric Eventhouse / KQL Database reference

Use this when the source is a Fabric KQL database item:

```json
{
  "eventhouseItem": {
    "itemId": "<kql-database-item-guid>",
    "workspaceId": "<workspace-guid>",
    "itemType": "KustoDatabase"
  }
}
```

### 2. External ADX / Kusto cluster reference

Use this when the source is an external ADX/Kusto cluster instead of a Fabric item:

```json
{
  "eventhouseItem": {
    "clusterHostName": "mycluster.westeurope.kusto.windows.net",
    "databaseName": "MyDatabase"
  }
}
```

> **Exact schema field names:** the ADX reference uses `clusterHostName` and `databaseName`. It is **not** `clusterUrl`.

## Design Guidance

- **Do NOT pre-filter conditions in KQL** — return all data and let the Activator rule handle detection logic (thresholds, text conditions, filters). The KQL query should only select the relevant time window and project the needed columns
- For Fabric sources, `eventhouseItem.itemId` is the **KQL Database** item ID (not the Eventhouse ID) — resolve via the Fabric Items API (`GET /v1/workspaces/{wsId}/kqlDatabases`)
- For ADX/Kusto sources, use `eventhouseItem.clusterHostName` and `eventhouseItem.databaseName`
- The `queryParameters` and `metadata` fields are **required** even if empty
- **Default to time-axis mode** when the query results contain a reasonable datetime column
- Use **snapshot mode** only when there is no reasonable timestamp column and the rows represent current state, not an event stream

---

## Time-Axis Default (`eventTimeSettings`)

If the query results have a usable datetime column, use `eventTimeSettings` plus `queryParameters`. This is the default mode for KQL sources because it gives Activator an explicit event-time axis, watermark tracking, and late-arrival handling.

### Choose the Mode

| Mode | When to Use |
|------|-------------|
| **Time-axis mode** | The query results include a reasonable datetime column that represents when each row/event happened |
| **Snapshot mode** | The source has no reasonable timestamp column and each row represents the latest state of an entity |

### Configuration

Add `eventTimeSettings` and `queryParameters` to the kqlSource payload for the normal time-axis case:

```json
{
  "query": {
    "queryString": "declare query_parameters(startTime:datetime, endTime:datetime);\nMyTable | where Timestamp between (startTime .. endTime) | project Timestamp, DeviceId, Temperature"
  },
  "eventTimeSettings": {
    "timeFieldName": "Timestamp",
    "ingestionDelayInSeconds": 120,
    "timeZone": "UTC"
  },
  "queryParameters": [
    { "name": "startTime", "type": "DURATION_START", "value": "2025-01-01T00:00:00Z" },
    { "name": "endTime", "type": "DURATION_END", "value": "2025-01-01T00:05:00Z" }
  ]
}
```

### `eventTimeSettings` Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timeFieldName` | string | yes | The datetime column in query results used as the time axis. After each execution, the max value of this column becomes the watermark for the next query. |
| `ingestionDelayInSeconds` | number | no | Late-arrival buffer in seconds. Shifts the query end-time back from "now" by this amount, ensuring late-arriving data is not missed. Default: 0. |
| `timeZone` | string | no | Time zone for interpretation. Currently only `"UTC"` is supported. |

### `queryParameters` with Time-Axis

When `eventTimeSettings` is set, `queryParameters` **must** include one `DURATION_START` and one `DURATION_END` entry. The KQL itself must also declare those parameters with `declare query_parameters(startTime:datetime, endTime:datetime);` before the query body.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Parameter name referenced in the KQL query (e.g., `startTime`) |
| `type` | string | `"DURATION_START"` or `"DURATION_END"` |
| `value` | string | Initial value (ISO 8601) — defines the backfill window on first execution |

### How Execution Works

1. **First execution:** Query runs with the `value` from each parameter to determine the initial data window
2. **Subsequent executions:** `DURATION_START` is automatically overridden with the watermark (max event time from previous results). `DURATION_END` is overridden with `now - ingestionDelayInSeconds`

### KQL Query Pattern for Time-Axis

Use `declare query_parameters(...)` followed by `between` with the parameter names:

```kql
declare query_parameters(startTime:datetime, endTime:datetime);
MyTable
| where Timestamp between (startTime .. endTime)
| project Timestamp, DeviceId, Temperature, Building
```

Do **not** use `ago()` as the normal pattern for KQL sources. If there is a usable timestamp column, model it explicitly with `eventTimeSettings`.

### Snapshot Mode (No Reasonable Timestamp Column)

Use snapshot mode only when there is no reasonable timestamp column and each row is the current state of an entity. In that case:

- Omit `eventTimeSettings`
- Set `queryParameters` to `[]`
- Do not add `ago()`, `between`, or other time filtering
- Project the current-state columns the rule needs

```kql
DeviceInventory
| project DeviceId, DeviceName, Status, Location, BatteryLevel
```

# Digital Twin Builder / Ontology Source (`digitalTwinBuilderSource-v1`)

Queries an existing **Digital Twin Builder** or **Ontology** Fabric item on a schedule and feeds the returned rows into the Activator pipeline.

> **Important:** `query.queryString` is **not KQL**. It is a JSON-string payload that Activator later POSTs to the DTB query endpoint.

> **Time-axis default:** If the DTB query results include a reasonable datetime field, prefer `eventTimeSettings` plus `DURATION_START` / `DURATION_END` query parameters. Only use snapshot mode when the query returns current-state rows with no reasonable event-time field.

> **Validate first:** Before creating or updating the Activator, run the DTB / Ontology query directly first and confirm the returned columns, key fields, timestamp field, requested signal field, and at least one representative row are correct. If the query returns no rows or the requested field is missing, treat the source as missing and ask for the correct source and fields rather than authoring against an empty source. If the user explicitly instructs authoring against a future / not-yet-emitting source, state that assumption and continue without claiming rows were observed.

```json
{
  "uniqueIdentifier": "<dtb-source-guid>",
  "payload": {
    "name": "Truck telemetry from ontology",
    "runSettings": {
      "executionIntervalInSeconds": 300
    },
    "query": {
      "queryString": "{\"entitySelector\":{\"query\":\"MATCH [t:Truck] RETURN t.id as TruckId, t.site as Site\"},\"timeSeriesSelector\":{\"entityType\":{\"Name\":\"Truck\"},\"keyColumns\":{\"id\":\"TruckId\"},\"metrics\":[{\"field\":\"velocity\"},{\"field\":\"temperature\"}],\"groupBy\":[\"TruckId\",\"Site\"]}}",
      "compositeKey": {
        "name": "dtbCompositeKey",
        "keys": ["TruckId", "Site"]
      }
    },
    "connection": {
      "itemId": "<ontology-or-dtb-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "Ontology"
    },
    "queryParameters": [
      { "name": "start", "type": "DURATION_START", "value": "2025-09-04T19:00:00Z" },
      { "name": "end", "type": "DURATION_END", "value": "2025-09-04T19:20:00Z" }
    ],
    "eventTimeSettings": {
      "timeFieldName": "Timestamp",
      "ingestionDelayInSeconds": 120
    },
    "metadata": {
      "digitalTwinBuilderEntityId": "Truck"
    },
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "digitalTwinBuilderSource-v1"
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | yes | Display name |
| `runSettings.executionIntervalInSeconds` | integer | yes | Poll frequency in seconds. Schema range: 60-86400 |
| `query.queryString` | string | yes | JSON-string query payload sent to the DTB endpoint |
| `query.compositeKey.name` | string | no | Display name for a generated composite key column |
| `query.compositeKey.keys[]` | string[] | no | Column names to concatenate into the composite key |
| `connection.itemId` | GUID | yes | Target Digital Twin Builder / Ontology item ID |
| `connection.workspaceId` | GUID | yes | Workspace containing that item |
| `connection.itemType` | string | yes | Either `"DigitalTwinBuilder"` or `"Ontology"` |
| `queryParameters` | array | no | Optional query params. Use `DURATION_START` / `DURATION_END` for time-axis mode |
| `eventTimeSettings.timeFieldName` | string | no | Event-time field in the returned rows |
| `eventTimeSettings.ingestionDelayInSeconds` | integer | no | Late-arrival buffer in seconds |
| `metadata.digitalTwinBuilderEntityId` | string | no | Optional DTB entity identifier. If `metadata` is present, this field is required |
| `parentContainer.targetUniqueIdentifier` | GUID | yes | Container ref |

---

## `connection` Item Types

The DTB source can point at either supported item kind:

```json
{
  "connection": {
    "itemId": "<item-guid>",
    "workspaceId": "<workspace-guid>",
    "itemType": "DigitalTwinBuilder"
  }
}
```

```json
{
  "connection": {
    "itemId": "<item-guid>",
    "workspaceId": "<workspace-guid>",
    "itemType": "Ontology"
  }
}
```

Use the actual item type returned by the Fabric Items API when you resolve the target item dynamically.

## Query Payload Pattern

`query.queryString` stores a JSON object as a string. The backend test coverage shows this general shape:

```json
{
  "entitySelector": {
    "query": "MATCH [t:Truck] RETURN t.id as TruckId, t.color as Color"
  },
  "timeSeriesSelector": {
    "entityType": { "Name": "Truck" },
    "keyColumns": { "id": "TruckId" },
    "metrics": [{ "field": "velocity" }],
    "groupBy": ["TruckId"]
  }
}
```

Common authoring notes:

- Build that object in Python, then serialize it with `json.dumps(...)`
- Store the serialized string in `query.queryString`
- Do **not** embed the object directly as nested JSON inside `ReflexEntities.json`
- Use `query.compositeKey` when the returned rows need a stable synthetic identity built from multiple columns

## Design Guidance

- Resolve the backing Fabric item dynamically by name and type, then use its `itemId`, `workspaceId`, and actual `itemType`
- Prefer **Ontology** when the source is an ontology item; prefer **DigitalTwinBuilder** when the source is the DTB item itself
- Keep the DTB query focused on data retrieval and shaping; let the Activator rule handle thresholds, text conditions, and filtering logic
- Use `query.compositeKey` when identity depends on multiple returned fields
- If `metadata` is included, it must contain `digitalTwinBuilderEntityId`

---

## Time-Axis Mode

Use time-axis mode when the DTB result rows include a reasonable datetime field.

```json
{
  "queryParameters": [
    { "name": "start", "type": "DURATION_START", "value": "2025-09-04T19:00:00Z" },
    { "name": "end", "type": "DURATION_END", "value": "2025-09-04T19:20:00Z" }
  ],
  "eventTimeSettings": {
    "timeFieldName": "Timestamp",
    "ingestionDelayInSeconds": 120
  }
}
```

### Important difference from KQL

For KQL sources, the duration parameters are referenced inside the KQL text. For DTB sources, the backend appends them as **URL query-string parameters** when calling the DTB endpoint. The query payload itself stays as the JSON-string body.

Backend examples use `start` and `end`, which are good names to mirror in authored payloads. Even though the executor can fall back to default names, do **not** rely on that fallback in authored definitions.

## Snapshot Mode

Use snapshot mode when the DTB query returns the latest state and there is no reliable event-time field.

```json
{
  "payload": {
    "name": "Truck inventory snapshot",
    "runSettings": {
      "executionIntervalInSeconds": 300
    },
    "query": {
      "queryString": "{\"entitySelector\":{\"query\":\"MATCH [t:Truck] RETURN t.id as TruckId, t.state as State, t.battery as BatteryLevel\"}}"
    },
    "connection": {
      "itemId": "<dtb-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "DigitalTwinBuilder"
    },
    "queryParameters": [],
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  }
}
```

Snapshot-mode guidance:

- omit `eventTimeSettings`
- set `queryParameters` to `[]` unless the endpoint genuinely needs stable `HARDCODED` parameters
- do not model rolling time windows when the source has no trustworthy timestamp field

## Backend Notes

The full stored DTB source document also contains service-managed fields such as:

- `system.metadata.internalEventName`
- `system.metadata.initialDigitalTwinBuilderCapacityId`
- `system.connection.connectionString`
- `system.connection.authMethod`

Those fields matter for backend execution and readback, but the main authoring task is to construct the correct **entity payload** shown above.

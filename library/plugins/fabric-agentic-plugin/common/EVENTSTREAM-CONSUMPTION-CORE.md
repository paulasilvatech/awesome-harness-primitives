# EVENTSTREAM-CONSUMPTION-CORE.md — Read-Only Eventstream Discovery and Monitoring Patterns for Fabric

> **Purpose**: Shared reference for Eventstream consumption skills. Covers listing and discovering Eventstreams, monitoring health, inspecting topology, checking source/destination status, and integration with downstream analytics.
> **Language-agnostic** — all API references are raw REST specifications (verb, URL, headers, payload). No CLI commands or SDK code.
> **Schema source**: Property schemas are aligned with the official [`eventstream-definition.json`](https://github.com/microsoft/fabric-event-streams/blob/main/API%20Templates/eventstream-definition.json) template from `microsoft/fabric-event-streams`.

---

## Listing and Discovering Eventstreams

### List Eventstreams in a Workspace

```text
GET /v1/workspaces/{workspaceId}/eventstreams
```

Returns a paginated array of Eventstream items with `id`, `displayName`, `description`, `type`.

Pagination follows standard Fabric patterns: check for `continuationUri` in the response.

### Get Eventstream Properties

```text
GET /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}
```

Returns metadata for a single Eventstream: `id`, `displayName`, `description`, `type`, `workspaceId`.

### Search Across Workspaces

To find Eventstreams across workspaces, use the Fabric Catalog Search API or list items with type filter:

```text
GET /v1/workspaces/{workspaceId}/items?type=Eventstream
```

Or iterate across accessible workspaces using the List Workspaces API.

---

## Inspecting Eventstream Topology

### Topology API (Recommended)

The Topology API returns the runtime topology with per-node **status**, **error info**, and **input schemas** — without requiring base64 decoding. [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/topology).

```text
GET /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/topology
```

Response includes `compatibilityLevel`, `sources[]`, `destinations[]`, `operators[]`, and `streams[]`. Each node has:

| Field | Description |
|-------|-------------|
| `id` | Node GUID (use as `{sourceId}` / `{destinationId}` in other Topology API calls) |
| `name` | Unique node name |
| `type` | Source/destination/operator type enum |
| `properties` | Type-specific configuration |
| `status` | Runtime status: `Running`, `Paused`, `Error`, etc. |
| `error` | Error details if status is not healthy (null otherwise) |
| `inputNodes` | References to upstream nodes (destinations and operators) |
| `inputSchemas` | Resolved column schemas with name, type, and nested fields |

### Inspecting Individual Nodes

```text
GET /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/sources/{sourceId}
GET /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/destinations/{destinationId}
```

Returns detailed properties, status, and error info for a single node.

### Custom Endpoint Source — Connection Details

The Items API `getDefinition` returns empty properties for Custom Endpoint sources. Use the Topology API to retrieve the Kafka/Event Hub connection info:

```text
GET /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/sources/{sourceId}/connection
```

Returns `fullyQualifiedNamespace`, `eventHubName`, and `accessKeys` (primary/secondary keys and connection strings). **Only supported for Custom Endpoint sources.**

### Get Definition (Alternative)

```text
POST /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/getDefinition
```

Returns the full topology as base64-encoded `eventstream.json` (and optionally
`eventstreamProperties.json` and `.platform`). The request can return
`202 Accepted`; poll the `Location` header until the long-running operation
completes.

**Decode workflow**:
1. Extract the `payload` field from the `eventstream.json` part
2. Base64-decode it to get the topology JSON
3. Parse to inspect sources, destinations, operators, and streams

### Topology Inspection Patterns

After decoding `eventstream.json`, the topology is a graph with four arrays:

| Array | What It Contains |
|-------|-----------------|
| `sources[]` | Ingestion entry points — each has `name`, `type`, `properties` |
| `destinations[]` | Output sinks — each has `name`, `type`, `properties`, `inputNodes` |
| `operators[]` | Transformation nodes — each has `name`, `type`, `properties`, `inputNodes` |
| `streams[]` | Data streams — DefaultStream (auto) or DerivedStream (from operators) |

### Tracing Data Flow

To trace the path from source to destination:
1. Start at a `source` node
2. Find the `stream` whose `inputNodes` references that source name
3. Find `operators` whose `inputNodes` reference that stream name
4. Follow the chain of operators via their `inputNodes`
5. Find `destinations` or `DerivedStream` nodes at the end of the chain

---

## Monitoring Eventstream Health

### Node Status via Topology API (Recommended)

```text
GET /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/topology
```

Each node in the response includes a `status` field (`Running`, `Paused`, `Error`) and an `error` object with `errorCode`, `errorMessage`, and `errorDetails` when unhealthy. This is the fastest way to check pipeline health without decoding definitions.

### Operational Control — Pause and Resume

These endpoints mutate runtime state. A read-only consumer should inspect status
through topology and route pause/resume requests to `eventstream-cli` authoring
mode.

Pause is bodyless:

```http
POST /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/pause
```

Resume requires a JSON request body:

```http
POST /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}/resume
Content-Type: application/json

{
  "startType": "WhenLastStopped"
}
```

Pause/resume all sources and destinations. Granular control per source or destination is also available:

```text
POST .../sources/{sourceId}/pause
POST .../sources/{sourceId}/resume
POST .../destinations/{destinationId}/pause
POST .../destinations/{destinationId}/resume
```

Resume operations require `startType` (`Now`, `WhenLastStopped`, or
`CustomTime`); `CustomTime` also requires `customStartDateTime`. These write
operations require `Eventstream.ReadWrite.All` or `Item.ReadWrite.All`.

### Eventstream Properties Check

```text
GET /v1/workspaces/{workspaceId}/eventstreams/{eventstreamId}
```

Verify the Eventstream exists and check its metadata. A missing or errored response indicates the item may have been deleted or the workspace is unavailable.

### EventstreamProperties Inspection

Decode `eventstreamProperties.json` from the definition to check:

| Property | Description | Monitoring Use |
|----------|-------------|----------------|
| `retentionTimeInDays` | Event retention period (1–90 days) | Verify retention meets compliance requirements |
| `eventThroughputLevel` | `Low`, `Medium`, or `High` | Check if throughput tier matches expected load |

---

## Source and Destination Status

### Source Validation

Use the Topology API (`GET .../topology`) to check per-source status and errors, or validate from the decoded definition:

For each source in the topology:

| Check | What to Verify |
|-------|---------------|
| `type` is valid | Must be one of the 25 API-supported type enums (see AUTHORING-CORE) |
| `dataConnectionId` exists | Cloud connection GUID must be valid and accessible |
| `consumerGroupName` set | Required for Event Hub, IoT Hub, Kafka-based sources |
| `inputSerialization` configured | Encoding must match the source data format |

### Destination Validation

For each destination in the decoded topology:

| Check | What to Verify |
|-------|---------------|
| `type` is valid | Must be `Lakehouse`, `Eventhouse`, `Activator`, or `CustomEndpoint` |
| `workspaceId` / `itemId` resolve | Target item must exist and be accessible |
| `inputNodes` connected | Must reference a valid upstream node name |
| Eventhouse direct ingestion | `connectionName` and `mappingRuleName` must be set |

### Counting Topology Nodes

Parse the decoded topology JSON to summarize the Eventstream's complexity:

| Metric | How to Calculate |
|--------|-----------------|
| Source count | `len(sources)` |
| Destination count | `len(destinations)` |
| Operator count | `len(operators)` |
| Stream count | `len(streams)` |
| Total nodes | Sum of above |

---

## Integration with Downstream Analytics

### Eventstream → Eventhouse (KQL)

When an Eventstream routes data to an Eventhouse destination:
- Data lands in a KQL table in the specified KQL Database
- Use the `eventhouse-cli` skill to query the data with KQL
- For direct ingestion mode, check the data mapping and ingestion health via KQL management commands

### Eventstream → Lakehouse

When an Eventstream routes data to a Lakehouse destination:
- Data lands as a Delta table in the specified Lakehouse
- Use the `sqldw-consumption-cli` skill to query via SQL endpoint
- Or use the `spark-consumption-cli` skill for interactive Spark exploration
- Check `minimumRows` and `maximumDurationInSeconds` to understand batching behaviour

### Eventstream → Activator

When routed to a Fabric Activator:
- Events trigger Activator rules and actions
- Monitor via the Activator item in the Fabric portal

### DerivedStreams and Real-Time Hub

DerivedStreams are published to the Real-Time Hub and can be:
- Subscribed to by other Eventstreams
- Consumed by external Kafka clients
- Monitored for availability and throughput

---

## Gotchas and Troubleshooting Reference

| # | Symptom | Cause | Fix |
|---|---------|-------|-----|
| 1 | List Eventstreams returns empty | Wrong workspace ID or no Contributor role | Verify workspace ID; check RBAC |
| 2 | Get Definition returns `202 Accepted` | Long-running operation in progress | Poll the `Location` header URL |
| 3 | Decoded topology has empty arrays | Eventstream created but not yet configured | Expected for newly created Eventstreams — add sources/destinations via Update Definition |
| 4 | `continuationUri` in list response | More results available | Follow pagination links |
| 5 | Source type not recognized | Preview source created via UI | Preview sources don't appear in API type enum — topology will still decode but type may be unfamiliar |
| 6 | Destination shows `inputNodes: []` | Destination not wired to any stream/operator | Eventstream topology may be incomplete — check in UI |
| 7 | Eventhouse destination data not appearing | Ingestion mapping mismatch | Check `mappingRuleName` and verify table schema matches |
| 8 | Lakehouse destination data delayed | Batching thresholds not met | Check `minimumRows` and `maximumDurationInSeconds` — data is buffered until one threshold is reached |
| 9 | `401 Unauthorized` on API call | Token expired or wrong audience | Re-acquire token with `--resource https://api.fabric.microsoft.com` |
| 10 | `429 Too Many Requests` | API rate limiting | Implement exponential backoff; respect `Retry-After` header |

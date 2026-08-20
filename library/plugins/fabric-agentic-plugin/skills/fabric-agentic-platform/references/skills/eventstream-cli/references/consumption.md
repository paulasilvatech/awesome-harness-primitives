<!-- Mode reference for the `eventstream-cli` skill. Loaded on demand from `skills/eventstream-cli/SKILL.md` when the request matches the `consumption` mode. -->

> **SCOPE BOUNDARY -- READ-ONLY (mandatory)**
> This mode may inspect Eventstream items, definitions, runtime topology, health,
> retention, throughput and connection metadata. It must not create, update,
> delete, pause or resume Eventstreams. If the user asks for a mutation, switch
> explicitly to `eventstream-cli` authoring mode, read `references/authoring.md`
> before continuing, and do not issue the write from consumption mode.

# eventstream-cli consumption mode -- Eventstream Consumption via CLI

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id] |
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) | |
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) | |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Includes pagination, LRO polling, and rate-limiting patterns |
| Gotchas, Best Practices & Troubleshooting | [COMMON-CORE.md § Gotchas, Best Practices & Troubleshooting](../../../common/COMMON-CORE.md#gotchas-best-practices--troubleshooting) | |
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../../common/COMMON-CLI.md#tool-selection-rationale) | |
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource`**; includes pagination and LRO helpers |
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference | [COMMON-CLI.md § Quick Reference](../../../common/COMMON-CLI.md#quick-reference) | `az rest` template + token audience/tool matrix |
| Listing and Discovering Eventstreams | [EVENTSTREAM-CONSUMPTION-CORE.md § Listing and Discovering Eventstreams](../../../common/EVENTSTREAM-CONSUMPTION-CORE.md#listing-and-discovering-eventstreams) | List, Get, Search across workspaces |
| Inspecting Eventstream Topology | [EVENTSTREAM-CONSUMPTION-CORE.md § Inspecting Eventstream Topology](../../../common/EVENTSTREAM-CONSUMPTION-CORE.md#inspecting-eventstream-topology) | Decode base64 definition → trace graph flow |
| Monitoring Eventstream Health | [EVENTSTREAM-CONSUMPTION-CORE.md § Monitoring Eventstream Health](../../../common/EVENTSTREAM-CONSUMPTION-CORE.md#monitoring-eventstream-health) | Retention and throughput checks |
| Source and Destination Status | [EVENTSTREAM-CONSUMPTION-CORE.md § Source and Destination Status](../../../common/EVENTSTREAM-CONSUMPTION-CORE.md#source-and-destination-status) | Validation checklist for sources and destinations |
| Integration with Downstream Analytics | [EVENTSTREAM-CONSUMPTION-CORE.md § Integration with Downstream Analytics](../../../common/EVENTSTREAM-CONSUMPTION-CORE.md#integration-with-downstream-analytics) | Eventhouse, Lakehouse, Activator, Real-Time Hub |
| Gotchas and Troubleshooting Reference | [EVENTSTREAM-CONSUMPTION-CORE.md § Gotchas and Troubleshooting Reference](../../../common/EVENTSTREAM-CONSUMPTION-CORE.md#gotchas-and-troubleshooting-reference) | 10 common issues with causes and fixes |
| List Eventstreams | [Consumption mode § List Eventstreams](#list-eventstreams) | |
| Inspect Eventstream Topology | [Consumption mode § Inspect Eventstream Topology](#inspect-eventstream-topology) | Decode and explore the graph |
| Get Custom Endpoint Connection String | [Consumption mode § Get Custom Endpoint Connection String](#get-custom-endpoint-connection-string) | Retrieve Kafka/EH connection via Topology API |
| Validate Eventstream Configuration | [Consumption mode § Validate Eventstream Configuration](#validate-eventstream-configuration) | |
| Gotchas, Rules, Troubleshooting | [Consumption mode § Gotchas, Rules, Troubleshooting](#gotchas-rules-troubleshooting) | **MUST DO / AVOID / PREFER** checklists |

---

## List Eventstreams

### List All Eventstreams in a Workspace

```bash
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams" \
  --resource "https://api.fabric.microsoft.com"
```

Returns an array of Eventstream items. Use JMESPath to filter by name:

```bash
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams" \
  --resource "https://api.fabric.microsoft.com" \
  --query "value[?displayName=='my-eventstream']"
```

### Get Eventstream Details

```bash
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams/${EVENTSTREAM_ID}" \
  --resource "https://api.fabric.microsoft.com"
```

---

## Inspect Eventstream Topology

> **Tip**: The Topology API (`GET .../eventstreams/{id}/topology`) returns runtime status, error info, and node IDs without base64 decoding. Prefer it for operational inspection (health checks, connection retrieval). Use `POST .../getDefinition` (below) when you need the full authoring-time graph structure for topology modification.

Retrieve the Eventstream definition and decode it to inspect the full graph topology.

### Step 1: Get the Definition

> **API Note**: The Eventstream Definition API uses `POST .../getDefinition`, not `GET .../definition`. This follows the Fabric Items Definition pattern. See [official docs](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/api-get-eventstream-definition).

```bash
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams/${EVENTSTREAM_ID}/getDefinition" \
  --resource "https://api.fabric.microsoft.com" \
  --body '{}'
```

### Step 2: Decode the Topology

Extract the `eventstream.json` part's `payload` field and base64-decode it:

```bash
# Using jq + base64 (Linux; on macOS use base64 -D instead of -d)
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams/${EVENTSTREAM_ID}/getDefinition" \
  --resource "https://api.fabric.microsoft.com" \
  --body '{}' \
  | jq -r '.definition.parts[] | select(.path=="eventstream.json") | .payload' \
  | base64 -d | jq .
```

```powershell
# PowerShell (Windows)
$def = az rest --method POST `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/eventstreams/$EVENTSTREAM_ID/getDefinition" `
  --resource "https://api.fabric.microsoft.com" `
  --body '{}' | ConvertFrom-Json
$payload = ($def.definition.parts | Where-Object { $_.path -eq 'eventstream.json' }).payload
[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($payload)) | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Step 3: Summarize the Topology

After decoding, count and list each node type:

| Metric | Path in decoded JSON |
|--------|---------------------|
| Sources | `.sources[] \| .name, .type` |
| Destinations | `.destinations[] \| .name, .type` |
| Operators | `.operators[] \| .name, .type` |
| Streams | `.streams[] \| .name, .type` |

---

## Get Custom Endpoint Connection String

The `POST .../getDefinition` endpoint returns **empty properties** for Custom Endpoint sources. To retrieve the Kafka/Event Hub connection info, use the **Topology API** `/connection` endpoint.

> **Important**: This endpoint requires `Eventstream.ReadWrite.All` permission scope (not just Read).

### Step 1: Get the Topology to Find the Source ID

```bash
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams/${EVENTSTREAM_ID}/topology" \
  --resource "https://api.fabric.microsoft.com"
```

From the response, find the Custom Endpoint source node and extract its `id`:

```bash
# Extract the sourceId for a Custom Endpoint source (use name filter if multiple exist)
SOURCE_ID=$(az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams/${EVENTSTREAM_ID}/topology" \
  --resource "https://api.fabric.microsoft.com" \
  | jq -r '[.sources[] | select(.type=="CustomEndpoint")] | if length == 0 then error("No Custom Endpoint sources found in this Eventstream") elif length > 1 then error("Multiple Custom Endpoint sources found — filter by .name") else .[0].id end') \
  || { echo "Failed to resolve Custom Endpoint source ID"; exit 1; }

if [ -z "$SOURCE_ID" ]; then echo "SOURCE_ID is empty — check topology output"; exit 1; fi
```

```powershell
# PowerShell — extract sourceId for Custom Endpoint (fails clearly if multiple exist)
$topology = az rest --method GET `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/eventstreams/$EVENTSTREAM_ID/topology" `
  --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json
$customSources = @($topology.sources | Where-Object { $_.type -eq 'CustomEndpoint' })
if ($customSources.Count -eq 0) { throw "No Custom Endpoint sources found in this Eventstream" }
if ($customSources.Count -gt 1) { throw "Multiple Custom Endpoint sources found. Filter by name: $($customSources.name -join ', ')" }
$sourceId = $customSources[0].id
```

### Step 2: Get the Connection Details

> ⚠️ **Security**: This endpoint returns access keys and connection strings. Get explicit user confirmation before calling it. Redact `primaryKey`, `secondaryKey`, `primaryConnectionString`, and `secondaryConnectionString` from any displayed output unless the user explicitly asks for secret values in a secure context. Avoid logging raw credentials; store securely and rotate as needed.

```bash
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams/${EVENTSTREAM_ID}/sources/${SOURCE_ID}/connection" \
  --resource "https://api.fabric.microsoft.com"
```

```powershell
az rest --method GET `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/eventstreams/$EVENTSTREAM_ID/sources/$sourceId/connection" `
  --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json
```

### Expected Response

```json
{
  "fullyQualifiedNamespace": "namespace.servicebus.windows.net",
  "eventHubName": "es_<guid>",
  "accessKeys": {
    "primaryKey": "...",
    "secondaryKey": "...",
    "primaryConnectionString": "Endpoint=sb://namespace.servicebus.windows.net/;...",
    "secondaryConnectionString": "..."
  }
}
```

### Kafka Producer Configuration

Use the response to configure a Kafka producer:

| Setting | Value |
|---------|-------|
| `bootstrap_servers` | `{fullyQualifiedNamespace}:9093` |
| `topic` | `{eventHubName}` |
| `security_protocol` | `SASL_SSL` |
| `sasl_mechanism` | `PLAIN` |
| `sasl_plain_username` | `$ConnectionString` (fixed literal — not a variable) |
| `sasl_plain_password` | `{primaryConnectionString}` |

> **Limitation**: The `/connection` endpoint is only supported for Custom Endpoint sources (returns Kafka/Event Hub credentials). Other source types (Event Hub, IoT Hub, etc.) store their connection configuration (e.g., `dataConnectionId`, `consumerGroup`) directly in the decoded definition properties.

---

## Validate Eventstream Configuration

Check key configuration aspects of a decoded Eventstream topology:

### Source Validation Checklist

| Check | How |
|-------|-----|
| Source type is API-supported | Compare against 29 known type enums |
| Cloud connection exists | Verify `dataConnectionId` GUID resolves |
| Consumer group set | Required for Event Hub, IoT Hub, Kafka sources |
| Serialization matches source | `inputSerialization.type` = `Json`, `Csv`, or `Avro` |

### Destination Validation Checklist

| Check | How |
|-------|-----|
| Destination type is valid | Must be `Lakehouse`, `Eventhouse`, `Activator`, or `CustomEndpoint` |
| Target item accessible | Verify `workspaceId` + `itemId` resolve via GET |
| Input wired | `inputNodes` array must not be empty |
| Eventhouse direct ingestion | `connectionName` and `mappingRuleName` set |

### EventstreamProperties Validation

Decode `eventstreamProperties.json` and check:
- `retentionTimeInDays` is within 1–90
- `eventThroughputLevel` is `Low`, `Medium`, or `High`

---

## Gotchas, Rules, Troubleshooting

### MUST DO

- **Always pass `--resource https://api.fabric.microsoft.com`** with `az rest` calls
- **Always use JMESPath filtering** to resolve workspace name → ID and item name → ID
- **Always base64-decode** the definition payload before inspecting topology (not needed for the Topology API — that returns JSON directly)
- **For Custom Endpoint connection details, use the Topology API** — `POST .../getDefinition` returns empty properties; call `GET .../topology` to get the sourceId, then `GET .../sources/{sourceId}/connection`
- **Use POST for definition endpoints** — `POST .../getDefinition` (not GET), `POST .../updateDefinition` (not PUT). See [official docs](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/api-get-eventstream-definition).
- **Handle pagination** — check for `continuationUri` in list responses
- **Poll LRO responses** — Get Definition may return `202 Accepted`

### PREFER

- Decode topology JSON into structured output for readable summaries
- Use `jq` (bash) or `ConvertFrom-Json` (PowerShell) for parsing
- Validate configurations before reporting issues to users
- Cross-reference destinations with downstream skills (eventhouse, sqldw, spark)

### AVOID

- Do NOT confuse Eventstream with Eventhouse — they are separate Fabric workloads
- Do NOT hardcode workspace or item IDs — always discover them via the API
- Do NOT assume all source types appear in API enums — preview sources exist only in the UI
- Do NOT modify Eventstream topology with this consumption skill — use `eventstream-cli authoring mode` for writes
- Do NOT attempt to query event data through the Eventstream API — use downstream skills (`eventhouse-cli` consumption mode, `sqldw-cli`) for querying landed data

---

## Examples

> **Platform note** — examples use PowerShell. Always write the JSON body to
> a temp file via `[IO.File]::WriteAllText()` (no BOM) and pass
> `--body "@$file"` to `az rest`, rather than inline `--body "..."` which
> `cmd.exe` can mangle. Use `-Compress` with `ConvertTo-Json` to avoid
> newline issues. The one safe inline exception is `--body '{}'` for empty bodies.
> For large workspaces, check for `continuationUri` in list responses to handle
> pagination.

### Example 1: List All Eventstreams in a Workspace

**Prompt**: "List all Eventstreams in my analytics workspace showing their names and IDs."

```powershell
# 1. Discover workspace ID
$wsId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='analytics'] | [0].id" -o tsv)
if (-not $wsId) { throw "Workspace 'analytics' not found" }

# 2. List Eventstreams (handles pagination)
$allItems = @()
$resp = az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams" `
  --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json
$allItems += $resp.value
while ($resp.continuationUri) {
    $resp = az rest --method get `
      --url $resp.continuationUri `
      --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json
    $allItems += $resp.value
}
$allItems | Select-Object displayName, id, description | Format-Table
```

### Example 2: Inspect Eventstream Topology

**Prompt**: "Show me the topology of my SensorIngestion Eventstream — all sources, operators, and destinations."

```powershell
# 1. Discover workspace + Eventstream IDs
$wsId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='analytics'] | [0].id" -o tsv)
if (-not $wsId) { throw "Workspace 'analytics' not found" }

$esId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='SensorIngestion'] | [0].id" -o tsv)
if (-not $esId) { throw "Eventstream 'SensorIngestion' not found" }

# 2. Get topology (returns JSON directly — no base64 decoding needed)
$topo = az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/topology" `
  --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json

# 3. Summarize nodes (filter nulls from arrays)
Write-Host "Sources:"
@($topo.sources | Where-Object { $_ -ne $null }) | ForEach-Object {
    Write-Host "  - $($_.name) (type: $($_.type), id: $($_.id))"
}
Write-Host "Operators:"
@($topo.operators | Where-Object { $_ -ne $null }) | ForEach-Object {
    Write-Host "  - $($_.name) (type: $($_.type))"
}
Write-Host "Destinations:"
@($topo.destinations | Where-Object { $_ -ne $null }) | ForEach-Object {
    Write-Host "  - $($_.name) (type: $($_.type))"
}
Write-Host "Streams:"
@($topo.streams | Where-Object { $_ -ne $null }) | ForEach-Object {
    Write-Host "  - $($_.name) (type: $($_.type))"
}
```

### Example 3: Check Retention and Throughput Settings

**Prompt**: "What are the retention and throughput settings for my SensorIngestion Eventstream?"

> **Note**: Retention and throughput settings are stored in the `eventstreamProperties.json`
> part of the definition (not `eventstream.json`). If this part is absent, the Eventstream
> uses platform defaults.

```powershell
# 1. Discover workspace + Eventstream IDs
$wsId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='analytics'] | [0].id" -o tsv)
if (-not $wsId) { throw "Workspace 'analytics' not found" }

$esId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items?type=Eventstream" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='SensorIngestion'] | [0].id" -o tsv)
if (-not $esId) { throw "Eventstream 'SensorIngestion' not found" }

# 2. Get definition (handles LRO via Location header)
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)
$ps5 = @{}; if ($PSVersionTable.PSVersion.Major -lt 6) { $ps5.UseBasicParsing = $true }
$response = Invoke-WebRequest @ps5 -Method Post `
  -Uri "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/getDefinition" `
  -Headers @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" } `
  -Body '{}'

if ($response.StatusCode -eq 202) {
    $location = $response.Headers['Location']
    if ($location -is [array]) { $location = $location[0] }
    if (-not $location) { throw "LRO response missing Location header" }
    $ra = $response.Headers['Retry-After']
    if ($ra -is [array]) { $ra = $ra[0] }
    $retryAfter = if ($ra) { [int]$ra } else { 5 }
    $def = $null
    for ($i = 0; $i -lt 12; $i++) {
        Start-Sleep -Seconds $retryAfter
        $poll = Invoke-RestMethod -Uri $location -Headers @{ Authorization = "Bearer $token" }
        if ($poll.status -eq 'Succeeded') {
            $def = Invoke-RestMethod -Uri "$location/result" `
              -Headers @{ Authorization = "Bearer $token" }
            break
        } elseif ($poll.status -in @('Failed', 'Cancelled')) {
            throw "getDefinition LRO $($poll.status): $($poll.error.message)"
        }
    }
    if (-not $def -or -not $def.definition) { throw "getDefinition LRO timed out (last status: $(if ($poll) { $poll.status } else { 'unknown' }))" }
} else {
    $def = $response.Content | ConvertFrom-Json
}

# 3. Decode eventstreamProperties.json part (holds retention + throughput)
$propsPart = $def.definition.parts | Where-Object { $_.path -eq 'eventstreamProperties.json' } | Select-Object -First 1
if ($propsPart) {
    $props = [Text.Encoding]::UTF8.GetString(
      [Convert]::FromBase64String($propsPart.payload)) | ConvertFrom-Json
    Write-Host "Retention: $($props.retentionTimeInDays) days"
    Write-Host "Throughput Level: $($props.eventThroughputLevel)"
} else {
    # Fall back to topology-level properties (older format)
    $esPart = $def.definition.parts | Where-Object { $_.path -eq 'eventstream.json' } | Select-Object -First 1
    if (-not $esPart) { throw "eventstream.json part not found in definition" }
    $topology = [Text.Encoding]::UTF8.GetString(
      [Convert]::FromBase64String($esPart.payload)) | ConvertFrom-Json
    if ($topology.properties.retentionTimeInDays) {
        Write-Host "Retention: $($topology.properties.retentionTimeInDays) days"
    } else {
        Write-Host "Retention: (platform default — not explicitly configured)"
    }
    if ($topology.properties.eventThroughputLevel) {
        Write-Host "Throughput Level: $($topology.properties.eventThroughputLevel)"
    } else {
        Write-Host "Throughput Level: (platform default — not explicitly configured)"
    }
}
```

### Example 4: Get Custom Endpoint Connection Metadata

**Prompt**: "Get the Kafka connection metadata for the Custom Endpoint source in my SensorIngestion Eventstream."

> **Security**: The connection endpoint returns access keys. Get user confirmation before
> calling it and avoid logging raw credentials.

```powershell
# 1. Discover workspace + Eventstream IDs (omitted for brevity)

# 2. Get topology to find Custom Endpoint source ID
$topo = az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/topology" `
  --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json

$ceSource = @($topo.sources | Where-Object { $_.type -eq 'CustomEndpoint' }) | Select-Object -First 1
if (-not $ceSource) { throw "No CustomEndpoint source found in this Eventstream" }
$sourceId = $ceSource.id

# 3. Get connection metadata
$conn = az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/sources/$sourceId/connection" `
  --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json

Write-Host "Fully Qualified Namespace: $($conn.fullyQualifiedNamespace)"
Write-Host "Event Hub Name:            $($conn.eventHubName)"
Write-Host "Kafka Bootstrap Server:    $($conn.fullyQualifiedNamespace):9093"
```

### Example 5: Validate Eventstream Configuration

**Prompt**: "Check if my SensorIngestion Eventstream has any configuration issues."

```powershell
# 1. Discover workspace + Eventstream IDs (omitted for brevity)

# 2. Get topology
$topo = az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/topology" `
  --resource "https://api.fabric.microsoft.com" | ConvertFrom-Json

# 3. Validate sources
@($topo.sources | Where-Object { $_ -ne $null }) | ForEach-Object {
    $src = $_
    Write-Host "Source: $($src.name) (type: $($src.type))"
    if ($src.properties.dataConnectionId) {
        Write-Host "  Cloud connection: $($src.properties.dataConnectionId)"
    }
    if ($src.type -in @('AzureEventHub','AzureEventHubExtended','AzureIoTHub','ConfluentCloud','ApacheKafka','AmazonMSKKafka') -and
        -not $src.properties.consumerGroupName) {
        Write-Host "  WARNING: No consumer group set (required for $($src.type))"
    }
}

# 4. Validate destinations
@($topo.destinations | Where-Object { $_ -ne $null }) | ForEach-Object {
    $dst = $_
    Write-Host "Destination: $($dst.name) (type: $($dst.type))"
    if (-not $dst.inputNodes -or $dst.inputNodes.Count -eq 0) {
        Write-Host "  WARNING: No input wired — destination will receive no events"
    }
    if ($dst.type -eq 'Eventhouse' -and -not $dst.properties.tableName) {
        Write-Host "  WARNING: No target table configured"
    }
    if ($dst.type -eq 'Eventhouse' -and $dst.properties.dataIngestionMode -eq 'DirectIngestion') {
        if (-not $dst.properties.connectionName -or -not $dst.properties.mappingRuleName) {
            Write-Host "  WARNING: DirectIngestion requires connectionName and mappingRuleName"
        }
    }
}

# 5. Check node count limits
$ceCount = @($topo.sources | Where-Object { $_.type -eq 'CustomEndpoint' }).Count +
           @($topo.destinations | Where-Object { $_.type -eq 'CustomEndpoint' }).Count +
           @($topo.destinations | Where-Object { $_.type -eq 'Eventhouse' -and
             $_.properties.dataIngestionMode -eq 'DirectIngestion' }).Count
Write-Host "CustomEndpoint + DI count: $ceCount / 11 limit"
if ($ceCount -gt 11) {
    Write-Host "WARNING: Exceeds limit of 11 CustomEndpoint + DirectIngestion nodes"
}
```

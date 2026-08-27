<!-- Mode reference for the `eventstream-cli` skill. Loaded on demand from `skills/eventstream-cli/SKILL.md` when the request matches the `authoring` mode. -->

# eventstream-cli authoring mode -- Eventstream Authoring via CLI

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
| Eventstream Resource Model | [EVENTSTREAM-AUTHORING-CORE.md § Eventstream Resource Model](../../../common/EVENTSTREAM-AUTHORING-CORE.md#eventstream-resource-model) | **Read first** — graph-based topology with sources, operators, streams, destinations |
| Source Configuration | [EVENTSTREAM-AUTHORING-CORE.md § Source Configuration](../../../common/EVENTSTREAM-AUTHORING-CORE.md#source-configuration) | 29 API-supported source types with per-source properties |
| Transformation Operators | [EVENTSTREAM-AUTHORING-CORE.md § Transformation Operators](../../../common/EVENTSTREAM-AUTHORING-CORE.md#transformation-operators) | 8 operator types: Filter, Aggregate, GroupBy, Join, ManageFields, Union, Expand, SQL |
| Destination Configuration | [EVENTSTREAM-AUTHORING-CORE.md § Destination Configuration](../../../common/EVENTSTREAM-AUTHORING-CORE.md#destination-configuration) | 4 API-supported destination types with node schema |
| Stream Types | [EVENTSTREAM-AUTHORING-CORE.md § Stream Types](../../../common/EVENTSTREAM-AUTHORING-CORE.md#stream-types) | DefaultStream (auto) and DerivedStream (from operators) |
| Eventstream Lifecycle (REST API) | [EVENTSTREAM-AUTHORING-CORE.md § Eventstream Lifecycle (REST API)](../../../common/EVENTSTREAM-AUTHORING-CORE.md#eventstream-lifecycle-rest-api) | CRUD + Definition endpoints |
| Item Definitions and Deployment | [EVENTSTREAM-AUTHORING-CORE.md § Item Definitions and Deployment](../../../common/EVENTSTREAM-AUTHORING-CORE.md#item-definitions-and-deployment) | Base64 encoding pattern for eventstream.json |
| Gotchas and Limitations | [EVENTSTREAM-AUTHORING-CORE.md § Gotchas and Limitations](../../../common/EVENTSTREAM-AUTHORING-CORE.md#gotchas-and-limitations) | Max 11 custom endpoints, base64 encoding, naming constraints |
| Create an Eventstream | [Authoring mode § Create an Eventstream](#create-an-eventstream) | |
| Deploy Full Topology | [Authoring mode § Deploy Full Topology](#deploy-full-topology) | End-to-end: build topology JSON → base64 encode → submit definition |
| Update Eventstream Topology | [Authoring mode § Update Eventstream Topology](#update-eventstream-topology) | |
| Pause and Resume an Eventstream | [Authoring mode § Pause and Resume an Eventstream](#pause-and-resume-an-eventstream) | Pause is bodyless; resume requires `startType` |
| Delete an Eventstream | [Authoring mode § Delete an Eventstream](#delete-an-eventstream) | |
| Gotchas, Rules, Troubleshooting | [Authoring mode § Gotchas, Rules, Troubleshooting](#gotchas-rules-troubleshooting) | **MUST DO / AVOID / PREFER** checklists |

---

## Create an Eventstream

Create an empty Eventstream item, then configure it with sources, destinations, and operators via the definition API.

### Step 1: Create the Item

```bash
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams" \
  --resource "https://api.fabric.microsoft.com" \
  --headers "Content-Type=application/json" \
  --body '{"displayName": "my-eventstream", "description": "IoT sensor pipeline"}'
```

Save the returned `id` as `EVENTSTREAM_ID`.

### Step 2: Build the Topology

Construct the `eventstream.json` topology with sources, streams, operators, and destinations. Each node references its upstream via `inputNodes`.

Prefer building the JSON programmatically to avoid serialization errors. Key rules:
- The topology must have exactly one DefaultStream — all sources feed into it via `inputNodes`
- Operators reference their input via `inputNodes[].name`
- DerivedStreams require `inputSerialization` in properties
- Destinations reference their input stream or operator

### Step 3: Deploy the Definition

Base64-encode the topology JSON and submit via the definition API. See [Item Definitions and Deployment](../../../common/EVENTSTREAM-AUTHORING-CORE.md#item-definitions-and-deployment) for the full payload structure.

---

## Deploy Full Topology

For deploying a complete Eventstream with topology in a single API call, use the Create Item with Definition endpoint:

```bash
# 1. Build eventstream.json content (topology)
TOPOLOGY_JSON='{"compatibilityLevel":"1.1","sources":[...],"streams":[...],"operators":[...],"destinations":[...]}'

# 2. Build eventstreamProperties.json (optional — controls retention and throughput)
PROPERTIES_JSON='{"retentionTimeInDays":1,"eventThroughputLevel":"Low"}'

# 3. Base64-encode both (no line wraps)
TOPOLOGY_B64=$(echo -n "$TOPOLOGY_JSON" | base64 -w 0)
PROPERTIES_B64=$(echo -n "$PROPERTIES_JSON" | base64 -w 0)

# 4. Submit via Items API
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/items" \
  --resource "https://api.fabric.microsoft.com" \
  --headers "Content-Type=application/json" \
  --body "{
    \"displayName\": \"my-eventstream\",
    \"type\": \"Eventstream\",
    \"definition\": {
      \"parts\": [
        {
          \"path\": \"eventstream.json\",
          \"payload\": \"${TOPOLOGY_B64}\",
          \"payloadType\": \"InlineBase64\"
        },
        {
          \"path\": \"eventstreamProperties.json\",
          \"payload\": \"${PROPERTIES_B64}\",
          \"payloadType\": \"InlineBase64\"
        }
      ]
    }
  }"
```

> **Note:** If `eventstreamProperties.json` is omitted, the API applies defaults: `retentionTimeInDays: 1`, `eventThroughputLevel: "Low"`. Include it explicitly to control retention (1–90 days) and throughput.

> On Windows (PowerShell), use `[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json))` for base64 encoding.

---

## Update Eventstream Topology

1. **Get current definition**: `POST /v1/workspaces/{wsId}/eventstreams/{esId}/getDefinition`
2. **Decode** the `eventstream.json` payload from base64
3. **Modify** the topology (add/remove/update nodes)
4. **Re-encode** to base64
5. **Submit**: `POST /v1/workspaces/{wsId}/eventstreams/{esId}/updateDefinition`

> **API Note**: The Eventstream Definition APIs use `POST` with action verbs (`getDefinition`, `updateDefinition`), not `GET`/`PUT` on a `/definition` resource. This follows the Fabric Items Definition pattern. See [official docs](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/api-get-eventstream-definition).

The Update Definition API returns `202 Accepted` for long-running operations. Poll the `Location` header URL until completion.

### Adding a Filter Operator

> **⚠️ CRITICAL**: Filter operator conditions use **nested objects** for `column` and `value` — NOT bare strings. Using `"column": "temperature"` instead of the object form below will cause a silent API rejection.

```json
{
  "name": "FilterHighTemp",
  "type": "Filter",
  "inputNodes": [{"name": "my-stream"}],
  "properties": {
    "conditions": [{
      "column": {
        "node": null,
        "columnName": "temperature",
        "columnPath": null,
        "expressionType": "ColumnReference"
      },
      "operatorType": "GreaterThan",
      "value": {
        "dataType": "Float",
        "value": "30.0",
        "expressionType": "Literal"
      }
    }]
  }
}
```

**Required structure for ALL operator condition fields:**
- `column` → object with `{node, columnName, columnPath, expressionType: "ColumnReference"}`
- `value` → object with `{dataType, value, expressionType: "Literal"}`
- `operatorType` → string: `Equals`, `NotEquals`, `GreaterThan`, `GreaterThanOrEquals`, `LessThan`, `LessThanOrEquals`, `Contains`, `DoesNotContain`, `StartsWith`, `DoesNotStartWith`, `EndsWith`, `DoesNotEndWith`, `IsEmpty`, `IsNull`, `IsNotNull`, `IsNotNullOrEmpty`
- `dataType` → `BigInt`, `Float`, `Nvarchar(max)`, `DateTime`, `Bit`

This same nested-object pattern applies to **all operators** that reference columns (Filter, Aggregate, GroupBy, Join, ManageFields).

---

## Pause and Resume an Eventstream

Pause requests are bodyless:

```powershell
az rest --method post `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/eventstreams/$EVENTSTREAM_ID/pause" `
  --resource "https://api.fabric.microsoft.com"
```

Resume requests require a JSON body with `startType`. Use `WhenLastStopped` to
continue from the last stopped position:

```powershell
$resumeBodyPath = Join-Path ([IO.Path]::GetTempPath()) "eventstream-resume.json"
$resumeBody = @{ startType = "WhenLastStopped" } | ConvertTo-Json -Compress
[IO.File]::WriteAllText($resumeBodyPath, $resumeBody, [Text.UTF8Encoding]::new($false))
try {
  az rest --method post `
    --url "https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/eventstreams/$EVENTSTREAM_ID/resume" `
    --resource "https://api.fabric.microsoft.com" `
    --headers "Content-Type=application/json" `
    --body "@$resumeBodyPath"
} finally {
  Remove-Item $resumeBodyPath -ErrorAction SilentlyContinue
}
```

Valid `startType` values are `Now`, `WhenLastStopped`, and `CustomTime`.
`CustomTime` also requires `customStartDateTime` in UTC
(`YYYY-MM-DDTHH:mm:ssZ`). Source- and destination-level controls use
`.../sources/{sourceId}/pause|resume` and
`.../destinations/{destinationId}/pause|resume`; node-level resume requests use
the same required body. Read the runtime topology after the call and confirm the
supported nodes reached `Paused` or `Running`.

---

## Delete an Eventstream

```bash
az rest --method DELETE \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventstreams/${EVENTSTREAM_ID}" \
  --resource "https://api.fabric.microsoft.com"
```

Returns `200 OK` on success.

---

## Gotchas, Rules, Troubleshooting

### MUST DO

- **Always base64-encode** the `eventstream.json` payload before submitting definitions
- **Always pass `--resource https://api.fabric.microsoft.com`** with `az rest` calls
- **Always use JMESPath filtering** to resolve workspace name → ID and item name → ID
- **Always use nested objects for operator column/value references** — `"column": {"columnName": "x", "expressionType": "ColumnReference", ...}`, never `"column": "x"` (API rejects bare strings silently)
- **Exactly one DefaultStream per topology** — all sources connect to it (the API rejects multiple DefaultStreams)
- **Poll LRO responses** — Update Definition returns `202 Accepted` with a `Location` header
- **Send a `startType` body on every resume request** — pause is bodyless, but resume without `startType` fails

### PREFER

- Build topology JSON programmatically rather than manual string construction
- Use `SampleData` source type for testing and prototyping
- Set `retentionTimeInDays` explicitly rather than relying on defaults
- Validate cloud connections before referencing them in source configurations
- When a source requires a `dataConnectionId` (e.g. `AzureEventHub`, `AzureIoTHub`, `AzureServiceBus`, `AzureSQLDBCDC`, `MySQLCDC`, `Mqtt`, `SolacePubSub`, most non-`SampleData`/`CustomEndpoint` sources) and the user has not supplied one, first list existing connections tenant-wide with `az rest --method get --url "https://api.fabric.microsoft.com/v1/connections" --resource "https://api.fabric.microsoft.com"` (paginate via `continuationToken`; note the endpoint is tenant-scoped and does not expose workspace association, so filter client-side by `connectionDetails.type` and — where useful — `displayName`) and reuse a matching connection; only ask the user for a `dataConnectionId` if no suitable connection exists
- Use DerivedStreams to make operator output available in Real-Time Hub

### AVOID

- Do NOT use raw JSON in the definition payload — it must be base64-encoded
- Do NOT use underscores or dots in Eventstream display names (breaks SQL operator)
- Do NOT use hyphens, underscores, dots, or spaces in **user-defined** topology node names (sources, operators, DerivedStreams, destinations) — only alphanumeric PascalCase is allowed (e.g., use `FilterTemperature` not `filter-temperature` or `filter_temperature`). Exception: DefaultStream names are auto-generated by the platform as `{eventstreamName}-stream` and may contain hyphens — do not rename them
- Do NOT exceed 11 combined CustomEndpoint sources and CustomEndpoint/Eventhouse-direct-ingestion destinations
- Do NOT confuse Eventstream with Eventhouse — they are separate Fabric workloads
- Do NOT hardcode workspace or item IDs — always discover them via the API

---

## Examples

> **Platform note** — examples use PowerShell. Always write the JSON body to
> a temp file via `[IO.File]::WriteAllText()` (no BOM) and pass
> `--body "@$file"` to `az rest`, rather than inline `--body "..."` which
> `cmd.exe` can mangle. Use `-Compress` with `ConvertTo-Json` to avoid
> newline issues. The one safe inline exception is `--body '{}'` for empty bodies.

### Example 1: Create an Eventstream with a Source

**Prompt**: "Create an Eventstream called SensorIngestion in my dev workspace with a sample data source."

```powershell
# 1. Discover workspace ID
$wsId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='dev'] | [0].id" -o tsv)
if (-not $wsId) { throw "Workspace 'dev' not found" }

# 2. Create empty Eventstream
$esBody = @{ displayName = "SensorIngestion"; description = "IoT sensor pipeline" } | ConvertTo-Json -Compress
$bodyFile = Join-Path ([IO.Path]::GetTempPath()) "es_create.json"
[IO.File]::WriteAllText($bodyFile, $esBody, [System.Text.UTF8Encoding]::new($false))
$created = az rest --method post `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams" `
  --resource "https://api.fabric.microsoft.com" `
  --headers "Content-Type=application/json" `
  --body "@$bodyFile" | ConvertFrom-Json

# 3. Get the created Eventstream ID from response
$esId = $created.id
if (-not $esId) { throw "Eventstream creation did not return an ID" }

# 4. Build topology — DefaultStream uses inputNodes (not parentName)
$topology = @{
    compatibilityLevel = "1.0"
    sources = @(@{
        name = "SampleSource"
        type = "SampleData"
        properties = @{ type = "Bicycles" }
    })
    streams = @(@{
        name = "SensorIngestion-stream"
        type = "DefaultStream"
        properties = @{}
        inputNodes = @(@{ name = "SampleSource" })
    })
    operators = @()
    destinations = @()
}
$topologyJson = $topology | ConvertTo-Json -Depth 10 -Compress
$topologyB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($topologyJson))

# 5. Deploy definition
$defBody = @{
    definition = @{
        parts = @(@{
            path = "eventstream.json"
            payload = $topologyB64
            payloadType = "InlineBase64"
        })
    }
} | ConvertTo-Json -Depth 5 -Compress
$defFile = Join-Path ([IO.Path]::GetTempPath()) "es_def.json"
[IO.File]::WriteAllText($defFile, $defBody, [System.Text.UTF8Encoding]::new($false))
# updateDefinition returns 202 Accepted (LRO). Use Invoke-WebRequest to capture headers.
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)
$ps5 = @{}; if ($PSVersionTable.PSVersion.Major -lt 6) { $ps5.UseBasicParsing = $true }
$response = Invoke-WebRequest @ps5 -Method Post `
  -Uri "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/updateDefinition" `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType "application/json; charset=utf-8" `
  -Body (Get-Content $defFile -Raw -Encoding UTF8)

if ($response.StatusCode -eq 202) {
    $location = $response.Headers['Location']
    if ($location -is [array]) { $location = $location[0] }
    if (-not $location) { throw "LRO response missing Location header" }
    $ra = $response.Headers['Retry-After']
    if ($ra -is [array]) { $ra = $ra[0] }
    $retryAfter = if ($ra) { [int]$ra } else { 5 }
    $succeeded = $false
    for ($i = 0; $i -lt 12; $i++) {
        Start-Sleep -Seconds $retryAfter
        $poll = Invoke-RestMethod -Uri $location -Headers @{ Authorization = "Bearer $token" }
        if ($poll.status -eq 'Succeeded') { $succeeded = $true; Write-Host "Update succeeded"; break }
        elseif ($poll.status -in @('Failed', 'Cancelled')) {
            throw "updateDefinition LRO $($poll.status): $($poll.error.message)"
        }
    }
    if (-not $succeeded) { throw "updateDefinition LRO timed out" }
}
```

### Example 2: Add a Filter Operator with a DerivedStream

**Prompt**: "Add a filter to my SensorIngestion Eventstream that keeps only events where No_Bikes > 5 and expose the filtered output as a DerivedStream."

> **Important**: Adding a Filter operator node alone does not redirect the DefaultStream.
> To make the filtered output consumable, wire a DerivedStream (or destination) to the
> filter's output via `inputNodes`.

```powershell
# 1. Discover workspace + Eventstream IDs
$wsId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='dev'] | [0].id" -o tsv)
if (-not $wsId) { throw "Workspace 'dev' not found" }

$esId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='SensorIngestion'] | [0].id" -o tsv)
if (-not $esId) { throw "Eventstream 'SensorIngestion' not found" }

# 2. Get current definition (handles LRO via Location header)
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

# 3. Decode existing topology
$esPart = $def.definition.parts | Where-Object { $_.path -eq 'eventstream.json' } | Select-Object -First 1
if (-not $esPart) { throw "eventstream.json part not found in definition" }
$topology = [Text.Encoding]::UTF8.GetString(
  [Convert]::FromBase64String($esPart.payload)) | ConvertFrom-Json

# 4. Add Filter operator (PascalCase name — no underscores or hyphens)
#    Column: expressionType + columnName; Value: expressionType + dataType + value
$filter = @{
    name = "FilterLowBikes"
    type = "Filter"
    inputNodes = @(@{ name = "SensorIngestion-stream" })
    properties = @{
        conditions = @(@{
            operatorType = "GreaterThan"
            column = @{
                expressionType = "ColumnReference"
                node = $null
                columnName = "No_Bikes"
                columnPath = $null
            }
            value = @{
                expressionType = "Literal"
                dataType = "BigInt"
                value = "5"
            }
        })
    }
}
$existingOps = @($topology.operators | Where-Object { $_ -ne $null })
$topology.operators = $existingOps + @($filter)

# 5. Add DerivedStream wired to filter output (makes filtered data available)
$derivedStream = @{
    name = "FilteredOutput"
    type = "DerivedStream"
    properties = @{
        inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } }
    }
    inputNodes = @(@{ name = "FilterLowBikes" })
}
$existingStreams = @($topology.streams | Where-Object { $_ -ne $null })
$topology.streams = $existingStreams + @($derivedStream)

# 6. Re-encode and update
$topologyJson = $topology | ConvertTo-Json -Depth 10 -Compress
$topologyB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($topologyJson))
$esPart.payload = $topologyB64

$defBody = @{ definition = @{ parts = $def.definition.parts } } | ConvertTo-Json -Depth 5 -Compress
$defFile = Join-Path ([IO.Path]::GetTempPath()) "es_def.json"
[IO.File]::WriteAllText($defFile, $defBody, [System.Text.UTF8Encoding]::new($false))
# updateDefinition returns 202 Accepted (LRO). Use Invoke-WebRequest to capture headers.
$ps5 = @{}; if ($PSVersionTable.PSVersion.Major -lt 6) { $ps5.UseBasicParsing = $true }
$response = Invoke-WebRequest @ps5 -Method Post `
  -Uri "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId/updateDefinition" `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType "application/json; charset=utf-8" `
  -Body (Get-Content $defFile -Raw -Encoding UTF8)

if ($response.StatusCode -eq 202) {
    $location = $response.Headers['Location']
    if ($location -is [array]) { $location = $location[0] }
    if (-not $location) { throw "LRO response missing Location header" }
    $ra = $response.Headers['Retry-After']
    if ($ra -is [array]) { $ra = $ra[0] }
    $retryAfter = if ($ra) { [int]$ra } else { 5 }
    $succeeded = $false
    for ($i = 0; $i -lt 12; $i++) {
        Start-Sleep -Seconds $retryAfter
        $poll = Invoke-RestMethod -Uri $location -Headers @{ Authorization = "Bearer $token" }
        if ($poll.status -eq 'Succeeded') { $succeeded = $true; Write-Host "Update succeeded"; break }
        elseif ($poll.status -in @('Failed', 'Cancelled')) {
            throw "updateDefinition LRO $($poll.status): $($poll.error.message)"
        }
    }
    if (-not $succeeded) { throw "updateDefinition LRO timed out" }
}
```

### Example 3: Deploy Full Topology (Create with Inline Definition)

**Prompt**: "Create a complete Eventstream called EventPipeline with a Custom Endpoint source, a filter for high-value events, and a DerivedStream for the filtered output."

> **Note**: This uses the Fabric Items API (`POST /items`) to create the Eventstream with its
> definition in a single call, rather than create-then-update.

```powershell
# 1. Discover workspace ID
$wsId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='dev'] | [0].id" -o tsv)
if (-not $wsId) { throw "Workspace 'dev' not found" }

# 2. Build complete topology with filter + DerivedStream
$topology = @{
    compatibilityLevel = "1.0"
    sources = @(@{
        name = "CustomSource"
        type = "CustomEndpoint"
        properties = @{}
    })
    streams = @(
        @{
            name = "EventPipeline-stream"
            type = "DefaultStream"
            properties = @{}
            inputNodes = @(@{ name = "CustomSource" })
        }
        @{
            name = "FilteredEvents"
            type = "DerivedStream"
            properties = @{
                inputSerialization = @{ type = "Json"; properties = @{ encoding = "UTF8" } }
            }
            inputNodes = @(@{ name = "FilterPremium" })
        }
    )
    operators = @(@{
        name = "FilterPremium"
        type = "Filter"
        inputNodes = @(@{ name = "EventPipeline-stream" })
        properties = @{
            conditions = @(@{
                operatorType = "GreaterThan"
                column = @{
                    expressionType = "ColumnReference"
                        node = $null
                        columnName = "Amount"
                        columnPath = $null
                    }
                value = @{
                    expressionType = "Literal"
                    dataType = "BigInt"
                    value = "100"
                }
            })
        }
    })
    destinations = @()
}

# 3. Create with inline definition (single API call)
$topologyJson = $topology | ConvertTo-Json -Depth 10 -Compress
$topologyB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($topologyJson))

$body = @{
    displayName = "EventPipeline"
    type = "Eventstream"
    definition = @{
        parts = @(@{
            path = "eventstream.json"
            payload = $topologyB64
            payloadType = "InlineBase64"
        })
    }
} | ConvertTo-Json -Depth 5 -Compress
$bodyFile = Join-Path ([IO.Path]::GetTempPath()) "es_create_full.json"
[IO.File]::WriteAllText($bodyFile, $body, [System.Text.UTF8Encoding]::new($false))

# Create-with-definition returns 202 Accepted (LRO). Use Invoke-WebRequest to capture headers.
$token = (az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv)
$ps5 = @{}; if ($PSVersionTable.PSVersion.Major -lt 6) { $ps5.UseBasicParsing = $true }
$response = Invoke-WebRequest @ps5 -Method Post `
  -Uri "https://api.fabric.microsoft.com/v1/workspaces/$wsId/items" `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType "application/json; charset=utf-8" `
  -Body (Get-Content $bodyFile -Raw -Encoding UTF8)

if ($response.StatusCode -eq 202) {
    $location = $response.Headers['Location']
    if ($location -is [array]) { $location = $location[0] }
    if (-not $location) { throw "LRO response missing Location header" }
    $ra = $response.Headers['Retry-After']
    if ($ra -is [array]) { $ra = $ra[0] }
    $retryAfter = if ($ra) { [int]$ra } else { 10 }
    $succeeded = $false
    for ($i = 0; $i -lt 12; $i++) {
        Start-Sleep -Seconds $retryAfter
        $poll = Invoke-RestMethod -Uri $location -Headers @{ Authorization = "Bearer $token" }
        if ($poll.status -eq 'Succeeded') { $succeeded = $true; Write-Host "Create succeeded"; break }
        elseif ($poll.status -in @('Failed', 'Cancelled')) {
            throw "Create LRO $($poll.status): $($poll.error.message)"
        }
    }
    if (-not $succeeded) { throw "Create LRO timed out" }
} else {
    Write-Host "Created: $(($response.Content | ConvertFrom-Json).displayName)"
}
```

### Example 4: Delete an Eventstream

**Prompt**: "Delete the SensorIngestion Eventstream from my dev workspace."

```powershell
# 1. Discover workspace + Eventstream IDs
$wsId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='dev'] | [0].id" -o tsv)
if (-not $wsId) { throw "Workspace 'dev' not found" }

$esId = (az rest --method get `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams" `
  --resource "https://api.fabric.microsoft.com" `
  --query "value[?displayName=='SensorIngestion'] | [0].id" -o tsv)
if (-not $esId) { throw "Eventstream 'SensorIngestion' not found" }

# 2. Delete
az rest --method delete `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$wsId/eventstreams/$esId" `
  --resource "https://api.fabric.microsoft.com"
```

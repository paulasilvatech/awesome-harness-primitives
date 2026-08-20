# Authoring CLI Quick Reference

Concise `az rest` invocation patterns for Dataflows Gen2 authoring, base64 helpers, definition manipulation, and agent tips. For full API patterns and M code structure, see [DATAFLOWS-AUTHORING-CORE.md](../../../../common/DATAFLOWS-AUTHORING-CORE.md). For full reusable scripts, see [authoring-script-templates.md](authoring-script-templates.md).

All examples assume reusable connection variables are set:

```bash
WS_ID="<workspaceId>"
DF_ID="<dataflowId>"
API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"
```

> **Cross-shell `--body` rule** — bash snippets below use inline `--body "{...}"` for brevity, but
> on **Windows / PowerShell** that pattern breaks: `az.exe` is launched through `cmd.exe`'s
> argument parser, which mangles embedded quotes and corrupts base64 payloads. For any non-trivial
> body (anything with quotes, newlines, or base64), write the JSON to a temp file and pass
> `--body "@<path>"`. PowerShell-safe write that avoids a UTF-8 BOM:
> `[IO.File]::WriteAllText("$env:TEMP\body.json", $json, [Text.UTF8Encoding]::new($false))`.
> Full PowerShell create template (workload-specific `/dataflows` endpoint, no `type` field needed):
> [authoring-script-templates.md § PowerShell — Create Dataflow with Definition](authoring-script-templates.md#powershell--create-dataflow-with-definition).

## Core Authoring via CLI

### Create Dataflow (Empty)

```bash
az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows" \
  --body '{"displayName":"MyDataflow","description":"Sales ETL dataflow"}'
```

### Create Dataflow (With Definition)

```bash
# Prepare definition parts (base64-encode each file)
QM_B64=$(cat queryMetadata.json | base64 -w0)
MASHUP_B64=$(cat mashup.pq | base64 -w0)
PLATFORM_B64=$(cat .platform | base64 -w0)

az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows" \
  --body "{
    \"displayName\": \"MyDataflow\",
    \"definition\": {
      \"parts\": [
        {\"path\":\"queryMetadata.json\",\"payload\":\"$QM_B64\",\"payloadType\":\"InlineBase64\"},
        {\"path\":\"mashup.pq\",\"payload\":\"$MASHUP_B64\",\"payloadType\":\"InlineBase64\"},
        {\"path\":\".platform\",\"payload\":\"$PLATFORM_B64\",\"payloadType\":\"InlineBase64\"}
      ]
    }
  }"
```

### Get Definition

> **⚠ LRO caveat:** `getDefinition` can return **202 + Location** (the body is empty on the initial response) instead of an inline 200. The one-liner below only works for the synchronous case. For production code, use the LRO-aware curl pattern in [Validate All Connections in a Dataflow](#validate-all-connections-in-a-dataflow-pre-refresh-check) below, or copy the [Fabric LRO Polling Pattern](authoring-script-templates.md#fabric-lro-polling-pattern) bash branch into your script.

```bash
# POST (not GET!) — happy-path one-liner; 200 only. See LRO caveat above.
az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition"
```

### Preview Before Save (executeQuery)

Preview a candidate Power Query M document against the dataflow's bound connections **before** persisting via `updateDefinition`. Surfaces syntax / source / credential errors at authoring time. Full bootstrap branch + auto-wrap rule + Arrow handling: [mashup-preview.md](mashup-preview.md). Full recipe + Arrow → CSV: [dataflows-cli consumption mode § Query Evaluation](../consumption.md#query-evaluation).

```bash
# customMashupDocument MUST be a complete `section Section1; ... shared X = ...;` doc.
# QueryName MUST match a `shared` member in the document.
# Cap preview cost: include Table.FirstN / TOP N — strip before saving.

QUERY_NAME="Customers"
M_DOC='section Section1;
shared Customers = let
    Source = Sql.Database("srv","db"),
    T = Source{[Schema="dbo", Item="Customers"]}[Data],
    Limited = Table.FirstN(T, 100)
in Limited;'

# executeQuery returns raw Apache Arrow IPC bytes (NOT a JSON envelope) via az rest.
# Pass --output-file so az captures the binary cleanly; failures are embedded as
# {"Error":"..."} inside the stream and HTTP 200 alone does NOT mean success.
jq -n --arg q "$QUERY_NAME" --arg m "$M_DOC" \
  '{QueryName: $q, customMashupDocument: $m}' > preview-req.json

az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/executeQuery" \
  --body @preview-req.json \
  --output-file preview.arrow

if grep -q '"Error":"' preview.arrow; then
  echo "✗ Preview failed (embedded source error):"
  python3 -c "import re,sys; raw=open(sys.argv[1],'rb').read().decode('utf-8','replace'); m=re.search(r'\\{\"Error\":\"[^\"]+\"\\}', raw); print(m.group(0) if m else '(marker present, JSON not parsed)')" preview.arrow
  exit 1
fi
echo "✓ Preview OK — $(wc -c < preview.arrow) bytes captured."
```

> **Bootstrap (new credentialed dataflow)**: bind connections via a minimal `updateDefinition` save **before** previewing credentialed M — [mashup-preview.md § Bootstrap branch](mashup-preview.md#bootstrap-branch--new-dataflow--new-credentialed-source).

### Update Definition

```bash
# Always send all 3 parts — full replacement
az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition?updateMetadata=true" \
  --body @definition.json
```

### Delete Dataflow

```bash
az rest --method delete \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID"
```

### Trigger Refresh (Simple)

```bash
# jobType MUST be "Refresh" for dataflows. "Pipeline" returns 400 InvalidJobType.
az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances?jobType=Refresh" \
  --headers "Content-Length=0"
```

### Trigger Refresh (With Parameters)

```bash
az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances?jobType=Refresh" \
  --body '{
    "executionData": {"executeOption": "ApplyChangesIfNeeded"},
    "parameters": [
      {"name":"ServerName","value":"prod.database.windows.net","type":"Automatic"},
      {"name":"StartDate","value":"2025-01-01","type":"Automatic"}
    ]
  }'
```

### Rename Dataflow (Properties Only)

```bash
az rest --method patch \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID" \
  --body '{"displayName":"RenamedDataflow","description":"Updated description"}'
```

## Connection Discovery and Validation

> **Critical**: Always validate all connection IDs before triggering refresh. Nonexistent connections cause cryptic refresh failures.

### List All Connections

```bash
# List all accessible connections
az rest --method get \
  --resource "$RESOURCE" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[].{id:id, name:displayName, type:connectionDetails.type}" -o json
```

### Find Connection by Name

```bash
# Find a connection by display name (may return multiple results)
CONN_NAME="MyDatabase"
az rest --method get \
  --resource "$RESOURCE" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[?displayName=='$CONN_NAME'].{id:id, type:connectionDetails.type}" -o json
```

### Find Connection by Type

```bash
# Find all SQL Server connections
az rest --method get \
  --resource "$RESOURCE" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[?connectionDetails.type=='SQL'].{id:id, name:displayName}" -o json

# Find all Azure Blob Storage connections
az rest --method get \
  --resource "$RESOURCE" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[?connectionDetails.type=='AzureBlobs'].id" -o tsv
```

### Validate a Specific Connection Exists

```bash
CONN_ID="550e8400-e29b-41d4-a716-446655440000"

# List all connections and filter by ID
RESULT=$(az rest --method get \
  --resource "$RESOURCE" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[?id=='$CONN_ID'] | [0] | {id:id, name:displayName, type:connectionDetails.type}" \
  -o json)

if [ "$RESULT" == "null" ] || [ -z "$RESULT" ]; then
  echo "❌ Connection not found: $CONN_ID"
  exit 1
else
  echo "✅ Connection found:"
  echo "$RESULT" | jq '.'
fi
```

### Extract Connection IDs from Dataflow Definition

> **⚠ LRO caveat:** the `az rest --method post .../getDefinition` call below is a happy-path one-liner that only works when the response is synchronous (200). For large definitions or under load the API returns **202 + Location**; this snippet will then yield an empty/operation-status payload and `jq` will fail silently. Use the LRO-aware curl pattern in [Validate All Connections in a Dataflow](#validate-all-connections-in-a-dataflow-pre-refresh-check) below, or copy the [Fabric LRO Polling Pattern](authoring-script-templates.md#fabric-lro-polling-pattern) bash branch into your script before relying on this in production.

```bash
# Get definition, extract queryMetadata, then list all referenced connections
RESULT=$(az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  --headers "Content-Length=0")

QUERY_META=$(echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d)

# List all connection references
echo "$QUERY_META" | jq '.connections[] | {path:.path, connectionId:.connectionId}'
```

### Validate All Connections in a Dataflow (Pre-Refresh Check)

```bash
#!/bin/bash
# Validate all connections referenced in a dataflow before refresh

WS_ID="<id>"
DF_ID="<id>"
RESOURCE="https://api.fabric.microsoft.com"

# getDefinition can return 200 (sync) or 202 + Location (LRO) — handle both.
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
GET_DEF_BODY=$(mktemp); GET_DEF_HDR=$(mktemp)
HTTP_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$GET_DEF_HDR" -o "$GET_DEF_BODY" -w "%{http_code}")
if [ "$HTTP_CODE" = "202" ]; then
  # Fabric LRO: poll operation state, then GET /result.
  # See authoring-script-templates.md § Fabric LRO Polling Pattern for the contract.
  LOCATION=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) RESULT=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; exit 1 ;;
    esac
  done
else
  RESULT=$(cat "$GET_DEF_BODY")
fi
rm -f "$GET_DEF_BODY" "$GET_DEF_HDR"

QUERY_META=$(echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d)

# List all connections once for efficiency
ALL_CONNECTIONS=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value" -o json)

MISSING=0
echo "Validating connections..."
# queryMetadata.json connections[].connectionId is a STRINGIFIED COMPOSITE
# of shape {"ClusterId":"…","DatasourceId":"…"}. The plain-GUID `id` returned
# by GET /v1/connections matches the DatasourceId field. Parse before comparing.
# Use process substitution so MISSING updates persist (a piped `... | while` runs in a subshell).
while IFS= read -r row; do
  RAW_CONN_ID=$(echo "$row" | jq -r '.connectionId')
  CONN_PATH=$(echo "$row" | jq -r '.path')

  DATASOURCE_ID=$(echo "$RAW_CONN_ID" | jq -r '.DatasourceId? // empty' 2>/dev/null)
  [ -z "$DATASOURCE_ID" ] && DATASOURCE_ID="$RAW_CONN_ID"

  CONN_NAME=$(echo "$ALL_CONNECTIONS" | jq -r ".[] | select(.id==\"$DATASOURCE_ID\") | .displayName" 2>/dev/null || echo "")

  if [ -z "$CONN_NAME" ]; then
    echo "❌ $CONN_PATH: $DATASOURCE_ID NOT FOUND"
    MISSING=$((MISSING + 1))
  else
    echo "✅ $CONN_PATH: $DATASOURCE_ID ($CONN_NAME)"
  fi
done < <(echo "$QUERY_META" | jq -c '.connections[]')

if [ $MISSING -gt 0 ]; then
  echo "⚠️  Validation failed: $MISSING missing connection(s)"
  exit 1
else
  echo "✅ All connections validated"
fi
```

## Base64 Encoding Helpers

### Bash

```bash
# Encode file to base64 (no line wrapping)
base64 -w0 < mashup.pq

# Decode base64 payload to file
echo "<base64string>" | base64 -d > mashup.pq

# Extract and decode a specific part from getDefinition response
echo "$RESPONSE" | jq -r '.definition.parts[] | select(.path=="mashup.pq") | .payload' | base64 -d
```

### PowerShell

```powershell
# Encode file to base64
[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("mashup.pq"))

# Decode base64 to file
[System.IO.File]::WriteAllBytes("mashup.pq", [Convert]::FromBase64String($base64String))

# Encode string content (UTF-8, no BOM)
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))
```

## Definition Manipulation Patterns

### Read-Modify-Write Workflow

> **⚠ LRO caveat:** the one-liner `getDefinition` below assumes a synchronous 200 response. Under load or for large definitions the API returns **202 + Location**, which this snippet does not handle — it will silently fail and decode garbage. For production, use the LRO-aware curl pattern in [Validate All Connections in a Dataflow](#validate-all-connections-in-a-dataflow-pre-refresh-check) above, or copy the [Fabric LRO Polling Pattern](authoring-script-templates.md#fabric-lro-polling-pattern) bash branch into your script.

```bash
# 1. Get current definition (happy path; 200 only)
RESULT=$(az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition")

# 2. Extract and decode each part
echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d > queryMetadata.json
echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="mashup.pq") | .payload' | base64 -d > mashup.pq
echo "$RESULT" | jq -r '.definition.parts[] | select(.path==".platform") | .payload' | base64 -d > .platform

# 3. Edit files as needed (e.g., modify mashup.pq)

# 4. Re-encode and build update payload
QM_B64=$(base64 -w0 < queryMetadata.json)
MASHUP_B64=$(base64 -w0 < mashup.pq)
PLATFORM_B64=$(base64 -w0 < .platform)

jq -n \
  --arg qm "$QM_B64" --arg mash "$MASHUP_B64" --arg plat "$PLATFORM_B64" \
  '{definition:{parts:[
    {path:"queryMetadata.json",payload:$qm,payloadType:"InlineBase64"},
    {path:"mashup.pq",payload:$mash,payloadType:"InlineBase64"},
    {path:".platform",payload:$plat,payloadType:"InlineBase64"}
  ]}}' > definition.json

# 5. Update
az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition?updateMetadata=true" \
  --body @definition.json
```

### LRO Polling Helper

```bash
# Poll operation until terminal status. Accepts both enum sets:
#   - LRO operation status (getDefinition/updateDefinition/async create): Succeeded
#   - Job instance status (refresh jobs): Completed
# Both have the same terminal Failed / Cancelled values.
poll_operation() {
  local url="$1"
  while true; do
    STATUS=$(az rest --method get --resource "$RESOURCE" --url "$url" --query "status" --output tsv)
    echo "Status: $STATUS"
    case "$STATUS" in
      Succeeded|Completed|Failed|Cancelled) break ;;
      *) sleep 10 ;;
    esac
  done
  echo "Final status: $STATUS"
}
```

### Status Enum Reference — LRO Operation vs Job Instance

Fabric returns **two different status enums** depending on which endpoint you polled. Conflating them produces infinite polling loops or silently treats a still-running operation as terminal.

| Polled URL came from… | Endpoint examples | Enum values (live-verified 2026-05-13) | Terminal-success value |
|---|---|---|---|
| **LRO operation** (`Location` header from a long-running endpoint) | `POST /…/getDefinition`, `POST /…/updateDefinition`, async `POST /…/dataflows` (`202 + Location`) | `Running` / `Succeeded` / `Failed` / `Cancelled` | **`Succeeded`** |
| **Job instance** (`Location` header from `/jobs/instances?jobType=…`) | `POST /…/dataflows/{id}/jobs/instances?jobType=Refresh`, `POST /…/items/{id}/jobs/instances?jobType=Pipeline` | `NotStarted` / `InProgress` / `Completed` / `Failed` / `Cancelled` | **`Completed`** |

**Rule of thumb:** if the URL the agent is polling came from `…/jobs/instances/…`, the terminal-success value is `Completed`; otherwise it is `Succeeded`. `Failed` and `Cancelled` are valid terminal failures in both enums.

## Connection Creation Quick Patterns

For the full decision tree, schemas per credential type, and pitfalls, see [connection-management.md](connection-management.md).

**List supported connection types** (always do this before `POST /v1/connections`):
```bash
az rest --method get --resource "$RESOURCE" \
  --url "$API/connections/supportedConnectionTypes" \
  --query "value[?type=='SQL']"
```

**Create cloud SQL connection (Basic auth, Key Vault-backed password)**:
```bash
az rest --method post --resource "$RESOURCE" --url "$API/connections" --body '{
  "connectivityType": "ShareableCloud",
  "displayName": "ContosoSqlConnection",
  "connectionDetails": {
    "type": "SQL", "creationMethod": "SQL",
    "parameters": [
      {"dataType":"Text","name":"server","value":"contoso.database.windows.net"},
      {"dataType":"Text","name":"database","value":"sales"}
    ]
  },
  "privacyLevel": "Organizational",
  "credentialDetails": {
    "singleSignOnType": "None",
    "connectionEncryption": "Encrypted",
    "skipTestConnection": false,
    "credentials": {
      "credentialType": "Basic",
      "username": "admin",
      "passwordReference": {"connectionId":"<kvConnId>","secretName":"sql-pwd"}
    }
  }
}'
```

**Create cloud Lakehouse connection (Workspace identity)**:
```bash
az rest --method post --resource "$RESOURCE" --url "$API/connections" --body '{
  "connectivityType": "ShareableCloud",
  "displayName": "ContosoLakehouseConnection",
  "connectionDetails": {
    "type": "Lakehouse", "creationMethod": "Lakehouse",
    "parameters": [
      {"dataType":"Text","name":"workspaceId","value":"<wsId>"},
      {"dataType":"Text","name":"lakehouseId","value":"<lhId>"}
    ]
  },
  "privacyLevel": "Organizational",
  "credentialDetails": {
    "singleSignOnType": "None",
    "connectionEncryption": "Encrypted",
    "skipTestConnection": false,
    "credentials": {"credentialType":"WorkspaceIdentity"}
  }
}'
```

**Capture the new connection's plain-GUID `id` directly from the response**:
```bash
NEW_CONN_ID=$(az rest --method post --resource "$RESOURCE" \
  --url "$API/connections" --body @body.json \
  --query "id" --output tsv)
```

> **Connector parameters and supported credentials vary by tenant, gateway, and over time.** Treat the snippets above as illustrative; `supportedConnectionTypes` is authoritative.

## Connection Binding Quick Patterns

**Get current definition (handles both 200 sync and 202 LRO)**:
```bash
# az rest cannot return response headers; use curl with an az-acquired token to capture Location.
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
HDR=$(mktemp); BODY=$(mktemp)
CODE=$(curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$HDR" -o "$BODY" -w "%{http_code}")
if [ "$CODE" = "202" ]; then
  # Fabric LRO: poll operation state, then GET /result.
  # See authoring-script-templates.md § Fabric LRO Polling Pattern for the contract.
  LOCATION=$(tr -d '\r' < "$HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) DEF=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; exit 1 ;;
    esac
  done
else
  DEF=$(cat "$BODY")
fi
rm -f "$HDR" "$BODY"
```

**Get ClusterId for a connection**:

The endpoint lives on the Power BI control plane (not on `api.fabric.microsoft.com`) and the field is `clusterId` (camelCase). Pass `--resource "https://analysis.windows.net/powerbi/api"` to get the right token audience.

```bash
CONN_ID="<connectionId>"
PBI_RESOURCE="https://analysis.windows.net/powerbi/api"

# Use the LIST endpoint and filter by `id`. The per-id route
# (.../gatewayClusterDatasources/$CONN_ID) returns PowerBIEntityNotFound for
# cloud connections; list+filter is the supported pattern. Newly-created
# connections may take a few seconds to surface here — retry if empty.
CLUSTER_ID=$(az rest --method get \
  --resource "$PBI_RESOURCE" \
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" \
  --query "value[?id=='$CONN_ID'] | [0].clusterId" --output tsv)
```

**Extract queryMetadata.json from definition**:
```bash
echo "$DEF" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 --decode > queryMetadata.json
```

**Add connection to queryMetadata.json** (with ClusterId):
```bash
jq '.connections += [{
  "connectionId": "{\"ClusterId\": \"'$CLUSTER_ID'\", \"DatasourceId\": \"'$CONN_ID'\"}",
  "kind": "Sql",
  "path": "[dbo]"
}]' queryMetadata.json > queryMetadata_updated.json
```

**Update dataflow with all 3 parts** (full read-modify-write):
```bash
# Encode all parts
QM_B64=$(base64 -w0 < queryMetadata_updated.json)
MASHUP_B64=$(echo "$DEF" | jq -r '.definition.parts[] | select(.path=="mashup.pq") | .payload')
PLATFORM_B64=$(echo "$DEF" | jq -r '.definition.parts[] | select(.path==".platform") | .payload')

# Build the body in a temp file and pass via --body "@<path>".
# DO NOT use inline --body "{...}" with embedded base64 — cmd.exe argument parsing
# on Windows mangles the quotes and corrupts the payload. See SKILL.md MUST DO.
UPDATE_BODY=$(mktemp --suffix=.json 2>/dev/null || mktemp)
jq -n --arg qm "$QM_B64" --arg mp "$MASHUP_B64" --arg pf "$PLATFORM_B64" '{
  definition: { parts: [
    { path: "queryMetadata.json", payload: $qm, payloadType: "InlineBase64" },
    { path: "mashup.pq",          payload: $mp, payloadType: "InlineBase64" },
    { path: ".platform",          payload: $pf, payloadType: "InlineBase64" }
  ]}}' > "$UPDATE_BODY"

az rest --method post --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition" \
  --headers "Content-Type=application/json" \
  --body "@$UPDATE_BODY"
rm -f "$UPDATE_BODY"
```

See [authoring-script-templates.md § Connection Binding Templates](authoring-script-templates.md#connection-binding-templates) for complete end-to-end examples.

## Agent Integration Notes

- **GitHub Copilot CLI**: Generate `az rest` one-liners for dataflow CRUD or complete `.sh` scripts. Always include `--resource "https://api.fabric.microsoft.com"` in output. Remind user about base64 encoding for definition parts.
- **Claude Code / Cowork**: Run `az rest` commands via `bash` tool directly. For definition manipulation: write files first, then encode and send. Always verify `az login` before first use. After updates: get definition again to confirm.
- **Common agent pattern**:
  1. Discover workspace ID + dataflow ID
  2. Get current definition (decode all 3 parts)
  3. Formulate changes to M code or metadata
  4. Re-encode all 3 parts and update definition
  5. Optionally trigger refresh and poll for completion

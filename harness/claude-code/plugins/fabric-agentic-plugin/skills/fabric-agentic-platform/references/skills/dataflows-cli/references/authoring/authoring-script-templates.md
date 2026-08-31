# Authoring Script Templates

Self-contained templates for generating reusable Dataflows Gen2 authoring scripts.

**Common prerequisites** (validated in each template):
- `az` CLI installed — `https://aka.ms/install-azure-cli`
- `az login` session active
- `jq` installed — `apt-get install jq` / `brew install jq`
- Env vars: `WS_ID` (workspace ID), `API`, `RESOURCE`

## Fabric LRO Polling Pattern

`getDefinition` (and other Fabric mutations) follow the [Fabric Long-Running Operation contract](https://learn.microsoft.com/rest/api/fabric/articles/long-running-operation):

- **200 / 201** — operation completed synchronously; body holds the result.
- **202 Accepted** — body is empty. Three headers are returned:
  - `Location` — operation-state URL `…/v1/operations/{id}`.
  - `Retry-After` — seconds to wait before polling.
  - `x-ms-operation-id` — operation ID (can also be extracted from the Location URL).

**The correct sequence**: poll the operation-state URL until `status` is `Succeeded` / `Failed` / `Cancelled`, then GET `…/v1/operations/{id}/result` for the actual payload. A **single GET** on `Location` will most often return `{"status":"Running"}` and cause downstream parsing (`jq '.definition.parts[]'`, `ConvertFrom-Json`) to fail silently.

The reusable bash / PowerShell branches below are inlined in every template in this file; copy them into your own scripts wherever you call a Fabric LRO endpoint.

### Bash — LRO branch (drop-in)

```bash
# Prerequisites: $RESOURCE, $TOKEN, headers file $HDR, body file $BODY, $HTTP_CODE (e.g. from curl -D -o -w "%{http_code}")
if [ "$HTTP_CODE" = "202" ]; then
  LOCATION=$(tr -d '\r' < "$HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) RESULT=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: LRO $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
else
  RESULT=$(cat "$BODY")
fi
```

### PowerShell — LRO branch (drop-in)

```powershell
# Prerequisites: $resource, $resp (from Invoke-WebRequest -UseBasicParsing)
if ($resp.StatusCode -eq 202) {
    $location = $resp.Headers["Location"]
    if ($location -is [array]) { $location = $location[0] }
    $retryRaw = $resp.Headers["Retry-After"]
    if ($retryRaw -is [array]) { $retryRaw = $retryRaw[0] }
    $retryAfter = 5; [void][int]::TryParse([string]$retryRaw, [ref]$retryAfter)
    $result = $null
    while ($null -eq $result) {
        Start-Sleep -Seconds $retryAfter
        $op = az rest --method get --resource $resource --url $location | ConvertFrom-Json
        switch ($op.status) {
            'Succeeded' { $result = az rest --method get --resource $resource --url "$($location.TrimEnd('/'))/result" | ConvertFrom-Json }
            'Failed'    { Write-Error "LRO failed: $($op.error.message)"; exit 1 }
            'Cancelled' { Write-Error "LRO cancelled"; exit 1 }
        }
    }
} else {
    # Synchronous success — body may be JSON (e.g. getDefinition 200) OR empty (e.g.
    # updateDefinition 200, job triggers, deletes). Don't pipe an empty string to
    # ConvertFrom-Json — it throws even though the operation succeeded. Callers that
    # need a definition object should branch on $null before dereferencing it.
    if ([string]::IsNullOrWhiteSpace($resp.Content)) {
        $result = $null
    } else {
        $result = $resp.Content | ConvertFrom-Json
    }
}
```

> **Why `Invoke-WebRequest` and not `az rest` on PowerShell?** `az rest` cannot surface response headers (no `--include-response-headers` flag), so it cannot capture the `Location` header on a 202. Use `Invoke-WebRequest -UseBasicParsing` for the initial call, then `az rest --method get` (which carries the cached token) for the poll URL.

## Bash Templates

### Bash — Create Dataflow with Inline Definition

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_ID="${WS_ID:?Set WS_ID env var}"
API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"
DATAFLOW_NAME="${1:?Usage: $0 <dataflow_name>}"

command -v az >/dev/null 2>&1 || { echo "ERROR: az CLI not found."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }
az account show >/dev/null 2>&1 || { echo "Run 'az login' first."; exit 1; }

# Define M code (Power Query section document)
MASHUP='section Section1;

shared SalesData = let
    Source = Lakehouse.Contents([]),
    Nav1 = Source{[workspaceId = "'"$WS_ID"'"]}[Data],
    Nav2 = Nav1{[lakehouseId = "your-lakehouse-id"]}[Data],
    Nav3 = Nav2{[Id = "sales", ItemKind = "Table"]}[Data]
in
    Nav3;'

# Define query metadata
QUERY_METADATA='{
  "formatVersion": "202502",
  "computeEngineSettings": {"allowFastCopy": true, "maxConcurrency": 1},
  "name": "'"$DATAFLOW_NAME"'",
  "queryGroups": [],
  "documentLocale": "en-US",
  "queriesMetadata": {
    "SalesData": {
      "queryId": "'$(uuidgen | tr '[:upper:]' '[:lower:]')'",
      "queryName": "SalesData",
      "isHidden": false
    }
  },
  "connections": [],
  "fastCombine": false,
  "allowNativeQueries": true,
  "parametric": false
}'

# Define .platform
PLATFORM='{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {"type": "Dataflow", "displayName": "'"$DATAFLOW_NAME"'"},
  "config": {"version": "2.0", "logicalId": "'$(uuidgen | tr '[:upper:]' '[:lower:]')'"}
}'

# Base64-encode all parts
QM_B64=$(echo -n "$QUERY_METADATA" | base64 -w0)
MASHUP_B64=$(echo -n "$MASHUP" | base64 -w0)
PLATFORM_B64=$(echo -n "$PLATFORM" | base64 -w0)

# Build request body
BODY=$(jq -n \
  --arg name "$DATAFLOW_NAME" \
  --arg qm "$QM_B64" --arg mash "$MASHUP_B64" --arg plat "$PLATFORM_B64" \
  '{displayName:$name,definition:{parts:[
    {path:"queryMetadata.json",payload:$qm,payloadType:"InlineBase64"},
    {path:"mashup.pq",payload:$mash,payloadType:"InlineBase64"},
    {path:".platform",payload:$plat,payloadType:"InlineBase64"}
  ]}}')

echo "Creating dataflow '$DATAFLOW_NAME' ..."
RESULT=$(az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows" \
  --body "$BODY")

echo "$RESULT" | jq '{id, displayName}'
echo "✓ Dataflow created"
```

### Bash — Read-Modify-Write Dataflow Definition

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_ID="${WS_ID:?Set WS_ID env var}"
DF_ID="${DF_ID:?Set DF_ID env var}"
API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"
WORK_DIR="${1:-./_df_work}"

command -v az >/dev/null 2>&1 || { echo "ERROR: az CLI not found."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }
az account show >/dev/null 2>&1 || { echo "Run 'az login' first."; exit 1; }

mkdir -p "$WORK_DIR"

echo "[1/4] Getting current definition ..."
# getDefinition is an LRO — handle both 200 (sync) and 202 + Location (async).
# See § Fabric LRO Polling Pattern above for the full contract.
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
GET_DEF_HDR=$(mktemp); GET_DEF_BODY=$(mktemp)
HTTP_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$GET_DEF_HDR" -o "$GET_DEF_BODY" -w "%{http_code}")
if [ "$HTTP_CODE" = "202" ]; then
  LOCATION=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) RESULT=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
else
  RESULT=$(cat "$GET_DEF_BODY")
fi
rm -f "$GET_DEF_HDR" "$GET_DEF_BODY"

echo "[2/4] Decoding definition parts ..."
echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d > "$WORK_DIR/queryMetadata.json"
echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="mashup.pq") | .payload' | base64 -d > "$WORK_DIR/mashup.pq"
echo "$RESULT" | jq -r '.definition.parts[] | select(.path==".platform") | .payload' | base64 -d > "$WORK_DIR/.platform"

echo "Files written to $WORK_DIR/"
echo "  - queryMetadata.json"
echo "  - mashup.pq"
echo "  - .platform"
echo ""
echo "Edit the files as needed, then re-run with --upload flag."
echo ""

if [[ "${2:-}" == "--upload" ]]; then
  echo "[3/4] Re-encoding definition parts ..."
  QM_B64=$(base64 -w0 < "$WORK_DIR/queryMetadata.json")
  MASHUP_B64=$(base64 -w0 < "$WORK_DIR/mashup.pq")
  PLATFORM_B64=$(base64 -w0 < "$WORK_DIR/.platform")

  jq -n \
    --arg qm "$QM_B64" --arg mash "$MASHUP_B64" --arg plat "$PLATFORM_B64" \
    '{definition:{parts:[
      {path:"queryMetadata.json",payload:$qm,payloadType:"InlineBase64"},
      {path:"mashup.pq",payload:$mash,payloadType:"InlineBase64"},
      {path:".platform",payload:$plat,payloadType:"InlineBase64"}
    ]}}' > "$WORK_DIR/definition.json"

  echo "[4/4] Uploading updated definition ..."
  az rest --method post \
    --resource "$RESOURCE" \
    --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition?updateMetadata=true" \
    --body @"$WORK_DIR/definition.json"

  echo "✓ Definition updated"
fi
```

### PowerShell — Read-Modify-Write Dataflow Definition

PowerShell port of the bash template above. Same Discover → Formulate → Execute → Verify shape as [SKILL.md § Workflow B](../authoring.md#b-modify-an-existing-dataflow).

> **Verbatim-string trap (PowerShell only)** — once you base64-decode `queryMetadata.json` and `.platform`, the result is **already a JSON-formatted string**. Do **not** pipe it through `ConvertFrom-Json | ConvertTo-Json` if you are not modifying it: that re-quotes the entire JSON document as a single string literal and the server rejects the part with `400 InvalidDefinitionParts / InvalidPlatformFile`. Treat unchanged parts as opaque text and base64 them verbatim. If you *do* mutate one, mutate the deserialized object then `ConvertTo-Json -Depth 10 -Compress` **once** before re-encoding.

```powershell
#Requires -Version 5.1
param(
  [Parameter(Mandatory)][string]$WorkspaceId,
  [Parameter(Mandatory)][string]$DataflowId,
  [string]$WorkDir = (Join-Path $env:TEMP "_df_work")
)
$ErrorActionPreference = 'Stop'
$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$Resource = "https://api.fabric.microsoft.com"
$Api = "$Resource/v1"
New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

# 1. Discover — getDefinition (handle sync 200 or 202 + LRO).
#    az rest cannot capture response headers, so we use curl.exe for the initial POST.
$Token = az account get-access-token --resource $Resource --query accessToken -o tsv
$HdrFile  = Join-Path $env:TEMP "getdef-hdr.txt"
$BodyFile = Join-Path $env:TEMP "getdef-body.json"
$Code = & curl.exe -sS -X POST -H "Authorization: Bearer $Token" -H "Content-Length: 0" `
  "$Api/workspaces/$WorkspaceId/dataflows/$DataflowId/getDefinition" `
  -D $HdrFile -o $BodyFile -w "%{http_code}"
if ($Code -eq "202") {
  $Location = (Get-Content $HdrFile) -match "^Location:" | ForEach-Object { ($_ -split ":\s*", 2)[1].Trim() }
  while ($true) {
    Start-Sleep -Seconds 5
    $Op = az rest --method get --resource $Resource --url $Location | ConvertFrom-Json
    if ($Op.status -eq "Succeeded") {
      $Def = az rest --method get --resource $Resource --url "$Location/result" | ConvertFrom-Json
      break
    } elseif ($Op.status -in 'Failed','Cancelled') {
      Write-Error "getDefinition $($Op.status): $($Op | ConvertTo-Json)"; exit 1
    }
  }
} else {
  $Def = Get-Content $BodyFile -Raw | ConvertFrom-Json
}
Remove-Item $HdrFile, $BodyFile -Force

# 2. Decode all three parts. The decoded strings are already JSON text where applicable;
#    keep them as raw strings unless you need to mutate them.
function From-B64([string]$b64) { [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64)) }
function To-B64([string]$s)     { [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($s)) }
$MashupText   = From-B64 (($Def.definition.parts | Where-Object path -eq "mashup.pq").payload)
$MetaText     = From-B64 (($Def.definition.parts | Where-Object path -eq "queryMetadata.json").payload)
$PlatformText = From-B64 (($Def.definition.parts | Where-Object path -eq ".platform").payload)

# Persist a working copy for diffing / editing offline (optional).
Set-Content -LiteralPath (Join-Path $WorkDir "mashup.pq")          -Value $MashupText   -NoNewline -Encoding UTF8
Set-Content -LiteralPath (Join-Path $WorkDir "queryMetadata.json") -Value $MetaText     -NoNewline -Encoding UTF8
Set-Content -LiteralPath (Join-Path $WorkDir ".platform")          -Value $PlatformText -NoNewline -Encoding UTF8

# 3. Formulate — edit mashup.pq. Example: append a Table.SelectRows filter step.
#    For real changes, read $WorkDir\mashup.pq from disk after editing it externally.
$NewMashup = $MashupText -replace 'in\s+PromotedHeaders;', @'
,
    FilterFirstClass = Table.SelectRows(PromotedHeaders, each [Pclass] = "1")
in
    FilterFirstClass;
'@

# 4. Execute — re-encode all 3 parts (full replacement per SKILL.md MUST DO) and POST.
$UpdateBody = @{
  definition = @{
    parts = @(
      @{ path = "mashup.pq";          payload = (To-B64 $NewMashup);    payloadType = "InlineBase64" }
      @{ path = "queryMetadata.json"; payload = (To-B64 $MetaText);     payloadType = "InlineBase64" }
      @{ path = ".platform";          payload = (To-B64 $PlatformText); payloadType = "InlineBase64" }
    )
  }
}
$UpdateFile = Join-Path $env:TEMP "df-update-body.json"
[IO.File]::WriteAllText($UpdateFile, ($UpdateBody | ConvertTo-Json -Depth 10 -Compress), [Text.UTF8Encoding]::new($false))
az rest --method post --resource $Resource `
  --url "$Api/workspaces/$WorkspaceId/dataflows/$DataflowId/updateDefinition?updateMetadata=true" `
  --headers "Content-Type=application/json" --body "@$UpdateFile"
Remove-Item $UpdateFile -Force
Write-Host "✓ Definition updated"
```

### Bash — Author + Preview + Save Loop (executeQuery → updateDefinition)

Author a Power Query M change, preview it via `executeQuery` against the dataflow's bound connections, and only call `updateDefinition` if the preview succeeds. Catches M syntax / schema / credential errors at authoring time, before refresh. Includes `Table.FirstN` cap on the preview only — the persisted mashup omits the cap.

For the bootstrap branch (new credentialed dataflow needing initial connection binding), see [mashup-preview.md § Bootstrap branch](mashup-preview.md#bootstrap-branch--new-dataflow--new-credentialed-source).

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_ID="${WS_ID:?Set WS_ID env var}"
DF_ID="${DF_ID:?Set DF_ID env var}"
QUERY_NAME="${QUERY_NAME:?Set QUERY_NAME env var (must match a 'shared' member)}"
API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"

command -v az >/dev/null 2>&1 || { echo "ERROR: az CLI not found."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }
az account show >/dev/null 2>&1 || { echo "Run 'az login' first."; exit 1; }

# 1. Compose the candidate document (production form — no Table.FirstN cap).
#    NOTE: the `shared` member name MUST match $QUERY_NAME, otherwise executeQuery
#    returns `Query '$QUERY_NAME' not found in customMashupDocument`.
PROD_M_DOC=$(cat <<EOF
section Section1;

shared $QUERY_NAME = let
    Source = Sql.Database("server.database.windows.net", "salesdb"),
    $QUERY_NAME = Source{[Schema="dbo", Item="$QUERY_NAME"]}[Data]
in
    $QUERY_NAME;
EOF
)

# 2. Preview form — same logic but with Table.FirstN cap to keep evaluation cheap.
PREVIEW_M_DOC=$(cat <<EOF
section Section1;

shared $QUERY_NAME = let
    Source = Sql.Database("server.database.windows.net", "salesdb"),
    $QUERY_NAME = Source{[Schema="dbo", Item="$QUERY_NAME"]}[Data],
    Limited = Table.FirstN($QUERY_NAME, 100)
in
    Limited;
EOF
)

# 3. Preview against bound connections.
#    executeQuery returns raw Apache Arrow IPC bytes (NOT a JSON envelope) via az rest.
#    Pass --output-file so az captures the binary; failures are embedded as
#    {"Error":"..."} inside the stream and HTTP 200 alone does NOT mean success.
echo "→ Previewing '$QUERY_NAME' via executeQuery ..."
PREVIEW_REQ=$(mktemp); PREVIEW_OUT="$(mktemp).arrow"
jq -n --arg q "$QUERY_NAME" --arg m "$PREVIEW_M_DOC" \
  '{QueryName: $q, customMashupDocument: $m}' > "$PREVIEW_REQ"

az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/executeQuery" \
  --body "@$PREVIEW_REQ" \
  --output-file "$PREVIEW_OUT"

if grep -q '"Error":"' "$PREVIEW_OUT"; then
  echo "✗ Preview failed (embedded source error):"
  python3 -c "import re,sys; raw=open(sys.argv[1],'rb').read().decode('utf-8','replace'); m=re.search(r'\\{\"Error\":\"[^\"]+\"\\}', raw); print(m.group(0) if m else '(marker present, JSON not parsed)')" "$PREVIEW_OUT"
  echo "Adjust M and re-run. updateDefinition NOT called."
  rm -f "$PREVIEW_REQ" "$PREVIEW_OUT"
  exit 1
fi

PREVIEW_BYTES=$(wc -c < "$PREVIEW_OUT")
echo "✓ Preview OK. capturedBytes=$PREVIEW_BYTES"
rm -f "$PREVIEW_REQ" "$PREVIEW_OUT"

# 4. Build the production definition payload (PROD_M_DOC — no cap).
#    Read existing definition to preserve queryMetadata.json connection bindings.
#    getDefinition can return 200 (sync, body inline) or 202 + Location header (LRO).
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
GET_DEF_BODY=$(mktemp); GET_DEF_HDR=$(mktemp)
HTTP_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$GET_DEF_HDR" -o "$GET_DEF_BODY" -w "%{http_code}")
if [ "$HTTP_CODE" = "202" ]; then
  # Fabric LRO: poll operation state, then GET /result. See § Fabric LRO Polling Pattern.
  LOCATION=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) EXISTING_DEF=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
else
  EXISTING_DEF=$(cat "$GET_DEF_BODY")
fi
rm -f "$GET_DEF_BODY" "$GET_DEF_HDR"

QM_B64=$(echo "$EXISTING_DEF" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload')
PLATFORM_B64=$(echo "$EXISTING_DEF" | jq -r '.definition.parts[] | select(.path==".platform") | .payload')
NEW_MASHUP_B64=$(echo -n "$PROD_M_DOC" | base64 -w0)

DEFINITION_PAYLOAD=$(jq -n \
  --arg qm "$QM_B64" --arg mp "$NEW_MASHUP_B64" --arg pl "$PLATFORM_B64" '{
    definition: { parts: [
      {path:"queryMetadata.json", payload:$qm, payloadType:"InlineBase64"},
      {path:"mashup.pq",          payload:$mp, payloadType:"InlineBase64"},
      {path:".platform",          payload:$pl, payloadType:"InlineBase64"}
    ]}
  }')

# 5. Persist the production mashup (always write to temp file — never inline --body for large payloads).
#    updateDefinition can return 200 (sync) or 202 + Location (LRO). Use curl so we can
#    observe the status / Location header, then poll until the operation terminates BEFORE
#    the verify step — otherwise the read-back can race the in-flight save and report
#    stale connections[]. See § Fabric LRO Polling Pattern.
echo "→ Saving via updateDefinition ..."
UPDATE_BODY=$(mktemp); UPDATE_HDR=$(mktemp); UPDATE_OUT=$(mktemp)
echo "$DEFINITION_PAYLOAD" > "$UPDATE_BODY"
UPDATE_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary @"$UPDATE_BODY" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition?updateMetadata=true" \
  -D "$UPDATE_HDR" -o "$UPDATE_OUT" -w "%{http_code}")
if [ "$UPDATE_CODE" = "202" ]; then
  UPD_LOC=$(tr -d '\r' < "$UPDATE_HDR" | grep -i "^location:" | awk '{print $2}')
  UPD_RETRY=$(tr -d '\r' < "$UPDATE_HDR" | grep -i "^retry-after:" | awk '{print $2}'); UPD_RETRY=${UPD_RETRY:-5}
  while :; do
    sleep "$UPD_RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$UPD_LOC")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) break ;;
      Failed|Cancelled) echo "ERROR: updateDefinition $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
elif [ "$UPDATE_CODE" != "200" ] && [ "$UPDATE_CODE" != "201" ]; then
  echo "ERROR: updateDefinition HTTP $UPDATE_CODE" >&2; cat "$UPDATE_OUT" >&2; exit 1
fi
rm -f "$UPDATE_BODY" "$UPDATE_HDR" "$UPDATE_OUT"
echo "✓ Saved."

# 6. Verify connections survived the full-replacement write.
#    getDefinition can return 200 or 202 + Location (LRO) — handle both.
VERIFY_TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
VERIFY_BODY=$(mktemp); VERIFY_HDR=$(mktemp)
VERIFY_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $VERIFY_TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$VERIFY_HDR" -o "$VERIFY_BODY" -w "%{http_code}")
if [ "$VERIFY_CODE" = "202" ]; then
  # Fabric LRO: poll operation state, then GET /result. See § Fabric LRO Polling Pattern.
  VERIFY_LOC=$(tr -d '\r' < "$VERIFY_HDR" | grep -i "^location:" | awk '{print $2}')
  VERIFY_RETRY=$(tr -d '\r' < "$VERIFY_HDR" | grep -i "^retry-after:" | awk '{print $2}'); VERIFY_RETRY=${VERIFY_RETRY:-5}
  while :; do
    sleep "$VERIFY_RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$VERIFY_LOC")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) POST_DEF=$(az rest --method get --resource "$RESOURCE" --url "${VERIFY_LOC%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: verify getDefinition $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
else
  POST_DEF=$(cat "$VERIFY_BODY")
fi
rm -f "$VERIFY_BODY" "$VERIFY_HDR"
SURVIVING_CONNS=$(echo "$POST_DEF" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' \
  | base64 -d | jq -r '.connections | length')
echo "✓ queryMetadata.json connections[] count after save: $SURVIVING_CONNS"
```

### Bash — Trigger Refresh with LRO Polling

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_ID="${WS_ID:?Set WS_ID env var}"
DF_ID="${DF_ID:?Set DF_ID env var}"
API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"
POLL_INTERVAL="${POLL_INTERVAL:-15}"
MAX_POLLS="${MAX_POLLS:-60}"

command -v az >/dev/null 2>&1 || { echo "ERROR: az CLI not found."; exit 1; }
az account show >/dev/null 2>&1 || { echo "Run 'az login' first."; exit 1; }

echo "Triggering refresh for dataflow $DF_ID ..."

# Trigger the job — capture Location header for polling.
# az rest cannot return response headers; use curl with an az-acquired token.
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
OP_URL=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances?jobType=Refresh" \
  -o /dev/null -D - | tr -d '\r' | grep -i "^location:" | awk '{print $2}')

if [[ -z "$OP_URL" ]]; then
  echo "No operation URL captured. Check Azure portal for refresh status."
  exit 1
fi

echo "Polling: $OP_URL"
ATTEMPT=0
while [[ $ATTEMPT -lt $MAX_POLLS ]]; do
  STATUS=$(az rest --method get --resource "$RESOURCE" --url "$OP_URL" --query "status" --output tsv 2>/dev/null)
  PCT=$(az rest --method get --resource "$RESOURCE" --url "$OP_URL" --query "percentComplete" --output tsv 2>/dev/null || echo "?")
  echo "  [$ATTEMPT] Status: $STATUS ($PCT%)"

  case "$STATUS" in
    Completed)
      echo "✓ Refresh completed successfully"
      exit 0
      ;;
    Failed)
      echo "✗ Refresh failed"
      az rest --method get --resource "$RESOURCE" --url "$OP_URL" 2>/dev/null | jq .
      exit 1
      ;;
    Cancelled)
      echo "✗ Refresh was cancelled"
      exit 1
      ;;
  esac

  sleep "$POLL_INTERVAL"
  ATTEMPT=$((ATTEMPT + 1))
done

echo "✗ Polling timed out after $((MAX_POLLS * POLL_INTERVAL))s"
exit 1
```

### Bash — CI/CD Export and Import

```bash
#!/usr/bin/env bash
set -euo pipefail

API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"
ACTION="${1:?Usage: $0 <export|import> [options]}"

command -v az >/dev/null 2>&1 || { echo "ERROR: az CLI not found."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }
az account show >/dev/null 2>&1 || { echo "Run 'az login' first."; exit 1; }

case "$ACTION" in
  export)
    SRC_WS="${2:?Usage: $0 export <src_workspace_id> <dataflow_id> <output_dir>}"
    SRC_DF="${3:?Usage: $0 export <src_workspace_id> <dataflow_id> <output_dir>}"
    OUT_DIR="${4:?Usage: $0 export <src_workspace_id> <dataflow_id> <output_dir>}"
    mkdir -p "$OUT_DIR"

    echo "Exporting dataflow $SRC_DF from workspace $SRC_WS ..."
    RESULT=$(az rest --method post \
      --resource "$RESOURCE" \
      --url "$API/workspaces/$SRC_WS/dataflows/$SRC_DF/getDefinition")

    echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d > "$OUT_DIR/queryMetadata.json"
    echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="mashup.pq") | .payload' | base64 -d > "$OUT_DIR/mashup.pq"
    echo "$RESULT" | jq -r '.definition.parts[] | select(.path==".platform") | .payload' | base64 -d > "$OUT_DIR/.platform"
    echo "✓ Exported to $OUT_DIR/"
    ;;

  import)
    TGT_WS="${2:?Usage: $0 import <tgt_workspace_id> <dataflow_id> <input_dir>}"
    TGT_DF="${3:?Usage: $0 import <tgt_workspace_id> <dataflow_id> <input_dir>}"
    IN_DIR="${4:?Usage: $0 import <tgt_workspace_id> <dataflow_id> <input_dir>}"

    echo "Importing definition from $IN_DIR to dataflow $TGT_DF ..."
    QM_B64=$(base64 -w0 < "$IN_DIR/queryMetadata.json")
    MASHUP_B64=$(base64 -w0 < "$IN_DIR/mashup.pq")
    PLATFORM_B64=$(base64 -w0 < "$IN_DIR/.platform")

    jq -n \
      --arg qm "$QM_B64" --arg mash "$MASHUP_B64" --arg plat "$PLATFORM_B64" \
      '{definition:{parts:[
        {path:"queryMetadata.json",payload:$qm,payloadType:"InlineBase64"},
        {path:"mashup.pq",payload:$mash,payloadType:"InlineBase64"},
        {path:".platform",payload:$plat,payloadType:"InlineBase64"}
      ]}}' > /tmp/df_import_payload.json

    az rest --method post \
      --resource "$RESOURCE" \
      --url "$API/workspaces/$TGT_WS/dataflows/$TGT_DF/updateDefinition?updateMetadata=true" \
      --body @/tmp/df_import_payload.json

    rm -f /tmp/df_import_payload.json
    echo "✓ Definition imported"
    ;;

  *)
    echo "Usage: $0 <export|import> [options]"
    exit 1
    ;;
esac
```

## PowerShell Templates

### PowerShell — Create Dataflow with Definition

> **Windows / PowerShell escaping rule** — do NOT pass JSON via `--body $body` inline:
> `az.exe` is invoked through `cmd.exe`'s argument parser which mangles embedded
> quotes and breaks base64 payloads. Always write the body to a temp file with
> **UTF-8, no BOM** and use `--body "@<path>"`. (Same pattern documented in
> [COMMON-CLI.md § Gotchas — Complex JSON with special characters](../../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific)
> and [EVENTHOUSE-CONSUMPTION-CORE.md § Querying via az rest](../../../../common/EVENTHOUSE-CONSUMPTION-CORE.md#querying-via-az-rest).)

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$DataflowName,
    [string]$Description = "Created via CLI"
)

$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$api = "https://api.fabric.microsoft.com/v1"
$resource = "https://api.fabric.microsoft.com"

# Define M code
$mashup = @"
section Section1;

shared SalesData = let
    Source = Lakehouse.Contents([]),
    Nav1 = Source{[workspaceId = "$WorkspaceId"]}[Data]
in
    Nav1;
"@

# Define query metadata (top-level `name` MUST match displayName)
$queryMetadata = @{
    formatVersion = "202502"
    computeEngineSettings = @{ allowFastCopy = $true; maxConcurrency = 1 }
    name = $DataflowName
    queryGroups = @()
    documentLocale = "en-US"
    queriesMetadata = @{
        SalesData = @{
            queryId = [guid]::NewGuid().ToString()
            queryName = "SalesData"
            isHidden = $false
        }
    }
    connections = @()
    fastCombine = $false
    allowNativeQueries = $true
    parametric = $false
} | ConvertTo-Json -Depth 5 -Compress

# Define .platform
$platform = @{
    "`$schema" = "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json"
    metadata = @{ type = "Dataflow"; displayName = $DataflowName }
    config = @{ version = "2.0"; logicalId = [guid]::NewGuid().ToString() }
} | ConvertTo-Json -Depth 3 -Compress

# Base64-encode each part (InlineBase64 payload required by the Items API)
$qmB64       = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($queryMetadata))
$mashupB64   = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($mashup))
$platformB64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($platform))

# Build the request body. The /dataflows endpoint accepts the same parts[] shape as the
# Items API but does NOT require `type` (the path implies it). Body must NOT include
# `definition.format` (sending it returns 400 InvalidDefinitionFormat).
$body = @{
    displayName = $DataflowName
    description = $Description
    definition = @{
        parts = @(
            @{ path = "queryMetadata.json"; payload = $qmB64;       payloadType = "InlineBase64" }
            @{ path = "mashup.pq";          payload = $mashupB64;   payloadType = "InlineBase64" }
            @{ path = ".platform";          payload = $platformB64; payloadType = "InlineBase64" }
        )
    }
} | ConvertTo-Json -Depth 6 -Compress

# Write to temp file with UTF-8 (no BOM) and pass via --body "@<path>".
# DO NOT use `--body $body` inline — cmd.exe quoting will corrupt the JSON / base64.
$bodyFile = Join-Path $env:TEMP "df-create-$([guid]::NewGuid()).json"
[System.IO.File]::WriteAllText($bodyFile, $body, [System.Text.UTF8Encoding]::new($false))

try {
    Write-Host "Creating dataflow '$DataflowName' ..."
    $result = az rest --method post --resource $resource `
        --url "$api/workspaces/$WorkspaceId/dataflows" `
        --headers "Content-Type=application/json" `
        --body "@$bodyFile" | ConvertFrom-Json

    Write-Host "Created: $($result.id) - $($result.displayName)"
}
finally {
    Remove-Item -Path $bodyFile -ErrorAction SilentlyContinue
}
```

### PowerShell — Trigger Refresh with Polling

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$DataflowId,
    [int]$PollIntervalSec = 15,
    [int]$TimeoutMin = 30
)

$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$api = "https://api.fabric.microsoft.com/v1"
$resource = "https://api.fabric.microsoft.com"

Write-Host "Triggering refresh ..."
# az rest cannot return response headers; use Invoke-WebRequest with an az-acquired token.
$token = az account get-access-token --resource $resource --query accessToken -o tsv
$headers = @{
    Authorization    = "Bearer $token"
    "Content-Length" = "0"
}
try {
    $resp = Invoke-WebRequest -Method Post `
        -Uri "$api/workspaces/$WorkspaceId/dataflows/$DataflowId/jobs/instances?jobType=Refresh" `
        -Headers $headers -UseBasicParsing
    $opUrl = $resp.Headers["Location"]
} catch {
    Write-Error "Failed to trigger refresh: $($_.Exception.Message)"
    exit 1
}

if (-not $opUrl) {
    Write-Warning "No operation URL captured. Check portal."
    exit 1
}

$deadline = (Get-Date).AddMinutes($TimeoutMin)
while ((Get-Date) -lt $deadline) {
    $op = az rest --method get --resource $resource --url $opUrl | ConvertFrom-Json
    Write-Host "  Status: $($op.status) ($($op.percentComplete)%)"

    switch ($op.status) {
        "Completed" { Write-Host "Refresh completed"; exit 0 }
        "Failed"    { Write-Error "Refresh failed"; $op | ConvertTo-Json; exit 1 }
        "Cancelled" { Write-Warning "Refresh cancelled"; exit 1 }
    }

    Start-Sleep -Seconds $PollIntervalSec
}

Write-Error "Polling timed out after $TimeoutMin minutes"
exit 1
```

## Pre-Refresh Validation Templates

> **Critical**: Always validate all connections before triggering a dataflow refresh. Missing connections cause cryptic errors that are difficult to debug.

### Bash — Validate All Connections in a Dataflow

```bash
#!/usr/bin/env bash
set -euo pipefail

WS_ID="${1:?Usage: $0 <workspace_id> <dataflow_id>}"
DF_ID="${2:?Usage: $0 <workspace_id> <dataflow_id>}"

API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"

command -v az >/dev/null 2>&1 || { echo "ERROR: az CLI not found."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }
az account show >/dev/null 2>&1 || { echo "Run 'az login' first."; exit 1; }

echo "Retrieving dataflow definition..."
# getDefinition can return 200 (sync, body inline) or 202 + Location header (LRO).
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
GET_DEF_BODY=$(mktemp); GET_DEF_HDR=$(mktemp)
HTTP_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$GET_DEF_HDR" -o "$GET_DEF_BODY" -w "%{http_code}")
if [ "$HTTP_CODE" = "202" ]; then
  # Fabric LRO: poll operation state, then GET /result. See § Fabric LRO Polling Pattern.
  LOCATION=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) RESULT=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
else
  RESULT=$(cat "$GET_DEF_BODY")
fi
rm -f "$GET_DEF_BODY" "$GET_DEF_HDR"

QUERY_META=$(echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d)

# List all connections once for efficiency
ALL_CONNECTIONS=$(az rest --method get \
  --resource "$RESOURCE" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value" -o json)

echo "Validating connections..."
MISSING=0

# queryMetadata.json connections[].connectionId is a STRINGIFIED COMPOSITE
# of shape {"ClusterId":"…","DatasourceId":"…"}. The plain-GUID `id` returned
# by GET /v1/connections matches the DatasourceId field. Parse before comparing.
# Use process substitution so the while loop runs in the current shell and
# updates to MISSING persist (a piped `... | while` would run in a subshell).
while IFS= read -r row; do
  RAW_CONN_ID=$(echo "$row" | jq -r '.connectionId')
  CONN_PATH=$(echo "$row" | jq -r '.path')

  DATASOURCE_ID=$(echo "$RAW_CONN_ID" | jq -r '.DatasourceId? // empty' 2>/dev/null)
  [ -z "$DATASOURCE_ID" ] && DATASOURCE_ID="$RAW_CONN_ID"

  CONN_NAME=$(echo "$ALL_CONNECTIONS" | jq -r ".[] | select(.id==\"$DATASOURCE_ID\") | .displayName" 2>/dev/null || echo "")

  if [ -z "$CONN_NAME" ]; then
    echo "  ❌ $CONN_PATH: $DATASOURCE_ID — NOT FOUND"
    MISSING=$((MISSING + 1))
  else
    echo "  ✅ $CONN_PATH: $DATASOURCE_ID ($CONN_NAME)"
  fi
done < <(echo "$QUERY_META" | jq -c '.connections[]')

echo ""
if [ $MISSING -eq 0 ]; then
  echo "✅ All connections validated. Safe to refresh."
  exit 0
else
  echo "❌ Validation failed: $MISSING missing connection(s)"
  echo "Run: az rest --method get --resource 'https://api.fabric.microsoft.com' --url 'https://api.fabric.microsoft.com/v1/connections' --query 'value[] | {id, name:displayName}'"
  exit 1
fi
```

### PowerShell — Validate All Connections in a Dataflow

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$DataflowId
)

$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$api = "https://api.fabric.microsoft.com/v1"
$resource = "https://api.fabric.microsoft.com"

Write-Host "Retrieving dataflow definition..."
# getDefinition can return 200 (sync, body inline) or 202 + Location header (LRO).
# az rest cannot capture response headers, so use Invoke-WebRequest with an az-acquired token.
$token = az account get-access-token --resource $resource --query accessToken -o tsv
$headers = @{ Authorization = "Bearer $token"; "Content-Length" = "0" }
try {
    $resp = Invoke-WebRequest -Method Post -Uri "$api/workspaces/$WorkspaceId/dataflows/$DataflowId/getDefinition" `
        -Headers $headers -UseBasicParsing
} catch {
    Write-Error "getDefinition failed: $_"; exit 1
}
if ($resp.StatusCode -eq 202) {
    # Fabric LRO: poll operation state, then GET /result. See § Fabric LRO Polling Pattern.
    $location = $resp.Headers["Location"]
    if ($location -is [array]) { $location = $location[0] }
    $retryRaw = $resp.Headers["Retry-After"]
    if ($retryRaw -is [array]) { $retryRaw = $retryRaw[0] }
    $retryAfter = 5; [void][int]::TryParse([string]$retryRaw, [ref]$retryAfter)
    $result = $null
    while ($null -eq $result) {
        Start-Sleep -Seconds $retryAfter
        $op = az rest --method get --resource $resource --url $location | ConvertFrom-Json
        switch ($op.status) {
            'Succeeded' { $result = az rest --method get --resource $resource --url "$($location.TrimEnd('/'))/result" | ConvertFrom-Json }
            'Failed'    { Write-Error "getDefinition failed: $($op.error.message)"; exit 1 }
            'Cancelled' { Write-Error "getDefinition cancelled"; exit 1 }
        }
    }
} else {
    $result = $resp.Content | ConvertFrom-Json
}

# Decode queryMetadata.json
$queryMetaB64 = $result.definition.parts | Where-Object { $_.path -eq "queryMetadata.json" } | Select-Object -ExpandProperty payload
$queryMetaJson = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($queryMetaB64))
$queryMeta = $queryMetaJson | ConvertFrom-Json

# List all connections once for efficiency
$allConnections = az rest --method get --resource $resource `
    --url "https://api.fabric.microsoft.com/v1/connections" `
    --query "value" | ConvertFrom-Json

Write-Host "Validating $($queryMeta.connections.Count) connection(s)..."
$missing = 0

# queryMetadata.json connections[].connectionId is a STRINGIFIED COMPOSITE
# of shape {"ClusterId":"…","DatasourceId":"…"}. The plain-GUID `id` returned
# by GET /v1/connections matches the DatasourceId field. Parse before comparing.
foreach ($conn in $queryMeta.connections) {
    $rawConnId = $conn.connectionId
    $connPath = $conn.path

    $datasourceId = $rawConnId
    try {
        $parsed = $rawConnId | ConvertFrom-Json -ErrorAction Stop
        if ($parsed.DatasourceId) { $datasourceId = $parsed.DatasourceId }
    } catch {
        # Not composite JSON — assume plain GUID
    }

    $connCheck = $allConnections | Where-Object { $_.id -eq $datasourceId } | Select-Object -ExpandProperty displayName

    if ($connCheck) {
        Write-Host "  ✅ $connPath`: $datasourceId ($connCheck)"
    } else {
        Write-Host "  ❌ $connPath`: $datasourceId — NOT FOUND"
        $missing++
    }
}

Write-Host ""
if ($missing -eq 0) {
    Write-Host "✅ All connections validated. Safe to refresh." -ForegroundColor Green
    exit 0
} else {
    Write-Error "Validation failed: $missing missing connection(s)"
    Write-Host "To see available connections, run:"
    Write-Host "  az rest --method get --resource 'https://api.fabric.microsoft.com' --url 'https://api.fabric.microsoft.com/v1/connections' --query 'value[] | {id, name:displayName}'"
    exit 1
}
```

### Bash — Batch Refresh with Connection Validation

```bash
#!/usr/bin/env bash
set -euo pipefail

# Validate and refresh multiple dataflows
# Usage: $0 <workspace_id> <dataflow_id1> <dataflow_id2> ...

WS_ID="${1:?Usage: $0 <workspace_id> <dataflow_id1> <dataflow_id2> ...}"
shift
DATAFLOWS=("$@")

if [ ${#DATAFLOWS[@]} -eq 0 ]; then
  echo "Usage: $0 <workspace_id> <dataflow_id1> <dataflow_id2> ..."
  exit 1
fi

API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"

validate_and_refresh() {
  local df_id="$1"
  echo ""
  echo "Processing dataflow: $df_id"

  # Get definition — getDefinition can return 200 or 202 + Location (LRO).
  TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
  GET_DEF_BODY=$(mktemp); GET_DEF_HDR=$(mktemp)
  HTTP_CODE=$(curl -sS -X POST \
    -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
    "$API/workspaces/$WS_ID/dataflows/$df_id/getDefinition" \
    -D "$GET_DEF_HDR" -o "$GET_DEF_BODY" -w "%{http_code}")
  if [ "$HTTP_CODE" = "202" ]; then
    # Fabric LRO: poll operation state, then GET /result. See § Fabric LRO Polling Pattern.
    LOCATION=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^location:" | awk '{print $2}')
    RETRY=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
    while :; do
      sleep "$RETRY"
      OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
      case "$(echo "$OP" | jq -r '.status // empty')" in
        Succeeded) RESULT=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
        Failed|Cancelled) echo "  ❌ getDefinition $(echo "$OP" | jq -r '.status') for $df_id"; return 1 ;;
      esac
    done
  else
    RESULT=$(cat "$GET_DEF_BODY")
  fi
  rm -f "$GET_DEF_BODY" "$GET_DEF_HDR"

  QUERY_META=$(echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d)

  # List all connections once for efficiency
  ALL_CONNECTIONS=$(az rest --method get \
    --resource "$RESOURCE" \
    --url "https://api.fabric.microsoft.com/v1/connections" \
    --query "value" -o json)

  # Validate connections — connectionId is a composite; parse DatasourceId before comparing.
  # Use process substitution so MISSING updates persist (a piped `... | while` runs in a subshell).
  MISSING=0
  while IFS= read -r row; do
    RAW_CONN_ID=$(echo "$row" | jq -r '.connectionId')
    DATASOURCE_ID=$(echo "$RAW_CONN_ID" | jq -r '.DatasourceId? // empty' 2>/dev/null)
    [ -z "$DATASOURCE_ID" ] && DATASOURCE_ID="$RAW_CONN_ID"
    CONN_NAME=$(echo "$ALL_CONNECTIONS" | jq -r ".[] | select(.id==\"$DATASOURCE_ID\") | .displayName" 2>/dev/null || echo "")

    if [ -z "$CONN_NAME" ]; then
      echo "  ❌ Connection not found: $DATASOURCE_ID"
      MISSING=$((MISSING + 1))
    fi
  done < <(echo "$QUERY_META" | jq -c '.connections[]')

  if [ $MISSING -gt 0 ]; then
    echo "  ⚠️  Skipping refresh: $MISSING missing connection(s)"
    return 1
  fi

  # Trigger refresh
  # az rest cannot return response headers; use curl with an az-acquired token to capture Location.
  echo "  Triggering refresh..."
  TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
  LOCATION=$(curl -sS -X POST \
    -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
    "$API/workspaces/$WS_ID/dataflows/$df_id/jobs/instances?jobType=Refresh" \
    -o /dev/null -D - | tr -d '\r' | grep -i "^location:" | awk '{print $2}')

  if [ -z "$LOCATION" ]; then
    echo "  ⚠️  No operation URL; cannot poll"
    return 0
  fi

  # Poll for completion (max 5 minutes)
  ATTEMPTS=0
  MAX_ATTEMPTS=20
  while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    STATUS=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION" --query "status" --output tsv 2>/dev/null || echo "Unknown")
    echo "  Status: $STATUS"

    case "$STATUS" in
      Completed) echo "  ✅ Refresh completed"; return 0 ;;
      Failed) echo "  ❌ Refresh failed"; return 1 ;;
      Cancelled) echo "  ⚠️  Refresh cancelled"; return 1 ;;
      *) sleep 15; ATTEMPTS=$((ATTEMPTS + 1)) ;;
    esac
  done

  echo "  ⚠️  Polling timed out"
  return 0
}

# Validate connections and refresh all dataflows
for df_id in "${DATAFLOWS[@]}"; do
  validate_and_refresh "$df_id" || true
done

echo ""
echo "✅ Batch refresh complete"
```

---

## Connection Binding Templates

### Bash — Bind Connections to a Dataflow

```bash
#!/usr/bin/env bash
set -euo pipefail

# Bind one or more connections to a dataflow
# Usage: $0 <workspace_id> <dataflow_id> <connection_id1> [connection_id2] ...

WS_ID="${1:?Usage: $0 <workspace_id> <dataflow_id> <connection_id1> [connection_id2] ...}"
DF_ID="${2:?Dataflow ID required}"
shift 2
CONN_IDS=("$@")

if [ ${#CONN_IDS[@]} -eq 0 ]; then
  echo "Usage: $0 <workspace_id> <dataflow_id> <connection_id1> [connection_id2] ..."
  exit 1
fi

API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"

echo "Binding ${#CONN_IDS[@]} connection(s) to dataflow $DF_ID..."

# Step 1: Get current definition
# getDefinition can return 200 (sync, body inline) or 202 + Location header (LRO) — handle both.
# az rest cannot return response headers; use curl with an az-acquired token to capture Location.
echo "Step 1: Fetching definition..."
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
GET_DEF_BODY=$(mktemp); GET_DEF_HDR=$(mktemp)
HTTP_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$GET_DEF_HDR" -o "$GET_DEF_BODY" -w "%{http_code}")
if [ "$HTTP_CODE" = "202" ]; then
  # Fabric LRO: poll operation state, then GET /result. See § Fabric LRO Polling Pattern.
  LOCATION=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$GET_DEF_HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOCATION")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) DEF=$(az rest --method get --resource "$RESOURCE" --url "${LOCATION%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
else
  DEF=$(cat "$GET_DEF_BODY")
fi
rm -f "$GET_DEF_BODY" "$GET_DEF_HDR"

# Extract all parts
QUERY_META_B64=$(echo "$DEF" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload')
QUERY_META=$(echo "$QUERY_META_B64" | base64 --decode)
MASHUP_B64=$(echo "$DEF" | jq -r '.definition.parts[] | select(.path=="mashup.pq") | .payload')
PLATFORM_B64=$(echo "$DEF" | jq -r '.definition.parts[] | select(.path==".platform") | .payload')

# Step 2: Get ClusterIds for all connections
# Endpoint is on the Power BI control plane (not api.fabric.microsoft.com) and the
# response field is `clusterId` (camelCase). Use the Power BI token audience.
# IMPORTANT: list the user's gateway-cluster datasources and filter by `id` — the
# per-id route (gatewayClusterDatasources/$id) returns PowerBIEntityNotFound for
# cloud connections. List once; reuse across all conn ids.
echo "Step 2: Retrieving ClusterIds..."
PBI_RESOURCE="https://analysis.windows.net/powerbi/api"
declare -A CLUSTER_IDS
DS_LIST=$(az rest --method get --resource "$PBI_RESOURCE" \
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources")
for conn_id in "${CONN_IDS[@]}"; do
  echo "  Getting ClusterId for $conn_id..."
  cluster_id=$(echo "$DS_LIST" | jq -r --arg cid "$conn_id" \
    '.value[] | select(.id==$cid) | .clusterId' | head -n 1)
  CLUSTER_IDS[$conn_id]="$cluster_id"
  echo "    ClusterId: $cluster_id"
done

# Step 3: Add connections to queryMetadata.json
echo "Step 3: Adding connections to queryMetadata.json..."
UPDATED_META="$QUERY_META"
for conn_id in "${CONN_IDS[@]}"; do
  cluster_id="${CLUSTER_IDS[$conn_id]}"
  echo "  Adding connection $conn_id (cluster: $cluster_id)..."

  UPDATED_META=$(echo "$UPDATED_META" | jq \
    --arg cid "$conn_id" \
    --arg clid "$cluster_id" \
    '.connections += [{
      "connectionId": "{\"ClusterId\": \"" + $clid + "\", \"DatasourceId\": \"" + $cid + "\"}",
      "kind": "Sql",
      "path": "[dbo]"
    }]')
done

# Step 4: Re-encode and update
echo "Step 4: Updating dataflow definition..."
UPDATED_QUERY_META_B64=$(echo "$UPDATED_META" | base64 -w0)

# Write the body to a temp file and pass it as --body "@<path>".
# DO NOT use inline `--body "{...}"` — embedded escaped quotes + base64 are fragile
# under shell quoting (and outright broken on Windows where az.exe is invoked
# through cmd.exe's argument parser). See SKILL.md MUST DO: pass JSON via @file.
UPDATE_BODY=$(mktemp --suffix=.json 2>/dev/null || mktemp)
jq -n \
  --arg qm "$UPDATED_QUERY_META_B64" \
  --arg mp "$MASHUP_B64" \
  --arg pf "$PLATFORM_B64" \
  '{ definition: { parts: [
       { path: "queryMetadata.json", payload: $qm, payloadType: "InlineBase64" },
       { path: "mashup.pq",          payload: $mp, payloadType: "InlineBase64" },
       { path: ".platform",          payload: $pf, payloadType: "InlineBase64" }
     ]}}' > "$UPDATE_BODY"

# updateDefinition can return 200 (sync) or 202 + Location (LRO). Use curl so we can
# observe the status / Location header, then poll until the operation terminates BEFORE
# the verify step — otherwise the read-back can race the in-flight save and report
# stale connections[]. See § Fabric LRO Polling Pattern.
UPDATE_HDR=$(mktemp); UPDATE_OUT=$(mktemp)
UPDATE_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary @"$UPDATE_BODY" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition" \
  -D "$UPDATE_HDR" -o "$UPDATE_OUT" -w "%{http_code}")
if [ "$UPDATE_CODE" = "202" ]; then
  UPD_LOC=$(tr -d '\r' < "$UPDATE_HDR" | grep -i "^location:" | awk '{print $2}')
  UPD_RETRY=$(tr -d '\r' < "$UPDATE_HDR" | grep -i "^retry-after:" | awk '{print $2}'); UPD_RETRY=${UPD_RETRY:-5}
  while :; do
    sleep "$UPD_RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$UPD_LOC")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) break ;;
      Failed|Cancelled) echo "ERROR: updateDefinition $(echo "$OP" | jq -r '.status')" >&2; echo "$OP" >&2; exit 1 ;;
    esac
  done
elif [ "$UPDATE_CODE" != "200" ] && [ "$UPDATE_CODE" != "201" ]; then
  echo "ERROR: updateDefinition HTTP $UPDATE_CODE" >&2; cat "$UPDATE_OUT" >&2; exit 1
fi

rm -f "$UPDATE_BODY" "$UPDATE_HDR" "$UPDATE_OUT"

# Step 5: Verify connections survived the full-replacement write.
#   updateDefinition replaces all parts atomically, so a malformed queryMetadata.json
#   payload (e.g. doubly-wrapped composite connectionId) saves successfully but with
#   an empty connections[]. Always read-back and assert count > 0 before refreshing.
echo "Step 5: Verifying connections[] survived save..."
VERIFY_HDR=$(mktemp); VERIFY_BODY=$(mktemp)
VERIFY_CODE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$VERIFY_HDR" -o "$VERIFY_BODY" -w "%{http_code}")
if [ "$VERIFY_CODE" = "202" ]; then
  # Fabric LRO: poll operation until terminal status, then GET /result for the payload.
  # A single GET on Location returns the operation status ({"status":"Running",…}), not the definition.
  VERIFY_LOC=$(tr -d '\r' < "$VERIFY_HDR" | grep -i "^location:" | awk '{print $2}')
  VERIFY_RETRY=$(tr -d '\r' < "$VERIFY_HDR" | grep -i "^retry-after:" | awk '{print $2}'); VERIFY_RETRY=${VERIFY_RETRY:-5}
  while :; do
    sleep "$VERIFY_RETRY"
    VERIFY_OP=$(az rest --method get --resource "$RESOURCE" --url "$VERIFY_LOC")
    case "$(echo "$VERIFY_OP" | jq -r '.status // empty')" in
      Succeeded) POST_DEF=$(az rest --method get --resource "$RESOURCE" --url "${VERIFY_LOC%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: post-save getDefinition $(echo "$VERIFY_OP" | jq -r '.status')" >&2; exit 1 ;;
    esac
  done
else
  POST_DEF=$(cat "$VERIFY_BODY")
fi
rm -f "$VERIFY_HDR" "$VERIFY_BODY"
SURVIVING_CONNS=$(echo "$POST_DEF" \
  | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' \
  | base64 -d | jq -r '.connections | length')
if [ "$SURVIVING_CONNS" -lt "${#CONN_IDS[@]}" ]; then
  echo "❌ Expected ${#CONN_IDS[@]} connection(s) after save, found $SURVIVING_CONNS. Aborting before refresh."
  exit 1
fi

echo "✅ Connections bound successfully ($SURVIVING_CONNS in queryMetadata.json)"
```

### PowerShell — Bind a Single Connection to a Dataflow

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$DataflowId,
    [Parameter(Mandatory)][string]$ConnectionId
)

$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$api = "https://api.fabric.microsoft.com/v1"
$resource = "https://api.fabric.microsoft.com"

Write-Host "Binding connection $ConnectionId to dataflow..."

# Step 1: Get definition
# getDefinition can return 200 (sync, body inline) or 202 + Location header (LRO).
# az rest cannot capture response headers, so use Invoke-WebRequest with an az-acquired token.
Write-Host "Step 1: Fetching definition..."
$token = az account get-access-token --resource $resource --query accessToken -o tsv
$headers = @{ Authorization = "Bearer $token"; "Content-Length" = "0" }
try {
    $resp = Invoke-WebRequest -Method Post -Uri "$api/workspaces/$WorkspaceId/dataflows/$DataflowId/getDefinition" `
        -Headers $headers -UseBasicParsing
} catch {
    Write-Error "getDefinition failed: $_"; exit 1
}
if ($resp.StatusCode -eq 202) {
    # Fabric LRO: poll operation state, then GET /result. See § Fabric LRO Polling Pattern.
    $location = $resp.Headers["Location"]
    if ($location -is [array]) { $location = $location[0] }
    $retryRaw = $resp.Headers["Retry-After"]
    if ($retryRaw -is [array]) { $retryRaw = $retryRaw[0] }
    $retryAfter = 5; [void][int]::TryParse([string]$retryRaw, [ref]$retryAfter)
    $result = $null
    while ($null -eq $result) {
        Start-Sleep -Seconds $retryAfter
        $op = az rest --method get --resource $resource --url $location | ConvertFrom-Json
        switch ($op.status) {
            'Succeeded' { $result = az rest --method get --resource $resource --url "$($location.TrimEnd('/'))/result" | ConvertFrom-Json }
            'Failed'    { Write-Error "getDefinition failed: $($op.error.message)"; exit 1 }
            'Cancelled' { Write-Error "getDefinition cancelled"; exit 1 }
        }
    }
} else {
    $result = $resp.Content | ConvertFrom-Json
}

# Extract parts
$queryMetaB64 = $result.definition.parts | Where-Object { $_.path -eq "queryMetadata.json" } | Select-Object -ExpandProperty payload
$queryMetaJson = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($queryMetaB64))
$queryMeta = $queryMetaJson | ConvertFrom-Json

$mashupB64 = $result.definition.parts | Where-Object { $_.path -eq "mashup.pq" } | Select-Object -ExpandProperty payload
$platformB64 = $result.definition.parts | Where-Object { $_.path -eq ".platform" } | Select-Object -ExpandProperty payload

# Step 2: Get ClusterId (Power BI control-plane endpoint; field is `clusterId`)
# Note: the resource audience here is Power BI, NOT api.fabric.microsoft.com —
# calling the Fabric audience against this URL returns 404. Use the LIST endpoint
# and filter by `id`; the per-id route (gatewayClusterDatasources/$ConnectionId)
# returns PowerBIEntityNotFound for cloud connections.
Write-Host "Step 2: Retrieving ClusterId for $ConnectionId..."
$pbiResource = "https://analysis.windows.net/powerbi/api"
$dsList = az rest --method get --resource $pbiResource `
    --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" | ConvertFrom-Json
$clusterId = ($dsList.value | Where-Object { $_.id -eq $ConnectionId } | Select-Object -First 1).clusterId
Write-Host "  ClusterId: $clusterId"

# Step 3: Add connection to queryMetadata.
# connectionId is a STRINGIFIED COMPOSITE — a JSON-string value whose CONTENT
# is itself the JSON object {"ClusterId":"…","DatasourceId":"…"}. Build the
# composite as a plain .NET string here; ConvertTo-Json below will encode it
# (escape its inner quotes) exactly once. Wrapping it in extra literal `"…`"
# produces a doubly-quoted string that Fabric rejects silently (refresh binds
# to no datasource).
Write-Host "Step 3: Adding connection to queryMetadata..."
# Ensure the queryMetadata object actually has a `connections` property — a PSCustomObject
# produced by ConvertFrom-Json rejects `+=` on a missing property ("cannot be found on this
# object"), so we must materialize the array first for definitions that omit connections[].
if (-not $queryMeta.PSObject.Properties['connections']) {
    $queryMeta | Add-Member -NotePropertyName connections -NotePropertyValue @()
}
$compositeConnectionId = "{`"ClusterId`": `"$clusterId`", `"DatasourceId`": `"$ConnectionId`"}"
$connectionEntry = @{
    connectionId = $compositeConnectionId
    kind = "Sql"
    path = "[dbo]"
}
$queryMeta.connections += $connectionEntry

# Step 4: Update definition
Write-Host "Step 4: Updating dataflow..."
# -Depth 10: queryMetadata.json has nested queriesMetadata + connections[] objects; the
# default depth (2) silently serializes them as "@{...}" placeholders, base64-encoding
# corruption into the saved definition. Always pass an explicit depth here.
$updatedQueryMetaJson = $queryMeta | ConvertTo-Json -Depth 10 -Compress
$updatedQueryMetaB64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($updatedQueryMetaJson))

$body = @{
    definition = @{
        parts = @(
            @{ path = "queryMetadata.json"; payload = $updatedQueryMetaB64; payloadType = "InlineBase64" },
            @{ path = "mashup.pq"; payload = $mashupB64; payloadType = "InlineBase64" },
            @{ path = ".platform"; payload = $platformB64; payloadType = "InlineBase64" }
        )
    }
} | ConvertTo-Json -Depth 10 -Compress

# Write the body to a temp file with UTF-8 (no BOM) and pass via --body "@<path>".
# DO NOT use `--body $body` inline — cmd.exe argument parsing mangles the embedded
# quotes and base64, which is the root cause of flaky-test #132.
$bodyFile = Join-Path $env:TEMP "df-bind-$([guid]::NewGuid()).json"
[System.IO.File]::WriteAllText($bodyFile, $body, [System.Text.UTF8Encoding]::new($false))

try {
    # updateDefinition can return 200 (sync) or 202 + Location (LRO). Use Invoke-WebRequest
    # so we can observe the status / Location header, then poll until the operation
    # terminates BEFORE the verify step — otherwise the read-back can race the in-flight
    # save and report stale connections[]. See § Fabric LRO Polling Pattern.
    $updResp = Invoke-WebRequest -Method Post -Uri "$api/workspaces/$WorkspaceId/dataflows/$DataflowId/updateDefinition" `
        -Headers @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" } `
        -InFile $bodyFile -UseBasicParsing
    if ($updResp.StatusCode -eq 202) {
        $updLoc = $updResp.Headers["Location"]
        if ($updLoc -is [array]) { $updLoc = $updLoc[0] }
        $updRetryRaw = $updResp.Headers["Retry-After"]
        if ($updRetryRaw -is [array]) { $updRetryRaw = $updRetryRaw[0] }
        $updRetry = 5; [void][int]::TryParse([string]$updRetryRaw, [ref]$updRetry)
        while ($true) {
            Start-Sleep -Seconds $updRetry
            $op = az rest --method get --resource $resource --url $updLoc | ConvertFrom-Json
            if ($op.status -eq 'Succeeded')    { break }
            if ($op.status -eq 'Failed')       { Write-Error "updateDefinition failed: $($op.error.message)"; exit 1 }
            if ($op.status -eq 'Cancelled')    { Write-Error "updateDefinition cancelled"; exit 1 }
        }
    }
} finally {
    Remove-Item -Path $bodyFile -ErrorAction SilentlyContinue
}

# Step 5: Verify connections survived the full-replacement write.
Write-Host "Step 5: Verifying connections[] survived save..."
try {
    $verifyResp = Invoke-WebRequest -Method Post -Uri "$api/workspaces/$WorkspaceId/dataflows/$DataflowId/getDefinition" `
        -Headers $headers -UseBasicParsing
} catch {
    Write-Error "Post-save getDefinition failed: $_"; exit 1
}
if ($verifyResp.StatusCode -eq 202) {
    # Fabric LRO: poll operation until terminal status, then GET /result for the payload.
    # A single GET on Location returns {status:"Running",…}, NOT the definition.
    $verifyLoc = $verifyResp.Headers["Location"]
    if ($verifyLoc -is [array]) { $verifyLoc = $verifyLoc[0] }
    $verifyRetryRaw = $verifyResp.Headers["Retry-After"]
    if ($verifyRetryRaw -is [array]) { $verifyRetryRaw = $verifyRetryRaw[0] }
    $verifyRetry = 5; [void][int]::TryParse([string]$verifyRetryRaw, [ref]$verifyRetry)
    $postDef = $null
    while ($null -eq $postDef) {
        Start-Sleep -Seconds $verifyRetry
        $op = az rest --method get --resource $resource --url $verifyLoc | ConvertFrom-Json
        switch ($op.status) {
            'Succeeded' { $postDef = az rest --method get --resource $resource --url "$($verifyLoc.TrimEnd('/'))/result" | ConvertFrom-Json }
            'Failed'    { Write-Error "Post-save getDefinition failed: $($op.error.message)"; exit 1 }
            'Cancelled' { Write-Error "Post-save getDefinition cancelled"; exit 1 }
        }
    }
} else {
    $postDef = $verifyResp.Content | ConvertFrom-Json
}
$postQmB64 = $postDef.definition.parts | Where-Object { $_.path -eq "queryMetadata.json" } | Select-Object -ExpandProperty payload
$postQmJson = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($postQmB64))
$postQm = $postQmJson | ConvertFrom-Json
$survivingConns = @($postQm.connections).Count
if ($survivingConns -lt 1) {
    Write-Error "Expected at least 1 connection after save, found $survivingConns. Aborting before refresh."
    exit 1
}

Write-Host "✅ Connection bound successfully ($survivingConns in queryMetadata.json)" -ForegroundColor Green
```

## Connection Creation Templates

For schemas, decision tree, credential variants, and pitfalls, see [connection-management.md](connection-management.md). The templates below cover the most common case (cloud SQL with Basic auth) and are designed to compose with the existing **Connection Binding** templates above.

### Bash — Create Cloud SQL Connection (Basic auth)

Schema-accurate `POST /v1/connections` using `passwordReference` (Key Vault-backed via a Fabric Key Vault connection).

```bash
#!/usr/bin/env bash
set -euo pipefail

API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"

DISPLAY_NAME="${DISPLAY_NAME:?Set DISPLAY_NAME (e.g. ContosoSqlConnection)}"
SQL_SERVER="${SQL_SERVER:?Set SQL_SERVER}"
SQL_DATABASE="${SQL_DATABASE:?Set SQL_DATABASE}"
SQL_USER="${SQL_USER:?Set SQL_USER}"
KV_CONN_ID="${KV_CONN_ID:?Set KV_CONN_ID to the Fabric Key Vault connection id}"
KV_SECRET_NAME="${KV_SECRET_NAME:?Set KV_SECRET_NAME}"

command -v az >/dev/null 2>&1 || { echo "ERROR: az CLI not found."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }
az account show >/dev/null 2>&1 || { echo "Run 'az login' first."; exit 1; }

# Step 1 — list supported types and confirm parameter names match
az rest --method get --resource "$RESOURCE" \
  --url "$API/connections/supportedConnectionTypes" \
  --query "value[?type=='SQL'].creationMethods[].parameters[].{name:name,dataType:dataType,required:required}" \
  --output table

# Step 2 — build the Key Vault-backed credentials block
CREDENTIALS=$(jq -n \
  --arg user "$SQL_USER" \
  --arg kvConn "$KV_CONN_ID" --arg secret "$KV_SECRET_NAME" \
  '{ credentialType: "Basic", username: $user,
     passwordReference: { connectionId: $kvConn, secretName: $secret } }')

# Step 3 — assemble the request body
BODY=$(jq -n \
  --arg name "$DISPLAY_NAME" \
  --arg server "$SQL_SERVER" --arg db "$SQL_DATABASE" \
  --argjson creds "$CREDENTIALS" \
  '{
    connectivityType: "ShareableCloud",
    displayName: $name,
    connectionDetails: {
      type: "SQL", creationMethod: "SQL",
      parameters: [
        { dataType: "Text", name: "server",   value: $server },
        { dataType: "Text", name: "database", value: $db }
      ]
    },
    privacyLevel: "Organizational",
    credentialDetails: {
      singleSignOnType: "None",
      connectionEncryption: "Encrypted",
      skipTestConnection: false,
      credentials: $creds
    }
  }')

# Step 4 — create and capture the plain-GUID id
NEW_CONN_ID=$(az rest --method post --resource "$RESOURCE" \
  --url "$API/connections" --body "$BODY" \
  --query "id" --output tsv)

echo "✅ Created connection: $NEW_CONN_ID ($DISPLAY_NAME)"
echo "    Use NEW_CONN_ID with the Bash — Bind Connection template above."
```

### PowerShell — Create Cloud SQL Connection (Basic auth)

```powershell
# Schema-accurate POST /v1/connections (cloud, Basic auth)
# Requires passwordReference (Key Vault-backed via a Fabric Key Vault connection).

param(
    [Parameter(Mandatory=$true)] [string]$DisplayName,
    [Parameter(Mandatory=$true)] [string]$Server,
    [Parameter(Mandatory=$true)] [string]$Database,
    [Parameter(Mandatory=$true)] [string]$Username,
    [Parameter(Mandatory=$true)] [string]$KvConnectionId,
    [Parameter(Mandatory=$true)] [string]$KvSecretName
)

$api      = "https://api.fabric.microsoft.com/v1"
$resource = "https://api.fabric.microsoft.com"

# Step 1 — confirm parameter names from the live tenant
az rest --method get --resource $resource `
    --url "$api/connections/supportedConnectionTypes" `
    --query "value[?type=='SQL'].creationMethods[].parameters[].{name:name,required:required}" `
    --output table

# Step 2 — build the Key Vault-backed credentials block
$credentials = @{
    credentialType = "Basic"
    username = $Username
    passwordReference = @{
        connectionId = $KvConnectionId
        secretName = $KvSecretName
    }
}

# Step 3 — assemble request body
$body = @{
    connectivityType = "ShareableCloud"
    displayName = $DisplayName
    connectionDetails = @{
        type = "SQL"
        creationMethod = "SQL"
        parameters = @(
            @{ dataType = "Text"; name = "server";   value = $Server },
            @{ dataType = "Text"; name = "database"; value = $Database }
        )
    }
    privacyLevel = "Organizational"
    credentialDetails = @{
        singleSignOnType = "None"
        connectionEncryption = "Encrypted"
        skipTestConnection = $false
        credentials = $credentials
    }
} | ConvertTo-Json -Depth 10 -Compress

# Step 4 — create and capture the plain-GUID id.
# Write body to a UTF-8 (no-BOM) temp file and pass via --body "@<path>".
# DO NOT use `--body $body` inline on Windows — cmd.exe argument parsing mangles
# the embedded quotes (same root cause as flaky-test #132 for dataflow create/update).
$bodyFile = Join-Path $env:TEMP "conn-create-$([guid]::NewGuid()).json"
[System.IO.File]::WriteAllText($bodyFile, $body, [System.Text.UTF8Encoding]::new($false))

try {
    $newConnId = az rest --method post --resource $resource `
        --url "$api/connections" --body "@$bodyFile" `
        --query "id" --output tsv
} finally {
    Remove-Item -Path $bodyFile -ErrorAction SilentlyContinue
}

Write-Host "✅ Created connection: $newConnId ($DisplayName)" -ForegroundColor Green
Write-Host "   Use `$newConnId with the PowerShell — Bind Connection template above."
```



---

## End-to-End Smoke Test  Create + Bootstrap + Preview + Update + Refresh

This is the **canonical happy-path** flow for a brand-new dataflow with a credentialed source. It is the script that was live-validated against `DataflowTests` workspace on 2026-05-13 (Northwind OData, PersonalCloud anonymous). Use it as the smoke-test starting point when introducing a new connection type or validating skill changes.

**The five-step contract** the script enforces:

1. **Create** the dataflow via `POST /v1/workspaces/{ws}/dataflows` with `displayName` + all three definition parts.
2. **Bootstrap-save** via `updateDefinition`  *required* before the first `executeQuery` against a credentialed source, even if the create payload already included `queryMetadata.connections[]`. Without this save, preview fails with `"Credentials are required to connect to the <source> source"`.
3. **Preview** the candidate `customMashupDocument` via `executeQuery` (with a `Table.FirstN` cap). Check the Arrow stream for an embedded `{"Error":"..."}` marker.
4. **Persist** the validated mashup via `updateDefinition` (strip the cap before saving).
5. **Refresh** via `POST /v1/workspaces/{ws}/dataflows/{df}/jobs/instances?jobType=Refresh`; poll the job-instance enum (`NotStarted` / `InProgress` / **`Completed`** / `Failed` / `Cancelled`)  see `references/authoring-cli-quickref.md  Status Enum Reference`.

**Preconditions** the script assumes:

- Workspace ID is on a capacity that supports Dataflow Gen2.
- A connection of the target type exists in the tenant; for cloud-only public sources prefer a `PersonalCloud` connection (see `connection-management.md  Picking between PersonalCloud and OnPremisesGateway`).

### PowerShell  E2E Smoke Test

```powershell
$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'

# ============== Config (caller fills these in) ==============
$resource    = 'https://api.fabric.microsoft.com'
$pbiResource = 'https://analysis.windows.net/powerbi/api'
$wsId        = '<workspace-guid>'
$connId      = '<connection-guid>'            # PersonalCloud anonymous OData for the smoke test
$sourceUrl   = 'http://services.odata.org/V3/Northwind/Northwind.svc'
$sourceKind  = 'OData'
$dfName      = "skill-e2e-test-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# ============== Step 0: ClusterId for the composite connectionId ==============
# List the user's gateway-cluster datasources and filter by `id`. The per-id
# route (.../gatewayClusterDatasources/$connId) returns PowerBIEntityNotFound
# for cloud connections.
$dsList = az rest --method get --resource $pbiResource `
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" | ConvertFrom-Json
$clusterId = ($dsList.value | Where-Object { $_.id -eq $connId } | Select-Object -First 1).clusterId
$composite = @{ ClusterId = $clusterId; DatasourceId = $connId } | ConvertTo-Json -Compress

# ============== Step 1: Create dataflow ==============
$logicalId = [guid]::NewGuid().ToString()
$queryId   = [guid]::NewGuid().ToString()

# Bootstrap mashup. loadEnabled defaults to true (Fabric auto-attaches a staging Lakehouse and loads every
# query to it by default). Set false only on helper queries you do NOT want loaded. Refresh with
# executeOption = ApplyChangesIfNeeded to reconcile the draft state of an API-created dataflow.
$mashup = @"
section Section1;
shared Customers = let
    Source = OData.Feed("$sourceUrl", null, [Implementation="2.0"]),
    Customers_table = Source{[Name="Customers",Signature="table"]}[Data],
    Selected = Table.SelectColumns(Customers_table, {"CustomerID","CompanyName","Country","City"})
in
    Selected;
"@

$queryMeta = @{
  formatVersion   = '202502'
  name            = $dfName
  queriesMetadata = @{ Customers = @{ queryId = $queryId; queryName = 'Customers' } }   # loadEnabled omitted = load (default)
  connections     = @(@{ path = $sourceUrl; kind = $sourceKind; connectionId = $composite })
} | ConvertTo-Json -Depth 8 -Compress

$platform = @{
  '$schema' = 'https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json'
  metadata  = @{ type = 'Dataflow'; displayName = $dfName }
  config    = @{ version = '2.0'; logicalId = $logicalId }
} | ConvertTo-Json -Depth 6 -Compress

$enc = [System.Text.Encoding]::UTF8
$body = @{
  displayName = $dfName
  definition  = @{ parts = @(
    @{ path = 'mashup.pq';          payload = [Convert]::ToBase64String($enc.GetBytes($mashup));    payloadType = 'InlineBase64' }
    @{ path = 'queryMetadata.json'; payload = [Convert]::ToBase64String($enc.GetBytes($queryMeta)); payloadType = 'InlineBase64' }
    @{ path = '.platform';          payload = [Convert]::ToBase64String($enc.GetBytes($platform));  payloadType = 'InlineBase64' }
  ) }
} | ConvertTo-Json -Depth 8 -Compress

$bodyFile = Join-Path $env:TEMP "df-body-$([guid]::NewGuid()).json"
[System.IO.File]::WriteAllText($bodyFile, $body, [System.Text.UTF8Encoding]::new($false))
try {
  $token = az account get-access-token --resource $resource --query accessToken -o tsv
  $resp = Invoke-WebRequest -Method POST -UseBasicParsing `
    -Uri "$resource/v1/workspaces/$wsId/dataflows" `
    -Headers @{ Authorization = "Bearer $token"; 'Content-Type' = 'application/json' } `
    -InFile $bodyFile
} finally { Remove-Item -Path $bodyFile -ErrorAction SilentlyContinue }

# Handle 201 sync / 202 LRO (Succeeded  /result for the dataflow id)
if ($resp.StatusCode -eq 201) {
  $dfId = ($resp.Content | ConvertFrom-Json).id
} else {
  $loc = $resp.Headers['Location']; if ($loc -is [array]) { $loc = $loc[0] }
  do {
    Start-Sleep -Seconds 5
    $op = az rest --method get --resource $resource --url $loc | ConvertFrom-Json
  } until ($op.status -in 'Succeeded','Failed','Cancelled')
  if ($op.status -ne 'Succeeded') { throw "Create $($op.status)" }
  $dfId = (az rest --method get --resource $resource --url "$($loc.TrimEnd('/'))/result" | ConvertFrom-Json).id
}
Write-Host "Created dataflow: $dfId"

# ============== Step 2: Bootstrap save (REQUIRED for credentialed sources) ==============
# Persists the connections[] binding into the preview engine's context.
# Without this, the next executeQuery returns: {"Error":"Credentials are required..."}
$updBody = @{ definition = @{ parts = @(
    @{ path = 'mashup.pq';          payload = [Convert]::ToBase64String($enc.GetBytes($mashup));    payloadType = 'InlineBase64' }
    @{ path = 'queryMetadata.json'; payload = [Convert]::ToBase64String($enc.GetBytes($queryMeta)); payloadType = 'InlineBase64' }
    @{ path = '.platform';          payload = [Convert]::ToBase64String($enc.GetBytes($platform));  payloadType = 'InlineBase64' }
) } } | ConvertTo-Json -Depth 8 -Compress
$updFile = Join-Path $env:TEMP "df-upd-$([guid]::NewGuid()).json"
[System.IO.File]::WriteAllText($updFile, $updBody, [System.Text.UTF8Encoding]::new($false))
try {
  $token = az account get-access-token --resource $resource --query accessToken -o tsv
  $u = Invoke-WebRequest -Method POST -UseBasicParsing `
    -Uri "$resource/v1/workspaces/$wsId/dataflows/$dfId/updateDefinition" `
    -Headers @{ Authorization = "Bearer $token"; 'Content-Type' = 'application/json' } `
    -InFile $updFile
} finally { Remove-Item -Path $updFile -ErrorAction SilentlyContinue }
if ($u.StatusCode -eq 202) {
  $loc = $u.Headers['Location']; if ($loc -is [array]) { $loc = $loc[0] }
  do {
    Start-Sleep -Seconds 5
    $op = az rest --method get --resource $resource --url $loc | ConvertFrom-Json
  } until ($op.status -in 'Succeeded','Failed','Cancelled')
  if ($op.status -ne 'Succeeded') { throw "Bootstrap save $($op.status)" }
}
Write-Host "Bootstrap save complete"

# ============== Step 3: Preview via executeQuery (Table.FirstN-capped) ==============
$candidate = @"
section Section1;
shared Customers = let
    Source = OData.Feed("$sourceUrl", null, [Implementation="2.0"]),
    Customers_table = Source{[Name="Customers",Signature="table"]}[Data],
    Selected = Table.SelectColumns(Customers_table, {"CustomerID","CompanyName","Country","City"}),
    Preview = Table.FirstN(Selected, 5)
in
    Preview;
"@
$execBody = @{ QueryName = 'Customers'; customMashupDocument = $candidate } | ConvertTo-Json -Compress
$execFile = Join-Path $env:TEMP "df-exec-$([guid]::NewGuid()).json"
[System.IO.File]::WriteAllText($execFile, $execBody, [System.Text.UTF8Encoding]::new($false))
$arrowFile = Join-Path $env:TEMP "preview-$([guid]::NewGuid()).arrow"
try {
  az rest --method post --resource $resource `
    --url "$resource/v1/workspaces/$wsId/dataflows/$dfId/executeQuery" `
    --headers 'Content-Type=application/json' --body "@$execFile" --output-file $arrowFile | Out-Null
} finally { Remove-Item -Path $execFile -ErrorAction SilentlyContinue }
$arrowText = [System.IO.File]::ReadAllText($arrowFile, [System.Text.Encoding]::UTF8)
if ($arrowText -match '\{"Error":') {
  $i = $arrowText.IndexOf('{"Error":')
  throw "Preview error: $($arrowText.Substring($i, [Math]::Min(400, $arrowText.Length - $i)))"
}
Remove-Item $arrowFile
Write-Host 'Preview OK'

# ============== Step 4: Persist validated mashup ==============
# Strip the Table.FirstN preview cap so the saved mashup returns all rows.
# Reuses $queryMeta, $platform, $enc from Step 1; same Invoke-WebRequest + LRO branch
# as Step 2's bootstrap save. Skipping this step leaves the bootstrap (full-row) mashup
# in place — fine for this Northwind smoke test, but in real use you'd never preview a
# different candidate than the one you save.
$finalMashup = @"
section Section1;
shared Customers = let
    Source = OData.Feed("$sourceUrl", null, [Implementation="2.0"]),
    Customers_table = Source{[Name="Customers",Signature="table"]}[Data],
    Selected = Table.SelectColumns(Customers_table, {"CustomerID","CompanyName","Country","City"})
in
    Selected;
"@
$saveBody = @{ definition = @{ parts = @(
    @{ path = 'mashup.pq';          payload = [Convert]::ToBase64String($enc.GetBytes($finalMashup)); payloadType = 'InlineBase64' }
    @{ path = 'queryMetadata.json'; payload = [Convert]::ToBase64String($enc.GetBytes($queryMeta));   payloadType = 'InlineBase64' }
    @{ path = '.platform';          payload = [Convert]::ToBase64String($enc.GetBytes($platform));    payloadType = 'InlineBase64' }
) } } | ConvertTo-Json -Depth 8 -Compress
$saveFile = Join-Path $env:TEMP "df-save-$([guid]::NewGuid()).json"
[System.IO.File]::WriteAllText($saveFile, $saveBody, [System.Text.UTF8Encoding]::new($false))
try {
  $token = az account get-access-token --resource $resource --query accessToken -o tsv
  $s = Invoke-WebRequest -Method POST -UseBasicParsing `
    -Uri "$resource/v1/workspaces/$wsId/dataflows/$dfId/updateDefinition" `
    -Headers @{ Authorization = "Bearer $token"; 'Content-Type' = 'application/json' } `
    -InFile $saveFile
} finally { Remove-Item -Path $saveFile -ErrorAction SilentlyContinue }
if ($s.StatusCode -eq 202) {
  $loc = $s.Headers['Location']; if ($loc -is [array]) { $loc = $loc[0] }
  do {
    Start-Sleep -Seconds 5
    $op = az rest --method get --resource $resource --url $loc | ConvertFrom-Json
  } until ($op.status -in 'Succeeded','Failed','Cancelled')
  if ($op.status -ne 'Succeeded') { throw "Final save $($op.status)" }
}
Write-Host 'Final save complete'

# ============== Step 5: Trigger refresh + poll job-instance enum ==============
$token = az account get-access-token --resource $resource --query accessToken -o tsv
$r = Invoke-WebRequest -Method POST -UseBasicParsing `
  -Uri "$resource/v1/workspaces/$wsId/dataflows/$dfId/jobs/instances?jobType=Refresh" `
  -Headers @{ Authorization = "Bearer $token"; 'Content-Length' = '0' }
$refreshLoc = $r.Headers['Location']; if ($refreshLoc -is [array]) { $refreshLoc = $refreshLoc[0] }

# Note: refresh poll uses the JOB-INSTANCE enum: terminal-success = "Completed" (NOT "Succeeded").
while ($true) {
  $status = az rest --method get --url $refreshLoc --resource $resource --query 'status' -o tsv
  Write-Host "Refresh status: $status"
  if ($status -in 'Completed','Failed','Cancelled') { break }
  Start-Sleep -Seconds 10
}
if ($status -ne 'Completed') { throw "Refresh $status (expected Completed)" }
Write-Host 'E2E smoke passed.'
```

### Bash  E2E Smoke Test

The bash variant is structurally identical. Reuse the LRO and refresh-poll patterns from earlier sections:

- Create:  Bash Templates  `Create Dataflow with Definition`
- Bootstrap save and final save:  Bash  Read-Modify-Write Dataflow Definition (LRO-aware version)
- Preview:  Mashup Preview (`executeQuery` + Arrow `{"Error":"..."}` detection)
- Refresh:  Bash  Trigger Dataflow Refresh and Poll (terminal-success = `Completed`)
# Script Templates

Self-contained templates for dataflow consumption via CLI. Copy-paste and customize.

## Bash — List Dataflows with Pagination

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
WS_ID="${WS_ID:?Set WS_ID env var (workspace ID)}"
API="https://api.fabric.microsoft.com/v1"

# --- Prerequisites ---
az account show >/dev/null 2>&1 || { echo "ERROR: Not logged in. Run: az login"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found. Install: apt-get install jq"; exit 1; }

# --- Paginated listing ---
echo "Dataflows in workspace $WS_ID:"
echo "---"
URL="$API/workspaces/$WS_ID/dataflows"
COUNT=0
while [ -n "$URL" ]; do
  RESPONSE=$(az rest --method get --resource "https://api.fabric.microsoft.com" --url "$URL")
  echo "$RESPONSE" | jq -r '.value[] | "\(.displayName)\t\(.id)"'
  PAGE_COUNT=$(echo "$RESPONSE" | jq '.value | length')
  COUNT=$((COUNT + PAGE_COUNT))
  TOKEN=$(echo "$RESPONSE" | jq -r '.continuationToken // empty')
  if [ -n "$TOKEN" ]; then
    URL="$API/workspaces/$WS_ID/dataflows?continuationToken=$TOKEN"
  else
    URL=""
  fi
done
echo "---"
echo "✓ Total: $COUNT dataflow(s)"
```

## Bash — Full Definition Decode and Report

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
WS_ID="${WS_ID:?Set WS_ID env var}"
DF_ID="${DF_ID:?Set DF_ID env var (dataflow ID)}"
API="https://api.fabric.microsoft.com/v1"
OUTPUT_DIR="${1:-.}"

# --- Prerequisites ---
az account show >/dev/null 2>&1 || { echo "ERROR: Run 'az login' first."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }
mkdir -p "$OUTPUT_DIR"

# --- Get dataflow name ---
DF_NAME=$(az rest --method get --resource "https://api.fabric.microsoft.com" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID" --query "displayName" -o tsv)
echo "=== Dataflow: $DF_NAME ==="

# --- Get definition ---
echo "Fetching definition..."
RESPONSE=$(az rest --method post --resource "https://api.fabric.microsoft.com" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition")

# --- Decode and save each part ---
for PART in "mashup.pq" "queryMetadata.json" ".platform"; do
  FILENAME=$(basename "$PART")
  echo "$RESPONSE" | jq -r ".definition.parts[] | select(.path==\"$PART\") | .payload" | \
    base64 --decode > "$OUTPUT_DIR/$FILENAME"
  echo "✓ Decoded $PART → $OUTPUT_DIR/$FILENAME"
done

# --- Report: Queries ---
echo ""
echo "=== Queries ==="
grep -oP '(?<=shared )\w+(?= =)' "$OUTPUT_DIR/mashup.pq" | while read -r QUERY; do
  echo "  - $QUERY"
done

# --- Report: Connections ---
echo ""
echo "=== Connections ==="
jq -r '.connections[] | "  - [\(.kind)] \(.path)"' "$OUTPUT_DIR/queryMetadata.json"

# --- Report: Load-enabled queries ---
echo ""
echo "=== Output Queries (loadEnabled=true) ==="
jq -r '.queriesMetadata | to_entries[] | select(.value.loadEnabled==true) | "  - \(.key)"' "$OUTPUT_DIR/queryMetadata.json"

echo ""
echo "✓ Definition report complete. Files saved to $OUTPUT_DIR/"
```

## Bash — Monitor Refresh with Polling Loop

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
WS_ID="${WS_ID:?Set WS_ID env var}"
DF_ID="${DF_ID:?Set DF_ID env var}"
API="https://api.fabric.microsoft.com/v1"
MAX_WAIT="${MAX_WAIT:-3600}"  # 60 minutes default
POLL_INTERVAL=5

# --- Prerequisites ---
az account show >/dev/null 2>&1 || { echo "ERROR: Run 'az login' first."; exit 1; }

# --- Get latest job instance ---
echo "Checking latest job for dataflow $DF_ID..."
LATEST=$(az rest --method get --resource "https://api.fabric.microsoft.com" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances" \
  --query "value[0]")

STATUS=$(echo "$LATEST" | jq -r '.status')
JOB_ID=$(echo "$LATEST" | jq -r '.id')
echo "Job $JOB_ID — Status: $STATUS"

if [ "$STATUS" = "Completed" ] || [ "$STATUS" = "Failed" ] || [ "$STATUS" = "Cancelled" ]; then
  echo "Job already in terminal state."
  echo "$LATEST" | jq '{status, invokeType, startTimeUtc, endTimeUtc, failureReason}'
  exit 0
fi

# --- Poll until terminal ---
ELAPSED=0
while [ "$ELAPSED" -lt "$MAX_WAIT" ]; do
  sleep "$POLL_INTERVAL"
  ELAPSED=$((ELAPSED + POLL_INTERVAL))

  STATUS=$(az rest --method get --resource "https://api.fabric.microsoft.com" \
    --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances" \
    --query "value[0].status" -o tsv)

  echo "[${ELAPSED}s] Status: $STATUS"

  case "$STATUS" in
    Completed|Failed|Cancelled)
      echo "✓ Job reached terminal state: $STATUS"
      az rest --method get --resource "https://api.fabric.microsoft.com" \
        --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances" \
        --query "value[0]"
      exit 0
      ;;
  esac

  # Exponential backoff: 5 → 10 → 20 → 30 (cap)
  if [ "$POLL_INTERVAL" -lt 30 ]; then
    POLL_INTERVAL=$((POLL_INTERVAL * 2))
    [ "$POLL_INTERVAL" -gt 30 ] && POLL_INTERVAL=30
  fi
done

echo "⚠ Timeout after ${MAX_WAIT}s. Last status: $STATUS"
exit 1
```

## Bash — Parameter Discovery Report

```bash
#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
WS_ID="${WS_ID:?Set WS_ID env var}"
DF_ID="${DF_ID:?Set DF_ID env var}"
API="https://api.fabric.microsoft.com/v1"

# --- Prerequisites ---
az account show >/dev/null 2>&1 || { echo "ERROR: Run 'az login' first."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "ERROR: jq not found."; exit 1; }

# --- Get dataflow name ---
DF_NAME=$(az rest --method get --resource "https://api.fabric.microsoft.com" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID" --query "displayName" -o tsv)
echo "=== Parameters for: $DF_NAME ==="
echo ""

# --- Discover parameters ---
PARAMS=$(az rest --method get --resource "https://api.fabric.microsoft.com" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/parameters" 2>&1) || {
  echo "No parameters found (dataflow may not be parametric)."
  exit 0
}

PARAM_COUNT=$(echo "$PARAMS" | jq '.value | length')
if [ "$PARAM_COUNT" -eq 0 ]; then
  echo "No parameters defined."
  exit 0
fi

echo "$PARAMS" | jq -r '.value[] | "Parameter: \(.name)\n  Type:     \(.type)\n  Required: \(.isRequired)\n  Default:  \(.defaultValue // "none")\n  Desc:     \(.description // "none")\n"'

echo "---"
echo "✓ $PARAM_COUNT parameter(s) discovered"
```

## PowerShell — List Dataflows

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$WorkspaceId
)

$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$API = "https://api.fabric.microsoft.com/v1"
$url = "$API/workspaces/$WorkspaceId/dataflows"
$allDataflows = @()

do {
    $response = az rest --method get --resource "https://api.fabric.microsoft.com" --url $url | ConvertFrom-Json
    $allDataflows += $response.value
    if ($response.continuationToken) {
        $url = "$API/workspaces/$WorkspaceId/dataflows?continuationToken=$($response.continuationToken)"
    } else {
        $url = $null
    }
} while ($url)

$allDataflows | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.displayName
        Id   = $_.id
        Desc = $_.description
    }
} | Format-Table -AutoSize

Write-Host "Total: $($allDataflows.Count) dataflow(s)"
```

## PowerShell — Definition Decode

> **⚠ LRO caveat:** the `az rest --method post .../getDefinition` call below assumes a synchronous 200 response. The Fabric API may return **202 + Location** (large definitions, server load). For production code, use the `Invoke-WebRequest` LRO branch shown immediately below, or copy the [Fabric LRO Polling Pattern](../authoring/authoring-script-templates.md#fabric-lro-polling-pattern) PowerShell branch into your script.

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$DataflowId,
    [string]$OutputDir = "."
)

$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$API = "https://api.fabric.microsoft.com/v1"
$resource = "https://api.fabric.microsoft.com"
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# getDefinition is an LRO. az rest cannot surface response headers, so use Invoke-WebRequest
# to capture the 202/Location case, then poll per Fabric LRO contract.
$token = az account get-access-token --resource $resource --query accessToken -o tsv
$headers = @{ Authorization = "Bearer $token"; "Content-Length" = "0" }
try {
    $resp = Invoke-WebRequest -Method Post -Uri "$API/workspaces/$WorkspaceId/dataflows/$DataflowId/getDefinition" `
        -Headers $headers -UseBasicParsing
} catch {
    Write-Error "getDefinition failed: $($_.Exception.Message)"; exit 1
}
if ($resp.StatusCode -eq 202) {
    $location = $resp.Headers["Location"]
    if ($location -is [array]) { $location = $location[0] }
    $retryRaw = $resp.Headers["Retry-After"]
    if ($retryRaw -is [array]) { $retryRaw = $retryRaw[0] }
    $retryAfter = 5; [void][int]::TryParse([string]$retryRaw, [ref]$retryAfter)
    $response = $null
    while ($null -eq $response) {
        Start-Sleep -Seconds $retryAfter
        $op = az rest --method get --resource $resource --url $location | ConvertFrom-Json
        switch ($op.status) {
            'Succeeded' { $response = az rest --method get --resource $resource --url "$($location.TrimEnd('/'))/result" | ConvertFrom-Json }
            'Failed'    { Write-Error "getDefinition failed: $($op.error.message)"; exit 1 }
            'Cancelled' { Write-Error "getDefinition cancelled"; exit 1 }
        }
    }
} else {
    $response = $resp.Content | ConvertFrom-Json
}

foreach ($part in $response.definition.parts) {
    $filename = Split-Path $part.path -Leaf
    $decoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($part.payload))
    Set-Content -Path (Join-Path $OutputDir $filename) -Value $decoded -Encoding UTF8
    Write-Host "Decoded $($part.path) -> $OutputDir\$filename"
}

Write-Host "`nDone. Files saved to $OutputDir"
```

## PowerShell — Job History Report

```powershell
#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$WorkspaceId,
    [Parameter(Mandatory)][string]$DataflowId
)

$null = az account show 2>$null
if ($LASTEXITCODE -ne 0) { Write-Error "Not logged in. Run: az login"; exit 1 }

$API = "https://api.fabric.microsoft.com/v1"
$jobs = (az rest --method get --resource "https://api.fabric.microsoft.com" `
  --url "$API/workspaces/$WorkspaceId/dataflows/$DataflowId/jobs/instances" | ConvertFrom-Json).value

if (-not $jobs) { Write-Host "No job history found."; exit 0 }

$jobs | ForEach-Object {
    [PSCustomObject]@{
        Status    = $_.status
        Type      = $_.invokeType
        Start     = $_.startTimeUtc
        End       = $_.endTimeUtc
        Error     = $_.failureReason
    }
} | Format-Table -AutoSize

$completed = $jobs | Where-Object { $_.status -eq "Completed" }
$failed = $jobs | Where-Object { $_.status -eq "Failed" }
Write-Host "Summary: $($completed.Count) completed, $($failed.Count) failed, $($jobs.Count) total"
```


## Bash — Query Execution and Arrow Conversion

Execute a query and convert Apache Arrow results to CSV:

```bash
#!/bin/bash

# Configuration
WORKSPACE_ID="${1:?Usage: $0 <workspace_id> <dataflow_id> <query_name>}"
DATAFLOW_ID="${2:?Usage: $0 <workspace_id> <dataflow_id> <query_name>}"
QUERY_NAME="${3:?Usage: $0 <workspace_id> <dataflow_id> <query_name>}"

API="https://api.fabric.microsoft.com/v1"
AZ="az rest --resource https://api.fabric.microsoft.com"

echo "Executing query: $QUERY_NAME from dataflow: $DATAFLOW_ID"

# Execute the query — raw Apache Arrow IPC stream is captured via --output-file (NOT a JSON envelope).
# For persisted queries, send QueryName only — omit customMashupDocument.
ARROW_PATH="${QUERY_NAME}_results.arrow"
$AZ --method post \
  --url "$API/workspaces/$WORKSPACE_ID/dataflows/$DATAFLOW_ID/executeQuery" \
  --body "{\"QueryName\": \"$QUERY_NAME\"}" \
  --output-file "$ARROW_PATH"

if [ ! -s "$ARROW_PATH" ]; then
  echo "ERROR: Empty response from executeQuery"
  exit 1
fi

# Detect embedded source errors — executeQuery returns HTTP 200 even on Kusto/SQL failures;
# the error JSON sits inside the stream's PQ Arrow Metadata block.
if grep -q '"Error":"' "$ARROW_PATH"; then
  echo "ERROR: Query execution failed (embedded in Arrow body):"
  python3 -c "import re,sys; raw=open(sys.argv[1],'rb').read().decode('utf-8','replace'); m=re.search(r'\\{\"Error\":\"[^\"]+\"\\}', raw); print(m.group(0) if m else '(error marker present, JSON not parsed)')" "$ARROW_PATH"
  exit 1
fi

echo "Arrow data saved to: $ARROW_PATH"

# Convert to CSV if pyarrow is available
if command -v python3 >/dev/null && python3 -c "import pyarrow, pandas" 2>/dev/null; then
  python3 << EOF
import pyarrow as pa
import pandas as pd

table = pa.ipc.open_stream(open("${QUERY_NAME}_results.arrow", "rb")).read_all()
df = table.to_pandas()
df.to_csv("${QUERY_NAME}_results.csv", index=False)

print(f"Converted {len(df)} rows to: ${QUERY_NAME}_results.csv")
print(f"Columns: {list(df.columns)}")
EOF
else
  echo "Note: Install pyarrow+pandas for automatic CSV conversion: pip install pyarrow pandas"
fi
```

## PowerShell — Query Execution and Arrow Conversion

Execute a query and convert Apache Arrow results to CSV:

```powershell
param(
    [Parameter(Mandatory)]
    [string]$WorkspaceId,
    
    [Parameter(Mandatory)]
    [string]$DataflowId,
    
    [Parameter(Mandatory)]
    [string]$QueryName,
    
    [string]$CustomMashup = ""
)

$API = "https://api.fabric.microsoft.com/v1"
$AZ = "az rest --resource https://api.fabric.microsoft.com"

Write-Host "Executing query: $QueryName from dataflow: $DataflowId"

# Build request body — omit customMashupDocument for persisted queries
if ($CustomMashup) {
    $body = @{
        QueryName = $QueryName
        customMashupDocument = $CustomMashup
    } | ConvertTo-Json -Compress
} else {
    $body = @{
        QueryName = $QueryName
    } | ConvertTo-Json -Compress
}

$bodyFile = [IO.Path]::GetTempFileName()
[IO.File]::WriteAllText($bodyFile, $body, [Text.UTF8Encoding]::new($false))

$arrowPath = "${QueryName}_results.arrow"

# Execute the query — raw Apache Arrow IPC stream is captured via --output-file (NOT a JSON envelope).
try {
    az rest --method post `
      --resource "https://api.fabric.microsoft.com" `
      --url "$API/workspaces/$WorkspaceId/dataflows/$DataflowId/executeQuery" `
      --body "@$bodyFile" `
      --output-file $arrowPath
} catch {
    Write-Error "Failed to execute query: $_"
    exit 1
} finally {
    Remove-Item $bodyFile -ErrorAction SilentlyContinue
}

if (-not (Test-Path $arrowPath) -or (Get-Item $arrowPath).Length -eq 0) {
    Write-Error "Empty response from executeQuery"
    exit 1
}

# Detect embedded source errors — executeQuery returns HTTP 200 even on Kusto/SQL failures;
# the error JSON sits inside the stream's PQ Arrow Metadata block.
$arrowText = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($arrowPath))
$embeddedErr = [Regex]::Match($arrowText, '\{"Error":"[^"]+"\}').Value
if ($embeddedErr) {
    Write-Error "Query execution failed (embedded in Arrow body): $embeddedErr"
    exit 1
}

Write-Host "Arrow data saved to: $arrowPath"

# Convert to CSV if pyarrow is available
$pythonScript = @"
import pyarrow as pa
import pandas as pd
import sys

try:
    table = pa.ipc.open_stream(open('$arrowPath', 'rb')).read_all()
    df = table.to_pandas()
    df.to_csv('${QueryName}_results.csv', index=False)
    print(f'Converted {len(df)} rows to: ${QueryName}_results.csv')
    print(f'Columns: {list(df.columns)}')
except Exception as e:
    print(f'Conversion failed: {e}', file=sys.stderr)
    sys.exit(1)
"@

$pythonScript | python3
# Native commands don't throw on non-zero exit — guard on $LASTEXITCODE so a missing
# pyarrow/pandas (ModuleNotFoundError) or absent python3 surfaces the install hint
# instead of silently leaving a half-finished conversion.
if ($LASTEXITCODE -ne 0) {
    Write-Host "Note: Install pyarrow+pandas for automatic CSV conversion: pip install pyarrow pandas"
}
```

## Batch Query Execution with Error Handling

Execute multiple queries and collect results:

```bash
#!/bin/bash

# Configuration
WORKSPACE_ID="${1:?Usage: $0 <workspace_id> <dataflow_id>}"
DATAFLOW_ID="${2:?Usage: $0 <workspace_id> <dataflow_id>}"
QUERIES=("SalesData" "CustomerList" "ProductCatalog")

API="https://api.fabric.microsoft.com/v1"
AZ="az rest --resource https://api.fabric.microsoft.com"

mkdir -p query_results
FAILED_QUERIES=()

for QUERY in "${QUERIES[@]}"; do
    echo "Processing: $QUERY"

    ARROW_PATH="query_results/${QUERY}.arrow"
    $AZ --method post \
      --url "$API/workspaces/$WORKSPACE_ID/dataflows/$DATAFLOW_ID/executeQuery" \
      --body "{\"QueryName\": \"$QUERY\"}" \
      --output-file "$ARROW_PATH" 2>/dev/null

    # executeQuery returns HTTP 200 even on source-layer failures; the error JSON is embedded
    # inside the Arrow stream's PQ Arrow Metadata block. Treat absence of "Error":" as success.
    if [ -s "$ARROW_PATH" ] && ! grep -q '"Error":"' "$ARROW_PATH"; then
        echo "  ✓ Saved to $ARROW_PATH"
    else
        echo "  ✗ Failed"
        FAILED_QUERIES+=("$QUERY")
    fi
done

echo ""
echo "Summary: $((${#QUERIES[@]} - ${#FAILED_QUERIES[@]}))/${#QUERIES[@]} queries succeeded"

if [ ${#FAILED_QUERIES[@]} -gt 0 ]; then
    echo "Failed queries: ${FAILED_QUERIES[*]}"
    exit 1
fi
```

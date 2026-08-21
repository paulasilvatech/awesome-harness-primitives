# Eventhouse Authoring Script Templates

Reusable Bash and PowerShell templates for common Eventhouse authoring operations via `az rest`.

---

## Bash Templates

### Create Table and Ingest from Blob

```bash
#!/bin/bash
set -euo pipefail

CLUSTER_URI="${1:?Usage: $0 <cluster_uri> <database>}"
DB="${2:?Usage: $0 <cluster_uri> <database>}"

run_mgmt() {
  cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":"$1"}
EOF
  az rest --method POST \
    --url "${CLUSTER_URI}/v1/rest/mgmt" \
    --resource "https://kusto.kusto.windows.net" \
    --headers "Content-Type=application/json" \
    --body @/tmp/kql_body.json \
    | jq '.Tables[0].Rows'
}

echo "=== Creating table ==="
run_mgmt ".create-merge table Events (Timestamp: datetime, EventType: string, UserId: string, Properties: dynamic, Duration: real)"

echo "=== Creating CSV mapping ==="
run_mgmt ".create-or-alter table Events ingestion csv mapping 'EventsCsvMapping' '[{\"column\":\"Timestamp\",\"datatype\":\"datetime\",\"ordinal\":0},{\"column\":\"EventType\",\"datatype\":\"string\",\"ordinal\":1},{\"column\":\"UserId\",\"datatype\":\"string\",\"ordinal\":2},{\"column\":\"Properties\",\"datatype\":\"dynamic\",\"ordinal\":3},{\"column\":\"Duration\",\"datatype\":\"real\",\"ordinal\":4}]'"

echo "=== Ingesting data ==="
BLOB_URI="${3:-}"
if [ -n "${BLOB_URI}" ]; then
    run_mgmt ".ingest into table Events (h'${BLOB_URI};impersonate') with (format='csv', ingestionMappingReference='EventsCsvMapping', ignoreFirstRecord=true)"
    echo "Ingestion command submitted."
else
    echo "No blob URI provided — skipping ingestion."
fi

echo "=== Verifying ==="
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":"Events | count"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'
echo "Done."
```

---

### Schema Deployment (Idempotent)

```bash
#!/bin/bash
set -euo pipefail

CLUSTER_URI="${1:?Usage: $0 <cluster_uri> <database> <schema_file>}"
DB="${2:?}"
SCHEMA_FILE="${3:?}"

echo "=== Deploying schema from ${SCHEMA_FILE} ==="
while IFS= read -r cmd; do
  [[ "$cmd" =~ ^// ]] && continue   # skip comment lines
  [[ -z "$cmd" ]] && continue        # skip blank lines
  cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":"${cmd}"}
EOF
  az rest --method POST \
    --url "${CLUSTER_URI}/v1/rest/mgmt" \
    --resource "https://kusto.kusto.windows.net" \
    --headers "Content-Type=application/json" \
    --body @/tmp/kql_body.json \
    | jq '.Tables[0].Rows'
done < "${SCHEMA_FILE}"

echo "=== Verifying deployment ==="
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show tables details | project TableName, TotalRowCount"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'

cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show functions | project Name, Folder"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'

cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show materialized-views | project Name, IsEnabled, IsHealthy"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'

echo "Schema deployment complete."
```

---

### Export Schema to File

```bash
#!/bin/bash
set -euo pipefail

CLUSTER_URI="${1:?Usage: $0 <cluster_uri> <database> [output_file]}"
DB="${2:?}"
OUTPUT="${3:-schema_export_$(date +%Y%m%d).kql}"

echo "=== Exporting schema for ${DB} ==="
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show database ${DB} schema as csl script"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/mgmt" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq -r '.Tables[0].Rows[][0]' > "${OUTPUT}"
echo "Schema exported to ${OUTPUT}"
```

---

### Set Retention and Caching Policies

```bash
#!/bin/bash
set -euo pipefail

CLUSTER_URI="${1:?Usage: $0 <cluster_uri> <database> <table> <retention_days> <cache_days>}"
DB="${2:?}"
TABLE="${3:?}"
RETENTION_DAYS="${4:?}"
CACHE_DAYS="${5:?}"

run_mgmt() {
  cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":"$1"}
EOF
  az rest --method POST \
    --url "${CLUSTER_URI}/v1/rest/mgmt" \
    --resource "https://kusto.kusto.windows.net" \
    --headers "Content-Type=application/json" \
    --body @/tmp/kql_body.json \
    | jq '.Tables[0].Rows'
}

echo "=== Setting retention to ${RETENTION_DAYS}d for ${TABLE} ==="
run_mgmt ".alter table ${TABLE} policy retention '{\"SoftDeletePeriod\":\"${RETENTION_DAYS}.00:00:00\",\"Recoverability\":\"Enabled\"}'"

echo "=== Setting hot cache to ${CACHE_DAYS}d for ${TABLE} ==="
run_mgmt ".alter table ${TABLE} policy caching hot = ${CACHE_DAYS}d"

echo "=== Verifying ==="
cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show table ${TABLE} policy retention"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'

cat > /tmp/kql_body.json << EOF
{"db":"${DB}","csl":".show table ${TABLE} policy caching"}
EOF
az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'

echo "Done."
```

---

## PowerShell Templates

### Create Table and Ingest

```powershell
param(
    [Parameter(Mandatory)][string]$ClusterUri,
    [Parameter(Mandatory)][string]$Database,
    [string]$BlobUri
)

function Invoke-KustoMgmt {
    param([string]$Command)
    @{ db = $Database; csl = $Command } | ConvertTo-Json -Compress | Out-File $env:TEMP\kql_body.json -Encoding utf8NoBOM
    az rest --method POST `
      --url "$ClusterUri/v1/rest/mgmt" `
      --resource "https://kusto.kusto.windows.net" `
      --headers "Content-Type=application/json" `
      --body "@$env:TEMP\kql_body.json" 2>$null | ConvertFrom-Json | ForEach-Object { $_.Tables[0].Rows }
}

Write-Host "=== Creating table ===" -ForegroundColor Cyan
Invoke-KustoMgmt ".create-merge table Events (Timestamp: datetime, EventType: string, UserId: string, Properties: dynamic, Duration: real)"

Write-Host "=== Creating CSV mapping ===" -ForegroundColor Cyan
Invoke-KustoMgmt ".create-or-alter table Events ingestion csv mapping 'EventsCsvMapping' '[{`"column`":`"Timestamp`",`"datatype`":`"datetime`",`"ordinal`":0},{`"column`":`"EventType`",`"datatype`":`"string`",`"ordinal`":1},{`"column`":`"UserId`",`"datatype`":`"string`",`"ordinal`":2},{`"column`":`"Properties`",`"datatype`":`"dynamic`",`"ordinal`":3},{`"column`":`"Duration`",`"datatype`":`"real`",`"ordinal`":4}]'"

if ($BlobUri) {
    Write-Host "=== Ingesting from $BlobUri ===" -ForegroundColor Cyan
    Invoke-KustoMgmt ".ingest into table Events (h'${BlobUri};impersonate') with (format='csv', ingestionMappingReference='EventsCsvMapping', ignoreFirstRecord=true)"
}

Write-Host "=== Verifying ===" -ForegroundColor Cyan
@{ db = $Database; csl = "Events | count" } | ConvertTo-Json -Compress | Out-File $env:TEMP\kql_body.json -Encoding utf8NoBOM
az rest --method POST `
  --url "$ClusterUri/v1/rest/query" `
  --resource "https://kusto.kusto.windows.net" `
  --headers "Content-Type=application/json" `
  --body "@$env:TEMP\kql_body.json" 2>$null | ConvertFrom-Json | ForEach-Object { $_.Tables[0].Rows }
Write-Host "Done." -ForegroundColor Green
```

---

### Schema Deployment

```powershell
param(
    [Parameter(Mandatory)][string]$ClusterUri,
    [Parameter(Mandatory)][string]$Database,
    [Parameter(Mandatory)][string]$SchemaFile
)

Write-Host "=== Deploying schema from $SchemaFile ===" -ForegroundColor Cyan
Get-Content $SchemaFile | Where-Object { $_ -and $_ -notmatch '^\s*//' } | ForEach-Object {
    @{ db = $Database; csl = $_ } | ConvertTo-Json -Compress | Out-File $env:TEMP\kql_body.json -Encoding utf8NoBOM
    az rest --method POST `
      --url "$ClusterUri/v1/rest/mgmt" `
      --resource "https://kusto.kusto.windows.net" `
      --headers "Content-Type=application/json" `
      --body "@$env:TEMP\kql_body.json" 2>$null | ConvertFrom-Json | ForEach-Object { $_.Tables[0].Rows }
}

Write-Host "=== Verification ===" -ForegroundColor Cyan
foreach ($cmd in @(
    ".show tables details | project TableName, TotalRowCount",
    ".show functions | project Name, Folder",
    ".show materialized-views | project Name, IsEnabled, IsHealthy"
)) {
    @{ db = $Database; csl = $cmd } | ConvertTo-Json -Compress | Out-File $env:TEMP\kql_body.json -Encoding utf8NoBOM
    az rest --method POST `
      --url "$ClusterUri/v1/rest/query" `
      --resource "https://kusto.kusto.windows.net" `
      --headers "Content-Type=application/json" `
      --body "@$env:TEMP\kql_body.json" 2>$null | ConvertFrom-Json | ForEach-Object { $_.Tables[0].Rows }
}

Write-Host "Schema deployment complete." -ForegroundColor Green
```

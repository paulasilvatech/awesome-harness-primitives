# Dataflow Save-As (Gen2.1 Copy) — CLI Quick Reference

One-liner `az rest` patterns for scanning, assessment, and save-as operations.

---

## Authentication Setup

```bash
# Set API audiences
RESOURCE_FABRIC="https://api.fabric.microsoft.com"
RESOURCE_PBI="https://analysis.windows.net/powerbi/api"
API_FABRIC="https://api.fabric.microsoft.com/v1"
API_PBI="https://api.powerbi.com/v1.0/myorg"
```

---

## Workspace Discovery

```bash
# List all workspaces — resolve ID by name
az rest --method get --resource "$RESOURCE_FABRIC" \
  --url "$API_FABRIC/workspaces" \
  --query "value[?displayName=='MyWorkspace'].id" -o tsv

# List all workspaces (Admin API — tenant-wide, requires admin role)
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/admin/groups?\$top=5000" -o json
```

---

## Gen1 Dataflow Detection

The Power BI REST API returns a `generation` property (`1` or `2`) on each dataflow. This is the **preferred** detection method.

### Per-Workspace Detection (Non-Admin)

```bash
WS_ID="<workspaceId>"

# List all dataflows — use `generation` property to distinguish Gen1 from Gen2
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows" \
  --query "value[].{id:objectId, name:name, generation:generation, modelUrl:modelUrl}" -o json

# Filter Gen1 only
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows" \
  --query "value[?generation==\`1\`].{id:objectId, name:name, modelUrl:modelUrl}" -o json

# Filter Gen2 only
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows" \
  --query "value[?generation==\`2\`].{id:objectId, name:name}" -o json
```

### Tenant-Wide Detection (Admin)

```bash
# All dataflows in tenant — Admin API may not expose `generation`; use modelUrl as fallback
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/admin/dataflows" \
  --query "value[?modelUrl!=null].{id:objectId, name:name, ws:workspaceId, owner:configuredBy, storage:modelUrl}" \
  -o json

# Paginate large tenants
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/admin/dataflows?\$top=200&\$skip=0" -o json
```

---

## Risk Signal Detection

### Data Sources (per dataflow)

```bash
DF_ID="<dataflowId>"

# Get data sources for a dataflow
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows/$DF_ID/datasources" -o json
```

### Upstream Dataflow Dependencies

```bash
# Check for linked/computed entities (upstream dataflows)
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows/$DF_ID/upstreamDataflows" -o json
```

### Dataflow Transactions (recent refresh status)

```bash
# Get recent transactions — check for incremental refresh patterns
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows/$DF_ID/transactions" -o json
```

### Dataflow Definition (full JSON export)

```bash
# Export dataflow definition — inspect for DirectQuery, incremental refresh config
az rest --method get --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows/$DF_ID" -o json > dataflow-definition.json

# Check for incremental refresh policies in the definition
cat dataflow-definition.json | jq '.entities[]? | select(.ppiConfig != null) | {name: .name, incrementalRefresh: .ppiConfig}'

# Check for DirectQuery data source types
cat dataflow-definition.json | jq '.entities[]?.partitions[]? | select(.mode == "directQuery") | {entity: .name, mode: .mode}'
```

---

## Save-As Execution

### saveAsNativeArtifact (Gen1 → Gen2.1 CI/CD)

`saveAsNativeArtifact` does not do an in-place migration. It creates an upgraded Gen2.1 copy and keeps the original Gen1 dataflow.

> **Gotcha — inline body**: Pass the request body via file (`--body @file.json`), not inline. Inline `--body '{...}'` can cause `az rest` to wrap the payload in an extra envelope, producing `"saveAsRequest is a required parameter"` errors.

> **Gotcha — Windows `az.cmd`**: Omit `-o json` from this call on Windows. The flag produces `"A value that is not valid (json) was specified for the outputFormat parameter"` when routed through `az.cmd`. Capture output without `-o json` and parse with `ConvertFrom-Json` (PowerShell) or `jq` (bash).

> **Gotcha — not idempotent**: Each call creates a new artifact. If a batch run is interrupted and retried, duplicate artifacts appear in the target workspace. Before calling, verify no Gen2 artifact with the intended name already exists, or use a unique timestamped `displayName` per run.

> **Gotcha — owner permissions**: Requires you to be the dataflow **owner** or have **Contributor/Admin** in the source workspace. Non-owners receive `DataflowUnauthorizedError`.

```bash
GEN1_ID="<gen1DataflowId>"

# Basic — same workspace, auto-generated name
echo '{}' > /tmp/save-as-body.json
az rest --method post --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows/$GEN1_ID/saveAsNativeArtifact" \
  --headers "Content-Type=application/json" \
  --body @/tmp/save-as-body.json

# Full options — custom name, target workspace, include schedule
# Use a unique displayName to avoid duplicates on retry (e.g., append a timestamp)
TS=$(date -u +%Y%m%d%H%M%S)
cat > /tmp/save-as-body.json <<EOF
{
  "displayName": "MyDataflow_Gen2CICD_${TS}",
  "description": "Saved as Gen2.1 copy from Gen1",
  "includeSchedule": true,
  "targetWorkspaceId": "<targetWorkspaceId>"
}
EOF
az rest --method post --resource "$RESOURCE_PBI" \
  --url "$API_PBI/groups/$WS_ID/dataflows/$GEN1_ID/saveAsNativeArtifact" \
  --headers "Content-Type=application/json" \
  --body @/tmp/save-as-body.json

# PowerShell — parse output without -o json (Windows az.cmd compatible)
$body = @{ displayName = "MyDataflow_Gen2CICD"; includeSchedule = $true; targetWorkspaceId = "<targetWorkspaceId>" }
$tmp = [System.IO.Path]::GetTempFileName()
$body | ConvertTo-Json | Set-Content $tmp
$response = az rest --method post --resource $RESOURCE_PBI `
  --url "$API_PBI/groups/$WS_ID/dataflows/$GEN1_ID/saveAsNativeArtifact" `
  --headers "Content-Type=application/json" `
  --body "@$tmp" | ConvertFrom-Json
$response.artifactMetadata.objectId  # new Gen2 CI/CD artifact ID

# Parse response (bash/jq)
# .artifactMetadata.objectId  — new Gen2 CI/CD artifact ID
# .artifactMetadata.provisionState — should be "Active"
# .errors[] — non-fatal warnings (FailedToCopySchedule, ConnectionsUpdateFailed, etc.)
```

---

## Post-Save-As Verification

```bash
NEW_ID="<newGen2CicdArtifactId>"

# Verify the new artifact exists in Fabric API
az rest --method get --resource "$RESOURCE_FABRIC" \
  --url "$API_FABRIC/workspaces/$WS_ID/dataflows/$NEW_ID" -o json

# Get the new artifact's definition (Gen2 CI/CD — 3-part format)
az rest --method post --resource "$RESOURCE_FABRIC" \
  --url "$API_FABRIC/workspaces/$WS_ID/dataflows/$NEW_ID/getDefinition" \
  --headers "Content-Type=application/json" -o json
```

---

## Readiness Snapshot JSON Schema

```json
{
  "$schema": "readiness-snapshot",
  "snapshotDate": "ISO-8601 datetime",
  "scanScope": "workspace | tenant",
  "scanTarget": "workspace name or 'tenant-wide'",
  "summary": {
    "total": 0,
    "safe": 0,
    "manual": 0,
    "blocked": 0
  },
  "dataflows": [
    {
      "workspaceName": "string",
      "workspaceId": "uuid",
      "dataflowName": "string",
      "dataflowId": "uuid",
      "type": "Gen1",
      "owner": "email",
      "modelUrl": "URL or null",
      "readiness": "safe | manual | blocked",
      "riskSignals": [
        {
          "signal": "string",
          "severity": "warning | blocker",
          "detail": "string"
        }
      ],
      "recommendation": "string",
      "saveAsPath": "saveAsNativeArtifact"
    }
  ]
}
```

---

## Agent Integration Notes

### GitHub Copilot CLI / VS Code
- Use `az rest` for all API calls — no extra dependencies needed.
- Pipe JSON output through `jq` for filtering and formatting.
- Store readiness snapshot to file with `> readiness-snapshot.json`.

### Claude Code / Cursor / Windsurf / Codex
- Same `az rest` patterns apply.
- For large tenant scans, implement pagination with `$top` and `$skip`.
- The Admin API is rate-limited to 200 req/hour — batch assessment calls.

### PowerShell Alternative

```powershell
# Fabric API — list workspaces
$headers = @{ Authorization = "Bearer $(az account get-access-token --resource 'https://api.fabric.microsoft.com' --query accessToken -o tsv)" }
$workspaces = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces" -Headers $headers

# Power BI API — list dataflows
$pbiHeaders = @{ Authorization = "Bearer $(az account get-access-token --resource 'https://analysis.windows.net/powerbi/api' --query accessToken -o tsv)" }
$dataflows = Invoke-RestMethod -Uri "https://api.powerbi.com/v1.0/myorg/groups/$wsId/dataflows" -Headers $pbiHeaders
```

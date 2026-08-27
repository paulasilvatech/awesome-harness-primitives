# Risk Assessment Guide — Dataflow Save-As (Gen2.1 Copy)

Detailed detection logic, API calls, and classification criteria for each of the seven risk signals evaluated during Phase 1 (Readiness Assessment).

This guide assumes `saveAsNativeArtifact` behavior: no in-place migration is available; save-as creates an upgraded Gen2.1 copy while preserving the original Gen1 dataflow.

---

## Risk Signal Overview

| # | Signal | Severity | Detection API | Key Indicator |
|---|---|---|---|---|
| 1 | Incremental refresh | ⚠️ Warning | Power BI Dataflows — Get Dataflow | `entities[].ppiConfig` present |
| 2 | BYOSA / Custom ADLS Gen2 storage | ❌ Blocker | Power BI Dataflows — Get Dataflows / Admin API | `modelUrl` → customer `dfs.core.windows.net` |
| 3 | Power Automate / API triggers | ⚠️ Warning | Manual / Power Automate inventory | External refresh triggers referencing Gen1 ID |
| 4 | Downstream pipeline dependencies | ⚠️ Warning | Fabric Pipelines API | Pipeline activities referencing dataflow ID |
| 5 | Linked / computed entities | ⚠️/❌ | Power BI Dataflows — Get Upstream Dataflows | `upstreamDataflows[]` non-empty |
| 6 | DirectQuery connections | ❌ Blocker | Power BI Dataflows — Get Dataflow (definition) | `entities[].partitions[].mode == "directQuery"` |
| 7 | Caller is not owner / insufficient role | ❌ Blocker | Power BI Dataflows — List Dataflows (`configuredBy`) + workspace role check | `configuredBy` differs from current user AND workspace role < Contributor |

---

## Signal 1: Incremental Refresh (PPI)

### What It Is
Gen1 dataflows can be configured with incremental refresh policies (PPI — Power Platform Incremental). This policy defines how much historical data to retain and how to refresh incrementally. The PPI configuration may need reconfiguration or verification after save-as to ensure it works the same way in Gen2 CI/CD format.

> **Note**: Schedule copying (disabled state) is universal to all save-as operations via the `includeSchedule` parameter — this is not specific to PPI. The risk signal here is about the PPI policy configuration itself, not the schedule state.

### Detection

```bash
WS_ID="<workspaceId>"
DF_ID="<gen1DataflowId>"

# Export the full definition and check for PPI config
DEFINITION=$(az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows/$DF_ID" -o json)

# Check for incremental refresh policies (ppiConfig)
echo "$DEFINITION" | jq '[.entities[]? | select(.ppiConfig != null) | 
  {entity: .name, incrementalRefreshPolicy: .ppiConfig}]'
```

### Classification
- **Empty result** → No incremental refresh policy → safe from this signal
- **Entities with `ppiConfig`** → ⚠️ Warning: PPI configuration detected; verify policy behavior and performance after save-as

### Remediation
1. After save-as, verify the new Gen2 CI/CD dataflow's incremental refresh policy is working as expected
2. Test a refresh cycle to confirm the incremental window (retention + new data) is correct
3. Adjust retention periods or incremental logic if needed for Gen2 format

---

## Signal 2: BYOSA / Custom ADLS Gen2 Storage

### What It Is
Gen1 dataflows can use Bring Your Own Storage Account (BYOSA) — data is stored in the customer's ADLS Gen2 account instead of Power BI-managed storage. Gen2 CI/CD dataflows use Fabric-managed storage exclusively.

### Detection

```bash
# From List Dataflows response — check modelUrl
az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows" \
  --query "value[].{id:objectId, name:name, modelUrl:modelUrl}" -o json

# BYOSA indicator: modelUrl points to a customer storage account
# Pattern: https://<customAccount>.dfs.core.windows.net/powerbi/...
# Non-BYOSA: modelUrl is null, empty, or points to Power BI-managed storage
```

```bash
# Using Admin API — tenant-wide BYOSA detection
az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/admin/dataflows" \
  --query "value[?modelUrl!=null].{id:objectId, name:name, ws:workspaceId, storage:modelUrl}" -o json
```

### Classification
- **`modelUrl` is null or Power BI-managed** → No BYOSA → safe from this signal
- **`modelUrl` points to `<customer>.dfs.core.windows.net`** → ❌ Blocker: data lives in external storage; save-as will not move data

### Remediation
1. Evaluate whether the BYOSA data can be moved to Fabric-managed storage
2. If data must stay in customer storage, save-as cannot proceed — keep as Gen1 or redesign the dataflow
3. Consider creating a new Gen2 dataflow from scratch that reads from the same ADLS source

---

## Signal 3: Power Automate / API Triggers

### What It Is
External systems (Power Automate flows, custom APIs, Logic Apps) may trigger refreshes on the Gen1 dataflow using its ID. After save-as, the Gen2 CI/CD artifact has a **new ID** — all triggers must be updated.

### Detection

This signal cannot be fully detected via REST API alone. The agent should:

1. **Ask the user**: "Are there Power Automate flows or external APIs that trigger refresh on this dataflow?"
2. **Check refresh history** for API-initiated refreshes:

```bash
# Check transaction history for externally triggered refreshes
az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows/$DF_ID/transactions" \
  --query "value[?refreshType=='OnDemand' || refreshType=='ViaApi']" -o json
```

### Classification
- **No external triggers confirmed** → safe from this signal
- **External triggers exist** → ⚠️ Warning: all triggers must be updated to use the new Gen2 CI/CD artifact ID

### Remediation
1. Note the new artifact ID from the `saveAsNativeArtifact` response
2. Update all Power Automate flows to reference the new ID
3. Update any custom API integrations
4. Test each trigger against the new artifact

---

## Signal 4: Downstream Pipeline Dependencies

### What It Is
Fabric Data Factory pipelines may have dataflow activities that reference the Gen1 dataflow by ID. After save-as, pipeline activities must be re-bound to the new Gen2 CI/CD artifact.

### Detection

```bash
# List pipelines in the workspace
PIPELINES=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/dataPipelines" \
  --query "value[].{id:id, name:displayName}" -o json)

# For each pipeline, get its definition and search for the dataflow ID
# (Pipeline definitions reference dataflow activities by artifact ID)
```

> **Note**: Full pipeline definition inspection requires the `getDefinition` API on each pipeline. For large workspaces, this may be time-consuming.

### Classification
- **No pipelines reference this dataflow** → safe from this signal
- **Pipelines reference this dataflow** → ⚠️ Warning: pipeline activities must be updated to the new Gen2 CI/CD artifact ID

### Remediation
1. After save-as, update each referencing pipeline's dataflow activity to point to the new artifact ID
2. Test pipeline execution to verify the updated reference works

---

## Signal 5: Linked / Computed Entities

### What It Is
Gen1 dataflows can reference entities from other dataflows (linked entities) or compute entities based on other entities in the same or different dataflows. If the source dataflow isn't saved first, linked entities in the saved dataflow may break.

### Detection

```bash
# Check upstream dataflow dependencies
UPSTREAM=$(az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows/$DF_ID/upstreamDataflows" -o json)

echo "$UPSTREAM" | jq '.'
```

```bash
# Also check the definition for entity references
DEFINITION=$(az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows/$DF_ID" -o json)

# Look for linked entity references
echo "$DEFINITION" | jq '[.entities[]? | select(.linkedEntityRef != null) | 
  {entity: .name, linkedTo: .linkedEntityRef}]'
```

### Classification
- **No upstream dataflows and no linked entity refs** → safe from this signal
- **Upstream dataflows exist, all already Gen2** → ⚠️ Warning: verify references after save-as
- **Upstream dataflows exist, some still Gen1** → ❌ Blocker: must save upstream dataflows first

### Remediation
1. Build a dependency graph of all linked dataflows
2. Save in topological order: upstream first, then downstream
3. After each save-as, verify linked entity references still resolve

---

## Signal 6: DirectQuery Connections

### What It Is
Gen1 dataflows can use DirectQuery mode for certain data sources. Gen2 CI/CD dataflows do not support DirectQuery — they only support Import mode with optional staging (Fast Copy).

### Detection

```bash
# Export the definition and check partition modes
DEFINITION=$(az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows/$DF_ID" -o json)

# Check for DirectQuery partitions
echo "$DEFINITION" | jq '[.entities[]? | .partitions[]? | 
  select(.mode == "directQuery") | {entity: .name, mode: .mode}]'
```

### Classification
- **No DirectQuery partitions** → safe from this signal
- **DirectQuery partitions found** → ❌ Blocker: DirectQuery not supported in Gen2 CI/CD

### Remediation
1. Convert DirectQuery entities to Import mode before save-as
2. Alternatively, redesign the dataflow to use Import with scheduled refresh
3. If DirectQuery is required, the dataflow cannot be saved — keep as Gen1

---

## Composite Risk Assessment

After checking all seven signals, combine results into a final readiness classification:

| Rule | Result |
|---|---|
| Any ❌ Blocker present | ❌ **Blocked** — resolve blockers before save-as |
| Only ⚠️ Warnings present | ⚠️ **Manual followups** — can save, but remediation needed |
| No signals detected | ✅ **Safe** — save immediately |

### Assessment Script Pattern

```bash
# Initialize
READINESS="safe"
SIGNALS="[]"

# Check each signal and accumulate
# (See individual signal sections above for API calls)

# Signal 2: BYOSA check
MODEL_URL=$(echo "$PBI_DATAFLOW" | jq -r '.modelUrl // empty')
if [ -n "$MODEL_URL" ]; then
  READINESS="blocked"
  SIGNALS=$(echo "$SIGNALS" | jq '. + [{"signal":"BYOSA storage","severity":"blocker","detail":"modelUrl: '$MODEL_URL'"}]')
fi

# Signal 6: DirectQuery check
DQ_COUNT=$(echo "$DEFINITION" | jq '[.entities[]?.partitions[]? | select(.mode == "directQuery")] | length')
if [ "$DQ_COUNT" -gt 0 ]; then
  READINESS="blocked"
  SIGNALS=$(echo "$SIGNALS" | jq '. + [{"signal":"DirectQuery","severity":"blocker","detail":"'$DQ_COUNT' DirectQuery partitions found"}]')
fi

# Signal 5: Linked entities check
UPSTREAM_COUNT=$(echo "$UPSTREAM" | jq '. | length')
if [ "$UPSTREAM_COUNT" -gt 0 ]; then
  if [ "$READINESS" != "blocked" ]; then READINESS="manual"; fi
  SIGNALS=$(echo "$SIGNALS" | jq '. + [{"signal":"Linked entities","severity":"warning","detail":"'$UPSTREAM_COUNT' upstream dataflow dependencies"}]')
fi

# ... (repeat for signals 1, 3, 4)

echo "Readiness: $READINESS"
echo "Signals: $SIGNALS" | jq '.'
```

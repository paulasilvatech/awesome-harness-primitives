<!-- Mode reference for the `dataflows-cli` skill. Loaded on demand from `skills/dataflows-cli/SKILL.md` when the request matches the `upgrade` mode. -->

> **GENERATION BOUNDARY -- HARD STOP (mandatory)**
> This skill executes save-as only from Gen1 to Gen2.1. For an execution
> request whose source is Gen2, or whose source generation is not established,
> state that no public save-as or in-place upgrade endpoint is available and
> stop before API calls. This does not block a read-only readiness scan whose
> purpose is to discover and classify Gen1 candidates.
> Do not interpret "choose the closest endpoint and proceed" as approval to
> export a definition and create a copy, do not invoke the authoring skill
> automatically, and do not mutate anything. Ask the user to clarify the
> intended outcome and explicitly approve any separately documented
> alternative.

# dataflows-cli upgrade mode — Dataflow Save-As Gen1 → Gen2.1 CI/CD via CLI

A save-as companion for creating upgraded Gen2.1 copies from Power BI Gen1 dataflows using readiness assessment and guarded execution.

> We currently cannot perform an in-place migration of your dataflow. We can use save-as to create an upgraded Gen2.1 copy while preserving the original Gen1 dataflow.

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* |
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) | |
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) | |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401 |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Pagination, LRO polling, rate limits |
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection](../../../common/COMMON-CLI.md#tool-selection-rationale) | |
| Authentication Recipes | [COMMON-CLI.md § Auth Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource`** |
| Gotchas & Troubleshooting (CLI) | [COMMON-CLI.md § Gotchas](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping |
| Quick Reference | [COMMON-CLI.md § Quick Ref](../../../common/COMMON-CLI.md#quick-reference) | Token audience / tool matrix |
| Dataflow Definition Structure | [DATAFLOWS-AUTHORING-CORE.md § Definition](../../../common/DATAFLOWS-AUTHORING-CORE.md#dataflow-definition-structure) | 3-part format for Gen2 CI/CD |
| Consumption Capability Matrix | [DATAFLOWS-CONSUMPTION-CORE.md § Capabilities](../../../common/DATAFLOWS-CONSUMPTION-CORE.md#consumption-capability-matrix) | Read-only discovery patterns |
| Upgrade CLI Quick Reference | [upgrade-cli-quickref.md](upgrade/upgrade-cli-quickref.md) | All `az rest` one-liners for scanning & save-as |
| Risk Assessment Guide | [risk-assessment-guide.md](upgrade/risk-assessment-guide.md) | Risk signal detection logic & API calls |

---

## Tool Stack

| Tool | Role | Install |
|---|---|---|
| `az` CLI | **Primary**: Auth (`az login`), REST API calls (`az rest`) against both Fabric and Power BI APIs. | Pre-installed in most dev environments |
| `jq` | Parse and filter JSON responses (dataflow lists, risk signal extraction). | Pre-installed or trivial |
| `base64` | Decode dataflow definitions for inspection. | Built into bash / `[Convert]::ToBase64String()` in PowerShell |

> **Agent check** — verify before first operation:
> ```bash
> az --version 2>/dev/null || echo "INSTALL: https://aka.ms/install-azure-cli"
> jq --version 2>/dev/null || echo "INSTALL: apt-get install jq OR brew install jq"
> ```

---

## Authentication & API Audiences

This skill uses **two distinct API audiences**. Using the wrong audience returns 401.

| API | Audience (`--resource`) | Use For |
|---|---|---|
| **Fabric Items API** | `https://api.fabric.microsoft.com` | List Gen2 dataflows (Fabric-native), workspace discovery |
| **Power BI REST API** | `https://analysis.windows.net/powerbi/api` | Gen1 dataflow discovery, `saveAsNativeArtifact`, data sources, upstream dataflows, Admin API scanning |

```bash
# Fabric Items API — list Gen2 dataflows in a workspace
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/dataflows"

# Power BI REST API — list all dataflows (Gen1 + Gen2) in a workspace
az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows"

# Power BI Admin API — list all dataflows tenant-wide (requires admin role)
az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/admin/dataflows"
```

---

## Phase 1 — Awareness & Readiness

> **Goal**: "Should I use save-as, and what will happen when I create a Gen2.1 copy?"

### Agentic Workflow: Discover → Assess → Classify → Report

Follow this sequence for every save-as assessment:

1. **Discover** — Scan workspace(s) to inventory all dataflows, identifying Gen1 vs Gen2
2. **Assess** — For each Gen1 dataflow, check seven risk signals
3. **Classify** — Assign a readiness category: ✅ Safe / ⚠️ Manual followups / ❌ Blocked
4. **Report** — Output a Save-As Readiness Snapshot (markdown table + JSON)

### Step 1: Discover — Identify Gen1 Dataflows

The Power BI REST API returns a `generation` property (value `1` or `2`) on each dataflow. This is the **preferred** detection method — a single API call per workspace.

#### Non-Admin Path (per workspace)

```bash
WS_ID="<workspaceId>"
RESOURCE_PBI="https://analysis.windows.net/powerbi/api"

# List all dataflows — the `generation` property distinguishes Gen1 from Gen2
ALL_DATAFLOWS=$(az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows" \
  --query "value[].{id:objectId, name:name, generation:generation, modelUrl:modelUrl, configuredBy:configuredBy}" -o json)

# Filter Gen1 dataflows
echo "$ALL_DATAFLOWS" | jq '[.[] | select(.generation == 1)]'

# Filter Gen2 dataflows
echo "$ALL_DATAFLOWS" | jq '[.[] | select(.generation == 2)]'
```

> **Tip**: A `modelUrl` pointing to `dfs.core.windows.net` additionally indicates BYOSA (customer-managed storage) — a save-as blocker.

#### Admin Path (tenant-wide)

Requires **Fabric administrator** role or service principal with `Tenant.Read.All` scope. Rate limited to 200 requests/hour.

```bash
RESOURCE_PBI="https://analysis.windows.net/powerbi/api"

# List ALL dataflows in the tenant
ADMIN_DATAFLOWS=$(az rest --method get \
  --resource "$RESOURCE_PBI" \
  --url "https://api.powerbi.com/v1.0/myorg/admin/dataflows" \
  --query "value[].{id:objectId, name:name, workspaceId:workspaceId, modelUrl:modelUrl, configuredBy:configuredBy}" \
  -o json)

# Filter Gen1 dataflows — those with a modelUrl indicate CDM/Gen1 storage
# Note: Admin API may not expose the `generation` property; use modelUrl as fallback
echo "$ADMIN_DATAFLOWS" | jq '[.[] | select(.modelUrl != null and .modelUrl != "")]'
```

> **Note**: The Admin API supports `$filter`, `$top`, and `$skip` for pagination on large tenants.

### Step 2: Assess — Check Risk Signals

For each Gen1 dataflow found, evaluate seven risk signals. See [risk-assessment-guide.md](upgrade/risk-assessment-guide.md) for detailed API calls.

| # | Risk Signal | Detection Method | Impact |
|---|---|---|---|
| 1 | **Incremental refresh** | Check dataflow definition for incremental refresh policy configuration | ⚠️ Schedule migrates in disabled state; must re-enable and validate |
| 2 | **BYOSA / Custom ADLS Gen2 storage** | Check `modelUrl` — if points to customer storage account (not Power BI managed) | ❌ Data stays in old storage; Gen2 CI/CD uses Fabric-managed storage |
| 3 | **Power Automate / API triggers** | Check for external orchestration referencing the Gen1 dataflow ID | ⚠️ All integrations must update to new Gen2 artifact ID |
| 4 | **Downstream pipeline dependencies** | Check Fabric pipelines for dataflow activity references | ⚠️ Pipeline activities reference dataflow by ID; must re-bind |
| 5 | **Linked / computed entities** | Inspect dataflow definition for entity references to other dataflows | ⚠️/❌ Cross-dataflow references may break if source dataflows are not saved first |
| 6 | **DirectQuery connections** | Inspect data source types in definition | ❌ DirectQuery not supported in Gen2 CI/CD dataflows |
| 7 | **Caller is not owner / insufficient role** | Compare `configuredBy` against `az account show --query user.name -o tsv` — or attempt call and catch `DataflowUnauthorizedError` | ❌ `saveAsNativeArtifact` requires the caller to be the dataflow **owner** or have **Contributor/Admin** in the source workspace; Viewer/Member without ownership cannot execute save-as |

### Step 3: Classify — Readiness Categories

| Category | Criteria | Action |
|---|---|---|
| ✅ **Safe** | No risk signals detected | Create a Gen2.1 save-as copy with `saveAsNativeArtifact` |
| ⚠️ **Manual followups** | Risk signals 1, 3, 4, or 5 (non-blocking) | Execute save-as, then remediate flagged issues |
| ❌ **Blocked** | Risk signals 2, 6, or 7 (blocking) | Cannot execute save-as until blocker is resolved |

> **Tip — detect ownership before save-as**: The `configuredBy` field in the dataflow list response contains the owner's email. Compare it against the currently logged-in user (`az account show --query user.name -o tsv`). If they don't match and your workspace role is below Contributor, flag the dataflow as ❌ Blocked (signal 7) and escalate to the owner.

### Step 4: Report — Save-As Readiness Snapshot

#### Markdown Output (terminal)

```
## Save-As Readiness Snapshot
| Workspace | Dataflow | Type | Readiness | Risk Signals | Recommendation |
|---|---|---|---|---|---|
| Sales Analytics | SalesETL | Gen1 | ✅ Safe | None | Save as Gen2.1 copy now |
| Sales Analytics | CustomerLoad | Gen1 | ⚠️ Manual | Incremental refresh, Pipeline dep | Save as Gen2.1 copy, then re-enable schedule & update pipeline |
| Finance | FinanceDaily | Gen1 | ❌ Blocked | BYOSA storage | Resolve storage dependency first |
```

#### JSON Output (automation)

```json
{
  "snapshotDate": "2025-04-13T10:00:00Z",
  "summary": { "total": 3, "safe": 1, "manual": 1, "blocked": 1 },
  "dataflows": [
    {
      "workspaceName": "Sales Analytics",
      "workspaceId": "...",
      "dataflowName": "SalesETL",
      "dataflowId": "...",
      "type": "Gen1",
      "readiness": "safe",
      "riskSignals": [],
      "recommendation": "Save as Gen2.1 copy now",
      "saveAsPath": "saveAsNativeArtifact"
    }
  ]
}
```

> Save JSON to file: pipe to `jq '.' > readiness-snapshot.json`

---

## Execute with Guardrails

> **Goal**: Invoke save-as and capture outcomes safely.

### Gen1 → Gen2.1 CI/CD: `saveAsNativeArtifact` API

```
POST https://api.powerbi.com/v1.0/myorg/groups/{groupId}/dataflows/{gen1DataflowId}/saveAsNativeArtifact
```

This is a **Preview API**. It creates a **new Gen2.1 CI/CD artifact copy** while preserving the original Gen1 dataflow.

```bash
WS_ID="<workspaceId>"
GEN1_ID="<gen1DataflowId>"

# Write body to a temp file — az rest wraps inline --body in an envelope
# on some platforms, causing "saveAsRequest is a required parameter" errors.
cat > /tmp/save-as-body.json <<'EOF'
{
  "displayName": "MyDataflow_Gen2CICD",
  "description": "Saved as Gen2.1 copy from Gen1",
  "includeSchedule": true,
  "targetWorkspaceId": "<targetWorkspaceId>"
}
EOF

az rest --method post \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows/$GEN1_ID/saveAsNativeArtifact" \
  --headers "Content-Type=application/json" \
  --body @/tmp/save-as-body.json
```

> **Gotcha — inline body**: Passing JSON inline via `--body '{...}'` can cause `az rest` to wrap the payload in an extra envelope, resulting in `"saveAsRequest is a required parameter"` errors. Always use **file-based body** (`--body @file.json`) for this endpoint.

> **Gotcha — Windows `az.cmd`**: On Windows, omit `-o json` from `saveAsNativeArtifact` calls — the flag produces `"A value that is not valid (json) was specified for the outputFormat parameter"` when routed through `az.cmd`. Capture output without `-o json` and parse with `ConvertFrom-Json` in PowerShell, or pipe to `jq` in bash.

> **Gotcha — not idempotent (duplicate artifacts on retry)**: `saveAsNativeArtifact` creates a **new artifact every time it is called**. If a batch is interrupted and re-run, you will end up with multiple copies in the target workspace. To make retries safe: (1) check whether a Gen2 artifact with the intended name already exists before calling, or (2) include a timestamp in `displayName` and treat each run as a distinct artifact.

> **Gotcha — owner permissions**: You must be the **dataflow owner** or have **Contributor/Admin** in the source workspace to call `saveAsNativeArtifact`. If you are only a Viewer or Workspace Member who does not own the dataflow, the API returns `DataflowUnauthorizedError`. Ask the dataflow owner or a workspace admin to run the save-as operation for those dataflows.

**Request parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `displayName` | string (max 200) | No | Name for new artifact. Auto-generated with `_copy1` suffix if omitted |
| `description` | string (max 4000) | No | Description. Copied from source if omitted |
| `includeSchedule` | boolean | No | Copy refresh schedule in **disabled** state |
| `targetWorkspaceId` | string (uuid) | No | Target workspace. Same workspace if omitted |

**Response**: `200 OK` with `SaveAsNativeDataflowResponse`:
- `artifactMetadata` — full metadata of the new Gen2 CI/CD artifact (including `objectId`, `provisionState`)
- `errors[]` — non-fatal warning codes (save-as succeeds even if these occur):
  - `FailedToCopySchedule` — schedule could not be copied
  - `SetDataflowOriginFailed` — origin tracking not set
  - `ConnectionsUpdateFailed` — connection strings could not be updated to Fabric format

### Gen2 → Gen2 CI/CD: In-Place Upgrade

> **NOT YET AVAILABLE** — This API is not available in the current public surface. This skill will be updated when the endpoint is published. Do not attempt to call a non-existent endpoint.

## Post-Save-As Validation Checklist

Run these checks after save-as before any Gen1 cleanup:

- Confirm `artifactMetadata.provisionState` reaches `Active`.
- Review `errors[]` in `SaveAsNativeDataflowResponse` and create follow-up tasks for each warning.
- Confirm the new artifact exists in the target workspace and has expected name/description.
- Verify dependent orchestration (pipelines, flows, API callers) is updated to the new artifact ID.
- Only trigger refresh when the user explicitly approves.

---

## Must/Prefer/Avoid

### MUST DO

- **Always pass `--resource`** to `az rest` — use the correct audience per the API table above. Wrong audience = silent 401.
- **Always include `--headers "Content-Type=application/json"`** on POST calls to the Power BI REST API.
- **Use file-based body for `saveAsNativeArtifact`** — pass `--body @file.json` instead of inline JSON. Inline `--body '{...}'` can cause `az rest` to wrap the payload in an extra envelope, producing `"saveAsRequest is a required parameter"` errors.
- **On Windows, omit `-o json` on `saveAsNativeArtifact` calls** — use `ConvertFrom-Json` in PowerShell or pipe to `jq` instead. The `-o json` flag fails with `"A value that is not valid (json)"` error when routed through `az.cmd`.
- **Verify you are the dataflow owner or Contributor before save-as** — `saveAsNativeArtifact` returns `DataflowUnauthorizedError` for non-owners who are only Workspace Members or Viewers.
- **Check for existing Gen2 artifacts before retrying** — `saveAsNativeArtifact` is not idempotent; interrupted batch runs create duplicate copies on retry. Either verify the target name is absent before calling, or use a unique timestamped `displayName` per run.
- **Scan before save-as** — always run the readiness scan before execution.
- **Never refresh without explicit user consent** — the Gen2 CI/CD artifact schedule is created in disabled state for safety.
- **Check `errors[]` in saveAsNativeArtifact response** — save-as may succeed with non-fatal warnings.
- **Verify `provisionState` is `Active`** after save-as — poll the artifact metadata until terminal state.
- **Preserve the original Gen1 dataflow** — `saveAsNativeArtifact` leaves the Gen1 intact. Do not delete it until post-save-as validation passes.

### PREFER

- **Admin API for tenant-wide scanning** — more efficient than workspace-by-workspace for large tenants.
- **JSON output for automation** — markdown is for human review, JSON for scripting and CI/CD integration.
- **Topological save-as order** — save upstream dataflows (with linked entities) before downstream consumers.
- **Readiness-first execution** — do not skip readiness assessment before save-as.
- **`generation` property for Gen1 detection** — the Power BI REST API returns `generation: 1` or `generation: 2` on each dataflow. Use this single-API-call approach over cross-API comparison.
- **`modelUrl` check as secondary signal** — dataflows with a `modelUrl` pointing to `dfs.core.windows.net` are Gen1 using customer storage (BYOSA blocker).

### AVOID

- **Saving blocked (❌) dataflows** — resolve BYOSA storage and DirectQuery issues first.
- **Batch save-as without review** — always review the readiness snapshot before saving multiple dataflows.
- **Hardcoded workspace/dataflow IDs** — resolve dynamically via REST API.
- **Ignoring non-fatal errors** — `FailedToCopySchedule`, `ConnectionsUpdateFailed`, etc. require manual follow-up.
- **Calling the Gen2→Gen2 CI/CD in-place save-as API** — it does not exist yet. Do not fabricate endpoints.
- **Deleting Gen1 artifacts without explicit user consent** — never delete Gen1 dataflows unless the user explicitly approves deletion, even after post-save-as validation confirms data integrity.
- **Using `-o json` with `saveAsNativeArtifact` on Windows** — omit the flag; capture raw output and parse it explicitly.
- **Re-running batch save-as scripts without idempotency checks** — always verify the target artifact doesn't already exist to avoid duplicate copies in the workspace.

---

## Examples

### Example 1: Full Phase 1 — Readiness Scan for a Single Workspace

**Prompt**: "Scan my Sales workspace for Gen1 dataflows and show me a readiness snapshot"

**Agent response**:

```bash
# Step 1 — Resolve workspace ID
WS_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[?displayName=='Sales'].id" -o tsv)

# Step 2 — List all dataflows with generation property
ALL_DFS=$(az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows" -o json)

# Step 3 — Filter Gen1 dataflows by generation property
GEN1_DFS=$(echo "$ALL_DFS" | jq '[.value[] | select(.generation == 1) |
  {id: .objectId, name: .name, generation: .generation, modelUrl: .modelUrl}]')

echo "Gen1 dataflows found: $(echo $GEN1_DFS | jq length)"
echo "$GEN1_DFS" | jq '.'
```

### Example 2: Save-As a Gen1 Dataflow to Gen2.1

**Prompt**: "Migrate or upgrade the SalesETL Gen1 dataflow in my Sales workspace"

**Agent response**:

```bash
WS_ID="<workspaceId>"
GEN1_ID="<gen1DataflowId>"

# Write body to file (avoids az rest envelope wrapping)
cat > /tmp/save-as-body.json <<'EOF'
{"displayName": "SalesETL_Gen2CICD", "includeSchedule": true}
EOF

# Execute save-as
RESPONSE=$(az rest --method post \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/groups/$WS_ID/dataflows/$GEN1_ID/saveAsNativeArtifact" \
  --headers "Content-Type=application/json" \
  --body @/tmp/save-as-body.json)

# Check result
echo "$RESPONSE" | jq '{
  newId: .artifactMetadata.objectId,
  state: .artifactMetadata.provisionState,
  errors: .errors
}'
```

### Example 3: Tenant-Wide Admin Scan

**Prompt**: "Show me all Gen1 dataflows across the entire tenant"

**Agent response**:

```bash
# Requires Fabric administrator role
ALL_DFS=$(az rest --method get \
  --resource "https://analysis.windows.net/powerbi/api" \
  --url "https://api.powerbi.com/v1.0/myorg/admin/dataflows" -o json)

# Gen1 dataflows have a modelUrl
echo "$ALL_DFS" | jq '[.value[] | select(.modelUrl != null and .modelUrl != "") |
  {id: .objectId, name: .name, workspace: .workspaceId,
   owner: .configuredBy, storage: .modelUrl}]'
```

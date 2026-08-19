# Pipeline Run Diagnosis

When the user provides a **pipeline name or ID** with a **pipeline run ID** (job instance ID), auto-discover all Spark-related activities and diagnose each one.

**Trigger examples:**
- *"Diagnose pipeline ETL_Pipeline run abc-123"*
- *"My pipeline failed, run ID is abc-123"*
- *"Check all Spark jobs in pipeline run abc-123"*

## Step P1 — Resolve Pipeline & Get Run Status

```bash
# Resolve pipeline item ID (if user gave name)
pipelineId=$(az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/items?type=DataPipeline" \
  --query "value[?displayName=='<PipelineName>'].id" --output tsv)

# Get pipeline run status
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/items/$pipelineId/jobs/instances/$jobInstanceId" \
  --output json
```

Response includes: `id`, `status` (Completed/Failed/InProgress/Cancelled), `startTimeUtc`, `endTimeUtc`, `failureReason`.

## Step P2 — Query Activity Runs

Use the public `queryActivityRuns` API to get all activities within the pipeline run. This returns activity details including Spark session IDs, notebook item IDs, parameters, error details, and tracebacks — everything needed for diagnosis.

**API endpoint** ([docs](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-rest-api)):

```
POST $FABRIC_API_URL/workspaces/$workspaceId/datapipelines/pipelineruns/$jobInstanceId/queryactivityruns
```

**Shell escaping**: In PowerShell, inline JSON bodies for `az rest` **must** use escaped double quotes inside double-quoted strings (`"{`\"key`\":`\"value`\"}"`) or use a `--body @file.json` approach. Single-quoted strings with inner double quotes (`'{"key":"value"}'`) work correctly in PowerShell but may fail if the shell double-processes escapes.

**PowerShell `&` in URLs**: The `&` character in URL query parameters (e.g., `?type=driver&fileName=stderr`) is interpreted as PowerShell's call operator, breaking the URL. For Spark Monitoring endpoints that require multiple query params, write the URL to a variable first or use `--url-parameters`:

```powershell
# BROKEN: PowerShell treats & as call operator
az rest --url "https://...?type=driver&fileName=stderr"

# WORKAROUND: Use a JSON body file or single-param endpoints when possible
# The Spark Monitoring jobs, advice, stagesSummary, and resourceUsage endpoints
# require NO query params — prefer these over log download endpoints.
```

```bash
# Bash — use heredoc or file
cat > /tmp/query-body.json << 'EOF'
{
  "filters": [],
  "orderBy": [{"orderBy": "ActivityRunStart", "order": "DESC"}],
  "lastUpdatedAfter": "<pipeline startTimeUtc minus 1 hour>",
  "lastUpdatedBefore": "<pipeline endTimeUtc plus 1 hour, or now if InProgress>"
}
EOF
az rest --method post --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/datapipelines/pipelineruns/$jobInstanceId/queryactivityruns" \
  --body @/tmp/query-body.json --output json
```

```powershell
# PowerShell — escape inner double quotes with backslash
az rest --method post --resource $FABRIC_RESOURCE_SCOPE `
  --url "$FABRIC_API_URL/workspaces/$workspaceId/datapipelines/pipelineruns/$jobInstanceId/queryactivityruns" `
  --body '{\"filters\":[],\"orderBy\":[{\"orderBy\":\"ActivityRunStart\",\"order\":\"DESC\"}],\"lastUpdatedAfter\":\"<startTimeUtc minus 1h>\",\"lastUpdatedBefore\":\"<endTimeUtc plus 1h>\"}' `
  --output json
```

**Response schema** — paginated `{ continuationToken, value: [...] }`:

| Field | Description |
|---|---|
| `value[].activityName` | Activity name (e.g., "Check Load") |
| `value[].activityType` | `TridentNotebook`, `SparkJob`, `Copy`, `ExecutePipeline`, etc. |
| `value[].status` | `Succeeded`, `Failed`, `Inactive`, `Cancelled` |
| `value[].iterationHash` | Unique per ForEach iteration — different hashes = loop iterations |
| `value[].retryAttempt` | Retry count (`null` if no retries) |
| `value[].input.notebookId` | Notebook item ID — **use directly** for Spark Monitoring API calls |
| `value[].input.workspaceId` | Workspace ID for the notebook (may differ for cross-workspace) |
| `value[].input.parameters` | Pipeline parameters passed to the notebook |
| `value[].output.result.sessionId` | **Livy session ID** — use directly with Spark Monitoring APIs |
| `value[].output.result.runStatus` | `Succeeded` / `Failed` |
| `value[].output.result.error` | `{ ename, evalue, traceback[] }` — full Python traceback |
| `value[].output.result.highConcurrencyModeStatus` | `null` or HC status |
| `value[].output.result.metadata.runStartTime` | Actual Spark execution start |
| `value[].output.result.metadata.runEndTime` | Actual Spark execution end |
| `value[].output.SparkMonitoringURL` | Relative URL to Fabric Spark Monitor UI |
| `value[].output.executionDuration` | Runtime in seconds |
| `value[].error` | `{ errorCode, message, failureType, target }` — pipeline-level error |
| `continuationToken` | If present, pass as query param to get next page |

> **Key insight**: The `queryActivityRuns` response provides both `input.notebookId` and `output.result.sessionId` directly — no need to decode the pipeline definition to build an activity→item map. The `input.notebookId` is the item ID needed for all Spark Monitoring API calls.

**Error API priority for pipeline runs** — richest to leanest:

| Priority | Source | Error fields | Notes |
|----------|--------|-------------|-------|
| 1 | **`queryActivityRuns`** `output.result.error` | `ename`, `evalue`, `traceback[]` (cell + line number) | Most detailed — always try first |
| 2 | **`queryActivityRuns`** `error` | `errorCode`, `message`, `failureType` (UserError/SystemError) | Pipeline-level error (e.g., timeout, dependency) |
| 3 | **Spark Advisor** (`/advice`) | `TaskError.name`, `description`, fix recommendation | Spark-infrastructure failures (OOM, skew) |
| 4 | **Driver stderr** (`/logs?type=driver&fileName=stderr`) | Raw Java/Python stack traces | When traceback is absent or points to Spark internals |
| 5 | **Job Instance** (`/jobs/instances/{id}`) | `failureReason` (high-level string) | Quick triage only — often too vague |

> **Use `queryActivityRuns` first** — it has the longest data retention and returns structured error data. Spark Monitoring APIs (Advisor, logs) have shorter TTL and may return 404 for older runs.

## Step P3 — Identify Spark Activities & Handle Edge Cases

Filter activities by type to find Notebook and Spark Job Definition activities:

| `activityType` value | Item type | Contains Spark session |
|---|---|---|
| `TridentNotebook` | Fabric Notebook | Yes |
| `SparkJob` | Spark Job Definition | Yes |
| `DataflowV2` | Dataflow Gen2 | Sometimes (if Spark engine) |
| `ExecutePipeline` | Child pipeline | Recurse (see below) |

**Skip non-Spark activities** (e.g., `Wait`, `Copy`, `SetVariable`, `ForEach`, `IfCondition`, `Until`) for diagnostic analysis.

**Edge case handling:**

| Case | Detection | Action |
|---|---|---|
| **ForEach / loop iterations** | Multiple runs with same `activityName` but different `iterationHash` | Diagnose each iteration separately; group in report by activity name + iteration |
| **Retry attempts** | `retryAttempt > 0` | Diagnose only the **latest attempt** (highest `retryAttempt` value per activity); mention earlier attempts failed |
| **Nested pipelines** | `activityType == "ExecutePipeline"` | Extract the child pipeline's `jobInstanceId` from `output` and **recurse** — re-run Steps P1–P6 on the child pipeline |
| **Cancelled downstream** | `status == "Cancelled"` and activity has no `output.result.sessionId` | Report as "Cancelled — no Spark session (likely due to upstream failure)"; do not attempt Spark diagnostics |
| **Null sessionId** | `output.result.sessionId == null` or `output` is empty | Spark never started — report the `error` field from the activity; common cause: environment setup failure or library install error |
| **Cross-workspace notebook** | `input.workspaceId` differs from pipeline's workspace | Use the notebook's `input.workspaceId` for Monitoring API calls (user must have Viewer access on that workspace) |
| **High-concurrency mode** | `output.result.highConcurrencyModeStatus` is present and not `null`/`None` | The `sessionId` maps to a **shared** Livy session serving multiple notebooks concurrently. Diagnostics (stages, executors, resource usage) reflect **all** notebooks in that session, not just this activity. Note this in the report: "HC session — metrics are aggregated across N notebooks". Consider filtering Spark jobs by time window (`activityRunStart`–`activityRunEnd`) to isolate this activity's contribution. |
| **Inactive activities** | `status == "Inactive"` | Activity was disabled in the pipeline; skip entirely. `output.state` will say "Inactive" and `output.message` confirms it was skipped. |

**Deduplication for ForEach:**
```
# Group activities by activityName
# For each group:
#   If all have same iterationHash → single run (no loop)
#   If different iterationHash values → ForEach loop
#     → Diagnose each iteration
#     → In report, show: "Activity: LoadRawData [iteration 1/5] (Failed)"
```

**Deduplication for retries:**
```
# Group activities by activityName + iterationHash
# For each group:
#   Keep only the run with max(retryAttempt)
#   Note: "Activity retried N times; analyzing final attempt"
```

## Step P4 — Extract Spark Session IDs from Activity Output

For each Notebook/SJD activity found in Step P3, the `output` and `input` fields from `queryActivityRuns` contain everything needed for Spark diagnostics:

**Key fields from `queryActivityRuns` response:**

| Field | Description | Use |
|---|---|---|
| `input.notebookId` | Notebook item ID | **Use directly** for Spark Monitoring API calls — no need to decode pipeline definition |
| `input.workspaceId` | Workspace ID for the notebook | Use for cross-workspace notebooks |
| `input.parameters` | Pipeline parameters passed to notebook | Useful context for understanding iteration-specific behavior |
| `output.result.sessionId` | Livy session UUID | **This is the `livyId`** — use directly with Spark Monitoring APIs |
| `output.result.runId` | Notebook/SJD job instance ID | Can also query via Job Scheduler API |
| `output.result.runStatus` | `Succeeded` / `Failed` | Determines which diagnostic steps to run |
| `output.result.error` | `{ ename, evalue, traceback[] }` | Full Python exception with traceback — often sufficient for diagnosis |
| `output.result.highConcurrencyModeStatus` | `null` or HC status | Detect shared session scenarios |
| `output.result.metadata.runStartTime` | ISO timestamp | Actual Spark execution start |
| `output.result.metadata.runEndTime` | ISO timestamp | Actual Spark execution end |
| `output.SparkMonitoringURL` | Relative URL to Fabric Spark Monitor | Share with user for visual inspection |
| `output.executionDuration` | Runtime in seconds | Quick duration check |
| `error.message` | Pipeline-level error message | Summary of failure (may duplicate `output.result.error`) |
| `error.failureType` | `UserError` / `SystemError` | Quick classification |

**Extract livyId and resolve Spark application:**
```bash
# From the queryActivityRuns response, for each Notebook/SJD activity:
livyId="<activity.output.result.sessionId>"
notebookId="<activity.input.notebookId>"
workspaceId="<activity.input.workspaceId>"  # may differ from pipeline workspace

# Get the Spark application ID for this session
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId" \
  --query "sparkApplicationId" --output tsv
```

> **No time correlation needed** — `output.sessionId` gives the exact Livy session.

**Handling null sessionId (Spark never started):**
```bash
# When output.result.sessionId is null, Spark never launched.
# Check output.result.error for the Python traceback:
#   output.result.error.ename   — exception class name
#   output.result.error.evalue  — exception message
#   output.result.error.traceback — full stack trace lines
# Also check the pipeline-level error:
#   error.errorCode, error.message, error.failureType
# Common causes:
#   - Library/environment setup failure
#   - Invalid Spark pool configuration
#   - Capacity exhausted (could not allocate executors)
#   - Notebook syntax error caught before submission
```

**Business logic exceptions vs Spark infra failures:**
When `error.failureType` is `UserError` and `output.result.error.traceback` shows a deliberate `raise Exception(...)` in user code, this is a **business logic failure** — Spark ran successfully but the notebook intentionally failed. Report this separately from Spark infrastructure issues. No Spark-level diagnostics are needed for these.

## Step P4b — Extract Exact Notebook Cell & Line from Traceback

The `output.result.error.traceback` array from `queryActivityRuns` is the **primary source** for identifying exactly which notebook code failed. Parse the traceback lines to extract the cell number, line number, and failing code.

**Traceback format** — each entry in `traceback[]` is a string line. Look for the pattern:
```
Cell In[<cell_number>], line <line_number>
```

**Example traceback lines:**
```
  File "Cell In[14], line 19"  
    raise Exception(f"Expected key '{key}' not found in URL: {url}")
Exception: Expected key 'cluster_id' not found in URL: https://...
```

**Parsing rules:**
1. **Cell number** — `Cell In[14]` = notebook cell #14 (1-indexed)
2. **Line number** — `line 19` = line 19 within that cell
3. **Exception class** — `output.result.error.ename` (e.g., `Exception`, `ValueError`, `KeyError`)
4. **Exception message** — `output.result.error.evalue` — the human-readable error
5. **Full stack** — walk `traceback[]` bottom-to-top to find the root cause frame

**Construct the Notebook Snapshot URL** so users can open the exact failed run in the Fabric UI:

```
https://app.powerbi.com/workloads/de-ds/sparkmonitor/{notebookId}/{livyId}?trident=1&experience=power-bi&ctid={tenantId}&tab=related
```

| Component | Source | Example |
|---|---|---|
| Host | `app.powerbi.com` (production) or `msit.powerbi.com` (MSIT) | |
| `notebookId` | `input.notebookId` from `queryActivityRuns` | `8e28e1fd-9d6c-4613-928d-0af78770954b` |
| `livyId` | `output.result.sessionId` from `queryActivityRuns` | `0ec839d8-c4d1-42c5-ab9b-8e438430affb` |
| `tenantId` | `az account show --query tenantId --output tsv` | `72f988bf-86f1-41af-91ab-2d7cd011db47` |
| `tab` | `data` (shows cell outputs) or omit for default Spark monitor view | |

**What to report for each failed activity:**
```
#### Activity: <activityName> [iteration <N>/<total>] — FAILED
- **Notebook**: <notebookId> (resolve display name via Items API)
- **Cell**: Cell In[14], line 19
- **Exception**: <ename>: <evalue>
- **Notebook Snapshot**: [Open in Fabric UI](<constructed snapshot URL>)
- **Parameters**: <key pipeline parameters for this iteration>
- **Traceback** (last 5 frames):
  <paste relevant traceback lines>
```

**For ForEach iterations** — group by unique error pattern:
- If 31/36 iterations fail with the same `ename` + same cell/line, report once with count
- Show the unique `evalue` values (or a sample) to reveal iteration-specific differences
- Example: "31/36 iterations failed at Cell In[14], line 19 with `Exception: Expected key 'cluster_id' not found`"

> **Key insight**: For user-code failures (business logic, data validation, missing keys), the traceback is the definitive diagnostic — Spark Monitoring APIs will show all jobs SUCCEEDED because the Spark engine ran fine; it was the Python code that raised an exception.

## Step P4c — Validate with Spark Monitoring Jobs API

To confirm whether the failure is in **Spark infrastructure** or **user code**, check the Spark job-level status:

```bash
# Get all Spark jobs for the session
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$sparkApplicationId/jobs" \
  --output json
```

**Classification logic:**

| Spark Jobs Status | `output.result.error` | Diagnosis |
|---|---|---|
| All SUCCEEDED | Has traceback with `Cell In[N]` | **User-code failure** — Python/notebook logic error. Report cell/line from traceback. No Spark-level diagnostics needed. |
| Some FAILED | Has traceback | **Spark infrastructure failure** — proceed with full Spark diagnostics (stages, executors, memory). The traceback may show `Py4JJavaError` wrapping a Spark exception. |
| All SUCCEEDED | No error (activity Succeeded) | **Healthy** — check performance only if slow. |
| Jobs endpoint returns 404 | Any | **Session data purged** — rely on traceback from `queryActivityRuns`. See Data TTL note below. |

> **Data TTL**: Spark Monitoring data (stages, jobs, executor logs, driver stderr) is retained on the online Spark History Server for a **limited time** after session completion. For sessions that completed hours or days ago, the monitoring endpoints may return 404. The `queryActivityRuns` traceback data has a **longer retention** but also expires (observed: data available for ~1 hour after run, then purged). Always attempt `queryActivityRuns` first — it is the most reliable data source for recent failures.

## Step P5 — Run Standard Diagnostics on Each Session

For each Spark session found (where `sessionId` is not null **and** Spark jobs show failures):
1. Apply **Step 2** (auto-route by session state) from the main workflow
2. Run **Steps 3–6** as applicable (failure analysis, performance, resource, session health)
3. Tag findings with the activity name (+ iteration index if ForEach) for the report

**Skip full Spark diagnostics** when Step P4c confirms all Spark jobs SUCCEEDED — the traceback from Step P4b is sufficient.

### Handle Nested Pipelines (ExecutePipeline activities)

For each `ExecutePipeline` activity:
```bash
# Extract child pipeline run info from activity output
childJobInstanceId="<from activity output>"

# Recurse: run the full Pipeline Run Diagnosis (Steps P1–P6) on the child pipeline
# Use the child pipeline's workspaceId and pipelineId from typeProperties
```

Report nested pipeline findings under a sub-section: "Child Pipeline: <name> (run <id>)".

## Step P6 — Pipeline-Level Report

Present a combined report showing all activities and their Spark diagnostics:

```
## Pipeline Diagnostic Summary

**Pipeline**: <pipeline name> | **Run ID**: <jobInstanceId> | **Status**: <status>
**Duration**: <startTimeUtc> → <endTimeUtc>

### Activity Overview

| # | Activity | Type | Status | Duration | Spark Issues | Notes |
|---|----------|------|--------|----------|--------------|-------|
| 1 | LoadRawData | TridentNotebook | Failed | 5m 23s | 1 HIGH, 1 MEDIUM | |
| 2 | LoadRawData [iter 2] | TridentNotebook | Succeeded | 4m 10s | 0 HIGH, 1 MEDIUM | ForEach iteration 2 |
| 3 | TransformSilver | TridentNotebook | Succeeded | 12m 45s | 0 HIGH, 2 MEDIUM | Retried 1× |
| 4 | PublishGold | SparkJob | Cancelled | — | — | Upstream failure |
| 5 | RunChildPipeline | ExecutePipeline | Failed | 8m 30s | See child report | Nested pipeline |
| 6 | SetupEnv | TridentNotebook | Failed | 0s | — | Spark never started (library error) |

### Detailed Findings

#### Activity: LoadRawData (Failed)
| # | Severity | Finding | Fix |
|---|----------|---------|-----|
| 1 | HIGH | Executor OOM in stage 4 (skewed partition) | Enable AQE skew join |
| 2 | MEDIUM | Disk spill 1.3 GB in stage 3 | Increase shuffle partitions to 400 |

#### Activity: TransformSilver (Succeeded — performance issues)
| # | Severity | Finding | Fix |
|---|----------|---------|-----|
| 1 | MEDIUM | Data skew ratio 4.1× in stage 7 | Salt the join key |
| 2 | MEDIUM | Core efficiency 28% | Reduce executor count |

#### Activity: SetupEnv (Failed — no Spark session)
**Error**: library packaging error — `pip install failed for package xyz==2.0`
**Fix**: Verify package version compatibility with Fabric runtime Python version.

#### Activity: ValidateData [31/36 iterations FAILED — user-code error]
**Notebook**: Check load_ virtualization (8e28e1fd-...)
**Cell**: Cell In[14], line 19
**Exception**: `Exception: Expected key 'cluster_id' not found in URL`
**Spark Jobs**: 13/13 SUCCEEDED — failure is in Python code, not Spark infrastructure
**Pattern**: 31 iterations fail at the same cell with the same exception class; 5 succeed
**Sample failing parameters**: `cluster_url=https://...`, `batch_key=...`
**Root Cause**: Notebook business logic expects a key in the URL that is missing for certain cluster URLs
**Fix**: Update notebook validation logic to handle URLs without the expected key, or fix upstream data

#### Child Pipeline: IngestPipeline (Failed)
[Recursive report from child pipeline diagnosis]
```

> **Prioritization**: In the report, order activities by: (1) Failed activities first, (2) Succeeded but slow, (3) Succeeded and healthy. For ForEach iterations, group by activity name and highlight which iterations failed.

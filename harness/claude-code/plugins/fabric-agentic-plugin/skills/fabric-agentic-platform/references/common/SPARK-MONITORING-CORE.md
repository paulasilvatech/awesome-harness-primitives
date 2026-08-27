# Spark Monitoring APIs

> **Scope**: GA Spark Monitoring APIs for Microsoft Fabric — retrieve Spark application metrics, logs, advisor recommendations, and resource usage via REST without requiring an active Livy session. All examples use `az rest` against the Fabric API.

---

## Overview

Fabric provides a comprehensive monitoring API suite for Spark applications. These APIs work at the **application level** — you need a `livyId` (Livy session ID) and optionally an `appId` (Spark application ID) to query them.

### API URL Pattern

All monitoring APIs follow this structure:

```
https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/{itemType}/{itemId}/livySessions/{livyId}/applications/{appId}/...
```

Where `{itemType}` is one of: `notebooks`, `sparkJobDefinitions`, `lakehouses`.

### Key Difference from Interactive Livy APIs

| Aspect | Interactive Livy API | Monitoring APIs |
|---|---|---|
| Path prefix | `livyapi/versions/2023-12-01/sessions` | `livySessions/{livyId}/applications/{appId}` |
| Requires active session | Yes | No — works on completed sessions too |
| Item types supported | Lakehouses only | Notebooks, SparkJobDefinitions, Lakehouses |
| Data available | Session state + statement output | Jobs, stages, executors, logs, metrics, advice |

---

## Workspace and Item-Level Session Listing

### List Spark Applications in a Workspace

Retrieve all Spark applications across the workspace with filtering by time range, submitter, and state.

```bash
# List all Spark applications in a workspace
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/spark/livySessions" \
  --output json
```

### List Spark Applications for a Specific Item

```bash
# For a notebook
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions" \
  --output json

# For a Spark Job Definition
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/sparkJobDefinitions/$sjdId/livySessions" \
  --output json

# For a Lakehouse
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/livySessions" \
  --output json
```

### Get Details of a Specific Livy Session

```bash
# Notebook session details (includes driverCores, executorMemory, dynamicAllocation, etc.)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId" \
  --output json
```

**Response properties** (GA additions):
- `driverCores`, `driverMemory`
- `executorCores`, `executorMemory`
- `numExecutors`
- `dynamicAllocationEnabled`, `dynamicAllocationMaxExecutors`

---

## Open-Source Spark History Server APIs

These APIs follow the same contract as [Spark open-source monitoring REST API](https://spark.apache.org/docs/latest/monitoring.html#rest-api). They provide access to jobs, stages, tasks, executors, SQL queries, and event logs.

> **Note**: The `/applications` (list all apps) and `/version` endpoints are **not** supported. Use the workspace/item-level session listing APIs instead.

### Available Endpoints

| Endpoint Suffix | Description |
|---|---|
| `/jobs` | List all jobs in the application |
| `/jobs/{jobId}` | Get details of a specific job |
| `/stages` | List all stages |
| `/stages/{stageId}` | Get stage details (tasks, metrics) |
| `/executors` | List all executors with memory/disk metrics |
| `/allexecutors` | List all executors including dead ones |
| `/sql` | List all SQL queries |
| `/sql/{sqlId}` | Get SQL query plan and metrics |
| `/logs` | Get the event log |

### Get Job Details

```bash
# List all jobs in a Spark application
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/jobs" \
  --output json

# Get a specific job
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/jobs/$jobId" \
  --output json
```

**Job response fields**: `jobId`, `name`, `status` (SUCCEEDED/FAILED/RUNNING), `stageIds`, `numTasks`, `numCompletedTasks`, `numFailedTasks`, `submissionTime`, `completionTime`.

### Get Stage Details

```bash
# List all stages
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/stages" \
  --output json

# Get a specific stage with task metrics
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/stages/$stageId" \
  --output json
```

### Get Executor Information

```bash
# List all active executors
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/executors" \
  --output json

# Include dead executors
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/allexecutors" \
  --output json
```

### Get SQL Query Details

```bash
# Get details of a specific SQL query (includes physical plan)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/sql/$sqlId?details=false" \
  --output json
```

**SQL response fields**: `id`, `status`, `description`, `planDescription`, `duration`, `successJobIds`, `failedJobIds`.

### Get Event Log

```bash
# Download Spark event log for a specific attempt
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/1/logs" \
  --output json
```

### Permissions

Requires `read` permission on the item. Delegated scopes: `Item.Read.All` or item-specific scopes (`Notebook.Read.All`, `SparkJobDefinition.Read.All`, `Lakehouse.Read.All`). Supports user, service principal, and managed identities.

---

## Driver and Executor Log APIs

Direct REST access to driver and executor logs — no active session required.

### Driver Log Metadata

```bash
# Get driver log file metadata
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=driver&meta=true&fileName=stderr" \
  --output json
```

**Response**: `containerId`, `nodeId`, and `containerLogMeta` with `fileName`, `length`, `lastModified`, `creationTime`.

### Driver Log Content

```bash
# Download driver stderr log
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=driver&fileName=stderr&isDownload=true" \
  --output json
```

**Partial download** (useful for large logs):
```bash
# Read a specific byte range from driver log
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=driver&fileName=stderr&isDownload=true&isPartial=true&offset=0&size=10240" \
  --output json
```

### Rolling Driver Logs

For long-running applications, driver logs are rotated into multiple files:

```bash
# List rolling driver log files
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=rollingdriver&meta=true&filenamePrefix=stderr" \
  --output json
```

### Executor Log Metadata

```bash
# List all executor log files
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=executor&meta=true" \
  --output json

# Filter by specific executor container
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=executor&meta=true&containerId=$containerId" \
  --output json
```

### Executor Log Content

```bash
# Read a specific executor's stderr log
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=executor&containerId=$containerId&fileName=stderr" \
  --output json
```

---

## Livy Log API

Retrieve Livy session logs (higher-level than driver/executor logs).

### Livy Log Metadata

```bash
# Get Livy log metadata
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/none/logs?type=livy&meta=true" \
  --output json
```

**Response**: `fileName` ("livy.log"), `length`, `lastModified`, `creationTime`.

> **Note**: The `appId` path segment is `none` for Livy logs — they are session-level, not application-level.

### Livy Log Content

```bash
# Get full Livy log
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/none/logs?type=livy" \
  --output json

# Partial download with byte-offset
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/none/logs?type=livy&isDownload=true&isPartial=true&offset=0&size=10240" \
  --output json
```

---

## Spark Advisor API

Automated recommendations for Spark application performance, including data skew detection, time skew detection, and task error classification.

### Get All Advice

```bash
# Get all advice for a Spark application
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/advice" \
  --output json
```

### Filter Advice by Scope

```bash
# Advice for a specific stage
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/advice?stageId=$stageId" \
  --output json

# Advice for a specific job
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/advice?jobId=$jobId" \
  --output json

# Advice for a specific statement (jobGroup)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/advice?jobGroupId=$jobGroupId" \
  --output json

# Advice filtered by stage path
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/advice/stages/$stageId" \
  --output json
```

### Advice Response Format

Each advice item contains:

| Field | Type | Description |
|---|---|---|
| `id` | long | Advice identifier |
| `name` | string | Short description of the issue |
| `description` | string | Detailed explanation with recommended fix |
| `source` | string | `"System"`, `"User"`, or `"Dependency"` |
| `level` | string | `"info"`, `"warn"`, or `"error"` |
| `stageId` | long | Affected stage (-1 if not stage-specific) |
| `jobId` | long | Affected job (-1 if not job-specific) |
| `executionId` | long | Affected SQL query (-1 if not query-specific) |
| `jobGroupId` | string | Affected statement |
| `detail` | object | Rich detail — `DataSkew`, `TimeSkew`, or `TaskError` |

### DataSkew Detail

When `detail.data` is a `DataSkew` object:

| Field | Description |
|---|---|
| `stageId` | Stage with skewed data |
| `skewedTaskPercentage` | Percentage of tasks affected |
| `maxDataRead` / `meanDataRead` | Max vs mean data read (MiB) |
| `taskDataReadSkewness` | Pearson's Second Coefficient of Skewness |

### TimeSkew Detail

When `detail.data` is a `TimeSkew` object:

| Field | Description |
|---|---|
| `stageId` | Stage with skewed task durations |
| `skewedTaskPercentage` | Percentage of tasks affected |
| `maxTaskDuration` / `meanTaskDuration` | Max vs mean duration (seconds) |
| `taskDurationSkewness` | Pearson's Second Coefficient of Skewness |

### TaskError Detail

When `detail.data` is a `TaskError` object:

| Field | Description |
|---|---|
| `name` | Error/exception name |
| `tsg` | Troubleshooting guide reference |
| `taskTypes` | Spark task types affected (e.g., `ResultTask`, `ShuffleMapTask`) |
| `executorIds` | Affected executors |
| `stageIds` | Affected stages |
| `count` | Number of failed tasks |

---

## Resource Usage API

Monitor vCore allocation and utilization across executors over time.

### Resource Usage Timeline

```bash
# Get full resource usage timeline
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/resourceUsage" \
  --output json

# Filter by time range (epoch milliseconds)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/resourceUsage?start=$startMs&end=$endMs" \
  --output json

# Filter by statement (jobGroup)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/resourceUsage?jobGroup=$jobGroupId" \
  --output json
```

**Timeline response fields**:

| Field | Description |
|---|---|
| `duration` | Total application duration (ms) |
| `idleTime` | Total idle time (ms) |
| `coreEfficiency` | Overall core utilization rate (0.0–1.0) |
| `capacityExceeded` | `true` if 10K task limit exceeded (data will be empty) |
| `data.timestamps` | Array of time points |
| `data.allocatedCores` | Total allocated cores at each time point |
| `data.runningCores` | Actively used cores at each time point |
| `data.idleCores` | Idle cores at each time point |
| `data.executors` | Per-executor core and task counts |

### Resource Usage Snapshot

Get resource usage at a specific point in time:

```bash
# Get snapshot closest to a given timestamp
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/resourceUsage/$timestampMs" \
  --output json
```

### Interpreting Resource Usage

| Metric | Healthy Range | Action if Unhealthy |
|---|---|---|
| `coreEfficiency` | > 0.5 | Low efficiency = over-provisioned or idle executors |
| `idleTime / duration` | < 0.3 | High idle ratio = reduce executor count or session timeout |
| `allocatedCores - runningCores` | Close to 0 | Large gap = executors underutilized |
| `capacityExceeded` | `false` | If `true`, reduce task count or split workload |

---

## Diagnostic Workflow Using Monitoring APIs

### Step 1: Find the Livy Session

```bash
# List recent sessions for a notebook
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions" \
  --output json
```

Extract `livyId` and `appId` from the session of interest.

### Step 2: Check Advisor Recommendations

```bash
# Get automated advice — often identifies the root cause immediately
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/advice" \
  --output json
```

### Step 3: Inspect Failed Jobs/Stages

```bash
# Find failed jobs
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/jobs" \
  --query "[?status=='FAILED']" --output json

# Get stage details for the failed job
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/stages/$stageId" \
  --output json
```

### Step 4: Pull Logs

```bash
# Driver stderr (where exceptions appear)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=driver&fileName=stderr&isDownload=true" \
  --output json

# If executor OOM suspected, check executor logs
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/logs?type=executor&meta=true" \
  --output json
```

### Step 5: Analyze Resource Utilization

```bash
# Check if executors were underutilized or over-allocated
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/notebooks/$notebookId/livySessions/$livyId/applications/$appId/resourceUsage" \
  --query "{efficiency:coreEfficiency, idleTime:idleTime, duration:duration}" --output json
```

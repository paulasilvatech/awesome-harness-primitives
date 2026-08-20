# Session Health

> **Scope**: Monitor and manage Livy session lifecycle in Microsoft Fabric — detect idle/zombie sessions, assess resource usage, and recover from session failures. All examples use `az rest` against the Fabric API.

---

## Livy Session Lifecycle

### Session States

Livy sessions in Fabric follow a defined state machine. Understanding the states and expected transition times is critical for diagnosing stuck sessions.

| State | Description | Expected Duration | Action if Stuck |
|---|---|---|---|
| `not_started` | Session created but not yet submitted | < 5 seconds | Check API response for errors |
| `starting` | Spark application launching | 10–30s (Starter Pool) / 2–5 min (custom) | Check capacity; see Starting Stuck below |
| `idle` | Ready for statements | Indefinite (until timeout) | Normal — submit statements |
| `busy` | Executing a statement | Depends on workload | Monitor statement progress |
| `shutting_down` | Graceful shutdown in progress | < 30 seconds | Wait; do not force-kill |
| `dead` | Session terminated (normal or error) | Terminal state | Create a new session |
| `killed` | Session killed externally | Terminal state | Investigate cause; create new session |
| `error` | Session failed to start or crashed | Terminal state | Read logs; fix config; create new session |
| `success` | Batch session completed | Terminal state | N/A (batch only) |

### Expected Startup Times

| Pool Type | Cold Start | Warm Start (Starter Pool) |
|---|---|---|
| Starter Pool | 10–30 seconds | 3–5 seconds |
| Custom Pool (Small) | 2–4 minutes | N/A |
| Custom Pool (Large) | 3–6 minutes | N/A |

### Starting Stuck Diagnosis

If a session stays in `starting` beyond the expected time:

```bash
# Check how long the session has been starting
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId" \
  --query "{state:state, appId:appId, log:log[-5:]}" --output json
```

| Indicator | Likely Cause | Resolution |
|---|---|---|
| No `appId` assigned after 2 min | Capacity exhausted or throttled | Check capacity usage; wait or scale up |
| `appId` assigned but still `starting` | Executor allocation slow | Check pool size; reduce executor count |
| Error in last log lines | Configuration error | Read log; fix session config |

---

## Idle and Zombie Session Detection

Sessions that remain idle consume capacity units even when unused. Zombie sessions are sessions that lost their owning process but remain allocated.

### List All Sessions with State

> **Workspace-level listing**: To list Spark applications across an entire workspace (not just one lakehouse), use the [Workspace and Item-Level Session Listing](../../../../common/SPARK-MONITORING-CORE.md#workspace-and-item-level-session-listing) API which supports filtering by time range, submitter, and application state.

```bash
# Get all sessions for a specific lakehouse
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions" \
  --query "sessions[].{id:id, name:name, state:state, appId:appId}" \
  --output table
```

### Identify Idle Sessions

```bash
# Filter for idle sessions only
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions" \
  --query "sessions[?state=='idle'].{id:id, name:name, appId:appId}" \
  --output table
```

### Clean Up Idle Sessions

Before cleaning up, verify no active work depends on these sessions:

```bash
# Delete a specific idle session
az rest --method delete --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId"
```

**Batch cleanup of all idle sessions**:
```bash
# List idle session IDs, then delete each
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions" \
  --query "sessions[?state=='idle'].id" --output tsv | while read sid; do
    echo "Deleting idle session: $sid"
    az rest --method delete --resource "$FABRIC_RESOURCE_SCOPE" \
      --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sid"
done
```

### Detect Zombie Sessions

A zombie session is one in `idle` or `busy` state but with no recent statement activity. Check the last statement timestamp:

```bash
# Get session statements to detect zombies
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId/statements" \
  --query "statements[-1:].{id:id, state:state, code:code}" --output json
```

If the session has zero statements or the last statement completed long ago, the session is likely a zombie — safe to delete.

---

## Session Resource Monitoring

### Check Session Configuration

```bash
# View memory and core allocation for a session
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId" \
  --query "{driverMemory:driverMemory, driverCores:driverCores, executorMemory:executorMemory, executorCores:executorCores, numExecutors:numExecutors}" \
  --output json
```

### Monitor Executor Usage via Livy Statement

Submit a PySpark diagnostic snippet to an idle session:

```bash
cat > /tmp/body.json << 'DIAG'
{
  "code": "import json\nsc = spark.sparkContext\nexecs = sc._jsc.sc().getExecutorMemoryStatus()\nresult = {\n    'total_executors': len(execs),\n    'driver_memory_status': str(list(execs.entrySet().iterator().next())),\n    'default_parallelism': sc.defaultParallelism,\n    'dynamic_allocation': sc.getConf().get('spark.dynamicAllocation.enabled', 'unknown')\n}\nprint(json.dumps(result, indent=2))",
  "kind": "pyspark"
}
DIAG
az rest --method post --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId/statements" \
  --body @/tmp/body.json --output json
```

### Check Active Capacity Consumption

Session resource usage contributes to capacity consumption. Use the capacity APIs to see overall utilization:

```bash
# Get capacity utilization (requires admin permissions)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/capacities" \
  --query "value[].{name:displayName, id:id, sku:sku, state:state}" \
  --output table
```

---

## Session Recovery Patterns

### When to Create a New Session vs Retry

| Session State | Recovery Action |
|---|---|
| `dead` (after timeout) | Create a new session — the old one cannot be restarted |
| `dead` (after error) | Read error from logs first, fix config, then create new session |
| `error` | Session failed to start — check capacity and config before retry |
| `killed` | Investigate who/what killed it; create new session with same config |
| `idle` (but unresponsive) | Try submitting a simple statement; if no response in 60s, kill and recreate |

### Create Replacement Session

When recreating a session, preserve the original configuration:

```bash
# Get the old session's config (if still accessible)
az rest --method get --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$oldSessionId" \
  --query "{driverMemory:driverMemory, driverCores:driverCores, executorMemory:executorMemory, executorCores:executorCores, conf:conf}" \
  --output json > /tmp/old-session-config.json

# Create new session with same config
cat > /tmp/body.json << 'EOF'
{
    "name": "recovery-session",
    "driverMemory": "56g",
    "driverCores": 8,
    "executorMemory": "56g",
    "executorCores": 8,
    "conf": {
        "spark.dynamicAllocation.enabled": "true",
        "spark.fabric.pool.name": "Starter Pool"
    }
}
EOF
az rest --method post --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions" \
  --body @/tmp/body.json --query "{id:id, state:state}" --output json
```

### Session Keep-Alive Pattern

To prevent idle timeout on long-running diagnostic sessions, submit periodic no-op statements:

```bash
# Keep-alive: run every few minutes to prevent session timeout
cat > /tmp/body.json << 'EOF'
{"code": "spark.sparkContext.applicationId", "kind": "pyspark"}
EOF
az rest --method post --resource "$FABRIC_RESOURCE_SCOPE" \
  --url "$FABRIC_API_URL/workspaces/$workspaceId/lakehouses/$lakehouseId/$LIVY_API_PATH/sessions/$sessionId/statements" \
  --body @/tmp/body.json --output json
```

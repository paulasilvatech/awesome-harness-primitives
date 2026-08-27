# Spark History Server — Local Setup Reference

> **Scope**: Start a local OSS Spark History Server to view the full Spark UI (DAG, tasks, SQL plans) for Fabric Spark applications whose event logs have been downloaded to local disk. This is the **Tier 2 offline fallback** when online Monitoring APIs are insufficient.

---

## Overview

The Spark History Server (SHS) is a standalone web UI for viewing completed Spark application event logs. It reconstructs the Spark UI from event log files, allowing post-mortem analysis of jobs, stages, tasks, SQL queries, and executor metrics.

**When to use**: Escalate from Tier 1 (online APIs) when you need the full DAG visualization, task-level detail, or SQL plan visualizations that the REST API cannot provide. See [Diagnostic Tiers](diagnostic-workflow.md#diagnostic-tiers).

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Java | 11+ (Java 17 recommended for Spark 4.x) | `JAVA_HOME` must be set or `java` on PATH |
| Apache Spark | 4.1.1 (or matching runtime) | Only the history server component needed (~500 MB) |
| Disk space | ~500 MB for Spark + event logs | Event logs vary in size (1 MB – 2 GB typical) |

---

## Key Configuration Properties

| Property | Default | Description |
|----------|---------|-------------|
| `spark.history.fs.logDirectory` | `file:///tmp/spark-events` | Directory containing event log files. Supports `file:///`, `hdfs://`, `s3a://`, etc. |
| `spark.history.fs.update.interval` | `10s` | How often the SHS scans for new/updated logs. |
| `spark.history.retainedApplications` | `50` | Max number of applications to keep in memory. |
| `spark.history.ui.port` | `18080` | HTTP port for the SHS web UI. |
| `spark.history.fs.cleaner.enabled` | `false` | Whether to periodically clean old event logs. |
| `spark.history.fs.cleaner.interval` | `1d` | How often to run the cleaner. |
| `spark.history.fs.cleaner.maxAge` | `7d` | Max age of event logs before cleaning. |

---

## Starting the History Server

### Unix/Linux/macOS
```bash
$SPARK_HOME/sbin/start-history-server.sh
```

### Windows (via spark-class)
```cmd
%SPARK_HOME%\bin\spark-class.cmd org.apache.spark.deploy.history.HistoryServer
```

### With Custom Config

Create a `spark-defaults.conf` with your settings and point to it:
```bash
export SPARK_CONF_DIR=/path/to/conf
$SPARK_HOME/sbin/start-history-server.sh
```

Example `spark-defaults.conf`:
```properties
spark.history.fs.logDirectory=file:///home/user/.spark-local/event-logs
spark.history.ui.port=18080
```

---

## Stopping the History Server

### Unix/Linux/macOS
```bash
$SPARK_HOME/sbin/stop-history-server.sh
```

### Windows
Kill the Java process by PID, or use Task Manager.

---

## Event Log Directory Format

The SHS expects event log files in the configured `logDirectory`. Each Spark application writes one event log file (or directory):
```
spark-events/
  local-1234567890123/     # directory-based log
    events_1_...           # event data
  application_1234567890123_0001   # single-file log
```

### Using Local File Paths on Windows

When using `file:///` URIs on Windows, convert backslashes to forward slashes:
```properties
# Correct
spark.history.fs.logDirectory=file:///C:/Users/me/.spark-local/event-logs/abc123

# Wrong — backslashes will cause errors
spark.history.fs.logDirectory=file:///C:\Users\me\.spark-local\event-logs\abc123
```

---

## Workflow: From Fabric Event Logs to Local SHS

### Step 1 — Copy Event Logs from Fabric

Use the [JobInsight API](jobinsight-api.md) to copy event logs to a OneLake lakehouse:
```scala
import com.microsoft.jobinsight.diagnostic.LogUtils
LogUtils.copyEventLog(workspaceId, artifactId, livyId, "sessions", targetDir, true, 1)
```

### Step 2 — Download from OneLake

Download the event log files from OneLake DFS to local disk:
```bash
# Get token for OneLake
TOKEN=$(az account get-access-token --resource https://storage.azure.com --query accessToken -o tsv)

# List files in event log directory
curl -H "Authorization: Bearer $TOKEN" \
  "https://onelake.dfs.fabric.microsoft.com/$workspaceId/$lakehouseId/Files/spark-events/$livyId?resource=filesystem&recursive=true" | jq '.paths[].name'

# Download each file
curl -H "Authorization: Bearer $TOKEN" \
  "https://onelake.dfs.fabric.microsoft.com/$workspaceId/$lakehouseId/Files/spark-events/$livyId/<filename>" \
  -o ~/.spark-local/event-logs/<filename>
```

### Step 3 — Start Local SHS

```bash
# Point SHS to the downloaded event logs
export SPARK_HOME=~/.spark-local/spark-4.1.1-bin-hadoop3
export SPARK_CONF_DIR=~/.spark-local/conf

cat > $SPARK_CONF_DIR/spark-defaults.conf << EOF
spark.history.fs.logDirectory=file:///$HOME/.spark-local/event-logs
spark.history.ui.port=18080
EOF

$SPARK_HOME/sbin/start-history-server.sh
```

### Step 4 — Open Spark UI

Navigate to `http://localhost:18080`. The application should appear in the list. Click through to:
- **Jobs** tab — overview of all Spark jobs
- **Stages** tab — detailed stage metrics, task distribution
- **Executors** tab — memory/disk/GC per executor
- **SQL** tab — SQL plan visualization with metrics
- **Environment** tab — Spark configuration snapshot

---

## Common Issues

### "No completed applications found"
- The event log directory is empty or contains no valid event logs
- Check that `spark.history.fs.logDirectory` points to the correct path
- Ensure the files are Spark event logs (not arbitrary JSON/text files)

### "Port already in use"
- Another process is using port 18080
- Change the port: `spark.history.ui.port=18081`
- Or stop the existing process

### Java Not Found
- SHS requires Java 11+ (Java 17 recommended for Spark 4.x)
- Set `JAVA_HOME` or ensure `java` is on `PATH`

### OutOfMemoryError on Large Logs
- Very large event logs (>1 GB) may require more heap memory
- Set `SPARK_DAEMON_MEMORY` before starting:
  ```bash
  export SPARK_DAEMON_MEMORY=4g
  ```

### Windows-Specific Issues
- **Long paths:** Event log paths exceeding 260 characters may fail. Use short directory names or enable Windows long path support.
- **File locking:** If files are locked by another process, SHS cannot read them. Ensure no other application has the event logs open.
- **Firewall:** Windows Firewall may block the SHS port. Allow `java.exe` through the firewall or add a port exception.

---

## Spark 4.x Changes

Spark 4.x (including 4.1.1 used by Fabric) introduces:
- Improved Structured Streaming UI in History Server
- Better support for Spark Connect session history
- Enhanced SQL/DataFrame metrics visualization
- Requires Java 17 (Java 11 minimum)

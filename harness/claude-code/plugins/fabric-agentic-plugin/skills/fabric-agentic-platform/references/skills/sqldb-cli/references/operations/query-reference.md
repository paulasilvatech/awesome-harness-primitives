# SQL Database in Fabric — Operations Query Reference

Diagnostic T-SQL queries for performance investigation, blocking analysis, Query Store inspection, and resource pressure diagnosis on SQL database in Fabric. All queries are **read-only** (the XE session creation in the blocking section creates a session on the database — see notes there).

> **Engine notes**:
> - Query Store is **always enabled** by default.
> - Auto-tuning (automatic index management) is **on by default** — check `sys.dm_db_tuning_recommendations` before manually creating indexes.
> - Optimized locking is **on by default** — reduces lock memory and eliminates lock escalation.
> - `sys.dm_db_resource_stats` is available (Engine Edition 11) — 15-second granularity, 1-hour retention.
> - Server-scoped DMVs (`sys.dm_os_ring_buffers`, `sys.dm_os_schedulers`, `sys.configurations`) are **not** available.
> - Extended Events are partially supported — use `CREATE EVENT SESSION ... ON DATABASE` (not `ON SERVER`); `ring_buffer` target is reliably available; file targets may have limitations.

The examples assume you have a reusable `$SQLCMD` shell variable for invoking `sqlcmd` against the target SQL database in Fabric.

---

## Query Store

### Top Resource-Consuming Queries — By Duration (Last Hour)

```bash
$SQLCMD -Q "
SELECT TOP 20
    qsq.query_id,
    LEFT(qst.query_sql_text, 200) AS query_text,
    CASE WHEN qsq.object_id = 0 THEN N'Ad-hoc' ELSE OBJECT_NAME(qsq.object_id) END AS object_name,
    CAST(rs.avg_duration / 1000.0 AS NUMERIC(18,1)) AS avg_duration_ms,
    CAST(rs.max_duration / 1000.0 AS NUMERIC(18,1)) AS max_duration_ms,
    CAST(rs.avg_cpu_time / 1000.0 AS NUMERIC(18,1)) AS avg_cpu_time_ms,
    rs.avg_logical_io_reads,
    rs.avg_physical_io_reads,
    SUM(rs.count_executions) AS total_executions,
    CASE
        WHEN rs.max_duration > rs.avg_duration * 5 THEN 'HIGH VARIANCE'
        ELSE 'Consistent'
    END AS performance_pattern,
    CASE
        WHEN rs.avg_cpu_time > rs.avg_duration * 0.8 THEN 'CPU BOUND'
        WHEN rs.avg_cpu_time < rs.avg_duration * 0.2 THEN 'IO/WAIT BOUND'
        ELSE 'Balanced'
    END AS bottleneck_type
FROM sys.query_store_query qsq
JOIN sys.query_store_query_text qst ON qsq.query_text_id = qst.query_text_id
JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
JOIN sys.query_store_runtime_stats rs ON qsp.plan_id = rs.plan_id
WHERE rs.last_execution_time > DATEADD(HOUR, -1, GETUTCDATE())
    AND rs.execution_type = 0
GROUP BY qsq.query_id, qst.query_sql_text, qsq.object_id,
    rs.avg_duration, rs.max_duration, rs.avg_cpu_time,
    rs.avg_logical_io_reads, rs.avg_physical_io_reads
ORDER BY rs.avg_duration DESC
" -W
```

### Top Resource-Consuming Queries — By Logical IO (Last Hour)

```bash
$SQLCMD -Q "
SELECT TOP 20
    qsq.query_id,
    LEFT(qst.query_sql_text, 200) AS query_text,
    CASE WHEN qsq.object_id = 0 THEN N'Ad-hoc' ELSE OBJECT_NAME(qsq.object_id) END AS object_name,
    rs.avg_logical_io_reads AS avg_logical_io,
    SUM(rs.count_executions) AS total_executions,
    CAST(rs.avg_cpu_time / 1000.0 AS NUMERIC(18,1)) AS avg_cpu_ms
FROM sys.query_store_query qsq
JOIN sys.query_store_query_text qst ON qsq.query_text_id = qst.query_text_id
JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
JOIN sys.query_store_runtime_stats rs ON qsp.plan_id = rs.plan_id
WHERE rs.last_execution_time > DATEADD(HOUR, -1, GETUTCDATE())
GROUP BY qsq.query_id, qst.query_sql_text, qsq.object_id,
    rs.avg_logical_io_reads, rs.avg_cpu_time
ORDER BY rs.avg_logical_io_reads DESC
" -W
```

### Top Resource-Consuming Queries — By CPU (Last 24 Hours)

```bash
$SQLCMD -Q "
SELECT TOP 20
    q.query_id, qt.query_sql_text,
    SUM(rs.avg_cpu_time * rs.count_executions) AS total_cpu,
    SUM(rs.count_executions) AS total_executions
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
JOIN sys.query_store_runtime_stats_interval rsi ON rs.runtime_stats_interval_id = rsi.runtime_stats_interval_id
WHERE rsi.start_time > DATEADD(HOUR, -24, GETUTCDATE())
GROUP BY q.query_id, qt.query_sql_text
ORDER BY total_cpu DESC
" -W
```

---

## Volatile Query Detection (Coefficient of Variation)

Identifies queries with inconsistent performance — the first diagnostic step when users report intermittent slowness. CV% > 100 indicates extreme variability.

```bash
# Adjust DATEADD minutes for lookback window (default: 60 minutes)
$SQLCMD -Q "
SELECT TOP 20
    q.query_id,
    LEFT(qt.query_sql_text, 200) AS sql_text,
    COUNT(DISTINCT p.plan_id) AS plan_count,
    COUNT(rs.runtime_stats_id) AS execution_intervals,
    CAST(MIN(rs.avg_duration / 1000.0) AS NUMERIC(18,1)) AS min_avg_dur_ms,
    CAST(MAX(rs.avg_duration / 1000.0) AS NUMERIC(18,1)) AS max_avg_dur_ms,
    CAST(AVG(rs.avg_duration / 1000.0) AS NUMERIC(18,1)) AS overall_avg_dur_ms,
    CAST(STDEV(rs.avg_duration / 1000.0) AS NUMERIC(18,1)) AS stddev_dur_ms,
    CAST(
        CASE WHEN AVG(rs.avg_duration) > 0
             THEN (STDEV(rs.avg_duration) / AVG(rs.avg_duration)) * 100
             ELSE 0
        END AS NUMERIC(18,1)
    ) AS cv_pct,
    SUM(rs.count_executions) AS total_executions,
    CAST(AVG(rs.avg_logical_io_reads) AS NUMERIC(18,1)) AS avg_logical_reads,
    CAST(AVG(rs.avg_cpu_time / 1000.0) AS NUMERIC(18,1)) AS avg_cpu_ms
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
JOIN sys.query_store_runtime_stats_interval rsi ON rs.runtime_stats_interval_id = rsi.runtime_stats_interval_id
WHERE rsi.start_time >= DATEADD(MINUTE, -60, GETUTCDATE())
    AND q.is_internal_query = 0
GROUP BY q.query_id, qt.query_sql_text
HAVING COUNT(rs.runtime_stats_id) >= 2
ORDER BY cv_pct DESC
" -W
```

### Interpreting CV%

| CV% Range | Interpretation | Likely Causes |
|-----------|---------------|---------------|
| < 50% | Moderate variability | Normal fluctuation, minor contention |
| 50–100% | High variability | Blocking, plan changes, resource pressure |
| > 100% | Extreme variability | Severe blocking, plan regression, parameter sniffing |

**Plan Count > 1**: Multiple execution plans detected — strong indicator of plan regression or parameter sniffing.

---

## Wait Category Analysis

Determines WHY queries are slow. Run after volatile query detection to identify the root cause category.

```bash
$SQLCMD -Q "
SELECT TOP 20
    q.query_id,
    LEFT(qt.query_sql_text, 200) AS sql_text,
    ws.wait_category_desc AS wait_category,
    SUM(ws.total_query_wait_time_ms) AS total_wait_ms,
    SUM(ws.total_query_wait_time_ms) * 100.0
        / NULLIF(SUM(SUM(ws.total_query_wait_time_ms)) OVER (PARTITION BY q.query_id), 0)
        AS wait_pct_of_query_total,
    COUNT(DISTINCT p.plan_id) AS plan_count
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_wait_stats ws ON p.plan_id = ws.plan_id
JOIN sys.query_store_runtime_stats_interval rsi ON ws.runtime_stats_interval_id = rsi.runtime_stats_interval_id
WHERE rsi.start_time >= DATEADD(MINUTE, -60, GETUTCDATE())
    AND q.is_internal_query = 0
GROUP BY q.query_id, qt.query_sql_text, ws.wait_category_desc
ORDER BY total_wait_ms DESC
" -W
```

### Root Cause Decision Tree

| Dominant Wait Category | Root Cause | Next Steps |
|---|---|---|
| **Lock** | Blocking — queries waiting for locks held by other sessions | Run [Live Blocking](#live-blocking) queries below |
| **CPU** | CPU contention — plan regressions, parameter sniffing, expensive queries | Check plan count > 1; consider `sp_query_store_force_plan` |
| **IO** | IO contention — missing indexes, table scans, large reads | Check missing index DMVs; review logical reads |
| **Memory** | Memory grant issues — bad cardinality estimates, sort/hash spills | Update statistics; check execution plans for warnings |
| **Network** | Network latency — large result sets | Reduce result set sizes; add pagination |

---

## Recently Regressed Queries

Compares last hour vs prior 24 hours to find queries whose performance has degraded.

```bash
$SQLCMD -Q "
;WITH Last24Hours AS (
    SELECT qsq.query_id,
        LEFT(qst.query_sql_text, 200) AS query_text,
        AVG(rs.avg_duration) AS avg_duration,
        AVG(rs.avg_logical_io_reads) AS avg_io,
        SUM(rs.count_executions) AS total_executions
    FROM sys.query_store_query qsq
    JOIN sys.query_store_query_text qst ON qsq.query_text_id = qst.query_text_id
    JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
    JOIN sys.query_store_runtime_stats rs ON qsp.plan_id = rs.plan_id
    WHERE rs.last_execution_time BETWEEN DATEADD(HOUR, -25, GETUTCDATE()) AND DATEADD(HOUR, -1, GETUTCDATE())
    GROUP BY qsq.query_id, qst.query_sql_text
),
LastHour AS (
    SELECT qsq.query_id,
        AVG(rs.avg_duration) AS avg_duration,
        AVG(rs.avg_logical_io_reads) AS avg_io,
        SUM(rs.count_executions) AS total_executions
    FROM sys.query_store_query qsq
    JOIN sys.query_store_query_text qst ON qsq.query_text_id = qst.query_text_id
    JOIN sys.query_store_plan qsp ON qsq.query_id = qsp.query_id
    JOIN sys.query_store_runtime_stats rs ON qsp.plan_id = rs.plan_id
    WHERE rs.last_execution_time > DATEADD(HOUR, -1, GETUTCDATE())
    GROUP BY qsq.query_id, qst.query_sql_text
)
SELECT TOP 20
    h.query_id, h.query_text,
    CAST(h.avg_duration / 1000.0 AS NUMERIC(18,1)) AS baseline_avg_dur_ms,
    CAST(l.avg_duration / 1000.0 AS NUMERIC(18,1)) AS recent_avg_dur_ms,
    CAST(CASE WHEN h.avg_duration = 0 THEN 0
         ELSE ((l.avg_duration - h.avg_duration) / h.avg_duration) * 100
    END AS NUMERIC(18,1)) AS duration_change_pct,
    CAST(CASE WHEN h.avg_io = 0 THEN 0
         ELSE ((l.avg_io - h.avg_io) / h.avg_io) * 100
    END AS NUMERIC(18,1)) AS io_change_pct
FROM Last24Hours h
JOIN LastHour l ON h.query_id = l.query_id
WHERE CASE WHEN h.avg_duration = 0 THEN 0
           ELSE ((l.avg_duration - h.avg_duration) / h.avg_duration) * 100 END > 10
ORDER BY duration_change_pct DESC
" -W
```

---

## Multi-Plan Queries (Plan Instability)

Identifies queries with multiple execution plans — indicates parameter sniffing or plan regression.

```bash
$SQLCMD -Q "
SELECT q.query_id,
    LEFT(qt.query_sql_text, 200) AS sql_text,
    COUNT(DISTINCT p.plan_id) AS plan_count,
    MIN(p.plan_id) AS min_plan_id,
    MAX(p.plan_id) AS max_plan_id,
    SUM(rs.count_executions) AS total_executions
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
WHERE rs.last_execution_time > DATEADD(DAY, -7, GETUTCDATE())
    AND q.is_internal_query = 0
GROUP BY q.query_id, qt.query_sql_text
HAVING COUNT(DISTINCT p.plan_id) > 1
ORDER BY plan_count DESC
" -W
```

---

## Query Store Configuration Check

```bash
$SQLCMD -Q "
SELECT actual_state_desc, desired_state_desc,
    query_capture_mode_desc, size_based_cleanup_mode_desc,
    current_storage_size_mb, max_storage_size_mb,
    stale_query_threshold_days, max_plans_per_query
FROM sys.database_query_store_options
" -W
```

---

## CPU Pressure Investigation

### Step 1: Confirm CPU Pressure

```bash
$SQLCMD -Q "
;WITH CteCPULast AS (
    SELECT
        MIN(end_time) AS window_start_utc,
        MAX(end_time) AS window_end_utc,
        AVG(avg_cpu_percent) AS avg_cpu_percent,
        MAX(avg_cpu_percent) AS max_cpu_percent,
        CASE WHEN AVG(avg_cpu_percent) >= 80 THEN 'CPU pressure likely'
             ELSE 'No strong sustained pressure in last 10m'
        END AS sustained_cpu_assessment
    FROM sys.dm_db_resource_stats
    WHERE end_time >= DATEADD(MINUTE, -10, SYSUTCDATETIME())
)
SELECT * FROM CteCPULast WHERE avg_cpu_percent > 80
" -W
```

No rows = no sustained CPU pressure. Expand the lookback or proceed to Query Store historical analysis.

### Step 2: Real-Time CPU Consumers

```bash
$SQLCMD -Q "
SELECT TOP 10
    req.session_id,
    req.status,
    req.cpu_time AS cpu_time_ms,
    req.total_elapsed_time AS elapsed_time_ms,
    (req.total_elapsed_time - req.cpu_time) AS non_cpu_time_ms,
    CAST((req.total_elapsed_time - req.cpu_time) * 1.0
        / NULLIF(req.cpu_time, 0) AS DECIMAL(10,2)) AS non_cpu_to_cpu_ratio,
    req.dop,
    req.wait_type,
    req.wait_time AS wait_time_ms
FROM sys.dm_exec_requests req
JOIN sys.dm_exec_sessions s ON req.session_id = s.session_id
WHERE req.session_id <> @@SPID
    AND s.is_user_process = 1
    AND req.cpu_time > 1000
ORDER BY req.cpu_time DESC
" -W
```

### Step 3: CPU Consumers with SQL Text

```bash
$SQLCMD -Q "
SELECT TOP 10
    req.session_id,
    req.cpu_time AS cpu_time_ms,
    req.total_elapsed_time AS elapsed_time_ms,
    req.logical_reads,
    req.dop,
    req.wait_type,
    REPLACE(REPLACE(
        SUBSTRING(st.text,
            (req.statement_start_offset / 2) + 1,
            ((CASE req.statement_end_offset WHEN -1 THEN DATALENGTH(st.text)
              ELSE req.statement_end_offset END - req.statement_start_offset) / 2) + 1),
        CHAR(10), ' '), CHAR(13), ' ') AS statement_text
FROM sys.dm_exec_requests req
JOIN sys.dm_exec_sessions s ON req.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(req.sql_handle) st
WHERE req.session_id <> @@SPID
    AND s.is_user_process = 1
    AND req.cpu_time > 1000
ORDER BY req.cpu_time DESC
" -W
```

### Step 4: CPU Usage Trend (Last Hour)

```bash
$SQLCMD -Q "
SELECT end_time,
    avg_cpu_percent,
    avg_data_io_percent,
    avg_log_write_percent,
    avg_memory_usage_percent
FROM sys.dm_db_resource_stats
WHERE end_time >= DATEADD(HOUR, -1, SYSUTCDATETIME())
ORDER BY end_time
" -W
```

---

## IO Pressure Investigation

### Step 1: Confirm IO Pressure

```bash
$SQLCMD -Q "
;WITH CteIOLast AS (
    SELECT
        MIN(end_time) AS window_start_utc,
        MAX(end_time) AS window_end_utc,
        AVG(avg_data_io_percent) AS avg_data_io_percent,
        MAX(avg_data_io_percent) AS max_data_io_percent,
        AVG(avg_log_write_percent) AS avg_log_write_percent,
        MAX(avg_log_write_percent) AS max_log_write_percent,
        CASE
            WHEN AVG(avg_data_io_percent) >= 80 THEN 'Data IO pressure likely'
            WHEN AVG(avg_log_write_percent) >= 80 THEN 'Log IO pressure likely'
            ELSE 'No strong sustained IO pressure in last 10m'
        END AS sustained_io_assessment
    FROM sys.dm_db_resource_stats
    WHERE end_time >= DATEADD(MINUTE, -10, SYSUTCDATETIME())
)
SELECT * FROM CteIOLast
" -W
```

### Step 2: Real-Time IO Consumers

```bash
$SQLCMD -Q "
SELECT TOP 10
    req.session_id,
    req.status,
    req.logical_reads,
    req.reads AS physical_reads,
    req.writes AS physical_writes,
    CAST(req.logical_reads * 1.0
        / NULLIF(DATEDIFF(SECOND, req.start_time, GETDATE()), 0)
        AS DECIMAL(18,2)) AS logical_reads_per_sec,
    req.wait_type,
    req.wait_time AS wait_time_ms,
    req.wait_resource
FROM sys.dm_exec_requests req
JOIN sys.dm_exec_sessions s ON req.session_id = s.session_id
WHERE req.session_id <> @@SPID
    AND s.is_user_process = 1
    AND req.logical_reads > 10000
ORDER BY req.logical_reads DESC
" -W
```

### Step 3: IO Consumers with SQL Text

```bash
$SQLCMD -Q "
SELECT TOP 10
    req.session_id,
    req.logical_reads,
    req.reads AS physical_reads,
    req.writes AS physical_writes,
    req.wait_type,
    REPLACE(REPLACE(
        SUBSTRING(st.text,
            (req.statement_start_offset / 2) + 1,
            ((CASE req.statement_end_offset WHEN -1 THEN DATALENGTH(st.text)
              ELSE req.statement_end_offset END - req.statement_start_offset) / 2) + 1),
        CHAR(10), ' '), CHAR(13), ' ') AS statement_text
FROM sys.dm_exec_requests req
JOIN sys.dm_exec_sessions s ON req.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(req.sql_handle) st
WHERE req.session_id <> @@SPID
    AND s.is_user_process = 1
    AND req.logical_reads > 10000
ORDER BY req.logical_reads DESC
" -W
```

---

## Missing Index Analysis

> **Always check auto-tuning recommendations first.** Auto-tuning automatically creates and drops indexes — manually creating an index that auto-tuning would create wastes effort.

### Auto-Tuning Recommendations (Check First)

```bash
$SQLCMD -Q "
SELECT name, reason, score,
    JSON_VALUE(state, '$.currentValue') AS state,
    JSON_VALUE(details, '$.indexName') AS suggested_index,
    JSON_VALUE(details, '$.schema') AS schema_name,
    JSON_VALUE(details, '$.table') AS table_name
FROM sys.dm_db_tuning_recommendations
WHERE JSON_VALUE(state, '$.currentValue') = 'Active'
ORDER BY score DESC
" -W
```

### DMV Missing Index Recommendations

```bash
$SQLCMD -Q "
SELECT TOP 20
    CONVERT(DECIMAL(18,2), migs.user_seeks * migs.avg_total_user_cost * (migs.avg_user_impact * 0.01)) AS index_advantage,
    migs.last_user_seek,
    mid.[statement] AS [table],
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    migs.user_seeks,
    migs.avg_total_user_cost
FROM sys.dm_db_missing_index_group_stats migs
JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE mid.database_id = DB_ID()
ORDER BY index_advantage DESC
" -W
```

### Missing Indexes for a Specific Table

```bash
# Replace 'dbo.Orders' with target table
$SQLCMD -Q "
SELECT TOP 10
    CONVERT(DECIMAL(18,2), migs.user_seeks * migs.avg_total_user_cost * (migs.avg_user_impact * 0.01)) AS index_advantage,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    migs.user_seeks
FROM sys.dm_db_missing_index_group_stats migs
JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE mid.database_id = DB_ID()
    AND mid.[statement] LIKE '%Orders%'
ORDER BY index_advantage DESC
" -W
```

---

## Statistics Staleness Check

Identifies statistics that may need updating based on modification percentage.

```bash
# Adjust thresholds: @min_rows (100000), @pct_threshold (10.00)
$SQLCMD -Q "
SELECT
    SCHEMA_NAME(so.schema_id) AS [schema],
    so.name AS [table],
    ss.name AS statistic_name,
    sp.last_updated,
    sp.rows AS rows_in_table,
    sp.rows_sampled,
    CAST(100 * sp.rows_sampled / sp.rows AS DECIMAL(18,2)) AS pct_sampled,
    sp.modification_counter AS row_modifications,
    CAST(100.0 * sp.modification_counter / sp.rows AS DECIMAL(18,2)) AS pct_changed
FROM sys.objects so
JOIN sys.stats ss ON so.object_id = ss.object_id
JOIN sys.schemas sch ON so.schema_id = sch.schema_id
OUTER APPLY sys.dm_db_stats_properties(so.object_id, ss.stats_id) sp
WHERE so.type IN ('U','V')
    AND sp.rows >= 100000
    AND (CAST(100.0 * sp.modification_counter / sp.rows AS DECIMAL(18,2))) >= 10.00
ORDER BY pct_changed DESC
" -W
```

---

## Resource Usage Overview

```bash
# Last 30 minutes of resource usage
$SQLCMD -Q "
SELECT end_time,
    avg_cpu_percent,
    avg_data_io_percent,
    avg_log_write_percent,
    avg_memory_usage_percent,
    max_worker_percent,
    max_session_percent
FROM sys.dm_db_resource_stats
WHERE end_time >= DATEADD(MINUTE, -30, SYSUTCDATETIME())
ORDER BY end_time
" -W
```

---

## Table Access Patterns

Identifies the most accessed tables by reads or writes.

```bash
$SQLCMD -Q "
SELECT TOP 20
    OBJECT_SCHEMA_NAME(ius.object_id) AS [schema],
    OBJECT_NAME(ius.object_id) AS [table],
    (ius.user_seeks + ius.user_scans + ius.user_lookups) AS total_reads,
    ius.user_updates AS total_writes,
    ius.last_user_seek,
    ius.last_user_scan,
    ius.last_user_update
FROM sys.dm_db_index_usage_stats ius
WHERE ius.database_id = DB_ID()
    AND OBJECTPROPERTY(ius.object_id, 'IsUserTable') = 1
ORDER BY total_reads DESC
" -W
```

---

## Live Blocking

### Blocked Sessions

```bash
$SQLCMD -Q "
SELECT
    r.session_id,
    r.blocking_session_id,
    s.program_name,
    s.host_name,
    s.login_name,
    r.status AS request_status,
    r.command,
    r.wait_type,
    r.wait_time AS wait_time_ms,
    r.wait_resource,
    DATEDIFF(SECOND, r.start_time, GETDATE()) AS elapsed_seconds,
    r.open_transaction_count,
    t.text AS sql_text
FROM sys.dm_exec_sessions s
JOIN sys.dm_exec_connections c ON s.session_id = c.session_id
JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE s.is_user_process = 1
    AND r.blocking_session_id <> 0
" -W
```

No rows = no blocking at the time of check. If blocking is intermittent, set up an XE session (below).

### Head Blocker Details

```bash
$SQLCMD -Q "
SELECT
    s.session_id,
    s.program_name,
    s.host_name,
    s.login_name,
    s.status AS session_status,
    s.cpu_time AS cpu_time_ms,
    s.memory_usage * 8 AS memory_usage_kb,
    s.last_request_start_time,
    s.last_request_end_time,
    s.open_transaction_count,
    r.command AS current_command,
    r.wait_type,
    r.status AS request_status,
    COALESCE(t.text, '-- No active request (idle with open transaction)') AS sql_text,
    blocked_counts.blocked_session_count
FROM sys.dm_exec_sessions s
JOIN sys.dm_exec_connections c ON s.session_id = c.session_id
LEFT JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(COALESCE(r.sql_handle, c.most_recent_sql_handle)) t
JOIN (
    SELECT blocking_session_id, COUNT(*) AS blocked_session_count
    FROM sys.dm_exec_requests
    WHERE blocking_session_id <> 0
    GROUP BY blocking_session_id
) blocked_counts ON s.session_id = blocked_counts.blocking_session_id
WHERE NOT EXISTS (
    SELECT 1 FROM sys.dm_exec_requests r2
    WHERE r2.session_id = s.session_id AND r2.blocking_session_id <> 0
)
" -W
```

### Blocking Chain Hierarchy

```bash
$SQLCMD -Q "
;WITH BlockingChain AS (
    SELECT r.session_id, r.blocking_session_id, 0 AS chain_level,
        CAST(CAST(r.blocking_session_id AS VARCHAR(10)) + ' -> ' + CAST(r.session_id AS VARCHAR(10)) AS VARCHAR(4000)) AS blocking_chain
    FROM sys.dm_exec_requests r
    WHERE r.blocking_session_id <> 0
        AND NOT EXISTS (
            SELECT 1 FROM sys.dm_exec_requests r2
            WHERE r2.session_id = r.blocking_session_id AND r2.blocking_session_id <> 0
        )
    UNION ALL
    SELECT r.session_id, r.blocking_session_id, bc.chain_level + 1,
        CAST(bc.blocking_chain + ' -> ' + CAST(r.session_id AS VARCHAR(10)) AS VARCHAR(4000))
    FROM sys.dm_exec_requests r
    JOIN BlockingChain bc ON r.blocking_session_id = bc.session_id
    WHERE r.blocking_session_id <> 0
)
SELECT bc.blocking_chain, bc.chain_level,
    bc.session_id AS blocked_session_id,
    bc.blocking_session_id AS blocked_by,
    s.program_name,
    r.command, r.wait_type,
    r.wait_time AS wait_time_ms,
    t.text AS sql_text
FROM BlockingChain bc
JOIN sys.dm_exec_sessions s ON bc.session_id = s.session_id
JOIN sys.dm_exec_requests r ON bc.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) t
ORDER BY bc.blocking_chain, bc.chain_level
" -W
```

---

## Blocking — Setup Extended Events Session

For intermittent blocking that cannot be caught live. Creates an Extended Events session to passively capture the blocker.

> **Caveat**: Use `ON DATABASE` (not `ON SERVER`). Only `ring_buffer` target is reliably available. The session is dropped at the end — see Clean Up XE Session.

### Create Session to Capture a Suspect Query

Write the batch to a `.sql` file and run it with `$SQLCMD -i` — piping a here-doc
directly into `sqlcmd` has portability quirks across shells and platforms.

```bash
# Replace 'SELECT%FROM dbo.Orders%' with a LIKE pattern matching the blocked query.
cat > create_xe_session.sql <<'SQL'
SET NOCOUNT ON;

-- Drop existing session if present
IF EXISTS (SELECT 1 FROM sys.dm_xe_database_sessions WHERE name = 'CaptureBlockingQuery')
    ALTER EVENT SESSION CaptureBlockingQuery ON DATABASE STATE = STOP;
IF EXISTS (SELECT 1 FROM sys.database_event_sessions WHERE name = 'CaptureBlockingQuery')
    DROP EVENT SESSION CaptureBlockingQuery ON DATABASE;

CREATE EVENT SESSION CaptureBlockingQuery ON DATABASE
ADD EVENT sqlserver.sql_statement_completed
(
    ACTION (sqlserver.sql_text, sqlserver.session_id, sqlserver.client_app_name,
            sqlserver.client_hostname, sqlserver.username)
    WHERE sqlserver.sql_text LIKE N'SELECT%FROM dbo.Orders%'
)
ADD TARGET package0.ring_buffer (SET max_memory = 4096);

ALTER EVENT SESSION CaptureBlockingQuery ON DATABASE STATE = START;
PRINT 'XE session CaptureBlockingQuery started.';
SQL

$SQLCMD -i create_xe_session.sql
```

PowerShell equivalent (write the file, then run it with `-i`):

```powershell
# Replace 'SELECT%FROM dbo.Orders%' with a LIKE pattern matching the blocked query.
@'
SET NOCOUNT ON;

-- Drop existing session if present
IF EXISTS (SELECT 1 FROM sys.dm_xe_database_sessions WHERE name = 'CaptureBlockingQuery')
    ALTER EVENT SESSION CaptureBlockingQuery ON DATABASE STATE = STOP;
IF EXISTS (SELECT 1 FROM sys.database_event_sessions WHERE name = 'CaptureBlockingQuery')
    DROP EVENT SESSION CaptureBlockingQuery ON DATABASE;

CREATE EVENT SESSION CaptureBlockingQuery ON DATABASE
ADD EVENT sqlserver.sql_statement_completed
(
    ACTION (sqlserver.sql_text, sqlserver.session_id, sqlserver.client_app_name,
            sqlserver.client_hostname, sqlserver.username)
    WHERE sqlserver.sql_text LIKE N'SELECT%FROM dbo.Orders%'
)
ADD TARGET package0.ring_buffer (SET max_memory = 4096);

ALTER EVENT SESSION CaptureBlockingQuery ON DATABASE STATE = START;
PRINT 'XE session CaptureBlockingQuery started.';
'@ | Set-Content -Path create_xe_session.sql -Encoding UTF8

& $SQLCMD -i create_xe_session.sql
```

### Read XE Session Data

```bash
$SQLCMD -Q "
SELECT
    event_data.value('(event/@timestamp)[1]', 'DATETIME2') AS event_time,
    event_data.value('(event/action[@name=\"session_id\"]/value)[1]', 'INT') AS session_id,
    event_data.value('(event/action[@name=\"username\"]/value)[1]', 'NVARCHAR(256)') AS username,
    event_data.value('(event/action[@name=\"client_app_name\"]/value)[1]', 'NVARCHAR(256)') AS app_name,
    event_data.value('(event/action[@name=\"client_hostname\"]/value)[1]', 'NVARCHAR(256)') AS hostname,
    event_data.value('(event/data[@name=\"duration\"]/value)[1]', 'BIGINT') / 1000 AS duration_ms,
    event_data.value('(event/action[@name=\"sql_text\"]/value)[1]', 'NVARCHAR(MAX)') AS sql_text
FROM (
    SELECT CAST(target_data AS XML) AS target_xml
    FROM sys.dm_xe_database_session_targets dst
    JOIN sys.dm_xe_database_sessions ds ON dst.event_session_address = ds.address
    WHERE ds.name = 'CaptureBlockingQuery'
        AND dst.target_name = 'ring_buffer'
) AS xdata
CROSS APPLY target_xml.nodes('RingBufferTarget/event') AS xevents(event_data)
ORDER BY event_time DESC
" -W
```

### Clean Up XE Session

```bash
$SQLCMD -Q "
ALTER EVENT SESSION CaptureBlockingQuery ON DATABASE STATE = STOP;
DROP EVENT SESSION CaptureBlockingQuery ON DATABASE;
PRINT 'XE session CaptureBlockingQuery dropped.';
" -W
```

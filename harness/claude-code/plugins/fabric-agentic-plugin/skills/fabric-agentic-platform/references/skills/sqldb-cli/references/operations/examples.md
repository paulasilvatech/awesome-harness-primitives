# Examples — sqldb-cli operations mode

Prompt/response patterns showing typical investigation flow.

## Diagnose Intermittent Slowness

**User:** "Some users say queries are slow sometimes — can you check?"

**Agent:** Runs [Volatile Query Detection](query-reference.md#volatile-query-detection-coefficient-of-variation):

```bash
sqlcmd -S "<endpoint>.database.fabric.microsoft.com,1433" -d "MyDB" -G -Q "
SELECT TOP 10 q.query_id, LEFT(qt.query_sql_text, 80) AS sql_text,
    COUNT(DISTINCT p.plan_id) AS plan_count,
    CAST((STDEV(rs.avg_duration) / NULLIF(AVG(rs.avg_duration), 0)) * 100 AS NUMERIC(18,1)) AS cv_pct
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
JOIN sys.query_store_runtime_stats_interval rsi ON rs.runtime_stats_interval_id = rsi.runtime_stats_interval_id
WHERE rsi.start_time >= DATEADD(MINUTE, -60, GETUTCDATE())
GROUP BY q.query_id, qt.query_sql_text
HAVING COUNT(rs.runtime_stats_id) >= 2
ORDER BY cv_pct DESC"
```

> **Top volatile queries (last hour):**
> 1. `SELECT * FROM dbo.Orders WHERE CustomerID = ?` — CV% 187, plan_count = 3 → **plan instability**
> 2. `UPDATE dbo.Inventory SET Qty = Qty - ? WHERE SKU = ?` — CV% 134, plan_count = 1 → **likely blocking**
>
> Running wait category analysis to confirm root cause...

## Diagnose Live Blocking

**User:** "Several sessions are stuck."

**Agent:** Runs [Live Blocking](query-reference.md#live-blocking) and presents:

> **Live blocking detected:**
> - Head blocker: session 64, app `MyApp.exe`, `open_transaction_count = 1`, no active request
> - Blocked sessions: 72, 89, 95 — all waiting on `LCK_M_X` for ~120 seconds
> - Head blocker last_request_end_time was 5 minutes ago — **the application is holding an uncommitted transaction**
>
> Recommendation: review client code for missing `COMMIT`/`ROLLBACK` in error paths. If you explicitly confirm that you want to terminate the blocker as a temporary mitigation, `KILL 64` is an option, but it requires sufficient permissions and will disconnect that session and roll back its in-flight transaction.

## Recommend an Index

**User:** "Should I create an index on dbo.Orders.CustomerID?"

**Agent:** Runs [Auto-Tuning Recommendations](query-reference.md#auto-tuning-recommendations-check-first), then [Missing Indexes for a Specific Table](query-reference.md#missing-indexes-for-a-specific-table):

> **Auto-tuning** has no pending recommendations for `dbo.Orders`.
>
> **DMV analysis** shows:
> - `index_advantage = 1245.30` for `(CustomerID) INCLUDE (OrderDate, Status)` — based on 8,200 user_seeks
>
> Recommendation: yes, this index is justified by workload patterns. Suggested DDL:
> ```sql
> CREATE INDEX IX_Orders_CustomerID_INC_OrderDate_Status
>     ON dbo.Orders (CustomerID) INCLUDE (OrderDate, Status);
> ```
> Note: auto-tuning may also create this in the next tuning cycle. If both happen, drop the manual one.

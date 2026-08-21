# EVENTHOUSE-CONSUMPTION-CORE.md — KQL Consumption Patterns for Fabric Eventhouse

> **Purpose**: Shared reference for Eventhouse consumption skills. Covers read-only query patterns, schema discovery, monitoring, and performance best practices for Fabric Eventhouse and KQL Databases.
> **Not a tutorial** — assumes familiarity with KQL basics. Focus is Fabric-specific behaviour and CLI-driven workflows.

---

## Connection Fundamentals

### Cluster URI

Each KQL Database in Fabric has a unique **Query URI** (cluster URI):

```
https://<cluster>.kusto.fabric.microsoft.com
```

Discover it via Fabric REST API:

```bash
# List KQL Databases in a workspace
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WS_ID}/kqlDatabases" \
  --resource "https://api.fabric.microsoft.com"
```

The response includes `queryServiceUri` (the cluster URI) and `databaseName` for each KQL Database.

> **Token audience**: `https://kusto.kusto.windows.net/.default` for all direct access methods. See [COMMON-CORE.md](./COMMON-CORE.md) for full audience table.

### Querying via `az rest`

> **Always use the temp-file pattern** — KQL queries contain `|` (pipe) characters which break
> shell escaping in both bash and PowerShell. Write the JSON body to a file and use `--body @<file>`.
> On PowerShell, use `@{db="X";csl="..."} | ConvertTo-Json -Compress | Out-File $env:TEMP\kql_body.json -Encoding utf8NoBOM` then `--body "@$env:TEMP\kql_body.json"`.

```bash
# Run a KQL query against the Eventhouse data plane
cat > /tmp/kql_body.json << 'EOF'
{"db":"MyDB","csl":".show tables"}
EOF

az rest --method POST \
  --url "${CLUSTER_URI}/v1/rest/query" \
  --resource "https://kusto.kusto.windows.net" \
  --headers "Content-Type=application/json" \
  --body @/tmp/kql_body.json \
  | jq '.Tables[0].Rows'
```

> **Tip**: Pipe through `jq` for readable output, or redirect to a file for CSV-style export:
> `az rest ... --output-file results.json`

---

## Schema Discovery and Security

### Schema Discovery

Key commands:

```kql
.show tables                              // list all tables
.show table MyTable schema as json        // column names + types
.show table MyTable details               // row count, extent count, size
.show functions                           // list stored functions
.show materialized-views                  // list materialized views
```

### Security

- Eventhouse uses **Fabric workspace roles** for access control (Admin, Member, Contributor, Viewer).
- KQL Database-level roles (`admins`, `viewers`, `users`) can further restrict access.
- **Row-Level Security (RLS)** is supported via `restrict access` and security functions.
- Discover principals: `.show database MyDatabase principals` or `.show table MyTable principals`.

---

## Monitoring and Diagnostics

### Active Queries

```kql
// Currently running queries
.show queries

// Recent completed commands
.show commands
| where StartedOn > ago(1h)

// Journal of management operations
.show journal
| where Event == "CREATE-TABLE" or Event == "ALTER-TABLE-RETENTION-POLICY"
| top 20 by EventTimestamp desc
```

### Ingestion Monitoring

```kql
// Ingestion failures
.show ingestion failures
| where FailedOn > ago(24h)
| summarize count() by ErrorCode, Details
| top 10 by count_

// Table ingestion metrics
.show table MyTable extents
| summarize ExtentCount = count(), TotalRows = sum(RowCount), TotalSize = sum(OriginalSize)
```

### Database Statistics

```kql
// Database usage (size, extent count, row count)
.show database datastats
```

---

## Performance Best Practices

### Query Patterns

| Pattern | Why |
|---|---|
| **Always filter by time first** | `where Timestamp > ago(1h)` — enables extent pruning |
| **Use `has` over `contains`** | `has` uses term index (fast); `contains` does substring scan (slow) |
| **`project` early** | Drop unneeded columns early to reduce memory |
| **`summarize` with `bin()`** | Time bucketing enables efficient aggregation |
| **`take` for exploration** | Use `take 100` instead of full scans when exploring |
| **`materialize()` for reuse** | Cache sub-expression results used multiple times |
| **Avoid `*` in `project`** | Explicit column list prevents schema-change surprises |

### String Matching Performance

| Operator | Indexed | Case-Sensitive | Speed |
|---|---|---|---|
| `==` | ✅ Yes | Yes | Fastest |
| `has` | ✅ Yes | No | Fast |
| `has_cs` | ✅ Yes | Yes | Fast |
| `contains` | ❌ No | No | Slow |
| `startswith` | ✅ Partial | No | Medium |
| `matches regex` | ❌ No | Yes | Slowest |

### Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| No time filter | Always add `where Timestamp > ago(...)` |
| `contains` on large tables | Switch to `has` if searching for whole terms |
| `join` without reducing both sides | Filter/project both sides before joining |
| `mv-expand` on large arrays without limit | Add `limit` or filter after expand |
| Cartesian joins | Ensure join keys actually match; use `kind=inner` |

---

## Common Consumption Patterns

### Time-Series Analysis

```kql
// Hourly trend
MyTable
| where Timestamp > ago(24h)
| summarize Count = count() by bin(Timestamp, 1h)
| render timechart

// Compare today vs yesterday
let today = MyTable | where Timestamp > ago(1d) | summarize TodayCount = count() by bin(Timestamp, 1h);
let yesterday = MyTable | where Timestamp between (ago(2d) .. ago(1d))
    | summarize YesterdayCount = count() by bin(Timestamp, 1h);
today | join kind=fullouter (yesterday) on Timestamp
```

### Top-N Analysis

```kql
MyTable
| where Timestamp > ago(7d)
| summarize EventCount = count() by Category
| top 10 by EventCount desc
```

### Percentile Distribution

```kql
MyTable
| where Timestamp > ago(1h)
| summarize
    p50 = percentile(Duration, 50),
    p90 = percentile(Duration, 90),
    p99 = percentile(Duration, 99)
    by bin(Timestamp, 5m)
| render timechart
```

### Dynamic Field Exploration

```kql
MyTable
| take 100
| mv-expand kind=array Properties
| extend Key = Properties[0], Value = Properties[1]
| summarize dcount(Value) by tostring(Key)
```

---

## Gotchas, Troubleshooting, and Quick Reference

### Gotchas and Troubleshooting

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | `Request is invalid and cannot be processed` | Token audience mismatch | Use audience `https://kusto.kusto.windows.net/.default` |
| 2 | Query timeout | No time filter, scanning too much data | Add `where Timestamp > ago(...)` to narrow scan |
| 3 | `Partial query failure` | One or more extents failed to respond | Retry; if persistent, check `.show database datastats` and Fabric capacity health |
| 4 | `has` returns unexpected results | `has` matches whole terms, not substrings | Use `contains` for substring matching (slower) |
| 5 | `==` misses rows | `==` is case-sensitive for strings | Use `=~` for case-insensitive equality |
| 6 | `join` produces too many rows | Many-to-many join | Add `kind=inner` and filter both sides first |
| 7 | `dynamic` column shows as string | Column stored as string, not dynamic | Wrap with `parse_json(ColumnName)` or `todynamic()` |
| 8 | Empty results on valid table | Wrong database context | Check `database("CorrectDB").TableName` or reconnect |
| 9 | `Forbidden (403)` | Insufficient permissions | Request `viewer` role on the database |
| 10 | Slow `contains` queries | Full-text scan, no index | Switch to `has` (term index) or `has_any()` |
| 11 | `render` not showing in CLI | `render` is client-side hint | Use Fabric Real-Time Intelligence portal or export data |
| 12 | `dcount()` returns approximate value | HyperLogLog algorithm by design | Use `dcount(x, 4)` for higher accuracy (costly) or `T \| distinct Column \| count` for exact |

### Quick Reference: Consumption Capabilities by Scenario

| Scenario | KQL Pattern |
|---|---|
| Explore table shape | `.show table T schema as json` then `T \| take 10` |
| Row count | `T \| count` |
| Time-series trend | `T \| where Timestamp > ago(1d) \| summarize count() by bin(Timestamp, 1h) \| render timechart` |
| Top contributors | `T \| summarize Count=count() by Dimension \| top 10 by Count desc` |
| Search for value | `T \| where Column has "searchterm"` |
| Cross-database query | `database("OtherDB").OtherTable \| take 10` |
| Export to CSV | `az rest ... --output-file results.json` then convert with `jq` |
| Materialized view | `materialized_view("MyMV") \| where ...` |

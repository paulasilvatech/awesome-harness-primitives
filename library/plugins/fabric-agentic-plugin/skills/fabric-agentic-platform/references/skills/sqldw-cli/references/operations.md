<!-- Mode reference for the `sqldw-cli` skill. Loaded on demand from `skills/sqldw-cli/SKILL.md` when the request matches the `operations` mode. -->

> **MODE-CRITICAL NOTES (operations mode)**
> 1. `queryinsights.*` views exist on **both a Warehouse and a Lakehouse SQL analytics endpoint**, and reading them needs **Contributor or higher** on the workspace. Query Insights is always on — there is no setting to enable. A completed query lands in the `queryinsights` of the item it ran against.
> 2. **Every figure comes from a query you ran in the turn you report it, cited inline** — `2,140 ms (queryinsights.long_running_queries)`. Do not carry numbers forward from an earlier turn: re-run the query. "I already ran the diagnostics" is not a source, and an uncited number reads as invented. Zero rows is a valid finding; never fill the gap from this reference.
> 3. **Read-only:** `SELECT` only. Do not issue `ALTER`, `CREATE`, `DROP`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, or a `SET` that changes warehouse configuration — including a tuning change you are confident in, such as `ALTER DATABASE ... SET RESULT_SET_CACHING ON`. Applying the change yourself is never the answer here.
> 4. **A vague optimisation request ("just make my warehouse faster") is a new diagnostic question, not a summary request.** Re-run the queries backing the levers you are about to name — in that same turn — then **ask which target to pursue**. Recommend only what those queries showed; never answer from earlier turns' output, and never list every knob that could be tuned.

# sqldw-cli operations mode — Fabric Warehouse Performance and Diagnostics

This skill provides performance analysis, deep diagnostics, and optimization guidance for Microsoft Fabric Data Warehouse via the **`fabric-sqlendpoint-execute_query` MCP tool** and the built-in **`queryinsights`** views. All queries are read-only.

## Prerequisites

For workspace/item discovery via `az rest`, see [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest). For legacy `sqlcmd` reference (fallback only), see [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../../common/COMMON-CLI.md#sql--tds-data-plane-access).

> **⚠️ SQL Execution Override:** For SQL data-plane execution, this skill supersedes COMMON-CLI SQL/TDS guidance. Use MCP `fabric-sqlendpoint-execute_query` (see [Tool Stack](#tool-stack)) unless explicitly using Legacy CLI Fallback.

**Monitoring-specific requirements:**
- **Workspace role**: Contributor or higher on the target workspace (required for `queryinsights` views)
- **A Warehouse or Lakehouse SQL analytics endpoint must exist** with recent query activity (`queryinsights` views retain 30 days; data appears with up to 15 min delay)

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id] |
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) ||
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) ||
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Includes pagination, LRO polling, and rate-limiting patterns |
| Capacity Management | [COMMON-CORE.md § Capacity Management](../../../common/COMMON-CORE.md#capacity-management) ||
| Gotchas, Best Practices & Troubleshooting (Platform) | [COMMON-CORE.md § Gotchas, Best Practices & Troubleshooting](../../../common/COMMON-CORE.md#gotchas-best-practices--troubleshooting) ||
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../../common/COMMON-CLI.md#tool-selection-rationale) ||
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource`**; includes pagination and LRO helpers |
| SQL / TDS Data-Plane Access | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../../common/COMMON-CLI.md#sql--tds-data-plane-access) | Legacy `sqlcmd` reference (MCP is primary — see Tool Stack) |
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference | [COMMON-CLI.md § Quick Reference](../../../common/COMMON-CLI.md#quick-reference) | `az rest` template + token audience/tool matrix |
| Connection Fundamentals | [SQLDW-CONSUMPTION-CORE.md § Connection Fundamentals](../../../common/SQLDW-CONSUMPTION-CORE.md#connection-fundamentals) | TDS, port 1433, Entra-only, no MARS |
| Monitoring and Diagnostics | [SQLDW-CONSUMPTION-CORE.md § Monitoring and Diagnostics](../../../common/SQLDW-CONSUMPTION-CORE.md#monitoring-and-diagnostics) | Query labels; DMVs (live) + `queryinsights.*` (30-day history) |
| Performance: Best Practices and Troubleshooting | [SQLDW-CONSUMPTION-CORE.md § Performance: Best Practices and Troubleshooting](../../../common/SQLDW-CONSUMPTION-CORE.md#performance-best-practices-and-troubleshooting) | Statistics, caching, clustering, query tips |
| Gotchas and Troubleshooting (Consumption) | [SQLDW-CONSUMPTION-CORE.md § Gotchas and Troubleshooting Reference](../../../common/SQLDW-CONSUMPTION-CORE.md#gotchas-and-troubleshooting-reference) | 18 numbered issues with cause + resolution |
| Data Ingestion (DW Only) | [SQLDW-AUTHORING-CORE.md § Data Ingestion (DW Only)](../../../common/SQLDW-AUTHORING-CORE.md#data-ingestion-dw-only) | COPY INTO, OPENROWSET, method comparison |
| Query Reference | [query-reference.md](operations/query-reference.md) | T-SQL queries, parameters, and example output for all analyses |
| Composite Recipes | [COMMON-CLI.md § Composite Recipes](../../../common/COMMON-CLI.md#composite-recipes) ||
| Item-Type Capability Matrix | [SQLDW-CONSUMPTION-CORE.md § Item-Type Capability Matrix](../../../common/SQLDW-CONSUMPTION-CORE.md#item-type-capability-matrix) | Read-vs-write scope by item type; `queryinsights` itself is available on both Warehouse and SQLEP |
| Prerequisites | [SKILL.md § Prerequisites](#prerequisites) | Tools, auth, workspace role |
| Tool Stack | [SKILL.md § Tool Stack](#tool-stack) ||
| Connection | [SKILL.md § Connection](#connection) ||
| Performance Analysis | [SKILL.md § Performance Analysis](#performance-analysis) | Long-running queries, resource consumers, user insights, baselines |
| Deep Diagnostics | [SKILL.md § Deep Diagnostics](#deep-diagnostics) | Pressure windows, cache warmth, cluster keys |
| Fabric DW Constraints | [SKILL.md § Fabric DW Constraints](#fabric-dw-constraints) | **NEVER recommend unsupported features** |
| Best Practices | [SKILL.md § Best Practices](#best-practices) | Monitoring-specific guidance |
| Agentic Workflows | [SKILL.md § Agentic Workflows](#agentic-workflows) | Common investigation patterns |
| Gotchas, Rules, Troubleshooting | [SKILL.md § Gotchas, Rules, Troubleshooting](#gotchas-rules-troubleshooting) | **MUST DO / AVOID / PREFER** checklists |
| Examples | [SKILL.md § Examples](#examples) | Prompt/response pairs |

---

## Tool Stack

For installation and setup, see [Prerequisites](#prerequisites).

| Tool | Role |
|---|---|
| `fabric-sqlendpoint-execute_query` MCP tool | **Primary**: Execute monitoring T-SQL queries against Fabric SQL Endpoints. Auth handled by MCP protocol. |
| `az` CLI | Token acquisition, Fabric REST for workspace/item discovery |
| `jq` | Parse JSON from `az rest` |

> **IMPORTANT — MCP vs sqlcmd:**
> This skill uses the `fabric-sqlendpoint-execute_query` MCP tool for all T-SQL execution. Do **not** use COMMON-CLI SQL/TDS/sqlcmd sections for query execution.

> **Agent preflight** — verify before first operation:
> 1. Confirm the `fabric-sqlendpoint-execute_query` tool is available in your tool list. This tool is provided by the `fabric-sqlendpoint` MCP server, which is registered either by installing a Fabric skills **plugin** (the path for end users) or via this repo's `.mcp.json` — other MCP clients may register it through their own configuration.
> 2. If no matching tool is found, the user must register the Fabric SQL Endpoint MCP server.
>    - **Global URL**: `https://api.fabric.microsoft.com/v1/mcp/dataPlane/sqlEndpoint`
>    - **Item-scoped URL**: `https://api.fabric.microsoft.com/v1/mcp/dataPlane/workspaces/{workspaceId}/items/{itemId}/sqlEndpoint`

### MCP Tool Signature

```text
fabric-sqlendpoint-execute_query(workspaceId, itemId, query)
```

> **Tool name may differ:** `execute_query` is the logical operation. Depending on how the server is
> registered, the concrete tool name in your tool list may be prefixed (e.g.
> `fabric-sqlendpoint-execute_query` or `sqlendpoint-global-execute_query`). Invoke the concrete name
> shown in your tool list, always passing `workspaceId`, `itemId`, and `query`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `workspaceId` | string (UUID) | The workspace GUID containing the target Warehouse |
| `itemId` | string (UUID) | The GUID of the Warehouse item |
| `query` | string | T-SQL query text (single batch — no `GO` separators) |

**Returns:** CSV resource (RFC 4180) with tabular results + metadata text.

**Limits:** 10,000 rows max | 300s timeout | 20 req/min rate limit _(observed defaults, not a documented contract — the service can change them; verify against live 429/timeout/truncation responses)_

---

## Connection

### Discover workspaceId and itemId

You need the workspace GUID and warehouse GUID to call `fabric-sqlendpoint-execute_query`:

```bash
# 1. Find workspace ID by name (capture into WS_ID for the next call)
WS_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[?displayName=='MyWorkspace'].id" --output tsv)
echo "Workspace ID: $WS_ID"

# 2. Find warehouse item ID by name
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/warehouses" \
  --query "value[?displayName=='MyWarehouse'].id" --output tsv
```

### Execute a Monitoring Query

```text
fabric-sqlendpoint-execute_query(
  workspaceId: "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  itemId: "11111111-2222-3333-4444-555555555555",
  query: "SELECT TOP 5 * FROM queryinsights.long_running_queries ORDER BY last_run_total_elapsed_time_ms DESC"
)
```

**No additional connection setup needed** — authentication is handled transparently by the MCP protocol.

---

## Performance Analysis

All SQL queries, parameters, return fields, and response formatting are in [query-reference.md](operations/query-reference.md).

### Long-Running Queries Summary

Find the slowest queries from `queryinsights.long_running_queries`. See [query-reference.md § Long-Running Queries Summary](operations/query-reference.md#long-running-queries-summary) for SQL and formatting.

### Top Resource Consumers

Find CPU- and storage-heavy queries from `queryinsights.exec_requests_history`. See [query-reference.md § Top Resource Consumers](operations/query-reference.md#top-resource-consumers) for SQL, thresholds, and formatting.

**Recommendation thresholds:**
- Remote scans > 1,000 MB → review data layout, consider clustering
- CPU > 5,000,000 ms → review query logic
- Elapsed > 300,000 ms → check joins, filters, statistics
- Reference: [Performance guidelines](https://learn.microsoft.com/fabric/data-warehouse/guidelines-warehouse-performance)

### Top Users Insights

Analyze user activity and query patterns. See [query-reference.md § Top Users Insights](operations/query-reference.md#top-users-insights) for SQL and classification logic.

### Compare Recent vs Baseline

Detect performance regressions by comparing recent window against historical baseline. See [query-reference.md § Compare Recent vs Baseline](operations/query-reference.md#compare-recent-vs-baseline) for SQL and formatting.

### Recent Queries

Retrieve the most recently executed queries. See [query-reference.md § Recent Queries](operations/query-reference.md#recent-queries) for SQL.

### Search Query Patterns

Search historical query patterns by table name, column, or keyword. See [query-reference.md § Search Query Patterns](operations/query-reference.md#search-query-patterns) for SQL.

---

## Deep Diagnostics

All SQL queries for diagnostics are in [query-reference.md](operations/query-reference.md).

### Analyze Long-Running Query Plans

See [query-reference.md § Long-Running Query Analysis](operations/query-reference.md#long-running-query-analysis) for SQL.

**Analysis guidance** — when reviewing slow queries, check:
- High `data_scanned_remote_storage_mb` → data layout issues (run OPTIMIZE, consider clustering)
- High `allocated_cpu_time_ms` relative to elapsed → CPU-bound (simplify joins, reduce columns)
- High elapsed but low CPU → waiting on resources (check for pressure windows)

### Analyze Pressure Window Queries

Identify SQL pool pressure events using `queryinsights.sql_pool_insights` and correlate with the heaviest queries running during those windows. See [query-reference.md § Pressure Window Analysis](operations/query-reference.md#pressure-window-analysis) for the two-step SQL.

**Usage:** Step 1 returns pressure windows with `window_start` and `window_end` timestamps. Substitute those actual timestamp values into Step 2's WHERE clause to find overlapping queries.

**Global recommendations** — based on aggregate pressure analysis:
- If SELECT pool has more pressure → read-heavy workload, suggest caching and column pruning
- If NONSELECT pool has more pressure → write-heavy, suggest batching and COPY INTO
- If total pressure > 60 min → suggest scaling capacity or staggering workloads

### Analyze Query Cache Warmth

See [query-reference.md § Cache Warmth Analysis](operations/query-reference.md#cache-warmth-analysis) for SQL.

**Classification logic** — for each execution, compute `total_mb = remote + memory + disk`:
- `result_cache_hit = 1` → **cached**
- `remote_mb / total_mb > 0.8` → **cold** (>80% from remote storage)
- `(memory_mb + disk_mb) / total_mb > 0.8` → **warm** (>80% from cache)

**Recommendations:**
- Over 50% cold runs → Enable result set caching: `ALTER DATABASE SET RESULT_SET_CACHING ON;`
- Always-cold patterns → Check for `GETDATE()`/`GETUTCDATE()` or volatile functions that bust the cache key

### Recommend Cluster Keys

See [query-reference.md § Cluster Key Recommendations](operations/query-reference.md#cluster-key-recommendations) for SQL.

**Key rules:**
- Only `WHERE` predicates benefit from clustering — equality `JOIN ON` conditions do **not**
- Prefer mid-to-high cardinality columns (many distinct values)
- Maximum 4 clustering columns
- Use CTAS with `WITH (CLUSTER BY (...))` — `ALTER TABLE` is not supported

**To apply clustering** — see [query-reference.md § Cluster Key Recommendations](operations/query-reference.md#cluster-key-recommendations) for CTAS creation, `sp_rename` table swap, and verification SQL.

> **Note:** Fabric does not support `ALTER TABLE SET DATA_CLUSTERING_KEY` or `RENAME OBJECT`. Always use CTAS with `WITH (CLUSTER BY (...))` and `sp_rename` for table swaps.

---

## Fabric DW Constraints

**NEVER recommend features not supported in Fabric Data Warehouse.** Always consult this list before making optimization suggestions.

| Do NOT Recommend | Why | Recommend Instead |
|------------------|-----|-------------------|
| Nonclustered indexes | Not supported | V-Order, column pruning, predicate pushdown |
| Materialized views | Not supported | Standard views or result set caching |
| Index hints (FORCESEEK/FORCESCAN) | Not supported | Simplify query structure |
| Multi-column statistics | Not supported | Single-column statistics on key columns |
| `ALTER TABLE SET DATA_CLUSTERING_KEY` | Not supported | CTAS with `WITH (CLUSTER BY (...))` |
| `RENAME OBJECT` | Not supported | `EXEC sp_rename 'schema.old', 'new'` |
| Change isolation level | Snapshot only | Fabric uses snapshot isolation exclusively |
| CREATE USER | Not supported | Manage users via Fabric workspace |
| Triggers | Not supported | Application logic or Fabric pipelines |
| Recursive CTEs | Not supported | Iterative approach |
| "Enable Query Insights" setting | Query Insights is always on — there is no setting | If access is denied, the user needs Contributor or higher on the workspace |

---

## Agentic Workflows

### Workflow 1: "Why is my warehouse slow?"

1. **Check for pressure events** → Run the pressure window analysis query (last 24h)
2. **Find the heaviest queries** → Run top resource consumers query (last 1h)
3. **Analyze slow queries** → Run long-running queries analysis
4. **Check cache behavior** → Run cache warmth analysis (last 24h)
5. **Recommend clustering** → Run cluster key recommendation queries

### Workflow 2: "Has performance degraded?"

1. **Compare against baseline** → Run recent vs baseline comparison (1h vs 7-day)
2. **Identify new slow queries** → Run long-running queries summary (top 5)
3. **Check user patterns** → Run top users insights (last 24h)

### Workflow 3: "Optimize my warehouse"

1. **Review best practices** → See [SQLDW-CONSUMPTION-CORE.md § Performance: Best Practices and Troubleshooting](../../../common/SQLDW-CONSUMPTION-CORE.md#performance-best-practices-and-troubleshooting)
2. **Find optimization targets** → Run top resource consumers (last 24h)
3. **Recommend clustering** → Run cluster key recommendation queries
4. **Analyze cold-start queries** → Run cache warmth analysis

### Workflow 4: "What are people running?"

1. **Recent activity** → Run recent queries (top 10)
2. **User patterns** → Run top users insights (last 24h)
3. **Search for specific patterns** → Run query pattern search with search term

---

## Best Practices

For comprehensive Fabric DW best practices, see [SQLDW-CONSUMPTION-CORE.md § Performance: Best Practices and Troubleshooting](../../../common/SQLDW-CONSUMPTION-CORE.md#performance-best-practices-and-troubleshooting) and the [Fabric guidelines](https://learn.microsoft.com/fabric/data-warehouse/guidelines-warehouse-performance).

**Monitoring-specific best practices:**

- **Start broad, then drill down** — begin with long-running queries summary and baseline comparison before deep diagnostics
- **Use pressure window analysis** for root-cause analysis rather than guessing at bottlenecks
- **Label all agent queries** with `OPTION (LABEL = 'AGENTCLI_MONITOR_...')` for tracing in Query Insights
- **Prefer mid-to-high cardinality columns** for clustering keys — low cardinality columns offer limited file-skipping benefit
- **Use `WHERE` predicates** to identify cluster key candidates — equality `JOIN ON` conditions do not benefit from clustering
- **Always verify clustering** after CTAS by querying `sys.index_columns.data_clustering_ordinal`
- **Check cold vs warm cache** before concluding a query is inherently slow — first execution may be a cold start
- **Adjust time windows** (`DATEADD` parameters) to match user's investigation scope — don't default to arbitrary windows

---

## Gotchas, Rules, Troubleshooting

For generic CLI gotchas (connection, auth, shell escaping): see [COMMON-CLI.md § Gotchas & Troubleshooting](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific).
For T-SQL/platform gotchas: see [SQLDW-CONSUMPTION-CORE.md § Gotchas and Troubleshooting Reference](../../../common/SQLDW-CONSUMPTION-CORE.md#gotchas-and-troubleshooting-reference).

### MUST DO
- Always check [Fabric DW Constraints](#fabric-dw-constraints) before recommending optimizations
- When recommending clustering, instruct users to use CTAS with `WITH (CLUSTER BY (...))` — not ALTER TABLE
- Report actual query output — do not fabricate or assume results
- **Label queries** with `OPTION (LABEL = 'AGENTCLI_MONITOR_...')` for Query Insights tracing
- **Verify `fabric-sqlendpoint-execute_query` MCP tool availability** before first operation

### PREFER
- Start with high-level queries (long-running summary, baseline comparison) before drilling into diagnostics
- Use the pressure window analysis for root-cause analysis rather than guessing at bottlenecks
- Combine multiple queries in the [Agentic Workflows](#agentic-workflows) for comprehensive investigations
- Adjust time windows (`DATEADD` parameters) based on what the user asks for
- Consolidate related diagnostic queries into fewer calls to respect rate limits

### AVOID
- Recommending Fabric-unsupported features (nonclustered indexes, materialized views, index hints, triggers)
- Suggesting that Query Insights needs to be "enabled" or "turned on" — `queryinsights` views are always available; permission errors indicate insufficient workspace role (Contributor or higher required)
- Running monitoring queries without confirming workspaceId and itemId
- Guessing at performance root causes without running the diagnostic queries
- Using `SELECT *` in monitoring queries — always select specific columns
- Using `GO` separators or sqlcmd meta-commands in queries (MCP tool accepts single batches only)
- Unbounded queries without `TOP N` — 10,000 row limit applies

### TROUBLESHOOTING (Monitoring-Specific)

For generic connection/auth troubleshooting, see [COMMON-CLI.md § Gotchas & Troubleshooting](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific).

| Symptom | Cause | Fix |
|---|---|---|
| `Invalid object name 'queryinsights...'` | New warehouse < 2 min old | Wait ~2 minutes |
| Permission errors on `queryinsights.*` | Insufficient workspace role | Requires Contributor or higher |
| No data in queryinsights views | No recent query activity or < 15 min delay | Wait 15 min after query completion |
| No rows but data exists | RLS filtering | Check `USER_NAME()`, verify RLS policies |
| `fabric-sqlendpoint-execute_query` tool not available | MCP server not registered | User must add Fabric SQL Endpoint MCP server |
| HTTP 429 rate limit | Too many calls in 1 min | Wait 60s; consolidate queries |
| Query timeout (300s) | Complex diagnostics | Narrow time window with tighter DATEADD |

---

## Examples

### Find Slow Queries

**User:** "What are the slowest queries in my warehouse?"

**Agent:** Runs the long-running queries summary via `fabric-sqlendpoint-execute_query`:

```text
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT TOP 5
      left(last_run_command, 80) AS query_preview,
      number_of_runs,
      last_run_total_elapsed_time_ms,
      median_total_elapsed_time_ms
   FROM queryinsights.long_running_queries
   ORDER BY median_total_elapsed_time_ms DESC")
```

> The top 5 slowest queries are:
> 1. `SELECT * FROM FactSales JOIN DimCustomer...` — ran 12 times, last took 45,200 ms (median 38,500 ms)
> 2. `SELECT region, SUM(amount)...` — ran 8 times, last took 32,100 ms (median 29,000 ms)
> ...

### Diagnose Performance Degradation

**User:** "Is my warehouse slower than last week?"

**Agent:** Runs the baseline comparison query and presents:

> **Performance Comparison (last 1h vs 7-day baseline):**
> - Elapsed time: 2,450 ms avg → 4,100 ms avg (+67.3%)
> - CPU consumption: 1,200 ms → 2,800 ms (+133.3%)
> - Data scanned: 450 MB → 480 MB (+6.7%)
>
> Significant regression detected. Let me check for pressure events and analyze the heaviest queries...

Then follows up with pressure window and resource consumer queries.

### Get Clustering Recommendations

**User:** "Which tables should I cluster and on what columns?"

**Agent:** Runs the cluster key recommendation queries and presents:

> **Recommended Clustering Keys:**
> | Table | Recommended Columns | Row Count | Total Scanned MB |
> |-------|-------------------|-----------|-----------------|
> | dbo.FactSales | SaleDate, Region | 50M | 12,500 MB |
> | dbo.FactInventory | ProductID, WarehouseID | 12M | 3,200 MB |
>
> To apply clustering, use CTAS:
> ```sql
> CREATE TABLE dbo.FactSales_clustered
> WITH (CLUSTER BY (SaleDate, Region))
> AS SELECT * FROM dbo.FactSales;
> ```

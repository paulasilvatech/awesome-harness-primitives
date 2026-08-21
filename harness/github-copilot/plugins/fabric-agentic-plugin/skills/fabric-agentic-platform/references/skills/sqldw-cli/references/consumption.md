<!-- Mode reference for the `sqldw-cli` skill. Loaded on demand from `skills/sqldw-cli/SKILL.md` when the request matches the `consumption` mode. -->

> **MODE-CRITICAL NOTES (consumption mode)**
> 1. This mode is **read-only**. Run `SELECT` and catalog queries only — no `CREATE`, `ALTER`, `DROP`, `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `TRUNCATE` or `COPY INTO`. If the user asks for a write, refuse the mutation in the final answer and name `sqldw-cli authoring mode` as a separate follow-up request rather than performing it.
> 2. The deliverable is the answer, not the reading. Run the query against the live endpoint and report the real rows; a summary of this reference does not answer the request.

# sqldw-cli consumption mode — Fabric Warehouse, Lakehouse SQL Endpoint and Mirrored Database Querying

> **⚠️ SQL Execution Override:** For SQL data-plane execution, this skill supersedes COMMON-CLI SQL/TDS guidance. Use MCP `fabric-sqlendpoint-execute_query` (see [Tool Stack](#tool-stack)) unless explicitly using Legacy CLI Fallback.

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id]|
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) ||
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) ||
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Includes pagination, LRO polling, and rate-limiting patterns |
| OneLake Data Access | [COMMON-CORE.md § OneLake Data Access](../../../common/COMMON-CORE.md#onelake-data-access) | Requires `storage.azure.com` token, not Fabric token |
| Job Execution | [COMMON-CORE.md § Job Execution](../../../common/COMMON-CORE.md#job-execution) ||
| Capacity Management | [COMMON-CORE.md § Capacity Management](../../../common/COMMON-CORE.md#capacity-management) ||
| Gotchas, Best Practices & Troubleshooting | [COMMON-CORE.md § Gotchas, Best Practices & Troubleshooting](../../../common/COMMON-CORE.md#gotchas-best-practices--troubleshooting) ||
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../../common/COMMON-CLI.md#tool-selection-rationale) ||
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource`**; includes pagination and LRO helpers |
| OneLake Data Access via `curl` | [COMMON-CLI.md § OneLake Data Access via curl](../../../common/COMMON-CLI.md#onelake-data-access-via-curl) | Use `curl` not `az rest` (different token audience) |
| SQL / TDS Data-Plane Access | [SKILL.md § Tool Stack](#tool-stack) | `fabric-sqlendpoint-execute_query` MCP tool — replaces sqlcmd |
| Job Execution (CLI) | [COMMON-CLI.md § Job Execution](../../../common/COMMON-CLI.md#job-execution) ||
| OneLake Shortcuts | [COMMON-CLI.md § OneLake Shortcuts](../../../common/COMMON-CLI.md#onelake-shortcuts) ||
| Capacity Management (CLI) | [COMMON-CLI.md § Capacity Management](../../../common/COMMON-CLI.md#capacity-management) ||
| Composite Recipes | [COMMON-CLI.md § Composite Recipes](../../../common/COMMON-CLI.md#composite-recipes) ||
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference | [COMMON-CLI.md § Quick Reference](../../../common/COMMON-CLI.md#quick-reference) | `az rest` template + token audience/tool matrix |
| Item-Type Capability Matrix | [SQLDW-CONSUMPTION-CORE.md § Item-Type Capability Matrix](../../../common/SQLDW-CONSUMPTION-CORE.md#item-type-capability-matrix) | **Read first** — shows what's read-only (SQLEP) vs read-write (DW) |
| Connection Fundamentals | [SQLDW-CONSUMPTION-CORE.md § Connection Fundamentals](../../../common/SQLDW-CONSUMPTION-CORE.md#connection-fundamentals) | TDS, port 1433, Entra-only, no MARS |
| Supported T-SQL Surface Area (Consumption Focus) | [SQLDW-CONSUMPTION-CORE.md § Supported T-SQL Surface Area](../../../common/SQLDW-CONSUMPTION-CORE.md#supported-t-sql-surface-area-consumption-focus) | **Read before writing T-SQL** — includes data types (no `nvarchar`/`datetime`/`money`) |
| Read-Side Objects You Can Create | [SQLDW-CONSUMPTION-CORE.md § Read-Side Objects You Can Create](../../../common/SQLDW-CONSUMPTION-CORE.md#read-side-objects-you-can-create) | Views, TVFs, scalar UDFs, procedures |
| Temporary Tables | [SQLDW-CONSUMPTION-CORE.md § Temporary Tables](../../../common/SQLDW-CONSUMPTION-CORE.md#temporary-tables) | Use `DISTRIBUTION = ROUND_ROBIN` for INSERT INTO SELECT support |
| Cross-Database Queries | [SQLDW-CONSUMPTION-CORE.md § Cross-Database Queries](../../../common/SQLDW-CONSUMPTION-CORE.md#cross-database-queries) | 3-part naming, same workspace |
| Security for Consumption | [SQLDW-CONSUMPTION-CORE.md § Security for Consumption](../../../common/SQLDW-CONSUMPTION-CORE.md#security-for-consumption) | GRANT/DENY, RLS, CLS, DDM |
| Monitoring and Diagnostics | [SQLDW-CONSUMPTION-CORE.md § Monitoring and Diagnostics](../../../common/SQLDW-CONSUMPTION-CORE.md#monitoring-and-diagnostics) | Includes query labels; DMVs (live) + `queryinsights.*` (30-day history) |
| Performance: Best Practices and Troubleshooting | [SQLDW-CONSUMPTION-CORE.md § Performance: Best Practices and Troubleshooting](../../../common/SQLDW-CONSUMPTION-CORE.md#performance-best-practices-and-troubleshooting) | Statistics, caching, clustering, query tips |
| REST API: Refresh SQL Endpoint Metadata | [SQLDW-CONSUMPTION-CORE.md § REST API: Refresh SQL Endpoint Metadata](../../../common/SQLDW-CONSUMPTION-CORE.md#rest-api-refresh-sql-endpoint-metadata) | Force metadata sync when SQLEP data is stale after ETL |
| System Catalog Queries (Metadata Exploration) | [SQLDW-CONSUMPTION-CORE.md § System Catalog Queries](../../../common/SQLDW-CONSUMPTION-CORE.md#system-catalog-queries-metadata-exploration) | `sys.tables`, `sys.columns`, `sys.views`, `sys.stats` |
| Common Consumption Patterns (End-to-End Examples) | [SQLDW-CONSUMPTION-CORE.md § Common Consumption Patterns](../../../common/SQLDW-CONSUMPTION-CORE.md#common-consumption-patterns-end-to-end-examples) | Reporting views, cross-DB analytics, temp table staging |
| Gotchas and Troubleshooting Reference | [SQLDW-CONSUMPTION-CORE.md § Gotchas and Troubleshooting Reference](../../../common/SQLDW-CONSUMPTION-CORE.md#gotchas-and-troubleshooting-reference) | 18 numbered issues with cause + resolution |
| Quick Reference: Consumption Capabilities by Scenario | [SQLDW-CONSUMPTION-CORE.md § Quick Reference: Consumption Capabilities](../../../common/SQLDW-CONSUMPTION-CORE.md#quick-reference-consumption-capabilities-by-scenario) | Scenario → approach lookup |
| Schema and Object Discovery | [discovery-queries.md § Schema and Object Discovery](consumption/discovery-queries.md#schema-and-object-discovery) | Tables, columns, views, functions, procedures, cross-DB |
| Security Discovery | [discovery-queries.md § Security Discovery](consumption/discovery-queries.md#security-discovery) ||
| Statistics and Performance Metadata | [discovery-queries.md § Statistics and Performance Metadata](consumption/discovery-queries.md#statistics-and-performance-metadata) ||
| Data Export Workflow | [script-templates.md § Data Export Workflow](consumption/script-templates.md#data-export-workflow) | Query to CSV + parameterized date range export |
| Schema Discovery Workflow | [script-templates.md § Schema Discovery Workflow](consumption/script-templates.md#schema-discovery-workflow) | Full schema report via MCP |
| Performance Investigation Workflow | [script-templates.md § Performance Investigation Workflow](consumption/script-templates.md#performance-investigation-workflow) | Active queries, slow query analysis |
| Tool Stack | [SKILL.md § Tool Stack](#tool-stack) | `fabric-sqlendpoint-execute_query` MCP tool + `az` CLI |
| Connection | [SKILL.md § Connection](#connection) ||
| Agentic Exploration ("Chat With My Data") | [SKILL.md § Agentic Exploration](#agentic-exploration-chat-with-my-data) | **Start here** for data exploration |
| Script Generation | [consumption-cli-quickref.md § Script Generation](consumption/consumption-cli-quickref.md#script-generation) | When to emit a standalone bash/PowerShell script; `az rest` discovery + Legacy CLI Fallback |
| Monitoring and Performance | [consumption-cli-quickref.md § Monitoring and Performance](consumption/consumption-cli-quickref.md#monitoring-and-performance) | Active queries DMV (read-only; session termination is out of scope) |
| Gotchas, Rules, Troubleshooting | [SKILL.md § Gotchas, Rules, Troubleshooting](#gotchas-rules-troubleshooting) | **MUST DO / AVOID / PREFER** checklists |
| Agent Integration Notes | [consumption-cli-quickref.md § Agent Integration Notes](consumption/consumption-cli-quickref.md#agent-integration-notes) | Per-agent CLI tips |

---

## Tool Stack

| Tool | Role | Install |
|---|---|---|
| `fabric-sqlendpoint-execute_query` MCP tool | **Primary**: Execute T-SQL queries against Fabric SQL Endpoints. Returns CSV results. Auth handled by MCP protocol. | No install — server-side. Requires MCP server registration (see below). |
| `az` CLI | Auth (`az login`), Fabric REST for workspace/item discovery. | Pre-installed in most dev environments |
| `jq` | Parse JSON from `az rest` | Pre-installed or trivial |

> **IMPORTANT — MCP vs sqlcmd:**
> This skill uses the `fabric-sqlendpoint-execute_query` MCP tool for all T-SQL execution. Do **not** use COMMON-CLI SQL/TDS/sqlcmd sections for query execution. Those references apply only for `az rest` control-plane patterns.

> **Agent preflight** — verify before first SQL operation:
> 1. Confirm the `fabric-sqlendpoint-execute_query` tool is available in your tool list. This tool is provided by the `fabric-sqlendpoint` MCP server, which is registered either by installing a Fabric skills **plugin** (the path for end users) or via this repo's `.mcp.json` — other MCP clients may register it through their own configuration.
> 2. If no matching tool is found, the user must register the Fabric SQL Endpoint MCP server. See [mcp-setup/](../../../mcp-setup/) for registration instructions.
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
| `workspaceId` | string (UUID) | The workspace GUID containing the target item |
| `itemId` | string (UUID) | The Fabric item GUID to query. For a **Warehouse** or **Mirrored Database**, use the item id. For a **Lakehouse**, use its **SQL analytics endpoint** id (`properties.sqlEndpointProperties.id`) — **not** the Lakehouse item id. |
| `query` | string | T-SQL query text (single batch — no `GO` separators or sqlcmd meta-commands) |

**Returns:** CSV resource (RFC 4180) with tabular results + metadata text ("Query returned N rows.").

> **Batch guidance:** Multiple statements (e.g., `SET NOCOUNT ON; SELECT ...`) are allowed in a single call as long as there are no `GO` separators. Only the last result set is returned. For independent read queries, prefer separate `fabric-sqlendpoint-execute_query` calls for clearer error handling.

### MCP Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Max rows | 10,000 | Results are truncated beyond this. Use `TOP`, filters, or aggregations. |
| Query timeout | 300 seconds | Long-running queries fail with timeout error. |
| Rate limit | 20 requests/min per identity | HTTP 429 returned when exceeded. Retry after backoff. |

> These values are **observed defaults, not a documented contract** — the MCP service can change them. Treat them as guidance and confirm the current behavior from live `429` / timeout / truncation responses (or Microsoft Learn, if/when published) rather than relying on the exact numbers.

### Supported Item Types

| Item Type | itemId Source | Read Queries | DML (INSERT/UPDATE/DELETE) |
|-----------|--------------|--------------|---------------------------|
| **Warehouse** | `GET /v1/workspaces/{wId}/warehouses` → item `id` | ✅ | ✅ |
| **Lakehouse SQL Endpoint** | `GET /v1/workspaces/{wId}/lakehouses` → `properties.sqlEndpointProperties.id` (**not** the lakehouse `id`) | ✅ | ❌ (read-only) |
| **Mirrored Database** | `GET /v1/workspaces/{wId}/mirroredDatabases` → item `id` | ✅ | ❌ (read-only) |

---

## Connection

### Discover workspaceId and itemId

You need the workspace GUID and item GUID to call `fabric-sqlendpoint-execute_query`. Discover them via the Fabric REST API:

```bash
# 1. Find workspace ID by name (capture into WS_ID for the next calls)
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
# For a Lakehouse, pass its SQL analytics endpoint id — NOT the lakehouse item id
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses" \
  --query "value[?displayName=='MyLakehouse'].properties.sqlEndpointProperties.id" --output tsv
```

### Execute a Query

Once you have `workspaceId` and `itemId`, call the MCP tool:

```text
fabric-sqlendpoint-execute_query(
  workspaceId: "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  itemId: "11111111-2222-3333-4444-555555555555",
  query: "SELECT TOP 10 * FROM dbo.FactSales"
)
```

**No additional connection setup needed** — authentication is handled transparently by the MCP protocol.

---

## Agentic Exploration ("Chat With My Data")

### Schema Discovery Sequence

Run these in order to understand what's in the endpoint. See [references/discovery-queries.md](consumption/discovery-queries.md) for extended discovery queries.

```text
# 1. List schemas
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY schema_name")

# 2. List tables and views
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT table_schema, table_name, table_type FROM INFORMATION_SCHEMA.TABLES ORDER BY table_schema, table_name")

# 3. Columns for a table
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT column_name, data_type, character_maximum_length, is_nullable FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema='dbo' AND table_name='FactSales' ORDER BY ordinal_position")

# 4. Preview rows
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT TOP 5 * FROM dbo.FactSales")

# 5. Row counts
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS row_count FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id JOIN sys.partitions p ON t.object_id=p.object_id AND p.index_id IN (0,1) GROUP BY s.name, t.name ORDER BY row_count DESC")

# 6. Programmability objects (views, functions, procedures)
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT name, type_desc FROM sys.objects WHERE type IN ('V','FN','IF','P','TF') ORDER BY type_desc, name")
```

### Agentic Workflow

1. **Discover** → Run Steps 1–3 to understand available tables/columns.
2. **Sample** → `SELECT TOP 5` on relevant tables.
3. **Formulate** → Write T-SQL using [SQLDW-CONSUMPTION-CORE.md](../../../common/SQLDW-CONSUMPTION-CORE.md) Supported T-SQL Surface Area.
4. **Execute** → Call `fabric-sqlendpoint-execute_query(workspaceId, itemId, query)`.
5. **Iterate** → Refine based on results.
6. **Present** → Show results or generate follow-up queries.

---

## Gotchas, Rules, Troubleshooting

For full T-SQL/platform gotchas: [SQLDW-CONSUMPTION-CORE.md](../../../common/SQLDW-CONSUMPTION-CORE.md) Gotchas and Troubleshooting Reference.

### MUST DO

- **Verify `fabric-sqlendpoint-execute_query` MCP tool is available** — check tool list before first operation. If unavailable, instruct user to register the MCP server.
- **Always use `TOP` or `WHERE` filters** — the MCP tool returns a maximum of 10,000 rows. If exactly 10,000 rows are returned, results are likely truncated.
- **Use `COUNT(*)` first for large tables** — check row counts before running unbounded SELECTs.
- **`SET NOCOUNT ON;`** at the start of multi-statement queries — suppresses row-count messages.
- **Label queries** with `OPTION (LABEL = 'AGENTCLI_...')` for Query Insights tracing.
- **Send valid T-SQL only** — no `GO` batch separators, no `:setvar`, no sqlcmd meta-commands. Each `fabric-sqlendpoint-execute_query` call is a single T-SQL batch.
- **Use multiple tool calls for multi-batch operations** — if you need `GO` separators, split into separate `fabric-sqlendpoint-execute_query` calls.

### AVOID

- **`sqlcmd`** — use the `fabric-sqlendpoint-execute_query` MCP tool instead. Do not shell out to sqlcmd for query execution.
- **Unbounded `SELECT *`** — will hit the 10,000 row cap. Always use `TOP N` or `WHERE` filters.
- **Rapid-fire sequential queries** — rate limit is 20 req/min per identity. Space out calls or consolidate with JOINs/UNION ALL.
- **DML on Lakehouse/Mirrored DB** — these are read-only. DML only works on Warehouse items.
- **`GO` separators in query text** — not supported. Use separate tool calls for each batch.
- **MARS** — not supported. Each query runs independently.
- **Hardcoded item IDs** — discover via REST API (Connection section).

### PREFER

- **`fabric-sqlendpoint-execute_query` MCP tool** over any CLI tool for T-SQL execution.
- **`TOP N`** on exploration queries — avoid hitting row limits.
- **Consolidating related queries** into single SELECTs with JOINs to reduce rate-limit pressure.
- **`az rest`** for Fabric REST API operations — workspace/item discovery, capacity management.
- **Aggregate queries** (`COUNT`, `SUM`, `AVG`, `GROUP BY`) over full table scans.
- **`ORDER BY` with `TOP`** for deterministic results.

### TROUBLESHOOTING

| Symptom | Cause | Fix |
|---|---|---|
| MCP tool not available | MCP server not registered | Register `https://api.fabric.microsoft.com/v1/mcp/dataPlane/sqlEndpoint` in MCP client config |
| HTTP 401 / Unauthorized | Auth token expired or invalid | Re-authenticate (depends on MCP client — may need `az login` refresh) |
| HTTP 403 / Forbidden | Insufficient permissions on workspace/item | Verify user has Viewer+ role on the workspace/item |
| HTTP 404 / Not Found | Wrong workspaceId/itemId, or feature not enabled | Verify IDs via REST API; check if MCP feature is enabled for the tenant |
| HTTP 429 / Too Many Requests | Rate limit exceeded (20 req/min) | Wait and retry with backoff; consolidate queries |
| Query timeout (300s) | Query too complex or data too large | Simplify query, add filters, use `TOP` |
| Exactly 10,000 rows returned | Result truncation | Add `TOP N` or `WHERE` filters; use `COUNT(*)` to check total |
| "Invalid workspaceId/itemId" | Malformed UUID | Verify UUIDs are correct format (8-4-4-4-12 hex digits) |
| SQL error in response | T-SQL syntax error or invalid object | Fix T-SQL; verify table/column names via schema discovery |
| No rows but data exists | RLS filtering | Check `USER_NAME()`, verify RLS policies |
| `Invalid object name 'queryinsights...'` | New warehouse < 2 min old | Wait ~2 minutes |


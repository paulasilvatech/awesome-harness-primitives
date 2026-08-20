<!-- Mode reference for the `sqldw-cli` skill. Loaded on demand from `skills/sqldw-cli/SKILL.md` when the request matches the `authoring` mode. -->

> **MODE-CRITICAL NOTES (authoring mode)**
> 1. Table DDL, DML, `COPY INTO` / `OPENROWSET` ingestion, transactions and time travel are **Warehouse-only**. A Lakehouse SQL analytics endpoint and a Mirrored Database are read-only for table data — only views, functions, procedures and schemas can be authored there.
> 2. Reading the reference is not authoring. Every mutation ends with a `fabric-sqlendpoint-execute_query` call that runs the DDL/DML, followed by a readback query proving it landed.

# sqldw-cli authoring mode — Fabric Warehouse and SQL Endpoint T-SQL Authoring

> **⚠️ SQL Execution Override:** For SQL data-plane execution, this skill supersedes COMMON-CLI SQL/TDS guidance. Use MCP `fabric-sqlendpoint-execute_query` (see [Tool Stack](#tool-stack)) unless explicitly using Legacy CLI Fallback.

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id] |
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) ||
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) ||
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Includes pagination, LRO polling, and rate-limiting patterns |
| OneLake Data Access | [COMMON-CORE.md § OneLake Data Access](../../../common/COMMON-CORE.md#onelake-data-access) | Requires `storage.azure.com` token, not Fabric token |
| Definition Envelope | [ITEM-DEFINITIONS-CORE.md § Definition Envelope](../../../common/ITEM-DEFINITIONS-CORE.md#definition-envelope) | Definition payload structure |
| Per-Item-Type Definitions | [ITEM-DEFINITIONS-CORE.md § Per-Item-Type Definitions](../../../common/ITEM-DEFINITIONS-CORE.md#per-item-type-definitions) | Support matrix, decoded content, part paths — [REST specs](../../../common/COMMON-CORE.md#item-creation), [CLI recipes](../../../common/COMMON-CLI.md#item-crud-operations) |
| Job Execution | [COMMON-CORE.md § Job Execution](../../../common/COMMON-CORE.md#job-execution) ||
| Capacity Management | [COMMON-CORE.md § Capacity Management](../../../common/COMMON-CORE.md#capacity-management) ||
| Gotchas, Best Practices & Troubleshooting (Platform) | [COMMON-CORE.md § Gotchas, Best Practices & Troubleshooting](../../../common/COMMON-CORE.md#gotchas-best-practices--troubleshooting) ||
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../../common/COMMON-CLI.md#tool-selection-rationale) ||
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource`**; includes pagination and LRO helpers |
| OneLake Data Access via `curl` | [COMMON-CLI.md § OneLake Data Access via curl](../../../common/COMMON-CLI.md#onelake-data-access-via-curl) | Use `curl` not `az rest` (different token audience) |
| SQL / TDS Data-Plane Access | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../../common/COMMON-CLI.md#sql--tds-data-plane-access) | Legacy `sqlcmd` reference (MCP is primary — see Tool Stack) |
| Job Execution (CLI) | [COMMON-CLI.md § Job Execution](../../../common/COMMON-CLI.md#job-execution) ||
| OneLake Shortcuts | [COMMON-CLI.md § OneLake Shortcuts](../../../common/COMMON-CLI.md#onelake-shortcuts) ||
| Capacity Management (CLI) | [COMMON-CLI.md § Capacity Management](../../../common/COMMON-CLI.md#capacity-management) ||
| Composite Recipes | [COMMON-CLI.md § Composite Recipes](../../../common/COMMON-CLI.md#composite-recipes) ||
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference | [COMMON-CLI.md § Quick Reference](../../../common/COMMON-CLI.md#quick-reference) | `az rest` template + token audience/tool matrix |
| Item-Type Capability Matrix | [SQLDW-CONSUMPTION-CORE.md § Item-Type Capability Matrix](../../../common/SQLDW-CONSUMPTION-CORE.md#item-type-capability-matrix) | Shows read-only (SQLEP) vs read-write (DW) |
| Connection Fundamentals | [SQLDW-CONSUMPTION-CORE.md § Connection Fundamentals](../../../common/SQLDW-CONSUMPTION-CORE.md#connection-fundamentals) | TDS, port 1433, Entra-only, no MARS |
| Supported T-SQL Surface Area (Consumption Focus) | [SQLDW-CONSUMPTION-CORE.md § Supported T-SQL Surface Area](../../../common/SQLDW-CONSUMPTION-CORE.md#supported-t-sql-surface-area-consumption-focus) | **Read before writing T-SQL** — includes data types (no `nvarchar`/`datetime`/`money`) |
| Read-Side Objects You Can Create | [SQLDW-CONSUMPTION-CORE.md § Read-Side Objects You Can Create](../../../common/SQLDW-CONSUMPTION-CORE.md#read-side-objects-you-can-create) | Views, TVFs, scalar UDFs, procedures |
| Temporary Tables | [SQLDW-CONSUMPTION-CORE.md § Temporary Tables](../../../common/SQLDW-CONSUMPTION-CORE.md#temporary-tables) ||
| Cross-Database Queries | [SQLDW-CONSUMPTION-CORE.md § Cross-Database Queries](../../../common/SQLDW-CONSUMPTION-CORE.md#cross-database-queries) | 3-part naming, same workspace only |
| Security for Consumption | [SQLDW-CONSUMPTION-CORE.md § Security for Consumption](../../../common/SQLDW-CONSUMPTION-CORE.md#security-for-consumption) | GRANT/DENY, RLS, CLS, DDM |
| Monitoring and Diagnostics | [SQLDW-CONSUMPTION-CORE.md § Monitoring and Diagnostics](../../../common/SQLDW-CONSUMPTION-CORE.md#monitoring-and-diagnostics) | Includes query labels; DMVs (live) + `queryinsights.*` (30-day history) |
| Performance: Best Practices and Troubleshooting | [SQLDW-CONSUMPTION-CORE.md § Performance: Best Practices and Troubleshooting](../../../common/SQLDW-CONSUMPTION-CORE.md#performance-best-practices-and-troubleshooting) | Statistics, caching, clustering, query tips |
| REST API: Refresh SQL Endpoint Metadata | [SQLDW-CONSUMPTION-CORE.md § REST API: Refresh SQL Endpoint Metadata](../../../common/SQLDW-CONSUMPTION-CORE.md#rest-api-refresh-sql-endpoint-metadata) | Force metadata sync when SQLEP is stale after ETL |
| System Catalog Queries (Metadata Exploration) | [SQLDW-CONSUMPTION-CORE.md § System Catalog Queries](../../../common/SQLDW-CONSUMPTION-CORE.md#system-catalog-queries-metadata-exploration) | `sys.tables`, `sys.columns`, `sys.views`, `sys.stats` |
| Common Consumption Patterns | [SQLDW-CONSUMPTION-CORE.md § Common Consumption Patterns](../../../common/SQLDW-CONSUMPTION-CORE.md#common-consumption-patterns-end-to-end-examples) | Reporting views, cross-DB analytics, temp table staging |
| Gotchas and Troubleshooting (Consumption) | [SQLDW-CONSUMPTION-CORE.md § Gotchas and Troubleshooting Reference](../../../common/SQLDW-CONSUMPTION-CORE.md#gotchas-and-troubleshooting-reference) | 18 numbered issues with cause + resolution |
| Quick Reference: Consumption Capabilities | [SQLDW-CONSUMPTION-CORE.md § Quick Reference: Consumption Capabilities](../../../common/SQLDW-CONSUMPTION-CORE.md#quick-reference-consumption-capabilities-by-scenario) ||
| Authoring Capability Matrix | [SQLDW-AUTHORING-CORE.md § Authoring Capability Matrix](../../../common/SQLDW-AUTHORING-CORE.md#authoring-capability-matrix) | **Read first** — DW vs SQLEP authoring scope |
| Table DDL (DW Only) | [SQLDW-AUTHORING-CORE.md § Table DDL (DW Only)](../../../common/SQLDW-AUTHORING-CORE.md#table-ddl-dw-only) | CREATE, CTAS, ALTER, sp_rename, DROP, constraints, schema evolution, IDENTITY |
| DML Operations (DW Only) | [SQLDW-AUTHORING-CORE.md § DML Operations (DW Only)](../../../common/SQLDW-AUTHORING-CORE.md#dml-operations-dw-only) | INSERT...SELECT, UPDATE, DELETE, TRUNCATE, MERGE |
| Data Ingestion (DW Only) | [SQLDW-AUTHORING-CORE.md § Data Ingestion (DW Only)](../../../common/SQLDW-AUTHORING-CORE.md#data-ingestion-dw-only) | COPY INTO, OPENROWSET, method comparison |
| Transactions (DW Only) | [SQLDW-AUTHORING-CORE.md § Transactions (DW Only)](../../../common/SQLDW-AUTHORING-CORE.md#transactions-dw-only) | Snapshot isolation only; write-write conflict rules |
| Stored Procedures (Authoring Patterns) | [SQLDW-AUTHORING-CORE.md § Stored Procedures (Authoring Patterns)](../../../common/SQLDW-AUTHORING-CORE.md#stored-procedures-authoring-patterns) | ETL procs, upsert, CTAS swap, cursor replacement |
| Time Travel and Warehouse Snapshots | [SQLDW-AUTHORING-CORE.md § Time Travel and Warehouse Snapshots (DW Only)](../../../common/SQLDW-AUTHORING-CORE.md#time-travel-and-warehouse-snapshots-dw-only) | FOR TIMESTAMP AS OF; 30-day retention; snapshots GA |
| Source Control and CI/CD | [SQLDW-AUTHORING-CORE.md § Source Control and CI/CD (DW Only — Preview)](../../../common/SQLDW-AUTHORING-CORE.md#source-control-and-cicd-dw-only--preview) | Git integration, SQL DB projects, deployment pipelines |
| Authoring Permission Model | [SQLDW-AUTHORING-CORE.md § Authoring Permission Model](../../../common/SQLDW-AUTHORING-CORE.md#authoring-permission-model) | Contributor minimum for DDL/DML; Admin for GRANT |
| Authoring Gotchas and Troubleshooting | [SQLDW-AUTHORING-CORE.md § Authoring Gotchas and Troubleshooting](../../../common/SQLDW-AUTHORING-CORE.md#authoring-gotchas-and-troubleshooting) | 17-row issue/cause/resolution table |
| Common Authoring Patterns | [SQLDW-AUTHORING-CORE.md § Common Authoring Patterns](../../../common/SQLDW-AUTHORING-CORE.md#common-authoring-patterns-end-to-end-examples) | Incremental load, SCD Type 1, SQLEP view layer |
| Quick Reference: Authoring Decision Guide | [SQLDW-AUTHORING-CORE.md § Quick Reference: Authoring Decision Guide](../../../common/SQLDW-AUTHORING-CORE.md#quick-reference-authoring-decision-guide) | Scenario → recommended approach lookup |
| Core Authoring via MCP | [authoring-cli-quickref.md § Core Authoring via MCP](authoring/authoring-cli-quickref.md#core-authoring-via-mcp) | Table DDL, DML, data ingestion via execute_query |
| Advanced Authoring Patterns via MCP | [authoring-cli-quickref.md § Advanced Authoring Patterns via MCP](authoring/authoring-cli-quickref.md#advanced-authoring-patterns-via-mcp) | Transactions, schema evolution, stored procedures, time travel |
| MCP Workflow Templates | [authoring-script-templates.md § MCP Workflow Templates](authoring/authoring-script-templates.md#mcp-workflow-templates) | COPY INTO, ELT pipeline, upsert with retry, schema migration, time travel recovery |
| Tool Stack | [SKILL.md § Tool Stack](#tool-stack) | `fabric-sqlendpoint-execute_query` MCP tool + `az` CLI; verify before first op |
| Connection | [SKILL.md § Connection](#connection) | workspaceId/itemId discovery, execute example |
| Query Execution | [authoring-cli-quickref.md § Query Execution](authoring/authoring-cli-quickref.md#query-execution) | MCP tool call format, batch considerations |
| Agentic Workflows | [SKILL.md § Agentic Workflows](#agentic-workflows) | **Start here** — discover schema before any write |
| Monitoring Authoring Operations | [authoring-cli-quickref.md § Monitoring Authoring Operations](authoring/authoring-cli-quickref.md#monitoring-authoring-operations) | Active DML/DDL, recent ETL, failed writes |
| Gotchas, Rules, Troubleshooting | [SKILL.md § Gotchas, Rules, Troubleshooting](#gotchas-rules-troubleshooting) | **MUST DO / AVOID / PREFER** checklists |
| Agent Integration Notes | [authoring-cli-quickref.md § Agent Integration Notes](authoring/authoring-cli-quickref.md#agent-integration-notes) | Platform-specific tips (Copilot CLI, Claude Code) |

---

## Tool Stack

| Tool | Role | Install |
|---|---|---|
| `fabric-sqlendpoint-execute_query` MCP tool | **Primary**: Execute DDL/DML T-SQL queries against Fabric SQL Endpoints. Returns CSV results. Auth handled by MCP protocol. | No install — server-side. Requires MCP server registration. |
| `az` CLI | Auth (`az login`), Fabric REST for workspace/item discovery, snapshot management. | Pre-installed in most dev environments |
| `jq` | Parse JSON from `az rest` | Pre-installed or trivial |

> **IMPORTANT — MCP vs sqlcmd:**
> This skill uses the `fabric-sqlendpoint-execute_query` MCP tool for all T-SQL execution. Do **not** use COMMON-CLI SQL/TDS/sqlcmd sections for query execution.

> **Agent preflight** — verify before first operation:
> 1. Confirm the `fabric-sqlendpoint-execute_query` tool is available in your tool list. This tool is provided by the `fabric-sqlendpoint` MCP server, which is registered either by installing a Fabric skills **plugin** (the path for end users) or via this repo's `.mcp.json` — other MCP clients may register it through their own configuration.
> 2. If no matching tool is found, the user must register the Fabric SQL Endpoint MCP server. See [mcp-setup/](../../../mcp-setup/).
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
| `itemId` | string (UUID) | The Fabric item GUID to target. For a **Warehouse**, use the item id. For a **Lakehouse**, use its **SQL analytics endpoint** id (`properties.sqlEndpointProperties.id`) — **not** the Lakehouse item id. |
| `query` | string | T-SQL query text (single batch — no `GO` separators or sqlcmd meta-commands) |

**Returns:** CSV resource (RFC 4180) with tabular results + metadata text.

> **Batch guidance:** Multiple statements without `GO` are allowed in one call (e.g., `CREATE TABLE ...; INSERT INTO ...`). However, only the last result set is returned, and an error in any statement fails the entire batch. **Prefer separate `fabric-sqlendpoint-execute_query` calls** for independent DDL/DML operations — this gives clearer error messages and lets you verify each step succeeded before proceeding.

### MCP Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Max rows returned | 10,000 | For DDL/DML, row count metadata indicates affected rows |
| Query timeout | 300 seconds | Long-running operations may timeout |
| Rate limit | 20 requests/min per identity | HTTP 429 returned when exceeded |

> These values are **observed defaults, not a documented contract** — the MCP service can change them. Treat them as guidance and confirm the current behavior from live `429` / timeout / truncation responses (or Microsoft Learn, if/when published) rather than relying on the exact numbers.

### Authoring Scope by Item Type

| Capability | Warehouse (DW) | Lakehouse/Mirrored DB SQLEP |
|---|---|---|
| Table DDL (CREATE/ALTER/DROP) | ✅ | ❌ |
| DML (INSERT/UPDATE/DELETE/MERGE) | ✅ | ❌ |
| COPY INTO, OPENROWSET (ingest) | ✅ | OPENROWSET read-only |
| Transactions | ✅ | ❌ |
| Time travel, snapshots | ✅ | ❌ |
| CREATE VIEW/FUNCTION/PROCEDURE | ✅ | ✅ |
| CREATE SCHEMA | ✅ | ✅ |

### Fabric DW DDL Constraints

These constraints are **hard requirements** — violating them produces errors:

| Constraint | Details |
|---|---|
| No `DEFAULT` in CREATE TABLE | Default values not supported. Set defaults in application/INSERT logic. |
| No `PRIMARY KEY` inside CREATE TABLE | Must add via `ALTER TABLE ... ADD CONSTRAINT ... PRIMARY KEY NONCLUSTERED (col) NOT ENFORCED` |
| `DATETIME2` requires precision | Always use `DATETIME2(6)`, never bare `DATETIME2` |
| Unsupported data types | `NCHAR`, `NVARCHAR`, `TEXT`, `IMAGE`, `MONEY`, `SMALLMONEY`, `DATETIME` — use `VARCHAR`, `DECIMAL`, `DATETIME2(6)` instead |
| No `WITH DISTRIBUTION` | Distribution is automatic in Fabric |
| Constraints must be `NOT ENFORCED` | `PRIMARY KEY NONCLUSTERED NOT ENFORCED`, `UNIQUE NONCLUSTERED NOT ENFORCED`, `FOREIGN KEY NOT ENFORCED` |
| PK columns must be `NOT NULL` | Declare PK columns as `NOT NULL` in CREATE TABLE before adding PK constraint |
| `ALTER TABLE` scope | Add/drop nullable columns (must specify `NULL`) and add/drop constraints (`NOT ENFORCED` only) are GA; `ALTER COLUMN` type changes are **in preview** (see note below) |

> **`MERGE` and `ALTER COLUMN` are NOT hard errors.** Per [T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area), `MERGE` is a **generally available** Warehouse feature and `ALTER TABLE ... ALTER COLUMN` is **in preview**. Prefer an explicit `DELETE`+`INSERT` when snapshot-conflict isolation matters, and `CTAS` + `sp_rename` for production-critical column-type changes — as a robustness choice, not because the syntax is blocked.

**Correct CREATE TABLE pattern:**

```sql
CREATE TABLE dbo.Orders (
    OrderID INT NOT NULL,
    CustomerName VARCHAR(100) NULL,
    Amount DECIMAL(19,4) NULL,
    CreatedAt DATETIME2(6) NULL
)
```

```sql
ALTER TABLE dbo.Orders ADD CONSTRAINT PK_Orders PRIMARY KEY NONCLUSTERED (OrderID) NOT ENFORCED
```

**Additional supported patterns:**
- `CREATE TABLE [dbo].[clone] AS CLONE OF [dbo].[source]` — duplicate table structure + data
- `COPY INTO` — highest-throughput ingestion from external storage

---

## Connection

### Discover workspaceId and itemId

You need the workspace GUID and item GUID to call `fabric-sqlendpoint-execute_query`:

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

# For a Lakehouse SQL endpoint, pass its SQL analytics endpoint id — NOT the lakehouse item id
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses" \
  --query "value[?displayName=='MyLakehouse'].properties.sqlEndpointProperties.id" --output tsv
```

### Execute a Query

```text
fabric-sqlendpoint-execute_query(
  workspaceId: "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  itemId: "11111111-2222-3333-4444-555555555555",
  query: "CREATE TABLE dbo.FactSales (SaleID bigint NOT NULL, Amount decimal(19,4) NOT NULL)"
)
```

**No additional connection setup needed** — authentication is handled transparently by the MCP protocol.

### Verifying DDL/DML Results

For DDL (CREATE/ALTER/DROP), the tool returns success with metadata. Always verify:

```text
# After CREATE TABLE, verify it exists
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT table_schema, table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_name = 'FactSales'")

# After DML, check row count
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT COUNT(*) AS row_count FROM dbo.FactSales")
```

---

## Agentic Workflows

### Schema Discovery Before Authoring

Before any write operation, discover the target schema:

```text
# 1. List tables
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT table_schema, table_name FROM INFORMATION_SCHEMA.TABLES ORDER BY 1,2")

# 2. Check columns
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT column_name, data_type, is_nullable FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='FactSales' ORDER BY ordinal_position")

# 3. Sample data
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT TOP 5 * FROM dbo.FactSales")

# 4. Check constraints
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT constraint_name, constraint_type FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE table_name='FactSales'")

# 5. Row counts
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS row_count FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id JOIN sys.partitions p ON t.object_id=p.object_id AND p.index_id IN (0,1) GROUP BY s.name, t.name ORDER BY row_count DESC")

# 6. Programmability objects
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT name, type_desc FROM sys.objects WHERE type IN ('V','FN','IF','P','TF') ORDER BY type_desc, name")
```

### Agentic Workflow

1. **Discover** → Run steps 1–4 to understand available tables/columns.
2. **Sample** → `SELECT TOP 5` on relevant tables.
3. **Formulate** → Select pattern from [SQLDW-AUTHORING-CORE.md](../../../common/SQLDW-AUTHORING-CORE.md) (Table DDL through Common Authoring Patterns).
4. **Execute** → Call `fabric-sqlendpoint-execute_query(workspaceId, itemId, query)`. For multi-batch operations (e.g., CREATE PROCEDURE with BEGIN/END), use a single batch without `GO`.
5. **Verify** → Query affected table (`SELECT COUNT(*)`, `SELECT TOP 5`).
6. **Optionally follow up** → Run additional queries to confirm schema changes.

---

## Gotchas, Rules, Troubleshooting

For full authoring gotchas: [SQLDW-AUTHORING-CORE.md](../../../common/SQLDW-AUTHORING-CORE.md) Authoring Gotchas and Troubleshooting.
For CLI-specific issues: [COMMON-CLI.md](../../../common/COMMON-CLI.md) Gotchas & Troubleshooting (CLI-Specific).

### MUST DO

- **Verify workspace has capacity before creating warehouse** — call `GET /v1/workspaces/{id}` and check `capacityId`.
- **Verify `fabric-sqlendpoint-execute_query` MCP tool is available** — check the tool list before the first operation. If unavailable, instruct the user to register the MCP server.
- **Discover `workspaceId` and `itemId` first** — resolve the target Warehouse via `az rest`; the tool takes GUIDs, not an FQDN or `-d <DatabaseName>`.
- **`az login` first (for discovery)** — the `az rest` workspace/warehouse lookups need an Azure CLI session. The `fabric-sqlendpoint` MCP server itself ships headerless and authenticates via your MCP client's native Fabric session, not the Azure CLI token; no signed-in session → auth failure on either path.
- **`SET NOCOUNT ON;`** in scripts — suppresses row-count messages that corrupt output.
- **Send a single T-SQL batch per call** — no `GO` separators and no `-i file.sql`; split multi-batch work (CREATE PROCEDURE, multi-step transactions) into separate `fabric-sqlendpoint-execute_query` calls.
- **Label authoring queries** with `OPTION (LABEL = 'ETL_description')`.
- **Use explicit `CAST()`** in CTAS to control output types.
- **Keep transactions short** — long transactions increase conflict window.

### AVOID

- **`GO` separators** — the MCP tool accepts only a single T-SQL batch. Combine related DDL in one statement or call `fabric-sqlendpoint-execute_query` multiple times.
- **sqlcmd meta-commands** (`:setvar`, `:r`, `-i`) — not available in MCP tool. Inline all SQL in the `query` parameter.
- **Unbounded `SELECT *`** — 10,000 row limit. Always use `TOP N` or `WHERE` to limit result sets.
- **Singleton `INSERT ... VALUES`** at scale — creates tiny Parquet files. Use INSERT...SELECT, CTAS, or COPY INTO.
- **`DROP TABLE IF EXISTS` + `CREATE TABLE`** to refresh — loses time-travel history. Use `TRUNCATE TABLE` + `INSERT INTO`.
- **MERGE in production** — GA, but table-level snapshot-conflict detection makes concurrent writers likely to fail. Prefer DELETE + INSERT when isolation matters.
- **ALTER COLUMN in production** — in preview; prefer CTAS + `sp_rename` for production-critical column-type changes (Schema Evolution).
- **Variables in CTAS** — not allowed. Wrap in dynamic SQL: `EXEC sp_executesql N'CREATE TABLE ...'`.
- **DML on Lakehouse/Mirrored DB SQLEP** — read-only for table data. Only views/funcs/procs can be authored.
- **Concurrent UPDATE/DELETE on same table** — snapshot isolation conflicts at table level. Serialize writes.
- **Rapid-fire MCP calls** — rate limit is 20 req/min. Consolidate multiple statements into one batch where possible.
- **MARS** — not supported. Remove `MultipleActiveResultSets` from connection strings.

### PREFER

- **CTAS** over `CREATE TABLE` + `INSERT` — parallel, single-operation.
- **`INSERT ... SELECT`** over singleton INSERTs.
- **`COPY INTO`** for external file ingestion — highest throughput.
- **DELETE + INSERT** over MERGE for upserts in production.
- **`TRUNCATE TABLE`** over `DELETE FROM` without WHERE — faster, preserves history.
- **Consolidating related DDL** into a single `fabric-sqlendpoint-execute_query` call when no `GO` is required between statements.
- **CTAS + sp_rename** for large-scale transforms instead of UPDATE.
- **`fabric-sqlendpoint-execute_query` MCP tool** over sqlcmd for all T-SQL operations.
- **`SET NOCOUNT ON;`** prefix — reduces metadata noise in results.
- **`TOP N` or `WHERE`** clauses — stay within 10K row limit.

### TROUBLESHOOTING

| Symptom | Fix |
|---|---|
| Error 24556/24706 snapshot conflict | Serialize writes to same table; retry with backoff |
| COPY INTO auth error | Grant Storage Blob Data Reader on ADLS; or SAS in CREDENTIAL |
| COPY INTO from OneLake fails | Provision workspace identity; check firewall rules |
| CTAS unexpected types | Use explicit `CAST()` in SELECT |
| Singleton INSERT poor perf | Remediate: CTAS + drop + rename to consolidate Parquet |
| `fabric-sqlendpoint-execute_query` tool not available | MCP server not registered — user must add Fabric SQL Endpoint MCP server |
| HTTP 429 rate limit exceeded | Wait 60s and retry; consolidate queries into fewer calls |
| Query timeout (300s) | Break into smaller operations; for COPY INTO, check source file sizes |
| sp_rename on SQLEP fails | Only available on Warehouse, not Lakehouse/Mirrored DB |
| Deploy drops/recreates table | Avoid ALTER TABLE in DB project; apply manually |
| Only last result set returned | MCP returns only the final SELECT. Split multi-SELECT batches into separate calls. |
| Binary columns unreadable | Columns with `[base64]` suffix are base64-encoded. Decode if needed. |

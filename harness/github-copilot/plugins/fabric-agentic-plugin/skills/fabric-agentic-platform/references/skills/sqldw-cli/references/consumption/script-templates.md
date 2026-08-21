# Script Templates

Agent workflow templates using the `fabric-sqlendpoint-execute_query` MCP tool. Each template shows a sequence of MCP tool calls that accomplish a specific task.

> **Note:** These templates are for AI agents using the MCP `fabric-sqlendpoint-execute_query` tool. For users who need standalone shell scripts outside of an agent, see the [Legacy CLI Fallback](#legacy-cli-fallback) section at the bottom.

## Data Export Workflow

### Query to CSV

The `fabric-sqlendpoint-execute_query` tool returns results as CSV natively. To export data:

```text
# Step 1: Execute query — results arrive as CSV resource
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SET NOCOUNT ON;
SELECT ProductID, ProductName, Category, Price
FROM dbo.DimProduct
ORDER BY ProductName
")
```

The response contains an embedded CSV resource that can be saved directly.

### Parameterized Date Range Export

```text
# Step 1: Check total rows in range
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SELECT COUNT(*) AS total_rows
FROM dbo.FactSales
WHERE SaleDate BETWEEN '2025-01-01' AND '2025-06-30'
")

# Step 2: Export (paginate if > 10,000 rows)
# List the columns you need explicitly (avoid SELECT *) and ORDER BY a unique key
# so pagination is stable across calls.
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SET NOCOUNT ON;
SELECT SaleID, ProductID, SaleDate, Amount
FROM dbo.FactSales
WHERE SaleDate BETWEEN '2025-01-01' AND '2025-06-30'
ORDER BY SaleID
OFFSET 0 ROWS FETCH NEXT 10000 ROWS ONLY
")
```

## Schema Discovery Workflow

```text
# Step 1: List schemas
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY schema_name")

# Step 2: Tables with row counts
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS rows
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name
ORDER BY rows DESC
")

# Step 3: Views
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT SCHEMA_NAME(schema_id) AS [schema], name FROM sys.views ORDER BY [schema], name")

# Step 4: Stored Procedures
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT SCHEMA_NAME(schema_id) AS [schema], name FROM sys.procedures ORDER BY [schema], name")

# Step 5: Functions
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT SCHEMA_NAME(schema_id) AS [schema], name, type_desc FROM sys.objects WHERE type IN ('FN','IF','TF') ORDER BY [schema], name")
```

## Performance Investigation Workflow

```text
# Step 1: Active queries
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT request_id, session_id, command, status, total_elapsed_time/1000 AS elapsed_sec FROM sys.dm_exec_requests WHERE status='running' ORDER BY total_elapsed_time DESC")

# Step 2: Top 20 slowest queries (last 24h)
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SELECT TOP 20
    distributed_statement_id,
    login_name,
    COALESCE(label,'') AS label,
    total_elapsed_time_ms,
    data_scanned_remote_storage_mb,
    LEFT(command, 120) AS command_preview
FROM queryinsights.exec_requests_history
WHERE start_time >= DATEADD(HOUR, -24, GETUTCDATE())
ORDER BY total_elapsed_time_ms DESC
")

# Step 3: Top 10 most frequent queries
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SELECT TOP 10
    query_hash,
    number_of_runs,
    avg_total_elapsed_time_ms,
    LEFT(last_run_command, 120) AS query_preview
FROM queryinsights.frequently_run_queries
ORDER BY number_of_runs DESC
")
```

## Workspace/Item Discovery (via az rest)

These `az rest` commands are still needed for discovering workspace and item IDs before calling `fabric-sqlendpoint-execute_query`:

```bash
# Find workspace ID (capture into WS_ID for the next call)
WS_ID=$(az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[?displayName=='MyWorkspace'].id" --output tsv)
echo "Workspace ID: $WS_ID"

# Find warehouse ID
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/warehouses" \
  --query "value[?displayName=='MyWarehouse'].id" --output tsv
```

---

## Legacy CLI Fallback

> **Use only when the `fabric-sqlendpoint-execute_query` MCP tool is not available** (e.g., outside an AI agent environment).

For standalone scripts outside of agent environments, `sqlcmd` (Go) can be used as a fallback:

```bash
# Install: winget install sqlcmd (Windows) / brew install sqlcmd (macOS)
sqlcmd -S "<endpoint>.datawarehouse.fabric.microsoft.com" -d "<DatabaseName>" -G \
  -Q "SET NOCOUNT ON; SELECT TOP 10 * FROM dbo.FactSales" -W -s"," -o results.csv
```

See [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../../../common/COMMON-CLI.md#sql--tds-data-plane-access) for full sqlcmd reference.


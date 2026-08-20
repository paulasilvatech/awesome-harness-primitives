# Consumption CLI Quick Reference

Concise MCP `fabric-sqlendpoint-execute_query` patterns, monitoring queries, and agent tips. For full T-SQL patterns, see [SQLDW-CONSUMPTION-CORE.md](../../../../common/SQLDW-CONSUMPTION-CORE.md). For workflow templates, see [script-templates.md](script-templates.md).

> **Note:** All T-SQL execution uses the `fabric-sqlendpoint-execute_query` MCP tool. See [consumption.md § Tool Stack](../consumption.md#tool-stack) for tool signature and limits.

## Query Patterns

### Single Query

```text
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SET NOCOUNT ON; SELECT * FROM dbo.FactSales WHERE SaleDate >= '2025-01-01'")
```

### Multi-Statement (Single Batch)

Multiple statements can be combined in a single batch (no `GO` required):

```text
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SET NOCOUNT ON;
SELECT COUNT(*) AS TotalRows FROM dbo.FactSales;
")
```

> **Note:** If you need multiple result sets, use separate `fabric-sqlendpoint-execute_query` calls. The MCP tool returns only the last result set in a multi-statement batch.

### Parameterized Date Ranges

Use string interpolation in the query text (no sqlcmd variables):

```text
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SET NOCOUNT ON;
SELECT * FROM dbo.FactSales
WHERE SaleDate BETWEEN '2025-01-01' AND '2025-06-30'
ORDER BY SaleDate
")
```

### Large Result Handling

The MCP tool caps at ~10,000 rows (an observed default, not a documented contract — verify against live truncation). For large datasets:

```text
-- Step 1: Check total count
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT COUNT(*) AS total FROM dbo.FactSales WHERE SaleDate >= '2025-01-01'")

-- Step 2: Page through if needed (using OFFSET/FETCH). List only the columns you
-- need -- narrow selects reduce the chance of hitting the ~10,000-row/payload cap.
fabric-sqlendpoint-execute_query(workspaceId, itemId, "
SELECT SaleID, SaleDate, ProductKey, CustomerKey, Quantity, Amount FROM dbo.FactSales
WHERE SaleDate >= '2025-01-01'
ORDER BY SaleID
OFFSET 0 ROWS FETCH NEXT 10000 ROWS ONLY
")
```

## Monitoring and Performance

For full query catalog see [SQLDW-CONSUMPTION-CORE.md § Monitoring and Diagnostics](../../../../common/SQLDW-CONSUMPTION-CORE.md#monitoring-and-diagnostics) and [script-templates.md § Performance Investigation](script-templates.md#performance-investigation-workflow).

```text
# Active queries
fabric-sqlendpoint-execute_query(workspaceId, itemId, "SELECT request_id, session_id, command, status, total_elapsed_time/1000 AS elapsed_sec FROM sys.dm_exec_requests WHERE status='running' ORDER BY total_elapsed_time DESC")
```

> Session termination (`KILL`) is an operational/admin action outside this read-only skill's scope.

## Script Generation

When the user asks for a reusable script (not an agent workflow), you can generate a standalone bash/PowerShell script. Use `az rest` for control-plane discovery (workspace/item IDs); for T-SQL execution outside an agent, use the **Legacy CLI Fallback** (`sqlcmd`) documented in [script-templates.md § Legacy CLI Fallback](script-templates.md#legacy-cli-fallback). Note: `curl` only covers OneLake file access — it cannot execute T-SQL against a SQL endpoint. For agent workflows, see [script-templates.md](script-templates.md).

## Agent Integration Notes

- **All AI agents**: Use the `fabric-sqlendpoint-execute_query` MCP tool directly. No shell commands needed for SQL execution.
- **GitHub Copilot CLI / VS Code**: The MCP tool appears in the tool list automatically when the server is registered.
- **Claude Code / Cowork / Cursor / Windsurf**: Verify `fabric-sqlendpoint-execute_query` is in the available tools before proceeding.
- **Rate limiting**: Space out calls if running multi-step investigations (max 20 req/min per identity).
- **Workspace/item discovery**: Use `az rest` for control-plane operations (finding workspace ID, item ID).


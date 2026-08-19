# Authoring CLI Quick Reference

Concise `fabric-sqlendpoint-execute_query` MCP tool patterns for DDL, DML, data ingestion, monitoring, and agent tips. For full T-SQL patterns, see [SQLDW-AUTHORING-CORE.md](../../../../common/SQLDW-AUTHORING-CORE.md). For workflow templates, see [authoring-script-templates.md](authoring-script-templates.md).

## Query Execution

All T-SQL operations use the `fabric-sqlendpoint-execute_query` MCP tool:

```text
fabric-sqlendpoint-execute_query(workspaceId, itemId, query)
```

- **workspaceId**: Workspace GUID (discover via `az rest`)
- **itemId**: Warehouse item GUID, or a Lakehouse's **SQL analytics endpoint** id (`properties.sqlEndpointProperties.id`, **not** the lakehouse item id) — discover via `az rest`
- **query**: Single T-SQL batch (no `GO` separators, no sqlcmd meta-commands)
- **Returns**: CSV results (RFC 4180) + metadata text

### Key Constraints

- **No `GO` separators** — each call is one batch. For multi-batch workflows, call `fabric-sqlendpoint-execute_query` multiple times.
- **10,000 row max** — use `TOP N` or `WHERE` to limit results.
- **300s timeout** — break very long operations into steps.
- **20 req/min** — consolidate related statements into one batch where possible.
- **Only last result set** — if a batch has multiple SELECTs, only the final one is returned.
- _Limit values (10,000 rows / 300s / 20 req/min) are observed defaults, not a documented contract — verify against live 429/timeout/truncation responses._

## Core Authoring via MCP

### Table DDL

```text
# CREATE TABLE
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE TABLE dbo.FactSales (
      SaleID bigint NOT NULL,
      ProductID int NOT NULL,
      SaleDate date NOT NULL,
      Amount decimal(19,4) NOT NULL
  )")

# Verify
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT table_schema, table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_name = 'FactSales'")

# CTAS with explicit types (preferred for populated tables)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE TABLE dbo.FactSales_2024 AS
   SELECT SaleID, CAST(Amount AS decimal(19,2)) AS Amount
   FROM dbo.FactSales WHERE SaleDate >= '2024-01-01'")

# ALTER TABLE — add column
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "ALTER TABLE dbo.FactSales ADD Region varchar(50) NULL")

# DROP TABLE
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "DROP TABLE IF EXISTS dbo.StagingTable")
```

### DML

```text
# INSERT...SELECT (preferred for bulk)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "INSERT INTO dbo.FactSales (SaleID, ProductID, SaleDate, Amount)
   SELECT SaleID, ProductID, SaleDate, Amount
   FROM dbo.StagingTable WHERE IsValid = 1")

# Upsert (production-safe: DELETE + INSERT in a TRY/CATCH transaction)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "BEGIN TRY
     BEGIN TRANSACTION;
     DELETE FROM dbo.FactSales WHERE SaleDate = '2025-06-15';
     INSERT INTO dbo.FactSales (SaleID, ProductID, SaleDate, Amount)
     SELECT SaleID, ProductID, SaleDate, Amount FROM dbo.StagingTable WHERE SaleDate = '2025-06-15';
     COMMIT TRANSACTION;
   END TRY
   BEGIN CATCH
     IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
     THROW;
   END CATCH")

# TRUNCATE (fast, preserves history — use instead of DELETE FROM)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "TRUNCATE TABLE dbo.StagingTable")
```

### Data Ingestion

```text
# Parquet from ADLS Gen2 (uses caller's Entra ID credentials)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "COPY INTO dbo.FactSales
   FROM 'https://storageacct.dfs.core.windows.net/container/sales/*.parquet'
   WITH (FILE_TYPE = 'PARQUET')")

# CSV with options
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "COPY INTO dbo.FactSales
   FROM 'https://storageacct.dfs.core.windows.net/container/sales/*.csv'
   WITH (FILE_TYPE = 'CSV', FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = '\n')")

# OPENROWSET + CTAS (transform-on-ingest)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE TABLE dbo.CleanData AS
   SELECT id, UPPER(country) AS Country, CAST(amount AS decimal(19,4)) AS Amount
   FROM OPENROWSET(BULK 'https://storageacct.dfs.core.windows.net/container/raw/*.parquet') AS raw
   WHERE amount > 0")
```

## Advanced Authoring Patterns via MCP

### Transactions

Transactions work within a single `fabric-sqlendpoint-execute_query` batch (no `GO` needed):

```text
# Simple transaction — all in one batch
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "BEGIN TRANSACTION;
   INSERT INTO dbo.FactSales SELECT * FROM dbo.StagingTable WHERE IsValid = 1;
   DELETE FROM dbo.StagingTable WHERE IsValid = 1;
   COMMIT TRANSACTION;")

# Transaction with TRY/CATCH
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "BEGIN TRY
       BEGIN TRANSACTION;
       INSERT INTO dbo.FactSales SELECT * FROM dbo.StagingTable WHERE IsValid = 1;
       DELETE FROM dbo.StagingTable WHERE IsValid = 1;
       COMMIT TRANSACTION;
   END TRY
   BEGIN CATCH
       IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
       THROW;
   END CATCH;")
```

### Schema Evolution

```text
# Add nullable column (fast metadata op)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "ALTER TABLE dbo.FactSales ADD Region varchar(50) NULL")

# Drop column (April 2025+)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "ALTER TABLE dbo.FactSales DROP COLUMN Region")

# Change column type (CTAS + rename — robust; ALTER COLUMN is preview)
# Step 1: Create new table with correct type
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE TABLE dbo.FactSales_New AS SELECT SaleID, ProductID, SaleDate, CAST(Amount AS decimal(19,2)) AS Amount FROM dbo.FactSales")

# Step 2: Rename tables
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "EXEC sp_rename 'dbo.FactSales', 'FactSales_Old'")
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "EXEC sp_rename 'dbo.FactSales_New', 'FactSales'")
```

> **Warning**: CTAS + rename loses time-travel history and security. Re-apply GRANT/DENY after swap.

### Stored Procedures

```text
# Create procedure (single batch, no GO needed)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE OR ALTER PROCEDURE dbo.sp_LoadFactSales @BatchDate date
   AS
   BEGIN
       SET NOCOUNT ON;
       DELETE FROM dbo.FactSales WHERE SaleDate = @BatchDate;
       INSERT INTO dbo.FactSales (SaleID, ProductID, SaleDate, Amount)
       SELECT SaleID, ProductID, SaleDate, Amount
       FROM dbo.StagingTable WHERE SaleDate = @BatchDate;
   END")

# Execute procedure
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "EXEC dbo.sp_LoadFactSales @BatchDate = '2025-06-15'")

# Create view on Lakehouse SQLEP (read-only — views/funcs/procs allowed)
# lakehouseSqlEndpointId = lakehouse's properties.sqlEndpointProperties.id (NOT the lakehouse item id)
fabric-sqlendpoint-execute_query(workspaceId, lakehouseSqlEndpointId,
  "CREATE OR ALTER VIEW dbo.vw_ActiveCustomers AS
   SELECT CustomerID, Name, Email FROM dbo.Customers WHERE IsActive = 1")
```

### Time Travel and Recovery

```text
# Query data as it existed at a specific time (UTC)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT TOP 100 * FROM dbo.FactSales
   OPTION (FOR TIMESTAMP AS OF '2025-06-14T23:59:59.999')")

# Recover deleted data via CTAS
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE TABLE dbo.FactSales_Recovered AS
   SELECT * FROM dbo.FactSales
   OPTION (FOR TIMESTAMP AS OF '2025-06-14T23:59:59.999')")
```

## Monitoring Authoring Operations

For full monitoring catalog see [SQLDW-CONSUMPTION-CORE.md § Monitoring and Diagnostics](../../../../common/SQLDW-CONSUMPTION-CORE.md#monitoring-and-diagnostics).

```text
# Active DML/DDL operations
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT request_id, session_id, command, status, total_elapsed_time/1000 AS sec
   FROM sys.dm_exec_requests
   WHERE command IN ('INSERT','UPDATE','DELETE','MERGE','CREATE TABLE','COPY')
   ORDER BY total_elapsed_time DESC")

# Recent ETL queries (last 24h)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT TOP 20 distributed_statement_id, login_name, label, total_elapsed_time_ms
   FROM queryinsights.exec_requests_history
   WHERE start_time >= DATEADD(HOUR,-24,GETUTCDATE()) AND label LIKE 'ETL_%'
   ORDER BY total_elapsed_time_ms DESC")

# Failed writes (last 7d) — detect snapshot conflicts
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT TOP 10 distributed_statement_id, command, start_time, status
   FROM queryinsights.exec_requests_history
   WHERE status='Failed' AND start_time >= DATEADD(DAY,-7,GETUTCDATE())
   ORDER BY start_time DESC")

# Kill a stuck session (Admin role)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "KILL '<distributed_statement_id>'")
```

## Agent Integration Notes

- **GitHub Copilot CLI / MCP-enabled agents**: Call `fabric-sqlendpoint-execute_query(workspaceId, itemId, query)` directly. For COPY INTO, remind user about Storage Blob Data Reader role on the storage account.
- **Multi-batch workflows**: Call `fabric-sqlendpoint-execute_query` once per logical batch. No `GO` separators — each call is one batch.
- **Common agent pattern**:
  1. Discover schema (columns, types) via `fabric-sqlendpoint-execute_query`
  2. Formulate CTAS/DML with explicit CASTs
  3. Execute via `fabric-sqlendpoint-execute_query(workspaceId, itemId, query)`
  4. Verify result (row count, sample) via another `fabric-sqlendpoint-execute_query` call
  5. Report results to user
- **Rate limit awareness**: If performing many sequential operations, space calls ~3s apart to avoid 429 errors. Consolidate multiple statements into one batch when they don't require `GO` between them.

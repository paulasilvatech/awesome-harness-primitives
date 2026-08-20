# Authoring Workflow Templates

MCP `fabric-sqlendpoint-execute_query` workflow templates for common authoring operations. Each template shows the sequence of `fabric-sqlendpoint-execute_query` calls an agent should perform.

**Prerequisites:**
- `fabric-sqlendpoint-execute_query` MCP tool available (verify in tool list)
- `workspaceId` and `itemId` known (discover via `az rest` — see SKILL.md § Connection)

**Placeholders:** The storage URLs (`https://storageacct.dfs.core.windows.net/...`), dates
(`2025-06-15`, `2025-06-01`, etc.), and `LABEL` values (`ETL_Transform_20250615`) below are
**illustrative** — replace them with your own `<storage_path>`, `<YYYY-MM-DD>`, and label values
before running. Recommended `LABEL` convention: `<process>_<step>_<YYYYMMDD>` (e.g. `ETL_Stage_20250615`)
so loads are traceable in `queryinsights` without hardcoding a stale date.

---

## MCP Workflow Templates

### Template 1: COPY INTO Ingestion

```text
# Step 1: Load data from ADLS
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "COPY INTO dbo.StagingData
   FROM 'https://storageacct.dfs.core.windows.net/container/sales/*.parquet'
   WITH (FILE_TYPE = 'PARQUET')")

# Step 2: Verify load
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT COUNT(*) AS row_count FROM dbo.StagingData")
```

**Notes:**
- User must have Storage Blob Data Reader on the ADLS account
- For OneLake paths, ensure workspace identity is provisioned
- COPY INTO is the highest-throughput ingestion method

---

### Template 2: Full ELT Pipeline (Stage → Transform → Load)

```text
# Step 1: Load raw data into staging
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "COPY INTO dbo.Staging_RawSales
   FROM 'https://storageacct.dfs.core.windows.net/container/raw/*.parquet'
   WITH (FILE_TYPE = 'PARQUET')")

# Step 2: Transform and load into fact table
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "INSERT INTO dbo.FactSales (SaleID, ProductID, CustomerID, SaleDate, Amount)
   SELECT SaleID, ProductID, CustomerID,
          CAST(SaleTimestamp AS date) AS SaleDate,
          CAST(RawAmount AS decimal(19,4)) AS Amount
   FROM dbo.Staging_RawSales
   WHERE RawAmount > 0 AND SaleID IS NOT NULL
   OPTION (LABEL = 'ETL_Transform_20250615')")

# Step 3: Clean staging
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "TRUNCATE TABLE dbo.Staging_RawSales")

# Step 4: Verify
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT COUNT(*) AS fact_rows FROM dbo.FactSales")
```

---

### Template 3: Incremental Upsert (DELETE + INSERT with Retry)

```text
# Step 1: Execute transactional upsert
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SET NOCOUNT ON;
   BEGIN TRY
       BEGIN TRANSACTION;
       DELETE FROM dbo.FactSales WHERE SaleDate >= '2025-06-01';
       INSERT INTO dbo.FactSales
       SELECT * FROM SalesLakehouse.dbo.ProcessedSales WHERE SaleDate >= '2025-06-01';
       COMMIT TRANSACTION;
   END TRY
   BEGIN CATCH
       IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
       THROW;
   END CATCH;")

# If step 1 fails with snapshot conflict (error 24556/24706):
# Wait 5-10 seconds and retry. Max 3 attempts.
# Space retries: 5s, 10s, 15s.

# Step 2: Verify
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT COUNT(*) AS updated_rows FROM dbo.FactSales WHERE SaleDate >= '2025-06-01'")
```

**Error handling:**
- Error 24556/24706 (snapshot conflict): Retry with exponential backoff
- HTTP 429 (rate limit): Wait 60s before retry
- Timeout (300s): Break into smaller date ranges

---

### Template 4: Schema Migration (CTAS Workaround)

`ALTER TABLE ... ALTER COLUMN` is in preview; for a robust, GA-only path use CTAS + rename:

```text
# Step 1: Create new table with updated schema
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE TABLE dbo.FactSales_V2 AS
   SELECT SaleID, ProductID, CustomerID, SaleDate,
          CAST(Amount AS decimal(19,2)) AS Amount, Quantity
   FROM dbo.FactSales")

# Step 2: Rename the original out of the way (keeps a rollback copy)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "EXEC sp_rename 'dbo.FactSales', 'FactSales_Old'")

# Step 3: Rename the new table into place
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "EXEC sp_rename 'dbo.FactSales_V2', 'FactSales'")

# Step 4: Re-apply constraints
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "ALTER TABLE dbo.FactSales
   ADD CONSTRAINT PK_FactSales PRIMARY KEY NONCLUSTERED (SaleID) NOT ENFORCED")

# Step 5: Verify
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT column_name, data_type, numeric_precision, numeric_scale
   FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'FactSales' AND column_name = 'Amount'")

# Step 6: Drop the original only after the rename + verification succeed
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "DROP TABLE dbo.FactSales_Old")
```

**WARNING:** CTAS + rename loses time-travel history and security. Re-apply GRANT/DENY after swap.

---

### Template 5: Time Travel Recovery

```text
# Step 1: Preview data at point in time
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT TOP 10 * FROM dbo.FactSales
   OPTION (FOR TIMESTAMP AS OF '2025-06-14T23:59:59.999')")

# Step 2: Create recovery table
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE TABLE dbo.FactSales_Recovered AS
   SELECT * FROM dbo.FactSales
   OPTION (FOR TIMESTAMP AS OF '2025-06-14T23:59:59.999')")

# Step 3: Count recovered rows
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT COUNT(*) AS recovered_rows FROM dbo.FactSales_Recovered")

# Step 4: Merge back missing rows (adjust PK column as needed)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "INSERT INTO dbo.FactSales
   SELECT r.* FROM dbo.FactSales_Recovered r
   WHERE NOT EXISTS (SELECT 1 FROM dbo.FactSales t WHERE t.SaleID = r.SaleID)")

# Step 5: Cleanup
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "DROP TABLE dbo.FactSales_Recovered")
```

---

### Template 6: Create Stored Procedure

```text
# Step 1: Create/update procedure (single batch, no GO)
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "CREATE OR ALTER PROCEDURE dbo.sp_IncrementalLoad
       @CutoffDate date
   AS
   BEGIN
       SET NOCOUNT ON;
       BEGIN TRY
           BEGIN TRANSACTION;
           DELETE FROM dbo.FactSales WHERE SaleDate >= @CutoffDate;
           INSERT INTO dbo.FactSales
           SELECT * FROM SalesLakehouse.dbo.ProcessedSales WHERE SaleDate >= @CutoffDate;
           COMMIT TRANSACTION;
       END TRY
       BEGIN CATCH
           IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
           THROW;
       END CATCH;
   END")

# Step 2: Verify creation
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "SELECT name, type_desc, create_date, modify_date FROM sys.procedures WHERE name = 'sp_IncrementalLoad'")

# Step 3: Execute
fabric-sqlendpoint-execute_query(workspaceId, itemId,
  "EXEC dbo.sp_IncrementalLoad @CutoffDate = '2025-06-01'")
```

---

## Legacy CLI Fallback

If the `fabric-sqlendpoint-execute_query` MCP tool is unavailable (e.g., MCP server not registered), fall back to sqlcmd:

```bash
# Install: winget install sqlcmd (Windows) / brew install sqlcmd (macOS)
# Auth: az login
# Connect: sqlcmd -S "<endpoint>.datawarehouse.fabric.microsoft.com" -d "<DB>" -G -Q "<sql>"
```

For the full CLI patterns, refer to [COMMON-CLI.md](../../../../common/COMMON-CLI.md).


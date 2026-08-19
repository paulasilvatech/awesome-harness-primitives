# SQLDB-AUTHORING-CORE.md

> **Scope**: Authoring T-SQL patterns — database lifecycle, DDL, DML, vector columns, SqlPackage deployments, source control, CI/CD, GraphQL API — for **SQL database in Fabric** (based on the Azure SQL Database engine).
> Language-agnostic for application code examples — avoids C# and Python implementation guidance, but may reference Fabric- and SQL-related tooling such as SqlPackage, BCP, and CI/CD workflows where relevant.

---

## SQL Database vs Data Warehouse — Authoring Capability Matrix

> **Relationship to SQLDB-CONSUMPTION-CORE.md**: Read-side topics (SELECT, cross-database queries, vector search, AI/RAG, monitoring, security inspection) live in `SQLDB-CONSUMPTION-CORE.md`. This document covers authoring-exclusive topics: database lifecycle, table DDL, DML, constraints, triggers, vector columns, SqlPackage, source control/CI/CD, GraphQL API, and mirroring considerations.

| Capability | SQL database in Fabric | Fabric Data Warehouse |
|---|---|---|
| Engine | Azure SQL Database engine (row-store, OLTP) | Synapse MPP (columnar, analytics) |
| Database compatibility level | 100–170 (default 170) | N/A |
| Full ACID transactions | ✅ (all isolation levels) | ✅ (snapshot isolation only) |
| Optimized locking | ✅ (reduces lock memory, eliminates lock escalation) | N/A |
| Accelerated Database Recovery (ADR) | ✅ | N/A |
| CREATE TABLE with enforced PK/FK/UNIQUE/CHECK/DEFAULT | ✅ | NOT ENFORCED only |
| Temporal tables (system-versioned) | ✅ | ❌ |
| Triggers (AFTER, INSTEAD OF, DDL) | ✅ | ❌ |
| IDENTITY columns | ✅ | ✅ (preview) |
| Computed columns (persisted + virtual) | ✅ | ❌ |
| Vector data type | ✅ | ❌ |
| Non-clustered indexes | ✅ | ❌ (auto-managed) |
| Clustered columnstore indexes | ✅ (with mirroring caveats) | ✅ (auto) |
| INSERT / UPDATE / DELETE / MERGE | ✅ | ✅ |
| COPY INTO | ❌ | ✅ |
| CTAS (CREATE TABLE AS SELECT) | ❌ | ✅ |
| SELECT INTO | ✅ | ✅ |
| Stored procedures / functions / triggers | ✅ (most Azure SQL surface; no EXECUTE AS) | ✅ (limited; no triggers) |
| sp_invoke_external_rest_endpoint | ✅ | ❌ |
| Native AI functions | ✅ | ❌ |
| External tables (Parquet, CSV) | ✅ | ✅ |
| OPENROWSET BULK (data virtualization) | ✅ (preview — OneLake) | ✅ |
| BCP (Bulk Copy Program) | ✅ | ✅ |
| Views (regular, indexed) | ✅ | ✅ (regular only) |
| SqlPackage (.dacpac/.bacpac) | ✅ | ❌ |
| Microsoft.Build.Sql projects (.sqlproj) | ✅ | ✅ |
| SSDT (Visual Studio) | ✅ (VS 2026+) | ✅ (VS 2026+) |
| Source control (Git integration) | ✅ | ✅ (preview) |
| Deployment pipelines | ✅ | ✅ |
| GraphQL API | ✅ | ❌ |
| Data Factory connectors | ✅ | ✅ |
| Spark connector (read/write) | ✅ (preview — `mssql()`) | ✅ (`synapsesql()`) |
| Copilot (NL-to-SQL, code completion) | ✅ | ✅ |
| Automatic replication to OneLake | ✅ (mirroring) | ✅ (native) |
| CDC (Change Data Capture) | ❌ | ❌ |
| Auto-indexing / Automatic Tuning | ✅ | ❌ |
| Intelligent Query Processing | ✅ (adaptive joins, batch mode, memory grant feedback, parameter sensitivity) | Partial |
| Certificates & database-scoped credentials | ✅ | ✅ |
| Column encryption (ENCRYPTBYKEY/DECRYPTBYKEY) | ✅ | ✅ |
| Always Encrypted (client-side CMK) | ❌ | ❌ |
| Extended events (XEvents) | ✅ (partial) | ✅ (partial) |
| Linked server (as target) | ✅ | ❌ |
| Automatic backups (7-day ZRS) | ✅ | ✅ |
| Point-in-time restore | ✅ | ✅ |

**Summary**: SQL Database offers most of the Azure SQL Database T-SQL surface (OLTP-optimized, row-store, enforced constraints, triggers, temporal tables, vectors, IQP, external tables, AI functions — see [limitations](https://learn.microsoft.com/en-us/fabric/database/sql/limitations) for exceptions). Data Warehouse offers MPP columnar analytics with CTAS/COPY INTO. Choose SQL Database for transactional/operational workloads; choose Data Warehouse for large-scale analytics.


---

## Database Lifecycle

> **Generic item CRUD** (list, get, update metadata, delete) is covered in `COMMON-CORE.md` and `COMMON-CLI.md`. Definition envelope and per-item-type formats (including SQL Database `dacpac`/`sqlproj`) are in `ITEM-DEFINITIONS-CORE.md`. This section covers **SQL-Database-specific** lifecycle operations only.

### Create via REST API

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items
Content-Type: application/json

{
  "displayName": "MyDatabase",
  "type": "SQLDatabase",
  "description": "Operational database for app",
  "creationPayload": {
    "collation": "SQL_Latin1_General_CP1_CI_AS",
    "creationMode": "new"
  }
}
```

- `creationPayload.collation` is optional. Default: `SQL_Latin1_General_CP1_CI_AS`.
- Collation **cannot be changed** after creation. Individual column collations are supported.
- Supported collations include `Latin1_General_100_BIN2_UTF8` and others available in Azure SQL Database.
- `creationPayload.backupRetentionDays` is optional (1–35, default 7). Sets how long automatic backups are retained for point-in-time restore.

**SQL-Database-specific response properties** (returned by `GET .../sqlDatabases` and `GET .../sqlDatabases/{id}`): `connectionString`, `databaseName`, `serverFqdn`, `collation`, `backupRetentionDays`, `earliestRestorePoint`, `latestRestorePoint`.

### Point-in-Time Restore (PITR) from Live Database

Restore a SQL database to any point within its backup retention window by creating a new database with `creationMode: "Restore"`:

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlDatabases
Content-Type: application/json

{
  "displayName": "MyDatabase_Restored",
  "creationPayload": {
    "creationMode": "Restore",
    "sourceDatabaseReference": {
      "referenceType": "ById",
      "itemId": "<sourceSqlDatabaseId>",
      "workspaceId": "<sourceWorkspaceId>"
    },
    "restorePointInTime": "2025-06-15T14:30:00.000Z"
  }
}
```

- `restorePointInTime` must be between the source database's `earliestRestorePoint` and `latestRestorePoint` (check via `GET .../sqlDatabases/{id}`).
- The source database must be in the same tenant. Cross-workspace restore is supported.
- No other creation properties (`collation`, `backupRetentionDays`) are accepted in Restore mode.

**Scope**: `SQLDatabase.ReadWrite.All` or `Item.ReadWrite.All`.

### Delete and Restore

Deleting a SQL database via the generic delete endpoint (`DELETE .../sqlDatabases/{id}`) **soft-deletes** by default. Add `?hardDelete=true` to permanently delete with no recovery.

**Restorable Deleted Databases** (preview) — list soft-deleted databases that can be restored:

```
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlDatabases/restorableDeletedDatabases
```

Response includes `restorableDeletedDatabaseName`, `earliestRestorePoint`, `latestRestorePoint`, and `deletionTimestamp`.

**Restore a deleted database** — create a new database with `creationMode: "RestoreDeletedDatabase"`:

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlDatabases
Content-Type: application/json

{
  "displayName": "MyDatabase_Recovered",
  "creationPayload": {
    "creationMode": "RestoreDeletedDatabase",
    "restorableDeletedDatabaseName": "<name from list above>",
    "restorePointInTime": "2025-06-15T14:30:00.000Z"
  }
}
```

- `restorableDeletedDatabaseName` comes from the list restorable deleted databases response (includes a timestamp suffix, e.g. `"MyDB,134140258788170000"`).
- `restorePointInTime` must be between the deleted database's `earliestRestorePoint` and `latestRestorePoint`.

**Scope**: `SQLDatabase.ReadWrite.All` or `Item.ReadWrite.All`.

---

## Table DDL

### CREATE TABLE

```sql
CREATE TABLE dbo.Orders (
    OrderID       int IDENTITY(1,1) PRIMARY KEY,
    CustomerID    int NOT NULL,
    OrderDate     datetime2(0) NOT NULL DEFAULT GETUTCDATE(),
    TotalAmount   decimal(19,4) NOT NULL CHECK (TotalAmount >= 0),
    Status        varchar(20) NOT NULL DEFAULT 'Pending',
    Notes         nvarchar(max) NULL,
    CONSTRAINT FK_Orders_Customer FOREIGN KEY (CustomerID) REFERENCES dbo.Customers(CustomerID)
);
```

**Column name restrictions**: Cannot contain spaces or these characters: `,` `;` `{` `}` `(` `)` `\n` `\t` `=`.

**Primary key restrictions**: PK columns cannot use `hierarchyid`, `sql_variant`, or `timestamp` data types.

### Indexes

```sql
-- Non-clustered index
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID ON dbo.Orders (CustomerID);

-- Filtered index
CREATE INDEX IX_Orders_Pending ON dbo.Orders (OrderDate) WHERE Status = 'Pending';

-- Clustered columnstore (for analytics-heavy tables)
-- Must be created inline with CREATE TABLE if mirroring is active,
-- OR stop mirroring before adding (table won't be mirrored either way).
CREATE CLUSTERED COLUMNSTORE INDEX CCI_FactEvents ON dbo.FactEvents;
```

**Auto-indexing**: SQL database in Fabric has Automatic Tuning enabled by default. The engine creates, validates, and drops indexes automatically based on workload patterns. Check recommendations via:

```sql
SELECT * FROM sys.dm_db_tuning_recommendations;
```

### ALTER TABLE

```sql
-- Add column
ALTER TABLE dbo.Orders ADD ShippingAddress nvarchar(500) NULL;

-- Add constraint
ALTER TABLE dbo.Orders ADD CONSTRAINT CK_Status 
  CHECK (Status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled'));

-- Drop column
ALTER TABLE dbo.Orders DROP COLUMN Notes;

-- Drop constraint
ALTER TABLE dbo.Orders DROP CONSTRAINT CK_Status;

-- Alter column type
ALTER TABLE dbo.Orders ALTER COLUMN Status varchar(50) NOT NULL;
```

### Vector Columns

```sql
CREATE TABLE dbo.Documents (
    DocID         int IDENTITY(1,1) PRIMARY KEY,
    Title         nvarchar(500) NOT NULL,
    Content       nvarchar(max) NOT NULL,
    Embedding     vector(1536) NULL  -- OpenAI ada-002 dimensions
);

-- Create an approximate vector index (DiskANN) for similarity search.
-- Preview in Azure SQL DB / SQL database in Fabric. A standard relational
-- CREATE INDEX cannot key on a vector column -- use CREATE VECTOR INDEX.
-- Requires the table to have a primary key clustered index and at least
-- 100 rows with non-NULL vectors at creation time.
CREATE VECTOR INDEX IX_Docs_Embedding ON dbo.Documents (Embedding)
    WITH (METRIC = 'cosine', TYPE = 'DiskANN');
```

Vector data type supports dimensions up to 1998. Common embedding sizes:
- OpenAI `text-embedding-ada-002`: 1536
- OpenAI `text-embedding-3-small`: 1536
- OpenAI `text-embedding-3-large`: 3072 (truncate to 1998 or use smaller)

---

## DML Operations

### INSERT

```sql
-- Single row
INSERT INTO dbo.Orders (CustomerID, OrderDate, TotalAmount, Status)
VALUES (1, GETUTCDATE(), 99.95, 'Pending');

-- Multi-row
INSERT INTO dbo.Orders (CustomerID, OrderDate, TotalAmount, Status)
VALUES 
  (1, GETUTCDATE(), 99.95, 'Pending'),
  (2, GETUTCDATE(), 149.00, 'Pending');

-- INSERT ... SELECT
INSERT INTO dbo.OrderArchive (OrderID, CustomerID, OrderDate, TotalAmount)
SELECT OrderID, CustomerID, OrderDate, TotalAmount
FROM dbo.Orders
WHERE OrderDate < DATEADD(YEAR, -1, GETUTCDATE());
```

### UPDATE

```sql
UPDATE dbo.Orders
SET Status = 'Shipped', ShippedDate = GETUTCDATE()
WHERE OrderID = 42;

-- UPDATE with JOIN
UPDATE o
SET o.Status = 'Cancelled'
FROM dbo.Orders o
INNER JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
WHERE c.IsActive = 0;
```

### DELETE

```sql
DELETE FROM dbo.Orders WHERE Status = 'Cancelled' AND OrderDate < '2024-01-01';
```

### MERGE

```sql
MERGE dbo.Customers AS target
USING dbo.StagingCustomers AS source
ON target.CustomerID = source.CustomerID
WHEN MATCHED THEN
    UPDATE SET target.Email = source.Email, target.Name = source.Name
WHEN NOT MATCHED BY TARGET THEN
    INSERT (CustomerID, Name, Email)
    VALUES (source.CustomerID, source.Name, source.Email)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;
```

### Transactions

Full ACID with all standard isolation levels (READ COMMITTED default):

```sql
BEGIN TRANSACTION;
  UPDATE dbo.Inventory SET Quantity = Quantity - 1 WHERE ProductID = 100;
  INSERT INTO dbo.OrderItems (OrderID, ProductID, Quantity) VALUES (42, 100, 1);
COMMIT TRANSACTION;
```

---

## Temporal Tables (System-Versioned)

Temporal tables automatically track full history of data changes — ideal for audit trails, point-in-time analysis, and slowly-changing dimensions.

### Create a Temporal Table

```sql
CREATE TABLE dbo.Products (
    ProductID     int IDENTITY(1,1) PRIMARY KEY,
    ProductName   nvarchar(200) NOT NULL,
    Price         decimal(19,4) NOT NULL,
    Category      nvarchar(100) NOT NULL,
    ValidFrom     datetime2 GENERATED ALWAYS AS ROW START NOT NULL,
    ValidTo       datetime2 GENERATED ALWAYS AS ROW END NOT NULL,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.ProductsHistory));
```

### Convert Existing Table to Temporal

```sql
ALTER TABLE dbo.Products
ADD ValidFrom datetime2 GENERATED ALWAYS AS ROW START NOT NULL DEFAULT SYSUTCDATETIME(),
    ValidTo   datetime2 GENERATED ALWAYS AS ROW END NOT NULL DEFAULT CONVERT(datetime2, '9999-12-31 23:59:59.9999999'),
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo);
ALTER TABLE dbo.Products SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.ProductsHistory));
```

### Query Historical Data

```sql
-- Point-in-time snapshot
SELECT * FROM dbo.Products FOR SYSTEM_TIME AS OF '2025-01-15T10:00:00';

-- All changes in a range
SELECT * FROM dbo.Products FOR SYSTEM_TIME BETWEEN '2025-01-01' AND '2025-02-01';

-- Full history
SELECT * FROM dbo.Products FOR SYSTEM_TIME ALL ORDER BY ValidFrom;
```

---

## Data Virtualization (External Tables and OPENROWSET)

Query and ingest data from OneLake (Lakehouse files) directly in T-SQL without moving data into the database. Supported file formats: **Parquet**, **CSV** (JSON via CSV format with JSON parsing).

### Create External Data Source

```sql
CREATE EXTERNAL DATA SOURCE LakehouseFiles
WITH (
    LOCATION = 'abfss://<workspaceId>@<tenant>.dfs.fabric.microsoft.com/<lakehouseId>/Files/'
);
```

### Query with OPENROWSET (ad-hoc)

```sql
-- Parquet (automatic schema inference)
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'abfss://<workspaceId>@<tenant>.dfs.fabric.microsoft.com/<lakehouseId>/Files/sales/orders.parquet',
    FORMAT = 'parquet'
) AS orders;

-- CSV with explicit schema
SELECT *
FROM OPENROWSET(
    BULK '/customers.csv',
    FORMAT = 'CSV', FIRST_ROW = 2,
    DATA_SOURCE = 'LakehouseFiles'
) WITH (
    CustomerID int, Name nvarchar(200), Email nvarchar(200)
) AS customers;

-- Wildcard / partitioned data
SELECT * FROM OPENROWSET(
    BULK '/sales/year=*/month=*/*.parquet',
    FORMAT = 'parquet',
    DATA_SOURCE = 'LakehouseFiles'
) AS sales WHERE sales.filepath(1) = '2025';
```

### Create External Table (persistent)

```sql
CREATE EXTERNAL FILE FORMAT ParquetFormat WITH (FORMAT_TYPE = PARQUET);

CREATE EXTERNAL TABLE dbo.LakehouseOrders (
    OrderID int, CustomerID int, OrderDate datetime2, Amount decimal(19,4)
) WITH (
    LOCATION = '/sales/orders.parquet',
    DATA_SOURCE = LakehouseFiles,
    FILE_FORMAT = ParquetFormat
);

-- Queryable like a regular table
SELECT * FROM dbo.LakehouseOrders WHERE OrderDate > '2025-01-01';
```

### Ingest from OneLake into Local Table

```sql
INSERT INTO dbo.Orders (OrderID, CustomerID, OrderDate, Amount)
SELECT OrderID, CustomerID, OrderDate, Amount
FROM OPENROWSET(
    BULK '/sales/orders.parquet',
    FORMAT = 'parquet',
    DATA_SOURCE = 'LakehouseFiles'
) AS src;
```

> **OneLake shortcuts** extend data virtualization to external sources (Azure Blob, ADLS Gen2, Amazon S3, Google Cloud Storage, Dataverse, SharePoint) without copying data.

---

## Views and Computed Columns

### Views

```sql
-- Standard view
CREATE OR ALTER VIEW dbo.vw_ActiveOrders AS
SELECT o.OrderID, c.Name AS CustomerName, o.OrderDate, o.TotalAmount
FROM dbo.Orders o
INNER JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
WHERE o.Status = 'Active';

-- Schemabound view (required for indexed views)
CREATE VIEW dbo.vw_OrderSummary WITH SCHEMABINDING AS
SELECT c.CustomerID, c.Name, COUNT_BIG(*) AS OrderCount, SUM(o.TotalAmount) AS TotalSpend
FROM dbo.Orders o INNER JOIN dbo.Customers c ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerID, c.Name;

-- Indexed (materialized) view
CREATE UNIQUE CLUSTERED INDEX IX_OrderSummary ON dbo.vw_OrderSummary (CustomerID);
```

### Computed Columns

```sql
CREATE TABLE dbo.OrderItems (
    ItemID       int IDENTITY(1,1) PRIMARY KEY,
    Quantity     int NOT NULL,
    UnitPrice    decimal(19,4) NOT NULL,
    Discount     decimal(5,2) NOT NULL DEFAULT 0,
    -- Virtual computed column (calculated at query time)
    LineTotal    AS (Quantity * UnitPrice * (1 - Discount)),
    -- Persisted computed column (stored physically, indexable)
    LineTotalPersisted AS (Quantity * UnitPrice * (1 - Discount)) PERSISTED
);
```

---

## Bulk Copy Program (BCP)

BCP is a command-line tool for high-performance bulk data import/export.

```bash
# Export to CSV
bcp "SELECT * FROM dbo.Orders" queryout orders.csv -S "<endpoint>" -d "<db>" -G -c -t","

# Import from CSV
bcp dbo.Orders in orders.csv -S "<endpoint>" -d "<db>" -G -c -t"," -F2

# Export a table
bcp dbo.Orders out orders.dat -S "<endpoint>" -d "<db>" -G -n
```

> BCP uses `-G` for Entra authentication (same as sqlcmd). For service principals, use `-U <appId>` with `BCPPASSWORD` env var.

### Ingestion Method Comparison

| Method | Best For | Throughput | Transforms | Source |
|---|---|---|---|---|
| BCP | Bulk import/export (CSV, native) | High | No | Local files |
| `INSERT ... SELECT` | Small-to-medium loads from local tables | Medium | Yes (T-SQL) | Local tables |
| OPENROWSET + INSERT | Load with transformations from OneLake | Medium | Yes (T-SQL) | Parquet, CSV in OneLake |
| SqlPackage Import (.bacpac) | Full database restore (schema + data) | Medium | No | .bacpac file |
| Data Factory pipelines | Scheduled, multi-source ETL | Varies | Yes | 100+ connectors |
| Dataflows Gen2 | Low-code transformations | Varies | Yes (Power Query) | Multiple sources |
| Spark connector (preview) | Large-scale read/write from Spark notebooks | High | Yes (PySpark/Scala) | DataFrames, any Spark source |

---

## Stored Procedures, Functions, Triggers

### Stored Procedures

```sql
CREATE OR ALTER PROCEDURE dbo.usp_PlaceOrder
    @CustomerID int,
    @ProductID int,
    @Quantity int
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        INSERT INTO dbo.Orders (CustomerID, OrderDate, TotalAmount, Status)
        VALUES (@CustomerID, GETUTCDATE(), 0, 'Pending');
        
        DECLARE @OrderID int = SCOPE_IDENTITY();
        
        UPDATE dbo.Inventory SET Quantity = Quantity - @Quantity
        WHERE ProductID = @ProductID;
        
        COMMIT TRANSACTION;
        SELECT @OrderID AS NewOrderID;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
```

### sp_invoke_external_rest_endpoint

Call Azure OpenAI or other external REST APIs directly from T-SQL:

```sql
DECLARE @url nvarchar(4000) = 'https://<aoai-resource>.openai.azure.com/openai/deployments/<model>/embeddings?api-version=2024-02-01';
DECLARE @payload nvarchar(max) = '{"input": "search text here"}';

DECLARE @response nvarchar(max);
DECLARE @retval int;

EXEC @retval = sp_invoke_external_rest_endpoint
    @url = @url,
    @method = 'POST',
    @payload = @payload,
    @credential = [https://<aoai-resource>.openai.azure.com/],
    @response = @response OUTPUT;
```

Requires a database-scoped credential for the target endpoint.

### Native AI Functions

SQL Database in Fabric supports the native `AI_GENERATE_EMBEDDINGS` T-SQL function. It wraps the embedding-model call so you don't hand-build the `sp_invoke_external_rest_endpoint` request/response JSON, but it is **not** credential-free: it requires a one-time `EXTERNAL MODEL` of type `EMBEDDINGS` backed by a database-scoped credential (the `external rest endpoint enabled` option is on by default in Fabric). The `USE MODEL <model>` clause is mandatory.

```sql
-- One-time setup: register the embedding model (backed by a database-scoped credential)
CREATE EXTERNAL MODEL MyEmbeddingModel
WITH (
    LOCATION   = 'https://<aoai-resource>.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15',
    API_FORMAT = 'Azure OpenAI',
    MODEL_TYPE = EMBEDDINGS,
    MODEL      = 'text-embedding-ada-002',
    CREDENTIAL = [https://<aoai-resource>.openai.azure.com/]
);

-- Generate embeddings directly in a query (USE MODEL is required)
SELECT AI_GENERATE_EMBEDDINGS(Title USE MODEL MyEmbeddingModel) AS embedding
FROM dbo.Documents;

-- Use in an UPDATE to populate a vector column
UPDATE dbo.Documents
SET Embedding = AI_GENERATE_EMBEDDINGS(Content USE MODEL MyEmbeddingModel)
WHERE Embedding IS NULL;
```

> `AI_GENERATE_EMBEDDINGS` removes the manual JSON request/response handling of `sp_invoke_external_rest_endpoint`, but still needs the `EXTERNAL MODEL` + database-scoped credential prerequisite above.

### Database-Scoped Credentials

Required for sp_invoke_external_rest_endpoint, external data sources, and other external connectivity:

```sql
-- Create credential for Azure OpenAI
CREATE DATABASE SCOPED CREDENTIAL [https://<aoai-resource>.openai.azure.com/]
WITH IDENTITY = 'HTTPEndpointHeaders', SECRET = '{"Authorization": "Bearer <token>"}';

-- Create credential using Managed Identity
CREATE DATABASE SCOPED CREDENTIAL ManagedIdentityCredential
WITH IDENTITY = 'Managed Identity';
```

### Triggers

```sql
CREATE TRIGGER dbo.trg_Orders_Audit
ON dbo.Orders
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO dbo.OrderAudit (OrderID, Action, AuditDate)
    SELECT OrderID, 'INSERT', GETUTCDATE() FROM inserted
    UNION ALL
    SELECT OrderID, 'DELETE', GETUTCDATE() FROM deleted WHERE OrderID NOT IN (SELECT OrderID FROM inserted);
END;
```

---

## SqlPackage Workflows

SqlPackage is the primary tool for portable, repeatable database deployments.

### Prerequisites

- .NET 8 SDK
- Install: `dotnet tool install --global Microsoft.SqlPackage`

### Extract (.dacpac — schema only)

```
sqlpackage /Action:Extract \
  /TargetFile:"MyDatabase.dacpac" \
  /SourceConnectionString:"Server=<endpoint>;Initial Catalog=<db>;Authentication=Active Directory Default;Encrypt=Yes"
```

### Publish (.dacpac — incremental deploy)

```
sqlpackage /Action:Publish \
  /SourceFile:"MyDatabase.dacpac" \
  /TargetConnectionString:"Server=<endpoint>;Initial Catalog=<db>;Authentication=Active Directory Default;Encrypt=Yes"
```

Publish compares the .dacpac to the live database and applies incremental changes (new columns, altered procedures, etc.).

### Export (.bacpac — schema + data)

```
sqlpackage /Action:Export \
  /TargetFile:"MyDatabase.bacpac" \
  /SourceConnectionString:"Server=<endpoint>;Initial Catalog=<db>;Authentication=Active Directory Default;Encrypt=Yes"
```

### Import (.bacpac — restore schema + data)

```
sqlpackage /Action:Import \
  /SourceFile:"MyDatabase.bacpac" \
  /TargetConnectionString:"Server=<endpoint>;Initial Catalog=<db>;Authentication=Active Directory Default;Encrypt=Yes"
```

**Portability**: .bacpac files can migrate between SQL database in Fabric, Azure SQL Database, Azure SQL Managed Instance, and SQL Server.

---

## Source Control and CI/CD

### Git Integration

SQL Database in Fabric supports source control via Azure DevOps or GitHub:

- **Commit**: Serializes live database object definitions into the connected repository.
- **Update**: Applies differential changes from the repository to the database (builds `.dacpac`, then runs SqlPackage publish).
- Object definitions are stored as individual `.sql` files per schema/object.

| Action | Fabric Portal | CLI / REST API |
|---|---|---|
| Connect workspace to repo | Workspace Settings → Git | Fabric REST API |
| Commit database to source control | Source control panel → Commit | — |
| Update database from source control | Source control panel → Update | — |
| Edit schema offline & push | — | `git push` |
| Build/validate `.dacpac` | — | `dotnet build` |
| Schema compare & incremental publish | — | SqlPackage CLI |

**Repository structure** (auto-generated on commit):

```
<DatabaseName>.SQLDatabase/
├── <DatabaseName>.sqlproj          # auto-managed — avoid manual edits
├── .sharedqueries/                 # saved queries + pre/post-deployment scripts
├── dbo/
│   ├── Tables/Orders.sql
│   ├── Views/vw_ActiveOrders.sql
│   ├── StoredProcedures/usp_PlaceOrder.sql
│   └── Functions/fn_FullName.sql
```

> **Important**: The `.sqlproj` file is auto-generated by Fabric. Avoid manual edits — they are overwritten on next commit from Fabric.

### Deployment Pipelines

Promote database schema across environments (Dev → Test → Prod). Schema only — no data.

| Action | Fabric Portal | CLI / REST API |
|---|---|---|
| Create pipeline & assign stages | Pipeline UI | Fabric REST API |
| Deploy between stages | Deploy button | `POST .../pipelines/{id}/deploy` |
| SqlPackage publish (direct) | — | `sqlpackage /Action:Publish` |

### SQL Database Projects

Develop and validate schema offline using SQL Database Projects (`.sqlproj`). Build `.dacpac` with `dotnet build`, deploy with `sqlpackage /Action:Publish`. Also available as built-in features in VS Code (SQL Database Projects extension) and SSMS (Solution Explorer).

---

## GraphQL API

Create a GraphQL API to expose SQL Database data:

### Via Fabric Portal

1. Open your SQL database in Fabric portal.
2. Select **New API for GraphQL** from the ribbon.
3. Name the API, select tables to expose.
4. Choose authentication: SSO (per-user permissions) or Saved Credentials (shared).

### Via REST API

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items
Content-Type: application/json

{
  "displayName": "MyGraphQLAPI",
  "type": "GraphQLApi",
  "definition": {
    "parts": [{
      "path": "schema.graphql",
      "payload": "<base64-encoded-schema>"
    }]
  }
}
```

**Authentication considerations**:
- **SSO**: Users need Execute on API + permissions on underlying data source. Autobinding works in deployment pipelines.
- **Saved credentials**: Users only need API access. Does NOT autobind in deployment pipelines.

---

## Mirroring Considerations

SQL Database data is **automatically replicated** to OneLake in Parquet format:

- Creates a SQL analytics endpoint for read-only analytical queries.
- Near real-time replication (not instantaneous).
- Clustered columnstore indexes must be created at table creation time, or mirroring must be stopped first.
- Security policies (RLS, CLS, DDM) configured on the SQL database do **not** automatically apply to the SQL analytics endpoint — must be re-configured separately.

### Tables That Cannot Be Mirrored

| Condition | Workaround |
|---|---|
| Clustered columnstore index (CCI) on existing table | Stop mirroring → create CCI → restart mirroring. Table still won't mirror after CCI. |
| CCI created inline with `CREATE TABLE` | Table created but not mirrored |
| `vector` or `json` columns | Cannot mirror; cannot `ALTER` column to these types. Query via OLTP endpoint. |
| Temporal history tables | History excluded; data table mirrors normally |
| Graph / External tables | Table created but not mirrored |
| Tables beyond 1000 per database | Skipped from mirroring |
| PK of type `datetime2(7)`, `datetimeoffset(7)`, `time(7)` | Table cannot be mirrored (Delta precision limit) |

### Columns Skipped or Truncated During Mirroring

- **Skipped entirely**: computed columns; `image`, `text`, `ntext`, `xml`, `rowversion`/`timestamp`, `sql_variant`, UDT, `geometry`, `geography`, `hierarchyid`, `vector`, `json`.
- **Truncated**: LOB columns > 1 MB are truncated to 1 MB in OneLake.
- **Precision loss**: `datetime2(7)` 7th fractional digit trimmed; `datetimeoffset(7)` time zone and 7th decimal lost.

### Objects Not Mirrored

Views, stored procedures, functions, triggers — only base tables are mirrored.

### Security NOT Propagated to OneLake

RLS, object-level permissions (column grants), DDM, and Purview sensitivity labels are NOT replicated. Anyone with access to the SQL analytics endpoint sees full unfiltered, unmasked data.

### DDL Restrictions While Mirroring Is Active

| Operation | Status |
|---|---|
| `ALTER INDEX ALL` on a table | Blocked — alter individual indexes by name |
| `ALTER PRIMARY KEY` | Blocked |
| DDL change on mirrored table | Triggers full data reseed for that table |

### Mirroring / Replication

Replication of a Fabric SQL database to its SQL analytics endpoint (OneLake Delta tables) is **automatic and managed by the platform** — there is no start/stop mirroring REST operation on the SQLDatabase item. The [SQLDatabase Items REST surface](https://learn.microsoft.com/en-us/rest/api/fabric/sqldatabase/items) exposes only Create / Delete / Get / Get Definition / List / List Restorable Deleted Databases / Revalidate CMK / Update / Update Definition. (Manual start/stop mirroring verbs exist for the separate **MirroredDatabase** item type, not for SQL database in Fabric.)

> **Sources**: [Mirroring limitations](https://learn.microsoft.com/en-us/fabric/database/sql/mirroring-limitations), [SQL database limitations](https://learn.microsoft.com/en-us/fabric/database/sql/limitations).

---

## Limitations Reference

> **Sources**: [SQL database limitations](https://learn.microsoft.com/en-us/fabric/database/sql/limitations), [Mirroring limitations](https://learn.microsoft.com/en-us/fabric/database/sql/mirroring-limitations).

### Database / Table / Column Limits

| Scope | Limitation |
|---|---|
| Database names | Cannot contain `! [ ] < > * % & : / ? # = @ ^ " ' ; ( )` |
| Database name reuse | Deleted names cannot be reused in the same workspace |
| Collation | Set at creation only; cannot be changed afterwards |
| `ALTER DATABASE SET` | All options currently preview |
| TDE | Not supported (storage-level encryption with service-managed keys is used) |
| PK data types | Cannot be `hierarchyid`, `sql_variant`, `timestamp` |
| In-memory / Ledger / Always Encrypted tables | Not supported |
| Partition SWITCH / SPLIT / MERGE | Not supported |
| Partition compression (`DATA_COMPRESSION = ROW\|PAGE`) via `ALTER TABLE REBUILD` | Not supported |
| Column names | Cannot contain spaces, `, ; { } ( ) \n \t =` |

### Resource Limits

| Resource | Limit |
|---|---|
| Compute | Up to 32 vCores |
| Storage | Up to 4 TB |
| Tempdb | Up to 1024 GB |
| Log write throughput | Up to 50 MB/s |
| Databases per workspace | 150 |
| Backups | ZRS automatic, 7-day retention |
| Trial capacity | Max 3 databases |

### Connection Limits

| Limitation | Detail |
|---|---|
| Connection policy | `Default` only (cannot be changed) |
| Auth | Microsoft Entra ID only — no SQL auth, no `CREATE LOGIN` |
| Ports | 1433 (gateway) + 11000–11999 (redirect range) must be open outbound |
| MARS | Not supported |

### Unsupported Features (vs Azure SQL Database)

| Feature | Status in SQL database in Fabric |
|---|---|
| `EXECUTE AS` | Not supported |
| CDC (Change Data Capture) | Not supported |
| Always Encrypted | Not supported |
| Ledger tables | Not supported |
| In-memory tables | Not supported |
| Application roles | Not supported |
| Server-level roles | Not supported |
| Elastic queries / elastic jobs | Not supported |
| Linked servers | Target only (not source) |
| Service Broker | Not supported |
| Distributed transactions (MS DTC) | Not supported |
| SQL Server Agent | Not supported — use Data Factory pipelines or Airflow |
| `BACKUP` command | Automatic backups only (7-day ZRS) |
| Trace flags | Not supported |
| SQL Server Auditing | Not supported (Fabric auditing IS available — see Auditing Configuration) |
| Database watcher | Not currently supported |
| VNet service endpoints / global peering | Not supported |
| Azure CLI / Azure PowerShell for management | Not supported — use Fabric REST API via `az rest` |
| Full-text search (`CONTAINS`/`FREETEXT`) | Preview only; third-party filters and word breakers not supported |
| Time zone choice | Not supported |
| Customer-managed keys (data plane) | Not supported (CMK at item creation supported via REST) |

### Source Control / CI-CD Limits

| Limitation | Detail |
|---|---|
| `.sqlproj` file changes | Not persisted — source control integration resets the file on next commit |
| Database-level settings | Not included in source control (collation, compat level). Must be scripted post-deploy. |

### Server-Scoped DMVs Not Available

`sys.dm_os_ring_buffers`, `sys.dm_os_schedulers`, `sys.configurations`, and other instance-level DMVs are not exposed. Use database-scoped DMVs (`sys.dm_db_resource_stats`, Query Store views) for diagnostics.

---

## T-SQL Anti-Patterns

When writing or reviewing T-SQL for SQL database in Fabric, check for and fix these patterns.

### Non-SARGable Expressions

Avoid functions on columns in `WHERE`, `JOIN ON`, or `HAVING` clauses. Isolate the column on the left side.

```sql
-- Bad: function on column prevents index seek
WHERE YEAR(OrderDate) = 2025

-- Good: half-open range allows index seek
WHERE OrderDate >= '2025-01-01' AND OrderDate < '2026-01-01'

-- Bad: ISNULL wrapping
WHERE ISNULL(Status, 'Unknown') = 'Active'

-- Good: explicit NULL handling
WHERE Status = 'Active'

-- Bad: UPPER/LOWER on column (if collation is already CI)
WHERE UPPER(CustomerName) = 'CONTOSO'

-- Good: direct comparison (CI collation handles case)
WHERE CustomerName = 'Contoso'
```

### Implicit Conversions

Match variable and parameter data types explicitly to avoid `CONVERT_IMPLICIT` in execution plans.

```sql
-- Bad: varchar parameter against nvarchar column causes implicit conversion
DECLARE @id VARCHAR(50) = '12345';
SELECT * FROM dbo.Orders WHERE OrderRef = @id;  -- OrderRef is nvarchar

-- Good: match types
DECLARE @id NVARCHAR(50) = N'12345';
SELECT * FROM dbo.Orders WHERE OrderRef = @id;
```

### SELECT *

Replace with explicit column names. Reduces IO, avoids breaking changes, and enables covering index usage.

### Cursor Elimination

Replace cursors with set-based operations, JOINs, or window functions. Acceptable cursor uses: DDL per object, external side effects per row, or genuinely procedural logic.

```sql
-- Bad: cursor loop for updates
DECLARE cur CURSOR FOR SELECT OrderID, Amount FROM dbo.Orders;
-- ... FETCH, UPDATE one row at a time

-- Good: set-based update
UPDATE dbo.Orders SET Tax = Amount * 0.1 WHERE Tax IS NULL;
```

### Correlated Subqueries → CTEs

Replace correlated subqueries (execute per row) with CTEs joined back to the main query.

```sql
-- Bad: correlated subquery runs per row
SELECT o.OrderID,
    (SELECT COUNT(*) FROM dbo.OrderItems i WHERE i.OrderID = o.OrderID) AS ItemCount
FROM dbo.Orders o;

-- Good: CTE with JOIN
;WITH ItemCounts AS (
    SELECT OrderID, COUNT(*) AS ItemCount FROM dbo.OrderItems GROUP BY OrderID
)
SELECT o.OrderID, ISNULL(ic.ItemCount, 0) AS ItemCount
FROM dbo.Orders o
LEFT JOIN ItemCounts ic ON o.OrderID = ic.OrderID;
```

### Batch Small Transactions (Log IO Pressure)

Replace single-row INSERT/UPDATE/DELETE loops with set-based operations. For large sets, use chunked batches:

```sql
-- Chunked delete to avoid lock escalation and log growth
DECLARE @BatchSize INT = 5000;
WHILE 1 = 1
BEGIN
    DELETE TOP (@BatchSize) FROM dbo.AuditLog WHERE LogDate < DATEADD(YEAR, -1, GETDATE());
    IF @@ROWCOUNT < @BatchSize BREAK;
END
```

### LIKE Wildcard Misuse

- Leading wildcard (`'%way'`) → not indexable; use `RIGHT(col, N)` if possible
- Both sides (`'%way%'`) → consider `CHARINDEX` for efficiency
- Trailing wildcard (`'way%'`) → indexable, fine to use

### SQL Injection in Dynamic SQL

Use `sp_executesql` with parameters instead of string concatenation:

```sql
-- Bad
EXEC('SELECT * FROM ' + @tableName);

-- Good
DECLARE @sql NVARCHAR(MAX) = N'SELECT * FROM ' + QUOTENAME(@tableName);
EXEC sp_executesql @sql;
```

---

## Schema Design Guidance

> For computed columns (virtual vs persisted), see [Views and Computed Columns](#views-and-computed-columns). For auto-indexing recommendations, see `sys.dm_db_tuning_recommendations` in SQLDB-CONSUMPTION-CORE.md § Performance and Monitoring.

### Index Strategy

SQL database in Fabric has auto-tuning that creates/drops indexes automatically. Before manually creating indexes, let auto-tuning run for representative workloads first. Only create indexes manually for patterns auto-tuning doesn't catch.

### Naming Conventions

- Use `schema.object` notation consistently (`dbo.Orders`, not just `Orders`)
- Prefix constraints: `PK_TableName`, `FK_Child_Parent`, `IX_Table_Column`, `CK_Table_Rule`, `DF_Table_Column`
- Use singular table names or be consistent (don't mix `Order` and `Products`)

### Script Documentation Pattern

When generating T-SQL scripts, use this documentation format:

```sql
-- Created by <agent>
/*
  <2-3 sentence summary of script purpose>
*/

-- Create staging table for daily order import
CREATE TABLE dbo.OrderStaging (
    OrderID int NOT NULL,
    ...
);

-- Merge staging data into production
MERGE dbo.Orders AS target
USING dbo.OrderStaging AS source ON target.OrderID = source.OrderID
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

- One comment per DDL/DML statement (not per keyword)
- Inline comments for numeric constants: `WHERE Amount > 10000 -- high-value threshold`
- Always include `SET NOCOUNT ON;` at the top of stored procedures

---

## Auditing Configuration (REST API)

> **REST API reference**: [SQL Audit Settings API](https://learn.microsoft.com/en-us/rest/api/fabric/sqldatabase/sql-audit-settings)

Auditing tracks database events and writes them to audit logs stored in OneLake. Configuration is via REST API or Fabric portal only — not T-SQL.

### Get Audit Settings

```
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlDatabases/{sqlDatabaseId}/settings/sqlAudit
```

**Scope**: `SQLDatabase.Read.All` or `SQLDatabase.ReadWrite.All`.

### Enable / Update Auditing

```
PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlDatabases/{sqlDatabaseId}/settings/sqlAudit
Content-Type: application/json

{
  "state": "Enabled",
  "retentionDays": 10,
  "predicateExpression": "statement not like '[select ]%'"
}
```

| Field | Type | Default | Description |
|---|---|---|---|
| `state` | `Enabled` / `Disabled` | — | Required. Enabling for the first time with no other fields applies defaults. |
| `retentionDays` | integer | `0` (indefinite) | Days to retain audit logs. |
| `auditActionsAndGroups` | string[] | `["BATCH_COMPLETED_GROUP", "FAILED_DATABASE_AUTHENTICATION_GROUP", "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP"]` | Audit action groups to capture. |
| `predicateExpression` | string | none | T-SQL predicate to filter which events are logged. |

Response includes `storageEndpoint` (OneLake path where logs are stored).

**Scope**: `SQLDatabase.ReadWrite.All` or `Item.ReadWrite.All`.

> **Querying audit logs**: Once enabled, logs are queryable via T-SQL — see `sys.fn_get_audit_file_v2()` in SQLDB-CONSUMPTION-CORE.md.

---

## Customer-Managed Key (CMK) Revalidation

> **REST API reference**: [Revalidate CMK](https://learn.microsoft.com/en-us/rest/api/fabric/sqldatabase/items/revalidate-cmk)

If the SQL database uses a Customer-Managed Key (CMK) for encryption via Azure Key Vault, revalidation checks that the currently configured AKV key is still accessible, valid, and authorized for encryption operations.

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/sqlDatabases/{sqlDatabaseId}/revalidateCMK
```

- This is a long-running operation (LRO) — poll the `Location` header for completion.
- Use when the AKV key has been rotated, access policies changed, or after key vault recovery.

**Scope**: `SQLDatabase.ReadWrite.All` or `Item.ReadWrite.All`.

---

## Authoring Permission Model

| Action | Minimum Permission |
|---|---|
| Create SQL Database item | Admin or Member role on workspace |
| CREATE/ALTER/DROP tables, indexes | Contributor role or db_owner |
| INSERT/UPDATE/DELETE data | Contributor role or db_datawriter |
| CREATE VIEW/PROCEDURE/FUNCTION | Contributor role or appropriate SQL permissions |
| GRANT/DENY/REVOKE | Admin role or db_securityadmin |
| SqlPackage publish | Contributor role or db_ddladmin |
| Get audit settings | Reader or higher item permission |
| Update audit settings | Write permission on SQL database |
| Point-in-time restore (PITR) | Contributor role (creates new item) |
| Revalidate CMK | Write permission on SQL database |

Authentication: **Microsoft Entra ID only** — no SQL authentication (login/password).

---

## Authoring Gotchas and Troubleshooting

| # | Issue | Cause | Resolution |
|---|---|---|---|
| 1 | Clustered columnstore fails on existing table | Mirroring conflict | Stop mirroring, create CCI, restart mirroring; or create CCI at table creation |
| 2 | SqlPackage publish fails with auth error | Wrong authentication method | Use `Authentication=Active Directory Default` in connection string |
| 3 | sp_invoke_external_rest_endpoint fails | Missing database-scoped credential | Create credential: `CREATE DATABASE SCOPED CREDENTIAL` for target URL |
| 4 | Foreign key creation fails | Referenced table/column doesn't exist or type mismatch | Verify referenced table exists and column types match exactly |
| 5 | DML slower than expected | Missing indexes on filter/join columns | Check `sys.dm_db_tuning_recommendations`; auto-indexing will adapt over time |
| 6 | Trigger not firing | Trigger disabled or wrong event type | Check `sys.triggers` for `is_disabled`; verify AFTER vs INSTEAD OF |
| 7 | GraphQL API doesn't reflect schema changes | API caches schema at creation | Manually refresh: remove and re-add tables in the API, or recreate |
| 8 | Deployment pipeline copies metadata only | By design | Data must be populated separately in each environment |
| 9 | `Login failed for user` | Wrong database name or no Entra access | Verify database display name (case-sensitive); check workspace permissions |
| 10 | Vector column insert fails | Dimension mismatch | Ensure vector literal has exactly the declared number of dimensions |
| 11 | Full-text queries return errors | Full-text search is preview only; third-party filters and word breakers not supported | Enable full-text in portal if available, or use `LIKE`, `CHARINDEX`, or vector search |
| 12 | External table query fails | Missing Entra permissions or wrong path | Verify Lakehouse ABFSS path and user ReadAll on Lakehouse |
| 13 | Temporal table history growing large | System-versioned retains all history | Archive old history or set retention policy |

---

## Common Authoring Patterns (End-to-End Examples)

### Upsert with MERGE

SQL Database supports full MERGE (GA) — the preferred pattern for upsert operations:

```sql
CREATE OR ALTER PROCEDURE dbo.usp_UpsertCustomers
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        MERGE dbo.Customers AS target
        USING dbo.StagingCustomers AS source
        ON target.CustomerID = source.CustomerID
        WHEN MATCHED THEN
            UPDATE SET target.Name = source.Name,
                       target.Email = source.Email,
                       target.Region = source.Region
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (CustomerID, Name, Email, Region)
            VALUES (source.CustomerID, source.Name, source.Email, source.Region)
        WHEN NOT MATCHED BY SOURCE THEN
            DELETE;

        TRUNCATE TABLE dbo.StagingCustomers;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
```

### Incremental Load from OneLake

Load new data from Lakehouse files into a local table using data virtualization:

```sql
CREATE OR ALTER PROCEDURE dbo.usp_IncrementalLoadOrders
    @CutoffDate date
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        DELETE FROM dbo.Orders WHERE OrderDate >= @CutoffDate;

        INSERT INTO dbo.Orders (OrderID, CustomerID, OrderDate, Amount)
        SELECT OrderID, CustomerID, OrderDate, Amount
        FROM OPENROWSET(
            BULK '/sales/orders/*.parquet',
            FORMAT = 'parquet',
            DATA_SOURCE = 'LakehouseFiles'
        ) AS src
        WHERE src.OrderDate >= @CutoffDate;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
```

### Running Procedures from Pipelines

- **Stored Procedure activity**: Supports SQL database in Fabric connections directly (Azure SQL engine). Select the SQL database as the linked service.
- **Script activity**: Alternative — execute `EXEC dbo.usp_IncrementalLoadOrders @CutoffDate = '2025-01-01'` as inline T-SQL.
- **Notebook activity**: Use `pyodbc` or `pymssql` to connect and call `EXEC`.

---

## Quick Reference: Authoring Decision Guide

| Scenario | Recommended Approach |
|---|---|
| Bulk load from local files | BCP (`bcp ... in`) |
| Load with transformations from OneLake | OPENROWSET + INSERT |
| Ingest from another Fabric item | INSERT ... SELECT via SQL analytics endpoint (3-part naming) |
| Upsert (insert or update) | MERGE or DELETE + INSERT in transaction |
| Large-scale column transform | UPDATE with WHERE clause; or SELECT INTO + swap |
| Add a nullable column | `ALTER TABLE ADD col type NULL` |
| Change column data type | `ALTER TABLE ALTER COLUMN col newtype` |
| Rename table or column | `EXEC sp_rename` |
| Schema-as-code deployment | SqlPackage Publish (.dacpac) |
| Full database migration | SqlPackage Import (.bacpac) |
| Version control schema | Git integration + SQL Database Projects |
| Expose data via API | GraphQL API (portal or REST API) |
| Call external REST services from T-SQL | `sp_invoke_external_rest_endpoint` + database-scoped credential |
| Generate embeddings in T-SQL | `AI_GENERATE_EMBEDDINGS(col USE MODEL <model>)` (needs an EXTERNAL MODEL + DB-scoped credential) or `sp_invoke_external_rest_endpoint` |
| Automate ETL with T-SQL | Stored procedures + pipeline Script activity |
| Read/write from Spark notebooks | Spark SQL connector (preview) — `df.write.mssql()` / `spark.read.mssql()` |
| Audit trail for data changes | Temporal tables (system-versioned) |
| Point-in-time restore (live DB) | `POST .../sqlDatabases` with `creationMode: "Restore"` + `sourceDatabaseReference` + `restorePointInTime` |
| Recover soft-deleted database | `POST .../sqlDatabases` with `creationMode: "RestoreDeletedDatabase"` + `restorableDeletedDatabaseName` |
| Enable SQL auditing | `PATCH .../settings/sqlAudit` with `"state": "Enabled"` |
| Revalidate CMK after key rotation | `POST .../sqlDatabases/{id}/revalidateCMK` |

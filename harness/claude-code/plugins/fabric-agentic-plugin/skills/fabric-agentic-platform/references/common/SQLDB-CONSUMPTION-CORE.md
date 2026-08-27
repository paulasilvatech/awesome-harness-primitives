# SQLDB-CONSUMPTION-CORE.md

> **Scope**: Primarily consumption-oriented T-SQL patterns for **SQL database in Fabric** and its **SQL analytics endpoint**, with limited administrative/configuration examples where they support diagnostics, security, or operational understanding.
> This document is *language-agnostic* — no C#, Python, CLI, or SDK references. It covers endpoint selection, T-SQL query patterns, cross-database queries, vector search, AI/RAG, metadata discovery, performance monitoring, security inspection, troubleshooting, and narrowly scoped configuration examples needed to explain those scenarios.

> **Relationship to SQLDB-AUTHORING-CORE.md**: Full authoring topics (database lifecycle, primary DDL/DML workflows, temporal table creation, data virtualization setup, constraints, triggers, vector columns, SqlPackage, source control/CI/CD, GraphQL API, mirroring) live in `SQLDB-AUTHORING-CORE.md`. This document may cross-reference or include limited examples when they are directly relevant to consumption, inspection, or troubleshooting workflows.

---

## Endpoint Selection

Fabric exposes **two endpoints** for different workloads on a SQL database in Fabric:

| Endpoint | Engine | Use Case | Data Freshness | Write Support |
|---|---|---|---|---|
| **SQL Database (TDS)** | Azure SQL Database engine | OLTP queries, application reads, vector search, stored procedures | Live (real-time) | Full DML |
| **SQL Analytics Endpoint** | Fabric Data Warehouse engine | Cross-database joins, heavy analytics, BI reporting | Near real-time (replicated via mirroring) | Read-only |

### When to Use Which

| Scenario | Recommended Endpoint |
|---|---|
| Application queries (point lookups, OLTP) | SQL Database |
| Vector similarity search / RAG | SQL Database |
| Calling stored procedures | SQL Database |
| Cross-database joins with warehouses/lakehouses | SQL Analytics Endpoint |
| Power BI reports / semantic models | SQL Analytics Endpoint |
| Heavy aggregation / analytical queries | SQL Analytics Endpoint (avoids OLTP impact) |
| Spark notebook access (read-only, OneLake) | SQL Analytics Endpoint (via OneLake) |
| Spark notebook access (read/write, direct) | SQL Database (via Spark SQL connector — preview) |

### Connection Parameters

| Parameter | SQL Database | SQL Analytics Endpoint |
|---|---|---|
| **Server FQDN** | `<id>.database.fabric.microsoft.com` | `<id>.datawarehouse.fabric.microsoft.com` |
| **Port** | 1433 (+ ports 11000–11999 for redirect) | 1433 |
| **Database** | Display name of the SQL database item | Display name of the SQL database item |
| **Authentication** | Microsoft Entra ID only (no SQL auth, no logins) | Microsoft Entra ID only (no SQL auth) |
| **Supported identities** | Users, service principals, Entra groups | Users, service principals, Entra groups |
| **Encryption** | Required (TDS 8.0) | Required |
| **Token audience** | `https://database.windows.net/.default` | `https://database.windows.net/.default` |
| **Collation** | `SQL_Latin1_General_CP1_CI_AS` (case-insensitive) | Workspace default — typically `Latin1_General_100_BIN2_UTF8` (case-sensitive) |
| **Write support** | Full DML | Read-only |

**Critical**:
- The two endpoints have **different server FQDNs**. Discover each via Settings → Connection strings in the Fabric portal, or via REST API.
- Always specify the **database name** as `Initial Catalog` or `-d` parameter. The FQDN alone is insufficient — connection will fail with `Login failed for user`.
- **MARS (Multiple Active Result Sets) is not supported** on either endpoint. Remove or set to `false` in connection strings.
- **Connection policy is Default** (cannot be changed). Clients must allow outbound to Azure SQL IPs on ports 11000–11999 (redirect) in addition to port 1433 (gateway).
- **Collation mismatch**: The SQL analytics endpoint may use a different (case-sensitive) collation than the SQL database. Queries that work on the SQL database endpoint may return different results or errors on the analytics endpoint due to case sensitivity. The workspace collation can be changed to case-insensitive in workspace settings.
- **Service principals** require the **"Service principals can use Fabric APIs"** tenant setting to be enabled, plus Read item permission on the database.

---

## Supported T-SQL Surface Area

SQL database in Fabric uses the **Azure SQL Database engine**, so it supports most of the Azure SQL T-SQL surface (see [limitations](https://learn.microsoft.com/en-us/fabric/database/sql/limitations) for exceptions). Key areas for consumption:

### Query Features

- Standard SELECT with WHERE, ORDER BY, GROUP BY, HAVING
- CTEs (standard, recursive, nested)
- Window functions (ROW_NUMBER, RANK, DENSE_RANK, NTILE, LAG, LEAD, FIRST_VALUE, LAST_VALUE, SUM/AVG/MIN/MAX OVER)
- CASE, IIF, CHOOSE, COALESCE, NULLIF
- Subqueries (correlated and non-correlated)
- UNION / UNION ALL / INTERSECT / EXCEPT
- EXISTS / NOT EXISTS
- TOP / OFFSET-FETCH
- CROSS APPLY / OUTER APPLY
- PIVOT / UNPIVOT
- FOR JSON (PATH, AUTO) / FOR XML
- STRING_AGG, STRING_SPLIT
- JSON functions (OPENJSON, JSON_VALUE, JSON_QUERY, JSON_MODIFY)
- Temporal queries (FOR SYSTEM_TIME AS OF, BETWEEN, ALL)
- OPENROWSET BULK (data virtualization from OneLake — Parquet, CSV)
- External tables (Parquet, CSV via CREATE EXTERNAL TABLE)
- Native AI functions (`AI_GENERATE_EMBEDDINGS(col USE MODEL <model>)` — requires an EXTERNAL MODEL + DB-scoped credential)

**Intelligent Query Processing (IQP)**: Enabled by default (DB compat level 170). Includes adaptive joins, batch mode on rowstore, memory grant feedback, scalar UDF inlining, table variable deferred compilation, parameter sensitivity plan optimization, and optimistic concurrency via optimized locking. These features automatically improve query performance without code changes.

### Data Types

Azure SQL Database type system including:

| Category | Types |
|---|---|
| Exact numeric | `bigint`, `int`, `smallint`, `tinyint`, `bit`, `decimal`/`numeric`, `money`, `smallmoney` |
| Approximate numeric | `float`, `real` |
| Date/Time | `date`, `time`, `datetime`, `datetime2`, `datetimeoffset`, `smalldatetime` |
| Character | `char(n)`, `varchar(n)`, `varchar(max)`, `nchar(n)`, `nvarchar(n)`, `nvarchar(max)` |
| Binary | `binary(n)`, `varbinary(n)`, `varbinary(max)` |
| Other | `uniqueidentifier`, `xml`, `sql_variant`, `geometry`, `geography` |
| AI | `vector(n)` — native vector data type for embeddings |

> **Note**: Unlike Fabric Data Warehouse, SQL Database fully supports `nvarchar`, `datetime`, `money`, `xml`, `geometry`, `geography`, and other types that DW restricts.

> **Preview only**: Full-text search (`CONTAINS`, `FREETEXT`, full-text indexes) is available as a **preview feature** with limitations (no third-party filters or word breakers). Use `LIKE`, `CHARINDEX`, or vector similarity search as alternatives if full-text is not enabled.

---

## Cross-Database Queries

Cross-database queries use **three-part naming** and are supported **only via the SQL analytics endpoint**:

```sql
-- Join SQL Database data with a warehouse table
SELECT o.OrderID, o.CustomerID, w.CategoryName
FROM MyDatabase.dbo.Orders AS o
INNER JOIN ContosoWarehouse.dbo.DimCategory AS w
    ON o.CategoryID = w.CategoryID;

-- Join with a lakehouse table
SELECT d.DocID, d.Title, l.Metadata
FROM MyDatabase.dbo.Documents AS d
INNER JOIN SalesLakehouse.dbo.DocumentMetadata AS l
    ON d.DocID = l.DocID;
```

**Supported cross-database sources**: Other SQL databases, mirrored databases, warehouses, and lakehouse SQL analytics endpoints within the **same workspace**.

**Limitation**: Cross-database queries are read-only and only available on the SQL analytics endpoint, not the OLTP database endpoint.

---

## Temporal Table Queries

For temporal table creation, conversion, and query syntax (FOR SYSTEM_TIME AS OF, BETWEEN, CONTAINED IN, ALL), see [SQLDB-AUTHORING-CORE.md § Temporal Tables](SQLDB-AUTHORING-CORE.md#temporal-tables-system-versioned).

**Use cases** (consumption perspective): Slowly-changing dimension tracking, regulatory audit, point-in-time reporting, undo/revert analysis.

---

## Data Virtualization (Querying OneLake Files)

For OPENROWSET BULK, external data sources, external tables, CSV with explicit schema, and wildcard/partitioned paths, see [SQLDB-AUTHORING-CORE.md § Data Virtualization](SQLDB-AUTHORING-CORE.md#data-virtualization-external-tables-and-openrowset).

**Consumption note**: All examples in the authoring reference work read-only on the SQL analytics endpoint as well. For ingestion (INSERT INTO ... SELECT FROM OPENROWSET), use the SQL Database endpoint.

---

## JSON Functions

SQL database in Fabric supports the Azure SQL JSON function set:

```sql
-- Parse JSON column
SELECT OrderID,
    JSON_VALUE(OrderDetails, '$.shipping.method') AS ShipMethod,
    JSON_QUERY(OrderDetails, '$.items') AS Items
FROM dbo.Orders
WHERE JSON_VALUE(OrderDetails, '$.status') = 'delivered';

-- OPENJSON: Expand JSON array to rows
SELECT o.OrderID, item.ProductName, item.Quantity, item.Price
FROM dbo.Orders o
CROSS APPLY OPENJSON(o.OrderDetails, '$.items')
    WITH (ProductName nvarchar(200), Quantity int, Price decimal(19,4)) AS item;

-- FOR JSON PATH: Generate JSON from relational data
SELECT OrderID, CustomerID, OrderDate, TotalAmount
FROM dbo.Orders
WHERE CustomerID = 42
FOR JSON PATH, ROOT('orders');

-- JSON_MODIFY: Create a modified JSON document (preview without writing)
SELECT JSON_MODIFY(OrderDetails, '$.status', 'shipped') AS updated_order_details
FROM dbo.Orders
WHERE OrderID = 123;
```

---

## Vector Search and AI/RAG Patterns

### Vector Similarity Search

```sql
-- Find top 10 most similar documents to a query embedding
DECLARE @query_embedding vector(1536) = '<embedding-vector-literal>';

SELECT TOP 10 DocID, Title,
    VECTOR_DISTANCE('cosine', Embedding, @query_embedding) AS distance
FROM dbo.Documents
WHERE Embedding IS NOT NULL
ORDER BY distance ASC;
```

**Supported distance metrics** (via `VECTOR_DISTANCE`):
- `cosine` — most common for text embeddings
- `dot` — dot product
- `euclidean` — L2 distance

### RAG Pattern (Retrieval-Augmented Generation)

End-to-end RAG workflow in T-SQL:

1. **Generate query embedding** via `sp_invoke_external_rest_endpoint` calling Azure OpenAI.
2. **Vector search** to retrieve relevant documents.
3. **Augment prompt** with retrieved context.
4. **Call LLM** via `sp_invoke_external_rest_endpoint` for generation.

```sql
-- Step 1: Get embedding for user question
DECLARE @question nvarchar(max) = 'What is the return policy?';
DECLARE @embedding_response nvarchar(max);
DECLARE @retval int;

EXEC @retval = sp_invoke_external_rest_endpoint
    @url = 'https://<aoai>.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2024-02-01',
    @method = 'POST',
    @payload = N'{"input": "What is the return policy?"}',
    @credential = [https://<aoai>.openai.azure.com/],
    @response = @embedding_response OUTPUT;

-- Step 2: Extract embedding and search (simplified — parse JSON in practice)
-- Step 3: Use top-K results as context for chat completion call
```

### LangChain / Semantic Kernel Integration

- **LangChain**: Use `langchain-sqlserver` PyPI package for vector store backed by SQL database in Fabric.
- **Semantic Kernel**: Use the SQL Server connector for memory/vector storage.
- Both frameworks connect via standard TDS endpoint with Entra authentication.

---

## Metadata and Schema Discovery

### Tables and Columns

```sql
-- List all user tables
SELECT s.name AS [schema], t.name AS [table], 
    SUM(p.rows) AS row_count
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name
ORDER BY s.name, t.name;

-- Columns for a specific table
SELECT c.name AS column_name, ty.name AS data_type, 
    c.max_length, c.precision, c.scale, c.is_nullable, c.is_identity
FROM sys.columns c
JOIN sys.types ty ON c.user_type_id = ty.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.Orders')
ORDER BY c.column_id;

-- INFORMATION_SCHEMA alternative
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_schema = 'dbo' AND table_name = 'Orders'
ORDER BY ordinal_position;
```

### Indexes

```sql
SELECT i.name AS index_name, i.type_desc,
    STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS columns
FROM sys.indexes i
JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE i.object_id = OBJECT_ID('dbo.Orders')
GROUP BY i.name, i.type_desc;
```

### Constraints

```sql
SELECT tc.constraint_name, tc.constraint_type, kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu 
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_schema = 'dbo' AND tc.table_name = 'Orders'
ORDER BY tc.constraint_type, kcu.ordinal_position;
```

### Programmability Objects

```sql
SELECT name, type_desc, create_date, modify_date
FROM sys.objects
WHERE type IN ('V','P','FN','IF','TF','TR')
ORDER BY type_desc, name;
```

### Permissions

```sql
SELECT pr.name, pr.type_desc, pe.state_desc, pe.permission_name
FROM sys.database_principals AS pr
INNER JOIN sys.database_permissions AS pe
    ON pe.grantee_principal_id = pr.principal_id
ORDER BY pr.name;
```

---

## Performance and Monitoring

### Automatic Tuning

SQL database in Fabric enables Automatic Tuning by default. View recommendations:

```sql
-- Current tuning recommendations
SELECT name, reason, score,
    JSON_VALUE(state, '$.currentValue') AS state,
    JSON_VALUE(details, '$.indexName') AS suggested_index
FROM sys.dm_db_tuning_recommendations
WHERE JSON_VALUE(state, '$.currentValue') = 'Active';
```

### DMVs

```sql
-- Active sessions
SELECT session_id, login_name, status, program_name, 
    cpu_time, reads, writes, last_request_start_time
FROM sys.dm_exec_sessions
WHERE is_user_process = 1;

-- Active requests
SELECT r.session_id, r.status, r.command, r.cpu_time, r.total_elapsed_time,
    SUBSTRING(st.text, (r.statement_start_offset/2)+1,
        ((CASE r.statement_end_offset WHEN -1 THEN DATALENGTH(st.text)
         ELSE r.statement_end_offset END - r.statement_start_offset)/2)+1) AS query_text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) st
WHERE r.session_id != @@SPID;
```

### Query Store

```sql
-- Top resource-consuming queries (last 24 hours)
SELECT TOP 20 
    q.query_id, qt.query_sql_text,
    SUM(rs.avg_cpu_time * rs.count_executions) AS total_cpu,
    SUM(rs.count_executions) AS total_executions
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
JOIN sys.query_store_runtime_stats_interval rsi ON rs.runtime_stats_interval_id = rsi.runtime_stats_interval_id
WHERE rsi.start_time > DATEADD(HOUR, -24, GETUTCDATE())
GROUP BY q.query_id, qt.query_sql_text
ORDER BY total_cpu DESC;
```

### Extended Events (XEvents)

For advanced diagnostics beyond DMVs and Query Store:

```sql
-- List available XEvents
SELECT name, description FROM sys.dm_xe_objects WHERE object_type = 'event' ORDER BY name;

-- Example: Create a session tracking long queries
CREATE EVENT SESSION LongQueries ON DATABASE
ADD EVENT sqlserver.sql_statement_completed
    (ACTION (sqlserver.sql_text, sqlserver.session_id)
     WHERE duration > 5000000)  -- > 5 seconds
ADD TARGET package0.ring_buffer;
ALTER EVENT SESSION LongQueries ON DATABASE STATE = START;
```

### Query Writing Best Practices

| Practice | Why |
|---|---|
| `SELECT` only needed columns | Reduces I/O and network transfer |
| Filter early with `WHERE` | Pushes predicates to storage; reduces row processing |
| Avoid `SELECT *` | Scans all columns; wastes resources |
| Use `TOP` / `OFFSET-FETCH` for exploration | Limits data returned for ad-hoc queries |
| Prefer `EXISTS` over `IN` for large subqueries | Generally more efficient execution |
| Avoid unnecessary `DISTINCT` | Forces deduplication pass on entire result |
| Use `UNION ALL` instead of `UNION` when duplicates are acceptable | Skips deduplication sort |
| Use appropriate data types in predicates | Avoids implicit conversions (e.g., comparing varchar to int) |
| Batch complex logic into views/procedures | Encapsulation, reuse, easier security management |
| Use parameterized queries | Promotes plan reuse; prevents SQL injection |

> **For deep performance diagnostics** — Query Store volatile detection, wait-category analysis, blocking chains, missing-index/auto-tuning analysis, CPU/IO pressure investigation, and Extended Events workflows — see the **`sqldb-operations-cli`** skill (`references/query-reference.md`). This section covers patterns useful during normal consumption; the operations skill owns the deep-diagnostic catalog.

---

## Security

### Row-Level Security (RLS)

```sql
-- Create predicate function
CREATE FUNCTION dbo.fn_SecurityPredicate(@UserName nvarchar(128))
RETURNS TABLE
WITH SCHEMABINDING
AS
    RETURN SELECT 1 AS result WHERE @UserName = USER_NAME()
        OR USER_NAME() = 'dbo';

-- Create security policy
CREATE SECURITY POLICY dbo.OrdersFilter
ADD FILTER PREDICATE dbo.fn_SecurityPredicate(OwnerUserName)
ON dbo.Orders
WITH (STATE = ON);
```

### Column-Level Security (CLS)

```sql
-- Grant SELECT on specific columns only
GRANT SELECT ON dbo.Orders (OrderID, CustomerID, OrderDate, Status)
TO [analyst@contoso.com];
-- Denies access to TotalAmount, Notes, etc.
```

### Dynamic Data Masking (DDM)

```sql
-- Mask email column
ALTER TABLE dbo.Customers
ALTER COLUMN Email ADD MASKED WITH (FUNCTION = 'email()');

-- Mask partial phone number
ALTER TABLE dbo.Customers
ALTER COLUMN Phone ADD MASKED WITH (FUNCTION = 'partial(0, "XXX-XXX-", 4)');

-- Grant unmask to specific user
GRANT UNMASK ON dbo.Customers TO [admin@contoso.com];
```

### Auditing

```sql
-- Query audit logs (after enabling auditing via REST API or Fabric portal)
SELECT event_time, action_id, succeeded, server_principal_name,
    database_name, object_name, statement
FROM sys.fn_get_audit_file_v2(NULL, NULL, NULL)
ORDER BY event_time DESC;
```

Auditing can be enabled via the **REST API** (`PATCH .../sqlDatabases/{id}/settings/sqlAudit`) or the Fabric portal. Logs are stored in OneLake and queryable via `sys.fn_get_audit_file_v2`.

### Sharing and Permissions

- **Share** a SQL database via the Fabric portal Share button, or assign workspace roles via REST API (`POST .../workspaces/{id}/roleAssignments`), to grant access without direct workspace membership.
- Sharing grants access to **both** the SQL database and its SQL analytics endpoint.
- Shared databases appear in the user's **Shared with Me** section and OneLake Data Hub.
- Fabric item permissions: Read, ReadAll, Write — control item-level access.
- SQL-level GRANT/DENY/REVOKE — control object-level access within the database.

### Security Do and Don't

| Do | Don't |
|---|---|
| Use Viewer role + SQL GRANT for consumers | Give Contributor/Member to report consumers |
| Use roles (`CREATE ROLE`) for permission management | GRANT to individual users at scale |
| Set RLS on SQL analytics endpoint separately if data is sensitive | Assume RLS from SQL database covers the analytics endpoint |
| Test security by connecting as the target user | Rely on owner-testing (owners bypass RLS/CLS) |
| Use DDM for dev/test scenarios with real data shapes | Treat DDM as encryption — it is a viewing restriction only |
| Enable auditing via REST API or portal for compliance | Ignore audit logs for sensitive databases |
| Use `sp_invoke_external_rest_endpoint` credentials scoped to specific URLs | Create overly broad credentials |

---

## Gotchas and Troubleshooting Reference

| # | Issue | Cause | Resolution |
|---|---|---|---|
| 1 | Cross-database query fails on SQL Database endpoint | Cross-DB only works on SQL analytics endpoint | Connect to the SQL analytics endpoint instead |
| 2 | Data appears stale in SQL analytics endpoint | Mirroring replication lag (near real-time, not instant) | Wait for replication; check mirroring status via T-SQL (`SELECT * FROM sys.dm_change_feed_log_scan_sessions`) or Fabric portal |
| 3 | RLS from SQL database not applied on analytics endpoint | Security policies are per-endpoint | Re-configure RLS on the SQL analytics endpoint separately |
| 4 | `Login failed for user` | Wrong database name or no Entra access | Verify exact display name (case-sensitive); check workspace permissions |
| 5 | `Cannot open server` / `Login timeout expired` | Wrong FQDN or port 1433 blocked | Re-discover FQDN via REST API; check firewall/VPN; allow ports 11000–11999 for redirect |
| 6 | Vector search returns no results | NULL embeddings or dimension mismatch | Verify `WHERE Embedding IS NOT NULL`; check vector dimensions match |
| 7 | `sp_invoke_external_rest_endpoint` HTTP 401 | Missing or invalid database-scoped credential | Verify credential matches target URL; check Entra app permissions |
| 8 | Query Store views empty | Query Store not yet populated | Run workload; data populates automatically over time |
| 9 | `sys.fn_get_audit_file_v2` returns no rows | Auditing not enabled | Enable auditing via REST API (`PATCH .../settings/sqlAudit`) or Fabric portal |
| 10 | INFORMATION_SCHEMA shows fewer tables than expected | User lacks SELECT permission on some tables | Check grants: `SELECT * FROM sys.database_permissions WHERE grantee_principal_id = DATABASE_PRINCIPAL_ID()` |
| 11 | Analytical query impacts OLTP performance | Running heavy reads on the OLTP endpoint | Use the SQL analytics endpoint for analytical workloads |
| 12 | `ActiveDirectoryDefault` auth failure | `az login` session expired or wrong tenant | Run `az login --tenant <tenantId>` |
| 13 | Full-text search (`CONTAINS`/`FREETEXT`) fails | Full-text search is preview only; third-party filters and word breakers not supported | Enable full-text in portal if available, or use `LIKE`, `CHARINDEX`, or vector search |
| 14 | OPENROWSET returns permission error | Missing Entra passthrough or Lakehouse access | User needs ReadAll on the Lakehouse and valid ABFSS path |
| 15 | Temporal query returns empty history | Table not system-versioned or no changes yet | Verify `SYSTEM_VERSIONING = ON` in table properties |
| 16 | FOR JSON PATH returns NULL | No matching rows or NULL column values | Add `INCLUDE_NULL_VALUES` option or check WHERE clause |
| 17 | Copilot NL-to-SQL generates wrong query | Ambiguous or non-descriptive column/table names | Use descriptive names; rephrase prompt more specifically |
| 18 | Query works on SQL Database but fails on analytics endpoint with collation error | SQL Database uses case-insensitive collation; analytics endpoint defaults to case-sensitive (`Latin1_General_100_BIN2_UTF8`) | Use explicit `COLLATE` in comparisons, or change workspace collation to case-insensitive in workspace settings |
| 19 | Service principal cannot connect | "Service principals can use Fabric APIs" tenant setting not enabled | Admin must enable the tenant setting; SP also needs Read item permission on the database |

---

## Quick Reference: Consumption Capabilities by Scenario

| Scenario | Approach | Endpoint |
|---|---|---|
| Point lookup by primary key | `SELECT ... WHERE PK = @value` | SQL Database |
| Full-text search | **Preview only** — use `LIKE`, `CHARINDEX`, or vector search if not enabled | SQL Database |
| Vector similarity search | `VECTOR_DISTANCE()` + `ORDER BY` + `TOP K` | SQL Database |
| Cross-database join | Three-part naming | SQL Analytics Endpoint |
| Query OneLake files (Parquet/CSV) | `OPENROWSET(BULK ...)` or external tables | SQL Database |
| Temporal point-in-time query | `FOR SYSTEM_TIME AS OF` | SQL Database |
| JSON processing | `OPENJSON`, `JSON_VALUE`, `FOR JSON PATH` | SQL Database |
| Time-series aggregation | Window functions + GROUP BY | Either (prefer Analytics for large scans) |
| Row count / table stats | `sys.partitions` or `COUNT(*)` | Either |
| Schema discovery | `INFORMATION_SCHEMA` / `sys.tables` / `sys.columns` | Either |
| RLS policy inspection | `sys.security_policies` + `sys.security_predicates` | Either |
| Audit log review | `sys.fn_get_audit_file_v2()` | SQL Database |
| Performance investigation | Query Store views + DMVs | SQL Database |
| Extended events diagnostics | `CREATE EVENT SESSION` + `sys.dm_xe_sessions` | SQL Database |
| Copilot NL-to-SQL | Chat pane or `--` comments in query editor | SQL Database (portal, SSMS, VS Code) |
| Power BI report | Connect via SQL analytics endpoint or create semantic model | SQL Analytics Endpoint |
| Spark notebook read/write | Spark SQL connector (preview) — `spark.read.mssql()` / `df.write.mssql()` | SQL Database |
| Data Factory pipeline | SQL database connector in Data Factory | Either |

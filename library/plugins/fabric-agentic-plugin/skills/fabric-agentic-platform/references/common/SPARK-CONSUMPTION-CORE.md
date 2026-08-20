# SPARK-CONSUMPTION-CORE.md

> **Scope**: Consumption-oriented patterns for Microsoft Fabric data engineering — Livy session management, interactive data exploration, analytical queries, and monitoring via REST APIs and CLI tools. This document is *language-agnostic* — no specific CLI, SDK, or tool references.
>
> **Companion files**:
> - `SPARK-AUTHORING-CORE.md` — Authoring patterns: notebook deployment, lakehouse creation, job execution
> - `COMMON-CORE.md` — Fabric REST API patterns, authentication, token audiences  
> - `COMMON-CLI.md` — CLI invocation patterns for cross-platform tools

---

## Relationship to SPARK-AUTHORING-CORE.md

Consumption and authoring workflows often overlap. This document covers what is **exclusive to consumption**:

| Topic | Where Documented |
|---|---|
| Lakehouse creation and deployment | `SPARK-AUTHORING-CORE.md` Lakehouse Management |
| Notebook deployment and job execution | `SPARK-AUTHORING-CORE.md` Notebook Management, Notebook Execution & Job Management |
| CI/CD and infrastructure automation | `SPARK-AUTHORING-CORE.md` CI/CD & Automation Patterns, Infrastructure-as-Code |
| **Lakehouse Livy session management and configuration** | **This document — Lakehouse Livy Session Management** |
| **Interactive data exploration via Livy** | **This document — Interactive Data Exploration** |
| **Cross-lakehouse analytics and performance** | **This document — PySpark Analytics Patterns** |

---

## Data Engineering Consumption Capability Matrix

| Capability | Lakehouse Livy Session | Direct SQL | Notebook Output | Data Pipeline |
|---|---|---|---|---|
| Interactive queries | ✅ | ✅ | ❌ | ❌ |
| Real-time exploration | ✅ | ✅ | ❌ | ❌ |
| Historical analysis | ✅ | ✅ | ✅ | ✅ |
| Parameterized queries | ✅ | ✅ | ❌ | ✅ |
| Session state management | ✅ | ❌ | ❌ | ❌ |
| Cross-lakehouse queries | ✅ | ✅ | ✅ | ✅ |

---

## OneLake Table APIs (Schema-enabled Lakehouses)

### Overview

OneLake Table APIs provide Unity Catalog-compatible metadata operations for **schema-enabled lakehouses**. These APIs are essential for:
- Schema discovery in schema-enabled lakehouses
- Table metadata retrieval (columns, data types, constraints)
- Catalog browsing when Fabric Tables APIs return "UnsupportedOperationForSchemasEnabledLakehouse"

**Base URL**: `https://onelake.table.fabric.microsoft.com`
**API Version**: Unity Catalog API v2.1
**Authentication**: **Storage token** with audience `https://storage.azure.com` (NOT Fabric API tokens)

> **Critical**: OneLake Table APIs only work with **schema-enabled lakehouses**. For non-schema lakehouses, use Fabric Tables APIs (COMMON-CORE.md Long-Running Operations).

### Schema Discovery

**List Schemas**:
```
GET https://onelake.table.fabric.microsoft.com/delta/{workspaceId}/{lakehouseId}/api/2.1/unity-catalog/schemas?catalog_name={lakehouseName}.Lakehouse
```

**Response**:
```json
{
  "schemas": [
    {
      "name": "dbo",
      "catalog_name": "MyLakehouse.Lakehouse",
      "comment": "Default schema",
      "full_name": "MyLakehouse.Lakehouse.dbo",
      "schema_type": "MANAGED_SCHEMA"
    }
  ]
}
```

### Table Discovery

**List Tables**:
```
GET https://onelake.table.fabric.microsoft.com/delta/{workspaceId}/{lakehouseId}/api/2.1/unity-catalog/tables?catalog_name={lakehouseName}.Lakehouse&schema_name=dbo
```

**Response** (key fields; many optional fields may be null):
```json
{
  "tables": [
    {
      "name": "sales_data",
      "catalog_name": "MyLakehouse.Lakehouse",
      "schema_name": "dbo",
      "data_source_format": "DELTA",
      "storage_location": "https://onelake.dfs.fabric.microsoft.com/{workspaceId}/{lakehouseId}/Tables/dbo/sales_data"
    }
  ],
  "next_page_token": null
}
```

### Table Schema Details

**Get Table Schema**:
```
GET https://onelake.table.fabric.microsoft.com/delta/{workspaceId}/{lakehouseId}/api/2.1/unity-catalog/tables/{lakehouseName}.Lakehouse.dbo.{tableName}
```

Response includes column metadata (types, constraints), storage location, table properties, and partitioning information.

### Error Handling

**URL Format**: Use `{workspaceId}/{lakehouseId}` in path:
```
https://onelake.table.fabric.microsoft.com/delta/{workspaceId}/{lakehouseId}/api/2.1/...
```

**Common HTTP Status Codes**:

| HTTP Status | Error | Solution |
|---|---|------|
| 401 | Unauthorized | Verify workspace ID and lakehouse ID in URL path |
| 403 | Forbidden | User needs read access to lakehouse |
| 404 | Not Found | Check workspace ID and lakehouse ID are correct |
| 400 | Bad Request | Lakehouse is not schema-enabled, use Fabric Tables APIs instead |

**Fallback Pattern**:
```
1. Try OneLake Table APIs with workspace ID/lakehouse ID format
2. If 400: Use Fabric Tables API (lakehouse not schema-enabled)
3. If 403: Check permissions
4. Final fallback: SQL Endpoint (TDS connection)
```

---

## Lakehouse Livy Session Management

> **Lakehouse Livy sessions vs Notebook Spark sessions** — This section covers **Lakehouse Livy sessions**, created via the public Livy API endpoint (`/lakehouses/{lhId}/livyapi/.../sessions`) for ad-hoc interactive Spark execution from remote clients. **Notebook Spark sessions** are a different mechanism — they are created internally when a Fabric Notebook runs (via portal or Jobs API `RunNotebook`) and are managed by the notebook execution lifecycle, not the Livy API. For notebook execution, see `SPARK-AUTHORING-CORE.md` § Notebook Execution & Job Management.

### Session Creation

**Endpoint**: `POST /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livyapi/versions/2023-12-01/sessions`

> **CLI Note**: When using `az rest` or bash scripts, use the `$LIVY_API_PATH` variable from COMMON-CLI.md (currently `livyapi/versions/2023-12-01`) to ensure version consistency.

**Session Configuration** (Recommended for Starter Pool):
```json
{
  "name": "analytical_session",
  "driverMemory": "56g",
  "driverCores": 8,
  "executorMemory": "56g",
  "executorCores": 8,
  "conf": {
    "spark.dynamicAllocation.enabled": "true",
    "spark.fabric.pool.name": "Starter Pool"
  }
}
```

**Key configuration notes**:
- Use `spark.fabric.pool.name: "Starter Pool"` for development/testing with faster startup
- Enable `spark.dynamicAllocation.enabled: "true"` when using Starter Pool
- For production workloads, use workspace pools instead of starter pools
- Do NOT use `spark.fabric.pool.enabled` (deprecated/incorrect property)

**Compute Tier Reference** (for workspace pools):

| Tier | Driver Cores | Driver Memory | Executor Cores | Executor Memory | Suggested Use Case |
|------|--------------|---------------|----------------|-----------------|-------------------|
| Small | 4 | 28g | 4 | 28g | Standard transformations, small data collection |
| Medium | 8 | 56g | 8 | 56g | Medium-sized joins, intermediate aggregation |
| Large | 16 | 112g | 16 | 112g | Heavy collect(), high partition count, large metadata |
| XLarge | 32 | 224g | 32 | 224g | Very high volume data manipulation |

**Valid memory values**:  28g, 56g, 112g, 200g, 224g, 400g  
**Important**: Using invalid memory values (e.g., 4g, 2g) will result in validation errors.

**Alternative configuration** (Small tier for light workloads):
```json
{
  "name": "analytical_session",
  "driverMemory": "28g",
  "driverCores": 4,
  "executorMemory": "28g", 
  "executorCores": 4,
  "numExecutors": 2
}
```

**Response** (key fields):
```json
{
  "id": 123,
  "name": "analytical_session",
  "appId": "application_1234567890_0001",
  "state": "starting",
  "kind": "pyspark"
}
```

### Session States and Lifecycle

**Session State Transitions**:
- `not_started` → `starting` → `idle` → `busy` → `idle`
- Terminal states: `dead`, `killed`, `success`, `error`

**State Management**:
- **Active Session**: Maximum 1 active session per lakehouse per user
- **Session Timeout**: Automatic termination after inactivity period
- **Resource Cleanup**: Sessions automatically cleaned up on termination

### Session Information Retrieval

**List Sessions**: `GET /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livyapi/versions/2023-12-01/sessions`

**Get Session Details**: `GET /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livyapi/versions/2023-12-01/sessions/{sessionId}`

Returns session state, kind, driver/executor memory, start time, and last activity timestamp.

### Session Termination

**Delete Session**: `DELETE /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livyapi/versions/2023-12-01/sessions/{sessionId}`

**Termination Scenarios**:
- **Manual Termination**: Explicit DELETE request
- **Timeout Termination**: Automatic after inactivity period
- **Error Termination**: Session failure due to resource issues
- **Resource Cleanup**: All temporary data cleared on termination

---

## Interactive Data Exploration

### Statement Execution

**Execute Code**: `POST /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livyapi/versions/2023-12-01/sessions/{sessionId}/statements`

**Request Pattern**:
```json
{
  "code": "df = spark.sql('SELECT * FROM table_name LIMIT 10')\ndf.show()"
}
```

**Statement Response**:
```json
{
  "id": 1,
  "code": "df = spark.sql('SELECT * FROM table_name LIMIT 10')\ndf.show()",
  "state": "running",
  "output": null,
  "started_at": "2026-02-08T10:00:00Z",
  "completed_at": null
}
```

### Output Retrieval

**Statement Status**: `GET /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/livyapi/versions/2023-12-01/sessions/{sessionId}/statements/{statementId}`

**Completed Statement Response**:
```json
{
  "id": 1,
  "state": "available",
  "output": {
    "status": "ok",
    "execution_count": 1,
    "data": {
      "text/plain": ["+-----+--------+\n|  id |   name |\n+-----+--------+\n|   1 |  Alice |\n|   2 |    Bob |\n+-----+--------+"]
    }
  }
}
```

---

## PySpark Analytics Patterns

> Generic PySpark syntax (filtering, aggregation, window functions) is omitted — LLMs already know standard Spark. This section covers **Fabric-specific** patterns only.

### Cross-Lakehouse Analytics

**Multi-Lakehouse Queries** (Fabric 3-part naming):
```python
# Query from different lakehouses using 3-part names
bronze_data = spark.sql("SELECT * FROM bronze_lakehouse.default.raw_transactions")
silver_data = spark.sql("SELECT * FROM silver_lakehouse.default.cleaned_transactions")

# Join across lakehouses
joined_data = bronze_data.alias("b").join(
    silver_data.alias("s"),
    col("b.transaction_id") == col("s.transaction_id"),
    "inner"
)
```

**Incremental Cross-Lakehouse Sync**:
```python
new_data = spark.sql("""
    SELECT * FROM source_lakehouse.default.table_name 
    WHERE date > (SELECT MAX(date) FROM target_lakehouse.default.table_name)
""")
new_data.write.mode("append").saveAsTable("target_lakehouse.default.table_name")
```

### Performance Optimization

| Technique | Pattern | When to Use |
|---|---|---|
| Predicate pushdown | `.filter(col("partition_date") == "2026-02-08")` | Always filter on partition columns first |
| Column projection | `.select("id", "name", "amount")` | Wide tables — select only needed columns |
| Broadcast join | `large_df.join(broadcast(small_df), "key")` | Small dimension tables (<100MB) |
| Caching | `df.cache(); df.count()` | Repeatedly accessed DataFrames |

---

This document provides the core patterns for Microsoft Fabric data engineering consumption workflows. For authoring patterns (notebook deployment, lakehouse creation), refer to `SPARK-AUTHORING-CORE.md`.
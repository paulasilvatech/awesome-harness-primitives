# SPARK-AUTHORING-CORE.md

> **Scope**: Authoring-oriented concepts for Microsoft Fabric data engineering — lakehouse lifecycle, notebook deployment, job execution, and workspace management via REST APIs. This document is *language-agnostic* — no specific CLI, SDK, or tool references.
>
> **Companion files**:
> - `SPARK-CONSUMPTION-CORE.md` — Consumption patterns: Livy sessions, data exploration, analytics workflows
> - `COMMON-CORE.md` — Fabric REST API patterns, authentication, token audiences  
> - `COMMON-CLI.md` — CLI invocation patterns for cross-platform tools

---

## Relationship to SPARK-CONSUMPTION-CORE.md

Authoring and consumption workflows often overlap. This document covers what is **exclusive to authoring**: lakehouse creation/configuration, notebook deployment and management, notebook execution and job scheduling, and compute pool strategy.

For Livy session management, interactive data queries, PySpark analytics patterns, and cross-lakehouse exploration, see `SPARK-CONSUMPTION-CORE.md`. For workspace/item discovery and authentication, see `COMMON-CORE.md` and `COMMON-CLI.md`.

---

## Data Engineering Authoring Capability Matrix

| Capability | Lakehouse | Notebook | Data Pipeline | Spark Job Definition |
|---|---|---|---|---|
| Create via REST API | ✅ | ✅ | ✅ | ✅ |
| Deploy content | ✅ | ✅ | ✅ | ✅ |
| Schema organization | ✅ | ❌ | ❌ | ❌ |
| Execute/Schedule | ❌ | ✅ | ✅ | ✅ |
| Parameter passing | ❌ | ✅ | ✅ | ✅ |
| Monitoring & status | ❌ | ✅ | ✅ | ✅ |
| Version control integration | ✅ | ✅ | ✅ | ✅ |

---

## Lakehouse Management

### Lakehouse Creation

**Endpoint**: `POST /workspaces/{workspaceId}/items`

```json
{
  "displayName": "MyLakehouse",
  "type": "Lakehouse", 
  "description": "Data lakehouse for analytics workloads",
  "creationPayload": {
    "enableSchemas": true
  }
}
```

- Set `enableSchemas: true` to enable multi-schema support (recommended). Without it, only the default `dbo` schema is available.
- Every lakehouse automatically gets `Tables/` (managed Delta tables) and `Files/` (unmanaged files) folders, a SQL analytics endpoint, and a OneLake path.

### Lakehouse Update

```
PATCH /workspaces/{workspaceId}/items/{lakehouseId}
```

Update `displayName` and `description`. Response includes `sqlEndpointProperties` (connection string, provisioning status) and `oneLakeFilesPath`/`oneLakeTablesPath`.

### Lakehouse Deletion

```
DELETE /workspaces/{workspaceId}/items/{lakehouseId}
```

**Cascading effects**: SQL Endpoint deleted automatically; all OneLake data permanently removed; external shortcuts become inaccessible; notebooks referencing this lakehouse will fail at runtime.

### Lakehouse Schema Organization

Schemas provide logical organization for tables within a lakehouse. Common use cases: medallion architecture (bronze/silver/gold), domain separation, access control.

**Creating and using schemas**:
```sql
-- Via Spark SQL or SQL Endpoint (T-SQL syntax identical)
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Create table in schema
CREATE TABLE bronze.raw_data (...) USING DELTA;

-- Query across schemas
SELECT * FROM bronze.raw JOIN silver.cleansed ON ...;

-- Set default schema
USE silver;
```

```python
# DataFrame API
df.write.format("delta").saveAsTable("silver.cleansed_data")
```

**Key rules**: use lowercase names; default schema is `dbo`; `DROP SCHEMA name CASCADE` removes schema with all tables; grant permissions via SQL Endpoint (`GRANT SELECT ON SCHEMA::gold TO [user@domain.com]`).

---

## Notebook Management

### Notebook Creation


**Endpoint**: `POST /workspaces/{workspaceId}/items`

Two workflows: (1) create empty notebook (omit `definition`), then deploy content separately via `POST /v1/workspaces/{workspaceId}/notebooks/{notebookId}/updateDefinition`; (2) create with content in a single operation:
**IMPORTANT: All creation and definition calls return HTTP 202 Accepted (async).** 

You must:

1. Capture the `Location` header from the 202 response
2. Poll `GET {Location}` until `status == "Succeeded"`
3. For `getDefinition`, call `GET {Location}/result` to retrieve the actual content

### Notebook Creation Workflows

**Two Primary Patterns**:

1. **Empty Notebook Creation**: Create placeholder notebook, deploy content separately
2. **Notebook with Content Creation**: Create and populate notebook in single operation

### Empty Notebook Creation

**Step 1 - Create Empty Notebook**:

**Endpoint**: `POST /workspaces/{workspaceId}/items`

```json
{
  "displayName": "DataProcessingNotebook",
  "type": "Notebook",
  "description": "PySpark notebook for data processing"
}
```

**Step 2 - Deploy Content** (separate operation):

```json
PATCH /workspaces/{workspaceId}/items/{itemId}/definition
{
  "definition": {
    "format": "ipynb",
    "parts": [
      {
        "path": "notebook-content.ipynb",
        "payload": "<base64-encoded-notebook-content>",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

### Notebook with Content Creation

**Endpoint**: `POST /workspaces/{workspaceId}/items`

```json
{
  "displayName": "DataProcessingNotebook",
  "type": "Notebook",
  "description": "PySpark notebook for data processing",
  "definition": {
    "format": "ipynb",
    "parts": [
      {
        "path": "notebook-content.ipynb",
        "payload": "<base64-encoded-notebook-content>",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

The `payload` is a base64-encoded standard `.ipynb` file. The Fabric-specific addition is the `metadata.dependencies` section for lakehouse binding:

```json
{
  "metadata": {
    "dependencies": {
      "lakehouse": {
        "default_lakehouse": "<lakehouse-id>",
        "default_lakehouse_workspace_id": "<workspace-id>",
        "default_lakehouse_name": "<lakehouse-name>"
      }
    }
  }
}
```

One default lakehouse per notebook (auto-mounted at runtime). Additional lakehouses accessible via SparkSQL 3-part names.

### Notebook Update

**Content Update (Notebook-Specific API)**:

`POST /v1/workspaces/{workspaceId}/notebooks/{notebookId}/updateDefinition`

```json
{
  "definition": {
    "format": "ipynb",
    "parts": [
      {
        "path": "notebook-content.ipynb",
        "payload": "<base64-encoded-notebook-content>",
        "payloadType": "InlineBase64"
      }
    ]
  }
}
```

**Alternative: Generic Items API**:

`PATCH /v1/workspaces/{workspaceId}/items/{itemId}/definition` — same `definition` structure.

> **Note**: The notebook-specific `updateDefinition` endpoint (POST) is the recommended method for updating notebook content.

**Metadata Update**:

`PATCH /v1/workspaces/{workspaceId}/items/{itemId}` — update `displayName` and `description`.

### Notebook Deletion

`DELETE /workspaces/{workspaceId}/items/{itemId}`

Job history is preserved. Lakehouse and other notebooks sharing the same lakehouse are unaffected.

---

## Notebook Execution & Job Management

### On-Demand Execution

**Endpoint**: `POST /workspaces/{workspaceId}/items/{itemId}/jobs/instances?jobType=RunNotebook`

**CRITICAL: Preventing Duplicate Job Submissions**

Before creating a new job instance:
1. **Check for recent jobs first**: Query `GET /workspaces/{workspaceId}/items/{itemId}/jobs/instances` and filter for jobs started in the last 5 minutes
2. **If recent job found**: Monitor that existing job instead of creating a new one
3. **If POST response is unreadable**: Query job history to verify if job was created before retrying
4. **Store job ID immediately**: Capture `jobInstanceId` from response before any other operations
5. **Never retry POST with same parameters**: If you have a job ID, only use GET to check status

**Anti-patterns to avoid**:
- ❌ Retrying POST immediately on failure (creates duplicates)
- ❌ Creating new job when one is already running
- ❌ Not checking recent job history before submission

**Pool options** (passed via `executionData.configuration`):
- **Workspace Pool** (`useWorkspacePool: true`): Production workloads, consistent performance
- **Starter Pool** (`useStarterPool: true`): Development/testing, shared resources
- **Custom Pool**: Enterprise scenarios with specific VM types or GPU requirements

The `defaultLakehouse` object (with both `id` and `name`) must be provided in the configuration.

### Job Monitoring

**Endpoint**: `GET /workspaces/{workspaceId}/items/{itemId}/jobs/instances/{jobInstanceId}`

**Job states**: `NotStarted` → `Running` → `Completed` | `Failed` | `Cancelled`

**Polling pattern**:
1. Submit job once and store `jobInstanceId`
2. Poll every 10-30 seconds: `GET /jobs/instances/{jobInstanceId}`
3. Check `status` field for completion
4. On error during polling, continue polling same job (don't create new job)
5. Timeout after reasonable duration (e.g., 30 minutes for typical notebooks)

### Error Handling

| Failure | Cause | Fix |
|---|---|---|
| DefaultLakehouse: missing name | Only `id` provided | Supply both `id` and `name` |
| Pool unavailable | Workspace pool not configured or at capacity | Check pool config or use starter pool |
| Authentication failure | Invalid or expired token | Refresh token (see COMMON-CORE.md) |
| Resource limits | Notebook exceeds memory/compute | Use larger pool or optimize workload |

---

## CI/CD & Automation Patterns

### Deployment Pipeline Structure

| Stage | Activity | Method |
|---|---|---|
| Source Control | Notebooks stored as `.ipynb` files in Git | Git integration |
| Build | Validate notebook format, lint PySpark code | CI pipeline |
| Deploy | Upload to Fabric workspace | REST API (`POST /workspaces/{workspaceId}/items`) |
| Test | Execute notebooks with test data | Job API (`POST .../jobs/instances?jobType=RunNotebook`) |
| Production | Deploy to production workspace | REST API with prod workspace IDs |

### Environment Management

Separate environments (dev/test/prod) with parameterized workspace and lakehouse IDs. Configuration pattern:

```json
{
  "environments": {
    "dev":  { "workspaceId": "<dev-ws-id>",  "lakehouseId": "<dev-lh-id>" },
    "test": { "workspaceId": "<test-ws-id>", "lakehouseId": "<test-lh-id>" },
    "prod": { "workspaceId": "<prod-ws-id>", "lakehouseId": "<prod-lh-id>" }
  }
}
```

### Version Control Best Practices

- **Clear outputs before commit**: Prevent noise in diffs
- **Parameterize environment-specific values**: Use notebook parameters or config files
- **Modular design**: Split complex logic into multiple notebooks
- **Documentation**: Markdown cells explaining business logic

---

## Infrastructure-as-Code

### Workspace Provisioning

```json
POST /workspaces
{
  "displayName": "{project}-{environment}",
  "description": "Data engineering workspace",
  "capacityId": "<capacity-id>"
}
```

### Resource Templates

Provision lakehouses and notebooks via REST API or ARM/Bicep templates. Use naming conventions (`{project}-{environment}`), capacity assignment per environment tier, and RBAC with least-privilege roles.

| Resource | API | Key Configuration |
|---|---|---|
| Workspace | `POST /workspaces` | `capacityId`, RBAC roles |
| Lakehouse | `POST /workspaces/{id}/items` (type: Lakehouse) | `enableSchemas`, naming convention |
| Notebook | `POST /workspaces/{id}/items` (type: Notebook) | `definition` with base64 `.ipynb` content |
| Environment | `POST /workspaces/{id}/items` (type: Environment) | Spark pool config, library management |

---

## Performance Optimization & Resource Management

### Compute Pool Strategy

| Pool | Use Case | Sizing Guidance |
|---|---|---|
| Starter Pool | Development, small datasets, prototyping | < 1 GB workloads |
| Workspace Pool | Production, consistent performance | 1–10 GB workloads |
| Custom Pool | High-memory, GPU, specific VM types | > 10 GB workloads |

### Monitoring

- **Status polling**: Regular checks of job instance status via the monitoring endpoint
- **Failure notifications**: Alert on job failures with `failureReason` from job response
- **Performance tracking**: Monitor execution time trends across job instances
- **Resource usage**: Track compute and memory utilization per pool

---

## Authoring Gotchas and Troubleshooting

| # | Issue | Cause | Resolution |
|---|---|---|---|
| 1 | Notebook creation returns 202 but no item appears | Async operation — must poll `Location` header | Poll `GET {Location}` until `status == "Succeeded"` |
| 2 | `updateDefinition` fails silently | Invalid base64 payload or malformed `.ipynb` | Validate JSON structure before encoding; check `nbformat` version |
| 3 | Duplicate job submissions | POST retried on timeout without checking existing jobs | Query recent job instances before creating new ones |
| 4 | DefaultLakehouse: missing name | Only `id` provided in execution config | Supply both `id` and `name` in `defaultLakehouse` object |
| 5 | Notebook fails at runtime with lakehouse error | Lakehouse was deleted or renamed | Verify lakehouse exists; update `metadata.dependencies` |
| 6 | Pool unavailable error | Workspace pool not configured or at capacity | Check pool configuration or fall back to starter pool |
| 7 | Schema creation fails on lakehouse | `enableSchemas` not set at creation time | Recreate lakehouse with `enableSchemas: true` in `creationPayload` |
| 8 | Content update via generic PATCH doesn't work for notebooks | Generic Items API may not handle notebook-specific format | Use notebook-specific `POST .../updateDefinition` endpoint |
| 9 | Job stuck in NotStarted state | Insufficient compute capacity or pool warming | Wait for pool warm-up; check capacity SKU limits |
| 10 | Cross-lakehouse query fails | Incorrect 3-part naming or missing permissions | Verify `workspace.lakehouse.schema.table` format and access |
| 11 | `getDefinition` POST returns HTTP 411 Length Required | POST sent with no request body | Always add `--body '{}'` (or `-d '{}'`) to `getDefinition` and `updateDefinition` calls |
| 12 | `updateDefinition` returns HTTP 400 with `updateMetadata` error | `updateMetadata: true` included but no `.platform` file part provided | Remove `updateMetadata` flag (or set to `false`) when doing content-only updates |
| 13 | `getDefinition` LRO polling returns `Succeeded` but no content | Caller polled `{Location}` without the `/result` suffix | For `getDefinition`, call `GET {Location}/result` after the poll confirms `Succeeded` |
| 14 | Source lines merge visually in Fabric notebook editor | Lines in `cell['source']` missing `\n` terminators | Ensure every source line (except the last in a cell) ends with `\n` |

---

## Quick Reference: Authoring Decision Guide

| Scenario | Recommended Approach |
|---|---|
| Create lakehouse with schema support | `POST /workspaces/{id}/items` with `enableSchemas: true` |
| Create and deploy notebook in one step | `POST /workspaces/{id}/items` with `definition` block |
| Read existing notebook content | `POST .../notebooks/{id}/getDefinition?format=ipynb` → poll LRO → `GET {Location}/result` → base64 decode |
| Update existing notebook content | `POST .../notebooks/{id}/updateDefinition` with base64-encoded `.ipynb` payload (omit `updateMetadata` flag) |
| Execute notebook on-demand | `POST .../jobs/instances?jobType=RunNotebook` |
| Monitor job completion | `GET .../jobs/instances/{jobInstanceId}` — poll every 10-30s |
| Organize tables in lakehouse | Create schemas via Spark SQL (`CREATE SCHEMA`) |
| Deploy across environments | Parameterize workspace/lakehouse IDs per environment |
| Bulk data processing | Workspace Pool for production; Starter Pool for dev |
| Recover from failed notebook run | Check `failureReason` in job response; fix config and re-submit |

| Version control notebooks | Clear outputs before commit; modular design; markdown documentation |
# COMMON-CORE.md — Microsoft Fabric Core Concepts for Data-Plane Skills

> **Purpose**: Shared reference for all Microsoft Fabric data-plane skills targeting GitHub Copilot CLI, GitHub Copilot, and Claude Code.
> **Language-agnostic** — no SDK code, no CLI commands. Every API reference is a raw REST specification (verb, URL, headers, payload, response).

---

## Fabric Topology & Key Concepts

### Hierarchy

| Concept | Description |
|---|---|
| **Tenant** | Single Fabric instance per organisation, aligned with one Microsoft Entra ID tenant. |
| **Capacity** | Compute pool (F-SKU or P-SKU) powering Fabric workloads. Every workspace must be assigned to a capacity. |
| **Workspace** | Container for Fabric items. Defines collaboration and security boundary. "My workspace" is personal (no workspace identity, no sharing). |
| **Item** | Artefact inside a workspace — Lakehouse, Warehouse, Notebook, SemanticModel, etc. Each has a unique GUID (`itemId`). |
| **OneLake** | Unified tenant-wide data lake. All items store data as Delta/Parquet files in OneLake. |

### Finding Things in Fabric

1. If workspace AND item are specified:
   1. Resolve workspace ID by name if needed (see Resolve Workspace Properties)
   2. Resolve item properties within the workspace (see Resolve Item Properties by Name)
2. If workspace is *not specified*: use the Catalog Search API (see Catalog Search)

*Use APIs exactly as specified — they have implementation limitations.*

## Environment URLs

### Production (Public Cloud)

| Service | URL |
|---|---|
| **Fabric REST API** | `https://api.fabric.microsoft.com/v1/` |
| **OneLake DFS (global)** | `https://onelake.dfs.fabric.microsoft.com` |
| **OneLake DFS (regional)** | `https://<region>-onelake.dfs.fabric.microsoft.com` |
| **OneLake Blob (global)** | `https://onelake.blob.fabric.microsoft.com` |
| **OneLake API (general)** | `https://api.onelake.fabric.microsoft.com` |
| **OneLake API (regional)** | `https://<region>-api.onelake.fabric.microsoft.com` |
| **OneLake Workspace-scoped** | `https://<wsid>.z<xy>.onelake.fabric.microsoft.com` (Private Link) |
| **Warehouse / SQL Endpoint TDS** | `<unique-id>.datawarehouse.fabric.microsoft.com:1433` |
| **SQL Database TDS** | `<unique-id>.database.windows.net:1433` |
| **XMLA Endpoint** | `powerbi://api.powerbi.com/v1.0/myorg/<workspace>` |
| **Entra ID Token Endpoint** | `https://login.microsoftonline.com/<tenantId>/oauth2/v2.0/token` |
| **Power BI REST API** | `https://api.powerbi.com/v1.0/myorg/` |
| **KQL Cluster URI** | `https://trd-<hash>.z<n>.kusto.fabric.microsoft.com` (per-item) |
| **KQL Ingestion URI** | `https://ingest-trd-<hash>.z<n>.kusto.fabric.microsoft.com` (per-item) |
| **Livy Endpoint** | Per-lakehouse: see Lakehouse Settings |

## Authentication & Token Acquisition

### Core Principle

**All** Fabric REST API calls require a **Microsoft Entra ID OAuth 2.0 bearer token**. Fabric does not support API keys, SAS tokens, or SQL authentication for REST APIs.

### Token Audiences / Scopes per Workload

Using the wrong audience is the most common cause of `401 Unauthorized`.

| Access Target | Token Audience / Scope |
|---|---|
| **Fabric REST API** | `https://api.fabric.microsoft.com/.default` |
| **Power BI REST API** (legacy) | `https://analysis.windows.net/powerbi/api/.default` |
| **OneLake** (DFS / Blob) | `https://storage.azure.com/.default` |
| **Warehouse / SQL Endpoint / SQL Database** (TDS) | `https://database.windows.net/.default` |
| **KQL / Kusto** | `https://kusto.kusto.windows.net/.default` (or per-cluster URI) |
| **XMLA Endpoint** | `https://analysis.windows.net/powerbi/api/.default` |
| **Azure Resource Management** | `https://management.azure.com/.default` |

> **OneLake**: Only accepts `https://storage.azure.com/.default`. Using `https://datalake.azure.net/` will fail.
>
> **SQL double-slash gotcha**: With MSAL v1.0 endpoint, the scope must be `https://database.windows.net//.default` (double slash). The v2.0 endpoint handles this correctly.
>
> Ref: https://learn.microsoft.com/en-us/rest/api/fabric/articles/scopes

### Delegated vs Application Permissions

| Flow | Use Case | Notes |
|---|---|---|
| **Delegated** (interactive) | User CLI login | Uses `authorization_code` or `device_code` grant. |
| **Delegated on-behalf-of** | Backend acting for signed-in user | Exchanges user token for downstream resource token. |
| **Application** (client credentials) | Headless automation, CI/CD | Requires Application permissions with admin consent. Fabric admin must enable "Service principals can use Fabric APIs". |

### OAuth 2.0 Token Request (REST)

**Endpoint:** `POST https://login.microsoftonline.com/<tenantId>/oauth2/v2.0/token`

**Client Credentials:**
```
grant_type=client_credentials&client_id=<appId>&client_secret=<secret>&scope=https://api.fabric.microsoft.com/.default
```

**Device Code:**
1. `POST .../oauth2/v2.0/devicecode` with `client_id=<appId>&scope=https://api.fabric.microsoft.com/.default`
2. Poll for token using returned `device_code`.

### Identity Types

| Identity | Description |
|---|---|
| **User principal** | Interactive human user (UPN). Broadest API support. |
| **Service principal (SPN)** | App registration in Entra ID. Requires admin consent + tenant setting. |
| **Managed identity** | Azure-managed (system or user-assigned). Works from Azure compute. |
| **Workspace identity** | Fabric-managed SPN tied to a workspace. Created via workspace settings or `POST .../provisionIdentity`. Used for shortcuts, pipelines, semantic models, Dataflows Gen2. No secret to manage. Cannot be used for programmatic token acquisition from notebooks (as of mid-2025). |

### Entra App Registration Requirements

1. **App Registration**: Create at `https://entra.microsoft.com` > Applications > App registrations.
2. **Redirect URI**: For interactive flows, add `http://localhost` as Mobile/Desktop redirect URI.
3. **API Permissions**: Under **Power BI Service** (where Fabric scopes appear): `Workspace.ReadWrite.All`, `Item.ReadWrite.All`, `OneLake.ReadWrite.All`, etc. For client_credentials: grant Application permissions with admin consent.
4. **Tenant Admin Setting**: Enable "Service principals can use Fabric APIs" in Fabric Admin Portal. Include the SPN/security group in the allowlist.

## Core Control-Plane REST APIs

Base URL: `https://api.fabric.microsoft.com/v1`

All requests require `Authorization: Bearer <token>` and `Content-Type: application/json` for POST/PUT/PATCH.

All requests **must also include the skill-attribution header** `x-ms-fabric-skill: <skill-name>`, where `<skill-name>` is the `name:` value from the calling skill's `SKILL.md` YAML frontmatter (verbatim — also the skill's directory name). This attributes the call to the originating skill for per-skill health and usage (MAU) telemetry; it carries only the skill identifier (no user data or PII) and never alters API behavior. It applies to `api.fabric.microsoft.com` calls only — not OneLake, SQL/TDS, or Kusto. For concrete `az rest`/`curl` examples see [COMMON-CLI.md § Skill Attribution Header](COMMON-CLI.md#skill-attribution-header--x-ms-fabric-skill-required-on-every-fabric-api-call).

Useful response headers: `x-ms-request-id` (troubleshooting), `x-ms-operation-id` (LRO tracking), `Location` (LRO poll URL), `Retry-After` (wait time on 202/429).

### Catalog Search

```
POST /v1/catalog/search
{ "search": "<text>", "filter": "Type eq '<itemType>'", "pageSize": 10, "continuationToken": "..." }
```

**Required delegated scope:** `Catalog.Read.All`

Response: `{ "value": [{ "id", "type", "catalogEntryType", "displayName", "description", "hierarchy": { "workspace": { "id", "displayName" } } }], "continuationToken" }`

* Filter supports `eq`, `ne`, `or`, and parentheses.
* `search` can be empty, allowing filtering by type only.
* Indexing delay: Newly created items can take up to 24 hours to appear in search results.
 
### List Workspaces

```
GET /v1/workspaces[?roles=Admin|Member|Contributor|Viewer][&continuationToken=...]
```

Response: `{ "value": [{ "id", "displayName", "type": "Workspace", "capacityId" }], "continuationToken" }`

### Get Workspace by ID

```
GET /v1/workspaces/<workspaceId>
```

Returns: `id`, `displayName`, `capacityId`, `capacityAssignmentProgress`.

### List Items in a Workspace

```
GET /v1/workspaces/<workspaceId>/items[?type=Lakehouse|Warehouse|...][&continuationToken=...]
```

Response: `{ "value": [{ "id", "displayName", "type", "workspaceId" }], "continuationToken" }`

### List Items in a workspace by Specific Type

Type-specific endpoints return additional `properties` (connection strings, etc.):

```
GET /v1/workspaces/<workspaceId>/{lakehouses|warehouses|notebooks|semanticModels|kqlDatabases|sqlDatabases|dataPipelines|eventstreams|eventhouses|reports|environments}
```

### Get Item by ID

```
GET /v1/workspaces/<workspaceId>/items/<itemId>
```

Or type-specific: `GET /v1/workspaces/<workspaceId>/warehouses/<warehouseId>`

### Resolve Workspace Properties

**Prefer direct ID lookup whenever a workspace UUID is available** (from a prior create response, earlier list result already in context, or explicit user input): call `GET /v1/workspaces/<workspaceId>` directly. Permission-checked direct lookup with no listing or filtering concerns. See [Get Workspace reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace).

**Resolve by name (only when an ID is not available).** The Fabric REST API has no "get workspace by name" endpoint:

1. Call `GET /v1/workspaces`
2. Iterate with pagination until `displayName` matches.

> **Filter on `displayName`, not `name`.** The Workspace object exposes `displayName`, not `name` (see [List Workspaces reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspaces)). JMESPath queries on `name` (filter or projection) return empty / nulls and are easily misread as "workspace not found".

### Resolve Item Properties by Name

When workspace is known:
1. Call `GET /v1/workspaces/<workspaceId>/items?type=<ItemType>`
2. Iterate with pagination until `displayName` matches.

When workspace is not known (cross-workspace discovery):
1. Call `POST /v1/catalog/search` with the item name and optional type filter.
2. If ambiguous, present results and ask the user to disambiguate.

### Get Item Connections

```
GET /v1/workspaces/<workspaceId>/items/<itemId>/connections
```

Returns SQL connection strings, OneLake paths, and other connectivity info.

### Create Workspace

```
POST /v1/workspaces
{ "displayName": "NewWorkspace", "description": "...", "capacityId": "<capacityId>" }
```

**Capacity requirements**: Lakehouse, Warehouse, SparkJobDefinition, and Notebook execution all require workspace capacity. Without it: `FeatureNotAvailable`. Prefer assigning capacity during creation. Alternatively, create workspace first then call `POST /v1/workspaces/{id}/assignToCapacity`. Always verify `capacityAssignmentProgress` is "Completed" before creating capacity-dependent items.

Use `GET /v1/capacities` to discover available capacities (see Capacity Management).

### Workspace Role Assignment

```
POST /v1/workspaces/<workspaceId>/roleAssignments
{ "principal": { "id": "<principalId>", "type": "User|Group|ServicePrincipal" }, "role": "Admin|Member|Contributor|Viewer" }
```

### Provision Workspace Identity

```
POST /v1/workspaces/<workspaceId>/provisionIdentity
```

Response (200/202 LRO): `{ "applicationId", "servicePrincipalId" }`

### Item Creation

```
POST /v1/workspaces/<workspaceId>/items
{ "displayName": "MyItem", "type": "<ItemType>", "description": "..." }
```

Lakehouse creation auto-provisions a SQL analytics endpoint. Response includes `properties.sqlEndpointProperties`, `oneLakeFilesPath`, `oneLakeTablesPath`.

Some item types are asynchronous (follow Long-Running Operations (LRO) pattern).

For items that support definitions (content files), create the item first, then use Update Item Definition to deploy content. For the definition envelope, supported formats, and per-item-type parts, see [ITEM-DEFINITIONS-CORE.md](ITEM-DEFINITIONS-CORE.md).

```
POST /v1/workspaces/<workspaceId>/items/<itemId>/updateDefinition[?updateMetadata=true]
{
  "definition": {
    "format": "<format>",
    "parts": [
      { "path": "<filePath>", "payload": "<base64>", "payloadType": "InlineBase64" }
    ]
  }
}
```

> **Gotcha**: Omitting `?updateMetadata=true` silently ignores the `.platform` part.

### Pagination

All list APIs use **continuation-token-based pagination**.

1. Make the initial `GET` request.
2. If `continuationToken` is non-null, repeat with `?continuationToken=<value>`.
3. Continue until `continuationToken` is null or empty.

You can use `continuationUri` directly. Do **not** modify the token — it is opaque.

### Long-Running Operations (LRO)

> Ref: https://learn.microsoft.com/en-us/rest/api/fabric/articles/long-running-operation

Many mutating operations return `202 Accepted` with:
- `Location` — poll URL
- `x-ms-operation-id` — operation GUID
- `Retry-After` — seconds to wait

**Poll:** `GET /v1/operations/<operationId>` — returns `{ "status": "Running|Succeeded|Failed", "percentComplete" }`

**Get result:** `GET /v1/operations/<operationId>/result` (after `Succeeded`)

**Best practices**: Honour `Retry-After`. Use exponential backoff if absent. Set a max timeout. Handle `Failed` gracefully.

### Rate Limiting & Throttling

HTTP `429 Too Many Requests` includes a `Retry-After` header. The caller **must** wait.

| API Category | Limit |
|---|---|
| Admin APIs | 200 req/hour per principal per tenant |
| General Fabric APIs | Varies by endpoint |
| OneLake ADLS APIs | Standard Azure Storage throttling (per-workspace) |
| Warehouse TDS | ~128 concurrent connections (varies by SKU) |

Implement retry with **exponential backoff + jitter**. Respect `Retry-After`. Avoid tight polling loops. Monitor `x-ms-ratelimit-remaining-*` headers.

## OneLake Data Access

### URL Structure

OneLake uses ADLS Gen2-compatible REST APIs:

```
https://onelake.dfs.fabric.microsoft.com/<workspace>/<item>.<itemtype>/<path>
```

ABFS URI (for Spark): `abfss://<workspace>@onelake.dfs.fabric.microsoft.com/<item>.<itemtype>/<path>`

- `<workspace>` — GUID or display name (use GUID for ABFS — spaces not allowed)
- `<item>.<itemtype>` — e.g. `MySalesLakehouse.Lakehouse`
- `<path>` — `Tables/<tableName>` or `Files/<folder>/<file>`

### OneLake Token Requirement

OneLake **only** accepts `scope = https://storage.azure.com/.default`. Other audiences will return `401 — Audience validation failed`.

### OneLake API Parity with ADLS Gen2

> Ref: https://learn.microsoft.com/en-us/fabric/onelake/onelake-api-parity

Key differences from standard ADLS Gen2:
- Cannot create/delete workspaces or items via ADLS APIs — use Fabric REST API.
- Cannot modify permissions via ADLS APIs.
- HEAD calls only at workspace/tenant levels.
- Ignored headers reported in `x-ms-rejected-headers`.

### OneLake Shortcuts

Virtual pointers to other storage (OneLake, ADLS Gen2, S3, GCS):

```
POST /v1/workspaces/<workspaceId>/items/<lakehouseId>/shortcuts
{
  "path": "Tables/external_data",
  "name": "my_shortcut",
  "target": {
    "oneLake": {
      "workspaceId": "<sourceWorkspaceId>",
      "itemId": "<sourceItemId>",
      "path": "Tables/source_table"
    }
  }
}
```

## Job Execution

### Run On-Demand Job

```
POST /v1/workspaces/<workspaceId>/items/<itemId>/jobs/instances?jobType=<jobType>
```

| Item Type | jobType |
|---|---|
| Notebook | `RunNotebook` |
| DataPipeline | `Pipeline` |
| SparkJobDefinition | `SparkJob` |
| SemanticModel | `Refresh` |

> **Gotcha**: `DefaultJob` does **not** work for most item types. Use the type-specific value.

Response: `202 Accepted` with `Location` and `x-ms-operation-id` headers.

### Get / Cancel Job

```
GET  /v1/workspaces/<workspaceId>/items/<itemId>/jobs/instances/<jobInstanceId>
POST /v1/workspaces/<workspaceId>/items/<itemId>/jobs/instances/<jobInstanceId>/cancel
```

### Job Scheduling

```
POST /v1/workspaces/<workspaceId>/items/<itemId>/jobs/<jobType>/schedules
{
  "enabled": true,
  "configuration": {
    "startDateTime": "2026-01-01T06:00:00.000Z",
    "endDateTime": "2027-01-01T06:00:00.000Z",
    "type": "Daily",
    "interval": 1,
    "localTimeZoneId": "UTC",
    "times": ["06:00"]
  }
}
```

**Required fields**: `enabled`, `configuration.startDateTime`, `configuration.endDateTime`, `configuration.type`

`type` values: `Daily`, `Weekly` (also requires `weekDays`), `Monthly`.

```
GET    /v1/workspaces/<workspaceId>/items/<itemId>/jobs/<jobType>/schedules
DELETE /v1/workspaces/<workspaceId>/items/<itemId>/jobs/<jobType>/schedules/<scheduleId>
```

## Capacity Management

### List Capacities

```
GET /v1/capacities
```

Response: `{ "value": [{ "id", "displayName", "sku", "region", "state" }] }`

Filter to `"state": "Active"`. If empty, user must provision capacity via Fabric portal or Azure.

### Assign Workspace to Capacity

```
POST /v1/workspaces/<workspaceId>/assignToCapacity
{ "capacityId": "<capacityId>" }
```

Verify `capacityAssignmentProgress` is "Completed" before creating items.

## Gotchas, Best Practices & Troubleshooting

### Common Errors

| Error | Likely Cause | Resolution |
|---|---|---|
| `401 Unauthorized` | Wrong token audience, expired token, or insufficient permissions | Verify `aud` claim in JWT (decode at jwt.ms). Ensure correct scope (see Token Audiences / Scopes per Workload). |
| `403 Forbidden` | Missing workspace role or item permission | Check role assignments. For SPNs: verify admin portal settings. |
| `404 Not Found` | Wrong workspace/item ID or item deleted | Re-resolve the workspace/item. |
| `429 Too Many Requests` | Rate limit exceeded | Wait for `Retry-After`, then retry. |
| `PrincipalTypeNotSupported` | SPN used where only user principal is supported | Some APIs are user-only — check docs. |
| `Login failed... database not found` | Wrong `Initial Catalog` in SQL connection | Use item display name, not FQDN. Verify workspace role. |
| Token size limit | Too many Entra groups or SQL items | Limit groups per user; keep SQL items per workspace <= 40. |
| TDS connection timeout | Port 1433 blocked or TDS redirect blocked | Open outbound TCP 1433. Allow `*.datawarehouse.fabric.microsoft.com` and `*-pbidedicated.windows.net`. |

### Best Practices

- **Parameterise all URLs** — base URL, workspace ID, item ID, token audience.
- **Use type-specific list endpoints** when item properties are needed (e.g. `.../warehouses` returns `connectionString`).
- **Check before creating** — implement idempotent operations.
- **Handle LROs universally** — wrap all mutating calls in an LRO-aware handler.
- **Log `x-ms-request-id`** from responses for support requests.
- **Cache workspace/item metadata** — avoid repeated list calls.
- **Filter with query parameters** — `?type=Lakehouse` reduces response size.
- **Use regional OneLake endpoints** to reduce latency.
- **Use Entra ID with least-privilege scopes** — `Read.All` when write isn't needed.
- **Prefer certificates or managed identities** over client secrets.
- **Store secrets in Key Vault** — never in source code or plain-text config.
- **Distinguish transient vs permanent errors** — retry 429/503/504; fix 400/403/404.
- URL-encode display names in URLs. Prefer GUIDs for programmatic access.
- Current API version: `v1`. The `preview` parameter is deprecated in favour of `beta` (supported until March 31, 2026).

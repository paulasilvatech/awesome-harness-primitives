# Notebook Context Resolution — Property Sources & Resolution Strategy

How to resolve the notebook execution context (workspace, lakehouse, environment) before generating or modifying code.

## Strategy

**Read from local files first; fall back to Fabric REST APIs only when local data is missing.** This minimizes network calls and avoids unnecessary latency.

> **VS Code only** — The local file resolution (lighter-config.json, .workspace-info, .artifact-info) is only available when the notebook has been synced to a local workspace via the VS Code Fabric extension. Portal-only users will not have these files; skip to Step 5 (API calls) in that case.

---

## Local File Structure

```text
{workspace_id}/
├── .workspace-info                          # workspace metadata (JSON) — redundant if lighter-config.json exists
└── SynapseNotebook/{artifact_id}/
    ├── .artifact-info                       # artifact metadata (JSON) — redundant if lighter-config.json exists
    ├── conf/lighter-config.json             # session launcher config (JSON) — PRIMARY source
    └── {artifact_name}/{artifact_name}.ipynb # notebook content (ipynb JSON)
```

---

## Resolution Steps

### Step 1 — Identify the target notebook

- Target = the notebook file the user wants to modify or generate code for.
- If user specifies a notebook name, locate `.ipynb` at: `{workspace_id}/SynapseNotebook/{artifact_id}/{artifact_name}/{artifact_name}.ipynb`
- If no notebook is specified and no context is available, **STOP** and ask the user which notebook to target.

### Step 2 — Read `lighter-config.json` (primary local source)

Path: `{workspace_id}/SynapseNotebook/{artifact_id}/conf/lighter-config.json`

This single file provides nearly all context fields:

| Fields Available |
|---|
| `workspace_id`, `workspace_name`, `capacity_id` |
| `artifact_id`, `artifact_name` |
| `lakehouse_id`, `lakehouse_name`, `lakehouse_workspace_id` |
| `tenant_id`, `host`, `platform` |
| `auth`, `client_id`, `scope_url`, `session_pool_id`, `refresh_token` |

> `workspace_name` may be missing in older versions — fall back to `.workspace-info` → `.name` if needed.

### Step 3 — Read ipynb metadata (for dependencies)

From `{name}/{name}.ipynb` → `metadata.dependencies`:

- **Lakehouse**: `default_lakehouse` (id), `default_lakehouse_name`, `default_lakehouse_workspace_id`, `known_lakehouses[]` (ids only)
- **Environment**: `environmentId`, `workspaceId` (the attached Environment artifact)

### Step 4 — Fallback to `.workspace-info` / `.artifact-info`

Only if `lighter-config.json` does not exist (notebook never launched):

| File | Fields |
|---|---|
| `.workspace-info` | `workspace_id` (`.id`), `workspace_name` (`.name`), `capacity_id` (`.capacityObjectId`) |
| `.artifact-info` | `artifact_id` (`.objectId`), `artifact_name` (`.displayName`) |

### Step 5 — API calls for missing data

Use Fabric REST APIs only for data not available locally:

| Missing Data | API Call |
|---|---|
| `known_lakehouses` name/details | `GET /v1/workspaces/{wsId}/lakehouses/{lhId}` (per entry) |
| `environment_name` | `GET /v1/workspaces/{envWsId}/environments/{envId}` → `.displayName` |
| `workspace_name` / `capacity_id` | `GET /v1/workspaces/{wsId}` |
| `lakehouse_workspace_capacity_id` (cross-ws) | `GET /v1/workspaces/{lhWsId}` → `.capacityId` |
| `tenant_id` | `az account show` → `.tenantId` |

### Step 6 — Validate environment completeness

Required fields: `workspace_id`, `capacity_id`

If any required field is missing → **STOP** and notify user:
> "⚠️ Missing critical Fabric environment context (`workspace_id`, `capacity_id`). Please ensure the notebook has been synced from a Fabric workspace, or provide these values manually."

---

## Property Resolution Table

| Property | Primary Source (Local) | Fallback Source (API) |
|---|---|---|
| `workspace_id` | `lighter-config.json` → `.platform_config.workspace_id` | folder name or `GET /v1/workspaces` |
| `workspace_name` | `lighter-config.json` → `.platform_config.workspace_name` | `GET /v1/workspaces/{wsId}` → `.displayName` |
| `capacity_id` | `lighter-config.json` → `.platform_config.capacity_id` | `GET /v1/workspaces/{wsId}` → `.capacityId` |
| `artifact_id` | `lighter-config.json` → `.platform_config.artifact_id` | folder name |
| `artifact_name` | `lighter-config.json` → `.platform_config.artifact_name` | `GET /v1/workspaces/{wsId}/notebooks/{nbId}` → `.displayName` |
| `tenant_id` | `lighter-config.json` → `.platform_config.tenant_id` | `az account show` → `.tenantId` |
| `lakehouse_id` | `lighter-config.json` → `.platform_config.lakehouse_id` | `ipynb` → `.metadata.dependencies.lakehouse.default_lakehouse` |
| `lakehouse_name` | `lighter-config.json` → `.platform_config.lakehouse_name` | `GET /v1/workspaces/{wsId}/lakehouses/{lhId}` → `.displayName` |
| `lakehouse_workspace_id` | `lighter-config.json` → `.platform_config.lakehouse_workspace_id` | `ipynb` → `.metadata.dependencies.lakehouse.default_lakehouse_workspace_id` |
| `known_lakehouses` | `ipynb` → `.metadata.dependencies.lakehouse.known_lakehouses` (id only) | Per entry: `GET /v1/workspaces/{wsId}/lakehouses/{lhId}` |
| `environment_id` | `ipynb` → `.metadata.dependencies.environment.environmentId` | — |
| `environment_name` | — (not stored locally) | `GET /v1/workspaces/{envWsId}/environments/{envId}` → `.displayName` |
| `host` | `lighter-config.json` → `.platform_config.host` | LRO `Location` header |
| `platform` | `lighter-config.json` → `.platform` | — |

---

## Important Notes

- **`lighter-config.json` is the primary local source** — if it exists, `.workspace-info` and `.artifact-info` are redundant.
- **`known_lakehouses`** in ipynb only stores IDs. To resolve names and workspace details, API calls are required per entry.
- **`environment_id`** is only present when an Environment is explicitly attached to the notebook. `environment_name` always requires an API call.
- **Static/auth fields** (`authority`, `client_id`, `scope_url`, `auth`) are effectively constants — no resolution needed.
- **`envType`** is not stored anywhere — determined by the runtime environment.

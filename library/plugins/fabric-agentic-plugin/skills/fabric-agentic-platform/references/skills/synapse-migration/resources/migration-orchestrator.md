# Migration Orchestrator — Synapse → Fabric

Automated end-to-end migration workflow. Two modes:

- **Lift-and-shift**: User provides source and target workspace — nothing else. All decisions are auto-resolved with sensible defaults. Notebooks and SJDs are migrated as-is; Environments mirror Synapse pools exactly; databases become schemas in one Lakehouse.
- **Migrate-and-modernize**: User provides source and target workspace, then the orchestrator asks guided questions at each decision point (mapping mode, non-Delta handling, code refactoring, etc.).

> **How to use**: The user says "migrate workspace X to workspace Y" and picks a strategy. For lift-and-shift, that's all — zero further inputs.

---

## Required Inputs

Collect these from the user before starting:

| Input | Example | How to Obtain |
|---|---|---|
| Synapse workspace name | `my-synapse-ws` | User provides (name or URL) |
| Synapse resource group | `my-rg` | Parse from workspace URL, or user provides, or discover via ARM |
| Azure subscription ID | `xxxxxxxx-xxxx-...` | Parse from workspace URL, or user provides, or `az account show` |
| Fabric workspace name or ID | `Migration-Target` | User provides |
| Migration strategy | `lift-and-shift` or `migrate-and-modernize` | Ask user — see [§ Strategy Decision](#step-0-strategy-decision) |

> **URL parsing**: If the user provides a Synapse Studio URL, extract all three values from the embedded ARM path:
> `https://web.azuresynapse.net/en/home?workspace=%2Fsubscriptions%2F{subId}%2FresourceGroups%2F{rg}%2Fproviders%2FMicrosoft.Synapse%2Fworkspaces%2F{wsName}`
> This eliminates the need to ask for resource group and subscription ID separately.

### Derived Values (Auto-Discovered)

| Value | Derived From |
|---|---|
| Synapse data-plane endpoint | `https://{workspaceName}.dev.azuresynapse.net` |
| Fabric workspace ID | `GET /v1/workspaces` → filter by `displayName` |
| ARM base path | `/subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.Synapse/workspaces/{ws}` |

### Parsing a Synapse Workspace URL

```python
import re
from urllib.parse import unquote

def parse_synapse_url(url):
    """Extract subscription_id, resource_group, workspace_name from a Synapse Studio URL."""
    decoded = unquote(url)
    m = re.search(
        r'/subscriptions/([^/]+)/resourceGroups/([^/]+)/providers/Microsoft\.Synapse/workspaces/([^/?\s&]+)',
        decoded, re.IGNORECASE
    )
    if m:
        return {"subscription_id": m.group(1), "resource_group": m.group(2), "workspace_name": m.group(3)}
    return None
```

If the user provides a URL, call this first. Only ask for resource group / subscription ID if parsing fails or the user provides just a workspace name.

---

## Orchestration Flow

```
Migration Orchestrator:
│
├── Step 0: Strategy decision (lift-and-shift vs. migrate-and-modernize)
├── Step 1: Authenticate (acquire 3 tokens)
├── Step 2: Full inventory (Spark pools, databases, notebooks, SJDs)
│
├── Phase 0: Spark Pools → Environments
│   ├── Execute spark-pool-migration.md Steps 1–6
│   ├── ⏸ GATE: Validate Environments (V1)
│   └── Output: poolMappings JSON
│
├── Phase 1: Lake Databases / HMS → Lakehouses
│   ├── Detect: built-in vs. external HMS
│   ├── Execute lake-database-migration.md or external-hms-migration.md
│   ├── ⏸ GATE: Validate data (V2)
│   └── Output: lakehouseMappings JSON
│
├── Phase 1b: Storage Path Inventory (migrate-and-modernize only)
│   ├── Scan notebook/SJD code for abfss:// paths
│   ├── Deduplicate by storage account + container
│   ├── Create OneLake shortcuts for each unique container
│   └── Output: shortcutMappings JSON (consumed by Phase 2 path rewriting)
│
├── Phase 2: Notebooks → Fabric Notebooks
│   ├── Execute spark-item-migration.md Phase 2 Steps 1–6
│   ├── ⏸ GATE: Validate notebooks (V3)
│   └── Output: notebookMappings JSON
│
├── Phase 3: SJDs → Fabric SJDs
│   ├── Execute spark-item-migration.md Phase 3 Steps 1–4
│   ├── ⏸ GATE: Validate SJDs (V4)
│   └── Output: sjdMappings JSON
│
├── Final Validation: V5 (query comparison) + V6 (full report)
│
├── Migration Report: Query Fabric workspace → generate Markdown
│   ├── Per-phase tables with clickable portal links
│   ├── Blockers & post-migration actions
│   └── Output: migration-report-{migrationId}.md
│
└── (Optional) Security & Governance — for production deployment
    └── Apply when promoting validated migration to production
```

---

## Step 0: Strategy Decision

Ask the user which migration strategy to use:

| Strategy | User Inputs | Auto-Resolved Defaults | When to Use |
|---|---|---|---|
| **Lift-and-shift** | Source workspace + target workspace only | All decision points auto-resolved (see table below) | Fast migration; team will refactor post-cutover |
| **Migrate-and-modernize** | Source + target workspace, then guided decisions per phase | None — user makes every choice | Clean migration; items ready to run in Fabric |

### Lift-and-Shift Defaults

When strategy is `lift-and-shift`, the orchestrator auto-resolves every decision point with no user input:

| Decision Point | Auto-Resolved To | Rationale |
|---|---|---|
| Phase 0: Starter Pool vs Environment? | **Always create Environment** — mirror the Synapse pool exactly (pool size, libraries, Spark config) | Preserves pool→notebook/SJD binding; notebooks run against identical compute settings |
| Phase 0: Spark version? | **Runtime 1.3** (Spark 3.5) — upgrade from 3.3/3.4 | Older runtimes are EOL |
| Phase 1: Mapping mode? | **Mode A** — all databases → schemas in one Lakehouse | Simplest; least items to create |
| Phase 1: Non-Delta tables? | **Option A** — convert to Delta | Delta-first aligns with Fabric; full catalog registration |
| Phase 1: External HMS databases? | **Migrate all databases** | No selection needed |
| Phase 1: External HMS credentials? | **Ask user** (only exception — credentials cannot be auto-resolved) | Security requirement |
| Phase 2: Code refactoring? | **Skip** — migrate notebooks as-is | User will refactor post-cutover |
| Phase 2: Strip Synapse fields? | **Skip** — Fabric ignores unrecognized fields | Preserves original notebook structure |
| Phase 2: Lakehouse binding? | **Auto-bind** — first Lakehouse created in Phase 1 | Every notebook needs a default Lakehouse |
| Phase 2: Environment binding? | **Auto-bind** — use `poolMappings` from Phase 0 to match notebook's original `bigDataPool` | Preserves pool→notebook association |
| Phase 3: Code/path updates? | **Skip** — migrate SJDs as-is | User will refactor post-cutover |
| Phase 3: Pool → Environment remap? | **Auto-bind** — use `poolMappings` from Phase 0 | Preserves pool→SJD association |

> **Only exception**: External HMS JDBC credentials must always be provided by the user — there is no safe default.

Store the choice — it determines the behavior of every subsequent phase.

---

## Step 1: Authenticate

Acquire three tokens and verify access. Use a `TokenManager` class to handle automatic refresh — Azure AD tokens expire after ~60 minutes, and large workspace migrations (50+ items) routinely exceed this.

> **Token audiences** (see [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) for base `az login` flows):
> - ARM: `https://management.azure.com`
> - Synapse data-plane: `https://dev.azuresynapse.net`
> - Fabric: `https://api.fabric.microsoft.com`

### Token Manager

```python
import subprocess, json, requests, time, shutil

def get_token(resource):
    """Acquire a token via az CLI."""
    az_path = shutil.which("az")
    if not az_path:
        raise RuntimeError(f"az CLI not found in PATH")
    result = subprocess.run(
        [az_path, "account", "get-access-token", "--resource", resource,
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

class TokenManager:
    """Auto-refreshing token manager for multi-phase migrations.
    Tokens expire after ~60 min. For large workspaces (50+ items),
    migration routinely exceeds this. The manager detects 401 responses
    and transparently re-acquires all three tokens."""

    def __init__(self):
        self.refresh_all()

    def refresh_all(self):
        self.arm = get_token("https://management.azure.com")
        self.synapse = get_token("https://dev.azuresynapse.net")
        self.fabric = get_token("https://api.fabric.microsoft.com")
        self._update_headers()

    def _update_headers(self):
        self.arm_headers = {"Authorization": f"Bearer {self.arm}"}
        self.syn_headers = {"Authorization": f"Bearer {self.synapse}"}
        self.fab_headers = {
            "Authorization": f"Bearer {self.fabric}",
            "Content-Type": "application/json"
        }

    def refresh_if_needed(self, resp):
        """If response is 401 TokenExpired, refresh all tokens and return True."""
        if resp.status_code == 401:
            self.refresh_all()
            return True
        return False

tokens = TokenManager()
```

> **Why all three tokens?** When one expires, the others are likely close to expiry too. Refreshing all three at once avoids cascading 401s across phases.

> **Usage pattern**: After every Fabric/Synapse API call, check for 401 and retry once:
> ```python
> resp = requests.post(url, headers=tokens.fab_headers, json=payload)
> if tokens.refresh_if_needed(resp):
>     resp = requests.post(url, headers=tokens.fab_headers, json=payload)
> ```

### Verify Access

```python
# Verify Synapse ARM access
resp = requests.get(
    f"https://management.azure.com/subscriptions/{sub_id}/resourceGroups/{rg}"
    f"/providers/Microsoft.Synapse/workspaces/{ws_name}?api-version=2021-06-01",
    headers=tokens.arm_headers
)
assert resp.status_code == 200, f"ARM access failed: {resp.status_code} {resp.text}"

# Verify Synapse data-plane access
resp = requests.get(
    f"https://{ws_name}.dev.azuresynapse.net/notebooks?api-version=2020-12-01",
    headers=tokens.syn_headers
)
assert resp.status_code == 200, f"Synapse data-plane access failed: {resp.status_code}"

# Resolve Fabric workspace ID
resp = requests.get(
    "https://api.fabric.microsoft.com/v1/workspaces",
    headers=tokens.fab_headers
)
workspaces = resp.json()["value"]
fabric_ws = next((w for w in workspaces if w["displayName"] == fabric_ws_name), None)
assert fabric_ws, f"Fabric workspace '{fabric_ws_name}' not found"
fabric_ws_id = fabric_ws["id"]
```

### Idempotent Resume

Migrations can be interrupted by token expiry, network errors, or API throttling. The orchestrator **must** be idempotent — re-running it should skip already-created items and continue from where it left off.

Before each phase, query existing items of that type and build a `displayName → id` lookup:

```python
def existing_items_map(item_type):
    """Get map of displayName → id for existing items. Used to skip duplicates on resume."""
    resp = requests.get(
        f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/items?type={item_type}",
        headers=tokens.fab_headers
    )
    if tokens.refresh_if_needed(resp):
        resp = requests.get(
            f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/items?type={item_type}",
            headers=tokens.fab_headers
        )
    result = {}
    if resp.status_code == 200:
        for item in resp.json().get("value", []):
            result[item["displayName"]] = item["id"]
    return result
```

At the start of each phase:
```python
# Phase 0 example
existing_envs = existing_items_map("Environment")
for pool in pools:
    env_name = f"{pool_name}_env"
    if env_name in existing_envs:
        env_id = existing_envs[env_name]
        # Record in mappings and skip creation
        continue
    # ... create new Environment
```

> **Why this matters**: In production testing, a workspace with 22 pools + 50 notebooks exhausted the Fabric token (~60 min lifetime) partway through Phase 2. Without idempotent resume, the operator would need to manually delete partial results and restart. With it, re-running the script picked up exactly where it left off — 14 notebooks skipped, 36 newly created.

---

## Step 2: Full Inventory

Run all inventory queries in one pass to give the user a complete picture before any migration begins.

### 2a. Spark Pools (ARM API)

```python
pools_resp = requests.get(
    f"https://management.azure.com/subscriptions/{sub_id}/resourceGroups/{rg}"
    f"/providers/Microsoft.Synapse/workspaces/{ws_name}/bigDataPools?api-version=2021-06-01",
    headers=tokens.arm_headers
)
pools = pools_resp.json()["value"]
```

### 2b. Detect External HMS

For each pool, check `properties.sparkConfigProperties.content` for `spark.hadoop.javax.jdo.option.ConnectionURL`. If found, flag as external HMS.

```python
external_hms_pools = []
for pool in pools:
    config_content = pool.get("properties", {}).get("sparkConfigProperties", {}).get("content", "")
    if "javax.jdo.option.ConnectionURL" in config_content:
        external_hms_pools.append(pool["name"])
has_external_hms = len(external_hms_pools) > 0
```

### 2c. Lake Databases (Data Plane API)

```python
dbs_resp = requests.get(
    f"https://{ws_name}.dev.azuresynapse.net/databases?api-version=2021-04-01",
    headers=tokens.syn_headers
)
databases = [db for db in dbs_resp.json().get("value", [])
             if db.get("properties", {}).get("origin", {}).get("type") != "SQLOD"]
```

For each database, fetch tables:

```python
all_tables = {}
for db in databases:
    db_name = db["name"]
    tables_resp = requests.get(
        f"https://{ws_name}.dev.azuresynapse.net/databases/{db_name}/TABLEs?api-version=2021-04-01",
        headers=tokens.syn_headers
    )
    all_tables[db_name] = tables_resp.json().get("value", [])
```

### 2d. Notebooks (Data Plane API)

```python
notebooks_resp = requests.get(
    f"https://{ws_name}.dev.azuresynapse.net/notebooks?api-version=2020-12-01",
    headers=tokens.syn_headers
)
notebooks = notebooks_resp.json()["value"]
# Handle pagination
while "nextLink" in notebooks_resp.json():
    notebooks_resp = requests.get(notebooks_resp.json()["nextLink"],
                                  headers=tokens.syn_headers)
    notebooks.extend(notebooks_resp.json()["value"])
```

### 2e. Spark Job Definitions (Data Plane API)

```python
sjds_resp = requests.get(
    f"https://{ws_name}.dev.azuresynapse.net/sparkJobDefinitions?api-version=2020-12-01",
    headers=tokens.syn_headers
)
sjds = sjds_resp.json()["value"]
```

### 2f. Compute Inventory Metrics

```python
gpu_count = sum(
    1 for p in pools
    if "GPU" in p.get("properties", {}).get("nodeSizeFamily", "")
)
delta_count = sum(
    1 for tables in all_tables.values() for t in tables
    if t.get("properties", {}).get("storageDescriptor", {}).get("format", {}).get("formatType", "").lower() == "delta"
)
non_delta_count = sum(len(t) for t in all_tables.values()) - delta_count
```

### 2g. Present Inventory Summary

Present this to the user and ask for confirmation before proceeding:

```
╔══════════════════════════════════════════════════════════════════╗
║                    SYNAPSE WORKSPACE INVENTORY                  ║
║  Source: {ws_name}                                              ║
║  Target: {fabric_ws_name} ({fabric_ws_id})                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Spark Pools:        {len(pools)}                               ║
║    - GPU pools:      {gpu_count} (MIGRATION BLOCKER if > 0)    ║
║    - External HMS:   {len(external_hms_pools)} pools            ║
║                                                                  ║
║  Lake Databases:     {len(databases)}                           ║
║    - Total tables:   {sum(len(t) for t in all_tables.values())} ║
║    - Delta tables:   {delta_count}                              ║
║    - Non-Delta:      {non_delta_count}                          ║
║                                                                  ║
║  Notebooks:          {len(notebooks)}                           ║
║  Spark Job Defs:     {len(sjds)}                                ║
║                                                                  ║
║  Strategy:           {strategy}                                 ║
║  HMS Type:           {"External" if has_external_hms else "Built-in"} ║
╚══════════════════════════════════════════════════════════════════╝
```

> **Ask user**: "Proceed with migration? (yes/no)"
>
> If GPU pools exist, warn: "GPU pools cannot be migrated to Fabric. These pools and their bound notebooks/SJDs will be skipped."

---

## Phase 0: Spark Pools → Environments

Follow [spark-pool-migration.md](spark-pool-migration.md) Steps 1–7.

### Orchestrator Actions

**Lift-and-shift**: Create an Environment for **every** pool (skip GPU pools). Mirror the Synapse pool exactly — same node size, same libraries, same Spark config. No decision tree; no Starter Pool optimization.

**Migrate-and-modernize**: For each pool, apply the decision tree from spark-pool-migration.md Step 2 → determine Starter Pool vs. Environment vs. Custom Pool. Ask the user to confirm choices.

1. **For each pool** (skip GPU pools):
   - **Lift-and-shift**: Always create Environment with full pool config (Custom Pool definition + libraries + Spark config)
   - **Migrate-and-modernize**: Apply decision tree → Starter Pool, librariesOnly, or customPool
   - After `POST /environments` → 201, call `updateDefinition` with retry (handles post-creation race condition):

```python
import time, requests

def update_env_definition(workspace_id, env_id, definition_payload, max_retries=3):
    """Upload Environment definition with retry for post-creation race condition
    and automatic token refresh on 401.
    After POST /environments → 201, the updateDefinition endpoint may return 404
    for a few seconds while the Environment is provisioned."""
    url = (f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"
           f"/environments/{env_id}/updateDefinition")
    for attempt in range(1, max_retries + 1):
        resp = requests.post(url, headers=tokens.fab_headers, json=definition_payload)
        if resp.status_code == 401:
            tokens.refresh_if_needed(resp)
            resp = requests.post(url, headers=tokens.fab_headers, json=definition_payload)
            return resp
        if resp.status_code == 404 and attempt < max_retries:
            time.sleep(3 * attempt)  # 3s, 6s backoff
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
```

2. **Wait for all publishes** to complete (poll LRO until `Succeeded`)

3. **Build `poolMappings` JSON** (Step 6 output)

4. **Run Phase 0 Gate** (Step 7):

```python
# Validate every Environment
for pool_name, mapping in pool_mappings.items():
    if mapping["mode"] == "starterPool":
        continue
    env_id = mapping["fabricEnvironmentId"]
    resp = requests.get(
        f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/environments/{env_id}",
        headers=tokens.fab_headers
    )
    publish_state = resp.json()["properties"]["publishDetails"]["state"]
    assert publish_state == "Success", f"Environment {pool_name}_env publish failed: {publish_state}"
```

> **Gate decision**: If any Environment failed to publish → stop and present the error. Do not proceed to Phase 1.

### Phase 0 Output

```json
{
  "poolMappings": {
    "{poolName}": {
      "fabricEnvironmentId": "{envId}",
      "fabricEnvironmentName": "{poolName}_env",
      "mode": "customPool | librariesOnly | starterPool"
    }
  }
}
```

---

## Phase 1: Lake Databases / HMS → Lakehouses

### Route Decision

```
Has external HMS? (detected in Step 2b)
├── YES → Follow external-hms-migration.md Steps 0–8
│         (JDBC connection details needed — ask user for credentials, even in lift-and-shift)
└── NO  → Follow lake-database-migration.md Steps 1–8
```

> If the workspace has **both** built-in Lake Databases and external HMS pools, run **both** guides. In lift-and-shift, auto-detect which databases belong to which metastore. In migrate-and-modernize, ask the user.

### Mapping Mode

**Lift-and-shift**: Auto-select **Mode A** (all databases → schemas in one Lakehouse named `{ws_name}_Lakehouse`). No user input.

**Migrate-and-modernize**: Present the databases and ask which mapping mode to use:

```
Databases found: sales, marketing, staging, default

Choose mapping mode:
  A) Schemas — all databases → schemas in one Lakehouse (simplest)
  B) Separate — each database → its own Lakehouse (most isolation)
  C) Hybrid — assign each database individually (most flexible)
```

For Mode C, ask the user to provide the assignment map (see lake-database-migration.md § Mode C).

### Orchestrator Actions

1. **Create Lakehouse(es)**:
   - **Lift-and-shift**: One Lakehouse, schemas enabled, all databases → schemas
   - **Migrate-and-modernize**: Based on user's chosen mode
2. **Create schemas** (Mode A / Mode C schema assignments)
3. **For each table**: determine format → create shortcut (Delta → `Tables/`, non-Delta → `Files/`)
4. **Handle non-Delta tables**:
   - **Lift-and-shift**: Auto-select Option A (convert to Delta)
   - **Migrate-and-modernize**: Ask user — Option A / Option B / per-table
5. **Build `lakehouseMappings` JSON**

6. **Run Phase 1 Gate** (Step 8):

```python
# Validate shortcuts
for db_name, tables in all_tables.items():
    schema = lakehouse_mappings[db_name]["schema"]
    for table in tables:
        table_name = table["name"]
        format_type = table["properties"]["storageDescriptor"]["format"]["formatType"]
        section = "Tables" if format_type == "delta" else "Files"
        # List shortcut contents via Fabric API or notebook
        # Verify shortcut resolves without error
```

> **Gate decision**: If any shortcut fails to resolve or row counts don't match → stop and present the error. Do not proceed to Phase 2.

### Phase 1 Output

```json
{
  "lakehouseMappings": {
    "{databaseName}": {
      "lakehouseId": "{lhId}",
      "lakehouseName": "{lhName}",
      "schema": "{fabricSchemaName}",
      "mode": "dedicated | schema"
    }
  }
}
```

---

## Phase 1b: Storage Path Inventory & Shortcut Creation (Migrate-and-Modernize Only)

> **Lift-and-shift**: Skip this phase entirely. Notebooks keep their original `abfss://` paths, which continue to work as long as the Fabric workspace identity has `Storage Blob Data Reader` on the source storage accounts.

### Purpose

Synapse notebooks often read/write data via direct `abfss://` paths that are **not registered** as Lake Database tables. These paths won't appear in Phase 1's inventory. Phase 1b scans notebook and SJD code for these paths, creates shortcuts, and produces a mapping so Phase 2 can rewrite the paths to OneLake-relative paths.

### Step 1: Scan Notebooks and SJDs for Storage Paths

```python
import re

abfss_pattern = re.compile(
    r'abfss://([^@]+)@([^.]+)\.dfs\.core\.windows\.net/([^\s\'")\]]*)'
)

storage_refs = {}  # key: (container, account) → set of subpaths

for nb in notebooks:
    for cell in nb["properties"]["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        for match in abfss_pattern.finditer(source):
            container, account, subpath = match.groups()
            key = (container, account)
            # Extract the top-level directory as the shortcut target
            top_dir = subpath.split("/")[0] if subpath else ""
            storage_refs.setdefault(key, set()).add(top_dir)

for sjd in sjds_source:
    file_path = sjd["properties"].get("jobProperties", {}).get("file", "")
    for match in abfss_pattern.finditer(file_path):
        container, account, subpath = match.groups()
        key = (container, account)
        top_dir = subpath.split("/")[0] if subpath else ""
        storage_refs.setdefault(key, set()).add(top_dir)
```

### Step 2: Filter Out Already-Shortcutted Paths

Remove any storage paths that were already covered by Phase 1 shortcuts (Lake Database tables):

```python
# phase1_shortcuts: set of (container, account) already covered by Phase 1
phase1_shortcuts = set()
for db_name, mapping in lakehouse_mappings.items():
    for table in mapping.get("tables", []):
        loc = table.get("sourceLocation", "")
        m = abfss_pattern.match(loc)
        if m:
            phase1_shortcuts.add((m.group(1), m.group(2)))

# Only create shortcuts for paths NOT already covered
new_shortcuts = {k: v for k, v in storage_refs.items() if k not in phase1_shortcuts}
```

### Step 3: Create Shortcuts

Create one OneLake shortcut per unique (container, account) pair, targeting the Lakehouse from Phase 1:

```python
lakehouse_id = list(lakehouse_mappings.values())[0]["lakehouseId"]  # primary Lakehouse

shortcut_mappings = {}

for (container, account), subdirs in new_shortcuts.items():
    shortcut_name = f"{account}_{container}"  # e.g., "mystorageaccount_raw"
    payload = {
        "name": shortcut_name,
        "path": "Files",
        "target": {
            "type": "AdlsGen2",
            "adlsGen2": {
                "location": f"https://{account}.dfs.core.windows.net",
                "subpath": f"/{container}",
                "connectionId": adls_connection_id
            }
        }
    }
    resp = requests.post(
        f"{BASE_URL}/workspaces/{fabric_ws_id}/items/{lakehouse_id}/shortcuts",
        headers=tokens.fab_headers,
        json=payload
    )
    if resp.status_code == 409:
        # Shortcut already exists — reuse it
        pass
    else:
        resp.raise_for_status()

    # Build the path mapping: original abfss:// → OneLake relative path
    shortcut_mappings[(container, account)] = {
        "shortcutName": shortcut_name,
        "lakehouseId": lakehouse_id,
        "onelakePath": f"Files/{shortcut_name}",
        # Notebooks can use relative path: Files/{shortcut_name}/{subpath}
    }
```

### Step 4: Produce shortcutMappings Output

```python
# Convert to serializable format
shortcut_mappings_json = {}
for (container, account), mapping in shortcut_mappings.items():
    key = f"abfss://{container}@{account}.dfs.core.windows.net"
    shortcut_mappings_json[key] = mapping
```

### Phase 1b Output

```json
{
  "shortcutMappings": {
    "abfss://raw@mystorageaccount.dfs.core.windows.net": {
      "shortcutName": "mystorageaccount_raw",
      "lakehouseId": "{lhId}",
      "onelakePath": "Files/mystorageaccount_raw"
    },
    "abfss://processed@mystorageaccount.dfs.core.windows.net": {
      "shortcutName": "mystorageaccount_processed",
      "lakehouseId": "{lhId}",
      "onelakePath": "Files/mystorageaccount_processed"
    }
  }
}
```

> **Phase 2 consumption**: During code transforms (Step 2), the shortcutMappings are used to rewrite `abfss://` paths to OneLake-relative paths:
> ```python
> # Rewrite: abfss://raw@mystorageaccount.dfs.core.windows.net/incoming/2026/
> # →        Files/mystorageaccount_raw/incoming/2026/
> for prefix, mapping in shortcut_mappings_json.items():
>     source = source.replace(prefix, mapping["onelakePath"])
> ```

---

## Phase 2: Notebooks → Fabric Notebooks

Follow [spark-item-migration.md](spark-item-migration.md) Phase 2.

### Pre-Migration: Code Audit

**Both strategies** run the code audit — it's informational and takes seconds:

```python
search_patterns = [
    "mssparkutils", "spark.synapse.linkedService", "getSecretWithLS",
    "TokenLibrary", "synapsesql", "spark.catalog.listDatabases",
    "spark.catalog.currentDatabase", "spark.catalog.getDatabase",
    "LinkedServiceBasedTokenProvider", "getPropertiesAsMap",
    "spark.storage.synapse", "/user/trusted-service-user/",
    "cosmos.oltp", "kusto.spark.synapse"
]

audit = {}
for nb in notebooks:
    nb_name = nb["name"]
    hits = []
    for cell in nb["properties"]["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        for pattern in search_patterns:
            if pattern in source:
                hits.append(pattern)
    if hits:
        audit[nb_name] = list(set(hits))
    # else: safe to lift-and-shift
```

Present audit results:

```
Notebook Code Audit:
  Clean (no Synapse-specific code):  85 notebooks
  Has Synapse-specific patterns:     37 notebooks

  Top patterns found:
    mssparkutils           → 35 notebooks  (replace with notebookutils)
    TokenLibrary           → 12 notebooks  (replace with direct OAuth)
    synapsesql             →  8 notebooks  (replace with Delta read)
    cosmos.oltp            →  3 notebooks  (update auth)
    kusto.spark.synapse    →  2 notebooks  (update auth)
```

> **Lift-and-shift**: Present the audit as informational only: "These 37 notebooks contain Synapse-specific code that will need refactoring before they can run in Fabric. They will be migrated as-is — refactor post-cutover."
>
> **Migrate-and-modernize**: Present the audit and proceed to apply code transforms for notebooks with hits.

### Flagging Warnings for the Migration Report

Convert code audit hits into structured warnings that appear in the final [migration report](migration-report.md) with links to the [troubleshooting guide](migration-gotchas.md):

```python
warnings = []

FLAG_ANCHORS = {
    "SYNAPSESQL_NO_EQUIVALENT": "g1-sparkreadsynapsesql--no-direct-fabric-equivalent",
    "LIBRARY_VERSION_CONFLICT": "g2-custom-library-version-conflicts-with-fabric-runtime",
    "DELTA_PROTOCOL_MISMATCH": "g3-delta-lake-protocol-version-incompatibility",
    "SECURITY_MODEL_INCOMPATIBLE": "g4-synapse-security-model--managed-identities--ip-firewall",
    "GPU_POOL_UNSUPPORTED": "g5-gpu-pool-migration-blocker",
    "DOTNET_SPARK_UNSUPPORTED": "g6-net-for-spark-cf-sjd-blocker",
    "SESSION_CONFIG_IGNORED": "g7-notebook-session-configuration-configure",
    "SHORTCUT_CONNECTION_FAILED": "g8-shortcut-creation-failures-adls-connection-issues",
}

def flag_warning(item_name, flag_id, severity, details):
    warnings.append({
        "item": item_name, "flag": flag_id,
        "severity": severity, "details": details,
        "anchor": FLAG_ANCHORS.get(flag_id, flag_id.lower()),
    })

# Phase 0 — GPU pool blockers
for pool in pools:
    if pool["properties"].get("nodeSizeFamily") == "HardwareAcceleratedGPU":
        flag_warning(pool["name"], "GPU_POOL_UNSUPPORTED", "High",
                     "GPU pool — no Fabric equivalent")

# Phase 2 — code audit hits
PATTERN_FLAGS = {
    "synapsesql":       ("SYNAPSESQL_NO_EQUIVALENT", "High",
                         "Uses spark.read.synapsesql() — replace with JDBC or shortcut"),
    "LinkedServiceBasedTokenProvider": ("SECURITY_MODEL_INCOMPATIBLE", "Medium",
                         "Uses LinkedServiceBasedTokenProvider — replace with ClientCredsTokenProvider"),
    "getPropertiesAsMap": ("SECURITY_MODEL_INCOMPATIBLE", "Medium",
                         "Uses TokenLibrary.getPropertiesAsMap() — no Fabric equivalent"),
}

for nb_name, patterns in audit.items():
    for pat in patterns:
        if pat in PATTERN_FLAGS:
            fid, sev, det = PATTERN_FLAGS[pat]
            flag_warning(nb_name, fid, sev, det)

# Phase 3 — .NET SJD blockers
for sjd in sjds_source:
    lang = sjd["properties"].get("language", "")
    if lang.lower() in ("dotnet", "csharp"):
        flag_warning(sjd["name"], "DOTNET_SPARK_UNSUPPORTED", "High",
                     f".NET SJD (language={lang}) — rewrite in Python or Scala")
```

> The `warnings` list is passed to the report generator. See [migration-report.md § Collecting Warnings](migration-report.md#collecting-warnings-during-migration).

### Orchestrator Actions

**Lift-and-shift**:
1. **For each notebook**:
   - Extract `.ipynb` content (Step 1)
   - **Skip** code transforms (Step 2) — migrate as-is
   - **Skip** stripping Synapse fields (Step 3) — Fabric ignores them
   - **Auto-bind** Lakehouse (Step 4) — bind to the first (only) Lakehouse from Phase 1
   - **Auto-bind** Environment — look up the notebook's `bigDataPool.referenceName` in `poolMappings` and set the matching Environment
   - Base64-encode and POST (Steps 5–6)

**Migrate-and-modernize**:
1. **For each notebook**:
   - Extract `.ipynb` content (Step 1)
   - If notebook has audit hits → apply code transforms (Step 2) — see [code-patterns.md](code-patterns.md), [connector-refactoring.md](connector-refactoring.md), [utility-api-mapping.md](utility-api-mapping.md)
   - If Phase 1b produced `shortcutMappings` → rewrite `abfss://` paths to OneLake-relative paths (Step 2)
   - Strip Synapse-specific fields (Step 3)
   - Add Lakehouse binding (Step 4) — if multiple Lakehouses exist (Mode B/C), ask user which one to bind. If only one Lakehouse (Mode A), auto-bind.
   - Bind Environment — use `poolMappings`; if ambiguous, ask user
   - Base64-encode and POST (Steps 5–6)

2. **Build `notebookMappings` JSON**

3. **Run Phase 2 Gate** (Step 7):

```python
# Run each notebook via Job API
for nb_name, mapping in notebook_mappings.items():
    nb_id = mapping["fabricNotebookId"]
    resp = requests.post(
        f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}"
        f"/items/{nb_id}/jobs/instances?jobType=RunNotebook",
        headers=tokens.fab_headers,
        json={}
    )
    # Poll for completion...
```

> **Gate decision**: If critical notebooks fail → stop and present errors with fix guidance (see [validation-testing.md → V3](validation-testing.md#v3-notebook-execution-testing)). Ask user whether to proceed to Phase 3 or fix first.

### Phase 2 Output

```json
{
  "notebookMappings": {
    "{notebookName}": {
      "synapseNotebookName": "{originalName}",
      "fabricNotebookId": "{nbId}",
      "refactored": true,
      "auditPatterns": ["mssparkutils", "TokenLibrary"],
      "boundLakehouse": "{lakehouseId}",
      "boundEnvironment": "{environmentId}"
    }
  }
}
```

---

## Phase 3: SJDs → Fabric SJDs

Follow [spark-item-migration.md](spark-item-migration.md) Phase 3.

### Orchestrator Actions

**Lift-and-shift**:
1. **For each SJD**:
   - Export from Synapse (Step 1)
   - **Skip** file path/code updates (Step 2) — migrate as-is
   - **Auto-bind** Environment — look up SJD's `targetBigDataPool.referenceName` in `poolMappings` (Step 3)
   - Create SJD in Fabric (Step 4)

**Migrate-and-modernize**:
1. **For each SJD**:
   - Export from Synapse (Step 1)
   - Update file paths and code (Step 2)
   - Remap pool → Environment using `poolMappings` (Step 3) — ask user to confirm
   - Create SJD in Fabric (Step 4)

2. **Build `sjdMappings` JSON**

3. **Run Phase 3 Gate** (Step 5):

```python
# Run each SJD via Job API
for sjd_name, mapping in sjd_mappings.items():
    sjd_id = mapping["fabricSjdId"]
    resp = requests.post(
        f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}"
        f"/items/{sjd_id}/jobs/instances?jobType=SparkJob",
        headers=tokens.fab_headers,
        json={}
    )
    # Poll for completion...
```

> **Gate decision**: If SJDs fail → present errors. Ask user whether to proceed to final validation or fix first.

### Phase 3 Output

```json
{
  "sjdMappings": {
    "{sjdName}": {
      "synapseSjdName": "{originalName}",
      "fabricSjdId": "{sjdId}",
      "boundEnvironment": "{environmentId}",
      "language": "python | scala"
    }
  }
}
```

---

## Final Validation

Run the complete validation suite from [validation-testing.md](validation-testing.md):

1. **V1–V4**: Re-run all phase validations as a comprehensive sweep
2. **V5**: Query result comparison — checksums + sample rows for critical tables
3. **V6**: Generate the full validation report

```python
# Collect all mappings into a single migration state
migration_state = {
    "source": {"workspace": ws_name, "subscription": sub_id, "resourceGroup": rg},
    "target": {"workspace": fabric_ws_name, "workspaceId": fabric_ws_id},
    "strategy": strategy,
    "poolMappings": pool_mappings,
    "lakehouseMappings": lakehouse_mappings,
    "notebookMappings": notebook_mappings,
    "sjdMappings": sjd_mappings,
}
```

### Cutover Readiness

Present the final verdict:

```
╔══════════════════════════════════════════════════════════════════╗
║                    MIGRATION VALIDATION REPORT                  ║
╠══════════════════════════════════════════════════════════════════╣
║  Environments:  {env_pass}/{env_total} passed                   ║
║  Lakehouses:    {lh_pass}/{lh_total} passed                     ║
║  Shortcuts:     {sc_pass}/{sc_total} passed                     ║
║  Row counts:    {rc_pass}/{rc_total} matched                    ║
║  Notebooks:     {nb_pass}/{nb_total} executed successfully      ║
║  SJDs:          {sjd_pass}/{sjd_total} executed successfully    ║
║  Checksums:     {cs_pass}/{cs_total} matched                    ║
╠══════════════════════════════════════════════════════════════════╣
║  VERDICT:       {READY FOR CUTOVER | ISSUES REMAIN}            ║
╚══════════════════════════════════════════════════════════════════╝
```

If `READY FOR CUTOVER`:
> "All validations passed. You can now decommission the Synapse workspace. Synapse data remains untouched (shortcuts are read-only references)."

If `ISSUES REMAIN`:
> "Some validations failed. Review the failures above and fix before cutover. Synapse remains fully operational — no data was modified."

---

## Migration Report

Generate a comprehensive post-migration report with clickable Fabric portal links for every migrated item, blockers, and post-migration actions. This step runs **automatically** at the end of every migration — regardless of validation outcome — so the user always has a written record.

> For portal URL patterns and the standalone report script, see [migration-report.md](migration-report.md).

### Report Generation Script

```python
import requests, json, base64, os
from datetime import datetime, timezone

# --- Inputs (from migration state) ---
FABRIC_TOKEN = "<fabric-token>"
WORKSPACE_ID = migration_state["target"]["workspaceId"]
SYNAPSE_WS = migration_state["source"]["workspaceName"]
SUB_ID = migration_state["source"]["subscriptionId"]
RG = migration_state["source"]["resourceGroup"]
STRATEGY = migration_state["strategy"]
shortcut_mappings = migration_state.get("shortcutMappings", {})  # populated by Phase 1b; empty for lift-and-shift

PORTAL_URL = "https://app.fabric.microsoft.com"
FAB_BASE = "https://api.fabric.microsoft.com/v1"
headers = {"Authorization": f"Bearer {FABRIC_TOKEN}"}

# --- Collect all items from Fabric workspace ---
def list_items(item_type=None):
    url = f"{FAB_BASE}/workspaces/{WORKSPACE_ID}/items"
    if item_type:
        url += f"?type={item_type}"
    items = []
    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        items.extend(data.get("value", []))
        url = data.get("continuationUri")
    return items

environments = list_items("Environment")
lakehouses = list_items("Lakehouse")
notebooks = list_items("Notebook")
sjds = list_items("SparkJobDefinition")

# --- URL builder ---
def item_url(item):
    itype = item["type"]
    iid = item["id"]
    type_paths = {
        "Lakehouse": f"lakehouses/{iid}",
        "Notebook": f"synapse/notebooks/{iid}",
        "SparkJobDefinition": f"synapse/sparkjobdefinitions/{iid}",
        "Environment": f"environments/{iid}",
    }
    path = type_paths.get(itype, f"items/{iid}")
    return f"{PORTAL_URL}/groups/{WORKSPACE_ID}/{path}"

# --- Build report ---
lines = []
lines.append("# Synapse → Fabric Migration Report")
lines.append("")
lines.append(f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
lines.append(f"**Source**: Synapse workspace `{SYNAPSE_WS}` (sub: `{SUB_ID}`, rg: `{RG}`)")
lines.append(f"**Target**: [Fabric Workspace]({PORTAL_URL}/groups/{WORKSPACE_ID})")
lines.append(f"**Strategy**: {STRATEGY}")
lines.append("")

# Phase 0: Environments
lines.append("## Phase 0: Spark Pool → Environment")
lines.append("")
lines.append("| # | Environment | Source Pool | Link | Status |")
lines.append("|---|---|---|---|---|")
for i, env in enumerate(environments, 1):
    link = item_url(env)
    desc = env.get("description", "")
    pool = desc.replace("Migrated from Synapse Spark pool: ", "") if "Migrated from" in desc else "—"
    lines.append(f"| {i} | `{env['displayName']}` | {pool} | [Open]({link}) | ✓ |")
lines.append("")

# Phase 1: Lakehouses
lines.append("## Phase 1: Lake Database → Lakehouse")
lines.append("")
if lakehouses:
    lines.append("| # | Lakehouse | Source DB | Link | Shortcuts | Status |")
    lines.append("|---|---|---|---|---|---|")
    for i, lh in enumerate(lakehouses, 1):
        link = item_url(lh)
        desc = lh.get("description", "")
        db = desc.replace("Migrated from Synapse database: ", "") if "Migrated from" in desc else "—"
        # Shortcut count from migration state if available
        sc = migration_state.get("lakehouseMappings", {}).get(lh["displayName"], {}).get("shortcutCount", "—")
        lines.append(f"| {i} | `{lh['displayName']}` | {db} | [Open]({link}) | {sc} | ✓ |")
else:
    lines.append("No Lakehouses created (source had 0 Lake Databases or Phase 1 was skipped).")
lines.append("")

# Phase 1b: Storage Path Shortcuts (migrate-and-modernize only)
if shortcut_mappings:  # initialized in Phase 1b Step 3; empty dict in lift-and-shift mode
    lines.append("## Phase 1b: Storage Path Shortcuts")
    lines.append("")
    lines.append("OneLake shortcuts created for ad-hoc `abfss://` storage paths found in notebook/SJD code.")
    lines.append("")
    lines.append("| # | Shortcut Name | Source Storage | Container | Lakehouse | Path Refs |")
    lines.append("|---|---|---|---|---|---|")
    for i, (prefix, mapping) in enumerate(shortcut_mappings.items(), 1):
        # Parse account and container from prefix
        parts = prefix.replace("abfss://", "").split("@")
        container = parts[0] if parts else "—"
        account = parts[1].replace(".dfs.core.windows.net", "") if len(parts) > 1 else "—"
        lh_name = next(
            (lh["displayName"] for lh in lakehouses if lh["id"] == mapping["lakehouseId"]),
            mapping["lakehouseId"]
        )
        lines.append(
            f"| {i} | `{mapping['shortcutName']}` | `{account}` | `{container}` "
            f"| `{lh_name}` | `{mapping['onelakePath']}` |"
        )
    lines.append("")
    lines.append(f"**Total shortcuts**: {len(shortcut_mappings)}")
    lines.append("")

# Phase 2: Notebooks
lines.append("## Phase 2: Notebooks")
lines.append("")
lines.append("| # | Notebook | Source | Link | Flagged Patterns | Status |")
lines.append("|---|---|---|---|---|---|")
for i, nb in enumerate(notebooks, 1):
    link = item_url(nb)
    desc = nb.get("description", "")
    source = desc.replace("Migrated from Synapse: ", "") if "Migrated from" in desc else "—"
    # Check migration state for flagged patterns
    nb_state = migration_state.get("notebookMappings", {}).get(nb["displayName"], {})
    flags = nb_state.get("flaggedPatterns", [])
    flag_str = ", ".join(f"`{f}`" for f in flags) if flags else "—"
    status = "⚠ Needs refactoring" if flags else "✓"
    lines.append(f"| {i} | `{nb['displayName']}` | {source} | [Open]({link}) | {flag_str} | {status} |")
lines.append("")

# Phase 3: SJDs
lines.append("## Phase 3: Spark Job Definitions")
lines.append("")
lines.append("| # | SJD | Source | Language | Link | Status |")
lines.append("|---|---|---|---|---|---|")
for i, sjd in enumerate(sjds, 1):
    link = item_url(sjd)
    desc = sjd.get("description", "")
    source, lang = "—", "—"
    if "Migrated from Synapse SJD: " in desc:
        rest = desc.replace("Migrated from Synapse SJD: ", "")
        if " (language: " in rest:
            source, lang_part = rest.rsplit(" (language: ", 1)
            lang = lang_part.rstrip(")")
        else:
            source = rest
    lines.append(f"| {i} | `{sjd['displayName']}` | {source} | {lang} | [Open]({link}) | ✓ |")
lines.append("")

# Blockers (from migration state errors)
blockers = [e for e in migration_state.get("errors", []) if e.get("severity") == "blocker"]
if blockers:
    lines.append("## Migration Blockers")
    lines.append("")
    lines.append("| # | Source Item | Phase | Reason |")
    lines.append("|---|---|---|---|")
    for i, b in enumerate(blockers, 1):
        lines.append(f"| {i} | `{b['item']}` | {b['phase']} | {b['error']} |")
    lines.append("")

# Post-migration actions
lines.append("## Post-Migration Actions")
lines.append("")
lines.append("| Priority | Action | Items Affected |")
lines.append("|---|---|---|")
# Auto-generate actions from flagged patterns
refactor_nbs = [nb["displayName"] for nb in notebooks
                if migration_state.get("notebookMappings", {}).get(nb["displayName"], {}).get("flaggedPatterns")]
if refactor_nbs:
    lines.append(f"| **High** | Refactor Synapse-specific patterns (`mssparkutils`, `TokenLibrary`, etc.) | {', '.join(f'`{n}`' for n in refactor_nbs)} |")
if blockers:
    lines.append(f"| **Medium** | Resolve migration blockers (see table above) | {len(blockers)} item(s) |")
lines.append("| **Low** | Run security & governance setup for production | See [security-governance.md](security-governance.md) |")
lines.append("")

# Summary
total = len(environments) + len(lakehouses) + len(notebooks) + len(sjds)
lines.append("## Summary")
lines.append("")
lines.append("| Phase | Type | Count |")
lines.append("|---|---|---|")
lines.append(f"| 0 | Environments | {len(environments)} |")
lines.append(f"| 1 | Lakehouses | {len(lakehouses)} |")
lines.append(f"| 2 | Notebooks | {len(notebooks)} |")
lines.append(f"| 3 | Spark Job Definitions | {len(sjds)} |")
lines.append(f"| **Total** | | **{total}** |")

report = "\n".join(lines)
print(report)

# Save report
report_path = f"migration-report-{migration_state.get('migrationId', 'output')}.md"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)
print(f"\nReport saved to {report_path}")
```

### Report Output

The report includes:
- **Per-phase tables** with clickable Fabric portal links for every migrated item
- **Migration blockers** (GPU pools, .NET SJDs, unsupported features)
- **Post-migration actions** auto-generated from notebook audit results (flagged `mssparkutils`, `TokenLibrary`, etc.)
- **Summary table** with item counts per phase

> **Lift-and-shift mode**: Report is generated automatically after final validation — no user prompt needed.
> **Migrate-and-modernize mode**: Orchestrator asks "Generate migration report?" before producing it.

### State File Update

After report generation, update the migration state file:

```python
migration_state["reportGeneratedAt"] = datetime.now(timezone.utc).isoformat()
migration_state["reportPath"] = report_path
migration_state["summary"] = {
    "environments": len(environments),
    "lakehouses": len(lakehouses),
    "notebooks": len(notebooks),
    "sjds": len(sjds),
    "total": total,
    "blockers": len(blockers),
}
# Save updated state
with open(state_file_path, "w") as f:
    json.dump(migration_state, f, indent=2)
```

---

## (Optional) Security & Governance — Production Deployment

Security setup is **not required** for dev/test migrations. Apply when promoting to production.

> **Why security is last**: Migration typically starts in a dev workspace for code refactoring, dependency validation, and functional testing. Security is applied when the validated workspace is promoted to production. Applying production security too early blocks testing and adds unnecessary friction.

**When to run**: After the migration is functionally validated and the team is ready to deploy to a production workspace.

Follow [security-governance.md](security-governance.md):

| Section | What to Configure |
|---|---|
| S1: Identity & Authentication | Enable Workspace Identity, register service principals, eliminate SQL auth |
| S2: Workspace RBAC | Map Synapse roles → Fabric roles, assign security groups |
| S3: Secret Management | Production Key Vault access, credential rotation |
| S4: Governance & Compliance | Purview, sensitivity labels, endorsement, audit logs |
| S5: Data-Level Security | OneLake RBAC for table/folder access, recreate RLS/CLS/DDM on SQL endpoint |
| S6: Network Security | Managed Private Endpoints, Conditional Access, Private Link |
| S7: OPDG | On-premises data gateway for on-prem sources (if applicable) |
| S8: Checklist | Final security verification before opening to end users |

---

## Migration State File

The orchestrator maintains a JSON state file throughout the migration. This enables:
- **Resume from failure**: If the orchestrator stops mid-phase, reload the state file and continue from the last completed step
- **Audit trail**: Full record of what was migrated, when, and the mapping between source and target items

```json
{
  "migrationId": "{uuid}",
  "startedAt": "2026-04-24T10:00:00Z",
  "strategy": "migrate-and-modernize",
  "source": {
    "workspaceName": "my-synapse-ws",
    "subscriptionId": "...",
    "resourceGroup": "my-rg"
  },
  "target": {
    "workspaceName": "Migration-Target",
    "workspaceId": "..."
  },
  "phases": {
    "phase0": { "status": "completed", "completedAt": "...", "envCount": 3 },
    "phase1": { "status": "completed", "completedAt": "...", "lakehouseCount": 2, "shortcutCount": 87 },
    "phase2": { "status": "completed", "completedAt": "...", "notebookCount": 122, "refactoredCount": 37 },
    "phase3": { "status": "in-progress", "sjdCount": 15, "completedSjds": 8 },
    "validation": { "status": "not-started" },
    "report": { "status": "not-started" }
  },
  "reportGeneratedAt": null,
  "reportPath": null,
  "poolMappings": { ... },
  "lakehouseMappings": { ... },
  "notebookMappings": { ... },
  "sjdMappings": { ... },
  "errors": [
    { "phase": "phase2", "item": "ETL_LoadCustomers", "error": "ImportError: No module named 'custom_lib'", "resolution": "Add custom_lib to Environment" }
  ]
}
```

> **State file location**: Save as `migration-state-{migrationId}.json` in the user's working directory.

---

## Decision Points Summary

### Lift-and-Shift (express — minimal user interaction)

| When | Question | Asked? |
|---|---|---|
| Step 0 | Migration strategy? | **Yes** — the only required choice |
| Step 2f | Proceed with migration? | **Yes** — confirmation after inventory |
| Phase 1 (if external HMS) | JDBC credentials? | **Yes** — credentials cannot be auto-resolved |
| Phase 2 Gate | Notebook failures — fix or proceed? | **Yes** — gate check |
| Phase 3 Gate | SJD failures — fix or proceed? | **Yes** — gate check |
| All other decisions | — | **Auto-resolved** (see Step 0 defaults table) |

### Migrate-and-Modernize (guided — full user interaction)

| When | Question | Options |
|---|---|---|
| Step 0 | Migration strategy? | `lift-and-shift` / `migrate-and-modernize` |
| Step 2f | Proceed with migration? | `yes` / `no` |
| Phase 0 | Per-pool: Starter Pool vs Environment? | User confirms per pool |
| Phase 1 | Mapping mode? | `A (schemas)` / `B (separate)` / `C (hybrid)` |
| Phase 1 (if Mode C) | Per-database assignment? | User provides JSON map |
| Phase 1 | Non-Delta tables? | `Option A (convert to Delta)` / `Option B (retain format)` / `per-table` |
| Phase 1 (if external HMS) | JDBC credentials? | User provides connection string + username + password |
| Phase 1 (if external HMS, shared) | Which databases to migrate? | User selects from list |
| Phase 2 | Which Lakehouse to bind each notebook to? | Auto-derived or user override |
| Phase 2 | Confirm code refactoring per notebook? | User reviews audit and approves |
| Phase 2 Gate | Notebook failures — fix or proceed? | `fix` / `proceed to Phase 3` |
| Phase 3 Gate | SJD failures — fix or proceed? | `fix` / `proceed to validation` |
| Final | Generate migration report? | **Auto-generated** (always) |

---

## Error Recovery

### Resume After Failure

If the orchestrator encounters a fatal error or the session is interrupted:

1. **Load the state file**: `migration-state-{migrationId}.json`
2. **Identify the last completed phase** from `phases.{phaseN}.status`
3. **Resume from the next incomplete phase** — all prior outputs (mappings) are preserved in the state file
4. **For partially completed phases**: check individual item mappings to determine which items were already created and skip them

### Common Failures and Recovery

| Failure | Phase | Recovery |
|---|---|---|
| Token expired (401) | Any | `TokenManager.refresh_if_needed()` handles this automatically. If using manual tokens, re-run `get_token()` for all three audiences. The orchestrator is idempotent — re-running skips already-created items. |
| API 429 (throttled) | Any | Retry with `Retry-After` header delay |
| LRO 202 with no body | Phase 2/3 | Item creation returns 202 (async). Wait 5s, then query `GET /items?type={type}` and filter by `displayName` to resolve the item ID. |
| Environment `updateDefinition` 404 after creation | Phase 0 | Race condition — Environment not fully provisioned yet. Wait 2–5 seconds and retry (up to 3 attempts) |
| Environment publish failed | Phase 0 | Check library compatibility → fix environment.yml → re-publish |
| Shortcut creation failed (403) | Phase 1 | Grant Storage Blob Data Reader on source storage → retry |
| Notebook import failed (409 Conflict) | Phase 2 | Notebook with same name exists → rename or delete existing |
| Notebook execution failed | Phase 2 Gate | Check error against [validation-testing.md → V3 failure patterns](validation-testing.md#v3-notebook-execution-testing) |
| SJD execution failed | Phase 3 Gate | Check main file path, Lakehouse binding, Environment binding |

---

## Rollback & Cleanup

Rollback deletes migrated items from the **Fabric target workspace only**. The Synapse source is never modified.

### Rollback Scope

| Scope | What gets deleted | Use when |
|---|---|---|
| `--phase 3` | SJDs only | Phase 3 failed, need to retry SJD migration |
| `--phase 2` | Notebooks + SJDs (Phases 2–3) | Notebook migration went wrong, need to redo from Phase 2 |
| `--phase 1` | Lakehouses + shortcuts + Notebooks + SJDs (Phases 1–3) | Mapping mode was wrong, need to redo from Phase 1 |
| `--phase 0` | Environments + Lakehouses + Notebooks + SJDs (all phases) | Full restart |
| `--all` | Same as `--phase 0` | Alias for full cleanup |

> **Always rolls back in reverse order** (Phase 3 → 2 → 1 → 0) to delete dependents before their dependencies.

### Data Loss Warning

| Item type | Data impact |
|---|---|
| Environment | No data loss — configuration only |
| Notebook | No data loss — code only (job history preserved briefly) |
| SJD | No data loss — definition only |
| **Lakehouse** | **⚠ DESTRUCTIVE** — all OneLake data permanently removed. Delta tables converted from non-Delta sources (Option A) will be lost. Shortcuts to external ADLS are safe (external data is untouched), but any data materialized directly in the Lakehouse is gone. |

### Rollback Script

```python
import requests, json
from datetime import datetime, timezone

def rollback_migration(state_file_path, from_phase, dry_run=True):
    """
    Roll back migrated items from Fabric workspace.
    
    Args:
        state_file_path: Path to migration-state-{uuid}.json
        from_phase: Lowest phase to roll back (0 = all, 3 = SJDs only)
        dry_run: If True, list items without deleting
    """
    with open(state_file_path) as f:
        state = json.load(f)

    fabric_token = get_token("https://api.fabric.microsoft.com")
    ws_id = state["target"]["workspaceId"]
    headers = {"Authorization": f"Bearer {fabric_token}"}

    # Build deletion plan in reverse phase order
    deletion_plan = []

    # Phase 3: SJDs (key: fabricSjdId — see Phase 3 Output schema)
    if from_phase <= 3 and "sjdMappings" in state:
        for source_name, mapping in state["sjdMappings"].items():
            if "fabricSjdId" in mapping:
                deletion_plan.append({
                    "phase": 3, "type": "SparkJobDefinition",
                    "name": source_name, "itemId": mapping["fabricSjdId"],
                    "warning": None
                })

    # Phase 2: Notebooks (key: fabricNotebookId — see Phase 2 Output schema)
    if from_phase <= 2 and "notebookMappings" in state:
        for source_name, mapping in state["notebookMappings"].items():
            if "fabricNotebookId" in mapping:
                deletion_plan.append({
                    "phase": 2, "type": "Notebook",
                    "name": source_name, "itemId": mapping["fabricNotebookId"],
                    "warning": None
                })

    # Phase 1: Lakehouses (key: lakehouseId — see Phase 1 Output schema)
    # Shortcuts are deleted automatically with their Lakehouse
    if from_phase <= 1 and "lakehouseMappings" in state:
        for source_name, mapping in state["lakehouseMappings"].items():
            if "lakehouseId" in mapping:
                phase1_info = state.get("phases", {}).get("phase1", {})
                shortcut_count = phase1_info.get("shortcutCount", 0)
                deletion_plan.append({
                    "phase": 1, "type": "Lakehouse",
                    "name": source_name, "itemId": mapping["lakehouseId"],
                    "warning": f"⚠ DESTRUCTIVE: Lakehouse + {shortcut_count} shortcuts + all OneLake data will be permanently deleted"
                })

    # Phase 0: Environments (key: fabricEnvironmentId — see Phase 0 Output schema)
    if from_phase <= 0 and "poolMappings" in state:
        for source_name, mapping in state["poolMappings"].items():
            if "fabricEnvironmentId" in mapping:
                deletion_plan.append({
                    "phase": 0, "type": "Environment",
                    "name": source_name, "itemId": mapping["fabricEnvironmentId"],
                    "warning": None
                })

    # --- Dry Run: Print plan ---
    print(f"Rollback Plan (from Phase {from_phase}):")
    print(f"  Items to delete: {len(deletion_plan)}")
    print()

    has_destructive = False
    for item in deletion_plan:
        status = "⚠ DESTRUCTIVE" if item["warning"] else "  safe"
        print(f"  [{status}] Phase {item['phase']} — {item['type']}: {item['name']}")
        if item["warning"]:
            print(f"           {item['warning']}")
            has_destructive = True

    if dry_run:
        print("\n  DRY RUN — no items deleted. Re-run with dry_run=False to execute.")
        return deletion_plan

    # --- Execute Deletion ---
    if has_destructive:
        confirm = input("\n  ⚠ This will permanently delete Lakehouse data. Type 'DELETE' to confirm: ")
        if confirm != "DELETE":
            print("  Rollback cancelled.")
            return []

    results = {"deleted": 0, "failed": 0, "errors": []}

    for item in deletion_plan:
        resp = requests.delete(
            f"https://api.fabric.microsoft.com/v1/workspaces/{ws_id}/items/{item['itemId']}",
            headers=headers
        )

        if resp.status_code in (200, 204):
            results["deleted"] += 1
            print(f"  ✓ Deleted {item['type']}: {item['name']}")
        elif resp.status_code == 404:
            results["deleted"] += 1  # Already gone
            print(f"  ✓ Already deleted: {item['name']}")
        else:
            results["failed"] += 1
            results["errors"].append({
                "item": item["name"], "type": item["type"],
                "status": resp.status_code, "error": resp.text
            })
            print(f"  ✗ Failed to delete {item['type']}: {item['name']} — {resp.status_code}")

    # --- Update State File ---
    for phase_num in range(3, from_phase - 1, -1):
        phase_key = f"phase{phase_num}"
        if phase_key in state.get("phases", {}):
            state["phases"][phase_key]["status"] = "not_started"
            state["phases"][phase_key]["rolledBackAt"] = (
                datetime.now(timezone.utc).isoformat()
            )

    with open(state_file_path, "w") as f:
        json.dump(state, f, indent=2)

    print(f"\nRollback complete: {results['deleted']} deleted, {results['failed']} failed")
    print(f"State file updated — rolled-back phases marked as not_started")

    for err in results["errors"]:
        print(f"  FAILED: {err['item']} ({err['type']}) — {err['status']}: {err['error']}")

    return results
```

### Usage

```python
# Dry run — see what would be deleted (safe, no changes)
rollback_migration("migration-state-abc123.json", from_phase=2, dry_run=True)

# Execute — delete Phase 2 (Notebooks) and Phase 3 (SJDs), retry from Phase 2
rollback_migration("migration-state-abc123.json", from_phase=2, dry_run=False)

# Full cleanup — delete everything and start over
rollback_migration("migration-state-abc123.json", from_phase=0, dry_run=False)
```

### After Rollback

1. **Fix the root cause** — library issue, mapping mode, code pattern, etc.
2. **Re-run the orchestrator** with the same state file — it will resume from the rolled-back phase (status = `not_started`)
3. **If retrying Phase 1 with a different mapping mode**: update `state["decisions"]["mappingMode"]` in the state file, or delete the state file and start fresh

---

## Quick Start

### Lift-and-Shift (express)

User says:
> "Lift-and-shift my Synapse workspace `my-synapse-ws` (resource group `my-rg`, subscription `xxxx`) to Fabric workspace `Migration-Target`."

The agent then:
1. Authenticates and verifies access
2. Runs the full inventory → presents summary
3. **No further questions** — auto-resolves all decisions
4. Creates Environments mirroring every pool
5. Creates one Lakehouse with all databases as schemas
6. Migrates all notebooks as-is with auto-bound Lakehouse + Environment
7. Migrates all SJDs as-is with auto-bound Environment
8. Validates after each phase
9. Produces the final migration report

### Migrate-and-Modernize (guided)

User says:
> "Migrate and modernize my Synapse workspace `my-synapse-ws` (resource group `my-rg`, subscription `xxxx`) to Fabric workspace `Migration-Target`."

The agent then:
1. Authenticates and verifies access
2. Runs the full inventory → presents summary
3. **Asks guided questions** at each decision point (mapping mode, non-Delta handling, etc.)
4. For each pool: asks user to confirm Starter Pool vs Environment
5. Creates Lakehouses per user's chosen mapping mode
6. Runs code audit → refactors notebooks with Synapse-specific patterns
7. Migrates SJDs with path/code updates
8. Validates after each phase
9. Produces the final migration report

# Migration Report — Synapse → Fabric

Generate a comprehensive post-migration report with clickable links to every migrated item in the Fabric portal.

---

## Fabric Portal URL Patterns

All Fabric portal links use base URL `https://app.fabric.microsoft.com`.

### Workspace Link

```
https://app.fabric.microsoft.com/groups/{workspaceId}
```

### Item Links by Type

| Item Type | Portal URL |
|---|---|
| **Lakehouse** | `https://app.fabric.microsoft.com/groups/{workspaceId}/lakehouses/{itemId}` |
| **Notebook** | `https://app.fabric.microsoft.com/groups/{workspaceId}/synapse/notebooks/{itemId}` |
| **Spark Job Definition** | `https://app.fabric.microsoft.com/groups/{workspaceId}/synapse/sparkjobdefinitions/{itemId}` |
| **Environment** | `https://app.fabric.microsoft.com/groups/{workspaceId}/environments/{itemId}` |

> The `workspaceId` and `itemId` are the GUIDs returned by the Fabric REST API when creating items.

---

## Collecting Item IDs for the Report

During each migration phase, capture the item `id` from the Fabric REST API response.

### From Item Creation (POST response)

```json
// POST /v1/workspaces/{workspaceId}/items → 201/202
{
  "id": "5b218778-e7a5-4d73-8187-f10824047715",   // ← capture this
  "displayName": "MyNotebook",
  "type": "Notebook",
  "workspaceId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### From Item List (if IDs weren't captured during creation)

```
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items?type={itemType}
```

Filter by `displayName` to find the item ID. Item types: `Lakehouse`, `Notebook`, `SparkJobDefinition`, `Environment`.

---

## Report Generation Script

Run this after all migration phases are complete. It queries the Fabric workspace and produces a Markdown report with clickable links.

```python
import requests, json
from datetime import datetime, timezone

# --- Configuration ---
FABRIC_TOKEN = "<your-fabric-token>"  # az account get-access-token --resource https://api.fabric.microsoft.com
WORKSPACE_ID = "<your-fabric-workspace-id>"
SYNAPSE_WORKSPACE_NAME = "<your-synapse-workspace-name>"

BASE_URL = "https://api.fabric.microsoft.com/v1"
PORTAL_URL = "https://app.fabric.microsoft.com"
headers = {"Authorization": f"Bearer {FABRIC_TOKEN}"}

# --- Collect all items from the Fabric workspace ---
def list_items(item_type=None):
    url = f"{BASE_URL}/workspaces/{WORKSPACE_ID}/items"
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

# --- URL builders ---
def workspace_url():
    return f"{PORTAL_URL}/groups/{WORKSPACE_ID}"

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

# --- Build Markdown report ---
lines = []
lines.append("# Synapse → Fabric Migration Report")
lines.append("")
lines.append(f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
lines.append("")
lines.append(f"**Source**: Synapse workspace `{SYNAPSE_WORKSPACE_NAME}`")
lines.append("")
lines.append(f"**Target**: [Fabric Workspace]({workspace_url()})")
lines.append("")

# Phase 0: Environments
lines.append("---")
lines.append("## Phase 0: Spark Pool → Environment")
lines.append("")
lines.append("| # | Environment Name | Fabric Link | Description | Status |")
lines.append("|---|---|---|---|---|")
for i, env in enumerate(environments, 1):
    link = item_url(env)
    desc = env.get("description", "")
    status = env.get("_status", "✓ Created")
    lines.append(f"| {i} | `{env['displayName']}` | [Open in Fabric]({link}) | {desc} | {status} |")
lines.append("")
lines.append(f"**Total Environments**: {len(environments)}")
lines.append("")

# Phase 1: Lakehouses
lines.append("---")
lines.append("## Phase 1: Lake Database → Lakehouse")
lines.append("")
lines.append("| # | Lakehouse Name | Fabric Link | Description | Status |")
lines.append("|---|---|---|---|---|")
for i, lh in enumerate(lakehouses, 1):
    link = item_url(lh)
    desc = lh.get("description", "")
    status = lh.get("_status", "✓ Created")
    lines.append(f"| {i} | `{lh['displayName']}` | [Open in Fabric]({link}) | {desc} | {status} |")
lines.append("")
lines.append(f"**Total Lakehouses**: {len(lakehouses)}")
lines.append("")

# Phase 2: Notebooks
lines.append("---")
lines.append("## Phase 2: Notebooks")
lines.append("")
lines.append("| # | Notebook Name | Fabric Link | Description | Status |")
lines.append("|---|---|---|---|---|")
for i, nb in enumerate(notebooks, 1):
    link = item_url(nb)
    desc = nb.get("description", "")
    status = nb.get("_status", "✓ Created")
    lines.append(f"| {i} | `{nb['displayName']}` | [Open in Fabric]({link}) | {desc} | {status} |")
lines.append("")
lines.append(f"**Total Notebooks**: {len(notebooks)}")
lines.append("")

# Phase 3: Spark Job Definitions
lines.append("---")
lines.append("## Phase 3: Spark Job Definitions")
lines.append("")
lines.append("| # | SJD Name | Fabric Link | Description | Status |")
lines.append("|---|---|---|---|---|")
for i, sjd in enumerate(sjds, 1):
    link = item_url(sjd)
    desc = sjd.get("description", "")
    status = sjd.get("_status", "✓ Created")
    lines.append(f"| {i} | `{sjd['displayName']}` | [Open in Fabric]({link}) | {desc} | {status} |")
lines.append("")
lines.append(f"**Total SJDs**: {len(sjds)}")
lines.append("")

# Migration Warnings — flag issues for post-migration remediation
# `warnings` is populated during the migration phases (see Collecting Warnings below)
# Initialize to empty list if not already set (e.g., when running report standalone)
if 'warnings' not in dir():
    warnings = []
if warnings:
    lines.append("---")
    lines.append("## Migration Warnings")
    lines.append("")
    lines.append("Items below were migrated successfully but require post-migration action. See the [Troubleshooting Guide](migration-gotchas.md) for resolution steps.")
    lines.append("")
    lines.append("| # | Item | Flag | Severity | Details | Guide |")
    lines.append("|---|---|---|---|---|---|")
    for i, w in enumerate(warnings, 1):
        lines.append(f"| {i} | `{w['item']}` | `{w['flag']}` | {w['severity']} | {w['details']} | [{w['flag']}](migration-gotchas.md#{w['anchor']}) |")
    lines.append("")
    lines.append(f"**Total warnings**: {len(warnings)}")
    lines.append("")

# Summary
total = len(environments) + len(lakehouses) + len(notebooks) + len(sjds)
lines.append("---")
lines.append("## Summary")
lines.append("")
lines.append("| Phase | Item Type | Count |")
lines.append("|---|---|---|")
lines.append(f"| 0 | Environments | {len(environments)} |")
lines.append(f"| 1 | Lakehouses | {len(lakehouses)} |")
lines.append(f"| 2 | Notebooks | {len(notebooks)} |")
lines.append(f"| 3 | Spark Job Definitions | {len(sjds)} |")
lines.append(f"| **Total** | | **{total}** |")

report = "\n".join(lines)
print(report)

# Optionally save to file
with open("migration_report.md", "w") as f:
    f.write(report)
print(f"\nReport saved to migration_report.md")
```

---

## Collecting Warnings During Migration

Build the `warnings` list during migration phases. Each warning has a flag ID from [migration-gotchas.md](migration-gotchas.md):

```python
warnings = []

# Flag ID → anchor mapping (for report links)
FLAG_ANCHORS = {
    "SYNAPSESQL_NO_EQUIVALENT": "g1-sparkreadsynapsesql--no-direct-fabric-equivalent",
    "LIBRARY_VERSION_CONFLICT": "g2-custom-library-version-conflicts-with-fabric-runtime",
    "DELTA_PROTOCOL_MISMATCH": "g3-delta-lake-protocol-version-incompatibility",
    "SECURITY_MODEL_INCOMPATIBLE": "g4-synapse-security-model--managed-identities--ip-firewall",
    "GPU_POOL_UNSUPPORTED": "g5-gpu-pool-migration-blocker",
    "DOTNET_SPARK_UNSUPPORTED": "g6-net-for-spark-cf-sjd-blocker",
    "NULLABLE_POOL_REFERENCE": "g7-bigdatapool--targetbigdatapool-field-is-null-not-missing",
    "SESSION_CONFIG_IGNORED": "g8-notebook-session-configuration-configure",
    "SHORTCUT_CONNECTION_FAILED": "g9-shortcut-creation-failures-adls-connection-issues",
}

def flag_warning(item_name, flag_id, severity, details):
    """Call during migration when an edge case is detected."""
    warnings.append({
        "item": item_name,
        "flag": flag_id,
        "severity": severity,
        "details": details,
        "anchor": FLAG_ANCHORS.get(flag_id, flag_id.lower()),
    })

# --- Example: Phase 0 — flag GPU pools ---
for pool in synapse_pools:
    if pool["properties"].get("nodeSizeFamily") == "HardwareAcceleratedGPU":
        flag_warning(pool["name"], "GPU_POOL_UNSUPPORTED", "High",
                     "GPU pool — no Fabric equivalent")

# --- Example: Phase 2 — flag code patterns during notebook audit ---
for nb_name, patterns in audit.items():
    if "synapsesql" in patterns:
        flag_warning(nb_name, "SYNAPSESQL_NO_EQUIVALENT", "High",
                     "Uses spark.read.synapsesql() — replace with JDBC or shortcut")
    if "LinkedServiceBasedTokenProvider" in patterns:
        flag_warning(nb_name, "SECURITY_MODEL_INCOMPATIBLE", "Medium",
                     "Uses LinkedServiceBasedTokenProvider — replace with ClientCredsTokenProvider")
    if "%%configure" in patterns or "spark.synapse." in str(patterns):
        flag_warning(nb_name, "SESSION_CONFIG_IGNORED", "Low",
                     "Has Synapse-specific %%configure keys — remove spark.synapse.* keys")

# --- Example: Phase 3 — flag .NET SJDs ---
for sjd in synapse_sjds:
    lang = sjd["properties"].get("language", "")
    if lang.lower() in ("dotnet", "csharp"):
        flag_warning(sjd["name"], "DOTNET_SPARK_UNSUPPORTED", "High",
                     f".NET SJD (language={lang}) — rewrite in Python or Scala")
```

---

## Report Output Example

The script produces a Markdown file like this:

```markdown
# Synapse → Fabric Migration Report

**Generated**: 2026-04-24 15:30 UTC

**Source**: Synapse workspace `my-synapse-ws`

**Target**: [Fabric Workspace](https://app.fabric.microsoft.com/groups/a1b2c3d4-e5f6-7890-abcd-ef1234567890)

---
## Phase 0: Spark Pool → Environment

| # | Environment Name | Fabric Link | Description |
|---|---|---|---|
| 1 | `ETLPool_env` | [Open in Fabric](https://app.fabric.microsoft.com/groups/a1b2c3d4-.../environments/5b218778-...) | Migrated from Synapse Spark pool: ETLPool |
| 2 | `MLPool_env` | [Open in Fabric](https://app.fabric.microsoft.com/groups/a1b2c3d4-.../environments/c3d4e5f6-...) | Migrated from Synapse Spark pool: MLPool |

**Total Environments**: 2

---
## Phase 1: Lake Database → Lakehouse

| # | Lakehouse Name | Fabric Link | Description |
|---|---|---|---|
| 1 | `SilverLakehouse` | [Open in Fabric](https://app.fabric.microsoft.com/groups/a1b2c3d4-.../lakehouses/7890abcd-...) | Migrated from Synapse lake database: silver_db |

**Total Lakehouses**: 1

---
## Phase 1b: Storage Path Shortcuts (Migrate-and-Modernize)

OneLake shortcuts created for ad-hoc `abfss://` storage paths found in notebook/SJD code.

| # | Shortcut Name | Source Storage | Container | Lakehouse | OneLake Path |
|---|---|---|---|---|---|
| 1 | `mystorageaccount_raw` | `mystorageaccount` | `raw` | `SilverLakehouse` | `Files/mystorageaccount_raw` |
| 2 | `mystorageaccount_processed` | `mystorageaccount` | `processed` | `SilverLakehouse` | `Files/mystorageaccount_processed` |

**Total shortcuts**: 2

---
## Phase 2: Notebooks

| # | Notebook Name | Fabric Link | Description |
|---|---|---|---|
| 1 | `bronze_ingest` | [Open in Fabric](https://app.fabric.microsoft.com/groups/a1b2c3d4-.../synapse/notebooks/1234abcd-...) | |
| 2 | `silver_transform` | [Open in Fabric](https://app.fabric.microsoft.com/groups/a1b2c3d4-.../synapse/notebooks/5678efgh-...) | |
| 3 | `gold_aggregate` | [Open in Fabric](https://app.fabric.microsoft.com/groups/a1b2c3d4-.../synapse/notebooks/9012ijkl-...) | |

**Total Notebooks**: 3

---
## Phase 3: Spark Job Definitions

| # | SJD Name | Fabric Link | Description |
|---|---|---|---|
| 1 | `daily_etl_job` | [Open in Fabric](https://app.fabric.microsoft.com/groups/a1b2c3d4-.../synapse/sparkjobdefinitions/mnop3456-...) | |

**Total SJDs**: 1

---
## Migration Warnings

Items below were migrated successfully but require post-migration action. See the [Troubleshooting Guide](migration-gotchas.md) for resolution steps.

| # | Item | Flag | Severity | Details | Guide |
|---|---|---|---|---|---|
| 1 | `bronze_ingest` | `SYNAPSESQL_NO_EQUIVALENT` | High | Uses spark.read.synapsesql() — replace with JDBC or shortcut | [G1](migration-gotchas.md#g1-sparkreadsynapsesql--no-direct-fabric-equivalent) |
| 2 | `silver_transform` | `SECURITY_MODEL_INCOMPATIBLE` | Medium | Uses LinkedServiceBasedTokenProvider — replace with ClientCredsTokenProvider | [G4](migration-gotchas.md#g4-synapse-security-model--managed-identities--ip-firewall) |
| 3 | `gold_aggregate` | `SESSION_CONFIG_IGNORED` | Low | Has Synapse-specific %%configure keys — remove spark.synapse.* keys | [G7](migration-gotchas.md#g7-notebook-session-configuration-configure) |

**Total warnings**: 3

---
## Summary

| Phase | Item Type | Count |
|---|---|---|
| 0 | Environments | 2 |
| 1 | Lakehouses | 1 |
| 2 | Notebooks | 3 |
| 3 | Spark Job Definitions | 1 |
| **Total** | | **7** |
```

---

## Incremental Report — Track During Migration

If you prefer to build the report incrementally as each item is migrated (rather than querying after the fact), maintain a tracking list during each phase:

```python
# Initialize at the start of migration
migration_log = []

def log_migrated_item(phase, synapse_name, fabric_item, status="success", notes=""):
    """Call after each successful Fabric item creation."""
    migration_log.append({
        "phase": phase,
        "synapse_name": synapse_name,
        "fabric_name": fabric_item["displayName"],
        "fabric_id": fabric_item["id"],
        "fabric_type": fabric_item["type"],
        "fabric_url": f"https://app.fabric.microsoft.com/groups/{WORKSPACE_ID}/{_type_path(fabric_item)}",
        "status": status,
        "notes": notes,
    })

def _type_path(item):
    paths = {
        "Lakehouse": f"lakehouses/{item['id']}",
        "Notebook": f"synapse/notebooks/{item['id']}",
        "SparkJobDefinition": f"synapse/sparkjobdefinitions/{item['id']}",
        "Environment": f"environments/{item['id']}",
    }
    return paths.get(item["type"], f"items/{item['id']}")

# Usage after creating a notebook:
# log_migrated_item(2, "bronze_ingest", fabric_response_json, notes="lift-and-shift, no refactoring")
```

Then at the end, generate the report from `migration_log`:

```python
import json

# Save as JSON for programmatic use
with open("migration_log.json", "w") as f:
    json.dump(migration_log, f, indent=2)

# Generate Markdown from log
for entry in migration_log:
    status_icon = "✅" if entry["status"] == "success" else "❌"
    print(f"| {status_icon} | `{entry['synapse_name']}` → `{entry['fabric_name']}` | [Open]({entry['fabric_url']}) | {entry['notes']} |")
```

---

## Extended Report — With Synapse Source Links

To include links back to the Synapse source items for comparison:

| Item Type | Synapse Studio URL Pattern |
|---|---|
| **Notebook** | `https://web.azuresynapse.net/en/authoring/analyze/notebooks/{notebookName}?workspace=/subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.Synapse/workspaces/{ws}` |
| **SJD** | `https://web.azuresynapse.net/en/authoring/analyze/sparkJobDefinitions/{sjdName}?workspace=...` |
| **Spark Pool** | `https://web.azuresynapse.net/en/management/sparkPools/{poolName}?workspace=...` |
| **Lake Database** | `https://web.azuresynapse.net/en/authoring/analyze/databases/{dbName}?workspace=...` |

```python
def synapse_item_url(item_type, item_name, sub_id, rg, ws_name):
    """Build a Synapse Studio URL for the source item."""
    base = "https://web.azuresynapse.net/en"
    ws_path = f"/subscriptions/{sub_id}/resourceGroups/{rg}/providers/Microsoft.Synapse/workspaces/{ws_name}"
    type_paths = {
        "Notebook": f"/authoring/analyze/notebooks/{item_name}",
        "SparkJobDefinition": f"/authoring/analyze/sparkJobDefinitions/{item_name}",
        "SparkPool": f"/management/sparkPools/{item_name}",
        "Database": f"/authoring/analyze/databases/{item_name}",
    }
    return f"{base}{type_paths.get(item_type, '')}{f'?workspace={ws_path}'}"
```

This allows the report to include side-by-side links:

```markdown
| Synapse Item | Fabric Item | Status |
|---|---|---|
| [bronze_ingest (Synapse)](https://web.azuresynapse.net/en/authoring/...) | [bronze_ingest (Fabric)](https://app.fabric.microsoft.com/groups/.../synapse/notebooks/...) | ✅ Migrated |
```

# Security & Governance — Production Readiness

Security and governance configuration for Fabric workspaces. Apply when promoting a validated migration to production.

> **When to use this guide**: After all migration phases are complete and functionally validated in a dev/test workspace. This guide is for **production deployment** — it is not required for dev/test migrations where the goal is to validate code, dependencies, and functionality.
>
> **Migration context**: This guide is the final optional step in the migration workflow. See [migration-orchestrator.md](migration-orchestrator.md) for the full end-to-end flow.
>
> **Typical promotion path**:
> ```
> Dev (migrate + refactor + test) → Test (integration testing) → Stage (UAT) → Prod (apply security)
> ```
>
> Security setup is environment-specific — dev/test may use relaxed permissions, while production requires full RBAC, network isolation, and governance.

---

## Sections

```
Security & Governance:
│
│  ── API-Automatable ──────────────────────────────────
├── S1: Identity & Authentication                    (API)
├── S2: Workspace RBAC Mapping (Synapse → Fabric)    (API)
├── S3: Secret Management (Key Vault integration)    (API)
├── S4: Governance & Compliance (Purview, labels)     (API)
│
│  ── Partial / Manual ─────────────────────────────────
├── S5: Data-Level Security (OneLake RBAC, RLS, CLS) (Partial — T-SQL + Portal)
├── S6: Network Security (MPE, Private Link)          (Manual — Portal / Admin)
├── S7: On-Premises Data Gateway (OPDG)               (Manual — Install)
│
│  ── Checklist ────────────────────────────────────────
└── S8: Production Security Checklist
```

---

## S1: Identity & Authentication `(API)`

### Synapse → Fabric Identity Mapping

| Synapse Identity | Fabric Equivalent | Migration Action |
|---|---|---|
| Workspace Managed Identity (MSI) | **Fabric Workspace Identity** | Enable in Workspace Settings → assign Storage Blob Data Reader on ADLS accounts that shortcuts reference |
| Linked Service with Service Principal | **Service principal profile** (for multi-tenancy) or **direct SP auth** via Key Vault | Register SP in Entra ID; store credentials in Key Vault; reference via `notebookutils.credentials.getSecret()` |
| SQL Authentication (Dedicated Pool) | **Not available** in Fabric Spark — Entra-only | Convert all SQL auth to Entra ID (service principals or managed identity). Fabric Warehouse SQL endpoint supports Entra auth only |
| User-assigned managed identity | **Not directly supported** in Fabric | Use Fabric Workspace Identity or service principal instead |

### Fabric Workspace Identity Setup

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/assignWorkspaceIdentity
```

After assigning, the workspace identity can be used for:
- **Trusted workspace access** to ADLS Gen2 (no explicit credentials needed for shortcuts)
- **OneLake shortcuts** to storage accounts configured with trusted workspace access

### Authentication Migration Checklist

- [ ] Enable Fabric Workspace Identity on the production workspace
- [ ] Grant Workspace Identity **Storage Blob Data Reader** on all ADLS accounts referenced by shortcuts
- [ ] Register all service principals used by notebooks/SJDs in the Fabric workspace
- [ ] Verify no notebooks rely on SQL auth — convert to Entra if found
- [ ] Test token acquisition: `notebookutils.credentials.getToken("https://management.azure.com")`

### Automated Migration: Identity & Storage Access

#### Step 1: Enable Fabric Workspace Identity

```python
import requests

fabric_token = get_token("https://api.fabric.microsoft.com")

resp = requests.post(
    f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/assignWorkspaceIdentity",
    headers={"Authorization": f"Bearer {fabric_token}"}
)

if resp.status_code in (200, 201):
    print("Workspace Identity enabled")
elif resp.status_code == 409:
    print("Workspace Identity already assigned")
else:
    print(f"Failed: {resp.status_code} — {resp.text}")
```

#### Step 2: Discover ADLS Accounts from Synapse Linked Services

Scan Synapse for Linked Services that reference ADLS Gen2 storage accounts:

```python
synapse_dev_token = get_token("https://dev.azuresynapse.net")

# List Linked Services via Synapse data-plane API
resp = requests.get(
    f"https://{ws_name}.dev.azuresynapse.net/linkedservices"
    f"?api-version=2020-12-01",
    headers={"Authorization": f"Bearer {synapse_dev_token}"}
)

# Extract ADLS Gen2 storage account names
adls_accounts = set()
for ls in resp.json().get("value", []):
    props = ls.get("properties", {}).get("typeProperties", {})
    url = props.get("url", "") or props.get("endpoint", "")
    # Match https://<account>.dfs.core.windows.net or .blob.core.windows.net
    if ".dfs.core.windows.net" in url or ".blob.core.windows.net" in url:
        account_name = url.split("//")[1].split(".")[0]
        adls_accounts.add(account_name)

print(f"Found {len(adls_accounts)} ADLS accounts referenced by Synapse:")
for acct in sorted(adls_accounts):
    print(f"  - {acct}")
```

#### Step 3: Also Check Shortcut Targets (Fabric Side)

If Lakehouses were already created (Phase 1), check which storage accounts shortcuts point to:

```python
# List all Lakehouses in the target workspace
resp = requests.get(
    f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/items?type=Lakehouse",
    headers={"Authorization": f"Bearer {fabric_token}"}
)

shortcut_accounts = set()
for lh in resp.json().get("value", []):
    lh_id = lh["id"]
    # List shortcuts for this Lakehouse
    sc_resp = requests.get(
        f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}"
        f"/items/{lh_id}/shortcuts",
        headers={"Authorization": f"Bearer {fabric_token}"}
    )
    if sc_resp.status_code == 200:
        for sc in sc_resp.json().get("value", []):
            target = sc.get("target", {})
            if "adlsGen2" in target:
                loc = target["adlsGen2"].get("location", "")
                if ".dfs.core.windows.net" in loc:
                    acct = loc.split("//")[1].split(".")[0]
                    shortcut_accounts.add(acct)

all_accounts = adls_accounts | shortcut_accounts
print(f"\nAll ADLS accounts needing Storage Blob Data Reader ({len(all_accounts)}):")
for acct in sorted(all_accounts):
    source = []
    if acct in adls_accounts: source.append("Linked Service")
    if acct in shortcut_accounts: source.append("Shortcut")
    print(f"  - {acct}  (from: {', '.join(source)})")
```

#### Step 4: Grant Storage Blob Data Reader on Each Account

```python
import uuid

# Storage Blob Data Reader role definition ID
STORAGE_BLOB_DATA_READER = "2a2b9908-6ea1-4ae2-8e65-a410df84e7d1"

# Get the Fabric Workspace Identity's service principal ID
ws_resp = requests.get(
    f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}",
    headers={"Authorization": f"Bearer {fabric_token}"}
)
ws_identity_id = ws_resp.json().get("identity", {}).get("servicePrincipalId")

if not ws_identity_id:
    print("ERROR: Workspace Identity not found. Run Step 1 first.")
else:
    results = {"success": 0, "exists": 0, "failed": 0}

    for acct in all_accounts:
        storage_scope = (
            f"/subscriptions/{sub_id}/resourceGroups/{rg}"
            f"/providers/Microsoft.Storage/storageAccounts/{acct}"
        )
        assignment_id = str(uuid.uuid4())

        resp = requests.put(
            f"https://management.azure.com{storage_scope}"
            f"/providers/Microsoft.Authorization/roleAssignments/{assignment_id}"
            f"?api-version=2022-04-01",
            headers={
                "Authorization": f"Bearer {arm_token}",
                "Content-Type": "application/json"
            },
            json={
                "properties": {
                    "roleDefinitionId": f"/subscriptions/{sub_id}/providers/Microsoft.Authorization/roleDefinitions/{STORAGE_BLOB_DATA_READER}",
                    "principalId": ws_identity_id,
                    "principalType": "ServicePrincipal"
                }
            }
        )

        if resp.status_code in (200, 201):
            results["success"] += 1
            print(f"  ✓ Granted on {acct}")
        elif resp.status_code == 409:
            results["exists"] += 1
            print(f"  ✓ Already granted on {acct}")
        else:
            results["failed"] += 1
            print(f"  ✗ Failed on {acct}: {resp.status_code} — {resp.text}")

    print(f"\nResults: {results['success']} granted, {results['exists']} already existed, {results['failed']} failed")
```

#### Step 5: Detect SQL Authentication Usage in Notebooks

Scan exported notebooks for SQL authentication patterns that must be converted to Entra:

```python
import re

SQL_AUTH_PATTERNS = [
    (r"jdbc:.*User=|jdbc:.*Password=", "JDBC with SQL credentials"),
    (r"\.option\([\"']user[\"']", "Spark JDBC .option('user')"),
    (r"\.option\([\"']password[\"']", "Spark JDBC .option('password')"),
    (r"SqlConnection\(.*Uid=|SqlConnection\(.*Pwd=", ".NET SqlConnection with SQL auth"),
    (r"pyodbc\.connect\(.*UID=|pyodbc\.connect\(.*PWD=", "pyodbc with SQL auth"),
]

# notebooks = list of exported notebook dicts (from Phase 2 inventory)
sql_auth_issues = []

for nb in notebooks:
    nb_name = nb.get("name", "unknown")
    cells = nb.get("properties", {}).get("cells", [])
    for i, cell in enumerate(cells):
        source = "".join(cell.get("source", []))
        for pattern, description in SQL_AUTH_PATTERNS:
            if re.search(pattern, source, re.IGNORECASE):
                sql_auth_issues.append({
                    "notebook": nb_name,
                    "cell": i + 1,
                    "issue": description
                })

if sql_auth_issues:
    print(f"⚠ Found {len(sql_auth_issues)} SQL auth usage(s) — must convert to Entra:")
    for issue in sql_auth_issues:
        print(f"  {issue['notebook']} (cell {issue['cell']}): {issue['issue']}")
    print("\n  → Replace with Entra token: notebookutils.credentials.getToken('https://database.windows.net')")
else:
    print("✓ No SQL authentication patterns found in notebooks")
```

---

## S2: Workspace RBAC Mapping `(API)`

### Synapse Roles → Fabric Roles

| Synapse Role | Closest Fabric Role | Permission Delta |
|---|---|---|
| **Synapse Administrator** | **Admin** | Equivalent — full workspace control |
| **SQL Administrator** | **Admin** or **Member** | Fabric has no SQL-specific admin role; Admin covers all |
| **Apache Spark Administrator** | **Member** | Fabric has no Spark-specific admin; Member can run notebooks/SJDs |
| **Synapse Contributor** | **Contributor** | Similar — can create, edit, run items but not manage access |
| **Synapse Linked Data Manager** | No direct equivalent | Fabric Workspace Identity replaces linked data management. Admin or Member can manage connections |
| **Synapse Monitoring Operator** | **Viewer** | Fabric Viewer can see items but not run them. For monitoring, use Fabric Monitoring Hub (no role required beyond Viewer) |
| **Synapse Credential User** | No direct equivalent | In Fabric, credential access is controlled by Key Vault RBAC, not workspace roles |
| **Synapse User** | **Viewer** | Read-only access to workspace items |

### Fabric Role Permissions

| Permission | Admin | Member | Contributor | Viewer |
|---|---|---|---|---|
| Manage workspace settings & access | Yes | No | No | No |
| Add/remove members | Yes | Yes (not Admins) | No | No |
| Create/edit/delete items | Yes | Yes | Yes | No |
| Run notebooks & SJDs | Yes | Yes | Yes | No |
| View items | Yes | Yes | Yes | Yes |
| Share items | Yes | Yes | Yes (with reshare) | No |
| Connect to SQL endpoint | Yes | Yes | Yes | Yes (read-only) |
| Manage OneLake RBAC | Yes | Yes | No | No |

### Role Assignment via REST API

**List current Fabric assignments**:
```
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/roleAssignments
```

Response: `{ "value": [ { "id": "...", "principal": { "id": "...", "displayName": "...", "type": "User" }, "role": "Contributor" }, ... ] }`

**Add role assignment**:
```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/roleAssignments
```

```json
{
  "principal": {
    "id": "{entraObjectId}",
    "type": "User"
  },
  "role": "Contributor"
}
```

`principal.type`: `User`, `Group`, `ServicePrincipal`, `ServicePrincipalProfile`

**Role values**: `Admin`, `Member`, `Contributor`, `Viewer`

**Update role assignment** (change an existing user's role):
```
PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/roleAssignments/{roleAssignmentId}
```

```json
{
  "role": "Member"
}
```

**Delete role assignment**:
```
DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/roleAssignments/{roleAssignmentId}
```

### Automated Migration: Export Synapse → Import Fabric

#### Step 1: Export Synapse Role Assignments (ARM API)

Synapse workspace RBAC is managed via Azure RBAC. Query the ARM API for role assignments scoped to the Synapse workspace:

```python
import requests

arm_token = get_token("https://management.azure.com")
synapse_scope = (
    f"/subscriptions/{sub_id}/resourceGroups/{rg}"
    f"/providers/Microsoft.Synapse/workspaces/{ws_name}"
)

# List all role assignments on the Synapse workspace
resp = requests.get(
    f"https://management.azure.com{synapse_scope}"
    f"/providers/Microsoft.Authorization/roleAssignments"
    f"?api-version=2022-04-01&$filter=atScope()",
    headers={"Authorization": f"Bearer {arm_token}"}
)
synapse_assignments = resp.json()["value"]
```

Each assignment has:
- `properties.principalId` — Entra object ID (user, group, or SP)
- `properties.principalType` — `User`, `Group`, `ServicePrincipal`
- `properties.roleDefinitionId` — ends with the role GUID

#### Step 2: Resolve Synapse Role Names

Map Azure RBAC role definition IDs to Synapse role names:

```python
# Azure RBAC role GUIDs scoped to Synapse workspaces
# Note: Synapse Studio RBAC roles (Apache Spark Administrator, Synapse SQL Administrator,
# Linked Data Manager, Credential User) are managed via the Synapse RBAC API at
# https://{ws}.dev.azuresynapse.net/rbac/roleAssignments — they do NOT appear in ARM
# roleAssignments. The mapping below covers Azure RBAC roles only.
SYNAPSE_ROLES = {
    "6e4bf58a-b8e1-4cc3-bbf9-d73143322b78": "Synapse Administrator",
    "7af0c69a-a548-47d6-aea3-d00e69bd83aa": "Synapse SQL Administrator",
    "c3a6d2f1-a26f-4810-9b0f-591308d5cbf1": "Synapse Contributor",
    "b5c23728-2989-4e2a-9958-2c22a2689f09": "Synapse Monitoring Operator",
    "2a5c394f-5eb7-4d4f-9c8e-e8eae39faebc": "Synapse User",
}

def resolve_synapse_role(role_def_id):
    """Extract the role GUID and map to Synapse role name."""
    role_guid = role_def_id.split("/")[-1]
    return SYNAPSE_ROLES.get(role_guid, f"Unknown ({role_guid})")
```

#### Step 3: Map to Fabric Roles

```python
# Azure RBAC Synapse role → Fabric role mapping
ROLE_MAP = {
    "Synapse Administrator":       "Admin",
    "Synapse SQL Administrator":   "Admin",
    "Synapse Contributor":         "Contributor",
    "Synapse Monitoring Operator": "Viewer",
    "Synapse User":                "Viewer",
}
# Note: Synapse Studio RBAC roles (Apache Spark Administrator, Linked Data Manager,
# Credential User) are not exported via ARM. If needed, query the Synapse RBAC API
# at https://{ws}.dev.azuresynapse.net/rbac/roleAssignments separately.

# Build the migration plan
migration_plan = []
skipped = []

for assignment in synapse_assignments:
    props = assignment["properties"]
    synapse_role = resolve_synapse_role(props["roleDefinitionId"])
    fabric_role = ROLE_MAP.get(synapse_role)

    entry = {
        "principalId":   props["principalId"],
        "principalType": props.get("principalType", "User"),
        "synapseRole":   synapse_role,
        "fabricRole":    fabric_role,
    }

    if fabric_role is None:
        skipped.append(entry)
    else:
        migration_plan.append(entry)
```

#### Step 4: Present Migration Plan for Review

```python
print("RBAC Migration Plan:")
print(f"  Assignments to migrate: {len(migration_plan)}")
print(f"  Assignments skipped:    {len(skipped)}")
print()
print(f"  {'Principal ID':<40} {'Synapse Role':<30} {'Fabric Role':<15}")
print(f"  {'─'*40} {'─'*30} {'─'*15}")
for entry in migration_plan:
    print(f"  {entry['principalId']:<40} {entry['synapseRole']:<30} {entry['fabricRole']:<15}")

if skipped:
    print()
    print("  Skipped (no Fabric equivalent):")
    for entry in skipped:
        print(f"    {entry['principalId']} — {entry['synapseRole']}")
        print(f"      → Action: Configure Key Vault RBAC instead (see S3)")
```

#### Step 5: Bulk-Create Fabric Role Assignments

```python
fabric_token = get_token("https://api.fabric.microsoft.com")

# Deduplicate — if a principal has multiple Synapse roles, take the highest Fabric role
ROLE_PRIORITY = {"Admin": 4, "Member": 3, "Contributor": 2, "Viewer": 1}

principal_roles = {}
for entry in migration_plan:
    pid = entry["principalId"]
    role = entry["fabricRole"]
    if pid not in principal_roles or ROLE_PRIORITY[role] > ROLE_PRIORITY[principal_roles[pid]["fabricRole"]]:
        principal_roles[pid] = entry

# Create assignments
results = {"success": 0, "failed": 0, "errors": []}

for pid, entry in principal_roles.items():
    resp = requests.post(
        f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/roleAssignments",
        headers={
            "Authorization": f"Bearer {fabric_token}",
            "Content-Type": "application/json"
        },
        json={
            "principal": {
                "id": entry["principalId"],
                "type": entry["principalType"]
            },
            "role": entry["fabricRole"]
        }
    )

    if resp.status_code in (200, 201):
        results["success"] += 1
    elif resp.status_code == 409:
        # Assignment already exists — update instead
        # First, list existing to get the roleAssignmentId
        existing = requests.get(
            f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/roleAssignments",
            headers={"Authorization": f"Bearer {fabric_token}"}
        ).json()["value"]
        match = next((a for a in existing if a["principal"]["id"] == pid), None)
        if match:
            requests.patch(
                f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/roleAssignments/{match['id']}",
                headers={
                    "Authorization": f"Bearer {fabric_token}",
                    "Content-Type": "application/json"
                },
                json={"role": entry["fabricRole"]}
            )
            results["success"] += 1
    else:
        results["failed"] += 1
        results["errors"].append({
            "principal": pid, "role": entry["fabricRole"],
            "status": resp.status_code, "error": resp.text
        })

print(f"\nRBAC Migration Results: {results['success']} succeeded, {results['failed']} failed")
for err in results["errors"]:
    print(f"  FAILED: {err['principal']} → {err['role']} — {err['status']}: {err['error']}")
```

#### Step 6: Verify Assignments

```python
# List all Fabric role assignments and compare
resp = requests.get(
    f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}/roleAssignments",
    headers={"Authorization": f"Bearer {fabric_token}"}
)
fabric_assignments = resp.json()["value"]

print(f"\nFabric Workspace Role Assignments ({len(fabric_assignments)} total):")
print(f"  {'Display Name':<30} {'Type':<20} {'Role':<15}")
print(f"  {'─'*30} {'─'*20} {'─'*15}")
for a in fabric_assignments:
    print(f"  {a['principal'].get('displayName', 'N/A'):<30} {a['principal']['type']:<20} {a['role']:<15}")
```

### Migration Steps

1. **Export Synapse role assignments** — ARM API query (Step 1–2 above)
2. **Map to Fabric roles** — automated mapping with deduplication (Step 3)
3. **Review migration plan** — present to user for confirmation (Step 4)
4. **Bulk-create Fabric role assignments** — REST API (Step 5)
5. **Verify** — list and compare (Step 6)

> **Recommendation**: Use Entra security groups rather than individual user assignments. If Synapse assigns roles to individual users, consider creating security groups (e.g., `Fabric-{workspace}-Contributors`) and adding those users to the group, then assigning the group to the Fabric workspace role. This simplifies ongoing management.

---

## S3: Secret Management `(API)`

### Consolidating Credential Access

In Synapse, secrets are distributed across Linked Services, TokenLibrary, and Key Vault references. In Fabric, all secrets should flow through **Azure Key Vault** via `notebookutils.credentials.getSecret()`.

> **Already covered**: See [connector-refactoring.md](connector-refactoring.md) for code-level changes (TokenLibrary → Key Vault, Linked Service → direct auth). This section focuses on the **access control** side.

### Production Credential Checklist

| Task | Details |
|---|---|
| **Identify all secrets needed** | Scan migrated notebooks/SJDs for `getSecret()` calls → list all vault URLs + secret names |
| **Verify Key Vault access** | The Fabric Workspace Identity (or service principal running notebooks) must have `Key Vault Secrets User` role on each Key Vault |
| **Rotate credentials** | If migrating service principal secrets or connection strings, consider rotating at cutover |
| **Remove dev/test secrets** | Ensure production Key Vault only contains production credentials — dev/test endpoints should not be accessible from prod |
| **Audit access** | Enable Key Vault diagnostic logging → monitor which identities read which secrets |

### Key Vault Access via REST API

Grant the Fabric Workspace Identity access to Key Vault:

```
PUT https://management.azure.com/subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.KeyVault/vaults/{vaultName}/providers/Microsoft.Authorization/roleAssignments/{assignmentId}?api-version=2022-04-01
```

```json
{
  "properties": {
    "roleDefinitionId": "/subscriptions/{subId}/providers/Microsoft.Authorization/roleDefinitions/4633458b-17de-408a-b874-0445c86b69e6",
    "principalId": "{workspaceIdentityObjectId}",
    "principalType": "ServicePrincipal"
  }
}
```

> Role `4633458b-17de-408a-b874-0445c86b69e6` = Key Vault Secrets User (read-only access to secrets).

### Automated Migration: Scan Notebooks → Grant Key Vault Access

#### Step 1: Scan Notebooks for Secret References

Extract all Key Vault URLs and secret names from migrated notebooks:

```python
import re

# notebooks = list of exported notebook dicts (from Phase 2 inventory)
vault_secrets = {}  # vault_url → set of secret names
linked_services = set()  # Linked Service names (need manual resolution)

for nb in notebooks:
    nb_name = nb.get("name", "unknown")
    cells = nb.get("properties", {}).get("cells", [])
    for i, cell in enumerate(cells):
        source = "".join(cell.get("source", []))

        # Match getSecret calls with vault URL + secret name
        for match in re.finditer(
            r'getSecret\s*\(\s*["\']([^"\']+vault\.azure\.net[^"\']*)["\'],?\s*["\']([^"\']*)["\']',
            source
        ):
            vault_url = match.group(1).rstrip("/")
            secret_name = match.group(2)
            vault_secrets.setdefault(vault_url, set()).add(secret_name)
            print(f"  {nb_name} (cell {i+1}): getSecret → {vault_url} / {secret_name}")

        # Match TokenLibrary.getSecret
        for match in re.finditer(
            r'TokenLibrary\.getSecret\s*\(\s*["\']([^"\']+vault\.azure\.net[^"\']*)["\'],?\s*["\']([^"\']*)["\']',
            source
        ):
            vault_url = match.group(1).rstrip("/")
            secret_name = match.group(2)
            vault_secrets.setdefault(vault_url, set()).add(secret_name)
            print(f"  {nb_name} (cell {i+1}): TokenLibrary.getSecret → {vault_url} / {secret_name}")

        # Match getConnectionStringOrCreds (Linked Service — needs manual vault mapping)
        for match in re.finditer(
            r'getConnectionStringOrCreds\s*\(\s*["\']([^"\']+)["\']',
            source
        ):
            ls_name = match.group(1)
            linked_services.add(ls_name)
            print(f"  {nb_name} (cell {i+1}): getConnectionStringOrCreds → LinkedService: {ls_name}")

print(f"\nSummary:")
print(f"  Key Vaults discovered: {len(vault_secrets)}")
for vault_url, secrets in vault_secrets.items():
    print(f"    {vault_url}: {len(secrets)} secrets ({', '.join(sorted(secrets))})")

if linked_services:
    print(f"\n  ⚠ Linked Services still using getConnectionStringOrCreds ({len(linked_services)}):")
    for ls in sorted(linked_services):
        print(f"    - {ls}")
    print("    → These must be migrated to getSecret() first (see connector-refactoring.md)")
```

#### Step 2: Extract Vault Names and Resolve Resource IDs

```python
vault_resources = {}

for vault_url in vault_secrets:
    # Extract vault name from URL: https://myvault.vault.azure.net → myvault
    vault_name = vault_url.replace("https://", "").split(".")[0]

    # Resolve the vault's resource ID via ARM (try known resource group first, then search)
    resp = requests.get(
        f"https://management.azure.com/subscriptions/{sub_id}/resourceGroups/{rg}"
        f"/providers/Microsoft.KeyVault/vaults/{vault_name}?api-version=2022-07-01",
        headers={"Authorization": f"Bearer {arm_token}"}
    )

    if resp.status_code == 200:
        vault_resources[vault_name] = resp.json()["id"]
    else:
        # Search across all resource groups
        search_resp = requests.get(
            f"https://management.azure.com/subscriptions/{sub_id}"
            f"/resources?$filter=resourceType eq 'Microsoft.KeyVault/vaults'"
            f" and name eq '{vault_name}'&api-version=2021-04-01",
            headers={"Authorization": f"Bearer {arm_token}"}
        )
        matches = search_resp.json().get("value", [])
        if matches:
            vault_resources[vault_name] = matches[0]["id"]
        else:
            print(f"  ⚠ Could not find vault: {vault_name}")

print(f"\nResolved {len(vault_resources)} vault resource IDs")
```

#### Step 3: Grant Key Vault Secrets User to Workspace Identity

```python
import uuid

KEY_VAULT_SECRETS_USER = "4633458b-17de-408a-b874-0445c86b69e6"

# Get Workspace Identity service principal ID (from S1 Step 4)
ws_resp = requests.get(
    f"https://api.fabric.microsoft.com/v1/workspaces/{fabric_ws_id}",
    headers={"Authorization": f"Bearer {fabric_token}"}
)
ws_identity_id = ws_resp.json().get("identity", {}).get("servicePrincipalId")

if not ws_identity_id:
    print("ERROR: Workspace Identity not enabled. Run S1 first.")
else:
    results = {"granted": 0, "exists": 0, "failed": 0}

    for vault_name, vault_resource_id in vault_resources.items():
        assignment_id = str(uuid.uuid4())

        resp = requests.put(
            f"https://management.azure.com{vault_resource_id}"
            f"/providers/Microsoft.Authorization/roleAssignments/{assignment_id}"
            f"?api-version=2022-04-01",
            headers={
                "Authorization": f"Bearer {arm_token}",
                "Content-Type": "application/json"
            },
            json={
                "properties": {
                    "roleDefinitionId": f"/subscriptions/{sub_id}/providers/Microsoft.Authorization/roleDefinitions/{KEY_VAULT_SECRETS_USER}",
                    "principalId": ws_identity_id,
                    "principalType": "ServicePrincipal"
                }
            }
        )

        if resp.status_code in (200, 201):
            results["granted"] += 1
            print(f"  ✓ Granted Key Vault Secrets User on {vault_name}")
        elif resp.status_code == 409:
            results["exists"] += 1
            print(f"  ✓ Already granted on {vault_name}")
        else:
            results["failed"] += 1
            print(f"  ✗ Failed on {vault_name}: {resp.status_code} — {resp.text}")

    print(f"\nKey Vault access: {results['granted']} granted, {results['exists']} existed, {results['failed']} failed")
```

#### Step 4: Verify Access

```python
# Test secret retrieval for each vault (requires running from a Fabric notebook)
# This step must be executed inside a Fabric notebook after deployment:

# for vault_url, secrets in vault_secrets.items():
#     for secret_name in secrets:
#         try:
#             val = notebookutils.credentials.getSecret(vault_url, secret_name)
#             print(f"  ✓ {vault_url}/{secret_name} — accessible")
#         except Exception as e:
#             print(f"  ✗ {vault_url}/{secret_name} — {e}")
```

> **Note**: Step 4 must run inside a Fabric notebook (it uses `notebookutils`). Steps 1–3 can run from any Python environment with Azure credentials.

---

## S4: Governance & Compliance `(API)`

### Synapse → Fabric Governance Mapping

| Synapse Governance Feature | Fabric Equivalent | Migration Action |
|---|---|---|
| **Purview scan** (configured separately) | **Purview Hub** (built into Fabric — no separate scan needed) | Fabric items are automatically registered in Purview when connected. No manual scan configuration required |
| **Data classification** (Purview labels) | **Sensitivity labels** (Microsoft Information Protection — MIP) | Apply MIP sensitivity labels to Fabric items via Portal or REST API |
| **Endorsement** | **Endorsement** (Promoted / Certified) | Mark production items as Certified after validation |
| **Data lineage** (configured via Purview) | **Automatic lineage** (built into Fabric) | Fabric tracks lineage automatically — no configuration needed |
| **Audit logs** (Azure Monitor) | **Fabric audit logs** (Microsoft 365 audit log) | Configure audit log export to your SIEM/monitoring solution |

### Sensitivity Labels

Apply sensitivity labels to production items to classify data (e.g., Confidential, Internal, Public):

```
PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}
```

```json
{
  "sensitivityLabel": {
    "labelId": "{mipLabelId}"
  }
}
```

> Sensitivity labels are inherited: setting a label on a Lakehouse propagates to downstream items (datasets, reports) that consume its data.

### Endorsement

Mark validated production items as Certified:

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/endorse
```

```json
{
  "endorsement": "Certified"
}
```

Values: `None`, `Promoted`, `Certified` (Certified requires tenant admin to grant certification permission to the user).

---

## S5: Data-Level Security `(Partial — T-SQL + Portal)`

### OneLake RBAC (Table/Folder-Level Permissions)

OneLake RBAC controls **read access** to specific tables or folders within a Lakehouse. This replaces Synapse's per-database access model.

> **Scope**: OneLake RBAC applies to the **Tables/** and **Files/** sections of a Lakehouse. By default, all workspace members can read all data. OneLake RBAC **restricts** access — it's a deny-by-default model once enabled.
>
> **Automation note**: OneLake RBAC now has a **public REST API** — [`OneLake Data Access Security`](https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-data-access-security) provides CRUD operations for data access roles:
> - `PUT /v1/workspaces/{wsId}/items/{itemId}/dataAccessRoles` — create/update roles
> - `GET /v1/workspaces/{wsId}/items/{itemId}/dataAccessRoles` — list roles
> - `DELETE /v1/workspaces/{wsId}/items/{itemId}/dataAccessRoles/{roleName}` — delete a role
>
> RLS/CLS/DDM are T-SQL statements that can be scripted and executed via the SQL endpoint.

#### When to Use OneLake RBAC

| Synapse Pattern | Fabric Equivalent |
|---|---|
| Separate databases with different ACLs | Single Lakehouse with OneLake RBAC per schema/table, **or** separate Lakehouses (each with independent workspace RBAC) |
| Per-table access control in same database | OneLake RBAC roles on specific tables |
| No data-level security (all users see all) | No OneLake RBAC needed — workspace RBAC is sufficient |

#### OneLake RBAC Configuration

**Define a custom role** (via Fabric Portal → Lakehouse → Manage OneLake data access):

| Setting | Description |
|---|---|
| Role name | Descriptive name (e.g., `sales_readers`) |
| Assign members | Users, groups, or service principals |
| Permissions | `Read` or `ReadAll` on specific folders/tables |
| Folder scope | `Tables/sales/*`, `Tables/marketing/*`, `Files/raw/*`, etc. |

**Example**: Restrict so that only the Sales team can read `Tables/sales/` and only Marketing can read `Tables/marketing/`:

| Role | Members | Permission | Scope |
|---|---|---|---|
| `sales_readers` | Sales security group | Read | `Tables/sales/**` |
| `marketing_readers` | Marketing security group | Read | `Tables/marketing/**` |
| `etl_full_access` | ETL service principal | ReadAll | `Tables/**`, `Files/**` |

> **Important**: Once OneLake RBAC is enabled on a Lakehouse, users without an explicit role assignment **lose read access** to the protected folders. Plan carefully before enabling.

### SQL Endpoint Security (RLS, CLS, DDM)

If Synapse Dedicated SQL Pool uses row-level security, column-level security, or dynamic data masking, these must be recreated on the Fabric SQL endpoint.

| Feature | Synapse Dedicated SQL Pool | Fabric SQL Endpoint / Warehouse | Migration Action |
|---|---|---|---|
| **Row-Level Security (RLS)** | `CREATE SECURITY POLICY` + `FUNCTION` | Supported on Warehouse & SQL endpoint | Recreate security policies and filter predicates |
| **Column-Level Security (CLS)** | `GRANT SELECT (col1, col2)` | Supported on Warehouse & SQL endpoint | Recreate column-level `GRANT` statements |
| **Dynamic Data Masking (DDM)** | `ALTER TABLE ... ADD MASKED` | Supported on Warehouse & SQL endpoint | Recreate masking definitions |

> **Spark limitation**: RLS, CLS, and DDM apply to the **SQL endpoint only**. Spark notebooks reading from `Tables/` via OneLake access the underlying files directly and **bypass** SQL-level security policies. Use OneLake RBAC (folder-level) to restrict Spark access.

### Migration Steps for Data-Level Security

1. **Audit Synapse security policies** — export RLS policies, CLS grants, and DDM definitions from Dedicated SQL Pool
2. **Decide enforcement layer**:
   - SQL consumers only → recreate on Fabric SQL endpoint
   - Spark consumers too → use OneLake RBAC for folder-level restriction
   - Both → combine OneLake RBAC + SQL endpoint policies
3. **Recreate policies** on the Fabric Warehouse or Lakehouse SQL endpoint
4. **Test** — verify that restricted users cannot access protected data through both SQL and Spark

### Automated Migration: Export Synapse RLS/CLS/DDM → Recreate on Fabric

> **Prerequisites**: `sqlcmd` (Go version) installed, or `pyodbc` available. These scripts query Synapse Dedicated SQL Pool system views and generate T-SQL to recreate policies on Fabric.

#### Step 1: Export RLS Policies from Synapse

Query Synapse Dedicated SQL Pool to extract all security policies and their filter predicates:

```sql
-- Run against Synapse Dedicated SQL Pool
-- Export RLS security policies, filter functions, and predicate bindings

-- 1a. List all security policies
SELECT
    p.name AS policy_name,
    p.is_enabled,
    SCHEMA_NAME(p.schema_id) AS policy_schema
FROM sys.security_policies p
ORDER BY p.name;

-- 1b. List all filter predicate functions
SELECT
    SCHEMA_NAME(o.schema_id) AS function_schema,
    o.name AS function_name,
    m.definition AS function_definition
FROM sys.objects o
JOIN sys.sql_modules m ON o.object_id = m.object_id
WHERE o.type = 'IF'  -- Inline table-valued function
ORDER BY o.name;

-- 1c. List all security predicates (bindings)
SELECT
    sp.security_policy_id,
    pol.name AS policy_name,
    sp.predicate_type_desc,
    SCHEMA_NAME(t.schema_id) + '.' + t.name AS target_table,
    sp.predicate_definition AS filter_predicate
FROM sys.security_predicates sp
JOIN sys.security_policies pol ON sp.security_policy_id = pol.object_id
JOIN sys.objects t ON sp.target_object_id = t.object_id
ORDER BY pol.name;
```

#### Step 2: Export CLS Grants from Synapse

```sql
-- Run against Synapse Dedicated SQL Pool
-- Export column-level GRANT/DENY permissions

SELECT
    dp.state_desc AS permission_state,  -- GRANT or DENY
    dp.permission_name,
    SCHEMA_NAME(o.schema_id) + '.' + o.name AS table_name,
    c.name AS column_name,
    pr.name AS grantee_name,
    pr.type_desc AS grantee_type
FROM sys.database_permissions dp
JOIN sys.objects o ON dp.major_id = o.object_id
JOIN sys.columns c ON dp.major_id = c.object_id AND dp.minor_id = c.column_id
JOIN sys.database_principals pr ON dp.grantee_principal_id = pr.principal_id
WHERE dp.minor_id > 0  -- Column-level permissions only
ORDER BY table_name, column_name, grantee_name;
```

#### Step 3: Export DDM Definitions from Synapse

```sql
-- Run against Synapse Dedicated SQL Pool
-- Export Dynamic Data Masking definitions

SELECT
    SCHEMA_NAME(t.schema_id) + '.' + t.name AS table_name,
    c.name AS column_name,
    c.masking_function AS mask_function
FROM sys.masked_columns c
JOIN sys.tables t ON c.object_id = t.object_id
WHERE c.is_masked = 1
ORDER BY table_name, column_name;
```

#### Step 4: Generate Fabric-Compatible T-SQL

Python script to query Synapse, extract policies, and generate T-SQL for Fabric:

```python
import pyodbc

# Connect to Synapse Dedicated SQL Pool
synapse_conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={synapse_sql_endpoint};"
    f"DATABASE={dedicated_pool_name};"
    f"Authentication=ActiveDirectoryDefault;"
)
cursor = synapse_conn.cursor()

fabric_sql_statements = []

# --- RLS: Export filter functions + security policies ---
cursor.execute("""
    SELECT SCHEMA_NAME(o.schema_id) AS fn_schema, o.name AS fn_name, m.definition
    FROM sys.objects o
    JOIN sys.sql_modules m ON o.object_id = m.object_id
    WHERE o.type = 'IF'
""")
for row in cursor.fetchall():
    fabric_sql_statements.append(f"-- RLS filter function: {row.fn_schema}.{row.fn_name}")
    fabric_sql_statements.append(row.definition + ";")
    fabric_sql_statements.append("")

cursor.execute("""
    SELECT pol.name AS policy_name, pol.is_enabled,
           sp.predicate_type_desc,
           SCHEMA_NAME(t.schema_id) + '.' + t.name AS target_table,
           sp.predicate_definition AS filter_predicate
    FROM sys.security_predicates sp
    JOIN sys.security_policies pol ON sp.security_policy_id = pol.object_id
    JOIN sys.objects t ON sp.target_object_id = t.object_id
    ORDER BY pol.name
""")
policies = {}
for row in cursor.fetchall():
    if row.policy_name not in policies:
        policies[row.policy_name] = {"enabled": row.is_enabled, "predicates": []}
    policies[row.policy_name]["predicates"].append({
        "type": row.predicate_type_desc,
        "table": row.target_table,
        "predicate": row.filter_predicate
    })

for policy_name, policy in policies.items():
    predicates = ", ".join(
        f"ADD {p['type']} PREDICATE {p['predicate']} ON {p['table']}"
        for p in policy["predicates"]
    )
    state = "ON" if policy["enabled"] else "OFF"
    fabric_sql_statements.append(f"-- RLS policy: {policy_name}")
    fabric_sql_statements.append(f"CREATE SECURITY POLICY {policy_name}")
    fabric_sql_statements.append(f"    {predicates}")
    fabric_sql_statements.append(f"    WITH (STATE = {state});")
    fabric_sql_statements.append("")

# --- CLS: Export column-level grants ---
cursor.execute("""
    SELECT dp.state_desc, dp.permission_name,
           SCHEMA_NAME(o.schema_id) + '.' + o.name AS table_name,
           c.name AS column_name, pr.name AS grantee
    FROM sys.database_permissions dp
    JOIN sys.objects o ON dp.major_id = o.object_id
    JOIN sys.columns c ON dp.major_id = c.object_id AND dp.minor_id = c.column_id
    JOIN sys.database_principals pr ON dp.grantee_principal_id = pr.principal_id
    WHERE dp.minor_id > 0
    ORDER BY table_name, column_name
""")
for row in cursor.fetchall():
    fabric_sql_statements.append(
        f"-- CLS: {row.state_desc} {row.permission_name} on {row.table_name}.{row.column_name}")
    fabric_sql_statements.append(
        f"{row.state_desc} {row.permission_name} ON {row.table_name}({row.column_name}) TO [{row.grantee}];")
    fabric_sql_statements.append("")

# --- DDM: Export masking definitions ---
cursor.execute("""
    SELECT SCHEMA_NAME(t.schema_id) + '.' + t.name AS table_name,
           c.name AS column_name, c.masking_function
    FROM sys.masked_columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    WHERE c.is_masked = 1
""")
for row in cursor.fetchall():
    fabric_sql_statements.append(
        f"-- DDM: Mask {row.table_name}.{row.column_name}")
    fabric_sql_statements.append(
        f"ALTER TABLE {row.table_name} ALTER COLUMN {row.column_name} "
        f"ADD MASKED WITH (FUNCTION = '{row.masking_function}');")
    fabric_sql_statements.append("")

synapse_conn.close()

# Write output
output = "\n".join(fabric_sql_statements)
print(f"Generated {len(fabric_sql_statements)} T-SQL statements")
print(output)

# Save to file for review before execution
with open("fabric-security-policies.sql", "w") as f:
    f.write(output)
print("\nSaved to fabric-security-policies.sql — review before executing on Fabric SQL endpoint")
```

#### Step 5: Apply to Fabric SQL Endpoint

Execute the generated SQL against the Fabric SQL endpoint using `sqlcmd` (see [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) for connection setup):

```bash
# Review the generated SQL first, then execute against Fabric SQL endpoint
sqlcmd -S {fabric_sql_endpoint} -d {warehouse_or_lakehouse_name} \
    -G -i fabric-security-policies.sql
```

> **Important considerations**:
> - **Grantee names**: Synapse may use database-level users (SQL auth). Fabric requires Entra identities. Update `grantee` names in the generated SQL to match Entra user/group names.
> - **Schema differences**: If table schemas changed during migration (e.g., from `dbo` to `bronze`), update table references in the generated SQL.
> - **Test with restricted users**: After applying, connect as a restricted user and verify they cannot see masked/filtered data.
> - **Spark bypass**: Remember that RLS/CLS/DDM only apply to SQL endpoint queries. Spark reads bypass these. Use OneLake RBAC (above) for Spark access control.

---

## S6: Network Security `(Manual — Portal / Admin)`

### Synapse → Fabric Network Mapping

| Synapse Network Feature | Fabric Equivalent | Key Difference |
|---|---|---|
| Managed Virtual Network | **Managed Private Endpoints** (capacity-level) | Fabric MPE is configured at the **capacity** level, not per workspace. All workspaces in a capacity share the same MPE configuration |
| Managed Private Endpoints (per workspace) | **Managed Private Endpoints** (per capacity) | Same concept, different scope |
| Workspace Firewall (IP rules) | **Conditional Access policies** + tenant-level IP restrictions | No workspace-level firewall in Fabric; use Entra Conditional Access |
| Synapse Private Link Hub | **Fabric Private Link** | For private connectivity to Fabric from on-prem or VNets |
| Data exfiltration protection | **Capacity-level outbound restrictions** | Configure in Fabric capacity admin settings |

> **Automation note**: Managed Private Endpoints, Conditional Access, and Private Link are configured via the Fabric admin portal and Entra admin center — not via workspace-level REST APIs. These require capacity admin or tenant admin privileges.

### When Network Security Matters

| Scenario | Action Required |
|---|---|
| Synapse has Managed VNet + Private Endpoints to Azure SQL, Cosmos DB, Storage | Configure Fabric Managed Private Endpoints on the capacity for the same targets |
| Synapse workspace has IP firewall rules | Configure Entra Conditional Access policies with named locations |
| Synapse uses Private Link for client access | Set up Fabric Private Link for VNet-connected clients |
| No network restrictions in Synapse | None — Fabric works over public endpoints by default |

> For detailed setup instructions, see [Microsoft Docs: Managed Private Endpoints in Fabric](https://learn.microsoft.com/fabric/security/security-managed-private-endpoints-overview).

---

## S7: On-Premises Data Gateway (OPDG) `(Manual — Install)`

### When OPDG Is Needed

| Source | Synapse Mechanism | Fabric Mechanism |
|---|---|---|
| On-premises SQL Server | Self-hosted Integration Runtime | **OPDG** (On-Premises Data Gateway) |
| On-premises file shares | Self-hosted IR | **OPDG** |
| On-premises Oracle, SAP, etc. | Self-hosted IR | **OPDG** |
| Cloud-only sources (ADLS, Azure SQL, Cosmos DB) | Managed VNet + Private Endpoints | Fabric MPE — **no OPDG needed** |

> **Automation note**: OPDG requires physical installation on a machine with network access to on-prem sources. This cannot be automated via REST API.

### Migration Steps

1. **Identify on-prem sources** — check Synapse Linked Services for self-hosted IR references
2. **Install OPDG** on a machine with network access to on-prem sources (same machine as self-hosted IR, or new)
3. **Register gateway** in Fabric tenant settings (Power Platform admin center)
4. **Create Fabric connections** that use the gateway for on-prem sources
5. **Test connectivity** from a Fabric notebook or pipeline

> For detailed OPDG installation and configuration, see [Microsoft Docs: On-premises data gateway](https://learn.microsoft.com/data-integration/gateway/service-gateway-install).

---

## S8: Production Security Checklist

Run through this checklist before opening the production workspace to end users.

### Identity & Authentication

- [ ] Fabric Workspace Identity is enabled and has Storage Blob Data Reader on all referenced ADLS accounts
- [ ] All service principals used by notebooks/SJDs are registered in the workspace
- [ ] No notebooks rely on SQL authentication — all use Entra-based auth
- [ ] Token acquisition tested: `notebookutils.credentials.getToken()` returns valid tokens

### Workspace RBAC

- [ ] Synapse role assignments mapped to Fabric roles (see S2 mapping table)
- [ ] Security groups assigned to workspace roles (prefer groups over individual users)
- [ ] No unnecessary Admin role assignments — principle of least privilege
- [ ] Verified: Contributors cannot manage access; Viewers cannot run notebooks

### Data-Level Security

- [ ] OneLake RBAC configured on Lakehouses with sensitive data (if applicable)
- [ ] RLS/CLS/DDM policies recreated on Fabric SQL endpoint (if migrated from Dedicated SQL Pool)
- [ ] Verified: restricted users cannot access protected data via both SQL and Spark paths
- [ ] Verified: ETL service principals have full data access for pipeline execution

### Network Security

- [ ] Managed Private Endpoints configured on Fabric capacity for all required targets (if applicable)
- [ ] Entra Conditional Access policies applied (if replacing Synapse workspace firewall)
- [ ] Fabric Private Link configured (if on-prem clients need private connectivity)
- [ ] Verified: notebooks/SJDs can reach all external data sources through MPE

### Secret Management

- [ ] All required secrets exist in production Key Vault
- [ ] Fabric Workspace Identity has Key Vault Secrets User role on production Key Vault
- [ ] Dev/test secrets are not accessible from production workspace
- [ ] Key Vault diagnostic logging enabled

### On-Premises Data Gateway

- [ ] OPDG installed and registered (if on-prem sources exist)
- [ ] Fabric connections configured to use the gateway
- [ ] Tested: notebooks/pipelines can read from on-prem sources

### Governance

- [ ] Fabric workspace connected to Purview (verify items appear in Purview catalog)
- [ ] Sensitivity labels applied to items with classified data
- [ ] Production items endorsed as Certified
- [ ] Audit log export configured

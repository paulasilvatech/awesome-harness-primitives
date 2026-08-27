# Linked Services → Fabric Connections

Reference for mapping Synapse Analytics linked service types to Fabric Connection types for use in pipeline activities.

> **Scope**: This file covers pipeline-oriented connection migration. For notebook connectivity (ADLS shortcuts, `notebookutils.credentials`), see the **synapse-migration** skill's [connectivity-migration.md](../../synapse-migration/resources/connectivity-migration.md).

---

## Decision Guide

| Synapse Linked Service Type | Fabric Connection Type | Notes |
|---|---|---|
| **Azure Data Lake Storage Gen2** | `AzureDataLakeStorage` | Most common — used by Copy, Lookup, GetMetadata, Delete |
| **Azure Blob Storage** | `AzureBlobStorage` | Blob-based sources and sinks |
| **Azure SQL Database** | `AzureSqlDatabase` | SQL source/sink in Copy; Script, Lookup |
| **Azure SQL Managed Instance** | `SqlServerDatabase` | MI connection type |
| **Azure Synapse Analytics (Dedicated SQL)** | `AzureSqlDatabase` or direct Fabric Warehouse ref | Post-migration, the pool becomes a Fabric Warehouse |
| **Azure Database for PostgreSQL** | `PostgreSqlDatabase` | |
| **Azure Database for MySQL** | `MySqlDatabase` | |
| **Azure Cosmos DB (SQL API)** | `CosmosDb` | |
| **Azure Event Hubs** | `AzureEventHubs` | Pipeline event-based activities |
| **Azure Service Bus** | `AzureServiceBus` | |
| **REST / HTTP** | `RestService` or `ODataRest` | Generic REST calls; also covered by WebActivity (no connection) |
| **Key Vault** | Not needed as a connection | Pipeline options: (1) `WebActivity` with MSI to call Key Vault REST API, (2) pipeline parameter typed as `SecureString`, or (3) store non-secret config in a Variable Library |
| **File System** | `FileServer` | On-premises; requires on-premises data gateway |
| **SQL Server (on-premises)** | `SqlServerDatabase` | On-premises; requires on-premises data gateway |
| **Oracle** | `Oracle` | On-premises or cloud; gateway may be required |
| **SAP** (any) | ⚠️ Check Fabric connector support | Many SAP connectors require gateway |
| **Teradata** | `Teradata` | Requires on-premises data gateway |
| **Amazon S3** | `AmazonS3` | |
| **Google Cloud Storage** | `GoogleCloudStorage` | |
| **FTP / SFTP** | `Ftp` / `Sftp` | |
| **SharePoint** | `SharePointOnlineList` | |
| **Dynamics 365** | `Dynamics` | |
| **Salesforce** | `Salesforce` | |

> **For Self-Hosted Integration Runtime (SHIR) backed linked services**: see [pipeline-gotchas.md § PG5](pipeline-gotchas.md#pg5--self-hosted-ir-activities-require-on-premises-data-gateway) — you must configure an on-premises data gateway in Fabric.

---

## How Fabric Connections Work in Pipelines

In Fabric Data Factory, connections are workspace-level resources. A pipeline activity references a connection by name via a `LinkedServiceReference` set on **`activity.linkedService`** — a root-level activity property that is a sibling of `typeProperties`, not nested inside `source`/`sink`/`dataset`. (For cross-system Copy activities, the second connection is embedded under `typeProperties.sink.linkedService`; see `dataset-inlining.md` and `activity-mapping.md`.) Connection display names in Fabric and linked service names in Synapse are independent values — but if you create the Fabric connection using the same display name as the Synapse linked service, the `referenceName` fields in your migrated pipeline JSON will resolve as-is with no remapping needed.

> If you intentionally use different names (e.g. environment-prefixed Fabric connections like `ADLS_Production_Connection`), you must maintain a Synapse-name → Fabric-name mapping and rewrite each `referenceName` during migration. See the Name-Matching Strategy below.

### Name-Matching Strategy

The simplest migration approach is to **create Fabric connections with the same display name as the Synapse linked service**. This means the `referenceName` fields in your pipeline activity JSON need no changes after inlining datasets.

If names differ, you must maintain a mapping table:
```json
{
  "AzureDataLakeStorage1": "ADLS_Production_Connection",
  "AzureSqlDB_Sales": "SQL_Sales_Connection"
}
```

---

## Creating Fabric Connections via API

### List Existing Connections

```bash
FABRIC_TOKEN="<fabric-token>"

az rest --method GET \
  --headers "Authorization=Bearer ${FABRIC_TOKEN}" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --query "value[].{name:displayName, type:connectionDetails.type, id:id}" -o table
```

### Create a Connection

The connection creation API is:
```
POST https://api.fabric.microsoft.com/v1/connections
```

Connection creation requires `connectivityType`, `displayName`, `connectionDetails` (with `type`, `creationMethod`, and `parameters`), and `credentialDetails` (with `credentials` nested inside). Connector identity comes from `connectionDetails.type` + `connectionDetails.creationMethod` — there is no top-level `connectorId` field. See the [Create Connection REST API reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/create-connection) and use [ListSupportedConnectionTypes](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/list-supported-connection-types) to discover the exact `type` / `creationMethod` / parameter names for each connector.

> **Note**: As of mid-2025, connection creation via API requires interactive OAuth for some connector types. For fully automated creation, use the Fabric portal and note the resulting connection name for use in pipeline JSON.

#### Example: Azure Data Lake Storage Gen2

```bash
az rest --method POST \
  --headers "Authorization=Bearer ${FABRIC_TOKEN}" "Content-Type=application/json" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --body '{
    "connectivityType": "ShareableCloud",
    "displayName": "AzureDataLakeStorage1",
    "connectionDetails": {
      "type": "AzureDataLakeStorage",
      "creationMethod": "AzureDataLakeStorage",
      "parameters": [
        {
          "dataType": "Text",
          "name": "server",
          "value": "https://<storageaccount>.dfs.core.windows.net"
        }
      ]
    },
    "credentialDetails": {
      "singleSignOnType": "None",
      "connectionEncryption": "NotEncrypted",
      "skipTestConnection": false,
      "credentials": {
        "credentialType": "WorkspaceIdentity"
      }
    }
  }'
```

> **Payload shape (critical):** Per the [Create Connection REST API](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/create-connection), the body has **no top-level `connectorId` field**. Connector identity comes from `connectionDetails.type` + `connectionDetails.creationMethod`. Credentials live under `credentialDetails.credentials` (not `credentialDetails.singleCredential`). The exact `parameters` names (`server`, `database`, `path`, etc.) vary per connector — discover them via [ListSupportedConnectionTypes](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/list-supported-connection-types) before constructing the body.

#### Example: Azure SQL Database

```bash
az rest --method POST \
  --headers "Authorization=Bearer ${FABRIC_TOKEN}" "Content-Type=application/json" \
  --url "https://api.fabric.microsoft.com/v1/connections" \
  --body '{
    "connectivityType": "ShareableCloud",
    "displayName": "AzureSqlDB_Sales",
    "connectionDetails": {
      "type": "AzureSqlDatabase",
      "creationMethod": "AzureSqlDatabase",
      "parameters": [
        {
          "dataType": "Text",
          "name": "server",
          "value": "<server>.database.windows.net"
        },
        {
          "dataType": "Text",
          "name": "database",
          "value": "<database-name>"
        }
      ]
    },
    "credentialDetails": {
      "singleSignOnType": "None",
      "connectionEncryption": "NotEncrypted",
      "skipTestConnection": false,
      "credentials": {
        "credentialType": "WorkspaceIdentity"
      }
    }
  }'
```

> For ServicePrincipal auth, replace the `credentials` block under `credentialDetails` with `{"credentialType": "ServicePrincipal", "tenantId": "...", "servicePrincipalClientId": "...", "servicePrincipalSecret": "..."}` and supply via `--body @body.json` (see the security note below — never pass `servicePrincipalSecret` inline).

> **Security note**: Never pass `servicePrincipalSecret` (or any secret credential value) as a literal string in a shell command — it will appear in shell history and process logs. The credential lives at `credentialDetails.credentials.servicePrincipalSecret` in the request body. Prefer one of:
> - **WorkspaceIdentity** (managed identity) — set `credentialDetails.credentials.credentialType` to `"WorkspaceIdentity"` and omit secret fields entirely. This is the recommended approach when the Fabric workspace has a managed identity assigned.
> - **File redirection** *(recommended for service-principal flows)*: write the JSON body to a temp file with restricted permissions and pass `--body @body.json`. The secret never appears on the command line or in `ps` output.
>
>   **Linux/macOS** (`chmod 600` for owner-only access):
>   ```bash
>   printf '{"credentialDetails":{"singleSignOnType":"None","connectionEncryption":"NotEncrypted","skipTestConnection":false,"credentials":{"credentialType":"ServicePrincipal","servicePrincipalClientId":"...","servicePrincipalSecret":"%s","tenantId":"..."}}}' "$MY_SP_SECRET" > /tmp/conn_body.json
>   chmod 600 /tmp/conn_body.json
>   az rest --method POST --url "..." --body @/tmp/conn_body.json
>   rm /tmp/conn_body.json
>   ```
>
>   **Windows PowerShell** (`icacls` to restrict the ACL to the current user, then delete; uses `$env:TEMP` so the path is portable across user profiles):
>   ```powershell
>   $body = "{`"credentialDetails`":{`"singleSignOnType`":`"None`",`"connectionEncryption`":`"NotEncrypted`",`"skipTestConnection`":false,`"credentials`":{`"credentialType`":`"ServicePrincipal`",`"servicePrincipalClientId`":`"...`",`"servicePrincipalSecret`":`"$env:MY_SP_SECRET`",`"tenantId`":`"...`"}}}"
>   $tmp  = Join-Path $env:TEMP "conn_body.json"
>   Set-Content -Path $tmp -Value $body -Encoding UTF8 -NoNewline
>   icacls $tmp /inheritance:r /grant:r "$($env:USERNAME):(R,W)" | Out-Null
>   az rest --method POST --url "..." --body "@$tmp"
>   Remove-Item $tmp -Force
>   ```
> - **Environment variable** *(requires double-quoted JSON)*: if you prefer an inline command, use double-quotes around the JSON body so the shell expands `$MY_SP_SECRET`; single-quoted strings silently embed the literal text `$MY_SP_SECRET` instead of the value:
>   ```bash
>   az rest --method POST --url "..." \
>     --body "{\"credentialDetails\":{\"singleSignOnType\":\"None\",\"connectionEncryption\":\"NotEncrypted\",\"skipTestConnection\":false,\"credentials\":{\"credentialType\":\"ServicePrincipal\",\"servicePrincipalClientId\":\"...\",\"servicePrincipalSecret\":\"$MY_SP_SECRET\",\"tenantId\":\"...\"}}}"
>   ```
>   Ensure `MY_SP_SECRET` is set only in the current session and not exported to child processes (`export` is optional; avoid writing it to `.bashrc`/`.profile`).

---

## Credential Type Mapping

| Synapse Auth Method | Fabric Credential Type |
|---|---|
| Managed Identity | `WorkspaceIdentity` |
| Service Principal (client secret) | `ServicePrincipal` |
| Service Principal (certificate) | `ServicePrincipalCertificate` |
| Account Key (storage) | `Key` |
| SQL Authentication (username/password) | `Basic` |
| OAuth2 | `OAuth2` |
| Anonymous | `Anonymous` |

> **Prefer `WorkspaceIdentity`** over service principal or key-based credentials where possible — it eliminates secret rotation and aligns with Fabric's identity model.

---

## Extracting Linked Service Configuration from Synapse

```python
import requests, json

SYNAPSE_TOKEN = "<synapse-data-plane-token>"
SYNAPSE_ENDPOINT = "https://myworkspace.dev.azuresynapse.net"
headers = {"Authorization": f"Bearer {SYNAPSE_TOKEN}"}

def get_all_linked_services():
    url = f"{SYNAPSE_ENDPOINT}/linkedservices?api-version=2020-12-01"
    items = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("value", []))
        url = data.get("nextLink")
    return items

linked_services = get_all_linked_services()

for ls in linked_services:
    name = ls["name"]
    ls_type = ls["properties"]["type"]
    connect_via = ls["properties"].get("connectVia", {}).get("referenceName", "AutoResolveIntegrationRuntime")
    print(f"  {name}: {ls_type} (via {connect_via})")
```

---

## Integration Runtime (IR) → Gateway Mapping

| Synapse IR Type | Fabric Equivalent |
|---|---|
| `AutoResolveIntegrationRuntime` | Cloud / built-in (no action needed) |
| `ManagedIntegrationRuntime` | Fabric-managed cloud compute (no action needed) |
| Self-Hosted IR (`IntegrationRuntimeReference`) | **On-premises data gateway** — must be installed and registered in Fabric |
| Azure Integration Runtime (specific region) | Fabric uses regional compute automatically (no explicit IR selection) |

> **SHIR → Gateway**: The Fabric portal path is: **Settings → Manage connections and gateways → On-premises data gateways**. Install the on-premises data gateway and register it before creating SHIR-backed connections in Fabric. See [pipeline-gotchas.md § PG5](pipeline-gotchas.md#pg5--self-hosted-ir-activities-require-on-premises-data-gateway) for the full procedure.

---

## Build Linked Service → Connection Map (Script)

> **Convention note (display name vs GUID)**: This skill standardizes on the connection **display name** in pipeline activity `linkedService.referenceName` blocks. The canonical Copy-activity alternative is to reference the connection **GUID** via `externalReferences.connection` in the activity's `typeProperties`. Both forms are accepted by the Fabric pipeline runtime; the display-name form is preferred here because (a) it round-trips cleanly through `get_connection_id_map()` without an extra GUID-resolution step at author time and (b) it keeps the generated pipeline JSON diff-readable when a connection is recreated with the same name but a new GUID. Both forms have been hand-validated against a live Fabric workspace as of June 2026. If you have a strict policy requiring GUID references, swap the `referenceName` for an `externalReferences.connection` entry per the [Fabric Copy activity reference](https://learn.microsoft.com/en-us/fabric/data-factory/copy-data-activity) — the rest of the migration flow is unchanged.

After creating all Fabric connections, build the mapping file used by dataset inlining and activity transformation:

```python
import requests, json
from urllib.parse import quote

FABRIC_TOKEN = "<fabric-token>"
headers = {"Authorization": f"Bearer {FABRIC_TOKEN}"}

def get_connection_id_map():
    """Return {connectionDisplayName: connectionId} for API operations (e.g. verifying a connection exists).

    NOTE: Pipeline activity JSON uses the connection display name in referenceName — NOT the GUID.
    Use the keys of this map (display names) when writing pipeline JSON.
    Use the values (GUIDs) only for Fabric API calls that require a connection ID.
    """
    url = "https://api.fabric.microsoft.com/v1/connections"
    connections = {}
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        for c in data.get("value", []):
            connections[c["displayName"]] = c["id"]
        cont = data.get("continuationToken")
        # Fabric continuation tokens are base64-like and routinely contain
        # '+', '/', '=' which must be percent-encoded; raw concatenation
        # breaks pagination on workspaces with > 1 page of connections.
        url = (
            f"https://api.fabric.microsoft.com/v1/connections"
            f"?continuationToken={quote(cont, safe='')}"
        ) if cont else None
    return connections

connection_id_map = get_connection_id_map()
print(json.dumps(connection_id_map, indent=2))
# {
#   "AzureDataLakeStorage1": "aaaa-...",  # key = display name used in pipeline referenceName
#   "AzureSqlDB_Sales": "bbbb-..."        # value = GUID used in API calls only
# }
```

Save this output as `connection_map.json` for use in Phase 3 (dataset inlining) and Phase 4 (activity transformation).

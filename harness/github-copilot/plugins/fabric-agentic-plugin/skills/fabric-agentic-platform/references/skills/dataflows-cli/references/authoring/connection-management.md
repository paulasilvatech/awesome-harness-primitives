# Connection Management via CLI

Operational guide for the **full Fabric data source connection lifecycle** — discover, create, list, find, inspect, test, and bind to dataflows — using `az rest` against the Fabric REST API. Pairs with the existing **bind connection to dataflow** workflows under [authoring-cli-quickref.md § Connection Binding Quick Patterns](authoring-cli-quickref.md#connection-binding-quick-patterns) and connection discovery/validation under [authoring-cli-quickref.md § Connection Discovery and Validation](authoring-cli-quickref.md#connection-discovery-and-validation).

> **Scope.** This reference covers `GET /v1/connections`, `GET /v1/connections/{id}`, `GET /v1/connections/supportedConnectionTypes`, `POST /v1/connections`, `POST /v1/connections/{id}/testConnection`, and the discover → inspect → create → bind → test → refresh flow needed when a Dataflow Gen2 references a connection that does not yet exist. Sharing, role assignments, `PATCH`, and `DELETE` of connections are related lifecycle tasks but are **out of scope** here.
>
> **API-only.** Every step uses `az rest` against the Fabric REST API. Portal/UI-driven connection creation (Fabric portal "New connection" dialog, OAuth2 browser consent flows) is out of scope — this reference targets headless, scriptable, CI-friendly automation.

> **Authoritative API spec.** All schemas, field names, defaults, and credential shapes in this document are taken from Microsoft Learn:
> - [List Connections](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/list-connections)
> - [Get Connection](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/get-connection)
> - [List Supported Connection Types](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/list-supported-connection-types)
> - [Create Connection](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/create-connection)
> - [Test Connection](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/test-connection)

## Table of Contents

| Section | Why |
|---|---|
| [Decision Tree](#decision-tree) | When to call which API in what order |
| [Required Permissions](#required-permissions) | Scopes for read / create / gateway operations |
| [Concept Model](#concept-model) | The type system underlying every connection: `connectivityType`, `credentialType`, encryption, privacy |
| [Step 1 — List Supported Connection Types](#step-1--list-supported-connection-types) | Always call this **before** create, never guess parameters |
| [Step 2 — Create Connection (Cloud)](#step-2--create-connection-cloud) | `POST /v1/connections` for `ShareableCloud` |
| [Credential Type Schemas](#credential-type-schemas) | Schema-accurate body shapes per credential type |
| [Connection Type Examples](#connection-type-examples) | SQL, AzureBlobs, Web, Lakehouse, Warehouse — examples only |
| [Step 3 — Verify and Get the Connection ID](#step-3--verify-and-get-the-connection-id) | `GET /v1/connections/{id}` to inspect; list+filter for discovery |
| [Step 3b — Test the Connection (optional)](#step-3b--test-the-connection-optional) | `POST /v1/connections/{id}/testConnection` LRO pre-bind sanity check |
| [Step 4 — Bind to Dataflow and Refresh](#step-4--bind-to-dataflow-and-refresh) | Hand-off to existing bind workflow + post-save verification |
| [Connection ID Format Cheat Sheet](#connection-id-format-cheat-sheet) | REST `id` vs `queryMetadata` composite vs plain `DatasourceId` |
| [Operational Pitfalls](#operational-pitfalls) | Re-bind-after-save; multi-source; AllowCombine; Lakehouse consolidation |
| [Gateways (Appendix)](#gateways-appendix) | List gateways; VNet create; on-prem caveat |
| [Troubleshooting](#troubleshooting) | DuplicateConnectionName, Invalid*, IncorrectCredentials |
| [Out of Scope](#out-of-scope) | Sharing, PATCH, DELETE, OAuth2 create, on-prem encrypted credentials |

## Decision Tree

```
Need a connection for a dataflow?
│
├─► (1) GET /v1/connections — list and filter by displayName / path / connectionDetails.type
│       │
│       ├─ FOUND → (1a) GET /v1/connections/{id}
│       │           Inspect connectivityType, connectionDetails.type, credentialDetails, gatewayId.
│       │           │
│       │           ├─ Matches required source + network path → reuse. Take `id`, skip to (4).
│       │           └─ Wrong type / wrong network path / wrong credentials → create a new one.
│       │
│       └─ NOT FOUND → continue.
│
├─► (2) GET /v1/connections/supportedConnectionTypes
│       (filter to the type you need; capture parameter names + supported credential types)
│
├─► (3) POST /v1/connections
│       (use a `connectivityType` matching the network path: ShareableCloud / OnPremisesGateway / VirtualNetworkGateway)
│       Capture `id` from the 201 response.
│
├─► (3b) POST /v1/connections/{id}/testConnection   (optional)
│       LRO. Sanity-check credentials/network before binding. Skip for connection types where
│       `skipTestConnection` was used at create time or `supportsSkipTestConnection: false`.
│
├─► (4) Bind it to the dataflow definition (`queryMetadata.json connections[]`) + `updateDefinition`,
│
└─► (5) Verify `connections[]` survived the save and trigger refresh.
```

> **Why list-types-before-create?** Each connection type (`SQL`, `AzureBlobs`, `Lakehouse`, `Warehouse`, `Web`, `Dataverse`, …) has a different set of required parameters and supports a different set of credential types. The same connection type may also expose multiple `creationMethod` variants (e.g., several for `Web`). Step 2 below covers the exact endpoint.

## Required Permissions

Delegated scopes (or service-principal equivalents):

| Scope | Needed for |
|---|---|
| `Connection.Read.All` | `GET /v1/connections`, `GET /v1/connections/supportedConnectionTypes` |
| `Connection.ReadWrite.All` | `POST /v1/connections` (create) |
| `Gateway.Read.All` | `GET /v1/gateways` |
| `Gateway.ReadWrite.All` | `POST /v1/gateways` (VNet gateway only — see [appendix](#gateways-appendix)) |

Additional caller requirements:
- **Service principals creating connections** require Fabric tenant admin enablement: see [*Service principals can create workspaces, connections, and deployment pipelines*](https://learn.microsoft.com/en-us/fabric/admin/service-admin-portal-developer#service-principals-can-create-workspaces-connections-and-deployment-pipelines).
- **Gateway connections** require the caller to have permission on the target gateway.

For `az login` recipes and token audience rules, see [COMMON-CLI.md § Authentication Recipes](../../../../common/COMMON-CLI.md#authentication-recipes) and [COMMON-CORE.md § Authentication & Token Acquisition](../../../../common/COMMON-CORE.md#authentication--token-acquisition).

## Concept Model

A Fabric connection is a credential-bearing object that data sources reference for authenticated access. Every connection is defined along the following dimensions — getting any of them wrong is the most common cause of `InvalidInput` on `POST`:

| Dimension | Values | Notes |
|---|---|---|
| `connectivityType` | `ShareableCloud` · `PersonalCloud` · `OnPremisesGateway` · `OnPremisesGatewayPersonal` · `VirtualNetworkGateway` | Drives routing and which credential-details schema applies. `ShareableCloud` / `PersonalCloud` are cloud-only (no `gatewayId`). The three gateway variants require `gatewayId`. |
| `connectionDetails.type` | `SQL`, `AzureBlobs`, `Lakehouse`, `Web`, `Dataverse`, … | The connector kind. Discover the full set via [Step 1](#step-1--list-supported-connection-types). The M `kind` recorded in `queryMetadata.json` may differ in casing — see [Connection Type Examples](#connection-type-examples). |
| `connectionDetails.creationMethod` | per-type; often equal to `type` | Some types expose multiple creation methods (`Web` has several). Read each method's `parameters[]` from Step 1 — never guess. |
| `credentialType` | `Anonymous`, `Basic`, `Key`, `KeyPair`, `ServicePrincipal`, `SharedAccessSignature`, `WorkspaceIdentity`, `Windows`, `WindowsWithoutImpersonation` | `OAuth2` may appear in a connector's `supportedCredentialTypes` but **cannot be created via this API** — see [Credential Type Schemas](#credential-type-schemas). |
| `privacyLevel` | `None`, `Public`, `Organizational`, `Private` | Default: `Organizational`. Affects multi-source folding (whether queries from different sources can be combined). |
| `connectionEncryption` | `NotEncrypted`, `Encrypted`, `Any` | Per-connector support varies — confirm via Step 1's `supportedConnectionEncryptionTypes`. |
| `skipTestConnection` | `bool` | `false` (default) runs a test at create time; failure surfaces as `IncorrectCredentials`. Set `true` to defer validation to first use (rare). |

A cloud connection identity has **two IDs**: the plain Fabric GUID (`.id` from the POST/GET response) and a Power BI gateway `ClusterId`. They're embedded differently depending on context — see [Connection ID Format Cheat Sheet](#connection-id-format-cheat-sheet).

## Step 1 — List Supported Connection Types

`GET /v1/connections/supportedConnectionTypes` returns, per type:
- `creationMethods[].parameters[]` — the names + dataTypes + `required` flag for `connectionDetails.parameters`
- `supportedCredentialTypes[]` — which `credentialDetails.credentials.credentialType` values are valid
- `supportedConnectionEncryptionTypes[]` — which `connectionEncryption` values are valid
- `supportsSkipTestConnection`
- `supportedCredentialTypesForUsageInUserControlledCode` — subset usable from notebooks (`allowUsageInUserControlledCode`)

**Cloud (no gateway):**

```bash
RESOURCE="https://api.fabric.microsoft.com"
API="https://api.fabric.microsoft.com/v1"

az rest --method get \
  --resource "$RESOURCE" \
  --url "$API/connections/supportedConnectionTypes" \
  --query "value[?type=='SQL']"
```

**For a specific gateway (cloud + on-prem types may differ):**

```bash
GW_ID="<gatewayId>"
az rest --method get \
  --resource "$RESOURCE" \
  --url "$API/connections/supportedConnectionTypes?gatewayId=$GW_ID&showAllCreationMethods=true"
```

Pagination: response includes `continuationToken` + `continuationUri`; reuse the `continuationToken` query parameter to fetch the next page. Page until `continuationToken` is `null` — stopping early hides connector types that may only appear on later pages.

**`showAllCreationMethods=false` (default)** returns only the recommended creation methods for each type. Set to `true` if you need a less-common method.

> **⚠ Send `dataType` correctly per parameter.** Each parameter's `dataType` (`Text`, `Boolean`, `Number`, `Date`, `DateTime`, `DateTimeZone`, `Duration`, …) is part of the connector's contract. The Fabric `POST /v1/connections` endpoint is **lenient** about type coercion at create time — most connectors accept `dataType: "Text"` for a numeric / boolean param and the create returns `201`. **The failures surface later**: at refresh / `executeQuery` time the engine binds parameters by declared type, and a string passed where a Boolean / Number was expected produces silent NULL substitution or `EntityUserFailure`. Read `creationMethods[].parameters[].dataType` from this Step 1 response and pass it back exactly — that is the only forward-compatible behavior.

> **Casing matters.** REST `connectionDetails.type` is `SQL`. The corresponding M connector kind in `queryMetadata.json connections[].kind` is **`Sql`** (camel case). Do not assume 1-to-1 casing between the REST type and the dataflow definition.

## Step 2 — Create Connection (Cloud)

`POST /v1/connections` — body shape depends on the value of `connectivityType`:

| `connectivityType` | Routing | Credential schema |
|---|---|---|
| `ShareableCloud` | Cloud, can be shared | `CreateCredentialDetails` (this section) |
| `VirtualNetworkGateway` | Cloud via VNet data gateway | `CreateCredentialDetails` (same shape; requires `gatewayId`) |
| `OnPremisesGateway` | On-prem data gateway | **Different schema** — see [Gateways (Appendix)](#gateways-appendix); requires RSA-encrypted credentials |

### Cloud body — minimum fields

```jsonc
{
  "connectivityType": "ShareableCloud",
  "displayName": "ContosoSqlConnection",
  "connectionDetails": {
    "type": "SQL",
    "creationMethod": "SQL",
    "parameters": [
      { "dataType": "Text", "name": "server",   "value": "contoso.database.windows.net" },
      { "dataType": "Text", "name": "database", "value": "sales" }
    ]
  },
  "privacyLevel": "Organizational",
  "credentialDetails": {
    "singleSignOnType": "None",
    "connectionEncryption": "Encrypted",
    "skipTestConnection": false,
    "credentials": {
      "credentialType": "Basic",
      "username": "admin",
      "passwordReference": {
        "connectionId": "<keyVaultConnectionId>",
        "secretName": "sql-admin-password"
      }
    }
  }
}
```

Important defaults and optional fields:

| Field | Default | Notes |
|---|---|---|
| `privacyLevel` | `Organizational` | Other values: `None`, `Public`, `Organizational`, `Private`. **Set explicitly** to make intent obvious. |
| `connectionEncryption` | not encrypted | Allowed: `NotEncrypted`, `Encrypted`, `Any`. |
| `skipTestConnection` | `false` | Test runs at create time; failure → `IncorrectCredentials`. |
| `singleSignOnType` | `None` | `Kerberos`, `MicrosoftEntraID`, `SecurityAssertionMarkupLanguage`, `KerberosDirectQueryAndRefresh`. |
| `allowUsageInUserControlledCode` | `false` | Set `true` only if the connection should be usable from Notebooks (and only when the credential type is in the supported subset for that). |
| `allowConnectionUsageInGateway` | unset | Allow this cloud connection to also be used through a gateway. |

### Bash — create cloud SQL connection (Basic auth via Key Vault reference)

```bash
#!/usr/bin/env bash
set -euo pipefail

RESOURCE="https://api.fabric.microsoft.com"
API="https://api.fabric.microsoft.com/v1"

DISPLAY_NAME="${DISPLAY_NAME:?Set DISPLAY_NAME}"
SQL_SERVER="${SQL_SERVER:?Set SQL_SERVER}"
SQL_DATABASE="${SQL_DATABASE:?Set SQL_DATABASE}"
SQL_USER="${SQL_USER:?Set SQL_USER}"
KV_CONN_ID="${KV_CONN_ID:?Set KV_CONN_ID — Fabric Key Vault connection ID}"
KV_SECRET_NAME="${KV_SECRET_NAME:?Set KV_SECRET_NAME}"

BODY=$(jq -n \
  --arg name "$DISPLAY_NAME" \
  --arg server "$SQL_SERVER" --arg db "$SQL_DATABASE" \
  --arg user "$SQL_USER" \
  --arg kvConn "$KV_CONN_ID" --arg secret "$KV_SECRET_NAME" \
  '{
    connectivityType: "ShareableCloud",
    displayName: $name,
    connectionDetails: {
      type: "SQL",
      creationMethod: "SQL",
      parameters: [
        { dataType: "Text", name: "server",   value: $server },
        { dataType: "Text", name: "database", value: $db }
      ]
    },
    privacyLevel: "Organizational",
    credentialDetails: {
      singleSignOnType: "None",
      connectionEncryption: "Encrypted",
      skipTestConnection: false,
      credentials: {
        credentialType: "Basic",
        username: $user,
        passwordReference: { connectionId: $kvConn, secretName: $secret }
      }
    }
  }')

az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/connections" \
  --body "$BODY" \
  --query "{id:id, name:displayName, type:connectionDetails.type, path:connectionDetails.path}"
```

> **Secret-safe generation.** Use `passwordReference` in generated examples; do not render a plaintext credential field even as an unsafe or local-testing example. Never commit plaintext credentials, and never echo or log runtime secret values.

> **⚠ Unknown credential keys are silently dropped.** Fabric does **not** return `400` for unknown keys inside `credentialDetails.credentials` — it discards them and proceeds with the recognized fields that remain. A typo like `passWord` instead of `password` produces a `201 Created` with no usable credential, and the first refresh then fails with a generic `IncorrectCredentials`. **Validate your request body's credential keys against the discovered schema from Step 1 before POSTing.**

> **Caching guidance.** `supportedConnectionTypes` is stable per tenant — cache aggressively (24h+). `gatewayClusterDatasources` updates whenever a connection is created — cache ~5 min per process. The `/v1/connections` list changes whenever anyone with overlapping visibility creates a connection — cache short (<1m) or not at all if precision matters.

## Credential Type Schemas

The full union accepted by **`CreateCredentialDetails.credentials`** for `ShareableCloud` and `VirtualNetworkGateway` connections. Always check the type's `supportedCredentialTypes` from Step 1 first — not every type accepts every credential.

| Credential type | Required fields | KV reference variant |
|---|---|---|
| `Anonymous` | `credentialType` | — |
| `Basic` | `username`, `password` **OR** `passwordReference` | `passwordReference` |
| `Key` | `key` **OR** `keyReference` | `keyReference` |
| `KeyPair` | `identifier`, `privateKey` (PKCS #8), `passphrase` | — |
| `ServicePrincipal` | `tenantId`, `servicePrincipalClientId`, `servicePrincipalSecret` **OR** `servicePrincipalSecretReference` | `servicePrincipalSecretReference` |
| `SharedAccessSignature` | `token` **OR** `tokenReference` | `tokenReference` |
| `WorkspaceIdentity` | `credentialType` only (no other fields) | — |
| `Windows` / `WindowsWithoutImpersonation` | On-prem gateway only | — |

> **OAuth2 is not creatable via `POST /v1/connections`.** It can appear in `supportedCredentialTypes` for some connector types, but the Create Connection schema does not define an OAuth2 credentials body. Live-verified — the API rejects any `OAuth2` payload with:
>
> ```jsonc
> 400 InvalidInput
> {
>   "errorCode": "InvalidInput",
>   "message": "The request has an invalid input",
>   "moreDetails": [{
>     "errorCode": "InvalidParameter",
>     "message": "The CredentialType input is not supported for this API"
>   }],
>   "isRetriable": false
> }
> ```
>
> Use an existing OAuth2-backed connection that was authored interactively in the portal/UI, or pick a different credential type from the connector's `supportedCredentialTypes`.

### Key Vault reference shape (`KeyVaultSecretReference`)

```jsonc
{
  "connectionId": "<keyVaultConnectionIdAsUuid>",  // not a Key Vault URL — a Fabric KV connection ID
  "secretName": "<secret-name-in-vault>",
  "version": "<optional secret version>"
}
```

> **Chicken-and-egg.** A Key Vault reference points at *another Fabric connection* (a Key Vault connection) that already exists. If you do not have one, create the Key Vault connection first via this same API or pause and request that prerequisite; generated templates should not silently downgrade to plaintext credentials.

### Service principal example

```jsonc
"credentials": {
  "credentialType": "ServicePrincipal",
  "tenantId": "<tenantId>",
  "servicePrincipalClientId": "<appId>",
  "servicePrincipalSecretReference": {
    "connectionId": "<kvConnectionId>",
    "secretName": "sp-client-secret"
  }
}
```

### Workspace identity example (Lakehouse / Warehouse / Eventhouse common case)

```jsonc
"credentials": { "credentialType": "WorkspaceIdentity" }
```

### KeyPair example (Snowflake-style)

```jsonc
"credentials": {
  "credentialType": "KeyPair",
  "identifier": "admin",
  "privateKey": "-----BEGIN ENCRYPTED PRIVATE KEY-----\n...\n-----END ENCRYPTED PRIVATE KEY-----",
  "passphrase": "<passphrase>"
}
```

## Connection Type Examples

> **Examples only — always confirm via `supportedConnectionTypes`.** Connector parameters and supported credential types vary by tenant, gateway, and over time. Casing of `connectionDetails.type` may also differ from the M `kind` recorded in `queryMetadata.json`.

| `connectionDetails.type` | Common required parameters | Typical credentials | M `kind` (in queryMetadata) |
|---|---|---|---|
| `SQL` | `server`, `database` (optional) | `Basic`, `ServicePrincipal`, `WorkspaceIdentity` | `Sql` |
| `AzureBlobs` | `account`, `domain` | `Key`, `SharedAccessSignature`, `WorkspaceIdentity` | `AzureStorage` |
| `Web` | `url` | `Anonymous`, `Basic`, `Key` | `Web` |
| `Lakehouse` | `workspaceId`, `lakehouseId` | `WorkspaceIdentity`, `OAuth2` (not creatable here) | `Lakehouse` |
| `Warehouse` | `workspaceId`, `warehouseId` | `WorkspaceIdentity`, `ServicePrincipal` | `Sql` (DW SQL endpoint) |

For Fabric-source connections (`Lakehouse`, `Warehouse`, `Eventhouse`) the workspace ID is **mandatory** because artifact names are scoped to the parent workspace and would otherwise be ambiguous.

## Step 3 — Verify and Get the Connection ID

The `POST /v1/connections` `201 Created` response includes the new connection's `id`. Capture it directly:

```bash
NEW_CONN_ID=$(az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/connections" \
  --body @body.json \
  --query "id" --output tsv)

echo "Created connection: $NEW_CONN_ID"
```

### Inspect an existing connection — `GET /v1/connections/{id}`

When the caller already knows the connection's GUID (e.g., captured at create time, copied from another script, or extracted from `queryMetadata.json connections[].connectionId`'s `DatasourceId`), prefer `GET /v1/connections/{id}` over `GET /v1/connections` + filter. It is a direct lookup, returns the full `connectivityType` / `connectionDetails` / `credentialDetails` shape, and surfaces `EntityNotFound` clearly:

```bash
az rest --method get \
  --resource "$RESOURCE" \
  --url "$API/connections/$NEW_CONN_ID" \
  --query "{id:id, name:displayName, connectivity:connectivityType, type:connectionDetails.type, path:connectionDetails.path, credType:credentialDetails.credentialType, gw:gatewayId}"
```

Use this to:
- Confirm the connection still exists and is reachable for this caller (`403`/`404` ⇒ no access or deleted).
- Check `connectivityType` before binding — prefer `ShareableCloud` / `PersonalCloud` for cloud-reachable sources over `OnPremisesGateway` / `VirtualNetworkGateway` to avoid an unnecessary gateway-online failure surface (see [Picking between PersonalCloud and OnPremisesGateway when both exist](#picking-between-personalcloud-and-onpremisesgateway-when-both-exist)).
- Verify `credentialDetails.credentialType` matches the M `kind` recorded in `queryMetadata.json`.

### Discover by name — `GET /v1/connections` + filter

When the GUID is unknown (e.g., from another shell, or after `POST` without capturing the response), list-and-filter via the standard recipe in [authoring-cli-quickref.md § Connection Discovery and Validation](authoring-cli-quickref.md#connection-discovery-and-validation):

```bash
az rest --method get \
  --resource "$RESOURCE" \
  --url "$API/connections" \
  --query "value[?displayName=='ContosoSqlConnection'].id" --output tsv
```

> **Per-caller visibility.** `GET /v1/connections` only returns connections the caller has at least read permission on; an empty result is **not** proof the connection is absent from the tenant. Request access from the connection owner if expected results are missing.

## Step 3b — Test the Connection (optional)

After create (or before binding a connection whose credentials may have rotated), call `POST /v1/connections/{id}/testConnection` as a pre-bind sanity check. This catches `IncorrectCredentials`, offline gateways, and network-path issues *before* they surface as a generic `EntityUserFailure` on the next refresh.

This endpoint is **LRO** — a successful test may return either `200 OK` (synchronous, with `ConnectionStatusResponse`) or `202 Accepted` with the following headers (live-verified):

| Header | Purpose |
|---|---|
| `Location` | Absolute URL of the LRO operation resource; `GET` it to poll `status`. |
| `Retry-After` | Server-recommended polling interval (seconds; typically `5`). |
| `x-ms-operation-id` | Operation GUID — also the suffix of the `Location` URL. Use this to correlate logs across the request and any retries. |

Body of the `202` is `null`; all state lives on the LRO resource at `Location`. Final `ConnectionStatusResponse` payload is at `${Location}/result` once `status` is terminal.

```bash
# az rest cannot capture response headers — use curl for the initial call so we can read Location.
TOKEN=$(az account get-access-token --resource "$RESOURCE" --query accessToken -o tsv)
HDR=$(mktemp); BODY=$(mktemp)
CODE=$(curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/connections/$NEW_CONN_ID/testConnection" \
  -D "$HDR" -o "$BODY" -w "%{http_code}")

if [ "$CODE" = "200" ]; then
  jq '.' "$BODY"
elif [ "$CODE" = "202" ]; then
  LOC=$(tr -d '\r' < "$HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  # Poll the LRO until terminal status, then GET /result for the ConnectionStatusResponse payload.
  # Full polling helper: authoring-cli-quickref.md § LRO Polling Helper.
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOC")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) az rest --method get --resource "$RESOURCE" --url "${LOC%/}/result"; break ;;
      Failed|Cancelled) echo "ERROR: testConnection $(echo "$OP" | jq -r '.status')" >&2; exit 1 ;;
    esac
  done
else
  echo "ERROR: testConnection HTTP $CODE" >&2; cat "$BODY" >&2; exit 1
fi
rm -f "$HDR" "$BODY"
```

**Skip Step 3b when:**
- The connection was created with `skipTestConnection: true` and the connector advertises `supportsSkipTestConnection: false` for the chosen credential type (call will return `400`).
- The source is rate-limited and a probe call is unsafe.
- The agent records an explicit skip reason (e.g., test traffic billed per call).

**Common failures:** `IncorrectCredentials` (rotate or re-create), `EntityNotFound` (connection deleted or no access), gateway-offline (the response will surface the gateway error).

## Step 4 — Bind to Dataflow and Refresh

Once you have the connection's `id` GUID, bind it into `queryMetadata.json` and update the dataflow definition. The bind mechanics already live in this skill — do not reinvent:

- [authoring-cli-quickref.md § Connection Binding Quick Patterns](authoring-cli-quickref.md#connection-binding-quick-patterns) — `az rest` snippets to fetch ClusterId, edit `queryMetadata.json`, and `updateDefinition`.
- [authoring-script-templates.md § Connection Binding Templates](authoring-script-templates.md#connection-binding-templates) — full end-to-end Bash/PowerShell flow.

After `updateDefinition`, **always verify** that `queryMetadata.json connections[]` still contains your binding (see [Operational Pitfalls](#operational-pitfalls) below). Then trigger refresh and poll using the existing helpers.

## Connection ID Format Cheat Sheet

Three different ID forms appear in this flow. Confusing them is the most common cause of "connection not found" at refresh.

| Where | Field | Format |
|---|---|---|
| `POST /v1/connections` response | `id` | Plain GUID, e.g. `eeec9a3a-6ef5-4e2b-bb6a-0060bd2f0172` |
| `GET /v1/connections` response | `value[].id` | Plain GUID |
| `GET /v1/connections/{id}` response | `id` | Plain GUID |
| `queryMetadata.json connections[].connectionId` (dataflow definition) | `connectionId` | **Stringified composite JSON**, e.g. `"{\"ClusterId\":\"<guid>\",\"DatasourceId\":\"<guid>\"}"` |
| Power BI v2 `gatewayClusterDatasources` response | `clusterId` (camelCase) | Plain GUID — the **ClusterId** to embed in the composite above. See [Resolving ClusterId](#resolving-clusterid-power-bi-v2) below. |

Rule of thumb:
- **REST `POST` / `GET` / `PATCH` / `DELETE` operations on `/v1/connections/...`** want the **plain GUID** (the `.id` from any of the above responses).
- **Dataflow definition `queryMetadata.json connections[].connectionId`** wants the **stringified composite** `{"ClusterId":"…","DatasourceId":"…"}`.

### Resolving ClusterId (Power BI v2)

The `ClusterId` value embedded in the composite comes from the **Power BI v2 control-plane endpoint** `myorg/me/gatewayClusterDatasources`. Use the **list-and-filter** pattern — list the user's gateway-cluster datasources, then filter the response by the connection's plain GUID (`value[?id=='{connId}'].clusterId`):

| URL | Returns | Notes |
|---|---|---|
| `GET https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources` | `{ value: [...] }` — flat, paginated array of cluster + datasource records, each with `clusterId`, `id`, `datasourceReference`, … | Canonical pattern. Filter by `id == <connectionId>` to obtain `clusterId`. Newly-created connections may take a few seconds to surface here — retry the list call if the filter returns empty. |

> **Don't use the per-id route.** `GET .../gatewayClusterDatasources/{datasourceId}` returns `PowerBIEntityNotFound` for cloud connections (verified live against `connectivityType: ShareableCloud` + Web). Use list+filter only.

> **Token audience.** The list endpoint accepts the Power BI audience (`https://analysis.windows.net/powerbi/api` — **no** trailing slash; the slashed form fails AADSTS500011). The Fabric token (`https://api.fabric.microsoft.com/`) is also accepted in current tenants — for scripts that already hold a Fabric token, no separate token acquisition is needed.

```bash
PBI_RESOURCE="https://analysis.windows.net/powerbi/api"
CONN_ID="<datasourceId>"

CLUSTER_ID=$(az rest --method get \
  --resource "$PBI_RESOURCE" \
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" \
  --query "value[?id=='$CONN_ID'] | [0].clusterId" --output tsv)
```

> **Empty result after retries.** If the filter still returns empty after ~30s of retries, the connection is not visible to PBI v2 — that's a connection-lifecycle problem (e.g., orphaned record after a failed create), not a ClusterId-lookup problem. Verify the connection exists via `GET /v1/connections/{id}`; if Fabric shows it but PBI v2 doesn't, recreate the connection.

### Picking between PersonalCloud and OnPremisesGateway when both exist

When multiple connections target the same source (e.g., a public OData feed registered both as `connectivityType: PersonalCloud` and `connectivityType: OnPremisesGateway`), prefer the **PersonalCloud** connection for cloud-only / publicly reachable sources:

| `connectivityType` | When to use | Failure surface |
|---|---|---|
| `PersonalCloud` | Source is reachable from the Fabric cloud (public REST/OData/Web endpoints, Azure-hosted sources) | None beyond the cloud → source path. |
| `OnPremisesGateway` (or `VirtualNetwork`) | Source sits behind a firewall / on-prem network and a gateway hop is mandatory | Adds gateway-online and gateway-permission as additional failure modes. `executeQuery` and refresh both fail (often with the same generic "Credentials required" / `EntityUserFailure` error) when the gateway is offline or misconfigured. |

If a cloud-reachable source happens to be registered against a gateway connection, picking that connection forces an unnecessary gateway hop and an unnecessary failure surface — the preview and refresh will fail in non-obvious ways if the gateway is cold or the cluster is unhealthy. Inspect each candidate connection with `GET /v1/connections/{id}` (see [Step 3 — Inspect an existing connection](#inspect-an-existing-connection--get-v1connectionsid)) and check `connectivityType` before binding.

## Operational Pitfalls

These are observed pitfalls, not formal API guarantees — verify each one in your environment before treating it as load-bearing.

### Verify connections survived `updateDefinition`

`updateDefinition` is a full replacement: any 3-part payload that omits or scrubs `queryMetadata.json connections[]` will leave the dataflow with no bindings. If a workflow modifies `mashup.pq` and re-builds `queryMetadata.json` from a stale snapshot, bindings get silently dropped.

**Mandatory step after every `updateDefinition`:**

> **⚠ LRO caveat:** the `getDefinition` call below assumes a synchronous 200 response. For production code, handle **202 + Location** with the LRO-aware curl pattern (see [authoring-cli-quickref.md § Validate All Connections in a Dataflow](authoring-cli-quickref.md#validate-all-connections-in-a-dataflow-pre-refresh-check) or [authoring-script-templates.md § Bash — Read-Modify-Write Dataflow Definition](authoring-script-templates.md#bash--read-modify-write-dataflow-definition)).

```bash
# Re-fetch and confirm bindings survived (happy-path 200 only — see caveat)
RESULT=$(az rest --method post \
  --resource "$RESOURCE" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  --headers "Content-Length=0")

echo "$RESULT" \
  | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' \
  | base64 -d \
  | jq '.connections // []'
```

If `connections[]` is empty or missing the entry you expected, **re-bind and updateDefinition again** before triggering refresh.

### Multi-source dataflows

If a dataflow reads from multiple distinct sources, each source needs its own connection bound. The M section also needs to opt in to combining queries:

```m
[AllowCombine = true]
section Section1;
```

Without `[AllowCombine = true]`, the engine refuses to fold queries that touch multiple sources and refresh fails with privacy-level errors.

For multiple Lakehouse reads in the same workspace, **consolidate into one `Lakehouse.Contents([...])` call** rather than calling it once per table — the engine treats each call as a separate source for combine-rule purposes.

### Don't convert published single-source dataflows to multi-source in place

Editing a published single-source dataflow to add a second source frequently leaves the dataflow in an inconsistent binding state. **Create a fresh dataflow** that is multi-source from the start, then retire the old one.

### Duplicate connection names

`POST /v1/connections` with a `displayName` that already exists returns `409 DuplicateConnectionName`. Recovery:

```bash
# 1. List existing connections with the same name
az rest --method get --resource "$RESOURCE" --url "$API/connections" \
  --query "value[?displayName=='ContosoSqlConnection']"

# 2. Either reuse the existing id, or pick a unique name (e.g. add an environment suffix)
DISPLAY_NAME="ContosoSqlConnection-$(date +%Y%m%d-%H%M)"
```

## Gateways (Appendix)

### List gateways

```bash
az rest --method get \
  --resource "$RESOURCE" \
  --url "$API/gateways" \
  --query "value[].{id:id, name:displayName, type:type}"
```

### VNet gateway connection

VNet gateway connections use the same `CreateCredentialDetails` schema as `ShareableCloud`, plus a top-level `gatewayId`:

```jsonc
{
  "connectivityType": "VirtualNetworkGateway",
  "gatewayId": "<vnetGatewayId>",
  "displayName": "ContosoVnetSqlConnection",
  "connectionDetails": { /* same as cloud */ },
  "privacyLevel": "Organizational",
  "credentialDetails": {
    "singleSignOnType": "None",
    "connectionEncryption": "Encrypted",
    "skipTestConnection": false,
    "credentials": { /* Basic / ServicePrincipal / WorkspaceIdentity / etc. */ }
  }
}
```

> Creating the **VNet gateway itself** (`POST /v1/gateways`) requires a Fabric capacity, an Azure subscription, resource group, VNet, subnet, and subnet delegation — that's gateway provisioning, outside the dataflows authoring scope. Treat the VNet gateway as a prerequisite that exists before you author the connection.

### On-premises gateway connection — different credential flow

`OnPremisesGateway` connections use `CreateOnPremisesCredentialDetails`, where credentials are not plaintext but **RSA-encrypted with each gateway member's public key**:

```jsonc
"credentialDetails": {
  "singleSignOnType": "None",
  "connectionEncryption": "NotEncrypted",
  "skipTestConnection": false,
  "credentials": {
    "credentialType": "Windows",
    "values": [
      { "gatewayId": "<gatewayMember1>", "encryptedCredentials": "<RSA-encrypted-blob>" },
      { "gatewayId": "<gatewayMember2>", "encryptedCredentials": "<RSA-encrypted-blob>" }
    ]
  }
}
```

> **Out of scope for ready-to-run templates.** Generating `encryptedCredentials` requires fetching the gateway member's RSA public key and serializing the credential payload according to Microsoft's encryption format. See [*Configure credentials programmatically*](https://learn.microsoft.com/en-us/power-bi/developer/embedded/configure-credentials) for the algorithm. **Plaintext templates do not work for on-prem.**

For Dataflow Gen2 use, prefer either `ShareableCloud` (when the source is reachable from the cloud) or `VirtualNetworkGateway` over on-prem when feasible.

## Troubleshooting

| Error / Symptom | Root cause | Fix |
|---|---|---|
| `409 DuplicateConnectionName` | A connection with that `displayName` already exists in the tenant. | List existing → reuse `id` **or** rename. |
| `400 InvalidConnectionDetails` | Wrong `type`, missing/extra `parameters`, or wrong `creationMethod`. | Re-run `GET /v1/connections/supportedConnectionTypes`; copy parameter names exactly. |
| `400 InvalidCredentialDetails` | `credentialType` not in `supportedCredentialTypes` for that connection type, or required fields missing (e.g., SP without `tenantId`). | Verify schema in [Credential Type Schemas](#credential-type-schemas); re-check `supportedConnectionTypes`. |
| `400 InvalidInput` — *"The CredentialType input is not supported for this API"* | Tried to create with `credentialType: OAuth2` (or another non-API-creatable type) via `POST /v1/connections`. | OAuth2 connections must be authored interactively in the portal — see [Out of Scope](#out-of-scope). Pick a different credential type from the source's `supportedCredentialTypes`. |
| `400 IncorrectCredentials` | Test connection failed at create time. | Verify credentials by hand against the source; **or** set `skipTestConnection: true` if the type supports it. |
| `400 CreateGatewayConnectionFailed` | `connectivityType` is gateway-bound but `gatewayId` is wrong, the caller lacks gateway permission, or (on-prem) `encryptedCredentials` is malformed. | Confirm `gatewayId` exists; check caller's gateway role; for on-prem, regenerate RSA-encrypted credentials. |
| `403 Forbidden` on `POST` | Caller lacks `Connection.ReadWrite.All`, or service principal not enabled by tenant admin. | Check delegated scope or grant admin enablement. |
| `429 Too Many Requests` | Tenant connection-create rate limit. | Honor `Retry-After`; back off. |
| Refresh after create reports "connection not found" | The dataflow was bound using the wrong ID format (e.g., plain GUID where composite is required, or vice versa). | See [Connection ID Format Cheat Sheet](#connection-id-format-cheat-sheet). |
| `connections[]` missing after `updateDefinition` | Read-modify-write rebuilt `queryMetadata.json` from a snapshot that did not include bindings. | Re-bind, `updateDefinition` again, **verify** before refresh. |

## Out of Scope

The following endpoints and flows are **live-confirmed to exist** at the API level, but their lifecycle, governance, and integration surfaces differ from the discover → create → bind path covered here:

- **Update a connection** (`PATCH /v1/connections/{id}`) — rotate credentials, change `displayName`, adjust `privacyLevel`. Endpoint exists (returns typed `InvalidInput` on bad payload, not `405`).
- **Delete a connection** (`DELETE /v1/connections/{id}`) — destructive; not idempotent across active bindings. Endpoint exists (returns `EntityNotFound` on missing id, not `405`).
- **Connection sharing / role assignments** — granting other principals access to use the connection.
- **OAuth2 connection authoring** — interactive only (portal / UI); the API rejects `OAuth2` in `POST /v1/connections` with `InvalidInput` (see [Troubleshooting](#troubleshooting)).
- **On-premises gateway credential encryption** — see Microsoft's [*Configure credentials programmatically*](https://learn.microsoft.com/en-us/power-bi/developer/embedded/configure-credentials) for the RSA encryption format.
- **Creating gateways** — VNet/on-prem gateway provisioning is an admin/network task, not a dataflows authoring task.

For dataflow → connection **binding** (where you already have a connection ID), see:
- [authoring-cli-quickref.md § Connection Binding Quick Patterns](authoring-cli-quickref.md#connection-binding-quick-patterns)
- [authoring-script-templates.md § Connection Binding Templates](authoring-script-templates.md#connection-binding-templates)

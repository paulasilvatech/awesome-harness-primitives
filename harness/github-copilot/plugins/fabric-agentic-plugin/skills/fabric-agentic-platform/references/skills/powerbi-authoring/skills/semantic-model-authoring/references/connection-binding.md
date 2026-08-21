# Semantic Model Connection Binding Reference

Programmatically bind (or unbind) a semantic model's data source references to a Fabric data connection using the **Bind Semantic Model Connection** Fabric REST API. Use this when promoting a model across environments (dev -> prod), switching gateways, repointing to a new server, or wiring up a freshly deployed model.

This API supersedes the legacy Power BI [Bind to Gateway in Group](https://learn.microsoft.com/rest/api/power-bi/datasets/bind-to-gateway-in-group). It supports gateway, cloud, virtual network, automatic, and unbind (`None`) connectivity types.

> **Reference docs**
> - [Bind Semantic Model Connection](https://learn.microsoft.com/rest/api/fabric/semanticmodel/items/bind-semantic-model-connection)
> - [List Item Connections](https://learn.microsoft.com/rest/api/fabric/core/items/list-item-connections)
> - [List Connections](https://learn.microsoft.com/rest/api/fabric/core/connections/list-connections)
> - [Create Connection](https://learn.microsoft.com/rest/api/fabric/core/connections/create-connection)

---

## Prerequisites

- Caller is the **owner** of the semantic model.
- Delegated scope: `SemanticModel.ReadWrite.All` or `Item.ReadWrite.All`.
- Identities: User, Service Principal, Managed Identity.
- Fabric audience for `az rest`: `https://api.fabric.microsoft.com`.

## Limitations

- **No bulk operations.** Submit one `bindConnection` request per data source reference. A model with N data sources requires N requests.

---

## Endpoint

```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/semanticModels/{semanticModelId}/bindConnection
```

### Request body

```jsonc
{
  "connectionBinding": {
    "id": "<connectionId-uuid>",                // Required for gateway/cloud bindings; OMIT for Automatic and None
    "connectivityType": "OnPremisesGateway",    // See ConnectivityType table below
    "connectionDetails": {
      "type": "SQL",                            // Data source type from List Item Connections
      "path": "contoso.database.windows.net;sales"  // Data source path from List Item Connections
    }
  }
}
```

`connectionDetails` identifies **which data source reference** of the semantic model is being bound. It must match the `connectionDetails` returned by `List Item Connections` for that model.

### `connectivityType` values

| Value                       | Use                                                                                       |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| `ShareableCloud`            | Cloud connection that can be shared with others.                                          |
| `PersonalCloud`             | Cloud connection scoped to a single user.                                                 |
| `OnPremisesGateway`         | Standard on-premises data gateway.                                                        |
| `OnPremisesGatewayPersonal` | Personal on-premises data gateway.                                                        |
| `VirtualNetworkGateway`     | Virtual network data gateway.                                                             |
| `Automatic`                 | Implicit cloud connection (e.g. SSO scenarios). Do **not** include `id`.                  |
| `None`                      | Unbind the data source reference, leaving it disconnected. Do **not** include `id`.       |

### Responses

| Status                  | Meaning                                                                       |
| ----------------------- | ----------------------------------------------------------------------------- |
| `200 OK`                | Binding applied.                                                              |
| `429 Too Many Requests` | Rate limited. Honor `Retry-After`.                                            |
| `400 InvalidRequest`    | Payload invalid (mismatched `connectionDetails`, wrong `connectivityType`).   |
| `404 ItemNotFound`      | Workspace or semantic model not found.                                        |
| `403 Forbidden`         | Caller is not the model owner or lacks the required scope.                    |

---

## End-to-end Workflow

Follow these steps in order. Steps 1-3 discover what to bind to what; step 4 performs the bind.

### Step 1 - List the semantic model's data source references

Discover which data sources the model needs and the exact `connectionDetails` to echo back in the bind payload.

```bash
WS_ID="<workspaceId>"
MODEL_ID="<semanticModelId>"

az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/items/$MODEL_ID/connections"
```

Each entry in the response contains the `connectionDetails` (`type` + `path`) for one data source reference, plus the currently bound connection (if any).

### Step 2 - List connections you can access

```bash
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/connections"
```

### Step 3 - Match (or create) a connection

For each data source reference from step 1, find a connection in step 2 whose `connectionDetails.type` and `connectionDetails.path` match. Capture its `id`.

If no matching connection exists, create one with [Create Connection](https://learn.microsoft.com/rest/api/fabric/core/connections/create-connection) before continuing.

> **Match rule:** `connectionDetails.type` and `connectionDetails.path` must match **exactly** (case- and format-sensitive) between the model's data source reference and the target connection.

### Step 4 - Submit one bind request per data source reference

#### Bind to a gateway or cloud connection

```bash
CONNECTION_ID="<connectionId>"

cat > /tmp/bind.json << EOF
{
  "connectionBinding": {
    "id": "$CONNECTION_ID",
    "connectivityType": "OnPremisesGateway",
    "connectionDetails": {
      "type": "SQL",
      "path": "contoso.database.windows.net;sales"
    }
  }
}
EOF

az rest --method post \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/semanticModels/$MODEL_ID/bindConnection" \
  --headers "Content-Type=application/json" \
  --body @/tmp/bind.json
```

#### Bind using default / automatic settings (SSO)

Omit `id`.

```jsonc
{
  "connectionBinding": {
    "connectivityType": "Automatic",
    "connectionDetails": { "type": "SQL", "path": "contoso.database.windows.net;sales" }
  }
}
```

#### Unbind a data source reference

Omit `id` and use `None`.

```jsonc
{
  "connectionBinding": {
    "connectivityType": "None",
    "connectionDetails": { "type": "SQL", "path": "contoso.database.windows.net;sales" }
  }
}
```

### Step 5 - Validate

Re-run **Step 1** (`List Item Connections`) and confirm each data source reference now reports the expected connection `id` (or is unbound when `None` was sent). Then trigger a refresh to confirm credentials resolve end-to-end.

---

## Common scenarios

| Scenario                                         | Approach                                                                                                                                                       |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Promote model dev -> prod                        | After deploy via `updateDefinition`, list its data source refs, find prod connections in step 2, send one bind request per ref.                                 |
| Move from cloud connection to gateway            | Send a single bind request with `connectivityType: OnPremisesGateway` and the gateway connection's `id`.                                                       |
| Disconnect a data source temporarily             | Send `connectivityType: None` (no `id`).                                                                                                                       |
| Model has multiple data sources                  | Loop over the data source refs from Step 1; submit **one** bind request per ref. Bulk binding is **not** supported.                                            |
| New deployment with no connections yet           | Create connections first via Create Connection, then bind.                                                                                                     |

---

## Must / Avoid

### MUST

- Submit **one request per data source reference**. The API rejects bulk payloads.
- Use the **exact** `connectionDetails.type` and `connectionDetails.path` from `List Item Connections` - do not reformat, lowercase, or otherwise normalize them.
- Authenticate against the Fabric audience (`https://api.fabric.microsoft.com`), not the Power BI audience.
- Validate by re-listing item connections after each bind.

### AVOID

- Using the legacy `Default.BindToGateway` Power BI endpoint - this API supersedes it.
- Sending `id` together with `connectivityType: Automatic` or `None` - omit `id` for those.
- Hardcoding connection IDs - resolve them dynamically by matching `connectionDetails` from step 1 against step 2.
- Assuming a successful bind means credentials are valid - always trigger a refresh to confirm.

---

## Troubleshooting

| Symptom                                | Likely cause / fix                                                                                                          |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `400 InvalidRequest`                   | `connectionDetails` does not match any data source reference of the model. Re-fetch via `List Item Connections` and copy verbatim. |
| `403 Forbidden`                        | Caller is not the owner of the semantic model, or missing `SemanticModel.ReadWrite.All` / `Item.ReadWrite.All` scope.       |
| `404 ItemNotFound`                     | Wrong `workspaceId` or `semanticModelId`. Re-resolve via the Finding Workspaces and Items pattern.                          |
| Bind succeeds but refresh fails        | Connection credentials are missing or invalid. Configure credentials on the connection itself; bind only links the IDs.     |
| Only some data sources updated         | You sent one request but the model has multiple data sources. Submit one bind request per data source reference.            |
| `id` rejected for `Automatic` / `None` | Remove `id` from the payload - it is only valid for explicit cloud / gateway / VNet bindings.                               |

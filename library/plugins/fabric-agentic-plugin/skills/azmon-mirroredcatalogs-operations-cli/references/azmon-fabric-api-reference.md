# Azure Monitor → Fabric API reference

Guidance on which flows are **documented/supported** versus **UI-only** or
**internal/unsupported**, and the rules for the two connector modes. This file is
agent guidance — do not paste it verbatim to users.

## Supported vs UI-only vs internal — at a glance

| Capability | Status | Notes |
|-----------|--------|-------|
| Mirrored Catalog item CRUD | Documented REST API | See mirrored-catalog-reference.md. Create **supports service principals / managed identities** per docs; some SP runs have **observed** app-only create rejected (falls back to user/UI) — **prefer reuse**, attempt create under the SP, fall back to user/UI create only if denied. |
| Mirrored Catalog item definition | Documented REST API | Item definition format |
| Mirrored Catalog discovery | Documented REST API | Browse scopes/tables |
| Mirrored Catalog monitoring | Documented REST API | Item/table mirroring status |
| Mirrored Catalog refresh / sync | Documented REST API | Trigger metadata sync |
| Operations Agent item CRUD + definition | Documented Fabric item APIs | `type: "OperationsAgent"` |
| **OAuth** Azure Monitor connector creation | **UI-only** | Created once in Fabric → Manage Connections. **No public API.** Detect + reuse only. |
| **Service Principal** connector create-or-reuse | Automated | Idempotent create-or-reuse; secrets from env/Key Vault only |
| OneLake shortcut → queryable KQL table | Programmatic (external Delta table) | Core Shortcuts API creates a OneLake **link only** (not queryable). Register an external Delta table (`.create external table … kind=delta … ;impersonate`) at the mirrored OneLake path; query via `external_table()` — see eventhouse-shortcuts-reference.md |

## Portal fallback boundary

Portal-guided instructions are allowed ONLY for OAuth Azure Monitor connector creation.

Portal guidance must NOT be used as a generic fallback for:

- Log Analytics workspace validation
- Fabric workspace validation
- Connection detection
- Connection reuse
- Service Principal connector creation
- Mirrored Catalog item creation
- Discovery
- Monitoring
- Refresh
- Eventhouse shortcut creation
- Schema verification
- Operations Agent creation

Before declaring a capability unavailable, the Skill should determine whether another supported execution path exists:

- Fabric REST APIs
- Azure REST APIs
- Fabric Actions
- Azure CLI
- Azure Resource Graph
- Fabric REST **read-only** discovery via authenticated `az rest --method get`
  against `https://api.fabric.microsoft.com/...`

MCP unavailability does not automatically imply capability unavailability.

### Fabric REST read-only discovery exception (bounded)

Arbitrary shell / CLI / `az` / PowerShell execution remains out of scope. There
is ONE narrow exception: the Skill MAY use an authenticated `az rest --method
get` call for Fabric REST **read-only discovery** only, when ALL of these hold:

- Endpoint is `https://api.fabric.microsoft.com/...`.
- HTTP method is **GET** only.
- The operation is discovery / read-only only.
- Nothing is created, updated, deleted, or modified — no Fabric items, shortcuts,
  mirrored catalog items, or connectors are created through the CLI.
- No tokens, secrets, raw auth headers, or sensitive payloads are exposed.
- The Skill clearly states the capability path used.

This exception is limited to Stage 3 (Fabric workspace discovery) and Stage 5
(Azure Monitor OAuth connection detection). It does not relax any other stage's
boundary, does not authorize non-GET `az rest` calls, and does not permit use of
the Kusto / KQL data-plane when disabled.

## Connector rules (authoritative)

Keep the two modes strictly separated. **Prefer Service Principal (automated) as
the default; fall back to OAuth only when Service Principal is unavailable or the
user explicitly requests it.** Never route OAuth through Service Principal logic
and never route Service Principal through OAuth/interactive sign-in logic.

> **Who can create a connection (grounded in the Create Connection API).** The
> Create Connection API supports **both** User and Service Principal identities,
> so the split is about the **credential type**, not the caller identity: a
> **ServicePrincipal** credential is created **non-interactively** (the automated
> SP path), whereas an **OAuth2** credential requires an **interactive sign-in**
> to mint the token — which cannot be done headlessly. That is why Azure Monitor
> **OAuth** connector creation stays UI-guided, while **Service Principal**
> connector creation is automated.

### Connection API shapes (documented — use these; do NOT guess)

Use these exact Fabric **Core** REST endpoints for connection detection and
creation. Do **not** invent a payload or search general docs — when the
connector's exact `type` / `creationMethod` / `parameters` are unknown, read them
from **List Supported Connection Types** below.

- **List connections** (detection): `GET https://api.fabric.microsoft.com/v1/connections`
  — paged via `continuationToken`; there is no server-side filter, so page through
  and match **client-side** on `connectionDetails.path` (the Log Analytics
  workspace resource id / data-source path) and `credentialDetails.credentialType`
  (`ServicePrincipal` for Mode A, `OAuth2` for Mode B). Returns only connections
  the caller holds a role on.
  [List Connections](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/list-connections)
- **Get a connection**: `GET https://api.fabric.microsoft.com/v1/connections/{connectionId}`.
  [Get Connection](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/get-connection)
- **Discover the exact connector shape** (authoritative — resolves the Azure
  Monitor `type`, `creationMethod`, and required `parameters` instead of guessing):
  `GET https://api.fabric.microsoft.com/v1/connections/supportedConnectionTypes?showAllCreationMethods=true`
  — each entry gives `type`, `creationMethods[].name`,
  `creationMethods[].parameters[]` (`name` / `dataType` / `required`) and
  `supportedCredentialTypes`. Find the Azure Monitor / Log Analytics entry and use
  its returned `type` + `creationMethod` + `parameters` **verbatim**.
  [List Supported Connection Types](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/list-supported-connection-types)
- **Create a connection** (Service Principal / Mode A):
  `POST https://api.fabric.microsoft.com/v1/connections` with this documented
  skeleton — fill `type` / `creationMethod` / `parameters` from the
  supportedConnectionTypes result, never fabricated:

  ```json
  {
    "connectivityType": "ShareableCloud",
    "displayName": "<name>",
    "connectionDetails": {
      "type": "<from supportedConnectionTypes>",
      "creationMethod": "<from supportedConnectionTypes>",
      "parameters": [
        { "dataType": "Text", "name": "<param name>", "value": "<value>" }
      ]
    },
    "privacyLevel": "Organizational",
    "credentialDetails": {
      "singleSignOnType": "None",
      "connectionEncryption": "NotEncrypted",
      "skipTestConnection": false,
      "credentials": {
        "credentialType": "ServicePrincipal",
        "tenantId": "<tenant>",
        "servicePrincipalClientId": "<app id>",
        "servicePrincipalSecretReference": { "connectionId": "<kv conn id>", "secretName": "<name>" }
      }
    }
  }
  ```

  The secret comes from a Key Vault reference (`servicePrincipalSecretReference`)
  or a `servicePrincipalSecret` supplied from an env var — **never** pasted into
  chat, logged, or echoed.
  [Create Connection](https://learn.microsoft.com/en-us/rest/api/fabric/core/connections/create-connection)

**OAuth2 (Mode B) creation is NOT automatable** — the `OAuth2` credential needs an
interactive sign-in, so create it once in Fabric → Manage Connections (see OAuth
mode below); detection/reuse still uses the List/Get endpoints above.

### Connection visibility & permissions (applies to both modes)

The Fabric connections listing returns only connections on which the **calling
identity** holds a role. Holding **any role** is enough for the connection to
appear and be reused: a **User** role is sufficient to **detect and reuse** it,
while **Owner** is only needed to **manage / modify / delete** it. This is true
for both the Service Principal (Mode A) and the user (Mode B) — e.g. a user with
only a **User** role assigned on the connection can still see it via the API. A
"no matching connection" result therefore does NOT prove the connection is
absent — it may exist but be invisible because the caller holds **no role** on it.

Before concluding a connection does not exist, the Skill MUST surface the
permission possibility and advise granting the Service Principal / user at least
a **User** role on the existing Azure Monitor connection (same Log Analytics
workspace) — **Owner is not required** for detection or reuse — then re-running
detection. Only after that may it create a new connector (Mode A) or fall back to
OAuth create-once guidance (Mode B).

> **Service Principal note (observed).** Per the docs, **any** assigned role
> should make a connection visible to the caller, and that is what the guidance
> above is based on. In practice, some Service Principal runs have only seen an
> Azure Monitor connection when the SP held the **Owner** role, even though a
> lower role should suffice. Keep the docs-based behaviour as the default (any
> role → discoverable), but give the agent this fallback: if an SP's detection
> returns nothing **after** a User-level role was granted, first verify the role
> actually applied to the right principal/connection, then, as a last resort, try
> granting the SP **Owner** before concluding the connection does not exist.

### Service Principal mode (automated create-or-reuse, default)

- Automated, non-interactive: no user login, no UI step. Attempt this **first**.
- **Idempotent**: reuse an existing matching Azure Monitor Service Principal
  connector for the same Log Analytics workspace (same data source path +
  Service Principal credential type) instead of creating a duplicate.
- Only **one** connector per run.
- **Never** reuse a non-Service-Principal (e.g. OAuth) connector in this mode.
- **Never** ask the user to paste a raw client secret into chat.
- Secrets come from **environment variables or Key Vault references** only; they
  are never echoed, logged, exposed, or included in generated instructions.
- If required inputs are missing, describe **what** is missing (tenant id, app /
  client id, and a securely-provided secret reference) using presence checks
  only. Never request the secret value in chat. Only when Service Principal
  inputs cannot be provided, fall back to OAuth mode.

### OAuth mode (UI-guided only, fallback)

Use only when Service Principal is unavailable or the user explicitly requests it.

- OAuth connector **creation** is interactive in **Fabric → Manage Connections**.
- The Skill only **detects** and **reuses** an existing Azure Monitor OAuth
  connection. Detection is **non-destructive** (never create/update/delete).
- **Never** claim public-API support for OAuth Azure Monitor connector creation.
- **Never** document browser-inspected / internal connector endpoints, hidden
  payloads, `CredentialType` internals, OAuth codes, tokens, cookies, nonces, or
  redirect URLs as supported public APIs, and never surface them to the user.
- Reuse a connection ONLY when the data source path / LAW resource id matches the
  **same** Log Analytics workspace exactly. Any mismatch → treat as no match.
- If the user explicitly supplies a connection id, validate it (must be an Azure
  Monitor Mirrored Catalog connection whose data source path matches this
  workspace) before reusing. Reject mismatches.

User-facing message when no connection exists (keep it this simple):

```text
I couldn’t find an existing Azure Monitor connection for this workspace.
Please create it once in Fabric Manage Connections, then come back and continue.
```

> **Workspace identity** is a third Mode B credential option (no secret) — the
> identity is provisioned via API and gets a Log Analytics role (assigned by
> the Skill when the caller is permitted, otherwise granted by the user).
> See [workspace-identity-connection-reference.md](workspace-identity-connection-reference.md);
> it reuses the Create Connection payload above with
> `credentialType = "WorkspaceIdentity"`.

## Supported-scope / validation rules

Before creating anything, verify: the workspace exists; the caller has required
Log Analytics access; the caller can create the item in the target Fabric
workspace. Surface pass/fail in user terms; never expose raw API responses.

## Fabric workspace discovery & capability resolution

Fabric workspaces are **not** Azure Resource Manager resources. They cannot be
enumerated through Azure resource listing, Azure Resource Graph, or `az`
resource commands, so an ARM-only environment reaching Azure resources does
**not** imply a Fabric control-plane path exists — and the reverse also holds:
lack of automatic enumeration does NOT mean no Fabric workspace exists.

Stage 3 (Fabric workspace selection) MUST follow the **Fabric Workspace
Discovery & Capability Resolution Policy** in `SKILL.md`. In short:

- Discover all surfaced Fabric mechanisms first: Fabric REST APIs, Fabric
  Actions, Fabric / OneLake / Power BI execution capabilities, authenticated
  Fabric REST read-only discovery via `az rest --method get` against
  `https://api.fabric.microsoft.com/...` (GET-only, read-only, no modifications,
  no secret/token/header exposure, capability path stated), or any other
  documented capability provider available to the agent environment.
- If automatic enumeration is unavailable, do NOT terminate. Distinguish "no
  Fabric control-plane capability at all" from "enumeration unavailable but the
  workflow can continue with user-provided workspace info".
- Ask the user for a **Fabric Workspace Name**, **Workspace ID**, or **Workspace
  URL**, then validate it as far as the available capabilities allow.
- Never fabricate a workspace, workspace id, or validation result, and never
  claim a Fabric action succeeded when the required execution capability is
  unavailable.
- Mark Stage 3 BLOCKED only after every programmatic discovery path AND every
  user-supplied resolution path (Name / ID / URL) is exhausted. UI-guided
  selection is permitted only as the final fallback.

## Fabric Operations Agent surface

Operations Agent is a first-class Fabric item (`type: "OperationsAgent"`). It can
be created and populated through documented Fabric item APIs (create item, then
set the definition with the instructions and the KQL database data source). Teams
notifications are a built-in action — no custom channel binding is required for
basic alerts. See operations-agent-reference.md.

## External references

- [Items - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/items)
- [Mirrored Catalog item definition](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/mirrored-catalog-definition)
- [Discovery - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/discovery)
- [Monitoring - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/monitoring)
- [Refresh - REST API (MirroredCatalog)](https://learn.microsoft.com/en-us/rest/api/fabric/mirroredcatalog/refresh)

> The Mirrored Catalog references above cover item CRUD, item definition,
> discovery, monitoring, and refresh/sync operations. They do **not** document
> OAuth Azure Monitor connector creation. Treat OAuth connector creation as
> UI-guided only.

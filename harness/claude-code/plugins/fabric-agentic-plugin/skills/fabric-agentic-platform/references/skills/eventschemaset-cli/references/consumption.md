<!-- Mode reference for the `eventschemaset-cli` skill. Loaded on demand from `skills/eventschemaset-cli/SKILL.md` when the request matches the `consumption` mode. -->

> **SCOPE BOUNDARY — READ-ONLY (mandatory)**
> This mode may only issue read-only calls (List, Get, GetDefinition). Do not
> create, update, override, or delete an Event Schema Set, event type, or schema.
> If the user asks for a write, state plainly that this mode is read-only, then
> announce the mode switch and read `authoring.md` before the first management call.

# eventschemaset-cli consumption mode — Read-Only Event Schema Set Inspection via CLI

> **Preview**: The Fabric **EventSchemaSet** item and its REST operations (List, Get, GetDefinition) are currently in **Preview** — behavior, response shapes, and availability may change.
>
> **Identity (all operations)**: Microsoft Learn documents every Event Schema Set REST operation (List, Get, GetDefinition) as supporting **delegated (user) identity only** — with service principals and managed identities listed as not supported. In practice, because the item is in **Preview**, service-principal / managed-identity access can succeed and is **tenant-dependent**. Prefer signing in as a user with `az login` (not `--service-principal`, and not a managed-identity context). If you must use a service principal or managed identity and a call fails with **401/403**, fall back to a delegated user identity.

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id] |
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../../common/COMMON-CORE.md#fabric-topology--key-concepts) | |
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../../common/COMMON-CORE.md#environment-urls) | |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Includes pagination, LRO polling, and rate-limiting patterns |
| Gotchas, Best Practices & Troubleshooting | [COMMON-CORE.md § Gotchas, Best Practices & Troubleshooting](../../../common/COMMON-CORE.md#gotchas-best-practices--troubleshooting) | |
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../../common/COMMON-CLI.md#tool-selection-rationale) | |
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource`**; includes pagination and LRO helpers |
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference | [COMMON-CLI.md § Quick Reference](../../../common/COMMON-CLI.md#quick-reference) | `az rest` template + token audience/tool matrix |
| List Event Schema Sets | [List Event Schema Sets](#list-event-schema-sets) | |
| Get Event Schema Set (Properties) | [Get Event Schema Set (Properties)](#get-event-schema-set-properties) | |
| Get Event Schema Set Definition | [Get Event Schema Set Definition](#get-event-schema-set-definition) | Decode base64 definition → summarize eventTypes & schemas |
| Validate Event Schema Set Configuration | [Validate Event Schema Set Configuration](#validate-event-schema-set-configuration) | |
| Must / Prefer / Avoid | [Must / Prefer / Avoid](#must--prefer--avoid) | **MUST DO / AVOID / PREFER** checklists |
| Examples | [Examples](#examples) | Prompt → command-flow pairs (list, inspect, decode definition, get schema version, list business events) |
| Agent Integration Notes | [Agent Integration Notes](#agent-integration-notes) | |

---

## Tool Stack

| Tool | Purpose |
|---|---|
| **az cli** | REST calls via `az rest`; Fabric control-plane discovery |
| **jq** | JSON processing and output formatting |
| **curl** | Required for `fabric_lro` when polling `202 Accepted` long-running operations (captures the `Location` header) |

See [COMMON-CLI.md](../../../common/COMMON-CLI.md) for installation and authentication setup.

---

## List Event Schema Sets

### List All Event Schema Sets in a Workspace

```bash
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets" \
  --resource "https://api.fabric.microsoft.com"
```

Returns a JSON object with a `value` array of items. Use JMESPath to filter by the Event Schema Set's
**display name** (set `ITEM_NAME` to the name you are looking for — not the
`eventSchemaSets` collection segment from the URL):

```bash
ITEM_NAME="my-event-schema-set"
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets" \
  --resource "https://api.fabric.microsoft.com" \
  --query "value[?displayName=='${ITEM_NAME}']"
```

### Get Event Schema Set (Properties)

Return the properties of a single Event Schema Set with the
[Get Event Schema Set](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/get-event-schema-set)
operation (read-only, scope `Item.Read.All` or `Item.ReadWrite.All`):

```bash
az rest --method GET \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}" \
  --resource "https://api.fabric.microsoft.com"
```

The response returns the item metadata:

| Field | Description |
|---|---|
| `id` | Item ID (GUID) |
| `displayName` | Item display name |
| `description` | Item description |
| `type` | Always `EventSchemaSet` |
| `workspaceId` | Owning workspace ID |
| `folderId` | Folder ID (if the item is in a folder) |
| `properties.oneLakeRootPath` | OneLake path to the Event Schema Set root directory |
| `sensitivityLabel.id` | Applied sensitivity label ID (if any) |
| `tags` | List of applied tags (`id`, `displayName`) |

When reporting to the user, summarize the display name, description, `properties.oneLakeRootPath`, and
sensitivity label. To read the schema contents (`eventTypes` / `schemas`), use
[Get Event Schema Set Definition](#get-event-schema-set-definition) below.

---

## Get Event Schema Set Definition

Retrieve the full definition of a selected Event Schema Set with the
[Get Event Schema Set Definition](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/get-event-schema-set-definition)
operation. The definition contains a schema part (named `EventSchemaSetDefinition.json` per the
definition article; the API may return a versioned name such as `EventSchemaSetV1.json`) plus a
`.platform` metadata part. The schema part's `payload` is base64-encoded JSON describing the
item's `eventTypes` and `schemas`.

> Spec: [EventSchemaSet definition](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/eventschemaset-definition)
>
> **Scope**: `getDefinition` requires `Item.ReadWrite.All` (read + write workspace permissions),
> even though it only reads the definition. (List and Get require read permissions.)
>
> **Identity**: Microsoft Learn documents `getDefinition` (like List and Get) as supporting
> **delegated (user) identity only**, with service principals and managed identities not
> supported. In practice this is **Preview** behavior and service-principal / managed-identity
> access can succeed depending on the tenant (see the top-level Identity note). Prefer a
> delegated user; on **401/403** with an SP/MI, fall back to `az login`.

#### Step 1: Retrieve the Definition

`getDefinition` is a **POST** (not GET) on the Event Schema Set endpoint. It supports an optional
`?format={format}` query parameter. Always send an explicit empty JSON body (`--body '{}'`) —
a POST without a body can return `411 Length Required`.

The examples below assume the common **synchronous `200 OK`** response, whose body is the
definition. `getDefinition` may instead return a **`202 Accepted`** long-running operation with an
**empty body** — the definition is *not* in the 202 response, so piping it straight into `jq`
yields nothing. Handle the async path explicitly (see **If `getDefinition` returns `202 Accepted`** below).

```bash
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}/getDefinition" \
  --resource "https://api.fabric.microsoft.com" \
  --body '{}'
```

#### Step 2: Decode the Definition Part

Extract the schema part (everything except `.platform`) and base64-decode its `payload`:

```bash
# Using jq + base64 (Linux; on macOS use base64 -D instead of -d)
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}/getDefinition" \
  --resource "https://api.fabric.microsoft.com" \
  --body '{}' \
  | jq -r '.definition.parts[] | select(.path != ".platform") | .payload' \
  | base64 -d | jq .
```

```powershell
# PowerShell (Windows)
$def = az rest --method POST `
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/eventSchemaSets/$ITEM_ID/getDefinition" `
  --resource "https://api.fabric.microsoft.com" `
  --body '{}' | ConvertFrom-Json
$payload = ($def.definition.parts | Where-Object { $_.path -ne '.platform' }).payload
[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($payload)) | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

#### If `getDefinition` returns `202 Accepted` (async)

`az rest` surfaces only the response **body**, not headers, so on a `202` the operation URL in
the `Location` header is not visible to `az rest` alone. This is the standard Fabric
long-running-operation (LRO) pattern: capture `Location`, poll until `Succeeded` (honouring
`Retry-After`), then `GET` the operation **result** and decode its parts as shown above. Use the
reusable `fabric_lro` helper — see [COMMON-CLI.md § Long-Running Operations](../../../common/COMMON-CLI.md#long-running-operations-lro-pattern)
— rather than hand-rolling token capture and the poll loop here.

On a synchronous `200 OK`, skip this and decode the POST response directly as shown above.

#### Step 3: Summarize the Definition

The decoded schema part has two top-level collections (both optional):

| Field | Type | Description |
|---|---|---|
| `eventTypes` | `EventType[]` | Event metadata used to communicate between source, Eventstream, and destination items |
| `schemas` | `Schema[]` | Formats used to represent the messages stored in the catalog |

Each **EventType** exposes: `id` (required), `description`, `eventTypeCategory`
(`EventType` or `BusinessEventType`), `format` (required), `envelopeMetadata`, `schemaUrl`,
`schemaFormat`, `schema`, `protocol`, and `protocolOptions`. `schemaUrl` and `schema` are mutually
exclusive.

Each **Schema** exposes: `id` (required), `description`, `format` (required), and `versions` (the
iterations of that schema, each carrying its own `format`).

`format` means different things on either side: `eventTypes[].format` is the envelope format
(`CloudEvents/1.0`), while `eventTypes[].schemaFormat`, `schemas[].format` and each
`schemas[].versions[].format` are payload-schema formats (`JsonSchema/draft-07`, `Avro/1.12.0`).
Report them as they are stored — a bare `Json` is not a value the service accepts.

When reporting to the user, enumerate the event types (id, category, format, and whether they carry
an inline `schema` or a `schemaUrl`) and the schemas (id, format, and version count).

---

## Validate Event Schema Set Configuration

After decoding the definition (see [Get Event Schema Set Definition](#get-event-schema-set-definition)),
use the parsed structure to answer read-only validation questions about how the Event Schema Set is
configured. This is inspection only — it never mutates the item.

- **Inline `schema` vs `schemaUrl` per event type** — `schema` (an embedded schema document) and
  `schemaUrl` (a pointer to an externally hosted schema) are **mutually exclusive** on each event
  type. Report, per `eventType`, which one it carries. Both are **optional**, so an event type with
  **neither** is valid (report it neutrally); only an event type carrying **both** is invalid.
- **Schema formats and versions** — for each entry under `schemas`, report its `format` (e.g.
  `JsonSchema`) and the number of `versions`. Use this to confirm the catalog uses a consistent
  format and to spot schemas with zero or unexpectedly many versions.
- **Category mix** — summarize the `eventTypeCategory` distribution (`EventType` vs
  `BusinessEventType`) so the user can confirm the catalog matches its intended purpose.

```bash
# Given the decoded definition JSON in $DEF (see Get Event Schema Set Definition),
# list each event type and whether it uses an inline schema or a schemaUrl:
echo "$DEF" | jq -r '(.eventTypes // [])[]
  | "\(.id): \(.eventTypeCategory) [\(.format)] -> "
    + (if (.schema != null and .schemaUrl != null) then "BOTH schema and schemaUrl (invalid)" elif .schema != null then "inline schema" elif .schemaUrl != null then "schemaUrl=\(.schemaUrl)" else "no inline schema or schemaUrl" end)'

# Summarize schema formats and version counts:
echo "$DEF" | jq -r '(.schemas // [])[] | "\(.id): \(.format), \(.versions | length) version(s)"'
```

Report the findings as a short per-event-type summary plus a schema-format/version rollup. If the
workspace contains no Event Schema Set, report that none were found (this is not an error).

---

## Must / Prefer / Avoid

### Must

- **Refuse the write, but still serve any read-only part of the request** — if the user asks
  to **create, add, update, modify, rename, or delete** an Event Schema Set or an event
  type/schema, state plainly that this skill is **read-only (consumption-only)** and cannot
  perform writes, then direct them to the `authoring` mode.
  For a request that is **only** a write, refuse up front: do NOT list or inspect items first,
  and do NOT proceed even if the target does not exist. For a **mixed** request that also asks
  for something read-only ("inspect X, and also delete it"), complete the read-only part and
  refuse only the mutation — leaving the item unchanged.
- **Always pass `--resource https://api.fabric.microsoft.com`** with `az rest` calls
- **Always use JMESPath filtering** to resolve workspace name → ID and item name → ID
- **Handle pagination** — check for `continuationUri`/`continuationToken` in list responses
- **Poll LRO responses** — long-running calls may return `202 Accepted`

### Prefer

- Use `jq` (bash) or `ConvertFrom-Json` (PowerShell) for parsing
- Decode/structure output into readable summaries before reporting to the user

### Avoid

- Do NOT hardcode workspace or item IDs — always discover them via the API
- Do NOT modify the event schema set nor event schema with this consumption skill — use the `authoring` mode for writes

---

## Examples

### Example 1 — List Event Schema Sets in a workspace

**Prompt:** "List all Event Schema Sets in my `Analytics` workspace."

**Flow:**
1. Resolve the workspace name → ID via `GET /v1/workspaces` + JMESPath (see the Table of Contents' *Finding Workspaces and Items in Fabric* reference).
2. `GET /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets`.
3. Report each item's `displayName` and `id` (handle pagination via `continuationToken`).

### Example 2 — Inspect an Event Schema Set's properties

**Prompt:** "Show the OneLake path and sensitivity label of the `orders-catalog` Event Schema Set in `Analytics`."

**Flow:**
1. Resolve workspace ID, then resolve the item ID by filtering the list on `displayName=='orders-catalog'`.
2. `GET /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}`.
3. Summarize `displayName`, `description`, `properties.oneLakeRootPath`, and `sensitivityLabel.id`.

### Example 3 — Decode a definition and summarize event types & schemas

**Prompt:** "Decode the definition of the `orders-catalog` Event Schema Set and tell me its event types and schemas."

**Flow:**
1. Resolve workspace ID and item ID (as above).
2. `POST /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}/getDefinition` (send an empty `{}` body; poll the `Location` header if it returns `202`).
3. Select the schema part (`.path != ".platform"`), base64-decode its `payload`, and parse the JSON.
4. Enumerate `eventTypes` (id, category, format, inline `schema` vs `schemaUrl`) and `schemas` (id, format, version count).

### Example 4 — Get a specific version of a schema

**Prompt:** "Get version `v2` of schema `BicycleSchema` in the `orders-catalog` Event Schema Set in `Analytics`."

The user supplies the **Event Schema Set name**, a **schema id**, and a **version id**. Each version is an object with a required, stable string `id` (e.g. `v1`, `v2`) — select the version by that `id`, not by array position.

**Flow:**
1. Resolve the workspace ID, then resolve the Event Schema Set item ID by filtering the list on `displayName`. If no item matches, report that the Event Schema Set was not found and stop.
2. `POST /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}/getDefinition` (send an empty `{}` body; poll the `Location` header if it returns `202`), select the schema part (`.path != ".platform"`), base64-decode its `payload`, and parse the JSON.
3. Find the entry in `schemas` whose `id` equals the requested schema id (use null-safe access — `schemas` may be absent). If no schema matches, report the requested id was not found, list the available schema ids, and stop.
4. In that schema's `versions` array (null-safe), find the version whose `id` matches the requested version id — e.g. `(.versions // [])[] | select(.id == $versionId)`. If no version has that `id`, do **not** silently pick another. Tell the user the requested version id was not found, list the available version ids, and ask whether they want:
   - the **latest** version (the last entry, `(.versions // [])[-1]`),
   - a **different** version id they specify, or
   - to **abort**.
   Proceed only once the user chooses (and re-validate their new choice). If the schema has no versions at all, report that and stop.
5. Report the selected version's `id`, `format`, and `schema` document. This is read-only — never mutate the item.

### Example 5 — List business events (vs regular events)

**Prompt:** "List all business events in the `orders-catalog` Event Schema Set in `Analytics`."

Business events are **not** a separate collection — they are `eventTypes` entries whose `eventTypeCategory` is `BusinessEventType`. Regular events are those with `eventTypeCategory` set to `EventType` **or the field absent** (it is optional).

**Flow:**
1. Resolve the workspace ID and the Event Schema Set item ID (as above).
2. `POST /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}/getDefinition` (send an empty `{}` body; poll the `Location` header if it returns `202`), select the schema part (`.path != ".platform"`), base64-decode its `payload`, and parse the JSON into `$DEF`.
3. Filter the `eventTypes` array by category (use null-safe access — `eventTypes` may be absent):
   - **Business events:** `echo "$DEF" | jq -r '(.eventTypes // [])[] | select(.eventTypeCategory == "BusinessEventType") | .id'`
   - **Regular events** (symmetric): replace the predicate with `select((.eventTypeCategory // "EventType") != "BusinessEventType")`.
4. Report each matching event's `id`, `format`, and whether it carries an inline `schema` or a `schemaUrl`. If none match, report that the schema set has no business events (this is not an error). Read-only — never mutate the item.

---

## Agent Integration Notes

- This skill is **read-only** — it does not create, alter, or delete items.
- For authoring operations, use the `authoring` mode.
- For cross-workload orchestration, delegate to the **FabricDataEngineer** agent.

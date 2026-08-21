<!-- Mode reference for the `eventschemaset-cli` skill. Loaded on demand from `skills/eventschemaset-cli/SKILL.md` when the request matches the `authoring` mode. -->

> **PRE-MUTATION REQUIREMENTS GATE (mandatory)**
> Before any create, update, override, or delete, confirm the request identifies
> the target workspace and the specific Event Schema Set (and, for a definition
> override, the intended eventTypes/schemas change). If the request is generic or
> ambiguous, such as "set up my event schema set" or "delete the first one", ask a
> clarifying question and stop before mutation. UpdateDefinition REPLACES the whole
> definition and Delete is permanent with `?hardDelete=true` -- always echo the
> resolved displayName + id for the audit trail. When the request already names the
> target item AND the destructive/overwrite action explicitly, that instruction IS
> the confirmation: proceed with the single write after echoing. Ask for a separate
> yes/no confirmation only when the target or intent is ambiguous.

# eventschemaset-cli authoring mode — Event Schema Set Authoring via CLI

> **Preview**: The Fabric **EventSchemaSet** item and its REST operations (Create, Update, UpdateDefinition, Delete) are currently in **Preview** — behavior, response shapes, and availability may change.
>
> **Identity (all operations)**: Microsoft Learn documents every Event Schema Set write operation (Create, Update, UpdateDefinition, Delete) as supporting **delegated (user) identity only** — with service principals and managed identities listed as not supported. In practice, because the item is in **Preview**, service-principal / managed-identity access can succeed and is **tenant-dependent**. Prefer signing in as a user with `az login` (not `--service-principal`, and not a managed-identity context). If you must use a service principal or managed identity and a call fails with **401/403**, fall back to a delegated user identity.
>
> **Permissions**: Write operations require a workspace **Contributor** role (or higher) and the `Item.ReadWrite.All` delegated scope. The workspace must be on a supported Fabric capacity.

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
| Long-Running Operations (LRO) | [COMMON-CLI.md § Long-Running Operations (LRO) Pattern](../../../common/COMMON-CLI.md#long-running-operations-lro-pattern) | `202 Accepted` → capture `Location`, poll `Retry-After` until `Succeeded` |
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference | [COMMON-CLI.md § Quick Reference](../../../common/COMMON-CLI.md#quick-reference) | `az rest` template + token audience/tool matrix |
| Create an Event Schema Set | [Create an Event Schema Set](#create-an-event-schema-set) | Empty item, or created with an inline definition |
| Update Event Schema Set Properties | [Update Event Schema Set Properties](#update-event-schema-set-properties) | Rename / change description via PATCH |
| Update Event Schema Set Definition | [Update Event Schema Set Definition](#update-event-schema-set-definition) | Override `eventTypes` / `schemas` (build → base64 → submit) |
| Delete an Event Schema Set | [Delete an Event Schema Set](#delete-an-event-schema-set) | |
| Definition Structure | [Definition Structure](#definition-structure) | `eventTypes` and `schemas` shape used by Create/UpdateDefinition |
| Must / Prefer / Avoid | [Must / Prefer / Avoid](#must--prefer--avoid) | **MUST DO / AVOID / PREFER** checklists |
| Examples | [Examples](#examples) | Prompt → command-flow pairs (create, rename, override definition, add event type, delete) |
| Agent Integration Notes | [Agent Integration Notes](#agent-integration-notes) | |

---

## Tool Stack

| Tool | Purpose |
|---|---|
| **az cli** | REST calls via `az rest`; Fabric control-plane discovery |
| **jq** | JSON processing, building the definition payload, and output formatting |
| **base64** | Encode the definition part payload before submission |
| **curl** | Required for the LRO helper when polling `202 Accepted` responses (captures the `Location` header) |

See [COMMON-CLI.md](../../../common/COMMON-CLI.md) for installation and authentication setup.

---

## Create an Event Schema Set

Create a new Event Schema Set with the
[Create Event Schema Set](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/create-event-schema-set)
operation (scope `Item.ReadWrite.All`, workspace **Contributor**). The request body takes a required
`displayName` and optional `description`, `definition`, and `sensitivityLabelSettings`.

The call returns **`201 Created`** with the new item on the synchronous path, or **`202 Accepted`**
(LRO) with an empty body while provisioning continues — in that case capture the `Location` header
and poll until `Succeeded` (see the LRO reference in the Table of Contents). Always confirm the new
item's `id` from the final response before reporting success.

### Create an empty Event Schema Set

```bash
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets" \
  --resource "https://api.fabric.microsoft.com" \
  --body '{"displayName":"orders-catalog","description":"Order domain event catalog"}'
```

### Create with an inline definition

To create the item already populated, include a `definition` object whose `parts[]` carry the
base64-encoded schema part (and optionally a `.platform` part). Build the definition JSON first (see
[Definition Structure](#definition-structure)), base64-encode it, then embed it. Guide the model to
assemble the payload rather than pasting a fixed template — the `eventTypes`/`schemas` content is
scenario-specific.

```bash
# $DEF_JSON holds the decoded EventSchemaSet definition document (eventTypes/schemas).
PAYLOAD=$(printf '%s' "$DEF_JSON" | base64 -w0)   # macOS: base64 | tr -d '\n'
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets" \
  --resource "https://api.fabric.microsoft.com" \
  --body "$(jq -n --arg name "orders-catalog" --arg payload "$PAYLOAD" '{
    displayName: $name,
    definition: { parts: [ { path: "EventSchemaSetDefinition.json", payload: $payload, payloadType: "InlineBase64" } ] }
  }')"
```

> Prefer writing the assembled request body to a file and passing `--body @body.json` when the payload
> is large — long inline `--body` strings hit shell-quoting and length limits.

---

## Update Event Schema Set Properties

Change an existing item's `displayName` or `description` with the
[Update Event Schema Set](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/update-event-schema-set)
operation. This is a **PATCH** on the item endpoint and only touches metadata — it does **not** alter
the `eventTypes`/`schemas` definition (use [Update Event Schema Set Definition](#update-event-schema-set-definition)
for that).

```bash
az rest --method PATCH \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}" \
  --resource "https://api.fabric.microsoft.com" \
  --body '{"displayName":"orders-catalog-v2","description":"Renamed order catalog"}'
```

Send only the fields you intend to change. Resolve `${ITEM_ID}` by listing the workspace's Event
Schema Sets and filtering on `displayName` (see the *Finding Workspaces and Items* reference) — never
hardcode it.

---

## Update Event Schema Set Definition

Override the item's definition — its full `eventTypes` and `schemas` — with the
[Update Event Schema Set Definition](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/update-event-schema-set-definition)
operation. This is a **POST** on `.../updateDefinition` and **replaces** the entire definition (it is
an override, not a merge), so build the complete target definition, not just the delta.

> **Scope**: requires `Item.ReadWrite.All` (read + write workspace permissions).
>
> **`updateMetadata`**: pass `?updateMetadata=true` only when you include a `.platform` part and want
> the item's metadata refreshed from it. Updating the definition does **not** change the sensitivity label.

#### Step 1: Build and encode the target definition

Assemble the complete definition document (see [Definition Structure](#definition-structure)),
then base64-encode it as the schema part's `payload`:

```bash
# $DEF_JSON = the complete, decoded EventSchemaSet definition after your edits.
PAYLOAD=$(printf '%s' "$DEF_JSON" | base64 -w0)   # macOS: base64 | tr -d '\n'
jq -n --arg payload "$PAYLOAD" '{
  definition: { parts: [ { path: "EventSchemaSetDefinition.json", payload: $payload, payloadType: "InlineBase64" } ] }
}' > updateDefinition-body.json
```

To edit an existing definition, first retrieve and decode it with the `consumption` mode
(Get Definition), apply the change to the decoded JSON, then re-encode as above.

#### Step 2: Submit the override

```bash
az rest --method POST \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}/updateDefinition" \
  --resource "https://api.fabric.microsoft.com" \
  --body @updateDefinition-body.json
```

Returns **`200 OK`** on the synchronous path or **`202 Accepted`** (LRO) — on a `202`, capture the
`Location` header and poll until `Succeeded` before reporting success (see the LRO reference).

---

## Delete an Event Schema Set

Remove an Event Schema Set with the
[Delete Event Schema Set](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/delete-event-schema-set)
operation. By default (`hardDelete` omitted or `false`) the item is **soft-deleted** when the item
type supports it — recoverable from the workspace recycle bin; pass `?hardDelete=true` to remove it
**permanently**. Delete is permanent only with `?hardDelete=true`; always echo the resolved target
first, and — when the request did not already name the item and the delete explicitly — confirm with
the user before issuing it.

```bash
# Default: soft-delete (recoverable if the item type supports it).
# Append ?hardDelete=true to the URL to delete permanently.
az rest --method DELETE \
  --url "https://api.fabric.microsoft.com/v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}" \
  --resource "https://api.fabric.microsoft.com"
```

Resolve `${ITEM_ID}` by name first and echo back the resolved `displayName` + `id`. When the request
already named the item and the delete explicitly, that IS the confirmation — proceed; otherwise ask
the user to confirm before issuing the DELETE.

---

## Definition Structure

Create and Update-Definition submit a **base64-encoded** definition document. Decoded, it has two
top-level, optional collections:

| Field | Type | Description |
|---|---|---|
| `eventTypes` | `EventType[]` | Event metadata shared between source, Eventstream, and destination items |
| `schemas` | `Schema[]` | Formats used to represent the messages stored in the catalog |

Each **EventType** carries: `id` (required), `description`, `eventTypeCategory`
(`EventType` or `BusinessEventType`), `format` (required), `envelopeMetadata`, `schemaUrl`,
`schemaFormat`, `schema`, `protocol`, and `protocolOptions`. `schemaUrl` and `schema` are **mutually
exclusive** — set at most one.

Each **Schema** carries: `id` (required), `description`, `format` (required), and `versions` (each
version has a stable string `id` such as `v1`, `v2`, plus its own **required** `format`).

### Format fields — use versioned values, never bare `Json`

`format` means different things on an EventType than on a Schema, and the service validates both.
Sending a bare `Json` fails with `400 InputError`: *"Provided \"Format\" is not valid. Supported
formats are JsonSchema, Avro, Protobuf and XSD."*

| Field | Meaning | Use |
|---|---|---|
| `eventTypes[].format` | Envelope / serialization format of the event | `CloudEvents/1.0` |
| `eventTypes[].schemaFormat` | Format of that event's payload schema | `JsonSchema/draft-07`, `Avro/1.12.0` |
| `schemas[].format` | Format of the schema declaration | `JsonSchema/draft-07`, `Avro/1.12.0` |
| `schemas[].versions[].format` | Required on every version; match the parent schema | `JsonSchema/draft-07`, `Avro/1.12.0` |

**When the user says "JSON format"**, they mean the payload schema, not the envelope: set
`eventTypes[].format` to `CloudEvents/1.0` and put `JsonSchema/draft-07` on `schemaFormat` (and on
the `schemas[]` entry plus each of its `versions[]`). Never put `Json` in any `format` field.

> `eventTypeCategory` is accepted on write but is **not** returned by Get Definition today (Preview).
> Send it when the user asks for a `BusinessEventType`, but do not expect to read it back, and do not
> report an event's category from a decoded definition — it will look empty.

The definition is wrapped for submission as a part:

```json
{
  "definition": {
    "parts": [
      { "path": "EventSchemaSetDefinition.json", "payload": "<base64 of the decoded document>", "payloadType": "InlineBase64" }
    ]
  }
}
```

See the [EventSchemaSet definition article](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/eventschemaset-definition)
for the authoritative part naming and structure. The `path` is a label (the REST operation examples
also show `EventSchemaSetV1.json`); when overriding an existing item, **reuse the exact part `path`
returned by Get Definition** rather than inventing one. Let the model generate the concrete
`eventTypes`/`schemas` from the user's intent — do not hardcode a fixed catalog.

---

## Must / Prefer / Avoid

### Must

- **Confirm destructive and overwrite actions before executing** — Delete is permanent (with `?hardDelete=true`), and
  Update-Definition **replaces** the whole definition. Always echo the resolved `displayName` + `id`; a request that
  already names the target item AND the destructive/overwrite action IS the confirmation, so proceed with the single
  write after echoing. Ask for a separate confirmation only when the target or intent is ambiguous.
- **Always pass `--resource https://api.fabric.microsoft.com`** with `az rest` calls.
- **Always resolve workspace and item IDs via JMESPath filtering** — never hardcode them.
- **Build the complete definition for `updateDefinition`** — it is an override, not a merge. To edit,
  decode the current definition (via the `consumption` mode), change it, re-encode the full document.
- **Handle LRO responses** — Create and Update-Definition may return `202 Accepted`; capture `Location`
  and poll until `Succeeded` before reporting success.
- **Prefer a delegated user identity** (`az login`) — write ops are documented as user-only; fall back
  from SP/MI to a user on 401/403.

### Prefer

- Write large request bodies to a file and pass `--body @file.json` to avoid shell-quoting/length limits.
- Use `jq -n` to assemble request bodies and inject the base64 `payload`, rather than string concatenation.
- Base64-encode with no line wraps (`base64 -w0`, or `base64 | tr -d '\n'` on macOS).
- Send only changed fields in the PATCH (Update Properties).

### Avoid

- Do NOT hardcode workspace or item IDs — always discover them via the API.
- Do NOT send a partial definition to `updateDefinition` expecting a merge — you will drop the omitted event types/schemas.
- Do NOT set both `schema` and `schemaUrl` on one event type — they are mutually exclusive.
- Do NOT use this authoring skill for read-only listing/inspection/decoding — use the `consumption` mode.
- Do NOT confuse EventSchemaSet with Eventstream or Eventhouse — use their dedicated skills.

---

## Examples

### Example 1 — Create an empty Event Schema Set

**Prompt:** "Create an Event Schema Set called `orders-catalog` in my `Analytics` workspace."

**Flow:**
1. Resolve the workspace name → ID via `GET /v1/workspaces` + JMESPath (see the Table of Contents' *Finding Workspaces and Items in Fabric* reference).
2. `POST /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets` with `{"displayName":"orders-catalog"}`.
3. If the response is `202 Accepted`, capture `Location` and poll until `Succeeded`. Report the new item's `id`.

### Example 2 — Rename an Event Schema Set / change its description

**Prompt:** "Rename the `orders-catalog` Event Schema Set to `orders-catalog-v2` in `Analytics`."

**Flow:**
1. Resolve the workspace ID, then resolve the item ID by filtering the list on `displayName=='orders-catalog'`. If none matches, report not found and stop.
2. `PATCH /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}` with `{"displayName":"orders-catalog-v2"}`.
3. Confirm the updated `displayName` in the response.

### Example 3 — Override the definition to add an event type

**Prompt:** "Add a `BusinessEventType` event `OrderPlaced` (JSON format) to the `orders-catalog` Event Schema Set."

**Flow:**
1. Resolve the workspace ID and item ID (as above).
2. Retrieve and decode the current definition (delegate to the `consumption` mode Get Definition), so the override preserves existing event types/schemas.
3. Append the new `eventTypes` entry (`id: OrderPlaced`, `eventTypeCategory: BusinessEventType`, `format: CloudEvents/1.0`, and — since the user said JSON — `schemaFormat: JsonSchema/draft-07`) to the decoded document.
4. Base64-encode the **complete** updated document and `POST .../updateDefinition` with the wrapped `definition.parts` body, reusing the exact part `path` returned by Get Definition.
5. If `202 Accepted`, poll the `Location` until `Succeeded`. Confirm the new event type is present by re-decoding.

### Example 4 — Create an Event Schema Set with an inline definition

**Prompt:** "Create `payments-catalog` in `Analytics` with a `JsonSchema` schema `PaymentSchema` and an `EventType` event `PaymentReceived`."

**Flow:**
1. Resolve the workspace ID.
2. Build the definition document with the requested `schemas` (`PaymentSchema`, `format: JsonSchema/draft-07`, each entry under `versions` carrying the same `format`) and `eventTypes` (`PaymentReceived`, `format: CloudEvents/1.0`, `schemaFormat: JsonSchema/draft-07`).
3. Base64-encode it and `POST /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets` with `{ displayName, definition: { parts: [...] } }`.
4. Handle `201`/`202`; report the created item `id`.

### Example 5 — Delete an Event Schema Set

**Prompt:** "Delete the `orders-catalog-old` Event Schema Set from `Analytics`."

**Flow:**
1. Resolve the workspace ID and the item ID by filtering on `displayName=='orders-catalog-old'`. If none matches, report not found and stop.
2. Echo the resolved `displayName` + `id`. The prompt already named the item and the delete, so that instruction IS the confirmation — proceed (delete is permanent if `hardDelete=true`).
3. Issue `DELETE /v1/workspaces/${WORKSPACE_ID}/eventSchemaSets/${ITEM_ID}`.
4. Report success (HTTP 200).

---

## Agent Integration Notes

- This skill performs **writes** — Create, Update (properties), Update-Definition (override), and Delete.
- For read-only listing, property inspection, and definition decoding, delegate to the `consumption` mode.
- For the Eventstream ingestion/routing pipeline, use `eventstream-cli`.
- For cross-workload orchestration, delegate to the **FabricDataEngineer** agent.

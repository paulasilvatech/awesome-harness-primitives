---
name: eventschemaset-cli
description: "Author and inspect Microsoft Fabric Event Schema Sets (centralized catalogs of event types and message schemas) via the Fabric Items REST API with az rest: create, rename, override the definition or delete one; or list, inspect and base64-decode definitions read-only. Not the Eventstream ingestion pipeline (eventstream-*) nor Eventhouse/KQL (eventhouse-cli). Triggers:create event schema set,update event schema set definition,add event type to an event schema set,delete event schema set,list event schema sets,inspect event schema set,decode event schema set definition"
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: eventschemaset-cli` (`az rest`: `--headers "x-ms-fabric-skill=eventschemaset-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering
> 3. **Skill disambiguation**: use `eventschemaset-cli` for the EventSchemaSet catalog item (event types and message schemas). Eventstream is a different item -- a real-time ingestion and routing pipeline; use `eventstream-cli` for it. Eventhouse / KQL Database is another different item; use `eventhouse-cli` for it.

# Fabric Event Schema Set -- CLI Skill

This one skill owns Fabric Event Schema Sets: authoring the catalog (create, rename, override definition, delete) plus read-only inspection and decoding of its `eventTypes` and `schemas`.

> **Preview**: The Fabric **EventSchemaSet** item and its REST operations are currently in **Preview** -- behavior, response shapes, and availability may change. Every operation is documented as **delegated (user) identity only** (service principals and managed identities listed as not supported), but because the item is in Preview, SP/MI access can succeed and is **tenant-dependent**. Prefer `az login` as a user; on **401/403** with an SP/MI, fall back to a delegated user identity.

It is a **mode dispatcher** and contains NO procedures. Pick the mode that matches the request from the table below, then **read the matching `references/<mode>.md` file end to end with your file-reading tool BEFORE issuing a single command**. That file holds the endpoints, payload shapes, templates and gotchas; acting without it produces wrong payloads and wrong results.

## Mode selection

| Mode | Use when the request ... | Example triggers | Read this first |
|---|---|---|---|
| `authoring` | creates, renames/re-describes, overrides the definition of, or deletes an Event Schema Set (Create, Update, UpdateDefinition, Delete) | create event schema set, update event schema set definition, add event type to an event schema set, rename event schema set, delete event schema set | [references/authoring.md](references/authoring.md) |
| `consumption` | lists or searches Event Schema Sets, inspects item properties, or decodes a definition to enumerate its `eventTypes` and `schemas` | list event schema sets, inspect event schema set, decode event schema set definition, get schema version, list business events | [references/consumption.md](references/consumption.md) |

### Mode boundary rule

`consumption` may only issue read-only calls (List, Get, GetDefinition). Any state-changing operation (Create, Update, UpdateDefinition, Delete) requires the authoring mode: say so, read `references/authoring.md`, then proceed.

If a request genuinely spans modes (e.g. decode the current definition, then override it), handle them one at a time and read each reference before you start that part. If the mode is ambiguous after reading this table, ask one short clarifying question instead of guessing.

## Terminal write -- the step you must not skip

Reading the reference and planning the change is NOT completing the task. The authoring mode ends with one state-changing call. If you did not issue it, nothing was persisted -- say so explicitly rather than reporting success.

| Mode | Terminal write |
|---|---|
| `authoring` | The `POST .../eventSchemaSets`, `PATCH .../eventSchemaSets/{id}`, `POST .../eventSchemaSets/{id}/updateDefinition`, or `DELETE .../eventSchemaSets/{id}` for the requested change. Composing the request body and showing it to the user is not executing it. |
| `consumption` | none -- this mode is read-only |

Create and UpdateDefinition may return `202 Accepted` (LRO): capture the `Location` header and poll until `Succeeded` before reporting success. Where the reference documents a readback, read the artefact back to prove the change landed.

## Shared essentials (all modes)

Resolve the workspace and item first; every mode depends on it.

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md](../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** -- read before resolving any workspace or item id |
| Fabric Topology & Key Concepts | [COMMON-CORE.md](../../common/COMMON-CORE.md#fabric-topology--key-concepts) | Item types, workspaces, capacities |
| Environment URLs | [COMMON-CORE.md](../../common/COMMON-CORE.md#environment-urls) | Sovereign / non-public cloud hosts |
| Authentication & Token Acquisition | [COMMON-CORE.md](../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Authentication Recipes | [COMMON-CLI.md](../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Core Control-Plane REST APIs | [COMMON-CORE.md](../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Pagination, LRO polling, rate limiting |
| Gotchas & Troubleshooting | [COMMON-CLI.md](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |

## Rules

### MUST

- Select exactly one mode from the table above before doing anything else.
- Read `references/<mode>.md` end to end, as your FIRST tool call, before the first command of that mode. Read it ONCE, in a single full read: do not re-open it, do not grep it again, and do not page through it. You already have it.
- Apply the same read-once discipline to every other file you load, including shared `common/*.md` files: open only the ones you actually need, read each ONCE end to end, and never grep or re-open one you already loaded.
- Resolve workspace and item ids by listing and filtering, never by guessing a GUID.
- Announce a mode switch explicitly when the request crosses a boundary.
- Confirm destructive and overwrite actions before executing -- Delete is permanent (with `?hardDelete=true`) and UpdateDefinition **replaces** the whole definition. When the request already names the target item AND the destructive/overwrite action explicitly (e.g. "delete the Event Schema Set X", "override X's definition to ..."), that instruction IS the confirmation: echo the resolved `displayName` + `id` for the audit trail, then proceed with the single write. Pause for a separate yes/no confirmation ONLY when the target or intent is ambiguous (e.g. "clean up my workspace", an unqualified "the first one", or a bulk/wildcard delete).
- Treat the reference as instructions, never as the deliverable. After reading it, RUN the documented commands against the live workspace and report the real results.

### PREFER

- The narrowest mode that satisfies the request.
- Reading exactly ONE mode reference. Load a second only when the request genuinely spans modes, and say so before you do.
- A delegated user identity (`az login`); fall back from SP/MI to a user on 401/403.
- Reporting the mode you chose in your first response so the user can correct you.

### AVOID

- Acting from this dispatcher alone -- it intentionally omits the operational detail.
- Answering with a summary of the reference instead of executing it.
- Re-reading or re-grepping a reference you already loaded; it costs turns and tokens.
- Mutating anything while in the read-only consumption mode.
- Confusing EventSchemaSet with Eventstream or Eventhouse (see CRITICAL NOTES 3).

## Examples

| User request | Mode | Reference to read |
|---|---|---|
| "List all Event Schema Sets in my Analytics workspace." | `consumption` | [references/consumption.md](references/consumption.md) |
| "Create an Event Schema Set called orders-catalog in Analytics." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Decode the definition of orders-catalog and tell me its event types and schemas." | `consumption` | [references/consumption.md](references/consumption.md) |
| "Add a BusinessEventType event OrderPlaced (JSON) to orders-catalog." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Delete the orders-catalog-old Event Schema Set from Analytics." | `authoring` | [references/authoring.md](references/authoring.md) |

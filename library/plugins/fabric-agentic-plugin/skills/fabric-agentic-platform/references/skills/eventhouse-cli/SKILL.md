---
name: eventhouse-cli
description: "Author and query Fabric Eventhouse / KQL databases: create tables, functions, policies, materialized views and ingestion, or run read-only KQL for real-time and time-series analytics. Ingestion topology is eventstream-cli. Triggers:kql query,query eventhouse,create kql table,kql ingestion,kql retention policy,materialized view kql"
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: eventhouse-cli` (`az rest`: `--headers "x-ms-fabric-skill=eventhouse-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering
> 3. **Skill disambiguation**: use `eventhouse-cli` for anything expressed in KQL or stored in a KQL Database. Use the matching `eventstream-cli` mode for streaming topology, and the matching `sqldw-*` skill for T-SQL against a Warehouse or Lakehouse SQL endpoint.

# Fabric Eventhouse / KQL Database -- CLI Skill

This one skill owns Fabric Eventhouse and KQL Database: schema and ingestion management plus read-only KQL analytics.

It is a **mode dispatcher** and contains NO procedures. Pick the mode that matches the request from the table below, then **read the matching `references/<mode>.md` file end to end with your file-reading tool BEFORE issuing a single command**. That file holds the endpoints, payload shapes, templates and gotchas; acting without it produces wrong payloads and wrong results.

## Mode selection

| Mode | Use when the request ... | Example triggers | Read this first |
|---|---|---|---|
| `authoring` | runs KQL management commands (`.create`, `.alter`, `.ingest`, `.drop`), policies, mappings, functions or materialized views | create kql table, kql ingestion, kql retention policy, kql function, materialized view, kql mapping | [references/authoring.md](references/authoring.md) |
| `consumption` | runs read-only KQL (`where`, `summarize`, `join`, `render`), discovers schema with `.show`, or monitors ingestion health | kql query, query eventhouse, time-series kql, show tables kql, explore eventhouse | [references/consumption.md](references/consumption.md) |

### Mode boundary rule

`consumption` may only issue read-only KQL and `.show` commands. Any dot-command that changes state (`.create`, `.alter`, `.ingest`, `.drop`, `.set-or-append`) requires the authoring mode: say so, read `references/authoring.md`, then proceed.

If a request genuinely spans modes, handle them one at a time and read each reference before you start that part. If the mode is ambiguous after reading this table, ask one short clarifying question instead of guessing.

## Terminal write -- the step you must not skip

Reading the reference and planning the change is NOT completing the task. Each mutating mode ends with one state-changing call. If you did not issue it, nothing was persisted -- say so explicitly rather than reporting success.

| Mode | Terminal write |
|---|---|
| `authoring` | `POST .../v1/rest/mgmt` carrying the literal `.create-merge table` (or `CREATE TABLE`-equivalent), `.alter` or `.ingest` command. Composing the KQL management command and showing it to the user is not executing it. |
| `consumption` | none -- this mode is read-only |

Before you report the task done, confirm the terminal call returned success and, where the reference documents a readback, read the artefact back to prove the change landed.

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
- Apply the same read-once discipline to every other file you load, including nested `references/<mode>/*.md` sub-references and shared `common/*.md` files: open only the ones you actually need, read each ONCE end to end, and never grep or re-open one you already loaded.
- Resolve workspace and item ids by listing and filtering, never by guessing a GUID.
- Announce a mode switch explicitly when the request crosses a boundary.
- Treat the reference as instructions, never as the deliverable. After reading it, RUN the documented commands against the live workspace and report the real results. Quoting what the reference says instead of executing it does not answer the request.

### PREFER

- The narrowest mode that satisfies the request.
- Reading exactly ONE mode reference. Load a second only when the request genuinely spans modes, and say so before you do.
- Reporting the mode you chose in your first response so the user can correct you.

### AVOID

- Acting from this dispatcher alone -- it intentionally omits the operational detail.
- Answering with a summary of the reference instead of executing it.
- Re-reading or re-grepping a reference you already loaded; it costs turns and tokens.
- Mutating anything while in a read-only mode.
- Loading a different skill for work this family already owns (see CRITICAL NOTES 3).

## Examples

| User request | Mode | Reference to read |
|---|---|---|
| "How many events arrived per hour in the last day in the Telemetry eventhouse?" | `consumption` | [references/consumption.md](references/consumption.md) |
| "Create a KQL table for the sensor feed and a 30-day retention policy." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Show me the tables in the KQL database and their row counts." | `consumption` | [references/consumption.md](references/consumption.md) |

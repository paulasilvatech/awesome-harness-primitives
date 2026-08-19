---
name: sqldb-cli
description: "Design, read and troubleshoot a Fabric SQL database item (OLTP, SQL Server engine): schema with constraints, indexes and vector columns; sqlcmd lookups including temporal and similarity search; Query Store, blocking and regressed-plan investigation. Warehouse items belong to sqldw-cli. Triggers:create sqldb table,sqldb foreign key,dacpac deploy,sqldb sys.tables,vector similarity sqldb,sqldb query store,sql database blocked sessions"
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: sqldb-cli` (`az rest`: `--headers "x-ms-fabric-skill=sqldb-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering
> 3. **Skill disambiguation**: use `sqldb-cli` ONLY for a Fabric SQL database item (the OLTP, SQL Server engine). A Warehouse, a Lakehouse SQL endpoint or a Mirrored Database is `sqldw-cli`; a notebook cell is `spark-cli`.

# Fabric SQL Database (OLTP) -- CLI Skill

This one skill owns Fabric SQL database: T-SQL schema authoring, read-only querying, and OLTP performance diagnostics.

It is a **mode dispatcher** and contains NO procedures. Pick the mode that matches the request from the table below, then **read the matching `references/<mode>.md` file end to end with your file-reading tool BEFORE issuing a single command**. That file holds the endpoints, payload shapes, templates and gotchas; acting without it produces wrong payloads and wrong results.

## Mode selection

| Mode | Use when the request ... | Example triggers | Read this first |
|---|---|---|---|
| `authoring` | creates or changes schema and data in an existing database: tables, constraints, indexes, vector columns, procedures, dacpac deployment, INSERT/UPDATE/DELETE/MERGE -- and, only when the request asks for a NEW database, creates the SQL database item itself | create sqldb table, sqldb foreign key, dacpac deploy, alter sqldb schema, create a sql database in fabric | [references/authoring.md](references/authoring.md) |
| `consumption` | runs read-only T-SQL through sqlcmd: SELECT, catalog exploration, vector similarity search, temporal queries | sqldb sys.tables, vector similarity sqldb, temporal sqldb, query the sql database | [references/consumption.md](references/consumption.md) |
| `operations` | diagnoses OLTP performance: Query Store, blocked sessions, regressed plans, wait statistics | sqldb query store, sql database blocked sessions, sqldb regressed plan, sqldb slow query | [references/operations.md](references/operations.md) |

### Mode boundary rule

`consumption` issues read-only T-SQL only. Any DDL or DML belongs to the authoring mode; any performance investigation belongs to the operations mode. Announce the switch, read the matching reference, then act.

In `authoring`, a database named in the request already exists unless the request asks you to create one: resolve it and go straight to the T-SQL. Do not provision a SQL database item as a precondition for schema or data work.

If a request genuinely spans modes, handle them one at a time and read each reference before you start that part. If the mode is ambiguous after reading this table, ask one short clarifying question instead of guessing.

## Terminal write -- the step you must not skip

Reading the reference and planning the change is NOT completing the task. Each mutating mode ends with one state-changing call. If you did not issue it, nothing was persisted -- say so explicitly rather than reporting success.

| Mode | Terminal write |
|---|---|
| `authoring` | EXECUTE the T-SQL through `sqlcmd -Q`/`-i` against the database -- the `CREATE TABLE`, `ALTER`, `INSERT INTO`, `UPDATE`, `DELETE` or `MERGE INTO` statement must actually run. Composing DDL or DML and showing it to the user changes nothing. Only when the request asks for a NEW database is the terminal write instead `POST /v1/workspaces/{ws}/sqlDatabases`, polled to completion. |
| `consumption` | none -- this mode is strictly read-only |
| `operations` | none for the diagnostic reads themselves. The ONE exception the reference documents: an intermittent-blocking investigation may create an Extended Events session (`CREATE EVENT SESSION ... ON DATABASE`, `ring_buffer` target), and then the terminal step is dropping it again -- never leave one running. |

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
- Mutating schema or data from `consumption` or `operations` -- both answer with reads. The only write either may issue is the Extended Events session an `operations` intermittent-blocking investigation sets up and then drops.
- Loading a different skill for work this family already owns (see CRITICAL NOTES 3).

## Examples

| User request | Mode | Reference to read |
|---|---|---|
| "Create an Orders table with a foreign key to Customers in the Fabric SQL database." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Create a new SQL database in this workspace called sales_oltp." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Find the 5 nearest embeddings to this vector in the SQL database." | `consumption` | [references/consumption.md](references/consumption.md) |
| "Which queries regressed in the last day according to Query Store?" | `operations` | [references/operations.md](references/operations.md) |


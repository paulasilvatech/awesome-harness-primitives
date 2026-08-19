---
name: spark-cli
description: "Author, run and diagnose Fabric Spark: notebook cell code (%%configure, %%sql, PySpark, notebookutils), named notebook runs, Livy-session ad-hoc calculations, Spark failure triage, and the whole Materialized Lake View lifecycle -- definition, incremental-refresh readiness review, schedules, refresh jobs, run history and refresh-failure diagnosis. KQL materialized views are eventhouse-cli. Triggers:write notebook code,run notebook,notebookutils,create a Livy session,failed notebook,Spark OOM,create materialized lake view,schedule MLV,diagnose MLV refresh failure"
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: spark-cli` (`az rest`: `--headers "x-ms-fabric-skill=spark-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering
> 3. **Skill disambiguation**: use `spark-cli` for notebook cell code (including `%%sql` cells), named notebook runs, Livy sessions, Spark failure triage, and everything about a Materialized Lake View -- writing the definition, reviewing a query for incremental-refresh readiness, and scheduling, refreshing, monitoring or diagnosing an existing one. A KQL materialized view in an Eventhouse is `eventhouse-cli`; plain read-only T-SQL against a Warehouse or Lakehouse SQL endpoint is `sqldw-cli`.
> 4. **Hard routing boundary**: never execute an Eventhouse/KQL materialized-view request from this skill. Route it to `eventhouse-cli`; if that skill is unavailable, state that the request cannot be completed in the current skill context and stop without calling Fabric APIs or creating artifacts.

# Fabric Spark and Materialized Lake Views -- CLI Skill

This one skill owns Fabric Spark: notebook cell authoring, notebook runs, Livy-session analysis, Spark failure diagnostics, and the whole Materialized Lake View lifecycle.

It is a **mode dispatcher** and contains NO procedures. Pick the mode that matches the request from the table below, then **read the matching `references/<mode>.md` file end to end with your file-reading tool BEFORE issuing a single command**. That file holds the endpoints, payload shapes, templates and gotchas; acting without it produces wrong payloads and wrong results.

## Mode selection

| Mode | Use when the request ... | Example triggers | Read this first |
|---|---|---|---|
| `authoring` | writes notebook cell code (PySpark, Scala, SparkR, `%%sql`, `%%configure`), runs a notebook by name and reports a NORMAL run status, or authors a Materialized Lake View definition or reviews an MLV query for incremental-refresh readiness | write notebook code, notebook cell code, %%sql cell, run notebook, execute notebook, notebookutils, create materialized lake view, is this MLV query incremental-refresh ready | [references/authoring.md](references/authoring.md) |
| `consumption` | runs interactive ad-hoc PySpark in a Lakehouse Livy session -- never a notebook | create a Livy session, run calculation in Livy, PySpark, DataFrame analysis, join tables across lakehouses, Delta time-travel | [references/consumption.md](references/consumption.md) |
| `operations` | diagnoses a FAILED, unhealthy, throttled or slow Spark notebook / pipeline / Livy run | failed notebook, Spark Livy health, Spark OOM, why is my notebook slow, job diagnostics, 430 throttling | [references/operations.md](references/operations.md) |
| `mlv` | discovers or operates EXISTING Materialized Lake Views: Spark SQL discovery, refresh schedules, on-demand refresh, run history, cancellation, and refresh-failure classification | discover MLVs, list materialized lake views, schedule MLV, MLV run history, cancel refresh, trigger MLV refresh, diagnose MLV refresh failure | [references/mlv.md](references/mlv.md) |

### Mode boundary rule

Mode is decided by the artefact and the outcome, not by the language. A notebook cell is always `authoring` even when the cell is `%%sql`. A Livy session is always `consumption`. A Spark run that FAILED or is unhealthy is `operations`; a run that succeeded is reported by `authoring`. For a Materialized Lake View the VERB decides: writing or reviewing the definition is `authoring`, while discovering, scheduling, refreshing, monitoring or diagnosing existing MLVs is `mlv`. If discovery must be executed, switch to `consumption` for Livy or `authoring` for a notebook only after reading the discovery command from `references/mlv.md`.

If a request genuinely spans modes, handle them one at a time and read each reference before you start that part. If the mode is ambiguous after reading this table, ask one short clarifying question instead of guessing.

## Terminal write -- the step you must not skip

Reading the reference and planning the change is NOT completing the task. Each mutating mode ends with one state-changing call. If you did not issue it, nothing was persisted -- say so explicitly rather than reporting success.

| Mode | Terminal write |
|---|---|
| `authoring` | for an EXISTING notebook, `POST .../notebooks/{id}/updateDefinition` to save the cell; a NEW notebook needs `POST /v1/workspaces/{ws}/items` first; for a run request, trigger the job via the Jobs API. Printing cell code into the chat is not saving or running it. |
| `consumption` | none -- this mode is read-only |
| `operations` | none -- this mode is read-only |
| `mlv` | `POST /v1/workspaces/{ws}/lakehouses/{lakehouse}/jobs/refreshMaterializedLakeViews/instances` for an on-demand refresh, or the schedule create/update/delete call for a scheduling request. Reporting what the schedule would be is not creating it. |

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
- Treat vague requests such as "set up my data" as insufficiently scoped. Ask what artefact, source, destination, and outcome the user wants; never infer intent by finding and running an existing notebook or job.
- Read `references/<mode>.md` end to end, as your FIRST tool call, before the first command of that mode. Read it ONCE, in a single full read: do not re-open it, do not grep it again, and do not page through it. You already have it.
- Apply the same read-once discipline to every other file you load, including nested `references/<mode>/*.md` sub-references and shared `common/*.md` files: open only the ones you actually need, read each ONCE end to end, and never grep or re-open one you already loaded.
- Resolve workspace and item ids by listing and filtering, never by guessing a GUID.
- Stop after routing any Eventhouse/KQL materialized-view request. Unavailable sibling skills are a blocking boundary, not permission to implement their workload directly.
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
- Attempting an out-of-scope request through raw REST calls when the owning skill is unavailable. Name the owning skill and stop; do not improvise by creating Fabric artefacts outside `spark-cli`'s scope.

## Examples

| User request | Mode | Reference to read |
|---|---|---|
| "Write a notebook cell that reads the bronze table and writes a silver Delta table." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Create a Livy session and count the distinct customers in the lakehouse." | `consumption` | [references/consumption.md](references/consumption.md) |
| "My notebook run failed with an OOM -- work out why." | `operations` | [references/operations.md](references/operations.md) |
| "Is this materialized lake view query ready for incremental refresh?" | `authoring` | [references/authoring.md](references/authoring.md) |
| "Show me the Spark SQL command that lists the MLVs in schema silver." | `mlv` | [references/mlv.md](references/mlv.md) |
| "Schedule a nightly refresh for the lakehouse MLV lineage and show me its run history." | `mlv` | [references/mlv.md](references/mlv.md) |

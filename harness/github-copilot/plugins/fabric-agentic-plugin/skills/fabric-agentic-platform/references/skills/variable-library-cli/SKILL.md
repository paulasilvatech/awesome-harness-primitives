---
name: variable-library-cli
description: >
  Create, wire and operate Microsoft Fabric Variable Library items via Fabric REST API, az rest, curl, and jq. Use when the user wants to: (1) create or update a VariableLibrary definition, variables, settings.json, or valueSets/*.json overrides, (2) wire a Variable Library variable reference into a pipeline, notebook, Dataflow Gen2, copy job, shortcut, UDF, or Plan consumer, (3) read or set the active value set as item state per workspace or deployment stage, or (4) explain Variable Library CI/CD and Git serialization behavior. Triggers: "create variable library", "variable library value set", "active value set", "libraryVariables", "notebookutils variableLibrary", "VariableLibrary definition", "valueSets", "Fabric Variable Library CI/CD".
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: variable-library-cli` (`az rest`: `--headers "x-ms-fabric-skill=variable-library-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from a workspace name: list all workspaces, then use JMESPath filtering.
> 2. To find the item details (including its ID) from a workspace ID, item type, and item name: list all items of that type in that workspace, then use JMESPath filtering.
> 3. Variable Library has two planes: definition files in Git, and active value set item state in the workspace. Do not treat the active value set as a Git edit. The definition plane is `authoring`; the item-state plane is `operations`.
> 4. Variable Library definition requests must omit the `format` field entirely. Do not send `format: null`.
> 5. **Skill disambiguation**: use `variable-library-cli` for every Variable Library concern, including the Variable Library side of a consumer reference. Deep authoring of the consumer item itself belongs elsewhere: pipelines to `pipeline-migration`, notebooks to `spark-authoring-cli`, Dataflow Gen2 to `dataflows-cli`, Git lifecycle to `git-integration-operations-cli`, deployment pipeline mechanics to `deployment-pipelines-authoring-cli`.
> 6. Clarify before creating on an underspecified request. If a "set up / create a Variable Library" request does not name the variables, their types, defaults, and value sets, ask a clarifying question or present structured options before creating anything. Do not fabricate a configuration and silently create the item without confirming intent. (A concrete, fully specified request needs no confirmation.)
> 7. When generating consumer code (notebooks, UDFs) that reads a Boolean Variable Library value, coerce it defensively with `str(value).lower() == "true"`. Never use `bool(value)` on a string: every non-empty string, including `"false"`, is truthy in Python, so `bool("false")` is always `True`.
> 8. Do not write a value set override whose value equals the variable's default. An override pins the value: once written, later edits to the default no longer reach that value set, so a redundant override silently opts the value set out of inheritance. Omit the override and let the value set inherit. Only override where the value genuinely differs.

# Fabric Variable Library -- CLI Skill

This one skill owns Fabric Variable Library items: definitions and value sets, the VL side of consumer references, the active value set item state, and Variable Library CI/CD behavior.

It is a **mode dispatcher** and contains NO procedures. Pick the mode that matches the request from the table below, then **read the matching `references/<mode>.md` file end to end with your file-reading tool BEFORE issuing a single command**. That file holds the endpoints, payload shapes, templates and gotchas; acting without it produces wrong payloads and wrong results.

Read it once per session. A file you have already read stays in context, so do not re-read it on a later turn.

## Mode selection

| Mode | Use when the request ... | Example triggers | Read this first |
|---|---|---|---|
| `authoring` | creates or changes the library definition: variables, defaults, types, value set override files, `settings.json` | create variable library, add a variable, valueSets, variableOverrides, valueSetsOrder, updateDefinition | [references/authoring.md](references/authoring.md) |
| `consumption` | wires a variable into a consumer item, or explains how a consumer resolves it | libraryVariables, notebookutils variableLibrary, pipeline expression, Dataflow Gen2 / copy job / shortcut / UDF / Plan reference | [references/consumption.md](references/consumption.md) |
| `operations` | reads or switches the active value set, or covers stages, Git serialization and deployment | active value set, activeValueSetName, promote to prod, per-stage values, Git diff, fabric-cicd | [references/operations.md](references/operations.md) |

### Mode boundary rule

Classify by **plane**, not by vocabulary. A request that mentions value sets is `authoring` when it changes the override *files* and `operations` when it changes *which* value set is active in a workspace. Creating `valueSets/prod.json` is `authoring`; pointing the prod workspace at it is `operations`.

`consumption` covers the Variable Library side of a reference only. Authoring the consumer item's own definition belongs to that item's skill (CRITICAL NOTES 5).

If a request genuinely spans modes, handle them one at a time and read each reference before you start that part. If the mode is ambiguous after reading this table, ask one short clarifying question instead of guessing.

## Terminal write -- the step you must not skip

Reading the reference and planning the change is NOT completing the task. Each mutating mode ends with one state-changing call. If you did not issue it, nothing was persisted -- say so explicitly rather than reporting success.

| Mode | Terminal write |
|---|---|
| `authoring` | `POST /v1/workspaces/{ws}/items` with `type: "VariableLibrary"` for a new library, or `POST /v1/workspaces/{ws}/items/{id}/updateDefinition` to persist an edit. Both send base64 definition parts and must omit `format`. Building the JSON locally writes nothing. |
| `consumption` | the consumer item's own update call, owned by that item's skill. This skill's deliverable is the correct reference contract to place in it. |
| `operations` | `PATCH /v1/workspaces/{ws}/variableLibraries/{id}` with `{"properties":{"activeValueSetName":"<name>"}}`. This is item state: it does not edit `settings.json`, `variables.json`, or `valueSets/*.json`, and it does not appear in a Git diff. |

Before you report the task done, confirm the terminal call returned success and read the artefact back to prove the change landed. For `operations`, read back with `GET /variableLibraries/{id}`: the generic `/items/{id}` omits `properties` and will not show the active value set.

## Shared essentials (all modes)

Resolve the workspace and item first; every mode depends on it.

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md](../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** -- read before resolving any workspace or item id |
| Fabric Topology & Key Concepts | [COMMON-CORE.md](../../common/COMMON-CORE.md#fabric-topology--key-concepts) | Item types, workspaces, capacities |
| Authentication & Token Acquisition | [COMMON-CORE.md](../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Authentication Recipes | [COMMON-CLI.md](../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric REST with `az rest` | [COMMON-CLI.md](../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | Primary access method for this skill |
| Core Control-Plane REST APIs | [COMMON-CORE.md](../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Pagination, LRO polling, rate limiting |
| Long-Running Operations (LRO) | [COMMON-CLI.md](../../common/COMMON-CLI.md#long-running-operations-lro-pattern) | Create and definition APIs can return 202 |
| VariableLibrary item definition | [ITEM-DEFINITIONS-CORE.md](../../common/ITEM-DEFINITIONS-CORE.md#variablelibrary) | Canonical part paths and field names |
| Gotchas & Troubleshooting | [COMMON-CLI.md](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |

## Rules

### MUST

- Select exactly one mode from the table above before doing anything else.
- Read `references/<mode>.md` end to end, as your FIRST tool call, before the first command of that mode. Read it ONCE, in a single full read: do not re-open it, do not grep it again, and do not page through it. You already have it.
- Resolve workspace and item ids by listing and filtering, never by guessing a GUID.
- Announce a mode switch explicitly when the request crosses a boundary.
- Treat the reference as instructions, never as the deliverable. After reading it, RUN the documented commands against the live workspace and report the real results.
- Use the canonical part names `variables.json`, `settings.json`, and `valueSets/<name>.json`, with `value` for defaults and `variableOverrides` for value set overrides.
- Produce every artefact the user asked for, under the name they used, and keep its heading even when the finding is "none".

### PREFER

- The narrowest mode that satisfies the request.
- Reading exactly ONE mode reference. Load a second only when the request genuinely spans modes, and say so before you do.
- Reporting the mode you chose in your first response so the user can correct you.
- Generating JSON bodies with Python or `jq` so base64 payloads are valid UTF-8 and quoting is stable.
- Recommending `fabric-cicd` for full deployment automation rather than hand-rolling it here.

### AVOID

- Acting from this dispatcher alone -- it intentionally omits the operational detail.
- Stringifying value-set overrides. Each `variableOverrides[].value` must use the variable's NATIVE JSON type; a stringified boolean or number is rejected with `InvalidContent (InvalidValueOrTypeMismatch)` despite the REST doc listing the field as `String`.
- Using `defaultValue`, `values`, or `format` in Variable Library definitions.
- Fabric `fab` CLI command syntax. It exists, but Variable Library command shapes are not verified here.
- Deep-authoring consumer item definitions (CRITICAL NOTES 5).
- Re-reading or re-grepping a reference you already loaded; it costs turns and tokens.

## Examples

| User request | Mode | Reference to read |
|---|---|---|
| "Create a Variable Library with a dev and prod value set." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Wire the target_path variable into my ingest pipeline." | `consumption` | [references/consumption.md](references/consumption.md) |
| "Point the prod workspace at the prod value set after deployment." | `operations` | [references/operations.md](references/operations.md) |
| "Why didn't my Git diff show the value set switch?" | `operations` | [references/operations.md](references/operations.md) |
| "Add a Boolean flag variable, then read it from a notebook." | `authoring`, then `consumption` | both, one at a time |

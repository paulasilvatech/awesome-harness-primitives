<!-- Mode reference for the `dataflows-cli` skill. Loaded on demand from `skills/dataflows-cli/SKILL.md` when the request matches the `authoring` mode. -->

> **PRE-MUTATION REQUIREMENTS GATE (mandatory)**
> Before any mutation, confirm enough user intent for the requested operation.
> For create or update requests, establish the source, query/schema and
> transformation, destination behavior, and refresh behavior (including an
> explicit choice of no destination or no refresh). If the request is generic,
> such as "set up the Dataflow I need for reporting," ask a structured
> clarifying question and stop before mutation. Do not infer requirements from
> unrelated workspace items or create a best-guess source, connection, or
> Dataflow.

# dataflows-cli authoring mode — Dataflows Gen2 Authoring via CLI

## Table of Contents

**This skill (`SKILL.md`)**

| Section | Notes |
|---|---|
| [Tool Stack](#tool-stack) | `az` + `jq` + `base64` + `curl` |
| [Connection](#connection) | Workspace/dataflow ID discovery |
| [Agentic Workflows](#agentic-workflows) | **Start here.** A: create end-to-end; B: modify existing; C: preview loop |
| [MUST DO / AVOID / PREFER](#must-do) | Authoring rules |
| [Troubleshooting](#troubleshooting) | Symptom → fix table |
| [Examples](#examples) | Runnable bash + PowerShell recipes |
| [Output Expectations](#output-expectations) | Response conventions |

**References** (in [`references/`](authoring/))

| File | When to read |
|---|---|
| [authoring-cli-quickref.md](authoring/authoring-cli-quickref.md) | One-liner recipes, status enums, base64 helpers, connection-binding quick patterns |
| [authoring-script-templates.md](authoring/authoring-script-templates.md) | Full bash + PowerShell templates; end-to-end smoke test; LRO polling pattern |
| [connection-management.md](authoring/connection-management.md) | List/create/inspect connections; `supportedConnectionTypes`; resolve `ClusterId`; ID format cheat sheet |
| [connectors.md](authoring/connectors.md) | M-side source connectors: live-verified function inventory, Lakehouse deep navigation, gateway scope for `Web.Page` / `Web.BrowserContents`, and `Html.Table` / `Csv.Document` / `Json.Document` patterns |
| [m-language.md](authoring/m-language.md) | M language semantics for Dataflow Gen2: `try` record shapes, per-cell error wrapping in column transforms, `each` scoping in row vs sub-table contexts, optional field access `[?]` / `Record.FieldOrDefault`, quoted identifiers, sandbox-disabled symbols (`File.Contents`) |
| [mashup-preview.md](authoring/mashup-preview.md) | `executeQuery` contract: bootstrap branch, auto-wrap rule, hard avoid for unbounded preview |
| [output-destinations.md](authoring/output-destinations.md) | Output destination patterns: Lakehouse Table, Lakehouse Files, Warehouse, ADX, Azure SQL. `DataDestinations` annotation, hidden query, `loadEnabled` rules, connection limitations |

**Common refs** (in [`../../common/`](../../../common/))

| File | When to read |
|---|---|
| [COMMON-CLI.md](../../../common/COMMON-CLI.md) | `az login`, token acquisition, `az rest`, pagination, LRO polling, CLI gotchas. **§ Finding Workspaces and Items in Fabric is mandatory.** |
| [COMMON-CORE.md](../../../common/COMMON-CORE.md) | Fabric topology, environment URLs, authentication, core REST API surface |
| [ITEM-DEFINITIONS-CORE.md](../../../common/ITEM-DEFINITIONS-CORE.md) | Definition envelope; per-item-type payload contracts |
| [DATAFLOWS-AUTHORING-CORE.md](../../../common/DATAFLOWS-AUTHORING-CORE.md) | Authoring capability matrix; 3-part definition structure; M structure; connection model; ALM / Git integration |

**Sister skills**

| Skill | Use for |
|---|---|
| [dataflows-cli consumption mode](consumption.md) | Execute persisted queries; ad-hoc read-only `customMashupDocument` with no intent to persist; Arrow → CSV/pandas conversion; refresh status/history. |

---

## Tool Stack

| Tool | Role | Install |
|---|---|---|
| `az` CLI | **Primary**: Auth (`az login`), REST API calls (`az rest`), token acquisition. | Pre-installed in most dev environments |
| `jq` | Parse and manipulate JSON responses and definition payloads. | Pre-installed or trivial |
| `base64` | Encode/decode definition parts for the REST API. | Built into bash / `[Convert]::ToBase64String()` in PowerShell |
| `curl` | Alternative to `az rest` when raw HTTP control is needed. | Pre-installed |
| `uuidgen` | Generate per-query / per-platform GUIDs for `queryId` and `logicalId` when building a new dataflow definition (Workflow A). | Pre-installed on Linux/macOS; on Windows use PowerShell `[guid]::NewGuid().Guid` or run via WSL |

> **Agent check** — verify `az`, `jq`, and `curl` are available before first operation. `uuidgen` is only needed for Workflow A (Create).
> For installation and auth setup see [COMMON-CLI.md](../../../common/COMMON-CLI.md).

---

## Connection

### Discover Workspace and Dataflow IDs

Per [COMMON-CLI.md](../../../common/COMMON-CLI.md) Finding Workspaces and Items in Fabric:

```bash
# List workspaces — find workspace ID by name
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces" \
  --query "value[?displayName=='MyWorkspace'].id" --output tsv

# List dataflows in workspace — find dataflow ID by name
WS_ID="<workspaceId>"
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/dataflows" \
  --query "value[?displayName=='MyDataflow'].id" --output tsv
```

### Reusable Connection Variables

```bash
WS_ID="<workspaceId>"
DF_ID="<dataflowId>"
API="https://api.fabric.microsoft.com/v1"
RESOURCE="https://api.fabric.microsoft.com"
```

---

## Agentic Workflows

Three workflows cover the typical authoring tasks:

- **[A. Create a New Dataflow End-to-End](#a-create-a-new-dataflow-end-to-end)** — discover/create a connection, create the dataflow, save M + bindings, validate, optionally refresh.
- **[B. Modify an Existing Dataflow](#b-modify-an-existing-dataflow)** — read-modify-write the definition; the canonical Discover → Formulate → Execute → Verify loop.
- **[C. Preview-Driven Authoring Loop](#c-preview-driven-authoring-loop)** — iterate on candidate M via `executeQuery` before persisting via `updateDefinition`.
- **[D. Output Destination](#d-output-destination)** — write query results to Lakehouse (table/files), Warehouse, ADX, or Azure SQL via `DataDestinations` annotation. Full reference: [output-destinations.md](authoring/output-destinations.md).

### A. Create a New Dataflow End-to-End

Use this when **the dataflow does not yet exist**. Covers the full happy path: discover-or-create a connection, create the dataflow shell, save M + bindings in one `updateDefinition`, validate, optionally refresh.

**Steps:**

1. **List existing connections** and filter by `connectionDetails.type` and the target URL/host — reuse if a match exists (`GET /v1/connections` + JMESPath).
2. **If no match, create the connection.** First `GET /v1/connections/supportedConnectionTypes` to discover required parameters and supported credential types, then `POST /v1/connections` (sync 201). Body shape and credential schemas: [connection-management.md](authoring/connection-management.md).
3. **Resolve `ClusterId` for the composite binding.** `GET https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources` with `--query "value[?id=='$CONN_ID'] | [0].clusterId"`, audience `--resource "https://analysis.windows.net/powerbi/api"` (no trailing slash). The per-id route returns `PowerBIEntityNotFound` for cloud connections. Newly-created connections may take a few seconds to surface — retry on empty. Detail: [connection-management.md § Resolving ClusterId](authoring/connection-management.md#resolving-clusterid-power-bi-v2).
4. **Create the dataflow shell.** `POST /v1/workspaces/{ws}/dataflows` with `{"displayName":"<displayName>"}` returns sync 201. The `definition` field is optional at create time and can be set in the next step. If you instead supply the full `definition` (all three parts) in this create POST, that call is the persist surface -- name `POST /v1/workspaces/{ws}/dataflows` (not `updateDefinition`) as the persist path in your summary.
5. **Save M + connection bindings in one call.** `POST /v1/workspaces/{ws}/dataflows/{df}/updateDefinition?updateMetadata=true` with three parts: `mashup.pq` (real `Web.Contents` / `Sql.Database` / …), `queryMetadata.json` (with `connections[]` populated; each `connectionId` is the stringified composite `{"ClusterId":"…","DatasourceId":"…"}`), and `.platform`. Typically returns sync 200; may return 202 + LRO `Location` on large bodies — handle both.
6. **Verify the binding persisted.** Re-call `getDefinition`, decode `queryMetadata.json`, and confirm `connections[]` is intact. **Do not** use `GET /items/{id}/connections` for verification — that endpoint reflects refresh-materialized state, not the persisted definition, and returns 0 even after a successful bind. See [AVOID](#avoid).
   **Guarded preview-only fallback:** If connection binding cannot proceed because Power BI v2 `gatewayClusterDatasources` returns 401/403/Unauthorized or no `ClusterId` is visible after retries, do not stop before creating the dataflow. Create the shell, persist the saved query definitions without claiming a valid source binding, call `executeQuery` with `QueryName` only for each saved query, surface the exact credential or binding error from the Arrow stream, do not fabricate chart data, and do not refresh.
7. **(Encouraged) Offer to preview output as ASCII charts.** Ask the user: *"Would you like me to preview the data as charts before the first refresh?"*. In this create flow the definition is already saved in step 5, so the chart preview here is a **post-save validation gate before you materialize via refresh** — not a pre-save step. (If instead you want to validate *candidate* M **before** the first `updateDefinition` — e.g. iterating on the M, or bootstrap-binding a credentialed source so `executeQuery` can see it — use the pre-persist [Preview-Driven Authoring Loop](#c-preview-driven-authoring-loop); the chart rendering is identical, only the ordering relative to the save differs.) If accepted, call `executeQuery` for each entity, parse the Arrow IPC stream, render line charts (time-series) or horizontal bar charts (categories) via `references/authoring/charts/line_chart.py` / `references/authoring/charts/bar_chart.py`, and ask the user to confirm before proceeding. Details: [mashup-preview.md § ASCII chart preview](authoring/mashup-preview.md#ascii-chart-preview-optional). If declined, proceed directly to step 8.
8. **(Optional) Trigger refresh** to materialize. `POST .../jobs/instances?jobType=Refresh` with body `{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}`. **`ApplyChangesIfNeeded` is required on the first refresh after any definition change** — without it, Fabric refreshes the previously-applied definition. Poll the LRO until `status` is `Completed` (refresh enum) or `Failed`/`Cancelled`.

```bash
# Concise skeleton — full runnable bash is Example 1 below.
# PowerShell + LRO-polled variants: references/authoring-script-templates.md

WS_ID="<workspaceId>"; URL="<source-url>"
RES="https://api.fabric.microsoft.com"; API="$RES/v1"
PBI="https://analysis.windows.net/powerbi/api"

# 1. List existing & try reuse
CONN_ID=$(az rest --method get --resource "$RES" --url "$API/connections" \
  --query "value[?connectionDetails.type=='Web' && connectionDetails.path=='$URL'] | [0].id" -o tsv)

# 2. Create connection if missing — see connection-management.md for full body
# 3. List+filter for ClusterId
CLUSTER_ID=$(az rest --method get --resource "$PBI" \
  --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" \
  --query "value[?id=='$CONN_ID'] | [0].clusterId" -o tsv)

# 4. Empty dataflow shell — sync 201
SHELL_BODY=$(mktemp --suffix=.json 2>/dev/null || mktemp)
printf '{"displayName":"my-df"}' > "$SHELL_BODY"
DF_ID=$(az rest --method post --resource "$RES" \
  --url "$API/workspaces/$WS_ID/dataflows" \
  --headers "Content-Type=application/json" \
  --body "@$SHELL_BODY" --query id -o tsv)
rm -f "$SHELL_BODY"

# 5. One-shot updateDefinition with real M + connections[] (sync 200 typical)
#    Body assembly (mashup.pq + queryMetadata.json + .platform, base64-encoded;
#    queryMetadata.json.connections[].connectionId = composite ClusterId/DatasourceId):
#    see Example 1 below.

# 6. Verify via getDefinition (NOT GET /items/{id}/connections — see AVOID)
# 7. (optional) executeQuery — Workflow C
# 8. (optional) Refresh with executeOption=ApplyChangesIfNeeded — Example 2
```

> **One-shot vs two-step bind+save.** Steps 4-5 can be one call (default; saves an HTTP round trip) or split into a bootstrap-bind `updateDefinition` followed by a full-M `updateDefinition`. Both work — see [PREFER](#prefer).

### B. Modify an Existing Dataflow

Use this when the dataflow already exists. Canonical Discover → Formulate → Execute → Verify loop. If the dataflow does not yet exist, see [Workflow A](#a-create-a-new-dataflow-end-to-end) instead.

1. **Discover** — list workspaces, list dataflows, `getDefinition` (decode `mashup.pq` and `queryMetadata.json`). Validate all `connections[]` entries via `GET /v1/connections/{id}`.
2. **Formulate** — modify M, re-encode parts, ensure every referenced `connectionId` exists in the caller's connection store.
3. **Execute** — `POST .../updateDefinition?updateMetadata=true` with **all 3 parts** (full replacement). Optionally trigger refresh.
4. **Verify** — re-call `getDefinition` to confirm changes; poll refresh LRO; for refresh failures, make at most **one** `executeQuery` isolation attempt to localize a fixable M/source issue. On a terminal/non-retriable failure (`isRetriable: false`, workspace-wide `UnknownException`), surface the raw error and **stop** rather than re-triggering.

```bash
# Concise skeleton — full templates: references/authoring-script-templates.md
# Acquire $TOKEN per common/COMMON-CLI.md § Token-in-Variable Pattern (resource = $RESOURCE).
RESOURCE="https://api.fabric.microsoft.com"; API="$RESOURCE/v1"

# 1. Discover — getDefinition (handles 200 sync and 202 + LRO via curl)
HDR=$(mktemp); BODY=$(mktemp)
CODE=$(curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  -D "$HDR" -o "$BODY" -w "%{http_code}")
if [ "$CODE" = "202" ]; then
  LOC=$(tr -d '\r' < "$HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOC")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) RESULT=$(az rest --method get --resource "$RESOURCE" --url "${LOC%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; exit 1 ;;
    esac
  done
else
  RESULT=$(cat "$BODY")
fi
rm -f "$HDR" "$BODY"

# Validate bound connections (connectionId is a composite JSON string — iterate safely)
QUERY_META=$(echo "$RESULT" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d)
echo "$QUERY_META" | jq -c '.connections[]?' | while IFS= read -r conn; do
  RAW=$(echo "$conn" | jq -r '.connectionId')
  DATASOURCE_ID=$(echo "$RAW" | jq -r '.DatasourceId? // empty' 2>/dev/null)
  [ -z "$DATASOURCE_ID" ] && DATASOURCE_ID="$RAW"
  # GET /v1/connections/$DATASOURCE_ID to confirm access
done

# 2-3. Formulate & Execute — see Example 3
# 4. Verify — trigger refresh via curl (az rest cannot capture Location header).
#    Full LRO polling: references/authoring-script-templates.md.
```

### C. Preview-Driven Authoring Loop (pre-save executeQuery — see [mashup-preview.md](authoring/mashup-preview.md#preview-driven-authoring-loop))

When the change touches Power Query M (new query, edited mashup, new source, changed parameters), preview the candidate `customMashupDocument` against the dataflow's bound connections **before** persisting. Catches syntax, schema, and credential errors at authoring time. Full ordered steps, bootstrap branch, auto-wrap rule, hard-avoid for unbounded preview, ASCII chart preview, and Apache Arrow handling: [mashup-preview.md § Preview-Driven Authoring Loop](authoring/mashup-preview.md#preview-driven-authoring-loop).

> **Intent split.** This workflow is for the *pre-save* intent. To execute a **saved** query (`QueryName` only) or run an **ad-hoc read-only** `customMashupDocument` with no intent to persist, use [`dataflows-cli consumption mode`](consumption.md#query-evaluation). `mashup-preview.md` is the shared API reference for both intents.

Skip the preview only for metadata-only edits (display name, schedule, `loadEnabled` toggle) or when the agent records an explicit skip reason (bootstrap, prohibitive cost, side-effecting source).

### D. Output Destination

Use this when the dataflow should **write query results to an external store** (Lakehouse table, Lakehouse files, Warehouse, ADX, Azure SQL). Extends Workflow A with `DataDestinations` annotations and a hidden destination query. Full reference with complete examples: [output-destinations.md](authoring/output-destinations.md).

**Key requirements:**

1. **Source query** carries a `[DataDestinations = {[...]}]` annotation referencing the destination query by name.
2. **Hidden destination query** (suffixed `_DataDestination`) navigates to the target storage using null-safe `?[Data]?` (tables) or `?[Content]?` (files) operators.
3. **queryMetadata.json** must set `"loadEnabled": false` on the destination query — refresh fails without it. State this in your summary using the literal part name (e.g., "set `loadEnabled: false` on the destination query in `queryMetadata.json`").
4. **Always use `IsNewTarget = true`** for API-created dataflows, even for existing tables.
5. **Bind the appropriate connection** (Lakehouse: kind `"Lakehouse"`; Warehouse: kind `"Warehouse"`; ADX: kind `"AzureDataExplorer"`; Azure SQL: kind `"Sql"`) with composite `ClusterId`/`DatasourceId` ID.
6. **First refresh must use `ApplyChangesIfNeeded`** to publish the draft and reconcile annotations.
7. **All source columns must be typed** — `Any`-type columns are rejected by all destination types.
8. **Name the definition parts in your written summary.** Because the CLI transcript truncates long command bodies, the final summary (prose, not just shell commands) MUST name the three definition parts by their literal paths — `mashup.pq`, `queryMetadata.json`, and `.platform` — so the part names survive in the answer (e.g., "Saved `mashup.pq` + `queryMetadata.json` + `.platform` via `updateDefinition`"). Do not abbreviate `queryMetadata.json` to "query metadata" or the inner field `queriesMetadata`.

**Supported destinations:**

| Destination | Connection Kind | Destination Query Function | Notes |
|---|---|---|---|
| Lakehouse Table | `Lakehouse` | `Lakehouse.Contents(...)` | Path: `"Lakehouse"` |
| Lakehouse Files | `Lakehouse` | `Lakehouse.Contents(...)` | `TypeSettings = [Kind = "File"]`, `?[Content]?` |
| Warehouse | `Warehouse` | `Fabric.Warehouse(...)` | Path: `"Warehouse"`, Schema/Item navigation |
| Azure Data Explorer | `AzureDataExplorer` | `AzureDataExplorer.Contents(...)` | Path must match connection exactly (trailing slash!) |
| Azure SQL | `Sql` | `Sql.Database(...)` | Path: `"server;database"` |

**Minimal steps:** Create dataflow → Find/create connection → Resolve ClusterId → Save definition with OD annotations → Verify → Refresh.

```bash
# Skeleton — full PowerShell recipe: references/output-destinations.md § Complete Example
WS_ID="<workspaceId>"; LH_ID="<lakehouseId>"; RES="https://api.fabric.microsoft.com"

# M pattern (two queries):
# 1. Source with [DataDestinations] annotation
# 2. Hidden _DataDestination query with ?[Data]? null-safe navigation
# queryMetadata: source loadEnabled=true, destination loadEnabled=false + isHidden=true
# Refresh: {"executionData":{"executeOption":"ApplyChangesIfNeeded"}}
```

---

## Gotchas, Rules, Troubleshooting

For full authoring gotchas: [DATAFLOWS-AUTHORING-CORE.md](../../../common/DATAFLOWS-AUTHORING-CORE.md) Gotchas and Troubleshooting.
For CLI-specific issues: [COMMON-CLI.md](../../../common/COMMON-CLI.md) Gotchas & Troubleshooting (CLI-Specific).
For connection discovery: [authoring-cli-quickref.md § Connection Discovery and Validation](authoring/authoring-cli-quickref.md#connection-discovery-and-validation).

### MUST DO

- **Offer to preview every entity before the first refresh of a new dataflow** — after creating the shell and binding connections via `updateDefinition` (which persists the definition), ask the user if they want to see preview charts before materializing via refresh. In the [preview-driven loop](#c-preview-driven-authoring-loop) the preview instead precedes the persisting `updateDefinition`. If accepted, follow [mashup-preview.md § ASCII chart preview](authoring/mashup-preview.md#ascii-chart-preview-optional). Skip only for metadata-only edits (display name, schedule) or when the agent records an explicit skip reason.
- **`az login` first** — all `az rest` calls use the active session. No session → 401.
- **Use `--resource "https://api.fabric.microsoft.com"` for Fabric APIs.** For Power BI v2 (`gatewayClusterDatasources`), use `--resource "https://analysis.windows.net/powerbi/api"` **without a trailing slash** — the slashed form fails `AADSTS500011 invalid_resource`.
- **Base64-encode all 3 definition parts** — `mashup.pq` + `queryMetadata.json` + `.platform`, each `payloadType: "InlineBase64"`. `updateDefinition` is a full replacement; sending 1 or 2 parts silently drops queries.
- **Handle sync AND async responses.** `POST /dataflows`, `updateDefinition`, and `getDefinition` typically return sync (200/201) but may return 202 + LRO `Location` on large bodies — handle both. See [authoring-script-templates.md § Fabric LRO Polling Pattern](authoring/authoring-script-templates.md#fabric-lro-polling-pattern).
- **Set `formatVersion: "202502"`** in `queryMetadata.json` and include a top-level `name` matching `displayName` — omitting either causes save-time failures or stale display-name state.
- **`loadEnabled` is opt-out, not opt-in.** Fabric auto-loads every query to the staging Lakehouse by default; set `loadEnabled: false` only on helper queries you do not want written. Note: `loadEnabled: true` is also stripped from `queryMetadata.json` on round-trip via `getDefinition` (it's the default) — its absence on read-back is **not** a bug. Detail: [DATAFLOWS-AUTHORING-CORE.md § loadEnabled semantics](../../../common/DATAFLOWS-AUTHORING-CORE.md).
- **Use the right ID format per context.** REST `/v1/connections` operations take the **plain GUID** from `connection.id`; `queryMetadata.json connections[].connectionId` takes the **stringified composite** `{"ClusterId":"…","DatasourceId":"…"}`. See [connection-management.md § Connection ID Format Cheat Sheet](authoring/connection-management.md#connection-id-format-cheat-sheet).
- **Resolve `ClusterId` via list+filter.** `GET .../gatewayClusterDatasources` filtered by `value[?id=='$CONN_ID']`. The per-id route returns `PowerBIEntityNotFound` for cloud connections; newly-created connections may need a 5-15 s retry. See [connection-management.md § Resolving ClusterId](authoring/connection-management.md#resolving-clusterid-power-bi-v2).
- **`executeQuery` body uses a top-level `QueryName` field** (PascalCase canonical; the field name itself is case-insensitive on the wire — lowercase `queryName` also evaluates). Value must name a `shared` member from the persisted M or the supplied `customMashupDocument`. The `{"queries":[…]}` array shape **always** fails with `DataflowExecuteQueryError: Invalid query name`; a wrong query name returns `QueryNotFound`. Full contract: [mashup-preview.md § Request body](authoring/mashup-preview.md).
- **Use the exact, case-sensitive API names.** The endpoint is `executeQuery` (singular, never `executeQueries`) and the request-body field is `customMashupDocument` (never `mashupDocument`, never base64-encoded — it is a plain UTF-8 M string). The same M body becomes the saved `mashup.pq` part referenced as `customMashupDocument`. Vocabulary table: [mashup-preview.md § Vocabulary](authoring/mashup-preview.md#vocabulary----name-the-things-you-send).
- **First refresh after any `updateDefinition` MUST use `executeOption: "ApplyChangesIfNeeded"`.** Body: `{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}`. Without it, Fabric refreshes the previously-applied definition.
- **Treat a terminal refresh failure as a stop condition — do not debug-loop.** When a refresh/LRO job reaches terminal `Failed`/`Cancelled`, or a backend error carries `isRetriable: false` (or a workspace-wide `UnknownException`), report the raw error verbatim and **stop**. These are backend/infra outcomes the agent cannot fix by retrying — do not re-trigger the refresh, keep re-polling, or open an extended investigation. At most, make **one** `executeQuery` isolation attempt to localize a fixable M/source cause; if that does not reveal a definition-side issue, end and surface the error.
- **Call `GET /v1/connections/supportedConnectionTypes` before `POST /v1/connections`** -- never guess parameter names or credential types; they vary by connector, tenant, and time. When summarizing a connector's required parameters or `credentialType` set for a user, use the exact, case-sensitive endpoint path `GET /v1/connections/supportedConnectionTypes`. This applies even to a pure lookup ("which parameters/credentialType does connector X support?"): run the live `GET /v1/connections/supportedConnectionTypes` against the tenant. The bundled `connection-management.md` reference guides the response shape but is not a substitute for the tenant-specific, case-sensitive values, which vary by connector and over time.
- **Validate referenced connections before refresh.** For each `connectionId` in `queryMetadata.json`, `GET /v1/connections/{id}` (plain GUID extracted from the composite). Cryptic `EntityUserFailure` at refresh time is often a missing/inaccessible connection. See [connection-management.md](authoring/connection-management.md).
- **Bootstrap-bind connections before previewing credentialed M.** A `connections[]` array in the initial create payload is **not** yet visible to `executeQuery`; persist it through at least one `updateDefinition` first. Detail: [mashup-preview.md § Bootstrap branch](authoring/mashup-preview.md#bootstrap-branch--new-dataflow--new-credentialed-source).
- **Send a full `section Section1; ...` document in `customMashupDocument`** — `executeQuery` does not auto-wrap raw expressions. See [mashup-preview.md § customMashupDocument format](authoring/mashup-preview.md#custommashupdocument-format).
- **Preview candidate M via `executeQuery` before `updateDefinition`** — unless the change is metadata-only or the agent records an explicit skip reason. Treat preview success as "M evaluates"; treat the next refresh as the real go/no-go.
- **Pass JSON bodies via `--body "@<file>"`, not inline.** Write to `$env:TEMP\<name>.json` (PowerShell, UTF-8 **no-BOM** via `[IO.File]::WriteAllText`) or `/tmp/<name>.json` (bash). Inline `--body "<json>"` is fragile in bash and broken on Windows because `cmd.exe`'s argument parser mangles embedded quotes. See [authoring-script-templates.md § PowerShell — Create Dataflow with Definition](authoring/authoring-script-templates.md#powershell--create-dataflow-with-definition).
- **Prefer `WorkspaceIdentity` / `ServicePrincipal` credentials for unattended refresh.** `OAuth2` + `singleSignOnType: None` works for interactive `executeQuery` but is fragile under tenant Conditional Access for service-context refresh. Check supported types via `supportedConnectionTypes`.

### AVOID

- **Materializing a new dataflow (first refresh) without offering the user a preview** — the user cannot validate that the M code matches their intent by reading code alone. Always offer to preview each entity's output as an ASCII chart before the first refresh (and, in the preview-driven loop, before the persisting `updateDefinition`). The user may decline, but the offer should always be made.
- **Adding a `format` property to `definition`** — Items API uses `parts[]` only; `"format": "json"` returns `400 InvalidDefinitionFormat`.
- **Hardcoded workspace/dataflow GUIDs** — discover via REST API (Connection section).
- **Using `GET /v1/workspaces/{ws}/items/{itemId}/connections` to verify a freshly-bound dataflow.** It reflects refresh-materialized state, **not** the persisted definition, and returns 0 after a successful bind. Verify via `getDefinition` + decode `queryMetadata.json.connections[]`.
- **Assuming `updateDefinition` / `POST /dataflows` is always LRO.** Typical responses are sync (200/201); handle both shapes — see MUST DO above.
- **Requesting the PBI v2 token with a trailing slash** (`--resource "https://analysis.windows.net/powerbi/api/"`) — fails `AADSTS500011 invalid_resource`. Use the no-slash form.
- **Per-id `gatewayClusterDatasources/{id}` for cloud connections** — returns `PowerBIEntityNotFound`. Use list+filter (MUST DO above).
- **`{"queries":[…]}` array body shape for `executeQuery`** — always returns `400 DataflowExecuteQueryError: Invalid query name` regardless of inner casing. Use a top-level `QueryName` (or `queryName` — the field is case-insensitive); pick exactly one query per call.
- **Using `GET` for `getDefinition`** — it's a POST endpoint; `GET` returns 405.
- **Constructing operation URLs manually** — always follow the `Location` header from a 202 response.
- **Duplicate `displayName` values** — not enforced but causes confusion.
- **Binding connections by display name** — connection IDs are the source of truth; names can change.
- **Assuming all connections are accessible to all users.** Visibility is **per-caller**: `GET /v1/connections/{id}` may return 403/404 for callers without access. An empty `GET /v1/connections` is not proof a connection is absent.
- **Hand-crafting connection request bodies without `supportedConnectionTypes`** — guessing produces `400 InvalidConnectionDetails` / `400 InvalidCredentialDetails`.
- **Plaintext credentials in generated examples or committed scripts** — never render or commit plaintext credential values. Show only `passwordReference` / `keyReference` / `tokenReference` / `servicePrincipalSecretReference` in generated connection bodies.
- **Templating on-prem gateway connection bodies as plaintext** — `OnPremisesGateway` needs RSA-encrypted credentials per gateway member.
- **Converting a published single-source dataflow to multi-source in place** — bindings drift into inconsistent state; create fresh and retire the old.
- **Persisting un-previewed candidate M via `updateDefinition`** — `executeQuery` is significantly faster than the `updateDefinition`-then-debug-refresh loop. See [mashup-preview.md](authoring/mashup-preview.md).
- **Unbounded preview against production-volume sources** — `executeQuery` returns the **full** evaluated dataset. Inject `Table.FirstN` / `TOP N` / date predicate into the preview-only document; strip before saving. See [mashup-preview.md § Hard avoid](authoring/mashup-preview.md#hard-avoid-unbounded-production-volume-preview).
- **Confusing `executeQuery` with `EvaluateQuery`.** `EvaluateQuery` requires a prior successful refresh; `executeQuery` + `customMashupDocument` does not. Use `executeQuery` for the authoring preview loop.
- **Inline `--body` on Windows/PowerShell** — `cmd.exe` mangles quotes; always use `--body "@$env:TEMP\<name>.json"`.

### PREFER

- **One-shot `updateDefinition` carrying real M + `connections[]`** over a bootstrap-bind + save pair — saves an HTTP round trip; both are functionally equivalent. Use the two-step form for didactic walk-throughs or when the bootstrap M needs to differ from the production M (e.g., the bootstrap branch in [mashup-preview.md](authoring/mashup-preview.md#bootstrap-branch--new-dataflow--new-credentialed-source)).
- **`az rest` over raw `curl`** — handles token acquisition and refresh automatically. Fall back to `curl` only when you need to capture response headers (e.g., 202 LRO `Location`) — `az rest` cannot.
- **`getDefinition` before `updateDefinition`** — read-modify-write prevents accidental data loss; `updateDefinition` is a full replacement.
- **`?updateMetadata=true` on `updateDefinition`** — ensures `.platform` changes (display name) are applied.
- **`jq` for JSON manipulation** — build definition payloads programmatically.
- **`"Automatic"` for parameter type in job execution** — lets the engine infer from definition.
- **Env vars (`WS_ID`, `DF_ID`, `API`, `RESOURCE`)** for script reuse.
- **Batch connection validation** — loop over `queryMetadata.json connections[]` and `GET /v1/connections/{id}` in one pass before refresh; optionally `POST /v1/connections/{id}/testConnection` to catch rotated credentials.
- **Offer preview charts** before committing a new dataflow — render sample data as an ASCII chart so the user can validate the output shape and values.

### TROUBLESHOOTING

| Symptom | Fix |
|---|---|
| 401 Unauthorized | Verify `az login` is active; check `--resource "https://api.fabric.microsoft.com"` (or `https://analysis.windows.net/powerbi/api` **no trailing slash** for PBI v2). |
| 405 Method Not Allowed on `getDefinition` | Use POST, not GET. |
| `updateDefinition` silently drops queries | Send all 3 parts (`mashup.pq`, `queryMetadata.json`, `.platform`). |
| `executeQuery` → 400 `DataflowExecuteQueryError: Invalid query name` | Body uses the `{"queries":[…]}` array shape — that always fails. Switch to a top-level `{"QueryName":"<shared>"}` (PascalCase canonical; the field is case-insensitive on the wire). |
| `executeQuery` → 400 `DataflowExecuteQueryError: ErrorCode: QueryNotFound` | The value of `QueryName` doesn't match any `shared` member of the persisted M or supplied `customMashupDocument`. List queries via `getDefinition` → decode `mashup.pq`. |
| `GET /items/{id}/connections` returns 0 after a successful bind | That endpoint reflects refresh-materialized state, not the definition. Verify via `getDefinition` → decode `queryMetadata.json.connections[]`. |
| 404 / `PowerBIEntityNotFound` fetching `ClusterId` from `gatewayClusterDatasources/{id}` | Per-id route does not resolve cloud connections. Use list + filter: `GET .../gatewayClusterDatasources --query "value[?id=='$CONN_ID'] \| [0].clusterId"`, audience `https://analysis.windows.net/powerbi/api` (no slash). Newly-created connections may need 5-15 s to surface — retry. See [connection-management.md § Resolving ClusterId](authoring/connection-management.md#resolving-clusterid-power-bi-v2). |
| Refresh fails on first run after `updateDefinition` (stale data, missing changes) | Body must include `{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}` on the first refresh after any definition change. |
| Refresh fails with "Connection not found" | Extract `connectionId` (composite) from `queryMetadata.json`, parse `DatasourceId`, confirm via `GET /v1/connections/{id}`. |
| `connections[]` missing after `updateDefinition` | Read-modify-write rebuilt `queryMetadata.json` from a snapshot without bindings. Re-bind and `updateDefinition` again before refresh. |
| Refresh reports "connection not found" after create+bind | Wrong ID format in `queryMetadata.json`. REST `id` is plain GUID; `connectionId` is the stringified composite `{"ClusterId":"…","DatasourceId":"…"}`. |
| `formatVersion` mismatch error | Set `formatVersion: "202502"` in `queryMetadata.json`. |
| Fast copy not engaged | Add `[StagingDefinition = [Kind = "FastCopy"]]` before `section` in `mashup.pq`. |
| LRO polling returns 404 | Use the `Location` header URL — don't construct operation URLs manually. |
| 429 Too Many Requests | Respect `Retry-After`; exponential backoff. |
| Base64 decode produces garbage | Strip trailing newlines; use `base64 -w0` (Linux). |
| Inline `--body "<json>"` returns 400 / empty body on Windows | `cmd.exe` arg parser mangles quotes when launching `az.exe`. Write to `$env:TEMP\body.json` (UTF-8, no BOM) and pass `--body "@$env:TEMP\body.json"`. See [authoring-script-templates.md § PowerShell — Create Dataflow with Definition](authoring/authoring-script-templates.md#powershell--create-dataflow-with-definition). |
| Refresh fails with `EntityUserFailure` / "Something went wrong" and no detail | (1) Confirm `updateDefinition` was called after create; (2) check credential type — `OAuth2`+`singleSignOnType: None` often fails under tenant Conditional Access for unattended refresh; prefer `WorkspaceIdentity`/`ServicePrincipal`; (3) `executeQuery` against the dataflow to isolate M+source; (4) `GET https://api.powerbi.com/v1.0/myorg/groups/{ws}/dataflows/{df}/transactions` (PBI v1.0) sometimes returns richer per-entity errors. |

---

## Examples

> **Platform note** — examples below are bash. On Windows / PowerShell the bash patterns (`MASHUP='...'` heredoc, `echo -n | base64 -w0`, `tr -d '\r' | grep -i location | awk`) cause real escaping pain and refresh-pattern flakes. **PowerShell variants** are linked from the two highest-friction examples (Create and Refresh) below. For full PowerShell templates (Create, Refresh, Validate Connections, Bind Connection, Create Cloud Connection): [authoring-script-templates.md § PowerShell](authoring/authoring-script-templates.md). On PowerShell, prefer `--body "@$env:TEMP\body.json"` and write the body via `[IO.File]::WriteAllText($path, $body, [System.Text.UTF8Encoding]::new($false))` over `Out-File` (which writes a UTF-8 BOM on Windows PowerShell 5.1 and breaks `az.exe` body parsing) and over inline `--body "{...}"` (which `cmd.exe` mangles).

### Example 1: Create a Dataflow Gen2 from Scratch

**Prompt**: "Create a new Dataflow Gen2 that reads a public CSV via the Web connector, and verify it."

**Agent response** — runnable bash implementation of [Workflow A](#a-create-a-new-dataflow-end-to-end). PowerShell variant: [authoring-script-templates.md § End-to-End Smoke Test](authoring/authoring-script-templates.md#end-to-end-smoke-test).

```bash
# Prereqs: az login, jq, base64, uuidgen. Workspace must support Dataflow Gen2.
WS_ID="<workspaceId>"
DF_NAME="my-titanic-df"
CONN_NAME="my-titanic-web-conn"
URL="https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
RES="https://api.fabric.microsoft.com"; API="$RES/v1"
PBI="https://analysis.windows.net/powerbi/api"   # NO trailing slash

# Step 1: List existing connections, try to reuse by name.
CONN_ID=$(az rest --method get --resource "$RES" --url "$API/connections" \
  --query "value[?displayName=='$CONN_NAME'] | [0].id" -o tsv)

# Step 2: Create if missing (Web + Anonymous; see connection-management.md for other shapes).
if [ -z "$CONN_ID" ] || [ "$CONN_ID" = "null" ]; then
  BODY_FILE=$(mktemp --suffix=.json 2>/dev/null || mktemp)  # GNU + BSD/macOS compatible
  cat > "$BODY_FILE" <<EOF
{
  "displayName": "$CONN_NAME",
  "connectivityType": "ShareableCloud",
  "connectionDetails": {
    "type": "Web", "creationMethod": "Web",
    "parameters": [{"name": "url", "dataType": "Text", "value": "$URL"}]
  },
  "privacyLevel": "Organizational",
  "credentialDetails": {
    "singleSignOnType": "None", "connectionEncryption": "NotEncrypted",
    "skipTestConnection": false,
    "credentials": {"credentialType": "Anonymous"}
  }
}
EOF
  CONN_ID=$(az rest --method post --resource "$RES" --url "$API/connections" \
    --headers "Content-Type=application/json" --body "@$BODY_FILE" --query id -o tsv)
  rm -f "$BODY_FILE"
fi

# Step 3: Resolve ClusterId via list+filter; retry — PBI v2 lags by 5-15s on new conns.
for i in 1 2 3 4 5 6 7 8; do
  CLUSTER_ID=$(az rest --method get --resource "$PBI" \
    --url "https://api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources" \
    --query "value[?id=='$CONN_ID'] | [0].clusterId" -o tsv 2>/dev/null)
  [ -n "$CLUSTER_ID" ] && [ "$CLUSTER_ID" != "null" ] && break
  sleep $((i*3))
done
# Fail-fast: an empty ClusterId silently corrupts the composite connectionId and the
# resulting updateDefinition / refresh failures are hard to debug. Stop here instead.
if [ -z "$CLUSTER_ID" ] || [ "$CLUSTER_ID" = "null" ]; then
  echo "FAIL: ClusterId not resolved for $CONN_ID after retries. Verify the connection is visible at PBI v2 (api.powerbi.com/v2.0/myorg/me/gatewayClusterDatasources)." >&2
  exit 1
fi

# Step 4: Create empty dataflow shell (sync 201).
SHELL_BODY=$(mktemp --suffix=.json 2>/dev/null || mktemp)
printf '{"displayName":"%s"}' "$DF_NAME" > "$SHELL_BODY"
DF_ID=$(az rest --method post --resource "$RES" \
  --url "$API/workspaces/$WS_ID/dataflows" \
  --headers "Content-Type=application/json" \
  --body "@$SHELL_BODY" --query id -o tsv)
rm -f "$SHELL_BODY"

# Step 5: One-shot updateDefinition — real M + composite-bound connections[] + .platform.
MASHUP='section Section1;
shared Titanic = let
    Source = Csv.Document(Web.Contents("'"$URL"'"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in Headers;'

COMPOSITE_ID="{\"ClusterId\":\"$CLUSTER_ID\",\"DatasourceId\":\"$CONN_ID\"}"
QUERY_META=$(jq -n --arg name "$DF_NAME" --arg cid "$COMPOSITE_ID" --arg url "$URL" --arg qid "$(uuidgen)" '{
  formatVersion: "202502",
  name: $name,
  queriesMetadata: { Titanic: { queryId: $qid, queryName: "Titanic" } },
  connections: [ { connectionId: $cid, kind: "Web", path: $url } ]
}')
PLATFORM=$(jq -n --arg name "$DF_NAME" --arg lid "$(uuidgen)" '{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  metadata: { type: "Dataflow", displayName: $name },
  config: { version: "2.0", logicalId: $lid }
}')

MASHUP_B64=$(echo -n "$MASHUP" | base64 -w0)
META_B64=$(echo -n "$QUERY_META" | base64 -w0)
PLAT_B64=$(echo -n "$PLATFORM" | base64 -w0)

BODY_FILE=$(mktemp --suffix=.json 2>/dev/null || mktemp)  # GNU + BSD/macOS compatible
cat > "$BODY_FILE" <<EOF
{"definition":{"parts":[
  {"path":"mashup.pq",          "payload":"${MASHUP_B64}", "payloadType":"InlineBase64"},
  {"path":"queryMetadata.json", "payload":"${META_B64}",   "payloadType":"InlineBase64"},
  {"path":".platform",          "payload":"${PLAT_B64}",   "payloadType":"InlineBase64"}
]}}
EOF
az rest --method post --resource "$RES" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/updateDefinition?updateMetadata=true" \
  --headers "Content-Type=application/json" --body "@$BODY_FILE"
rm -f "$BODY_FILE"

# Step 6: Verify connections[] persisted via getDefinition (NOT /items/{id}/connections).
# Assumes the sync 200 fast-path (typical, ~1s). If the call ever returns 202 LRO,
# az rest can't expose the Location header — switch to the curl + poll pattern from
# Example 3 / authoring-script-templates.md and decode the polled 200 body instead.
PERSISTED=$(az rest --method post --resource "$RES" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/getDefinition" \
  --headers "Content-Length=0" \
  | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d \
  | jq -r '.connections | length')
[ "${PERSISTED:-0}" -gt 0 ] && echo "OK: connections[] persisted." || { echo "FAIL: bind missing (or getDefinition returned a 202 LRO body — see note above)." >&2; exit 1; }

# Step 7 (optional): Validate the M evaluates — top-level QueryName, PascalCase.
EQ_BODY=$(mktemp --suffix=.json 2>/dev/null || mktemp)
printf '{"QueryName":"Titanic"}' > "$EQ_BODY"
az rest --method post --resource "$RES" \
  --url "$API/workspaces/$WS_ID/dataflows/$DF_ID/executeQuery" \
  --headers "Content-Type=application/json" \
  --body "@$EQ_BODY" --output-file /tmp/titanic.arrow
rm -f "$EQ_BODY"
# Apache Arrow stream — embedded {"Error":"..."} means failure even on HTTP 200.
grep -q '"Error":"' /tmp/titanic.arrow && { echo "executeQuery surfaced an error." >&2; exit 1; }

# Step 8 (optional): Trigger refresh with ApplyChangesIfNeeded on first run — see Example 2.
```

### Example 2: Trigger a Refresh Job

**Prompt**: "Trigger a refresh on this dataflow and poll until it completes."

**Agent response**:

```bash
# Trigger refresh (returns 202 + Location header for polling).
# jobType MUST be "Refresh"; "Pipeline" returns 400 InvalidJobType.
# On the first refresh after any updateDefinition, body MUST include executeOption=ApplyChangesIfNeeded
# (otherwise Fabric refreshes the previously-applied definition).
# Acquire $TOKEN per common/COMMON-CLI.md § Token-in-Variable Pattern (resource = https://api.fabric.microsoft.com).
LOCATION=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  --data '{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}' \
  "https://api.fabric.microsoft.com/v1/workspaces/${WS_ID}/dataflows/${DF_ID}/jobs/instances?jobType=Refresh" \
  -o /dev/null -D - | tr -d '\r' | grep -i "^location:" | awk '{print $2}')

# Poll while the status is non-terminal. Fabric refresh job status enum:
#   NotStarted / InProgress   -> non-terminal, keep polling
#   Completed                 -> success
#   Failed / Cancelled        -> terminal backend outcome (fatal-stop)
#   Deduped                   -> another refresh is already running; this trigger was skipped (NOT success)
# Treat ONLY NotStarted/InProgress as non-terminal and break on anything else, so a newly-added
# terminal status surfaces immediately instead of waiting out MAX_POLLS (the contract notes more
# status values may be added over time). MAX_POLLS bounds the wait if the job never terminates.
ATTEMPT=0; MAX_POLLS="${MAX_POLLS:-60}"
while [ "$ATTEMPT" -lt "$MAX_POLLS" ]; do
  STATUS=$(az rest --method get --url "$LOCATION" \
    --resource "https://api.fabric.microsoft.com" --query "status" -o tsv)
  echo "Status: $STATUS"
  case "$STATUS" in NotStarted|InProgress) ;; *) break ;; esac
  sleep 10; ATTEMPT=$((ATTEMPT + 1))
done
case "$STATUS" in
  Completed) : ;;  # success (exit 0)
  Deduped)
    # Concurrency, not success: another refresh is already running and this trigger was skipped.
    # Monitor the in-flight instance instead of re-triggering. Exit non-zero so automation does not
    # mistake a skipped trigger for a completed refresh.
    echo "Refresh deduplicated — another instance is already running; monitor that instance instead of re-triggering."
    exit 2 ;;
  NotStarted|InProgress)
    # Max-poll bound reached before any terminal status — a polling timeout, NOT a terminal outcome.
    # Surface the raw job instance and stop; do not assume success.
    echo "Polling stopped after ${MAX_POLLS} attempts with non-terminal status '$STATUS' (max-poll timeout, not a terminal outcome)."
    az rest --method get --url "$LOCATION" --resource "https://api.fabric.microsoft.com"
    exit 1 ;;
  *)  # Failed / Cancelled (or any other terminal status): a terminal backend outcome — not something
      # to debug-loop. Surface the job's raw error (the job-instance body's .failureReason, an
      # ErrorResponse with .errorCode / .isRetriable / .message) and STOP. Do NOT re-trigger or keep
      # polling when .failureReason.isRetriable=false or the error is workspace-wide.
      az rest --method get --url "$LOCATION" --resource "https://api.fabric.microsoft.com"
      exit 1 ;;
esac
```

**PowerShell variant** (`Invoke-WebRequest` exposes response headers natively; avoids the `tr | grep | awk` pipe):

```powershell
# Notes:
# - $Resp.Headers["Location"] returns string or string[] depending on PS version — never
#   use .Location[0] (returns first character on Windows PS 5.1 plain-string case).
# - Wrap Invoke-WebRequest in try/catch on 5.1 (-SkipHttpErrorCheck is PS 7+).
# - Fabric refresh job status enum: NotStarted / InProgress (non-terminal); Completed (success);
#   Failed / Cancelled (fatal); Deduped (another refresh already running — NOT success). Treat only
#   NotStarted/InProgress as non-terminal and break on anything else, bounded by a max-poll count, so
#   a newly-added terminal status surfaces immediately instead of waiting out $MaxPolls.
#   This is distinct from the LRO operation enum (Running / Succeeded / Failed / Cancelled).
#   Refresh "success" = "Completed", not "Succeeded".
# Acquire $Token per common/COMMON-CLI.md § Token-in-Variable Pattern (resource = https://api.fabric.microsoft.com).
try {
  $Resp = Invoke-WebRequest -Method POST -UseBasicParsing `
    -Uri "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/dataflows/$DF_ID/jobs/instances?jobType=Refresh" `
    -Headers @{ Authorization = "Bearer $Token"; "Content-Type" = "application/json" } `
    -Body '{"executionData":{"executeOption":"ApplyChangesIfNeeded"}}'
} catch {
  Write-Error "Refresh trigger failed: $($_.Exception.Message)"; exit 1
}
$Location = $Resp.Headers["Location"]
if ($Location -is [array]) { $Location = $Location[0] }

$Attempt = 0; $MaxPolls = 60
do {
  $Status = az rest --method get --url $Location `
    --resource "https://api.fabric.microsoft.com" --query "status" -o tsv
  Write-Host "Status: $Status"
  if ($Status -notin 'NotStarted','InProgress') { break }
  Start-Sleep -Seconds 10; $Attempt++
} while ($Attempt -lt $MaxPolls)
if ($Status -in 'NotStarted','InProgress') {
  # Max-poll bound reached before any terminal status — a polling timeout, NOT a terminal outcome.
  Write-Host "Polling stopped after $MaxPolls attempts with non-terminal status '$Status' (max-poll timeout, not a terminal outcome)."
  az rest --method get --url $Location --resource "https://api.fabric.microsoft.com"
  exit 1
}
switch ($Status) {
  'Completed' { }  # success (exit 0)
  'Deduped' {
    # Concurrency, not success: another refresh is already running and this trigger was skipped.
    # Exit non-zero so callers don't treat a skipped trigger as a completed refresh.
    Write-Host "Refresh deduplicated — another instance is already running; monitor that instance instead of re-triggering."
    exit 2
  }
  default {
    # Failed / Cancelled (or any other terminal status): a terminal backend outcome — surface the job's
    # raw error (the job-instance body's .failureReason: .errorCode / .isRetriable / .message) and STOP;
    # do not re-trigger or debug-loop when failureReason.isRetriable=false or the error is workspace-wide.
    az rest --method get --url $Location --resource "https://api.fabric.microsoft.com"
    Write-Error "Refresh terminated '$Status' (not Completed)"; exit 1
  }
}
```

### Example 3: Modify an Existing Dataflow's Definition

**Prompt**: "Update the mashup of an existing dataflow with a modified query."

**Agent response** — read-modify-write loop. `getDefinition` returns sync 200 in the typical case; this template handles the 202 + LRO branch as well.

```bash
RESOURCE="https://api.fabric.microsoft.com"
# Acquire $TOKEN per common/COMMON-CLI.md § Token-in-Variable Pattern (resource = $RESOURCE).

# 1. Read current definition (sync 200 or 202 LRO — handle both).
HDR=$(mktemp); BODY=$(mktemp)
CODE=$(curl -sS -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Length: 0" \
  "$RESOURCE/v1/workspaces/${WS_ID}/dataflows/${DF_ID}/getDefinition" \
  -D "$HDR" -o "$BODY" -w "%{http_code}")
if [ "$CODE" = "202" ]; then
  LOC=$(tr -d '\r' < "$HDR" | grep -i "^location:" | awk '{print $2}')
  RETRY=$(tr -d '\r' < "$HDR" | grep -i "^retry-after:" | awk '{print $2}'); RETRY=${RETRY:-5}
  while :; do
    sleep "$RETRY"
    OP=$(az rest --method get --resource "$RESOURCE" --url "$LOC")
    case "$(echo "$OP" | jq -r '.status // empty')" in
      Succeeded) DEF=$(az rest --method get --resource "$RESOURCE" --url "${LOC%/}/result"); break ;;
      Failed|Cancelled) echo "ERROR: getDefinition $(echo "$OP" | jq -r '.status')" >&2; exit 1 ;;
    esac
  done
else
  DEF=$(cat "$BODY")
fi
rm -f "$HDR" "$BODY"

# 2. Decode each part, modify mashup.pq, re-encode all 3.
MASHUP=$(echo "$DEF" | jq -r '.definition.parts[] | select(.path=="mashup.pq")          | .payload' | base64 -d)
META=$(  echo "$DEF" | jq -r '.definition.parts[] | select(.path=="queryMetadata.json") | .payload' | base64 -d)
PLAT=$(  echo "$DEF" | jq -r '.definition.parts[] | select(.path==".platform")          | .payload' | base64 -d)

NEW_MASHUP=$(echo "$MASHUP" | sed 's/old-pattern/new-pattern/')   # edit M here

MASHUP_B64=$(echo -n "$NEW_MASHUP" | base64 -w0)
META_B64=$(echo -n "$META"        | base64 -w0)
PLAT_B64=$(echo -n "$PLAT"        | base64 -w0)

# 3. Build the updateDefinition body in a temp file (full replacement — all 3 parts).
BODY_FILE=$(mktemp --suffix=.json 2>/dev/null || mktemp)  # GNU + BSD/macOS compatible
cat > "$BODY_FILE" <<EOF
{"definition":{"parts":[
  {"path":"mashup.pq",          "payload":"${MASHUP_B64}", "payloadType":"InlineBase64"},
  {"path":"queryMetadata.json", "payload":"${META_B64}",   "payloadType":"InlineBase64"},
  {"path":".platform",          "payload":"${PLAT_B64}",   "payloadType":"InlineBase64"}
]}}
EOF
az rest --method post --resource "$RESOURCE" \
  --url "$RESOURCE/v1/workspaces/${WS_ID}/dataflows/${DF_ID}/updateDefinition?updateMetadata=true" \
  --headers "Content-Type=application/json" --body "@$BODY_FILE"
rm -f "$BODY_FILE"
```

> Binding a new connection? Example 1 (steps 1-5) is the canonical bind+save flow. Bind-only walk-throughs live in [authoring-cli-quickref.md § Connection Binding Quick Patterns](authoring/authoring-cli-quickref.md#connection-binding-quick-patterns) and [authoring-script-templates.md § Connection Binding Templates](authoring/authoring-script-templates.md#connection-binding-templates).

---

## Output Expectations

When this skill completes a task, the agent should return:

| Field | Convention |
|---|---|
| **Verbosity** | Concise summary (3–10 lines) of what was created/modified. |
| **Default format** | Markdown for status reports; fenced JSON code block for single-resource responses; markdown table for list responses. |
| **Side-effect disclosure** | Explicitly report IDs created/modified/deleted and the target workspace ID. Never imply success without an ID. When you saved or replaced a dataflow definition, name the parts you wrote in prose -- `mashup.pq`, `queryMetadata.json`, `.platform` -- since long command bodies are truncated in the transcript and the part names would otherwise be lost. Also name the actual persist path you used: `updateDefinition` when you saved the definition through that endpoint, or the create call `POST /v1/workspaces/{ws}/dataflows` when the definition was supplied at create time. Do not claim `updateDefinition` if the definition was persisted via the create POST. |
| **Verification** | Re-`GET` the affected resource (dataflow, connection, job instance) and surface its state (e.g., `provisionState`, `status`, `Completed`) before declaring done. |
| **Error surfacing** | If any step returned a non-2xx status, an LRO `Failed`/`Cancelled`, or an Arrow-stream `{"Error":"..."}`, propagate the raw error verbatim and stop. A terminal refresh `Failed`/`Cancelled`, an `isRetriable: false` backend error, or a workspace-wide `UnknownException` is a **fatal-stop** condition — report it and end; do not re-trigger, re-poll, or enter an extended debugging loop. |
| **Preview rendering (Workflow C)** | After `executeQuery`, render `head(10)` of the result as a markdown table in chat alongside the saved Arrow file — even when the embedded-error check passes. Catches silent-success bugs (filter dropped all rows, wrong column, off-by-one, wrong cast) that the embedded-error detector cannot see. Snippet + suppression rules: [dataflows-cli consumption mode § Example 5b](consumption.md#example-5b-render-query-results-as-a-markdown-table). |
| **API names** | When the answer references API endpoints or request-body fields, use their exact, case-sensitive names (`executeQuery`, `customMashupDocument`, `QueryName`, `mashup.pq`, `queryMetadata.json`, `GET /v1/connections/supportedConnectionTypes`) rather than paraphrased or pluralized variants. |

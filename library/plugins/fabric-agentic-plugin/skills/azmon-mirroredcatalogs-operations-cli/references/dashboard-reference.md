# Real-Time (KQL) Dashboard reference

Agent guidance for Stage 15 (optional dashboard suggestion and creation). Do not
paste verbatim to users. Keep everything domain-agnostic — derive tile names and
semantics from the user's real, verified data, never from an example.

## Surface

A **Real-Time Dashboard** (`KQLDashboard` Fabric item) renders tiles backed by
**KQL queries** against an Eventhouse / KQL database. Tiles bind to the **verified
columns / entities from schema verification (Stages 12–14)**, which always exist
by this point, so no extra semantic modeling is required. A materialized
`IncidentBins`-style object is **optional** here: the dashboard (Stage 15) runs
**before** the Operations Agent (Stage 16), so in a **dashboard-only** flow
`IncidentBins` may **not** exist yet — never assume it, and reference it only if
it was already materialized.

## Create / update mechanics

- **Create item**: `POST /v1/workspaces/{workspaceId}/kqlDashboards` with a display
  name (dedicated KQL dashboard endpoint; supports long-running operations). The
  generic `POST /v1/workspaces/{workspaceId}/items` with `type: "KQLDashboard"` is
  an alternative.
- **Apply definition**: create-with-definition, or `getDefinition` /
  `updateDefinition` on the dedicated endpoints
  (`.../kqlDashboards/{kqlDashboardId}/getDefinition` and
  `.../kqlDashboards/{kqlDashboardId}/updateDefinition`) with a base64-encoded
  payload describing the data-source binding and each tile (title, KQL query,
  visual type, layout).
- **Read before edit**: get the current definition before updating; do not
  fabricate definition fields.
- **Definition parts**: the KQL Dashboard definition has **two** parts —
  `RealTimeDashboard.json` (the dashboard content, below) and a `.platform`
  part (item metadata: display name, type, logical id). When you create the
  item first with a plain `POST .../kqlDashboards` (display name only) and then
  `updateDefinition`, the `.platform` part is **optional** — the item metadata
  already exists. When creating **with a definition** in one call, include both
  parts (or let the platform default `.platform` from the create request).

### `RealTimeDashboard.json` skeleton (`schema_version` empirically observed)

The Microsoft Learn [KQL dashboard definition](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/kql-dashboard-definition)
article documents this definition; its published example uses `schema_version`
`"52"`. The `"60"` below is an **empirically observed** viewer version from live
testing — it is version-specific and **will drift** as the viewer updates. The
item **create API accepts an incomplete payload regardless**, so a
`schema_version` mismatch degrades gracefully; it is the dashboard **viewer**
that validates strictly, so match the version the live viewer currently expects.
Build the definition part `RealTimeDashboard.json` from this skeleton so the
dashboard is a single-shot create instead of an error-by-error iteration:

```jsonc
{
  "schema_version": "60",
  "title": "<dashboard title>",
  "autoRefresh": { "enabled": false },
  "baseQueries": [],
  "parameters": [],
  "dataSources": [
    { "kind": "manual-kusto", "id": "<dsId>", "name": "<db>",
      "scopeId": "kusto", "clusterUri": "<queryServiceUri>", "database": "<db>" }
  ],
  "pages": [ { "id": "<pageId>", "name": "Overview" } ],
  "queries": [
    { "id": "<qId>", "text": "<KQL>", "usedVariables": [],
      "dataSource": { "kind": "inline", "dataSourceId": "<dsId>" } }
  ],
  "tiles": [
    { "id": "<tId>", "title": "<tile title>", "pageId": "<pageId>",
      "layout": { "x": 0, "y": 0, "width": 8, "height": 6 },
      "visualType": "column", "visualOptions": {},
      "queryRef": { "kind": "query", "queryId": "<qId>" } }
  ]
}
```

Gotchas the strict validator enforces (each caused a viewer error in testing):

- **Root** MUST include `baseQueries` and `parameters` (use `[]` when unused).
- Each **`dataSources[]`** entry MUST include `scopeId` (e.g. `"kusto"`) in
  addition to `id`, `name`, `kind`, `clusterUri`, `database`.
- Each **`queries[]`** entry MUST include `usedVariables` (`[]` when unused) and
  bind its source via a nested `dataSource` object — **not** a flat
  `dataSourceId`.
- The query's **`dataSource.kind` is `"inline"`**, which means *"reference a
  `dataSources[]` entry by id"* — it carries `dataSourceId` (matching a
  `dataSources[].id`) and MUST NOT carry `clusterUri`/`database`. The cluster and
  database live **only** in the root `dataSources[]` entry. (`kind: "parameter"`
  is the other `oneOf` branch and requires `parameterId`.)
- Each **`tiles[]`** entry references its query via `queryRef: { "kind":
  "query", "queryId": "<qId>" }` — a flat `queryId` on the tile is rejected as an
  unevaluated property.
- Every **`id`** (in `dataSources`, `pages`, `queries`, `baseQueries`,
  `parameters`, and `tiles`) MUST be a **freshly generated, unique RFC-4122
  UUID**. The readable placeholders above (`<dsId>`, `<pageId>`, `<qId>`,
  `<tId>`) are for legibility only — the Real-Time Dashboard loader rejects
  non-UUID ids. Cross-references (a tile's `queryRef.queryId`, a query's
  `dataSource.dataSourceId`) MUST reuse the exact same UUID string as the
  entry they point at.
- `visualType` values used: `column`, `bar`, `timechart`, `stat`, `table`.

Encode this JSON as the InlineBase64 payload of the `RealTimeDashboard.json`
definition part.

### Service Principal support

A Service Principal **can create and update** a `KQLDashboard` item with an
application-only token. Normal workspace create/write permission and a valid
data-source binding are still required.

## Tile patterns (generic — instantiate against real columns)

Infer a small candidate set at runtime; each tile must reference verified
columns/entities and bind to a real KQL query. Patterns (not a required list):

| Pattern | Business question it answers |
|---------|------------------------------|
| Metric trend per time bin | How did a key measure move over the incident window? |
| Categorical breakdown | Which entities were most impacted? |
| Single-stat KPI | What is the current / peak value of a KPI? |
| Two-signal overlay | Did an operational signal move with a business KPI? |
| Impact distribution / heatmap | Where do impacts concentrate (time × entity)? |

## Rules

- Suggest → approve → generate. Present tiles and WAIT for approval/revision
  before creating or modifying anything (Stage 15 confirmation gate).
- Only reference columns/entities proven to exist in schema verification.
- Do **not** depend on an `IncidentBins`-style object — it may not be
  materialized yet in a dashboard-only flow (that happens in Stage 16).
- Stay domain-agnostic; confirm entity meaning with the user in business terms.
- Prefer updating an existing dashboard over creating a duplicate when reuse is
  intended.

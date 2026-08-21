# Ontology Consumption — Query Routing Reference

Deep reference for translating a grounded ontology entity type (or relationship) into a source query against the correct per-datasource consumption skill. SKILL.md has the quick decision table; this file has the per-delegate invocation templates, field-mapping contracts, and edge cases.

See [ONTOLOGY-AUTHORING-CORE.md § DataBinding file](../authoring/ONTOLOGY-AUTHORING-CORE.md#databinding-file--entitytypesiddatabindingsguidjson) for the authoritative binding schema this routing layer consumes.

---

## Routing Matrix

| `source.kind` | `dataBindingType` | Default delegate | Alternate | Query language | Notes |
|---|---|---|---|---|---|
| `LakehouseTable` | `NonTimeSeries` | `sqldw-cli` (SQL endpoint) | `spark-cli` | T-SQL (default) or Spark SQL | Static attributes. SQL is default — Spark only when user explicitly wants PySpark / DataFrame work. |
| `LakehouseTable` | `TimeSeries` | `sqldw-cli` (SQL endpoint) | `spark-cli` | T-SQL (default) or Spark SQL | Requires `WHERE <timestampColumn> >= <from>`. Use Spark only for Spark-specific features (MLlib, DataFrames). |
| `KustoTable` | `TimeSeries` | `eventhouse-cli` | — | KQL | Requires `\| where <timestampColumn> > ago(…)`. |
| `KustoTable` | `NonTimeSeries` | **Invalid** — preview rejects | — | — | Surface to the user; the ontology is mis-authored. Switch to `fabriciq-ontology-cli` authoring mode. |
| Relationship contextualization | n/a (always `LakehouseTable`) | `sqldw-cli` (SQL endpoint) | `spark-cli` | T-SQL or Spark SQL | Linking tables are Lakehouse-only today. |

> ❓ **Warehouse bindings:** the shared ontology schema in [ONTOLOGY-AUTHORING-CORE.md § DataBinding file](../authoring/ONTOLOGY-AUTHORING-CORE.md#databinding-file--entitytypesiddatabindingsguidjson) documents **only** `LakehouseTable` and `KustoTable` as `source.type` values. If you see a Warehouse-specific binding variant in the wild, surface it to the user and flag for authoring-guide update — do not silently assume it is spellable as `LakehouseTable`.

**Rule of thumb:** Eventhouse for timeseries-over-Kusto; SQL for everything Lakehouse by default (including joins and relationship traversal); Spark only when the user explicitly wants Spark-specific capabilities.

---

## Field Mapping — Ontology → Delegate Input

Every delegate call needs a minimal, strongly-typed set of fields. Do **not** forward the full grounding JSON; extract only what the delegate needs.

### Eventhouse (`KustoTable` + `TimeSeries`) → `eventhouse-cli`

| Delegate input | Source in grounding JSON |
|---|---|
| `CLUSTER_URI` | `entityTypes[*].bindings[*].source.clusterUri` |
| `DB_NAME` | `entityTypes[*].bindings[*].source.databaseName` |
| Source table (KQL identifier) | `entityTypes[*].bindings[*].source.sourceTableName` |
| Timestamp column (for `where … > ago(…)`) | `entityTypes[*].bindings[*].timestampColumnName` |
| Key column(s) (for `where <key> == "<value>"`) | `entityTypes[*].keyPropertyIds[]` → resolve via `propertyBindings[]` to source column |
| Projected columns | `entityTypes[*].bindings[*].propertyBindings[].sourceColumnName` |

Example KQL body (composed from grounding JSON, then handed to the delegate):

```kql
AircraftReadings                                    // source.sourceTableName
| where AssetId == "N42ZA"                       // key column from propertyBindings
| where PreciseTimestamp > ago(1h)              // timestampColumnName
| project PreciseTimestamp, Temp_C              // propertyBindings sourceColumns
```

### Lakehouse (`LakehouseTable`) → `sqldw-cli` (default) **or** `spark-cli`

| Delegate input | Source in grounding JSON |
|---|---|
| `WS_ID` | `entityTypes[*].bindings[*].source.workspaceId` |
| Source item ID (lakehouse) | `entityTypes[*].bindings[*].source.itemId` |
| Schema | `entityTypes[*].bindings[*].source.sourceSchema` (Lakehouse: usually `dbo`) |
| Source table | `entityTypes[*].bindings[*].source.sourceTableName` |
| Key column(s) | `keyPropertyIds[]` → `propertyBindings[].sourceColumnName` |
| Projected columns | `propertyBindings[].sourceColumnName` |
| Timestamp column (only when `TimeSeries`) | `timestampColumnName` |

Example T-SQL (default dialect for `sqldw-cli`):

```sql
SELECT TOP 100 AssetId, Manufacturer, InstalledOn
FROM   dbo.Aircrafts
WHERE  AssetId = 'N42ZA';
```

Example T-SQL with time bounds (`TimeSeries` lakehouse binding):

```sql
SELECT AssetId, EventTime, Temp_C
FROM   dbo.AircraftReadings
WHERE  AssetId   = 'N42ZA'
  AND  EventTime >= DATEADD(hour, -1, SYSUTCDATETIME());
```

Equivalent **Spark SQL** (when delegating to `spark-cli` — do **not** mix T-SQL `DATEADD` / `SYSUTCDATETIME` into Spark):

```sql
SELECT AssetId, EventTime, Temp_C
FROM   dbo.AircraftReadings
WHERE  AssetId   = 'N42ZA'
  AND  EventTime >= current_timestamp() - INTERVAL 1 HOUR
```

### Relationship contextualization → `sqldw-cli` (default)

Contextualizations are always `LakehouseTable` with a **linking table**. Keys can be **composite** — both `sourceKeyRefBindings[]` and `targetKeyRefBindings[]` are arrays in the ontology schema, so join on **every** entry. SQL endpoint is the default; joins compose more cleanly in T-SQL than Spark SQL through `az rest`.

| Delegate input | Source in grounding JSON |
|---|---|
| Linking workspace / item ID / schema / table | `relationshipTypes[*].contextualizations[*].source.*` |
| Source-side key columns (1 or more) | `contextualizations[*].sourceKeyRefBindings[].sourceColumnName` |
| Target-side key columns (1 or more) | `contextualizations[*].targetKeyRefBindings[].sourceColumnName` |
| Source entity type's physical key column(s) | `entityTypes[sourceEtId].bindings[*].propertyBindings[]` mapped over `keyPropertyIds[]` |
| Target entity type's physical key column(s) | same, for target entity type |

Example T-SQL against the linking table (single-part key):

```sql
-- All Aircrafts operated by Airline 'ZA'
SELECT TailNumber
FROM   dbo.HubAircraftAssignment
WHERE  AirlineId = 'ZA';
```

Example T-SQL with a **composite** key (two-part source → two-part target):

```sql
-- Linking table has (AirlineCode, RegionId) → (FleetGroup, TailNumber)
SELECT FleetGroup, TailNumber
FROM   dbo.HubAircraftAssignment
WHERE  AirlineCode = 'ZA'
  AND  RegionId    = 'EMEA';
```

Follow-up calls join to per-entity bindings (often across different source kinds — see the cross-source section below).

---

## Cross-Source Traversal (Lakehouse ↔ Eventhouse)

A common ontology has **Entity A** on Lakehouse, **Entity B** on Eventhouse, and a `LakehouseTable` contextualization linking them. A single delegate cannot join across source kinds. The routing pattern is:

```text
1.  Hit sqldw-cli (or spark-cli) on the linking table.
      → returns [target keys]
2.  Hit eventhouse-cli with `where <targetKey> in (...)`.
      → returns the timeseries rows
3.  Merge in the agent, translate physical column names back to ontology property names.
```

Size guard: `~10,000` keys is a soft threshold — beyond it, Kusto `in (…)` query text + transport starts to buckle. Supported fallbacks (all composable via this skill + siblings):

- **Narrow the Lakehouse step first** — add more filters (region, date, tenant) so step 1 returns fewer keys.
- **Tighten the Kusto time window** in step 2 so fewer rows need the `in (…)` filter applied.
- **Batch the key list** into multiple Kusto calls of ≤10k each; merge client-side.
- **Stop and ask** — if the user's intent genuinely spans hundreds of thousands of entities, surface that this is a staged-integration problem rather than a ground-and-route one, and escalate to a data-engineering workflow outside this skill's scope.

Do **not** attempt out-of-scope workarounds (Kusto external tables, temp-table materialisation, cross-cluster writes) from this skill — those are owned by data-engineering / authoring tooling, not the consumption siblings.

---

## Delegate Invocation Shapes

Consumption siblings expect **resolved source metadata + a fully-composed query text in the target dialect**. This skill owns the composition; the delegate owns the connection and execution.

### Eventhouse delegate (`eventhouse-cli`)

Hand off:
- **Connection**: `clusterUri`, `databaseName` (read straight from the binding's `source`).
- **Query**: a composed KQL string targeting `sourceTableName`, with the time filter on `timestampColumnName` and the key predicate using the physical column name from `propertyBindings[]`.

```bash
# Fields extracted from grounding JSON (entityType "Aircraft", binding = KustoTable)
CLUSTER_URI="https://<cluster>.kusto.fabric.microsoft.com"
DB_NAME="TelemetryDB"
COMPOSED_KQL="AircraftReadings | where AssetId == 'N42ZA' | where PreciseTimestamp > ago(1h) | project PreciseTimestamp, Temp_C"
# Handoff → eventhouse-cli runs this KQL via its own az rest wiring.
```

### SQL endpoint delegate (`sqldw-cli`) — default for Lakehouse

Hand off:
- **Connection**: `workspaceId`, `itemId` (lakehouse), `sourceSchema` (typically `dbo`).
- **Query**: a composed T-SQL string using physical column names from `propertyBindings[]`.

```bash
WS_ID="<binding.source.workspaceId>"
ITEM_ID="<binding.source.itemId>"          # lakehouse ID
COMPOSED_TSQL="SELECT TOP 100 AssetId, Manufacturer FROM dbo.Aircrafts WHERE Manufacturer = 'Contoso'"
# Handoff → sqldw-cli runs this T-SQL via its own endpoint wiring.
```

### Spark delegate (`spark-cli`) — alternate for Lakehouse

Hand off:
- **Connection**: `workspaceId`, `itemId`, `sourceSchema`.
- **Query**: a composed **Spark SQL** string — use Spark-native time functions; do **not** use T-SQL `DATEADD` / `SYSUTCDATETIME`, they are not valid Spark SQL.

```bash
WS_ID="<binding.source.workspaceId>"
ITEM_ID="<binding.source.itemId>"
COMPOSED_SPARKSQL="SELECT AssetId, EventTime, Temp_C FROM dbo.AircraftReadings WHERE AssetId = 'N42ZA' AND EventTime >= current_timestamp() - INTERVAL 1 HOUR"
# Handoff → spark-cli runs this Spark SQL.
```

---

## Invariants the Router Must Enforce

- **Always remap** ontology property names → `propertyBindings[].sourceColumnName` before building any KQL / Spark SQL / T-SQL. Forwarding an ontology property name to the delegate will fail.
- **Always include a time filter** on `TimeSeries` bindings — `timestampColumnName > <from>`. The delegate will reject / time out on unbounded reads.
- **Always read `workspaceId` + `itemId` from the binding**, not from the ontology. Cross-workspace bindings are legal — the ontology may live in workspace `A` while its `Aircraft` binding points at a lakehouse in workspace `B`:

  ```text
  ontology.workspaceId        = "11111111-..."   ← do NOT pass this to the delegate
  binding.source.workspaceId  = "22222222-..."   ← pass THIS
  binding.source.itemId       = "33333333-..."   ← and THIS (item in workspace B)
  ```
- **Never join across source kinds in a single delegate call.** Split into two handoffs.
- **Never forward raw base64 or the full `definition.parts[]`** to a delegate. Hand only the extracted primitives listed in the field-mapping tables above.
- **Refuse** `KustoTable` + `NonTimeSeries` bindings. The preview does not support this combination; it indicates mis-authoring. Offer to switch to `fabriciq-ontology-cli` authoring mode.
- **Preserve user-value quoting.** KQL uses double quotes for strings; T-SQL uses single quotes; Spark SQL accepts either. Do not let grounding-JSON values carry unescaped quotes into a delegate.

---

## Failure-Mode Quick Reference

| Failure | Likely cause | Router action |
|---|---|---|
| Delegate returns "invalid column" | Ontology property name leaked through | Remap via `propertyBindings[]`, retry once |
| Delegate returns 0 rows on a non-empty source | Casing mismatch on `sourceTableName` or stale `clusterUri` | Compare binding fields to live source; if still mismatched, switch to `fabriciq-ontology-cli` authoring mode |
| Delegate times out | Missing time filter on `TimeSeries` | Add `where <timestampColumnName> > ago(…)` / `>= DATEADD(...)`, retry |
| Delegate returns auth error (401 / 403) | Wrong `--resource` audience or missing source-item role | Check the delegate's own connection contract (EH: `https://kusto.kusto.windows.net`; Spark: Fabric token; SQL: Fabric token) |
| `KustoTable` + `NonTimeSeries` encountered | Mis-authored ontology | Refuse; surface as authoring bug |
| Contextualization source table empty | Linking table has no rows yet | Surface to user; suggest inspecting via `sqldw-cli` before re-running the relationship query |

---

## When to **Not** Route (Agent-Side Work)

Some tasks look like data queries but are purely metadata. Answer these from the grounding JSON — do not invoke a delegate:

- "What entity types are in this ontology?" → grounding JSON `entityTypes[].name`.
- "What are the properties of Aircraft?" → grounding JSON `entityTypes[name=Aircraft].properties[]` + `timeseriesProperties[]`.
- "Which Eventhouse backs this ontology?" → grounding JSON `entityTypes[].bindings[].source.kind == KustoTable` → `itemId` + `clusterUri` + `databaseName`.
- "How is Airline related to Aircraft?" → grounding JSON `relationshipTypes[]` + `contextualizations[]`.

Delegating for these produces noise and may incur unnecessary capacity cost.

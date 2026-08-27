# DAX Performance Decision Guide

Decision framework for optimizing DAX query performance: workflow phases, engine internals, trace diagnostics, and routing into the on-demand pattern catalog.

## Reading Guide

### Must Read — Every Optimization

Always read these sections fully before starting any optimization session:

- **[Optimization Framework](#optimization-framework)** — tiers, autonomy rules, tool requirements
- **[Phase 1: Establish Baseline](#phase-1-establish-baseline)** — measure resolution, model context, run protocol
- **[Phase 2: Optimization Iterations](#phase-2-optimization-iterations)** — apply, test, compare, iterate
- **[Section 1: How the Engine Works](#section-1-how-the-engine-works)** — FE/SE architecture, xmSQL, segments, fusion
- **[Section 2: Trace Diagnostics](#section-2-reading-and-diagnosing-traces)** — metrics, event waterfall, signal interpretation

### Consult When Needed

Read these only when directed by the Decision Guide or after Tier 1 is exhausted:

- **[Section 3: Tier 1 — DAX Patterns](./dax-perf-patterns.md#section-3-tier-1-dax-optimization-patterns)** — DAX001–DAX021 — load only routed candidate patterns first
- **[Section 4: Tier 2 — Query Structure](./dax-perf-patterns.md#section-4-tier-2-query-structure-patterns)** — QRY001–QRY004 — requires user approval before applying
- **[Section 5: Tier 3 — Model Changes](./dax-perf-patterns.md#section-5-tier-3-model-optimization-patterns)** — MDL001–MDL009 — high caution, user approval, suggest model copy
- **[Section 6: Tier 4 — Direct Lake](./dax-perf-patterns.md#section-6-tier-4-direct-lake-optimization-patterns)** — DL001–DL002 — high caution, user approval, requires ETL/pipeline changes

---

## Decision Guide

Use this table as a router into Section 3. Route by trace evidence when available; otherwise route by DAX shape and treat the match as a hypothesis until execution results confirm it. Load only the routed candidate patterns first; read the rest of Section 3 only if no signal matches or routed patterns are exhausted. Sections 4–6 signals are escalation triggers; consult those sections only when the signal appears.

### Section 3 — Where to Start (read all of §3)

| Route when trace shows | Or DAX shape shows | Start With |
|-----------------------|-------------------|------------|
| `CallbackDataID` / callback-like FE row work | `IF`/`SWITCH` or `DIVIDE()` inside row iterators; per-row context transition inside iterators; `ADDCOLUMNS`/`SUMMARIZE` extension patterns | [DAX002](./dax-perf-patterns.md#dax002-use-summarizecolumns-for-grouped-calculations), [DAX007](./dax-perf-patterns.md#dax007-convert-boolean-tests-without-if), [DAX008](./dax-perf-patterns.md#dax008-context-transition-in-iterator), [DAX018](./dax-perf-patterns.md#dax018-keep-iterator-division-se-native) |
| High FE time, many short SE events, or repeated cache hits | repeated measure/expression references; `SUMX(VALUES(col), CALCULATE(...))`; high-cardinality iterator with low-cardinality dependency | [DAX003](./dax-perf-patterns.md#dax003-cache-repeated-expressions-in-variables), [DAX006](./dax-perf-patterns.md#dax006-precompute-iterator-inputs-with-summarizecolumns), [DAX015](./dax-perf-patterns.md#dax015-iterate-at-the-required-grain) |
| SE rows far exceed result rows, or FE filters a broad SE result | `FILTER(Table, ...)` as filter argument; combined predicates; complex `SUMMARIZE` source; filters inside `SUMMARIZECOLUMNS` | [DAX001](./dax-perf-patterns.md#dax001-use-simple-column-filter-predicates-as-calculate-arguments), [DAX005](./dax-perf-patterns.md#dax005-move-complex-summarize-inputs-to-calculatetable), [DAX009](./dax-perf-patterns.md#dax009-externalize-summarizecolumns-filters), [DAX010](./dax-perf-patterns.md#dax010-push-table-filters-with-calculatetable) |
| Multiple SE scans over the same fact with similar joins | sibling time-window measures; slice measures; `SWITCH`/`IF` branches choosing measures | [DAX019](./dax-perf-patterns.md#dax019-move-time-windows-outside-sibling-measures), [DAX020](./dax-perf-patterns.md#dax020-keep-slice-measures-fusion-friendly), [DAX013](./dax-perf-patterns.md#dax013-keep-branch-measures-se-friendly) |
| Near-identical SE scans differ only by filter value | sibling measures differ only by per-measure filters on the same fact | [DAX017](./dax-perf-patterns.md#dax017-align-scan-shape-with-boolean-multipliers) |
| Large `IN`/`INB`, `ININDEX`, or compound tuple predicates | `TREATAS`/`IN` re-filters the same fact with computed keys | [DAX021](./dax-perf-patterns.md#dax021-join-precomputed-key-sets-in-fe) |
| `DCOUNT` in xmSQL | `DISTINCTCOUNT`, including distinct count over known unique key | [DAX011](./dax-perf-patterns.md#dax011-test-distinctcount-alternatives), [DAX014](./dax-perf-patterns.md#dax014-use-countrows-for-recognized-keys) |
| Result changes with grouping/filter context, or repeated predicates appear | `ALLEXCEPT`; `ALL/REMOVEFILTERS + VALUES`; duplicate predicates; redundant key-set filters | [DAX012](./dax-perf-patterns.md#dax012-preserve-filters-deliberately), [DAX004](./dax-perf-patterns.md#dax004-remove-redundant-filters) |
| Unexpected joins or expanded bridge/M2M paths | bidirectional/M2M relationship in filter path; `TREATAS`/`CROSSFILTER` in measure | [DAX016](./dax-perf-patterns.md#dax016-test-relationship-overrides-locally) |

> No signal matches? Read all of §3 — patterns DAX001–DAX021 cover the full range.

### Sections 4–6 — Escalation Triggers

Only consult these sections if the corresponding signal is present. All require user approval before applying changes.

| Signal | Escalate To |
|--------|-------------|
| `__ValueFilterDM` in generated query | §4 → [QRY002](./dax-perf-patterns.md#qry002-eliminate-report-measure-filters-__valuefilterdm) |
| Groupby column is high-cardinality (e.g., `Calendar[Date]`) | §4 → [QRY003](./dax-perf-patterns.md#qry003-reduce-query-grain) |
| Tier 1 patterns exhausted; output change acceptable | §4 → [QRY001](./dax-perf-patterns.md#qry001-remove-unneeded-filters)–[QRY004](./dax-perf-patterns.md#qry004-remove-blank-suppression-changes-result-shape) |
| Few SE queries, low parallelism, clean xmSQL, high SE duration | §5/§6 → [data layout](./dax-perf-patterns.md#section-5-tier-3-model-optimization-patterns) |
| Many-to-many or bidirectional relationship overhead | §5 → [MDL001](./dax-perf-patterns.md#mdl001-many-to-many-relationship-optimization) |
| Direct Lake model + low parallelism or cold cache | §6 → [DL001](./dax-perf-patterns.md#dl001-v-ordering-delta-tables-for-direct-lake)–[DL002](./dax-perf-patterns.md#dl002-segment-size-and-parallelism) |

---

## Optimization Framework

### Tiers and Autonomy

| Tier | Scope | Autonomy |
|------|-------|----------|
| **Tier 1 — DAX Patterns** | Rewrite measure/UDF definitions | Auto-apply. Keep EVALUATE/grouping identical. |
| **Tier 2 — Query Structure** | Modify EVALUATE, grain, filters | Present recommendation. Wait for explicit user approval. |
| **Tier 3 — Model Changes** | Relationships, columns, agg tables, data types | High caution. Discuss trade-offs. Suggest model copy. Warn downstream risk. |
| **Tier 4 — Direct Lake** | OneLake layout, V-ordering, rowgroup sizing | High caution. Requires ETL/pipeline changes outside the model. |

**Success criteria — Tier 1:** Query duration improvement AND semantic equivalence (same row count, column count, data values).
**Success criteria — Tier 2/3/4:** Query duration improvement AND explicit user approval of output or structural changes.

### Requirements

- **Semantic model connection** — Any client that satisfies the Trace capture and Model metadata requirements below. See [Trace Capture Methods](#trace-capture-methods) for capability comparison across common clients.
- **Trace capture** — Ability to execute DAX queries with server timing trace capture. See [Trace Capture Methods](#trace-capture-methods).
- **Model metadata** — Ability to read measure definitions, function definitions, calculation group expressions, table metadata, and relationship metadata from the model.

### Trace Capture Methods

| Method | Scope | Capture mode | How you drive it | Notes |
|--------|-------|--------------|------------------|-------|
| **`powerbi-modeling-mcp`** | Local PBI Desktop + remote (Fabric XMLA) | Live trace subscription | Tool calls (agent-friendly) | Returns pre-calculated FE/SE split, peak memory, and result rows. |
| **TOM Trace API (ADOMD.NET / PowerShell)** | Local PBI Desktop + remote (Fabric XMLA) | Live trace subscription | PowerShell / .NET scripts | Subscribe to `QueryEnd`, `VertiPaqSEQueryEnd`, `VertiPaqSEQueryCacheMatch` and derive FE/SE manually (`FE = TotalDuration − union(VertiPaqSEQueryEnd intervals)`; SE wall-clock is the union of overlapping intervals, not the sum). Direct Lake databases are not exposed via the PBI Desktop local AS proxy — connect to the Fabric workspace XMLA endpoint instead. |
| **DAX Studio** | Local PBI Desktop + remote (Fabric XMLA) | Live trace subscription | Interactive UI | Server Timings pane shows pre-calculated FE/SE. Best for hands-on investigation. |
| **Fabric Workspace Monitoring** (`SemanticModelLogs` Eventhouse table) | Fabric workspaces (Workspace Monitoring enabled) | Logged events, queried after the fact | KQL queries against the Eventhouse | Per-row `OperationName`, `DurationMs`, `CpuTimeMs`; correlate events for one query via `OperationId`. Best for after-the-fact production analysis at scale; not suited for tight iterate-and-rerun loops. |

---

## Phase 1: Establish Baseline

### Step 1: Resolve All Measure and Function Definitions

Before optimizing, fully resolve every DAX expression in the query. Partial visibility leads to incorrect or incomplete optimizations.

1. **Identify measure references** in the user's query — any `[MeasureName]` pattern.
2. **Retrieve each measure's expression** — read the measure definition (name, table, DAX expression) from the model.
3. **Recursively resolve dependencies** — read each expression, find nested `[OtherMeasure]` calls, fetch those too.
4. **Retrieve user-defined functions** if referenced.
5. **Build a DEFINE block** that explicitly inlines all resolved measures and functions.
6. **Check for active calculation groups** — list all calculation groups in the model, retrieve their calculation item expressions. Note any that may be active in the query context as they affect query plans for every intercepted measure.

**Example:** If `[Profit Margin]` = `DIVIDE([Total Profit], [Total Revenue])`, retrieve all three definitions and build:

```dax
DEFINE
    MEASURE 'Sales'[Total Revenue] = SUM('Sales'[Revenue])
    MEASURE 'Sales'[Total Profit]  = SUM('Sales'[Revenue]) - SUM('Sales'[Cost])
    MEASURE 'Sales'[Profit Margin] = DIVIDE([Total Profit], [Total Revenue])

EVALUATE
SUMMARIZECOLUMNS ( 'Product'[Category], "Profit Margin", [Profit Margin] )
```

### Step 2: Gather Model Context

1. List all tables — understand table structure and storage modes (Import, DirectQuery, Direct Lake).
2. List all relationships — understand join paths and filter propagation.

This context helps distinguish model design issues (missing star schema, bidirectional relationships) from DAX expression problems.

### Step 3: Execute Baseline (1 warm-up + 2+ measured runs)

For each run:

1. **Clear VertiPaq cache** — clears the SE query cache only; columns stay resident.
   - Warm-up run: cold (on disk) → warm (resident).
   - Measured runs: **warm + no-cache** — the ideal optimization-test state.
2. **Execute with trace capture** — run the DAX query with server timing trace enabled.
3. **Derive key metrics** — Total Duration, FE/SE split, SE query count, peak memory, and result row count. See [Understanding FE vs. SE Metrics](#understanding-formula-engine-fe-vs-storage-engine-se-metrics) for derivation from trace events.
4. Record all metrics, save the full trace events, and save the baseline result data for semantic equivalence checks.

After all runs: discard the warm-up. Start with **2 measured runs**. If timings are close (for example, <20% spread), use the **fastest valid measured duration** as the baseline and record both runs. If the spread is wider, keep adding measured runs until the normal range is clear; discard only protocol-invalid runs (for example, cache not cleared), use the fastest valid duration, and record the full range.

**Isolating measures:** When a query has many measures and the trace is noisy, comment out all but one (or a small group), re-run, and compare. Repeat in groups to isolate which measures drive the majority of total duration.

### Step 4: Analyze Baseline

Apply **[Section 2: Trace Diagnostics](#section-2-reading-and-diagnosing-traces)** to interpret the metrics and events. Use the **Decision Guide** above to identify which Section 3 patterns to try first.

---

## Phase 2: Optimization Iterations

### Step 1: Select and Apply Optimizations

Using [Section 3 (Tier 1)](./dax-perf-patterns.md#section-3-tier-1-dax-optimization-patterns), start from trace identifiers when available; otherwise use the DAX-only fallback patterns as hypotheses. Apply one or more of DAX001–DAX021.

**CRITICAL:** Modify only the **measure definitions in the DEFINE block**. Do NOT change the EVALUATE clause or SUMMARIZECOLUMNS grouping columns. Query structure must stay identical to preserve semantic equivalence.

### Step 2: Execute and Compare

1. Clear the VertiPaq cache (returns the model to the warm + no-cache state — same condition as the baseline measured runs).
2. Execute the query with trace capture enabled.

**During iteration:** No warm-up is needed — columns are already resident from baseline. Clear the SE cache, execute **2 measured runs**, and use the fastest valid duration if timings are consistent. If the spread is wide, run additional measured attempts until normal performance is clear. Reserve the baseline protocol (warm-up + measured runs) for final confirmation against the original baseline.

**Evaluate:**
- **Improvement = (BaselineDuration − OptimizedDuration) / BaselineDuration × 100** using fastest valid measured durations.
- **Semantic equivalence:** Compare the CSV result from this run against the baseline CSV — same row count, same columns, same data values. If results differ, the change modified calculation semantics — revert it. Check this **immediately** after each iteration, not after multiple changes.

### Step 3: Iterate and Escalate

- **Meaningful improvement + semantically equivalent** → Success. "Meaningful" = exceeds the baseline's run-to-run noise band (e.g., baseline 1200/1280/1310 ms → 1200 ms is noise; 900 ms is real). Present to user; offer the optimized query as new baseline for further rounds (compound improvements are common).
- **Further rounds:** Re-run Phase 1 Steps 3–4 on the new baseline; re-analyze the new structure against the Decision Guide, as it may expose patterns that didn't apply before (fusion, materialization, etc.).
- **Within the noise band** → Try another Section 3 pattern, or combine patterns. Re-examine trace for other bottlenecks.
- **Results differ** → Revert; the optimization changed semantics. Try another approach.
- **Tier 1 exhausted** → Move to Phase 3 (Tier 2) with user approval. "Exhausted" = every signal-matching pattern tried (individually + combined), measures isolated for multi-measure queries, last 1–2 attempts at noise floor.

---

## Phase 3: Query Structure Changes (Tier 2 — User Approval Required)

> **STOP — Do not modify the query structure without explicit user approval.**

Consult **[Section 4: Tier 2 — Query Structure Patterns](./dax-perf-patterns.md#section-4-tier-2-query-structure-patterns)** (QRY001–QRY004).

Before applying any change:

1. Explain the specific change (e.g., "Group by YearMonth instead of Date reduces result rows from 365K to 12K").
2. Explain what changes in the output and what the user gains in performance.
3. Wait for explicit approval.
4. If approved, modify query structure, run the full baseline cycle, present results.

---

## Phase 4: Model and Data Layout Changes (Tier 3/4 — High Caution, User Approval Required)

> **STOP — Do not modify the model without explicit user approval.**

Consult **[Section 5: Tier 3 — Model Patterns](./dax-perf-patterns.md#section-5-tier-3-model-optimization-patterns)** (MDL001–MDL009) and **[Section 6: Tier 4 — Direct Lake](./dax-perf-patterns.md#section-6-tier-4-direct-lake-optimization-patterns)** (DL001–DL002).

Before proceeding:

1. Present the specific diagnosis and proposed model change.
2. Explain why the model design is causing the performance bottleneck.
3. Warn that model changes can break downstream reports and visuals.
4. Suggest creating a copy of the semantic model to experiment on.
5. Identify if upstream changes are required (Lakehouse tables, Warehouse views, Power Query transformations) — these cannot be done through semantic model tooling alone.
6. If approved, coordinate with the user's CI/CD process.
7. After applying changes, re-run the full baseline optimization workflow to measure impact.

---

## Error Handling

- **Connection failure** — Verify dataset name, workspace name, or XMLA endpoint. For Desktop, ensure Power BI Desktop is running and note the local port. For Service, verify XMLA read/write is enabled on the capacity.
- **Query syntax error** — Validate DAX syntax before executing.
- **Semantic equivalence failure** — Optimization changed calculation semantics. Review filter context, aggregation granularity, and CALCULATE filter arguments. Revert and try differently.
- **No improvement found** — Some queries are already well-optimized at the DAX level. Check whether the bottleneck is data layout (Phase 4) or query structure (Phase 3).
- **Trace events empty** — Ensure server timing / trace capture is enabled before executing the query. Verify the trace is subscribed to the correct event types (`QueryEnd`, `VertiPaqSEQueryEnd`, `VertiPaqSEQueryCacheMatch`).

---

## Section 1: How the Engine Works

### Query Processing Architecture

Every DAX query runs through two components: the **Formula Engine (FE)** and the **Storage Engine (SE)**.

The **FE** handles all DAX — branching logic, context transitions, complex arithmetic, measure evaluation. It is **single-threaded** and the bottleneck in most poorly written queries.

The **SE** reads compressed columnar data from VertiPaq. It is **multi-threaded** and very fast, but supports only a limited set of operations: the four basic arithmetic operators, GROUP BY, LEFT OUTER JOINs, and basic aggregations (SUM, COUNT, MIN, MAX, DISTINCTCOUNT).

For **DirectQuery models**, the data source serves as the SE role: the FE generates and pushes down SQL, trading network/source latency for in-memory scan cost.

**How they interact:**
- FE requests data via one or more SE scans; each result is a **datacache** (columns + aggregated values).
- Complex queries need multiple datacaches (e.g., one builds a filter set, one aggregates the fact).
- If the SE can't evaluate an expression natively → **callback** to FE row-by-row → that scan is effectively single-threaded.

The core principle of DAX optimization: **push as much work as possible into the SE, minimize SE scans, and eliminate callbacks entirely.**

---

### xmSQL: The Storage Engine Query Language

xmSQL is the human-readable representation of SE scan activity in trace events — it shows which tables are scanned, which columns are aggregated, which filters apply, and how joins resolve. Syntax resembles SQL with key differences:

**Implicit GROUP BY:** Every column in the SELECT list is automatically a grouping column — no GROUP BY keyword.

**Computed expressions:** Row-level calculations use a `WITH` block with `:=`, referenced in aggregations via `@`:
```
WITH $Expr0 := ( 'Sales'[UnitPrice] * 'Sales'[OrderQuantity] )
SELECT Product[Category], SUM ( @$Expr0 )
FROM Sales
    LEFT OUTER JOIN Product ON 'Sales'[ProductKey] = Product[ProductKey]
```

**Relationship joins are LEFT OUTER unless otherwise stated:** the many-side table is FROM, the one-side is joined in. Other internal forms (`INNER JOIN`, `REDUCED BY`, reverse joins) can also appear depending on the operation.

**Semi-join projections:** Appear as `DEFINE TABLE $Filter0 ... ININDEX` in xmSQL — an initial dimension scan builds a key index injected into the fact WHERE clause.

**Callbacks:** Occur whenever the SE must compute an expression that falls outside of VertiPaq's native capabilities. Forms include `CallbackDataID` (arbitrary expressions, most common) and specialized variants exposing individual FE functions (rounding, log/abs math). See [DAX002](./dax-perf-patterns.md#dax002-use-summarizecolumns-for-grouped-calculations), [DAX007](./dax-perf-patterns.md#dax007-convert-boolean-tests-without-if), [DAX008](./dax-perf-patterns.md#dax008-context-transition-in-iterator), [DAX018](./dax-perf-patterns.md#dax018-keep-iterator-division-se-native) for callback elimination patterns.

---

### Compression, Segments, and Parallelism

**Compression** determines scan speed. VertiPaq uses dictionary and run-length-style encodings to reduce scan work. For Direct Lake, source Delta/Parquet layout affects how quickly columns load into VertiPaq; V-Order improves RLE-friendly layout for read-heavy Power BI tables (see [DL001](./dax-perf-patterns.md#dl001-v-ordering-delta-tables-for-direct-lake)).

**Segments** are fixed-size column chunks — the unit of both compression and parallel execution. The SE assigns one CPU thread per segment, so segment count determines how many cores a scan can utilize.

**Parallelism:** A 32M-row table in 2 segments uses 2 threads; in 32 segments it uses all 16 available threads — a 4–8× speedup with zero DAX changes.

**Segment skew matters equally:** if one segment has 15M rows and the rest have 1M, the scan bottlenecks on the oversized segment. Segments must be evenly sized for parallelism to be effective.

**Diagnosing low parallelism:** The **SE Parallelism Factor** (StorageEngineCpuTime ÷ StorageEngineDuration) shows thread utilization. Values near 1.0 mean single-threaded execution; values of 8–16 indicate strong multi-core use. When a trace shows few SE queries (1–4), high SE Duration, Parallelism Factor ≈ 1.0, and clean xmSQL — the bottleneck is likely too few segments or skewed segment sizes. DAX changes are unlikely to help; use data layout instead (see [General Data Layout Best Practices](./dax-perf-patterns.md#section-5-tier-3-model-optimization-patterns) and [DL001–DL002](./dax-perf-patterns.md#section-6-tier-4-direct-lake-optimization-patterns)).

---

### SE Query Fusion

Fusion is the engine's ability to combine multiple SE scans into fewer scans. Two flavors:

- **Vertical fusion** merges multiple measure aggregations that share the same filter context into a single SE query. Three measures on the same fact table under the same filter = one scan instead of three. Gain scales with fact table size.
- **Horizontal fusion** merges SE queries that differ only in which value(s) of a column they filter. N separate fact scans collapse to one; the FE partitions the result.

**Why fusion breaks.** Fusion needs the competing SE requests to have compatible scan shapes — the same filter context for vertical fusion, compatible single-column filter differences for horizontal. Common triggers that break that:

- **FE chooses the branch** — SWITCH/IF between measures, or per-measure filter predicates that materialize separate `VAND` tuples → structurally different SE queries → see [DAX017](./dax-perf-patterns.md#dax017-align-scan-shape-with-boolean-multipliers)
- **Table- or range-valued filter** — time intelligence (DATESYTD, DATEADD, etc.) injects a per-measure date/range scan the SE can't fold in → see [DAX019](./dax-perf-patterns.md#dax019-move-time-windows-outside-sibling-measures)
- **Slicing column not in the groupby** — horizontal fusion can only merge slices the result groups by; absent that, scans stay separate
- **Runtime-computed filter value** — a predicate held in a variable is treated as dynamic and won't fuse
- **Calculation group items** — each item applies its own filter modification → structurally different SE query

**Trace diagnosis:** Same fact table + same joins across multiple SE queries → missed vertical fusion. Near-identical queries differing only by `WHERE` values → blocked horizontal fusion. See [Section 3](./dax-perf-patterns.md#section-3-tier-1-dax-optimization-patterns) and [Section 2 trace analysis](#section-2-reading-and-diagnosing-traces).

---

## Section 2: Reading and Diagnosing Traces

### Understanding Formula Engine (FE) vs. Storage Engine (SE) Metrics

These are the critical metrics for DAX optimization, derived from Analysis Services trace events.

| Metric | How to Derive | Description | Target |
|--------|--------------|-------------|--------|
| **Total Duration** | `QueryEnd.Duration` | End-to-end query time (ms) | Lower is better |
| **FE Duration** | Total Duration − SE wall-clock time | Single-threaded FE processing time (ms) — **the #1 bottleneck in most slow queries** | Lower is better |
| **SE Duration** | Union of overlapping `VertiPaqSEQueryEnd` intervals | Multi-threaded SE query time (ms) | Higher % of total is better |
| **SE Query Count** | Count of `VertiPaqSEQueryEnd` events | Number of SE scans generated | Fewer is better |
| **SE CPU Time** | Sum of all `VertiPaqSEQueryEnd.CpuTime` | Total CPU across all SE threads | Higher ratio to SE Duration is better |
| **SE Parallelism Factor** | SE CPU Time ÷ SE Duration | Thread utilization across all scans | Higher is better (>1 = multi-threaded) |
| **Cache Matches** | Count of `VertiPaqSEQueryCacheMatch` events | Cache hits (SE queries answered from memory) | Only relevant on warm cache |
| **Peak Memory (KB)** | From execution metrics summary | Memory consumed during query execution | Lower is better — high values signal excessive materializations |
| **SE Scan Row Count** | `volume` from `[Estimated size (volume, marshalling bytes): X, Y]` in `VertiPaqSEQueryEnd.TextData` | Rows materialized per SE scan | Large volumes signal excessive materialization — the SE is handing too many rows to the FE |
| **FE %** | FE Duration ÷ Total Duration × 100 | Percentage of time in formula engine | Lower is better |
| **SE %** | SE Duration ÷ Total Duration × 100 | Percentage of time in storage engine | Higher is better |

> **Net wall-clock:** SE Duration is the *union* of overlapping SE intervals — not the sum of individual durations. Three concurrent 100ms scans = ~100ms wall clock, not 300ms.

**Parallelism — aggregate vs. per-scan:** The aggregate parallelism factor is computed across all SE scans. Each individual scan has its own `CpuTime / Duration`. A healthy aggregate factor can mask a single unparallelized scan where `CpuTime ≈ Duration`.

**FE processing gaps:** FE Duration is the sum of all time intervals where no SE query was executing — gaps between SE events on the timeline.

### Analyzing Trace Events

Trace events are captured from the Analysis Services engine during query execution. Each event includes: `EventClass` (event type), `EventSubclass`, `TextData` (xmSQL or DAX), `Duration`, `CpuTime`, `StartTime`, `EndTime`.

**Key event types:**
- `VertiPaqSEQueryBegin` / `VertiPaqSEQueryEnd` — SE scan lifecycle. `Duration` and `CpuTime` are on the End event. `TextData` contains the xmSQL query.
- `VertiPaqSEQueryCacheMatch` — SE query answered from cache (no scan). Count these separately.
- `QueryBegin` / `QueryEnd` — Overall DAX query lifecycle. `Duration` on QueryEnd = total wall-clock time.
- `AggregateTableRewriteQuery` — Fired when the engine rewrites a query to use an aggregation table. `TextData` contains the rewritten query. Presence indicates the engine found and used an agg table hit — absence on an agg-enabled model means the query fell through to the detail table.

> **Filtering trace output:** Focus on the event types above. Ignore `VertiPaqScanInternal` subclass events — these duplicate the outer `VertiPaqScan` with internal detail (e.g., `DC_KIND="DENSE"`) and identical timing. Also ignore `CommandBegin`/`CommandEnd` (DAX execution wrapper, no diagnostic value) and `Error` events (only relevant when errors occur).

**Per-scan derived metrics (from VertiPaqSEQueryEnd events):**

Each `VertiPaqSEQueryEnd` event provides the raw data to derive per-scan diagnostics:

- **Rows scanned / Marshalling KB** — parse `[Estimated size (volume, marshalling bytes): X, Y]` at the end of `TextData`. X = rows, Y = bytes. Identifies excessive materializations on a specific scan.
- **Per-scan parallelism** — `CpuTime / Duration` for that individual scan. A ratio near 1.0 means single-threaded even if the aggregate `storageEngineCpuFactor` looks healthy.
- **Callbacks on slow scans** — scan `TextData` for `CallbackDataID`/`EncodeCallback` to confirm which specific SE query has the callback.

**Building an FE gap waterfall:**

FE processing occurs in the gaps *between* SE events. Use `StartTime`/`EndTime` offsets from `QueryBegin.StartTime` to build a timeline:
1. Gap between `QueryBegin` and the first SE `StartTime` → FE plan compilation
2. Gap between one SE `EndTime` and the next SE `StartTime` → FE processing block
3. Gap between the last SE `EndTime` and `QueryEnd.EndTime` → final FE assembly
4. Overlapping SE events → parallel SE execution; sequential non-overlapping → FE feeding results between scans
5. A large gap (>100ms) signals expensive FE computation — examine the SE query *before* the gap

### What to Look For

Scan for these signals in priority order when analyzing a slow query:

1. **Callbacks** — `CallbackDataID` or `EncodeCallback` in SE TextData. Fix first (DAX002, DAX007, DAX008, DAX018).
2. **High FE %** — FE doing too much work; usually paired with many short SE queries.
3. **High SE query count / repeated fact scans** — multiple SE queries hitting the same fact table with same joins but different WHERE clauses or aggregations → blocked fusion. See SE Query Fusion.
4. **Large materializations** — SE rows far exceed final result, or SE queries with no WHERE clause → FE filtering post-materialization instead of pushing to SE. See DAX009.
5. **Low parallelism factor** — near 1.0 on slow scans → data layout problem, not DAX. See Compression, Segments, and Parallelism.
6. **High KB per SE event** — wide intermediate tables; reduce columns or aggregate earlier.
7. **Two-step dimension pre-scans** — dimension-only SELECT followed by `where predicate` on the fact. Restructure query to collapse into one scan.
8. **Large semi-join index tables** — `DEFINE TABLE` + `ININDEX` or `WHERE ... IN` with hundreds of compound tuples (e.g., `(GroupByCol, FilterKey)` pairs). See DAX021.
9. **Missing aggregate table hit** — Model has agg tables configured but no `AggregateTableRewriteQuery` event in the trace → query fell through to the detail table. Check agg table mappings and query grain.

**Prioritization:** Callbacks → Large FE processing → SE query count (DAX) → parallelism and data volume (data layout). Target the highest-duration SE scan first — ignore 0ms cache-hit scans.

---

### DAX vs. Data Layout: Reading the Signal

**Many SE queries + high FE time + individually short SE scans → DAX problem**

Fusion is blocked, callbacks are present, or filters resolve iteratively. Fix the DAX — see [Section 3](./dax-perf-patterns.md#section-3-tier-1-dax-optimization-patterns) and [Section 4](./dax-perf-patterns.md#section-4-tier-2-query-structure-patterns). *Example:* 109 SE queries, 30% FE → after restructuring: 4 SE queries, 1% FE.

**Few SE queries + low FE time + high SE duration + low parallelism → Data layout problem**

The DAX is clean but SE scans are slow due to insufficient segments or poor compression. DAX changes will not help — see [Section 5](./dax-perf-patterns.md#section-5-tier-3-model-optimization-patterns) / [Section 6](./dax-perf-patterns.md#section-6-tier-4-direct-lake-optimization-patterns) (General Data Layout Best Practices, DL001–DL002).

---

## Further Reading

- [Analysis Services trace events](https://learn.microsoft.com/analysis-services/trace-events/analysis-services-trace-events)
- [Horizontal fusion in Power BI and Analysis Services](https://powerbi.microsoft.com/en-us/blog/announcing-horizontal-fusion-a-query-performance-optimization-in-power-bi-and-analysis-services/)
- [Understand Direct Lake query performance](https://learn.microsoft.com/fabric/fundamentals/direct-lake-understand-storage)

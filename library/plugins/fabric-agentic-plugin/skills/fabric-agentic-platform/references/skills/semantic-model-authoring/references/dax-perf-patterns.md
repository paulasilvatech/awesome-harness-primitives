# DAX Performance Pattern Catalog

Use this on demand after [dax-perf-decision-guide.md](./dax-perf-decision-guide.md) identifies candidate patterns. Patterns are candidate optimizations, not guarantees; validate trace/runtime and semantic equivalence before keeping changes.

## Section 3: Tier 1 DAX Optimization Patterns

> **Autonomy: Auto-apply freely. Modify only measure/UDF definitions in the DEFINE block. Keep EVALUATE and SUMMARIZECOLUMNS grouping identical.**

> **Candidate optimizations, not guarantees:** Each pattern is a hypothesis to test. Cardinality, data layout, relationships, filters, storage mode, and engine folding can make a rewrite help, do nothing, or hurt. Apply one or more matching patterns, validate trace/runtime and semantic equivalence after each step, and continue iterating because one rewrite can expose the next optimization opportunity. Keep changes that help; revert changes that do not.

> **Prefer SUMMARIZECOLUMNS:** Fully supported inside measure definitions — earlier restrictions no longer apply. Use it to replace `ADDCOLUMNS`/`SUMMARIZE` patterns (DAX002), pre-materialize context transitions before iterating (DAX006), and cache repeated evaluations into a single virtual table (DAX003). Prefer it over `ADDCOLUMNS(VALUES(...), ...)` unless a specific scenario prevents it.

### DAX001: Use Simple Column Filter Predicates as CALCULATE Arguments

**Identifier:** `FILTER(Table, ...)` as a filter argument, or combined predicates. Verify trace; simple cases can fold to `WHERE`.

**Action:** Keep filters column-scoped. Replace table filters with boolean predicates, and split `&&` into separate filter arguments.

**Anti-pattern — FILTER with table expression uses an iterator:**
```dax
CALCULATE(
    SUM('Sales'[Amount]),
    FILTER('Product', 'Product'[Category] = "Electronics")
)
```

**Preferred — column predicate, no iterator:**
```dax
CALCULATE(
    SUM('Sales'[Amount]),
    KEEPFILTERS( 'Product'[Category] = "Electronics")
)
```

**Anti-pattern — `&&` joins predicates into a single iterator argument:**
```dax
CALCULATETABLE( 'Sales', 'Sales'[Region] = "West" && 'Sales'[Amount] > 1000 )
```

**Preferred — separate predicates for better query plan:**
```dax
CALCULATETABLE( 'Sales', 'Sales'[Region] = "West", 'Sales'[Amount] > 1000 )
```

---

### DAX002: Use SUMMARIZECOLUMNS for Grouped Calculations

**Identifier:** grouped calculation built with `ADDCOLUMNS`/`SUMMARIZE`. Compare trace against a direct `SUMMARIZECOLUMNS` shape.

**Action:** Use `SUMMARIZECOLUMNS` for grouping + calculation when row shape and filter semantics stay identical.

**Anti-patterns:**
```dax
SUMMARIZE ( 'Sales', 'Sales'[ProductKey], "Total Profit", [Profit] )
ADDCOLUMNS ( SUMMARIZE ( 'Sales', 'Sales'[ProductKey] ), "Total Profit", [Profit] )
ADDCOLUMNS ( 'Sales', "Total Profit", CALCULATE ( [Profit] ) )
ADDCOLUMNS ( VALUES('Sales'[ProductKey]), "Total Profit", [Profit] )
```

**Preferred:**
```dax
SUMMARIZECOLUMNS ( 'Sales'[ProductKey], "Total Profit", [Profit] )
```

---

### DAX003: Cache Repeated Expressions in Variables

**Identifier:** repeated measure or expression references. Verify with FE time, repeated SE requests, or cache matches.

**Action:** Cache repeated or row-independent expressions in variables at the smallest safe scope.

**Anti-pattern — repeated measure reference:**
```dax
VAR TotalA = [Sales Amount] * 1.1
VAR TotalB = [Sales Amount] * 0.9
VAR TotalC = [Sales Amount] + 1000
```

**Preferred:**
```dax
VAR _SalesAmount = [Sales Amount]
VAR TotalA = _SalesAmount * 1.1
VAR TotalB = _SalesAmount * 0.9
VAR TotalC = _SalesAmount + 1000
```

**Anti-pattern — same measure iterated twice:**
```dax
VAR A = SUMX ( VALUES('Sales'[ProductKey]), [Total Sales] )
VAR B = AVERAGEX ( VALUES('Sales'[ProductKey]), [Total Sales] )
```

**Preferred — materialize once:**
```dax
VAR Base = SUMMARIZECOLUMNS ( 'Sales'[ProductKey], "@TotalSales", [Total Sales] )
VAR A = SUMX ( Base, [@TotalSales] )
VAR B = AVERAGEX ( Base, [@TotalSales] )
```

**Anti-pattern — context-independent expression inside iterator:**
```dax
SUMX( 'Sales', 'Sales'[Quantity] * [Average Price] * 1.1 )
// [Average Price] doesn't change per row
```

**Preferred:**
```dax
VAR _AvgPrice = [Average Price]
RETURN SUMX( 'Sales', 'Sales'[Quantity] * _AvgPrice * 1.1 )
```

---

### DAX004: Remove Redundant Filters

**Identifier:** repeated predicates, duplicate filter tables, or redundant key-set filters.

**Action:** Keep one copy of each filter. Remove key sets or variables that restate an active predicate.

**Anti-pattern — same predicate in CALCULATE + FILTER:**
```dax
CALCULATE(
    SUM('Sales'[Amount]),
    'Sales'[Year] = 2023,
    FILTER('Sales', 'Sales'[Year] = 2023)
)
```

**Anti-pattern — redundant filter variable:**
```dax
VAR FilteredValues = CALCULATETABLE ( DISTINCT ( 'Table'[Key1] ), 'Table'[Amount] > 1000 )
VAR Result =
    CALCULATETABLE (
        SUMMARIZECOLUMNS ( 'Table'[Key2], "TotalQty", SUM ( 'Table'[Quantity] ) ),
        'Table'[Amount] > 1000,
        'Table'[Key1] IN FilteredValues  -- redundant: already filtered by Amount > 1000
    )
```

**Preferred — single filter, no duplication:**
```dax
CALCULATE( SUM('Sales'[Amount]), 'Sales'[Year] = 2023 )

VAR Result =
    CALCULATETABLE (
        SUMMARIZECOLUMNS ( 'Table'[Key2], "TotalQty", SUM ( 'Table'[Quantity] ) ),
        'Table'[Amount] > 1000
    )
```

---

### DAX005: Move Complex SUMMARIZE Inputs to CALCULATETABLE

**Identifier:** `SUMMARIZE` starts from a filtered or computed table expression.

**Action:** Keep grouping simple; move filters to an outer `CALCULATETABLE`.

**Anti-pattern:**
```dax
SUMMARIZE(
    CALCULATETABLE('Sales', 'Sales'[Year] = 2023, 'Customer'[Segment] = "Enterprise"),
    'Sales'[CustomerKey],
    "DistinctStores", DISTINCTCOUNT('Sales'[StoreKey])
)
```

**Preferred:**
```dax
CALCULATETABLE(
    SUMMARIZECOLUMNS(
        'Sales'[CustomerKey],
        "DistinctStores", DISTINCTCOUNT('Sales'[StoreKey])
    ),
    'Sales'[Year] = 2023,
    'Customer'[Segment] = "Enterprise"
)
```

---

### DAX006: Precompute Iterator Inputs with SUMMARIZECOLUMNS

**Identifier:** iterator over `VALUES(...)` with `CALCULATE` or measure evaluation per row.

**Action:** Precompute iterator rows and values with `SUMMARIZECOLUMNS`, then iterate the materialized result.

**Anti-pattern:**
```dax
SUMX(
    VALUES('Product'[Attribute]),
    CALCULATE(SUM('Sales'[Amount]))
)
```

**Preferred:**
```dax
SUMX(
    SUMMARIZECOLUMNS(
        'Product'[Attribute],
        "@Amount", SUM('Sales'[Amount])
    ),
    [@Amount]
)
```

---

### DAX007: Convert Boolean Tests Without IF

**Identifier:** row-by-row `IF`/`SWITCH` boolean conversion. Trace may show `CallbackDataID` when it cannot fold.

**Action:** Convert boolean-to-1/0 tests without `IF`; use a predicate + `COUNTROWS` when counting rows.

**Anti-pattern:**
```dax
SUMX(
    'Products',
    IF([Sales Amount] > 10000000, 1, 0)
)
```

**Preferred:**
```dax
SUMX(
    'Products',
    INT([Sales Amount] > 10000000)
)
```

**Count rows case:** eliminate the iterator and callback with a simple predicate.
```dax
-- Anti-pattern: iterator + conditional = callback
SUMX( 'Sales', IF('Sales'[Amount] > 1000, 1, 0) )

-- Preferred: native SE aggregation, no iterator, no callback
CALCULATE( COUNTROWS('Sales'), 'Sales'[Amount] > 1000 )
```

---

### DAX008: Context Transition in Iterator

**Identifier:** measure reference or `CALCULATE` inside an iterator. Verify with FE time or repeated short SE events.

**Action:** Reduce or remove iterator context transitions:

1. **Remove it completely:**
```dax
// Instead of: SUMX( 'Sales', [Sales Amount] )
// Use: SUMX( 'Sales', 'Sales'[Unit Price] * 'Sales'[Quantity] )
```

2. **Iterate over a narrow key table:**
```dax
// Instead of: SUMX( 'Customer', [Total Sales] )
// Use: SUMX( VALUES('Customer'[CustomerKey]), [Total Sales] )
```

3. **Reduce cardinality before iteration:**
```dax
// Instead of: SUMX( 'Customer', [Total Sales] * 'Customer'[DiscountRate] )
// Use only when grouping customers by DiscountRate preserves the result:
SUMX(
    VALUES('Customer'[DiscountRate]),
    [Total Sales] * 'Customer'[DiscountRate]
)
```

---

### DAX009: Externalize SUMMARIZECOLUMNS Filters

**Identifier:** filter arguments inside `SUMMARIZECOLUMNS`. Verify materialization and result shape.

**Action:** Move filters to a wrapping `CALCULATETABLE`.

**Anti-pattern:**
```dax
SUMMARIZECOLUMNS (
    'Table'[Column],
    TREATAS ( { "Value" }, 'Table'[FilterColumn] ),
    "@Calculation", [Measure]
)
```

**Preferred:**
```dax
CALCULATETABLE (
    SUMMARIZECOLUMNS (
        'Table'[Column],
        "@Calculation", [Measure]
    ),
    'Table'[FilterColumn] = "Value"
)
```

---

### DAX010: Push Table Filters with CALCULATETABLE

**Identifier:** standalone `FILTER(...)` table where filter context could be applied directly. Simple cases can fold to `WHERE`.

**Action:** Use `CALCULATETABLE` so the filter applies before the table is consumed.

**Anti-pattern:**
```dax
FILTER( 'Sales', 'Sales'[Year] = 2023 )
```

**Preferred:**
```dax
CALCULATETABLE( 'Sales', 'Sales'[Year] = 2023 )
```

---

### DAX011: Test DISTINCTCOUNT Alternatives

**Identifier:** `DISTINCTCOUNT`; trace cue is `DCOUNT`, especially when cells have different filter sets.

**Action:** Benchmark `DISTINCTCOUNT` against `SUMX(DISTINCT(), 1)`; keep only if equivalent and faster for the target visual.

**Storage Engine Bound:**
```dax
DISTINCTCOUNT('Sales'[CustomerKey])
```

**Formula Engine Bound (sometimes faster):**
```dax
SUMX(DISTINCT('Sales'[CustomerKey]), 1)
```

---

### DAX012: Preserve Filters Deliberately

**Identifier:** `ALLEXCEPT` or `REMOVEFILTERS/ALL + VALUES` used to preserve filters. Validate across report groupings.

**Action:** Choose the preservation form that matches how the retained value is filtered.

**Use `ALLEXCEPT` only when the preserved column is already directly filtered:**
```dax
CALCULATE( [Total Sales], ALLEXCEPT('Sales', 'Sales'[Region]) )
```

**Keep `ALL/REMOVEFILTERS + VALUES` when the preserved value may be cross-filtered by another column:**
```dax
CALCULATE( [Total Sales], REMOVEFILTERS('Sales'), VALUES('Sales'[Region]) )
```

---

### DAX013: Keep Branch Measures SE-Friendly

**Identifier:** `SWITCH`/`IF` chooses between measure branches. Verify FE time and unused branch work in trace/query plan.

**Action checklist:**
- Read the selector column directly filtered by the slicer/query; avoid hidden sort keys unless filtered directly.
- Keep branches SE-native: one simple aggregation or one fact iterator with row-level arithmetic, not multiple separate aggregations.
- Use one numeric type across branches; cast mixed branches explicitly.
- Avoid iterator context transition; lift row-independent measures into variables.

For disconnected parameter tables, prefer field parameters or aligning the selector/filter column before making model metadata changes.

---

### DAX014: Use COUNTROWS for Recognized Keys

**Identifier:** `DISTINCTCOUNT` over a recognized unique key. Trace may compile to `COUNT`; verify before rewriting.

**Action:** Prefer `COUNTROWS` only when the counted column is a recognized unique key.

- Safe candidates: table key, or one-side key of a regular active relationship.
- Test first: inactive relationships, `USERELATIONSHIP`, or unmarked keys.
- Non-key/high-cardinality bottleneck → see DAX011.

---

### DAX015: Iterate at the Required Grain

**Identifier:** iterator scans more rows than a repeated measure/context-transition dependency requires. Do not use for simple SE-native column sums.

**Action:** Iterate the lowest distinct grain only when it removes repeated measure or context-transition work.

**Anti-pattern:**
```dax
-- 100K customers but only 5 distinct DiscountRate values → 100K context transitions
SUMX( 'Customer', CALCULATE(SUM('Sales'[Amount])) * 'Customer'[DiscountRate] )
```

**Preferred:**
```dax
-- 5 iterations instead of 100K
SUMX( VALUES('Customer'[DiscountRate]), CALCULATE(SUM('Sales'[Amount])) * 'Customer'[DiscountRate] )
```

---

### DAX016: Test Relationship Overrides Locally

**Identifier:** bidirectional/M2M filter path, or `TREATAS`/`CROSSFILTER` override. Verify joins in xmSQL.

**Action:** Test alternate filter propagation in the measure with `TREATAS`/`CROSSFILTER` before changing the model.

**Example — replace bidirectional bridge with explicit filter:**
```dax
CALCULATE(
    SUM('Sales'[Amount]),
    CROSSFILTER('Customer'[CustomerKey], 'CustomerBridge'[CustomerKey], NONE),
    TREATAS(VALUES('CustomerBridge'[CustomerKey]), 'Customer'[CustomerKey])
)
```

---

### DAX017: Align Scan Shape with Boolean Multipliers

**Identifier:** sibling measures differ only by per-measure filters on the same fact. Trace may show near-identical SE scans differing only by `WHERE` values.

**Action:** Move the per-measure filter into a boolean multiplier so competing SE scans can share shape; verify fusion in trace.

```dax
-- Anti-pattern: separate SE query per measure
CALCULATE( SUM('Sales'[Amount]), 'Product'[Category] = "Bikes" )
CALCULATE( SUM('Sales'[Amount]), 'Date'[Date] = _dateAnchor )
CALCULATE( MAX('Sales'[DateKey]),  'Sales'[Metric] <> 0 )

-- Fix: boolean multiplier — structurally similar SE queries can fuse; verify in trace
SUMX( KEEPFILTERS(ALL('Product'[Category])), CALCULATE(SUM('Sales'[Amount])) * ('Product'[Category] = "Bikes") )
SUMX( KEEPFILTERS(ALL('Date'[Date])),        CALCULATE(SUM('Sales'[Amount])) * ('Date'[Date] = _dateAnchor) )
MAXX( ALL('Date'[Date]),                     CALCULATE(MAX('Sales'[DateKey])) * INT(NOT ISBLANK(CALCULATE(SUM('Sales'[Metric])))) )
```

- `KEEPFILTERS` preserves external context; column in the groupby → detail cells iterate 1 row.
- Best for additive (`SUM`-style) aggregations.
- Validate `MIN`/`MAX`/`AVERAGE`: injected 0 values can corrupt the result.
- BLANK caveat: returns 0 instead of BLANK when no data exists; wrap if downstream `ISBLANK()` checks matter.

---

### DAX018: Keep Iterator Division SE-Native

**Identifier:** `DIVIDE()` inside an iterator. Trace may show `CallbackDataID` when it cannot fold.

**Action:** Use `/` only when the denominator is known non-zero; otherwise pre-filter zero denominators first.

**Anti-pattern:**
```dax
SUMX('Fact', 'Fact'[BaseAmount] * DIVIDE(RELATED('Items'[Discount]), RELATED('Items'[LocationAdjustment])))
```

**Preferred:**
```dax
SUMX('Fact', 'Fact'[BaseAmount] * (RELATED('Items'[Discount]) / RELATED('Items'[LocationAdjustment])))
```

---

### DAX019: Move Time Windows Outside Sibling Measures

**Identifier:** sibling measures each apply time-window filters. Verify whether trace shows separate SE scans.

**Action:** Keep base measures time-window free; apply TI once in the outer `CALCULATE`.

> **Custom time predicates:** `CALCULATE(expr, Column = _var)` does not match this rule; see **DAX017**.

**Anti-pattern — each measure applies TI independently (no fusion):**
```dax
MEASURE 'Sales'[Revenue YTD] = CALCULATE ( [Revenue], DATESYTD('Date'[Date]) )
MEASURE 'Sales'[Cost YTD]    = CALCULATE ( [Cost],   DATESYTD('Date'[Date]) )
MEASURE 'Sales'[Margin YTD] =
    [Revenue YTD] - [Cost YTD]
```

**Preferred — base measures fuse, TI applied once:**
```dax
MEASURE 'Sales'[Margin YTD] =
    CALCULATE ( [Revenue] - [Cost], DATESYTD ( 'Date'[Date] ) )
```

---

### DAX020: Keep Slice Measures Fusion-Friendly

**Identifier:** slice measures differ only by simple filters or dynamic values. Verify whether trace fuses or separates scans.

**Action:** Keep slice measures simple and literal; lift time-intelligence or dynamic filters to the combining measure.

**Anti-pattern — TI inside each slice measure (no fusion):**
```dax
MEASURE 'Sales'[Bikes YTD]       = CALCULATE ( SUM('Sales'[Amount]), 'Product'[Category] = "Bikes",       DATESYTD('Date'[Date]) )
MEASURE 'Sales'[Accessories YTD] = CALCULATE ( SUM('Sales'[Amount]), 'Product'[Category] = "Accessories", DATESYTD('Date'[Date]) )
```

**Preferred — slice measures fuse, TI applied once:**
```dax
MEASURE 'Sales'[Bikes]       = CALCULATE ( SUM('Sales'[Amount]), 'Product'[Category] = "Bikes" )
MEASURE 'Sales'[Accessories] = CALCULATE ( SUM('Sales'[Amount]), 'Product'[Category] = "Accessories" )
MEASURE 'Sales'[Combined YTD] = CALCULATE ( [Bikes] + [Accessories], DATESYTD('Date'[Date]) )
```

- Variable-driven slicers: leave base measures filter-free; put the dynamic predicate on the outer measure.
- Sliced column not in the groupby → see DAX017.

---

### DAX021: Join Precomputed Key Sets in FE

**Identifier:** computed key set re-filters the same fact via `TREATAS`/`IN`. Trace cue is large `IN`/`INB`; `ININDEX` or compound tuples can also appear.

**Action:** Precompute both aggregations at the shared key grain, then join in FE.

- Avoid pushing computed key sets back to the fact scan with `TREATAS`/`IN`.
- Both sides must keep a shared lineage column for `NATURALINNERJOIN`.

**Anti-pattern — TREATAS pushes key set back to SE, compounded by outer groupby:**
```dax
VAR _FilteredAgg =
    CALCULATETABLE (
        ADDCOLUMNS ( VALUES ( 'Fact'[Key] ), "@Agg1", [Measure] ),
        'Dim'[Filter] = "X"
    )
VAR _Qualifying = FILTER ( _FilteredAgg, [@Agg1] > 1000000 )
VAR _Result =
    CALCULATE (
        [Measure],
        TREATAS ( SELECTCOLUMNS ( _Qualifying, "K", 'Fact'[Key] ), 'Fact'[Key] )
    )
```

**Preferred — both aggregations pre-computed, joined in FE:**
```dax
VAR _FilteredAgg =
    CALCULATETABLE (
        ADDCOLUMNS ( VALUES ( 'Fact'[Key] ), "@Agg1", [Measure] ),
        'Dim'[Filter] = "X"
    )
VAR _Qualifying = FILTER ( _FilteredAgg, [@Agg1] > 1000000 )
VAR _UnfilteredAgg =
    ADDCOLUMNS ( VALUES ( 'Fact'[Key] ), "@Agg2", [Measure] )
VAR _Joined = NATURALINNERJOIN ( _Qualifying, _UnfilteredAgg )
VAR _Result = SUMX ( _Joined, [@Agg2] )
```

> **Goal:** replace the final key-set fact scan with precomputed tables and an FE join. Keep only if trace/runtime improves.

---

## Section 4: Tier 2 Query Structure Patterns

> **STOP — Requires user approval before applying any change. Explain the impact on query output and wait for explicit confirmation.**

> **Scope: Desktop-Achievable Changes Only**
>
> Every Tier 2 recommendation must map to an action the report author can perform in Power BI Desktop's UI. The agent optimizes the *generated* DAX query, but the user implements changes through the Desktop interface — not by editing DAX directly in the query pane. Examples of valid changes:
> - **Changing the axis/groupby field** (e.g., swap `Calendar Date` for `Calendar Month` on a visual axis)
> - **Removing or adding visual-level filters** (e.g., drop an unneeded slicer selection)
> - **Changing filter values** (e.g., narrow a date range filter)
> - **Removing measure value filters** (e.g., remove a "Top N" or "> threshold" filter from a visual)
> - **Changing aggregation type** on a column (e.g., Sum → Average)

### QRY001: Remove Unneeded Filters

Every filter adds a `WHERE` clause in xmSQL and may force an extra SE join. Users often apply slicer or visual-level filters that don't affect the calculation being optimized.

**Detection:** `WHERE` clauses on columns not used in the measure logic, or filter variables that restrict to a single value (e.g., `Currency[Code] = "USD"` in a USD-only model).

**Fix:** Remove filters one at a time and re-run; if the result doesn't change, the filter is unneeded. Filters needed across all visuals → push to the data source (model-level — see [Section 5](#section-5-tier-3-model-optimization-patterns)).

```dax
-- Before: filter on Currency adds an SE join for no benefit
SUMMARIZECOLUMNS (
    'Product'[Category],
    KEEPFILTERS ( TREATAS ( {"USD"}, 'Currency'[Code] ) ),
    "Revenue", [Total Revenue]
)

-- After: filter removed, same result, one fewer SE join
SUMMARIZECOLUMNS ( 'Product'[Category], "Revenue", [Total Revenue] )
```

---

### QRY002: Eliminate Report Measure Filters (__ValueFilterDM)

When a visual filters on a measure value (e.g., "Revenue > 1M"), Power BI generates a `__ValueFilterDM` variable that can evaluate the measure twice — once for the filter check, once for display.

**Detection:** `__ValueFilterDM` in the generated query.

**Fix:** Move the threshold into the measure itself — return BLANK below the cutoff. SUMMARIZECOLUMNS auto-drops blank rows, achieving the same visual result in one pass:
```dax
MEASURE 'Sales'[Total Revenue Filtered] =
    VAR __Rev = [Total Revenue]
    RETURN IF ( __Rev > 1000000, __Rev )
```

---

### QRY003: Reduce Query Grain

Grouping by a high-cardinality column (e.g., `Calendar[Date]` → 365 rows) when the user only needs monthly data (12 rows) inflates SE row count ~30×.

**Detection:** Groupby on a date or high-cardinality column producing far more rows than the visual needs.

**Option A — coarser groupby:**
```dax
-- Daily → monthly
SUMMARIZECOLUMNS ( 'Calendar'[YearMonth], "Revenue", [Total Revenue] )
```

**Option B — period-end axis + measure pin** (show period-end snapshot instead of full-period aggregate):

Requires a period-end column in the date table (e.g., `Calendar[MonthEndDate]`). User changes the visual axis to it, then pins the measure to that date:
```dax
-- User changes axis from Calendar[Date] to Calendar[MonthEndDate]
-- Measure pins CALCULATE to the period-end date to return that day's value only
MEASURE 'Sales'[Active Customers] =
    CALCULATE (
        DISTINCTCOUNT ( 'Sales'[CustomerID] ),
        'Calendar'[Date] = MAX ( 'Calendar'[MonthEndDate] )
    )
```
> Without the pin, grouping by `MonthEndDate` aggregates all days in the month instead of returning the single-day value.

**Option C — return BLANK for non-boundary dates** (keeps all dates in groupby but only computes on end-of-month):
```dax
MEASURE 'Sales'[Revenue EOM] =
    IF ( MAX('Calendar'[Date]) = EOMONTH(MAX('Calendar'[Date]), 0), [Total Revenue] )
```

**Option D — daily additive measure approximated at coarser grain** (divide monthly total by days in month):
```dax
MEASURE 'Sales'[Daily Avg Revenue] =
    DIVIDE (
        [Total Revenue],
        DAY ( EOMONTH ( MAX('Calendar'[Date]), 0 ) )
    )
```

---

### QRY004: Remove BLANK Suppression (Changes Result Shape)

`+ 0`, `IF(ISBLANK([M]), 0, [M])`, or `COALESCE(..., 0)` force SUMMARIZECOLUMNS to evaluate every groupby combination — including rows with no data — inflating the result set.

**Detection:** `+ 0`, `IF(ISBLANK(...))`, or `COALESCE(..., 0)` appended to measures.

**Anti-pattern:**
```dax
MEASURE 'Sales'[Revenue] = SUM ( 'Sales'[SalesAmount] ) + 0
```

**Preferred:**
```dax
MEASURE 'Sales'[Revenue] = SUM ( 'Sales'[SalesAmount] )
```

**If zeros are required selectively**, conditionally add 0 where it makes sense:
```dax
MEASURE 'Sales'[Revenue] =
    VAR _ForceZero = NOT ISEMPTY ( 'Sales' )
    RETURN [Sales Amount] + IF ( _ForceZero, 0 )
```


## Section 5: Tier 3 Model Optimization Patterns

> **STOP — Requires user approval before applying any change. Warn that model changes can break downstream reports. Suggest working on a model copy. Apply changes through whatever semantic-model authoring path is already in use; upstream source changes (Lakehouse, Warehouse, Power Query) must be coordinated with the user's data engineering or pipeline workflow.**

### General Data Layout Best Practices

Data layout decisions affect performance at the source level — before DAX, before the SE. Apply after exhausting DAX and query structure optimizations; changes here require ETL or pipeline modifications. Apply to both Import and Direct Lake.

1. **Remove unused columns and filter rows at the source.**
2. **Drop all-null/all-zero fact rows** that never contribute to results.
3. **Move low-cardinality string attributes off the fact table** into dimensions with integer keys.
4. **Partition on high-filter columns** (DateKey, TenantKey) so the engine skips entire files. Use **Z-order clustering** when partitioning creates too many small files.
5. **Presort on the most filtered/grouped column first** (e.g., DateKey, then ProductKey). RLE compression improves dramatically when values cluster into longer runs per segment.
6. **Use optimal data types.** See MDL003.

---

### MDL001: Many-to-Many Relationship Optimization

Bridge tables create expanded tables the engine materializes every query. The right layout depends on filter paths, bridge cardinality, and RLS. Test each option. Scenario: `User` (security), `Customer` (dimension), `UserCustomer` (bridge), `Fact`.

**A — Canonical (bidir bridge):** `User 1──* UserCustomer *──bidir──1 Customer 1──* Fact`
Customer filters Fact directly; bridge only traversed for User. Best when User is rarely a slicer alongside Customer. Bidir causes high FE cost when both filter together.

**B — M2M bridge to fact (no bidir):**
```
User 1──* UserCustomer *──1 Customer
                │
                *──M2M──* Fact
```
Both dims always filter through bridge M2M. Best when consistent query times matter more than peak Customer-only performance.

**C — Optimized hybrid:** `User 1──* UserCustomer *──M2M──* Fact *──1 Customer`
Customer filters Fact directly; User filters through bridge M2M. No bidir. Best general-purpose layout. Use inactive relationship + `USERELATIONSHIP` if you need Customer↔UserCustomer cross-queries.

**D — Pre-computed combination key:** `User 1──* UserCombinations *──M2M──* Fact *──1 Customer`
ETL assigns a surrogate key per unique set of customers a user can access — users with identical access share one key. Best when bridge is very large or many users share the same access patterns.

---

### MDL002: Star Schema Conformance

Snowflake schemas force multiple SE joins per query. Flatten dimension chains into a single wide dimension to reduce join depth and enable better fusion.

`Sales ──* Product ──* Subcategory ──* Category` → `Sales ──* Product [ProductKey, ProductName, Subcategory, Category]`

---

### MDL003: Column Cardinality and Data Type Optimization

High-cardinality columns inflate dictionary size and segment memory.

- **Integer keys over string keys:** Replace `"PROD-001234"` with integer surrogates.
- **Reduce timestamp precision:** `DateTime` → `Date` when queries only group by date.
- **Bin continuous values:** 50K distinct decimals → binned ranges if measure logic allows.
- **Split high-cardinality columns:** `FullAddress` (100K distinct) → `City`, `State`, `Zip`.

---

### MDL004: Aggregation Table Strategies

Pre-summarized Import tables intercept SE queries before they hit large DQ facts. Aggregate Awareness redirects automatically — no DAX changes.

**Setup:** `GROUP BY [FKs], SUM([Metrics])` → load as Import → connect to same dimensions → map in Manage Aggregations as `SUM OF [FactTable[Column]]`. Fact tables must be DQ.

**Filtered Aggs (hot/cold split):** Import only recent data (e.g., last 3 months). 95%+ queries served from Import.

---

### MDL005: Pre-Compute Period Comparison Columns

Period-over-period calcs (YoY, MoM) require two SE scans. Pre-computing prior-period values as physical columns on the fact row reduces it to one scan.

**Before (two scans):**
```dax
YoY = SUM ( 'Fact'[Sales] ) - CALCULATE ( SUM ( 'Fact'[Sales] ), SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
```
**After (one scan):**
```dax
YoY = SUM ( 'Fact'[Sales] ) - SUM ( 'Fact'[SalesLY] )
```

Wider fact table, but eliminates the TI scan entirely. Best for fixed period comparisons on large DQ tables.

---

### MDL006: Row-Based Time Intelligence Table

DAX TI functions break vertical fusion — each period measure gets its own SE query. A row-based TI table pre-materializes all periods as data rows so all period measures fuse into a single SE scan.

**Table:** `Period` (slicer label), `Date` (actual dates → relationship to fact), `AxisDate` (x-axis anchor). Relate via M2M to Fact or BiDir through Calendar.

---

### MDL007: Eliminate Referential Integrity Violations

Fact FKs with no matching dimension row prevent inner-join rewriting for SWITCH/multi-measure patterns.

**Detection:**
```dax
SELECT [Dimension_Name], [RIVIOLATION_COUNT]
FROM $SYSTEM.DISCOVER_STORAGE_TABLES
WHERE [RIVIOLATION_COUNT] > 0
```

**Fix:** Add an "Unknown" catch-all row to the dimension and map missing foreign keys in fact to "Unknown" record.

---

### MDL008: Replace SEARCH/FIND Filters with Pre-Computed Boolean Columns

`SEARCH()`/`FIND()` in filters forces row-by-row string scanning. Pre-compute the result as a boolean column (cardinality 2, ~1 bit/row) for pure columnar access. Generalizes to any fixed-value logical test — date flags, category indicators, prefix checks.

---

### MDL009: Cardinality Reduction via Historical Value Substitution

Replace old key values beyond a retention window with a single placeholder to collapse cardinality and shrink dictionaries. This can be done in both facts and dimensions.

```sql
CASE WHEN SaleDate >= DATEADD(year, -1, GETDATE()) THEN SalesKey ELSE 'Historical Key' END
```

---

## Section 6: Tier 4 Direct Lake Optimization Patterns

> **STOP — Requires user approval before applying any change. Changes here require Spark/ETL jobs or Fabric resource profile configuration outside the semantic model. Coordinate with the user's data engineering workflow.**

Direct Lake reads OneLake Delta/Parquet files and loads columns into VertiPaq on demand. Its speed depends on source file layout, memory residency, and segment health.

### DL001: V-Ordering Delta Tables for Direct Lake

Import refresh builds optimized VertiPaq storage. Direct Lake depends on Delta/Parquet layout at query time, so use V-Order for read-heavy Power BI tables to improve compression and column loading.

Two approaches:
- **Spark:** `spark.conf.set("spark.sql.parquet.vorder.default", "true")`, then run `OPTIMIZE` for existing Delta tables.
- **Fabric resource profile:** Use the [`readHeavyForPBI` resource profile](https://learn.microsoft.com/en-us/fabric/data-engineering/configure-resource-profile-configurations), which enables V-Order-oriented write settings for Power BI reads.

---

### DL002: Segment Size and Parallelism

Parquet row groups shape VertiPaq column segment size/count (see SE Parallelism Factor in [Section 1](./dax-perf-decision-guide.md#section-1-how-the-engine-works)).

**Target: 1–16M rows per rowgroup.** Too few rowgroups → single-threaded scans; too many tiny rowgroups → merge overhead. For small tables (< 1M rows) this rarely matters. Run `OPTIMIZE` regularly to consolidate small files into properly sized rowgroups.

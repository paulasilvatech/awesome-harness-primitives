---
applyTo: "**/*.{pbix,dax,md,txt}"
description: "Enforces Power BI DAX conventions for efficient, maintainable, testable measures, model-aware formulas, time intelligence, performance tuning, and documentation."
---

# Power BI DAX Conventions — Measures, Context, and Performance

These instructions apply to Power BI semantic models, DAX measures, calculation notes, and supporting documentation matched by `**/*.{pbix,dax,md,txt}`. They are authoritative for DAX formula structure, function choice, context handling, performance hygiene, measure organization, testing, and documentation; model-design or reporting primitives with stricter rules win for relationships, visual design, deployment, or tenant governance.

## Formula Structure and Variables

Use variables in non-trivial measures so expensive calculations are evaluated once, the formula is readable, and debugging can temporarily return intermediate values.

**Good:**

```dax
Sales YoY Growth % =
VAR CurrentSales = [Total Sales]
VAR PreviousYearSales =
    CALCULATE(
        [Total Sales],
        SAMEPERIODLASTYEAR('Date'[Date])
    )
RETURN
    DIVIDE(CurrentSales - PreviousYearSales, PreviousYearSales)
```

**Bad:**

```dax
Sales YoY Growth % =
DIVIDE(
    [Total Sales] - CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date])),
    CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
)
```

Why: the good measure names `CurrentSales` and `PreviousYearSales`, avoids repeated `CALCULATE`, and can return either variable during debugging; the bad measure repeats work and hides intent.

## Reference Syntax and Naming

Follow Microsoft DAX reference conventions consistently.

| Item | Convention | Rationale |
| --- | --- | --- |
| Columns | Fully qualify columns, for example `Sales[CustomerID]`, `Sales[Profit]`, `Sales[Revenue]`, `'Date'[Date]`, `Product[Category]`, `Geography[Region]`. | Column names are ambiguous across tables and need table context. |
| Measures | Do not table-qualify measures; write `[Total Sales]`, `[YTD Sales]`, `[YTD Sales PY]`, `[Total Profit]`, `[Total Revenue]`, `[Sales Growth %]`. | Measures can move between tables without breaking formulas. |
| Base measures | Use names such as `Revenue`, `Cost`, `Profit`, `Margin %`, `Base - Order Count`. | Hierarchical measures improve reuse and auditing. |
| Derived and KPI measures | Use names such as `Total Sales YTD`, `Total Sales PY`, `KPI - Revenue Growth`, `Calc - Days Since Last Order`. | Prefixes group related measures and clarify intent. |

Build measures hierarchically: `Revenue = SUM(Sales[Revenue])`, `Cost = SUM(Sales[Cost])`, `Profit = [Revenue] - [Cost]`, `Margin % = DIVIDE([Profit], [Revenue])`, `Profit YTD = CALCULATE([Profit], DATESYTD('Date'[Date]))`, and `Margin Trend = [Margin %] - CALCULATE([Margin %], PREVIOUSMONTH('Date'[Date]))`.

## Error Handling and BLANK Behavior

Prefer defensive model design and safe functions over broad error catchers.

| Pattern | Use | Avoid |
| --- | --- | --- |
| Division | `DIVIDE([Total Profit], [Total Revenue])` and `DIVIDE(CurrentSales - PreviousYearSales, PreviousYearSales)`. | `/` with manual zero checks unless the denominator rule is exceptional. |
| Missing values | Preserve `BLANK()` unless business users explicitly need zero. | `IF(ISBLANK([Total Sales]), 0, [Total Sales])` because zeros change visual behavior. |
| Error handling | Validate inputs with `IF`, `ISBLANK`, `COUNTROWS`, and model constraints before calculation. | `IFERROR` and `ISERROR` as routine wrappers because they hide defects and can cost performance. |
| Validation | Return `BLANK()` for invalid calculated results such as ratios outside expected bounds. | Returning misleading numbers when `Result`, `IsValid`, or input data fails checks. |

Use `Average Order Value` style measures with `VAR TotalOrders = COUNTROWS(Orders)`, `VAR TotalRevenue = SUM(Orders[Amount])`, and `IF(TotalOrders > 0, DIVIDE(TotalRevenue, TotalOrders))` when an explicit existence check improves readability.

During review, classify examples as `PREFERRED`, `AVOID`, `ALWAYS`, or `NEVER` only when the rule is that strong; the formula itself should remain self-documenting through variable-based structure rather than step-by-step comments.

## Function Selection and Context

Choose DAX functions according to their semantics and context cost.

| Need | Preferred functions and pattern | Rationale |
| --- | --- | --- |
| Unique counts | `DISTINCTCOUNT(Sales[CustomerID])` | Expresses cardinality directly. |
| Row counts | `COUNTROWS(Orders)` or `COUNTROWS(Sales)` | Faster and clearer than `COUNT(Sales[OrderID])` when counting rows. |
| Averages | `AVERAGE(Sales[DealValue])` | Uses storage-engine aggregation when possible. |
| Filtered measures | `CALCULATE([Total Sales], Sales[OrderValue] > 1000, Sales[OrderDate] >= DATE(2024,1,1))` | Direct Boolean filters are simpler than table filters. |
| Table manipulation | `FILTER`, `ALL`, `VALUES`, `ALLEXCEPT`, `ADDCOLUMNS`, `TOPN`, `RANKX`, `SUMX` | Use table expressions only when the calculation requires table shaping or iteration. |
| Logical guards | `OR`, `NOT`, `IN`, `TRUE()`, `SELECTEDVALUE` | Keep business conditions explicit. |
| Formatting and diagnostics | `FORMAT`, `NOW`, `DATEDIFF`, `ABS`, `MIN`, `MAX`, `TODAY` | Use for diagnostics, labels, and validated comparisons; keep presentation formatting out of numeric measures when possible. |

Avoid `FILTER(Sales, Sales[OrderValue] > 1000)` as a `CALCULATE` filter argument when `Sales[OrderValue] > 1000` is equivalent. Avoid nested `CALCULATE` calls such as `CALCULATE(CALCULATE([Total Sales], Product[Category] = "Electronics"), 'Date'[Year] = 2024)`; combine filters in one `CALCULATE` instead.

## Time Intelligence

Use a marked, contiguous date table and explicit date columns for time intelligence. Standard measures include `YTD Sales = CALCULATE([Total Sales], DATESYTD('Date'[Date]))`, `MTD Sales = CALCULATE([Total Sales], DATESMTD('Date'[Date]))`, `Same Period Last Year = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))`, and period offsets with `DATEADD('Date'[Date], -1, QUARTER)`.

| Scenario | Required pattern |
| --- | --- |
| Moving average | Capture `CurrentDate = MAX('Date'[Date])`, derive `StartDate = EDATE(CurrentDate, -2)`, then filter with `DATESBETWEEN('Date'[Date], StartDate, CurrentDate)`. |
| Fiscal year | Derive `FiscalYearStart` with `DATE(IF(MONTH(MAX('Date'[Date])) >= 7, YEAR(MAX('Date'[Date])), YEAR(MAX('Date'[Date])) - 1), 7, 1)` and filter through `FiscalYearEnd = MAX('Date'[Date])`. |
| Dynamic time calculations | Use calculation groups or selector rows such as `'Time Intelligence'[Time Calculation] = "Current"`, `"PY"`, `"MTD"`, and `"PY MTD"`. |
| Quarter over quarter | Use `CurrentQuarter`, `PreviousQuarter`, `DATEADD`, and `DIVIDE(CurrentQuarter - PreviousQuarter, PreviousQuarter)`. |

## Analytical Patterns

Keep advanced analytical formulas explicit about context, ranking scope, and business thresholds.

| Pattern | Required names and functions | Rule |
| --- | --- | --- |
| Ranking | `Product Rank`, `RANKX(ALL(Product[ProductName]), [Total Sales], , DESC, DENSE)` | Rank over the intended grain and specify tie behavior. |
| Running totals | `Running Total`, `Running Total Optimized`, `CurrentDate = MAX('Date'[Date])`, `FILTER(ALL('Date'[Date]), 'Date'[Date] <= CurrentDate)` | Store the current boundary in a variable before filtering all dates. |
| ABC Analysis | `ABC Classification`, `ABC Classification Advanced`, `CurrentProductSales`, `RunningTotal`, `PercentageOfTotal`, `ProductRank`, `ClassAThreshold`, `ClassBThreshold`, `SWITCH(TRUE(), ...)` | Declare thresholds such as `0.8`, `0.95`, `0.2`, and `0.5` visibly so business owners can validate them. |
| Top N with ties | `Top N Products with Ties`, `TopNValue = 10`, `MinTopNSales`, `MIN([Total Sales])`, `TOPN(TopNValue, ALL(Product[ProductName]), [Total Sales])` | Preserve tied products by comparing against the minimum Top N sales value. |
| Cohort retention | `Cohort Retention Rate`, `CohortMonth`, `CurrentMonth`, `MonthsFromCohort`, `CohortCustomers`, `ActiveCustomersInMonth`, `ALLEXCEPT(Sales, Sales[CustomerID])` | Calculate cohort boundaries once and reuse them. |
| Market basket | `Product Affinity Score`, `CurrentProduct`, `RelatedProduct`, `TransactionsWithBoth`, `TotalTransactions`, `EARLIER(Sales[TransactionID])` | Make transaction-grain assumptions explicit and test carefully. |
| Dynamic selection | `Dynamic Measure Selector`, `SelectedMeasure`, `SWITCH(SelectedMeasure, "Revenue", [Total Revenue], "Profit", [Total Profit], "Units", [Total Units], "Margin", [Profit Margin %], BLANK())` | Use selectors for report interaction, not to hide unrelated business logic. |
| JSON-like text | `Extract JSON Value`, `JSONString`, `ParsedValue`, `PATHCONTAINS(JSONString, "$.analytics.revenue")` | Prefer proper Power Query parsing when possible; document any DAX text workaround. |

For calculation groups or selector tables, preserve API-facing column names such as `MeasureName`; dynamic period measures may use `CurrentPeriodValue`, `PreviousPeriodValue`, `MTDCurrent`, and `MTDPrevious`. For total-sensitive calculations, name variables such as `TotalSales`, `TotalProducts`, `AvgOrderValue`, and `OrdersPerYear` so the denominator is obvious.

## Model Integration

Write DAX that works with the semantic model instead of compensating for weak relationships.

- Use star schema relationships for filters such as `Product[Category] = "Electronics"` and `Geography[Region] = "North America"`.
- Use dimension tables for slicers and filtering; do not duplicate dimensional attributes in fact-table DAX unless the model requires it.
- When a direct relationship does not exist, isolate the workaround with `CustomerList = VALUES(Customer[CustomerID])`, then filter `Sales` with `Sales[CustomerID] IN CustomerList`.
- Use `Row Context Example = SUMX(Sales, Sales[Quantity] * Sales[UnitPrice])` to express row context and `Filter Context Example = CALCULATE([Total Sales], Product[Category] = "Electronics")` to express filter context.
- Treat `Sales Per Product = SUMX(Product, CALCULATE([Total Sales]))` as an intentional context transition, not an accidental pattern.

## Performance Optimization

Optimize by reducing repeated work, limiting context transitions, and measuring real behavior.

| Technique | Apply it this way | Avoid |
| --- | --- | --- |
| Variable caching | Store expensive calculations such as `BaseCalculation`, `PreviousYear`, `Step1_FilteredSales`, and `Step2_PreviousYear`. | Recomputing the same `CALCULATE` branch in numerator and denominator. |
| Iterator discipline | Use `SUMX(Product, Product[UnitPrice] - Product[UnitCost])` only when row-by-row evaluation is required. | Unnecessary iterators over large tables. |
| Calculated columns | Create heavy transformations in Power Query when possible. | Large calculated columns that could be materialized upstream. |
| Relationship filtering | Let model relationships propagate filters before writing custom `FILTER(Customer, NOT(ISBLANK(Customer[CustomerName])))`. | Manual filters that duplicate relationship behavior. |
| Profiling | Use Power BI Performance Analyzer and DAX Studio for timings, query plans, and server timings. | Guessing at bottlenecks or relying on a DAX `Performance Monitor` measure with `NOW()` as proof. |

A `Query Performance Monitor` or `Performance Monitor` measure with `StartTime = NOW()`, `EndTime = NOW()`, `ExecutionTime` or `Duration = DATEDIFF(StartTime, EndTime, SECOND)`, and `WarningThreshold = 5` can be a temporary diagnostic note, but remove it from production semantic models unless it is intentionally user-facing.

## Debugging, Testing, and Validation

Make DAX testable through small variables, explicit validation measures, and business review.

- Use `Debug Measure` or `Complex Measure Debug` patterns with variables such as `Step1`, `Step2`, `Step3`, `Step4`, `Step3_GrowthAbsolute`, `Step4_GrowthPercentage`, and `DebugInfo`; return one variable at a time while troubleshooting.
- Create validation measures such as `Test - Sales Sum` with `DirectSum`, `MeasureResult`, `Difference = ABS(DirectSum - MeasureResult)`, and `IF(Difference < 0.01, "PASS", "FAIL: " & Difference)`.
- Validate calculations with business users so DAX matches requirements, especially for `Customer Lifetime Value`, returns, cancelled orders, ship-date revenue recognition, regional tax calculations, retention probability, and customer-lifespan assumptions.
- Use DAX Studio and Power BI Performance Analyzer before changing formulas solely for perceived performance.

## Documentation and Change Management

Document business logic in measure descriptions or nearby documentation when the formula encodes assumptions. Include the business rule, inputs, exclusions, and relevant version history, such as `v1.0 - Initial implementation (2024-01-15)`, `v1.1 - Added null checking for edge cases (2024-02-01)`, `v1.2 - Optimized performance using variables (2024-02-15)`, and `v2.0 - Changed business logic per stakeholder feedback (2024-03-01)`.

For formulas like `Customer Lifetime Value`, state assumptions: average order value over customer lifetime, purchase frequency, customer lifespan such as `CustomerLifespanYears = 3`, and retention probability based on last order date. Inline comments should clarify non-obvious business rules, not restate every DAX function.

## Good / Bad Examples

The examples below illustrate context-safe filtering, variables, and BLANK-preserving division.

**Good:**

```dax
Year Over Year Growth =
VAR CurrentYear =
    CALCULATE(
        SUM(Sales[Revenue]),
        Sales[Date] >= DATE(2024,1,1)
    )
VAR PreviousYear =
    CALCULATE(
        SUM(Sales[Revenue]),
        Sales[Date] >= DATE(2023,1,1),
        Sales[Date] < DATE(2024,1,1)
    )
RETURN
    DIVIDE(CurrentYear - PreviousYear, PreviousYear)
```

Why: the measure names each period, evaluates each branch once, and uses `DIVIDE` to handle a missing or zero previous year.

**Bad:**

```dax
Complex Without Variables =
DIVIDE(
    CALCULATE(SUM(Sales[Revenue]), Sales[Date] >= DATE(2024,1,1)) -
    CALCULATE(SUM(Sales[Revenue]), Sales[Date] >= DATE(2023,1,1), Sales[Date] < DATE(2024,1,1)),
    CALCULATE(SUM(Sales[Revenue]), Sales[Date] >= DATE(2023,1,1), Sales[Date] < DATE(2024,1,1))
)
```

Why: the measure repeats the previous-year expression, makes debugging harder, and obscures the business periods.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `VAR` and `RETURN` for non-trivial DAX measures | Expensive branches run once and formulas become easier to debug. |
| Fully qualify columns and never fully qualify measures | Column references need table context; measures should survive table moves. |
| Use `DIVIDE` and preserve `BLANK()` unless zero is a documented business rule | Safe division and visual behavior stay correct. |
| Prefer direct Boolean filters in `CALCULATE`; use `FILTER` only for table logic | Direct filters are clearer and usually more efficient. |
| Use `COUNTROWS`, `DISTINCTCOUNT`, `SUM`, `AVERAGE`, and iterator functions according to the required grain | Function choice communicates intent and reduces unnecessary context transitions. |
| Implement time intelligence against a proper date table with explicit date columns | Built-in functions such as `DATESYTD`, `DATESMTD`, and `SAMEPERIODLASTYEAR` require reliable date context. |
| Keep analytical thresholds, ranking scopes, and selector values visible | Business users can validate assumptions and edge cases. |
| Test with validation measures and profile with Power BI Performance Analyzer and DAX Studio | Correctness and performance must be proven, not guessed. |
| Document business assumptions and version history when measures encode policy | Future changes can distinguish formula mechanics from business intent. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use variables such as `CurrentSales`, `PreviousYearSales`, `CurrentDate`, and `StartDate` | Repeat the same `CALCULATE` expression throughout a measure. |
| Write `DISTINCTCOUNT(Sales[CustomerID])` and `SUM(Sales[Revenue])` | Write ambiguous column references such as `DISTINCTCOUNT([CustomerID])`. |
| Write `[YTD Sales]`, `[Total Sales PY]`, and `[Profit Margin %]` | Write table-qualified measure references such as `Sales[Total Sales]`. |
| Keep `BLANK()` for missing values unless the report requirement says zero | Convert every missing value to zero with `IF(ISBLANK(...), 0, ...)`. |
| Combine compatible filters in one `CALCULATE` | Nest `CALCULATE` calls for independent filters. |
| Use `ALL`, `ALLEXCEPT`, `VALUES`, `RANKX`, and `TOPN` with explicit grains | Let ranking, totals, or cohort logic inherit accidental visual context. |
| Validate formulas with business users and targeted test measures | Ship complex DAX because it returns a number in one sample visual. |
| Use Performance Analyzer and DAX Studio for optimization | Use temporary `NOW()` timing measures as the only performance evidence. |

## Checklist Before Opening a PR

- [ ] Non-trivial measures use variables and return a named final expression.
- [ ] Column references are table-qualified and measure references are not table-qualified.
- [ ] Division uses `DIVIDE`; `BLANK()` is preserved unless zero is a documented requirement.
- [ ] `CALCULATE` filters are direct Boolean filters unless table manipulation is required.
- [ ] Time-intelligence measures use a reliable date table and explicit date columns.
- [ ] Ranking, running totals, ABC, Top N, cohort, market basket, and dynamic selector measures declare their scope and thresholds.
- [ ] DAX follows the semantic model relationships instead of compensating for avoidable modeling gaps.
- [ ] Validation measures or business-user checks confirm calculation correctness.
- [ ] Power BI Performance Analyzer or DAX Studio evidence supports performance-sensitive changes.
- [ ] Measure descriptions or nearby documentation capture business assumptions and version history where relevant.

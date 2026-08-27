# DAX Language Guidelines

Guidelines for writing DAX code - variables, comments, coding patterns, and query syntax for Power BI semantic models.

---

## DAX Coding Best Practices

- Use meaningful variable names to improve readability
- Use the `VAR` keyword to break complex DAX into logical calculation steps; prefix variables with `_` to avoid naming conflicts
- Default to `DIVIDE()` instead of `/` for division because it safely handles divide-by-zero by returning BLANK; however, inside row iterators prefer `/` only when the denominator is guaranteed non-zero or rows have been pre-filtered to exclude zero denominators.
- Use `KEEPFILTERS()` or direct column predicates as `CALCULATE` filter arguments instead of wrapping `FILTER` over an entire table
- Use `TREATAS` instead of `INTERSECT` for virtual relationships (better performance)
- Use `REMOVEFILTERS()` instead of `ALL()` when the intent is to remove filters - it is semantically clearer and avoids subtle context issues
- Always refer to columns including the table name: `'Table Name'[Column Name]`
- Always refer to measures without including the table name: `[Measure Name]`
- Avoid excessive `CALCULATE` nesting - break into variables for readability and performance
- Avoid IFERROR inside iterators or scalar-by-scalar contexts where it forces callbacks; safe in scalar guards. Prefer DIVIDE, conditional logic, or COALESCE to handle expected error cases.
- Never use `EVALUATEANDLOG` in production models (debug function only)
- Never use `1-(x/y)` or `1+(x/y)` syntax - instead compute the full expression with `DIVIDE` and `VAR`:
  ```dax
  // Avoid: 1 - SUM('Sales'[Cost]) / SUM('Sales'[Revenue])
  // Use:
  VAR _revenue = SUM('Sales'[Revenue])
  RETURN DIVIDE(_revenue - SUM('Sales'[Cost]), _revenue)
  ```

---

## DAX Query Syntax Rules

### Query Structure

#### DEFINE Block

- Use DEFINE at the beginning if the query includes VAR, MEASURE, COLUMN, or TABLE definitions
- Only use a single DEFINE block per query
- Separate definitions with new lines (no commas or semicolons)

#### Measure Definitions

- When defining: ALWAYS fully qualify the measure name including its host table
  - Example: `DEFINE MEASURE 'TableName'[MeasureName] = ...`
  - The host table must exist in the semantic model
- When using: Refer to the measure by name only, without the table qualifier
  - Example: Use `[MeasureName]` in expressions like `CALCULATE([MeasureName], ...)`

#### Ordering Results

- ALWAYS include an ORDER BY clause when EVALUATE returns multiple rows
- Do not use the ORDERBY function to sort the final query result

### CALCULATE and CALCULATETABLE Filter Rules

Boolean filters in CALCULATE or CALCULATETABLE have important restrictions:

- Cannot directly use a measure or another CALCULATE function
  - Solution: Use a variable to store the result, then reference the variable
- Cannot reference columns from two different tables
- When using the IN operator, the table operand must be a table variable, not a table expression
- Do not assign a boolean filter to a VAR definition

### SUMMARIZECOLUMNS Function

**Purpose**: Build summary tables with groupby columns and measure-like extension columns

**Parameter Order** (all optional, but must follow this order if used):

1. Groupby columns (can be from one or multiple tables)
2. Filters
3. Measures or measure-like calculations

**Key Rules**:

- Use SUMMARIZECOLUMNS as the default for building summary tables with measures
- Do not use SUMMARIZECOLUMNS without measure-like extension columns
- Returns only rows where at least one measure value is not BLANK
- Allows ANY number of measure-like calculations of arbitrary complexity
- DO NOT use boolean filters with SUMMARIZECOLUMNS

**When to Use Alternatives**:

- If there are no measures or calculations, use SUMMARIZE instead

### SUMMARIZE Function

**Allowed Pattern**:

```dax
SUMMARIZE(<table expression>, <column1>, ..., <columnN>)
```

**Critical Restrictions**:

- Prefer SUMMARIZECOLUMNS over SUMMARIZE with extension columns
  - Use SUMMARIZECOLUMNS for measure calculations
- Use for extracting distinct combinations of columns only
- `VALUES('Table'[Column])` is a shortcut for `SUMMARIZE('Table', 'Table'[Column])`
- When extracting a column from a table variable: `SUMMARIZE(_TableVar, [Column])`
  - Note: `_TableVar[Column]` is not valid syntax

### GROUPBY Function

**Purpose**: Perform simple aggregations on table-valued variables at a grouped level

**Key Rules**:

- Only use GROUPBY with a table-valued variable as the first argument
- The CURRENTGROUP function is valid ONLY within GROUPBY
- CURRENTGROUP must not be used elsewhere

### SELECTCOLUMNS Function

**Purpose**: Project columns while preserving duplicates or renaming columns

**Key Rules**:

- Use to preserve duplicate rows (unlike SUMMARIZE which removes them)
- Use to rename columns for clarity
- When renaming columns, subsequent expressions (TOPN, ORDER BY) must use the NEW column names
- Include all columns needed for later operations (ORDER BY, FILTER, etc.)

### Set Functions

When using INTERSECT, UNION, or EXCEPT:

- Both input tables must produce an identical number of columns

### Time Intelligence Functions

**DATESINPERIOD Rolling Windows**:

- The negative period offset must precisely match the number of periods required
- Examples: 12-month window: Use -12 (not -11); 3-month window: Use -3 (not -2)
- This prevents off-by-one errors

**Maintaining Clear Date Context**:

- Always establish a valid date context for time intelligence calculations
- Methods: Include groupby columns from the date table, OR apply filters on date columns
- Without date context, time intelligence functions cannot determine a "current date" reference
- When using ROW function with time intelligence, supply external filters through CALCULATETABLE

---

## DAX Query Examples

### Example: Time Intelligence with Rolling Averages

Year-to-date total sales and 14-day moving average for red products:

```dax
// Year-to-date total sales and 14-day moving average of sales for red products.
EVALUATE
  CALCULATETABLE(
    ROW(
      "Total Sales Amount YTD", TOTALYTD([Total Amount], 'Calendar'[Date]),
      "Total Sales Amount 14-Day MA", AVERAGEX(DATESINPERIOD('Calendar'[Date], MAX('Calendar'[Date]), -14, DAY), [Total Amount])
    ),
    'Product'[Color] == "Red",
    TREATAS({ MAX('Sales'[OrderDate]) }, 'Calendar'[Date])
  )
```

### Example: Filtering with Measures Using Variables

Find products with total sales over $1 million that are red or black:

```dax
DEFINE
  VAR _Filter = TREATAS(
    { "Red", "Black" },
    'Product'[Color]
  )
  VAR _SummaryTable = SUMMARIZECOLUMNS(
    'Product'[Name],
    _Filter,
    "Total Sales", [Total Amount]
  )
EVALUATE
  SELECTCOLUMNS(
    FILTER( _SummaryTable, [Total Sales] > 1000000 ),
    'Product'[Name]
  )
  ORDER BY 'Product'[Name] ASC
```

### Example: Using Variables to Store Measure Results

Find products with list prices above the median:

```dax
DEFINE
  VAR _MedianListPrice = [Median List Price]
EVALUATE
  CALCULATETABLE(
    VALUES('Product'[Name]),
    'Product'[List Price] > _MedianListPrice
  )
  ORDER BY 'Product'[Name] ASC
```

### Example: Using Table Variables as Filters

Find the product with highest demand since 2020 and get its sale dates:

```dax
DEFINE
  VAR _Filter = FILTER( ALL('Calendar'[Year]), 'Calendar'[Year] >= 2020 )
  VAR _TopProduct = TOPN(
    1,
    SUMMARIZECOLUMNS( 'Product'[ProductKey], _Filter, "Total Quantity", [Total Quantity] ),
    [Total Quantity], DESC
  )
EVALUATE
  SELECTCOLUMNS(
    CALCULATETABLE( 'Sales', _TopProduct ),
    "Product Name", RELATED('Product'[Name]),
    'Sales'[OrderDate]
  )
  ORDER BY [Product Name] ASC, 'Sales'[OrderDate] ASC
```

### Example: Multi-Level Aggregation with GROUPBY

Average, minimum, and maximum monthly sales quantity by year:

```dax
DEFINE
  VAR _SummaryTable = SUMMARIZECOLUMNS(
    'Calendar'[Year],
    'Calendar'[Month],
    'Calendar'[MonthNumberOfYear],
    "Monthly Quantity", [Total Quantity]
  )
EVALUATE
  GROUPBY(
    _SummaryTable,
    'Calendar'[Year],
    "Avg Monthly Quantity", AVERAGEX(CURRENTGROUP(), [Monthly Quantity]),
    "Min Monthly Quantity", MINX(CURRENTGROUP(), [Monthly Quantity]),
    "Max Monthly Quantity", MAXX(CURRENTGROUP(), [Monthly Quantity])
  )
  ORDER BY 'Calendar'[Year] ASC
```

---

## DAX User-Defined Functions (UDFs)

DAX UDFs let you define reusable function definitions in a semantic model. Apply when refactoring repeated DAX patterns into a single named function.

### Syntax

```yaml
FunctionName: MyFunction
FunctionDefinition: |-
  (param1 [: Type [Scalar Subtype] [Val|Expr]],
   param2 [: Type [Scalar Subtype] [Val|Expr]]
  ) =>
      <Function body>
```

### Type System

**Parameter types:**

- `AnyVal` - scalar or table (default if omiited)
- `Scalar` - a single value
- `Table` - a DAX table expression
- `AnyRef` - a direct reference to a model object (column, table, measure) without pre-evaluation. Use when passing references to functions like `CALCULATE`, `TREATAS`, `SAMEPERIODLASTYEAR`. Allowed forms: `'Table'[Column]`, `'Table'`, `[Measure]`, `MyCalendar`.
- `MeasureRef` - a measure reference
- `ColumnRef` - a column reference
- `TableRef` - a table reference
- `CalendarRef` - a calendar reference

**Scalar subtypes** (optional): `Int64`, `Decimal`, `Double`, `String`, `DateTime`, `Boolean`, `Numeric`, `Variant`.
`BLANK()` is valid for any subtype.

**Parameter modes:**

- `Val` (default) - argument is evaluated at the call site, then the value is substituted in the body.
- `Expr` - the raw expression is substituted into the body and re-evaluated in inner contexts (e.g., inside `CALCULATE`, `FILTER`, iterators). Use when the expression must respond to context transitions inside the function.

### Examples

**Scalar with subtype** - circle area:

```yaml
FunctionName: CircleArea
FunctionDefinition: |-
    (radius : Scalar Numeric) =>
        PI() * radius * radius
```

**AnyRef** - statistical mode of a column:

```yaml
FunctionName: Mode
FunctionDefinition: |-
    (col : ColumnRef) =>
        SUMMARIZE(
            TOPN(1,
                ADDCOLUMNS(VALUES(col), "Freq", CALCULATE(COUNTROWS(TABLEOF(col)))),
                [Freq], DESC),
            col
        )
```

Usage: `Mode('Sales'[ProductKey])`

**Expr mode** - evaluate any scalar in the prior year:

```yaml
FunctionName: PriorYearValue
FunctionDefinition: |-
    (expression : Scalar Numeric Expr,
     dateColumn : ColumnRef
    ) =>
        CALCULATE(expression, SAMEPERIODLASTYEAR(dateColumn))
```

Usage: `PriorYearValue([Total Amount], 'Calendar'[Date])`. `Expr` ensures `[Total Amount]` is evaluated under the prior-year filter.

**Table-returning UDF** - top 3 products by sales:

```yaml
FunctionName: Top3ProductsBySales
FunctionDefinition: |-
    () =>
        TOPN(3, VALUES('Product'[ProductKey]), [Sales], DESC)
```

Usage: `CALCULATE([Total Amount], Top3ProductsBySales())`.

### Best Practices

- Specify parameter type (and subtype where useful) for clarity and validation.
- Use `Expr` only when the expression must re-evaluate in an inner context; otherwise use the default `Val`.
- Keep each UDF focused on a single purpose; use `VAR` inside the body to break up complex logic.
- Account for `BLANK()` and empty tables in the function body.



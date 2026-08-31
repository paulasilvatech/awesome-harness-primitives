# Semantic Model Metadata Discovery — DAX INFO Functions

Read-only DAX queries for metadata exploration using `INFO.VIEW.*` and `INFO.*` rowsets. Use this reference when discovering model metadata through **DAX INFO functions** instead of `powerbi-modeling-mcp` get/list tools.

## Recommended Discovery Order

1. Run the [Scope Estimation Queries](#scope-estimation-queries) to estimate metadata scope (table, column, measure, and relationship counts) before deep discovery.
2. Start with `INFO.VIEW.TABLES()` for a fast table inventory.
3. Expand to `INFO.VIEW.COLUMNS()` and `INFO.VIEW.MEASURES()` for semantic details.
4. Use `INFO.VIEW.RELATIONSHIPS()` to validate joins and filter behavior.
5. Use the deeper patterns only when a required metadata object is not covered by the `INFO.VIEW.*` functions.

## Metadata Object → INFO Function Map

| Metadata Object | Primary INFO functions |
|---|---|
| Model | `INFO.MODEL` |
| Tables | `INFO.VIEW.TABLES` |
| Columns | `INFO.VIEW.COLUMNS`, `INFO.GROUPBYCOLUMNS`, `INFO.RELATEDCOLUMNDETAILS` |
| Measures | `INFO.VIEW.MEASURES`, `INFO.FORMATSTRINGDEFINITIONS`, `INFO.DETAILROWSDEFINITIONS` |
| Relationships | `INFO.VIEW.RELATIONSHIPS` |
| Partitions | `INFO.PARTITIONS`, `INFO.EXPRESSIONS`, `INFO.QUERYGROUPS`, `INFO.REFRESHPOLICIES`, `INFO.DATACOVERAGEDEFINITIONS` |
| Expressions/Parameters | `INFO.EXPRESSIONS` |
| Security roles & permissions | `INFO.ROLES`, `INFO.TABLEPERMISSIONS`, `INFO.COLUMNPERMISSIONS` |
| Hierarchies | `INFO.HIERARCHIES`, `INFO.LEVELS`, `INFO.ATTRIBUTEHIERARCHIES`, `INFO.VARIATIONS` |
| Calculation groups/items | `INFO.CALCULATIONGROUPS`, `INFO.CALCULATIONITEMS` |
| Perspectives | `INFO.PERSPECTIVES`, `INFO.PERSPECTIVETABLES`, `INFO.PERSPECTIVECOLUMNS`, `INFO.PERSPECTIVEHIERARCHIES`, `INFO.PERSPECTIVEMEASURES` |
| Calendars | `INFO.CALENDARS`, `INFO.CALENDARCOLUMNGROUPS`, `INFO.CALENDARCOLUMNREFERENCES` |
| Cultures | `INFO.CULTURES` |
| Object translations | `INFO.OBJECTTRANSLATIONS` |
| Functions | `INFO.USERDEFINEDFUNCTIONS` |
| Dependencies / lineage | `INFO.DEPENDENCIES`, `INFO.CHANGEDPROPERTIES`, `INFO.EXCLUDEDARTIFACTS` |
| Storage internals / size | `INFO.STORAGETABLES`, `INFO.STORAGETABLECOLUMNS`, `INFO.STORAGETABLECOLUMNSEGMENTS`, `INFO.COLUMNSTORAGES`, `INFO.PARTITIONSTORAGES`, `INFO.TABLESTORAGES` |

## Scope Estimation Queries

```dax
// Probe object counts to estimate metadata scope before deep discovery
EVALUATE
ROW(
    "TableCount", COUNTROWS(INFO.VIEW.TABLES()),
    "ColumnCount", COUNTROWS(INFO.VIEW.COLUMNS()),
    "MeasureCount", COUNTROWS(INFO.VIEW.MEASURES()),
    "RelationshipCount", COUNTROWS(INFO.VIEW.RELATIONSHIPS())
)
```

## Narrowing Results (Projection + Filtering)

```dax
// Pull only needed columns for a single table to reduce output volume
EVALUATE
SELECTCOLUMNS(
    FILTER(INFO.VIEW.COLUMNS(), [Table] = "YourTableName"),
    "Column Alias", [Name],
    "DataType", [DataType]
)
```

## Ordering Results

`ORDER BY` must reference the column name **as it exists in the query's output**, not the underlying `INFO.*` source column:

- **Without `SELECTCOLUMNS`** — order by the INFO function's original column name (e.g. `ORDER BY [Name]` on `INFO.VIEW.TABLES()`).
- **With `SELECTCOLUMNS`** — the projection renames the columns, so `ORDER BY` **must use the alias** you defined, not the original INFO column. Referencing the original name (e.g. `[Name]`) after projecting it to `"Column Alias"` fails because that column no longer exists in the result.

```dax
// CORRECT: order by the alias defined in SELECTCOLUMNS
EVALUATE
SELECTCOLUMNS(
    FILTER(INFO.VIEW.COLUMNS(), [Table] = "YourTableName"),
    "Column Alias", [Name],
    "DataType", [DataType]
)
ORDER BY [Column Alias] ASC

// WRONG: [Name] does not exist in the projected result (it was aliased to "Column Alias")
EVALUATE
SELECTCOLUMNS(
    FILTER(INFO.VIEW.COLUMNS(), [Table] = "YourTableName"),
    "Column Alias", [Name],
    "DataType", [DataType]
)
ORDER BY [Name] ASC
```

## Dependency Discovery

### Dependency rowset for a DAX query

```dax
// Returns dependency graph for the query payload
DEFINE
VAR _Query = "EVALUATE SUMMARIZECOLUMNS('Date'[Year], 'Product'[Color], ""Sales"", [Sales])"
EVALUATE
INFO.DEPENDENCIES("QUERY", _Query)
```

### Dependency rowset scoped to a measure

```dax
// Adjust values to your model object names
EVALUATE
FILTER(
    INFO.DEPENDENCIES(),
    [OBJECT_TYPE] = "MEASURE"
        && [TABLE] = "Sales"
        && [OBJECT] = "Total Sales"
)
```

### Reverse dependencies (what references a measure?)

```dax
// Use when dependency columns are exposed in your engine rowset
EVALUATE
FILTER(
    INFO.DEPENDENCIES(),
    [REFERENCED_OBJECT_TYPE] = "MEASURE"
        && [REFERENCED_TABLE] = "Sales"
        && [REFERENCED_OBJECT] = "Total Sales"
)
```

> Dependency rowset column names may vary by engine/version; validate available fields with an unfiltered probe query first.

## Complete INFO Function Catalog

> **Warning:** Only run this query if the required metadata object is not returned by any of the frequently used functions.

Use this query to enumerate all currently exposed `INFO.*` functions in the active engine/version.

```dax
EVALUATE
SELECTCOLUMNS(
    FILTER(
        INFO.FUNCTIONS(),
        LEFT([FUNCTION_NAME], 5) = "INFO."
    ),
    [FUNCTION_NAME]
)
```


## Reference queries

```dax
// Detailed model metadata
EVALUATE
INFO.MODEL()
```

```dax
// Partition of a table
EVALUATE
FILTER(INFO.PARTITIONS(), [TableID] == 123)
```

```dax
// Probe output schema of an INFO function (returns column names and types with zero data rows)
EVALUATE
TOPN(0, INFO.VIEW.COLUMNS())
```

```dax
// Object translations metadata
EVALUATE
INFO.OBJECTTRANSLATIONS()
```

## Troubleshooting

- **Advanced INFO functions return permission errors**
  - **Issue:** Queries against `INFO.*` fail with authorization or privilege-related errors.
  - **Cause:** Many `INFO.*` functions require elevated semantic model permissions beyond standard read access.
  - **Fix:** Start with `INFO.VIEW.*` functions for read-oriented discovery.
- **Metadata output volume is too large for focused analysis**
  - **Issue:** Returning full metadata rowsets introduces too many properties and crowds the working context.
  - **Cause:** Unbounded `INFO.VIEW.*` and `INFO.*` queries return broad object/property surfaces that are often unnecessary for the current task.
  - **Fix:** Use the [Scope Estimation Queries](#scope-estimation-queries) to estimate scope and inspect output schemas, then narrow results with projection and filtering as shown in [Narrowing Results (Projection + Filtering)](#narrowing-results-projection--filtering).
- **Do not use `INFO` DAX functions to retrieve role memberships**
  - **Issue:** `INFO.ROLEMEMBERSHIPS()` returns empty or incomplete results.
  - **Cause:** Role members are assigned at the service level (Entra ID) after deployment, not in the model definition — so DAX `INFO` functions cannot reliably surface them.
  - **Fix:** Redirect to [Manage role membership documentation](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security#manage-role-membership) for current guidance on role membership management.

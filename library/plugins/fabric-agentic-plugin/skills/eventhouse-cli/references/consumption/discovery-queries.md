# KQL Schema Discovery Queries

Reference for schema exploration commands used during agentic discovery workflows.

---

## Table and Column Discovery

### Table Discovery

```kql
// List all tables with row counts and sizes
.show tables details
| project TableName, TotalRowCount, TotalOriginalSize, TotalExtentSize, HotOriginalSize

// List tables (names only)
.show tables
| project TableName

// Table schema (column names, types, folder)
.show table MyTable schema as json

// Table schema as CSL (for scripting)
.show table MyTable cslschema

// Compact column listing (CSL format)
.show table MyTable cslschema
| project TableName, Schema
```

### Column Statistics

```kql
// Column cardinality and statistics (sample-based)
.show table MyTable column statistics

// Quick column profiling via query
MyTable
| take 10000
| summarize
    Rows = count(),
    Nulls = countif(isnull(ColumnName)),
    Distinct = dcount(ColumnName),
    MinVal = min(ColumnName),
    MaxVal = max(ColumnName)
```

---

## Function and View Discovery

### Function Discovery

```kql
// List all stored functions
.show functions
| project Name, Parameters, Body = substring(Body, 0, 100), DocString, Folder

// Full function definition
.show function MyFunction

// Functions in a folder
.show functions
| where Folder == "Analytics"
```

### Materialized View Discovery

```kql
// List all materialized views
.show materialized-views
| project Name, SourceTable, Query = substring(Query, 0, 100), IsEnabled, IsHealthy

// View statistics (lag, processed records)
.show materialized-view MyView statistics

// View extents
.show materialized-view MyView extents
| summarize ExtentCount = count(), TotalRows = sum(RowCount)
```

---

## Policy Discovery

```kql
// Retention policies
.show table MyTable policy retention

// Caching policies
.show table MyTable policy caching

// All major policies for a table (run individually)
// retention, caching, streamingingestion, update, merge, sharding

// Streaming ingestion policy
.show table MyTable policy streamingingestion

// Update policies
.show table MyTable policy update
```

---

## External Tables and Ingestion Mappings

### External Table Discovery

```kql
// List external tables
.show external tables
| project TableName, TableType, Folder, ConnectionStrings

// External table schema
.show external table MyExternalTable schema as json
```

### Ingestion Mapping Discovery

```kql
// CSV mappings for a table
.show table MyTable ingestion csv mappings

// JSON mappings for a table
.show table MyTable ingestion json mappings

// All mappings for a table
.show table MyTable ingestion mappings
```

---

## Security Discovery

```kql
// Database-level principals
.show database MyDatabase principals

// Table-level principals
.show table MyTable principals

// Current identity
print CurrentUser = current_principal(), Cluster = current_cluster_endpoint()
```

---

## Database Overview Script

Run this sequence to get a complete picture of a KQL Database:

```kql
// 1. Database stats (uses current database context)
.show database datastats

// 2. All tables with details
.show tables details
| project TableName, TotalRowCount, TotalOriginalSize, CachingPolicy
| order by TotalRowCount desc

// 3. All functions
.show functions
| project Name, Folder, DocString, Parameters

// 4. All materialized views
.show materialized-views
| project Name, SourceTable, IsEnabled, IsHealthy

// 5. All external tables
.show external tables
```

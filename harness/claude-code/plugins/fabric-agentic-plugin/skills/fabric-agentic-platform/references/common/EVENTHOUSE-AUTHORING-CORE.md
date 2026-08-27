# EVENTHOUSE-AUTHORING-CORE.md — KQL Management Command Patterns for Fabric Eventhouse

> **Purpose**: Shared reference for Eventhouse authoring skills. Covers table management, ingestion, policies, materialized views, functions, and schema evolution for Fabric Eventhouse and KQL Databases.
> **Not a tutorial** — assumes familiarity with KQL management commands. Focus is Fabric-specific behaviour and CLI-driven workflows.

---

## Authoring Capability Matrix

> **Connection**: identical to consumption — see `EVENTHOUSE-CONSUMPTION-CORE.md`. Management commands (`.create`, `.alter`, `.drop`) require **Admin** or **Ingestor** database-level roles.

| Capability | KQL Database (Eventhouse) | Shortcut (OneLake) |
|---|---|---|
| **Create/alter tables** | ✅ | ❌ Read-only |
| **Ingest data** | ✅ | ❌ |
| **Retention/caching policies** | ✅ | ❌ |
| **Update policies** | ✅ | ❌ |
| **Materialized views** | ✅ | ❌ |
| **Stored functions** | ✅ | ❌ |
| **External tables** | ✅ | ❌ |
| **Streaming ingestion** | ✅ | ❌ |
| **Data mappings** | ✅ | ❌ |
| **Continuous export** | ✅ | ❌ |

---

## Table Management and Schema Evolution

### Create Table

```kql
.create table Events (
    Timestamp: datetime, EventType: string,
    UserId: string, Properties: dynamic, Duration: real
)
```

### Create-Merge Table (Safe Schema Evolution)

Adds columns if missing; never drops existing columns. **Preferred for idempotent deployments.**

```kql
.create-merge table Events (
    Timestamp: datetime, EventType: string, UserId: string,
    Properties: dynamic, Duration: real,
    Region: string       // new column — added safely
)
```

### Alter / Rename / Drop

```kql
.alter-merge table Events (NewColumn: string)       // add column
.rename column Events.OldName to NewName             // rename column
.drop column Events.OldColumn                        // drop column (irreversible)
.drop table Events ifexists                          // drop table
```

### Schema Evolution

```kql
.rename table OldName to NewName

// Atomic swap (Blue-Green pattern)
.rename tables NewEvents = Events, Events_Backup = Events_Old, Events = NewEvents
```

---

## Ingestion and Data Mappings

### Inline Ingestion (Small Data / Testing)

```kql
.ingest inline into table Events <|
2025-01-15T10:00:00Z,Login,user1,{},0.5
2025-01-15T10:01:00Z,Click,user2,{"page":"home"},0.2
```

### Set-or-Append / Set-or-Replace

```kql
// Append query results
.set-or-append Events <|
    OtherTable
    | where Timestamp > ago(1d)
    | project Timestamp, EventType, UserId, Properties, Duration

// Replace table content with query results
.set-or-replace Events <|
    StagingEvents | where IsValid == true
```

### Ingest from Storage (Blob / ADLS / OneLake)

```kql
// From Blob Storage with CSV mapping
.ingest into table Events (
    h'https://myaccount.blob.core.windows.net/container/events.csv.gz;impersonate'
) with (format="csv", ingestionMappingReference="EventsCsvMapping", ignoreFirstRecord=true)

// From OneLake
.ingest into table Events (
    h'abfss://workspace@onelake.dfs.fabric.microsoft.com/lakehouse.Lakehouse/Files/events.parquet;impersonate'
) with (format="parquet")
```

### Streaming Ingestion

Enable via policy first; data is then ingested via the streaming endpoint or SDKs.

```kql
.alter table Events policy streamingingestion enable
```


### Data Mappings

#### CSV Mapping

```kql
.create table Events ingestion csv mapping "EventsCsvMapping"
'['
'  {"column":"Timestamp",  "datatype":"datetime", "ordinal":0},'
'  {"column":"EventType",  "datatype":"string",   "ordinal":1},'
'  {"column":"UserId",     "datatype":"string",   "ordinal":2},'
'  {"column":"Properties", "datatype":"dynamic",  "ordinal":3},'
'  {"column":"Duration",   "datatype":"real",     "ordinal":4}'
']'
```

#### JSON Mapping

```kql
.create table Events ingestion json mapping "EventsJsonMapping"
'['
'  {"column":"Timestamp",  "path":"$.timestamp",  "datatype":"datetime"},'
'  {"column":"EventType",  "path":"$.eventType",  "datatype":"string"},'
'  {"column":"UserId",     "path":"$.userId",     "datatype":"string"},'
'  {"column":"Properties", "path":"$.properties", "datatype":"dynamic"},'
'  {"column":"Duration",   "path":"$.duration",   "datatype":"real"}'
']'
```

#### Show Mappings

```kql
.show table Events ingestion csv mappings
.show table Events ingestion json mappings
```

---

## Policies

### Retention Policy

```kql
// Table-level: 365-day retention
.alter table Events policy retention
```{"SoftDeletePeriod":"365.00:00:00","Recoverability":"Enabled"}```

// Database-level default (applies to tables without override)
.alter database MyDatabase policy retention
```{"SoftDeletePeriod":"90.00:00:00","Recoverability":"Enabled"}```
```

### Caching Policy

Controls how much data is kept in hot cache (SSD) vs cold storage.

```kql
.alter table Events policy caching hot = 30d
.alter database MyDatabase policy caching hot = 7d    // database default
```

### Partitioning Policy

```kql
.alter table Events policy partitioning
```
{
  "PartitionKeys": [
    {
      "ColumnName": "UserId",
      "Kind": "Hash",
      "Properties": { "Function": "XxHash64", "MaxPartitionCount": 64 }
    }
  ]
}
```
```

### Merge Policy

```kql
.alter table Events policy merge
```{"RowCountUpperBoundForMerge": 1000000, "MaxExtentsToMerge": 20}```
```

---

## Materialized Views

Pre-computed aggregations maintained incrementally as new data arrives.

```kql
// Create (with optional backfill of existing data)
.create materialized-view with (backfill=true) EventCounts on table Events {
    Events
    | summarize Count = count(), LastSeen = max(Timestamp) by EventType
}

// Alter
.alter materialized-view EventCounts on table Events {
    Events
    | summarize Count = count(), LastSeen = max(Timestamp), FirstSeen = min(Timestamp) by EventType
}

// Lifecycle
.show materialized-view EventCounts statistics
.disable materialized-view EventCounts
.enable materialized-view EventCounts
.drop materialized-view EventCounts
```

**Supported aggregations:** `count()`, `sum()`, `min()`, `max()`, `dcount()`, `avg()`, `countif()`, `sumif()`, `arg_max()`, `arg_min()`, `make_set()`, `make_list()`, `percentile()`, `take_any()`.

---

## Stored Functions and Update Policies

### Stored Functions

```kql
.create-or-alter function with (
    docstring = "Get events for a specific user in time range",
    folder = "Analytics"
) GetUserEvents(userId: string, lookback: timespan = 1d) {
    Events
    | where Timestamp > ago(lookback) and UserId == userId
    | sort by Timestamp desc
}

.show function GetUserEvents
.drop function GetUserEvents

// Usage
GetUserEvents("user123", 7d) | count
```

### Update Policies

Automatically transform data upon ingestion into a source table.

```kql
// Target table
.create table ParsedEvents (
    Timestamp: datetime, EventType: string, UserId: string, PageName: string
)

// Transformation function
.create-or-alter function ParseRawEvents() {
    RawEvents
    | extend Parsed = parse_json(RawData)
    | project
        Timestamp = todatetime(Parsed.timestamp),
        EventType = tostring(Parsed.eventType),
        UserId = tostring(Parsed.userId),
        PageName = tostring(Parsed.properties.page)
}

// Attach update policy
.alter table ParsedEvents policy update
@'[{"IsEnabled":true,"Source":"RawEvents","Query":"ParseRawEvents()","IsTransactional":true}]'
```

---

## External Tables

### OneLake / ADLS External Table

```kql
.create external table ExternalSales (
    OrderDate: datetime,
    ProductId: string,
    Quantity: int,
    Amount: real
) kind=storage
dataformat=parquet
(
    h'abfss://workspace@onelake.dfs.fabric.microsoft.com/lakehouse.Lakehouse/Tables/sales;impersonate'
)
```

### Query External Table

```kql
external_table("ExternalSales")
| where OrderDate > ago(30d)
| summarize TotalAmount = sum(Amount) by ProductId
| top 10 by TotalAmount desc
```

---

## Permission Model

### Database Roles

| Role | Can Query | Can Ingest | Can Admin |
|---|---|---|---|
| `viewer` | ✅ | ❌ | ❌ |
| `user` | ✅ | ❌ | ❌ |
| `ingestor` | ❌ | ✅ | ❌ |
| `admin` | ✅ | ✅ | ✅ |

### Grant Permissions

```kql
// Add a viewer
.add database MyDatabase viewers ('aaduser=user@contoso.com')

// Add an admin
.add database MyDatabase admins ('aaduser=admin@contoso.com')

// Add table-level admin
.add table Events admins ('aaduser=tableadmin@contoso.com')

// Show current principals
.show database MyDatabase principals
```

---

## Authoring Gotchas and Troubleshooting Reference

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | `.create table` fails with "already exists" | Table exists | Use `.create table ifnotexists` or `.create-merge table` |
| 2 | Ingestion succeeds but table empty | Data mapping mismatch | Check `.show table T ingestion csv mappings`; verify ordinals/paths match source |
| 3 | Update policy not triggering | Policy disabled or function error | Check `.show table T policy update`; test function independently |
| 4 | Materialized view stuck at 0% | Source table has no new data or backfill pending | Check `.show materialized-view MV statistics` |
| 5 | `.drop column` fails | Column used in materialized view or function | Remove dependent objects first |
| 6 | Retention deleting data too soon | Table-level policy overrides database default | Check `.show table T policy retention` |
| 7 | `Forbidden (403)` on management commands | Insufficient role | Request `admin` or `ingestor` database role |
| 8 | Streaming ingestion errors | Streaming policy not enabled | Run `.alter table T policy streamingingestion enable` |
| 9 | Ingest from OneLake fails with auth error | Missing `impersonate` in URI | Add `;impersonate` to storage URI |
| 10 | External table returns no data | Path or format mismatch | Verify path, format, and schema match the source files |


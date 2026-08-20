# Application Insights dynamic fields reference

**Critical:** many telemetry-to-business JOIN keys are **not** top-level columns.
In Application Insights / Azure Monitor tables, business identifiers are often
nested inside dynamic JSON-like columns. Schema verification MUST include
dynamic-field inspection — never rely on top-level schema alone.

## Common dynamic / object columns to inspect

- `Properties`
- `CustomDimensions`
- `Details`
- `Measurements`
- `Payload`
- `Context`
- `customDimensions`
- `customMeasurements`

## Business identifiers that commonly hide inside dynamic fields

`BookingId`, `booking_id`, `OrderId`, `order_id`, `CustomerId`, `customer_id`,
`UserId`, `user_id`, `UserAuthenticatedId`, `TenantId`, `tenant_id`, `AccountId`,
`FlightId`, `flight_number`, `PassportId`, `passport`, `SubscriptionId`,
`CorrelationId`, `OperationId`, `SessionId`, `Region`, `Country`, `ProductId`,
`ServiceName`.

## High-priority Application Insights tables for dynamic-field inspection

Before falling back to time-window correlation, inspect dynamic fields in the
following order:

Inspect these tables wherever they are queryable in the target KQL database —
**including telemetry that is already present as a native table**, not only the
shortcuts created in Stage 11. A business join key (e.g. `AppEvents.Properties`)
may already exist in the Eventhouse independently of the mirrored-catalog
shortcuts, so enumerate all telemetry tables in the database during Stage 12/13.

1. AppEvents
   - Properties
   - Measurements
   - Typical business identifiers:
     BookingId, OrderId, CustomerId, FlightId, SessionId, UserId

2. AppExceptions
   - Properties
   - Details
   - Typical business identifiers:
     PassportId, BookingId, CustomerId, TenantId, OperationId

3. AppRequests
   - Properties
   - Typical business identifiers:
     OperationId, SessionId, CustomerId, OrderId

4. AppDependencies
   - Properties
   - Typical business identifiers:
     CorrelationId, OrderId, TenantId, AccountId

5. AppTraces
   - Properties
   - Typical business identifiers:
     BookingId, CustomerId, OrderId, SessionId

6. AppPageViews

7. AppBrowserTimings

Only after inspecting these tables and validating candidate identifiers should
the Skill fall back to time-window correlation.

## Required dynamic-field verification steps

During schema verification (Stage 12):

1. Retrieve the real table schema with `getschema`.
2. Identify dynamic/object/string columns that may hold JSON-like business
   context.
3. Sample real rows from those columns.
4. Inspect the keys inside dynamic columns.
5. Extract candidate business identifiers with explicit KQL.
6. Validate candidate joins against real business tables (non-zero matches).
7. Prefer verified **direct joins** over time-window correlation.

## KQL patterns

> **Query convention.** Mirrored telemetry tables are **external tables** — query
> them via `external_table('<name>')` (they do not appear in `.show tables`).
> Business tables that live as **managed** tables in an Eventhouse are
> queried by their bare name. The examples below wrap telemetry accordingly.

### Inspect schema

```kusto
external_table('<TableName>')
| getschema
| project ColumnName, ColumnType
```

### Sample dynamic properties

```kusto
external_table('AppEvents')
| take 10
| project TimeGenerated, Name, Properties
```

### Extract possible business identifiers

```kusto
external_table('AppEvents')
| extend BookingId = tostring(Properties.BookingId)
| project TimeGenerated, Name, BookingId
```

### Alternative casing / naming (coalesce)

```kusto
external_table('AppEvents')
| extend BookingId = coalesce(
    tostring(Properties.BookingId),
    tostring(Properties.bookingId),
    tostring(Properties.booking_id)
  )
```

### Typed (bool / numeric) dynamic values

Not every dynamic value is a string. Boolean and numeric fields (e.g. a
`faulted` / `isError` flag, a `durationMs` or `amount`) are stored with their
real type and serialize as JSON literals (`true`/`false`, unquoted numbers).
Comparing them with `tostring(...) == "True"` silently matches **nothing**.
Cast to the real type and compare to a typed literal:

```kusto
external_table('AppEvents')
| where tobool(Properties.faulted) == true          // NOT tostring(...) == "True"
| extend amount = toreal(Properties.amount),
         retries = tolong(Properties.retryCount)
```

### Diagnose a zero-match filter before concluding "no data"

If a dynamic-field filter or join returns **0 rows**, confirm the value's real
type and distinct values before assuming the data is absent — a type/casing
mismatch is the most common cause:

```kusto
external_table('AppEvents')
| extend f = Properties.faulted
| summarize count() by value = tostring(f), type = gettype(f)
```

### Validate a direct join

```kusto
external_table('AppEvents')
| extend BookingId = tostring(Properties.BookingId)
| where isnotempty(BookingId)
| join kind=inner (
    Bookings
    | project BookingId = tostring(BookingId)
  ) on BookingId
| summarize MatchedRows=count(), DistinctBookings=dcount(BookingId)
```

## Confidence classification

- If a valid business identifier is found inside `Properties` / `CustomDimensions`
  and the join returns **non-zero** matches → classify as a **direct join, high
  confidence**.
- If no direct identifier is found after inspecting top-level columns **and**
  dynamic fields → fall back to **time-window correlation**, and state clearly
  that time-window correlation shows **correlation, not causality**.

> **Lesson learned:** screenshots can be misleading. A join key nested in
> `AppExceptions.Properties` (e.g. `passport`, `flight`) can yield a deterministic
> direct join to a business table even when top-level columns show nothing usable,
> and the real data window may be weeks older than assumed. Verify schema,
> dynamic fields, join matches, and freshness against real data first.

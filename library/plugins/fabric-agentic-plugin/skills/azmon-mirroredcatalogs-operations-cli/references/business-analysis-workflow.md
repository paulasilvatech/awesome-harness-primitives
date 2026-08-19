# Business analysis workflow (Stages 13–17)

Full detail for the **business-analysis half** of the skill. The operational
half (Stages 1–12) builds and verifies the environment in `SKILL.md`. Load this
reference at the **Stage 12 handoff** — once the user opts in to the
business-analysis half (impact modeling, an *optional* Real-Time (KQL) dashboard,
and an *optional* Operations Agent), e.g. confirms "Yes, continue with business
analysis based on this verified model." The Operations Agent (Stage 16) is opt-in
and runs **after** the optional dashboard (Stage 15), so do **not** gate loading
this file on the agent specifically — a user who wants only a dashboard still
needs Stages 13–15 from here.

These stages remain part of the STRICT STAGED WORKFLOW CONTROLLER: the stage
order, hard stops, and confirmation gates defined here are enforced exactly as if
they were inline in `SKILL.md`. `SKILL.md` no longer inlines these stages — it
keeps only a single pointer to this file at the Stage 12 handoff, plus the
Stages 13–17 entries in its controller Stages list. This file is the
authoritative, complete definition of the business-analysis half: follow the
steps, gates, and templates below verbatim once the user opts in.

## Stage 13 — Business data discovery and scoring

Business tables are **not** expected to exist in Log Analytics. They may live in
an Eventhouse, KQL database, Warehouse, Lakehouse, or via Fabric shortcuts.
Absence of business tables in Log Analytics MUST NOT be interpreted as absence of
business data — discover them across the available Fabric data surfaces.

If the exact business table or join is not known, do **not** fail. Score
candidate business databases/tables by likely relevance to the stated goal,
present a ranked list with explanation, propose shortcut creation for the top
candidates, and ask the user to choose. Never conclude "no correlation is
possible" without presenting options. Scoring hints are in
[Appendix A](#appendix-a-correlation-patterns-and-scoring).

## Stage 14 — Correlation planning

The user should not need to know joins, KQL, thresholds, or bins. Infer
candidates from verified top-level schema, verified dynamic fields, sampled
values, business table schema, actual join test results, and data freshness. When
asking for confirmation, ask about **business meaning**, not SQL/KQL, e.g.:

> "I found `BookingId` inside `AppEvents.Properties` and it matches
> `Bookings.BookingId`. Should I treat this as the booking identifier for
> business impact?"

Present a correlation plan (see
[Appendix B](#appendix-b-insight-modeling-and-thresholds))
including: operational signal; business impact table; verified join keys;
whether the join came from top-level columns or dynamic fields; match
count/validation result; time window + freshness status; proposed bin size;
metrics and thresholds. Then ask for confirmation and STOP.

Default modeling guidance: prefer **direct joins** when verified identifiers
exist; use **time-window correlation** only when no direct identifier is found
(and state clearly it shows correlation, not causality); default bin size **5
minutes** (larger when data is sparse or KPIs are slower); default derived entity
**IncidentBin**.

### Correlation planning validation (REQUIRED)

When finalizing the correlation model, the Skill MUST explain **why** the selected
telemetry source was chosen, justified using real data. Include:

- Match counts.
- Business identifiers discovered.
- Direct-join confidence.
- Validation results.

## Stage 15 — Optional dashboard suggestion and creation

Offer a **Real-Time (KQL) Dashboard** over the same verified KQL database, to
visualize the confirmed model. This stage is **optional** (offer it; act only if
the user wants it) and **suggest → approve → generate**: never create or modify a
dashboard before explicit approval. It comes **before** any Operations Agent
work — the user may want a dashboard and no agent at all. Because it runs before
the agent, do **not** assume an `IncidentBins`-style materialized table exists
yet — bind tiles to the Stage 12–14 verified columns, and use `IncidentBins` only
if it was already created.

Steps:

1. **Capability + source.** Confirm the target workspace and the Eventhouse / KQL
   database holding the verified/materialized data. A Service Principal is
   **documented as supported** to create and update a KQL Dashboard item with an
   application-only token; unlike the *observed* Mirrored Catalog app-only create
   fallback (see `SKILL.md`), we have not seen app-only dashboard create fail
   here. Normal workspace create permission and data-source binding still apply.
2. **Generate templates at runtime.** From the **verified model only**, infer a
   small set of candidate tiles. Each tile MUST reference columns/entities that
   were actually discovered and verified (Stages 12–14) — never invented, never
   assumed from any example. Bind every tile to a real KQL query against the KQL
   database.
3. **Frame by business need.** For each proposed tile, state the business
   question it answers in generic terms tied to the discovered schema (a metric
   trend over the incident window, a breakdown by an impacted entity, a
   single-stat KPI, a signal-vs-KPI overlay, an impact distribution). Choose and
   fill whichever patterns the real data supports; do not force a fixed set.
4. **Confirmation gate (HARD STOP).** Present the suggested tiles, then WAIT for
   the user to approve, revise (add/remove/change), or reject. Do not generate
   before explicit approval.
5. **Create on approval.** Create the dashboard item and apply the approved
   definition (tiles + KQL). Report what was created and offer to iterate. If the
   user is under a Service Principal and only reuse/update is intended, update an
   existing dashboard instead of creating a new one.

The tile set MUST stay domain-agnostic: derive names and semantics from the
user's real data, not from any illustrative example. See
[dashboard-reference.md](dashboard-reference.md) for the
create/update mechanics and the generic tile-pattern catalog.

## Stage 16 — Operations Agent instruction generation

### Gate — do we even want an agent? (MANDATORY, ask first)

Before doing any agent work, explicitly ask the user whether they want to build
an **Operations Agent** for automated business-impact alerting. Frame it in plain
terms, e.g. *"Do you want an Operations Agent that automatically alerts when this
business impact recurs, or is the dashboard enough for now?"*

- If the user says **no** (or "just the dashboard") → **skip Stages 16–17**; the
  business-analysis flow may end here. Do not generate instructions or create an
  agent.
- If the user says **yes** → proceed with instruction generation below.
- Never assume the user wants an agent — an agent is opt-in.

### Instruction generation

Only after the correlation model is confirmed. Produce a single clean copy/paste
block using the template in
[operations-agent-reference.md](operations-agent-reference.md).

The instructions MUST include **explicit KQL**, not conceptual descriptions:

- One verbatim **IncidentBin materialization query** whose **output columns are
  exactly the alert fields** (includes the `tostring(Properties.x)` extraction,
  the explicit `join`, and the exact aggregations).
- A per-field KQL definition list mapping each output column to a one-line
  expression.
- Alert rules that reference **actual output columns**.

Include **both** threshold sets:

- **Production-like:** e.g. ErrorCount increases by more than 20% versus the
  previous-hour baseline; AffectedCustomers ≥ configured business threshold;
  RevenueAtRisk ≥ configured business threshold.
- **Relaxed POC / debug:** e.g. `ErrorCount >= 1`; `ErrorCount >= 5 and
  AffectedBusinessRecords >= 1`; `AffectedCustomers >= 1`.

Required sections: Goal, Data sources, Field mapping definitions, Dynamic field
extraction logic, Derived analysis entity, IncidentBin materialization query,
Metric definitions, Correlation logic, Impact logic (production + POC), Alert
behavior, Output requirements, Validation / POC mode.

### PLAYBOOK MATERIALIZATION REQUIREMENT (MANDATORY)

Testing demonstrated that instructions and KQL **text alone are NOT sufficient**
for playbook generation — the Fabric Playbook Generator must be able to discover
the alert fields directly from a real schema object. Before generating Operations
Agent rules, the Skill MUST:

1. **Materialize IncidentBins** as a real, queryable schema object (a physical
   table or a function-backed table in the KQL database).
2. **Expose the alert fields as physical output columns** on that object.
3. **Verify the schema exists** (e.g. `IncidentBins | getschema`).

Required output columns:

- IncidentBin
- ErrorCount
- AffectedCustomers
- AffectedBookings
- RevenueAtRisk
- TopImpactedEntities
- TopImpactedSteps

The Playbook Generator MUST be able to discover these fields directly from the
materialized schema. KQL instructions alone are NOT sufficient. Business-specific
column names (for example `AffectedBookings`, `TopImpactedFlights`) adapt to the
business entities actually discovered in the data.

## Stage 17 — Optional Operations Agent creation / validation

Only if the user opted into an agent at Stage 16. Offer to create the Operations
Agent in the user's Fabric workspace and attach the Eventhouse / KQL database that
holds the verified data. Confirm target workspace and KQL database before creating
anything. Then guide validation (start with POC thresholds so an alert fires on
sparse seed data, then switch to production thresholds). See
[operations-agent-reference.md](operations-agent-reference.md)
for creation surface and troubleshooting.

---

## Appendix A: Correlation patterns and scoring

Reusable **observability signal → business impact** patterns, candidate join
keys, and scoring hints for ranking candidate business tables (used by Stage 13).
Always confirm business meaning with the user and verify keys against real data
before relying on them. Every business entity named here (bookings, orders,
customers, flights, revenue, tenants, payments, and similar) is an **EXAMPLE
ONLY** — do NOT infer the user's domain from these; discover and confirm the
real entities first.

### Patterns

#### 1. Availability → Bookings
- **Operational signal:** `AppRequests` failures, `AvailabilityResults` failures,
  `AppExceptions`.
- **Business impact:** failed / incomplete bookings.
- **Candidate keys:** `BookingId`, `CustomerId`, `SessionId`, `OperationId`,
  custom `Properties`.

#### 2. Latency → Conversion
- **Operational signal:** `AppRequests` duration, `AppPageViews`,
  `AppBrowserTimings`.
- **Business impact:** conversion drop, abandonment, funnel degradation.
- **Candidate keys:** `SessionId`, `UserId`, `CustomerId`, funnel event IDs.

#### 3. Exceptions → Orders / Revenue
- **Operational signal:** `AppExceptions`, `AppTraces`.
- **Business impact:** failed orders, revenue at risk.
- **Candidate keys:** `OrderId`, `CustomerId`, `TenantId`, `OperationId`,
  `Properties`.

#### 4. Dependency failures → Customer / Tenant impact
- **Operational signal:** `AppDependencies` failures / latency.
- **Business impact:** affected customers, tenants, regions, services.
- **Candidate keys:** `TenantId`, `AccountId`, `Region`, `DependencyTarget`.

#### 5. Regional outage → Business KPI impact
- **Operational signal:** `CloudRoleName`, `Region`, `ClientCountryOrRegion`,
  location fields.
- **Business impact:** regional bookings, customers, transactions, SLA.
- **Candidate keys:** `Region`, `Country`, `Location`, `AirportCode`,
  `DataCenter`.

#### 6. Traffic drop → Usage KPI degradation
- **Operational signal:** `AppEvents`, `AppPageViews`, `AppRequests` volume drop.
- **Business impact:** lower active users, reduced transactions, reduced revenue
  events.
- **Candidate keys:** `UserId`, `SessionId`, `ProductId`, event names.

### Business data scoring hints

When the exact business table or join is not known, **do not fail**. Score
candidate business databases/tables by likely relevance to the stated goal,
present a ranked list with explanation, propose shortcut creation for the top
candidates, and ask the user to choose. Never conclude "no correlation is
possible" without options.

| Business goal | Prioritize tables |
|---------------|-------------------|
| Booking impact | Bookings, Reservations, Orders, Flights, Customers, Transactions |
| Revenue impact | Orders, Payments, Revenue, Invoices, Subscriptions |
| Customer impact | Customers, Accounts, Tenants, Users, Subscriptions |
| Regional impact | Regions, Locations, Airports, DataCenters, Countries |
| Service availability | AppRequests, AvailabilityResults, AppExceptions, AppDependencies + business completion tables |
| Conversion | AppEvents, AppPageViews, AppRequests + funnel/business event tables |

### Candidate key reference

Infer candidates from column/table names; confirm meaning with the user and
verify against real data before relying on them.

- **Customer identifiers:** `CustomerId`, `UserId`, `PassportRef`, `AccountId`,
  `TenantId`, `SubscriptionId`.
- **Entity identifiers:** `FlightId`, `OrderId`, `BookingId`, `SessionId`,
  `OperationId`, `RequestId`, `ResourceId`.
- **Timestamps:** `TimeGenerated`, `Timestamp`, `EventTime`, `BookingTime`,
  `CreatedTime`.
- **Region/location:** `Region`, `Location`, `originAirport`,
  `destinationAirport`, `Country`, `DataCenter`.

### Table classification hints

- **Operational telemetry:** AppEvents, AppExceptions, AppRequests, AppPageViews,
  AppBrowserTimings, AppDependencies, AvailabilityResults, AzureMetrics, Perf,
  Usage.
- **Business tables:** Bookings, Customers, Flights, Orders, Payments,
  CounterCheckins, Subscriptions, Invoices.
- **Context/enrichment tables:** Flights, Regions, Products, Services, Tenants,
  Airports.

Confirm business meaning with the user; never fabricate tables the user has not
confirmed.

---

## Appendix B: Insight modeling and thresholds

How to turn a **verified** telemetry + business dataset into a correlation model
without asking the user for joins, KQL, bins, or thresholds (used by Stage 14).
The user confirms **business meaning**; the Skill translates it into the technical
model.

### Inputs the model is inferred from

- Verified top-level schema (`getschema`).
- Verified dynamic fields (sampled `Properties` / `CustomDimensions`).
- Sampled values.
- Business table schema.
- Actual join test results (non-zero match counts).
- Data freshness (real min/max time range).

Never propose a model before these are verified (Stage 12).

### Direct join vs time-window correlation

- **Direct join (preferred, high confidence):** a shared identifier exists and a
  test join returns non-zero matches. Use it. State the match count.
- **Time-window correlation (fallback):** no shared identifier after inspecting
  top-level and dynamic fields. Correlate events within the same time bin. Always
  state that this shows **correlation, not causality**.

### Bins

- **Default bin size: 5 minutes.** Explain it as granular enough to catch short
  operational spikes while aggregating enough events to be meaningful and reduce
  per-event noise.
- Use a **larger** bin when data is **sparse** (few events → 15–60 min) or when
  business KPIs are **slower** (e.g. daily bookings). Adjust for very noisy /
  high-volume data to stabilize the signal.

### Derived entity

- Default derived entity name: **IncidentBin** (unless a better
  business-specific name exists).
- Each IncidentBin represents one time window and is the unit of analysis for
  metrics and alert rules.

### Confirming business meaning (not SQL)

Ask about meaning, e.g.:

> "I found `BookingId` inside `AppEvents.Properties` and it matches
> `Bookings.BookingId`. Should I treat this as the booking identifier for
> business impact?"

Do not ask "what join should I use?" or "what bin/threshold do you want?".

### Correlation plan contents (present before generating instructions)

- Operational signal (which table/event indicates the problem).
- Business impact table.
- Verified join keys.
- Whether the join came from **top-level columns** or **dynamic fields**
  (`Properties` / `CustomDimensions`).
- Match count / validation result.
- Time window + freshness status.
- Proposed bin size.
- Metrics and thresholds.

Then ask for confirmation and STOP. The selected telemetry source must be
justified against actual data (match counts, business identifiers discovered,
direct-join confidence, validation results) — never chosen by default or
assumption; candidates must have been inspected and scored first (see
[telemetry-table-reference.md](telemetry-table-reference.md)).

### Metrics (typical)

- `ErrorCount` — faulted operational events per IncidentBin.
- `AffectedCustomers` — distinct impacted customers per IncidentBin.
- `AffectedBusinessRecords` — impacted business records per IncidentBin.
- `RevenueAtRisk` — summed revenue of impacted records per IncidentBin.
- `TopImpactedEntities` — top impacted entities by impact.
- `ImpactBand` — high / low / none.

### Thresholds

Always include **both** sets in the generated instructions.

- **Production-like:**
  - ErrorCount increases by more than 20% vs previous-hour baseline.
  - AffectedCustomers ≥ configured business threshold.
  - RevenueAtRisk ≥ configured business threshold.
- **Relaxed POC / debug** (validate Start + Teams alert end-to-end):
  - `ErrorCount >= 1`
  - `ErrorCount >= 5 and AffectedBusinessRecords >= 1`
  - `AffectedCustomers >= 1`

### Freshness and time window

Check the real data range before generating instructions:

```kusto
external_table('<TableName>')
| summarize Rows=count(), MinTime=min(TimeGenerated), MaxTime=max(TimeGenerated)
```

If data is old or sparse, do not assume `ago(1h)` — use a window covering the
actual range and explain it in user terms. Watch for locale-formatted timestamps
(DD/MM vs MM/DD) when reading results.

The materialization query output columns MUST match the alert fields exactly. See
[operations-agent-reference.md](operations-agent-reference.md) for the
explicit-KQL requirement and the full instruction template.

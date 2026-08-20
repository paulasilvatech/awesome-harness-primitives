# Operations Agent reference

Everything needed to generate, create, validate, and troubleshoot a Microsoft
Fabric **Operations Agent** over the Eventhouse/KQL database holding the verified
telemetry + business data. The end product is a clean copy/paste block of
instructions the user pastes into Fabric.

## Core principle

The user is **not** expected to know join logic, time binning, derived-entity
modeling, metric computation, or thresholds. Never open with "what JOIN should I
use?" or "what bin/threshold do you want?". Infer candidates from the **verified**
schema (Stage 12), propose in business language, confirm business meaning, then
translate to the technical model on the user's behalf.

## Give explicit per-field KQL, not conceptual descriptions (REQUIRED)

The Fabric playbook generator will **not infer** joins, aggregations, or how to
compute a metric. Conceptual-only field names (e.g. "AffectedCustomers",
"RevenueAtRisk") cause generation to fail with **"No playbook generated"** and
"I was not able to determine how to compute X". To avoid this:

- Provide **one verbatim materialization query** whose **output columns ARE the
  alert fields** (the `summarize`/`extend` produces `ErrorCount`,
  `AffectedCustomers`, `RevenueAtRisk`, … by `IncidentBin`). Include the
  `tostring(Properties.x)` extraction, the explicit `join`, and the exact
  aggregations (`count()`, `dcount()`, `dcountif()`, `sum()`, `make_set()`).
- Add a **field-definition list** restating each output column's KQL in one line
  (e.g. `AffectedCustomers = dcount(passport) by IncidentBin`), so message
  placeholders map 1:1 to columns.
- Make each **alert rule reference a concrete output column**. If one metric
  drives both the trigger and the message text (e.g. `RevenueAtRisk >= 1000` and
  `$<RevenueAtRisk>` in the message), say so explicitly.

## Playbook materialization requirement (MANDATORY)

Operations Agent creation can succeed while **playbook generation still fails**
until the incident entity is materialized as a real, queryable schema object.
Testing confirmed that instructions and KQL text alone are NOT sufficient — the
Playbook Generator discovers alert fields from an actual schema, not from prose.

Before generating Operations Agent rules:

1. **Materialize IncidentBins** as a real, queryable schema object (a physical
   table, or a stored-function-backed table, in the KQL database).
2. **Expose the alert fields as physical output columns.**
3. **Verify the schema exists** (`IncidentBins | getschema`).

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
column names adapt to the business entities actually discovered in the data.

## Required sections of the generated instructions

Goal · Data sources · Field mapping definitions · Dynamic field extraction logic ·
Derived analysis entity · IncidentBin materialization query · Metric definitions ·
Correlation logic · Impact logic (production + POC) · Alert behavior · Output
requirements · Validation / POC mode.

## Instruction template

Fill `<...>` placeholders with confirmed table/column names. Leave unknowns as
explicit placeholders — do not invent schema. Output as one copy/paste block.

```text
Goal:
Detect operational incidents and correlate them with business impact.

Data sources:
Operational telemetry tables:
- <OperationalTable>
Business tables:
- <BusinessTable>
Context/enrichment tables:
- <ContextTable>

Field mapping definitions:
- Customer identifier: <BusinessTable>.<CustomerIdColumn>
- Operational time:    <OperationalTable>.<OperationalTimestampColumn>
- Business time:       <BusinessTable>.<BusinessTimestampColumn>

Dynamic field extraction logic:
- Extract business keys nested in dynamic columns, e.g.
  BusinessKey = tostring(<OperationalTable>.Properties.<KeyName>)
- Use coalesce() for casing/naming variants:
  BusinessKey = coalesce(
    tostring(Properties.<KeyName>),
    tostring(Properties.<keyName>),
    tostring(Properties.<key_name>))

Join keys:
- Join <OperationalTable> to <BusinessTable> on <JoinKey> when available.
- If no direct key exists, correlate within the same 5-minute time bin
  (correlation, not causality).

Derived analysis entity:
Create IncidentBin. Each IncidentBin is one 5-minute window and is the unit of
analysis for rules and alerts.

IncidentBin materialization query (output columns == alert fields):
(Telemetry tables are external tables → query via external_table('<name>'). The
business table is bare if it is a managed table, or external_table('<name>') if
it too is a OneLake shortcut.)
external_table('<OperationalTable>')
| where <OperationalTimestampColumn> between (datetime(<MinTime>) .. datetime(<MaxTime>))
| extend BusinessKey = tostring(Properties.<KeyName>)
| where isnotempty(BusinessKey)
| join kind=inner (
    <BusinessTable>
    | project BusinessKey = tostring(<JoinKey>), <CustomerIdColumn>, <RevenueColumn>
  ) on BusinessKey
| summarize
    ErrorCount             = count(),
    AffectedCustomers      = dcount(<CustomerIdColumn>),
    AffectedBusinessRecords = dcount(BusinessKey),
    RevenueAtRisk          = sum(<RevenueColumn>),
    TopImpactedEntities    = make_set(<ContextColumn>, 3),
    TopImpactedSteps       = make_set(<OperationStepColumn>, 3)
    by IncidentBin = bin(<OperationalTimestampColumn>, 5m)

Metric definitions:
- ErrorCount = count() of faulted operational events by IncidentBin.
- AffectedCustomers = dcount(<CustomerIdColumn>) by IncidentBin.
- AffectedBusinessRecords = dcount(BusinessKey) by IncidentBin.
- RevenueAtRisk = sum(<RevenueColumn>) by IncidentBin.
- TopImpactedEntities = make_set(<ContextColumn>, 3) by IncidentBin.
- TopImpactedSteps = make_set(<OperationStepColumn>, 3) by IncidentBin.

Correlation logic:
Evaluate each IncidentBin for operational degradation and business impact.
Use direct joins when verified identifiers exist; otherwise time-window
correlation (correlation, not causality).

Impact logic:
Production-like thresholds:
- ErrorCount increases by more than 20% vs previous-hour baseline.
- AffectedCustomers >= <configured business threshold>.
- RevenueAtRisk >= <configured business threshold>.
POC / debug thresholds (validate Start + Teams alert end-to-end):
- ErrorCount >= 1
- ErrorCount >= 5 and AffectedBusinessRecords >= 1
- AffectedCustomers >= 1

Alert behavior:
- One alert per 5-minute IncidentBin.
- Include business context and recommended action.

Output requirements:
Alert title, incident time window, ErrorCount, AffectedCustomers,
AffectedBusinessRecords, RevenueAtRisk, TopImpactedEntities, business impact
summary, recommended action, investigation link if available.

Validation / POC mode:
Start with POC thresholds to confirm Start runs and a Teams alert arrives, then
switch to production-like thresholds for steady-state monitoring.
```

## Creating the agent (optional Stage 17)

Operations Agent is a first-class Fabric item (`type: "OperationsAgent"`), so it
can be created and populated through documented Fabric item APIs.

> **Auth restriction (verified — MUST check before this stage).** The Create
> OperationsAgent API supports a **User (delegated) identity only** — **service
> principal and managed identity are NOT supported**
> ([Microsoft Learn: Create Operations Agent](https://learn.microsoft.com/en-us/rest/api/fabric/operationsagent/items/create-operations-agent)
> — Microsoft Entra supported identities: User = Yes, Service principal & Managed
> identities = No). If the current session is authenticated as a service principal
> or managed identity, STOP and instruct the user to switch to delegated user auth
> before creating the agent; the create call will otherwise fail. (The
> OperationsAgent item is in Preview.)

1. Create the agent item in the target workspace (capture the returned item id).
2. Read the current definition, set `configuration.instructions` to the Instruction template
   block, and add the KQL database under `configuration.dataSources` as a
   `KustoDatabase` entry keyed by a friendly alias; then update the definition.
   Do **not** include an empty `playbook` object (it fails with "No rule
   definitions available in the playbook.").
3. Use the real **KQL database** item id (the `KQLDatabase` item whose display
   name matches the target Eventhouse — not the `Eventhouse` item).

Note (verified behavior): `updateDefinition` reliably saves the **instructions**
text, but live **bindings** (`dataSources[].id`, `messageDestination`) may read
back as placeholders (all-zeros / null) even on `200` — the portal Build page is
authoritative and typically shows the attached KQL database. Have the user open
the agent's **Build** page to confirm the Knowledge data source, let the playbook
generate, then **Save** and **Start**. Teams notifications are a built-in action;
no custom channel binding is required for basic alerts.

## Validation & troubleshooting

- **"No playbook generated" / "cannot compute X"** → conceptual-only fields, or
  the incident entity was not materialized as a real schema object. Materialize
  IncidentBins so its output columns are physical, discoverable columns; add the
  explicit materialization query (output columns == alert fields), the
  per-field KQL list, dynamic-field extraction, and concrete join keys; ensure
  each alert rule references an actual output column. Map specific messages:
  missing thresholds → add numeric thresholds; missing field mapping → add
  explicit field definitions; missing customer/entity id → add the identifier
  mapping; missing join key → specify keys or fall back to 5-minute correlation;
  missing time column → specify the timestamp columns.
- **Start succeeds but no Teams alert** → likely no data matched (thresholds too
  strict for the window). Switch to POC thresholds (`ErrorCount >= 1`, or
  `ErrorCount >= 5 and AffectedCustomers >= 1`), then restore production
  thresholds. Do not imply platform failure without evidence.

## Guardrails

- Do not fabricate schema — use placeholders when names are unknown.
- Confirm business meaning before producing final instructions.
- Say "correlated", not "caused", when only time-window correlation exists.
- Do not require the user to know KQL or joins.
- Only recommend adding Actions when the user needs capabilities beyond the
  built-in Teams alerts.


## External References

### Microsoft Learn

Create and Configure Operations Agents - Microsoft Fabric

https://learn.microsoft.com/en-us/fabric/real-time-intelligence/operations-agent

### Microsoft Community Hub

Microsoft Fabric Operations Agent Step by Step Walkthrough

https://techcommunity.microsoft.com/blog/analyticsonazure/microsoft-fabric-operations-agent-step-by-step-walkthrough/4512572

Use these references when:
- creating new Operations Agents
- understanding playbook generation behavior
- troubleshooting rule generation failures
- validating expected Operations Agent workflow


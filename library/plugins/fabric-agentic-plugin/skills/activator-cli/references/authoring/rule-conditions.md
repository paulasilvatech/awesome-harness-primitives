# Activator Rule Conditions — `timeSeriesView-v1` Templates & Rule Logic

> ⚠️ **Every template-backed `timeSeriesView-v1` entity MUST be wrapped in a `timeSeriesView-v1` entity envelope** with the template JSON.stringify'd into `definition.instance`. Never output a raw template — always output the full entity.

---

This reference covers the **template-backed `timeSeriesView-v1` entities** used in Activator definitions:

- **Rule views** (`definition.type = "Rule"`)
- **Event views** such as `SourceEvent` and `SplitEvent` (`definition.type = "Event"`)
- **Attribute views** such as `IdentityPartAttribute` and `BasicEventAttribute` (`definition.type = "Attribute"`)

Rules are the main focus because this file explains condition rows, detectors, aggregation, occurrence options, and actions, but the same `timeSeriesView-v1` envelope and template conventions also apply to the other view types listed below.

## Rule view entity envelope

Rules are `timeSeriesView-v1` entities with `definition.type = "Rule"`:

```json
{
  "uniqueIdentifier": "<guid>",
  "payload": {
    "name": "Too hot for medicine",
    "description": "Created by: skills-for-fabric",
    "parentObject": { "targetUniqueIdentifier": "<object-guid>" },
    "parentContainer": { "targetUniqueIdentifier": "<container-guid>" },
    "definition": {
      "type": "Rule",
      "instance": "<JSON-encoded template — MUST be a string, not nested object>",
      "settings": { "shouldRun": true, "shouldApplyRuleOnUpdate": false }
    }
  },
  "type": "timeSeriesView-v1"
}
```

> **Critical:** `definition.instance` is a **JSON-encoded string**. You must `JSON.stringify()` the template object and set it as a string value, not a nested object.

For user clarity, add `payload.description: "Created by: skills-for-fabric"` to rule entities.

Settings: `shouldRun` (boolean — is rule active), `shouldApplyRuleOnUpdate` (boolean — re-evaluate on definition update).

Default new rules to `shouldRun: true` so they start in the **started / running** state. Use `shouldRun: false` only when the user explicitly wants a stopped rule or when a safe verification workflow intentionally requires a disabled rule.

---

## Rule Template Structure

> **Template version:** Default newly authored rules to `1.2.4` unless backend guidance or a known-good readback requires a newer version. Features such as Fabric item parameters require at least `1.2`, and flexible item types / UDF `subitemId` require at least `1.2.3`, so `1.2.4` covers the known public requirements. When modifying an existing source-created graph, preserve the existing template shape unless the new rows require a newer version.

```json
{ "templateId": "AttributeTrigger", "templateVersion": "1.2.4",
  "steps": [
    { "name": "ScalarSelectStep", "id": "<guid>", "rows": [...] },
    { "name": "ScalarDetectStep", "id": "<guid>", "rows": [...] },
    { "name": "DimensionalFilterStep", "id": "<guid>", "rows": [...] },
    { "name": "ActStep", "id": "<guid>", "rows": [...] }
  ]
}
```

### Template IDs

| templateId | Used For | Step Sequence |
|------------|----------|---------------|
| `AttributeTrigger` | Rule views | `ScalarSelectStep → ScalarDetectStep → (DimensionalFilterStep)* → ActStep` |
| `EventTrigger` | Rule views | `FieldsDefaultsStep → (EventDetectStep)+ → (DimensionalFilterStep)* → ActStep` |
| `SourceEvent` | Event views | `SourceEventStep` |
| `SplitEvent` | Event views | `SplitEventStep` |
| `IdentityPartAttribute` | Attribute views | `IdPartStep` |
| `BasicEventAttribute` | Attribute views | `EventSelectStep → EventComputeStep` |

### Step Sequence Notation

- `*` means **zero or more**
- `+` means **one or more**

### Minimal EventTrigger Entity Graph

For pure event-trigger scenarios, the minimal valid graph is:

```text
Container -> Source -> SourceEvent -> Rule
                        \
                         -> (optional) fabricItemAction-v1
```

Do **not** add Object, SplitEvent, IdentityPartAttribute, or BasicEventAttribute entities unless you are intentionally switching to attribute-based modeling.

### Required FieldsDefaultsStep

Every `EventTrigger` must begin with exactly one `EventSelector` row. The
`EventReference` is nested inside that selector and points to the SourceEvent
entity. Do not place an `EventReference` row directly in `FieldsDefaultsStep`;
RSA rejects that shape with `InvalidTemplateInstance`.

```json
{
  "name": "FieldsDefaultsStep",
  "id": "<guid>",
  "rows": [
    {
      "name": "EventSelector",
      "kind": "Event",
      "arguments": [
        {
          "name": "event",
          "kind": "EventReference",
          "type": "complex",
          "arguments": [
            {
              "name": "entityId",
              "type": "string",
              "value": "<source-event-entity-guid>"
            }
          ]
        }
      ]
    }
  ]
}
```

### EventDetectStep Branches

Use exactly ONE branch per step:

| Branch | Rows | Use Case |
|--------|------|----------|
| `EventHeartbeatDetector` | `OnEveryValue` or `NoHeartbeat` alone | Fire on every event, or detect missing events |
| `EventStateDetector` | `EventFieldSelector` + state condition | Fire when event field meets condition |
| `EventChangeDetector` | `EventFieldSelector` + change condition | Fire when event field changes |

**OnEveryValue:**
```json
{ "name": "EventDetectStep", "id": "<guid>",
  "rows": [{ "name": "OnEveryValue", "kind": "OnEveryValue", "arguments": [] }] }
```

**NoHeartbeat (fire when events STOP — e.g., 5min = 300000ms):**
```json
{ "name": "EventDetectStep", "id": "<guid>",
  "rows": [{ "name": "NoHeartbeat", "kind": "NoHeartbeat",
    "arguments": [{ "name": "duration", "type": "timeSpan", "value": 300000 }] }] }
```

**EventStateDetector (field + state condition):**
```json
{ "name": "EventDetectStep", "id": "<guid>",
  "rows": [
    { "name": "EventFieldSelector", "kind": "EventField",
      "arguments": [{ "name": "fieldName", "type": "string", "value": "severity" }] },
    { "name": "TextValueCondition", "kind": "TextValueCondition",
      "arguments": [
        { "name": "op", "type": "string", "value": "IsEqualTo" },
        { "name": "value", "type": "string", "value": "Error" }] }
  ] }
```

State conditions: `NumberValueCondition`, `NumberRangeCondition`, `TextValueCondition`, `TextLengthCondition`, `LogicalValueCondition`.

**EventChangeDetector (field + change condition):**
```json
{ "name": "EventDetectStep", "id": "<guid>",
  "rows": [
    { "name": "EventFieldSelector", "kind": "EventField",
      "arguments": [{ "name": "fieldName", "type": "string", "value": "status" }] },
    { "name": "AnyValueChange", "kind": "AnyValueChange",
      "arguments": [{ "name": "op", "type": "string", "value": "Changes" }] }
  ] }
```

Change conditions: `NumberBecomes`, `NumberEntersOrLeavesRange`, `NumberChanges`, `NumberTrendsBy`, `TextChanges`, `LogicalBecomes`, `AnyValueChange`.

> ⚠️ **Common mistakes:** A top-level `EventReference` row in `FieldsDefaultsStep` is invalid; wrap it in the required `EventSelector` row. `EachTime` is an OccurrenceOption for AttributeTrigger's ScalarDetectStep — NOT valid in EventDetectStep. A bare `AnyValueChange` without `EventFieldSelector` before it causes `RowCountMismatch`. Another common mistake is overbuilding an Object/SplitEvent/Attribute graph for a rule that should just use `SourceEvent` + `EventTrigger`.

---

## Row Kinds Quick Reference

### State Conditions (fires while condition holds)

| kind | `op` values | Arguments |
|------|-------------|-----------|
| `NumberValueCondition` | `IsEqualTo`, `IsNotEqualTo`, `IsGreaterThan`, `IsGreaterThanOrEqualTo`, `IsLessThan`, `IsLessThanOrEqualTo` | `op` (string), `threshold` (number) |
| `NumberRangeCondition` | `IsInsideRange`, `IsOutsideRange` | `op` (string), `low` (number), `includeLow` (boolean), `high` (number), `includeHigh` (boolean) |
| `TextValueCondition` | `IsEqualTo`, `IsNotEqualTo`, `BeginsWith`, `Contains`, `EndsWith`, `DoesNotBeginWith`, `DoesNotContain`, `DoesNotEndWith` | `op` (string), `value` (string) |
| `TextLengthCondition` | `HasLengthGreaterThan`, `HasLengthGreaterThanOrEqualTo`, `HasLengthLessThan`, `HasLengthLessThanOrEqualTo`, `HasLengthEqualTo`, `HasLengthNotEqualTo` | `op` (string), `length` (number) |
| `LogicalValueCondition` | `IsEqual`, `IsNotEqual` | `op` (string), `value` (boolean) |

### Change Conditions (fires on transition)

| kind | `op` values | Arguments |
|------|-------------|-----------|
| `NumberBecomes` | `BecomesGreaterThan`, `BecomesGreaterThanOrEqualTo`, `BecomesLessThan`, `BecomesLessThanOrEqualTo` | `op` (string), `value` (number) |
| `NumberEntersOrLeavesRange` | `EntersRange`, `LeavesRange` | `op` (string), `low` (number), `includeLow` (boolean), `high` (number), `includeHigh` (boolean) |
| `NumberChanges` | `ChangesFrom`, `ChangesTo` | `op` (string), `value` (number) |
| `NumberChangesFromTo` | _(no op)_ | `oldValue` (number), `newValue` (number) |
| `NumberTrendsBy` | `DecreasesByAtLeast`, `IncreasesByAtLeast`, `ChangesByAtLeast` | `op` (string), `offset` (number), `inPercent` (boolean) |
| `TextChanges` | `ChangesFrom`, `ChangesTo` | `op` (string), `value` (string) |
| `TextChangesFromTo` | _(no op)_ | `oldValue` (string), `newValue` (string) |
| `LogicalBecomes` | `BecomesTrue`, `BecomesFalse` | `op` (string) |
| `AnyValueChange` | `Changes` | `op` (string) |

### Heartbeat Conditions

| kind | Arguments |
|------|-----------|
| `NoHeartbeat` | `duration` (timeSpan) |
| `OnFirstHeartbeat` | `duration` (timeSpan, optional) |

### Occurrence Options (optional, follows a detection row in ScalarDetectStep)

| kind | Description | Arguments |
|------|-------------|-----------|
| `EachTime` | Fire every time condition is met | _(none)_ |
| `ForNthTime` | Fire after N occurrences within a window | `n` (number), `duration` (timeSpan) |

### State Detector Option (optional, follows a state condition)

| kind | Description | Arguments |
|------|-------------|-----------|
| `SustainedPeriodOption` | Condition must persist for a duration before firing | `period` (timeSpan) |

---

## ScalarSelectStep — Attribute Selection & Aggregation

### Attribute Reference

```json
{ "name": "AttributeSelector", "kind": "Attribute",
  "arguments": [{
    "kind": "AttributeReference", "type": "complex", "name": "attribute",
    "arguments": [{ "name": "entityId", "type": "string", "value": "<attribute-entity-guid>" }]
  }] }
```

### Aggregation (NumberSummary)

```json
{ "name": "NumberSummary", "kind": "NumberSummary",
  "arguments": [
    { "name": "op", "type": "string", "value": "Average" },
    { "kind": "TimeDrivenWindowSpec", "type": "complex", "name": "window",
      "arguments": [
        { "name": "width", "type": "timeSpan", "value": 600000.0 },
        { "name": "hop", "type": "timeSpan", "value": 600000.0 }
      ] }
  ] }
```

Aggregation ops: `Average`, `Sum`, `Min`, `Max`, `Count`.

### Time Windows (`TimeDrivenWindowSpec`)

Values in **milliseconds**: 1min=60000, 5min=300000, 10min=600000, 30min=1800000, 1hr=3600000, 6hr=21600000, 24hr=86400000.

`width` = window size. `hop` = advance interval (= `width` for tumbling, smaller for sliding).

---

## ScalarDetectStep — Detection Conditions

Accepts **one** detection row (state or change — see Quick Reference), plus an optional occurrence modifier.

> **Default alerting preference:** for most notification scenarios, prefer **change / transition** detectors over steady-state detectors. Use `NumberBecomes`, `NumberEntersOrLeavesRange`, `LogicalBecomes`, or other explicit change conditions even when the user uses state-like wording such as "is greater than", "is below", or "is outside the normal range". Interpret ordinary alert wording as "notify me when it crosses into that state". Reserve steady-state conditions like `IsGreaterThan`, `IsLessThan`, and `IsOutsideRange` for cases where repeated firing while the condition remains true is intentionally desired, such as "notify me every time it is greater than 30" or "fire on every evaluation while it is above 30".

### NumberValueCondition

> **Note:** Uses `threshold` (not `value`) as argument name.

```json
{ "name": "NumberValueCondition", "kind": "NumberValueCondition",
  "arguments": [
    { "name": "op", "type": "string", "value": "IsGreaterThan" },
    { "name": "threshold", "type": "number", "value": 25.0 }] }
```

### NumberBecomes

Fires only on transition, not while condition remains true:

```json
{ "name": "NumberBecomes", "kind": "NumberBecomes",
  "arguments": [
    { "name": "op", "type": "string", "value": "BecomesGreaterThan" },
    { "name": "value", "type": "number", "value": 30.0 }] }
```

Use `BecomesGreaterThan` / `BecomesLessThan` when the goal is to avoid alert spam from repeated evaluations of the same high / low state.

### NumberEntersOrLeavesRange (change) & NumberRangeCondition (state)

> ⚠️ **Range change uses `NumberEntersOrLeavesRange`**, NOT `NumberBecomes`. Range state uses `NumberRangeCondition`.

Both share args: `op`, `low` (number), `includeLow` (boolean), `high` (number), `includeHigh` (boolean).

```json
{ "name": "NumberEntersOrLeavesRange", "kind": "NumberEntersOrLeavesRange",
  "arguments": [
    { "name": "op", "type": "string", "value": "LeavesRange" },
    { "name": "low", "type": "number", "value": 10.0 },
    { "name": "high", "type": "number", "value": 25.0 },
    { "name": "includeLow", "type": "boolean", "value": true },
    { "name": "includeHigh", "type": "boolean", "value": true }] }
```

For state: use kind `NumberRangeCondition` with ops `IsInsideRange` / `IsOutsideRange`.

For most alerting scenarios, prefer `EntersRange` / `LeavesRange` over `IsInsideRange` / `IsOutsideRange` so the rule fires when the value crosses the boundary rather than on every subsequent evaluation while it remains in-range or out-of-range.

### TextValueCondition

```json
{ "name": "TextValueCondition", "kind": "TextValueCondition",
  "arguments": [
    { "name": "op", "type": "string", "value": "IsEqualTo" },
    { "name": "value", "type": "string", "value": "Critical" }] }
```

For prompts like "alert when more than 10 ERROR readings occur in 5 minutes", select the text/status attribute, use `TextValueCondition` with an op such as `IsEqualTo`, then add an `OccurrenceOption` row. Do **not** model this as `NumberSummary` / `Count` over the text attribute, and do **not** put count operators into `TextValueCondition.op`; the backend expects text conditions to receive text operators and will reject mismatched count/numeric encodings.

```json
{ "name": "ScalarDetectStep", "id": "<guid>",
  "rows": [
    { "name": "TextValueCondition", "kind": "TextValueCondition",
      "arguments": [
        { "name": "op", "type": "string", "value": "IsEqualTo" },
        { "name": "value", "type": "string", "value": "ERROR" }] },
    { "name": "OccurrenceOption", "kind": "ForNthTime",
      "arguments": [
        { "name": "n", "type": "number", "value": 11 },
        { "name": "duration", "type": "timeSpan", "value": 300000 }] }
  ] }
```

Use `n = threshold + 1` for "more than N" wording. For example, "more than 10 ERROR readings" maps to `ForNthTime` with `n = 11` in the 5-minute window.

### TextLengthCondition

```json
{ "name": "TextLengthCondition", "kind": "TextLengthCondition",
  "arguments": [
    { "name": "op", "type": "string", "value": "HasLengthGreaterThan" },
    { "name": "length", "type": "number", "value": 100 }] }
```

### LogicalBecomes (change) & LogicalValueCondition (state)

Attribute must use `"Logical"` TypeAssertion.

```json
{ "name": "LogicalBecomes", "kind": "LogicalBecomes",
  "arguments": [{ "name": "op", "type": "string", "value": "BecomesTrue" }] }
```

```json
{ "name": "LogicalValueCondition", "kind": "LogicalValueCondition",
  "arguments": [
    { "name": "op", "type": "string", "value": "IsEqual" },
    { "name": "value", "type": "boolean", "value": false }] }
```

### NumberTrendsBy

> ⚠️ **Row name ≠ kind:** `name` is `"NumberTrends"`, `kind` is `"NumberTrendsBy"`. Wrong name causes API rejection.

```json
{ "name": "NumberTrends", "kind": "NumberTrendsBy",
  "arguments": [
    { "name": "op", "type": "string", "value": "IncreasesByAtLeast" },
    { "name": "offset", "type": "number", "value": 10.0 },
    { "name": "inPercent", "type": "boolean", "value": false }] }
```

Set `inPercent: true` for percentage-based trends.

### Value Change Detection

> ⚠️ **Row name ≠ kind for `FromTo` variants:** `NumberChangesFromTo` and `TextChangesFromTo` kinds use row names `"NumberChanges"` and `"TextChanges"` respectively.

```json
{ "name": "NumberChanges", "kind": "NumberChanges",
  "arguments": [
    { "name": "op", "type": "string", "value": "ChangesTo" },
    { "name": "value", "type": "number", "value": 0 }] }
```

```json
{ "name": "TextChanges", "kind": "TextChanges",
  "arguments": [
    { "name": "op", "type": "string", "value": "ChangesTo" },
    { "name": "value", "type": "string", "value": "ERROR" }] }
```

```json
{ "name": "AnyValueChange", "kind": "AnyValueChange",
  "arguments": [{ "name": "op", "type": "string", "value": "Changes" }] }
```

### Name ≠ Kind Reference

| Row Name (`name`) | Picker Kind (`kind`) |
|-------------------|---------------------|
| `NumberTrends` | `NumberTrendsBy` |
| `NumberChanges` | `NumberChanges` or `NumberChangesFromTo` |
| `TextChanges` | `TextChanges` or `TextChangesFromTo` |

### Heartbeat Conditions (AttributeTrigger ScalarDetectStep only)

```json
{ "name": "OnFirstHeartbeat", "kind": "OnFirstHeartbeat", "arguments": [] }
```

```json
{ "name": "NoHeartbeat", "kind": "NoHeartbeat",
  "arguments": [{ "name": "duration", "type": "timeSpan", "value": 300000 }] }
```

---

## Occurrence Options

```json
{ "name": "OccurrenceOption", "kind": "EachTime", "arguments": [] }
```

```json
{ "name": "OccurrenceOption", "kind": "ForNthTime",
  "arguments": [
    { "name": "n", "type": "number", "value": 5 },
    { "name": "duration", "type": "timeSpan", "value": 3600000 }] }
```

**SustainedPeriodOption** — state detector option, placed after a state condition row:

```json
{ "name": "SustainedPeriodOption", "kind": "SustainedPeriodOption",
  "arguments": [{ "name": "period", "type": "timeSpan", "value": 300000 }] }
```

---

## DimensionalFilterStep — Additional Filters

Optional step filtering which objects the rule applies to. Uses same condition kinds as ScalarDetectStep.

```json
{ "name": "DimensionalFilterStep", "id": "<guid>",
  "rows": [
    { "name": "AttributeSelector", "kind": "Attribute",
      "arguments": [{
        "kind": "AttributeReference", "type": "complex", "name": "attribute",
        "arguments": [{ "name": "entityId", "type": "string", "value": "<filter-attribute-guid>" }]
      }] },
    { "name": "TextValueCondition", "kind": "TextValueCondition",
      "arguments": [
        { "name": "op", "type": "string", "value": "IsEqualTo" },
        { "name": "value", "type": "string", "value": "Medicine" }] }
  ] }
```

---

## Enrichments — Adding Context to Notifications

Enrichments are references to existing `BasicEventAttribute` entities placed in the rule's `ActStep` action binding. Create the attribute entity first, then reference it from the action payload.

> ⚠️ **AttributeTrigger + TeamsMessage guidance**
>
> Dynamic Teams content can appear inline in the message/body, but the inline `AttributeReference` shape is different from the structured `additionalInformation` shape:
>
> - Inline mixed-content parts in `headline` / `optionalMessage` use `{"kind":"AttributeReference","type":"complex","arguments":[...]}` directly inside the field's `values` array.
> - Structured entries in `additionalInformation` use `NameReferencePair` whose `reference` argument is `{"kind":"AttributeReference","type":"complexReference","name":"reference",...}`.
>
> When adding dynamic Teams content to an `AttributeTrigger`, follow the exact shapes below rather than converting everything to `complexReference`.

### Inline mixed content in `optionalMessage`

Working readback shape for inline dynamic text in an `AttributeTrigger` Teams action:

```json
{
  "name": "optionalMessage",
  "type": "array",
  "values": [
    { "name": "string", "type": "string", "value": "The humidity of this package has crossed above or below the allowed range." },
    {
      "kind": "AttributeReference",
      "type": "complex",
      "arguments": [{ "name": "entityId", "type": "string", "value": "<humidity-attr-id>" }]
    },
    { "name": "string", "type": "string", "value": " " }
  ]
}
```

Use the same mixed-content `values` array pattern if you need inline dynamic parts in `headline`.

### Recommended `AttributeTrigger` Teams pattern

Combine inline message content and structured `additionalInformation` like this:

```json
{
  "name": "TeamsBinding",
  "kind": "TeamsMessage",
  "arguments": [
    { "name": "messageLocale", "type": "string", "value": "" },
    { "name": "recipients", "type": "array", "values": [
      { "type": "string", "value": "user@example.com" }
    ]},
    { "name": "headline", "type": "array", "values": [
      { "type": "string", "value": "Building-B critical temperature alert" }
    ]},
    { "name": "optionalMessage", "type": "array", "values": [
      { "name": "string", "type": "string", "value": "The current temperature is " },
      {
        "kind": "AttributeReference",
        "type": "complex",
        "arguments": [{ "name": "entityId", "type": "string", "value": "<temp-attr-id>" }]
      },
      { "name": "string", "type": "string", "value": " and pressure context is included below." }
    ]},
    { "name": "additionalInformation", "type": "array", "values": [
      {
        "kind": "NameReferencePair",
        "type": "complex",
        "arguments": [
          { "name": "name", "type": "string", "value": "Current Temperature" },
          {
            "kind": "AttributeReference",
            "type": "complexReference",
            "name": "reference",
            "arguments": [{ "name": "entityId", "type": "string", "value": "<temp-attr-id>" }]
          }
        ]
      },
      {
        "kind": "NameReferencePair",
        "type": "complex",
        "arguments": [
          { "name": "name", "type": "string", "value": "Current Pressure" },
          {
            "kind": "AttributeReference",
            "type": "complexReference",
            "name": "reference",
            "arguments": [{ "name": "entityId", "type": "string", "value": "<pressure-attr-id>" }]
          }
        ]
      }
    ]}
  ]
}
```

### Structured References in `additionalInformation`

**By attribute entity ID (`AttributeReference`):**
```json
{ "name": "additionalInformation", "type": "array",
  "values": [{
    "kind": "NameReferencePair", "type": "complex",
    "arguments": [
      { "name": "name", "type": "string", "value": "Current Temperature" },
      { "kind": "AttributeReference", "type": "complexReference", "name": "reference",
        "arguments": [{ "name": "entityId", "type": "string", "value": "<attr-id>" }] }
    ] }] }
```

**By raw event field name (`EventFieldReference`):**
```json
{ "kind": "NameReferencePair", "type": "complex",
  "arguments": [
    { "name": "name", "type": "string", "value": "Device ID" },
    { "kind": "EventFieldReference", "type": "complexReference", "name": "reference",
      "arguments": [{ "name": "fieldName", "type": "string", "value": "deviceId" }] }
  ] }
```

> Use `EventFieldReference` only when the rule template resolves raw event fields directly (commonly `EventTrigger`). For `AttributeTrigger`, prefer `AttributeReference` to the existing attribute entity.

### Which Action Fields Accept Enrichments

| Field | Accepts |
|-------|---------|
| `headline` | Array of content parts; use strings or mixed string + inline `AttributeReference` parts (`type: "complex"`) |
| `optionalMessage` | Array of content parts; use strings or mixed string + inline `AttributeReference` parts (`type: "complex"`) |
| `subject` (EmailMessage only) | Static text + `AttributeReference` |
| `additionalInformation` | `NameReferencePair` with `AttributeReference`; `EventFieldReference` only when the rule template exposes raw event fields |

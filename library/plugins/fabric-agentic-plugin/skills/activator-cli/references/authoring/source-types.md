# Activator Entity Types — High-Level Entity Map

---

This reference is the **high-level map of the main public entity types** you assemble in `ReflexEntities.json`.

It covers:

- the shared entity envelope used by all entities
- the top-level `container-v1` grouping entity
- the supported **source entity** types
- the main `timeSeriesView-v1` variants used to model events, objects, attributes, and rules

Standalone action entities such as `fabricItemAction-v1` are part of the overall Activator entity model too, but they are documented separately in [action-types.md](action-types.md).

## High-level entity type map

| Category | Entity type(s) | Purpose |
|----------|----------------|---------|
| Shared envelope | all entities | Common `uniqueIdentifier` + `payload` + `type` wrapper |
| Container | `container-v1` | Top-level grouping entity for hand-authored graphs |
| Sources | `eventstreamSource-v1`, `kqlSource-v1`, `digitalTwinBuilderSource-v1`, `realTimeHubSource-v1`, `powerBiSource-v1` | Connect Activator to upstream data |
| Views | `timeSeriesView-v1` | Model events, objects, attributes, and rules via `payload.definition.type` |
| Actions | `fabricItemAction-v1` | Standalone invokable Fabric item actions used by rules |

## Shared entity envelope

Every entity in `ReflexEntities.json`:

```json
{ "uniqueIdentifier": "<GUID>", "payload": { }, "type": "<entity-type-string>" }
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `uniqueIdentifier` | GUID | yes | Unique ID — other entities reference this |
| `payload` | object | yes | Entity-specific configuration |
| `type` | string | yes | Entity type (see below) |

## Reference Integrity Preflight

Before submitting `updateDefinition`, validate the full `ReflexEntities.json` array, not just the entity you changed. Every `parentContainer.targetUniqueIdentifier`, `parentObject.targetUniqueIdentifier`, `SourceReference.entityId`, `EventReference.entityId`, and `AttributeReference.entityId` must resolve to a top-level `uniqueIdentifier` in that same submitted array. Fabric item action rules must also resolve `fabricJobConnectionDocumentId` to a `fabricItemAction-v1.uniqueIdentifier` in the same array.

If Fabric returns `FailedToResolveEntity` with `DocumentType timeSeriesView not found`, one of those references points at a `timeSeriesView-v1` GUID that is absent from the payload. Re-read the definition, preserve existing entities, fix the missing reference, and retry only after the preflight passes.

---

## Container (`container-v1`)

Top-level grouping entity used by the hand-authored pull-source flows in this skill. KQL, DTB, and Real-time Hub examples should keep using explicit container references. Eventstream sink-created entities are different: in public readback they can appear without an explicit `parentContainer`.

```json
{
  "uniqueIdentifier": "<container-guid>",
  "payload": {
    "name": "Package delivery sample",
    "type": "samples"
  },
  "type": "container-v1"
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | yes | Display name |
| `type` | string | yes | Classification (e.g. `samples`, `kqlQueries`, `rthSubscriptions`, exact `pbiMetrics` for Power BI) |

---

## Source entity types

| Source | Entity Type | Reference | Use Case |
|--------|-------------|-----------|----------|
| Eventstream | `eventstreamSource-v1` | [eventstream-source.md](eventstream-source.md) | Push source created by configuring Activator as an Eventstream destination |
| KQL / Eventhouse | `kqlSource-v1` | [kql-source.md](kql-source.md) | Scheduled queries against a KQL database |
| Digital Twin Builder / Ontology | `digitalTwinBuilderSource-v1` | [dtb-source.md](dtb-source.md) | Scheduled DTB / ontology queries against an existing Fabric item |
| Real-time Hub | `realTimeHubSource-v1` | [real-time-hub-source.md](real-time-hub-source.md) | Fabric workspace event monitoring |
| Power BI | `powerBiSource-v1` | [powerbi-source.md](powerbi-source.md) | Stored query over a report visual / semantic model metric |

---

## View Types (`timeSeriesView-v1`)

Views are not sources themselves, but they sit between sources and rules. They are all entity type `timeSeriesView-v1`, distinguished by `payload.definition.type`.

### Event View (SourceEvent)

Connects to a source and defines what events to process.

> **Event-trigger shortcut:** For pure `EventTrigger` rules, `SourceEvent` is usually the last view you need before the rule. You do **not** need Object, SplitEvent, IdentityPartAttribute, or BasicEventAttribute entities just to fire on raw events.
>
> **Eventstream note:** An Eventstream Activator sink can auto-create a `SourceEvent` view with no explicit `parentContainer` and with `templateVersion: "1.1"`. When extending an Eventstream-backed Activator, preserve the shape already present in the decoded definition instead of forcing the generic container-based example below.

```json
{
  "uniqueIdentifier": "<source-event-guid>",
  "payload": {
    "name": "Sensor events",
    "parentContainer": { "targetUniqueIdentifier": "<container-guid>" },
    "definition": {
      "type": "Event",
      "instance": "<JSON-encoded SourceEvent template>"
    }
  },
  "type": "timeSeriesView-v1"
}
```

**SourceEvent template:**

```json
{
  "templateId": "SourceEvent",
  "templateVersion": "1.2.4",
  "steps": [{
    "name": "SourceEventStep",
    "id": "<guid>",
    "rows": [{
      "name": "SourceSelector",
      "kind": "SourceReference",
      "arguments": [{"name": "entityId", "type": "string", "value": "<source-entity-guid>"}]
    }]
  }]
}
```

### SplitEvent View

SplitEvent is optional — it splits events by object identity when needed. BasicEventAttribute can reference SourceEvent directly. Sits between SourceEvent and Attributes. Maps events to objects using an identity field.

> **Do not use SplitEvent for pure event triggers.** SplitEvent is only for object/attribute modeling when you need to turn raw events into per-object attributes for `AttributeTrigger` rules.

```json
{
  "uniqueIdentifier": "<split-event-guid>",
  "payload": {
    "name": "SplitEvent",
    "parentObject": { "targetUniqueIdentifier": "<object-guid>" },
    "parentContainer": { "targetUniqueIdentifier": "<container-guid>" },
    "definition": {
      "type": "Event",
      "instance": "<JSON-encoded SplitEvent template>"
    }
  },
  "type": "timeSeriesView-v1"
}
```

**SplitEvent template:**

> When SplitEvent is included, SplitEventStep MUST have EventSelector + SplitEventOptions (both required), plus zero or more FieldIdMapping rows.

```json
{
  "templateId": "SplitEvent",
  "templateVersion": "1.2.4",
  "steps": [{
    "name": "SplitEventStep",
    "id": "<guid>",
    "rows": [
      {
        "name": "EventSelector",
        "kind": "Event",
        "arguments": [{
          "kind": "EventReference",
          "type": "complex",
          "arguments": [{"name": "entityId", "type": "string", "value": "<source-event-entity-guid>"}],
          "name": "event"
        }]
      },
      {
        "name": "FieldIdMapping",
        "kind": "FieldIdMapping",
        "arguments": [
          {"name": "fieldName", "type": "string", "value": "<identity-field-name>"},
          {
            "kind": "AttributeReference",
            "type": "complex",
            "arguments": [{"name": "entityId", "type": "string", "value": "<identity-attribute-entity-guid>"}],
            "name": "idPart"
          }
        ]
      },
      {
        "name": "SplitEventOptions",
        "kind": "EventOptions",
        "arguments": [{"name": "isAuthoritative", "type": "boolean", "value": true}]
      }
    ]
  }]
}
```

> **Note:** BasicEventAttribute entities can reference either the **SplitEvent** or **SourceEvent** entity in their EventReference `entityId`. When SplitEvent is not used, reference SourceEvent directly.

### Object View

Groups events by an identity (e.g., a specific package, device, or customer).

```json
{
  "uniqueIdentifier": "<object-guid>",
  "payload": {
    "name": "Package",
    "parentContainer": { "targetUniqueIdentifier": "<container-guid>" },
    "definition": { "type": "Object" }
  },
  "type": "timeSeriesView-v1"
}
```

### Attribute View

Extracts a specific field from events. Attributes belong to an Object via `parentObject`.

```json
{
  "uniqueIdentifier": "<attribute-guid>",
  "payload": {
    "name": "Temperature (°C)",
    "parentObject": { "targetUniqueIdentifier": "<object-guid>" },
    "parentContainer": { "targetUniqueIdentifier": "<container-guid>" },
    "definition": {
      "type": "Attribute",
      "instance": "<JSON-encoded BasicEventAttribute template>"
    }
  },
  "type": "timeSeriesView-v1"
}
```

### IdentityPartAttribute Template

Defines an identity field for object grouping (e.g., SensorId, DeviceId). Uses a single `IdPartStep` with a `TypeAssertion` row.

```json
{
  "templateId": "IdentityPartAttribute",
  "templateVersion": "1.2.4",
  "steps": [{
    "name": "IdPartStep",
    "id": "<guid>",
    "rows": [{
      "name": "TypeAssertion",
      "kind": "TypeAssertion",
      "arguments": [
        { "name": "op", "type": "string", "value": "Text" },
        { "name": "format", "type": "string", "value": "" }
      ]
    }]
  }]
}
```

### BasicEventAttribute Template

Extracts a field value from events. Has TWO steps: `EventSelectStep` (selects the event and field) and `EventComputeStep` (asserts the data type).

```json
{
  "templateId": "BasicEventAttribute",
  "templateVersion": "1.2.4",
  "steps": [
    {
      "name": "EventSelectStep",
      "id": "<guid>",
      "rows": [
        {
          "name": "EventSelector",
          "kind": "Event",
          "arguments": [{
            "kind": "EventReference",
            "type": "complex",
            "arguments": [{ "name": "entityId", "type": "string", "value": "<source-event-entity-guid>" }],
            "name": "event"
          }]
        },
        {
          "name": "EventFieldSelector",
          "kind": "EventField",
          "arguments": [{ "name": "fieldName", "type": "string", "value": "<field-name>" }]
        }
      ]
    },
    {
      "name": "EventComputeStep",
      "id": "<guid>",
      "rows": [{
        "name": "TypeAssertion",
        "kind": "TypeAssertion",
        "arguments": [
          { "name": "op", "type": "string", "value": "Number" },
          { "name": "format", "type": "string", "value": "" }
        ]
      }]
    }
  ]
}
```

> **TypeAssertion `op` values:** Use `"Number"` for numeric fields, `"Text"` for text/string fields.
> **EventReference `entityId`:** Points to the SourceEvent entity (or SplitEvent if used).

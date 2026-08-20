<!-- Mode reference for the `activator-cli` skill. Loaded on demand from `skills/activator-cli/SKILL.md` when the request matches the `authoring` mode. -->

# activator-cli authoring mode — Activator Item & Rule Authoring via CLI

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | Optional background — workspace/item ID resolution detail; skip if `common/` is unavailable |
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401 |
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes) | Use the shared `az login` / token guidance from common docs |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../../common/COMMON-CORE.md#core-control-plane-rest-apis) | List Workspaces, List Items, Item Creation |
| Long-Running Operations (LRO) | [COMMON-CORE.md § Long-Running Operations (LRO)](../../../common/COMMON-CORE.md#long-running-operations-lro) | Create, getDefinition, updateDefinition may return 202 |
| Fabric Item Definitions | [ITEM-DEFINITIONS-CORE.md § Definition Envelope](../../../common/ITEM-DEFINITIONS-CORE.md#definition-envelope) | Base64-encoded parts structure |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource https://api.fabric.microsoft.com`** |
| LRO Pattern | [COMMON-CLI.md § Long-Running Operations (LRO) Pattern](../../../common/COMMON-CLI.md#long-running-operations-lro-pattern) | Poll 202 responses |
| Entity Types, Sources & Views | [source-types.md](authoring/source-types.md) | Entity envelope, source entities, and `timeSeriesView-v1` variants |
| Eventstream Source | [eventstream-source.md](authoring/eventstream-source.md) | Push-source workflow: create Eventstream sink first, then extend the discovered Activator entities |
| KQL Source | [kql-source.md](authoring/kql-source.md) | KQL source schema, time-axis support, design guidance |
| Digital Twin Builder / Ontology Source | [dtb-source.md](authoring/dtb-source.md) | DTB / ontology source schema, JSON-string query payloads, snapshot vs time-axis guidance |
| Real-time Hub Source | [real-time-hub-source.md](authoring/real-time-hub-source.md) | Real-time Hub source schema, workspace event types |
| Power BI Source | [powerbi-source.md](authoring/powerbi-source.md) | `powerBiSource-v1`, stored query payloads, `DatasetMetric`, filters, persistence, and ALM readback limits |
| Rule Conditions | [rule-conditions.md](authoring/rule-conditions.md) | Rule template structure, detection conditions, aggregation, time windows, occurrence options, enrichments |
| Action Types | [action-types.md](authoring/action-types.md) | TeamsMessage, EmailMessage, FabricItemInvocation action schemas |

---

## Tool Stack
| Tool | Purpose |
|---|---|
| **az CLI** | Fabric authentication and REST API token acquisition |
| **curl** | Header-aware Fabric REST calls through the shared `fabric_lro` helper |
| **jq** | JSON filtering and decoded definition inspection |
| **python** | **MUST use for building ReflexEntities.json** — `json.dumps()` handles nested stringification correctly. PowerShell's `ConvertTo-Json` corrupts nested JSON strings. |

> ⚠️ **CRITICAL: Always use Python (not PowerShell) to build the ReflexEntities.json payload and the API request body.**

### Python Patterns

```python
import json, base64, uuid

# Stringify template → JSON string for definition.instance
instance_string = json.dumps(template_dict, separators=(',', ':'))

# Encode entities and write updateDefinition request body
payload_b64 = base64.b64encode(json.dumps(entities).encode('utf-8')).decode('utf-8')
body = json.dumps({"definition": {"parts": [{"path": "ReflexEntities.json", "payload": payload_b64, "payloadType": "InlineBase64"}]}})
with open('update-body.json', 'w', encoding='utf-8') as f:
    f.write(body)
# Then: az rest --method POST --url "...updateDefinition" --resource "https://api.fabric.microsoft.com" --body @update-body.json

# Decode a getDefinition response
response = json.loads(api_output)
for part in response['definition']['parts']:
    if part['path'] == 'ReflexEntities.json':
        entities = json.loads(base64.b64decode(part['payload']).decode('utf-8'))

# Generate GUIDs for uniqueIdentifier and step id fields
entity_id = str(uuid.uuid4())
```

---

## Connection

Use the shared authentication guidance in [COMMON-CLI.md § Authentication Recipes](../../../common/COMMON-CLI.md#authentication-recipes). Resolve workspace and item IDs per [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric). Examples below assume `WS_ID` and `REFLEX_ID` are already resolved.

---

## Item CRUD

Use the shared mechanics in [COMMON-CLI.md § Item CRUD Operations](../../../common/COMMON-CLI.md#item-crud-operations). Activator uses the `reflexes` endpoint rather than the generic `items` endpoint:

| Operation | Endpoint | Method | Scopes | Notes |
|---|---|---|---|---|
| Create | `/v1/workspaces/{workspaceId}/reflexes` | POST | `Reflex.ReadWrite.All` or `Item.ReadWrite.All` | May return 202 LRO — use `fabric_lro` from COMMON-CLI |
| Update metadata | `/v1/workspaces/{workspaceId}/reflexes/{reflexId}` | PATCH | `Reflex.ReadWrite.All` or `Item.ReadWrite.All` | Follow COMMON-CLI metadata update pattern |
| Delete | `/v1/workspaces/{workspaceId}/reflexes/{reflexId}` | DELETE | `Reflex.ReadWrite.All` or `Item.ReadWrite.All` | Add `?hardDelete=true` for permanent deletion |
| `getDefinition` | `/v1/workspaces/{workspaceId}/reflexes/{reflexId}/getDefinition` | POST | `Reflex.ReadWrite.All` or `Item.ReadWrite.All` | Empty body required; may return 202 LRO — use `fabric_lro` |
| `updateDefinition` | `/v1/workspaces/{workspaceId}/reflexes/{reflexId}/updateDefinition` | POST | `Reflex.ReadWrite.All` or `Item.ReadWrite.All` | Use Python to build `update-body.json`, then follow COMMON-CLI updateDefinition pattern |

---

## Rule Management via Definitions

Rules are managed through `getDefinition` and `updateDefinition`. The payload is `ReflexEntities.json`, a Base64-encoded JSON array of entity objects. Workflow: **Get → Decode → Modify → Re-encode → Update**.

### Get Definition

> `getDefinition` is a **POST** (not GET), requires **ReadWrite** scopes, and may return **202 LRO**. Use the `fabric_lro` helper from [COMMON-CLI.md § Long-Running Operations (LRO) Pattern](../../../common/COMMON-CLI.md#long-running-operations-lro-pattern) so 202 responses can be polled via the `Location` header before decoding.

```bash
DEFINITION=$(fabric_lro POST \
  "https://api.fabric.microsoft.com/v1/workspaces/${WS_ID}/reflexes/${REFLEX_ID}/getDefinition" \
  '{}')

echo "$DEFINITION" \
  | jq '.definition.parts[] | select(.path=="ReflexEntities.json") | .payload' -r \
  | base64 -d | jq .
```

### Update Definition

> **MUST use Python** to build `update-body.json` (see [Python Patterns](#python-patterns)), then upload it using the COMMON-CLI updateDefinition pattern against `/v1/workspaces/{workspaceId}/reflexes/{reflexId}/updateDefinition`.

### ReflexEntities.json — Assembly Procedure

Build a JSON array of entities in order. Each needs a fresh GUID for `uniqueIdentifier`. For the hand-authored pull-source flows in this skill, use templateVersion `1.2.4`. For Eventstream sink-created flows, preserve the template version already present in the decoded Activator definition; those readbacks can use `1.1`.

**Step 1 — Container** (exactly 1):
- Type: `container-v1`. Use the container payload type that matches the source graph: `kqlQueries` for KQL sources, `rthSubscriptions` for Real-Time Hub workspace subscriptions, exact case-sensitive `pbiMetrics` for Power BI sources, or the service-created type already present in readback for Eventstream flows.
- All other entities reference this via `parentContainer.targetUniqueIdentifier`

**Step 2 — Data Source** (exactly 1, pick the right type):
- See [eventstream-source.md](authoring/eventstream-source.md), [kql-source.md](authoring/kql-source.md), [dtb-source.md](authoring/dtb-source.md), [real-time-hub-source.md](authoring/real-time-hub-source.md), or [powerbi-source.md](authoring/powerbi-source.md) for the supported source workflows
- For hand-authored pull sources, set `parentContainer.targetUniqueIdentifier` → Container GUID
- For `eventstreamSource-v1`: do **not** start by hand-authoring the source. Create or update the Eventstream with an `Activator` destination first, then read the Activator definition and continue from the auto-created `eventstreamSource-v1` + SourceEvent entities. In public readback, those sink-created entities can appear without explicit `parentContainer`.
- For `kqlSource-v1`: the KQL query should return ALL data (do NOT pre-filter conditions — let the rule handle that). Must include `eventhouseItem`, `metadata`, and `queryParameters`. For Fabric Eventhouse/KQL DB sources, use `eventhouseItem: { itemId, workspaceId, itemType: "KustoDatabase" }`. For external ADX/Kusto sources, use `eventhouseItem: { clusterHostName, databaseName }`. **Before creating the Activator, run the KQL directly against the target source first and confirm the returned columns, timestamp field, and row shape are correct.** **Use `eventTimeSettings` plus `DURATION_START`/`DURATION_END` queryParameters whenever the query results have a reasonable timestamp column, and declare those parameters in the KQL with `declare query_parameters(startTime:datetime, endTime:datetime);`.** Only use snapshot mode (`queryParameters: []`, no `eventTimeSettings`, no time filtering) when the underlying data has no reasonable timestamp column and each row represents current state. See [kql-source.md](authoring/kql-source.md).
- For `digitalTwinBuilderSource-v1`: use a DTB / Ontology `connection` item ref `{ itemId, workspaceId, itemType }`, where `itemType` is either `DigitalTwinBuilder` or `Ontology`. `query.queryString` must be a JSON-string payload, not KQL. **Before creating the Activator, run the DTB / Ontology query directly first and confirm the returned columns, key fields, and timestamp field are correct.** Prefer `eventTimeSettings` plus `DURATION_START`/`DURATION_END` query parameters when the returned rows include a reasonable timestamp field; unlike KQL, those duration parameters are applied as DTB endpoint URL query params rather than referenced inside the query body. See [dtb-source.md](authoring/dtb-source.md).
- For `powerBiSource-v1`: build the source deterministically from a scoped report/page/visual plus semantic model metadata. Its parent container must use exact `payload.type: "pbiMetrics"`. Store the source query payload as JSON text in `query.queryString` and a matching `DatasetMetric` in `metricDefinition`. Persist with `updateDefinition`, require explicit HTTP `200` (or terminal LRO success), and stop on any import error. See [powerbi-source.md](authoring/powerbi-source.md).

**Step 3 — SourceEvent view** (exactly 1):
- Type: `timeSeriesView-v1`, definition.type: `"Event"`, instance: `SourceEvent` template referencing Source by `entityId`
- For hand-authored pull-source flows, set `parentContainer` → Container GUID
- For Eventstream sink-created flows, reuse the auto-created SourceEvent from readback instead of creating a second one

**Step 4 — Choose the entity graph based on trigger type**

- **For `AttributeTrigger` rules** (thresholds, ranges, text matches, boolean checks, aggregations):
  - Create an **Object** view
  - Optionally create **SplitEvent** if events must be mapped to object instances
  - Create **IdentityPartAttribute** and any required **BasicEventAttribute** entities
  - The rule then references those value attributes in `ScalarSelectStep`

- **For `EventTrigger` rules** (fire on every event, heartbeat, event field state/change):
  - Use the minimal graph: **Container → Source → SourceEvent → Rule** (+ optional `fabricItemAction-v1`)
  - **Do NOT create Object, SplitEvent, IdentityPartAttribute, or BasicEventAttribute entities** unless the scenario truly needs attribute-based modeling
  - `FieldsDefaultsStep` must contain an `EventSelector` row whose nested `EventReference.entityId` points to the SourceEvent entity. A top-level `EventReference` row is invalid.
  - EventTrigger reads raw event fields directly in `FieldsDefaultsStep` / `EventDetectStep`

**Step 5 — Rule** (1 per alert):
- Type: `timeSeriesView-v1`, definition.type: `"Rule"`
- **Always add `"description": "Created by: skills-for-fabric"`** for user clarity
- Instance: rule template (see [rule-conditions.md](authoring/rule-conditions.md))
  - `AttributeTrigger` (v1.2.4): ScalarSelectStep → ScalarDetectStep → (DimensionalFilterStep)* → ActStep
  - `EventTrigger` (v1.2.4): FieldsDefaultsStep → (EventDetectStep)+ → (DimensionalFilterStep)* → ActStep
- `instance` **MUST be a JSON string** (use `json.dumps()`)
- Every template step inside `instance.steps[]` needs an `id` GUID. Missing step IDs can produce invalid expression graphs because backend translators use the step ID as the output node ID.
- For `AttributeTrigger`, set `parentObject` → Object and `parentContainer` → Container
- For `EventTrigger`, set `parentContainer` → Container and omit `parentObject` unless the design explicitly requires it
- Default to `settings: { "shouldRun": true, "shouldApplyRuleOnUpdate": false }` so newly created rules start in the **started / running** state
- Only set `shouldRun: false` when the user explicitly asks for a stopped rule or when a specific safe verification / eval workflow requires a disabled rule to avoid side effects
- For `TeamsMessage` actions with dynamic content, preserve the field-specific reference shapes from working readback: inline mixed-content fragments in `headline` / `optionalMessage` use `AttributeReference` with `type: "complex"`, while structured `additionalInformation` entries use `NameReferencePair` + `AttributeReference` / `EventFieldReference` with `type: "complexReference"` and `name: "reference"`

Example rule entity:
```python
{
    "uniqueIdentifier": "<rule-guid>",
    "payload": {
        "name": "My Rule Name",
        "description": "Created by: skills-for-fabric",  # Required for user clarity
        "parentObject": {"targetUniqueIdentifier": "<object-guid>"},
        "parentContainer": {"targetUniqueIdentifier": "<container-guid>"},
        "definition": {
            "type": "Rule",
            "instance": stringify_instance(rule_template),
            "settings": {"shouldRun": True, "shouldApplyRuleOnUpdate": False}
        }
    },
    "type": "timeSeriesView-v1"
}
```

**Step 6 — Fabric Item Action** (only for `FabricItemInvocation`):
- Type: `fabricItemAction-v1` — use this standalone action entity whenever the rule invokes a Fabric item such as a Pipeline, Notebook, Spark job definition, Dataflow, or UDF / Function Set
- In the rule's `FabricItemBinding`, set `fabricJobConnectionDocumentId` to the standalone `fabricItemAction-v1.uniqueIdentifier`
- See [action-types.md](authoring/action-types.md) for per-target schemas and UDF-specific gotchas (`itemType` vs readback `FunctionSet`, `subitemId`, canonical `parameterType` mapping, dynamic parameter shape)

### Reference Integrity Preflight

Before every `updateDefinition`, validate the exact entity array you will send:

1. Build the set of every top-level `uniqueIdentifier` in `ReflexEntities.json`.
2. Confirm every `parentContainer.targetUniqueIdentifier`, `parentObject.targetUniqueIdentifier`, `SourceReference.entityId`, `EventReference.entityId`, `AttributeReference.entityId`, and `fabricJobConnectionDocumentId` resolves to an entity in that same array (or to an unchanged entity from the latest decoded readback that is included in the re-encoded array).
3. Confirm each reference points to the expected entity type: containers to `container-v1`, source/event/attribute/rule/object references to `timeSeriesView-v1` when the template expects a view, source references to the source entity, and Fabric item action bindings to `fabricItemAction-v1`.
4. If any reference is missing, rebuild the graph from the latest `getDefinition` output and do not call `updateDefinition`.

`FailedToResolveEntity` with `DocumentType timeSeriesView not found` means a rule, attribute, split event, or event reference points at a `timeSeriesView-v1` GUID that is not present in the submitted definition. Treat that as an entity-wiring bug to fix before retrying, not as a transient backend failure.

### Entity Wiring Summary

```text
Container ← everything references this via parentContainer
    │
    ├── Source ← parentContainer → Container
    │
    ├── SourceEvent ← parentContainer → Container
    │        │         instance references Source by entityId
    │        │
    │        ├── EventTrigger Rule ← parentContainer → Container
    │        │       minimal event-only path; reads raw event fields directly
    │        │
    │        └── Object ← parentContainer → Container
    │              │
    │              ├── (SplitEvent) ← OPTIONAL, parentObject → Object, parentContainer → Container
    │              │       instance references SourceEvent by entityId
    │              │       maps events to objects via FieldIdMapping
    │              │
    │              ├── Identity Attr ← parentObject → Object, parentContainer → Container
    │              │
    │              ├── Value Attr(s) ← parentObject → Object, parentContainer → Container
    │              │       instance references SourceEvent (or SplitEvent if used) by entityId
    │              │
    │              └── AttributeTrigger Rule ← parentObject → Object, parentContainer → Container
    │                      instance references Value Attr by entityId in ScalarSelectStep
    │
    └── (FabricItemAction) ← parentContainer → Container (for any FabricItemInvocation action: Pipeline, Notebook, Spark job, Dataflow, or UDF / Function Set)
```

### Critical: `definition.instance` is a JSON String

`instance` inside `timeSeriesView-v1` entity's `definition` is a **JSON-encoded string**, not a nested object. Always wrap rule templates in the full entity envelope.

**❌ WRONG — raw template object (will fail):**

```json
{
  "templateId": "AttributeTrigger",
  "templateVersion": "1.2.4",
  "steps": [...]
}
```

**✅ CORRECT — entity envelope with stringified instance:**

```json
{
  "uniqueIdentifier": "<new-guid>",
  "payload": {
    "name": "My Rule Name",
    "parentObject": { "targetUniqueIdentifier": "<object-guid>" },
      "parentContainer": { "targetUniqueIdentifier": "<container-guid>" },
      "definition": {
        "type": "Rule",
        "instance": "{\"templateId\":\"AttributeTrigger\",\"templateVersion\":\"1.2.4\",\"steps\":[...]}",
        "settings": { "shouldRun": true, "shouldApplyRuleOnUpdate": false }
      }
    },
    "type": "timeSeriesView-v1"
}
```

Use `json.dumps()` to stringify. **Do NOT use PowerShell's `ConvertTo-Json`.**

### Two Rule Template Types

| Template | When to Use | Steps |
|----------|-------------|-------|
| `AttributeTrigger` | Monitor attribute value (numeric, text, boolean) | ScalarSelectStep → ScalarDetectStep → (DimensionalFilterStep)* → ActStep |
| `EventTrigger` | Fire on event occurrence (state, change, heartbeat) | FieldsDefaultsStep → (EventDetectStep)+ → (DimensionalFilterStep)* → ActStep |

> **EventTrigger** does NOT have ScalarSelectStep/ScalarDetectStep. Use when acting on events directly. Supports state, change, and heartbeat detection via EventDetectStep.

---

## Source Validation Gate

Before authoring **any** rule that references a signal (a measurement, field, or event property), confirm the source is real. A requested source only counts as **real** after all three checks pass:

1. **Resolve** the source in the **requested** workspace only -- do not search or substitute another workspace.
2. **Validate** that the requested signal column/field exists on that source (KQL table/column, Eventstream field, Real-Time Hub event property, or DTB / Ontology property).
3. **Observe** at least one representative row/event/sample carrying that signal -- run the KQL / DTB query or inspect the stream and confirm it actually returns data.

Treat **schema-only**, **zero-row**, **non-emitting**, or **stale** evidence as **missing source data**, not a real source. When the source is missing, **stop and ask** which source and fields provide the signal (plus any missing threshold, recipient, or action details). Do **not** create a Reflex or call `updateDefinition` on any existing Activator / Eventstream to force-fit the request, and state plainly that **no Activator / Reflex / Eventstream was created or updated**. The only exception is when the user explicitly instructs you to author against a future / not-yet-emitting source.

---

## Must / Prefer / Avoid

### MUST DO

- **Confirm a real source before authoring** -- follow the [Source Validation Gate](#source-validation-gate): resolve the source in the requested workspace, validate the requested signal column/field, and observe at least one representative row/event/sample before authoring. Schema-only, zero-row, non-emitting, or stale evidence is **missing source data** -- **stop and ask** which source and fields provide it (plus any missing threshold, recipient, or action details), and state that no Activator/Reflex/Eventstream was created or updated, instead of authoring the rule. If the user explicitly instructs authoring against a future / not-yet-emitting source, state that assumption and continue without claiming the source was observed.
- **Always use `--resource https://api.fabric.microsoft.com`** with `az rest` — without it, token audience is wrong
- **Always send `--body '{}'`** for `getDefinition` — it is a POST and omitting the body can cause 411 errors
- **Always Base64-encode** `ReflexEntities.json` payload when calling `updateDefinition`
- **Always JSON.stringify** the `definition.instance` field in `timeSeriesView-v1` entities — it must be a string, not a nested object. **Always wrap rule templates in the full entity envelope** (see the ❌/✅ example above) — never output a raw template object without the entity wrapper
- **Always use the correct template type** — `AttributeTrigger` for value-based conditions (has ScalarSelectStep + ScalarDetectStep), `EventTrigger` for event-based firing (has FieldsDefaultsStep + EventDetectStep, no ScalarDetectStep)
- **Always use the canonical EventTrigger selector** — `FieldsDefaultsStep.rows` contains `EventSelector` (`kind: Event`) with a nested complex `EventReference`; never put `EventReference` directly in `rows`
- **Always use new GUIDs** for `uniqueIdentifier` when adding entities — duplicate GUIDs cause corruption
- **Always update all cross-references** when changing a `uniqueIdentifier` — other entities reference it via `targetUniqueIdentifier`
- **Always run the Reference Integrity Preflight before `updateDefinition`** -- every `targetUniqueIdentifier`, `entityId`, and `fabricJobConnectionDocumentId` in the payload must resolve to an entity included in the submitted `ReflexEntities.json`
- **Handle LRO responses** — `create`, `getDefinition`, and `updateDefinition` may return 202; poll the `Location` header

### PREFER

- **Read-modify-write** over full replacement — get the current definition, modify the entity array, and update
- **Soft delete** over hard delete unless permanent removal is intended
- **Discover IDs dynamically** via workspace listing + JMESPath rather than hardcoding GUIDs
- **Transition-based alert conditions** over steady-state conditions for most alerts — prefer detectors such as `NumberBecomes`, `NumberEntersOrLeavesRange`, `LogicalBecomes`, or explicit change conditions even when the user says casual state-like wording such as "is greater than", "is below", or "is outside the range". Treat ordinary alert wording as "notify me when it crosses into that state" to avoid repeated notifications while the condition remains true
- **Steady-state conditions** such as `IsGreaterThan`, `IsLessThan`, or `IsOutsideRange` only when the user explicitly asks for repeated firing while the value stays in the triggered state, for example "notify me every time it is greater than 30", "fire on every evaluation while it is above 30", or when a downstream occurrence / windowing pattern truly depends on that semantics

### AVOID

- **Hardcoded workspace or item IDs** — always resolve dynamically
- **Forgetting the `.platform` part** — only include it with `updateDefinition` when using `?updateMetadata=true`
- **SELECT * without filtering** on list endpoints — use pagination for large workspaces
- **Modifying definitions of items with encrypted sensitivity labels** — `getDefinition` is blocked
- **Pre-filtering conditions in the KQL query** — return all data from KQL and let the Activator rule steps handle thresholds, text conditions, and dimensional filters. KQL is the data source, not the rule engine
- **Inline JSON in PowerShell `az rest --body`** — PowerShell mangles quotes and special characters. Always write JSON to a temp file with `[System.IO.File]::WriteAllText($path, $json, [System.Text.UTF8Encoding]::new($false))` and pass `--body @$path`
- **Reusing display names after deletion** — soft-deleted items hold their name for several minutes. Use a unique name or hard-delete first
- **Force-fitting a request onto unrelated existing items** -- when no source clears the [Source Validation Gate](#source-validation-gate) (missing, schema-only, zero-row, non-emitting, or stale), do NOT create a Reflex or call `updateDefinition` on an unrelated existing Activator / Eventstream to satisfy it; ask for the missing source first
- **Read-only listing or inspection** -- use [consumption mode](consumption.md) for prompts like "show me all Activators", "list Activators", "show the rules", "inspect this alert", or "decode the definition". This authoring skill should only run when the user asks to create, update, delete, configure, or change something.

---

## Examples

Follow the [Assembly Procedure](#reflexentitiesjson--assembly-procedure) to build definitions. See reference docs for complete entity schemas: [source-types.md](authoring/source-types.md), [rule-conditions.md](authoring/rule-conditions.md), [action-types.md](authoring/action-types.md).

---

## Agent Integration Notes

- This skill uses the Fabric Items API (`/reflexes`) for CRUD and the Definition API for rule management
- No additional data-plane protocols are needed — all operations use `az rest` with the Fabric API audience
- For **reading** Activator items and rules without modifying them, use the [consumption mode](consumption.md) skill instead

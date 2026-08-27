# Activator Action Types — Rule Action Bindings

> Complete reference for all supported action types that rules can trigger when conditions are met.

---

## Where Actions Live

Actions appear in two places in `ReflexEntities.json`:

1. **Inside a Rule's ActStep** — the action binding (TeamsMessage, EmailMessage) is defined inline as a row in the ActStep
2. **As a standalone entity** — `fabricItemAction-v1` entities define Fabric items (Pipelines, Notebooks, Spark jobs, Dataflows, Functions/UDFs) that rules can invoke

---

## Action Types Summary

| Action | Kind (in ActStep) | Entity Type | Description |
|--------|-------------------|-------------|-------------|
| Teams Message | `TeamsMessage` | (inline in rule) | Send a Teams notification |
| Email | `EmailMessage` | (inline in rule) | Send an email |
| Fabric Item | `FabricItemInvocation` | `fabricItemAction-v1` | Execute a Pipeline, Notebook, Spark job, Dataflow, or Function/UDF |

> **Note:** There is no dedicated "Power Automate flow" or "Custom endpoint/webhook" action type in the public definition API.

---

## TeamsMessage

Sends a notification to Microsoft Teams. Recipients are specified by email address.

```json
{
  "name": "TeamsBinding",
  "kind": "TeamsMessage",
  "arguments": [
    { "name": "messageLocale", "type": "string", "value": "" },
    { "name": "recipients", "type": "array", "values": [
        { "type": "string", "value": "user@example.com" },
        { "type": "string", "value": "team-lead@example.com" }
    ]},
    { "name": "headline", "type": "array", "values": [
        { "type": "string", "value": "Alert headline text" }
    ]},
    { "name": "optionalMessage", "type": "array", "values": [
        { "type": "string", "value": "Detailed message body with context" }
    ]},
    { "name": "additionalInformation", "type": "array", "values": [] }
  ]
}
```

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `messageLocale` | string | no | Language/locale (empty string for default) |
| `recipients` | array of strings | yes | Email addresses of recipients |
| `headline` | array of content parts | yes | Message title shown in Teams notification |
| `optionalMessage` | array of content parts | no | Detailed message body |
| `additionalInformation` | array | no | Extra context data |

### TeamsMessage Design Guidance

- Multiple recipients receive independent notifications
- The `headline` should be concise and actionable — it's the first thing users see
- Use `optionalMessage` for context that helps the recipient understand and act on the alert
- Inline dynamic content can be mixed into `headline` / `optionalMessage` by embedding `AttributeReference` parts directly in the field's `values` array
- For inline message parts, use `{"kind":"AttributeReference","type":"complex","arguments":[...]}` or `{"kind":"EventFieldReference","type":"complex","arguments":[...]}` — do **not** convert those inline parts to `complexReference`
- For attribute-trigger rules, reference attributes by entity ID; for event-trigger rules, reference event fields by field name
- The `additionalInformation` field can include structured dynamic data via `NameReferencePair`
- Structured `additionalInformation` uses nested `AttributeReference` / `EventFieldReference` entries with `type: "complexReference"` and `name: "reference"`

Working inline mixed-content example:

```json
{
  "name": "optionalMessage",
  "type": "array",
  "values": [
    { "name": "string", "type": "string", "value": "The humidity of this package has crossed above or below the allowed range." },
    {
      "kind": "AttributeReference",
      "type": "complex",
      "arguments": [{ "name": "entityId", "type": "string", "value": "<attr-id>" }]
    },
    { "name": "string", "type": "string", "value": " " }
  ]
}
```

Working event field message part:

```json
{
  "kind": "EventFieldReference",
  "type": "complex",
  "arguments": [
    { "name": "fieldName", "type": "string", "value": "Status" }
  ]
}
```

Working `additionalInformation` example:

```json
{
  "kind": "NameReferencePair",
  "type": "complex",
  "arguments": [
    { "name": "name", "type": "string", "value": "Temperature" },
    {
      "name": "reference",
      "kind": "AttributeReference",
      "type": "complexReference",
      "arguments": [
        { "name": "entityId", "type": "string", "value": "<temperature-attribute-guid>" }
      ]
    }
  ]
}
```

---

## EmailMessage

Sends an email alert with configurable recipients (To, CC, BCC), subject, and body.

> ⚠️ **Authoring guidance**
>
> In current backend behavior, authoring should use **array-shaped content fields** for `subject`, `headline`, `optionalMessage`, and `additionalInformation`, matching working readback and successful eval output.

```json
{
  "name": "EmailBinding",
  "kind": "EmailMessage",
  "arguments": [
    { "name": "messageLocale", "type": "string", "value": "en-us" },
    { "name": "sentTo", "type": "array", "values": [
        { "type": "string", "value": "primary@example.com" }
    ]},
    { "name": "copyTo", "type": "array", "values": [
        { "type": "string", "value": "manager@example.com" }
    ]},
    { "name": "bCCTo", "type": "array", "values": [] },
    { "name": "subject", "type": "array", "values": [
        { "type": "string", "value": "Alert: Sales threshold exceeded" }
    ]},
    { "name": "headline", "type": "array", "values": [
        { "type": "string", "value": "Main alert content displayed prominently" }
    ]},
    { "name": "optionalMessage", "type": "array", "values": [
        { "type": "string", "value": "Additional context and recommended actions" }
    ]},
    { "name": "additionalInformation", "type": "array", "values": [] }
  ]
}
```

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `messageLocale` | string | no | e.g. `en-us` |
| `sentTo` | array of strings | yes | Primary recipients (To) |
| `copyTo` | array of strings | no | CC recipients |
| `bCCTo` | array of strings | no | BCC recipients |
| `subject` | array of content parts | yes | Email subject line |
| `headline` | array of content parts | yes | Main content displayed prominently |
| `optionalMessage` | array of content parts | no | Additional body text |
| `additionalInformation` | array | no | Extra context |

### EmailMessage vs TeamsMessage Differences

| Field | TeamsMessage | EmailMessage |
|-------|-------------|-------------|
| Recipients | `recipients` (array) | `sentTo` + `copyTo` + `bCCTo` |
| Subject | N/A | `subject` (array) |
| Headline | array of content parts | array of content parts |
| Message | array of content parts | array of content parts |

---

## Fabric Item Action (`fabricItemAction-v1`)

A **standalone entity** that defines a Fabric item (Pipeline, Notebook, Spark job, Dataflow, or Function/UDF) to execute when a rule fires. Rules reference this entity by `uniqueIdentifier`.

```json
{
  "uniqueIdentifier": "<fabric-item-action-guid>",
  "payload": {
    "name": "Run alert pipeline",
    "fabricItem": {
      "itemId": "<pipeline-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "Pipeline"
    },
    "jobType": "Pipeline",
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "fabricItemAction-v1"
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | yes | Display name |
| `fabricItem.itemId` | GUID | yes | Fabric item ID |
| `fabricItem.workspaceId` | GUID | yes | Workspace containing the item |
| `fabricItem.itemType` | string | yes | `Pipeline`, `SynapseNotebook`, `SparkJobDefinition`, `DataflowFabric`, `UserDataFunctions`, or `FunctionSet` |
| `jobType` | string | yes | Job type (for example `Pipeline`, `RunNotebook`, `sparkjob`, or `Execute`) |
| `parentContainer.targetUniqueIdentifier` | GUID | yes | Container ref |

### Supported Fabric Item Types

| itemType | jobType | Description |
|----------|---------|-------------|
| `Pipeline` | `Pipeline` | Run a Data Factory pipeline |
| `SynapseNotebook` | `RunNotebook` | Run a Fabric notebook |
| `SparkJobDefinition` | `sparkjob` | Run a Spark job definition |
| `DataflowFabric` | `Execute` | Run a Dataflow |
| `UserDataFunctions` | `Execute` | Run a user data function |
| `FunctionSet` | `Execute` | Alias of `UserDataFunctions`; run a function from a function set |

> ⚠️ **Notebooks use `itemType: "SynapseNotebook"` with `jobType: "RunNotebook"`** (not `"Notebook"` or `"SparkJob"`).
>
> ⚠️ **`FunctionSet` is handled as an alias of `UserDataFunctions`** in backend execution.
>
> ⚠️ **The public Fabric items API exposes the underlying item type as `UserDataFunction` (singular), but Activator action payloads still use `itemType: "UserDataFunctions"` (plural).**
>
> ⚠️ **Readback nuance for UDF / function-set actions:** on write/import, authoring commonly uses `UserDataFunctions`. On a later `getDefinition` readback, the standalone `fabricItemAction-v1` entity may normalize `payload.fabricItem.itemType` to `FunctionSet`, while the rule's embedded `FabricItemBinding.arguments.itemType` still remains `UserDataFunctions`.
>
> ⚠️ **UDF prerequisite:** before wiring a UDF action, verify the target `UserDataFunction` item exposes the function you plan to call. If the item has no registered functions, fix the UDF definition first; do not treat the Activator action as valid.

### Target-Specific `fabricItemAction-v1` Examples

#### Notebook

```json
{
  "uniqueIdentifier": "<notebook-action-guid>",
  "payload": {
    "name": "Run alert notebook",
    "fabricItem": {
      "itemId": "<notebook-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "SynapseNotebook"
    },
    "jobType": "RunNotebook",
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "fabricItemAction-v1"
}
```

#### Spark Job Definition

```json
{
  "uniqueIdentifier": "<spark-job-action-guid>",
  "payload": {
    "name": "Run alert spark job",
    "fabricItem": {
      "itemId": "<spark-job-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "SparkJobDefinition"
    },
    "jobType": "sparkjob",
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "fabricItemAction-v1"
}
```

#### Dataflow

```json
{
  "uniqueIdentifier": "<dataflow-action-guid>",
  "payload": {
    "name": "Run alert dataflow",
    "fabricItem": {
      "itemId": "<dataflow-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "DataflowFabric"
    },
    "jobType": "Execute",
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "fabricItemAction-v1"
}
```

#### User Data Function / Function Set

```json
{
  "uniqueIdentifier": "<udf-action-guid>",
  "payload": {
    "name": "Run alert function",
    "fabricItem": {
      "itemId": "<udf-item-guid>",
      "workspaceId": "<workspace-guid>",
      "itemType": "UserDataFunctions"
    },
    "jobType": "Execute",
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "fabricItemAction-v1"
}
```

### How Rules Reference Fabric Item Actions

The ActStep uses a `FabricItemBinding` row with kind `FabricItemInvocation`. This is the same structure in both `AttributeTrigger` and `EventTrigger` — the ActStep grammar is identical across all trigger types.

**All 7 base arguments are required** (including empty arrays). Some item types add more arguments; for example UDF / Function Set bindings add `subitemId`.

Use a template version that supports every argument in the binding. Parameters require at least `1.2`, and flexible item types / UDF `subitemId` require at least `1.2.3`; the default rule template version `1.2.4` covers these known requirements.

Set `fabricJobConnectionDocumentId` to the `uniqueIdentifier` of the standalone `fabricItemAction-v1` entity. The backend treats that value as the reference from the rule binding row to the action document; do not replace it with the Fabric item ID.

For Spark Job Definition ActStep bindings, use `itemType: "SparkJobDefinition"`. The exact `jobType` value is backend-passed-through; prefer a known-good payload/readback for the target environment instead of guessing.

```json
{
  "name": "FabricItemBinding",
  "kind": "FabricItemInvocation",
  "arguments": [
    { "name": "workspaceId", "type": "string", "value": "<workspace-guid>" },
    { "name": "itemId", "type": "string", "value": "<pipeline-or-notebook-guid>" },
    { "name": "itemType", "type": "string", "value": "Pipeline" },
    { "name": "jobType", "type": "string", "value": "Pipeline" },
    { "name": "fabricJobConnectionDocumentId", "type": "string", "value": "<fabric-item-action-guid>" },
    { "name": "additionalInformation", "type": "array", "values": [] },
    { "name": "parameters", "type": "array", "values": [] }
  ]
}
```

> ⚠️ **Common mistakes that cause `RowCountMismatch`:**
> 1. **Missing arguments** — all 7 base arguments are required, including `additionalInformation` and `parameters` as empty arrays
> 2. **Wrong row name** — must be `"FabricItemBinding"` (not `"FabricItemInvocation"` — that's the `kind`)
> 3. **Multiple rows in ActStep** — ActStep allows exactly ONE action binding row

For `UserDataFunctions` and `FunctionSet`, include a `subitemId` string argument in the binding to name the specific function to execute. Match the binding's `parameterName` values to the names exposed by the Fabric function metadata, and use Activator's **canonical `parameterType` values** — `String`, `Number`, or `Boolean` — for each parameter. The Fabric function metadata may surface Python type names such as `str`, `float`, or `int`; do **not** pass those through as `parameterType` on the binding — the rule validator rejects them. Map them to the canonical Activator types instead:

| Fabric function metadata `dataType` | Activator binding `parameterType` |
|----|----|
| `str` | `String` |
| `int`, `float` | `Number` |
| `bool` | `Boolean` |

> **Recommended authoring pattern:** keep the binding `itemType` as `UserDataFunctions` even if a later readback shows the standalone action entity as `FunctionSet`.
>
> **Linkage prerequisite:** `subitemId` must match a real function exposed by the target User Data Function item. If the item exists but exposes no functions, fix the UDF definition first; the Activator linkage is not valid until a function is registered.

For dynamic parameter values inside `FabricItemParameter.parameterValue`, use reference-valued parts with `type: "complexReference"`. This differs from inline Teams `headline` / `optionalMessage` fragments, where `type: "complex"` is correct.

```json
{
  "name": "FabricItemBinding",
  "kind": "FabricItemInvocation",
  "arguments": [
    { "name": "workspaceId", "type": "string", "value": "<workspace-guid>" },
    { "name": "itemId", "type": "string", "value": "<function-set-guid>" },
    { "name": "itemType", "type": "string", "value": "UserDataFunctions" },
    { "name": "jobType", "type": "string", "value": "Execute" },
    { "name": "fabricJobConnectionDocumentId", "type": "string", "value": "<udf-action-guid>" },
    { "name": "additionalInformation", "type": "array", "values": [] },
    { "name": "parameters", "type": "array", "values": [
        {
          "kind": "FabricItemParameter",
          "type": "complex",
          "arguments": [
            { "name": "parameterName", "type": "string", "value": "name" },
            { "name": "parameterType", "type": "string", "value": "String" },
            { "name": "parameterValue", "type": "complexArray", "values": [
                { "type": "string", "value": "world" }
            ]}
          ]
        },
        {
          "kind": "FabricItemParameter",
          "type": "complex",
          "arguments": [
            { "name": "parameterName", "type": "string", "value": "temperature" },
            { "name": "parameterType", "type": "string", "value": "Number" },
            { "name": "parameterValue", "type": "complexArray", "values": [
                {
                  "kind": "AttributeReference",
                  "type": "complexReference",
                  "arguments": [
                    { "name": "entityId", "type": "string", "value": "<temperature-attribute-guid>" }
                  ]
                }
            ]}
          ]
        }
    ]},
    { "name": "subitemId", "type": "string", "value": "<published-function-name>" }
  ]
}
```

### Additional gotchas for dynamic `FabricItemParameter` values

The worked UDF binding example above covers the canonical static + dynamic pattern. A few additional gotchas are worth calling out explicitly because they each produced a 400 with a misleading error pointed at the leaf rule rather than the offending field:

#### Envelope contrast — same `AttributeReference`, two shapes

`AttributeReference` appears in several places inside the rule graph, and the envelope differs by location. Reuse the wrong shape and you get a 400. The two shapes you will see in the same definition:

| Where it appears | Envelope |
|----|----|
| Inside `ScalarSelectStep` / `DimensionalFilterStep` rows | `{ "kind": "AttributeReference", "type": "complex", "name": "attribute", "arguments": [...] }` |
| Inside `FabricItemParameter.parameterValue.values` | `{ "kind": "AttributeReference", "type": "complexReference", "arguments": [...] }` (no `name` field) |

For the structured `additionalInformation` form used by Teams / Email actions, see the [TeamsMessage guidance](#teamsmessage-design-guidance) further up — that one uses `type: "complexReference"` with `name: "reference"`, which is yet a different envelope.

#### `AttributeReference.entityId` must point at a `BasicEventAttribute`

Inside `FabricItemParameter.parameterValue`, the `AttributeReference.entityId` must resolve to a `BasicEventAttribute` entity in the same definition. Pointing at an `IdentityPartAttribute` returns `400 Invalid TimeSeriesView payload.` with no hint about the template type. If you want to pass an identity field dynamically, declare a parallel `BasicEventAttribute` over the same source field and reference that.

### Backend Execution Payload Shapes

The runtime request body sent to the Fabric jobs endpoint depends on `itemType`:

#### Notebook (`SynapseNotebook`)

```json
{
  "ExecutionData": {
    "Parameters": {
      "name": { "value": 345.13, "type": "float" },
      "isName": { "value": true, "type": "bool" },
      "NotebookName": { "value": "MyNotebook", "type": "string" }
    }
  }
}
```

#### Spark Job Definition (`SparkJobDefinition`)

```json
{
  "ExecutionData": {
    "mainClass": "com.microsoft.spark.example.OnePlusOneApp",
    "executableFile": "abfss://workspace@onelake.dfs.fabric.microsoft.com/lakehouse.Lakehouse/Files/job.jar",
    "commandLineArguments": "--input bronze --output silver"
  }
}
```

> Spark job definitions are schema-supported, but current backend parameter discovery returns no user-defined parameters. Use explicit parameter names like `mainClass`, `executableFile`, and `commandLineArguments`.

#### Dataflow (`DataflowFabric`)

```json
{
  "ExecutionData": {
    "ExecuteOption": "ApplyChangesIfNeeded",
    "Parameters": [
      { "parameterName": "Threshold", "type": "Automatic", "value": 25 },
      { "parameterName": "Mode", "type": "Automatic", "value": "Incremental" }
    ]
  }
}
```

#### User Data Function / Function Set (`UserDataFunctions` / `FunctionSet`)

```json
{
  "ExecutionData": {
    "FunctionName": "hello_fabric",
    "Parameters": {
      "name": "world"
    },
    "RunKind": "Activator",
    "RelatedArtifacts": "<activator-artifact-guid>"
  }
}
```

### Fabric Item Action Design Guidance

- The target Fabric item must already exist in the target workspace
- Resolve `itemId` and `workspaceId` dynamically via the Fabric Items API — do not hardcode
- The Activator's managed identity must have permissions to execute the target item
- Pipeline, notebook, dataflow, Spark job, and function actions can all pass parameters from the triggering event, but the runtime payload shape differs by item type

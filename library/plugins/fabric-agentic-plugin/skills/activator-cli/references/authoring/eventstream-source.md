# Activator Eventstream Source — Sink-First Push Workflow

Eventstream is a **push source** for Activator. Do **not** start by hand-authoring a full `eventstreamSource-v1` entity in `ReflexEntities.json`.

Instead, the supported workflow is:

1. create or identify the target Activator
2. create or update an Eventstream with an `Activator` destination pointing at that Activator
3. read the Activator definition back
4. find the auto-created Eventstream source and SourceEvent entities
5. add the rest of the trigger graph by referencing that discovered SourceEvent

## Eventstream-side topology shape

The Eventstream destination is authored on the **Eventstream** side, not inside `ReflexEntities.json`:

```json
{
  "name": "ActivatorDest",
  "type": "Activator",
  "properties": {
    "workspaceId": "<activator-workspace-guid>",
    "itemId": "<activator-item-guid>",
    "inputSerialization": {
      "type": "Json",
      "properties": { "encoding": "UTF8" }
    }
  },
  "inputNodes": [{ "name": "MainStream" }]
}
```

Minimal topology:

```json
{
  "sources": [
    {
      "name": "SampleSource",
      "type": "SampleData",
      "properties": { "type": "Bicycles" }
    }
  ],
  "streams": [
    {
      "name": "MainStream",
      "type": "DefaultStream",
      "properties": {},
      "inputNodes": [{ "name": "SampleSource" }]
    }
  ],
  "destinations": [
    {
      "name": "ActivatorDest",
      "type": "Activator",
      "properties": {
        "workspaceId": "<activator-workspace-guid>",
        "itemId": "<activator-item-guid>",
        "inputSerialization": {
          "type": "Json",
          "properties": { "encoding": "UTF8" }
        }
      },
      "inputNodes": [{ "name": "MainStream" }]
    }
  ],
  "operators": [],
  "compatibilityLevel": "1.1"
}
```

## Activator readback after sink creation

After the Eventstream sink is created, the target Activator definition auto-created:

1. one `eventstreamSource-v1`
2. one `timeSeriesView-v1` event view (`SourceEvent`) that references that source

### Auto-created `eventstreamSource-v1`

```json
{
  "uniqueIdentifier": "<eventstream-source-guid>",
  "payload": {
    "name": "EventStream",
    "metadata": {
      "eventstreamArtifactId": "<eventstream-item-guid>"
    }
  },
  "type": "eventstreamSource-v1"
}
```

### Auto-created SourceEvent view

```json
{
  "uniqueIdentifier": "<source-event-guid>",
  "payload": {
    "name": "<eventstream-display-name>-stream",
    "definition": {
      "type": "Event",
      "instance": "{\"templateId\":\"SourceEvent\",\"templateVersion\":\"1.1\",\"steps\":[{\"name\":\"SourceEventStep\",\"id\":\"<guid>\",\"rows\":[{\"name\":\"SourceSelector\",\"kind\":\"SourceReference\",\"arguments\":[{\"name\":\"entityId\",\"type\":\"string\",\"value\":\"<eventstream-source-guid>\"}]}]}]}"
    }
  },
  "type": "timeSeriesView-v1"
}
```

## Readback notes

- `payload.metadata.eventstreamArtifactId` matched the Eventstream item ID from the Eventstream item API.
- The auto-created SourceEvent `SourceSelector.entityId` pointed at the auto-created `eventstreamSource-v1.uniqueIdentifier`.
- The Eventstream destination node ID from Eventstream topology can match the `eventstreamSource-v1.uniqueIdentifier` seen in Activator readback.
- The auto-created Eventstream source and SourceEvent did **not** include explicit `parentContainer` fields in public readback.
- When appending rules to an Eventstream sink-created Activator, preserve missing `parentContainer` fields on the auto-created source/event entities. Do not invent a container unless you are adding a consistent container graph for every related entity.

Treat the destination-ID-to-source-ID match as a **useful readback clue**, not as an authoring input you set manually.

## Building the rest of the trigger graph

Once the sink has created the source entities:

1. call `getDefinition`
2. find the `timeSeriesView-v1` event view whose `definition.type` is `Event`
3. use that SourceEvent entity ID wherever the rule graph expects the upstream event reference
4. build the remaining rule and action entities using the general rule guidance for this skill
5. use the general rule template-version guidance for newly appended rules; do not downgrade a new rule just because an auto-created SourceEvent readback used an older version
6. to add a disabled rule, keep the rule entity lifecycle published and set `payload.definition.settings.shouldRun: false`; do not represent disabled state by changing lifecycle or by changing the auto-created source graph

## When to use Eventstream vs other Activator sources

Use Eventstream when:

- the upstream source is already modeled as an Eventstream topology
- data arrives continuously and should be pushed into Activator
- you want Activator to react to Eventstream sample data, CDC feeds, or Eventstream-connected services

Prefer KQL / DTB / Real-time Hub when:

- the scenario is naturally pull-based
- you can author the source completely inside `ReflexEntities.json`
- there is no Eventstream sink step involved

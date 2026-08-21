# Real-time Hub Source (`realTimeHubSource-v1`)

Monitors Fabric workspace events. Useful for governance and operational alerting — e.g., notifying when items are created, updated, or deleted.

Use a Real-Time Hub subscriptions container for workspace-event subscriptions:

```json
{
  "uniqueIdentifier": "<container-guid>",
  "payload": {
    "name": "eval-workspace-monitor",
    "type": "rthSubscriptions"
  },
  "type": "container-v1"
}
```

```json
{
  "uniqueIdentifier": "<rthub-source-guid>",
  "payload": {
    "name": "Workspace event monitor",
    "connection": {
      "scope": "Workspace",
      "tenantId": "<tenant-guid>",
      "workspaceId": "<workspace-guid>",
      "eventGroupType": "Microsoft.Fabric.WorkspaceEvents"
    },
    "filterSettings": {
      "eventTypes": [
        { "name": "Microsoft.Fabric.ItemCreateSucceeded" },
        { "name": "Microsoft.Fabric.ItemUpdateSucceeded" }
      ],
      "filters": []
    },
    "parentContainer": {
      "targetUniqueIdentifier": "<container-guid>"
    }
  },
  "type": "realTimeHubSource-v1"
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | yes | Display name |
| `connection.scope` | string | yes | e.g. `Workspace` |
| `connection.tenantId` | GUID | yes | Azure tenant ID |
| `connection.workspaceId` | GUID | yes | Fabric workspace ID |
| `connection.eventGroupType` | string | yes | e.g. `Microsoft.Fabric.WorkspaceEvents` |
| `filterSettings.eventTypes[].name` | string | yes | Event type names to monitor |
| `filterSettings.filters` | array | no | Additional filters |
| `parentContainer.targetUniqueIdentifier` | GUID | yes | Container ref |
| referenced container `payload.type` | string | yes | Use `rthSubscriptions` for Real-Time Hub workspace subscriptions |

## Required Workspace-Events Connection Shape

For Fabric workspace events, include all of these connection fields together:

```json
{
  "scope": "Workspace",
  "tenantId": "<tenant-guid>",
  "workspaceId": "<workspace-guid>",
  "eventGroupType": "Microsoft.Fabric.WorkspaceEvents"
}
```

Do not use ad-hoc container types such as `workspaceEvents` for this graph. Backend Real-Time Hub subscription builders use the `RthSubscriptions` enum, which serializes in Reflex definitions as `rthSubscriptions`.

> **Authoring caveat:** Fabric workspace-event subscriptions are normally provisioned through the OneRiver / Real-Time Hub subscription flow before the Activator definition is persisted. If a hand-authored `realTimeHubSource-v1` payload is rejected by `updateDefinition` with `Invalid definition`, do not keep adding Object / SplitEvent / Attribute scaffolding. Treat the source as requiring a known-good Real-Time Hub/onramp-created readback shape or a pre-created workspace-events fixture, then preserve that source graph when adding or updating rules.

## Supported Workspace Event Types

| Event Type | Description |
|------------|-------------|
| `Microsoft.Fabric.ItemCreateSucceeded` | An item was created |
| `Microsoft.Fabric.ItemCreateFailed` | An item creation failed |
| `Microsoft.Fabric.ItemUpdateSucceeded` | An item was updated |
| `Microsoft.Fabric.ItemUpdateFailed` | An item update failed |
| `Microsoft.Fabric.ItemDeleteSucceeded` | An item was deleted |
| `Microsoft.Fabric.ItemDeleteFailed` | An item deletion failed |

> `Microsoft.Fabric.ItemReadSucceeded` and `Microsoft.Fabric.ItemReadFailed` were retired for new subscriptions on 2025-03-21 and should not be used in new definitions.

## Event Payload Notes

- The event type tells you the lifecycle operation (`create`, `update`, `delete`, `succeeded`, `failed`)
- The event payload carries the changed artifact in `data.itemKind`, `data.itemId`, `data.itemName`, `data.workspaceId`, and `data.workspaceName`
- Artifact-specific differentiation is by `itemKind`, not by separate event type families

## Known Item-Kind Limitation

The official docs say Fabric workspace item events currently do **not** support these Power BI item kinds:

- Semantic Model
- Paginated report
- Report
- App
- Dashboard

# Backstage well-known actions

Verified from the Backstage first-party documentation on 2026-08-21. Treat this as
non-exhaustive and compare it with the target instance's Actions Service before use.

| Domain | Action | Key behavior |
| --- | --- | --- |
| Auth | `auth.who-am-i` | Returns current catalog user information and requires user credentials. |
| Catalog | `catalog.get-catalog-entity` | Reads one entity. |
| Catalog | `catalog.query-catalog-entities` | Queries entities with predicate filters. |
| Catalog | `catalog.register-entity` | Registers remote catalog locations. |
| Catalog | `catalog.unregister-entity` | Removes a location and entities it owns; destructive. |
| Catalog | `catalog.validate-entity` | Validates catalog entity content. |
| Catalog | `catalog.get-catalog-model-description` | Describes registered kinds, annotations, labels, tags, and relations. |
| Notifications | `notifications.get-notifications` | Reads the authenticated user's notifications with filters and pagination. |
| Scaffolder | `scaffolder.dry-run-template` | Validates a template without applying its effects. |
| Scaffolder | `scaffolder.list-scaffolder-actions` | Lists installed scaffolder actions. |
| Scaffolder | `scaffolder.list-scaffolder-tasks` | Lists template tasks. |
| Scaffolder | `scaffolder.execute-template` | Runs a template and may cause external effects. |
| Scaffolder | `scaffolder.get-scaffolder-task-logs` | Reads task execution logs. |
| Search | `search.query` | Queries indexed documents by type and query. |

Always inspect live action metadata. Action names exposed as MCP tools may be namespaced, and
permissions or filters may hide actions from a particular caller.

# ServiceNow integration

ServiceNow support is provided through active packages in `backstage/community-plugins`, not a
core Backstage plugin.

At commit `dc925a35a9064df8a12028244bfa3f172f5d1d95`, the frontend package is version
`1.14.0`, the backend package is version `1.13.1`, and the scaffolder module is version `2.16.1`.
Reverify versions and peer dependencies before installing.

## Capability map

| Capability | Package |
| --- | --- |
| Entity and user incident views | `@backstage-community/plugin-servicenow` |
| Incident API proxy | `@backstage-community/plugin-servicenow-backend` |
| Table API template actions | `@backstage-community/plugin-scaffolder-backend-module-servicenow` |

The frontend supports both legacy integration and an alpha entry point for the new frontend
system. Select the target mode explicitly. Entities use `servicenow.com/entity-id` to associate
incident records.

## Guardrails

- Verify current package peer dependencies and release status before installation.
- Keep base URL, username, password, tokens, and instance details in external configuration.
- Grant only the ServiceNow table and operation permissions needed.
- Treat create, update, and delete Table API actions as mutating and approval-gated.
- Validate incident-field mapping and avoid exposing sensitive ticket data to unauthorized users.

Sources:

- <https://github.com/backstage/community-plugins/tree/main/workspaces/servicenow>
- <https://github.com/backstage/community-plugins/tree/main/workspaces/scaffolder-backend-module-servicenow>

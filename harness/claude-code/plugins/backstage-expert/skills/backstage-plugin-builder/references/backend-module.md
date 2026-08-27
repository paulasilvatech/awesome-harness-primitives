# Backend Module

Use this to extend an existing Backstage backend plugin through official extension points.

## Official Direction

- Backend modules use `createBackendModule`.
- A module extends one backend plugin.
- Modules communicate through extension points, not plugin internals.
- Modules initialize before the plugin they extend.

## Common Module Types

- Catalog entity provider.
- Catalog processor.
- Scaffolder action.
- Auth provider or resolver.
- Search collator.
- Permission rule.

## Checks

- Identify the exact plugin being extended.
- Identify the official extension point package.
- Do not depend on private implementation files.
- Document installation in the backend app.
- Add tests for the extension point behavior.

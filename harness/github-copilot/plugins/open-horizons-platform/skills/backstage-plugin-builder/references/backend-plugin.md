# Backend Plugin

Use this for a new Backstage backend API or server-side integration owned by the plugin.

## Official Direction

- Use the new backend system for new backend work.
- Backend plugins are created with `createBackendPlugin`.
- Plugins declare dependencies on core services and register initialization logic.

## Workflow

1. Confirm plugin ID, API surface, auth needs, and external systems.
2. Create the backend plugin package.
3. Define routes, services, config schema, and permissions.
4. Add tests with Backstage backend test utilities when available.
5. Document `app-config.yaml` requirements.
6. Run validation commands.

## Expected Files

```text
plugins/<plugin-id>-backend/
  package.json
  README.md
  src/
    index.ts
    plugin.ts
    service/
      router.ts
```

## Checks

- Use `createBackendPlugin`.
- Use `coreServices` for logger, config, auth, discovery, database, and HTTP routing.
- Define unauthenticated routes explicitly and narrowly.
- Validate request input at the boundary.
- Do not put secrets in source or examples.

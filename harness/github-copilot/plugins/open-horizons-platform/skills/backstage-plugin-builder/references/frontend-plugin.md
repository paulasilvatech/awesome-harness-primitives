# Frontend Plugin

Use this for Backstage UI: pages, entity cards, tabs, dashboards, route content, and UI extensions.

## Official Direction

- Prefer the new frontend system for new work.
- Official docs state frontend plugin creation starts with `yarn new`, selecting plugin, and a package under `plugins/<pluginId>`.
- The new frontend system starts from `createFrontendPlugin` imported from `@backstage/frontend-plugin-api`.

## Workflow

1. Confirm plugin ID, target app path, and target Backstage version.
2. Run `yarn new` from the Backstage app root and select the frontend plugin option that matches the target version.
3. Implement a minimal page or extension first.
4. Add route bindings and app integration.
5. Add tests for rendering and entity conditions.
6. Run validation commands.

## Expected Files

```text
plugins/<plugin-id>/
  package.json
  README.md
  src/
    index.ts
    plugin.ts
    routes.ts
    components/
  dev/
    index.tsx
```

## Checks

- Export a stable plugin instance.
- Keep implementation outside `plugin.ts` when possible.
- Lazy-load large routable components.
- Avoid hard dependencies on another plugin's route refs when an external route is more appropriate.
- Document app integration in the plugin README.

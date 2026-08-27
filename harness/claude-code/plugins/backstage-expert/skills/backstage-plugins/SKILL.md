---
name: backstage-plugins
description: >-
  Apply Backstage plugin and module boundaries for frontend, backend, common, node, and
  extension-point code. Use when editing plugin or Backstage package TypeScript.
paths:
  - "plugins/**/*.{ts,tsx,json}"
  - "packages/**/*.{ts,tsx,json}"
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/instructions/backstage-plugins.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Plugin Conventions

These instructions apply to Backstage plugin and package implementation. They are authoritative
for plugin boundaries, frontend mode, backend registration, extension points, configuration, and
package-local validation in matched files; Backstage core contributor rules and repository-local
package policy win on conflict.

## Frontend and Backend Systems

- Declare frontend mode as `new`, `legacy`, or `dual` before editing.
- Use `createFrontendPlugin` for new frontend work.
- Preserve `createPlugin` only for explicit legacy support; use a documented alpha entry point
  when dual support is required.
- Use `createBackendPlugin` for backend plugins and `createBackendModule` for modules.
- Extend plugins through public extension points, not internal imports.

## Package Design

- Keep public exports minimal and update API reports or equivalent checks when public APIs change.
- Put shared types and schemas in common packages only when multiple packages consume them.
- Keep backend-only clients and extension points out of browser bundles.
- Declare config, permissions, auth assumptions, and external routes in package documentation.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep implementation independently testable. | App-only wiring hides plugin regressions. |
| Use lazy loading for large routable frontend surfaces. | It protects app startup performance. |
| Validate inputs and authorize backend operations. | Identity alone is not authorization. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Run package-local lint, typecheck, tests, and build scripts. | Run a Backstage core root build as routine validation. |
| Bind external routes explicitly. | Reach into another plugin's internal route definitions. |
| Preserve compatibility promised by the selected mode. | Silently convert a dual plugin to new-only. |

## Checklist Before Opening a PR

- [ ] Frontend mode and Backstage version are explicit.
- [ ] Plugin, module, and extension-point boundaries use public APIs.
- [ ] Config, auth, permissions, and route contracts are documented.
- [ ] Package-local validation and relevant API reports pass.
- [ ] No secrets, internal endpoints, or unrelated edits are present.

## References

- [New frontend plugin system](https://github.com/backstage/backstage/blob/master/docs/frontend-system/building-plugins/01-index.md)
- [New backend plugins and modules](https://github.com/backstage/backstage/blob/master/docs/backend-system/building-plugins-and-modules/01-index.md)

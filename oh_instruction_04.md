---
applyTo: "backstage/backstage.json,backstage/package.json,backstage/tsconfig.json,backstage/packages/app/**,backstage/packages/backend/**,backstage/plugins/ai-chat/**"
description: "Use when editing Backstage adopter-app composition, packages, dependency alignment, or package-owned tests."
---

# Backstage Application

These rules cover the adopter app under `backstage/`. App configuration is owned separately by the `backstage-config` instructions.

## Conventions

- Keep frontend composition in `backstage/packages/app`, backend composition in `backstage/packages/backend`, and reusable AI Chat behavior in its plugin package.
- Register plugins and modules through supported Backstage extension points; do not import package internals.
- Align `@backstage/*` dependencies with the release policy recorded by `backstage.json` and the root Backstage manifest.
- Preserve package ownership: package code, tests, and exports stay in the package that owns the behavior.
- Keep browser code free of server credentials, Node-only dependencies, and privileged integration logic.
- Use the repository's current frontend/backend system; make compatibility shims explicit and local when legacy behavior must remain.
- Prefer package public APIs and typed service contracts over cross-package relative imports.

## Verification

- The owning package's test, lint, typecheck, or build script covers the change.
- Dependency changes remain version-aligned across Backstage workspaces.
- Frontend bundles contain no secrets or backend-only configuration.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use package public APIs and execute the owning package checks. | Reach across package internals or claim an unrun build passed. |
| Preserve version alignment and frontend/backend boundaries. | Bundle secrets or backend-only configuration in browser code. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Package public APIs and workspace version alignment are preserved.
- [ ] Focused test, lint, typecheck, or build checks pass.
- [ ] Frontend output contains no secret or backend-only configuration.
- [ ] No unrelated edits or unresolved placeholders remain.

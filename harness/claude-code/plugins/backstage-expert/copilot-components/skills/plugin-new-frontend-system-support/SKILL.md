---
name: plugin-new-frontend-system-support
description: "Add new frontend-system support to an existing Backstage plugin while retaining its legacy entry point. Use when published or shared plugins need dual compatibility, alpha exports, PageBlueprint extensions, route reuse, and both old and new app consumers."
license: Apache-2.0
metadata:
  source-repository: "https://github.com/backstage/backstage"
  source-commit: "eeac444a9aba7c107525d2a726851e907418c181"
---

# Add new frontend-system support

Create an explicit dual-mode plugin without breaking existing legacy consumers.

## When to invoke

- "Add an alpha new-frontend entry point to this plugin."
- "Make this Backstage plugin work in old and new apps."
- "Publish dual frontend-system support."
- "Add PageBlueprint extensions while keeping createPlugin."

## Procedure

1. Confirm plugin mode is `dual`, target versions, publication audience, and a green package
   baseline.
2. Read [the pinned upstream procedure](references/upstream/SKILL.md).
3. Verify alpha exports, blueprints, route APIs, and compatibility packages against the target
   version.
4. Inventory the legacy plugin instance, routable extensions, routes, page shells, APIs, and tests.
5. Add the new-system alpha entry point and `createFrontendPlugin` surface while preserving the
   legacy entry point.
6. Update package exports and type mappings without changing existing import paths.
7. Reuse route refs and split page shells so both systems render correctly.
8. Test the legacy entry point and alpha entry point independently.
9. Run package lint, typecheck, tests, build, and publication dry-run when applicable.

## Output template

```markdown
## Dual frontend support result

**Package:** <package>
**Legacy entry:** <path>
**New entry:** <path>

| Contract | Legacy | New | Validation |
| --- | --- | --- | --- |
```

## Quality gate

- [ ] `dual` mode and supported Backstage versions are explicit.
- [ ] Existing import paths and legacy behavior remain compatible.
- [ ] The alpha entry point uses current new-system APIs.
- [ ] Routes, page layout, APIs, exports, and types work in both systems.
- [ ] Both entry points have tests.
- [ ] Package-local and publication checks pass.

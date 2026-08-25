---
name: backstage-plugin-full-frontend-system-migration
description: "Fully migrate a Backstage frontend plugin to the new frontend system and remove legacy support. Use when performing internal or intentionally breaking migrations from createPlugin to createFrontendPlugin, new route refs, blueprints, PageLayout, and legacy dependency removal."
license: Apache-2.0
metadata:
  source-repository: "https://github.com/backstage/backstage"
  source-commit: "eeac444a9aba7c107525d2a726851e907418c181"
---

# Backstage Plugin Full Frontend-System Migration

Perform a deliberate new-only migration after confirming that legacy compatibility may be dropped.

## When to invoke

- "Convert this internal plugin fully to the new frontend system."
- "Remove core-plugin-api from this plugin."
- "Replace legacy routable extensions with blueprints."
- "Drop the old plugin entry point."

## Procedure

1. Confirm `new` mode, consumer inventory, breaking-change approval, target version, and a green
   baseline.
2. Read [the pinned upstream procedure](references/upstream/SKILL.md).
3. Verify route-ref, blueprint, layout, and extension APIs against the target version.
4. Inventory every legacy export, consumer import, route binding, page shell, API, and test.
5. Migrate route refs and external-route defaults.
6. Replace the plugin instance and extensions with `createFrontendPlugin` and current blueprints.
7. Move page layout responsibility to the new system and migrate internal routing.
8. Remove legacy exports and dependencies only after consumer updates are complete.
9. Update tests, README, changeset, and migration notes.
10. Run package and consumer-app validation.

## Output template

```markdown
## Full frontend migration result

**Package:** <package>
**Breaking change:** <approved scope>

| Legacy contract | Replacement | Consumer migration | Validation |
| --- | --- | --- | --- |
```

## Progressive disclosure and bundled resources

- `references/upstream/SKILL.md`: complete upstream frontend-system migration procedure and examples.

## Quality gate

- [ ] New-only mode and breaking-change approval are explicit.
- [ ] All consumers and legacy exports are inventoried.
- [ ] Current new-system APIs are verified for the target version.
- [ ] Route, layout, API, and extension behavior is preserved.
- [ ] Legacy dependencies are removed only after consumer migration.
- [ ] Package, consumer, documentation, and changeset validation pass.

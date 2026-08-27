---
name: app-frontend-system-migration
description: >-
  Migrate a Backstage adopter app from the legacy frontend system to the new extension-based
  frontend system through hybrid and full-migration phases. Use when converting createApp, feature
  discovery, routes, sidebar, APIs, themes, or app-level frontend compatibility.
license: Apache-2.0
metadata:
  source-repository: "https://github.com/backstage/backstage"
  source-commit: eeac444a9aba7c107525d2a726851e907418c181
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/skills/app-frontend-system-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage app frontend-system migration

Adapt the pinned upstream Backstage migration procedure to the target app and version without
discarding working legacy behavior prematurely.

## When to invoke

- "Migrate packages/app to the new frontend system."
- "Enable hybrid frontend mode in Backstage."
- "Replace FlatRoutes and the legacy app shell."
- "Enable feature discovery and finish the app migration."

## Procedure

1. Confirm adopter-app mode, installed Backstage version, and a green app baseline.
2. Read [the pinned upstream procedure](references/upstream/SKILL.md).
3. Compare the target version with the pinned source commit and verify changed APIs in first-party
   documentation.
4. Inventory legacy app creation, routes, sidebar, APIs, themes, route bindings, and plugins.
5. Implement the hybrid phase first, preserving compatibility helpers and observable behavior.
6. Enable and validate feature discovery according to the target version.
7. Migrate one surface at a time with focused rendering, route, and integration tests.
8. Remove compatibility code only after every legacy surface has a new-system equivalent.
9. Run app typecheck, tests, build, and startup validation using repository scripts.

## Output template

```markdown
## App frontend migration result

**Phase:** inventory | hybrid | incremental | complete
**Target version:** <version>

| Surface | Legacy path | New-system path | Validation | Status |
| --- | --- | --- | --- | --- |
```

## Quality gate

- [ ] Adopter-app mode and target version are evidenced.
- [ ] A green baseline exists before migration.
- [ ] The pinned procedure was checked against the target version.
- [ ] Hybrid compatibility remains until equivalent new-system behavior is validated.
- [ ] Routes, sidebar, APIs, themes, and plugin installation are covered.
- [ ] App tests, typecheck, build, and startup checks pass.

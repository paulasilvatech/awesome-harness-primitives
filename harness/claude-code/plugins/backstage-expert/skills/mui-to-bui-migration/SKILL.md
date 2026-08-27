---
name: mui-to-bui-migration
description: >-
  Migrate Backstage app or plugin UI from Material-UI to Backstage UI with version-checked
  component mappings, CSS setup, accessibility, analytics, styling, and visual validation. Use
  when replacing @material-ui imports, MUI icons, makeStyles, or adopting BUI.
license: Apache-2.0
metadata:
  source-repository: "https://github.com/backstage/backstage"
  source-commit: eeac444a9aba7c107525d2a726851e907418c181
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/skills/mui-to-bui-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# MUI to Backstage UI migration

Migrate in reviewable slices and verify each component mapping against the target Backstage UI
version.

## When to invoke

- "Replace MUI with @backstage/ui."
- "Migrate makeStyles and MUI icons."
- "Adopt BUI components in this Backstage plugin."
- "Fix accessibility or analytics after a BUI migration."

## Procedure

1. Confirm target Backstage and `@backstage/ui` versions, frontend mode, and visual-test capability.
2. Read [the pinned upstream procedure](references/upstream/SKILL.md).
3. Verify component availability and props against the installed BUI package.
4. Inventory MUI packages, components, icons, styling APIs, theme assumptions, and tests.
5. Add the required BUI package and global CSS import through repository-approved dependency
   workflow.
6. Migrate one coherent component group at a time, preserving semantics and accessibility.
7. Prefer BUI navigation and interactive components so built-in analytics remain intact.
8. Replace styling with supported BUI tokens or CSS without copying incompatible MUI props.
9. Run typecheck, unit tests, accessibility checks, and visual review at supported viewports.
10. Remove MUI dependencies only when no remaining consumers require them.

## Output template

```markdown
## BUI migration result

**Package:** <package>
**BUI version:** <version>

| MUI surface | BUI replacement | Accessibility | Visual validation |
| --- | --- | --- | --- |
```

## Quality gate

- [ ] Component mappings match the installed BUI version.
- [ ] CSS, tokens, icons, and interaction semantics are migrated.
- [ ] Built-in analytics are not duplicated.
- [ ] Keyboard, focus, labels, contrast, and responsive behavior are reviewed.
- [ ] Typecheck, tests, and visual validation pass.
- [ ] MUI dependencies remain until all consumers are migrated.

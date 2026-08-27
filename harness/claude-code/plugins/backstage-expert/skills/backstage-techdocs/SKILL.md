---
name: backstage-techdocs
description: >-
  Configure, build, preview, publish, migrate, and troubleshoot Backstage TechDocs and MkDocs
  content. Use when handling techdocs-ref annotations, mkdocs.yml, local or external builders,
  object-storage publishers, CI generation, broken docs, or wiki-to-TechDocs migration.
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/skills/backstage-techdocs/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage TechDocs

Keep documentation source-controlled with its owner, validate generation before publication, and
separate authoring from storage credentials.

## When to invoke

- "Add TechDocs to this service."
- "Preview or fix a TechDocs build."
- "Move wiki content into repository docs."
- "Configure external TechDocs generation and publication."

## Procedure

1. Detect Backstage version, TechDocs builder mode, generator, publisher, storage, and CI workflow.
2. Confirm the catalog entity and `backstage.io/techdocs-ref` source.
3. Validate the source layout, `mkdocs.yml`, `docs/index.md`, navigation, links, and approved
   plugins.
4. For migrations, inventory source pages, preserve ownership and redirects where applicable, and
   avoid copying credentials or private operational data.
5. Run local TechDocs or MkDocs generation using the repository's existing command.
6. Inspect warnings, generated navigation, links, assets, and rendering.
7. For external builders, update CI and publication configuration without storing cloud
   credentials in the documentation repository.
8. Require explicit approval before publishing, changing storage, or deleting previously
   published content.
9. Validate the Backstage reader route after publication when runtime access is available.

## Deployment modes

| Mode | Use |
| --- | --- |
| Local builder | Development and small trusted installations. |
| External builder | CI-based production generation with controlled publication. |
| External source | Documentation sourced from another approved location. |

## Output template

```markdown
## TechDocs result

**Entity:** <entity ref>
**Builder:** <local or external>
**Publisher:** <type>

| Check | Result |
| --- | --- |

### Publication
- Approval: <approved | not requested | blocked>
- Result: <published | not run | failed>
```

## Quality gate

- [ ] The entity source and TechDocs annotation are valid.
- [ ] MkDocs config, navigation, links, plugins, and source files validate.
- [ ] Local generation succeeds before publication.
- [ ] Credentials remain external to docs and config examples.
- [ ] Publication or deletion is explicitly approved.
- [ ] Reader access is validated or reported as not tested.

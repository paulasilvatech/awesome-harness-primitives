---
name: backstage-techdocs
description: >-
  Use when editing tracked TechDocs configuration, annotations, navigation, or publication
  settings.
paths:
  - mkdocs.yml
  - backstage/catalog-info.yaml
  - backstage/examples/entities.yaml
  - backstage/app-config*.yaml
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/backstage-techdocs.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage TechDocs

## Conventions

- Keep `mkdocs.yml` navigation aligned with tracked source content; do not add entries for nonexistent root paths.
- Use `backstage.io/techdocs-ref` with a resolvable source location and a catalog owner responsible for publication.
- Keep local and external builder or publisher modes consistent with the matching Backstage configuration overlay.
- Preserve portable relative links, stable headings, accessible image text, and fenced Mermaid syntax supported by the configured MkDocs extensions.
- Keep publication credentials in CI or workload identity, never in MkDocs, catalog, or app configuration.
- Keep examples portable and independent of this checkout's absolute paths.

## Verification

- MkDocs strict build or the repository documentation check resolves navigation and links.
- TechDocs annotations resolve from the entity's source location.
- Publication configuration exposes no storage key or service credential.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Keep documentation portable and validate navigation, links, and entity annotations. | Depend on absolute checkout paths or unverified publication settings. |
| Use external credential providers for publication. | Commit storage keys or service credentials. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Strict documentation build or the repository documentation check passes.
- [ ] Entity annotations resolve from the source location.
- [ ] Publication configuration contains no literal credential.
- [ ] No unrelated edits or unresolved placeholders remain.

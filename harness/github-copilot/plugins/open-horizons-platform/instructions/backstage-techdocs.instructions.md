---
applyTo: "mkdocs.yml,backstage/catalog-info.yaml,backstage/examples/entities.yaml,backstage/app-config*.yaml"
description: "Use when editing tracked TechDocs configuration, annotations, navigation, or publication settings."
---

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

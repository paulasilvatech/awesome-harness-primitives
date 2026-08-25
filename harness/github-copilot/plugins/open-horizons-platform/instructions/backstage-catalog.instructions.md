---
applyTo: "backstage/catalog-info.yaml,backstage/catalog/*.yaml,backstage/examples/entities.yaml,backstage/examples/org.yaml,backstage/examples/demo-template.yaml,backstage/examples/template/content/catalog-info.yaml,docs/aeg-feature-scaffold/backstage/**/catalog-info.yaml"
description: "Use when editing Backstage catalog entities, ownership, relations, annotations, or discovery examples."
---

# Backstage Software Catalog

## Conventions

- Declare `apiVersion`, `kind`, kebab-case `metadata.name`, a useful description, and a resolvable `spec.owner`.
- Use lowercase kebab-case tags and stable namespaces; avoid encoding environments or mutable deployment details in entity identity.
- Express relationships with supported entity references and verify referenced owners, systems, components, APIs, resources, and locations exist.
- Keep `github.com/project-slug`, source locations, and TechDocs annotations pointed at real repositories and tracked paths.
- Use `ohorizons.ai/*` only for Open Horizons agent metadata; do not invent competing top-level fields.
- Keep examples ingestible and sanitized because templates and local catalog bootstrap consume them.
- Avoid duplicate entity triplets of `kind`, `namespace`, and `name`.

## Verification

- Catalog validation resolves owners and relation targets.
- Location targets and source annotations exist.
- Entity examples contain no credentials, tenant IDs, or customer-specific values.

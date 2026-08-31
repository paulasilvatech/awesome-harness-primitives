---
description: "Apply Backstage Software Catalog entity, ownership, relation, and discovery conventions. Use when editing catalog-info files or example entity YAML."
applyTo: "**/catalog-info.yaml,**/catalog-info.yml,examples/entities/**/*.yaml,examples/org/**/*.yaml"
---

# Backstage Software Catalog Conventions

These instructions apply to declarative Backstage catalog entities. They are authoritative for
entity identity, ownership, lifecycle, relations, and annotations in matched YAML; the target
repository's catalog model and registered custom kinds win on conflict.

## Entity Model

- Use stable lowercase entity names and explicit `spec.owner`.
- Choose `kind`, `spec.type`, and `spec.lifecycle` from the target catalog model.
- Model dependencies and APIs with supported relations rather than free-form annotations.
- Keep catalog YAML with the owning source repository when code is the source of truth.
- Use annotations only for registered integrations and never store credentials in entity files.

## Discovery and Ownership

- Preserve provider or location ownership and avoid registering the same entity through multiple
  sources.
- Treat missing owners and orphaned entities as governance findings, not values to guess.
- Validate entity references with the correct kind and namespace.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep entity identity stable across renames. | Entity-reference churn breaks relations and history. |
| Require a real owner. | Ownership drives accountability and permissions. |
| Keep provider schedules bounded. | Unbounded discovery can overload providers and the catalog. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Validate YAML and catalog ingestion. | Assume parse success means the entity was ingested. |
| Use explicit entity references. | Rely on ambiguous bare names across namespaces. |
| Document custom annotations. | Add integration keys or secrets to metadata. |

## Checklist Before Opening a PR

- [ ] Entity names, namespaces, kinds, types, lifecycle, and owners are valid.
- [ ] Relations resolve to intended entity references.
- [ ] Discovery does not duplicate an existing source.
- [ ] Catalog validation or ingestion evidence is recorded.
- [ ] No credentials, private tokens, or placeholders are present.

## References

- [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Descriptor format](https://backstage.io/docs/features/software-catalog/descriptor-format/)

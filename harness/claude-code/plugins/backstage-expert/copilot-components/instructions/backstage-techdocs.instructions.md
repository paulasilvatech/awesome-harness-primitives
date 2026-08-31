---
description: "Apply Backstage TechDocs source, MkDocs, build, publication, and ownership conventions. Use when editing mkdocs.yml or documentation rendered by TechDocs."
applyTo: "**/mkdocs.yml,docs/**/*.md"
---

# Backstage TechDocs Conventions

These instructions apply to TechDocs source and MkDocs navigation. They are authoritative for
documentation structure, TechDocs compatibility, local validation, and safe publication in
matched files; repository documentation policy and the selected TechDocs deployment model win on
conflict.

## Documentation Source

- Keep `docs/index.md` as the discoverable root when the project uses the conventional layout.
- Keep `mkdocs.yml` navigation aligned with files that exist.
- Use `techdocs-core` and repository-approved plugins only.
- Keep operational runbooks actionable and free of credentials or private production data.

## Build and Publication

- Distinguish local generation from external CI generation and publication.
- Validate locally before requesting publication.
- Require explicit approval before publishing to object storage or changing the publisher.
- Preserve the entity's `backstage.io/techdocs-ref` ownership and source location.

## Conventions

| Rule | Rationale |
| --- | --- |
| Treat docs as source-controlled product content. | Generated-site-only edits are lost. |
| Keep links relative and portable. | TechDocs builds in isolated environments. |
| Separate build credentials from content. | Docs repositories must not become secret stores. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Run the repository's TechDocs or MkDocs validation. | Assume Markdown rendering proves TechDocs publication. |
| Review generated navigation and links. | Leave missing files in `nav`. |
| Record publisher and storage impacts. | Publish or delete documentation without approval. |

## Checklist Before Opening a PR

- [ ] `mkdocs.yml`, navigation, plugins, and source files are consistent.
- [ ] Local generation or repository documentation checks pass.
- [ ] TechDocs ownership and source annotations remain valid.
- [ ] Publication is either approved or explicitly not run.
- [ ] Documentation contains no credentials or private production data.

## References

- [Backstage TechDocs](https://backstage.io/docs/features/techdocs/)

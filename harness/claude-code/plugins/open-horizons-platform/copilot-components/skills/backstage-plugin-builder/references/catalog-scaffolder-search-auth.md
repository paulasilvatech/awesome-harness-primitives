# Catalog, Scaffolder, Search, Auth, Permission, And TechDocs

Use this reference when the plugin is an extension of an existing Backstage capability rather than a standalone page or API.

## Catalog

- Use providers for source ingestion.
- Use processors for entity transformation or validation.
- Document entity kinds, annotations, and relations.
- Include sample `catalog-info.yaml` when useful.

## Scaffolder

- Use actions for custom template steps.
- Validate action input schema.
- Avoid shelling out when a typed API client is available.
- Add example templates and dry-run instructions.

## Search

- Use collators or modules for custom indexing.
- Define document shape and authorization behavior.
- Include index refresh and error handling strategy.

## Auth

- Use official auth extension points.
- Do not log tokens or profile claims beyond what is needed.
- Document sign-in resolver behavior.

## Permission

- Define resource type, policy behavior, and test cases.
- Deny by default when ownership or identity cannot be resolved.

## TechDocs

- Keep addon behavior isolated and documented.
- Test with generated docs and missing metadata.

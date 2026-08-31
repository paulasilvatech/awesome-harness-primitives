---
name: open-horizons-backstage-ai-catalog
description: "Install and use Backstage's AI catalog model for AiResource skills and rules plus mcp-server API entities, ownership, lifecycle, relationships, and source locations. Use when cataloging AI skills, governance rules, agents, or MCP servers."
---

# Backstage AI catalog

Model AI context as governed catalog entities while keeping skill and rule content in its source
repository.

## When to invoke

- "Catalog our AI skills and governance rules in Backstage."
- "Register an MCP server as an API entity."
- "Add the AiResource kind to Backstage."
- "Model ownership and dependencies between AI resources."

## Procedure

1. Confirm the target Backstage version and catalog backend mode.
2. Verify the current AI catalog documentation and package version.
3. Install `@backstage/plugin-catalog-backend-module-ai-model` in `packages/backend` and register
   the module through the backend system.
4. Model a skill or rule as `kind: AiResource` with lifecycle, owner, system, and type-specific
   fields.
5. Point `backstage.io/source-location` at the source skill or rule; do not copy its complete
   content into the entity.
6. Model an MCP server as `kind: API`, `spec.type: mcp-server`, with one or more explicit
   `remotes`.
7. Validate entity schemas, references, ownership, lifecycle, URLs, and catalog ingestion.
8. Protect internal or non-production MCP endpoints with repository policy and network controls.

## Model boundaries

- `AiResource` type `skill` may declare disciplines, categories, agents, and `dependsOn`.
- `AiResource` type `rule` requires a category and rationale.
- `mcp-server` is an API subtype and uses `remotes`, not an embedded OpenAPI definition.
- Source content remains external and addressable through source-location annotations.

## Open Horizons integration

- Scope the catalog output to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Backstage ownership, managed-identity, AKS, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage AI catalog result

| Entity | Type | Owner | Source or remote | Validation |
| --- | --- | --- | --- | --- |

### Module
- Package:
- Backend registration:
```

## Quality gate

- [ ] The AI catalog module and target version are verified.
- [ ] Every AI resource has stable identity, lifecycle, owner, and source location.
- [ ] Skill dependencies and rule rationales are explicit.
- [ ] MCP remotes use valid transport types and URLs.
- [ ] Catalog ingestion validates the registered model.
- [ ] Sensitive internal endpoints and credentials are not exposed.

## References

- [AI in the Software Catalog](https://backstage.io/docs/ai/ai-in-the-catalog)

---
name: open-horizons-backstage-catalog
description: >-
  Model, register, discover, validate, and troubleshoot Backstage Software Catalog entities,
  providers, processors, ownership, relations, locations, and lifecycle. Use when handling
  catalog-info YAML, entity ingestion, org discovery, duplicate entities, or catalog governance.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-catalog/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Software Catalog

Treat the catalog as a governed model whose declarative source remains with the systems it
describes.

## When to invoke

- "Create or validate catalog-info.yaml."
- "Configure GitHub organization discovery."
- "Why is this entity missing or duplicated?"
- "Model systems, APIs, resources, groups, and ownership."

## Procedure

1. Detect the repository mode, Backstage version, catalog providers, processors, and custom kinds.
2. Inventory entity sources and determine which source is authoritative for each entity.
3. Model stable identity, namespace, kind, type, lifecycle, owner, system, domain, APIs, resources,
   and relations.
4. Keep `catalog-info.yaml` with the owning code repository when code is the source of truth.
5. Configure locations or providers with bounded filters, schedules, timeouts, and credentials from
   integrations or secret storage.
6. Validate YAML, entity schemas, references, ownership, and ingestion logs.
7. Diagnose collisions, orphaning, refresh failures, provider rate limits, or processor errors
   before changing source records.
8. Report entity counts or examples without exporting sensitive annotations or provider tokens.

## Catalog criteria

- Entity names and namespaces are stable and unambiguous.
- Every production entity has an accountable owner.
- Relations use resolvable entity references.
- Provider and static-location sources do not duplicate the same entities.
- Deprecation and orphan status are explicit lifecycle signals, not cleanup shortcuts.

## Open Horizons integration

- Scope catalog changes to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Backstage ownership, managed-identity, AKS, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage catalog result

**Source of truth:** <provider, location, or repository file>

| Entity or provider | Owner | Validation | Status |
| --- | --- | --- | --- |

### Findings
- <duplicate, missing relation, ownership, ingestion, or schedule finding>
```

## Quality gate

- [ ] The authoritative entity source is explicit.
- [ ] Names, kinds, namespaces, types, lifecycle, and owners are valid.
- [ ] Relations resolve and discovery sources do not duplicate entities.
- [ ] Provider schedules and filters are bounded.
- [ ] Ingestion or catalog validation evidence is recorded.
- [ ] No credentials or sensitive integration values are stored in entity YAML.

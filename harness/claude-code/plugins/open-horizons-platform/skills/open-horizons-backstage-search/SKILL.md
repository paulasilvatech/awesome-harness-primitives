---
name: open-horizons-backstage-search
description: >-
  Install, configure, extend, operate, and troubleshoot Backstage Search frontends, engines,
  collators, indices, result extensions, filters, schedules, and permissions. Use when working
  with search pages, Catalog or TechDocs indexing, custom collators, Postgres or Elasticsearch, or
  missing results.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-search/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Search

Treat Backstage Search as an extensible indexing and presentation framework whose engine,
collators, and frontend result extensions are independently configurable.

## When to invoke

- "Install Backstage Search."
- "Index Catalog, TechDocs, or custom plugin content."
- "Add a collator, filter, or result component."
- "Diagnose stale or missing search results."

## Procedure

1. Confirm Backstage version, frontend mode, database, search engine, deployment topology, and
   indexed document types.
2. Install or verify `@backstage/plugin-search`, `@backstage/plugin-search-react`,
   `@backstage/plugin-search-backend`, the selected engine module, and collator modules.
3. Register the backend, engine, and Catalog or TechDocs collators.
4. Use frontend feature discovery or explicit modules for result items and filters.
5. Choose Lunr only for suitable in-memory scenarios; use an external or database-backed engine
   when persistence, scale, or multiple nodes require it.
6. Configure collator schedules with bounded frequency, timeout, initial delay, and distributed
   execution semantics.
7. Build custom collators with stable document types, location, authorization metadata, and
   incremental or batch behavior appropriate to the source.
8. Add result components and filters that match the indexed document contract.
9. Validate indexing logs, document counts, freshness, permissions, result rendering, and query
   behavior.
10. Diagnose engine, scheduler, collator, permission, or presentation layers separately.

## Open Horizons integration

- Scope search behavior to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Backstage ownership, data access, observability, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage Search result

| Document type | Collator | Engine | Schedule | Result extension | Status |
| --- | --- | --- | --- | --- | --- |

### Query validation
- Query:
- Expected:
- Actual:
```

## Quality gate

- [ ] Engine choice matches persistence, scale, and replica topology.
- [ ] Collator schedules are bounded and non-overlapping.
- [ ] Document types and frontend result extensions agree.
- [ ] Catalog, TechDocs, and custom collators expose intended content only.
- [ ] Permission-aware documents do not leak restricted content.
- [ ] Freshness, query, filter, and rendering tests pass.

## References

- [Backstage Search](https://backstage.io/docs/features/search/)
- [Search architecture](https://backstage.io/docs/features/search/architecture)
- [Getting started with Search](https://backstage.io/docs/features/search/getting-started)

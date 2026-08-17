---
name: backstage-plugin-builder
description: "Plan, architect, scaffold, validate, and prepare custom Backstage plugins and modules using official Backstage documentation. Use for frontend plugins, backend plugins, backend modules, catalog processors, scaffolder actions, search collators, auth providers, permission policies, TechDocs addons, common packages, node packages, plugin ADRs, architecture, validation hooks, and community publication preparation."
---

# Backstage Plugin Builder

Use this skill for Backstage plugin work. It plans, architects, validates, and prepares Backstage plugins using official Backstage guidance.

## Scope

This skill covers:

- Frontend plugins using the new frontend system.
- Backend plugins using the new backend system.
- Backend modules that extend existing backend plugins through extension points.
- Catalog processors, entity providers, and catalog integrations.
- Scaffolder actions and scaffolder modules.
- Search collators and search modules.
- Auth providers, resolvers, and auth modules.
- Permission policies and permission rules.
- TechDocs addons and documentation integrations.
- Common packages for shared types, schemas, and clients.
- Node packages for extension points and backend utilities.
- Planning artifacts, strategy, ADRs, architecture, hooks, validation scripts, and community publication preparation.

## First Step

Ask only for missing facts. If the intent is clear, proceed with the matching workflow.

Before recommending Backstage APIs, package versions, plugin types, publication steps, or migration guidance, validate current documentation through the `mcp-ecosystem` server when available. If the MCP lookup is unavailable or fails, state that in the output and use the official documentation fallback in [references/mcp-doc-validation.md](references/mcp-doc-validation.md).

Required facts for code generation:

- Plugin ID and package scope.
- Target Backstage app or monorepo path.
- Target Backstage version or package version policy.
- Plugin type: frontend, backend, backend module, catalog, scaffolder, search, auth, permission, TechDocs, common, or node package.
- Audience: internal, private package, open source, or community candidate.
- External systems, data sensitivity, auth needs, and runtime configuration.

## Routing

| User intent | Action |
| --- | --- |
| Plan, strategy, ADR, architecture | Read [references/planning-strategy-adr.md](references/planning-strategy-adr.md), then generate artifacts with `scripts/create_backstage_plugin_artifacts.py`. |
| Frontend plugin, page, card, tab, route, entity content | Read [references/frontend-plugin.md](references/frontend-plugin.md). |
| Backend plugin, API, service backend | Read [references/backend-plugin.md](references/backend-plugin.md). |
| Backend module, extension point implementation | Read [references/backend-module.md](references/backend-module.md). |
| Catalog provider, processor, scaffolder action, search, auth, permission, TechDocs | Read [references/catalog-scaffolder-search-auth.md](references/catalog-scaffolder-search-auth.md). |
| Dynamic loading strategy | Read [references/dynamic-plugin-strategy.md](references/dynamic-plugin-strategy.md). Keep it runtime-neutral. |
| Official community publication | Read [references/community-publication.md](references/community-publication.md). Prepare a package and PR plan, but do not promise acceptance. |
| Hooks, quality gates, validation scripts | Read [references/validation-hooks.md](references/validation-hooks.md). |

## Standard Workflow

1. Create plan, strategy, ADR, architecture, validation, and publication artifacts.
2. Scaffold or guide plugin creation using official Backstage commands and APIs.
3. Implement the smallest useful plugin slice.
4. Add tests and docs before publication or app integration.
5. Run validation scripts and package checks.
6. Prepare community publication only when the plugin is generic enough and the user requests it.

## Official Documentation Source Of Truth

Use [references/official-docs.md](references/official-docs.md) as the index of official Backstage documentation consulted by this skill.

Use [references/mcp-doc-validation.md](references/mcp-doc-validation.md) as the freshness gate for `mcp-ecosystem`, GitHub source lookup, and official web fallback.

Key principles:

- Use the new frontend system for new frontend plugins.
- Use the new backend system for backend plugins and modules.
- Use `createBackendPlugin` for standalone backend plugins.
- Use `createBackendModule` for modules that extend existing backend plugins.
- Use official extension points instead of reaching into plugin internals.
- Do not claim community publication is guaranteed. Maintainers decide.

## Scripts

Generate planning artifacts:

```bash
python .github/skills/backstage-plugin-builder/scripts/create_backstage_plugin_artifacts.py \
  --plugin-id my-plugin \
  --plugin-type frontend \
  --audience internal \
  --target-version 1.39.0 \
  --output plugins/my-plugin/docs
```

Validate a plugin package:

```bash
python .github/skills/backstage-plugin-builder/scripts/validate_backstage_plugin.py plugins/my-plugin
```

Validate official documentation fallback sources:

```bash
python .github/skills/backstage-plugin-builder/scripts/validate_official_docs.py
```

Generate local quality hooks:

```bash
python .github/skills/backstage-plugin-builder/scripts/generate_quality_hooks.py --root .
```

## Validation

- Run `python -m py_compile .github/skills/backstage-plugin-builder/scripts/*.py` after editing scripts.
- Validate documentation freshness with `mcp-ecosystem` when available; if not available, run `validate_official_docs.py` and cite the fallback.
- Run `validate_backstage_plugin.py` against generated or existing plugin packages.
- Run the package's `yarn lint`, `yarn tsc`, `yarn test`, and `yarn build` when available.
- For publication, run `npm pack --dry-run` and complete the community publication checklist.

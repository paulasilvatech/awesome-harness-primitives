---
name: backstage-plugin-builder
description: "Plan, architect, scaffold, validate, and prepare custom Backstage plugins and modules using official Backstage documentation. Use when the user asks for new, legacy, or dual frontend plugins, backend plugins, backend modules, catalog processors, entity providers, scaffolder actions, search collators, auth providers, permission policies, TechDocs addons, common packages, node packages, plugin ADRs, architecture, validation, or community publication preparation."
---

# Backstage plugin builder

Plan and build Backstage plugin work by routing the request to the correct plugin type, validating current official guidance, producing the smallest useful implementation slice, and reporting the checks needed before integration or publication.

## When to invoke

- "Plan a custom Backstage plugin for this app."
- "Scaffold a Backstage backend module for an extension point."
- "Add a catalog processor or scaffolder action."
- "Validate this Backstage plugin before publication."
- "Write a plugin ADR and architecture plan."

## Inputs

Collect only missing facts. If intent is already clear, proceed.

| Input | Why it matters |
| --- | --- |
| Plugin ID and package scope | Drives package name, route refs, catalog metadata, and publication naming. |
| Target Backstage app or monorepo path | Determines workspace layout, package manager commands, and integration files. |
| Target Backstage version or package version policy | Prevents stale API recommendations. |
| Plugin type | Choose frontend, backend, backend module, catalog, scaffolder, search, auth, permission, TechDocs, common, or node package. |
| Frontend mode | Select `new`, `legacy`, or `dual` explicitly; new work defaults to `new`, but never infer migration compatibility. |
| Audience | Internal, private package, open source, or community candidate changes docs and quality gates. |
| External systems, data sensitivity, auth needs, runtime configuration | Drives permissions, secrets, configuration schema, and backend boundary. |

## Prerequisites and context

- Validate current Backstage APIs, package versions, plugin types, publication steps, and migration guidance against first-party Backstage documentation.
- Use `references/documentation-validation.md` plus `references/official-docs.md` to choose and record first-party sources. Do not require an undeclared MCP server.
- Use official extension points instead of reaching into plugin internals.

## Plugin routing

| User intent | Required reference | Output to produce |
| --- | --- | --- |
| Plan, strategy, ADR, architecture | `references/planning-strategy-adr.md` | Decision record, architecture sketch, validation plan, and implementation sequence. |
| Frontend plugin, page, card, tab, route, entity content | `references/frontend-plugin.md` | New frontend system plugin surface with routes, components, APIs, tests, and docs. |
| Backend plugin, API, service backend | `references/backend-plugin.md` | New backend system plugin using `createBackendPlugin`. |
| Backend module, extension point implementation | `references/backend-module.md` | Module using `createBackendModule` against an official extension point. |
| Catalog provider, processor, scaffolder action, search, auth, permission, TechDocs | `references/catalog-scaffolder-search-auth.md` | Specialized module with integration tests and config contract. |
| Dynamic loading strategy | `references/dynamic-plugin-strategy.md` | Runtime-neutral loading approach that does not assume a proprietary loader. |
| Official community publication | `references/community-publication.md` | Package and PR plan; never promise maintainer acceptance. |
| Quality gates and validation scripts | `references/validation-hooks.md` | Repository-native checks and package-local validation. |

## Standard workflow

1. Confirm missing inputs, select `new`, `legacy`, or `dual` for frontend work, and validate documentation freshness against first-party sources.
2. Create plan, strategy, ADR, architecture, validation, and publication artifacts when the request is architectural.
3. Scaffold or guide plugin creation using official Backstage commands and APIs.
4. Implement the smallest useful plugin slice before expanding surfaces.
5. Add tests, docs, runtime config, and catalog metadata before publication or app integration.
6. Run validation scripts and package checks.
7. Prepare community publication only when the plugin is generic enough and the user explicitly requests it.

## Backstage API rules

| Area | Use | Avoid |
| --- | --- | --- |
| Frontend | New frontend system, routes, entity content, app integration points, package-local components. | Legacy examples unless required by the target app. |
| Backend plugin | `createBackendPlugin`, service factories, explicit config and permissions. | Side effects at import time or hidden singleton clients. |
| Backend module | `createBackendModule` and official extension points. | Importing another plugin's internal files. |
| Catalog | Catalog processors, entity providers, and integration points with clear ownership and refresh behavior. | Processors that mutate unrelated entity fields. |
| Scaffolder | Actions/modules with typed inputs, dry-run-safe logic, and tests. | Actions that shell out with unvalidated input. |
| Search | Collators/modules with batching and incremental behavior where supported. | Full re-indexing on every request path. |
| Auth and permission | Providers, resolvers, rules, policies, and least-privilege defaults. | Treating identity claims as authorization. |
| TechDocs | Addons and documentation integrations that preserve build and reader workflows. | UI-only docs changes with no generated documentation path. |
| Common and node packages | Shared types, schemas, clients, extension points, and backend utilities. | Cross-package cycles or app-specific leakage. |

## Scripts and commands

Run scripts from the installed skill directory. Resolve that directory from the active skill package instead of assuming a `.github/skills` installation path.

```bash
cd <installed-backstage-plugin-builder-skill-directory>
python3 scripts/create_backstage_plugin_artifacts.py \
  --plugin-id my-plugin \
  --plugin-type frontend \
  --mode new \
  --audience internal \
  --target-version 1.54.0 \
  --output <backstage-repository>/plugins/my-plugin/docs

python3 scripts/validate_backstage_plugin.py \
  <backstage-repository>/plugins/my-plugin \
  --mode new
python3 scripts/validate_official_docs.py
python3 -m py_compile scripts/*.py
```

Use `--run` only for a plugin package, never the Backstage core repository root. The validator runs available package-local `lint`, `tsc`, `test`, and `build` scripts. Use `--pack` to add `npm pack --dry-run`.

## Gotchas

- **Documentation freshness is load-bearing**: Backstage plugin APIs move; cite the first-party page or exact source commit used.
- **New systems are the default**: use the new frontend system and new backend system for new work unless the target app requires otherwise.
- **Frontend mode is explicit**: use `new`, `legacy`, or `dual`; do not let a legacy `createPlugin` example silently define a new plugin.
- **Core-root commands are constrained**: in `backstage/backstage`, use targeted tests, exact root `yarn tsc`, changed-file formatting, `yarn lint --fix`, and `yarn build:api-reports` as applicable. Do not run root `yarn build`, release, or changeset-version commands as routine validation.
- **Community publication is not guaranteed**: prepare a compliant package and PR plan, but maintainers decide.
- **Dynamic loading must stay runtime-neutral**: do not bake in a proprietary runtime unless the user named one.

## Progressive disclosure and bundled resources

- `references/official-docs.md`: index of official Backstage documentation.
- `references/documentation-validation.md`: freshness gate for first-party source lookup.
- `references/plugin-types.md`: choose the right package and extension shape.
- `references/planning-strategy-adr.md`, `references/frontend-plugin.md`, `references/backend-plugin.md`, `references/backend-module.md`, `references/catalog-scaffolder-search-auth.md`, `references/dynamic-plugin-strategy.md`, `references/community-publication.md`, `references/validation-hooks.md`: read only the route-specific file.
- `scripts/create_backstage_plugin_artifacts.py`, `scripts/validate_backstage_plugin.py`, `scripts/validate_official_docs.py`: deterministic artifact and validation helpers.
- `examples/catalog-info.yaml`, `examples/package-json-checklist.md`, `examples/plugin-readme-template.md`: publication and package examples.

The script names `validate_backstage_plugin.py` and `validate_official_docs.py` are the stable validation entry points even when invoked through a full path.

## Output template

```markdown
## Backstage plugin plan - <plugin-id>

**Status:** planned | implemented | validated | blocked
**Plugin type:** <frontend | backend | backend module | catalog | scaffolder | search | auth | permission | TechDocs | common | node>
**Frontend mode:** <new | legacy | dual | not applicable>
**Docs freshness:** <first-party URL or source commit | blocked>

| Area | Decision | Evidence or file |
| --- | --- | --- |
| Package | `<package name>` | `<source>` |
| Architecture | `<key design>` | `<reference or file>` |
| Validation | `<check>` | `<result>` |

**Commands run**
- `<command>`: <pass | fail | not available>

**Next steps**
- <smallest remaining implementation or publication task>
```

## Quality gate

- [ ] Missing facts were requested only when required to proceed.
- [ ] Official docs were validated against a named first-party URL or exact source commit.
- [ ] The chosen route matches the plugin type and request.
- [ ] Frontend work declares `new`, `legacy`, or `dual` mode explicitly.
- [ ] New frontend and backend work uses the new systems unless the target app requires legacy integration.
- [ ] Backend modules use official extension points and `createBackendModule`; backend plugins use `createBackendPlugin`.
- [ ] Generated artifacts, tests, docs, catalog metadata, and configuration are included when relevant.
- [ ] Script, package, and publication checks were run when available, with failures reported.
- [ ] No routine validation invoked a Backstage core root build, release, or changeset-version command.
- [ ] Community publication is framed as a preparation plan, not an acceptance guarantee.

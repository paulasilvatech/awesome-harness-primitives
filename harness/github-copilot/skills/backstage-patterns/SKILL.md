---
name: backstage-patterns
description: "Apply Backstage Software Catalog, TechDocs, Scaffolder, custom plugin, GitHub App, and production configuration patterns. Use when creating, reviewing, or troubleshooting Backstage entities, Golden Paths, documentation, plugins, or integrations."
metadata:
  mcpmarket-version: 1.0.0
---

# Backstage Patterns

Build and customize Backstage as an Internal Developer Portal using focused catalog, documentation,
templating, plugin, integration, and production patterns.

## When to invoke

- Creating or updating `catalog-info.yaml` for a service.
- Writing Backstage Scaffolder templates or Golden Paths.
- Building a custom Backstage frontend or backend plugin.
- Setting up TechDocs for a service.
- Configuring GitHub App integration.
- Designing the software catalog entity model.
- Onboarding services with ownership and dependency tracking.
- Implementing self-service provisioning workflows.
- Migrating documentation from a wiki to TechDocs.

## Workflow

1. Inspect the repository's Backstage version, `app-config` files, catalog conventions, plugins, and
   validation commands before selecting a pattern.
2. Identify the narrow surface: catalog, TechDocs, Scaffolder, custom plugin, GitHub integration, or
   production configuration.
3. Read only the applicable section of [the pattern reference](references/patterns.md).
4. Adapt examples to the installed Backstage APIs and local naming, ownership, lifecycle, and security
   conventions; do not copy version-sensitive snippets blindly.
5. Apply or return only the requested files and validate them with the repository's existing checks.

## Pattern references

- [Software Catalog](references/patterns.md#software-catalog)
- [TechDocs](references/patterns.md#techdocs)
- [Scaffolder templates](references/patterns.md#scaffolder-templates-golden-paths)
- [Custom plugins](references/patterns.md#custom-plugins)
- [GitHub App integration](references/patterns.md#github-app-integration)
- [Production configuration](references/patterns.md#production-configuration)

## Output template

```markdown
## Backstage Pattern Result

### Goal
- <catalog, TechDocs, Scaffolder, plugin, integration, or production configuration>

### Files
| Path | Purpose | Action |
| --- | --- | --- |
| `<path>` | <purpose> | <create, update, or review> |

### Pattern decisions
- Entity ownership:
- Lifecycle:
- Documentation:
- Template or plugin boundary:

### Validation
- Command or check:
- Result:
- Remaining risks:
```

## Quality gate

- [ ] The selected pattern matches the repository's installed Backstage version and local conventions.
- [ ] Catalog entities use valid kinds, ownership, lifecycle, relations, and stable identifiers.
- [ ] TechDocs, Scaffolder, plugin, and GitHub integration examples include only the resources needed.
- [ ] Credentials, tokens, integration keys, and production endpoints remain externalized.
- [ ] Generated or changed YAML and TypeScript receive the repository's existing validation.
- [ ] Version-sensitive claims are checked against official Backstage documentation before use.

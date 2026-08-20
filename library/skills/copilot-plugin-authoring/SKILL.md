---
name: copilot-plugin-authoring
description: "Create, migrate, audit, and validate GitHub Copilot plugins and marketplaces in this repository using Agent Plugins 1.0, canonical library sources, generated com.github.copilot mirrors, portable MCP configuration, hooks, client extensions, and isolated runtime tests. Use when adding a plugin, repairing a manifest, packaging existing agents or skills, or refreshing marketplace governance."
---

# GitHub Copilot plugin authoring

Build self-contained, installable plugin packages from canonical primitives and prove both static contracts and runtime discovery.

## When to invoke

- "Create a plugin from these existing agents and skills."
- "Migrate this plugin to Agent Plugins 1.0."
- "Why does this installed plugin not expose its agents?"
- "Audit every plugin in the marketplace."
- "Add hooks, MCP, or a client extension to a plugin."

## Source and layout decisions

Choose component ownership before editing:

| Mode | Canonical source | Runtime package |
| --- | --- | --- |
| `library` | `library/agents/` and `library/skills/` | Skills under `skills/`; agents generated under `com.github.copilot/agents/`. |
| `plugin` | The plugin's own `agents/`, `skills/`, `hooks/`, or `extensions/` | Canonical content stays local and runtime mirrors are generated under `com.github.copilot/`. |

Every managed manifest declares `extensions.com.paulasilvatech.copilot-primitives` with `componentSource`, `layoutVersion`, and source references. Do not hand-edit generated runtime mirrors.

Agent Plugins 1.0 uses:

- strict root `plugin.json`;
- fixed `skills/<name>/SKILL.md`;
- fixed root `mcp.json` with portable `stdio`, `streamable-http`, or `sse` transports;
- GitHub-specific agents, hooks, and client extensions under `com.github.copilot/`.

Instructions and VS Code prompts are repository workspace customizations, not portable core plugin components. Package a safe publisher skill when they must accompany a plugin.

## Procedure

1. Inspect the intended capability, existing canonical primitives, same-domain plugins, marketplace entry, and ownership mode.
2. Verify current first-party GitHub plugin, marketplace, hook, and Agent Plugins documentation when the user asks for current behavior, the CLI version changed, or local evidence conflicts.
3. Start from `docs/templates/plugin.template.json` and optionally `docs/templates/plugin-mcp.template.json`.
4. Use a valid plugin name that matches `library/plugins/<name>/`.
5. Reference only coherent agents, skills, hooks, MCP servers, or extensions. Reject componentless manifests and arbitrary “bundle everything” packages.
6. For shared sources, run `python3 library/scripts/normalize_plugin_manifests.py` and `python3 library/scripts/sync_plugin_components.py`.
7. Add or update the alphabetized `.github/plugin/marketplace.json` entry with source, exact manifest description, and exact version.
8. Validate schemas, components, ownership, marketplace coverage, and generated drift.
9. Install the plugin in an isolated `COPILOT_HOME`, list its skills and MCP servers, invoke a representative namespaced agent, and exercise hooks or extensions when their runtime surface is available.
10. Record dated current-platform evidence in `docs/HARNESS-VALIDATION.md` and regenerate `docs/PLUGIN-AUDIT.md` and `docs/CATALOG.md`.

## Required checks

```bash
python3 library/scripts/validate_primitives.py --strict
python3 library/scripts/normalize_plugin_manifests.py --check
python3 library/scripts/audit_plugins.py --check
python3 library/scripts/generate_catalog.py --check
python3 library/scripts/sync_plugin_components.py --check
python3 library/scripts/sync_installed_primitives.py --check
```

Also validate every new skill with the `skill-creator` validator, lint changed workflows with `actionlint`, compile or syntax-check bundled scripts, and run available package tests.

## Runtime acceptance

Static validation is not enough. A representative install must prove the applicable surfaces:

| Surface | Evidence |
| --- | --- |
| Plugin | `copilot plugin list` shows the expected version. |
| Marketplace | `copilot plugin marketplace browse <name>` lists the package. |
| Agent | `copilot --agent <plugin>:<agent>` resolves and runs. |
| Skill | `copilot skill list --json` reports `source: plugin`. |
| MCP | `copilot mcp list` shows each configured server. |
| Hook | A safe simulated payload or tool call produces the expected decision. |
| Client extension | Package install, mirror checks, dependency pinning, syntax, tests, and an interactive client test when available. |

Reinstall into a fresh isolated home after package changes because GitHub Copilot CLI caches installed content.

## Safety and quality

- Pin executable dependencies, actions, container images, and MCP packages to reviewed versions or digests.
- Embed no token, secret, tenant value, or private endpoint.
- Keep extension imports tied to an exact upstream commit and preserve source and license metadata.
- Do not claim a client extension works in non-interactive CLI merely because installation succeeds.
- Do not translate Agent Plugins MCP configuration to workspace MCP by copying it verbatim; map transports and validate the result.
- Do not refresh evidence dates without repeating the check.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Skills load but agents do not | Schema plugin still relies on root `agents/` | Generate `com.github.copilot/agents/` and declare the GitHub extension. |
| Manifest passes CLI but fails schema | Legacy top-level component fields remain | Move composition to repository extension metadata and normalize. |
| MCP server is absent | Legacy `.mcp.json`, missing schema, or wrong transport vocabulary | Use root `mcp.json` and the Agent Plugins MCP schema. |
| Hook does not fire | Wrong legacy path or non-executable script | Use the appropriate `com.github.copilot/hooks/hooks.json` mirror and direct payload tests. |
| Marketplace install is stale | Version or entry differs from manifest | Synchronize description/version and reinstall in a fresh home. |
| Audit reports drift | Canonical source changed without regeneration | Run the declared normalizer, importer, synchronizer, or catalog generator. |

## Limits

- Use the `copilot-primitive-architect` agent when package boundaries or component ownership are ambiguous.
- Use `skill-creator` for any skill created or repaired as part of the package.
- Do not import third-party code without verified provenance, license metadata, exact upstream commit, and applicable tests.

## Output template

```markdown
## Plugin authoring result

**Plugin:** <name>
**Version:** <version>
**Ownership:** <library|plugin>
**Status:** <created|migrated|repaired|blocked>

### Components
- Agents: <count>
- Skills: <count>
- Hooks: <count>
- MCP servers: <count>
- Client extensions: <count>

### Validation
- Schemas: <result>
- Repository gates: <result>
- Isolated install: <result>
- Runtime surfaces: <result>
- Unavailable tests: <reason or none>
```

## Quality gate

- [ ] Package purpose and component composition are coherent.
- [ ] Canonical ownership and generated mirrors are explicit.
- [ ] Manifest, MCP, hook, skill, and marketplace contracts pass.
- [ ] Dependencies and upstream sources are pinned.
- [ ] Isolated install proves every claimed runtime surface or reports an unavailable client test.
- [ ] Audit, catalog, synchronization, and repository gates pass.
- [ ] Current claims have dated first-party or runtime evidence.

# Backstage Expert

`backstage-expert` is a complete GitHub Copilot plugin for Backstage adopter applications,
Backstage core or fork contributions, and explicit frontend migration work. It packages one
mode-aware agent, focused skills, a safety hook, and a dry-run-first workspace publisher.

## Included capabilities

| Area | Primitive |
| --- | --- |
| App installation and bootstrap | `backstage-app-bootstrap` skill |
| Configuration and secrets | `backstage-app-configuration` skill |
| Sign-in and delegated access | `backstage-authentication` skill |
| Software Catalog | `backstage-catalog` skill |
| AI Catalog and MCP server entities | `backstage-ai-catalog` skill |
| Software Templates | `backstage-software-templates` skill |
| Plugin and module development | `backstage-plugin-builder` skill |
| Actions Registry and MCP tools | `backstage-mcp-actions` skill |
| TechDocs | `backstage-techdocs` skill |
| Kubernetes service-owner views | `backstage-kubernetes` skill |
| Notifications and signals | `backstage-notifications` skill |
| Authentication and permissions | `backstage-authentication` and `backstage-permissions` skills |
| Search engines and collators | `backstage-search` skill |
| Framework services and extension points | `backstage-framework` skill |
| GitHub, Azure DevOps, and ServiceNow | `backstage-external-integrations` skill |
| Operations and troubleshooting | `backstage-operations` skill |
| Version upgrades | `backstage-upgrade` skill |
| Backstage core contribution | `backstage-core-contribution` skill |
| Official frontend and OpenAPI migrations | Six pinned upstream adapter skills |
| Catalog database query performance | `backstage-catalog-db-performance` skill |
| Repository customization publication | `backstage-workspace-kit` skill |

## Runtime boundaries

Agent Plugins 1.0 installs the agent, skills, and safety hook. Repository instructions and VS
Code prompts are bundled but are not activated by plugin installation. Publish them with the
`backstage-workspace-kit` skill. The publisher plans changes by default and writes only with
`--apply`.

The agent detects one of these modes before editing:

1. Backstage adopter application.
2. Backstage core or a close fork.
3. Explicit legacy or dual frontend maintenance.
4. Open Horizons specialization.
5. Red Hat Developer Hub specialization.
6. Unknown, which blocks edits until the target is identified.

Open Horizons work belongs to the separately installable
`open-horizons-platform:open-horizons-backstage-expert` agent. This plugin does not silently
apply Open Horizons or Red Hat Developer Hub assumptions to a generic Backstage repository.

## Upstream provenance

Selected official Backstage skills are imported from
<https://github.com/backstage/backstage> at commit
`eeac444a9aba7c107525d2a726851e907418c181`. The imported reference snapshots remain
Apache-2.0 licensed. See `PROVENANCE.json`, `THIRD_PARTY_NOTICES.md`, `LICENSE`, and `NOTICE`.

## Safety

The `backstage-safety` hook defaults to approval mode. Set
`BACKSTAGE_EXPERT_HOOK_MODE=ask|audit|off` to control it. It asks before app creation,
version changes, publication, deployment, release operations, TechDocs publication, and
unsafe Backstage core root commands.

## Validation

From the repository root:

```bash
python3 harness/github-copilot/scripts/validate_primitives.py --strict
python3 harness/github-copilot/scripts/sync_plugin_components.py
python3 harness/github-copilot/scripts/audit_plugins.py --check
```

VS Code prompt files require **Chat: Run Prompt** for runtime validation. Static repository
validation does not prove prompt execution.

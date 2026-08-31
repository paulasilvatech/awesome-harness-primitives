---
applyTo: "backstage/catalog/ai-*.yaml,backstage/catalog/mcp-servers.yaml,backstage/plugins/ai-chat/**/*.ts,backstage/plugins/ai-chat/**/*.tsx,backstage/server/agent-api*/*.py,backstage/server/agent-api*/**/*.py"
description: "Use when editing Open Horizons AI catalog entities, AI Chat, agent APIs, or MCP tool exposure."
---

# Backstage AI Surfaces

These rules cover the catalog and application boundary between Backstage AI Chat, agent APIs, and MCP tools.

## Conventions

- Keep logical agent names, catalog entities, model-routing profiles, and UI choices aligned; do not expose deployment names as portable agent identities.
- Model AI assets with supported Backstage entity kinds and explicit owners, lifecycle, descriptions, and source relationships.
- Give MCP tools stable names, typed input/output contracts, bounded results, and an explicit read-only or mutating classification.
- Authenticate the Backstage service independently from the human actor and carry only validated identity context across the agent boundary.
- Preserve the AI Chat streaming contract and convert upstream failures into safe, actionable states without leaking prompts, tokens, or stack traces.
- Filter tool visibility and execution through authorization; catalog visibility is not execution permission.
- Keep model, endpoint, and credential configuration external to catalog entities and frontend bundles.
- Add contract tests for routing, stream parsing, denied tools, malformed events, and dependency failure.

## Verification

- Catalog identities and runtime role inventories agree.
- The browser receives no secret-bearing configuration or raw provider error.
- Tool execution remains governed even when invoked through MCP or delegated agents.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Preserve typed streaming, identity, authorization, and tool contracts. | Expose deployment details, credentials, raw errors, or unrestricted tools. |
| Execute routing, denied-tool, malformed-event, and dependency-failure tests. | Treat catalog visibility or hidden UI as execution permission. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Catalog, agent, route, and tool identities remain aligned.
- [ ] Authentication and backend authorization are tested separately.
- [ ] Streaming and failure-path contract tests pass or blockers are recorded.
- [ ] No secret-bearing client configuration or raw provider error is exposed.

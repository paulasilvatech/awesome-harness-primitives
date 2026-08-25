---
name: open-horizons-portal-integration
description: >-
  Implements and validates one product-specific integration in the existing Open Horizons Backstage portal and agent services. Use when wiring routes, plugins, catalog entities, app configuration, AI Chat SSE behavior, runtime APIs, or Backstage Kubernetes manifests without provisioning Azure or deploying live workloads.
---

# Open Horizons portal integration

Wire one product capability through the existing Backstage and runtime surfaces without crossing
identity, authorization, streaming, model-routing, or deployment boundaries.

## When to invoke

- Add or connect a portal route, navigation entry, frontend plugin, or backend module.
- Wire AI Chat to an existing Open Horizons agent runtime while preserving its SSE contract.
- Add product-specific catalog, configuration, or Kubernetes integration.
- Repair a broken connection between the Backstage frontend, proxy, runtime service, and manifest.

## Owning paths

Start from the actual surface that owns the behavior:

| Surface | Repository path |
| --- | --- |
| App composition and navigation | `backstage/packages/app/` |
| Backend composition and permission policy | `backstage/packages/backend/` |
| AI Chat plugin and SSE client | `backstage/plugins/ai-chat/` |
| Catalog entities | `backstage/catalog/` |
| Shared and environment config | `backstage/app-config*.yaml` |
| Kubernetes manifests | `backstage/k8s/` |
| Agent runtimes | `backstage/server/agent-api/`, `agent-api-impact/`, `agent-api-maf/`, `agent-api-sk/` |

Do not create substitute portal roots such as top-level `packages/`, `plugins/`, `golden-paths/`, or
`docs/`.

## Focused skill selection

Load only the Backstage skills needed by the selected surface:

| Change | Skill |
| --- | --- |
| Config layers or schema | `backstage-app-configuration` |
| Sign-in or delegated identity | `backstage-authentication` |
| Authorization or resource filtering | `backstage-permissions` |
| Catalog entities or discovery | `backstage-catalog` or `backstage-ai-catalog` |
| Frontend/backend plugin composition | `backstage-plugin-builder` or `backstage-framework` |
| Kubernetes visibility or manifests | `backstage-kubernetes` |
| External provider integration | `backstage-external-integrations` |
| Actions exposed as MCP tools | `backstage-mcp-actions` |

## Procedure

1. Define one user-visible flow and trace it through the existing route, plugin, proxy, backend
   module, runtime endpoint, config, catalog entity, or manifest that owns each hop.
2. Select the focused Backstage skills above and read the applicable path-scoped instructions.
3. Preserve authentication and authorization separately: keep browser requests credentialed,
   enforce permissions in the backend, and never treat a hidden UI control as access control.
4. Preserve the AI Chat contract when involved: `/api/proxy/agent-api` remains the Backstage proxy
   boundary, `/api/agents/chat` remains SSE, frames remain structured, fragmented frames and safe
   errors remain tested, and the frontend does not call a model provider directly.
5. Preserve model routing: repository harness model IDs stay on the GitHub Copilot surface, while
   application agents use the Microsoft Agent Framework and Microsoft Foundry deployment profiles
   defined by `.github/model-routing.yaml`. Fail closed on unknown routes or deployments.
6. Put shared defaults in `app-config.yaml`, environment overrides in the matching overlay, and
   secrets only in approved external configuration. Do not expose secrets through frontend config,
   catalog metadata, logs, or manifests.
7. Make the smallest end-to-end edit and add tests at the changed contract boundary.
8. Run the narrow package test, typecheck, config check, or runtime test that exercises the flow.
9. If `backstage/k8s/` or component selection changes, run:

   ```bash
   scripts/render-manifests.sh --dry-run
   ```

   Render local manifests without `--dry-run` only when generated output is an expected artifact
   of the task. The script is irrelevant for frontend-only, config-only, catalog-only, or runtime-
   only changes.
10. Report the flow, touched surfaces, focused skills, boundary checks, validation, and handoffs.

## Output template

```markdown
## Portal integration result

**Status:** completed | blocked
**Flow:** <user action -> portal -> backend/runtime -> result>

### Surfaces
| Path | Responsibility | Change |
| --- | --- | --- |

### Boundaries
| Auth | Permission | SSE | Model routing | Secrets |
| --- | --- | --- | --- | --- |

### Validation
- `<focused command>`: PASS | FAIL | NOT RUN - <evidence>
- `scripts/render-manifests.sh --dry-run`: <PASS | NOT RELEVANT | BLOCKED>

### Handoffs
- <Azure provisioning, organization settings, security review, deployment, or none>
```

## Limits

- Do not provision Azure, change organization settings, deploy live workloads, or manage secrets.
- Do not weaken backend permissions, bypass Backstage credentials, or replace SSE with an
  incompatible response contract.
- Do not pass GitHub Copilot model identifiers to application agents or Foundry deployment names
  to repository harness agents.
- Do not invent paths or broaden a product integration into a platform redesign.

## Quality gate

- [ ] One user flow is traced through real Open Horizons paths.
- [ ] Only relevant Backstage skills and surfaces were selected.
- [ ] Authentication, backend authorization, SSE, model routing, and secrets boundaries are preserved.
- [ ] Focused tests cover the changed integration contract.
- [ ] Manifest rendering ran only when Kubernetes or component selection made it relevant.
- [ ] Azure, organization, live deployment, and secret-management work has a separate owner.

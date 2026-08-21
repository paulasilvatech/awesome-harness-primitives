---
name: "open-horizons-backstage"
description: "Deploy, validate, and configure the Open Horizons Backstage portal with auth, catalog, Golden Paths, TechDocs, and AI Chat integration."
argument-hint: "environment=dev auth_provider=github github_identity_mode=standard components=Portal,GoldenPaths,TechDocs,AIChat"
agent: "open-horizons-backstage-expert"
tools: ['read', 'search', 'edit', 'execute', 'web']
---

# /open-horizons-backstage

## Objective
Configure and validate the Open Horizons Backstage portal so developers can sign in, browse catalog entities, run Golden Paths, read TechDocs, and use AI-enabled portal features where dependencies are ready.

## When to Invoke
Invoke this after Azure and Terraform prerequisites are ready, after `scripts/render-k8s.sh` has generated manifests when needed, or when Backstage-specific health, auth, catalog, scaffolder, TechDocs, or AI Chat issues need focused work.

## Preconditions
- The target environment `${input:environment:dev, staging, or prod}` is selected.
- Required infrastructure dependencies for the requested components are deployed or explicitly identified as pending.
- `.env.example` documents the relevant auth and image configuration model, and the generated environment file follows it.
- Kubernetes manifests can be rendered from `backstage/k8s/templates/` with `scripts/render-k8s.sh`.

## Inputs the Team Must Provide
- `environment`: Open Horizons environment to configure or validate.
- `auth_provider`: One of `github`, `entra`, or `guest`.
- `github_identity_mode`: One of `standard`, `saml-sso`, or `enterprise-managed-users`.
- `components`: Requested Backstage areas, such as `Portal`, `Golden Paths`, `TechDocs`, and `AI Chat`.

## What I Will Do
- Consult official Backstage documentation through available MCP ecosystem tools before recommending Backstage-specific configuration.
- Inspect `backstage/`, `backstage/k8s/templates/`, `golden-paths/`, and related rendered manifests before editing.
- Keep Backstage sign-in separate from GitHub technical integration, especially for Enterprise Managed Users.
- Use pinned image tags and generated manifests; do not introduce `latest` tags.
- Provide targeted validation commands for portal health, catalog ingestion, scaffolder templates, TechDocs, and AI Chat wiring.

## What I Will NOT Do
- I will not validate Azure subscription quota or provider registration; use the `azure-infra` prompt for that.
- I will not orchestrate the full platform deployment; use the `deploy-platform` prompt for end-to-end sequencing.
- I will not disable production authentication, expose unauthenticated backend ports, or commit secrets.
- I will not use commercial Backstage-specific assumptions; this repo targets open-source Backstage.

## Output Format
Approved workspace edit. Modify only files required by the prompt scope, then return a chat summary with changed paths and validation evidence.

Return a Backstage readiness and configuration summary in this shape:

````markdown
# Backstage Portal Plan

| Area | Target | Repository Path | Validation | Status |
| --- | --- | --- | --- | --- |
| Auth | github/entra/guest | `backstage/k8s/` | callback and sign-in check | Pending |
| Catalog | Golden Paths | `golden-paths/` | catalog ingestion check | Pending |
| TechDocs | enabled/disabled | `backstage/` | docs route check | Pending |
| AI Chat | enabled/disabled | `backstage/plugins/ai-chat/` | API health check | Pending |

## Commands
```bash
./scripts/render-k8s.sh
./scripts/validate-deployment.sh --environment <env>
```
````

## Definition of Done
- [ ] Requested Backstage components are mapped to real repository paths.
- [ ] Auth provider and GitHub identity mode are stated without mixing sign-in and technical integration.
- [ ] Required manifest rendering and validation commands are provided.
- [ ] Official Backstage documentation was consulted for Backstage-specific claims.
- [ ] Any Azure, Terraform, GitHub, ADO, security, or SRE work is redirected to the correct prompt.

## Prompt Body
You are the `@open-horizons-backstage-expert` agent. Focus on the open-source Backstage portal implementation in this repository and use the platform-specific files before proposing changes.

**Step 1 - Confirm requested components.** Parse `${input:components:Portal, Golden Paths, TechDocs, AI Chat}`, `${input:auth_provider:github, entra, or guest}`, and `${input:github_identity_mode:standard, saml-sso, or enterprise-managed-users}`. If dependencies are not ready, report the blocker and redirect to the `azure-infra` prompt or the `deploy-platform` prompt.

**Step 2 - Consult Backstage references.** Use `mcp-ecosystem/*` tools or web documentation for Backstage-specific behavior, then ground recommendations in local paths such as `backstage/`, `backstage/k8s/templates/`, and `golden-paths/`.

**Step 3 - Apply safe portal changes.** Edit only Backstage-related configuration needed for the requested components. Preserve pinned images, generated manifest flow, resource requests, probes, and non-root Kubernetes standards.

**Step 4 - Render and validate.** Use `./scripts/render-k8s.sh` when manifest templates change and `./scripts/validate-deployment.sh --environment ${input:environment:dev, staging, or prod}` when deployment evidence is available.

**Step 5 - Report handoffs.** Summarize portal URL assumptions, template visibility, auth callback requirements, and any handoff to the `security-review` prompt, the `hybrid-setup` prompt, or the `deploy-platform` prompt.

## Invocation Example
```text
/open-horizons-backstage environment=dev auth_provider=entra github_identity_mode=enterprise-managed-users components=Portal,GoldenPaths,TechDocs,AIChat
```

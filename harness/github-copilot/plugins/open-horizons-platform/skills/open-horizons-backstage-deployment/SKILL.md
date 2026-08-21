---
name: open-horizons-backstage-deployment
description: "Use when deploying or validating the upstream open-source Backstage developer portal on Azure AKS or locally, including app config, Kubernetes manifests, PostgreSQL, ACR image, GitHub OAuth, Microsoft Entra ID, and Enterprise Managed Users; produces deployment steps, health checks, and remediation. DO NOT USE FOR: full platform orchestration (use deploy-orchestration) or Azure infrastructure provisioning (use azure-portal-deploy). Triggers include \"deploy Backstage on AKS\", \"validate Backstage auth\", \"run Backstage locally\"."
---

# Open Horizons Backstage Deployment

This workflow deploys or validates the Open Horizons Backstage portal, either on AKS through repository manifests or locally for development. It produces a deployment plan, configuration checks, health evidence, and troubleshooting guidance while leaving full platform orchestration to `deploy-orchestration`.

> [!NOTE]
> This skill may shell out to `az`, `kubectl`, `docker`, `node`, `yarn`, and `gh`. Use Backstage official documentation through the `mcp-ecosystem` Backstage docs tools when available, and render Kubernetes manifests with `scripts/render-k8s.sh` before applying template-based changes.

## When to invoke
- "Deploy Backstage on AKS for Open Horizons."
- "Validate Backstage GitHub OAuth and Microsoft Entra ID settings."
- "Run the Backstage portal locally for development."
- "Troubleshoot why the Backstage pod is not ready."

## Prerequisites and context
- Repository paths exist: `backstage/`, `backstage/k8s/`, `terraform/modules/backstage/`, and `scripts/render-k8s.sh`.
- Azure and cluster access are configured for AKS deployment.
- GitHub App or OAuth credentials are available through approved secret storage.
- `AUTH_PROVIDER` and `GITHUB_IDENTITY_MODE` are selected for the target environment.
- User approval is available before building images, applying manifests, or updating auth configuration.

## Procedure

### Step 1: Load official and repository context
- Use Backstage documentation via `mcp-ecosystem` when available for deployment, Kubernetes, GitHub auth, and Microsoft auth.
- Inspect `backstage/app-config.yaml` and `backstage/app-config.production.yaml` when configuration changes are in scope.
- Inspect rendered or source manifests under `backstage/k8s/`.

### Step 2: Validate prerequisites
```bash
gh auth status
az account show -o table
kubectl config current-context
node --version
yarn --version
docker --version
```

- [ ] The cluster context is correct.
- [ ] Secrets are not printed.
- [ ] Auth provider mode matches the identity model.
- [ ] For Enterprise Managed Users, use `AUTH_PROVIDER=entra` with `GITHUB_IDENTITY_MODE=enterprise-managed-users` and keep GitHub App credentials for technical integration.

### Step 3: Confirm before deployment or configuration mutation
```text
Backstage operation summary:
- Target: local | AKS
- Namespace or local port:
- Auth provider:
- Manifests or image affected:
- Secrets or credentials affected:
Proceed with Backstage deployment or configuration changes? (y/n)
```

> [!IMPORTANT]
> Only proceed with image builds, manifest applies, Helm changes, auth changes, or paid Azure dependencies if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the plan and stop.

### Step 4: Render and deploy AKS manifests when approved
```bash
./scripts/render-k8s.sh
kubectl apply -f backstage/k8s/
kubectl rollout status deployment/backstage -n backstage --timeout=300s
```

If the platform is being deployed end to end, route to `scripts/deploy-full.sh` through `deploy-orchestration` instead of manually applying unrelated layers.

### Step 5: Validate portal health
```bash
kubectl get pods -n backstage
kubectl logs -n backstage -l app.kubernetes.io/name=backstage --tail=100
POD=$(kubectl get pod -n backstage -l app.kubernetes.io/name=backstage -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n backstage "$POD" -- \
  node -e "fetch('http://localhost:7007/.backstage/health/v1/readiness').then(r=>console.log(r.status))"
```

Expected readiness response is HTTP `200`.

### Step 6: Validate auth and catalog integration
- [ ] GitHub OAuth callback is `https://<portal-url>/api/auth/github/handler/frame` when GitHub auth is used.
- [ ] Microsoft callback is `https://<portal-url>/api/auth/microsoft/handler/frame` when Entra auth is used.
- [ ] GitHub App credentials are present for catalog sync, scaffolder writes, Actions, PRs, Codespaces, and packages.
- [ ] Golden Path templates under `golden-paths/` are reachable by catalog locations.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Secrets printed, wrong auth provider for Enterprise Managed Users, or production portal unavailable. |
| High | Pod crash loop, database connection failure, invalid OAuth callback, or public exposure without approval. |
| Medium | Catalog templates missing, image tag mismatch, or readiness probes failing intermittently. |
| Low | Documentation, labels, or local developer experience gaps. |

## Limits

- Do not use this skill for: full platform orchestration (use deploy-orchestration) or Azure infrastructure provisioning (use azure-portal-deploy).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Pod is not ready | Collect pod status, recent logs, and readiness endpoint result before changing manifests. |
| Auth callback fails | Verify provider mode, callback URL, client ID, and secret source without printing secrets. |
| Templates do not load | Check catalog locations and YAML parse errors in Backstage logs. |
| Manifest rendering fails | Report the missing `.env` value or template error and rerun `scripts/render-k8s.sh` after correction. |

## Output template

Return exactly this structure:
```markdown
# Backstage Deployment Report

## Scope
- Target:
- Namespace:
- Auth provider:

## Commands
| Command | Result |
|---|---|

## Health
| Check | Expected | Actual |
|---|---|---|

## Findings
| Severity | Finding | Fix |
|---|---|---|
```

## Quality gate
- [ ] Backstage official docs are checked when API or config guidance is needed.
- [ ] User confirmation is captured before deployment or configuration mutation.
- [ ] Kubernetes manifests are rendered with `scripts/render-k8s.sh` when templates are involved.
- [ ] Readiness, logs, auth mode, and catalog status are verified.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.

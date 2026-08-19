---
name: "azure-infra"
description: "Validate Azure subscription readiness and infrastructure dependencies for Open Horizons AKS, Key Vault, PostgreSQL, ACR, Managed Redis, and AI Foundry."
argument-hint: "environment=dev region=eastus2 components=AKS,KeyVault,PostgreSQL,ACR azure_context=<subscription-id>"
agent: "azure-portal-deploy"
tools: ['read', 'search', 'execute']
---

# /azure-infra

## Objective
Validate and prepare the Azure-side prerequisites that Open Horizons needs before Terraform, Kubernetes, and Backstage deployment can proceed safely.

## When to Invoke
Invoke this before the `deploy-platform` prompt, when an Azure validation run reports provider, quota, region, resource, or AKS access issues, or when confirming a subscription is ready for H1 Foundation infrastructure.

## Preconditions
- Azure CLI access is available to an authorized operator for `${input:azure_context:subscription name or ID}`.
- The target environment `${input:environment:dev, staging, or prod}` is known.
- The target region `${input:region:eastus2}` is approved for the deployment.
- The team knows which components are in scope: `${input:components:AKS, Key Vault, PostgreSQL, ACR, Managed Redis, AI Foundry, all}`.

## Inputs the Team Must Provide
- `environment`: Open Horizons environment, such as `dev`, `staging`, or `prod`.
- `region`: Azure region to validate, for example `eastus2`.
- `components`: Azure services to validate or prepare.
- `azure_context`: Subscription name, subscription ID, or tenant context expected by the run.

## What I Will Do
- Verify active Azure context before inspecting resources.
- Check provider registration, regional quota, SKU availability, and existing resource inventory.
- Use repository paths such as `.env.example`, `terraform/environments/`, and `terraform/modules/` to align findings with real Open Horizons configuration.
- Identify whether Terraform should create, validate, import, or remediate each component.
- Report Key Vault secret names and resource readiness without exposing secret values.

## What I Will NOT Do
- I will not manually create Terraform-managed resources unless an approved import or remediation path exists.
- I will not delete resource groups, clusters, databases, registries, or other Azure resources.
- I will not request quota increases, enable paid services, or change production access without explicit approval.
- I will not print keys, passwords, connection strings, tokens, or Key Vault secret values.

## Output Format
Chat response only. Do not create or modify workspace files from this prompt.

Return an Azure readiness report in this shape:

````markdown
# Azure Infrastructure Readiness

| Component | Expected State | Evidence | Gap | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| AKS | ready | `az aks show ...` | none | azure-portal-deploy | Pass |
| Key Vault | ready | secret names only | missing secret reference | security/deploy | Action Required |

## Provider and Quota Checks
- Subscription: `<id or name>`
- Tenant: `<tenant id or alias>`
- Region: `<region>`
- Provider blockers: `<none or list>`

## Recommended Next Commands
```bash
./scripts/validate-prerequisites.sh
./scripts/validate-config.sh --environment <env>
```
````

## Definition of Done
- [ ] Azure context, subscription, tenant, and region are identified.
- [ ] Provider, quota, SKU, and component readiness are summarized.
- [ ] Terraform ownership or import/remediation guidance is clear for every gap.
- [ ] No secret values are displayed.
- [ ] Next step is routed to the `terraform` prompt, the `backstage` prompt, or the `deploy-platform` prompt as appropriate.

## Prompt Body
You are the `@azure-portal-deploy` agent. Focus on Azure subscription and resource readiness for Open Horizons, not Terraform module authoring or Backstage application configuration.

**Step 1 - Confirm Azure context.** Compare the active Azure account with `${input:azure_context:subscription name or ID}` before running inventory or provider checks. Stop and report a context mismatch before collecting environment data.

**Step 2 - Inspect repository expectations.** Read `.env.example`, `terraform/environments/`, and relevant module names under `terraform/modules/` so Azure checks map to actual Open Horizons components.

**Step 3 - Validate Azure readiness.** Check provider registration, quotas, regional availability, and existing resources for `${input:components:AKS, Key Vault, PostgreSQL, ACR, Managed Redis, AI Foundry, all}` in `${input:region:eastus2}`.

**Step 4 - Classify every gap.** For each missing or unhealthy resource, state whether Terraform should create it, Terraform should import it, Azure must be remediated, or another agent owns the fix.

**Step 5 - Provide safe next actions.** Recommend `./scripts/validate-prerequisites.sh`, `./scripts/validate-config.sh --environment ${input:environment:dev, staging, or prod}`, or the `deploy-platform` prompt only when readiness evidence supports it.

## Invocation Example
```text
/azure-infra environment=dev region=eastus2 components=AKS,KeyVault,PostgreSQL,ACR azure_context=00000000-0000-0000-0000-000000000000
```

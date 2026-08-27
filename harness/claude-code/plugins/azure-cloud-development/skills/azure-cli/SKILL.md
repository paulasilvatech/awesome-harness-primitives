---
name: azure-cli
description: >-
  Azure CLI operations run az commands for cloud resource discovery, subscription context,
  identity, AKS, ACR, Key Vault, RBAC, managed identity, and federated credential workflows. Use
  this skill when working with az login, az account, az aks, az acr, az keyvault, resource group
  checks, or Azure day-2 operations.
---

<!-- Generated from harness/github-copilot/plugins/azure-cloud-development/skills/azure-cli/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure CLI

Use this skill to turn Azure operations requests into ordered `az` command workflows, verify the active cloud context, and return resource, identity, AKS, ACR, Key Vault, RBAC, or subscription evidence without exposing secrets.

## When to invoke

- "Check the current Azure subscription and account context."
- "Query Azure resources in a resource group."
- "Get AKS credentials or inspect an AKS cluster."
- "List Key Vault secret names or ACR repositories."
- "Configure or validate Azure RBAC, managed identity, or federated credentials."

## Prerequisites and context

- Azure CLI installed.
- Authenticated with `az login` or managed identity.
- Subscription selected.
- Appropriate RBAC roles.

## Procedure

1. Confirm authentication and subscription context before querying or changing Azure resources.
2. Select the narrowest `az` command for the requested resource type.
3. Prefer readable table output for human review and JSON output when another tool will parse the result.
4. Redact or avoid secret values in any returned output.
5. Return the result using the output template.

### Context

```bash
# Show current account
az account show -o table

# List subscriptions
az account list -o table --query "[].{Name:name, ID:id, State:state}"

# Set subscription
az account set --subscription "<subscription-id>"
```

### Resource queries

```bash
# List resources in RG
az resource list -g <resource-group> -o table

# Show resource
az resource show --ids <resource-id>

# Query with JMESPath
az resource list -g <rg> --query "[?type=='Microsoft.ContainerService/managedClusters']"
```

### AKS operations

```bash
# Get credentials
az aks get-credentials -g <rg> -n <cluster> --overwrite-existing

# Show cluster
az aks show -g <rg> -n <cluster> -o table

# Node pools
az aks nodepool list -g <rg> --cluster-name <cluster> -o table

# Scale cluster
az aks scale -g <rg> -n <cluster> --node-count 5
```

### Key Vault

```bash
# List secrets (names only)
az keyvault secret list --vault-name <kv> -o table --query "[].{Name:name}"

# Get secret
az keyvault secret show --vault-name <kv> -n <secret> --query value -o tsv
```

### ACR

```bash
# List repositories
az acr repository list -n <acr> -o table

# Show tags
az acr repository show-tags -n <acr> --repository <repo> --orderby time_desc
```

### Best practices

1. Use -o table for readable output.
2. Use -o json for parsing with jq.
3. Use --query for filtering.
4. Never expose secrets in output.
5. Verify subscription before operations.

## Output template

Return exactly this structure:

```markdown
**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the Azure resource, identity, AKS, ACR, Key Vault, or subscription outcome.

### Details
1. Command executed: `<az command>`
2. Subscription context: `<subscription name or ID>`
3. Target resource: `<resource group, resource ID, AKS cluster, ACR, Key Vault, or not applicable>`
4. Results: `<table summary, JSON summary, or operation result>`
5. Warnings or issues: `<RBAC, context, secret-handling, or none>`
6. Next steps: `<next Azure action or none>`

### Validation
- Context check: `<az account show evidence or reason not checked>`
- Command result: `<exit code or observed az output>`
```

## Limits

- Do not use this skill for Terraform IaC.
- Use `azure-terraform-cli` (`skill`) instead when the task is Terraform init, plan, apply, validate, fmt, state, import, module development, provider locks, tfvars, or tfsec scanning.
- Do not use this skill for Azure architecture patterns.
- Use `azure-infrastructure` (`skill`) instead when the task is architecture design, hub-spoke networking, private endpoints, Workload Identity patterns, naming, or tagging strategy.
- Do not use this skill for Kubernetes kubectl commands.
- Use `azure-kubectl-cli` (`skill`) instead when the task is direct Kubernetes resource inspection, logs, rollout status, events, or manifests.
- Do not use this skill for Helm charts.
- Use `azure-helm-cli` (`skill`) instead when the task is chart repositories, values, templates, releases, upgrades, or rollbacks.

## Progressive disclosure and bundled resources

- `scripts/setup-identity-federation.sh`: use when the Azure task requires identity federation setup automation.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-terraform` | `agent` | Planning or implementing Terraform-based Azure infrastructure changes. |
| `open-horizons-security-reviewer` | `agent` | Reviewing Azure RBAC, identity, or secret-handling risk. |
| `open-horizons-sre-investigator` | `agent` | Diagnosing Azure-side operational issues for running services. |
| `open-horizons-azure-readiness` | `agent` | Validating Azure subscription, provider, quota, and resource readiness. |
| `azure-terraform-cli` | `skill` | Managing infrastructure through Terraform rather than direct `az` commands. |
| `azure-kubectl-cli` | `skill` | Inspecting Kubernetes resources after AKS credentials are configured. |
| `azure-infrastructure` | `skill` | Designing Azure architecture patterns before CLI execution. |

## Quality gate

- [ ] `name` is `azure-cli` and matches the parent directory.
- [ ] The active subscription is verified before resource operations.
- [ ] Secret values are not exposed in the response unless the user explicitly requested retrieval and the value is handled safely.
- [ ] `--query` or output mode choices are reported when they materially affect the result.
- [ ] AKS, ACR, and Key Vault commands include the target resource name or resource group when applicable.
- [ ] The bundled script path listed above exists before referring to it.

---
name: azure-cli
description: "Use when running focused Azure CLI operations for Open Horizons cloud resources, including account context, AKS credentials, ACR, Key Vault metadata, resource inventory, provider registration, and RBAC checks; produces commands, results, and safe next steps. DO NOT USE FOR: Terraform IaC (use terraform-cli), Kubernetes operations (use kubectl-cli), or Helm charts (use helm-cli). Triggers include \"check Azure resources\", \"get AKS credentials\", \"register an Azure provider\"."
---

# Azure CLI

This workflow performs focused `az` operations for Azure resource discovery and controlled mutations. It produces verified command output while protecting secrets and keeping Terraform-managed infrastructure under Terraform ownership.

> [!NOTE]
> This skill shells out to the Azure CLI (`az`). Authentication, subscription selection, and RBAC must be verified before use. For GitHub OIDC federation setup, the repository script is `.github/skills/azure-cli/scripts/setup-identity-federation.sh`.

## When to invoke
- "Check which Azure subscription and resource group I am targeting."
- "Get AKS credentials for the Open Horizons cluster."
- "List ACR repositories and image tags."
- "Register the Azure providers needed by the platform."
- "Create an RBAC assignment after I approve the exact scope."

## Prerequisites and context
- Azure CLI installed and authenticated with `az account show` succeeding.
- Target subscription ID and resource group known.
- Appropriate Azure RBAC permissions for the operation.
- Understanding of whether the target resource is Terraform-managed under `terraform/`.
- Explicit approval before provider registration, role assignment, scaling, or resource creation.

## Procedure

### Step 1: Verify account context
```bash
az account show -o table
az account list -o table --query "[].{Name:name, ID:id, State:state}"
az account set --subscription "<subscription-id>"
```

- [ ] Tenant and subscription match the user's target.
- [ ] Environment and resource group are identified.
- [ ] Output does not include secrets.

### Step 2: Inventory resources safely
```bash
az resource list --resource-group <resource-group> -o table
az resource list --resource-group <resource-group> --query "[?type=='Microsoft.ContainerService/managedClusters']" -o table
az provider list --query "[?registrationState!='Registered'].{Namespace:namespace, State:registrationState}" -o table
```

### Step 3: Run focused read operations
```bash
az aks show --resource-group <resource-group> --name <cluster> -o table
az acr repository list --name <acr-name> -o table
az acr repository show-tags --name <acr-name> --repository <repo> --orderby time_desc -o table
az keyvault secret list --vault-name <vault-name> --query "[].{Name:name}" -o table
```

Do not print secret values. Prefer listing names and metadata.

### Step 4: Confirm before mutating Azure state
```text
Azure CLI mutation summary:
- Subscription:
- Resource group or scope:
- Command category: provider registration | RBAC | AKS credentials | scale | create | update
- Resources affected:
Proceed with this Azure CLI mutation? (y/n)
```

> [!IMPORTANT]
> Only proceed with provider registration, role assignment, scaling, resource creation, or other Azure state changes if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the proposed command and stop.

### Step 5: Execute approved mutations and verify
```bash
az provider register --namespace Microsoft.ContainerService
az role assignment create --assignee <principal-id> --role <role-name> --scope <resource-scope>
az aks get-credentials --resource-group <resource-group> --name <cluster> --overwrite-existing
```

- [ ] Verify the result with a read command.
- [ ] Record the exact scope and principal for RBAC changes.
- [ ] Route persistent infrastructure changes back to Terraform when applicable.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Wrong subscription, secret value exposed, or destructive change proposed outside Terraform. |
| High | Broad RBAC scope, public network exposure, or production scaling without approval. |
| Medium | Provider not registered, stale credentials, or incomplete resource inventory. |
| Low | Output formatting, naming, or tagging issues. |

## Limits

- Do not use this skill for: Terraform IaC (use terraform-cli), Kubernetes operations (use kubectl-cli), or Helm charts (use helm-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Not authenticated | Run `az login` or use managed identity, then verify `az account show`. |
| Wrong subscription | Stop, set the intended subscription, and rerun only read commands first. |
| Insufficient permissions | Report the missing role and exact scope needed. |
| Secret value requested | Refuse to print it; provide a safe retrieval or Key Vault reference pattern. |

## Output template

Return exactly this structure:
```markdown
# Azure CLI Operation Report

## Context
- Tenant:
- Subscription:
- Resource group:

## Commands
| Command | Result |
|---|---|

## Findings
| Severity | Finding | Recommendation |
|---|---|---|

## Next Steps
- 
```

## Quality gate
- [ ] Subscription context is verified before every operation.
- [ ] Mutations have explicit user confirmation.
- [ ] Secrets are never printed in output.
- [ ] Terraform-managed resources are not changed imperatively without approval.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.

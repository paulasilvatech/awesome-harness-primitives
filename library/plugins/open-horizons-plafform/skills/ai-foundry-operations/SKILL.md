---
name: ai-foundry-operations
description: "Use when provisioning Azure AI Foundry resources, deploying Azure OpenAI models, configuring RAG with Azure AI Search, testing endpoints, or operating Foundry workspaces; produces commands, status summaries, and cost/safety recommendations. DO NOT USE FOR: general Azure infrastructure (use azure-infrastructure), Terraform IaC authoring (use terraform-cli), or Kubernetes operations (use kubectl-cli). Triggers include \"provision AI Foundry\", \"deploy an Azure OpenAI model\", \"configure RAG in Foundry\"."
---

# AI Foundry Operations

This workflow operates the H3 AI layer for Open Horizons: Azure AI Foundry, Azure OpenAI deployments, model quota checks, RAG dependencies, managed identity access, endpoint testing, and day-2 status reporting. It produces verified CLI commands, resource status, and recommendations without replacing Terraform ownership of infrastructure definitions.

> [!NOTE]
> This skill shells out to the `az` CLI and may use Terraform in `terraform/` for existing H3 modules. Azure CLI must be authenticated, the target subscription must be selected, and current Microsoft Learn documentation should be checked for model names, API versions, quota, and regional availability.

## When to invoke
- "Provision Azure AI Foundry for the dev environment."
- "Deploy an Azure OpenAI model and show me the endpoint."
- "Configure the RAG dependencies for our H3 workloads."
- "Check Foundry model quota, deployments, and token usage."

## Prerequisites and context
- Azure CLI installed and authenticated with `az account show` returning the intended subscription.
- Environment configuration in `terraform/environments/` and the `terraform/modules/ai-foundry/` module present.
- Resource group, location, model deployment name, and capacity target identified.
- Managed identity principal IDs available for application access.
- Approval to create or scale paid Azure resources.

## Procedure

### Step 1: Verify context and quota
```bash
az account show -o table
az provider show --namespace Microsoft.CognitiveServices --query registrationState -o tsv
az cognitiveservices usage list --location <location> -o table
```

- [ ] Subscription and tenant are correct.
- [ ] `Microsoft.CognitiveServices` is registered.
- [ ] Requested model family has regional quota.
- [ ] The target location matches business and latency constraints.

### Step 2: Confirm before provisioning or model deployment
```text
AI Foundry operation summary:
- Subscription:
- Resource group:
- Location:
- Models or RAG resources:
- Estimated paid resources affected:
Proceed with provisioning, scaling, or deployment? (y/n)
```

> [!IMPORTANT]
> Only proceed with provisioning, model deployment, quota-consuming changes, or paid resource creation if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the plan and stop.

### Step 3: Use repository Terraform when changing managed infrastructure
```bash
cd terraform
terraform init
terraform plan -var-file=environments/<env>.tfvars -var="enable_h3=true" -out=h3.tfplan
terraform apply h3.tfplan
```

- [ ] Use `terraform/modules/ai-foundry/` for managed H3 infrastructure.
- [ ] Keep provider versions pinned by `.terraform.lock.hcl`; do not run `terraform init -upgrade`.
- [ ] Capture the plan summary before apply.

### Step 4: Operate Azure OpenAI resources with Azure CLI
```bash
az cognitiveservices account list -o table
az cognitiveservices account deployment list --name <account> --resource-group <rg> -o table
az cognitiveservices account show --name <account> --resource-group <rg> --query properties.endpoint -o tsv
```

- [ ] Deployments have expected model names, versions, and SKU capacity.
- [ ] Endpoint and keys are not printed together in logs.
- [ ] Diagnostic settings and content safety requirements are documented.

### Step 5: Configure managed identity access
```bash
az role assignment create \
  --assignee <principal-id> \
  --role "Cognitive Services User" \
  --scope /subscriptions/<subscription-id>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>
```

- [ ] Use managed identity or workload identity rather than API keys in application code.
- [ ] Scope the role assignment to the specific account where possible.
- [ ] Record the principal, role, and scope in the output.

### Step 6: Validate endpoint behavior safely
```bash
curl -sS -X POST "https://<endpoint>/openai/deployments/<deployment>/chat/completions?api-version=<api-version>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <managed-identity-token>" \
  -d '{"messages":[{"role":"user","content":"Health check"}],"max_tokens":20}'
```

Do not echo API keys. If key-based testing is unavoidable, redact values in all output.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Secrets exposed, public endpoint required for sensitive data, or production model deleted or replaced without rollback. |
| High | No managed identity, no quota/cost guardrail, or deployment uses unapproved model/region. |
| Medium | Missing diagnostic settings, unclear RAG data boundary, or capacity not aligned to expected traffic. |
| Low | Naming, tagging, or documentation gaps. |

## Limits

- Do not use this skill for: general Azure infrastructure (use azure-infrastructure), Terraform IaC authoring (use terraform-cli), or Kubernetes operations (use kubectl-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Provider not registered | Register `Microsoft.CognitiveServices`, wait for completion, then retry discovery. |
| Quota unavailable | Report region and model limits; do not deploy a substitute model without approval. |
| Terraform plan fails | Capture the failing module and variable; do not switch to ad hoc CLI creation unless explicitly approved. |
| Endpoint test fails | Check deployment name, API version, identity role, and network restrictions before changing resources. |

## Output template

Return exactly this structure:
```markdown
# AI Foundry Operation Report

## Scope
- Subscription:
- Resource group:
- Location:

## Actions
| Command | Result | Evidence |
|---|---|---|

## Deployments
| Account | Deployment | Model | Capacity | Endpoint |
|---|---|---|---|---|

## Risks And Recommendations
| Severity | Finding | Recommendation |
|---|---|---|
```

## Quality gate
- [ ] Subscription, resource group, and location are verified before mutation.
- [ ] User confirmation is captured before paid or mutating operations.
- [ ] Secrets and keys are redacted from output.
- [ ] Model names, API versions, and quota statements come from current official sources.
- [ ] Terraform-managed resources remain managed through `terraform/` unless the user approves an exception.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.

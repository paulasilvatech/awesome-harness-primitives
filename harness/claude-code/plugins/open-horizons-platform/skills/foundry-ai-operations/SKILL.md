---
name: foundry-ai-operations
description: >-
  Azure AI Foundry operations provisions workspaces, model deployments, RAG resources, operational
  settings, and resource checks. Use this skill when provisioning AI Foundry, deploying OpenAI
  models, configuring RAG, operating model endpoints, setting up AI workspaces, or checking
  Foundry resources.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/foundry-ai-operations/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Foundry AI Operations

Turn an Azure AI Foundry operations request into provisioning steps, model deployment commands, managed identity configuration, endpoint checks, and operational evidence for the Open Horizons H3 Innovation layer.

## When to invoke

- "Provision Azure AI Foundry resources."
- "Deploy and manage OpenAI models."
- "Configure RAG pipelines with AI Search."
- "Monitor token usage and costs."
- "Test model endpoints."

## Prerequisites and context

- Azure CLI authenticated (`az login`).
- Subscription with AI services quota.
- Terraform H3 modules applied, or manual provisioning approved.
- Project files to consult: `terraform/modules/ai-foundry/` and `scripts/golden-paths/` for checked-in Golden Path scaffolding.

## Procedure

### Provisioning

#### 1. Create AI Foundry Resources (via Terraform)

```bash
# Deploy H3 Innovation layer (includes AI Foundry)
cd terraform
terraform plan -var-file=environments/dev.tfvars -var="enable_h3=true" -out=tfplan
terraform apply tfplan

# Or via bootstrap script
./scripts/platform-bootstrap.sh --horizon h3 --environment dev
```

#### 2. Create Resources (via Azure CLI)

```bash
# Create Cognitive Services account (OpenAI)
az cognitiveservices account create \
  --name "${PROJECT}-${ENV}-openai" \
  --resource-group "${RG_NAME}" \
  --kind OpenAI \
  --sku S0 \
  --location eastus2 \
  --custom-domain "${PROJECT}-${ENV}-openai" \
  --tags environment="${ENV}" project="${PROJECT}"

# Create AI Search service
az search service create \
  --name "${PROJECT}-${ENV}-search" \
  --resource-group "${RG_NAME}" \
  --sku standard \
  --partition-count 1 \
  --replica-count 1

# Create model deployment (GPT-4o)
az cognitiveservices account deployment create \
  --name "${PROJECT}-${ENV}-openai" \
  --resource-group "${RG_NAME}" \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version "2024-05-13" \
  --model-format OpenAI \
  --sku-capacity 30 \
  --sku-name Standard
```

#### 3. Configure Managed Identity Access

```bash
# Assign Cognitive Services User role to AKS identity
az role assignment create \
  --assignee "${AKS_IDENTITY_PRINCIPAL_ID}" \
  --role "Cognitive Services User" \
  --scope "/subscriptions/${SUB_ID}/resourceGroups/${RG_NAME}/providers/Microsoft.CognitiveServices/accounts/${PROJECT}-${ENV}-openai"

# Get endpoint
az cognitiveservices account show \
  --name "${PROJECT}-${ENV}-openai" \
  --resource-group "${RG_NAME}" \
  --query "properties.endpoint" -o tsv
```

### Day-2 Operations

#### Resource Management

```bash
# List AI Foundry workspaces
az ml workspace list -o table

# Show workspace details
az ml workspace show --name <workspace> --resource-group <rg>

# List compute resources
az ml compute list --workspace-name <workspace> --resource-group <rg>
```

#### OpenAI Deployments

```bash
# List Cognitive Services accounts
az cognitiveservices account list -o table

# List deployments
az cognitiveservices account deployment list \
  --name <account> --resource-group <rg> -o table

# Check quota usage
az cognitiveservices usage list --location eastus2 -o table
```

#### Model Testing

```bash
# Test chat completion
curl -X POST "https://<endpoint>.openai.azure.com/openai/deployments/<deployment>/chat/completions?api-version=2024-02-15-preview" \
  -H "Content-Type: application/json" \
  -H "api-key: ${OPENAI_API_KEY}" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'

# Test with managed identity (from AKS pod)
curl -X POST "https://<endpoint>.openai.azure.com/openai/deployments/<deployment>/chat/completions?api-version=2024-02-15-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: ******" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

### Best practices

1. Configure content safety filters on all deployments.
2. Implement rate limiting and retry logic.
3. Use managed identity for authentication (never API keys in code).
4. Monitor token usage and set cost alerts.
5. Enable diagnostic logging for compliance.
6. Use private endpoints for production.
7. Deploy models in LATAM-nearest region with quota.

## Output template

Return exactly this structure:

```markdown
AI Foundry Operations Result

**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the Foundry provisioning, deployment, or operations outcome.

### Details
- Command executed: `command or not run`
- Resource status: workspace, Cognitive Services account, AI Search, deployment, or endpoint state
- Deployment details: model deployment, SKU, region, identity, endpoint, or RAG configuration
- Recommendations: operational next steps, cost controls, logging, or safety filters

### Validation
- Azure context: PASS | FAIL | SKIPPED with subscription, resource group, and evidence
- Command result: PASS | FAIL | SKIPPED with exit code or observed output
- Endpoint or resource check: PASS | FAIL | SKIPPED with endpoint, deployment, or query evidence
```

## Limits

- Do not use this skill for general Azure architecture.
- Use `azure-infrastructure` (`skill`) instead when designing landing zones, networking, identity, naming, tagging, or private connectivity patterns.
- Do not use this skill for Terraform execution.
- Use `terraform-cli` (`skill`) instead when running Terraform plans or applies.
- Do not use this skill for Kubernetes operations.
- Use `kubectl-cli` (`skill`) instead when operating AKS workloads.
- Do not use this skill for agent design patterns.
- Use `foundry-agent-blueprint` (`skill`) instead when mapping an agent design to Foundry primitives.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-deployment-operator` | `agent` | H3 provisioning is part of an approved end-to-end platform deployment. |
| `open-horizons-azure-readiness` | `agent` | Azure-side resources, quotas, provider registration, or portal validation are needed. |
| `foundry-agent-blueprint` | `skill` | The task is designing agent models, connections, tools, memory, evaluation, and tracing. |
| `azure-infrastructure` | `skill` | The task is broader Azure architecture or network and identity design. |
| `terraform-cli` | `skill` | Terraform command execution or state-safe plan handling is required. |

## Quality gate

- [ ] `name` matches the `ai-foundry-operations` directory.
- [ ] The request matches positive Foundry operations triggers.
- [ ] Required Azure context, quota, and H3 prerequisites are stated or checked.
- [ ] Commands preserve their original flags, resource names, model names, API versions, and paths.
- [ ] Managed identity and private endpoint best practices are considered before delivery.
- [ ] The response follows the output template with validation evidence.

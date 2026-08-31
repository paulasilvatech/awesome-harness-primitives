---
name: open-horizons-deploy-orchestration
description: >-
  Coordinates end-to-end Open Horizons platform deployment across prerequisites, Terraform, Kubernetes, GitOps, and verification. Use this skill when planning or executing full platform deployment, dry-run deployment, horizon enablement, deployment sequence, post-deploy verification, or deployment troubleshooting.
---

# Deploy Orchestration

Use deployment intent, environment configuration, and platform state to sequence Open Horizons deployment phases, run the right validation gates, and return phase-by-phase deployment evidence.

## When to invoke

- "Deploy the Open Horizons platform to a new environment."
- "Run a dry-run deployment for dev, staging, or prod."
- "Enable another horizon such as H3 on an existing deployment."
- "Verify the platform after deployment."
- "Troubleshoot a failed deployment sequence."

## Prerequisites and context

- Azure CLI authenticated (`az login`).
- GitHub CLI authenticated (`gh auth login`).
- All tools installed (run `./scripts/validate-prerequisites.sh`).
- Environment `.tfvars` configured.
- `.env` rendered into Kubernetes manifests when templates are used.
- Terraform provider versions remain pinned by `.terraform.lock.hcl`; do not run `terraform init -upgrade` for this workflow.

## Procedure

### Deployment phases

#### Phase 0: Initial Setup (Wizard)
```bash
# Interactive setup — collects org, domain, auth, Azure, AI config
scripts/install-wizard.sh

# This writes .env and optionally renders K8s manifests.
# For GitHub Enterprise Managed Users, select AUTH_PROVIDER=entra and
# GITHUB_IDENTITY_MODE=enterprise-managed-users.
# For CI/CD (non-interactive):
scripts/install-wizard.sh --auto --selection-file .openhorizons-selection.yaml
```

#### Phase 0b: Render K8s Manifests
```bash
# Generate manifests from templates using .env values
scripts/render-k8s.sh

# Dry-run to preview without writing:
scripts/render-k8s.sh --dry-run
```

#### Phase 1: Prerequisites
```bash
./scripts/validate-prerequisites.sh
```

#### Phase 2: Azure Setup
```bash
# Login
az login
az account set --subscription "$AZURE_SUBSCRIPTION_ID"

# Register providers
for provider in Microsoft.ContainerService Microsoft.ContainerRegistry   Microsoft.KeyVault Microsoft.Network Microsoft.ManagedIdentity   Microsoft.Security Microsoft.CognitiveServices Microsoft.Monitor; do
  az provider register --namespace "$provider"
done
```

#### Phase 2: Terraform Backend (first time only)
```bash
./scripts/setup-terraform-backend.sh   --customer-name contoso   --environment dev   --location brazilsouth
```

#### Phase 3: Configuration
```bash
# Copy template and edit
cp terraform/terraform.tfvars.example terraform/environments/dev.tfvars
# Edit with your values

# Set sensitive vars
export TF_VAR_azure_subscription_id="..."
export TF_VAR_azure_tenant_id="..."
export TF_VAR_admin_group_id="..."
export TF_VAR_github_org="..."
export TF_VAR_github_token="..."

# Validate
./scripts/validate-config.sh --environment dev
```

#### Phase 4: Deploy
```bash
cd terraform
# Never use -upgrade: .terraform.lock.hcl holds the pinned, tested provider set.
terraform init

# H1 first. The kubernetes/helm/kubectl providers read module.aks outputs, so a
# single-pass apply on an empty subscription fails at plan time.
terraform plan -var-file=environments/dev.tfvars -out=h1.tfplan
terraform apply h1.tfplan

# H2 modules, once AKS exists
terraform apply -var-file=environments/dev.tfvars   -target=module.argocd -target=module.observability   -target=module.external_secrets -target=module.databases
```

#### Phase 5: Verify
```bash
# Get AKS credentials
az aks get-credentials   --resource-group "$(terraform output -raw resource_group_name)"   --name "$(terraform output -raw aks_cluster_name)"

# Run validation
./scripts/validate-deployment.sh --environment dev
```

#### Phase 6: Post-Deployment
```bash
# Access ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Visit https://localhost:8080

# Access Grafana
kubectl port-forward svc/prometheus-grafana -n observability 3000:80
# Visit http://localhost:3000
```

## Output template

Return exactly this structure:

```markdown
# Deployment orchestration result

**Status:** PASS | FAIL | BLOCKED
**Environment:** dev | staging | prod | other
**Summary:** One sentence describing the deployment outcome.

### Phase results
| Phase | Action | Result | Evidence |
| --- | --- | --- | --- |
| Phase 0 | Initial setup | PASS | Command or file evidence |
| Phase 1 | Prerequisites | PASS | Validator output |
| Phase 4 | Terraform H1 then H2 | PASS | Plan/apply output summary |

### Details
- Commands executed or recommended, in order.
- Configuration files or manifests touched.
- Issues detected and remediation steps.

### Validation evidence
- Prerequisites: PASS | FAIL with command output summary.
- Configuration: PASS | FAIL with command output summary.
- Deployment: PASS | FAIL with command output summary.
```

## Limits

- Do not use this skill for isolated Terraform commands.
- Use `terraform-cli` (`skill`) instead when the task is limited to Terraform init, plan, module work, or state inspection.
- Use `kubectl-cli` (`skill`) instead when the task is limited to Kubernetes read operations or pod inspection.
- Use `helm-cli` (`skill`) instead when the task is limited to Helm package work.
- Use `argocd-cli` (`skill`) instead when the task is limited to ArgoCD-only sync or application management.

## Progressive disclosure and bundled resources

- `references/automated-deployment.md`: automated deployment command variants.
- `references/deployment-modes.md`: environment configuration and deployment mode tables.
- `references/rollback.md`: H3 rollback and complete teardown commands.
- `references/troubleshooting.md`: Terraform, AKS, and ArgoCD troubleshooting commands.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `prerequisites` | `skill` | Tool installation and local access must be checked before deployment. |
| `validation-scripts` | `skill` | Script-based configuration, deployment, naming, or primitive validation is needed. |
| `terraform-cli` | `skill` | Terraform-specific planning, module, or state work is the task. |
| `kubectl-cli` | `skill` | Kubernetes direct inspection or operations are the task. |
| `helm-cli` | `skill` | Helm chart install, upgrade, rollback, or values work is the task. |
| `argocd-cli` | `skill` | GitOps sync or ArgoCD application operations are the task. |
| `open-horizons-deployment-operator` | `agent` | End-to-end deployment orchestration requires an approved owning agent. |
| `open-horizons-sre-investigator` | `agent` | Deployment verification turns into reliability or incident work. |

## Quality gate

- [ ] The selected environment and horizon are explicit.
- [ ] Prerequisite and configuration validation ran or the reason for skipping is recorded.
- [ ] H1 Terraform apply precedes H2 module apply for empty subscriptions.
- [ ] `.terraform.lock.hcl` remains the pinned provider source of truth.
- [ ] Kubernetes manifests are rendered from `.env` when template values changed.
- [ ] Post-deploy validation evidence includes command output summaries.
- [ ] Any rollback or teardown recommendation references the deployment blast radius.

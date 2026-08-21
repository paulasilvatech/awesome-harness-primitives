---
name: deploy-orchestration
description: "Use when orchestrating an end-to-end Open Horizons deployment or dry run across prerequisites, Terraform H1/H2/H3 sequencing, Kubernetes rendering, validation, troubleshooting, resume, and teardown; produces a deployment plan, command log, validation report, and rollback guidance. DO NOT USE FOR: Terraform module authoring (use terraform-cli), Kubernetes read-only operations (use kubectl-cli), or Helm package operations (use helm-cli). Triggers include \"deploy the platform\", \"run deployment dry run\", \"validate deployment\"."
---

# Deploy Orchestration

This workflow orchestrates complete Open Horizons platform deployment and validation. It sequences prerequisites, configuration validation, Terraform deployment, Kubernetes manifest rendering, AKS verification, and post-deploy health checks while enforcing confirmation before any paid or destructive operation.

> [!NOTE]
> This skill shells out to repository scripts, Azure CLI, Terraform, kubectl, and GitHub CLI. Use `scripts/deploy-full.sh` for the supported automation path, and never run `terraform init -upgrade` because `.terraform.lock.hcl` is the tested provider set.

## When to invoke
- "Deploy the Open Horizons platform to dev."
- "Run a dry-run deployment before applying changes."
- "Validate the deployment after Terraform completed."
- "Resume a failed deployment or troubleshoot the deployment sequence."
- "Tear down the dev environment after approval."

## Prerequisites and context
- Required scripts exist: `scripts/validate-prerequisites.sh`, `scripts/validate-config.sh`, `scripts/deploy-full.sh`, `scripts/render-k8s.sh`, and `scripts/validate-deployment.sh`.
- Azure CLI and GitHub CLI are authenticated.
- Terraform environment file exists under `terraform/environments/`.
- User has selected environment: dev, staging, or prod.
- Explicit approval is available before apply, destroy, or paid resource creation.

## Procedure

### Step 1: Validate local prerequisites
```bash
./scripts/validate-prerequisites.sh
az account show -o table
gh auth status
```

- [ ] CLI tools are installed.
- [ ] Azure subscription and GitHub identity are correct.
- [ ] Required environment files are present.

### Step 2: Validate configuration
```bash
./scripts/validate-config.sh --environment <env>
./scripts/render-k8s.sh --dry-run
```

- [ ] `.env`-driven Kubernetes templates render.
- [ ] Terraform variables are complete for the target environment.
- [ ] H1/H2/H3 horizon selection is understood.

### Step 3: Prefer dry run first
```bash
./scripts/deploy-full.sh --environment <env> --dry-run
```

Review planned Azure resources, Kubernetes changes, and horizon scope before applying.

### Step 4: Confirm before apply or destroy
```text
Deployment operation summary:
- Environment:
- Horizon: h1 | h2 | h3 | all
- Operation: apply | resume | destroy
- Expected Azure/Kubernetes changes:
- Validation command:
Proceed with this deployment operation? (y/n)
```

> [!IMPORTANT]
> Only proceed with `scripts/deploy-full.sh` apply, resume, or destroy if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the dry-run results and stop.

### Step 5: Run the supported deployment command
```bash
./scripts/deploy-full.sh --environment <env>
./scripts/deploy-full.sh --environment <env> --horizon h1
./scripts/deploy-full.sh --environment <env> --resume
./scripts/deploy-full.sh --environment <env> --destroy
```

For manual Terraform sequencing, apply H1 before H2 modules because Kubernetes, Helm, and kubectl providers depend on AKS outputs:

```bash
cd terraform
terraform init
terraform plan -var-file=environments/<env>.tfvars -out=h1.tfplan
terraform apply h1.tfplan
terraform apply -var-file=environments/<env>.tfvars \
  -target=module.argocd -target=module.observability \
  -target=module.external_secrets -target=module.databases
```

### Step 6: Validate deployment health
```bash
./scripts/validate-deployment.sh --environment <env>
kubectl get nodes
kubectl get pods -A
```

- [ ] AKS credentials target the deployed cluster.
- [ ] ArgoCD, Backstage, observability, and optional H3 services are healthy for the selected horizon.
- [ ] Failures are routed to the narrow skill: `argocd-cli`, `open-horizons-backstage-deployment`, `database-management`, or `ai-foundry-operations`.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Wrong subscription, unapproved destroy, production outage, or secrets exposed. |
| High | Terraform apply fails after partial infrastructure, AKS unreachable, or H2 applied before H1 outputs exist. |
| Medium | Validation script fails, app health degraded, or manifest rendering incomplete. |
| Low | Documentation, tagging, or post-deploy access gaps. |

## Limits

- Do not use this skill for: Terraform module authoring (use terraform-cli), Kubernetes read-only operations (use kubectl-cli), or Helm package operations (use helm-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Prerequisite validation fails | Install or configure only the missing existing tools; rerun validation. |
| Config validation fails | Fix environment variables or tfvars before deployment. |
| Terraform plan/apply fails | Capture the module, provider, and command; do not run `init -upgrade`. |
| Kubernetes validation fails | Collect namespace, pod status, events, and route to the appropriate operations skill. |
| Destroy requested | Require explicit confirmation and record the environment and subscription. |

## Output template

Return exactly this structure:
```markdown
# Open Horizons Deployment Report

## Scope
- Environment:
- Horizon:
- Subscription:

## Commands
| Step | Command | Result |
|---|---|---|

## Validation
| Check | Result | Evidence |
|---|---|---|

## Risks And Follow-Ups
| Severity | Finding | Owner Skill |
|---|---|---|

## Rollback Or Resume
- Command:
- Preconditions:
```

## Quality gate
- [ ] Prerequisites and configuration validation pass before apply.
- [ ] Dry run is reviewed before paid or mutating deployment.
- [ ] Explicit confirmation is captured before apply, resume, or destroy.
- [ ] Post-deploy validation is run and reported.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.

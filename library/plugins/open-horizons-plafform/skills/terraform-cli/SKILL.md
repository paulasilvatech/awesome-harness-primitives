---
name: terraform-cli
description: 'Use when running or preparing Terraform operations for Azure infrastructure: fmt, validate, init, plan, apply, destroy, state inspection, module checks, and IaC security review. Produces formatted commands, plan summaries, risk classification, and approval-gated apply or destroy steps. DO NOT USE FOR: Azure CLI operations (use azure-cli), Kubernetes operations (use kubectl-cli), Helm charts (use helm-cli). Triggers include "run terraform plan", "validate Terraform", "apply this plan", and "inspect Terraform state".'
---

# Terraform CLI

Use this skill to operate Open Horizons Terraform under `terraform/`, including modules in `terraform/modules/` and environment variables in `terraform/environments/dev.tfvars`. It produces safe command sequences, plan summaries, state inspection guidance, and explicit approval gates for apply or destroy.

> [!NOTE]
> This skill depends on Terraform 1.5 or newer, Azure authentication through `az` or workload identity, access to the configured backend, and environment-specific tfvars under `terraform/environments/`. It does not use an MCP server by default.

## When to invoke

- "Run terraform plan for dev."
- "Validate the Terraform modules."
- "Apply the approved Terraform plan."
- "Inspect Terraform state for the AKS module."
- "Destroy this environment after approval."

## Prerequisites and context

- `terraform version` succeeds.
- `az account show` or the configured workload identity is available.
- `terraform/modules/` and `terraform/environments/dev.tfvars` exist.
- The target environment is known.
- Apply and destroy actions have explicit user approval.

## Procedure

### Step 1: Confirm scope and backend posture

```bash
cd terraform
terraform version
terraform fmt -check -recursive -diff
terraform init -backend=false
terraform validate
```

### Step 2: Create a plan

Use the repo's phased deployment guidance for empty subscriptions: H1 first, then H2 modules.

```bash
cd terraform
terraform init
terraform plan -var-file=environments/dev.tfvars -out=h1.tfplan
terraform show h1.tfplan
```

### Step 3: Inspect state read-only when needed

```bash
cd terraform
terraform state list
terraform state show '<resource-address>'
```

### Step 4: Classify Terraform risk

| Risk | Meaning |
| --- | --- |
| High | Destroy actions, replacement of AKS/network/database resources, backend changes, or production apply. |
| Medium | Adds or updates Azure resources, RBAC, Key Vault, networking, or Kubernetes/Helm providers. |
| Low | `fmt`, `validate`, `plan`, `show`, or read-only state inspection. |

### Step 5: User confirmation gate

```text
Terraform action: <apply|destroy>
Working directory: terraform/
Environment file: terraform/environments/dev.tfvars
Plan file: <planfile>
Risk: <High|Medium|Low>
Proceed with Terraform mutation? (y/n)
```

> [!IMPORTANT]
> Only run `terraform apply` or `terraform destroy` after an explicit affirmative response and a saved plan review. On a negative, ambiguous, or missing response, do not mutate infrastructure; output the plan summary and stop.

### Step 6: Execute approved apply

```bash
cd terraform
terraform apply h1.tfplan
```

For H2 module apply after H1 outputs exist:

```bash
cd terraform
terraform apply -var-file=environments/dev.tfvars   -target=module.argocd   -target=module.observability   -target=module.external_secrets   -target=module.databases
```

### Step 7: Verify with repository validation scripts

```bash
./scripts/validate-config.sh --environment dev
./scripts/validate-deployment.sh --environment dev
```

## Limits

- Do not use this skill for: Azure CLI operations (use azure-cli), Kubernetes operations (use kubectl-cli), Helm charts (use helm-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| `terraform init` fails | Report backend or provider error and stop before planning. |
| Validation fails | Report file and diagnostic; do not plan until fixed. |
| Plan includes unexpected destroy | Reclassify High risk and require explicit approval. |
| Provider needs AKS outputs on empty subscription | Use phased H1 then H2 apply as documented. |
| State lock is held | Report lock ID and owner; do not force-unlock without explicit approval. |

## Output template

Return exactly this structure:

```markdown
## Terraform Operation Report

**Working directory:** `terraform/`
**Environment:** <env>
**Action:** <fmt|validate|plan|apply|destroy|state>
**Risk:** <High|Medium|Low>

### Plan Summary
- Add: <count>
- Change: <count>
- Destroy: <count>

### Commands Run
- `<command>`

### Findings
- <finding>
```

## Quality gate

- [ ] Ran `terraform fmt -check -recursive -diff`.
- [ ] Ran `terraform validate`.
- [ ] Used an existing tfvars file under `terraform/environments/`.
- [ ] Reviewed a saved plan before mutation.
- [ ] Received explicit approval before apply or destroy.
- [ ] Ran relevant validation scripts after approved apply.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.

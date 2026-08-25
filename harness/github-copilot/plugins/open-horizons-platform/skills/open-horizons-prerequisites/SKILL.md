---
name: open-horizons-prerequisites
description: >-
  Validates and sets up local CLI tools and access needed before Open Horizons deployment. Use this skill when checking required tool availability, verifying minimum versions, preparing Azure login readiness, validating CI/CD runner prerequisites, or producing a prerequisite checklist.
---

# Open Horizons Prerequisites

Use the deployment target and local or CI runner context to verify required Open Horizons tools, versions, shell access, and setup commands before deployment work begins.

## When to invoke

- "Check prerequisites before deployment."
- "Validate that my local machine has the required CLI tools."
- "Prepare a CI/CD runner prerequisite checklist."
- "Find missing tools before running deploy-full.sh."
- "Verify Azure, Terraform, Kubernetes, Helm, GitHub, and ArgoCD CLI readiness."

## Prerequisites and context

- Bash shell.
- Access to download tools if missing.

## Criteria

### Required CLI tools

| Tool | Minimum Version | Purpose |
|------|-----------------|---------|
| az | 2.50.0 | Azure CLI |
| terraform | 1.5.0 | Infrastructure as Code |
| kubectl | 1.28.0 | Kubernetes CLI |
| helm | 3.12.0 | Kubernetes package manager |
| gh | 2.30.0 | GitHub CLI |
| argocd | 2.8.0 | ArgoCD CLI |
| jq | 1.6 | JSON processor |
| yq | 4.0.0 | YAML processor |

### Validation script

```bash
#!/bin/bash
set -euo pipefail

# Check required tools
TOOLS=("az" "terraform" "kubectl" "helm" "gh" "argocd" "jq" "yq")
MISSING=()

for tool in "${TOOLS[@]}"; do
  if ! command -v "$tool" &> /dev/null; then
    MISSING+=("$tool")
  fi
done

if [ ${#MISSING[@]} -ne 0 ]; then
  echo "Missing tools: ${MISSING[*]}"
  exit 1
fi

echo "All prerequisites satisfied"
```

### Installation commands

#### macOS (Homebrew)
```bash
brew install azure-cli terraform kubectl helm gh argocd jq yq
```

#### Ubuntu/Debian
```bash
# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### Best practices

1. Run prerequisite check before every deployment
2. Pin tool versions in CI/CD
3. Document version requirements
4. Use version managers (asdf, mise)
5. Include prerequisite check in pre-commit hooks

## Output template

Return exactly this structure:

```markdown
# Prerequisite validation result

**Status:** PASS | FAIL | BLOCKED
**Environment:** local | CI/CD | unknown
**Summary:** One sentence describing prerequisite readiness.

### Tool/version matrix
| Tool | Required | Found | Result | Evidence |
| --- | --- | --- | --- | --- |
| az | 2.50.0 | version or missing | PASS | command output summary |
| terraform | 1.5.0 | version or missing | PASS | command output summary |

### Missing tools
- Tool name: installation command or remediation.

### Validation evidence
- Script or command executed: exact command.
- Result: PASS | FAIL | BLOCKED with output summary.
```

## Limits

- Do not use this skill for full deployment orchestration.
- Use `deploy-orchestration` (`skill`) instead when the task includes deployment phases, Terraform apply sequencing, or post-deploy verification.
- Use `terraform-cli` (`skill`) instead when the task is Terraform operations beyond checking `terraform` availability.
- Use `kubectl-cli` (`skill`) instead when the task is Kubernetes operations beyond checking `kubectl` availability.
- Use `validation-scripts` (`skill`) instead when the task is post-deploy validation or repository validator execution.

## Progressive disclosure and bundled resources

- `scripts/validate-prerequisites.sh`: general prerequisites validator.
- `scripts/validate-cli-prerequisites.sh`: CLI prerequisites validator.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `deploy-orchestration` | `skill` | Prerequisite checks are part of a full deployment sequence. |
| `validation-scripts` | `skill` | Repository validation scripts need to be run or interpreted. |
| `terraform-cli` | `skill` | Terraform command behavior, state, or module validation is needed. |
| `kubectl-cli` | `skill` | Kubernetes command behavior or cluster access needs validation. |
| `helm-cli` | `skill` | Helm command behavior or chart operations need validation. |
| `argocd-cli` | `skill` | ArgoCD command behavior or GitOps access needs validation. |
| `open-horizons-deployment-operator` | `agent` | An approved deployment owner should coordinate prerequisite gates. |

## Quality gate

- [ ] Every required CLI tool is checked for presence.
- [ ] Minimum versions are compared against the required tool matrix.
- [ ] Missing tools include installation guidance for the detected platform when available.
- [ ] The result distinguishes local and CI/CD prerequisite context.
- [ ] Sensitive login state or credentials are not printed.
- [ ] Bundled validator paths exist before they are referenced.

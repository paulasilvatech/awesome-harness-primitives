# Open Horizons Agent Guide

Open Horizons is an open-source Agentic DevOps Platform on Azure AKS. It serves a Developer IDP and an Agent IDP through one Backstage portal, with Terraform-managed Azure infrastructure, Kubernetes workloads, GitOps, observability, and Copilot customization primitives.

> [!IMPORTANT]
> This file is the tool-agnostic source of truth for coding agents. Copilot-specific loading details live in [.github/copilot-instructions.md](.github/copilot-instructions.md), and the `.github/` primitive integration map lives in [.github/README.md](.github/README.md).

## How to use this file

- Treat this as a README for agents: use it to become productive quickly before searching broadly.
- Prefer the commands and layout below unless you verify they are incomplete or stale.
- Keep changes surgical, validate with the smallest relevant existing command, and do not commit unless explicitly asked.
- Follow scoped standards in `.github/instructions/*.instructions.md` when editing matching files.

## Project architecture

```text
L5 Agentic Execution   -> backstage/server/agent-api*/ + middleware/ + .github/agents/
L4 Intent Engineering  -> golden-paths/common/templates/ + .github/prompts/ + model-routing convention
L3 Context Engineering -> mcp-servers/ + memory/ + .github/skills/ + CODEMAP.md
L2 Platform Engineering-> backstage/ + argocd/ + policies/ + golden-paths/ + grafana/
L1 Cloud/Infrastructure-> terraform/modules/ + backstage/k8s/
```

Adoption stages:

- H1 Foundation: AKS, networking, security, databases.
- H2 Enhancement: ArgoCD, Backstage, observability, Golden Paths.
- H3 Innovation: AI Chat, AI Impact, agent capabilities.

## High-value paths

| Area | Path |
| --- | --- |
| Backstage app | `backstage/` |
| Backstage Kubernetes manifests | `backstage/k8s/` |
| AI Chat plugin | `backstage/plugins/ai-chat/` |
| Agent APIs | `backstage/server/agent-api*/` |
| Foundry agents gateway | `foundry/agents-service/` |
| Foundry Kubernetes manifests | `foundry/k8s/` |
| Terraform root | `terraform/` |
| Terraform modules | `terraform/modules/` |
| Terraform environments | `terraform/environments/` |
| Helm values | `deploy/helm/` |
| ArgoCD apps | `argocd/` |
| Golden Paths | `golden-paths/` |
| SDD intent templates | `golden-paths/common/templates/` |
| Numbered feature specifications | `specs/` |
| OPA policies | `policies/kubernetes/`, `policies/terraform/` |
| Grafana dashboards | `grafana/dashboards/` |
| MCP server tools | `mcp-servers/src/tools/` |
| Copilot primitives | `.github/agents/`, `.github/skills/`, `.github/instructions/`, `.github/prompts/` |
| Primitive validator | `.github/skills/validation-scripts/scripts/validate-agents.py` |
| Program skeleton | `CODEMAP.md` |

## Verified safe commands

These commands were checked in this workspace. Environment-sensitive validators may return non-zero until local `.env`, Terraform variables, or target resources are configured.

| Purpose | Command | Current result |
| --- | --- | --- |
| Check CLI prerequisites | `./scripts/validate-prerequisites.sh` | Passed. |
| Check dev configuration | `./scripts/validate-config.sh --environment dev` | Ran; reported missing sensitive `TF_VAR_*` values and no `.env`. |
| Check deployed dev platform | `./scripts/validate-deployment.sh --environment dev --phase all` | Passed with warnings for optional or absent resources. |
| Render Kubernetes templates | `./scripts/render-k8s.sh --dry-run` | Ran; requires `.env` first. |
| Validate Copilot primitives | `python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict` | Passed; listed portability warnings for VS Code-only `handoffs`. |
| Validate numbered SDD specifications | `python3 scripts/validate-specs.py --strict` | Validates frontmatter, EARS, traceability, contracts, tasks, tests, and links. |
| Exercise deployment dry run | `./scripts/deploy-full.sh --environment dev --dry-run --skip-prerequisites` | Ran through Terraform init and validate; plan stopped on missing tenant variables. |

Use `--help` on the scripts above for exact options when changing a workflow.

## Deployment and Terraform ordering

> [!WARNING]
> The commands in this section can create, modify, or destroy Azure infrastructure. Treat them as operational runbooks, not routine validation. Do not run `terraform apply`, `--destroy`, or non-dry-run deployment commands without explicit task scope and environment approval.

Preferred orchestrated dry run:

```bash
./scripts/deploy-full.sh --environment dev --dry-run --skip-prerequisites
```

Full orchestrated deployment, when explicitly approved:

```bash
./scripts/deploy-full.sh --environment dev
```

Manual Terraform deployment must keep the checked-in provider lock file and apply H1 before H2. Do not use `terraform init -upgrade` unless the task is specifically to refresh providers.

```bash
cd terraform
terraform init
terraform plan -var-file=environments/dev.tfvars -out=h1.tfplan
terraform apply h1.tfplan
terraform apply -var-file=environments/dev.tfvars \
  -target=module.argocd -target=module.observability \
  -target=module.external_secrets -target=module.databases
```

The Kubernetes, Helm, and kubectl providers are configured from `module.aks` outputs. A single-pass `terraform apply` on an empty subscription fails at plan time.

## Conventions and gotchas

- Use Workload Identity or Managed Identity for Azure access; never introduce service principal secrets.
- Store secrets in Azure Key Vault or existing secret-management flows; never commit credentials.
- Prefer private endpoints for Azure PaaS services and least-privilege RBAC everywhere.
- Use explicit image tags such as `v7.2.6`; never use `:latest` in deployment manifests.
- Kubernetes names and file names use kebab-case; Terraform variables and resources use snake_case.
- Kubernetes manifests should use Kustomize overlays, standard `app.kubernetes.io/*` labels, resource requests and limits, probes, non-root containers, and network policies.
- Terraform modules should pin provider versions, use reusable modules, tag resources, and protect PaaS services with private endpoints.
- Python APIs use Python 3.11+, FastAPI, Pydantic, structlog, and PEP 8.
- Shell scripts should use bash strict mode, usage text, input validation, and meaningful variable names.
- Nothing CLI-facing may depend on `.github/prompts/*.prompt.md`; prompt files are VS Code-only. Use a skill for CLI-portable reusable workflows.
- Agent `tools` lists may deliberately combine VS Code tool sets with Copilot CLI tokens; see [.github/README.md](.github/README.md) before removing entries that look redundant.
- Repo-root `.copilot/` is not read by the supported surfaces in this repository.

## Copilot primitive validation

Run the primitive validator after editing agents, skills, instructions, prompts, hooks, issue forms, or their templates:

```bash
python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict
```

For the integration model, source contracts, and precedence rules, see [.github/README.md](.github/README.md), [.github/docs/COPILOT-HARNESS-SPEC.md](.github/docs/COPILOT-HARNESS-SPEC.md), and [.github/docs/templates/](.github/docs/templates/).

## References used for this guide

- [AGENTS.md](https://agents.md/) describes AGENTS.md as an open, predictable README for agents.
- [GitHub repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) documents repository-wide instructions, path-specific instructions, and nearest `AGENTS.md` precedence for agents.
- [VS Code custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) documents `.github/copilot-instructions.md`, `AGENTS.md`, and `.instructions.md` as agent customization inputs.

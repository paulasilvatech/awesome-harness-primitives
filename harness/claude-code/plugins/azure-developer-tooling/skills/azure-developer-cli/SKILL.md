---
name: azure-developer-cli
description: >-
  Design, create, review, migrate, or troubleshoot Azure Developer CLI azd projects using
  azure.yaml, infra Bicep or Terraform, environments, secrets, hooks, deployment workflows, and
  azd-managed CI/CD. Use this skill when the user asks for azd project structure, Azure Developer
  CLI best practices, azd templates, or azure.yaml guidance.
license: MIT
---

<!-- Generated from harness/github-copilot/plugins/azure-developer-tooling/skills/azure-developer-cli/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Developer CLI best practices

Produce maintainable, secure, environment-aware `azd` projects by reading the repository manifest first, preserving the chosen IaC provider, and validating only the checks that apply.

## When to invoke

- "Review this azd project."
- "Create or fix azure.yaml for this app."
- "How should this Azure Developer CLI template be structured?"
- "Troubleshoot azd provision, deploy, or pipeline config."
- "Migrate this app to an azd template with Bicep or Terraform."

## Prerequisites and context

- Read `azure.yaml` before inferring services, paths, IaC provider, or deployment behavior.
- Find the configured `infra.path`, source projects, deployment scripts, `.gitignore`, and pipeline definitions before editing.
- Identify whether the task is create, migrate, review, deploy, or troubleshoot.
- Identify the active environment only when an environment-specific operation is required.
- Read bundled references on demand: `references/project-structure.md`, `references/iac-and-environments.md`, `references/security-cicd-operations.md`, and `references/official-docs.md`.

## Safety guardrails

| Guardrail | Rule |
| --- | --- |
| Local state | Never commit `.azure`, environment `.env` files, local Terraform state, generated deployment artifacts, or deployment outputs containing secrets. |
| Secrets | Never put literal secrets in `azure.yaml`, IaC parameter files, hooks, source control, logged command arguments, or IaC outputs. |
| Identity | Prefer managed identities, RBAC, Key Vault references, and `azd env set-secret`. |
| Cloud changes | Before resource-changing or cloud-changing commands, confirm environment, subscription, tenant, region, and expected scope. |
| User approval | Treat explicit deploy, provision, destroy, or pipeline requests as approval for that named action; otherwise ask before `azd up`, `azd provision`, `azd deploy`, `azd down`, or `azd pipeline config`. |
| Architecture | Do not replace Bicep with Terraform, Terraform with Bicep, or a hosting service unless the user asks. |
| Ownership | Preserve resources and state owned outside the current `azd` project. |

## Project defaults

| Concern | Preferred default |
| --- | --- |
| Project manifest | One `azure.yaml` at the repository root. |
| Application code | `src/<service-name>` per independently deployable service. |
| Infrastructure | `infra` with a thin entry point and reusable modules. |
| IaC provider | Bicep unless the repository or user chooses Terraform. |
| Deployment environments | Separate named environments for dev, test, staging, and production. |
| Local AZD state | `.azure/<environment-name>` excluded from source control. |
| Shared environment state | AZD remote environments backed by Azure Blob Storage. |
| Secrets | Managed identity/RBAC first, then Key Vault references. |
| Automation scripts | Short, idempotent scripts under `scripts/azd`. |
| CI authentication | Workload identity federation/OIDC where supported. |
| Routine development | `azd up` for simple workflows; separate phases for controlled workflows. |

## Modeling rules

| Area | Required practice |
| --- | --- |
| Services | Define one `services` entry for each independently deployable component; keep service keys stable; map each service to actual `project`, `language`, and `host`. |
| Shared infrastructure | Keep shared infrastructure in IaC rather than inventing a fake deployable service. |
| Dependencies | Declare dependencies with supported `azure.yaml` fields instead of relying on file order. |
| Bicep/Terraform entry | Keep `main.bicep` or `main.tf` as the orchestration entry point. |
| Modules | Split reusable or independently understandable infrastructure into modules. |
| Parameters | Parameterize environment-specific values; do not fork the IaC tree per environment. |
| Outputs | Output only stable, nonsecret values needed by deployment or application configuration. |
| Naming and tags | Use deterministic naming and tags that include project and environment. |
| Permissions | Add role assignments to identities rather than distributing service keys. |
| Layers | Use infrastructure layers only for separate scopes or lifecycle dependencies. |

For environments, use predictable names such as `<project>-dev` for shared environments and `<alias>-dev` for personal environments. Use `azd env set`, `azd env unset`, `azd env set-secret`, `azd env refresh`, `-e`, and `--environment` rather than hand-editing `.env` files or relying on implicit context.

## Hooks and CI/CD

Prefer declarative IaC and native service configuration over hooks. Use root hooks for project-wide behavior, service hooks for service-specific behavior, and versioned scripts under `scripts/azd` for nontrivial logic. Set `shell` explicitly, provide `windows` and `posix` variants when necessary, keep hooks idempotent and noninteractive in CI, fail on errors unless intentionally nonblocking, and test with `azd hooks run <hook-name>`.

For CI/CD, keep the pipeline definition with the template, review generated changes from `azd pipeline config`, use short-lived federated credentials, run tests and IaC validation before provisioning, use explicit environments and `--no-prompt`, add production approval gates, and configure protected remote state before Terraform pipeline setup.

## Validation commands

Run only checks applicable to the repository:

```text
Application: existing formatter, linter, type-check, build, and tests
Bicep:      az bicep build --file infra/main.bicep
Terraform:  terraform fmt -check -recursive
            terraform init -backend=false
            terraform validate
AZD hooks:  azd hooks run <hook-name>
Packaging:  azd package
```

For a Bicep what-if or Terraform plan, choose the correct deployment scope and environment because the command can authenticate to Azure or read remote state.

## Progressive disclosure and bundled resources

- `references/project-structure.md`: repository layout and `azure.yaml` guidance.
- `references/iac-and-environments.md`: Bicep, Terraform, parameters, outputs, layers, and environments.
- `references/security-cicd-operations.md`: secrets, hooks, CI/CD, deployment, and troubleshooting.
- `references/official-docs.md`: current Microsoft product documentation links.
- `examples/azure.yaml`: example manifest shape.

## Output template

```markdown
## Azure Developer CLI result — <project or task>

**Status:** changed | reviewed | blocked
**IaC provider:** Bicep | Terraform | unknown
**Environment assumptions:** <environment, subscription, tenant, region, or none>

| Area | Finding or change | Evidence | Follow-up |
| --- | --- | --- | --- |
| azure.yaml | <service/path/provider result> | `<file/path>` | <next action> |
| infra | <Bicep/Terraform result> | `<file/path>` | <next action> |
| security | <secret/state/identity result> | `<evidence>` | <next action> |
| validation | <command> | pass | fail | not run | <why> |

**Cloud-changing commands not run:** <azd up/provision/deploy/down/pipeline config or none>
**Preview or beta features:** <feature or none>
```

## Quality gate

- [ ] `azure.yaml` was read before service, provider, or path conclusions were made.
- [ ] `azure.yaml` paths exist and service settings match source projects.
- [ ] The IaC entry point and provider agree with `azure.yaml`.
- [ ] Required deployment outputs match variables consumed by services, hooks, and pipelines.
- [ ] `.gitignore` excludes `.azure`, secrets, local state, and generated artifacts.
- [ ] No secret appears in tracked content or command output.
- [ ] Applicable Bicep, Terraform, hook, package, application, or pipeline checks were run or explicitly deferred.
- [ ] Documentation explains prerequisites, environment creation, deployment, verification, and cleanup when this skill changes template behavior.

---
name: "ado-setup"
description: "Configure Azure DevOps PAT, repository discovery, pipeline visibility, boards integration, and Copilot Standalone guidance for Open Horizons Backstage."
argument-hint: "ado_org_url=https://dev.azure.com/contoso ado_project=my-project components=PAT,repos,pipelines,boards environment=dev"
agent: "ado-integration"
tools: ['read', 'search']
---

# /ado-setup

## Objective
Configure the Azure DevOps side of Open Horizons portal integration so Backstage can discover Azure Repos catalog entities, surface Azure Pipelines and Azure Boards metadata, and store required credentials safely without exposing secret values.

## When to Invoke
Invoke this after the target Azure DevOps organization and project exist, and before Backstage catalog or hybrid GitHub plus Azure DevOps scenarios are validated.

## Preconditions
- The Azure DevOps organization URL `${input:ado_org_url:https://dev.azure.com/contoso}` is reachable by the team.
- The Azure DevOps project `${input:ado_project:project name}` exists or the team can confirm it must be created outside this prompt.
- The target Open Horizons environment `${input:environment:dev, staging, or prod}` maps to `.env.example` conventions or an existing `terraform/environments/` configuration path.
- Secret values are available to an authorized human, but must not be pasted into chat or committed to files.

## Inputs the Team Must Provide
- `ado_org_url`: Azure DevOps organization URL, for example `https://dev.azure.com/contoso`.
- `ado_project`: Azure DevOps project name used by catalog discovery and pipeline annotations.
- `components`: Comma-separated list from `PAT`, `repos`, `pipelines`, and `boards`.
- `environment`: Open Horizons environment name such as `dev`, `staging`, or `prod`.

## What I Will Do
- Inspect existing Backstage, Golden Path, and configuration files before suggesting changes.
- Define least-privilege PAT scopes and Key Vault or Kubernetes secret references without printing token values.
- Map Azure DevOps catalog provider settings and entity annotations needed by Backstage.
- Provide validation commands using installed project conventions and safe read-only checks where possible.
- Redirect GitHub-only integration work to the `hybrid-setup` prompt or the GitHub integration specialist instead of mixing scopes.

## What I Will NOT Do
- I will not create, display, store, or commit an Azure DevOps PAT value.
- I will not delete Azure DevOps repositories, pipelines, boards, service connections, or work items.
- I will not configure GitHub-only features; use the `hybrid-setup` prompt for coexistence or the GitHub integration agent for GitHub-specific setup.
- I will not change Terraform infrastructure or deploy Backstage; use the `terraform` prompt, the `azure-infra` prompt, the `backstage` prompt, or the `deploy-platform` prompt for those tasks.

## Output Format
Chat response only. Do not create or modify workspace files from this prompt.

Return an Azure DevOps integration plan and validation checklist in this shape:

````markdown
# Azure DevOps Integration Plan

| Area | Requested | Configuration Target | Validation | Status |
| --- | --- | --- | --- | --- |
| PAT | yes/no | Key Vault or secret reference | command or portal check | Pending |
| Repos | yes/no | catalog provider and annotations | catalog ingestion check | Pending |
| Pipelines | yes/no | `dev.azure.com/build-definition` | pipeline visibility check | Pending |
| Boards | yes/no | work item integration settings | board visibility check | Pending |

## Secret Handling
- Token value: not displayed
- Storage target: `<Key Vault or Kubernetes secret reference>`

## Next Commands
```bash
az devops configure --defaults organization=<org-url> project=<project>
```
````

## Definition of Done
- [ ] Requested components are listed with explicit configuration targets.
- [ ] PAT scopes are minimized and secret values are not exposed.
- [ ] Catalog provider and entity annotation guidance matches the requested Azure DevOps project.
- [ ] Validation commands or portal checks are provided for each requested component.
- [ ] Any GitHub or Backstage deployment work is redirected to the correct prompt or agent.

## Prompt Body
You are the `@ado-integration` agent. Use your Azure DevOps integration expertise, but keep this prompt focused on repository discovery, pipeline visibility, boards integration, and secure PAT handling.

**Step 1 - Establish scope.** Confirm `${input:components:PAT, repos, pipelines, boards}` and `${input:environment:dev, staging, or prod}`. If the request is GitHub-only, stop and redirect to the GitHub integration workflow. If it is a mixed GitHub plus ADO migration, recommend the `hybrid-setup` prompt.

**Step 2 - Inspect repository configuration.** Read relevant Backstage and Golden Path configuration before editing. Prefer existing files under `backstage/`, `golden-paths/`, `.env.example`, and `terraform/environments/` when identifying integration points.

**Step 3 - Define secure credentials.** Specify the minimum PAT scopes and the destination secret reference. Do not ask the user to paste the PAT value. Do not write secret values to code, Markdown, logs, or shell history.

**Step 4 - Configure only requested components.** For repository discovery, provide provider settings and catalog annotations. For pipelines, provide `dev.azure.com/build-definition` guidance. For boards, provide the required metadata and validation path.

**Step 5 - Validate and hand off.** Provide safe checks, summarize remaining manual actions, and hand off Backstage deployment to the `backstage` prompt or full orchestration to the `deploy-platform` prompt when platform changes are ready.

## Invocation Example
```text
/ado-setup ado_org_url=https://dev.azure.com/contoso ado_project=platform components=PAT,repos,pipelines,boards environment=dev
```

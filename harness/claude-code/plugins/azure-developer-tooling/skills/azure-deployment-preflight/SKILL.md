---
name: azure-deployment-preflight
description: >-
  Validate Azure Bicep deployments before execution with syntax checks, azd preview, Azure CLI
  what-if, validation-level fallback, permission checks, and a preflight report. Use this skill
  when the user asks before azd up, azd provision, az deployment, Bicep deployment, infrastructure
  review, permission verification, or what-if change preview.
---

<!-- Generated from harness/github-copilot/plugins/azure-developer-tooling/skills/azure-deployment-preflight/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure deployment preflight

Validate Bicep infrastructure before deployment by detecting the workflow, running syntax and preview commands, categorizing what-if changes, and writing a `preflight-report.md` with actionable issues.

## When to invoke

- "Validate my Bicep deployment before I run it."
- "Preview what azd provision will change."
- "Run Azure what-if for this template."
- "Check whether I have permission to deploy this infrastructure."
- "Prepare for azd up or az deployment."

## Prerequisites and context

| Tool or value | Required for | How to check or obtain |
| --- | --- | --- |
| `az` | Standalone Azure CLI what-if | `az --version`; `az account show` for subscription. |
| `azd` | Projects with `azure.yaml` | `azd version`; `azd env list` for environments. |
| `bicep` | Local syntax validation | `bicep --version`; fallback to Azure validation if absent. |
| Resource group | `az deployment group what-if` | Ask user or check existing `.azure/` config. |
| Subscription | All deployments | `az account show` or ask user. |
| Location | `sub`, `mg`, or `tenant` scope | Ask user or use default from config. |
| Environment | `azd` projects | `azd env list` or user input. |

## Procedure

1. Detect project type: if `azure.yaml` exists, use the `azd` workflow; otherwise use the Azure CLI workflow.
2. Locate `.bicep` files. For `azd`, check `infra/` before the project root. For standalone deployments, use the user's file or search `infra/`, `deploy/`, and the root.
3. Match parameter files in this order: `<filename>.bicepparam`, `<filename>.parameters.json`, `parameters.json`, then `parameters/<env>.json` in the same area.
4. Run syntax validation for each Bicep file: `bicep build <bicep-file> --stdout`. Capture line and column errors, warnings, and build status. If `bicep` is not installed, note it and continue.
5. Run the deployment preview. Continue after failures and capture every issue.
6. Parse what-if change symbols and property changes.
7. Write `preflight-report.md` in the project root using `references/REPORT-TEMPLATE.md`.

## Preview commands

| Workflow or scope | Command |
| --- | --- |
| `azd` default environment | `azd provision --preview` |
| `azd` named environment | `azd provision --preview --environment <env-name>` |
| `resourceGroup` target scope | `az deployment group what-if --resource-group <rg-name> --template-file <bicep-file> --parameters <param-file> --validation-level Provider` |
| `subscription` target scope | `az deployment sub what-if --location <location> --template-file <bicep-file> --parameters <param-file> --validation-level Provider` |
| `managementGroup` target scope | `az deployment mg what-if --location <location> --management-group-id <mg-id> --template-file <bicep-file> --parameters <param-file> --validation-level Provider` |
| `tenant` target scope | `az deployment tenant what-if --location <location> --template-file <bicep-file> --parameters <param-file> --validation-level Provider` |
| RBAC fallback | Retry with `--validation-level ProviderNoRbac` and state that full permission validation did not run. |

## What-if interpretation

| Change type | Symbol | Meaning | Report detail |
| --- | --- | --- | --- |
| Create | `+` | New resource will be created | Resource type, name, location. |
| Delete | `-` | Existing resource will be deleted | Mark as high risk unless intentional. |
| Modify | `~` | Properties will change | Include property names and before/after values when available. |
| NoChange | `=` | Resource unchanged | Count only unless the user asked for full inventory. |
| Ignore | `*` | Resource not analyzed because limits were reached | Warn that the preview is incomplete. |
| Deploy | `!` | Resource will be deployed but changes are unknown | Require manual inspection. |

## Error handling

Continue validation even when errors occur; the report should contain all failures and warnings.

| Error type | Action |
| --- | --- |
| Not logged in | Note in report; suggest `az login` or `azd auth login`. |
| Permission denied | Retry what-if with `ProviderNoRbac`; note missing RBAC validation. |
| Bicep syntax error | Include every error; continue to other files. |
| Tool not installed | Note in report and skip only that validation step. |
| Resource group not found | Note in report; suggest creating it or selecting the correct group. |

## Progressive disclosure and bundled resources

- `references/VALIDATION-COMMANDS.md`: detailed command variants and flags.
- `references/REPORT-TEMPLATE.md`: required `preflight-report.md` structure.
- `references/ERROR-HANDLING.md`: detailed remediation guidance.

## Command and scope vocabulary

Preserve Azure deployment terminology exactly when reporting: `azd up`, `azd provision`, `az deployment`, `az deployment group`, `az deployment sub what-if`, `az deployment mg what-if`, `az deployment tenant what-if`, `--validation-level`, `--validation-level Provider`, `targetScope`, `Sub/MG/Tenant`, `JSON`, `line/column`, `success/failure`, and `create/modify/delete/unchanged`.

Use concrete examples when they match the repository: `infra/main.bicep`, `infra/main.bicepparam`, and `bicep build infra/main.bicep --stdout`.

## Output template

```markdown
## Azure deployment preflight

**Status:** pass | issues found | blocked
**Report:** `preflight-report.md`
**Workflow:** azd | az cli
**Target scope:** resourceGroup | subscription | managementGroup | tenant | unknown

### Tools executed
| Tool | Command | Result |
| --- | --- | --- |
| Bicep | `bicep build <bicep-file> --stdout` | <pass/fail/skipped> |
| Preview | `<azd provision --preview or az deployment ... what-if>` | <pass/fail> |

### What-if summary
| Symbol | Count | Notes |
| --- | --- | --- |
| `+` | <count> | <created resources> |
| `~` | <count> | <modified resources> |
| `-` | <count> | <deleted resources> |

### Issues
- <severity>: <error, warning, permission gap, or missing input>
```

## Quality gate

- [ ] Project type was detected from `azure.yaml` or absence of it.
- [ ] Bicep files and matching parameter files were located and reported.
- [ ] `bicep build <bicep-file> --stdout` was run or its absence was documented.
- [ ] The correct `azd provision --preview` or `az deployment ... what-if` scope was selected.
- [ ] `--validation-level ProviderNoRbac` fallback was used only after permission failure and was reported.
- [ ] What-if symbols `+`, `-`, `~`, `=`, `*`, and `!` were interpreted correctly.
- [ ] `preflight-report.md` was created in the project root or the blocker is explicit.
- [ ] Referenced bundled resources exist and were used on demand.

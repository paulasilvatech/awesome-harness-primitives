---
name: azure-import-infrastructure-as-code
description: >-
  Imports existing Azure resources into Terraform through read-only discovery, dependency mapping,
  Azure Verified Module selection, source-derived import addresses, and drift-safe plans. Use when
  reverse-engineering a subscription, resource group, or ARM resource ID into maintainable IaC.
argument-hint: "subscription-id=<id> | resource-group-name=<name> | resource-id=<arm-id>"
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/azure-import-infrastructure-as-code/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Import Infrastructure as Code

Convert one Azure discovery scope into reviewed Terraform with zero unintended destruction or updates.

## When to invoke

- Import an Azure resource group or selected ARM resources into Terraform.
- Reverse-engineer deployed Azure infrastructure.
- Map Azure dependencies before IaC adoption.
- Diagnose drift after an attempted import.

## Prerequisites and context

- Azure CLI and Terraform CLI are installed and authenticated for read-only discovery.
- Registry and Azure Verified Modules sources are reachable.
- A reviewed Terraform backend and ownership boundary are known before state mutation.

## Inputs

Parse `$ARGUMENTS` as exactly one discovery scope; reject missing or ambiguous combinations.

| Scope | Discovery command shape |
| --- | --- |
| `subscription-id` | `az resource list --subscription <id> -o json` |
| `resource-group-name` | `az resource list --resource-group <name> -o json` |
| `resource-id` | `az resource show --ids <id-1> <id-2> -o json` |

ARM IDs are cloud identifiers, never local file paths. Do not pass them to file-reading tools.

## Procedure

1. Confirm one scope, subscription context, target Terraform root, state owner, and approval boundary.
2. Discover resources with the narrowest read-only Azure command and preserve sanitized evidence.
3. Map parent/child relations, network and identity dependencies, cross-resource references, and creation order.
4. Select an Azure Verified Module for each resource type and read its README, required inputs,
   child-resource ownership, outputs, providers, and pinned version.
5. If no suitable AVM exists, stop and document the gap; do not silently invent a raw-resource design.
6. Generate providers, modules, variables, outputs, and examples with live non-default properties explicit.
7. Run `terraform init`, then derive import addresses from `.terraform/modules/<key>/main*.tf`;
   never guess nested module, `count`, or `for_each` addresses.
8. After explicit state-mutation approval, import one resource at a time and verify identity.
9. Run format, validate, and plan. The accepted plan has zero destroys and zero unwanted updates.

## Criteria

| Area | Required evidence |
| --- | --- |
| Scope | Exactly one subscription, resource group, or resource-ID set |
| Module | Pinned AVM source and reviewed Required Inputs |
| Address | Derived from downloaded module source after init |
| Drift | Live non-default values represented explicitly |
| Final plan | Zero destroys and zero unintended updates |

## Output template

```markdown
## Azure import result

**Status:** READY | IMPORTED | BLOCKED
**Scope:** <subscription/resource group/resource IDs>
**Terraform root:** <path>

| Resource | AVM module/version | Import address | Import | Plan result |
| --- | --- | --- | --- | --- |

### Drift and gaps
- <unmodeled property, unsupported resource, unwanted action, or none>

### Validation
- `terraform fmt`: <result>
- `terraform validate`: <result>
- `terraform plan`: <0 destroys/updates or blocker>
```

## Limits

- Do not read ARM IDs as files or expose sensitive resource payloads.
- Do not import before backend, state ownership, address, and mutation approval are explicit.
- Do not guess AVM child resources or import addresses.
- Do not accept a plan with destruction or unexplained updates.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-cli` | `skill` | Read-only Azure discovery commands are required. |
| `terraform-cli` | `skill` | Init, import, state inspection, validation, or plan procedure is required. |
| `azure-infrastructure` | `skill` | The imported topology needs an architecture decision. |
| `open-horizons-security-reviewer` | `agent` | Identity, network, or sensitive-data findings need review. |

## Quality gate

- [ ] Exactly one discovery scope is used.
- [ ] Dependencies and live non-default properties are mapped.
- [ ] AVM modules and versions are explicit or a gap blocks progress.
- [ ] Import addresses come from downloaded module source.
- [ ] State mutation had explicit approval.
- [ ] Final plan has zero destroys and zero unintended updates.

## References

- [Azure Verified Modules Terraform index](https://azure.github.io/Azure-Verified-Modules/indexes/terraform/)
- [Terraform import language](https://developer.hashicorp.com/terraform/language/import)

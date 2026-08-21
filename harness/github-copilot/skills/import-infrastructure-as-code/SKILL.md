---
name: import-infrastructure-as-code
description: >-
  Import existing Azure resources into Terraform with Azure CLI discovery, dependency mapping, Azure Verified Modules, exact import addresses, and drift-safe plans. Use when asked to reverse-engineer live Azure infrastructure, generate IaC from subscriptions, resource groups, or ARM resource IDs, map dependencies, use AVM modules, or validate imported Terraform.
---

# Import infrastructure as code

Convert live Azure infrastructure into maintainable Terraform by discovering resources, mapping dependencies, selecting Azure Verified Modules, generating AVM-based HCL, deriving exact import addresses from downloaded module source, and validating that `terraform plan` has no unwanted infrastructure changes.

## When to invoke

- "Import this Azure resource group into Terraform."
- "Generate IaC from these ARM resource IDs."
- "Reverse-engineer my Azure subscription with AVM modules."
- "Map dependencies and import existing Azure infrastructure."
- "Fix Terraform import drift for AVM modules."

## Prerequisites and context

- Azure CLI installed and authenticated with `az login`.
- Access to the target subscription, resource group, or resource IDs.
- Terraform CLI installed with network access to Terraform Registry and AVM index sources.
- At least one scope: `subscription-id`, `resource-group-name`, or `resource-id`.

## Inputs

| Input | Required | Default | Use |
| --- | --- | --- | --- |
| `subscription-id` | Conditional | Active CLI context | Subscription-scope discovery and `az account set --subscription <subscription-id>`. |
| `resource-group-name` | Conditional | None | Resource-group-scope discovery with `az resource list --resource-group <resource-group-name> -o json`. |
| `resource-id` | Conditional | None | Specific-resource discovery with `az resource show --ids <resource-id-1> <resource-id-2> ... -o json`. |

Treat ARM IDs such as `/subscriptions/.../providers/...` as cloud identifiers, never as local paths. Use them only with Azure CLI `--ids` arguments such as `az resource show --ids <resource-id>` unless the user explicitly says they are files.

## Procedure

1. Confirm exactly one usable discovery scope. If scope is missing, ask for `subscription-id`, `resource-group-name`, or `resource-id` and stop.
2. Authenticate and set context only as needed:

   ```bash
   az login
   az account set --subscription <subscription-id>
   az account show --query "{subscriptionId:id, name:name, tenantId:tenantId}" -o json
   ```

3. Discover resources with the smallest scoped command:

   ```bash
   az resource list --subscription <subscription-id> -o json
   az resource list --resource-group <resource-group-name> -o json
   az resource show --ids <resource-id-1> <resource-id-2> ... -o json
   ```

4. Save discovery evidence in a root `docs` folder: `exported-resources.json` with `id`, `type`, `name`, `location`, `tags`, `properties`, dependencies, and references; and `EXPORTED-ARCHITECTURE.MD` with a human-readable architecture overview.
5. Map parent-child relationships, cross-resource references in `properties`, creation order, and examples such as NIC -> Subnet -> VNet before generating HCL.
6. Select AVM modules first, using the latest compatible version. Justify each native `azurerm_*` fallback.
7. Read each selected module README before writing HCL. Then run `terraform init`, inspect `.terraform/modules/<module_key>/`, and derive import addresses from source rather than memory.
8. Generate `providers.tf`, `main.tf`, `variables.tf`, `outputs.tf`, and `terraform.tfvars.example`.
9. Diff every non-zero live property against module defaults in `variables.tf`; explicitly set any live value that differs.
10. Validate with `terraform init`, `terraform fmt -recursive`, `terraform validate`, and `terraform plan`. Do not declare completion until the plan shows 0 destroys and 0 unwanted updates to real resources.

## AVM selection and module reading

Use these AVM sources and preserve point-in-time risk: the CSV links point at the main branch and may change over time.

| Source | URL or pattern |
| --- | --- |
| Terraform Resource Modules | `https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformResourceModules.csv` |
| Terraform Pattern Modules | `https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformPatternModules.csv` |
| Terraform Utility Modules | `https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformUtilityModules.csv` |
| Registry namespace | `https://registry.terraform.io/namespaces/Azure` |
| Registry module | `https://registry.terraform.io/modules/Azure/<module>/azurerm/latest` |
| GitHub module | `https://github.com/Azure/terraform-azurerm-avm-res-{service}-{resource}` |
| README | `https://raw.githubusercontent.com/Azure/terraform-azurerm-avm-res-{service}-{resource}/refs/heads/main/README.md` |
| AVM index | `https://github.com/Azure/Azure-Verified-Modules/tree/main/docs/static/module-indexes` |

Search Terraform Registry for `avm` plus the resource name and filter by the `Partner` tag. If module information is unavailable locally, use `web_fetch` or a suitable MCP method; do not use the no-op `web` token. For each module, extract Required Inputs, Optional Inputs, declared `type`, usage examples, `parent_id` vs `resource_group_name`, inline child-resource maps vs sibling modules, and `variables.tf` defaults.

## AVM module rules

| Module or rule | Required handling |
| --- | --- |
| `avm-res-compute-virtualmachine` | `network_interfaces` is a Required Input; NICs are owned by the VM module. Do not create standalone `avm-res-network-networkinterface` modules beside a VM module. |
| TrustedLaunch | Use top-level `secure_boot_enabled = true` and `vtpm_enabled = true`; `security_type` under `os_disk` is for Confidential VM disk encryption, not TrustedLaunch. |
| VM boot diagnostics | `boot_diagnostics` is a `bool`; use `boot_diagnostics = true` and `boot_diagnostics_storage_account_uri` only when a storage URI is needed. |
| VM extensions | Model extensions in the module `extensions` map; do not create standalone extension resources unless README ownership says so. |
| `avm-res-network-virtualnetwork` | It is AzAPI-backed and uses `parent_id` as the full resource group ID string; do not use `resource_group_name` unless the README says so. |
| All AVM modules | Determine child ownership from Required Inputs, accepted names and types from Optional Inputs and `variables.tf`, and identifier shape from README examples. Do not infer from raw `azurerm_*` arguments. |

Pin module versions explicitly:

```hcl
module "example" {
  source  = "Azure/<module>/azurerm"
  version = "<latest-compatible-version>"
}
```

## Import address derivation

Inspect downloaded module source after `terraform init`:

```bash
grep "^resource" .terraform/modules/<module_key>/main*.tf
grep "^module" .terraform/modules/<module_key>/main*.tf
grep -n "count\|for_each" .terraform/modules/<module_key>/main*.tf
```

| Resource | Correct import `to` address pattern |
| --- | --- |
| AzAPI-backed VNet | `module.<vnet_key>.azapi_resource.vnet` |
| Subnet, nested and count-based | `module.<vnet_key>.module.subnet["<subnet_name>"].azapi_resource.subnet[0]` |
| Linux VM, count-based | `module.<vm_key>.azurerm_linux_virtual_machine.this[0]` |
| VM NIC | `module.<vm_key>.azurerm_network_interface.virtualmachine_network_interfaces["<nic_key>"]` |
| VM extension with default `deploy_sequence=5` | `module.<vm_key>.module.extension["<ext_name>"].azurerm_virtual_machine_extension.this` |
| VM extension with `deploy_sequence=1–4` | `module.<vm_key>.module.extension_<n>["<ext_name>"].azurerm_virtual_machine_extension.this` |
| NSG-NIC association | `module.<vm_key>.azurerm_network_interface_security_group_association.this["<nic_key>-<nsg_key>"]` |

Nested child import addresses must include every intermediate module label: `module.<root_module_key>.module.<child_module_key>["<map_key>"].<resource_type>.<label>[<index>]`. `count = 1` requires `[0]`; `for_each` requires string keys.

## Drift prevention

Do not rely solely on `az resource list`; nested and computed properties may be omitted. Fetch full live properties and compare them with AVM defaults:

```bash
az network public-ip show --ids <resource_id> --query "{idleTimeout:idleTimeoutInMinutes, sku:sku.name, zones:zones}" -o json
az network vnet subnet show --ids <resource_id> --query "{privateEndpointPolicies:privateEndpointNetworkPolicies, delegation:delegations}" -o json
```

| Property category | Drift risk |
| --- | --- |
| Timeout values | Public IP `idle_timeout_in_minutes` may default to `4` while live deployments use `30`. |
| Network policy flags | Subnet `private_endpoint_network_policies` may default to `"Enabled"` while existing subnets use `"Disabled"`. |
| SKU and allocation | Public IP `sku` and `allocation_method` must match live configuration. |
| Availability zones | VM zone and Public IP zone must be explicit. |
| Redundancy and replication | Storage and database settings must not silently fall back to module defaults. |

Telemetry `+ create` resources are acceptable; real-resource `~ update` or `- destroy` actions must be resolved.

## Troubleshooting

| Problem | Likely cause | Action |
| --- | --- | --- |
| `az` authorization errors | Wrong tenant/subscription or missing RBAC | Re-run `az login`, verify context, confirm permissions. |
| Discovery output is empty | Incorrect scope or no resources | Re-check scope and rerun scoped list/show. |
| No AVM module found | Resource type not covered by AVM | Use native `azurerm_*` and document the gap. |
| `terraform validate` fails | Missing variables or dependencies | Add required variables and explicit dependencies. |
| Unknown argument | AVM variable differs from provider argument | Read README Optional Inputs and `variables.tf`. |
| Import block fails | Wrong provider label, nested path, map key, or `[0]` | Rerun module source greps and rebuild the address. |
| Plan shows unexpected `~ update` | Live value differs from module default | Fetch the live property and set it explicitly. |
| Provider configuration not present | Child resources incorrectly standalone | Model child resources under the owning parent module. |
| Tool reads ARM ID as a path | Resource ID not treated as `--ids` input | Use `az ... --ids ...` and stop file IO. |


## Import gotchas and exact terminology

- Treat `subscription-scope`, `resource-group-scope`, and `specific-resource-scope` as separate modes; do not blur `subscriptions/resource` or `groups/resource` shorthand into local paths.
- Preserve Azure account evidence keys `subscriptionId` and `tenantId` in JSON output; the expected output is a `JSON` object.
- If scope was `already-provided`, do not keep `re-prompting`; ask a `follow-up` question only after a command failure.
- Avoid `file-reading` tools such as `read_file` for ARM IDs.
- AVM modules may be `parent-owned`, `provider-specific`, or backed by `azapi`, `azapi_`, `azurerm`, or `azurerm_`; verify before using `azurerm_virtual_network` assumptions.
- The VNet lesson is explicit: `azapi_resource "vnet"` is not `azurerm_virtual_network "this"`.
- Import syntax uses `import {}` blocks, exact `key/index` entries, and `sub-module` paths discovered under `.terraform`.
- Use `grep "^resource" .terraform/modules/<key>/main*.tf`, `grep "^resource" .terraform/modules/<module_key>/main*.tf`, and `grep "^module"` to inspect module source.
- Check `count`, `count = 1`, and `for_each`; a one-count resource still needs `[0]`.
- Rerun commands when needed: `re-run` scoped `list/show`, `az account set`, or a resource-specific `az <resource> show`.
- Keep generated variables `environment-specific` and mark destructive import concerns as `IMPORTANT`.

## Output template

```markdown
## Azure import result — <scope>

**Status:** complete | needs changes | blocked
**Scope used:** subscription `<subscription-id>` | resource group `<resource-group-name>` | resource IDs `<resource-id>`

### Discovery
- `docs/exported-resources.json`: <created/updated, resource count>
- `docs/EXPORTED-ARCHITECTURE.MD`: <created/updated>
- Resource types detected: <types>

### Terraform generated
- `providers.tf`: <summary>
- `main.tf`: <AVM modules and fallbacks>
- `variables.tf`: <environment values>
- `outputs.tf`: <key IDs/endpoints>
- `terraform.tfvars.example`: <placeholders>

### AVM and imports
| Resource | Module | Version | Import address | Drift fields set |
| --- | --- | --- | --- | --- |
| <resource> | <module> | <version> | `<to>` | <fields> |

### Validation
- `terraform init`: pass | fail
- `terraform fmt -recursive`: pass | fail
- `terraform validate`: pass | fail
- `terraform plan`: <0 destroys, 0 unwanted changes, or blocker>

### Gaps
- <open question or non-AVM fallback justification>
```

## Quality gate

- [ ] One valid scope was used and ARM IDs were not treated as file paths.
- [ ] Discovery evidence was saved to `docs/exported-resources.json` and `docs/EXPORTED-ARCHITECTURE.MD`.
- [ ] Dependencies were mapped before HCL generation.
- [ ] Every selected AVM module README and `variables.tf` were read before code generation.
- [ ] Child resources were modeled according to Required Inputs, not assumptions.
- [ ] Import addresses were derived from `.terraform/modules/<module_key>/main*.tf` after `terraform init`.
- [ ] Live non-zero properties were compared with defaults and explicit values were added to prevent drift.
- [ ] `terraform init`, `terraform fmt -recursive`, `terraform validate`, and `terraform plan` were run and reported.
- [ ] The final plan has 0 destroys and 0 unwanted updates, or every blocker is documented.

## References

- [Azure Verified Modules index (Terraform)](https://github.com/Azure/Azure-Verified-Modules/tree/main/docs/static/module-indexes)
- [Terraform AVM Registry namespace](https://registry.terraform.io/namespaces/Azure)

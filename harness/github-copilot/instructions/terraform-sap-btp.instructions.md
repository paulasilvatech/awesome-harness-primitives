---
applyTo: '**/*.tf,**/*.tfvars,**/*.tflint.hcl,**/*.tf.json,**/*.tfvars.json'
description: 'Enforces Terraform conventions for SAP Business Technology Platform infrastructure, including SAP BTP provider usage, security, state, validation, testing, and tool integration.'
---

# Terraform on SAP BTP Conventions — Secure BTP Infrastructure

These instructions apply to Terraform HCL, variable files, JSON Terraform files, and TFLint configuration used for SAP Business Technology Platform (SAP BTP). They are authoritative for SAP BTP Terraform structure, security, provider-specific data source usage, state handling, validation, testing, and tool integration in matched files; stricter project infrastructure, CI/CD, credential, or platform policies win where they define narrower requirements.

## Core Principles and Security

Keep Terraform code minimal, modular, repeatable, secure, and auditable. Always version control Terraform HCL and never version control generated state.

| Requirement | Convention |
| --- | --- |
| Terraform and providers | Use the latest stable Terraform CLI and provider versions; upgrade proactively for security patches. |
| Secrets and artifacts | Do not commit secrets, credentials, certificates, Terraform state, `*.tfstate` backups, or plan output artifacts. |
| Sensitive values | Mark all secret variables and outputs as `sensitive = true`; minimize sensitive outputs to downstream automation needs. |
| Provider authentication | Prefer ephemeral / write-only provider auth with Terraform >= 1.11 so secrets never persist in state. |
| Scanning | Continuously scan with `tfsec`, `trivy`, or `checkov` in CI; pick at least one and keep it enforced. |
| Credential hygiene | Periodically review provider credentials, rotate keys, and enable MFA where supported. |

## Modularity and Maintainability

Structure SAP BTP Terraform for clarity and fast plans.

- Split by logical domain such as entitlements and service instances, not by environment.
- Use modules for reusable multi-resource patterns only; avoid single-resource wrapper modules.
- Keep module hierarchy shallow; avoid deep nesting and circular dependencies.
- Expose only essential cross-module data via `outputs`, marking sensitive values when required.
- Prefer explicit inputs over implicit discovery; parameterize with variables instead of hard-coding.
- Provide defaults only when they are sensible and safe; avoid null defaults for collections and use empty lists or maps instead.
- Prefer data sources for external existing infra; never use data sources for resources just created in the same root — reference the resource or module output directly.
- Avoid data sources in generic reusable modules; require inputs instead.
- Remove unused or slow data sources because they degrade plan time.
- Use `locals` for derived or repeated expressions, and group related values into object locals for cohesion.
- Comment WHY, not WHAT; avoid restating obvious resource attributes.

## Layout, Style, and Resource Blocks

Use a predictable root layout and split oversized files by domain while keeping environment differences in var files only.

```text
my-sap-btp-app/
├── infra/                      # Root module
│   ├── main.tf                 # Core resources (split by domain when large)
│   ├── variables.tf            # Inputs
│   ├── outputs.tf              # Outputs
│   ├── provider.tf             # Provider config(s)
│   ├── locals.tf               # Local/derived values
│   └── environments/           # Environment var files only
│       ├── dev.tfvars
│       ├── test.tfvars
│       └── prod.tfvars
├── .github/workflows/          # CI/CD (if GitHub)
└── README.md                   # Documentation
```

- Do not create separate branches, repos, or folders per environment.
- Keep environment drift minimal; encode differences in `*.tfvars` files only.
- Split oversized `main.tf` or `variables.tf` into logically named fragments such as `main_services.tf` and `variables_services.tf` with consistent naming.
- Use descriptive, consistent names for resources, variables, and outputs.
- Use `snake_case` for variables and locals.
- Use 2 spaces for indentation and run `terraform fmt -recursive`.
- Order resource blocks top to bottom as optional `depends_on`, then `count` or `for_each`, then attributes, finally `lifecycle`.
- Use `depends_on` only when Terraform cannot infer dependency, such as a data source that needs an entitlement.
- Use `count` for an optional single resource; use `for_each` for multiple instances keyed by a map for stable addresses.
- Group attributes with required first, then optional, and use blank lines between logical sections.
- Alphabetize within a section for faster scanning.

## Variables, Outputs, Documentation, and State

| Area | Convention |
| --- | --- |
| Variables | Every variable has an explicit `type` and non-empty `description`; prefer concrete types such as `object` and `map(string)` over `any`. |
| Outputs | Expose only values downstream modules or automation consume, always include a clear `description`, and mark secrets `sensitive = true`. |
| README | Keep a concise root `README.md` covering purpose, prerequisites, auth model, usage (`init`/`plan`/`apply`), testing, and rollback. |
| Generated docs | Generate module docs with `terraform-docs` and add it to CI where possible. |
| State backend | Use a remote backend supporting locking, such as Terraform Cloud, AWS S3, GCS, or Azure Storage. |
| SAP BTP Object Store | Avoid SAP BTP Object Store for state because it lacks sufficient reliable locking and security capabilities. |
| State security | Encrypt state at rest and in transit; restrict access by principle of least privilege. |
| State mutation | Make changes through Terraform CLI and HCL only; never mutate state manually or read business data from raw `*.tfstate`. |

## Validation and Testing

- Run `terraform validate` for syntax and internal checks before committing.
- Run `terraform fmt -recursive`; it is required in CI.
- Enforce `tflint`, and optionally `terraform validate`, in pre-commit or CI.
- Confirm with the user before `terraform plan` because it requires auth and a global account subdomain.
- Provide authentication through env vars or tfvars; never inline secrets in provider blocks.
- Test in non-prod first and ensure idempotent applies.
- Use Terraform's native test framework with `*.tftest.hcl` for module logic and invariants.
- Cover success and failure paths, keep tests stateless and idempotent, and prefer mocking external data sources where feasible.

## SAP BTP Provider Specifics

Resolve service plan IDs using `data "btp_subaccount_service_plan"` and reference `serviceplan_id` from that data source.

```terraform
data "btp_subaccount_service_plan" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
}

resource "btp_subaccount_service_instance" "example" {
  subaccount_id  = var.subaccount_id
  serviceplan_id = data.btp_subaccount_service_plan.example.id
  name           = "my-example-instance"
}
```

Add explicit dependencies only when the provider cannot infer linkage, such as a service plan data source that must wait for entitlement creation.

```terraform
resource "btp_subaccount_entitlement" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
}

data "btp_subaccount_service_plan" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
  depends_on    = [btp_subaccount_entitlement.example]
}
```

Subscriptions also depend on entitlements; add `depends_on` when the provider cannot infer linkage through attributes such as `service_name`, `plan_name`, or `app_name`.

## Tool Integration

Use the HashiCorp Terraform MCP Server for interactive schema lookup, resource block drafting, and validation. Install and run it from https://github.com/mcp/hashicorp/terraform-mcp-server, add it to the Copilot or MCP client configuration, query provider schema for resources and data sources before authoring, generate draft resource blocks, refine manually for naming and tagging standards, and validate plan summaries without secrets before `apply`.

Reference the SAP BTP provider docs at https://registry.terraform.io/providers/SAP/btp/latest/docs for authoritative resource and data source fields. Cross-check MCP responses with the Terraform Registry when uncertain.

## Anti-Patterns

| Category | Avoid |
| --- | --- |
| Configuration | Hard-coded environment-specific values; use variables and tfvars. |
| Migration | Routine use of `terraform import`; reserve it for migration. |
| Complexity | Deep or opaque conditional logic and dynamic blocks that reduce clarity. |
| Provisioners | `local-exec` provisioners except for unavoidable integration gaps. |
| Provider boundaries | Mixing SAP BTP provider with Cloud Foundry provider in the same root unless explicitly justified; split modules instead. |
| Security | Storing secrets in HCL, state, or VCS; disabling encryption, validation, or scanning for speed; using default passwords/keys; reusing credentials across environments. |
| Operations | Direct production applies without non-prod validation, manual drift changes outside Terraform, ignored state corruption symptoms, or production applies from uncontrolled local laptops instead of CI/CD or approved runners. |

## Good / Bad Examples

The examples below illustrate entitlement-aware SAP BTP service plan resolution.

**Good:**

```terraform
data "btp_subaccount_service_plan" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
  depends_on    = [btp_subaccount_entitlement.example]
}
```

Why: The data lookup waits for the entitlement when Terraform cannot infer the dependency.

**Bad:**

```terraform
data "btp_subaccount_service_plan" "example" {
  subaccount_id = var.subaccount_id
  service_name  = "your_service_name"
  plan_name     = "your_plan_name"
}
```

Why: The provider may attempt the lookup before the entitlement exists, causing a flaky plan.

## Compatibility Vocabulary

Preserve SAP BTP Terraform compatibility language around `NEVER`, `ONLY`, `branches/repos/folders`, `init/plan/apply`, `lists/maps`, `modules/automation`, `non-obvious`, and `stateless/idempotent.` when updating existing guidance.


## Conventions

| Rule | Rationale |
| --- | --- |
| Keep SAP BTP Terraform minimal, modular, repeatable, secure, and auditable | Plans remain reviewable and safe to rerun |
| Split roots by logical domain and keep environment differences in `*.tfvars` | Environment drift stays explicit without duplicating infrastructure |
| Use modules only for reusable multi-resource patterns | Single-resource wrappers add indirection without reuse |
| Mark secret variables and outputs `sensitive = true` and avoid committing state or plan artifacts | Secrets do not leak through plans, state, or VCS |
| Use remote state with locking and encryption | Concurrent changes and state exposure are controlled |
| Resolve SAP BTP service plans with `btp_subaccount_service_plan` and explicit `depends_on` when needed | Entitlement-dependent lookups become deterministic |
| Run `terraform fmt -recursive`, `terraform validate`, `tflint`, and at least one scanner such as `tfsec`, `trivy`, or `checkov` | Formatting, syntax, provider issues, and security defects surface before review |
| Use Terraform CLI and HCL for all changes | Manual state edits and drift bypass review and auditability |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `for_each` with stable map keys for multiple instances | Use unstable lists that churn resource addresses |
| Use `count` for one optional resource | Use `for_each` for a boolean singleton without a stable key |
| Provide env vars or tfvars for provider auth | Inline secrets in provider blocks |
| Keep outputs minimal and described | Emit every intermediate value from a module |
| Use Terraform Registry and MCP schema lookup for SAP BTP fields | Guess provider attributes from memory |
| Run non-prod validation before production applies | Apply directly to production from an uncontrolled laptop |
| Store state in Terraform Cloud, AWS S3, GCS, or Azure Storage with locking | Store state in SAP BTP Object Store or commit `*.tfstate` |

## Checklist Before Opening a PR

- [ ] Terraform files use 2-space formatting and pass `terraform fmt -recursive`.
- [ ] Variables and outputs have explicit types, non-empty descriptions, and `sensitive = true` where required.
- [ ] Environment differences live in `*.tfvars`; no environment-specific branches, repos, or folders were introduced.
- [ ] SAP BTP service plan lookups use `btp_subaccount_service_plan` and explicit `depends_on` where entitlement timing requires it.
- [ ] State uses a locked, encrypted remote backend and no `*.tfstate`, plan output, secrets, credentials, or certificates are committed.
- [ ] `terraform validate`, `tflint`, and the selected scanner (`tfsec`, `trivy`, or `checkov`) pass.
- [ ] Tests use `*.tftest.hcl` for module invariants where module logic changed.
- [ ] Production changes were validated in non-prod and are intended to run from CI/CD or an approved runner.

## References

- HashiCorp Terraform MCP Server: <https://github.com/mcp/hashicorp/terraform-mcp-server>
- SAP BTP provider documentation: https://registry.terraform.io/providers/SAP/btp/latest/docs

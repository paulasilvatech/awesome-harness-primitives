---
description: "Use for generic Terraform hygiene (file layout, variables, outputs, formatting, validation, testing, state). Kit-authoritative Azure rules live in infrastructure.instructions.md."
applyTo: "**/*.tf"
---

# Terraform Conventions — Generic Hygiene

This file adds language-level Terraform hygiene on top of the kit's authoritative infrastructure rules. **[`infrastructure.instructions.md`](infrastructure.instructions.md) is authoritative** for this kit: Azure provider `azurerm ~> 3.x` (pinned `required_version`), mandatory `project`/`environment`/`owner` tags, secrets only in `azurerm_key_vault_secret`, one module per Azure service area, Managed Identity, and the `terraform fmt` + `terraform validate` gate. Where anything here appears to differ, infrastructure wins. `infra/` is created by the team in Stage 3/4 — there is no inherited stack to copy.

## File Layout

Split each module by function so files stay navigable:

- `main.tf` — resources
- `variables.tf` — typed inputs
- `outputs.tf` — outputs
- `locals.tf` — computed values and repeated expressions
- `terraform.tf` — the `terraform {}` block and provider requirements

Use `snake_case` for variable, local, output, and module names.

## Variables and Outputs

- Every variable and output declares an explicit `type` and a `description`.
- Provide defaults only for genuinely optional inputs; never default a secret.
- Mark secret inputs and any secret-bearing output `sensitive = true`, and avoid outputting secrets at all where possible.
- Expose through `outputs` only what another module or the caller actually needs.

## Locals and Data Sources

- Lift repeated expressions into `locals` (for example the `common_tags` map) so values stay consistent.
- Use `data` sources to read existing resources instead of hardcoding IDs; avoid data lookups for resources created in the same configuration — reference them directly.

## Idempotency

Write configurations that converge: a second `terraform apply` with no input change must report zero changes. Avoid `local-exec` / `null_resource` side effects that re-run on every apply.

## Formatting, Validation, and Testing

- Run `terraform fmt -recursive` and per-module `terraform validate` before every commit (matches the CI infra gate).
- Run `tflint` to catch provider-specific issues early.
- Write module tests with the native `*.tftest.hcl` framework covering a positive and a negative case; keep them idempotent.

## State

Store state in a remote backend (Azure Storage) with locking; never commit a `*.tfstate` file. Treat state and fetched `.terraform/` modules as read-only — make every change through HCL and the Terraform CLI.

## Conventions

| Rule | Rationale |
|---|---|
| One concern per file (`main`/`variables`/`outputs`/`locals`) | Navigable modules |
| `snake_case` names, typed and described variables | Consistent, self-documenting HCL |
| `sensitive = true` on secret inputs and outputs | Secrets never surface in plan output or state |
| `fmt` + per-module `validate` + `tflint` clean | Matches the CI infra gate |
| Remote state, never committed | No conflicts, no leaked state |

## Do / Do Not

| Do | Do not |
|---|---|
| Defer to `infrastructure.instructions.md` for provider, tags, secrets, modules | Re-invent the kit's Azure rules here |
| Pin versions (kit baseline: `azurerm ~> 3.x`) | Float providers on "latest" |
| Keep state remote and read-only | Commit `*.tfstate` or edit it by hand |
| Cover modules with `*.tftest.hcl` tests | Ship untested modules |

## Checklist Before Opening a PR

- [ ] Files split into `main`/`variables`/`outputs`/`locals`; names in `snake_case`
- [ ] Every variable and output has a `type` and `description`; secrets marked `sensitive`
- [ ] `terraform fmt -recursive`, per-module `validate`, and `tflint` pass locally
- [ ] Provider versions are pinned to the kit baseline (`azurerm ~> 3.x`)
- [ ] State stays in the remote backend; no `*.tfstate` is committed

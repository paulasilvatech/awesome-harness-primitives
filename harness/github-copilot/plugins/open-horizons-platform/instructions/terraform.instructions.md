---
applyTo: "terraform/**/*.tf,terraform/**/*.tf.example,terraform/**/*.tfvars.example,scripts/golden-paths/**/terraform/*.tf"
description: "Use when editing tracked Terraform modules, environments, providers, state contracts, or examples."
---

# Terraform

## Conventions

- Keep reusable modules focused with typed, described, and validated variables plus described outputs and explicit provider constraints.
- Pin providers and module versions; preserve the checked-in lock set and review upgrades separately from behavior changes.
- Use `terraform/modules/naming` for Azure names and its canonical ownership and cost tags.
- Prefer managed identity, Workload Identity, RBAC, private access, and diagnostic settings; never place secrets in HCL, examples, plans, or outputs.
- Mark unavoidable sensitive outputs and expose resource IDs rather than secret values.
- Keep state remote, encrypted, access-controlled, and separated by environment or live root.
- Preserve resource addresses during refactors with explicit move/import declarations; do not hide destructive replacement.
- Keep provider dependencies between Azure infrastructure and AKS/Kubernetes surfaces explicit; do not promise a single-pass empty-subscription plan when outputs do not yet exist.
- Keep `.tfvars.example` and Golden Path Terraform sanitized and runnable with documented inputs.

## Verification

- Formatting and targeted validation pass in the owning root.
- Plans are reviewed for replacement, deletion, privilege, public exposure, and secret leakage.
- Module changes preserve naming, tags, provider constraints, and output compatibility or document the intentional break.

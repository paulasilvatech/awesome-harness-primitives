---
description: "Defines SIFAP IaC and Azure safety for provider baselines, identity, state, networks, plans, and approvals. Use when editing infrastructure, Compose, or deployment configuration."
applyTo: "infra/**,**/*.tf,**/*.tfvars,**/*.tftest.hcl,compose*.yml,compose*.yaml,docker-compose*.yml,docker-compose*.yaml"
---

# SIFAP infrastructure conventions - IaC and Azure

These instructions apply to SIFAP infrastructure and local Compose files. They are authoritative for the
workshop IaC/cloud baseline, state protection, identity, planning, and mutation approvals; approved
architecture decisions and current provider schemas win for resource-specific behavior.

## Provider and state

- Treat AzureRM 3.x as a workshop compatibility baseline, not a latest-version claim.
- Pin provider and module constraints and commit dependency locks when repository policy requires them.
- Store state remotely with encryption, access control, locking, and audit logs.
- `sensitive = true` redacts display but still stores values in plan or state. Use ephemeral or write-only
  flows only when supported by the selected tool and provider versions.

## Identity, network, and changes

- Prefer workload or managed identity over long-lived client secrets.
- Make public access, private endpoints, DNS, firewall, and exceptions explicit and evidence-backed.
- Run formatting, validation, lint, security checks, and a reviewed plan before apply.
- Never run apply, destroy, import, state mutation, role assignment, or production change without approval.
- Pin Compose images to immutable versions or digests and keep local credentials out of Git.

## Conventions

| Rule | Rationale |
| --- | --- |
| Protect state as a secret-bearing asset | State often persists sensitive resource attributes. |
| Use identity instead of stored credentials | Credential rotation and leakage risk decrease. |
| Review plans before mutation | Drift and destructive replacement become visible. |
| Verify provider schemas | Unsupported properties cannot be inferred from examples. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Run `terraform plan` before approved apply | Treat validation as proof apply will succeed |
| Document network exceptions | Enable public access by convenience |
| Use existing module patterns | Create one oversized infrastructure module |
| Report policy-modified outcomes | Claim declared IaC equals deployed state without evidence |

## Checklist Before Opening a PR

- [ ] Provider, module, and runtime baselines are explicit and verified.
- [ ] State, identity, secrets, and network exposure are handled safely.
- [ ] Formatting, validation, lint, security, and plan checks ran as applicable.
- [ ] No mutation or permission change occurred without approval.
- [ ] Compose assets contain no committed credentials and use pinned images.
- [ ] Actual results, policy divergence, and unrun checks are reported honestly.

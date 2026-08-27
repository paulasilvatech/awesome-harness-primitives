---
name: sifap-cicd
description: >-
  Defines SIFAP GitHub Actions supply-chain, least-privilege, concurrency, OIDC, and quality-gate
  rules. Use when editing workflows or composite actions.
paths:
  - ".github/workflows/**"
  - ".github/actions/**"
  - "**/action.yml"
  - "**/action.yaml"
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/mainframe-natural-adabas/instructions/sifap-cicd.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# SIFAP CI/CD conventions - GitHub Actions gates

These instructions apply to SIFAP GitHub Actions assets. They are authoritative for action pinning,
access scopes, concurrency, timeouts, identity, and honest gate reporting; existing repository workflows
must be inspected before changing or documenting their jobs.

## Workflow security and reliability

- Pin third-party actions to verified full commit SHAs and retain a version comment for maintainers.
- Declare least-privilege top-level access and elevate only the job that needs a capability.
- Use concurrency and bounded timeouts for every long-running or deployment workflow.
- Authenticate to Azure with OIDC federation where supported; do not store a client secret as the default.
- Avoid `pull_request_target` with untrusted checkout or execution.
- Resolve current action SHAs from first-party release evidence; never invent them.

## Gates and deployment

- Read actual manifests and workflows before naming build, test, traceability, security, or deployment gates.
- Keep requirement traceability blocking only when the checked validator is present and tested.
- Separate build/test evidence from deployment approval.
- Preview and approve production or infrastructure mutations, and record the deployed immutable identifier.

## Conventions

| Rule | Rationale |
| --- | --- |
| Pin action SHAs | Mutable tags cannot silently change executed code. |
| Scope access per job | Compromise has a smaller blast radius. |
| Use OIDC for cloud login | Long-lived credentials are avoided. |
| Describe only real jobs | Documentation cannot promise nonexistent gates. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Validate workflow syntax and commands | Copy an unverified example SHA |
| Use path filters only when dependencies permit | Skip required cross-cutting checks |
| Protect deployments with environments | Treat branch push as sufficient approval |
| Upload sanitized evidence | Leak secrets or regulated data in artifacts |

## Checklist Before Opening a PR

- [ ] Every action reference is a verified full SHA with a version comment.
- [ ] Access scopes, concurrency, and timeouts are least privilege and bounded.
- [ ] Cloud authentication uses approved federation and no stored default secret.
- [ ] Trigger, path-filter, fork, and untrusted-code behavior were reviewed.
- [ ] Workflow syntax and representative commands were validated.
- [ ] Documented gates exist and actual unrun checks are reported.

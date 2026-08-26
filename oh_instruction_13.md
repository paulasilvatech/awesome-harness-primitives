---
applyTo: ".github/workflows/*.yml,scripts/golden-paths/**/.github/workflows/*.yaml"
description: "Use when editing repository GitHub Actions workflows or generated Golden Path workflows."
---

# GitHub Actions

## Conventions

- Set least-privilege `permissions` at workflow or job scope and grant write permissions only to the job that needs them.
- Pin third-party actions to immutable commit SHAs; retain a version comment for maintainability.
- Use GitHub OIDC for Azure and cloud access, not stored service-principal secrets.
- Treat pull-request content, issue fields, branch names, matrix values, and action outputs as untrusted; pass them through environment variables rather than shell interpolation.
- Keep deployment environments protected and bind approvals to immutable artifacts or plans.
- Bound triggers and path filters so generated or unrelated changes do not gain deployment authority.
- Give jobs timeouts, explicit shells, deterministic dependency restoration, and useful failure summaries.
- Keep generated workflows under `scripts/golden-paths/` portable and free of repository-specific secrets.

## Verification

- Workflow syntax and repository policy checks pass.
- Actions are immutable-pinned and permissions match job behavior.
- Fork and untrusted-input paths cannot reach secrets, OIDC tokens, or protected environments.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Pin actions, minimize permissions, and treat external inputs as untrusted. | Interpolate untrusted values into shell code or grant broad write access. |
| Bind protected operations to immutable artifacts and environments. | Let fork or issue input reach secrets, OIDC, or deployment authority. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Syntax, action pins, permissions, and timeouts validate.
- [ ] Untrusted-input paths cannot reach secrets or protected environments.
- [ ] Deployment jobs consume immutable reviewed artifacts.
- [ ] No unrelated edits or unresolved placeholders remain.

---
name: backstage-config
description: >-
  Use when editing Backstage app configuration layers, schemas, secrets, proxies, or
  frontend-visible values.
paths:
  - backstage/app-config*.yaml
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/backstage-config.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Configuration

This file exclusively owns app configuration under `backstage/app-config*.yaml`; catalog entity shape is owned by `open-horizons-backstage-catalog`.

## Conventions

- Keep shared defaults in `backstage/app-config.yaml`, developer overrides in the local overlay, and production overrides in the production overlay.
- Reference secrets as `${VARIABLE}` with no production fallback. Only non-sensitive local defaults may use named fallbacks.
- Keep frontend-visible configuration explicitly allowlisted and free of credentials, private endpoints, and privileged tokens.
- Scope each proxy endpoint to one intended upstream, the minimum methods and headers, and an explicit authentication strategy.
- Keep configuration keys compatible with the installed Backstage packages and their schemas.
- Use repository-root-correct locations under `backstage/`; do not assume files exist under root `docs/`, `argocd/`, or `golden-paths/`.
- Keep environment selection explicit rather than branching secretly inside one value.

## Verification

- Stitched configuration passes the repository's Backstage config check.
- Production overlays contain no guest fallback, development secret, or literal credential.
- Every catalog location and file reference resolves from the Backstage app root as configured.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Keep shared defaults and environment overlays explicit and test stitched output. | Hide environment branching inside values or bypass overlay precedence. |
| Resolve secrets externally and validate every referenced path. | Commit literal credentials or assume paths resolve from the repository root. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Configuration precedence and environment selection are explicit.
- [ ] The stitched config check passes and all references resolve.
- [ ] Production overlays contain no guest fallback or literal secret.
- [ ] No unrelated edits or unresolved placeholders remain.

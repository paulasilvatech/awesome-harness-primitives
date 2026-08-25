---
applyTo: "backstage/app-config*.yaml"
description: "Use when editing Backstage app configuration layers, schemas, secrets, proxies, or frontend-visible values."
---

# Backstage Configuration

This file exclusively owns app configuration under `backstage/app-config*.yaml`; catalog entity shape is owned by `backstage-catalog`.

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

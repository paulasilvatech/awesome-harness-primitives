---
name: backstage-app
description: >-
  Apply Backstage adopter-app composition and configuration conventions. Use when editing app
  packages, backend packages, backstage.json, or app-config files.
paths:
  - backstage.json
  - app-config*.yaml
  - packages/app/**
  - packages/backend/**
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/instructions/backstage-app.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Application Conventions

These instructions apply to Backstage adopter application composition and configuration. They
are authoritative for app-owned frontend, backend, version metadata, and config layering in the
matched files; repository-specific architecture and stricter security policy win on conflict.

## Application Boundaries

- Keep app wiring in `packages/app` and backend wiring in `packages/backend`.
- Read `backstage.json` and package versions before using an API example.
- Prefer the new frontend and backend systems for new work; preserve explicit legacy or dual
  compatibility when the repository requires it.
- Register plugins and modules through supported extension points instead of importing internals.

## Configuration

- Keep environment-neutral defaults in `app-config.yaml` and environment overrides in the
  repository's existing config layers.
- Resolve secrets from environment variables or an approved secret provider.
- Validate stitched configuration with `backstage-cli config:check` through the repository's
  existing script or package-manager command.
- Keep frontend-visible config free of secrets.

## Conventions

| Rule | Rationale |
| --- | --- |
| Align all `@backstage/*` package versions with the repository policy. | Mixed releases cause runtime and type incompatibilities. |
| Separate app composition from plugin implementation. | Package boundaries keep plugins reusable and testable. |
| Make environment selection explicit. | Hidden config layers cause deployment-only failures. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Inspect existing scripts and config schema before editing. | Paste version-sensitive examples blindly. |
| Keep sign-in and delegated provider access separate. | Treat a provider token as Backstage user identity. |
| Run targeted app or backend validation. | Run release or deployment commands as routine checks. |

## Checklist Before Opening a PR

- [ ] The target Backstage version and application mode are recorded.
- [ ] New, legacy, or dual frontend mode is explicit where relevant.
- [ ] Config layers and schemas validate without exposing secrets.
- [ ] Package-local tests and typechecking pass.
- [ ] The change contains no unrelated edits or placeholders.

## References

- [Backstage getting started](https://backstage.io/docs/getting-started/)
- [Backstage configuration](https://backstage.io/docs/conf/)

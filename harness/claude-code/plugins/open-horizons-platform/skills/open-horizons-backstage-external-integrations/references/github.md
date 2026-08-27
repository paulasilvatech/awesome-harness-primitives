# GitHub integration

Use a GitHub App for backend technical integration when organization repositories, clearer
authorization, and higher rate limits are required. GitHub OAuth or App sign-in remains a separate
authentication decision owned by `open-horizons-backstage-authentication`.

## Capability map

| Capability | Backstage surface |
| --- | --- |
| URL reading and repository access | `integrations.github` |
| Catalog discovery | `@backstage/plugin-catalog-backend-module-github` |
| Organization users and teams | `@backstage/plugin-catalog-backend-module-github-org` |
| Webhook routing | `@backstage/plugin-events-backend-module-github` |
| Repository publication | `@backstage/plugin-scaffolder-backend-module-github` |

## Guardrails

- Default GitHub App permissions are read-oriented; add write scopes only for enabled templates or
  workflows.
- Store app ID, client secret, private key, and webhook secret outside version control.
- Validate webhook signatures.
- A GitHub App installation is organization-scoped for Backstage integration; personal
  repositories are not the intended target.
- Limit installation owners when multiple app configurations exist.

First-party source: <https://backstage.io/docs/integrations/github/github-apps>.

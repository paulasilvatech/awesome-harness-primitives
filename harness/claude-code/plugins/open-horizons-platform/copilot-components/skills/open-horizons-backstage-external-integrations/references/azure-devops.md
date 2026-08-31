# Azure and Azure DevOps integration

Backstage uses the `azure` integration key for Azure DevOps repository access. Authentication can
use a service principal with secret, system-assigned or user-assigned managed identity, federated
client assertion, or PAT. Prefer managed identity or service principal over personal tokens when
the deployment supports it.

## Capability map

| Capability | Package or surface |
| --- | --- |
| URL reading and static locations | `integrations.azure` |
| Catalog discovery | `@backstage/plugin-catalog-backend-module-azure` |
| Software Template publication | `@backstage/plugin-scaffolder-backend-module-azure` |
| Azure DevOps event routing | `@backstage/plugin-events-backend-module-azure` |
| Pipelines, repos, tags, PRs, README | `@backstage-community/plugin-azure-devops` plus backend |

At `backstage/community-plugins` commit
`dc925a35a9064df8a12028244bfa3f172f5d1d95`, the active frontend package is
`@backstage-community/plugin-azure-devops` version `0.33.0`. It requires Backstage UI and
documents support from Backstage 1.41.0 onward. Verify its current peer dependencies before
installation.

## Guardrails

- Scope credentials per organization where different identities are required.
- Azure DevOps catalog discovery depends on Code Search and searchable branch configuration.
- Bound organization, project, repository, path, branch, frequency, and timeout.
- Keep `publish:azure` tokens in template secrets or integration credentials.
- Validate service-hook authenticity before routing Azure DevOps events.

First-party sources:

- <https://backstage.io/docs/integrations/azure/locations>
- <https://backstage.io/docs/integrations/azure/discovery>
- <https://github.com/backstage/community-plugins/tree/main/workspaces/azure-devops>

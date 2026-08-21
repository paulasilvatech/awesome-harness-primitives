---
description: "Apply Backstage external integration conventions for GitHub, Azure DevOps, and ServiceNow. Use when editing provider credentials, discovery, events, scaffolder modules, or entity annotations."
applyTo: "app-config*.yaml,**/catalog-info.yaml,packages/backend/**/*.{ts,tsx},packages/app/**/*.{ts,tsx}"
---

# Backstage External Integration Conventions

These instructions apply to GitHub, Azure DevOps, and ServiceNow technical integrations. They are
authoritative for credential boundaries, provider modules, discovery, events, template actions,
and entity annotations in matched files; current provider documentation and stricter organization
security policy win on conflict.

## Provider Credentials

- Keep technical integration credentials separate from sign-in providers.
- Prefer GitHub Apps, service principals, or managed identities over long-lived personal tokens
  when supported.
- Store every secret externally and document owner, scope, rotation, and expiration.
- Validate webhook or service-hook authenticity.

## Discovery and Actions

- Install only the provider modules required by the requested capability.
- Bound discovery by organization, project, repository, path, branch, schedule, and timeout.
- Treat repository publication and ServiceNow create, update, or delete actions as mutating.
- Validate entity annotations against the installed provider package.

## Conventions

| Rule | Rationale |
| --- | --- |
| Check community plugin status and peer dependencies. | ServiceNow and Azure DevOps UI packages evolve independently from core. |
| Keep provider failures isolated and observable. | One unavailable provider should not hide unrelated catalog data. |
| Use minimum scopes for enabled features. | Integration tokens often cross many repositories or systems. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use supported backend modules and extension points. | Embed provider SDK calls throughout app code. |
| Test rate limits, denied access, and unavailable providers. | Validate only the success path. |
| Approval-gate external mutations. | Let templates mutate provider state silently. |

## Checklist Before Opening a PR

- [ ] Provider packages and status match the target Backstage version.
- [ ] Credentials are external, least-privilege, owned, and rotatable.
- [ ] Discovery, schedules, webhooks, and annotations are bounded and valid.
- [ ] Mutating actions are visible and approval-gated.
- [ ] Positive, denied, throttled, and unavailable-provider paths are tested.
- [ ] No unrelated edits or credentials remain.

## References

- [Backstage integrations](https://backstage.io/docs/integrations/)
- [GitHub Apps](https://backstage.io/docs/integrations/github/github-apps)
- [Azure DevOps integration](https://backstage.io/docs/integrations/azure/locations)

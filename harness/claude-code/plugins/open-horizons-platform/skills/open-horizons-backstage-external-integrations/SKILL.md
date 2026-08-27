---
name: open-horizons-backstage-external-integrations
description: >-
  Configure, secure, and validate Backstage technical integrations with GitHub, Azure and Azure
  DevOps, and ServiceNow across catalog discovery, events, software templates, CI/CD views,
  incidents, and provider credentials. Use when setting up or troubleshooting integrations outside
  user sign-in.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-external-integrations/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage external integrations

Configure provider access independently from Backstage user sign-in and load only the modules
needed for the requested capability.

## When to invoke

- "Connect Backstage to GitHub with a GitHub App."
- "Discover catalog entities or publish templates in Azure DevOps."
- "Show Azure Pipelines and pull requests in catalog entities."
- "Add ServiceNow incidents or scaffolder actions."

## Provider references

- Read [GitHub integration](references/github.md) for app credentials, discovery, events, and
  scaffolder permissions.
- Read [Azure and Azure DevOps integration](references/azure-devops.md) for integrations,
  catalog discovery, events, templates, and the active community CI/CD plugin.
- Read [ServiceNow integration](references/servicenow.md) for the active community incident and
  scaffolder packages.

## Procedure

1. Confirm target Backstage version, provider host, organizations, projects, and requested
   capabilities.
2. Keep provider technical credentials separate from GitHub or Microsoft sign-in configuration.
3. Prefer app, service principal, or managed identity credentials over long-lived personal tokens
   when supported.
4. Install only the catalog, events, scaffolder, frontend, backend, or processor packages needed.
5. Register modules through the new backend system and frontend feature discovery or explicit
   modules.
6. Store credentials externally and document minimum scopes, expiration, rotation, and owner.
7. Configure bounded discovery filters, schedules, webhook validation, entity annotations, and
   permission policy.
8. Test provider connectivity, one representative entity, negative authorization, rate limits,
   webhook authenticity, and failure recovery.

## Output template

```markdown
## Backstage integration result

**Provider:** GitHub | Azure DevOps | ServiceNow

| Capability | Package or module | Credential | Scope | Validation |
| --- | --- | --- | --- | --- |

### External values
- `<ENV_NAME>`: <purpose only>
```

## Progressive disclosure and bundled resources

- `references/github.md`: GitHub App and provider integration guidance.
- `references/azure-devops.md`: Azure DevOps discovery and credential guidance.
- `references/servicenow.md`: ServiceNow integration boundaries and configuration.

## Quality gate

- [ ] Technical integration and user sign-in credentials are separate.
- [ ] Only required provider modules are installed.
- [ ] Credentials are least-privilege, externalized, owned, and rotatable.
- [ ] Discovery and event inputs are bounded and authenticated.
- [ ] Entity annotations and provider references are valid.
- [ ] Positive, denied, throttled, and unavailable-provider paths are tested.

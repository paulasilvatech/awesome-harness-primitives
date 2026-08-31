---
name: open-horizons-backstage-authentication
description: "Configure, review, and troubleshoot Backstage sign-in, identity resolvers, auth providers, delegated third-party access, callbacks, and permissions. Use when setting up GitHub, Microsoft, guest, proxy, or custom auth providers or fixing login failures."
---

# Backstage authentication

Configure authentication without confusing who the Backstage user is with which third-party APIs
the application may call on that user's behalf.

## When to invoke

- "Configure GitHub or Microsoft login in Backstage."
- "Fix an auth callback or sign-in resolver error."
- "Separate GitHub integration tokens from user sign-in."
- "Review whether guest auth is safe for this environment."

## Identity boundaries

| Concern | Purpose |
| --- | --- |
| Sign-in provider | Establishes the Backstage user identity. |
| Sign-in resolver | Maps provider identity to a catalog user or approved identity. |
| Delegated access | Obtains provider credentials for user-authorized external API calls. |
| Technical integration | Lets catalog providers or backend modules access external systems. |
| Permission policy | Authorizes actions after identity is established. |

## Procedure

1. Detect repository mode, Backstage version, backend system, environment, and existing providers.
2. Identify the desired sign-in identity and catalog user mapping.
3. Identify delegated provider access and service integration credentials separately.
4. Read current first-party auth documentation for the selected provider and target version.
5. Configure the provider and backend module through supported APIs.
6. Keep client secrets, private keys, and tokens in environment or approved secret storage.
7. Validate base URLs, callback URLs, resolver behavior, session or token settings, and logout.
8. Test successful login, denied or unmapped identity, expired credentials, and least-privilege
   permissions without logging secrets or tokens.
9. Require approval before changing production sign-in identity or disabling authentication.

## Built-in provider focus

- GitHub: use `@backstage/plugin-auth-backend-module-github-provider`, configure the OAuth or
  GitHub App callback, and select a resolver such as username, email, or stable user ID mapping.
- Microsoft Entra ID: use `@backstage/plugin-auth-backend-module-microsoft-provider`, configure
  client ID, tenant ID, secret, redirect URI, required delegated scopes, and a stable resolver.
- Keep GitHub App technical integration and Azure DevOps or Microsoft Graph technical credentials
  separate from either sign-in provider.
- Verify outbound access to provider identity endpoints and test admin-consent requirements.

## Limits

- Guest auth is for explicitly approved development or trusted scenarios, not a silent production
  fallback.
- A provider's profile or email claim is not authorization.
- Do not invent resolver behavior when catalog ownership or identity mapping is unknown.

## Open Horizons integration

- Scope authentication changes to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons identity, Backstage, managed-identity, AKS, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage authentication result

**Provider:** <provider>
**Environment:** <environment>
**Identity source:** <source>
**Resolver:** <resolver and mapping>

| Check | Expected | Result |
| --- | --- | --- |

### External secrets
- `<ENV_NAME>`: <purpose only>
```

## Quality gate

- [ ] Sign-in, delegation, integration credentials, and permission policy are separated.
- [ ] Provider and resolver behavior matches current first-party guidance.
- [ ] Callback and base URLs match the environment.
- [ ] Secrets remain external and absent from logs.
- [ ] Positive and negative sign-in paths are validated.
- [ ] Production auth mutations are explicitly approved.

## References

- [Backstage authentication](https://backstage.io/docs/auth/)
- [GitHub provider](https://backstage.io/docs/auth/github/provider)
- [Microsoft Entra ID provider](https://backstage.io/docs/auth/microsoft/provider)

---
name: backstage-auth
description: >-
  Apply Backstage sign-in, identity resolver, delegated access, service auth, and
  permission-boundary conventions. Use when editing auth configuration or provider modules.
paths:
  - app-config*.yaml
  - "packages/app/**/*.{ts,tsx}"
  - "packages/backend/**/*.{ts,tsx}"
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/instructions/backstage-auth.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Authentication Conventions

These instructions apply to Backstage authentication and identity wiring. They are authoritative
for provider separation, resolver mapping, callbacks, secret handling, and auth-to-permission
boundaries in matched files; deployment security policy and current provider documentation win on
conflict.

## Identity and Provider Boundaries

- Choose one normal sign-in identity even when several providers offer delegated access.
- Map provider identities to catalog users through explicit resolvers.
- Keep GitHub or Microsoft technical integration credentials separate from user sign-in.
- Use the auth and HTTP auth services for backend credentials and request authentication.
- Enforce authorization through the permission framework after authentication.

## GitHub and Microsoft Entra ID

- GitHub callbacks end at `/api/auth/github/handler/frame`.
- Microsoft callbacks end at `/api/auth/microsoft/handler/frame`.
- Use the GitHub provider module or Microsoft provider module matching the target version.
- Store client secret, tenant ID, and provider credentials in environment or secret storage.
- Request only required delegated scopes and document admin-consent requirements.

## Conventions

| Rule | Rationale |
| --- | --- |
| Test unmapped and denied identities. | Happy-path login does not prove resolver safety. |
| Keep guest access environment-gated. | Development convenience must not leak into production. |
| Protect backend and frontend exposure independently. | A sign-in page alone does not protect the frontend bundle. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Validate callback, logout, session, and resolver behavior. | Guess catalog identity mappings. |
| Keep secrets external and redacted. | Commit OAuth or Entra credentials. |
| Apply permissions after identity. | Treat profile claims as authorization. |

## Checklist Before Opening a PR

- [ ] Sign-in and delegated provider access are separate.
- [ ] Resolver choice and catalog identity mapping are tested.
- [ ] Callback URLs and environment selection match deployment.
- [ ] Provider secrets and scopes are least-privilege and external.
- [ ] Guest, unmapped, expired, and denied paths are covered.
- [ ] Production identity changes received approval.

## References

- [Backstage authentication](https://backstage.io/docs/auth/)
- [GitHub provider](https://backstage.io/docs/auth/github/provider)
- [Microsoft provider](https://backstage.io/docs/auth/microsoft/provider)

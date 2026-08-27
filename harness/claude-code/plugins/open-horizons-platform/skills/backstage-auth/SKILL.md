---
name: backstage-auth
description: >-
  Use when editing Backstage sign-in, identity resolution, service authentication, or permission
  boundaries.
paths:
  - backstage/app-config*.yaml
  - backstage/packages/app/src/components/SignInPage/**/*.tsx
  - backstage/packages/backend/src/**/*.ts
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/backstage-auth.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Authentication and Authorization

## Conventions

- Derive user identity from a validated Backstage auth context, never from request bodies or untrusted headers.
- Keep sign-in identity resolution separate from delegated access to GitHub, Azure, or other providers.
- Require explicit, deterministic ownership or group resolution; ambiguous matches must fail without silently choosing a user.
- Authenticate backend-to-backend calls with service credentials and validate issuer, audience, expiry, and approved caller.
- Apply permission checks at backend resource and action boundaries; hiding a frontend control is not authorization.
- Keep guest access local-only and visibly isolated from production overlays.
- Resolve client secrets and signing material from environment-backed secret stores, not source or frontend-visible config.
- Return generic authentication errors externally while retaining redacted correlation evidence internally.

## Verification

- Tests cover valid sign-in, unresolved identity, wrong audience, expired credentials, and denied permissions.
- Production configuration has no guest fallback or literal credential.
- Trusted actor and trusted service identities remain distinct throughout requests.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Validate identity and authorization independently at backend boundaries. | Trust request identity fields, hidden UI, or a successful sign-in as authorization. |
| Keep secrets external and errors safely redacted. | Put credentials in source, browser configuration, or user-visible errors. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Actor, service, delegated-provider, and permission identities remain distinct.
- [ ] Valid, unresolved, expired, wrong-audience, and denied cases are tested.
- [ ] Production configuration contains no guest fallback or literal credential.
- [ ] No unrelated edits or unresolved placeholders remain.

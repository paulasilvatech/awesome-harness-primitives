---
applyTo: "backstage/app-config*.yaml,backstage/packages/app/src/components/SignInPage/**/*.tsx,backstage/packages/backend/src/**/*.ts"
description: "Use when editing Backstage sign-in, identity resolution, service authentication, or permission boundaries."
---

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

---
applyTo: "backstage/app-config*.yaml,backstage/packages/backend/src/**/*.ts,backstage/catalog/*.yaml,backstage/catalog-info.yaml"
description: "Use when editing Backstage integrations with GitHub, Azure, Azure DevOps, or other external providers."
---

# Backstage External Integrations

## Conventions

- Use the least-privilege credential type supported by the provider, preferring GitHub Apps, managed identity, workload identity, or short-lived delegated tokens.
- Keep provider sign-in, catalog discovery, backend service access, and user-delegated actions as separate trust boundaries.
- Resolve credentials from environment-backed secret stores and keep them out of catalog entities, logs, and frontend config.
- Scope organizations, repositories, projects, tenants, and subscriptions explicitly; reject requests outside the configured boundary.
- Bound scheduled discovery and event processing with stable task IDs, timeouts, retries, and idempotency.
- Validate webhook signatures and event provenance before processing.
- Normalize provider failures into safe integration errors while retaining redacted correlation metadata.
- Keep provider-specific code behind typed adapters so catalog and UI contracts remain stable.

## Verification

- Integration tests use fixtures or mocks rather than production credentials.
- Permission scopes are documented by the owning configuration and match actual operations.
- Discovery, webhook replay, throttling, and provider-unavailable paths remain deterministic.

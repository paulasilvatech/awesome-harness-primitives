---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Python Dataverse SDK conventions for setup, OAuth configuration, client reuse, CRUD operations, batching, pagination, throttling, retries, and logging.

# Dataverse Python Conventions — SDK Authentication and Basic Operations

These instructions apply to Python code that installs, configures, authenticates, or uses the Dataverse Python SDK. They are authoritative for getting-started SDK usage, OAuth configuration, environment variables, CRUD operations, batching, pagination, throttling, retries, and troubleshooting in matched `**/*.py` files; project-specific security and deployment rules win when they impose stricter secret handling or identity requirements.

## Runtime and Installation

Use Python 3.10 or newer and isolate SDK dependencies in a virtual environment. Install the Dataverse SDK with `pip install dataverse-sdk`, and add supporting packages such as `python-dotenv` only when the project uses `.env` files for local development.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install dataverse-sdk python-dotenv
```

Keep dependency versions in the project's existing dependency file when one exists. Do not leave one-off local installs undocumented.

## Authentication and Configuration

Use OAuth with an Azure AD app registration for service-to-service access. Store tenant, client ID, client secret, and resource URL outside source code, preferably in environment variables loaded from `.env` only for local development.

| Setting | Purpose |
| --- | --- |
| `DATAVERSE_TENANT_ID` | Azure AD tenant used for OAuth. |
| `DATAVERSE_CLIENT_ID` | App registration client ID. |
| `DATAVERSE_CLIENT_SECRET` | App registration secret; keep out of source control. |
| `DATAVERSE_RESOURCE_URL` | Dataverse environment URL or resource URL used by the SDK. |

Validate required settings at process startup and fail with a clear message if any are missing. Never print secrets in logs or exception messages.

## SDK Usage and CRUD Operations

Reuse authenticated clients instead of creating a new client for every operation to avoid frequent `re-auth`. Keep SDK calls behind small service functions or classes so query, Create/update, create, update, delete, and batch operations have consistent error handling and logging.

| Task | Convention |
| --- | --- |
| Query tables | Use the SDK query mechanisms and request only needed columns when possible. |
| Create rows | Validate required fields before sending the create request. |
| Update rows | Send only intended changes and keep identifiers explicit. |
| Delete rows | Guard destructive operations with clear caller intent. |
| Batch operations | Group compatible operations where the SDK and Dataverse limits allow batching. |
| Pagination | Iterate all pages deliberately; do not assume the first response contains every row. |
| Throttling | Respect retry-after guidance and add bounded retries for transient failures. |

## Reliability and Troubleshooting

Add retries for transient HTTP failures, throttling, and network interruptions. Use exponential backoff with a maximum retry count so failures do not loop forever. Log request purpose, table name, correlation identifiers, status codes, and retry decisions; omit tokens, secrets, and full sensitive payloads.

## Good / Bad Examples

The examples below illustrate environment-based configuration and client reuse.

**Good:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

required = ["DATAVERSE_TENANT_ID", "DATAVERSE_CLIENT_ID", "DATAVERSE_CLIENT_SECRET", "DATAVERSE_RESOURCE_URL"]
missing = [name for name in required if not os.getenv(name)]
if missing:
    raise RuntimeError(f"Missing Dataverse settings: {', '.join(missing)}")
```

Why: Configuration is read from environment variables, secrets stay out of source, and missing settings fail early.

**Bad:**

```python
CLIENT_SECRET = "paste-secret-here"

for row in rows:
    client = create_dataverse_client(CLIENT_SECRET)
    client.create("accounts", row)
```

Why: The secret is hardcoded and the client is recreated repeatedly instead of being reused.

## Conventions

| Rule | Rationale |
|---|---|
| Use Python 3.10+ and a virtual environment for Dataverse SDK work | SDK dependencies remain isolated and compatible with modern Python features. |
| Install with `pip install dataverse-sdk` and record dependencies in the project manifest | Reproducible installs prevent local-only behavior. |
| Configure OAuth through Azure AD app registration and environment variables | Secrets stay outside code and authentication remains standard. |
| Reuse Dataverse clients across operations | Frequent re-authentication wastes time and can trigger throttling. |
| Handle CRUD, batch operations, pagination, and throttling explicitly | Dataverse responses may be partial, rate-limited, or transiently unavailable. |
| Log troubleshooting metadata without secrets | Operators can diagnose failures without leaking credentials. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `.env` with `python-dotenv` for local development secrets | Commit tenant IDs, client secrets, or resource URLs that should be private. |
| Validate `DATAVERSE_TENANT_ID`, `DATAVERSE_CLIENT_ID`, `DATAVERSE_CLIENT_SECRET`, and `DATAVERSE_RESOURCE_URL` at startup | Let authentication fail later with unclear missing-setting errors. |
| Reuse one authenticated SDK client per process or request scope | Create and authenticate a new client for every row. |
| Implement bounded retries and pagination loops | Assume one request always succeeds and returns all data. |
| Log table names, status codes, and retry decisions | Log OAuth tokens, secrets, or full sensitive payloads. |

## Checklist Before Opening a PR

- [ ] Python code targets Python 3.10+ and uses the project's dependency management convention.
- [ ] `dataverse-sdk` installation is documented or captured in the dependency manifest.
- [ ] OAuth configuration uses environment variables rather than hardcoded secrets.
- [ ] Required Dataverse settings are validated before SDK calls run.
- [ ] Clients are reused and SDK access is centralized behind clear functions or services.
- [ ] Query, create, update, delete, batch, pagination, and throttling paths handle errors deliberately.
- [ ] Logs aid troubleshooting without exposing secrets or sensitive payloads.

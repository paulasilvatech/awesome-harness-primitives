---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-authentication-security.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces authentication and security conventions for Python Dataverse SDK apps that use Azure Identity credentials, DataverseClient configuration, secure secret handling, tenant isolation, and Dataverse permissions.

# Dataverse Python Authentication Conventions — Azure Identity and Security

These instructions apply to Python Dataverse SDK code matched by `**/*.py`. They are authoritative for Azure Identity credential selection, `DataverseClient` authentication, secure configuration, token lifecycle, Dataverse-specific security, troubleshooting, and environment handling; organization identity policy, app registration governance, and platform secret-management standards win where they define stricter controls.

## Credential Selection

Use token-based authentication through Azure Identity instead of connection strings or hardcoded secrets. Token-based credentials support least privilege, scope access to intended apps, work across local development and Azure hosting, and avoid stored secrets when managed identity is available.

| Scenario | Credential | Convention |
| --- | --- | --- |
| Multi-environment apps | `DefaultAzureCredential` | Prefer this as the default path for dev, test, and production because it tries environment credentials, developer logins, and managed identity without environment-specific code. |
| Local interactive development | `InteractiveBrowserCredential` | Use only for developer workstations or desktop apps with UI; it opens a browser and caches tokens after first sign-in. |
| Unattended jobs outside Azure | `ClientSecretCredential` | Use for scheduled jobs, scripts, and on-premises services only when managed identity is unavailable. |
| Azure-hosted workloads | `ManagedIdentityCredential` | Prefer on App Service, Azure Functions, AKS, VMs, and other Azure resources because Azure manages token acquisition and refresh. |
| Multi-tenant routing | `DefaultAzureCredential` plus tenant-aware URL resolution | Resolve the Dataverse organization per tenant and keep tenant isolation explicit. |

`DefaultAzureCredential` may use `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_CLIENT_SECRET`; Visual Studio Code login; Azure CLI credentials from `az login`; Azure PowerShell credentials from `Connect-AzAccount`; and managed identity on Azure resources. Keep this chain unless a credential source is explicitly unsafe for the deployment.

## Client Construction and Configuration

Construct `DataverseClient` with an authenticated Azure Identity credential and a Dataverse `base_url` such as `https://myorg.crm.dynamics.com`. Keep the URL in configuration, not code, when it varies by environment.

| Setting or type | Convention | Rationale |
| --- | --- | --- |
| `DATAVERSE_URL` | Store the Dataverse URL in an environment variable or secure app setting. | Deployment changes do not require code edits. |
| `DataverseConfig` | Use for SDK logging and HTTP settings. | Configuration remains explicit and reviewable. |
| `cfg.logging_enable = True` | Enable only when detailed SDK logs are needed and logs do not expose secrets. | Authentication debugging needs context, but logs can leak operational details. |
| `cfg.http_timeout = 30` | Set a bounded request timeout in seconds. | Calls fail predictably instead of hanging indefinitely. |
| `cfg.http_retries = 3` | Set an explicit retry count when the SDK and workload support it. | Transient failures get a bounded retry policy. |
| `cfg.http_backoff = 1` | Start backoff at one second unless service guidance requires a different value. | Retries avoid immediate pressure on the service. |
| `cfg.connection_timeout = 5` | Bound connection establishment time. | Network failures surface quickly. |

Use `from PowerPlatform.Dataverse.client import DataverseClient`, `from PowerPlatform.Dataverse.core.config import DataverseConfig`, and Azure Identity imports directly where clients are composed. Reuse the same credential and client lifecycle when possible; repeated client creation can create unnecessary connections and token requests.

## Secret Handling and Least Privilege

Never hardcode tenant IDs, client IDs, or client secrets in source code. Read `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET` from the environment for `ClientSecretCredential`, or retrieve secrets with `SecretClient` from Azure Key Vault at a `vault_url` such as `https://<your-key-vault-name>.vault.azure.net` when policy requires a vault.

Development `.env` files that contain `DATAVERSE_URL`, `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, or `AZURE_CLIENT_SECRET` must be git-ignored. Production secrets belong in Azure Key Vault, managed identity, platform app settings, or another approved secret store. Rotate service-principal secrets regularly, time-limit credentials where possible, and grant only the Dataverse table and action permissions the app actually needs.

Avoid broad Dataverse roles for applications. Do not use **System Administrator** for app integrations unless a temporary break-glass process approves it. Prefer custom roles scoped to required tables and operations; use roles such as **Sales Manager** or **Service Representative** only when they match the business need.

## Authentication Monitoring and Token Lifecycle

Log authentication outcomes without logging tokens, secrets, or full credential payloads. Use a logger such as `logging.getLogger("dataverse_auth")`, record success at `info`, record authentication failures at `error`, and re-raise exceptions so callers cannot continue with an unauthenticated client.

Azure Identity caches and refreshes tokens automatically. Do not manually decode or persist access tokens except for diagnostics, and never write token values to logs. If an operation can fail because of token expiration, catch `ClientAuthenticationError`, retry a small bounded number of times such as `max_retries=2`, sleep briefly between attempts, and then raise the original failure.

## Multi-Tenant and Dataverse Security

Keep tenant isolation explicit. A tenant-aware helper such as `get_client_for_tenant(tenant_id: str) -> DataverseClient` may map a tenant to an organization through `get_org_for_tenant(tenant_id)` and build `base_url = f"https://{get_org_for_tenant(tenant_id)}.crm.dynamics.com"`; the mapping source must be trusted configuration or a database, not user-supplied host text.

Dataverse row-level security is enforced by the user's or application's security role. When code uses `InteractiveBrowserCredential`, each signed-in user sees only records allowed by that user's Dataverse roles. When code uses a service principal or managed identity, the app identity's roles control access, so least privilege is the only protection against over-broad reads and writes.

## Troubleshooting Authentication

Handle known authentication failures with targeted diagnostics and safe messages.

| Failure | Signal | Diagnostic convention |
| --- | --- | --- |
| Access denied | `DataverseError` with `status_code == 403` | Report that the user or app lacks Dataverse permissions and verify the Dataverse security role assignment. |
| Invalid credentials | HTTP `401` or Azure Identity failure | Check the active credential source; for local development, use `DefaultAzureCredential(exclude_cli_credential=False, exclude_powershell_credential=False)` and refresh with `az login` when appropriate. |
| Invalid tenant | Token audience or tenant mismatch | Verify `AZURE_TENANT_ID`, decode only non-sensitive claims for diagnostics, and compare the `tid` claim with the intended tenant. |
| Wrong Dataverse audience | `get_token` fails for `https://<your-org>.crm.dynamics.com/.default` | Confirm the Dataverse URL and app registration permissions. |

Do not run `subprocess.run(["az", "login"])` in production services. Restrict interactive remediation to developer tooling.

Use helper names such as `create_with_auth_retry`, `get_user_client`, `get_client_for_tenant`, and `DataverseSession` only when they express real lifecycle boundaries. If context managers define `__exit__`, keep `exc_type`, `exc_val`, and `exc_tb` parameters even when cleanup is empty so the signature remains conventional.

## Preserved Security Vocabulary

The following identifiers and placeholders remain meaningful in this domain and must not be removed from examples without an equivalent replacement.

| Category | Identifiers |
| --- | --- |
| Secret names and vault calls | `dataverse-client-secret`, `get_secret`, `EXPOSED` as an example warning label |
| Retry and table parameters | `create_with_auth_retry`, `table_name`, `max_retries=2` |
| User-context helpers | `get_user_client`, `user_username`, `tenant-specific`, `multi-tenant` |
| Operational wording | `User/app`, `auto-rotation`, `re-authentication`, `GOOD` as an example label |

## Good / Bad Examples

The examples below illustrate secure credential construction and configuration.

**Good:**

```python
import os
from azure.identity import DefaultAzureCredential
from PowerPlatform.Dataverse.client import DataverseClient
from PowerPlatform.Dataverse.core.config import DataverseConfig

cfg = DataverseConfig()
cfg.http_timeout = 30
cfg.connection_timeout = 5

credential = DefaultAzureCredential()
client = DataverseClient(
    base_url=os.environ["DATAVERSE_URL"],
    credential=credential,
    config=cfg,
)
records = client.get("account")
```

Why: The code uses the default Azure Identity chain, keeps the Dataverse URL in configuration, and sets bounded HTTP behavior without exposing secrets.

**Bad:**

```python
from azure.identity import ClientSecretCredential
from PowerPlatform.Dataverse.client import DataverseClient

credential = ClientSecretCredential(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-secret-key",
)
client = DataverseClient(base_url="https://myorg.crm.dynamics.com", credential=credential)
```

Why: The code hardcodes secret material and environment-specific values, making credential leakage and unsafe reuse likely.

## Conventions

| Rule | Rationale |
| --- | --- |
| Prefer `DefaultAzureCredential` for apps that run across environments. | One credential chain supports local developer login, service principal configuration, and managed identity. |
| Use `ManagedIdentityCredential` for Azure-hosted apps whenever Dataverse permissions can be granted to the managed identity. | Managed identity removes stored client secrets and handles token refresh. |
| Use `ClientSecretCredential` only with `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET` from secure configuration. | Service-principal secrets are high-value credentials and must not live in source. |
| Keep `DATAVERSE_URL` and tenant-to-organization mappings outside code. | Environment and tenant changes remain deploy-time configuration. |
| Configure `DataverseConfig` for logging, timeout, retry, backoff, and connection timeout intentionally. | Defaults may not match security, reliability, or diagnostic needs. |
| Log authentication events without secrets or tokens. | Operators need auditability without credential disclosure. |
| Retry `ClientAuthenticationError` only with small bounded retries. | Token refresh races can recover, but unbounded retry loops hide real permission failures. |
| Assign minimal Dataverse security roles to users, service principals, and managed identities. | Dataverse row-level security can only protect data if the identity is scoped correctly. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use token-based Azure Identity credentials. | Use connection strings or hardcoded Dataverse credentials. |
| Use `az login` or developer credentials only for local development. | Depend on interactive login in services, scheduled jobs, or production hosts. |
| Store secrets in Azure Key Vault, managed identity, app settings, or approved environment variables. | Commit `.env` files or source code containing `AZURE_CLIENT_SECRET`. |
| Grant custom least-privilege Dataverse roles. | Give application identities **System Administrator** by default. |
| Use `SecretClient` with `DefaultAzureCredential` when retrieving approved vault secrets. | Print, log, or persist secret values after retrieval. |
| Validate tenant IDs and organization mappings before constructing `base_url`. | Build `https://{get_org_for_tenant(tenant_id)}.crm.dynamics.com` from untrusted user input. |
| Handle `401`, `403`, and invalid-tenant failures with safe diagnostics. | Swallow authentication failures and continue with partial behavior. |

## Checklist Before Opening a PR

- [ ] Dataverse clients use Azure Identity credentials rather than connection strings or hardcoded secrets.
- [ ] `DefaultAzureCredential`, `InteractiveBrowserCredential`, `ClientSecretCredential`, or `ManagedIdentityCredential` matches the runtime scenario.
- [ ] `DATAVERSE_URL`, `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET` come from approved configuration or secret stores.
- [ ] No token, password, client secret, or full credential payload is logged, printed, or committed.
- [ ] `DataverseConfig` timeout, retry, backoff, connection timeout, and logging choices are intentional.
- [ ] Service principals and managed identities have minimal Dataverse security roles.
- [ ] Multi-tenant code validates tenant-to-organization mappings and isolates clients by tenant.
- [ ] Authentication failures preserve the original exception and provide safe operator diagnostics.
- [ ] Local-only commands such as `az login` are not embedded in production code paths.

## References

- Azure Identity Client Library: https://learn.microsoft.com/en-us/python/api/azure-identity
- Authenticate to Azure Services: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview
- Azure Key Vault for Secrets: https://learn.microsoft.com/en-us/azure/key-vault/general/overview
- Dataverse Security Model: https://learn.microsoft.com/en-us/power-platform/admin/security/security-overview
- Example Dataverse URL: https://myorg.crm.dynamics.com
- Placeholder Key Vault URL: https://<your-key-vault-name>.vault.azure.net
- Placeholder Dataverse token scope: https://<your-org>.crm.dynamics.com/.default
- Tenant-derived Dataverse URL pattern: https://{get_org_for_tenant(tenant_id)}.crm.dynamics.com

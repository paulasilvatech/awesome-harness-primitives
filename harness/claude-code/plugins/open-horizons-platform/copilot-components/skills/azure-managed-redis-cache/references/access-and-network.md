# Access and Network for Azure Managed Redis

Secure the cache the same way you would a database. Prefer identity over keys and private networking for sensitive data.

## Authentication

- **Microsoft Entra (AAD) with managed identity.** Assign the app or agent a managed identity and grant it a Redis data access role. Connect with `DefaultAzureCredential`. This avoids long-lived keys and works when tenant policy disables local auth.
- **Access keys.** Available but discouraged. If used, store in Key Vault and rotate. Do not embed in code.

## Network

- **Private endpoint.** Place Redis behind a private endpoint and integrate with the application VNet. Set `publicNetworkAccess` to disabled when the data requires it.
- **Public with firewall.** If public access is needed (for example early development), restrict by firewall rules. `publicNetworkAccess` is a required property on the resource, so set it explicitly.
- **DNS.** Plan private DNS zones for the private endpoint so the host name resolves inside the VNet.
- **TLS.** Require TLS for all client connections.

## Authorization and isolation

- Grant least privilege data roles. Separate read and write identities where it matters.
- Namespace keys by tenant and user so a shared instance cannot leak data across boundaries.

## Checklist

- Managed identity plus AAD auth, no embedded keys.
- Private endpoint and disabled public access for sensitive data.
- TLS enforced.
- Tenant and user key namespacing.
- Keys, if any, in Key Vault with rotation.

## Sources

- [Authenticate to Azure Managed Redis with Microsoft Entra ID](https://learn.microsoft.com/azure/redis/entra-for-authentication)
- [Azure Managed Redis network isolation](https://learn.microsoft.com/azure/redis/)
- [DefaultAzureCredential](https://learn.microsoft.com/azure/developer/intro/azure-developer-create-resources)

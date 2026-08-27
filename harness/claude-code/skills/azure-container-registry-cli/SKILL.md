---
name: azure-container-registry-cli
description: >-
  Manage Azure Container Registry with az acr CLI commands for registries, images, cloud builds,
  ACR Tasks, authentication, tokens, geo-replication, networking, purge, import, and diagnostics.
  Use when working with ACR, az acr, pushing or importing container images in Azure, or Azure
  Container Registry operations.
---

<!-- Generated from harness/github-copilot/skills/azure-container-registry-cli/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Container Registry CLI

Use the Azure CLI `az acr` command group to create registries, authenticate clients, build or import images, manage repositories and tags, configure security and networking, and diagnose Azure Container Registry behavior.

## When to invoke

- "Create an Azure Container Registry and push an image."
- "Use az acr build instead of local Docker."
- "Diagnose ACR login or pull permissions."
- "Import or purge images in Azure Container Registry."
- "Configure ACR geo-replication, Private Link, or repository tokens."

## Prerequisites and context

`az acr` ships with the core Azure CLI; no extension is required for normal registry work. The `acrtransfer` extension is only needed for export/import pipeline commands.

```bash
# Install Azure CLI
brew install azure-cli
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
winget install Microsoft.AzureCLI

# Sign in and select subscription
az login
az account set --subscription {subscription-id}
```

Confirm the resource group, registry name, subscription, SKU, and identity model before running mutating commands.

## Command map

| Need | Command pattern | Notes |
| --- | --- | --- |
| Registry lifecycle | `az acr create --resource-group {rg} --name {registry} --sku Standard` | SKU is `Basic`, `Standard`, or `Premium`. |
| Docker/Podman login | `az acr login --name {registry}` | Uses local credential helper. Use `--expose-token` for token-based flows. |
| Cloud build | `az acr build --registry {registry} --image app:v1 .` | No local Docker daemon required. |
| Server-side copy | `az acr import --name {registry} --source mcr.microsoft.com/hello-world:latest` | Avoids local pull and push. |
| Repositories | `az acr repository list --name {registry} --output table` | Inventory repositories. |
| Tags | `az acr repository show-tags --name {registry} --repository app --orderby time_desc` | Sort by recency for cleanup. |
| Health | `az acr check-health --name {registry} --yes` | Diagnoses Docker daemon, network, auth, and config. |
| Usage | `az acr show-usage --name {registry}` | Review quota and storage. |

Common task phrases include pushing/importing/purging images and replacing local pull/push loops with server-side operations.

## ACR principles

| Principle | Why it matters |
| --- | --- |
| Prefer `az acr build` and ACR Tasks over `docker build` plus `docker push`. | Builds run in Azure, work without a local daemon, and integrate with source, base-image, and timer triggers. |
| Prefer `az acr import` for registry-to-registry movement. | Import is server-side, faster, and does not require local storage. |
| Never enable the admin user for production. | Use Microsoft Entra identities, managed identities, RBAC roles `AcrPull` and `AcrPush`, ABAC roles `Container Registry Repository Reader` and `Container Registry Repository Writer`, or repository-scoped tokens. |
| Treat Premium-only features as design choices. | Geo-replication, private endpoints, retention policies, connected registries, and agent pools require Premium. Repository-scoped tokens work in all tiers; zone redundancy is automatic in supported regions. |
| Distinguish untag from delete. | Removing a tag may leave manifests; deleting manifests removes content. Use retention, soft delete, and purge intentionally. |

The repository command family covers List/show/delete/untag actions, Push/delete webhooks, artifact cache pull-through rules, soft-delete configuration, `content-trust`, and git/base-image/timer task triggers. ABAC-enabled registries may use `Container Registry Repository Reader`/`Writer` for scoped reads and writes.

## CLI structure

```text
az acr
├── create / delete / list / show / update
├── login
├── check-health / check-name / show-usage
├── build
├── run
├── task
├── agentpool
├── import
├── repository
├── manifest
├── credential
├── token / scope-map
├── replication
├── network-rule
├── private-endpoint-connection
├── config
├── cache / credential-set
├── webhook
├── connected-registry
└── export-pipeline / import-pipeline / pipeline-run
```

## Procedure

1. Run `az account show` and confirm the target subscription if the task mutates resources.
2. Choose the smallest command group that matches the task: lifecycle, auth, build, repository, networking, or diagnostics.
3. Prefer read-only `show`, `list`, `show-tags`, `show-usage`, and `check-health` commands before destructive updates.
4. For builds, imports, purges, retention, private endpoints, geo-replication, or repository-scoped tokens, read the relevant bundled reference first.
5. Execute the command with explicit `--resource-group`, `--name`, `--repository`, `--image`, `--output`, and confirmation flags rather than relying on defaults.
6. Report the command, registry, affected repository or tag, and any quota, auth, or network diagnostic result.

## Progressive disclosure and bundled resources

| Resource | Read when | Covers |
| --- | --- | --- |
| `references/auth-and-security.md` | Login, permissions, CI/CD, AKS pull access, tokens, or admin-user questions. | `az acr login`, `--expose-token`, Entra RBAC, service principals, managed identities, `--attach-acr`, repository-scoped tokens, scope maps, content trust. |
| `references/build-and-tasks.md` | Building images in Azure or automating builds. | `az acr build`, `az acr run`, multi-step task YAML, `az acr task`, git triggers, base-image triggers, timer triggers, logs, runs, agent pools. |
| `references/images-and-artifacts.md` | Repositories, tags, cleanup, storage costs, artifact cache. | `az acr import`, repository and manifest commands, untag vs delete, `acr purge`, image locking, retention policy, soft delete, `show-usage`. |
| `references/networking-and-geo.md` | Multi-region, private access, edge, or transfer scenarios. | Geo-replication, zone redundancy, private endpoints, network rules, dedicated data endpoints, connected registries, registry transfer pipelines. |

## Gotchas

- **Admin user is not production auth**: enabling it creates broad registry credentials; use identity-based pull and push instead.
- **Private endpoints change DNS and network paths**: a successful role assignment does not prove network reachability.
- **ACR Tasks are not local builds**: build context, secrets, and Dockerfile paths must be valid from the cloud task environment.
- **`acrtransfer` is separate**: install it only for export/import pipeline workflows, not for normal `az acr import`.

## Output template

```markdown
## Azure Container Registry CLI result

**Status:** complete | needs input | blocked
**Registry:** `{registry}`
**Subscription:** `{subscription-id}`
**Operation:** <lifecycle | auth | build | import | repository | networking | diagnostics>

### Commands
```bash
<az acr command executed or recommended>
```

### Result
- Affected resource: <registry/repository/tag/task>
- Output or diagnostic evidence: <summary>
- Follow-up: <next command or none>
```

## Quality gate

- [ ] The target subscription, resource group, registry, and SKU assumptions are explicit.
- [ ] Mutating operations use explicit flags and avoid relying on ambient defaults.
- [ ] Production auth avoids the admin user unless the user explicitly accepts the risk.
- [ ] Premium-only features are identified before commands are recommended.
- [ ] Image cleanup distinguishes tag removal, manifest deletion, retention, soft delete, and `acr purge`.
- [ ] The relevant bundled reference was read for auth, builds, artifacts, networking, or geo-replication work.

## References

- [Install Azure CLI on Linux](https://aka.ms/InstallAzureCLIDeb)

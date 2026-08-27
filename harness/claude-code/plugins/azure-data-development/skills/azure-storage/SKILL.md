---
name: azure-storage
description: >-
  Design and operate Azure Storage services including Blob Storage, File Shares, Queue Storage,
  Table Storage, and Data Lake, covering object storage, SMB file shares, async messaging, NoSQL
  key-value data, big data analytics, access tiers, and lifecycle management. Use when the user
  asks about blob storage, file shares, queue or table storage, Data Lake, uploading files or
  downloading blobs, storage accounts, hot, cool, cold, or archive access tiers, tier comparison
  and selection, or storage lifecycle management policies.
license: MIT
metadata:
  author: Microsoft
  version: 1.2.1
---

<!-- Generated from harness/github-copilot/plugins/azure-data-development/skills/azure-storage/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Storage Services

## When to invoke

- "Which storage access tier should I use for these blobs?"
- "Set up a storage account for file shares or queues."
- "Compare hot, cool, cold, and archive tiers."
- "Configure lifecycle management for old blobs."

## Services

| Service | Use When | MCP Tools | CLI |
|---------|----------|-----------|-----|
| Blob Storage | Objects, files, backups, static content | `azure__storage` | `az storage blob` |
| File Shares | SMB file shares, lift-and-shift | - | `az storage file` |
| Queue Storage | Async messaging, task queues | - | `az storage queue` |
| Table Storage | NoSQL key-value (consider Cosmos DB) | - | `az storage table` |
| Data Lake | Big data analytics, hierarchical namespace | - | `az storage fs` |

## MCP Server (Preferred)

When Azure MCP is enabled:

- `azure__storage` with command `storage_account_list` - List storage accounts
- `azure__storage` with command `storage_container_list` - List containers in account
- `azure__storage` with command `storage_blob_list` - List blobs in container
- `azure__storage` with command `storage_blob_get` - Download blob content
- `azure__storage` with command `storage_blob_put` - Upload blob content

**If Azure MCP is not enabled:** Run `/azure:setup` or enable via `/mcp`.

## CLI Fallback

```bash
# List storage accounts
az storage account list --output table

# List containers
az storage container list --account-name ACCOUNT --output table

# List blobs
az storage blob list --account-name ACCOUNT --container-name CONTAINER --output table

# Download blob
az storage blob download --account-name ACCOUNT --container-name CONTAINER --name BLOB --file LOCAL_PATH

# Upload blob
az storage blob upload --account-name ACCOUNT --container-name CONTAINER --name BLOB --file LOCAL_PATH
```

## Storage Account Tiers

| Tier | Use Case | Performance |
|------|----------|-------------|
| Standard | General purpose, backup | Milliseconds |
| Premium | Databases, high IOPS | Sub-millisecond |

## Blob Access Tiers

| Tier | Access Frequency | Cost |
|------|-----------------|------|
| Hot | Frequent | Higher storage, lower access |
| Cool | Infrequent (30+ days) | Lower storage, higher access |
| Cold | Rare (90+ days) | Lower still |
| Archive | Rarely (180+ days) | Lowest storage, rehydration required |

## Redundancy Options

| Type | Durability | Use Case |
|------|------------|----------|
| LRS | 11 nines | Dev/test, recreatable data |
| ZRS | 12 nines | Regional high availability |
| GRS | 16 nines | Disaster recovery |
| GZRS | 16 nines | Best durability |

## Service Details

For deep documentation on specific services:

- Blob storage patterns and lifecycle -> [Blob Storage documentation](https://learn.microsoft.com/azure/storage/blobs/storage-blobs-overview)
- File shares and Azure File Sync -> [Azure Files documentation](https://learn.microsoft.com/azure/storage/files/storage-files-introduction)
- Queue patterns and poison handling -> [Queue Storage documentation](https://learn.microsoft.com/azure/storage/queues/storage-queues-introduction)

## SDK Quick References

For building applications with Azure Storage SDKs, see the condensed guides:

- **Blob Storage**: [Python](references/sdk/azure-storage-blob-py.md) | [TypeScript](references/sdk/azure-storage-blob-ts.md) | [Java](references/sdk/azure-storage-blob-java.md) | [Rust](references/sdk/azure-storage-blob-rust.md)
- **Queue Storage**: [Python](references/sdk/azure-storage-queue-py.md) | [TypeScript](references/sdk/azure-storage-queue-ts.md)
- **File Shares**: [Python](references/sdk/azure-storage-file-share-py.md) | [TypeScript](references/sdk/azure-storage-file-share-ts.md)
- **Data Lake**: [Python](references/sdk/azure-storage-file-datalake-py.md)
- **Tables**: [Python](references/sdk/azure-data-tables-py.md) | [Java](references/sdk/azure-data-tables-java.md)

For full package listing across all languages, see [SDK Usage Guide](references/sdk-usage.md).

## Azure SDKs

For building applications that interact with Azure Storage programmatically, Azure provides SDK packages in multiple languages (.NET, Java, JavaScript, Python, Go, Rust). See [SDK Usage Guide](references/sdk-usage.md) for package names, installation commands, and quick start examples.

## Output template

```markdown
## Storage design result

**Status:** designed | configured | blocked
**Summary:** <one sentence covering scope and outcome>

### Details
Service and tier selection, redundancy, and lifecycle policy.

### Validation
- <check performed>: <result and evidence>
```

## Quality gate

- [ ] Tier and redundancy choices state their cost and durability trade-offs.
- [ ] Access uses Entra identity rather than account keys where supported.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was performed and its evidence is shown.
- [ ] Irreversible Azure actions were confirmed with the user first.

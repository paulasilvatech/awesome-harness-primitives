---
name: qdrant-version-upgrade
description: >-
  Plan Qdrant server, SDK, storage, cluster, rolling, and Qdrant Cloud upgrades without
  interrupting availability or risking data integrity. Use this skill when the user asks how to
  upgrade Qdrant, move between minor versions, match SDK and server versions, perform a rolling
  upgrade, or use qcloud for Qdrant Cloud upgrades.
---

<!-- Generated from harness/github-copilot/skills/qdrant-version-upgrade/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Qdrant version upgrade

Plan a Qdrant upgrade path that respects server/SDK compatibility, one-minor storage compatibility, replication requirements, rolling upgrade safety, and Qdrant Cloud automation.

## When to invoke

- "How do I upgrade Qdrant without downtime?"
- "Can I move from Qdrant 1.15.x to 1.17.x directly?"
- "Should I upgrade the SDK or Qdrant server first?"
- "Use qcloud to manage a Qdrant Cloud version upgrade."

## Compatibility rules

| Rule | Example | Required action |
| --- | --- | --- |
| Major and minor versions of Qdrant and SDK are expected to match. | Qdrant `1.17.x` with SDK `1.17.x`. | Target matching minor versions for final state. |
| Backward compatibility is tested between adjacent minor versions. | Qdrant `1.17.x` should work with SDK `1.16.x`; Qdrant server `1.16.x` should work with SDK `1.17.x` only for features available in `1.16.x`. | Avoid using new SDK features until the server is upgraded. |
| Upgrade SDK first for the next minor migration. | Move SDK `1.16.x` to `1.17.x`, then Qdrant server `1.16.x` to `1.17.x`. | Validate client behavior before server rollout. |
| Storage compatibility is guaranteed for one minor version. | Data stored with Qdrant `1.16.x` is expected to be compatible with Qdrant `1.17.x`. | Upgrade one minor at a time for self-managed clusters. |
| Multi-minor self-managed upgrades require stepping. | `1.15.x` → `1.16.x` → `1.17.x`. | Do not skip `1.16.x` when managing storage yourself. |
| Qdrant Cloud automates intermediate steps. | Cloud can upgrade `1.15.x` to `1.17.x` directly. | Use Cloud workflow or `qcloud` instead of manual node sequencing. |

## Rolling upgrade requirements

A Qdrant cluster with a replication factor of 2 or higher can be upgraded without downtime by performing a rolling upgrade: upgrade one node at a time while the other nodes continue to serve requests. Preserve the replication factor reference at https://qdrant.tech/documentation/operations/distributed_deployment/?s=replication-factor.

| Requirement | Check |
| --- | --- |
| Replication factor | Confirm every critical collection has replication factor `2` or higher before claiming zero downtime. |
| Backups or snapshots | Take and verify recoverable backups before changing server binaries or images. |
| Client compatibility | Upgrade SDK first and avoid new server features until rollout completes. |
| Node sequencing | Upgrade one node, wait for health and shard recovery, then proceed to the next node. |
| Observability | Monitor health, search/upsert errors, latency, shard state, and optimizer activity throughout rollout. |
| Rollback | Know whether rollback is safe for the storage version; after storage migration, restoring backup may be safer than downgrading. |

## Procedure

1. Record current Qdrant server version, SDK version, deployment type, replication factor, collection count, and backup status.
2. Choose the target version and build an adjacent-minor path. For self-managed multi-minor upgrades, include each intermediate minor version.
3. Upgrade the SDK to the next target minor first; keep feature usage within the old server's supported subset until server upgrade completes.
4. For self-managed replicated clusters, perform a rolling upgrade one node at a time and wait for health before continuing.
5. For Qdrant Cloud, use the managed upgrade flow or the `qcloud` CLI from https://github.com/qdrant/qcloud-cli.
6. Validate search, upsert, collection status, latency, and error rates after each step.

## Gotchas

- **Do not skip self-managed storage minors**: storage compatibility is only guaranteed for one minor version.
- **Do not promise zero downtime with replication factor 1**: rolling availability requires another replica serving traffic.
- **Do not use new SDK features against an older server**: adjacent compatibility covers only features available in the server version.
- **Do not downgrade casually**: once storage changes, restore-tested backups are the safe recovery path.

## Output template

```markdown
## Qdrant upgrade plan

**Status:** ready | needs prerequisite | blocked
**Current:** Qdrant `<server-version>`, SDK `<sdk-version>`
**Target:** Qdrant `<target-version>`, SDK `<target-sdk-version>`
**Deployment:** self-managed | Qdrant Cloud

| Step | Version/action | Availability risk | Validation |
| --- | --- | --- | --- |
| 1 | `<upgrade SDK or node>` | `<risk>` | `<health/search/upsert check>` |
| 2 | `<next minor or node>` | `<risk>` | `<health/search/upsert check>` |

**Rollback or recovery:** <backup, snapshot, or Cloud recovery plan>
```

## Quality gate

- [ ] Server and SDK major/minor compatibility is addressed.
- [ ] The SDK-first rule is applied for next-minor migration.
- [ ] Self-managed storage upgrades move one minor version at a time.
- [ ] Qdrant Cloud automation is distinguished from self-managed upgrade sequencing.
- [ ] Rolling upgrade guidance is limited to clusters with replication factor `2` or higher.
- [ ] Backup, validation, and rollback or recovery steps are included.

## References

- [Qdrant replication factor documentation](https://qdrant.tech/documentation/operations/distributed_deployment/?s=replication-factor)
- [qcloud CLI](https://github.com/qdrant/qcloud-cli)

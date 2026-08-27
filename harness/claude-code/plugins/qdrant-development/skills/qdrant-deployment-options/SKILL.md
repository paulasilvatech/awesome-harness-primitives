---
name: qdrant-deployment-options
description: >-
  Select the right Qdrant deployment model across local mode, Docker self-hosting, Qdrant Cloud,
  Hybrid Cloud, distributed deployment, and Qdrant EDGE. Use when someone asks how to deploy
  Qdrant, Docker vs Cloud, embedded Qdrant, local mode, self-hosted vs cloud, lowest latency, data
  residency, production readiness, or which deployment option fits a new vector search project.
---

<!-- Generated from harness/github-copilot/plugins/qdrant-development/skills/qdrant-deployment-options/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Qdrant deployment options

Choose a Qdrant deployment by matching the workload's operations model, latency target, production requirements, data residency, and compatibility needs to local mode, Docker self-hosting, Qdrant Cloud, Hybrid Cloud, distributed deployment, or Qdrant EDGE.

## When to invoke

- "How should I deploy Qdrant?"
- "Should I use Docker or Qdrant Cloud?"
- "Can I use local mode or embedded Qdrant for this project?"
- "Which Qdrant option gives the lowest latency?"
- "Do we need self-hosted Qdrant for data residency?"

## Deployment decision table

| Need | Recommended option | Why | Avoid when |
| --- | --- | --- | --- |
| Prototype, tests, CI/CD, learning | Local mode (Python only) | zero-dependency local mode: in-memory or disk-persisted, no server. | Production, benchmarking, or server data compatibility matters. |
| Real local server or simple self-hosted production | Docker | Full Qdrant Open Source feature set and minimal setup. | You cannot operate backups, upgrades, scaling, and monitoring. |
| Managed production with zero-ops | Qdrant Cloud | Handles upgrades, scaling, backups, monitoring, multi-version upgrades, `/sys_metrics`, managed resharding, and pre-configured alerts. | Data residency or infrastructure control requires your environment. |
| Managed control plane on your infrastructure | Hybrid Cloud | Qdrant Cloud management with customer infrastructure. | Qdrant Cloud satisfies residency and control needs; avoid unnecessary Kubernetes complexity. |
| Multi-node self-hosted production | Distributed deployment | Manual control over cluster topology and infrastructure. | The team cannot own distributed operations and failure handling. |
| Lowest possible latency, latency-critical workloads, or in-process search | Qdrant EDGE | In-process bindings to shard-level functions with no network overhead and server-compatible data format. | Distributed search is required; EDGE is single-node only. |

## Local and prototype rules

| Option | Use when | Technical rule |
| --- | --- | --- |
| Local mode | Python-only prototypes, tests, learning, and CI/CD pipelines. | Data format is not compatible with server; do not use it for production or benchmarking. |
| Docker quick start | You need a real Qdrant server locally. | Prefer Docker over local mode when testing network behavior, server configuration, or deployment parity. |

## Production rules

| Option | Operations owner | Production notes |
| --- | --- | --- |
| Docker self-hosted | Your team | Own upgrades, backups, scaling, monitoring, persistence, TLS, auth, and disaster recovery. |
| Distributed deployment | Your team | Configure multi-node clusters manually; validate shard replication, quorum, and failure modes. |
| Qdrant Cloud | Qdrant | Use for zero-downtime updates, automatic backups, managed resharding, and alerting. |
| Hybrid Cloud | Shared | Use only when data residency or infrastructure policy requires cloud management on your infrastructure. |
| Qdrant EDGE | Your application/runtime | Same data format as server and can sync through shard snapshots; limited to single-node feature set. |

## Criteria

- [ ] Managed operations versus full control is decided explicitly.
- [ ] Production versus prototype status is explicit.
- [ ] Network round-trip latency is acceptable, or Qdrant EDGE is considered.
- [ ] Data residency and infrastructure control requirements are stated.
- [ ] Backup, monitoring, scaling, and upgrade ownership is assigned.
- [ ] Compatibility needs are checked: local mode data is not server-compatible; Qdrant EDGE data format matches server.

## What not to do

| Anti-pattern | Why it is wrong | Correct choice |
| --- | --- | --- |
| Use local mode for production or benchmarking | It is not optimized and uses an incompatible data format. | Docker, Qdrant Cloud, Hybrid Cloud, or distributed deployment. |
| Self-host without monitoring and backups | Outages and data loss become silent until users notice. | Add operations plan or choose Qdrant Cloud. |
| Choose EDGE for distributed search | EDGE provides a single-node feature set only. | Use Qdrant Cloud or distributed deployment. |
| Pick Hybrid Cloud by default | It adds Kubernetes complexity without benefit when ordinary Qdrant Cloud works. | Use Hybrid Cloud only for residency/control requirements. |

## Output template

```markdown
### Qdrant deployment recommendation

**Status:** recommended | needs more context
**Recommended option:** Local mode | Docker | Qdrant Cloud | Hybrid Cloud | Distributed deployment | Qdrant EDGE
**Workload stage:** prototype | CI/CD | production | edge

| Decision factor | Answer | Impact |
| --- | --- | --- |
| Managed ops needed | yes/no | `<deployment consequence>` |
| Lowest latency required | yes/no | `<EDGE/server consequence>` |
| Data residency constraint | yes/no | `<Cloud/Hybrid/self-host consequence>` |
| Production readiness | yes/no | `<backup/monitoring consequence>` |
| Data compatibility required | yes/no | `<local mode/EDGE consequence>` |

**Do not use**
- `<rejected option>`: `<reason>`
```

## Quality gate

- [ ] The recommendation chooses exactly one primary deployment option.
- [ ] Local mode is rejected for production and benchmarking.
- [ ] Qdrant EDGE is rejected when distributed search is required.
- [ ] Self-hosted options include backup, monitoring, scaling, and upgrade ownership.
- [ ] Hybrid Cloud is justified by data residency or infrastructure-control requirements.
- [ ] The final answer preserves the relevant official Qdrant documentation link.

## References

- [Qdrant local mode quickstart](https://qdrant.tech/documentation/quickstart/)
- [Qdrant Docker quick start](https://qdrant.tech/documentation/quickstart/?s=download-and-run)
- [Distributed deployment](https://qdrant.tech/documentation/operations/distributed_deployment/)
- [Qdrant Cloud](https://qdrant.tech/documentation/cloud-quickstart/)
- [Hybrid Cloud](https://qdrant.tech/documentation/hybrid-cloud/)
- [Qdrant EDGE](https://qdrant.tech/documentation/edge/edge-quickstart/)

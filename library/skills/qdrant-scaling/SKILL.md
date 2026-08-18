---
name: "qdrant-scaling"
description: >-
  Guide Qdrant scaling decisions for data volume, query throughput, query latency, query volume, tenant growth, sharding, and capacity planning. Use when someone asks how many nodes are needed, whether to scale vertically or horizontally, why a cluster is slow, how to shard, or how to add capacity.
allowed-tools: [Read, Grep, Glob]
---

# Qdrant scaling

Classify the scaling pressure first, then choose the Qdrant scaling strategy that matches the bottleneck instead of adding nodes blindly.

## When to invoke

- "How many Qdrant nodes do I need?"
- "Our Qdrant data does not fit on one node."
- "Qdrant is slow; should we scale vertically or horizontally?"
- "How should we shard Qdrant for too many tenants?"
- "We need more QPS or lower query latency."

## Scaling goal classifier

| Goal | Primary symptom | Pulls toward | Tradeoff to watch | Deep reference |
| --- | --- | --- | --- | --- |
| Data volume | Dataset exceeds memory, disk, or operational capacity of one node. | Vertical scaling, horizontal sharding, tenant sharding, or sliding time windows. | More shards increase coordination and operational complexity. | `scaling-data-volume/SKILL.md` |
| Query throughput (QPS) | Single node cannot handle enough parallel queries. | Replicas, more nodes, load distribution, and query fan-out control. | Throughput tuning can increase per-query latency. | `scaling-qps/SKILL.md` |
| Query latency | One query is too slow even when QPS is acceptable. | Index tuning, payload filtering strategy, shard layout, hardware, and smaller search scope. | Latency and throughput are correlated sometimes, but not always. | `minimize-latency/SKILL.md` |
| Query volume | Each query returns too many results or too much payload. | Pagination, limits, payload projection, filtering, and result-size control. | Large result sets increase latency and client/network cost. | `scaling-query-volume/SKILL.md` |

Scaling for throughput and scaling for latency often push in opposite directions. Decide which one is the user's actual SLO before recommending topology changes.

## Data-volume options

| Option | Use when | Avoid when |
| --- | --- | --- |
| Vertical scaling | One larger node can hold the working set with safe headroom. | Hardware limits, downtime risk, or cost make a single large node fragile. |
| Horizontal scaling | Collections exceed one node or need distributed capacity. | Query fan-out would dominate latency. |
| Tenant scaling | Many tenants have uneven size or noisy-neighbor risk. | Tenant isolation is not required and operational simplicity matters more. |
| Sliding time window | Recent vectors are queried often and old data can age out or move. | Queries routinely span the full historical corpus. |

For detailed data-volume patterns, read `scaling-data-volume/SKILL.md` and its nested `horizontal-scaling/SKILL.md`, `tenant-scaling/SKILL.md`, `vertical-scaling/SKILL.md`, and `sliding-time-window/SKILL.md` resources when needed.

## Measurement checklist

Collect these facts before prescribing node count or sharding:

- Collection count, vector count, vector dimension, payload size, index type, replication factor, and shard count.
- Current CPU, RAM, disk, IOPS, network, and p95/p99 latency under representative load.
- QPS target, latency SLO, result limit, payload returned per query, and filter selectivity.
- Tenant count, largest tenant size, hot-tenant skew, and isolation requirements.
- Whether the problem is capacity, ingestion, search throughput, single-query latency, or oversized responses.

## Gotchas

- **Do not treat all slowness as missing nodes**: the slowest component in the query execution path determines latency.
- **Do not optimize throughput and latency with the same knob by default**: more parallelism can raise tail latency.
- **Do not ignore query volume**: returning too many results can look like search slowness even when vector search is fast.
- **Do not shard without an access pattern**: random sharding may increase fan-out and make filtered queries slower.

## Progressive disclosure and bundled resources

- `scaling-data-volume/SKILL.md`: data-size-driven scaling overview.
- `scaling-data-volume/horizontal-scaling/SKILL.md`: horizontal data scaling.
- `scaling-data-volume/tenant-scaling/SKILL.md`: tenant-oriented scaling.
- `scaling-data-volume/vertical-scaling/SKILL.md`: larger-node scaling.
- `scaling-data-volume/sliding-time-window/SKILL.md`: time-windowed collections.
- `scaling-qps/SKILL.md`: query throughput scaling.
- `minimize-latency/SKILL.md`: single-query latency reduction.
- `scaling-query-volume/SKILL.md`: large result-set control.

## Output template

```markdown
## Qdrant scaling recommendation

**Status:** recommendation | needs measurements | blocked
**Primary scaling goal:** data volume | query throughput | query latency | query volume

| Evidence | Interpretation | Recommendation |
| --- | --- | --- |
| `<metric or symptom>` | `<bottleneck>` | `<scaling action>` |

### Next checks
- `<measurement needed before changing topology>`
- `<reference file read, if any>`
```

## Quality gate

- [ ] The recommendation names exactly one primary scaling goal and any secondary goals.
- [ ] Throughput, latency, data volume, and query volume were considered separately.
- [ ] Node-count guidance is backed by capacity or SLO measurements, or the output requests the missing measurements.
- [ ] Sharding advice explains the access pattern and fan-out tradeoff.
- [ ] The relevant bundled deep reference was named when the request required detailed topology guidance.

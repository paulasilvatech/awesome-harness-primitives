---
name: "qdrant-monitoring"
description: >-
  Guide Qdrant monitoring, observability, health checks, Prometheus, Grafana, alerting, log centralization, and metric-based production debugging. Use when users ask how to monitor Qdrant, what metrics to track, whether Qdrant is healthy, why optimizers are stuck, why memory is growing, why requests are slow, or how to set up Prometheus or Grafana.
allowed-tools: [Read, Grep, Glob]
---

# Qdrant monitoring

Set up or diagnose Qdrant observability by choosing the right health probes, Prometheus metrics, Grafana panels, logs, and alert thresholds for availability, latency, optimizer progress, memory growth, and slow requests.

## When to invoke

- "How do I monitor Qdrant?"
- "What Qdrant metrics should we track?"
- "Is Qdrant healthy or is the optimizer stuck?"
- "Why is Qdrant memory growing or requests are slow?"
- "Set up Prometheus, Grafana, alerts, or health checks for Qdrant."

## Monitoring mode decision

| Need | First action | Evidence to collect |
| --- | --- | --- |
| New monitoring setup | Inventory deployment shape, endpoints, auth, and scrape path. | Prometheus target status, dashboard panels, alert rules. |
| Active production issue | Preserve current metrics before changing config. | Latency, request rate, memory, optimizer, disk, CPU, and logs for the incident window. |
| Health check | Separate process liveness from cluster readiness and collection availability. | Health endpoint result plus collection and shard status. |
| Capacity planning | Trend workload, vector count, payload size, RAM, disk, and optimizer work. | Time-series growth and saturation projections. |

Understand available metrics through the Qdrant monitoring documentation at https://qdrant.tech/documentation/operations/monitoring/.

## Core signals

| Signal | Watch for | Likely meaning | Response |
| --- | --- | --- | --- |
| Request latency | p95/p99 increase for search, upsert, or scroll. | Load, slow filters, disk pressure, optimizer work, or network. | Break down by operation and correlate with CPU, memory, disk, and optimizer metrics. |
| Error rate | 4xx/5xx spikes. | Client misuse, auth/config failure, node instability, or overload. | Separate user errors from server errors before paging operators. |
| Memory | Monotonic growth or frequent OOM risk. | Segment growth, mmap behavior, cache pressure, or insufficient capacity. | Compare vector count, payload indexes, quantization, and collection count. |
| Optimizers | Long-running or stuck optimization. | Large segments, insufficient IO/CPU, mis-sized thresholds, or write pressure. | Inspect optimizer metrics and logs before restarting. |
| Disk | High utilization or growth acceleration. | Collection growth, snapshots, WAL, or uncollected old data. | Alert before saturation; check snapshot retention. |
| Replication/shards | Unavailable or lagging shards. | Node failure, network issue, or rebalance. | Confirm cluster state before assuming query bug. |

## Setup checklist

| Component | Configuration rule |
| --- | --- |
| Prometheus scrape | Scrape Qdrant metrics endpoint from every node with stable labels for cluster, node, environment, and role. |
| Grafana dashboard | Include latency, throughput, errors, memory, disk, CPU, optimizer activity, collection size, and shard state. |
| Health probes | Use lightweight liveness for process health and stronger readiness checks for query-serving readiness. |
| Alerts | Alert on symptoms users feel: high p99 latency, sustained 5xx, low disk, OOM risk, unavailable shards, and optimizer stalling. |
| Logs | Centralize logs with timestamps, node identity, collection names, and request correlation when available. |
| Hybrid Cloud | Respect provider-specific access, scrape, and log-export mechanisms; do not assume direct node access. |

## Bundled deep dives

- `setup/SKILL.md`: Prometheus scraping, health probes, Hybrid Cloud specifics, alerting, and log centralization.
- `debugging/SKILL.md`: optimizer stuck, memory growth, slow requests, and metric-led production diagnosis.

## Gotchas

- **Do not treat liveness as readiness**: a live process can still be unable to serve a collection or shard.
- **Do not restart before capturing evidence**: optimizer and memory issues need the pre-restart time window.
- **Do not alert on raw counters**: alert on rates, saturation, or sustained state changes.
- **Do not ignore labels**: without cluster, node, collection, and operation labels, dashboards cannot isolate the cause.

## Output template

```markdown
## Qdrant monitoring result

**Status:** setup plan | diagnosis | blocked
**Mode:** new monitoring | active incident | health check | capacity planning

| Area | Evidence | Finding | Action |
| --- | --- | --- | --- |
| Metrics | `<Prometheus/Grafana observation>` | `<finding>` | `<next step>` |
| Health | `<probe or cluster state>` | `<finding>` | `<next step>` |
| Logs | `<log source/window>` | `<finding>` | `<next step>` |
| Alerts | `<rule or missing rule>` | `<finding>` | `<next step>` |

**Validation:** <how the setup or diagnosis was confirmed>
```

## Quality gate

- [ ] The response distinguishes setup work from active incident diagnosis.
- [ ] Prometheus, Grafana, health checks, alerts, or logs are addressed according to the user's request.
- [ ] Slow requests, memory growth, and optimizer-stuck symptoms are tied to concrete metrics before remediation.
- [ ] Liveness and readiness are not conflated.
- [ ] Any alert recommendation uses sustained rates or saturation, not raw counter values alone.
- [ ] The final result includes validation evidence or the missing evidence needed next.

## References

- [Qdrant monitoring documentation](https://qdrant.tech/documentation/operations/monitoring/)

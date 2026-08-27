---
name: cloud-design-patterns
description: >-
  Select, explain, and apply cloud design patterns for distributed systems across reliability,
  performance, messaging, architecture, deployment, security, and event-driven categories. Use
  when designing, reviewing, or implementing cloud workloads and distributed system architectures.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/cloud-design-patterns/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Cloud design patterns

Map workload constraints and nonfunctional requirements to industry-standard, technology-agnostic cloud design patterns, trade-offs, and Azure service options so a distributed architecture becomes reliable, secure, cost-optimized, high-performing, observable, and scalable.

## When to invoke

- "Which cloud design patterns fit this architecture?"
- "Review this distributed system for resilience and performance patterns."
- "Design a cloud workload using Azure Architecture Center patterns."
- "Map these requirements to reliability, messaging, security, and deployment patterns."

## Pattern categories at a glance

| Category | Patterns | Focus |
| --- | --- | --- |
| Reliability & Resilience | 9 patterns | Fault tolerance, self-healing, graceful degradation. |
| Performance | 10 patterns | Caching, scaling, load management, data optimization. |
| Messaging & Integration | 7 patterns | Decoupling, event-driven communication, workflow coordination. |
| Architecture & Design | 7 patterns | System boundaries, API gateways, migration strategies. |
| Deployment & Operational | 5 patterns | Infrastructure management, geo-distribution, configuration. |
| Security | 3 patterns | Identity, access control, content validation. |
| Event-Driven Architecture | 1 pattern | Event sourcing and audit trails. |

## Distributed-system fallacies to counter

Design patterns compensate for incorrect assumptions. Explicitly identify which fallacies the design is exposed to:

| Fallacy | Design response |
| --- | --- |
| The network is reliable. | Use Retry, Circuit Breaker, Health Endpoint Monitoring, and idempotent operations. |
| Latency is zero. | Use Cache-Aside, CQRS, asynchronous messaging, and locality-aware deployment. |
| Bandwidth is infinite. | Use Claim Check, compression, pagination, and coarse-grained APIs. |
| The network is secure. | Use Federated Identity, Valet Key, mTLS/private endpoints, and least privilege. |
| Topology doesn't change. | Use service discovery, Gateway Routing, and resilient client configuration. |
| There's one administrator. | Use External Configuration Store, policy-as-code, and operational ownership tags. |
| Component versioning is simple. | Use Anti-Corruption Layer, Backends for Frontends, and contract tests. |
| Observability implementation can be delayed. | Add Health Endpoint Monitoring, metrics, tracing, logs, and SLO dashboards from the start. |

## Pattern selection rules

| Requirement pressure | Prefer | Watch for |
| --- | --- | --- |
| Downstream dependency fails or throttles | Circuit Breaker, Retry, Bulkhead | Retry storms; use backoff, jitter, and idempotency. |
| Write and read models diverge | CQRS, Materialized View, Index Table | Eventual consistency and extra synchronization logic. |
| Bursty producers overload consumers | Queue-Based Load Leveling, Priority Queue, Competing Consumers | Poison messages and ordering constraints. |
| Long-running business transaction | Saga, Compensating Transaction, Scheduler Agent Supervisor | Compensation completeness and auditability. |
| Multiple clients need different API shapes | Backends for Frontends, Gateway Aggregation, Gateway Routing | Duplicated business logic in gateways. |
| Legacy replacement | Strangler Fig, Anti-Corruption Layer | Incomplete route ownership and data synchronization drift. |
| Multi-region availability | Deployment Stamps, Geode, Health Endpoint Monitoring | Data residency, replication lag, and operational complexity. |
| Secretless delegated access | Valet Key, Federated Identity | Over-scoped tokens and missing expiration. |

## Progressive disclosure and bundled resources

Load bundled references only when the task needs that category. Relative paths below are inside this skill package.

| Reference | When to load |
| --- | --- |
| `references/reliability-resilience.md` | Ambassador, Bulkhead, Circuit Breaker, Compensating Transaction, Retry, Health Endpoint Monitoring, Leader Election, Saga, Sequential Convoy. |
| `references/performance.md` | Async Request-Reply, Cache-Aside, CQRS, Index Table, Materialized View, Priority Queue, Queue-Based Load Leveling, Rate Limiting, Sharding, Throttling. |
| `references/messaging-integration.md` | Choreography, Claim Check, Competing Consumers, Messaging Bridge, Pipes and Filters, Publisher-Subscriber, Scheduler Agent Supervisor. |
| `references/architecture-design.md` | Anti-Corruption Layer, Backends for Frontends, Gateway Aggregation/Offloading/Routing, Gateway Aggregation, Gateway Offloading, Gateway Routing, Sidecar, Strangler Fig. |
| `references/deployment-operational.md` | Compute Resource Consolidation, Deployment Stamps, External Configuration Store, Geode, Static Content Hosting. |
| `references/security.md` | Federated Identity, Quarantine, Valet Key. |
| `references/event-driven.md` | Event Sourcing. |
| `references/best-practices.md` | Selecting appropriate patterns, Well-Architected Framework alignment, documentation, monitoring. |
| `references/azure-service-mappings.md` | Common Azure services for each pattern category. |

## Gotchas

- **Patterns have trade-offs**: explain why the pattern fits and what new operational burden it adds.
- **Do not implement patterns by name only**: identify the failure mode, data consistency model, and observability requirement.
- **Technology-agnostic first**: select the pattern before choosing Azure, another cloud platform, on-premises, or hybrid services.
- **Cost is part of architecture**: queues, caches, multi-region replicas, and gateway layers add spend and operations.

## Open Horizons integration

- Evaluate patterns against the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Azure, Backstage, AKS, managed-identity, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Cloud design pattern recommendation

**Workload:** <system or feature>
**Primary drivers:** <reliability | performance | messaging | security | deployment | migration>

| Requirement or risk | Recommended pattern | Category | Why it fits | Trade-off | Azure option |
| --- | --- | --- | --- | --- | --- |
| <risk> | <pattern> | <category> | <reason> | <cost/complexity/consistency impact> | <service or none> |

### Architecture notes
- <how the selected patterns work together>

### Validation
- <checks, tests, metrics, or runbooks needed>
```

## Quality gate

- [ ] Requirements and nonfunctional drivers are mapped to explicit patterns.
- [ ] At least one trade-off is documented for every recommended pattern.
- [ ] Distributed-computing fallacies relevant to the workload are addressed.
- [ ] Bundled references are loaded only for categories needed by the task.
- [ ] Azure service mappings are presented as options, not mandatory choices.
- [ ] The recommendation covers reliability, security, cost, operations, and performance impacts when relevant.

## References

- [Cloud Design Patterns - Azure Architecture Center](https://learn.microsoft.com/azure/architecture/patterns/)
- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/architecture/framework/)

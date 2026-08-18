---
name: cosmosdb-datamodeling
description: >-
  Capture Azure Cosmos DB for NoSQL workload requirements and produce access-pattern-driven data model artifacts. Use when the user asks to design a Cosmos DB NoSQL model, choose containers and partition keys, document access patterns, analyze aggregates, or create cosmosdb_requirements.md and cosmosdb_data_model.md.
---

# Azure Cosmos DB NoSQL data modeling

Gather application requirements, access patterns, volumetrics, concurrency, and relationship constraints; maintain `cosmosdb_requirements.md` during discovery; then create `cosmosdb_data_model.md` with a justified Azure Cosmos DB for NoSQL container, partition-key, indexing, and denormalization design.

## When to invoke

- "Design a Cosmos DB NoSQL data model for this app."
- "Help choose containers and partition keys from our access patterns."
- "Create cosmosdb_requirements.md and cosmosdb_data_model.md."
- "Review whether these entities should be embedded or separated."
- "We have massive Cosmos DB write volume and need a data model."

## Prerequisites and context

- Work from the user's domain, entities, relationships, access patterns, RPS, latency SLOs, consistency needs, document size, retention, and geographic distribution.
- Maintain two files in the working repository: `cosmosdb_requirements.md` as the live scratchpad and `cosmosdb_data_model.md` as the final deliverable.
- Ask one question at a time when possible, and at most three related questions.
- Read `references/extended-guide.md` when the main skill does not contain enough detail for advanced Cosmos DB modeling decisions.

## Discovery rules

Update `cosmosdb_requirements.md` after every user message that adds information. Capture evolving thoughts, uncertain assumptions, and design considerations instead of waiting for a final answer.

For massive scale signals such as `>10k writes/sec`, several million records in a short period, or the phrase "massive scale", immediately ask about:

1. Data binning or chunking strategies: can individual records be grouped into chunks?
2. Write reduction: what is the minimum number of actual write operations, and can work be batched?
3. Physical partition impact: how will total data size affect cross-partition query costs?

Every access pattern must have RPS. If the user does not know, estimate from business context and label the value as an assumption.

## Requirements artifact

Create or update `cosmosdb_requirements.md` with this concrete structure:

```markdown
# Azure Cosmos DB NoSQL Modeling Session

## Application Overview
- **Domain**: <domain>
- **Key Entities**: <entity list and relationships such as User (1:M) Orders>
- **Business Context**: <rules, constraints, compliance>
- **Scale**: <concurrent users, document sizes, retention, total requests/second>
- **Geographic Distribution**: <single region, multi-region reads, multi-region writes>

## Access Patterns Analysis
| Pattern # | Description | RPS (Peak and Average) | Type | Attributes Needed | Key Requirements | Design Considerations | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Get user profile by user ID when the user logs into the app | 500 RPS | Read | userId, name, email, createdAt | <50ms latency | Simple point read with id and partition key | Yes |
| 2 | Create new user account when the user is on the sign up page | 50 RPS | Write | userId, name, email, hashedPassword | Strong consistency | Consider unique key constraints for email | Pending |

## Entity Relationships Deep Dive
- **User → Orders**: 1:Many (avg 5 orders per user, max 1000)
- **Order → OrderItems**: 1:Many (avg 3 items per order, max 50)
- **Product → OrderItems**: 1:Many (popular products in many orders)
- **Products and Categories**: Many:Many

## Enhanced Aggregate Analysis
### <Entity1 + Entity2> Container Item Analysis
- **Access Correlation**: <% requiring both entities>
- **Query Patterns**: Entity1 only, Entity2 only, and both together percentages
- **Size Constraints**: Combined max size in MB and growth pattern
- **Update Patterns**: Independent or related update frequencies
- **Decision**: Single Document, Multi-Document Container, or Separate Containers
- **Justification**: <reasoning>

## Container Consolidation Analysis
| Parent | Child | Relationship | Access Overlap | Consolidation Decision | Justification |
| --- | --- | --- | --- | --- | --- |
| <Parent> | <Child> | 1:Many | <overlap> | Consolidate/Separate | <why> |

## Design Considerations (Subject to Change)
- **Hot Partition Concerns**: <analysis>
- **Large fan-out with Many Physucal partitions based on total Datasize Concerns**: <analysis>
- **Cross-Partition Query Costs**: <trade-offs>
- **Indexing Strategy**: <composite indexes, included paths, excluded paths>
- **Multi-Document Opportunities**: <30-70% correlation candidates>
- **Multi-Entity Query Patterns**: <related retrievals>
- **Denormalization Ideas**: <duplicated attributes>
- **Global Distribution**: <write regions and consistency levels>

## Validation Checklist
- [ ] Application domain and scale documented
- [ ] All entities and relationships mapped
- [ ] Aggregate boundaries identified based on access patterns
- [ ] Identifying relationships checked for consolidation opportunities
- [ ] Container consolidation analysis completed
- [ ] Every access pattern has: RPS (avg/peak), latency SLO, consistency level, expected result size, document size band
- [ ] Write pattern exists for every read pattern (and vice versa) unless USER explicitly declines
- [ ] Hot partition risks evaluated
- [ ] Consolidation framework applied; candidates reviewed
- [ ] Design considerations captured (subject to final validation)
```

## Modeling decisions

| Situation | Prefer | Reason |
| --- | --- | --- |
| `>70%` access correlation, bounded size, related operations | Multi-Document Container or embedded Single Document | Joint reads dominate and transaction scope may matter. |
| `50-70%` access correlation | Analyze operational coupling | Same backup/restore favors Multi-Document Container; different scaling or consistency favors Separate Containers. |
| `30-50%` access correlation | Compare cost and complexity carefully | Either design can be valid; quantify cross-partition query cost. |
| `<30%` access correlation | Separate Containers | Independent access dominates. |
| Child cannot exist without parent and queries always know `parent_id` | Identifying relationship with partition key `parent_id` | Avoid parent-to-child cross-partition queries. |
| Unbounded child growth | Separate documents or containers | Avoid exceeding document size and write amplification. |

Consolidate when access overlap is `>50%`, the relationship is natural parent-child, size is bounded, and an identifying relationship exists. Keep separate when access overlap is `<30%`, growth is unbounded, or operations must scale independently.

## Procedure

1. Capture application overview, entities, business context, scale, geographic distribution, and compliance constraints in `cosmosdb_requirements.md`.
2. Stay in access-pattern discovery until the user confirms all reads and writes are captured. Ask, "Do you have any other access patterns to discuss? I see we have a user login access pattern but no pattern to create users. Should we add one?"
3. For each access pattern, record average/peak RPS, read/write type, attributes, latency SLO, consistency level, result size, document size band, and status.
4. Analyze aggregates, identifying relationships, access correlation, update coupling, size constraints, hot partitions, cross-partition query costs, indexing, and denormalization.
5. Only after the user confirms access patterns are complete, create `cosmosdb_data_model.md` with final container designs and justifications.
6. Group indexes with the containers they belong to; do not create a detached indexing section that loses container context.

## Final deliverable

Create `cosmosdb_data_model.md` only after confirmation:

```markdown
# Azure Cosmos DB NoSQL Data Model

## Design Philosophy & Approach
<aggregate-oriented design principles and request-unit rationale>

## Aggregate Design Decisions
<why data was grouped together, split, or duplicated>

## Container Designs
### <Container name>
- **Purpose**: <what it stores>
- **Document Types**: <type discriminator values if Multi-Document Container>
- **Partition Key**: <path and why>
- **ID Strategy**: <id shape>
- **Items**: <example document summaries>
- **Indexes**: <included paths, excluded paths, composite indexes grouped here>
- **Served Access Patterns**: <pattern IDs>
- **Trade-offs**: <hot partition, cross-partition, transaction, consistency notes>
```

## Progressive disclosure and bundled resources

- `references/extended-guide.md`: deeper Cosmos DB modeling guidance for aggregate, partition-key, indexing, and scale decisions.

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `AP31`
- `CRITICAL`
- `Container/Separate`
- `Document/Multi-Document`
- `EVERY`
- `FILE`
- `IMMEDIATELY`
- `Independent/Related`
- `MANAGEMENT`
- `MASSIVE`
- `MOST`
- `MUST`
- `No/Yes/Yes`
- `SCALE`
- `WARNING`
- `artifacts_produced`
- `binning/chunking`
- `by-step`
- `e-commerce`
- `last_updated`
- `progressive-disclosure`
- `use-case`
- `user_id`
- `volume/size`
- `UserOrders`

## Output template

```markdown
## Cosmos DB data modeling result

**Status:** requirements-updated | model-created | blocked
**Files changed:** `cosmosdb_requirements.md`, `cosmosdb_data_model.md`

### Requirements captured
| Area | Status | Evidence |
| --- | --- | --- |
| Access patterns | <complete/incomplete> | <count and missing fields> |
| Scale and RPS | <complete/incomplete> | <avg/peak RPS notes> |
| Relationships | <complete/incomplete> | <entities and cardinality> |

### Design summary
| Container | Partition key | Document types | Main access patterns | Key trade-off |
| --- | --- | --- | --- | --- |
| <name> | <partition key> | <types> | <pattern IDs> | <trade-off> |

### Open questions
- <question or none>
```

## Quality gate

- [ ] `cosmosdb_requirements.md` was updated after every new user-provided fact.
- [ ] Every access pattern includes RPS, latency SLO, consistency, result size, and document size band.
- [ ] Every read has a matching write or an explicit user-declined write pattern.
- [ ] Massive-scale workloads triggered binning, write-reduction, and physical-partition questions.
- [ ] Aggregates were judged by access correlation, size, update coupling, and identifying relationships.
- [ ] `cosmosdb_data_model.md` was created only after the user confirmed discovery was complete.
- [ ] Index definitions are grouped under their owning containers.

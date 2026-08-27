---
name: qdrant-performance-optimization
description: >-
  Diagnose and optimize Qdrant performance across search speed, indexing throughput, memory usage,
  query shape, HNSW and payload indexes, quantization, storage, and hardware trade-offs. Use when
  asked to improve Qdrant latency, throughput, indexing speed, RAM usage, or vector search
  efficiency.
allowed-tools: Read, Grep, Glob
---

<!-- Generated from harness/github-copilot/skills/qdrant-performance-optimization/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Qdrant performance optimization

Choose the right Qdrant performance lever for latency, throughput, indexing, memory, query design, and hardware constraints, then produce a focused optimization plan with measurable validation steps.

## When to invoke

- "Optimize Qdrant search latency."
- "Improve Qdrant indexing throughput."
- "Reduce Qdrant memory usage."
- "Why are Qdrant filtered searches slow?"
- "Tune Qdrant for higher vector search throughput."

## Performance dimensions

| Dimension | Optimize for | Primary levers | Watch for |
| --- | --- | --- | --- |
| Search latency | Time to get one response for a single query. | HNSW parameters, `ef`, quantization, payload indexes, filtered query design, avoiding oversized result payloads. | Tail latency, cold segments, heavy filters without indexes. |
| Search throughput | Number of queries processed in a time frame. | Parallel clients, batching, shard/replica layout, CPU cores, async request handling, payload projection. | Saturated CPU, disk I/O, network serialization. |
| Indexing performance | Time to build or update vector and payload indexes. | Bulk upload, write batching, segment configuration, deferred indexing where acceptable, disk speed. | Rebuilding indexes during peak traffic. |
| Memory usage | RAM retained by vectors, HNSW graph, payload indexes, and caches. | On-disk vectors/payloads, quantization, payload field selection, collection sizing, segment compaction. | Latency increases when data moves from RAM to disk. |
| Hardware fit | Match workload to CPU, RAM, disk, and network. | NVMe for disk-backed workloads, enough RAM for hot vectors/indexes, CPU for distance computation, replicas for read scaling. | Assuming one setting fixes under-provisioned hardware. |

## Optimization decision rules

| Symptom | Likely cause | First checks | Candidate fixes |
| --- | --- | --- | --- |
| Slow filtered search | Payload filter scans too much data. | Check whether filtered fields have payload indexes and whether filters are selective. | Add payload indexes for frequently filtered fields; simplify filters; pre-partition collections when filters are dominant. |
| High recall but slow search | Search breadth is too high. | Inspect query `ef`, collection HNSW settings, vector size, and top-k. | Lower `ef` cautiously, reduce top-k, consider quantization, benchmark recall impact. |
| Fast unfiltered, slow with large payloads | Response serialization dominates. | Inspect returned payload/vector fields and response size. | Exclude vectors, project only needed payload fields, reduce `limit`. |
| Indexing blocks serving | Heavy writes compete with reads. | Check ingestion rate, optimizer activity, segment count, and CPU/disk saturation. | Batch upserts, schedule bulk loads off-peak, tune optimizers, separate write-heavy and read-heavy workloads. |
| RAM pressure | Vectors, HNSW, or payload indexes exceed memory. | Compare collection size, vector dimensions, index settings, and resident memory. | Enable on-disk storage for cold data, quantize vectors, drop unused payload indexes, scale RAM. |
| Low throughput under concurrency | Client or server parallelism is insufficient. | Measure client concurrency, server CPU, request queueing, and network. | Increase client concurrency, add replicas, shard appropriately, use async clients. |

## Search speed optimization

There are two criteria for search speed: latency and throughput. Latency is the time it takes to get a response for a single query; throughput is the number of queries processed in a given time frame. Decide which metric matters before changing configuration.

Use the bundled `search-speed-optimization` material in this skill package when the task is specifically about query latency, throughput, HNSW tuning, filtered search, or benchmarking search behavior.

Legacy bundled location: `search-speed-optimization/SKILL.md`.

## Indexing performance optimization

Qdrant needs to build a vector index to perform efficient similarity search. The time it takes to build the index varies by dataset size, hardware, vector dimensions, payload indexes, and collection configuration.

Use the bundled `indexing-performance-optimization` material in this skill package when the task is about bulk load speed, upsert throughput, optimizer activity, segment behavior, or index build time.

Legacy bundled location: `indexing-performance-optimization/SKILL.md`.

## Memory usage optimization

Vector search can be memory intensive, especially with large datasets. Qdrant can control which parts of storage stay in memory and which are stored on disk, so memory tuning is a latency/cost trade-off rather than a pure reduction exercise.

Use the bundled `memory-usage-optimization` material in this skill package when the task is about RAM pressure, on-disk vectors, payload storage, quantization, collection sizing, or cost reduction.

Legacy bundled location: `memory-usage-optimization/SKILL.md`.

## Gotchas

- **Optimize one metric at a time**: a latency fix such as keeping more index data in RAM may increase cost, while a memory fix such as on-disk vectors may increase latency.
- **Payload indexes are workload-specific**: indexing every field wastes memory and slows writes; index fields that are frequently filtered and selective.
- **Benchmark with representative filters**: unfiltered vector benchmarks hide the cost of production filter clauses.
- **Do not change HNSW or quantization blindly**: measure recall and latency before and after.

## Output template

```markdown
## Qdrant performance optimization plan

**Status:** plan | implemented | blocked
**Primary goal:** latency | throughput | indexing | memory | hardware fit

| Symptom | Evidence needed or observed | Recommended change | Expected trade-off | Validation metric |
| --- | --- | --- | --- | --- |
| `<slow filtered search>` | `<query/filter/index evidence>` | `<payload index or query change>` | `<RAM/write/recall impact>` | `<p95 latency/throughput/RAM>` |

### Next measurements
- `<benchmark, collection config, query sample, or system metric>`

### Validation
- Before: `<metric>`
- After: `<metric or pending>`
```

## Quality gate

- [ ] The plan states whether it optimizes latency, throughput, indexing performance, memory usage, or hardware fit.
- [ ] Recommendations are tied to observed or requested symptoms, not generic tuning.
- [ ] Search-speed guidance distinguishes latency from throughput.
- [ ] Indexing guidance accounts for dataset size, hardware, vector index build cost, and write/read contention.
- [ ] Memory guidance states the latency and cost trade-off of on-disk storage, indexes, or quantization.
- [ ] Payload index recommendations are limited to selective, frequently filtered fields.
- [ ] Validation metrics include before/after measurements or explicitly list measurements still needed.

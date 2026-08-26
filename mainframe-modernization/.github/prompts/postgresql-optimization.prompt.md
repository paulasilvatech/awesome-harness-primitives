---
name: "postgresql-optimization"
description: "Optimize PostgreSQL 16 queries, indexes, and schema using PostgreSQL-specific features, deferring the workflow to the postgresql-optimization skill."
argument-hint: "selection=<sql-or-query>"
agent: "dba"
tools: ["read", "search", "execute"]
---
# /postgresql-optimization

## Objective

Optimize a slow PostgreSQL query, index, or schema using PostgreSQL-specific features, backing every recommendation with a measured `EXPLAIN ANALYZE`. The full workflow lives in the [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md) skill; this prompt applies it to the SIFAP 2.0 database (PostgreSQL 16 via JPA/Hibernate) without restating it.

> [!IMPORTANT]
> No recommendation ships without a before/after `EXPLAIN ANALYZE`; a plan is evidence, not an opinion.

## When to Invoke

During Stage 3/4, when a query is slow, a report times out, or a schema needs tuning against realistic row counts.

## Preconditions

- The query or schema to optimize is available
- A staging snapshot with realistic row counts is reachable to run `EXPLAIN ANALYZE`
- The existing indexes on the involved tables can be listed
- The target is PostgreSQL 16

## Inputs the Team Must Provide

- `selection` — the query or schema to optimize
- The involved tables, their indexes, and realistic row counts
- Ask the user for anything that is missing.

## What I Will Do

- Apply the optimization workflow in the [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md) skill to the selection
- Read `EXPLAIN (ANALYZE, BUFFERS)` top to bottom and identify the dominant cost
- Recommend the right index type (GIN/GiST/partial/covering) or query rewrite with evidence
- Express index changes as online-safe, rollback-safe migrations

## What I Will NOT Do

- Recommend an index without weighing its write cost, or add one for every query
- Trust `EXPLAIN` without `ANALYZE`, or optimize against dev-sized data
- Concatenate user input into SQL, or drift the JPA mapping out of sync
- Apply a blocking `CREATE INDEX` on a hot table (I use `CONCURRENTLY`)

## Output Format

```markdown
### Bottleneck
Seq Scan on `payment` (4.0M rows) for a selective status filter.

### Recommendation
CREATE INDEX CONCURRENTLY idx_payment_status ON payment (status) WHERE status <> 'CLOSED';

### EXPLAIN ANALYZE
Before: Seq Scan, 820 ms. After: Index Scan, 4 ms.
```

## Definition of Done

- [ ] The dominant bottleneck is named with plan evidence
- [ ] The recommendation is backed by a before/after `EXPLAIN ANALYZE`
- [ ] Any index is online-safe (`CONCURRENTLY`) in a rollback-safe migration
- [ ] Queries stay parameterized and consistent with the JPA mapping

## Prompt Body

The [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md) skill owns the diagnostic workflow, index heuristics, and PostgreSQL feature set — read it, then apply it to the selection.

**Step 1 — Measure.**
Run `EXPLAIN (ANALYZE, BUFFERS)` on a staging snapshot and read the plan top to bottom.

**Step 2 — Apply the skill.**
Use the skill to choose the fix: index type, query rewrite, JSONB/array operator, window function, or partitioning.

**Step 3 — Respect the kit rules.**
Target PostgreSQL 16, keep the JPA mapping in sync, and deliver index changes as `CONCURRENTLY` migrations under `db/migration/`.

**Step 4 — Prove it.**
Re-run `EXPLAIN ANALYZE` and paste the before/after timings.

## Invocation Example

```
/postgresql-optimization selection="SELECT * FROM payment WHERE status = 'OPEN'"
```

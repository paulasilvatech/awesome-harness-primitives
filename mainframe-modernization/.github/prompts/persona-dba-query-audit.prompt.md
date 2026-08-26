---
name: "query-audit"
description: "Audit a SQL or JPQL query for injection, sequential-scan traps, and N+1, returning a verdict, a rewrite, and an EXPLAIN-based rationale."
argument-hint: "query=<sql-or-jpql> tables=<table,table>"
agent: "dba"
tools: ["read", "search", "execute"]
---
# /query-audit

## Objective

Review a SQL, JPQL, Criteria, or QueryDSL query intended for **PostgreSQL 16** for injection risk, sequential-scan traps, N+1 patterns, and SIFAP coding-standard violations. The deliverable is a verdict (Pass / Fix required / Reject), a rewritten parameterized query, an `EXPLAIN ANALYZE` interpretation, and—when justified—an index recommendation handed to `/migration`.

> [!WARNING]
> Any string concatenation of user input into SQL is an injection defect and an automatic Reject. Bind every parameter.

## When to Invoke

During Stage 3/4 code review of a data-access path, or when a query is slow, before it reaches a hot endpoint or a nightly batch in production.

## Preconditions

- The query text is available in its original form
- The schema of the involved tables is known, or reachable via `db/migration/`
- A staging snapshot with realistic row counts is available to run `EXPLAIN ANALYZE` against
- The existing indexes on the involved tables can be listed (`\d table_name`)

## Inputs the Team Must Provide

- The query in its original form (raw SQL, JPQL, Criteria API, or QueryDSL)
- The schema of the involved tables, or a pointer to migrations in `db/migration/`
- The existing indexes on those tables and realistic production row counts
- The calling code path—a hot endpoint (per request) or a batch job (nightly)
- Ask the user for anything that is missing.

## What I Will Do

- Run the static scan: reject string-concatenated user input and `SELECT *` on wide tables; flag index-defeating casts and functions on indexed columns
- Run the dynamic scan: `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` against a staging snapshot and read the plan top to bottom
- Flag `Seq Scan` on large tables with a selective filter, index-supportable `Sort` steps, costly `Nested Loop`s, and estimate-vs-actual divergence above 10×
- Check for N+1 (missing `JOIN FETCH`), lock and isolation risk, and full parameterization
- Compare against SIFAP standards and issue a verdict with a rewritten query
- Recommend a missing index and route its creation to `/migration`

## What I Will NOT Do

- Approve a query because "it is fast in dev"—dev has thousands of rows; production has millions
- Approve `SELECT *`, an unbound parameter, or `FOR UPDATE` on a hot row without a queue or backoff
- Trust `EXPLAIN` without `ANALYZE`, or add an index for every query without weighing write cost
- Write the index migration here—I recommend it and hand the file to `/migration` (the DBA migration prompt)
- Change the schema or the JPA entity mapping myself—mapping changes are routed back to the owning module
- Assume a column is or is not PII—I flag anything unlabeled and ask for a column `COMMENT`

## Output Format

```markdown
## Query Audit — payment lookup by status

### Verdict
Fix required — Seq Scan on a 4M-row table with a selective status filter.

### Findings
| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | High | Seq Scan on `payment` | EXPLAIN: Seq Scan (actual rows = 4.0M) |
| 2 | Medium | `SELECT *` on a wide table | returns 22 columns; 4 are used |

### Rewritten query
SELECT id, status, reviewed_at FROM payment WHERE status = :status;

### Index recommendation (route to /migration)
CREATE INDEX CONCURRENTLY idx_payment_status ON payment (status) WHERE status <> 'CLOSED';

### EXPLAIN ANALYZE before / after
Before: Seq Scan, 820 ms. After: Index Scan, 4 ms.

### Required application change
Bind `:status`; select only the four used columns.
```

## Definition of Done

- [ ] A verdict is stated: Pass / Fix required / Reject
- [ ] Findings include severity, evidence (file/line or an EXPLAIN snippet), and a recommendation
- [ ] The rewritten query is parameterized and ready to paste, with no string concatenation
- [ ] `EXPLAIN ANALYZE` is pasted before and after, with measured times
- [ ] Any index recommendation is online-safe (`CONCURRENTLY`) and routed to `/migration`
- [ ] PII access is flagged and column comments are confirmed

## Prompt Body

You are the `@dba`. The team wants a query audited before it reaches production. Read [`query-optimization`](../skills/query-optimization/SKILL.md) before you start; it owns the diagnostic workflow, the index-design heuristics, and the antipatterns.

**Step 1 — Run the static scan.**
Reject any string concatenation with user input as SQL injection. Reject `SELECT *` on a wide table. Flag implicit casts (`varchar = bigint`) and functions on indexed columns that defeat the index—fix them, or add an expression index only when the evidence justifies it.

**Step 2 — Run the dynamic scan.**
Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` against a staging snapshot. Read the plan top to bottom and flag: a `Seq Scan` on a table larger than 10k rows when a filter exists; a `Sort` an index could support; a `Nested Loop` over more than ~1k outer rows where a `Hash Join` is cheaper; and an estimated-vs-actual row divergence above 10× (stale statistics—run `ANALYZE`).

**Step 3 — Check for N+1.**
If the query comes from JPA, look for a missing `JOIN FETCH` or batch-size hint, and identify the parent loop in the application code.

**Step 4 — Check locks and isolation.**
`SELECT ... FOR UPDATE` on a hot table needs a queue or backoff. The default isolation is `READ COMMITTED`; flag unjustified `SERIALIZABLE`.

**Step 5 — Confirm parameterization.**
Every user-facing value must be a bound parameter, never interpolated—even from a "trusted" path. This is the OWASP injection guardrail.

**Step 6 — Compare against SIFAP standards.**
`snake_case` identifiers; `TIMESTAMPTZ` for timestamps; `NUMERIC(15,2)` for money, never `FLOAT`; a `COMMENT` on every PII column.

**Step 7 — Write the fix and classify.**
Rewrite the query parameterized. When the evidence justifies a new index, specify it with `CONCURRENTLY` and route its migration to `/migration`. State the verdict: Pass, Fix required, or Reject.

Never approve a query that disagrees with the JPA entity mapping—that hides an N+1 that returns later. If a mapping is wrong, send it back to the owning module rather than papering over it in SQL.

## Invocation Example

```
/query-audit query="SELECT * FROM payment WHERE status = 'OPEN'" tables=payment
```

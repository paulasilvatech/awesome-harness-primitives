---
name: "postgresql-code-review"
description: "Review SQL and schema for PostgreSQL 16 best practices and anti-patterns, deferring the checklist to the postgresql-code-review skill."
argument-hint: "selection=<sql-or-schema>"
agent: "dba"
tools: ["read", "search"]
---
# /postgresql-code-review

## Objective

Review PostgreSQL SQL, schema, functions, and security features (JSONB, arrays, custom types, Row Level Security) for a selection or the whole project, and return a verdict with concrete fixes. The full checklist lives in the [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md) skill; this prompt applies it to the SIFAP 2.0 database (PostgreSQL 16 via JPA/Hibernate) without restating it.

> [!IMPORTANT]
> Any user input concatenated into SQL is an injection defect and an automatic Reject — bind every parameter.

## When to Invoke

During Stage 3/4 code review of a migration, query, function, or schema change, before it merges into `develop`.

## Preconditions

- The SQL/schema under review is available (a selection, a migration file, or the project)
- The involved tables and their existing indexes are known or reachable via `db/migration/`
- The target is PostgreSQL 16

## Inputs the Team Must Provide

- `selection` — the SQL, schema, or migration to review (defaults to the current selection or project)
- The tables involved and any PII columns among them
- Ask the user for anything that is missing.

## What I Will Do

- Apply the review checklist in the [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md) skill to the selection
- Check data-type choices (CITEXT, TIMESTAMPTZ, ENUM, JSONB), index types (GIN/GiST/partial), and constraints
- Confirm every query is parameterized and every PII column is masked or commented
- Issue a verdict — Pass / Fix required / Reject — with the corrected SQL

## What I Will NOT Do

- Approve string-concatenated SQL or an unbound parameter
- Rewrite the JPA entity mapping here (mapping changes route back to the owning module)
- Treat JSONB like an opaque string, or ignore PostgreSQL-specific operators
- Assume a column is or is not PII — I flag anything unlabeled

## Output Format

```markdown
### Verdict
Fix required — missing GIN index for a JSONB containment query.

### Findings
| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | High | Unparameterized status filter | `data->>'status' = '` + input |
| 2 | Medium | No index for `data @> ...` | Seq Scan on `orders` |

### Corrected SQL
CREATE INDEX idx_orders_data ON orders USING gin(data);
SELECT id FROM orders WHERE data @> :filter;
```

## Definition of Done

- [ ] A verdict is stated: Pass / Fix required / Reject
- [ ] Every finding has a severity and evidence (file/line or a plan snippet)
- [ ] The corrected SQL is parameterized and ready to paste
- [ ] Every PII column is masked or carries a `COMMENT`

## Prompt Body

The [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md) skill owns the PostgreSQL-specific anti-patterns and quality checklist — read it, then apply it to the selection.

**Step 1 — Static scan.**
Reject concatenated user input; flag `SELECT *` on wide tables, generic types where PostgreSQL types fit, and missing constraints.

**Step 2 — Apply the skill.**
Work through the skill's areas: JSONB, arrays, custom types/domains, schema design, functions/triggers, extensions, and RLS.

**Step 3 — Respect the kit rules.**
Confirm PostgreSQL 16 features, parameterized access through JPA/Hibernate, rollback-safe migrations under `backend/src/main/resources/db/migration/`, and a `COMMENT` on every PII column.

**Step 4 — Verdict.**
State Pass, Fix required, or Reject with the corrected SQL and the reasons.

## Invocation Example

```
/postgresql-code-review selection=backend/src/main/resources/db/migration/V3__payment.sql
```

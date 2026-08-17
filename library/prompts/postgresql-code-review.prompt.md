---
name: 'postgresql-code-review'
description: 'Review PostgreSQL code for database-specific correctness, security, maintainability, and performance risks.'
agent: 'agent'
tools: ['changes', 'codebase', 'editFiles', 'problems']
argument-hint: 'target=<selection-or-project-area>'
---

# /postgresql-code-review

## Objective

Review PostgreSQL SQL, schema, migrations, functions, triggers, privileges, and related application code for PostgreSQL-specific correctness, security, maintainability, and performance issues, with special attention to features that distinguish PostgreSQL from generic SQL databases.

## When to Invoke

Use this prompt when reviewing PostgreSQL schema changes, migrations, SQL queries, PL/pgSQL functions, triggers, JSONB or array usage, extension usage, security policies, or application data-access code that targets PostgreSQL.

## Preconditions

- The PostgreSQL code, selected SQL, migration, function, trigger, or project area is available.
- The target database is PostgreSQL or the reviewed code intentionally uses PostgreSQL-specific features.
- Schema, index, and privilege context is available or can be inferred from inspected files.
- Edits are permitted only when the user asks for fixes; otherwise return review findings.

## Inputs the Team Must Provide

- `target` — `${selection}` or an explicit file, migration, schema, function, or project area.
- PostgreSQL version when known.
- Relevant table definitions, indexes, extensions, roles, and expected query patterns.
- Whether the desired result is review-only or approved edits.
- Ask the user for anything that is missing when it affects correctness, security, or performance judgement.

## What I Will Do

- Review JSONB, array operations, schema design, custom types, domains, functions, triggers, extensions, Row Level Security, privilege management, and PostgreSQL-specific performance features.
- Flag anti-patterns such as missing GIN/GiST indexes, inefficient JSONB filters, unvalidated JSONB, broad grants, wrong timestamp types, weak constraints, and trigger functions that fire unnecessarily.
- Recommend PostgreSQL-native improvements such as `CITEXT`, `JSONB`, arrays, ENUM types, CHECK constraints, domains, `TIMESTAMPTZ`, containment operators, PL/pgSQL, RLS, and built-in encryption functions.
- Provide evidence-based findings with severity, affected object, risk, and fix.

## What I Will NOT Do

- Treat PostgreSQL as a generic SQL database when PostgreSQL-specific features would improve correctness or safety.
- Recommend extensions, indexes, RLS policies, domains, or trigger changes without explaining trade-offs and migration impact.
- Grant broad privileges, weaken constraints, or bypass row-level security for convenience.
- Convert a portable query to PostgreSQL-specific syntax unless the target is confirmed PostgreSQL.
- Apply destructive schema changes or data changes without explicit approval.

## Output Format

Return findings or applied edits in this format:

```markdown
## PostgreSQL Code Review Result

### Target
- `${selection}` or `db/migrations/001_create_orders.sql`

### Findings
| Severity | Area | Evidence | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| High | JSONB | `data->>'status' = 'shipped'` | No index support | Use `data @> '{"status": "shipped"}'` with a GIN index |
| High | Privileges | `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user` | Excessive access | Grant only required table and sequence permissions |

### PostgreSQL-Specific Checklist
- Schema Design: [passed/failed]
- Performance Considerations: [passed/failed]
- PostgreSQL Features Utilization: [passed/failed]
- Security and Compliance: [passed/failed]

### Suggested SQL
    CREATE INDEX idx_orders_status ON orders USING gin((data->'status'));
    ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

### Validation
- Manual review completed against PostgreSQL-specific rules.
- Follow-up: run tests and `EXPLAIN (ANALYZE, BUFFERS)` for performance-sensitive queries.
```

## Definition of Done

- [ ] JSONB and array usage were checked for correct operators, validation, and indexability.
- [ ] Schema design was checked for `CITEXT`, `JSONB`, arrays, ENUM types, CHECK constraints, `TIMESTAMPTZ`, and custom domains where appropriate.
- [ ] Function and trigger code was checked for PL/pgSQL quality and unnecessary trigger execution.
- [ ] Extension use was checked for `uuid-ossp`, `pgcrypto`, `pg_trgm`, and `CREATE EXTENSION IF NOT EXISTS` where relevant.
- [ ] Security review included Row Level Security, policies, granular privileges, roles, sequences, and built-in encryption functions.
- [ ] Findings include severity, evidence, risk, and a PostgreSQL-specific recommendation.

## Prompt Body

Follow these steps in order.

**Step 1 — Establish scope.** Review `${selection}` when present; otherwise inspect the requested PostgreSQL files or the entire project area. Confirm whether this is review-only or approved-edit work.

**Step 2 — Review JSONB usage.** Flag inefficient JSONB patterns such as `SELECT * FROM orders WHERE data->>'status' = 'shipped';` when no index can support the predicate. Prefer indexable containment such as `SELECT * FROM orders WHERE data @> '{"status": "shipped"}';` with `CREATE INDEX idx_orders_status ON orders USING gin((data->'status'));`. Require JSONB validation such as `ALTER TABLE orders ADD CONSTRAINT valid_status CHECK (data->>'status' IN ('pending', 'shipped', 'delivered'));`. Avoid deep unvalidated updates such as `UPDATE orders SET data = data || '{"shipping":{"tracking":{"number":"123"}}}';` unless structure and validation are intentional.

**Step 3 — Review array operations.** Flag inefficient array searches such as `SELECT * FROM products WHERE 'electronics' = ANY(categories);` when no index supports them. Prefer GIN-indexed array operations: `CREATE INDEX idx_products_categories ON products USING gin(categories);` and `SELECT * FROM products WHERE categories @> ARRAY['electronics'];`. Avoid array concatenation in loops inside a `function/procedure`; prefer bulk operations such as `UPDATE products SET categories = categories || ARRAY['new_category'] WHERE id IN (SELECT id FROM products WHERE condition);`.

**Step 4 — Review schema design.** Prefer PostgreSQL-optimized schema choices when they fit the domain. Flag generic schemas such as `id INTEGER`, `email VARCHAR(255)`, and `created_at TIMESTAMP` when `BIGSERIAL PRIMARY KEY`, `CITEXT UNIQUE NOT NULL`, `TIMESTAMPTZ DEFAULT NOW()`, `metadata JSONB DEFAULT '{}'`, and a `valid_email` CHECK constraint would improve correctness. Recommend JSONB GIN indexes such as `CREATE INDEX idx_users_metadata ON users USING gin(metadata);` for metadata queries.

**Step 5 — Review custom types and domains.** Flag generic value columns such as `amount DECIMAL(10,2)`, `currency VARCHAR(3)`, and `status VARCHAR(20)` when constrained values should use `CREATE TYPE currency_code AS ENUM ('USD', 'EUR', 'GBP', 'JPY');`, `CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');`, and `CREATE DOMAIN positive_amount AS DECIMAL(10,2) CHECK (VALUE > 0);`.

**Step 6 — Review PostgreSQL anti-patterns.** Check for avoiding PostgreSQL-specific indexes, not using GIN/GiST for appropriate data types, misusing JSONB as a simple string field, ignoring array operators, poor partition key selection, not using ENUM types, missing CHECK constraints, wrong data types such as `VARCHAR` instead of `TEXT` or `CITEXT`, and unstructured JSONB without validation.

**Step 7 — Review functions and triggers.** Check PL/pgSQL functions for efficient timestamp handling and trigger firing conditions. Prefer `CURRENT_TIMESTAMP` for `updated_at`, and define triggers such as `CREATE TRIGGER update_modified_time_trigger BEFORE UPDATE ON table_name FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*) EXECUTE FUNCTION update_modified_time();` so they fire only when needed.

**Step 8 — Review extensions.** Verify extensions use `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`, `CREATE EXTENSION IF NOT EXISTS "pgcrypto";`, and `CREATE EXTENSION IF NOT EXISTS "pg_trgm";` when needed. Check appropriate use of `SELECT uuid_generate_v4();`, `SELECT crypt('password', gen_salt('bf'));`, and `SELECT word_similarity('postgres', 'postgre');`.

**Step 9 — Review security.** Check Row Level Security with `ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;` and policies such as `CREATE POLICY user_data_policy ON sensitive_data FOR ALL TO application_role USING (user_id = current_setting('app.current_user_id')::INTEGER);`. Flag broad grants such as `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;`; prefer granular grants like `GRANT SELECT, INSERT, UPDATE ON specific_table TO app_user;` and `GRANT USAGE ON SEQUENCE specific_table_id_seq TO app_user;`.

**Step 10 — Apply the checklist and report.** Check schema design, performance considerations, PostgreSQL features utilization, security, and compliance. Include appropriate index types, JSONB containment operators `@>` and `?`, array operators, window functions, CTEs, extensions, PL/pgSQL, advanced SQL features, optimization techniques, function error handling, audit trails, and built-in encryption functions. Report findings with severity and evidence.

## Invocation Example

```
/postgresql-code-review target=db/migrations/001_create_orders.sql
```

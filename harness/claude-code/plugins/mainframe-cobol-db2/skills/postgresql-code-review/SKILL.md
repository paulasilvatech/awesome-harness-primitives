---
name: postgresql-code-review
description: >-
  Review existing PostgreSQL SQL, schema, migrations, functions, triggers, indexes, JSONB, arrays,
  custom types, domains, extensions, privileges, and Row Level Security for PostgreSQL-specific
  anti-patterns. Use when asked to audit or critique PostgreSQL code, database migrations,
  PL/pgSQL, RLS policies, or schema design.
---

<!-- Generated from harness/github-copilot/plugins/mainframe-cobol-db2/skills/postgresql-code-review/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# PostgreSQL code review

Review PostgreSQL-specific code for correctness, performance, type quality, security, and maintainability, then return a verdict, evidence-backed findings, and paste-ready corrected SQL.

## When to invoke

- "Review this PostgreSQL migration for anti-patterns."
- "Audit our JSONB and array usage."
- "Is this schema using the right PostgreSQL types?"
- "Check this PL/pgSQL function and trigger before it merges."
- "Review this Row Level Security policy."

## Criteria

### JSONB and arrays

| Area | Bad pattern | Better pattern |
| --- | --- | --- |
| JSONB filters | `data->>'status' = 'shipped'` without index support. | Use containment: `data @> '{"status": "shipped"}'` and `CREATE INDEX idx_orders_status ON orders USING gin((data->'status'));`. |
| JSONB structure | Deep, unconstrained blobs such as `data || '{"shipping":{"tracking":{"number":"123"}}}'`. | Add validation such as `CONSTRAINT valid_status CHECK (data->>'status' IN ('pending', 'shipped', 'delivered'))`. |
| Array filters | `'electronics' = ANY(categories)` without a supporting index. | Use `CREATE INDEX idx_products_categories ON products USING gin(categories);` and `categories @> ARRAY['electronics']`. |
| Array mutation | Array concatenation in row-by-row loops. | Use bulk updates such as `categories = categories || ARRAY['new_category'] WHERE id IN (...)`. |

### Schema design and data types

| Concern | Review rule |
| --- | --- |
| Primary keys | Prefer PostgreSQL-appropriate generated identifiers such as `BIGSERIAL PRIMARY KEY` or the project standard. |
| Email and text | Use `CITEXT` for case-insensitive email, `TEXT` instead of arbitrary `VARCHAR` when there is no true length rule, and `CHECK` constraints for real validation. |
| Time | Use `TIMESTAMPTZ` instead of `TIMESTAMP` for instants. |
| JSONB | Default structured JSONB with `metadata JSONB DEFAULT '{}'` when optional document data is intentional. |
| Constrained values | Use `ENUM`, custom domains, or lookup tables rather than free `VARCHAR(20)` values. |
| Money-like values | Use a domain such as `positive_amount AS DECIMAL(10,2) CHECK (VALUE > 0)` when the constraint is reused. |

Example type objects to preserve: `CREATE TYPE currency_code AS ENUM ('USD', 'EUR', 'GBP', 'JPY');`, `CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');`, and `CREATE DOMAIN positive_amount AS DECIMAL(10,2) CHECK (VALUE > 0);`.

### Functions, triggers, extensions, and security

| Area | Review rule |
| --- | --- |
| Trigger timestamps | Use `CURRENT_TIMESTAMP` and fire triggers only when needed with `WHEN (OLD.* IS DISTINCT FROM NEW.*)`. |
| Trigger API | Check `CREATE OR REPLACE FUNCTION update_modified_time() RETURNS TRIGGER`, `NEW.updated_at`, `RETURN NEW`, `LANGUAGE plpgsql`, `CREATE TRIGGER update_modified_time_trigger`, and `EXECUTE FUNCTION update_modified_time()`. |
| Extensions | Use `CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`, `"pgcrypto"`, and `"pg_trgm"` only when needed; know `uuid_generate_v4()`, `crypt('password', gen_salt('bf'))`, and `word_similarity('postgres', 'postgre')`. |
| Row Level Security | Require `ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;` and policies such as `CREATE POLICY user_data_policy ... USING (user_id = current_setting('app.current_user_id')::INTEGER);` when tenant or user isolation is needed. |
| Privileges | Avoid `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user`; prefer `GRANT SELECT, INSERT, UPDATE ON specific_table TO app_user` and `GRANT USAGE ON SEQUENCE specific_table_id_seq TO app_user`. |
| Indexes | Check use of `GIN` for JSONB and arrays, `GiST` for ranges/geospatial, partial indexes for selective predicates, and evidence from plans where available. |
| SQL injection | No user input concatenated into SQL; require JPQL, derived queries, or bound native parameters when reviewing application access. |

## PostgreSQL anti-patterns

- Avoiding PostgreSQL-specific indexes such as `GIN` and `GiST` for appropriate data types.
- Treating `JSONB` like a string field instead of using operators such as `@>` and `?`.
- Ignoring array operators and indexes.
- Choosing poor partition keys or not leveraging partitioning where scale requires it.
- Using `VARCHAR` for limited value sets instead of `ENUM`, domain, lookup table, or `CHECK`.
- Missing validation constraints on data that application code assumes.
- Using `TIMESTAMP` for real-world instants where time zone correctness matters.
- Leaving unstructured `JSONB` without validation for fields the application depends on.

## SQL vocabulary to preserve

Use exact PostgreSQL examples when relevant: `UNIQUE`, `NULL`, `created_at`, `idx_users_metadata`, `valid_email`, `table_name`, `application_role`, `UUID`, `BEGIN`, `BEFORE`, `EACH`, `GOOD`, `JSONB/arrays`, `GIN/GiST`, `function/procedure`, and built-in security or extension capabilities.

Example schema facts include `email CITEXT UNIQUE NOT NULL`, `created_at TIMESTAMPTZ DEFAULT NOW()`, `metadata JSONB DEFAULT '{}'`, `CONSTRAINT valid_email CHECK (...)`, and `CREATE INDEX idx_users_metadata ON users USING gin(metadata);`.

## Output template

```markdown
## PostgreSQL review — <file or selection>

**Verdict:** Pass | Fix required | Reject

| # | Severity | Finding | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | High | User input concatenated into SQL | `<file:line or snippet>` | Bind through JPQL, a derived query, or a parameterized native query. |
| 2 | Medium | JSONB containment query has no GIN index | `Seq Scan on orders` | `CREATE INDEX idx_orders_data ON orders USING gin(data);` |
| 3 | Low | VARCHAR used for case-insensitive email | `email VARCHAR(255)` | Use `CITEXT` plus an appropriate `CHECK` constraint. |

### Corrected SQL
```sql
CREATE INDEX idx_orders_data ON orders USING gin(data);
-- Repository query stays parameterized: WHERE data @> :filter
```
```

## Quality gate

- [ ] A verdict is stated: Pass, Fix required, or Reject.
- [ ] Every finding carries severity and concrete evidence such as file/line, snippet, or plan output.
- [ ] No user input is concatenated into SQL; every parameter is bound.
- [ ] PostgreSQL-specific types including `CITEXT`, `JSONB`, arrays, `ENUM`, and domains were considered.
- [ ] Index types including `GIN`, `GiST`, and partial indexes were evaluated where relevant.
- [ ] `CHECK`, `ENUM`, and domain constraints were validated for constrained values.
- [ ] `RLS`, privileges, extension usage, functions, and triggers were checked when present.
- [ ] Corrected SQL is paste-ready and rollback-safe for schema changes.

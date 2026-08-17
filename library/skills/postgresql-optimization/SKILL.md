---
name: postgresql-optimization
description: >-
  Design, tune, and modernize PostgreSQL SQL, schemas, indexes, functions, and maintenance workflows using PostgreSQL-specific capabilities. Use this skill when the user asks for PostgreSQL optimization, query tuning, JSONB or array design, EXPLAIN ANALYZE interpretation, index strategy, full-text search, custom types, range/geometric types, pg_stat_statements, VACUUM, ANALYZE, partitioning, or secure parameterized database development.
---

# PostgreSQL optimization

Optimize `${selection}` or the current project by applying PostgreSQL-specific data types, operators, indexes, query plans, extensions, and maintenance practices, then return paste-ready SQL and evidence-backed recommendations.

## When to invoke

- "Optimize this PostgreSQL query."
- "Design indexes for these JSONB and array filters."
- "Review this EXPLAIN ANALYZE output."
- "Use PostgreSQL full-text search or range types here."
- "Improve our pg_stat_statements slow queries."

## PostgreSQL feature map

| Need | PostgreSQL capability | Use |
| --- | --- | --- |
| Semi-structured data | `JSONB`, `@>`, `?`, `#>>`, `jsonb_agg`, GIN | Query structured metadata without text casts. |
| Tags and many values | Arrays, `ANY`, `&&`, `@>`, `array_length`, `array_agg`, `unnest` | Model short bounded value lists and query with GIN when selective. |
| Analytics | `SUM() OVER`, `AVG() OVER`, `DENSE_RANK`, `ROW_NUMBER`, `LAG`, `LEAD`, frames like `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` | Running totals, moving averages, rankings, and comparisons. |
| Search | `tsvector`, `to_tsvector`, `plainto_tsquery`, `@@`, `ts_rank` | Full-text search with ranking and GIN indexes. |
| Reusable validation | `CREATE DOMAIN`, `CHECK`, custom composite types, `ENUM` | Encode business constraints in schema. |
| Time or numeric intervals | `tstzrange`, `numrange`, overlap `&&`, `EXCLUDE USING gist` | Reservations, prices, validity periods, non-overlap rules. |
| Spatial-lite data | `POINT`, `CIRCLE`, `POLYGON`, `<->`, GiST | Basic geometric distance and containment without PostGIS. |
| Cryptography and fuzzy text | `uuid-ossp`, `pgcrypto`, `unaccent`, `pg_trgm`, `btree_gin` | UUIDs, `crypt`, `gen_salt`, accent handling, trigram `similarity`, GIN support. |

## Query and index patterns

| Pattern | Avoid | Prefer |
| --- | --- | --- |
| JSON search | `data::text LIKE '%admin%'` | `CREATE INDEX idx_users_data_gin ON users USING gin(data);` then `data @> '{"role": "admin"}'`. |
| JSON path read | Repeated text extraction without index | Use `data #>> '{user,role}'` for scalar reads and containment for indexed filtering. |
| Array membership | Relying only on `'postgresql' = ANY(tags)` for large tables | Add `CREATE INDEX ... USING gin(tags)` and use `tags @> ARRAY['postgresql']` or `tags && ARRAY['database','sql']`. |
| Pagination | `ORDER BY id OFFSET 10000 LIMIT 20` | Cursor pagination: `WHERE id > $last_id ORDER BY id LIMIT 20`. |
| Recent aggregation | Full scan for a bounded date range | Partial index: `CREATE INDEX idx_orders_recent ON orders(user_id) WHERE order_date >= '2024-01-01';`. |
| Case-insensitive lookup | `lower(email)` scan | Expression index: `CREATE INDEX idx_users_lower_email ON users(lower(email));`. |
| Covering read | Index lookup plus table fetch for hot columns | `CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total, created_at);`. |
| Multi-column filters | Separate single-column indexes for correlated predicates | Composite index such as `CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);`. |
| Overlapping reservations | Application-only overlap checks | `EXCLUDE USING gist (room_id WITH =, reservation_period WITH &&)`. |

## Performance workflow

1. Capture the slow SQL and its parameters; never concatenate user input into SQL.
2. Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` on representative data.
3. Inspect sequential scans on large tables, join algorithms, sort and aggregate nodes, row estimate errors, filter selectivity, and buffer reads.
4. Check `pg_stat_statements` for `query`, `calls`, `total_time`, `mean_time`, `rows`, and cache hit percentage:

```sql
SELECT query, calls, total_time, mean_time, rows,
       100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

5. Propose the smallest safe change: rewrite SQL, add `CREATE INDEX`, add constraints, adjust schema types, or schedule maintenance.
6. Validate with a before/after plan, expected trade-offs, and rollback-safe SQL.

## Schema and data type guidance

```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_events_data_gin ON events USING gin(data);

CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');
CREATE DOMAIN email_address AS TEXT
CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email email_address NOT NULL,
    status order_status DEFAULT 'pending'
);
```

Use `TIMESTAMPTZ` for instants, `TEXT` when length is not a business rule, `CITEXT` or an expression index for case-insensitive text, domains for reusable validation, and declarative partitioning for large time- or tenant-partitioned tables.

## Monitoring and maintenance

| Task | Query or action |
| --- | --- |
| Connections | `SELECT count(*) AS connections, state FROM pg_stat_activity GROUP BY state;` |
| Memory settings | `SELECT name, setting, unit FROM pg_settings WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem');` |
| Database size | `SELECT pg_size_pretty(pg_database_size(current_database())) AS db_size;` |
| Table sizes | Use `pg_total_relation_size(schemaname||'.'||tablename)` from `pg_tables`. |
| Unused indexes | Query `pg_stat_user_indexes WHERE idx_scan = 0`. |
| Routine maintenance | Run regular `VACUUM` and `ANALYZE`; review PostgreSQL logs; monitor index bloat and fragmentation. |
| High concurrency | Use connection pooling such as `pgbouncer`; monitor pool usage and saturation. |

## Security rules

- Use parameterized queries exclusively; placeholders such as `$last_id` are acceptable, string concatenation is not.
- Implement proper access controls and row-level security where needed.
- Audit sensitive data access and use secure connection methods.
- Prefer `pgcrypto` for database-side cryptographic functions only when the architecture justifies it; avoid storing plaintext secrets.

## Technical index

Preserve these PostgreSQL identifiers, plan terms, and example names when producing SQL: `ALTER`, `CONSTRAINT`, `COUNT`, `DISTINCT`, `EXISTS`, `EXTENSION`, `EXTRACT`, `GOOD`, `INTEGER`, `JOIN`, `LEFT`, `OLAP`, `OLTP`, `PARTITION`, `RECURSIVE`, `UNION`, `UPDATE`, `UUID`, `Lag/Lead`, `address_type`, `category_tree`, `parent_id`, `postal_code`, `price_range`, `product_id`, `sale_date`, `search_vector`, `service_area`, `running_total`, `moving_avg`, `monthly_rank`, `prev_amount`, `order_count`, `idx_active_users`, `idx_documents_search`, `idx_locations_coords`, `idx_table_column`, `idx_tup_read`, `idx_tup_fetch`, `no_overlap`, `uuid_generate_v4`, `high-concurrency`, and `multi-column`.

## Output template

```markdown
## Query Performance Analysis

**Status:** optimized | needs data | blocked
**Original Query:**
```sql
<original SQL>
```

**Evidence:**
- Plan reviewed: `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)`
- Main issue: <sequential scan, missing index, join order, sort, row estimate, lock, or maintenance issue>

**Issues Identified:**
- <issue with cost, rows, buffers, or table size evidence>

**Optimized Query:**
```sql
<improved SQL>
```

**Recommended Indexes / Schema Changes:**
```sql
CREATE INDEX <index_name> ON <table>(<columns>);
```

**Performance Impact:** <expected impact and trade-off>
**Validation:** <before/after command or reason it could not be run>
```

## Quality gate

- [ ] Every SQL change is PostgreSQL-specific where PostgreSQL features add value.
- [ ] Expensive queries are backed by `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` or a stated blocker.
- [ ] Index recommendations name the index type, columns/order, predicate, and write/storage trade-off.
- [ ] JSONB, arrays, full-text search, ranges, geometric types, custom types, and extensions are used only when they fit the data model.
- [ ] Security guidance uses parameterized queries and avoids SQL injection.
- [ ] Maintenance recommendations cover `VACUUM`, `ANALYZE`, `pg_stat_statements`, connection usage, or log review when relevant.
- [ ] Output includes paste-ready SQL and does not claim measured speedups without evidence.

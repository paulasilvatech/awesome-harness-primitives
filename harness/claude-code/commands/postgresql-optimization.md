---
description: >-
  Optimize PostgreSQL implementations using database-specific features, indexing, monitoring, and
  query tuning guidance.
allowed-tools: Read, Grep, Glob, Edit, Write
---

<!-- Generated from harness/github-copilot/prompts/postgresql-optimization.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /postgresql-optimization

## Objective

Optimize PostgreSQL implementations using PostgreSQL-specific query, index, schema, data type, extension, monitoring, maintenance, security, and performance-tuning guidance while preserving query semantics and maintainability.

## When to Invoke

Use this prompt when a PostgreSQL query is slow, an execution plan shows an expensive operation, a schema or index needs PostgreSQL-specific tuning, JSONB or array patterns need review, or monitoring output must become concrete optimization work.

## Preconditions

- The PostgreSQL SQL, migration, repository method, schema, selected code, or performance symptom is available.
- The team can provide table definitions, indexes, row counts, workload shape, and execution evidence such as `EXPLAIN (ANALYZE, BUFFERS)` or `pg_stat_statements` when needed.
- Changes to SQL, indexes, migrations, or data-access code are permitted for the requested scope.
- Production-impacting changes such as new indexes, extension changes, partitioning, or query rewrites will be reviewed before deployment.

If a required precondition is not met, identify it and stop before making changes.

## Inputs the Team Must Provide

- `selection` or `target` — the query, schema, migration, repository method, or selected PostgreSQL code to optimize.
- Schema context — tables, columns, data types, constraints, primary keys, foreign keys, and current indexes.
- Workload context — row counts, data distribution, frequency, latency goal, read/write ratio, and production safety constraints.
- Evidence — `EXPLAIN (ANALYZE, BUFFERS)`, slow-query output, `pg_stat_statements`, logs, runtime measurements, or observed symptoms.
- Ask the user for anything that is missing. If evidence is required to avoid guessing, ask and stop before making risky changes.

## What I Will Do

- Use `postgresql-optimization` (type: skill) as the primary workflow reference when available.
- Analyze PostgreSQL-specific features including JSONB, arrays, window functions, full-text search, range types, geometric types, extensions, monitoring, maintenance, and query plans.
- Recommend query rewrites, index changes, configuration checks, monitoring queries, and maintenance actions with evidence and trade-offs.
- Prefer parameterized SQL, secure connections, access controls, and row-level security where the workload requires them.
- Validate recommendations with `EXPLAIN (ANALYZE, BUFFERS)`, realistic data volumes, or clearly labeled follow-up commands.

## What I Will NOT Do

- Claim an improvement without evidence, a measured plan, or a clearly labeled assumption.
- Recommend indexes without considering write cost, storage, cardinality, selectivity, existing indexes, bloat, and fragmentation.
- Use generic SQL advice when PostgreSQL-specific syntax or behavior matters.
- Concatenate untrusted input into SQL or weaken access controls.
- Run destructive database commands, drop indexes, or modify production data outside the approved scope.

## Output Format

Return or apply the result using this concrete structure:

````markdown
## PostgreSQL Optimization Result

### Target
- `[query-file, selection, migration, or schema]`
- PostgreSQL version: `[version if known]`

### Query Performance Analysis
**Original Query**:
`[Original SQL with performance issues]`

**Issues Identified**:
- `[sequential scan, missing index, inefficient join order, JSONB operator issue, pagination issue, etc.]`

**Optimized Query**:
`[Improved SQL with explanations]`

**Recommended Indexes**:
```sql
CREATE INDEX idx_table_column ON table(column);
```

### PostgreSQL Features Used
- `[JSONB|array|window function|full-text search|range type|extension|monitoring view]`

### Validation
- Plan command: `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) ...`
- Before: `[plan evidence and timing]`
- After: `[plan evidence and timing or expected validation step]`

### Risks and Trade-offs
- `[write overhead, storage cost, locking, migration, maintenance, or security note]`
````

## Definition of Done

- [ ] The PostgreSQL target and scope are identified, or unknowns are explicitly labeled.
- [ ] Findings are tied to SQL text, schema facts, execution-plan evidence, monitoring output, or labeled assumptions.
- [ ] Optimized SQL preserves semantics, ordering guarantees, duplicate behavior, and transaction behavior.
- [ ] Index recommendations include purpose, index type, column order, predicate or `INCLUDE` columns, and write/storage trade-offs.
- [ ] Security guidance preserves parameterization, access controls, and secure connection methods.
- [ ] Validation uses `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements`, realistic data volumes, or a clear follow-up command.

## Prompt Body

Follow these steps in order. Preserve existing project conventions and do not invent evidence.

**Step 1 — Establish the target, PostgreSQL version, schema, workload, safety constraints, and available evidence.**
Establish the target, PostgreSQL version, schema, workload, safety constraints, and available evidence.

**Step 2 — Inventory the PostgreSQL optimization checklist.**
Inventory the PostgreSQL-specific technical content below and use it as the optimization checklist.

**Step 3 — Analyze query shape, indexes, data types, extensions, monitoring, maintenance, and security.**
Analyze query shape, indexes, data types, extensions, monitoring, maintenance, and security. Prefer targeted changes with measurable impact.

**Step 4 — Report validation and trade-offs.**
Produce optimized SQL, index or maintenance recommendations, validation evidence, and trade-offs. Run or request `EXPLAIN (ANALYZE, BUFFERS)` before claiming improvement.

**Technical inventory from the source prompt.**
Preserve and apply these settings, rules, commands, paths, file patterns, examples, checklists, and output shapes when they are relevant to the invocation:

**PostgreSQL Development Assistant.**

Expert PostgreSQL guidance for ${selection} (or entire project if no selection). Focus on PostgreSQL-specific features, optimization patterns, and advanced capabilities.

Use `postgresql-optimization` (type: skill) as the primary workflow reference. Apply the additional examples, checklists, and output format in this prompt when they add task-specific detail not provided by the skill.

**PostgreSQL-Specific Features.**

**JSONB Operations.**
```sql
-- Advanced JSONB queries
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- GIN index for JSONB performance
CREATE INDEX idx_events_data_gin ON events USING gin(data);

-- JSONB containment and path queries
SELECT * FROM events 
WHERE data @> '{"type": "login"}'
  AND data #>> '{user,role}' = 'admin';

-- JSONB aggregation
SELECT jsonb_agg(data) FROM events WHERE data ? 'user_id';
```

**Array Operations.**
```sql
-- PostgreSQL arrays
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    tags TEXT[],
    categories INTEGER[]
);

-- Array queries and operations
SELECT * FROM posts WHERE 'postgresql' = ANY(tags);
SELECT * FROM posts WHERE tags && ARRAY['database', 'sql'];
SELECT * FROM posts WHERE array_length(tags, 1) > 3;

-- Array aggregation
SELECT array_agg(DISTINCT category) FROM posts, unnest(categories) as category;
```

**Window Functions & Analytics.**
```sql
-- Advanced window functions
SELECT 
    product_id,
    sale_date,
    amount,
    -- Running totals
    SUM(amount) OVER (PARTITION BY product_id ORDER BY sale_date) as running_total,
    -- Moving averages
    AVG(amount) OVER (PARTITION BY product_id ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg,
    -- Rankings
    DENSE_RANK() OVER (PARTITION BY EXTRACT(month FROM sale_date) ORDER BY amount DESC) as monthly_rank,
    -- Lag/Lead for comparisons
    LAG(amount, 1) OVER (PARTITION BY product_id ORDER BY sale_date) as prev_amount
FROM sales;
```

**Full-Text Search.**
```sql
-- PostgreSQL full-text search
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    search_vector tsvector
);

-- Update search vector
UPDATE documents 
SET search_vector = to_tsvector('english', title || ' ' || content);

-- GIN index for search performance
CREATE INDEX idx_documents_search ON documents USING gin(search_vector);

-- Search queries
SELECT * FROM documents 
WHERE search_vector @@ plainto_tsquery('english', 'postgresql database');

-- Ranking results
SELECT *, ts_rank(search_vector, plainto_tsquery('postgresql')) as rank
FROM documents 
WHERE search_vector @@ plainto_tsquery('postgresql')
ORDER BY rank DESC;
```

**PostgreSQL Performance Tuning.**

**Query Optimization.**
```sql
-- EXPLAIN ANALYZE for performance analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'::date
GROUP BY u.id, u.name;

-- Identify slow queries from pg_stat_statements
SELECT query, calls, total_time, mean_time, rows,
       100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;
```

**Index Strategies.**
```sql
-- Composite indexes for multi-column queries
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Partial indexes for filtered queries
CREATE INDEX idx_active_users ON users(created_at) WHERE status = 'active';

-- Expression indexes for computed values
CREATE INDEX idx_users_lower_email ON users(lower(email));

-- Covering indexes to avoid table lookups
CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total, created_at);
```

**Connection & Memory Management.**
```sql
-- Check connection usage
SELECT count(*) as connections, state 
FROM pg_stat_activity 
GROUP BY state;

-- Monitor memory usage
SELECT name, setting, unit 
FROM pg_settings 
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem');
```

**PostgreSQL Advanced Data Types.**

**Custom Types & Domains.**
```sql
-- Create custom types
CREATE TYPE address_type AS (
    street TEXT,
    city TEXT,
    postal_code TEXT,
    country TEXT
);

CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- Use domains for data validation
CREATE DOMAIN email_address AS TEXT 
CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Table using custom types
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email email_address NOT NULL,
    address address_type,
    status order_status DEFAULT 'pending'
);
```

**Range Types.**
```sql
-- PostgreSQL range types
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    reservation_period tstzrange,
    price_range numrange
);

-- Range queries
SELECT * FROM reservations 
WHERE reservation_period && tstzrange('2024-07-20', '2024-07-25');

-- Exclude overlapping ranges
ALTER TABLE reservations 
ADD CONSTRAINT no_overlap 
EXCLUDE USING gist (room_id WITH =, reservation_period WITH &&);
```

**Geometric Types.**
```sql
-- PostgreSQL geometric types
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    coordinates POINT,
    coverage CIRCLE,
    service_area POLYGON
);

-- Geometric queries
SELECT name FROM locations 
WHERE coordinates <-> point(40.7128, -74.0060) < 10; -- Within 10 units

-- GiST index for geometric data
CREATE INDEX idx_locations_coords ON locations USING gist(coordinates);
```

**PostgreSQL Extensions & Tools.**

**Useful Extensions.**
```sql
-- Enable commonly used extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";     -- Cryptographic functions
CREATE EXTENSION IF NOT EXISTS "unaccent";     -- Remove accents from text
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Trigram matching
CREATE EXTENSION IF NOT EXISTS "btree_gin";    -- GIN indexes for btree types

-- Using extensions
SELECT uuid_generate_v4();                     -- Generate UUIDs
SELECT crypt('password', gen_salt('bf'));      -- Hash passwords
SELECT similarity('postgresql', 'postgersql'); -- Fuzzy matching
```

**Monitoring & Maintenance.**
```sql
-- Database size and growth
SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;

-- Table and index sizes
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage statistics
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;  -- Unused indexes
```

**PostgreSQL-Specific Optimization Tips.**
- **Use EXPLAIN (ANALYZE, BUFFERS)** for detailed query analysis
- **Configure postgresql.conf** for your workload (OLTP vs OLAP)
- **Use connection pooling** (pgbouncer) for high-concurrency applications
- **Regular VACUUM and ANALYZE** for optimal performance
- **Partition large tables** using PostgreSQL 10+ declarative partitioning
- **Use pg_stat_statements** for query performance monitoring

**Monitoring and Maintenance.**

**Query Performance Monitoring.**
```sql
-- Identify slow queries
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;
```

**Database Maintenance.**
- **VACUUM and ANALYZE**: Regular maintenance for performance
- **Index Maintenance**: Monitor and rebuild fragmented indexes
- **Statistics Updates**: Keep query planner statistics current
- **Log Analysis**: Regular review of PostgreSQL logs

**Common Query Patterns.**

**Pagination.**
```sql
-- BAD: OFFSET for large datasets
SELECT * FROM products ORDER BY id OFFSET 10000 LIMIT 20;

-- GOOD: Cursor-based pagination
SELECT * FROM products 
WHERE id > $last_id 
ORDER BY id 
LIMIT 20;
```

**Aggregation.**
```sql
-- BAD: Inefficient grouping
SELECT user_id, COUNT(*) 
FROM orders 
WHERE order_date >= '2024-01-01' 
GROUP BY user_id;

-- GOOD: Optimized with partial index
CREATE INDEX idx_orders_recent ON orders(user_id) 
WHERE order_date >= '2024-01-01';

SELECT user_id, COUNT(*) 
FROM orders 
WHERE order_date >= '2024-01-01' 
GROUP BY user_id;
```

**JSON Queries.**
```sql
-- BAD: Inefficient JSON querying
SELECT * FROM users WHERE data::text LIKE '%admin%';

-- GOOD: JSONB operators and GIN index
CREATE INDEX idx_users_data_gin ON users USING gin(data);

SELECT * FROM users WHERE data @> '{"role": "admin"}';
```

**Optimization Checklist.**

**Query Analysis.**
- [ ] Run EXPLAIN ANALYZE for expensive queries
- [ ] Check for sequential scans on large tables
- [ ] Verify appropriate join algorithms
- [ ] Review WHERE clause selectivity
- [ ] Analyze sort and aggregation operations

**Index Strategy.**
- [ ] Create indexes for frequently queried columns
- [ ] Use composite indexes for multi-column searches
- [ ] Consider partial indexes for filtered queries
- [ ] Remove unused or duplicate indexes
- [ ] Monitor index bloat and fragmentation

**Security Review.**
- [ ] Use parameterized queries exclusively
- [ ] Implement proper access controls
- [ ] Enable row-level security where needed
- [ ] Audit sensitive data access
- [ ] Use secure connection methods

**Performance Monitoring.**
- [ ] Set up query performance monitoring
- [ ] Configure appropriate log settings
- [ ] Monitor connection pool usage
- [ ] Track database growth and maintenance needs
- [ ] Set up alerting for performance degradation

**Optimization Output Format.**

**Query Analysis Results.**
````
## Query Performance Analysis

**Original Query**:
[Original SQL with performance issues]

**Issues Identified**:
- Sequential scan on large table (Cost: 15000.00)
- Missing index on frequently queried column
- Inefficient join order

**Optimized Query**:
[Improved SQL with explanations]

**Recommended Indexes**:
```sql
CREATE INDEX idx_table_column ON table(column);
```

**Performance Impact**: Expected 80% improvement in execution time
````

**Advanced PostgreSQL Features.**

**Window Functions.**
```sql
-- Running totals and rankings
SELECT 
    product_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY product_id ORDER BY order_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY amount DESC) as rank
FROM sales;
```

**Common Table Expressions (CTEs).**
```sql
-- Recursive queries for hierarchical data
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 as level
    FROM categories 
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

Focus on providing specific, actionable PostgreSQL optimizations that improve query performance, security, and maintainability while leveraging PostgreSQL's advanced features.

## Invocation Example

```
/postgresql-optimization
```

---
description: >-
  Optimize SQL queries, indexes, pagination, batching, and performance diagnostics across common
  database engines.
argument-hint: "target=<query-file-or-selection> engine=<mysql|postgresql|sqlserver|oracle|other>"
allowed-tools: Read, Grep, Glob, Edit, Write
---

<!-- Generated from harness/github-copilot/prompts/sql-optimization.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /sql-optimization

## Objective

Analyze and optimize SQL in a selected query, file, or project area using database-aware but broadly portable techniques for query shape, indexes, pagination, batching, execution-plan review, and performance monitoring across MySQL, PostgreSQL, SQL Server, Oracle, and other SQL databases.

## When to Invoke

Use this prompt when a query is slow, an execution plan shows expensive scans or joins, pagination degrades at large offsets, indexes need review, batch operations are row-by-row, or database performance diagnostics must be translated into concrete SQL changes.

## Preconditions

- The SQL query, migration, repository method, selected code, or database performance symptom is available.
- The target database engine is known, or the requested result can stay database-agnostic until engine details are provided.
- The user can provide relevant schema details, table sizes, indexes, and execution-plan evidence when optimization depends on them.
- Changes to SQL, indexes, migrations, or data-access code are permitted for the requested target.
- Production-impacting changes such as new indexes, partitioning, or query rewrites will be reviewed before deployment.

## Inputs the Team Must Provide

- `target` — the SQL selection, file, repository method, migration, or performance report to optimize.
- `engine` — MySQL, PostgreSQL, SQL Server, Oracle, or another SQL database.
- Schema context — tables, columns, data types, primary keys, foreign keys, constraints, and current indexes.
- Workload context — expected row counts, data distribution, frequency, latency goal, and read/write ratio.
- Evidence — execution plan, slow-query log, monitoring query output, error message, or observed runtime.
- Safety constraints — whether edits, index DDL, migrations, or command execution are allowed.
- Ask the user for anything that is missing. If the engine, schema, or performance evidence is required to avoid guessing, ask and stop before making risky changes.

## What I Will Do

- Inspect the SQL and the surrounding data-access code when available.
- Identify anti-patterns such as `SELECT *`, non-sargable predicates, inefficient joins, correlated subqueries, high-offset pagination, row-by-row writes, and N+1 access.
- Propose query rewrites that preserve semantics while reducing scanned rows, sort work, network transfer, and repeated execution.
- Recommend indexes that match filter, join, sort, and projection patterns, including composite, covering, and partial indexes where supported.
- Distinguish portable SQL from database-specific syntax and call out engine-specific alternatives.
- Validate recommendations against execution plans, realistic data volumes, or the best available evidence.
- Report risks, trade-offs, and rollout notes for index and schema changes.

## What I Will NOT Do

- Claim a performance improvement without evidence, a reasoned plan expectation, or a clearly labeled assumption.
- Apply engine-specific syntax as universal SQL; SQL Server `INCLUDE`, PostgreSQL partial indexes, and vendor monitoring views must be labeled.
- Recommend indexes without considering write overhead, storage cost, cardinality, column order, and existing indexes.
- Rewrite a query in a way that changes result semantics, ordering guarantees, duplicate handling, or transaction behavior.
- Replace a database engine, ORM, or application architecture unless the user explicitly asks for that broader redesign.
- Run destructive commands, modify production data, drop indexes, or change migrations outside the requested edit scope.
- Treat offset pagination, temporary tables, partitioning, or denormalization as universal fixes without checking workload fit.

## Output Format

Return the optimization plan or applied changes in this concrete format:

```markdown
## SQL Optimization Result

### Target
- `queries/orders-report.sql`
- Engine: PostgreSQL

### Findings
| Severity | Area | Evidence | Recommendation |
| --- | --- | --- | --- |
| High | WHERE clause | `YEAR(o.created_at)` prevents index use | Use a date range predicate on `created_at` |
| Medium | Projection | `SELECT *` returns unused columns | Select only `id`, `customer_id`, `total_amount`, `created_at` |

### Optimized SQL

    SELECT o.id, o.customer_id, o.total_amount, o.created_at
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.id
    WHERE o.created_at >= '2024-01-01'
      AND o.created_at < '2025-01-01'
      AND c.status = 'active';

### Index Recommendations

    CREATE INDEX idx_orders_created_at ON orders(created_at);
    CREATE INDEX idx_orders_customer_id ON orders(customer_id);
    CREATE INDEX idx_customers_status ON customers(status);

### Validation
- Execution plan before: sequential scan on `orders`
- Execution plan after: expected range scan on `idx_orders_created_at`
- Test command or query: `EXPLAIN ANALYZE ...`

### Risks and Trade-offs
- New indexes increase storage and write cost.
- Verify with realistic row counts before production rollout.
```

## Definition of Done

- [ ] The target SQL and database engine are identified, or unknowns are explicitly labeled.
- [ ] Optimized SQL preserves the original result semantics.
- [ ] Findings are tied to specific query patterns, schema facts, execution-plan evidence, or labeled assumptions.
- [ ] Index recommendations include purpose, column order, and write/storage trade-offs.
- [ ] Database-specific syntax is labeled with the engine that supports it.
- [ ] Validation uses an execution plan, realistic data volume, monitoring output, or a clear follow-up command.
- [ ] No destructive or out-of-scope database operation is performed.

## Prompt Body

Follow these steps in order. Optimize for measurable performance improvement, but preserve correctness first.

**Step 1 — Establish the target and engine.**
Use `${selection}` when it contains SQL or related data-access code; otherwise inspect the requested target. Identify the database engine: MySQL, PostgreSQL, SQL Server, Oracle, or another SQL database. If the engine is unknown, keep recommendations portable and label any engine-specific alternative.

**Step 2 — Gather schema and workload evidence.**
Collect table definitions, relevant columns, primary keys, foreign keys, constraints, existing indexes, row counts, data distribution, query frequency, latency goal, and read/write ratio when available. Ask for missing schema or workload facts when the optimization depends on them.

**Step 3 — Analyze the execution evidence.**
Prefer an execution plan, slow-query log, monitoring view, or observed runtime with realistic data volumes. Look for full scans, high row estimates, sort spills, repeated nested-loop work, key lookups, lock waits, large offsets, and high rows-examined-to-rows-returned ratios.

**Step 4 — Fix projection and filtering first.**
Avoid `SELECT *` in production queries. Select only required columns to reduce I/O, memory, and network transfer.

```sql
-- BAD: SELECT * anti-pattern
SELECT * FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;

-- GOOD: Explicit column selection
SELECT lt.id, lt.name, at.value
FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;
```

Keep predicates index-friendly. Avoid wrapping indexed columns in functions when a normalized value, range predicate, generated column, expression index, or functional index is more appropriate.

```sql
-- BAD: Function calls in WHERE clause
SELECT * FROM orders
WHERE UPPER(customer_email) = 'JOHN@EXAMPLE.COM';

-- GOOD: Index-friendly WHERE clause
SELECT * FROM orders
WHERE customer_email = 'john@example.com';
-- Consider: CREATE INDEX idx_orders_email ON orders(LOWER(customer_email));
```

Use date ranges instead of extracting parts from a date column.

```sql
-- BAD: Inefficient query patterns
SELECT * FROM orders o
WHERE YEAR(o.created_at) = 2024
  AND o.customer_id IN (
      SELECT c.id FROM customers c WHERE c.status = 'active'
  );

-- GOOD: Optimized query with proper indexing hints
SELECT o.id, o.customer_id, o.total_amount, o.created_at
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01'
  AND o.created_at < '2025-01-01'
  AND c.status = 'active';

-- Required indexes:
-- CREATE INDEX idx_orders_created_at ON orders(created_at);
-- CREATE INDEX idx_customers_status ON customers(status);
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

**Step 5 — Review join shape and join semantics.**
Use the correct join type. Convert `LEFT JOIN` to `INNER JOIN` only when filters or business rules require a matching row and the result semantics remain unchanged. Push filters early when it helps the optimizer and does not alter outer-join behavior.

```sql
-- BAD: Inefficient JOIN order and conditions
SELECT o.*, c.name, p.product_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01'
  AND c.status = 'active';

-- GOOD: Optimized JOIN with filtering
SELECT o.id, o.total_amount, c.name, p.product_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id AND c.status = 'active'
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01';
```

**Step 6 — Replace expensive subquery patterns when appropriate.**
Use `EXISTS` instead of `IN` for subqueries when the engine and data distribution make it more efficient. Replace correlated aggregate subqueries with joins, derived tables, or window functions when that preserves semantics.

```sql
-- BAD: Correlated subquery
SELECT p.product_name, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(price)
    FROM products p2
    WHERE p2.category_id = p.category_id
);

-- GOOD: Window function approach
SELECT product_name, price
FROM (
    SELECT product_name, price,
           AVG(price) OVER (PARTITION BY category_id) as avg_category_price
    FROM products
) ranked
WHERE price > avg_category_price;
```

**Step 7 — Split complex OR predicates when it helps the optimizer.**
Consider `UNION ALL` when separate predicates can use separate indexes and duplicates are not a concern. Use `UNION` only when duplicate removal is required.

```sql
-- BAD: Complex OR conditions
SELECT * FROM products
WHERE (category = 'electronics' AND price < 1000)
   OR (category = 'books' AND price < 50);

-- GOOD: UNION approach for better optimization
SELECT * FROM products WHERE category = 'electronics' AND price < 1000
UNION ALL
SELECT * FROM products WHERE category = 'books' AND price < 50;
```

**Step 8 — Optimize pagination for large result sets.**
Use `LIMIT`, `TOP`, or engine-equivalent row limits for result set control. Avoid high-offset pagination for deep pages when cursor-based pagination can preserve user-visible ordering.

```sql
-- BAD: OFFSET-based pagination (slow for large offsets)
SELECT * FROM products
ORDER BY created_at DESC
LIMIT 20 OFFSET 10000;

-- GOOD: Cursor-based pagination
SELECT * FROM products
WHERE created_at < '2024-06-15 10:30:00'
ORDER BY created_at DESC
LIMIT 20;

-- Or using ID-based cursor
SELECT * FROM products
WHERE id > 1000
ORDER BY id
LIMIT 20;
```

When using cursor pagination, include a deterministic tie-breaker if the sort key is not unique, such as `(created_at, id)`.

**Step 9 — Consolidate aggregations.**
Combine related aggregation queries when one scan can produce the same result. Use conditional aggregation for status counts and similar dashboards.

```sql
-- BAD: Multiple separate aggregation queries
SELECT COUNT(*) FROM orders WHERE status = 'pending';
SELECT COUNT(*) FROM orders WHERE status = 'shipped';
SELECT COUNT(*) FROM orders WHERE status = 'delivered';

-- GOOD: Single query with conditional aggregation
SELECT
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'shipped' THEN 1 END) as shipped_count,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count
FROM orders;
```

**Step 10 — Batch bulk operations.**
Avoid row-by-row inserts, updates, or deletes when a set-based or batched operation is available and safe. Choose batch size based on transaction log pressure, lock duration, and application retry behavior.

```sql
-- BAD: Row-by-row operations
INSERT INTO products (name, price) VALUES ('Product 1', 10.00);
INSERT INTO products (name, price) VALUES ('Product 2', 15.00);
INSERT INTO products (name, price) VALUES ('Product 3', 20.00);

-- GOOD: Batch insert
INSERT INTO products (name, price) VALUES
('Product 1', 10.00),
('Product 2', 15.00),
('Product 3', 20.00);
```

**Step 11 — Use temporary tables for complex multi-step work.**
Use temporary tables when they reduce repeated expensive calculations, simplify complex operations, or allow useful intermediate indexing. Consider CTEs or derived tables first when the engine optimizes them well.

```sql
-- GOOD: Using temporary tables for complex operations
CREATE TEMPORARY TABLE temp_calculations AS
SELECT customer_id,
       SUM(total_amount) as total_spent,
       COUNT(*) as order_count
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY customer_id;

-- Use the temp table for further calculations
SELECT c.name, tc.total_spent, tc.order_count
FROM temp_calculations tc
JOIN customers c ON tc.customer_id = c.id
WHERE tc.total_spent > 1000;
```

**Step 12 — Design indexes from the query pattern.**
Create indexes on frequently queried columns, join keys, sort keys, and selective filters. Choose composite index order based on equality filters first, then range filters and ordering needs, while considering selectivity and engine behavior. Avoid over-indexing because every index adds storage and slows inserts, updates, and deletes.

```sql
-- BAD: Poor indexing strategy
CREATE INDEX idx_user_data ON users(email, first_name, last_name, created_at);

-- GOOD: Optimized composite indexing
-- For queries filtering by email first, then sorting by created_at
CREATE INDEX idx_users_email_created ON users(email, created_at);

-- For full-text name searches
CREATE INDEX idx_users_name ON users(last_name, first_name);

-- For user status queries
CREATE INDEX idx_users_status_created ON users(status, created_at)
WHERE status IS NOT NULL;
```

Use covering indexes when the engine can satisfy the query from the index alone.

```sql
-- GOOD: Covering index design
CREATE INDEX idx_orders_covering
ON orders(customer_id, created_at)
INCLUDE (total_amount, status);  -- SQL Server syntax
-- Or: CREATE INDEX idx_orders_covering ON orders(customer_id, created_at, total_amount, status); -- Other databases
```

Use partial indexes for specific high-value conditions when the engine supports them.

```sql
-- GOOD: Partial indexes for specific conditions
CREATE INDEX idx_orders_active
ON orders(created_at)
WHERE status IN ('pending', 'processing');
```

**Step 13 — Check schema, data type, and partition fit.**
Use appropriate data types for storage efficiency. Normalize appropriately: 3NF for OLTP, denormalized structures for OLAP when justified by read patterns. Use constraints to help the query optimizer. Consider partitioning large tables only when partition pruning, maintenance, or lifecycle management provides a measurable benefit.

**Step 14 — Detect N+1 and repeated-query patterns.**
Look for loops in application code that execute one SQL statement per row or entity. Replace N+1 access with joins, batched `IN` lookups, eager fetches, or explicit aggregate queries that match the repository's data-access style.

**Step 15 — Use prepared statements for repeated queries.**
Prefer prepared statements or parameterized queries for repeated execution. This can reduce parse overhead and supports safer parameter binding. Do not concatenate untrusted input into SQL.

**Step 16 — Use database monitoring views carefully.**
When diagnosing slow queries, use the engine's native views or logs and label the syntax.

```sql
-- Generic approach to identify slow queries
-- (Specific syntax varies by database)

-- For MySQL:
SELECT query_time, lock_time, rows_sent, rows_examined, sql_text
FROM mysql.slow_log
ORDER BY query_time DESC;

-- For PostgreSQL:
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC;

-- For SQL Server:
SELECT
    qs.total_elapsed_time/qs.execution_count as avg_elapsed_time,
    qs.execution_count,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
        ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) as query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;
```

**Step 17 — Apply the universal optimization checklist.**
Use this checklist before finalizing recommendations.

### Query Structure

- [ ] Avoiding `SELECT *` in production queries
- [ ] Using appropriate JOIN types (`INNER` vs `LEFT`/`RIGHT`)
- [ ] Filtering early in WHERE clauses
- [ ] Using `EXISTS` instead of `IN` for subqueries when appropriate
- [ ] Avoiding functions in WHERE clauses that prevent index usage

### Index Strategy

- [ ] Creating indexes on frequently queried columns
- [ ] Using composite indexes in the right column order
- [ ] Avoiding over-indexing because it impacts `INSERT`/`UPDATE` performance
- [ ] Using covering indexes where beneficial
- [ ] Creating partial indexes for specific query patterns

### Data Types and Schema

- [ ] Using appropriate data types for storage efficiency
- [ ] Normalizing appropriately: 3NF for OLTP, denormalized for OLAP
- [ ] Using constraints to help the query optimizer
- [ ] Partitioning large tables when appropriate

### Query Patterns

- [ ] Using `LIMIT`/`TOP` for result set control
- [ ] Implementing efficient pagination strategies
- [ ] Using batch operations for bulk data changes
- [ ] Avoiding N+1 query problems
- [ ] Using prepared statements for repeated queries

### Performance Testing

- [ ] Testing queries with realistic data volumes
- [ ] Analyzing query execution plans
- [ ] Monitoring query performance over time
- [ ] Setting up alerts for slow queries
- [ ] Regular index usage analysis

**Step 18 — Follow the optimization methodology.**
Use this loop for every optimization:

1. **Identify** — Use database-specific tools to find slow queries.
2. **Analyze** — Examine execution plans and identify bottlenecks.
3. **Optimize** — Apply appropriate optimization techniques.
4. **Test** — Verify performance improvements.
5. **Monitor** — Continuously track performance metrics.
6. **Iterate** — Perform regular performance review and optimization.

**Step 19 — Report validation and trade-offs.**
Explain expected or measured performance impact, validation evidence, and rollback considerations. State when an index or rewrite improves reads but may slow writes. If realistic data volumes are unavailable, report that limitation and provide the exact validation query or command the user should run.

## Invocation Example

```
/sql-optimization target=queries/orders-report.sql engine=postgresql
```

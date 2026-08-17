---
name: sql-optimization
description: >-
  Universal SQL performance optimization assistant for query tuning, execution-plan review, index strategy, pagination, batching, aggregation, and monitoring across MySQL, PostgreSQL, SQL Server, Oracle, and other SQL databases. Use this skill when the user asks to optimize slow SQL, review query plans, improve indexes, fix SELECT performance, reduce N+1 queries, tune pagination, or analyze database performance.
---

# SQL performance optimization

Optimize selected SQL or a project's database access by identifying measurable bottlenecks, rewriting queries into index-friendly forms, choosing practical indexes, and validating changes with realistic execution plans and data volumes.

## When to invoke

- "Optimize this slow SQL query."
- "Review this execution plan and suggest indexes."
- "Fix pagination performance for this table."
- "Find SQL anti-patterns in this repository."
- "Improve batch inserts or aggregation queries."

## Criteria

### Query structure

| Anti-pattern | Why it is slow | Prefer |
| --- | --- | --- |
| `SELECT *` in production queries | Reads and transfers unused columns; blocks covering indexes. | Select only required columns. |
| Function on indexed column in `WHERE`, such as `YEAR(created_at)` or `UPPER(customer_email)` | Prevents normal index seeks. | Use sargable ranges or normalized/search columns. |
| Large `IN (SELECT ...)` without optimizer-friendly shape | Can produce poor join plans. | `INNER JOIN`, `EXISTS`, or pre-aggregated sets depending on cardinality. |
| Complex `OR` across different predicates | May prevent selective index usage. | Split into `UNION ALL` branches when duplicates are not possible or acceptable. |
| N+1 query pattern | Repeats database round trips per row. | Join, batch load, eager load, or use set-based queries. |

```sql
-- BAD: function in predicate, SELECT *, and subquery shape
SELECT * FROM orders o
WHERE YEAR(o.created_at) = 2024
  AND o.customer_id IN (
      SELECT c.id FROM customers c WHERE c.status = 'active'
  );

-- GOOD: explicit columns, sargable date range, join filter
SELECT o.id, o.customer_id, o.total_amount, o.created_at
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01'
  AND o.created_at < '2025-01-01'
  AND c.status = 'active';

-- Candidate indexes:
-- CREATE INDEX idx_orders_created_at ON orders(created_at);
-- CREATE INDEX idx_customers_status ON customers(status);
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### Join and subquery rewrites

```sql
-- BAD: LEFT JOINs filtered as INNER JOINs by the WHERE clause
SELECT o.*, c.name, p.product_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01'
  AND c.status = 'active';

-- GOOD: correct join type, filtered early, explicit columns
SELECT o.id, o.total_amount, c.name, p.product_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id AND c.status = 'active'
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01';
```

```sql
-- BAD: correlated subquery per row
SELECT p.product_name, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(price)
    FROM products p2
    WHERE p2.category_id = p.category_id
);

-- GOOD: window function computes the category average once per partition
SELECT product_name, price
FROM (
    SELECT product_name, price,
           AVG(price) OVER (PARTITION BY category_id) AS avg_category_price
    FROM products
) ranked
WHERE price > avg_category_price;
```

### Index strategy

| Rule | Application |
| --- | --- |
| Put equality filters before range and sort columns in composite indexes. | `CREATE INDEX idx_users_email_created ON users(email, created_at);` |
| Build different indexes for different access paths. | `idx_users_name` on `(last_name, first_name)` for name search; `idx_users_status_created` on `(status, created_at)` for status timelines. |
| Avoid over-indexing. | Every index adds write cost to `INSERT`, `UPDATE`, and `DELETE`. |
| Use covering indexes for hot read paths. | SQL Server: `INCLUDE (total_amount, status)`; other databases often append covered columns to the index. |
| Use filtered or partial indexes when supported. | `CREATE INDEX idx_orders_active ON orders(created_at) WHERE status IN ('pending', 'processing');` |

```sql
-- Poor: one broad index that may not match any query well
CREATE INDEX idx_user_data ON users(email, first_name, last_name, created_at);

-- Better: indexes aligned to real predicates and sorts
CREATE INDEX idx_users_email_created ON users(email, created_at);
CREATE INDEX idx_users_name ON users(last_name, first_name);
CREATE INDEX idx_users_status_created ON users(status, created_at)
WHERE status IS NOT NULL;
```

```sql
CREATE INDEX idx_orders_covering
ON orders(customer_id, created_at)
INCLUDE (total_amount, status);  -- SQL Server syntax

-- Other databases often require covered columns in the key:
-- CREATE INDEX idx_orders_covering ON orders(customer_id, created_at, total_amount, status);
```

### Pagination, aggregation, and batching

```sql
-- BAD: large OFFSET scans and discards rows
SELECT * FROM products
ORDER BY created_at DESC
LIMIT 20 OFFSET 10000;

-- GOOD: cursor pagination by stable sort key
SELECT * FROM products
WHERE created_at < '2024-06-15 10:30:00'
ORDER BY created_at DESC
LIMIT 20;

-- GOOD: ID cursor when ID order is the product order
SELECT * FROM products
WHERE id > 1000
ORDER BY id
LIMIT 20;
```

```sql
-- BAD: multiple scans
SELECT COUNT(*) FROM orders WHERE status = 'pending';
SELECT COUNT(*) FROM orders WHERE status = 'shipped';
SELECT COUNT(*) FROM orders WHERE status = 'delivered';

-- GOOD: conditional aggregation in one scan
SELECT
    COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_count,
    COUNT(CASE WHEN status = 'shipped' THEN 1 END) AS shipped_count,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) AS delivered_count
FROM orders;
```

```sql
-- BAD: row-by-row insert
INSERT INTO products (name, price) VALUES ('Product 1', 10.00);
INSERT INTO products (name, price) VALUES ('Product 2', 15.00);
INSERT INTO products (name, price) VALUES ('Product 3', 20.00);

-- GOOD: batch insert
INSERT INTO products (name, price) VALUES
('Product 1', 10.00),
('Product 2', 15.00),
('Product 3', 20.00);
```

Use temporary tables for complex multi-step calculations when they reduce repeated scans and make later joins cheaper.

```sql
CREATE TEMPORARY TABLE temp_calculations AS
SELECT customer_id,
       SUM(total_amount) AS total_spent,
       COUNT(*) AS order_count
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY customer_id;

SELECT c.name, tc.total_spent, tc.order_count
FROM temp_calculations tc
JOIN customers c ON tc.customer_id = c.id
WHERE tc.total_spent > 1000;
```

### Monitoring evidence

Use the database's native slow-query and statistics views. Syntax varies by vendor.

```sql
-- MySQL
SELECT query_time, lock_time, rows_sent, rows_examined, sql_text
FROM mysql.slow_log
ORDER BY query_time DESC;

-- PostgreSQL
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC;

-- SQL Server
SELECT
    qs.total_elapsed_time / qs.execution_count AS avg_elapsed_time,
    qs.execution_count,
    SUBSTRING(qt.text, (qs.statement_start_offset / 2) + 1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
        ELSE qs.statement_end_offset END - qs.statement_start_offset) / 2) + 1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;
```

## Procedure

1. Identify the slow query, endpoint, report, or workload and capture current runtime, row counts, and database engine.
2. Read the execution plan before rewriting; note scans, joins, sorts, spills, estimates vs actuals, and missing indexes.
3. Rewrite the query for set-based, sargable access and explicit columns.
4. Propose indexes only for observed predicates, joins, sorting, grouping, or covering needs.
5. Test with realistic data volumes and compare before/after plans and timings.
6. Check write-path impact from new indexes and remove redundant suggestions.
7. Report measurable improvement or the remaining blocker.

## Gotchas

- **Do not optimize without a baseline**: without runtime, plan, or row-count evidence, recommendations are guesses.
- **Do not apply vendor syntax blindly**: `INCLUDE`, partial indexes, `LIMIT`, and monitoring views differ by database.
- **Cursor pagination needs deterministic ordering**: include a unique tie-breaker when the sort column is not unique.
- **Covering indexes can become write bottlenecks**: include only columns needed by the hot read path.


## Additional anti-pattern examples

```sql
-- BAD: SELECT * with unnecessary joins and broad row shape
SELECT *
FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;

-- GOOD: explicit columns
SELECT lt.id, lt.name, at.value
FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;

-- BAD: function call blocks a normal email index
SELECT * FROM orders
WHERE UPPER(customer_email) = 'JOHN@EXAMPLE.COM';

-- GOOD: normalize input or add an expression index when the engine supports it
SELECT * FROM orders
WHERE customer_email = 'john@example.com';
-- Consider: CREATE INDEX idx_orders_email ON orders(LOWER(customer_email));
```

Also check `LEFT/RIGHT` join semantics, `RIGHT` joins that obscure intent, `LIMIT/TOP` result control, `INSERT/UPDATE` write cost from indexes, `OLTP` versus `OLAP` schema goals, `full-text` search needs, `database-specific` syntax, `by-row` loops, and `anti-pattern` evidence. Preserve SQL Server expressions such as `qs.total_elapsed_time/qs.execution_count` and `qs.statement_start_offset/2` when comparing plans.

## Output template

```markdown
## SQL optimization result

**Status:** optimized | recommendations only | blocked
**Database:** `<MySQL|PostgreSQL|SQL Server|Oracle|other>`
**Target:** `<query, file, endpoint, or workload>`

### Findings
| # | Severity | Evidence | Recommendation | Expected impact |
| --- | --- | --- | --- | --- |
| 1 | High | `<plan/runtime/line>` | `<query rewrite or index>` | `<why it helps>` |

### Proposed SQL
```sql
<rewritten query and indexes>
```

### Validation
- Baseline: `<runtime/plan/rows>`
- After change: `<runtime/plan/rows or not run>`
- Write impact checked: yes | no | not applicable
```

## Quality gate

- [ ] The database engine and version constraints were considered before vendor-specific syntax was suggested.
- [ ] Every recommendation cites query text, file/line, execution-plan evidence, or runtime evidence.
- [ ] Rewrites preserve result semantics.
- [ ] Index suggestions match observed filters, joins, sorts, grouping, or covering needs.
- [ ] Performance was validated with realistic data volume, or the lack of validation is explicit.
- [ ] Added indexes were checked for write-path and storage impact.

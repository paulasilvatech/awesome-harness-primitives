---
name: sql-code-review
description: >-
  Review SQL code across PostgreSQL, MySQL, SQL Server, and Oracle for injection risks, access
  control, data protection, performance, schema quality, and maintainability. Use when asked to
  "review SQL", "find SQL injection", "audit database code", "check stored procedures", or
  "perform SQL security analysis".
---

<!-- Generated from harness/github-copilot/skills/sql-code-review/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# SQL code review

Review selected SQL or an entire project, transform security, performance, schema, and maintainability evidence into prioritized findings, and return paste-ready safer SQL where appropriate.

## When to invoke

- "Review this SQL for security issues."
- "Find SQL injection risks in these queries."
- "Audit our stored procedures and permissions."
- "Check this migration for maintainability and schema quality."
- "Review SQL Server, PostgreSQL, MySQL, or Oracle code."

## Criteria

### Security analysis

Treat SQL injection as **CRITICAL** until proven otherwise; label parameterized forms as **SECURE**. Review `Function/Procedure` security and keep recommendations database-agnostic unless a platform-specific feature is clearly better.


| Risk | Bad pattern | Safer pattern |
| --- | --- | --- |
| SQL injection | `query = "SELECT * FROM users WHERE id = " + userInput;` | Bind parameters instead of concatenating strings. |
| Formatted-string injection | `query = f"DELETE FROM orders WHERE user_id = {user_id}";` | Use placeholders and driver parameters. |
| SQL Server dynamic SQL | Concatenating values into command text. | `EXEC sp_executesql N'SELECT * FROM users WHERE id = @id', N'@id INT', @id = @user_id;` |
| Broad privileges | Direct grants to users or `GRANT ALL`. | Role-Based Access with least privilege. |
| Sensitive exposure | `SELECT *` from tables with PII or secrets. | Select explicit safe columns, mask through views/functions, and audit sensitive operations. |
| Procedure rights | Unreviewed `DEFINER` or owner-executed functions. | Verify DEFINER vs INVOKER rights and schema ownership. |

Parameterized examples:

```sql
-- PostgreSQL/MySQL
PREPARE stmt FROM 'SELECT * FROM users WHERE id = ?';
EXECUTE stmt USING @user_id;

-- SQL Server
EXEC sp_executesql N'SELECT * FROM users WHERE id = @id', N'@id INT', @id = @user_id;
```

### Performance analysis

| Pattern | Review rule | Example fix |
| --- | --- | --- |
| Function in `WHERE` | Functions such as `YEAR(order_date)` can prevent index usage. | Use ranges: `order_date >= '2024-01-01' AND order_date < '2025-01-01'`. |
| Implicit joins | `FROM users u, orders o` hides missing join conditions. | Use explicit `INNER JOIN`, `LEFT JOIN`, or `EXISTS`. |
| `SELECT *` | Pulls unnecessary data and can expose sensitive columns. | Select only required columns. |
| N+1 queries | Application loop issues one query per row. | Fetch related rows with one join or batched query. |
| Overuse of `DISTINCT` | Masks join errors and adds sort/hash work. | Fix join cardinality; use `GROUP BY` only when aggregation is intended. |
| Correlated aggregate | Repeats subquery per group. | Aggregate once with `GROUP BY`. |
| Index gaps | Frequent filters/joins lack supporting indexes. | Recommend single, composite, covering, partial, GIN/GiST, columnstore, or engine-specific indexes as appropriate. |

Bad and good structure:

```sql
-- BAD: inefficient query patterns
SELECT DISTINCT u.*
FROM users u, orders o, products p
WHERE u.id = o.user_id
AND o.product_id = p.id
AND YEAR(o.order_date) = 2024;

-- GOOD: optimized structure
SELECT u.id, u.name, u.email
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= '2024-01-01'
AND o.order_date < '2025-01-01';
```

### Maintainability and schema quality

- [ ] Naming is consistent for tables, columns, constraints, indexes, procedures, and views.
- [ ] Identifiers avoid reserved words and inconsistent case sensitivity.
- [ ] Formatting uses readable indentation and one major clause per line.
- [ ] Complex logic has meaningful comments without restating obvious syntax.
- [ ] Data types match storage, precision, collation, timezone, and performance needs.
- [ ] Constraints enforce integrity: `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `NOT NULL`, and appropriate defaults.
- [ ] Normalization is intentional; over-normalization and duplicated mutable facts are both justified.
- [ ] Error handling exists in procedures/functions where failure modes matter.

Clean formatting example:

```sql
SELECT u.id,
       u.name,
       o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
  AND o.order_date >= '2024-01-01';
```

## Database-specific checks

| Engine | Prefer | Watch for |
| --- | --- | --- |
| PostgreSQL | `JSONB`, `TIMESTAMPTZ`, arrays where appropriate, `JSON` when the engine lacks binary JSON, GIN indexes for JSONB/arrays, and multi-value arrays such as `post_id INT` with `tag_names TEXT[]`. | Treating JSONB as text, missing `gin(data)`, wrong timezone type. |
| MySQL | `ENGINE=InnoDB`, covering indexes such as `(status, created_at, id)`. | Wrong storage engine, poor character set/collation choices. |
| SQL Server | `BIGINT`, `NVARCHAR`, `DATETIME2`, `DECIMAL`, `IDENTITY`, `GETUTCDATE()`, columnstore indexes for analytics. | Dynamic SQL injection, missing schema qualification, inappropriate wide clustered keys. |
| Oracle | Sequences such as `user_id_seq.NEXTVAL`, `NUMBER`, `VARCHAR2`, and explicit auto-increment design. | Trigger/sequence misuse, implicit date conversions, unbounded privileges. |

Examples to recognize:

```sql
-- PostgreSQL JSONB and GIN
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_events_data ON events USING gin(data);

-- MySQL InnoDB
CREATE TABLE sessions (
    id VARCHAR(128) PRIMARY KEY,
    data TEXT,
    expires TIMESTAMP
) ENGINE=InnoDB;
ALTER TABLE large_table ADD INDEX idx_covering (status, created_at, id);

-- SQL Server columnstore
CREATE COLUMNSTORE INDEX idx_sales_cs ON sales;

-- Oracle sequence
CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;
CREATE TABLE users (
    id NUMBER DEFAULT user_id_seq.NEXTVAL PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);
```

## Anti-pattern review

Call out each anti-pattern by name: N+1 queries, overuse of `DISTINCT`, functions in `WHERE`, over/under-normalization and under-normalization, and correlated aggregates such as `order_count` subqueries.

## Validation checks

Use data integrity and execution-plan evidence when available:

```sql
-- Verify referential integrity
SELECT o.user_id
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;

-- Check for data consistency
SELECT COUNT(*) as inconsistent_records
FROM products
WHERE price < 0 OR stock_quantity < 0;
```

Review execution plans, load behavior with realistic data volumes, concurrency stress, and regression risk. Do not claim performance improvement without plan evidence, index rationale, or a clear complexity reduction.

## Output template

```markdown
## SQL code review - <file, selection, or project>

**Verdict:** Pass | Fix required | Reject
**Security Score:** <1-10> - <reason>
**Performance Score:** <1-10> - <reason>
**Maintainability Score:** <1-10> - <reason>
**Schema Quality Score:** <1-10> - <reason>

| # | Priority | Category | Location | Finding | Evidence | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Critical/High/Medium/Low | Security/Performance/Quality/Schema | <table/view/procedure and line> | <brief description> | <SQL snippet or plan detail> | <specific fix> |

### Issue detail
## [PRIORITY] [CATEGORY]: [Brief Description]

**Location**: [Table/View/Procedure name and line number if applicable]
**Issue**: [Detailed explanation of the problem]
**Security Risk**: [If applicable - injection risk, data exposure, etc.]
**Performance Impact**: [Query cost, execution time impact]
**Recommendation**: [Specific fix with code example]

**Before**:
```sql
-- Problematic SQL
```

**After**:
```sql
-- Improved SQL
```

**Expected Improvement**: [Performance gain, security benefit]

### Top 3 priority actions
1. **[Critical Security Fix]**: <action>
2. **[Performance Optimization]**: <action>
3. **[Code Quality]**: <action>
```

## Quality gate

- [ ] Every user input path is parameterized; no dynamic SQL uses string concatenation for values.
- [ ] Access control follows least privilege through roles, schemas, and procedure rights.
- [ ] Sensitive data exposure, audit logging, masking, and encryption concerns were checked.
- [ ] Index, join, aggregation, subquery, and `WHERE` clause patterns were reviewed.
- [ ] Engine-specific recommendations are labeled for PostgreSQL, MySQL, SQL Server, or Oracle.
- [ ] Every finding has concrete evidence and an actionable recommendation.
- [ ] Scores are justified and the top three actions match the highest risks.

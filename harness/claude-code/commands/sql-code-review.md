---
description: >-
  Review SQL code across database engines for security, maintainability, quality, and
  best-practice issues.
argument-hint: "target=<selection-or-project> engine=<postgresql|mysql|sqlserver|oracle|other>"
allowed-tools: Read, Grep, Glob, Edit, Write
---

<!-- Generated from harness/github-copilot/prompts/sql-code-review.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /sql-code-review

## Objective

Perform a thorough SQL code review of `${selection}` or the requested project scope, focusing on security, performance, maintainability, schema quality, and database-specific best practices across PostgreSQL, MySQL, SQL Server, Oracle, and other SQL engines.

## When to Invoke

Use this prompt when reviewing SQL queries, migrations, stored procedures, repository SQL, schema definitions, or database access patterns before merging or release.

## Preconditions

- The SQL code, selected text, migration, stored procedure, repository method, or project scope is available.
- The target database engine is known, or findings can be labeled database-agnostic until the engine is provided.
- The review scope permits inspecting related schema, indexes, and data-access code.
- Security and performance findings can cite a location such as table, view, procedure, file, or line number when available.

## Inputs the Team Must Provide

- `target` — `${selection}`, a file, a migration, a procedure, or a project area to review.
- `engine` — PostgreSQL, MySQL, SQL Server, Oracle, or another engine.
- Schema context — tables, columns, constraints, indexes, procedures, functions, and permissions.
- Risk context — sensitive data, write paths, user input sources, performance concerns, and deployment environment.
- Ask the user for anything that is missing, especially the database engine, schema context, or review scope.

## What I Will Do

- Review for SQL injection, dynamic SQL string concatenation, unsafe deletes, and missing parameterization.
- Check access control, least privilege, role-based access, schema ownership, and `DEFINER` versus `INVOKER` rights.
- Look for sensitive data exposure, audit logging gaps, data masking needs, and encryption expectations.
- Analyze query structure, indexes, joins, aggregates, window functions, and anti-patterns such as N+1 access.
- Review formatting, naming conventions, reserved words, case sensitivity, comments, and maintainability.
- Check schema design for normalization, data types, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `NOT NULL`, and default values.
- Call out PostgreSQL, MySQL, SQL Server, and Oracle best practices only when relevant to the engine.
- Produce prioritized issues with before/after SQL and top actions.

## What I Will NOT Do

- Execute destructive SQL or modify production data.
- Claim a vulnerability, performance impact, or expected improvement without evidence or a labeled assumption.
- Apply platform-specific advice as universal SQL.
- Recommend indexes without considering existing indexes, write overhead, maintenance, and query pattern fit.
- Rewrite SQL in a way that changes result semantics without explicitly flagging the behavior change.
- Mask join mistakes with `DISTINCT` without explaining the underlying issue.
- Ignore sensitive data exposure caused by `SELECT *`.

## Output Format

Return the review in this format:

````markdown
## SQL Code Review

### Summary Assessment
- **Security Score**: 7/10 — SQL injection protection, access controls
- **Performance Score**: 6/10 — Query efficiency, index usage
- **Maintainability Score**: 8/10 — Code quality, documentation
- **Schema Quality Score**: 7/10 — Design patterns, normalization

### Findings

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

### Top 3 Priority Actions
1. **[Critical Security Fix]**: Address SQL injection vulnerabilities.
2. **[Performance Optimization]**: Add missing indexes or optimize queries.
3. **[Code Quality]**: Improve naming conventions and documentation.

### Review Checklist
- Security: pass/fail with evidence
- Performance: pass/fail with evidence
- Code Quality: pass/fail with evidence
- Schema Design: pass/fail with evidence
````

## Definition of Done

- [ ] All user input paths are reviewed for parameterization.
- [ ] No dynamic SQL construction with string concatenation is left unflagged.
- [ ] Access controls, permissions, and sensitive data handling are evaluated.
- [ ] Query performance issues cite a concrete pattern, plan evidence, or labeled assumption.
- [ ] Index recommendations include purpose and trade-offs.
- [ ] Database-specific recommendations are labeled by engine.
- [ ] Findings include priority, category, location, recommendation, and expected improvement.
- [ ] The review includes security, performance, code quality, and schema design checklist results.

## Prompt Body

Follow these steps in order.

**Step 1 — Establish scope and engine.**
Review `${selection}` when present, or inspect the requested project scope. Identify the database engine and label unknowns. Focus on actionable, database-agnostic recommendations while highlighting platform-specific optimizations and best practices.

**Step 2 — Review SQL injection prevention.**
Flag any query built from user input with string concatenation, including patterns like `query = "SELECT * FROM users WHERE id = " + userInput;` and `query = f"DELETE FROM orders WHERE user_id = {user_id}";`. Recommend parameterized queries such as PostgreSQL/MySQL `PREPARE stmt FROM 'SELECT * FROM users WHERE id = ?'; EXECUTE stmt USING @user_id;` or SQL Server `EXEC sp_executesql N'SELECT * FROM users WHERE id = @id', N'@id INT', @id = @user_id;`.

**Step 3 — Review access control and data protection.**
Apply the principle of least privilege. Prefer database roles over direct user permissions. Check schema security, proper schema ownership, access controls, function/procedure security, and `DEFINER` versus `INVOKER` rights. Avoid `SELECT *` on tables with sensitive columns. Verify audit logging, data masking through views or functions, and encrypted storage for sensitive data.

**Step 4 — Analyze query structure.**
Flag inefficient patterns such as `SELECT DISTINCT u.* FROM users u, orders o, products p WHERE u.id = o.user_id AND o.product_id = p.id AND YEAR(o.order_date) = 2024;`. Prefer explicit columns, explicit joins, and date ranges such as `SELECT u.id, u.name, u.email FROM users u INNER JOIN orders o ON u.id = o.user_id WHERE o.order_date >= '2024-01-01' AND o.order_date < '2025-01-01';`.

**Step 5 — Review index strategy.**
Identify missing indexes for frequently queried columns, unused or redundant indexes, composite indexes for complex queries, and index maintenance concerns such as fragmented or outdated indexes. Consider over-indexing and write overhead before recommending an index.

**Step 6 — Review joins, aggregates, and window functions.**
Verify appropriate join types (`INNER` vs `LEFT` vs `EXISTS`), join order, smaller result sets first, missing join conditions, and Cartesian products. Compare subquery versus `JOIN` approaches. Replace inefficient correlated aggregate patterns such as `SELECT user_id, (SELECT COUNT(*) FROM orders o2 WHERE o2.user_id = o1.user_id) as order_count FROM orders o1 GROUP BY user_id;` with `SELECT user_id, COUNT(*) as order_count FROM orders GROUP BY user_id;` when semantics match.

**Step 7 — Review style and maintainability.**
Flag poor formatting like `select u.id,u.name,o.total from users u left join orders o on u.id=o.user_id where u.status='active' and o.order_date>='2024-01-01';`. Prefer readable formatting with uppercase keywords, one selected column per line for complex queries, clear indentation, and meaningful comments for complex logic.

**Step 8 — Review naming and schema design.**
Check consistent naming for tables, columns, constraints, and database objects. Prefer descriptive names. Avoid reserved words as identifiers. Maintain consistent case usage across schema. Check normalization level, avoid over/under-normalization, choose optimal data types, and enforce integrity through `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `NOT NULL`, and appropriate default values.

**Step 9 — Apply database-specific best practices.**
For PostgreSQL, prefer `JSONB` for JSON data when appropriate, `TIMESTAMPTZ DEFAULT NOW()` for timestamp defaults, GIN indexes such as `CREATE INDEX idx_events_data ON events USING gin(data);`, and array types like `TEXT[]` for true multi-value columns. For MySQL, use appropriate storage engines such as `ENGINE=InnoDB` and covering indexes such as `ALTER TABLE large_table ADD INDEX idx_covering (status, created_at, id);`. For SQL Server, use data types such as `BIGINT IDENTITY(1,1)`, `NVARCHAR(255)`, `DECIMAL(10,2)`, `DATETIME2 DEFAULT GETUTCDATE()`, and columnstore indexes such as `CREATE COLUMNSTORE INDEX idx_sales_cs ON sales;` for analytics. For Oracle, use sequences such as `CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;` and `user_id_seq.NEXTVAL` defaults when appropriate.

Use PostgreSQL array examples such as `post_id INT` with `tag_names TEXT[]` when reviewing multi-value tags. For Oracle, describe sequences as the auto-increment equivalent when comparing identity strategies across engines.

**Step 10 — Validate data integrity and performance assumptions.**
Suggest data integrity checks such as `SELECT o.user_id FROM orders o LEFT JOIN users u ON o.user_id = u.id WHERE u.id IS NULL;` and `SELECT COUNT(*) as inconsistent_records FROM products WHERE price < 0 OR stock_quantity < 0;`. Review execution plans, load testing with realistic data volumes, stress testing under concurrent load, and regression testing to ensure optimizations do not break functionality.

**Step 11 — Flag common anti-patterns.**
Identify N+1 query problems such as application loops that run `SELECT * FROM orders WHERE user_id = ?` per user; recommend a single query like `SELECT u.*, o.* FROM users u LEFT JOIN orders o ON u.id = o.user_id;` when appropriate. Flag overuse of `DISTINCT` masking join issues, for example `SELECT DISTINCT u.name FROM users u, orders o WHERE u.id = o.user_id;`, and prefer proper joins with explicit grouping when needed. Flag functions in `WHERE` clauses such as `WHERE YEAR(order_date) = 2024` and prefer range conditions.

**Step 12 — Complete the SQL review checklist.**
Security: all user inputs are parameterized; no dynamic SQL construction with string concatenation; appropriate access controls and permissions; sensitive data is properly protected; SQL injection attack vectors are eliminated. Performance: indexes exist for frequently queried columns; no unnecessary `SELECT *`; joins are optimized and use appropriate types; `WHERE` clauses are selective and use indexes; subqueries are optimized or converted to joins. Code quality: consistent naming conventions; proper formatting and indentation; meaningful comments for complex logic; appropriate data types; error handling is implemented. Schema design: tables are properly normalized; constraints enforce data integrity; indexes support query patterns; foreign key relationships are defined; default values are appropriate.

**Step 13 — Prioritize and report.**
Classify issues by priority and category. Include before/after SQL where possible, expected improvement, security risk, performance impact, and top three priority actions.

## Invocation Example

```
/sql-code-review target=${selection} engine=postgresql
```

---
paths:
  - "**/*.sql"
---

<!-- Generated from harness/github-copilot/instructions/sql-sp-generation.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for SQL schema generation, query style, stored procedure naming, parameter handling, security, and transactions.

# SQL and Stored Procedure Conventions — Schema and Query Hygiene

These instructions apply to SQL files matched by the `applyTo` glob. They are authoritative for schema naming, constraints, query structure, stored procedure shape, parameter handling, SQL security, and transaction hygiene; database-engine-specific standards and migration tooling win when they impose stricter syntax, deployment, or compatibility rules.

## Schema Generation and Constraints

Design tables and relationships consistently so schema diffs are predictable and generated SQL remains maintainable.

| Element | Convention |
| --- | --- |
| Table names | Use singular form |
| Column names | Use singular form |
| Primary key column | Include `id` on every table |
| Audit columns | Include `created_at` and `updated_at` |
| Primary key constraint | Define a primary key constraint for every table |
| Foreign key name | Name every foreign key constraint |
| Foreign key placement | Define foreign keys inline where the engine supports it |
| Referential actions | Use `ON DELETE CASCADE` and `ON UPDATE CASCADE` when child rows must follow the parent |
| Parent target | Reference the parent table primary key |

Use cascade actions deliberately. If cascade behavior could delete business-critical history, document the exception in the database-specific migration or review note.

## Query Style and Structure

- Use uppercase SQL keywords such as `SELECT`, `FROM`, and `WHERE`.
- Use consistent indentation for nested queries, joins, and conditions.
- Break long queries into multiple lines for readability.
- Organize clauses consistently as `SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, and `ORDER BY`.
- Use explicit column names instead of `SELECT *`.
- Qualify columns with a table name or alias when multiple tables participate.
- Prefer joins over subqueries when a join is clearer and performs well.
- Include `LIMIT` or `TOP` clauses (`LIMIT/TOP`) when returning unbounded result sets is unnecessary.
- Add appropriate indexes for frequently queried columns.
- Avoid functions on indexed columns in `WHERE` clauses because they can prevent index usage.
- Comment complex logic, not ordinary SQL syntax.

## Stored Procedure Shape

Stored procedures must be discoverable, predictable, and safe to call from application code.

| Concern | Convention |
| --- | --- |
| Prefix | Start stored procedure names with `usp_` |
| Name casing | Use PascalCase after the prefix, for example `usp_GetCustomerOrders` |
| Purpose | Use descriptive names that state the operation |
| Multiple rows | Use a plural noun, for example `usp_GetProducts` |
| Single row | Use a singular noun, for example `usp_GetProduct` |
| Header | Include a header comment block with description, parameters, and return values |
| Result shape | Return result sets with consistent column order |
| Status | Use OUTPUT parameters for status information when needed |
| Temporary tables | Prefix temporary tables with `tmp_` |
| DML procedures | Include `SET NOCOUNT ON` for procedures that modify data |
| Errors | Return standardized error codes or messages (`codes/messages`) without exposing system details |

## Parameters, Security, and Dynamic SQL

- Prefix parameters with `@`.
- Use camelCase for parameter names.
- Put required parameters before optional parameters.
- Provide default values for optional parameters.
- Validate parameter values before use.
- Document parameters with comments when the procedure header is not enough.
- Parameterize all queries to prevent SQL injection.
- Use prepared statements when executing dynamic SQL.
- Avoid dynamic SQL inside stored procedures unless there is no safer static alternative.
- Never embed credentials in SQL scripts.
- Handle errors without leaking internal server, schema, or stack details.

## Transactions and Large Operations

- Explicitly begin and commit transactions around multi-statement changes that must be atomic.
- Choose isolation levels based on consistency and concurrency requirements.
- Avoid long-running transactions that lock tables.
- Use batch processing for large data operations.
- Roll back on failures so partial writes do not survive.

## Good / Bad Examples

The examples below illustrate a safe stored procedure shape with named parameters, `SET NOCOUNT ON`, and explicit columns.

**Good:**

```sql
CREATE PROCEDURE usp_GetProduct
    @productId INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        product.id,
        product.name,
        product.updated_at
    FROM product
    WHERE product.id = @productId;
END;
```

Why: The procedure uses the required prefix and casing, a singular noun for one row, an explicit parameter, `SET NOCOUNT ON`, and an explicit column list.

**Bad:**

```sql
CREATE PROCEDURE GetStuff
AS
BEGIN
    SELECT * FROM product WHERE LOWER(name) = 'chair';
END;
```

Why: The name is vague, the prefix is missing, the query uses `SELECT *`, a literal value, and a function on a filtered column.

## Conventions

| Rule | Rationale |
|---|---|
| Use singular table and column names with `id`, `created_at`, and `updated_at` | Generated schemas remain consistent and auditable |
| Name primary and foreign key constraints and reference parent primary keys | Relationship errors are diagnosable and migrations stay deterministic |
| Use uppercase SQL keywords and consistent clause ordering | Queries are easier to scan and review |
| Select explicit columns and qualify names when joining | Result shapes stay stable and ambiguity is avoided |
| Prefix stored procedures with `usp_` and use PascalCase descriptive names | Procedures are discoverable and intent is clear |
| Prefix parameters with `@`, use camelCase, validate inputs, and document optional defaults | Procedure contracts are safe and predictable |
| Parameterize queries and prepared dynamic SQL; avoid embedded credentials | SQL injection and credential leakage are prevented |
| Keep transactions explicit, bounded, and batch large operations | Data remains consistent without excessive locks |

## Do / Do Not

| Do | Do not |
|---|---|
| Define `id`, `created_at`, and `updated_at` on generated tables | Create anonymous key or audit conventions per table |
| Use named inline foreign keys with `ON DELETE CASCADE` and `ON UPDATE CASCADE` when appropriate | Leave foreign key behavior implicit or unnamed |
| Write `SELECT` lists explicitly | Use `SELECT *` in application-facing queries |
| Add `LIMIT` or `TOP` for bounded reads | Return unlimited rows when the caller needs a page or sample |
| Use `usp_GetProducts` and `usp_GetProduct` style names | Use vague procedure names such as `GetStuff` |
| Use prepared statements for unavoidable dynamic SQL | Concatenate untrusted values into SQL |
| Use `SET NOCOUNT ON` in modifying stored procedures | Return noisy row-count messages from DML procedures |
| Keep transactions short and intentional | Hold locks across long-running batch work |

## Checklist Before Opening a PR

- [ ] Tables and columns use singular names and every table has `id`, `created_at`, and `updated_at`.
- [ ] Primary keys and named foreign keys are present, inline where supported, and reference parent primary keys.
- [ ] Cascade rules, including `ON DELETE CASCADE` and `ON UPDATE CASCADE`, are intentional.
- [ ] SQL keywords are uppercase and clauses are consistently ordered and indented.
- [ ] Queries use explicit columns, qualified names for joins, bounded result sets, and index-friendly filters.
- [ ] Stored procedures use `usp_`, PascalCase, descriptive singular or plural nouns, and consistent result columns.
- [ ] Parameters use `@`, camelCase, required-first ordering, validation, comments, and optional defaults where needed.
- [ ] Dynamic SQL is avoided or prepared, credentials are absent, and errors do not expose system details.
- [ ] Transactions are explicit, bounded, use appropriate isolation, and batch large operations.

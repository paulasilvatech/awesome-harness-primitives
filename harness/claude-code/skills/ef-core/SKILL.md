---
name: ef-core
description: >-
  Review or design Entity Framework Core data access using DbContext, entity mapping, LINQ
  queries, migrations, change tracking, performance, security, and tests. Use when the user asks
  for EF Core best practices, Entity Framework Core code review, query optimization, migration
  guidance, or database access improvements in .NET.
---

<!-- Generated from harness/github-copilot/skills/ef-core/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Entity Framework Core

Evaluate EF Core code or propose implementation changes; transform DbContext, entity, query, migration, and test concerns into concrete .NET guidance that avoids common correctness, performance, and security failures.

## When to invoke

- "Review this Entity Framework Core code."
- "Give EF Core best practices for this DbContext."
- "Fix this EF Core migration or query pattern."
- "Avoid N+1 queries in this repository."
- "How should I test EF Core data access?"

## DbContext and model design

| Area | Preferred practice | Watch for |
| --- | --- | --- |
| DbContext focus | Keep `DbContext` classes cohesive around one bounded context. | A single context owning unrelated schemas and migrations. |
| Configuration | Use constructor injection for `DbContextOptions<TContext>`. | Manually constructing options in application code. |
| Model building | Override `OnModelCreating` and move complex mapping to `IEntityTypeConfiguration<T>`. | Large unstructured model configuration blocks. |
| Factories | Use `IDbContextFactory<TContext>` or `DbContextFactory` patterns for console apps, background tasks, and tests that need explicit lifetimes. | Capturing scoped contexts in long-lived services. |
| Entity keys | Choose surrogate or natural keys deliberately. | Meaningless keys plus missing uniqueness constraints. |
| Relationships | Configure one-to-one, one-to-many, and many-to-many relationships explicitly when conventions are ambiguous. | Shadow foreign keys created accidentally. |
| Value objects | Use owned entity types for value objects. | Flattening important concepts into unrelated primitive columns. |

## Querying and performance

| Pattern | Use | Avoid |
| --- | --- | --- |
| `AsNoTracking()` | Read-only queries that do not update returned entities. | Applying it when later calling `SaveChanges()` on the same entity instances. |
| Projection with `Select` | Fetch only columns needed by the API or view. | Loading full entities for DTO responses. |
| `Include()` | Eager-load related data when the result genuinely needs navigations. | Blanket includes that create cartesian explosion. |
| Pagination with `Skip()` and `Take()` | Large result sets with deterministic `OrderBy`. | Unbounded queries returned to UI or API callers. |
| Compiled queries | Hot paths executed frequently with stable shape. | Premature use for one-off queries. |
| Query composition | Keep `IQueryable` inside data boundaries and understand when execution occurs. | Returning unbounded `IQueryable` from public APIs. |
| Database functions | Complex operations that must execute in SQL. | Client-side filtering after materialization. |
| Specification pattern | Reusable query rules with clear ownership. | Copy-pasted predicates across repositories. |

## LINQ operator reminders

Prefer `strongly-typed` LINQ over raw SQL for normal data access. Common operators include `Where`, `OrderBy`, `GroupBy`, `Skip`, `Take`, and `Select`; use `AsNoTracking()` for `read-only` result sets.
## Migrations and deployment

| Practice | Rule |
| --- | --- |
| Small migrations | Create small, focused migrations and name migrations descriptively. |
| SQL review | Verify generated migration SQL scripts before production deployment. |
| Migration bundles | Consider migration bundles for controlled deployment where supported. |
| Data seeding | Add deterministic seed data through migrations when appropriate. |
| Permissions | Use migrations or deployment scripts to manage database user permissions deliberately. |

## Change tracking, saving, and concurrency

- Use a scoped `DbContext` lifetime for web apps; do not share one context across concurrent requests.
- Batch related changes and avoid excessive `SaveChanges()` calls inside loops.
- Use transactions when multiple operations must commit or roll back together.
- Configure optimistic concurrency with rowversion/timestamp or concurrency tokens for multi-user updates.
- Choose tracking behavior intentionally: tracked for updates, no-tracking for read models, identity resolution when required.

## Security and raw SQL

| Risk | Safer EF Core practice |
| --- | --- |
| SQL injection | Prefer strongly typed LINQ; when raw SQL is necessary, use parameterized queries, not string concatenation. |
| Overexposure | Project to DTOs and enforce data access permissions before materialization. |
| Sensitive fields | Consider encryption or provider-level protection for sensitive information. |
| Raw SQL drift | Keep raw SQL localized, tested, and aligned with migrations. |
| Permission sprawl | Manage database principals and grants through controlled migrations or deployment automation. |

## Testing guidance

| Test type | Recommended provider | Use for | Caveat |
| --- | --- | --- | --- |
| Pure unit test | Mock `DbContext`/`DbSet` only when behavior is outside query translation. | Service branching around data access. | Mocks do not validate SQL translation. |
| Lightweight integration | SQLite in-memory or test database. | Relational constraints, query behavior, transactions. | SQLite differs from SQL Server/PostgreSQL for some functions and types. |
| Model regression | Snapshot or generated SQL inspection. | Detecting model or migration changes. | Review snapshots; do not approve blindly. |
| Migration test | Isolated environment. | Applying migrations and validating schema/data. | Never run destructive migration tests against shared production data. |

## Gotchas

- **The in-memory provider is not relational**: it can pass tests that fail against a real database; prefer SQLite or the production provider for integration behavior.
- **`Include()` is not a performance fix by itself**: it can trade N+1 queries for huge joined result sets; consider projection.
- **`IQueryable` leaks boundaries**: returning it from repositories or APIs lets callers change execution, filters, and performance outside the owner.
- **Raw SQL still needs parameters**: EF Core helpers can parameterize values, but string interpolation into SQL text can remain unsafe if misused.

## Output template

```markdown
## EF Core review — <context, entity, query, or migration>

**Status:** pass | improvements recommended | fix required | blocked
**Scope:** `<files or code areas reviewed>`

| Area | Finding | Severity | Recommendation |
| --- | --- | --- | --- |
| Querying | <issue or strength> | High | <specific EF Core change> |
| Migrations | <issue or strength> | Medium | <specific migration action> |

### Validation
- Build/tests/migration SQL reviewed: <command or not run>
- Remaining risk: <none or explicit gap>
```

## Quality gate

- [ ] `DbContext` lifetime, configuration, and `OnModelCreating` mapping were considered.
- [ ] Entity keys, relationships, navigations, constraints, and owned entity types were checked when relevant.
- [ ] Queries were reviewed for tracking behavior, projection, pagination, `Include()`, compiled queries, and N+1 risk.
- [ ] Migrations were assessed for size, naming, SQL review, deployment safety, and seeding.
- [ ] Raw SQL, permissions, and sensitive data handling were checked for security issues.
- [ ] Testing advice distinguishes in-memory provider limitations from relational integration tests.

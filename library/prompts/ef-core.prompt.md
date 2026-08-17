---
name: 'ef-core'
description: 'Apply Entity Framework Core best practices to data access code and project configuration.'
agent: 'agent'
tools: ['changes', 'codebase', 'editFiles', 'problems', 'runCommands']
---

# /ef-core

## Objective

Review or improve Entity Framework Core data access code so DbContext design, entity modeling, querying, migrations, change tracking, security, performance, and tests follow EF Core best practices without changing application semantics.

## When to Invoke

Use this prompt when creating, reviewing, or refactoring EF Core contexts, entities, repositories, LINQ queries, migrations, seeding, test contexts, or database access configuration.

## Preconditions

- The EF Core code, project configuration, migration, or query target is available.
- The database provider, application type, and expected DbContext lifetime are known or can be inferred safely.
- Changes to data access code or migrations are permitted for the requested target.
- Production-impacting migration SQL will be reviewed before application.

## Inputs the Team Must Provide

- `target` — the DbContext, entity, query, migration, repository, or project area to review or improve.
- Database provider and runtime context, such as web app, console app, tests, or background worker.
- Relevant schema, relationships, row counts, query behavior, migration constraints, and test expectations.
- Existing test command or migration verification process.
- Ask the user for anything that is missing, especially provider or production deployment constraints.

## What I Will Do

- Keep DbContext classes focused, cohesive, properly injected, and configured through OnModelCreating or separate `IEntityTypeConfiguration` classes.
- Model entities with meaningful keys, relationships, constraints, navigation properties, and owned entity types where appropriate.
- Improve query shape with `AsNoTracking()`, pagination, `Include()`, projection, compiled queries, and N+1 avoidance.
- Review migrations, seeding, migration bundles, SQL scripts, transactions, concurrency control, and DbContext lifetimes.
- Check parameterized queries, raw SQL risks, access permissions, sensitive data encryption, and testing strategy.

## What I Will NOT Do

- Apply production migrations, destructive schema changes, or permission changes without explicit approval.
- Recommend raw SQL when a strongly typed LINQ query is sufficient and safer.
- Hide N+1 problems with broad eager loading when projection or targeted includes are more appropriate.
- Use the EF Core in-memory provider as proof of relational behavior that requires SQLite or the production provider.
- Change domain semantics, relationship cardinality, or key strategy without calling out the trade-off.

## Output Format

Return or apply the EF Core changes with this structure:

```markdown
### EF Core Result

### Target
- `ApplicationDbContext`, `Order`, `OrderRepository`, or `<target>`

### Findings and Changes
| Area | Finding | Recommendation or Change |
| --- | --- | --- |
| Data Context Design | Model configuration is embedded in `DbContext` | Move rules to `IEntityTypeConfiguration<Order>` and call from `OnModelCreating` |
| Entity Design | Relationship cardinality is unclear | Define one-to-one, one-to-many, or many-to-many explicitly |
| Performance | Read query tracks entities unnecessarily | Add `AsNoTracking()` and project with `Select` |
| Migrations | Migration is broad and unnamed | Split into small, focused, descriptively named migrations |
| Querying | Query exposes `IQueryable` past the repository boundary | Materialize at the boundary or document composition rules |
| Change Tracking & Saving | Multiple `SaveChanges()` calls are row-by-row | Batch changes and use transactions for multi-step operations |
| Security | Raw SQL accepts interpolated input | Use parameterized queries and verify permissions |
| Testing | Provider hides relational behavior | Use SQLite integration tests or isolated migration tests |

### Validation
- Command: `<dotnet test, migration script, or not run>`
- Result: `<passed, failed, or not run with reason>`
```

## Definition of Done

- [ ] DbContext, entity configuration, and relationships are explicit and cohesive.
- [ ] Queries avoid unnecessary tracking, over-fetching, N+1 access, and unbounded result sets.
- [ ] Migration guidance is small, descriptive, reviewable, and production-safe.
- [ ] Raw SQL and sensitive data handling are secure and parameterized.
- [ ] Tests use the provider strategy appropriate to the behavior under test.
- [ ] Validation evidence or a precise not-run reason is reported.

## Prompt Body

Follow these steps in order. Preserve application behavior unless a requested change explicitly alters it.

**Step 1 — Identify the EF Core boundary.** Locate the target DbContext, entity, repository, migration, or query. Determine the provider, application type, and appropriate DbContext lifetime, such as scoped for web apps or `DbContextFactory` for console apps or tests.

**Step 2 — Review Data Context Design.** Keep DbContext classes focused and cohesive. Use constructor injection for configuration options. Override `OnModelCreating` for fluent API configuration, and separate larger rules into `IEntityTypeConfiguration` classes.

**Step 3 — Review Entity Design.** Use meaningful primary keys and call out natural vs surrogate key trade-offs. Implement one-to-one, one-to-many, and many-to-many relationships explicitly. Use data annotations or fluent API for constraints and validations. Keep navigation properties appropriate and consider owned entity types for value objects.

**Step 4 — Optimize Performance.** Use `AsNoTracking()` for read-only queries. Implement pagination for large result sets with `Skip()` and `Take()`. Use `Include()` only when eager loading is needed. Prefer projection with `Select` to retrieve only required fields. Use compiled queries for frequently executed queries. Avoid N+1 query problems by including or projecting related data properly.

**Step 5 — Review Migrations.** Create small, focused migrations with descriptive names. Verify migration SQL scripts before production. Consider migration bundles for deployment. Add data seeding through migrations only when appropriate and deterministic.

**Step 6 — Review Querying.** Use `IQueryable` judiciously and understand when queries execute. Prefer strongly typed LINQ (strongly-typed LINQ) over raw SQL. Use operators such as `Where`, `OrderBy`, and `GroupBy` intentionally. Use database functions for complex operations when provider support is clear. Consider the specifications pattern for reusable queries.

**Step 7 — Review Change Tracking & Saving.** Choose appropriate change tracking strategies. Batch `SaveChanges()` calls. Implement concurrency control for multi-user scenarios. Use transactions for multiple operations that must commit together. Verify lifetimes so contexts are not shared unsafely.

**Step 8 — Review Security and Testing.** Avoid SQL injection with parameterized queries. Be careful with raw SQL queries, permissions, migrations that manage database users, and encryption for sensitive information. Use the in-memory database provider only for unit tests, SQLite for relational integration tests, mocked DbContext and DbSet only for pure unit tests, isolated environments for migrations, and snapshot testing for model changes when useful.

**Step 9 — Validate and report.** Run the smallest existing `dotnet test`, migration script generation, or provider-specific validation command that covers the change. Report findings, edits, risks, and validation output.

## Invocation Example

```
/ef-core target=src/Data/ApplicationDbContext.cs
```

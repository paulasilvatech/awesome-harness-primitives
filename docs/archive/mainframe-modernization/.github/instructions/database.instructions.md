---
description: "Use when writing database repositories, migrations, schema changes, SQL queries, indexes, and rollback-safe data changes."
applyTo: "backend/src/main/java/**/infrastructure/**,backend/src/main/resources/db/migration/**"
---

# Database Conventions — Flyway Migrations and Repositories

This file activates when you edit persistence code under `backend/src/main/java/**/infrastructure/**` or Flyway migrations under `backend/src/main/resources/db/migration/**`. It teaches migration hygiene, repository query safety, indexing, and rollback-safe schema change on PostgreSQL 16. Entity and FDT-to-JPA mapping belong to [`modular-monolith.instructions.md`](modular-monolith.instructions.md); reading the Adabas FDT that a schema derives from belongs to [`natural-adabas.instructions.md`](natural-adabas.instructions.md).

## Flyway Migrations

Migrations are versioned, forward-only, and immutable once merged. Name them `V<n>__<snake_case_description>.sql`. One logical change per file. All identifiers are `snake_case`.

```sql
-- V1__create_resource.sql
CREATE TABLE resource (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    label       VARCHAR(120) NOT NULL,
    amount      NUMERIC(15, 2) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX ux_resource_label ON resource (label);
```

> [!WARNING]
> Never edit a migration that has already run on any shared database — Flyway validates its checksum and will fail. Fix forward with a new `V<n+1>__` migration.

## Money and Precision

Monetary and packed-decimal fields map to `NUMERIC(precision, scale)` in PostgreSQL and `BigDecimal` in Java. Never use `float`, `double`, `real`, or `money`.

```sql
amount NUMERIC(15, 2) NOT NULL -- maps to BigDecimal with scale 2
```

## Repositories

Repositories are Spring Data interfaces. Use derived query methods or `@Query` with JPQL and **named parameters** — never string concatenation, which invites SQL injection.

```java
interface ResourceRepository extends JpaRepository<Resource, UUID> {

    Optional<Resource> findByLabel(String label);

    @Query("select r from Resource r where r.amount >= :floor")
    List<Resource> findAllAtOrAbove(@Param("floor") BigDecimal floor);
}
```

- No `@Transactional` in a repository — the service owns the transaction boundary.
- Return `Optional<T>` for single lookups; never `null`.
- For a native query, still bind parameters (`:name` / `?1`); never interpolate strings.

## Indexes and Constraints

Declare uniqueness, foreign keys, and indexes in the migration, not in application code. Index the columns your repositories filter and join on.

```sql
CREATE INDEX ix_payment_resource_id ON payment (resource_id);
ALTER TABLE payment
    ADD CONSTRAINT fk_payment_resource
    FOREIGN KEY (resource_id) REFERENCES resource (id);
```

## Rollback-Safe Change (Expand / Contract)

Never rename or drop a column in the same release that deploys the code using it. Split every breaking change across releases so a rollback stays safe.

| Phase | Migration | Release |
|---|---|---|
| Expand | Add the new nullable column or table | N |
| Backfill | Copy data in batches; dual-write from the app | N |
| Contract | Drop the old column/constraint once nothing reads it | N+1 |

The [`safe-migration`](../skills/safe-migration/SKILL.md) skill owns the full zero-downtime procedure and backfill checklist.

## Query Performance

Avoid N+1 selects: fetch associations with `@EntityGraph` or a JPQL `join fetch`, and verify a real plan with `EXPLAIN ANALYZE`. The [`query-optimization`](../skills/query-optimization/SKILL.md) skill owns index and plan analysis.

```java
@EntityGraph(attributePaths = "payments")
List<Resource> findByLabelStartingWith(String prefix);
```

## Conventions

| Rule | Rationale |
|---|---|
| `V<n>__snake_case.sql`, forward-only | Deterministic, checksum-validated history |
| `snake_case` tables and columns | Idiomatic PostgreSQL, stable across tools |
| `NUMERIC` for money, `BigDecimal` in Java | No binary floating-point rounding on currency |
| JPQL / derived queries with bound params | No SQL injection, portable across dialects |
| Indexes and FKs declared in migrations | Schema is reproducible from version control |
| Expand-contract for breaking changes | Every deploy is rollback-safe |

## Do / Do Not

| Do | Do not |
|---|---|
| Add a new `V<n+1>__` migration to fix schema | Edit an already-applied migration |
| Bind every parameter | Concatenate values into SQL/JPQL |
| Keep `@Transactional` in the service | Annotate repositories transactional |
| Backfill in batches, then contract | Drop-and-recreate a live table |

## Checklist Before Opening a PR

- [ ] Migration follows `V<n>__snake_case.sql` and changes one thing
- [ ] No previously applied migration was edited
- [ ] Money/packed fields are `NUMERIC(p, s)` mapped to `BigDecimal`
- [ ] Every query binds parameters; no string concatenation anywhere
- [ ] New filter/join columns are indexed; foreign keys declared
- [ ] Breaking changes use expand → backfill → contract across releases

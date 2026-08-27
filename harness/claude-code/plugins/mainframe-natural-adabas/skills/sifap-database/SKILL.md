---
name: sifap-database
description: >-
  Defines SIFAP PostgreSQL 16 and Flyway correctness for precision, schema evolution, MU/PE
  mapping, indexes, and rollback strategy. Use when editing persistence code or migrations.
paths:
  - backend/src/main/java/**/infrastructure/**
  - backend/src/main/resources/db/migration/**
  - "**/*.sql"
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/mainframe-natural-adabas/instructions/sifap-database.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# SIFAP database conventions - PostgreSQL and Flyway

These instructions apply to the PostgreSQL 16 workshop baseline and its persistence adapters. They are
authoritative for migration safety, numeric precision, index evidence, and Flyway behavior; approved data
ADRs and the actual target schema define domain ownership.

## Schema and migration safety

- Treat applied versioned migrations as immutable and fix forward with a new version.
- Use expand/backfill/contract for breaking or high-volume changes.
- Run `CREATE INDEX CONCURRENTLY` outside a transaction and configure the Flyway script accordingly.
- Use Flyway Undo only with the normal `U<version>__...` naming and a confirmed edition that supports it;
  otherwise use forward compatibility plus tested backup/restore.
- Do not call arbitrary DDL idempotent merely because it uses `IF NOT EXISTS`; verify the existing object.

## Mapping and queries

- Map packed and financial values to `NUMERIC`/`BigDecimal` with explicit precision and scale.
- Prefer relational child structures for stable or queryable MU and PE data. Use JSONB only with evidence
  and an approved ADR.
- Bind SQL/JPQL parameters and inspect real plans before adding performance indexes.
- Encode durable integrity in constraints where ownership and rollout permit it.

## Conventions

| Rule | Rationale |
| --- | --- |
| Applied migrations are immutable | Flyway history and shared environments stay reproducible. |
| Concurrent indexes disable script transactions | PostgreSQL rejects them inside transaction blocks. |
| Relational mapping is the structured-data default | Query and integrity semantics remain explicit. |
| Indexes require workload evidence | Unused indexes add write and maintenance cost. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Test migrations on representative disposable data | Claim a staging run that did not occur |
| Use resumable bounded backfills | Backfill a large table in one transaction |
| Compare decimal values exactly | Use binary floating point for financial values |
| Record JSONB trade-offs in an ADR | Use JSONB as an automatic MU/PE mapping |

## Checklist Before Opening a PR

- [ ] Migration order, transaction behavior, and applied-file immutability are correct.
- [ ] Breaking changes use an explicit expand/backfill/contract sequence.
- [ ] Precision, constraints, MU/PE mapping, and indexes have evidence and rationale.
- [ ] Queries bind parameters and performance claims cite an actual plan when available.
- [ ] Focused repository and migration tests pass or exact blockers are reported.
- [ ] Rollback and restore strategy matches the available Flyway edition and data semantics.

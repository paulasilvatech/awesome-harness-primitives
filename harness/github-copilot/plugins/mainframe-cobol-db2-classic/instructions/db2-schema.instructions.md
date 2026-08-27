---
applyTo: "**/*.ddl,**/*.sql,**/db2/**,**/dclgen/**"
description: "Applies DB2 DDL, DCLGEN, cursor, and migration-script conventions for precision, nullability, access paths, and reconciliation evidence. Use when reading or writing DB2 schema and migration artifacts."
---

# DB2 Schema and Migration Conventions

These conventions apply to DB2 DDL, DCLGEN output, and migration scripts matched by the `applyTo` globs. They are authoritative for how this repository states DB2 structure and proves migrated data. The installed DB2 catalog wins for actual definitions; record the divergence when a script and the catalog disagree.

## Evidence Before Schema

A target column definition cites the DB2 DDL, the DCLGEN structure, or the `PIC` clause it came from. A definition derived from sampled data is a hypothesis and must be labeled as one.

Nullability, defaults, and key constraints are behavior. `NOT NULL WITH DEFAULT` and a nullable column with an application-supplied default are different systems; map each explicitly.

## Conventions

| Rule | Rationale |
| --- | --- |
| Map `DECIMAL(p,s)` and `COMP-3` to exact decimal types end to end. | One pass through binary floating point breaks reconciliation. |
| State the fractional precision when mapping `TIMESTAMP`. | Source precision often exceeds the target default and rounds silently. |
| Keep the legacy key column alongside a new surrogate key. | Reconciliation needs the original identity until sign-off. |
| Justify every foreign key with DDL or cited program behavior. | A relationship enforced only in COBOL is a hypothesis. |
| Prove uniqueness against real data before adding a unique constraint. | A failing unique index on load means the assumption was wrong. |
| Add a constraint only when the legacy system rejects the value. | A new constraint turns a load into silent data loss. |
| Preserve the ordinal for every `OCCURS` group mapped to a child table. | Occurrence position drives reports and first-entry logic. |
| Record the cursor `ORDER BY`, or state that order is not guaranteed. | Legacy output can look ordered without an ordering clause. |
| Reproduce `SQLCODE +100` as an empty result, not an error. | Empty-result branches are business behavior. |

## Migration Script Safety

Migration scripts are re-runnable against an empty target and never mutate the legacy source. Credentials come from the environment or a managed identity, never from a script or a connection string in version control. A destructive step requires an explicit flag and a recorded approval.

## Reconciliation Evidence

A migration is reconciled when the numbers exist, not when the script succeeds. Record row counts, occurrence totals, per-column aggregates at full precision, null counts, distinct counts for key columns, and a deterministic sampled diff. Report every check that could not run, with the blocking reason.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Cite DDL, DCLGEN, or `PIC` for every mapped column. | Infer a type from a sample value. |
| Decide null, blank, and default meaning per column. | Apply one blanket null mapping to a table. |
| Store occurrence groups as child tables with ordinals. | Flatten `OCCURS` into numbered columns. |
| Report reconciliation with actual numbers. | Write "counts match" without values. |
| Use synthetic fixtures. | Copy production extracts into tests. |

## Checklist Before Opening a PR

- [ ] Every column mapping cites DDL, DCLGEN, or a `PIC` clause.
- [ ] Monetary and quantity columns use exact decimal types in every layer.
- [ ] Null, default, sign, and length decisions are explicit per column.
- [ ] Keys, unique constraints, and indexes cite the evidence that justifies them.
- [ ] Occurrence groups keep identity, order, and actual counts.
- [ ] Empty-result behavior matches the legacy `SQLCODE +100` paths.
- [ ] Reconciliation reports actual numbers, and unrun checks say so.
- [ ] Scripts are re-runnable, carry no credentials, and gate destructive steps.
- [ ] No production or regulated data appears in fixtures, logs, or examples.

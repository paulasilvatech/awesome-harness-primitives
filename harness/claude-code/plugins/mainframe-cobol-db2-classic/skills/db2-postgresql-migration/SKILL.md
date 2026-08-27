---
name: db2-postgresql-migration
description: >-
  Model DB2 for z/OS tables, DDL, DCLGEN structures, COBOL record layouts, OCCURS and REDEFINES
  groups, packed decimal fields, cursors, and VSAM datasets as a PostgreSQL schema, then prove
  equivalence with recorded reconciliation numbers. Use when designing or reviewing a DB2 to
  PostgreSQL migration, mapping legacy types to column types, deciding child-table versus array
  storage, or verifying that migrated data matches the legacy source.
---

<!-- Generated from harness/github-copilot/plugins/mainframe-cobol-db2-classic/skills/db2-postgresql-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# DB2 to PostgreSQL migration

Turn inspected DB2 and COBOL record structure into a relational schema that preserves precision, occurrence semantics, and access paths, and prove the result with reconciliation numbers instead of assertions.

## When to invoke

- "Map this DB2 DDL to a PostgreSQL schema."
- "How should this OCCURS DEPENDING ON group be stored?"
- "This COMP-3 amount is losing precision after migration."
- "Prove the migrated table matches the legacy DB2 table."
- "Review this DB2 to PostgreSQL mapping before implementation."

## Type mapping

| DB2 or COBOL source | PostgreSQL | Rule |
| --- | --- | --- |
| `CHAR(n)` | `char(n)` or `varchar(n)` | DB2 `CHAR` is blank-padded. Decide whether trailing blanks are significant before choosing. |
| `VARCHAR(n)` | `varchar(n)` or `text` | Confirm the declared maximum against real data before shortening it. |
| `GRAPHIC`, `VARGRAPHIC` | `text` | Confirm the source CCSID; do not assume UTF-8. |
| `DECIMAL(p,s)`, COBOL `COMP-3` | `numeric(p,s)` | Precision and scale come from the DDL or the `PIC` clause, never from a sample value. |
| `NUMERIC`, zoned `PIC 9` display | `numeric(p,s)` | Check sign handling: `SIGN LEADING`, `SIGN TRAILING`, and `SEPARATE` change the stored bytes. |
| `SMALLINT`, `INTEGER`, `BIGINT`, `COMP` | `smallint`, `integer`, `bigint` | Match the binary width; COBOL `COMP` width depends on the `PIC` digits and compiler options. |
| `REAL`, `DOUBLE`, `FLOAT` | `real`, `double precision` | Never use these for money, quantities, or anything summed and compared. |
| `DATE`, `TIME`, `TIMESTAMP` | `date`, `time`, `timestamp` | DB2 `TIMESTAMP` can carry more fractional digits than the target default; state the precision. |
| Date as `PIC 9(8)` | `date` | Confirm the stored pattern, usually `YYYYMMDD`, and reject impossible values instead of coercing them. |
| `ROWID`, `IDENTITY` | Surrogate key plus a retained legacy column | Never expose a physical identifier as business identity. |
| `BLOB`, `CLOB` | `bytea`, `text` | Confirm size limits and whether the value is ever compared or indexed. |

Monetary and quantity fields keep exact decimal types end to end: `numeric` in PostgreSQL, `BigDecimal`
in Java, and a string in JSON. A single conversion through a binary floating type is enough to break a
reconciliation.

## Structure mapping

| Legacy structure | Default PostgreSQL shape | Use an alternative only when |
| --- | --- | --- |
| DB2 table | Table | Never merge two tables into one without a recorded decision. |
| Column | Column | The column is a documented composite that programs always split. |
| `OCCURS` fixed group | Child table with `(parent_id, occurrence)` | Order and cardinality are bounded, values are never queried individually, and an array is a recorded decision. |
| `OCCURS DEPENDING ON` | Child table with `(parent_id, occurrence)` | Never. The controlling count is data and must survive the migration. |
| `REDEFINES` | One column per real interpretation, plus a discriminator | Never collapse to a single column; the active reading is decided by program logic. |
| Nested `OCCURS` | Grandchild table with both ordinals | Never. Both occurrence dimensions are meaningful. |
| Primary and unique index | Primary key and unique constraint | Uniqueness was never enforced in the legacy data. |
| Secondary index | Index on the mapped columns | The index is unused by every inspected program and query. |
| VSAM KSDS | Table with a unique key on the mapped record key | The dataset is a pure sequential extract with no key semantics. |
| Sequential dataset | Staging table or file-backed load | The data is transient and never queried. |

Store the occurrence ordinal explicitly. Occurrence position is often load-bearing in reports, control
breaks, and "first entry wins" logic.

## Identity, integrity, and access paths

- A DB2 foreign key is declarative evidence; a relationship enforced only in COBOL is a hypothesis. Cite
  the program and line that establishes it.
- `WITH DEFAULT` and `NOT NULL WITH DEFAULT` change what an absent value means. Map each column explicitly.
- A cursor with `FOR UPDATE` implies locking behavior; a cursor without `ORDER BY` has no guaranteed order
  even when the legacy report appears sorted.
- `SQLCODE +100` is a normal empty result. The migrated query must produce the same empty-result behavior,
  not an error.
- Add a constraint only when the legacy behavior actually rejects the value. A constraint the legacy system
  never enforced turns a load into a silent data-loss event.

## Semantic traps

- **Null is not blank and not zero.** DB2 nullable columns, COBOL blank fields, and low-values are three
  distinct states. Decide the mapping per column and record it.
- **Blank padding.** `CHAR` comparisons include trailing blanks. Moving to `varchar` changes equality results.
- **Sign representation.** Zoned and packed values carry the sign in the last nibble or byte. A wrong read
  silently flips a sign on a subset of rows.
- **Shortened values on load.** Widening a column hides a legacy length rule that programs relied on.
  Preserve the rule explicitly or record it as an accepted deviation.
- **Variable-length records.** An `OCCURS DEPENDING ON` record read with the maximum length reads past the
  real data. Migrate the actual count, not the maximum.
- **Low-values and high-values.** These sentinels often mean "unset" or "end marker"; mapping them to a
  literal byte string changes comparisons.
- **Denormalized redundancy.** A value duplicated across tables is often intentionally stale. Normalizing
  it changes reported history.

## Reconciliation procedure

Equivalence is a measurement, not a claim. Run these against the same input and record actual numbers.

1. **Row counts.** Legacy row count per table or dataset versus target row count per table.
2. **Occurrence counts.** Total `OCCURS` entries versus child-table row counts.
3. **Aggregates per numeric column.** `count`, `count` of non-null, `sum`, `min`, and `max`, compared at
   full precision.
4. **Null and default distribution.** Null counts per nullable column, compared with the legacy state.
5. **Distribution checks.** Distinct-value counts for every indexed or key column.
6. **Sampled record diff.** Deterministic ordering, a fixed sample, and a field-by-field comparison
   including trailing blanks and occurrence order.
7. **Edge-case set.** Maximum and zero occurrences, negative and zero amounts, boundary precision, nulls,
   low-values, and the longest character values.

Report every number that was produced and every check that could not run. A reconciliation reported
without numbers is not evidence.

## Safety

- Fixtures and examples use synthetic data. Never copy production records, personal identifiers, or real
  monetary values into the repository, tests, logs, or issue text.
- Migration scripts are re-runnable against an empty target and never mutate the legacy source.
- Credentials come from the environment or a managed identity, never from a script, migration file, or
  connection string in version control.
- A destructive load step requires an explicit flag and a recorded approval.

## Limits

- This skill maps structure and proves data equivalence. It does not extract business meaning; use a
  business-rule extraction capability for that.
- It does not tune the resulting schema; use a PostgreSQL optimization capability after the mapping is correct.
- It does not decide scope, priority, or which tables migrate first.
- Reconciliation proves that data matches. It does not prove that behavior matches; that needs
  characterization tests against the legacy outputs.

## Output template

```markdown
## DB2 to PostgreSQL mapping

**Status:** proposed | reviewed | reconciled | blocked
**Scope:** <DB2 table, copybook, or dataset>

### Column mapping
| Source field | Type | Target column | Type | Rule or risk | Evidence |
| --- | --- | --- | --- | --- | --- |

### Structure mapping
| Structure | Target shape | Rationale | Evidence |
| --- | --- | --- | --- |

### Access paths
| Index or cursor | Target index | Uniqueness proven | Evidence |
| --- | --- | --- | --- |

### Reconciliation
| Check | Legacy value | Target value | Match | Evidence |
| --- | --- | --- | --- | --- |

### Open questions and accepted deviations
- <question or deviation, owner, decision reference>
```

## Quality gate

- [ ] Every mapped field cites the DDL, DCLGEN, or `PIC` clause rather than a sampled value.
- [ ] Monetary and quantity fields use exact decimal types across every layer.
- [ ] `OCCURS`, `OCCURS DEPENDING ON`, and `REDEFINES` structures preserve occurrence identity, order, and count.
- [ ] Indexes and cursors map to access paths that match the inspected queries.
- [ ] Every foreign key and unique constraint cites the DDL, program behavior, or data proof that justifies it.
- [ ] Null, blank, default, sign, and length decisions are explicit per column.
- [ ] Empty-result behavior matches the legacy `SQLCODE +100` paths.
- [ ] Reconciliation reports actual counts, aggregates, occurrence totals, null counts, and sampled diffs.
- [ ] Checks that could not run are reported as not run, with the blocking reason.
- [ ] No production, personal, or real monetary data entered fixtures, examples, or logs.

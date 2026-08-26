---
name: adabas-postgresql-migration
description: >-
  Model Adabas files, DDM and FDT definitions, MU and PE structures, packed and unpacked numerics, descriptors, and ISN identity as a PostgreSQL schema, then prove equivalence with recorded reconciliation numbers. Use when designing or reviewing an Adabas to PostgreSQL data migration, mapping legacy field formats to column types, deciding child-table versus array storage, or verifying that migrated data matches the legacy source.
---

# Adabas to PostgreSQL migration

Turn inspected Adabas structure into a relational schema that preserves precision, occurrence semantics, and access paths, and prove the result with reconciliation numbers instead of assertions.

## When to invoke

- "Map this Adabas DDM to a PostgreSQL schema."
- "How should this MU field and PE group be stored?"
- "This packed decimal amount is losing precision after migration."
- "Prove the migrated table matches the legacy file."
- "Review this Adabas to PostgreSQL mapping before implementation."

## Field format mapping

| Adabas format | PostgreSQL | Rule |
| --- | --- | --- |
| `A` alphanumeric, fixed | `char(n)` or `varchar(n)` | Decide whether trailing blanks are significant before choosing. Legacy comparisons often depend on them. |
| `W` wide | `text` | Confirm the source encoding; do not assume UTF-8. |
| `P` packed decimal | `numeric(p,s)` | Precision and scale come from the DDM or FDT, never from a sample value. |
| `U` unpacked, zoned | `numeric(p,s)` | Same rule as `P`. Check the sign representation in the trailing byte. |
| `B` binary | `bytea`, `integer`, or `bigint` | Choose an integer type only when the field is a documented number, not a bit field. |
| `F` floating | `real` or `double precision` | Never use it for money, quantities, or anything that is summed and compared. |
| `L` logical | `boolean` | Map the legacy true value explicitly; blank is not automatically false. |
| Date as `N8` or `A8` | `date` | Confirm the stored pattern, usually `YYYYMMDD`, and reject impossible values instead of coercing them. |
| Time as numeric | `time` or `timestamp` | State the time zone assumption, or store local time with a documented rule. |
| Natural `D` and `T` | `date`, `timestamp` | Natural date arithmetic uses a day origin; verify the epoch before converting. |

Monetary and quantity fields keep exact decimal types end to end: `numeric` in PostgreSQL, `BigDecimal`
in Java, and a string in JSON. A single conversion through a binary floating type is enough to break a
reconciliation.

## Structure mapping

| Adabas structure | Default PostgreSQL shape | Use an alternative only when |
| --- | --- | --- |
| File | Table | Never merge two files into one table without a recorded decision. |
| Elementary field | Column | The field is a documented composite that programs always split. |
| MU multiple-value field | Child table with `(parent_id, occurrence)` | Order and cardinality are bounded, values are never queried or joined individually, and an array is a recorded decision. |
| PE periodic group | Child table with `(parent_id, occurrence)` plus one column per group member | Never flatten a PE into numbered columns; occurrence count is data, not schema. |
| MU inside PE | Grandchild table with both ordinals | Never. Both occurrence dimensions are meaningful. |
| Descriptor | Index on the mapped column | The descriptor is unused by every inspected program. |
| Superdescriptor | Composite index, or an index on a generated column when the source concatenates or shortens parts | The parts are already covered by an equivalent composite index. |
| Subdescriptor | Expression index on the same substring | The substring is not an access path in any inspected program. |
| ISN | Surrogate key plus a retained `legacy_isn` column | Never expose ISN as business identity; it is a physical address. |

Store the occurrence ordinal explicitly. Adabas occurrence position is often load-bearing in reports,
control breaks, and "first occurrence wins" logic.

## Identity and integrity

- Adabas enforces no referential integrity. A foreign key is a hypothesis derived from observed program
  behavior, not from a descriptor name. Cite the program and line that establishes the relationship.
- A descriptor is an access path. Uniqueness must be proven against the data before a unique constraint
  is added; a unique index that fails on load is evidence the assumption was wrong.
- Keep `legacy_isn` and the legacy file identity for the life of the reconciliation, then decide
  explicitly whether to retain or drop them.
- Add a constraint only when the legacy behavior actually rejects the value. A constraint the legacy
  system never enforced turns a load into a silent data-loss event.

## Semantic traps

- **Empty is not null.** Adabas suppresses empty values, and a null-indicator value is distinct from a
  blank or zero. Decide the mapping per field and record it; a blanket `NULL` mapping changes behavior.
- **Zero occurrences.** An MU or PE with no occurrences is not the same as one occurrence holding a
  default. Absence must survive the migration.
- **Sign handling.** Packed and unpacked values carry the sign in the last nibble or byte. A wrong read
  silently flips a sign on a subset of rows.
- **Shortened values on load.** Widening a column hides a legacy length rule that programs relied on.
  Preserve the rule explicitly or record it as an accepted deviation.
- **Character comparison.** Legacy comparisons on fixed-length fields include trailing blanks. Moving to
  `varchar` changes equality results.
- **Denormalized redundancy.** A value duplicated across files is often intentionally stale. Normalizing
  it changes reported history.

## Reconciliation procedure

Equivalence is a measurement, not a claim. Run these against the same input and record actual numbers.

1. **Row counts.** Legacy record count per file versus target row count per table.
2. **Occurrence counts.** Total MU values and PE occurrences versus child-table row counts.
3. **Aggregates per numeric column.** `count`, `count` of non-null, `sum`, `min`, and `max`, compared at
   full precision.
4. **Distribution checks.** Distinct-value counts for every mapped descriptor column.
5. **Sampled record diff.** Deterministic ordering, a fixed sample, and a field-by-field comparison
   including trailing blanks and occurrence order.
6. **Edge-case set.** Maximum occurrences, zero occurrences, negative and zero amounts, boundary
   precision, suppressed empty values, and the longest alphanumeric values.

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
- It does not tune the resulting schema; use a PostgreSQL optimization capability after the mapping is
  correct.
- It does not decide scope, priority, or which files migrate first.
- Reconciliation proves that data matches. It does not prove that behavior matches; that needs
  characterization tests against the legacy outputs.

## Output template

```markdown
## Adabas to PostgreSQL mapping

**Status:** proposed | reviewed | reconciled | blocked
**Scope:** <Adabas file or DDM>

### Column mapping
| Adabas field | Format | Target column | Type | Rule or risk | Evidence |
| --- | --- | --- | --- | --- | --- |

### Structure mapping
| Structure | Target shape | Rationale | Evidence |
| --- | --- | --- | --- |

### Access paths
| Descriptor | Target index | Uniqueness proven | Evidence |
| --- | --- | --- | --- |

### Reconciliation
| Check | Legacy value | Target value | Match | Evidence |
| --- | --- | --- | --- | --- |

### Open questions and accepted deviations
- <question or deviation, owner, decision reference>
```

## Quality gate

- [ ] Every mapped field cites the DDM or FDT definition rather than a sampled value.
- [ ] Monetary and quantity fields use exact decimal types across every layer.
- [ ] MU and PE structures preserve occurrence identity, order, and zero-occurrence cases.
- [ ] Descriptors, superdescriptors, and subdescriptors map to indexes that match the inspected access paths.
- [ ] Every foreign key and unique constraint cites the program behavior or data proof that justifies it.
- [ ] Empty, null, blank, sign, and length decisions are explicit per field.
- [ ] Reconciliation reports actual counts, aggregates, occurrence totals, and sampled diffs.
- [ ] Checks that could not run are reported as not run, with the blocking reason.
- [ ] No production, personal, or real monetary data entered fixtures, examples, or logs.

---
name: reviewing-oracle-to-postgres-migration
description: >-
  Review Oracle-to-PostgreSQL migration plans or completed artifacts for behavioral risks: empty
  strings, exceptions, refcursors, type coercion, sorting and collations, UNION ALL planner
  changes, materialized-view refresh, timestamps, sequences, ROWNUM, NVL/DECODE, and concurrent
  transactions. Use when planning or validating database migrations and integration tests.
---

<!-- Generated from harness/github-copilot/plugins/oracle-to-postgres-migration-expert/skills/reviewing-oracle-to-postgres-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Oracle-to-PostgreSQL migration review

Cross-reference migration scope against the bundled Oracle/PostgreSQL behavior references, identify risks by cross-referencing before implementation, and validate post-migration work against integration-test evidence.

## When to invoke

- "Review this Oracle to PostgreSQL migration plan."
- "Validate that our migrated procedure preserves Oracle behavior."
- "Which Oracle/Postgres differences apply to this query?"
- "Check integration tests for Oracle-to-PostgreSQL edge cases."
- "Assess refcursor, timestamp, or UNION ALL migration risk."

## Procedure

1. Classify the task as planning or validation.
2. Identify the migration scope: procedures, triggers, queries, views, materialized views, and application callers.
3. Read `references/REFERENCE.md` as the index, then open only the reference files whose behavior appears in scope.
4. Map each applicable insight to a concrete risk, required code change, and required integration test.
5. For validation, verify migrated artifacts, scripts, and tests prove the new PostgreSQL semantics.
6. Gate the result with a risk table and an explicit pass/fix verdict.

## Risk assessment workflow

| Step | Action | Evidence to capture |
| --- | --- | --- |
| Identify scope | List affected database objects and caller code. | Object names, SQL files, application classes, refcursor clients. |
| Screen insights | Compare the scope to every entry in `references/REFERENCE.md`. | Applicable reference filenames and skipped references with reason. |
| Decide semantics | Flag behavior choices such as Oracle empty-string-as-NULL versus native PostgreSQL empty string behavior. | Decision owner or default recommendation. |
| Recommend fixes | Apply patterns from the specific reference file. | Query rewrite, function rewrite, test requirement, or design decision. |

## Validation workflow

| Step | Action | Gate |
| --- | --- | --- |
| Map artifact | Summarize the migrated object and change set. | Every changed procedure, trigger, query, view, or caller is named. |
| Cross-check insights | Confirm each applicable reference behavior is acknowledged and addressed. | No applicable insight is left as "not reviewed". |
| Verify tests | Confirm happy paths and failure paths exercise PostgreSQL behavior. | Integration tests cover exceptions, sorting, `UNION ALL`, refcursor consumption, concurrent transactions, timestamps, and materialized-view freshness when applicable. |
| Gate result | Report pass, conditional pass, or fix required. | Migration scripts run and tests pass, or blockers are explicit. |

## Behavior risk catalog

| Risk area | Look for | Bundled reference |
| --- | --- | --- |
| Empty strings | Oracle treats `''` like `NULL`; PostgreSQL does not. | `references/empty-strings-handling.md` |
| No data exceptions | Oracle `NO_DATA_FOUND` exception flow may become empty result handling. | `references/no-data-found-exceptions.md` |
| `NVL` and `DECODE` | Oracle-specific functions need PostgreSQL-safe equivalents. | `references/oracle-nvl-decode-functions.md` |
| Parenthesized `FROM` | Oracle join syntax and parentheses can change semantics. | `references/oracle-parentheses-from-clause.md` |
| Pagination | `ROWNUM` patterns need PostgreSQL pagination or window functions. | `references/oracle-rownum-pagination.md` |
| Sequences and `DUAL` | `SYSDATE`, sequences, and `DUAL` need PostgreSQL replacements. | `references/oracle-sysdate-sequences-dual.md` |
| Sorting and collations | NULL ordering, sorting/collations, collation, and case behavior may differ. | `references/oracle-to-postgres-sorting.md` |
| Timestamps | Time zone and precision semantics may change. | `references/oracle-to-postgres-timestamp-timezone.md` |
| Numeric formatting | `TO_CHAR` numeric output can differ. | `references/oracle-to-postgres-to-char-numeric.md` |
| Type coercion | Implicit casts accepted by Oracle may fail or change plans in PostgreSQL. | `references/oracle-to-postgres-type-coercion.md` |
| Concurrent transactions | Locking and isolation behavior may differ. | `references/postgres-concurrent-transactions.md` |
| Materialized views | Refresh requirements and freshness expectations must be explicit. | `references/postgres-materialized-view-refresh.md` |
| Refcursors | Application consumption and transaction scope must match PostgreSQL behavior. | `references/postgres-refcursor-handling.md` |
| `UNION ALL` planner | PostgreSQL planner choices may change behavior/performance or ordering assumptions. | `references/postgres-union-all-planner.md` |

## Progressive disclosure and bundled resources

- `references/REFERENCE.md`: index of all migration insights; read this first from the `references/` bundle.
- `references/*.md`: detailed behavior-specific guidance; read only the files that match the migration scope.

## Gotchas

- **Do not treat syntax conversion as semantic equivalence**: the migration can compile and still mishandle empty strings, timestamps, or exceptions.
- **Do not skip caller code**: refcursor handling, transaction boundaries, and materialized-view freshness often fail in application code, not only SQL.
- **Do not rely on unit tests alone**: database migration risks require integration tests against PostgreSQL behavior.

## Output template

```markdown
## Oracle-to-PostgreSQL migration review

**Status:** pass | conditional pass | fix required
**Mode:** planning | validation
**Scope:** <objects, queries, views, and callers reviewed>

| Insight | Applies? | Risk | Required action | Test evidence |
| --- | --- | --- | --- | --- |
| `references/<file>.md` | yes/no | <behavior difference> | <rewrite, design decision, or none> | <test name/result or missing> |

### Migration gate
- Scripts run: pass | fail | not checked
- Integration tests: pass | fail | missing
- Blocking decisions: <none or list>
```

## Quality gate

- [ ] `references/REFERENCE.md` was used as the index before opening detailed references.
- [ ] Every affected procedure, trigger, query, view, materialized view, and caller is listed or explicitly out of scope.
- [ ] Applicable differences include empty strings, exceptions, sorting, `UNION ALL`, refcursors, concurrent transactions, timestamps, and materialized-view refresh where relevant.
- [ ] Planning output includes risks and recommended actions; validation output includes test evidence.
- [ ] Integration tests cover both happy path and failure scenarios for every applicable behavior difference.
- [ ] The final verdict is pass, conditional pass, or fix required.

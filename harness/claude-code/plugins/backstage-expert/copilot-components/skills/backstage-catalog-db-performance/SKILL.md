---
name: backstage-catalog-db-performance
description: "Run and compare the Backstage catalog query performance battery against a safe database replica, capture PostgreSQL plans and buffers, detect regressions, and update the baseline. Use when changing catalog queries, indexes, schemas, or database performance behavior."
license: Apache-2.0
metadata:
  source-repository: "https://github.com/backstage/backstage"
  source-commit: "eeac444a9aba7c107525d2a726851e907418c181"
---

# Backstage catalog database performance

Use the pinned upstream procedure as detailed reference while protecting credentials and
production databases.

## When to invoke

- "Run the catalog query performance battery."
- "Compare catalog query plans to the baseline."
- "Check whether this catalog index change regressed performance."
- "Update the catalog database performance baseline."

## Procedure

1. Confirm Backstage core or close-fork mode and locate the catalog query battery and baseline.
2. Read [the pinned upstream procedure](references/upstream/catalog-db-performance.md).
3. Require a database replica or disposable test database. Do not run the battery against
   production.
4. Obtain connection details through environment configuration without writing or echoing them.
5. Establish catalog size and baseline comparability.
6. Run every documented scenario with its timeout, plan, timing, buffer, and anti-pattern capture.
7. Compare proportional timing and plan-shape changes to the previous baseline.
8. Update the baseline in its existing format only when the complete battery finished.
9. Report improvements, regressions, environment differences, and inconclusive scenarios.

## Output template

```markdown
## Catalog database performance result

**Database:** replica | disposable
**Baseline:** <path and date>

| Scenario | Plan change | Timing change | Buffers | Result |
| --- | --- | --- | --- | --- |

### Regressions
- <scenario, evidence, and recommendation>
```

## Quality gate

- [ ] The database is a replica or disposable test environment.
- [ ] Credentials were neither stored nor printed.
- [ ] Every scenario used the documented timeout and captured a plan.
- [ ] Catalog size differences are included in interpretation.
- [ ] The baseline changed only after a complete run.
- [ ] Regressions distinguish timing noise from plan-shape and index changes.

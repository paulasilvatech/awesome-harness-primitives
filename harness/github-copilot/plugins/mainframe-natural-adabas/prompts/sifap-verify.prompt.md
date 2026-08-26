---
name: 'sifap-verify'
description: 'Prove behavior and data equivalence for one implemented SIFAP slice with requirement coverage, migration mapping review, and recorded reconciliation numbers.'
argument-hint: 'scope=<implemented-slice> destination=response|<report-file>'
agent: 'sifap-quality'
---

# /sifap-verify

## Objective

Decide the SIFAP quality gate for one implemented slice using executed checks and recorded numbers, and
route every difference to the phase that owns its root cause.

## When to Invoke

Use during the quality stage after the implementation gate closed with build and test evidence.

## Preconditions

- The implemented slice, approved requirements, and legacy evidence are available.
- The DDM or FDT definitions for every in-scope Adabas file are readable.
- The response or exact report-file destination is approved.
- Test, database, and reconciliation commands exist or the blocker is known.

Stop if the slice scope, the requirement set, or the destination is ambiguous.

## Inputs the Team Must Provide

- `scope` - implemented slice, branch, or diff with its `REQ-NNN` set.
- `destination` - Chat response or exact report artifact path.
- Reconciliation input dataset and the commands that run it, or the reason none exist.

## What I Will Do

- Load SIFAP context, the loop skill, traceability, characterization testing, and Adabas-to-PostgreSQL migration Skills.
- Check that every in-scope requirement has a discriminating test tied to its `REQ-NNN`.
- Review the migration mapping for precision, occurrence semantics, identity, and access paths.
- Run the reconciliation checks and record the actual counts, aggregates, and sampled differences.
- Classify each difference as defect, accepted deviation, or environment failure, and name its owning phase.
- State the gate verdict and the criterion that decided it.

## What I Will NOT Do

- Report a reconciliation as matching without the recorded numbers.
- Substitute line coverage for requirement verification.
- Write a test from the implementation instead of from the legacy oracle.
- Repair a requirement defect inside a test or fixture.
- Copy production, personal, or real monetary data into fixtures, logs, or the report.
- Edit production code under review, legacy source, or approved requirements.

## Output Format

```markdown
## SIFAP verification report

**Status:** gate-passed | gate-failed | blocked
**Slice:** <implemented slice>

### Requirement verification
| REQ-ID | Test oracle | Result | Evidence |
| --- | --- | --- | --- |

### Data migration review
| Structure or field | Target shape | Finding | Evidence |
| --- | --- | --- | --- |

### Reconciliation
| Check | Legacy value | Target value | Match | Evidence |
| --- | --- | --- | --- | --- |

### Routed findings
| Finding | Class | Owning phase | Owner |
| --- | --- | --- | --- |
```

## Definition of Done

- [ ] Required SIFAP, loop, traceability, characterization, and migration Skills were loaded.
- [ ] Every in-scope requirement is verified or reported as uncovered.
- [ ] Every in-scope legacy file has a reviewed mapping or an explicit exclusion.
- [ ] Reconciliation numbers are recorded, and checks that did not run say so with the blocker.
- [ ] Differences are classified and routed rather than patched locally.
- [ ] Fixtures are synthetic and sensitive values are absent from the report.
- [ ] The verdict names the criterion that decided the gate.

## Prompt Body

1. **Validate scope and destination.** Stop if the slice, the requirement set, or the destination is ambiguous.
2. **Load context.** Load SIFAP context, the loop skill, and the verification and migration Skills.
3. **Check coverage.** Map every in-scope `REQ-NNN` to a discriminating test or mark it uncovered.
4. **Review the mapping.** Inspect DDM and FDT definitions against the target schema.
5. **Run reconciliation.** Execute the checks and record actual values, or report the exact blocker.
6. **Classify and route.** Assign each difference a class and an owning phase.
7. **Deliver.** Return Chat output or write only the exact approved report artifact.

## Invocation Example

```text
/sifap-verify scope=impl/001-payment-inspection destination=04-quality/reports/001-payment-inspection.md
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `sifap-quality` | agent | Owns the quality-gate verdict and routing decisions. |
| `adabas-postgresql-migration` | skill | Supplies the mapping rules and reconciliation procedure. |
| `sifap-loop` | skill | Evaluates the quality gate and records the iteration ledger. |

---
name: legacy-characterization-testing
description: >-
  Design and implement characterization, differential, golden-master, and behavior-equivalence tests that pin observable legacy behavior before modernization. Use when a legacy slice needs a trustworthy behavior oracle, regression baseline, or intentional-change record.
---

# Legacy characterization testing

Build the smallest reliable behavior oracle for a bounded legacy slice before changing its
implementation.

## When to invoke

- "Add characterization tests before rewriting this module."
- "Compare the legacy and modern implementations."
- "Create a golden-master test for this batch output."
- "Pin this undocumented behavior before refactoring."

## Oracle selection

| Oracle | Use when | Main risk |
| --- | --- | --- |
| Direct assertion | Inputs and outputs are deterministic and understood. | Missing hidden side effects. |
| Differential test | Legacy and candidate implementations can run on the same sanitized cases. | Shared defects appear equivalent. |
| Golden master | Output is large but stable and reviewable. | Snapshot noise hides meaningful drift. |
| State transition | Database or workflow state is the observable contract. | Uncontrolled fixtures or ordering. |
| Approval test | A human must approve a complex report or document baseline. | Approval without source evidence. |

## Procedure

1. Bound one behavior slice and identify its approved rule or source evidence.
2. List observable inputs, outputs, mutations, errors, ordering, precision, and side effects.
3. Choose the simplest oracle that can fail on a real behavioral regression.
4. Build deterministic, synthetic, and privacy-safe fixtures, including boundaries and negative paths.
5. Capture the legacy result before implementing or changing the target behavior.
6. Review and store the baseline with source evidence, normalization rules, and intentional omissions.
7. Run the same cases against the modern implementation and classify every difference as defect,
   intentional change, environmental noise, or unresolved.
8. Keep the focused tests in the target repository's existing framework and run the narrowest relevant
   suite plus the next broader suite when available.

## Determinism and privacy

- Freeze or inject time, randomness, locale, ordering, identifiers, and external responses.
- Normalize only non-semantic noise; document each normalization so it cannot hide business drift.
- Never copy production personal or financial data into fixtures. Generate representative synthetic data.
- Compare financial values with exact decimal semantics and explicit scale or rounding rules.
- Record environment dependencies when the legacy runtime cannot be reproduced locally.

## Intentional changes

Do not update a baseline merely to make tests pass. An intentional behavior change needs an approved
requirement or decision, the before/after outcome, rationale, affected tests, migration impact, and
rollback consideration.

## Limits

- Characterization proves observed behavior for tested cases; it does not prove the legacy behavior is
  desirable or complete.
- Use product-specific requirements to decide which behavior must remain.
- Use a security review before preserving behavior that exposes data or bypasses authorization.

## Output template

```markdown
## Characterization test result

**Status:** baseline-created | equivalent | drift-found | blocked
**Slice:** <bounded behavior>

### Oracle
- Type: <direct | differential | golden-master | state | approval>
- Source evidence: <paths and rule IDs>
- Normalization: <rules or none>

### Cases
| Case | Input class | Legacy outcome | Modern outcome | Classification |
| --- | --- | --- | --- | --- |

### Validation
- Legacy command: <command/result or blocker>
- Targeted tests: <command/result>
- Broader tests: <command/result or not run>
```

## Quality gate

- [ ] The test scope is one bounded behavior slice with source or requirement evidence.
- [ ] The oracle covers observable output, mutation, errors, precision, and ordering as applicable.
- [ ] Fixtures are deterministic, synthetic, and free of production-sensitive data.
- [ ] The legacy result was captured before target implementation changed.
- [ ] Every difference is classified and intentional changes have approval evidence.
- [ ] Targeted and broader validation ran, or exact blockers are reported.

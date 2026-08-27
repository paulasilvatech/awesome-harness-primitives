---
name: 'cobol-classic-build-slice'
description: 'Implement one approved COBOL/DB2 slice with behavior-pinning tests, recorded decisions, traceable validation, and explicit drift classification.'
argument-hint: 'slice=<NNN-slug> requirements=REQ-NNN[,REQ-NNN]'
agent: 'cobol-classic-builder'
---

# /cobol-classic-build-slice

## Objective

Implement one bounded slice so that approved behavior is preserved and every difference is classified.

## When to Invoke

Use during the implementation stage after the architecture gate closed for the slice.

## Preconditions

- Approved `REQ-NNN` requirements and decision records exist for the slice.
- The writable implementation and test paths are approved.
- Build and test commands exist in the target repository, or the blocker is known.
- The `cobol-classic-context` and `legacy-characterization-testing` skills are available.

Stop if the slice scope, the requirement set, or the writable paths are ambiguous.

## Inputs the Team Must Provide

- `slice` - the bounded slice identifier.
- `requirements` - the approved `REQ-NNN` set in scope.
- The legacy behavior oracle, or the reason none can be captured.

## What I Will Do

- Load the required Skills and verify scope, requirements, and decisions.
- Capture or reproduce the legacy behavior oracle for the slice.
- Add the smallest behavior-pinning test that can falsify the implementation.
- Implement the approved behavior using nearby conventions and the recorded decisions.
- Run targeted tests and the next relevant suite, then classify drift.

## What I Will NOT Do

- Translate COBOL structure line by line into the target language.
- Implement a requirement outside the declared slice.
- Use binary floating point for money or quantities.
- Drop an empty-result or error branch that the legacy system has.
- Finish with failing stubs, invented interfaces, or unrun checks reported as passing.
- Modify legacy source, requirements, or decision records.

## Output Format

```markdown
## COBOL/DB2 build result

**Status:** implemented | drift-found | blocked
**Slice:** <slice>

### Changes
- <path and behavior>

### Traceability and equivalence
| REQ-ID | Source evidence | Test oracle | Result |
| --- | --- | --- | --- |

### Validation
| Command | Result | Notes |
| --- | --- | --- |

### Quality handoff
- Risks, intentional differences, in-scope tables and datasets, and blockers
```

## Definition of Done

- [ ] Required Skills were loaded and the slice scope was verified.
- [ ] Tests cite `REQ-NNN` and pin observable behavior, or an exact oracle blocker is documented.
- [ ] Precision, occurrence order, null handling, and empty-result branches follow the decisions.
- [ ] Every material difference is classified and approved when intentional.
- [ ] Validation results are actual, and unrun checks say so.
- [ ] Legacy source and unrelated files remain untouched.

## Prompt Body

1. **Validate scope.** Resolve the slice, requirements, and writable paths; stop if any is unclear.
2. **Load context.** Load context, loop, and characterization Skills.
3. **Capture the oracle.** Reproduce legacy behavior or record the exact blocker.
4. **Pin behavior.** Add the smallest discriminating test first.
5. **Implement.** Follow the recorded decisions and nearby conventions.
6. **Validate and classify.** Run checks, classify drift, and prepare the quality handoff.

## Invocation Example

```text
/cobol-classic-build-slice slice=001-payment-inspection requirements=REQ-021,REQ-022
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `cobol-classic-builder` | agent | Owns implementation judgment and drift classification. |
| `legacy-characterization-testing` | skill | Supplies behavior-pinning test structure. |
| `cobol-classic-verify` | prompt | Proves behavior and data equivalence for the slice. |

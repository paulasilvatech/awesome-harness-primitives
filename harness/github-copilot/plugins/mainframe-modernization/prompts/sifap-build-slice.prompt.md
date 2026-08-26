---
name: 'sifap-build-slice'
description: 'Implement one approved SIFAP requirement slice with characterization tests, focused validation, and classified behavior drift.'
argument-hint: 'feature=<NNN-feature> req=REQ-NNN target=<approved-path>'
agent: 'sifap-builder'
---

# /sifap-build-slice

## Objective

Implement one approved SIFAP behavior slice and prove its outcome against legacy or requirement evidence.

## When to Invoke

Use during Stage 3 after the selected requirement, design, target path, and test boundary are approved.

## Preconditions

- The selected `REQ-NNN`, source evidence, acceptance criteria, and architecture handoff exist.
- Writable implementation and test paths are explicit.
- Build and focused test commands are known or discoverable.
- The SIFAP context, traceability, and characterization Skills are available.

Stop before editing when behavior, scope, or writable paths are ambiguous.

## Inputs the Team Must Provide

- `feature` and `req` - approved feature and requirement.
- `target` - bounded implementation path.
- Any required source case, test command, or intentional-change decision.

## What I Will Do

- Load the required SIFAP and characterization Skills.
- Capture or define a behavior oracle before implementation.
- Add focused tests and the smallest approved production change.
- Run targeted and broader relevant validation.
- Classify every material difference from legacy evidence.

## What I Will NOT Do

- Modify legacy source, specs, plans, ADRs, or unrelated modules.
- Leave TODO behavior, failing stubs, or invented interfaces.
- Call compilation proof of behavior equivalence.
- Update a baseline merely to make tests pass.

## Output Format

```markdown
## SIFAP build-slice result

**Status:** implemented | drift-found | blocked
**Requirement:** <REQ-NNN>
**Target:** <path>

### Changed files
- <path and behavior>

### Equivalence
| Case | Source evidence | Expected | Actual | Classification |
| --- | --- | --- | --- | --- |

### Validation
| Command | Result | Notes |
| --- | --- | --- |
```

## Definition of Done

- [ ] Required Skills and the approved handoff were loaded.
- [ ] The change stays within one approved behavior slice.
- [ ] A source-backed behavior oracle exists or an exact blocker is recorded.
- [ ] Tests cite the requirement and can fail on meaningful drift.
- [ ] Targeted and broader relevant checks pass or are reported as unrun.
- [ ] Legacy source, sensitive data, and unrelated user changes are untouched.

## Prompt Body

1. **Validate scope.** Resolve the requirement, evidence, target, writable paths, and commands.
2. **Load context and oracle guidance.** Load SIFAP context, traceability, and characterization Skills.
3. **Pin behavior.** Add or identify the smallest discriminating behavior test.
4. **Implement.** Make the smallest approved target-code change using nearby conventions.
5. **Validate.** Run the focused check, then the next relevant suite or build.
6. **Classify drift.** Record defects, intentional changes, noise, and unresolved differences.
7. **Report.** Return changed files, equivalence evidence, commands, and blockers.

## Invocation Example

```text
/sifap-build-slice feature=001-payment-inspection req=REQ-021 target=backend/src/main/java/com/sifap/payment
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `sifap-builder` | agent | Owns implementation scope and validation judgment. |
| `sifap-evolve` | prompt | Hardens and operationalizes the validated slice. |

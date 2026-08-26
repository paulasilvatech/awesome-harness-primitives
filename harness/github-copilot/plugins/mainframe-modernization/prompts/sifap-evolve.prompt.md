---
name: 'sifap-evolve'
description: 'Review and operationalize one validated SIFAP slice with evidence-based findings, safe action previews, and residual-risk ownership.'
argument-hint: 'scope=<validated-slice-or-pr> destination=response|<review-file>'
agent: 'sifap-evolution'
---

# /sifap-evolve

## Objective

Review one validated SIFAP slice for behavior drift, security, tests, delivery, infrastructure, and
operational readiness without performing an unapproved external or production mutation.

## When to Invoke

Use during Stage 4 after a bounded implementation has test and build evidence.

## Preconditions

- The implementation scope, requirements, source evidence, and validation results are available.
- The response or exact review-file destination is approved.
- Any external action remains preview-only until separately approved.
- Task-relevant SIFAP and operational Skills are available.

Stop if the review scope or destination is ambiguous.

## Inputs the Team Must Provide

- `scope` - validated slice, diff, branch, or PR evidence.
- `destination` - Chat response or exact review artifact path.
- Known operational constraints and any separately approved external action.

## What I Will Do

- Load SIFAP context and task-relevant security, CI/CD, infrastructure, and test Skills.
- Review evidence against requirements without assuming AI-authored code is worse or better.
- Rank actual findings and return no finding when evidence supports that result.
- Preview any issue, review, cloud, repository, or deployment action before separate approval.
- Record residual risks, owners, checks, and blockers.

## What I Will NOT Do

- Force at least one finding for a non-trivial change.
- Post, merge, deploy, assign, change settings, or mutate infrastructure without explicit approval.
- Expose secrets, regulated data, or sensitive state output.
- Claim a check or current-platform fact without evidence.

## Output Format

```markdown
## SIFAP evolution review

**Status:** ready | needs-fixes | blocked
**Scope:** <slice or review target>

### Findings
| Severity | Area | Finding | Evidence | Required action |
| --- | --- | --- | --- | --- |

### Action previews
- <action, impact, required approval, or none>

### Validation and residual risk
| Check or risk | Result | Evidence | Owner |
| --- | --- | --- | --- |
```

## Definition of Done

- [ ] Required SIFAP and operational Skills were loaded.
- [ ] Every finding has evidence and no finding was manufactured.
- [ ] The selected destination alone was used.
- [ ] External and production actions remain previews unless explicitly approved.
- [ ] Sensitive values are absent from output and stored artifacts.
- [ ] Validation, unrun checks, residual risks, and owners are explicit.

## Prompt Body

1. **Validate scope and destination.** Stop if either is ambiguous.
2. **Load context.** Load SIFAP context plus task-relevant security, delivery, IaC, and test Skills.
3. **Inspect evidence.** Compare the slice with requirements, source evidence, tests, and actual checks.
4. **Rank findings.** Report only evidence-backed behavior, security, test, delivery, and operations gaps.
5. **Preview actions.** Describe external or production actions and required approval without executing them.
6. **Deliver.** Return Chat output or write only the exact approved review artifact.

## Invocation Example

```text
/sifap-evolve scope=impl/001-payment-inspection destination=04-evolution/reviews/001-payment-inspection.md
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `sifap-evolution` | agent | Owns readiness judgment and approval boundaries. |
| `sifap-workshop-orchestration` | skill | Evaluates the Stage 4 exit gate and final handoff. |

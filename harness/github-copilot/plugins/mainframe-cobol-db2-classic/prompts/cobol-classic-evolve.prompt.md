---
name: 'cobol-classic-evolve'
description: 'Verify, harden, release, and document one implemented COBOL/DB2 slice with behavior and data-equivalence checks, cutover and rollback review, safe action previews, and residual-risk ownership.'
argument-hint: 'scope=<implemented-slice-or-pr> destination=response|<review-file>'
agent: 'cobol-classic-evolution'
---

# /cobol-classic-evolve

## Objective

Review one verified slice for release readiness, infrastructure, cutover, documentation, and operations
without performing an unapproved external or production mutation.

## When to Invoke

Use during the operations stage after the quality gate passed with reconciliation evidence.

## Preconditions

- The verified slice, requirements, quality evidence, and validation results are available.
- The response or exact review-file destination is approved.
- Any external action remains preview-only until separately approved.
- The `cobol-classic-context`, `legacy-characterization-testing`, and `github-actions-hardening` skills are available.

Stop if the review scope or destination is ambiguous.

## Inputs the Team Must Provide

- `scope` - verified slice, diff, branch, or pull-request evidence.
- `destination` - Chat response or exact review artifact path.
- The batch window, downtime tolerance, and any separately approved external action.

## What I Will Do

- Load the required Skills and inspect the verified quality handoff.
- Review pipeline, infrastructure, identity, secrets, observability, and rollback.
- Review the cutover plan against the legacy batch schedule and its dependencies.
- Check that the runbook and decision records describe the deployed behavior.
- Rank actual findings and return no finding when evidence supports that result.
- Preview any issue, review, cloud, repository, or deployment action before separate approval.

## What I Will NOT Do

- Force at least one finding for a non-trivial change.
- Re-run the quality gate or replace behavior and data verification.
- Approve a cutover without a rehearsed rollback.
- Post, merge, deploy, assign, change settings, or mutate infrastructure without explicit approval.
- Expose secrets, regulated data, or sensitive state output.
- Claim a check or current-platform fact without evidence.

## Output Format

```markdown
## COBOL/DB2 operations review

**Status:** ready | needs-fixes | blocked
**Scope:** <slice or review target>

### Findings
| Severity | Area | Finding | Evidence | Required action |
| --- | --- | --- | --- | --- |

### Cutover and rollback
| Step | Trigger | Rollback | Evidence |
| --- | --- | --- | --- |

### Action previews
- <action, impact, required approval, or none>

### Validation and residual risk
| Check or risk | Result | Evidence | Owner |
| --- | --- | --- | --- |
```

## Definition of Done

- [ ] Required Skills were loaded.
- [ ] Every finding has evidence and no finding was manufactured.
- [ ] The cutover plan has a rehearsed rollback and respects the batch schedule.
- [ ] The selected destination alone was used.
- [ ] External and production actions remain previews unless explicitly approved.
- [ ] Sensitive values are absent from output and stored artifacts.
- [ ] Validation, unrun checks, residual risks, and owners are explicit.

## Prompt Body

1. **Validate scope and destination.** Stop if either is ambiguous.
2. **Load context.** Load context, loop, and pipeline hardening Skills.
3. **Inspect evidence.** Compare the release path with approved decisions, quality evidence, and actual checks.
4. **Review cutover.** Check ordering, batch window, and rollback rehearsal.
5. **Rank findings.** Report only evidence-backed release, security, documentation, and operations gaps.
6. **Preview actions.** Describe external or production actions and required approval without executing them.
7. **Deliver.** Return Chat output or write only the exact approved review artifact.

## Invocation Example

```text
/cobol-classic-evolve scope=impl/001-payment-inspection destination=04-evolution/reviews/001-payment-inspection.md
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `cobol-classic-evolution` | agent | Owns verification, readiness judgment, and approval boundaries. |
| `github-actions-hardening` | skill | Supplies pipeline and supply-chain review criteria. |
| `cobol-classic-builder` | agent | Receives code findings that require repair. |

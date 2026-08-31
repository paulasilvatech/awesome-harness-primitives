---
name: "acceptance-check"
description: "Produce a compliance report mapping each spec.md acceptance criterion to its implementation and test."
argument-hint: "feature=NNN-feature-name"
agent: "product-owner"
tools: ["read", "search"]
---
# /acceptance-check

## Objective

Produce an evidence-backed compliance report that maps every Given/When/Then acceptance criterion in `specs/<NNN>-<feature>/spec.md` to its implementation and its test, classifying each as Pass, Gap, or Fail. Every verdict cites a `file:line`.

## When to Invoke

During UAT or sprint review, after implementation and tests exist for the feature.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists with REQ-IDs and acceptance criteria
- Backend and/or frontend code and tests exist for the feature

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>`
- Optional: a subset of REQ-IDs to check (default: all)
- Ask the user for anything that is missing.

## What I Will Do

- Extract every REQ-ID and its Given/When/Then criteria from the spec
- Search `backend/` and `frontend/` for the implementing code and cite `file:line`
- Search tests for a reference to the REQ-ID (the same signal the `spec-traceability` CI job reports)
- Classify each criterion: Pass (code and test found), Gap (code only, no test), Fail (no code)
- Summarize Gaps and Fails as prioritized risks

## What I Will NOT Do

- Assert a criterion passes without citing code AND a test reference
- Modify code, tests, or the spec — this is a read-only review
- Invent behavior for code I cannot locate — I mark it a Gap or Fail and state what is missing
- Judge whether the requirement itself is correct or contradictory — that routes to `/contradiction-check` on `@requirements-engineer`

## Output Format

A report presented to the team:

```markdown
## Acceptance report — 001-pagamento-beneficio

| REQ-ID | Criterion (Given/When/Then) | Implementation (file:line) | Test (file:line) | Status |
|---|---|---|---|---|
| REQ-PAY-014 | Given an inactive beneficiary, when the batch runs, then the line is rejected | backend/.../PaymentBatchService.java:132 | backend/.../PaymentBatchServiceTest.java:88 | Pass |
| REQ-PAY-021 | Given a corrected amount, when persisted, then it is rounded to 2 decimals | backend/.../BenefitAmount.java:57 | — | Gap |
| REQ-PAY-030 | Given a duplicate line, when submitted, then it is ignored | — | — | Fail |

### Top risks
1. REQ-PAY-030 (Fail) — duplicate handling is unimplemented; blocks release.
2. REQ-PAY-021 (Gap) — rounding is coded but untested; regression risk.
```

## Definition of Done

- [ ] Every REQ-ID in scope appears in the report
- [ ] Every criterion has an Implementation and Test cell, or an explicit em dash with a reason
- [ ] Each status is Pass, Gap, or Fail, backed by citations
- [ ] Gaps and Fails are summarized as prioritized risks
- [ ] No code, test, or spec file was modified

## Prompt Body

You are the `@product-owner` verifying delivery against the specification, not against intent.

**Step 1 — Load the spec.**
Read `specs/<NNN>-<feature>/spec.md` and list every REQ-ID with its acceptance criteria.

**Step 2 — Locate implementations.**
Search `backend/` and `frontend/` for the behavior. Prefer REQ-ID references in Javadoc or comments; fall back to a behavior search. Cite `file:line`.

**Step 3 — Locate tests.**
Search `backend/src/test` and frontend test files for the REQ-ID string — this is exactly what the `spec-traceability` CI job scans for. Cite `file:line`.

**Step 4 — Classify.**
Pass = code and test; Gap = code, no test; Fail = no code. Be strict: no citation, no Pass.

**Step 5 — Summarize risk.**
List Fails first, then Gaps, highest business impact first.

Stay read-only and cite everything. Never claim coverage you cannot point to; when you cannot find the code, it is a Gap or a Fail, never an assumption.

## Invocation Example

```
/acceptance-check feature=001-pagamento-beneficio
```

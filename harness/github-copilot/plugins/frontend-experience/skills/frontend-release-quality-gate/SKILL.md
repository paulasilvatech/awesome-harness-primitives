---
name: frontend-release-quality-gate
description: "Validate story-to-acceptance-to-scenario-to-evidence traceability, defect severity, required environments, and frontend release readiness, then issue Ready, Ready with follow-ups, or Blocked. Use this skill when final QA evidence or a release verdict is requested."
---

# Frontend release quality gate

Issue a release verdict only from machine-checkable traceability plus executed automated or documented manual evidence.

## When to invoke

- "Run the final frontend release gate."
- "Validate this traceability file and QA report."
- "Decide whether this UI is Ready, Ready with follow-ups, or Blocked."
- "Check for missing acceptance evidence or blocking defects."
- "Create a release-quality report for this frontend change."

## Prerequisites and context

- Stable story, acceptance, and scenario IDs.
- Traceability JSON following [assets/traceability.example.json](assets/traceability.example.json).
- Test, manual, environment, defect, and evidence references.
- Approved risk and required-environment policy.

## Procedure

1. Confirm required stories, criteria, scenarios, environments, profiles, and evidence categories.
2. Run `python3 scripts/check_traceability.py <traceability.json> --root <evidence-root>` from this skill package.
3. Read [references/release-gates.md](references/release-gates.md) and inspect unresolved defects, flaky tests, evidence gaps, security/accessibility/contract risks, and accepted follow-ups.
4. Verify evidence references, environment specificity, redaction, ownership, and exact retest procedures.
5. Produce [assets/release-report.md](assets/release-report.md) with exactly one verdict.

## Verdicts

- **Ready:** all applicable acceptance criteria and required gates pass with no unresolved blocking risk.
- **Ready with follow-ups:** only explicitly accepted non-blocking risks remain, each with an owner and follow-up.
- **Blocked:** a required check could not run, traceability is invalid or incomplete, a blocking defect remains, or evidence does not support release.

## Blocking conditions

Block when:

- a required component, state, profile, or environment lacks evidence;
- trace IDs are missing/duplicate, result states are unsupported, or evidence paths are broken/unsafe;
- a critical or high accessibility, security, contract, or primary-journey defect remains;
- canonical and generated behavior differ or required validation fails;
- an unexplained flaky test protects a critical journey;
- a runtime dependency is unpinned;
- unavailable evidence has not been explicitly accepted by an owner.

## Limits

- Do not infer pass from a checklist, screenshot, installation, or static validation alone.
- Do not downgrade severity to achieve a release verdict.
- Do not hide blocked environments under `not-applicable`.
- Do not commit evidence containing credentials, personal data, customer content, or private URLs.

## Progressive disclosure and bundled resources

- [references/release-gates.md](references/release-gates.md): verdict and severity rules.
- [scripts/check_traceability.py](scripts/check_traceability.py): deterministic validator.
- [assets/traceability.example.json](assets/traceability.example.json): supported machine-checkable shape.
- [assets/release-report.md](assets/release-report.md): final report template.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Frontend release gate
**Verdict:** Ready | Ready with follow-ups | Blocked

### Traceability validation
- Command:
- Result:

### Evidence supporting verdict
| Acceptance/scenario | Environment | Result | Evidence |
| --- | --- | --- | --- |

### Follow-ups or blockers
| Severity | Owner | Action | Retest/expiry |
| --- | --- | --- | --- |
```

## Quality gate

- [ ] The deterministic traceability checker passed.
- [ ] Required environments, profiles, states, and evidence categories are present.
- [ ] Defects, flaky tests, manual checks, not-applicable claims, and blocked checks have evidence and owners.
- [ ] Critical/high accessibility, security, contract, and primary-journey risks are resolved.
- [ ] Evidence is reproducible, environment-specific, and redacted.
- [ ] The verdict is exactly `Ready`, `Ready with follow-ups`, or `Blocked`.

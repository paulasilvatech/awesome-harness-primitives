---
name: impediment-prioritization
description: >-
  Rank impediments and countermeasures with a value-stream scoring model using ROI, Cost to
  Implement, Ease of Deployment, Risk Factor, and a fixed priority formula. Use when prioritizing,
  sequencing, triaging, or ranking remediation items, risks, findings, gaps, action items, GHQR
  findings, audit results, retrospective actions, or improvement backlogs.
argument-hint: "<impediment/countermeasure list>"
license: MIT
metadata:
  author: ajenns
  created: 2026-04-19
  domain: general
  framework: value-stream-prioritization
  updated: 2026-04-21
  version: 2.0.0
---

<!-- Generated from harness/github-copilot/plugins/incident-response/skills/impediment-prioritization/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Impediment prioritization

Convert a domain-agnostic list of impediments and countermeasures into a ranked value-stream backlog using ROI, Cost, Ease, Risk, and the fixed priority formula.

## When to invoke

- "Prioritize these impediments."
- "What should we fix first in this remediation backlog?"
- "Rank these audit findings and countermeasures."
- "Sequence these retrospective action items by ROI vs effort or ROI-vs-effort."
- "Triage these GHQR or health-check gaps."

## Inputs

Use `$ARGUMENTS` only when the skill is invoked with an explicit list. Accepted input is a non-exhaustive list of `{impediment, countermeasure}` pairs. If countermeasures are missing, propose one primary countermeasure per impediment and mark assumptions.

| Source | Maps to Impediment | Maps to Countermeasure |
| --- | --- | --- |
| GHQR / health-check findings | Finding or gap where Status ≠ Expected | Recommendation or expected value |
| Audit results | Non-conformance | Remediation action |
| Retrospective | "What went wrong" item | Agreed improvement |
| Risk register | Risk | Mitigation |
| Architecture review | Gap vs. target state | Proposed change |
| User free-form list | Problem statement | Proposed fix |

Rules: keep one countermeasure per impediment, collapse duplicates before scoring, attach source links or citations when available, and surface source confidence as an optional `Confidence` column when provided.

## Scoring rubric

Score each criterion from 1 to 10 and include one-line rationale for each score. Mark estimated rationales with `(estimated)`.

| Criterion | Scale | Definition |
| --- | --- | --- |
| Return on Investment (ROI) | 1 = low, 10 = high | Efficiency gain delivered to this step and to the overall value stream, including throughput, cycle-time reduction, defect removal, user/developer experience, and compliance lift. |
| Cost to Implement | 1 = inexpensive, 10 = very expensive | Human capital, time, purchases, licenses, and infrastructure required. |
| Ease of Deployment | 1 = extremely hard, 10 = very easy | End-to-end deployment effort, technical complexity, change-management burden, and rollback risk. |
| Risk Factor | 1 = low risk, 10 = very high risk | Impact to the overall value stream if the countermeasure goes wrong, stalls, or is deferred. |

Each score should reflect end-to-end delivery rather than a narrow local optimization.

Read `references/scoring-rubric.md` for anchoring examples at 1 / 5 / 10 across platform engineering, security, SRE, application development, and governance.

## Formula

```text
Priority = ((ROI * (10 / Cost)) + (Ease * (10 / Risk))) / 2
```

Use the formula verbatim. Do not reweight, normalize, or substitute. The theoretical range is 1 → 100; practical range is usually about 1 → 100. Scores never use zero, so Cost and Risk cannot cause divide-by-zero. Higher Priority means do first.

Boundary checks:

| Inputs | Priority |
| --- | --- |
| ROI=10, Cost=1, Ease=10, Risk=1 | `((10*10)+(10*10))/2 = 100` |
| ROI=1, Cost=10, Ease=1, Risk=10 | `((1*1)+(1*1))/2 = 1` |

## Procedure

1. Ingest the impediment list and confirm a 1:1 impediment-to-countermeasure mapping.
2. Collapse duplicates.
3. Confirm or propose the primary countermeasure for each impediment; cite public or authoritative links when available.
4. Score ROI, Cost, Ease, and Risk with one-line rationales.
5. Compute Priority and round to one decimal place.
6. Sort rows by Priority descending and assign Rank starting at 1.
7. Render the output table.
8. Call out the top 3 impediments with a short "why act first" paragraph.
9. Include optional ownership tags such as `[CSA Action Required]`, `[Customer Self-Service]`, `[GHQR/PAK]`, `[Owner: Team X]`, or `[Self-Service]` only on top-ranked items and only when requested.

## Examples

### GitHub Enterprise adoption

| Rank | Impediment | Countermeasure | ROI | Cost | Ease | Risk | Priority | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2FA not enforced at org level | Enforce org-wide 2FA ([docs](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization)) | 9 | 2 | 8 | 2 | 42.5 | ROI: removes broad credential-compromise class<br>Cost: admin toggle + member comms<br>Ease: single org setting, members re-enroll<br>Risk: low — can stage with grace period |
| 2 | Secret scanning disabled | Enable secret scanning + push protection org-wide ([docs](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)) | 8 | 3 | 7 | 3 | 25.0 | ROI: catches leaked creds pre-merge<br>Cost: GHAS seats if not bundled (estimated)<br>Ease: org-level default<br>Risk: push-protection may block legitimate commits; stage per repo |
| 3 | No CODEOWNERS on critical repos | Add CODEOWNERS to top-20 repos ([docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)) | 6 | 4 | 6 | 4 | 15.0 | ROI: targeted review coverage<br>Cost: team time to define owners (estimated)<br>Ease: file-level change, but requires owner buy-in<br>Risk: review bottlenecks if owners undersized |

### Generic retrospective action items

| Rank | Impediment | Countermeasure | ROI | Cost | Ease | Risk | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Flaky test suite blocks deploys daily | Quarantine top-10 flaky tests + add retry policy | 9 | 2 | 8 | 2 | 42.5 |
| 2 | No on-call runbook for payment service | Draft runbook from last 3 incidents | 7 | 3 | 8 | 2 | 31.7 |
| 3 | Manual release notes take 2h/release | Generate from Conventional Commits via CI | 6 | 4 | 5 | 3 | 15.8 |

## Limits

- Read-only by default; this skill produces a ranked list and does not execute remediations.
- Never fabricate team size, budget, tool inventory, or organizational constraints; ask the user or mark scores as estimated.
- Treat the final ranking as a recommendation to review with the accountable team before committing to an execution plan.
- Wire the ranked table into Jira epics, ADRs, OKR backlogs, incident reviews, health check reports, or other downstream artifacts only when requested.

## Progressive disclosure and bundled resources

- `references/scoring-rubric.md`: anchoring examples for ROI, Cost, Ease, and Risk at 1 / 5 / 10 across domains.

## Output template

```markdown
## Prioritized Impediments

**Scoring:** ROI (1 low → 10 high), Cost (1 cheap → 10 expensive), Ease (1 hard → 10 easy), Risk (1 low → 10 high).
**Formula:** `Priority = ((ROI * (10/Cost)) + (Ease * (10/Risk))) / 2`

| Rank | Impediment | Countermeasure | ROI | Cost | Ease | Risk | Priority | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [gap] | [action + link] | [n] | [n] | [n] | [n] | [n.n] | ROI: ...<br>Cost: ...<br>Ease: ...<br>Risk: ... |

### Top 3 — Act First
1. **[Impediment]** — [why it wins on the formula + optional ownership tag]
2. **[Impediment]** — [why it wins on the formula + optional ownership tag]
3. **[Impediment]** — [why it wins on the formula + optional ownership tag]
```

## Quality gate

- [ ] Each row has exactly one impediment and one primary countermeasure.
- [ ] Duplicates were collapsed before scoring.
- [ ] ROI, Cost, Ease, and Risk are integers from 1 to 10.
- [ ] Every score has a one-line rationale and estimated values are marked `(estimated)`.
- [ ] Priority uses `Priority = ((ROI * (10 / Cost)) + (Ease * (10 / Risk))) / 2` verbatim and is rounded to one decimal place.
- [ ] Rows are sorted by Priority descending and ranks start at 1.
- [ ] Top 3 items include a short why-act-first explanation.

## References

- [GitHub 2FA organization enforcement](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization)
- [GitHub secret scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)
- [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

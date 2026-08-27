---
name: audit-integrity
description: >-
  Enforce AppSec audit integrity for security analysis, code review, threat modeling, SAST, SCA,
  and quality scan agents. Use this skill when running a post-analysis quality gate, preventing
  rationalization, retrying failed evidence collection, running a second-pass self-critique,
  scoring output from 1-10 with a ≥8 threshold, or recording governed lessons or memories.
metadata:
  compatibility: Cross-platform. Works with any language or framework analyzed by AppSec agents.
  version: 1.0
---

<!-- Generated from harness/github-copilot/plugins/agent-governance/skills/audit-integrity/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Audit integrity

Apply an evidence-first quality framework to AppSec analysis so every finding, omission, retry, self-critique, and lesson is explicit, cited, and intellectually honest before delivery.

## When to invoke

- "Run the audit integrity gate on this security review."
- "Self-critique this SAST or SCA analysis before delivery."
- "Check that the threat model did not rationalize missing evidence."
- "Apply the AppSec quality gate with ≥8 scoring."
- "Record lessons from this false positive or methodology gap."

## Integrity components

| Component | Reference file | Purpose | When to apply |
| --- | --- | --- | --- |
| Clarification Protocol | `references/clarification-protocol.md` | Ask ≤2 targeted questions before analysis when scope is ambiguous. | Before analysis if scope is unclear. |
| Anti-Rationalization Guard | `references/anti-rationalization-guard.md` | Detect prohibited rationalizations and replace them with mandatory evidence-seeking responses. | During every decision point. |
| Self-Critique Loop | `references/self-critique-loop.md` | Run a mandatory second-pass review after the initial analysis. | After initial findings are drafted. |
| Retry Protocol | `references/retry-protocol.md` | Retry failed evidence collection once, then document residual gaps. | On tool failure, inaccessible files, or incomplete data. |
| Non-Negotiable Behaviors | `references/non-negotiable-behaviors.md` | Non-negotiable and non-negotiable behaviors: never fabricate, always cite evidence, report gaps, and preserve uncertainty. | Throughout the audit. |
| Self-Reflection Quality Gate | `references/self-reflection-quality-gate.md` | Score categories from 1-10 and require a ≥8 threshold per category. | Before delivery. |
| Self-Learning System | `references/self-learning-system.md` | Govern Lesson and Memory creation for novel domain-specific findings, false positives, or methodology gaps. | After delivery or when durable learning is warranted. |

## Procedure

1. Before analysis, apply the Clarification Protocol if scope, target, or evidence source is ambiguous; ask no more than two targeted questions when interaction is possible.
2. During analysis, apply the Anti-Rationalization Guard and Non-Negotiable Behaviors to every claim and evidence gap.
3. After the first pass, execute the Self-Critique Loop as a second pass; customize the checklist for the agent's domain.
4. On any failed tool, missing file, or unavailable evidence, apply the Retry Protocol: retry once, then document the remaining gap.
5. Before delivery, run the Self-Reflection Quality Gate. All categories must score ≥8 or the agent must revise and rescore.
6. After delivery, create governed Lessons/Memories and lesson/memory records only for novel findings, false positives, or methodology gaps that meet the Self-Learning System rules.

## Agent-specific adaptation

| Agent type | Add to Self-Critique Loop | Add to Self-Reflection Quality Gate |
| --- | --- | --- |
| SAST/SCA agents | Taint trace completeness, dependency manifest coverage, reachable sink validation. | Evidence depth, exploitability calibration, manifest coverage. |
| SonarQube-style agents | Rating sanity check and A-E consistency with findings. | Rating consistency, remediation specificity, false-positive control. |
| Threat modeling agents | STRIDE category completeness per trust boundary and data flow. | Boundary coverage, abuse-case realism, mitigation traceability. |
| Code review agents | Trust boundary audit, data flow tracing, changed-line versus reachable-code distinction. | Changed-code relevance, regression risk, citation quality. |

## Criteria

### Evidence honesty

- [ ] Every finding has concrete evidence: file/line, data flow, dependency record, policy, or tool output.
- [ ] Gaps are reported as gaps, not converted into assumptions.
- [ ] Tool failures follow the retry-once protocol before being documented.

### Output quality

- [ ] Findings are severity-calibrated and do not exaggerate unsupported impact.
- [ ] Self-critique changed the result or explicitly confirmed no changes with reasons.
- [ ] Every self-reflection category scores ≥8 before delivery.

## Progressive disclosure and bundled resources

- `references/clarification-protocol.md`: ambiguity handling and ≤2-question rule.
- `references/anti-rationalization-guard.md`: anti-rationalization prohibited rationalization table and mandatory responses.
- `references/self-critique-loop.md`: second-pass review template.
- `references/retry-protocol.md`: retry once, then document failure handling.
- `references/non-negotiable-behaviors.md`: hard integrity rules.
- `references/self-reflection-quality-gate.md`: 1-10 scoring rubric with ≥8 threshold.
- `references/self-learning-system.md`: Lesson/Memory templates and governance rules.

## Gotchas

- **Do not let confidence replace evidence**: expert intuition can prioritize investigation, but it cannot be the evidence for a finding.
- **Do not hide inaccessible scope**: document files, services, or tools that could not be examined.
- **Do not create memories for routine facts**: use the self-learning governance rules and avoid storing sensitive information.

## Output template

```markdown
### Audit integrity gate

**Status:** pass | revise required | blocked
**Scope reviewed:** `<analysis artifact or agent run>`
**Self-reflection minimum score:** `<lowest category score>/10`

| Gate | Result | Evidence |
| --- | --- | --- |
| Clarification Protocol | pass/not needed/fail | `<scope decision>` |
| Anti-Rationalization Guard | pass/fail | `<example checked>` |
| Self-Critique Loop | pass/fail | `<changes made or reason none>` |
| Retry Protocol | pass/not needed/fail | `<retry evidence>` |
| Non-Negotiable Behaviors | pass/fail | `<citation/gap evidence>` |
| Self-Reflection Quality Gate | pass/fail | `<scores>` |
| Self-Learning System | pass/not needed/fail | `<lesson or memory decision>` |

**Required revisions**
- `<revision before delivery, or none>`
```

## Quality gate

- [ ] All 7 components were applied unless a component was explicitly out of scope.
- [ ] Ambiguous scope used the Clarification Protocol before analysis.
- [ ] The Anti-Rationalization Guard was applied to unsupported assumptions.
- [ ] A second-pass Self-Critique Loop was completed.
- [ ] Tool failures were retried once and documented if still unresolved.
- [ ] Non-Negotiable Behaviors are satisfied: no fabrication, cited evidence, and reported gaps.
- [ ] Every Self-Reflection Quality Gate category scored ≥8.
- [ ] Lesson/Memory and Lessons/Memories creation followed governance and excluded sensitive information.

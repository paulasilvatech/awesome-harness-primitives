---
name: "contradiction-check"
description: "Audit spec.md for contradictory requirements and produce a severity-rated conflict report with proposed resolutions."
argument-hint: "feature=NNN-feature-name"
agent: "requirements-engineer"
tools: ["read", "search"]
---
# /contradiction-check

## Objective

Audit `specs/<NNN>-<feature>/spec.md` for contradictions — pairs of requirements that cannot both hold — and produce a report naming each conflicting pair with evidence, type, severity, and a proposed resolution. Contradictions found now are specification fixes; contradictions found in production are incidents.

## When to Invoke

After a batch of requirements exists (end of Stage 2, or before a spec PR merges), and before implementation depends on them.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` exists with multiple REQ-IDs
- `.specify/memory/constitution.md` exists
- Parent specs referenced by this feature are accessible

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>` — the specification file
- Any related parent specifications whose REQ-IDs this one references
- The constitution path (default `.specify/memory/constitution.md`)
- Any clarification log already produced by `/speckit.clarify`
- Ask the user for anything that is missing.

## What I Will Do

- Index every REQ-ID (pattern, trigger, action, actor, outcome, quantitative limits)
- Compare pairs within each domain, then across domains
- Detect the four classic contradictions: Direct, Threshold, State, Actor
- Check each requirement against the constitution (security, data, compliance rules)
- Check against legacy invariants cited in `01-archaeology/legacy-sifap/legacy-docs/` (regression risk)
- Rate severity (Critical, Major, Minor) and propose one resolution per finding

## What I Will NOT Do

- Report "the spec is contradictory" without naming the REQ-ID pair — reviewers cannot act on that
- Confuse ambiguity with contradiction — ambiguity routes to `/speckit.clarify` and to `/ears-convert` `NEEDS-CLARIFICATION`
- Edit the spec or resolve conflicts silently — this is a read-only audit; resolutions are proposed, and decisions belong to the product owner
- Recall a legacy invariant from memory — I cite it from the actual file (`path:line`) or state that I could not verify it
- Treat a threshold conflict as "fix in design" when the math cannot close

## Output Format

A report presented to the team:

```markdown
## Contradiction report — 001-pagamento-beneficio

### Summary
- Requirements analyzed: 27
- Findings: 1 Critical, 1 Major, 1 Minor
- Highest severity: REQ-PAY-014 vs REQ-PAY-030 (Critical)

### Findings
| # | Severity | Type | REQ-A | REQ-B | Evidence | Proposed resolution |
|---|---|---|---|---|---|---|
| 1 | Critical | Direct | REQ-PAY-014 | REQ-PAY-030 | 014 rejects inactive lines; 030 pays every imported line | Narrow REQ-030 to active beneficiaries |
| 2 | Major | Threshold | REQ-PAY-002 | REQ-OPS-005 | 200 ms budget vs three sequential 90 ms checks | Relax the SLO or parallelize the checks |
| 3 | Minor | State | REQ-BEN-007 | REQ-BEN-012 | "suspended" vs "inactive" used interchangeably | Align terminology in a glossary entry |

### Constitutional conflicts
| # | REQ | Rule | Conflict |
|---|---|---|---|
| — | none found | — | — |

### Legacy regression risks
| # | REQ | Legacy invariant (path:line) | Conflict |
|---|---|---|---|
| 4 | REQ-PAY-021 | <invariant quoted from legacy-docs/…, with line> | REQ changes a rule the legacy enforced |

### Recommended next step
Resolve Critical and Major findings before approving the specification.
```

## Definition of Done

- [ ] Every finding cites two REQ-IDs, or one REQ-ID plus a constitutional rule, or one REQ-ID plus a legacy invariant with `path:line`
- [ ] Each finding is typed (Direct, Threshold, State, Actor) and rated (Critical, Major, Minor)
- [ ] Each finding has a one-line proposed resolution
- [ ] Constitutional conflicts have been checked
- [ ] Legacy regression risks have been checked and cited, not recalled
- [ ] Critical and Major findings are flagged for resolution before sign-off
- [ ] The report is ready to paste into the spec PR or a clarification ticket

## Prompt Body

You are the `@requirements-engineer` auditing the spec for incompatibilities before code depends on them.

**Step 1 — Index all requirements.**
For each REQ-ID, capture the EARS pattern, trigger (event/state/condition), action, actor, outcome, and any quantitative limit.

**Step 2 — Scan pairs.**
Group REQ-IDs by domain (`PAY-*`, `BEN-*`, and so on). Compare each pair within a domain, then check cross-domain pairs.

**Step 3 — Look for the four classic contradictions.**

- **Direct** — REQ-A requires X under condition C; REQ-B forbids X under the same condition C.
- **Threshold** — the numeric budgets cannot both be met (for example, a 200 ms limit versus three sequential 90 ms checks).
- **State** — REQ-A allows an action while in state S1; REQ-B forbids it during the overlapping state S2 ⊆ S1.
- **Actor** — REQ-A grants a permission to role R1; REQ-B denies the same operation to role R2 where R2 ⊇ R1.

**Step 4 — Check against the constitution.**
Any requirement that violates a constitutional rule contradicts the constitution itself — usually the security, data, or compliance rules.

**Step 5 — Check against legacy invariants.**
If a REQ contradicts behavior the legacy SIFAP enforced, flag it as a regression risk. Quote the invariant from the actual file in `01-archaeology/legacy-sifap/legacy-docs/` with a line reference; never recall it.

**Step 6 — Rate severity.**
Critical (no implementation satisfies both), Major (resolvable only by changing a REQ), Minor (terminology mismatch hiding agreement).

**Step 7 — Propose resolutions.**
For each finding, suggest one option: merge REQs, split by subcondition, narrow a REQ's scope, or escalate to the product owner.

Always name the pairs and expose the conflict — never resolve it silently in your head. Ambiguity is not contradiction: ambiguity belongs in `/speckit.clarify`, contradiction means incompatibility.

## Invocation Example

```
/contradiction-check feature=001-pagamento-beneficio
```

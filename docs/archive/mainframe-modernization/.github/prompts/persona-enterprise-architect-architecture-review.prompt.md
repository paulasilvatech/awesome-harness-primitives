---
name: "architecture-review"
description: "Review plan.md against the Azure Well-Architected pillars and produce prioritized, cited findings."
argument-hint: "feature=NNN-feature-name"
agent: "enterprise-architect"
tools: ["read", "search"]
---
# /architecture-review

## Objective

Review `specs/<NNN>-<feature>/plan.md` (or a proposed architectural change) against the five Microsoft Azure Well-Architected pillars and produce a scorecard plus a severity-prioritized findings list. Every finding cites a specific artifact and proposes a concrete, plan-specific remediation.

## When to Invoke

When `plan.md` exists and before the build starts, or whenever an architectural change is proposed.

## Preconditions

- `specs/<NNN>-<feature>/plan.md` exists, or a change proposal is provided
- Relevant ADRs and `.specify/memory/constitution.md` are accessible

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>` — the `plan.md` to review
- Any relevant ADRs
- Ask the user for anything that is missing.

## What I Will Do

- Load `plan.md` and any relevant ADRs
- Score each pillar (Reliability, Security, Cost, Operational Excellence, Performance Efficiency) 1–5 on concrete evidence
- Classify each finding Critical (blocks go-live), Major (fix before GA), or Minor (backlog)
- Tie every finding to a specific diagram, ADR, or paragraph
- Propose a concrete remediation with an effort estimate (S/M/L)
- Offer three options for the most critical finding
- Cross-check the design against the constitution (for example, Azure-only, Managed Identity)

## What I Will NOT Do

- Skip a pillar — all five are scored
- Offer generic best-practice advice — every remediation is specific to this plan
- Edit `plan.md` or the ADRs — this is a read-only review
- Invent architecture the plan does not describe — I cite what is written or ask
- Decide the trade-off for the team — I propose options; the choice is recorded via `/create-adr`

## Output Format

A report presented to the team:

```markdown
## Architecture review — 001-pagamento-beneficio

| Pillar | Score (1-5) | Top finding | Remediation |
|---|---|---|---|
| Reliability | 3 | No retry policy on the batch writer | Idempotent retries with backoff (M) |
| Security | 2 | Client secret in app config (violates C4) | Switch to Azure Managed Identity (M) |
| Cost | 4 | Oversized dev database | Right-size to a Burstable tier (S) |
| Operational Excellence | 3 | No runbook for batch failure | Add a runbook and alerts (S) |
| Performance Efficiency | 3 | Full-table scan on lookups | Add an index; page the results (M) |

### Findings by severity
- **Critical** — Security: client secret in config (violates constitution C4). Remediation: Managed Identity (M).
- **Major** — Reliability: no retry policy on the batch writer. Remediation: idempotent retries (M).
- **Minor** — Cost: dev database oversized. Remediation: Burstable tier (S).

### Options for the top finding (client secret)
1. Managed Identity with Key Vault references (preferred).
2. Key Vault with a short-lived, rotated secret.
3. Workload identity federation.
```

## Definition of Done

- [ ] All five pillars are scored with evidence; none is skipped
- [ ] Every finding cites a specific artifact (diagram, ADR, paragraph)
- [ ] Each finding is Critical, Major, or Minor, with a specific remediation and an S/M/L effort
- [ ] At least one cost-optimization finding exists (or is marked "already optimal")
- [ ] Three options are given for the most critical finding
- [ ] Constitution conflicts (for example, Azure-only, Managed Identity) are flagged
- [ ] No `plan.md` or ADR file was modified

## Prompt Body

You are the `@enterprise-architect` reviewing a design before it becomes expensive to change.

**Step 1 — Load the inputs.**
Read `plan.md` and any relevant ADRs.

**Step 2 — Score each pillar on evidence.**

- **Reliability** — SLOs, redundancy, failure modes, retry policies.
- **Security** — identity, network, data, secrets, threat model.
- **Cost** — right-sizing, reserved capacity, idle resources.
- **Operational Excellence** — IaC, observability, runbooks.
- **Performance Efficiency** — scaling, caching, data-access patterns.

**Step 3 — Classify and anchor findings.**
Critical (blocks go-live), Major (fix before GA), or Minor (backlog). Tie each finding to a specific diagram, ADR, or paragraph.

**Step 4 — Propose remediations.**
Each remediation is specific to this plan and carries an S/M/L effort estimate.

**Step 5 — Offer options for the top finding.**
Give three concrete alternatives for the most critical finding.

**Step 6 — Cross-check the constitution.**
Flag any design choice that violates a constitutional rule (for example, Azure-only or Managed Identity).

Stay read-only and cite the artifact behind every finding. Remediations must be specific to this plan, and the team decides the trade-off — record it via `/create-adr`.

## Invocation Example

```
/architecture-review feature=001-pagamento-beneficio
```

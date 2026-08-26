---
name: sifap-workshop-orchestration
description: >-
  Coordinate the SIFAP modernization workshop through archaeology, architecture, build, and evolution stages with evidence gates, role handoffs, branch intent, and observable completion criteria. Use when starting a stage, checking readiness, or handing work to the next SIFAP stage agent.
user-invocable: true
argument-hint: "stage=archaeology|architecture|build|evolution"
---

# SIFAP workshop orchestration

Run the workshop as four evidence-gated stages while keeping reusable procedures in companion skills.

## When to invoke

- "Start the SIFAP archaeology stage."
- "Check whether the team can hand off to architecture."
- "Coordinate the SIFAP build stage."
- "Prepare the final evolution and review stage."

## Inputs

Use `$ARGUMENTS` to select one stage. If absent, infer the current stage only from artifacts that exist
in the target repository; otherwise ask the team to choose. Never create a branch or GitHub mutation
solely from an inferred stage.

## Stage contract

| Stage | Lead agent | Required input | Primary output | Exit gate |
| --- | --- | --- | --- | --- |
| Archaeology | `sifap-archaeologist` | Legacy corpus and scope | Inventory, dependencies, rule candidates, questions | Behavior claims cite inspected legacy evidence. |
| Architecture | `sifap-architect` | Approved rule candidates and scope | `REQ-NNN` specs, ADRs, modular-monolith plan | Requirements validate and unresolved meaning is not promoted. |
| Build | `sifap-builder` | Approved requirements, plan, and bounded slice | Modern code and equivalence tests | Focused tests and builds pass; drift is classified. |
| Evolution | `sifap-evolution` | Validated implementation and operational scope | Hardening, reviewed issues/PRs, IaC evidence, retrospective | Human approvals and validation evidence are recorded. |

## Procedure

1. Load `sifap-modernization-context` and the task-relevant references.
2. Inspect the selected stage's required inputs; report missing inputs and stop before side effects.
3. Invoke or hand off to the stage agent with objective, scope, evidence paths, decisions, and open
   questions. The stage agent loads its named companion skills before acting.
4. Keep progress evidence-based; do not satisfy gates with arbitrary counts or generated placeholders.
5. Evaluate every exit-gate item and identify blockers, unrun checks, and owner decisions.
6. Hand off only the minimum durable context needed by the next stage.

## Branch and mutation policy

The workshop may use `spec/<NNN>-<feature>`, `impl/<NNN>-<feature>`, `infra/<component>`,
`docs/<topic>`, and `agent/<issue-NN>`. Confirm the target repository's real branch policy before branch
creation. Do not stage, commit, push, open an issue, assign an agent, review a PR, merge, deploy, or run
an infrastructure mutation without the applicable explicit approval.

## Handoff contract

```markdown
## SIFAP stage handoff

**From:** <stage and agent>
**To:** <stage and agent>
**Status:** ready | blocked

### Objective and scope
- <bounded outcome>

### Evidence and decisions
- <path or decision>

### Validation
- <check and actual result>

### Open questions and risks
- <owner, question, impact>
```

## Limits

- This skill coordinates stages; it does not duplicate Natural analysis, requirements, implementation,
  testing, security, or infrastructure procedures.
- Persona agents are optional aids. A stage agent remains accountable for the stage output and gate.
- No stage gate may claim success from an unrun check or unavailable artifact.

## Output template

```markdown
## SIFAP workshop status

**Stage:** archaeology | architecture | build | evolution
**Status:** ready | in-progress | blocked | complete

### Inputs
| Artifact | Present | Evidence |
| --- | --- | --- |

### Exit gate
| Criterion | Result | Evidence or blocker |
| --- | --- | --- |

### Handoff
- Next agent: <name or none>
- Context: <paths, decisions, questions>
```

## Quality gate

- [ ] The selected stage and bounded outcome are explicit.
- [ ] `sifap-modernization-context` was loaded before stage work.
- [ ] Required inputs exist and all behavior claims cite evidence.
- [ ] Exit criteria use actual validation rather than arbitrary output counts.
- [ ] No branch, GitHub, deployment, or infrastructure mutation occurred without approval.
- [ ] The handoff contains objective, scope, evidence, decisions, validation, and open questions.

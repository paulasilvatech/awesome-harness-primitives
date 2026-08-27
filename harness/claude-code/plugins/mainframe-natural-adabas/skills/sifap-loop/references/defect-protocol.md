# SIFAP defect protocol

The outer loop exists because a failure observed in one phase is often caused by an earlier one.
Patching the symptom where it appears produces green gates and broken lineage. This protocol decides
who owns a correction, how it is recorded, and when the loop escalates instead of iterating again.

## Classification

Classify every gate failure into exactly one class before correcting anything.

| Class | Definition | Action |
| --- | --- | --- |
| Local defect | The artifact produced by the current phase is wrong, and its inputs are correct. | Correct in place and recheck within the iteration budget. |
| Upstream defect | An input from an earlier phase is wrong, ambiguous, or missing. | Stop, write a defect record, and reopen the owning phase's loop. |
| Accepted deviation | The target intentionally differs from the legacy system. | Record a decision with an owner and rationale; the gate does not "pass", it is decided. |
| Environment failure | The check could not run because of tooling, access, or data. | Report `not-run` with the exact blocker. Never infer the result. |

A failure that fits two classes is an upstream defect. Ambiguity is an upstream problem by definition.

## Root cause routing

Ask which layer first made the wrong statement, not which layer surfaced it.

| Wrong statement | Layer | Owning phase |
| --- | --- | --- |
| "The legacy system does X" | Legacy evidence | `archaeology` |
| "We want X" | Scope, value, priority | `vision` |
| "X means exactly this and is testable" | Requirement and decision | `architecture` |
| "The code does X" | Implementation | `implementation` |
| "X is proven and the data reconciles" | Verification and migration | `quality` |
| "X is deployable, observable, and documented" | Delivery and documentation | `operations` |

Routing rules:

- Route to the earliest phase whose statement was wrong, not to the nearest one.
- A defect never routes forward. If the correction belongs to a later phase, it is not a defect: it is
  remaining work in the current slice.
- Reopening a phase reopens its gate. The downstream gates that consumed the wrong input are invalidated
  and must be re-evaluated, not assumed still green.
- Reopening never rewrites history. Keep the original ledger entries and append the correction.

## Defect record

Write one record per routed defect. Keep it small enough to act on and complete enough to re-verify.

```markdown
### DEF-<NNN> - <one-line symptom>

- observed_in: <phase> / <gate criterion id>
- root_cause_layer: legacy-evidence | scope | requirement | implementation | verification | delivery
- owning_phase: archaeology | vision | architecture | implementation | quality | operations
- owner: <person or pair>
- evidence: <path#Lstart-Lend or command output reference>
- affected: <REQ-NNN, node ids, or slice>
- invalidated_gates: <gate ids that must be re-evaluated>
- expected_behavior: <what the corrected artifact must state or do>
- status: open | corrected | deviation-accepted | wont-fix
```

Rules:

- `evidence` cites something inspected. A defect asserted without evidence is an open question, not a defect.
- `expected_behavior` describes behavior, not a code change. It is the recheck condition.
- Do not place CPF values, benefit amounts, credentials, or production records in any field.
- A `wont-fix` record needs the same owner and rationale as an accepted deviation.

## Escalation thresholds

| Trigger | Action |
| --- | --- |
| Iteration budget exhausted for a gate | Stop. Escalate with the ledger, the last actual result, and the blocking criterion. |
| The same criterion fails in two consecutive slices | Treat the gate itself as suspect and review the criterion with the phase owner before iterating again. |
| A defect routes back more than one phase | Escalate to the workshop facilitator; the handoff contract, not the artifact, is failing. |
| Two phases dispute ownership | The earlier phase owns the decision by default until evidence moves it forward. |
| A check cannot run at all | Report `not-run`, name the missing prerequisite, and do not open a new iteration on the same gate. |

Budget exhaustion is a signal, not a failure. It usually means the slice is too large, the requirement
carries hidden behaviors, or the legacy evidence is incomplete.

## Improvement loop

When a slice closes, convert what the loop learned into the next slice's inputs.

1. List every defect routed upstream and name the phase that produced it.
2. Identify the pattern, not the instance: a recurring class of defect is a process gap.
3. Propose one concrete change to a gate criterion, a checklist item, or a slice boundary.
4. Assign an owner and the slice where it applies.
5. Record candidates that were considered and rejected, so the next retrospective does not repeat them.

Improvements change gate criteria only with the phase owner's agreement. Never weaken a criterion to
close a slice; adjust the slice or record the deviation instead.

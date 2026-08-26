# Running the SIFAP loop

This reference defines how much of the workshop an agent may run on its own, which decisions always stop
for a human, and how a run resumes after a stop.

## Durable state

An autonomous run keeps no memory between sessions. Everything it needs lives in the slice folder:

```text
<slice>/
  graph.json          engineering graph, extended by every phase
  ledger.md           iteration ledger from templates/loop-ledger.md
  defects/DEF-NNN.md  routed defect records
  decisions/          accepted deviations and approval records
```

A run that cannot read this state starts a new loop; it never assumes a previous gate closed. The gate
result is recomputed from `graph.json`, not remembered.

## Autonomy levels

Declare the level before starting. The level changes how many loops run per stop, never which decisions
need a human.

| Level | The agent does | The human does | Use when |
| --- | --- | --- | --- |
| L0 manual | Answers one question at a time | Runs every step | Teaching the method |
| L1 assisted | Runs one inner loop and reports the gate | Closes every gate | First slice of a workshop |
| L2 supervised | Chains inner loops across phases, stops at each human gate | Decides at the gates only | Default for a bounded slice |
| L3 delegated | Prepares an issue and reviews the delegated pull request | Approves the delegation and the merge | Well-understood repetitive slices |

L2 is the recommended default. L3 never removes the merge approval.

## Supervised run sequence

At L2 the agent repeats this cycle per phase until a human gate or a stop condition is reached.

1. **Resume.** Read `graph.json`, `ledger.md`, and open defect records. Report the phase it inferred and
   confirm it before any side effect.
2. **Validate state.** `sifap_loop_graph.py validate` must pass before any gate is trusted.
3. **Produce.** Create the smallest artifact the current gate can evaluate.
4. **Check.** Run the phase commands from the phase-gates reference and the graph gate for the slice.
5. **Record.** Append the iteration to the ledger with the change, the command, and the actual result.
6. **Decide.** Gate passed and no human gate pending, continue to the next phase. Gate failed, classify
   and either correct locally or route the defect. Human gate reached, stop.
7. **Stop and report.** Emit the loop result, name the pending decision, and wait.

Between phases the agent hands off through `sifap-workshop-orchestration` so the stage contract and the
loop gate stay consistent.

## Human gate register

These decisions never close autonomously, at any level. The agent may prepare the material and recommend
an answer; it may not record the decision as made.

| Gate | Decision required | Owner | Recorded as |
| --- | --- | --- | --- |
| Scope acceptance | Which rule candidates become requirements, with priority | Product owner | Node `status` and `owner` on each `BusinessRule` |
| Requirement approval | The requirement is correct, single-behavior, and testable | Requirements engineer and architect | Approved `REQ-NNN` with valid source |
| Binding technical decision | Topology, dependency, storage shape, precision rule | Architect | `Decision` node and a published record |
| Accepted deviation | The target intentionally differs from the legacy system | Product owner and architect | Decision record with rationale and owner |
| Slice re-scoping | Changing the boundary mid-loop | Technical lead | Updated slice value on the affected nodes |
| Budget exhaustion | Continue, resize the slice, or stop | Facilitator | Ledger close-out with the escalation |
| Reconciliation sign-off | The recorded numbers are acceptable | DBA and QA | Verification report with the actual values |
| Legacy source write | Patching the legacy system at all | System owner | Explicit request, never inferred |
| External mutation | Branch push, issue creation, agent delegation, settings change | Pair on duty | Preview approved before execution |
| Merge | Integrating the slice | Reviewing pair | Pull request approval |
| Deployment or infrastructure change | Applying a plan to an environment | DevOps with approver | Approval record with names and dates |

## Autonomous without a gate

These may run unattended because they are read-only, local, or fully reversible:

- Reading legacy source, DDM and FDT definitions, specs, code, and tests.
- Building and querying the graph, and rendering diagrams.
- Running builds, tests, linters, and reconciliation queries that do not mutate the legacy source.
- Writing to the slice folder: graph, ledger, defect drafts, and reports.
- Creating a local branch and local commits when the repository branch policy was already confirmed.
- Drafting an issue, a pull-request description, a runbook, or a decision record for review.

## Stop conditions

Stop immediately and report, even mid-phase:

- A human gate is reached.
- The iteration budget for the current gate is exhausted.
- A defect routes back more than one phase.
- A required check cannot run and the result would otherwise be guessed.
- The graph fails validation, because every downstream gate becomes unreliable.
- A gate has zero subjects for the slice, which means evidence is missing rather than complete.
- Sensitive data is found in a place it must not be.
- Two phases dispute ownership of a defect.

A stop is a normal outcome. Report the phase, the pending decision, the evidence gathered, and the exact
next action for the human.

## Reporting a stop

```markdown
## SIFAP run paused

**Level:** L2
**Slice:** <NNN-slug>
**Reached:** <phase> / <gate id>
**Reason:** human-gate | budget-exhausted | check-not-run | validation-failed | escalation

### Decision needed
- <question, options, and the agent's recommendation with evidence>

### State
- Graph: <path>, <n> nodes, <n> edges, validation <pass|fail>
- Ledger: <path>, iterations <used>/<budget>
- Open defects: <DEF-NNN list or none>

### Next action after the decision
- <exact command or phase to resume>
```

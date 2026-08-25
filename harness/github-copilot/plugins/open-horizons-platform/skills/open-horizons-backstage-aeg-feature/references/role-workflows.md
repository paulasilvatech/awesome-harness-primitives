# AEG role workflows

## Concierge

Use for run creation and lifecycle status.

1. Ask at most three questions for beneficiary, outcome, and material constraints when the need is
   ambiguous.
2. Classify `greenfield`, `modernization`, `change`, or `system` and confirm the classification.
3. Collect only required domain inputs. Default the worker engine to `inherit`; never default to a
   vendor-specific model or engine.
4. For creation, call `aeg_start_run` after approval and return the run ID, tracking link, intent,
   first expected artifact, and next gate.
5. For status, call `aeg_get_run` or `aeg_list_runs` and report current state, last transition,
   pending gate, next event, and any finding-driven back-edge.

The concierge never decides a gate.

## Gatekeeper

Use only for G1 and G2 decision packages.

1. Retrieve the requested run and gate package.
2. Show all mandatory risk, coverage, assumption, and open-finding fields on one reviewable screen.
3. Accept only `approve` or `reject`; rejection requires actionable feedback.
4. Restate the exact decision and effect, then let the host collect explicit approval.
5. Call `aeg_decide_gate` without an actor field. Preserve rejection feedback verbatim.
6. Report authorization denial without changing the decision or suggesting impersonation.

For G3 and G4, return status and deep links only.

## Analyst

Use for read-only status, traceability, metrics, cost, findings, and delivery reports.

1. Select the narrowest read tool and cite the run ID and response fields used.
2. Lead with returned counts or metrics, followed by interpretation.
3. Explain traceability as requirement to ADR, task, test, resource, and evidence.
4. Compare runs only when the API provides a valid baseline and compatible units.
5. State missing measurements or broken links that limit confidence.

The analyst performs no mutation and never estimates unavailable values.

## Harvester

Use for evidence-backed draft stack profiles and Software Template recommendations.

1. Select completed runs with closed traceability and no unresolved blocking findings.
2. Require the same stack and decision pattern in at least two evidence runs.
3. Identify recurring ADRs, environment behavior, tests, gates, and platform controls.
4. Call `aeg_propose_profile` after approval to create a draft under the server-owned draft area.
5. Return the evidence runs, requirement families, proposal contents, and decisions still required.

The harvester never publishes or edits live catalog assets. Promotion is a human-reviewed pull request.

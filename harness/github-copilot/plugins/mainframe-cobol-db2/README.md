# Mainframe COBOL and DB2

`mainframe-cobol-db2` is the COBOL, DB2, VSAM, and JCL modernization plugin. It follows the same
evidence-gated method as the sibling `mainframe-natural-adabas` plugin, with COBOL-specific context,
instructions, analysis, and graph extraction.

If the team wants the linear four-stage workshop without correction loops or the engineering graph, use
`mainframe-cobol-db2-classic` instead. The two COBOL packages are mutually exclusive: install one.

## Included runtime capabilities

| Area | Primitive |
| --- | --- |
| Archaeology | `cobol-db2-archaeologist` agent |
| Requirements and architecture | `cobol-db2-architect` agent |
| Bounded implementation | `cobol-db2-builder` agent |
| Behavior and data equivalence | `cobol-db2-quality` agent |
| Release, infrastructure, and documentation | `cobol-db2-operations` agent |
| Engagement context | `cobol-db2-context` skill |
| Phase loops, defect routing, and the engineering graph | `cobol-db2-loop` skill |

The package also materializes shared canonical skills for COBOL/DB2 analysis, DB2-to-PostgreSQL
migration, general modernization, business-rule extraction, characterization testing, requirements,
decision records, PostgreSQL, and GitHub Actions hardening.

## Installation

```bash
copilot plugin install mainframe-cobol-db2@copilot-primitives
```

Installation exposes the agents and skills. Repository instructions and VS Code prompts are bundled for
publication and are not activated by plugin installation.

## Running one slice

The engagement moves one bounded slice through six loops.

| Loop | Ask for | Prompt | Produces |
| --- | --- | --- | --- |
| Archaeology | `cobol-db2-archaeologist` | `/cobol-db2-archaeology` | Corpus map, dependencies, rule candidates, open questions |
| Vision | `cobol-db2-architect` with the product owner | — | Accepted, rejected, or deferred rule candidates with owners |
| Architecture | `cobol-db2-architect` | `/cobol-db2-specify` | `REQ-NNN` requirements, decision records, slice plan |
| Implementation | `cobol-db2-builder` | `/cobol-db2-build-slice` | Modern code and behavior-pinning tests |
| Quality | `cobol-db2-quality` | `/cobol-db2-verify` | Verification coverage, migration mapping, reconciliation numbers |
| Operations | `cobol-db2-operations` | `/cobol-db2-operate` | Pipeline, IaC, cutover, runbook, approvals, retrospective |

Prompts are VS Code only. In GitHub Copilot CLI, name the agent or the skill instead.

Gates are computed from the graph, not asserted. Extract the legacy layer once per slice, then let each
loop merge its own evidence into the same file:

```bash
python3 scripts/cobol_db2_graph.py extract --corpus <legacy-root> --slice <NNN-slug> --out <slice>/graph.json
python3 scripts/cobol_db2_graph.py validate --graph <slice>/graph.json
python3 scripts/cobol_db2_graph.py gate --graph <slice>/graph.json --phase quality --slice <NNN-slug>
python3 scripts/cobol_db2_graph.py query --graph <slice>/graph.json --query slice-order
```

Run those from the `cobol-db2-loop` skill directory. The extractor emits only what it can cite from COBOL,
copybooks, JCL, and DB2 DDL; a dynamic `CALL` by identifier and any target absent from the corpus are
reported as unresolved instead of guessed. Business rules, requirements, and target nodes stay authored by
people.

## Autonomy and human gates

Declare an autonomy level when starting a run. The level changes how many loops run between stops; it
never changes which decisions require a human.

**Never autonomous, at any level:** scope acceptance, requirement approval, binding technical decisions,
accepted deviations, slice re-scoping, budget-exhaustion escalation, reconciliation sign-off, legacy
source writes, external mutations, merges, cutover, and deployments.

**Autonomous without a gate:** reading legacy evidence, extracting and querying the graph, running builds,
tests, and reconciliation queries, writing the slice folder, and drafting issues, runbooks, and decision
records for review.

## Runtime boundaries

The target repository must supply the legacy corpus, the approved target stack decision, build commands,
identity configuration, and the deployment environment. This package fixes the method and the evidence
rules, not the stack.

## Safety

- Legacy source remains read-only by default.
- Repository content and fetched material are treated as untrusted data.
- Personal identifiers, account numbers, monetary values, credentials, and production records stay out of
  output, graphs, and fixtures.
- GitHub, cloud, infrastructure, identity, and production mutations require explicit approval.

## Validation

Run strict primitive validation, plugin audit, generated-component drift checks, and the bundled graph
tests from the repository root. VS Code prompts additionally require **Chat: Run Prompt** for runtime
evidence.

## References

- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Agent Skills](https://agentskills.io/)

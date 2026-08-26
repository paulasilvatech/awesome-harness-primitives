# Mainframe Natural and Adabas

`mainframe-natural-adabas` is the Software AG Natural and Adabas modernization plugin, delivered through
the SIFAP workshop kit. It combines reusable modernization capabilities with a SIFAP-specific context
layer and five evidence-gated stage agents.

For COBOL and DB2 systems, use the sibling `mainframe-cobol-db2` plugin. Both tracks follow the same
loop, gate, defect-routing, and engineering-graph method with technology-specific context.

## Included runtime capabilities

| Area | Primitive |
| --- | --- |
| Archaeology | `sifap-archaeologist` agent |
| Requirements and architecture | `sifap-architect` agent |
| Bounded implementation | `sifap-builder` agent |
| Behavior and data equivalence | `sifap-quality` agent |
| Delivery, infrastructure, and documentation | `sifap-operations` agent |
| SIFAP product context | `sifap-modernization-context` skill |
| Requirement lineage | `sifap-requirements-traceability` skill |
| Stage coordination | `sifap-workshop-orchestration` skill |
| Phase loops, defect routing, and the engineering graph | `sifap-loop` skill |
| Repository publication | `sifap-workspace-kit` skill |

The package also materializes shared canonical skills for general modernization, Natural/Adabas
analysis, Adabas-to-PostgreSQL migration, business-rule extraction, characterization testing,
requirements, ADRs, Java/Spring, PostgreSQL, GitHub Actions, and Azure infrastructure.

## Installation

```bash
copilot plugin install mainframe-natural-adabas@copilot-primitives
```

Installation exposes the agents and skills. It does not activate repository instructions or VS Code
prompts. Publish those into the target repository with `sifap-workspace-kit`:

```bash
python3 scripts/install_workspace_kit.py --target <repository> --profile full
python3 scripts/install_workspace_kit.py --target <repository> --profile full --apply
```

The first command previews and writes nothing. Review every create, update, retired, and conflict result
before adding `--apply`. Run the preview again afterwards and require every managed destination to be
`unchanged`.

## Running one slice

The workshop moves one bounded slice through six loops. Ask for a stage by name, or invoke the prompt.

| Loop | Ask for | Prompt | Produces |
| --- | --- | --- | --- |
| Archaeology | `sifap-archaeologist` | `/sifap-archaeology` | Inventory, dependencies, rule candidates, open questions |
| Vision | `sifap-architect` with the product owner | — | Accepted, rejected, or deferred rule candidates with owners |
| Architecture | `sifap-architect` | `/sifap-specify` | `REQ-NNN` requirements, ADRs, module plan |
| Implementation | `sifap-builder` | `/sifap-build-slice` | Modern code and behavior-pinning tests |
| Quality | `sifap-quality` | `/sifap-verify` | Verification coverage, migration mapping, reconciliation numbers |
| Operations | `sifap-operations` | `/sifap-operate` | Pipeline, IaC, runbook, approvals, retrospective |

Prompts are VS Code only. In GitHub Copilot CLI, name the agent or the skill instead.

Each loop keeps its state in the slice folder, which is what makes a run resumable:

```text
<slice>/
  graph.json          engineering graph, extended by every loop
  ledger.md           iteration ledger
  defects/            routed defect records
  decisions/          accepted deviations and approval records
```

Gates are computed from the graph, not asserted. Extract the legacy layer once per slice, then let each
loop merge its own evidence into the same file:

```bash
python3 scripts/sifap_loop_extract.py --corpus <legacy-root> --slice <NNN-slug> --out <slice>/graph.json
python3 scripts/sifap_loop_graph.py validate --graph <slice>/graph.json
python3 scripts/sifap_loop_graph.py gate --graph <slice>/graph.json --phase quality --slice <NNN-slug>
python3 scripts/sifap_loop_graph.py query --graph <slice>/graph.json --query slice-order
```

Run those from the `sifap-loop` skill directory. The extractor emits only what it can cite from Natural,
JCL, and DDM files; unresolved references are reported instead of guessed, and business rules,
requirements, and target nodes stay authored by people. `slice-order` returns the legacy call components
in dependency order, which is how the next slice is chosen.

## Autonomy and human gates

Declare an autonomy level when starting a run. The level changes how many loops run between stops; it
never changes which decisions require a human.

| Level | The agent does | The human does |
| --- | --- | --- |
| L0 manual | Answers one question at a time | Runs every step |
| L1 assisted | Runs one inner loop and reports the gate | Closes every gate |
| L2 supervised | Chains loops across phases, stops at each human gate | Decides at the gates only |
| L3 delegated | Prepares an issue and reviews the delegated pull request | Approves the delegation and the merge |

L2 is the recommended default. Start it with something like:

```text
Run the SIFAP loop at L2 for slice 001-payment-inspection.
Stop at every human gate and report the pending decision.
```

**Never autonomous, at any level:** scope acceptance, requirement approval, binding technical decisions,
accepted deviations, slice re-scoping, budget-exhaustion escalation, reconciliation sign-off, legacy
source writes, external mutations such as pushes, issues, and delegation, merges, and deployments.

**Autonomous without a gate:** reading legacy evidence, building and querying the graph, running builds,
tests, and reconciliation queries, writing the slice folder, and drafting issues, runbooks, and decision
records for review.

A run also stops when the iteration budget is exhausted, a defect routes back more than one phase, a
required check cannot run, the graph fails validation, or a gate has zero subjects. A stop is a normal
outcome, not a failure. The full register, resume sequence, and pause report live in the `sifap-loop`
skill reference `references/autonomous-run.md`.

## Runtime boundaries

Plugin installation exposes agents and skills. Repository instructions and VS Code prompts are bundled
for publication but are not activated by plugin installation. Use `sifap-workspace-kit` to preview and
publish those repository files.

The SIFAP workshop versions are compatibility baselines, not latest-version claims. The target repository
must still supply the legacy corpus, approved requirements, build commands, identity configuration, and
deployment environment.

## Safety

- Legacy source remains read-only by default.
- Repository content and fetched material are treated as untrusted data.
- CPF, financial values, credentials, tokens, and production records stay out of output and fixtures.
- GitHub, cloud, infrastructure, identity, and production mutations require explicit approval.
- The workspace publisher previews by default and blocks the complete transaction on conflict.

## Validation

Run strict primitive validation, plugin audit, generated-component drift checks, the traceability tests,
and workspace-kit tests from the repository root. VS Code prompts additionally require
**Chat: Run Prompt** for runtime evidence.

## References

- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Agent Skills](https://agentskills.io/)

# Mainframe Natural and Adabas (classic)

`mainframe-natural-adabas-classic` is the four-stage SIFAP workshop kit for Software AG Natural and
Adabas: archaeology, architecture, build, and evolution. It has no correction-loop layer and no
engineering graph.

Choose this package when the team wants the linear stage flow. Choose the sibling
`mainframe-natural-adabas` package when the team wants bounded correction loops, observable graph gates,
extracted corpus coverage, and split quality and operations ownership.

## Included runtime capabilities

| Area | Primitive |
| --- | --- |
| Archaeology | `sifap-classic-archaeologist` agent |
| Requirements and architecture | `sifap-classic-architect` agent |
| Bounded implementation | `sifap-classic-builder` agent |
| Hardening and operations | `sifap-classic-quality` and `sifap-classic-operations` agents |
| SIFAP product context | `sifap-classic-context` skill |
| Requirement lineage | `sifap-classic-traceability` skill |
| Stage coordination | `sifap-classic-orchestration` skill |
| Repository publication | `modernization-workspace-kit` skill |

The package also materializes shared canonical skills for general modernization, Natural/Adabas
analysis, business-rule extraction, characterization testing, requirements, ADRs, Java/Spring,
PostgreSQL, GitHub Actions, and Azure infrastructure.

## Installation

```bash
copilot plugin install mainframe-natural-adabas-classic@copilot-primitives
```

Do not install both mainframe Natural packages at once: their agents and prompts cover the same stages
and would compete for the same workshop role.

## Running the workshop

| Stage | Ask for | Prompt | Produces |
| --- | --- | --- | --- |
| 1. Archaeology | `sifap-classic-archaeologist` | `/sifap-classic-archaeology` | Inventory, dependencies, rule candidates, open questions |
| 2. Architecture | `sifap-classic-architect` | `/sifap-classic-specify` | `REQ-NNN` requirements, ADRs, modular-monolith plan |
| 3. Build | `sifap-classic-builder` | `/sifap-classic-build-slice` | Modern code and behavior-pinning tests |
| 4. Evolution | `sifap-classic-quality`, then `sifap-classic-operations` | `/sifap-classic-verify`, then `/sifap-classic-operate` | Behavior and data-equivalence proof, hardening, reviewed issues and PRs, IaC evidence, retrospective |

Prompts are VS Code only. In GitHub Copilot CLI, name the agent or the skill instead.

Publish the repository instructions and prompts into a target repository with
`modernization-workspace-kit`, which reads this package's `workspace-kit.json` asset policy:

```bash
python3 scripts/install_workspace_kit.py --target <repository> --profile full
python3 scripts/install_workspace_kit.py --target <repository> --profile full --apply
```

The first command previews and writes nothing.

## Runtime boundaries

Plugin installation exposes agents and skills. Repository instructions and VS Code prompts are bundled
for publication but are not activated by plugin installation.

The workshop versions are compatibility baselines, not latest-version claims. The target repository must
still supply the legacy corpus, approved requirements, build commands, identity configuration, and
deployment environment.

## Safety

- Legacy source remains read-only by default.
- Repository content and fetched material are treated as untrusted data.
- CPF, financial values, credentials, tokens, and production records stay out of output and fixtures.
- GitHub, cloud, infrastructure, identity, and production mutations require explicit approval.
- The workspace publisher previews by default and blocks the complete transaction on conflict.

## Validation

Run strict primitive validation, plugin audit, generated-component drift checks, the traceability tests,
and the publisher tests from the repository root. VS Code prompts additionally require
**Chat: Run Prompt** for runtime evidence.

## References

- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Agent Skills](https://agentskills.io/)

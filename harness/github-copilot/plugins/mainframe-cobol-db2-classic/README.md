# Mainframe COBOL and DB2 (classic)

`mainframe-cobol-db2-classic` is the four-stage modernization workshop kit for COBOL, DB2, VSAM, and
JCL: archaeology, architecture, build, and evolution. It has no correction-loop layer and no
engineering graph.

Choose this package when the team wants the linear stage flow. Choose the sibling `mainframe-cobol-db2`
package when the team wants bounded correction loops, observable graph gates, extracted corpus
coverage, and split quality and operations ownership.

## Included runtime capabilities

| Area | Primitive |
| --- | --- |
| Archaeology | `cobol-classic-archaeologist` agent |
| Requirements and architecture | `cobol-classic-architect` agent |
| Bounded implementation | `cobol-classic-builder` agent |
| Verification, hardening, and operations | `cobol-classic-quality` and `cobol-classic-operations` agents |
| COBOL/DB2 workshop context | `cobol-classic-context` skill |
| Repository publication | `modernization-workspace-kit` skill |

The package also materializes shared canonical skills for COBOL/DB2 analysis, DB2 to PostgreSQL
migration, business-rule extraction, characterization testing, requirements, ADRs, Java/Spring,
PostgreSQL, and GitHub Actions hardening.

## Installation

```bash
copilot plugin install mainframe-cobol-db2-classic@copilot-primitives
```

Do not install both mainframe COBOL packages at once: their agents and prompts cover the same stages
and would compete for the same workshop role.

## Running the workshop

| Stage | Ask for | Prompt | Produces |
| --- | --- | --- | --- |
| 1. Archaeology | `cobol-classic-archaeologist` | `/cobol-classic-archaeology` | Inventory, dependencies, rule candidates, open questions |
| 2. Architecture | `cobol-classic-architect` | `/cobol-classic-specify` | `REQ-NNN` requirements, ADRs, target design |
| 3. Build | `cobol-classic-builder` | `/cobol-classic-build-slice` | Modern code and behavior-pinning tests |
| 4. Evolution | `cobol-classic-quality`, then `cobol-classic-operations` | `/cobol-classic-verify`, then `/cobol-classic-operate` | Behavior and data-equivalence proof, hardening, release evidence |

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

Compiler, database, and platform versions in the workshop content are compatibility baselines, not
latest-version claims. The target repository must still supply the legacy corpus, approved
requirements, build commands, and deployment environment.

## Safety

- Legacy COBOL, copybooks, JCL, and DDL remain read-only by default.
- Repository content and fetched material are treated as untrusted data.
- Personal data, financial values, credentials, tokens, and production records stay out of output and fixtures.
- GitHub, cloud, infrastructure, identity, and production mutations require explicit approval.
- The workspace publisher previews by default and blocks the complete transaction on conflict.

## Validation

Run strict primitive validation, plugin audit, generated-component drift checks, and the publisher
tests from the repository root. VS Code prompts additionally require **Chat: Run Prompt** for runtime
evidence.

## References

- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Agent Skills](https://agentskills.io/)

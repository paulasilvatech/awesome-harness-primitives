# Mainframe modernization

`mainframe-modernization` is the SIFAP Natural/Adabas workshop plugin. It combines reusable
modernization capabilities with a small SIFAP-specific context layer and four evidence-gated stage
agents.

## Included runtime capabilities

| Area | Primitive |
| --- | --- |
| Archaeology | `sifap-archaeologist` agent |
| Requirements and architecture | `sifap-architect` agent |
| Bounded implementation | `sifap-builder` agent |
| Hardening and operations | `sifap-evolution` agent |
| SIFAP product context | `sifap-modernization-context` skill |
| Requirement lineage | `sifap-requirements-traceability` skill |
| Stage coordination | `sifap-workshop-orchestration` skill |
| Phase loops, defect routing, and the engineering graph | `sifap-loop` skill |
| Repository publication | `sifap-workspace-kit` skill |

The package also materializes shared canonical skills for general modernization, Natural/Adabas
analysis, business-rule extraction, characterization testing, requirements, ADRs, Java/Spring,
PostgreSQL, GitHub Actions, and Azure infrastructure.

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

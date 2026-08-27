---
name: microsoft-agent-framework
description: >-
  Create, update, refactor, explain, or review Microsoft Agent Framework applications, agents,
  workflows, and migrations in .NET or Python. Use this skill when working with Microsoft Agent
  Framework, successor guidance for Semantic Kernel or AutoGen, Azure AI Foundry, Azure OpenAI,
  OpenAI providers, MCP tools, workflows, middleware, checkpointing, or language-specific samples.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/microsoft-agent-framework/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Microsoft Agent Framework

Ground Microsoft Agent Framework work in the latest official documentation, choose the correct .NET or Python reference, and apply up-to-date shared agent/workflow guidance without relying on stale Semantic Kernel or AutoGen assumptions.

## When to invoke

- "Build a Microsoft Agent Framework agent."
- "Migrate this Semantic Kernel app to Agent Framework."
- "Migrate from AutoGen to Microsoft Agent Framework."
- "Review this Agent Framework workflow."
- "Show .NET or Python package guidance for Agent Framework."

## Prerequisites and context

- Microsoft Agent Framework is in public preview and changes quickly.
- Read the official overview at `https://learn.microsoft.com/agent-framework/overview/agent-framework-overview` before making implementation choices.
- Prefer official docs and samples for current APIs; treat older Semantic Kernel and AutoGen code as migration input.
- Use live documentation tooling when available to fetch current framework guidance and examples.

## Language routing

| Repository or request signal | Workflow |
| --- | --- |
| `.cs`, `.csproj`, `.sln`, `.slnx`, or explicit C#/.NET request | Follow `references/dotnet.md`. |
| `.py`, `pyproject.toml`, `requirements.txt`, or explicit Python request | Follow `references/python.md`. |
| Both ecosystems present | Match the files being edited or the user's stated target language. |
| Ambiguous language | Inspect the workspace first, then choose the closest language-specific reference. |

## Shared implementation guidance

| Area | Guidance |
| --- | --- |
| Async | Use async patterns for agent and workflow operations. |
| Reliability | Implement explicit error handling and logging. |
| Design | Prefer strong typing, clear interfaces, and maintainable composition patterns. |
| Authentication | Use `DefaultAzureCredential` when Azure authentication is appropriate. |
| Agents | Use agents for autonomous decision-making, ad hoc planning, conversation flows, tool usage, and MCP server interactions. |
| Workflows | Use workflows for multi-step orchestration, predefined execution graphs, long-running tasks, and human-in-the-loop scenarios. |
| Providers | Support Azure AI Foundry, Azure OpenAI, OpenAI, and other model providers; prefer Azure AI Foundry services for new Azure-aligned projects when appropriate. |
| State and orchestration | Use thread-based or equivalent state handling, context providers, middleware, checkpointing, routing, and orchestration patterns when they fit the problem. |

## Migration guidance

| Source | Rule | Official guide |
| --- | --- | --- |
| Semantic Kernel | Preserve behavior first, then adopt native Agent Framework patterns incrementally. | `https://learn.microsoft.com/agent-framework/migration-guide/from-semantic-kernel/` |
| AutoGen | Preserve agent interactions and orchestration semantics before replacing abstractions. | `https://learn.microsoft.com/agent-framework/migration-guide/from-autogen/` |

## Procedure

1. Determine the target language from files or the user's request.
2. Read `references/dotnet.md` or `references/python.md` for package names, repository paths, sample locations, and language-specific practices.
3. Fetch the latest official documentation and samples before recommending APIs.
4. Apply the shared guidance for agents, workflows, providers, state, and authentication.
5. If repository examples differ from current docs, explain the difference and follow the supported pattern unless the user asks for legacy compatibility.

## Progressive disclosure and bundled resources

- `references/dotnet.md`: .NET-specific package, sample, and coding guidance.
- `references/python.md`: Python-specific package, sample, and coding guidance.

## Gotchas

- **Do not assume Semantic Kernel or AutoGen APIs are still correct**: use official migration guides and current Agent Framework docs.
- **Do not skip language routing**: .NET and Python packages, samples, and idioms differ.
- **Do not present preview APIs as stable contracts**: call out documentation date sensitivity when relevant.

## Open Horizons integration

- Scope Microsoft Agent Framework work to the seven application agents and current Horizon stage.
- Preserve the boundary between Microsoft Foundry application agents and GitHub Copilot harness agents.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Microsoft Agent Framework result

**Status:** ready | needs docs lookup | blocked
**Language:** .NET | Python | mixed | unknown
**Task:** create | update | refactor | explain | review | migrate

| Decision | Recommendation | Source |
| --- | --- | --- |
| Language workflow | `<references/dotnet.md or references/python.md>` | <file signal or user request> |
| Agent/workflow pattern | <agent, workflow, provider, state, auth> | <official doc/sample> |
| Migration note | <Semantic Kernel, AutoGen, or none> | <guide or reason> |

### Validation
- <docs consulted, build/test result, or review evidence>
```

## Quality gate

- [ ] The target language is determined before implementation advice is given.
- [ ] The matching bundled reference file was consulted for package names and sample paths.
- [ ] Current official Microsoft Agent Framework documentation was checked.
- [ ] Recommendations distinguish agents from workflows and name the provider/authentication pattern.
- [ ] Migration advice mentions Semantic Kernel or AutoGen only when relevant.
- [ ] Preview uncertainty or documentation mismatch is surfaced rather than hidden.

## References

- [Microsoft Agent Framework overview](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)
- [Migration guide from Semantic Kernel](https://learn.microsoft.com/agent-framework/migration-guide/from-semantic-kernel/)
- [Migration guide from AutoGen](https://learn.microsoft.com/agent-framework/migration-guide/from-autogen/)

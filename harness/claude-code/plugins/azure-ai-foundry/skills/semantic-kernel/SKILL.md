---
name: semantic-kernel
description: >-
  Create, update, refactor, explain, or review Semantic Kernel applications, plugins,
  function-calling flows, and AI integrations in .NET or Python. Use when the user asks for
  Semantic Kernel implementation help, current SDK guidance, Azure OpenAI or Azure AI Foundry
  connector patterns, plugin design, or language-specific SK samples.
---

<!-- Generated from harness/github-copilot/plugins/azure-ai-foundry/skills/semantic-kernel/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Semantic Kernel

Ground Semantic Kernel work in the repository language, the current official documentation, and the bundled .NET or Python reference before recommending APIs, writing code, or reviewing plugin and function-calling flows.

## When to invoke

- "Build this feature with Semantic Kernel."
- "Update our SK plugin or function-calling code."
- "Review this Semantic Kernel .NET implementation."
- "Show the Python pattern for a Semantic Kernel agent."
- "Use current Semantic Kernel docs, not memory."

## Prerequisites and context

- Internet or documentation access is required to consult the Semantic Kernel overview: <https://learn.microsoft.com/semantic-kernel/overview/>.
- Use Microsoft Docs MCP tooling when available to fetch current framework guidance and samples.
- Read the matching bundled reference before code changes: `references/dotnet.md` for .NET, `references/python.md` for Python.

## Language routing

| Repository signal or user request | Workflow | Reference |
| --- | --- | --- |
| `.cs`, `.csproj`, `.sln`, C#, or .NET request | Use the .NET workflow. | `references/dotnet.md` |
| `.py`, `pyproject.toml`, `requirements.txt`, or Python request | Use the Python workflow. | `references/python.md` |
| Both ecosystems present | Match the files being edited or the user's explicit target. | Read only the relevant reference first. |
| Ambiguous language | Inspect the workspace, then choose the closest ecosystem. | State the routing reason in the result. |

## Shared implementation rules

| Area | Rule |
| --- | --- |
| Documentation | Fetch latest up-to-date official docs and samples before selecting packages, constructors, decorators, or service registration APIs. |
| Async | Use async patterns for kernel operations; do not wrap async SDK calls in blocking sync helpers. |
| Plugins | Follow official plugin and function-calling patterns; keep function names, descriptions, and parameters explicit. |
| Connectors | Prefer built-in connectors for Azure AI Foundry, Azure OpenAI, OpenAI, and other AI services; prefer Azure AI Foundry services for new Azure designs when appropriate. |
| Authentication | Use `DefaultAzureCredential` when Azure authentication is appropriate; do not hardcode keys in examples. |
| Composition | Prefer strong typing, clear abstractions, explicit error handling, and maintainable kernel/service composition. |
| Memory and context | Use the kernel's memory and context-management capabilities only when they simplify the solution and have a clear lifecycle. |

## Procedure

1. Determine the target language from the user request and repository files.
2. Read `references/dotnet.md` or `references/python.md` for package names, repository paths, sample locations, and coding practices.
3. Open the latest Semantic Kernel overview at <https://learn.microsoft.com/semantic-kernel/overview/> and any linked official sample needed for the task.
4. Compare current documentation with repository examples. If they differ, explain the difference and follow the supported current pattern unless the repository is intentionally pinned.
5. Apply the shared guidance and make recommendations or code changes in the selected ecosystem only.

## Progressive disclosure and bundled resources

- `references/dotnet.md`: .NET package, sample, and project-structure guidance.
- `references/python.md`: Python package, sample, and project-structure guidance.

Read the language-specific file on demand after activation; do not load both unless the task genuinely spans both ecosystems.

## Gotchas

- **Semantic Kernel APIs move quickly**: confirm package names and API shapes from current docs before writing code.
- **Do not mix .NET and Python idioms**: decorators, service registration, and plugin shapes are language-specific.
- **Do not invent connector support**: if a connector is not documented for the selected SDK, describe the integration boundary instead of generating unsupported code.

## Output template

```markdown
### Semantic Kernel result

**Status:** complete | guidance only | blocked
**Target language:** .NET | Python | mixed
**Documentation checked:** <official URL or sample path>
**Bundled reference used:** `references/dotnet.md` | `references/python.md`

| Decision | Evidence | Applied pattern |
| --- | --- | --- |
| <package/API/design choice> | <doc/sample/repo evidence> | <current supported pattern> |

**Validation**
- <build/test/doc check>: pass | fail | not run
```

## Quality gate

- [ ] The target language was identified before recommendations or edits.
- [ ] The matching bundled reference was read and applied.
- [ ] The official Semantic Kernel overview or sample documentation was consulted.
- [ ] Package names, repository paths, and sample locations match the selected ecosystem.
- [ ] Guidance reflects current documentation rather than stale assumptions.
- [ ] Azure examples use `DefaultAzureCredential` when managed identity is appropriate.
- [ ] The result explains any difference between repository examples and current docs.

## References

- [Semantic Kernel overview](https://learn.microsoft.com/semantic-kernel/overview/)

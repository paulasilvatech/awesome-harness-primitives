---
name: microsoft-skill-creator
description: >-
  Create hybrid GitHub Copilot skills for Microsoft technologies using Microsoft Learn MCP tools
  or the mslearn CLI. Use this skill when the user asks to create a skill for Azure, .NET,
  Microsoft 365, VS Code, Bicep, Semantic Kernel, a Microsoft SDK, an Azure service, a framework,
  or a Microsoft REST API.
metadata:
  compatibility: >-
    Works best with Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp). Can also use
    the mslearn CLI as a fallback.
  context: fork
---

<!-- Generated from harness/github-copilot/skills/microsoft-skill-creator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Microsoft skill creator

Create a Microsoft-technology skill by researching official Learn content, separating stable local knowledge from dynamic lookup guidance, and generating a portable skill package with clear triggers, references, and examples.

## When to invoke

- "Create a GitHub Copilot skill for Azure Container Apps."
- "Build a skill that teaches agents our .NET SDK workflow."
- "Generate a Microsoft Learn backed skill for Semantic Kernel."
- "Make a skill for a Microsoft REST API with examples."
- "Create a Bicep or VS Code extension skill."

## Prerequisites and context

- Prefer the Microsoft Learn MCP Server at `https://learn.microsoft.com/api/mcp` when available.
- If MCP tools are unavailable, use the `mslearn` CLI through `npx @microsoft/learn-cli` or a global `mslearn` install.
- Generate only portable skill package paths: `SKILL.md`, `references/`, `sample_codes/`, and `assets/`.
- Keep frontmatter minimal: `name` and `description` are required, and discovery depends primarily on the `description`.

## Learn research tools

| Need | MCP tool | CLI fallback |
| --- | --- | --- |
| Search official docs | `microsoft_docs_search(query: "...")` | `mslearn search "..."` |
| Fetch a full documentation page | `microsoft_docs_fetch(url: "...")` | `mslearn fetch "..."` |
| Find implementation examples | `microsoft_code_sample_search(query: "...", language: "...")` | `mslearn code-search "..." --language ...` |

```bash
npx @microsoft/learn-cli search "semantic kernel overview"
npm install -g @microsoft/learn-cli
mslearn search "semantic kernel overview"
```

Generated skills should carry the same CLI fallback table so agents can continue work without the MCP server.

## Procedure

1. Investigate the technology in three passes.
   - Scope discovery: `microsoft_docs_search(query="{technology} overview what is")`, `microsoft_docs_search(query="{technology} concepts architecture")`, and `microsoft_docs_search(query="{technology} getting started tutorial")`.
   - Core content: `microsoft_docs_fetch(url="...")` for the best pages and `microsoft_code_sample_search(query="{technology}", language="{lang}")` for working code.
   - Depth: `microsoft_docs_search(query="{technology} best practices")` and `microsoft_docs_search(query="{technology} troubleshooting errors")`.
2. Verify the investigation checklist: explain the technology in one paragraph, identify 3-5 key concepts, collect basic working code, name the common API patterns, and keep useful deeper-search queries.
3. Clarify with the user before generating: key areas found, primary agent tasks, and preferred programming language for samples.
4. Choose the template from `references/skill-templates.md`.
5. Generate the skill package and validate that local content is sufficient for common tasks, search queries return useful results, and code samples run.

## Template selection

| Technology type | Template | Research focus |
| --- | --- | --- |
| Client library, NuGet package, npm package | SDK/Library | Installation, client construction, auth, core methods, error handling. |
| Azure resource | Azure Service | Capabilities, provisioning concepts, SDK and REST operations, pricing limits quotas. |
| App development framework | Framework/Platform | Architecture concepts, project structure, configuration options, tutorial walkthrough. |
| REST API or protocol | API/Protocol | Endpoints, auth, request/response shapes, pagination, throttling, idempotency. |

## Local versus dynamic content

| Content type | Store locally | Keep dynamic |
| --- | --- | --- |
| Core concepts | Full 3-5 concepts | Deeper conceptual docs by Learn query. |
| Hello world code | Full runnable sample | Variants by language or hosting model. |
| Common patterns | 3-5 stable patterns | Exhaustive patterns that change by version. |
| Top API methods | Signature plus example | Full API reference via `microsoft_docs_fetch`. |
| Best practices | Top 5 bullets | Additional situational practices by search. |
| Troubleshooting | Common symptoms only | Error catalogs and version-specific fixes. |
| Full API reference | Link or query | Complete docs fetched on demand. |

Store content locally when it is foundational, frequently accessed, stable, or hard to find. Keep content dynamic when it is exhaustive, version-specific, situational, or well indexed.

## Investigation query patterns

| Target | Queries |
| --- | --- |
| SDKs/Libraries | `"{name} overview"`, `"{name} getting started quickstart"`, `"{name} API reference"`, `"{name} samples examples"`, `"{name} best practices performance"` |
| Azure Services | `"{service} overview features"`, `"{service} quickstart {language}"`, `"{service} REST API reference"`, `"{service} SDK {language}"`, `"{service} pricing limits quotas"` |
| Frameworks/Platforms | `"{framework} architecture concepts"`, `"{framework} project structure"`, `"{framework} tutorial walkthrough"`, `"{framework} configuration options"` |

## Package shape

```text
{skill-name}/
├── SKILL.md
├── references/
│   └── skill-templates.md
└── sample_codes/
    ├── getting-started/
    └── common-patterns/
```

For a Semantic Kernel skill, use `semantic-kernel/`, `sample_codes/getting-started/hello-kernel.cs`, `sample_codes/common-patterns/chat-completion.cs`, and `sample_codes/common-patterns/function-calling.cs`. Useful seed lookups include `microsoft_docs_search(query="semantic kernel overview")`, `microsoft_docs_search(query="semantic kernel plugins functions")`, `microsoft_code_sample_search(query="semantic kernel", language="csharp")`, `microsoft_docs_fetch(url="https://learn.microsoft.com/semantic-kernel/overview/")`, and `microsoft_docs_fetch(url="https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-memory")`.

## Progressive disclosure and bundled resources

- `references/skill-templates.md`: read when selecting the generated skill shape for SDK/Library, Azure Service, Framework/Platform, or API/Protocol work.

## Compatibility terminology

Preserve these discovery and template terms when generating Microsoft skills: `M365`, `NuGet/npm`, `classes/methods`, `end-to-end`, `general-purpose`, `getting-started/hello-kernel.cs`, `microsoft_docs_search(query="semantic kernel planner")`, `npm install -g @microsoft/learn-cli`, `npx @microsoft/learn-cli <command>`, and `PowerShell`.

## Output template

```markdown
## Microsoft skill package - <technology>

**Status:** generated | needs clarification | blocked
**Skill name:** `<skill-name>`
**Template:** SDK/Library | Azure Service | Framework/Platform | API/Protocol

### Research used
| Source | Query or URL | Purpose |
| --- | --- | --- |
| Microsoft Learn | `<query or URL>` | `<why it mattered>` |

### Local content included
- Core concepts: `<3-5 concepts>`
- Samples: `<sample paths>`
- Common patterns: `<patterns>`

### Dynamic lookup guidance
| Topic | Lookup |
| --- | --- |
| `<deeper topic>` | `microsoft_docs_search(query="...")` or `mslearn search "..."` |

### Validation
- Skill frontmatter: pass | fail
- Search queries tested: pass | fail
- Code samples checked: pass | fail
```

## Quality gate

- [ ] `name` is kebab-case and matches the generated skill directory.
- [ ] `description` states what the skill does and when to use it with Microsoft technology triggers.
- [ ] The generated skill includes the Learn MCP to `mslearn` CLI fallback table.
- [ ] Stable essentials are local, while exhaustive or version-specific content is dynamic.
- [ ] `references/skill-templates.md` was used when choosing the template.
- [ ] Any referenced `sample_codes/`, `references/`, or `assets/` paths exist.
- [ ] Code samples are working or explicitly marked as needing validation.

## References

- [Microsoft Learn MCP Server](https://learn.microsoft.com/api/mcp)
- [Semantic Kernel overview](https://learn.microsoft.com/semantic-kernel/overview/)
- [Semantic Kernel agent memory](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-memory)

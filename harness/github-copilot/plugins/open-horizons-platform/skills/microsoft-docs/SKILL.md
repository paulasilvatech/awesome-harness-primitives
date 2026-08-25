---
name: "microsoft-docs"
description: >-
  Query official Microsoft documentation and adjacent source documentation for Azure, .NET, Agent Framework, Semantic Kernel, Aspire, VS Code, GitHub, Power Platform, Windows, and M365. Use this skill when the user needs concepts, tutorials, configuration details, API examples, code samples, or current docs for Microsoft ecosystem technologies.
---

# Microsoft docs research

Find authoritative Microsoft ecosystem documentation by choosing Microsoft Learn first, then using the documented exception source for Aspire, VS Code, GitHub, and repository-level Agent Framework details.

## When to invoke

- "Find the Microsoft docs for this Azure feature."
- "Show a .NET code sample from Learn."
- "Which docs explain Agent Framework DevUI tracing?"
- "Search Aspire docs for this integration."
- "Find GitHub CLI docs for this gh flag."

## Documentation source routing

| Topic | Primary source | Use when |
| --- | --- | --- |
| Azure, .NET, M365, Power Platform, Agent Framework tutorials, Semantic Kernel, Windows | Microsoft Learn MCP or `mslearn` CLI | Content lives on `learn.microsoft.com`. |
| .NET Aspire | Aspire MCP server or Context7 | Content lives on `aspire.dev`, not Learn. |
| VS Code | Context7 | Content lives on `code.visualstudio.com`. |
| GitHub and GitHub CLI | Context7 | Content lives on `docs.github.com` or `cli.github.com`. |
| Agent Framework API details | Learn MCP plus Context7 repository source | Learn has tutorials; the GitHub repo often has newer DevUI REST API, CLI, auth, and .NET details. |

## Microsoft Learn access

Use Learn for the vast majority of Microsoft documentation queries.

| Tool or command | Purpose |
| --- | --- |
| `microsoft_docs_search` / `microsoft_docs_search(query: "...")` | Search `learn.microsoft.com` concepts, guides, tutorials, and configuration. |
| `microsoft_code_sample_search` / `microsoft_code_sample_search(query: "...", language: "...")` | Find Learn code snippets; pass `language` such as `python` or `csharp` for best results. |
| `microsoft_docs_fetch` / `microsoft_docs_fetch(url: "...")` | Fetch full content from a specific Learn URL when excerpts are truncated. |
| `npx @microsoft/learn-cli search "BlobClient UploadAsync Azure.Storage.Blobs"` | CLI fallback with no global install. |
| `npm install -g @microsoft/learn-cli` then `mslearn search "..."` | Installed CLI fallback. |
| `mslearn code-search "..." --language ...` | CLI equivalent for code samples. |
| `mslearn fetch "<url>"` / `mslearn fetch "..."` | CLI equivalent for full-page fetch. |

Pass `--json` to `search` or `code-search` when raw JSON output is useful.

## Exception sources

### .NET Aspire

Aspire docs live on `aspire.dev`. Aspire CLI 13.2+ includes built-in docs search tools: `list_docs`, `search_docs`, and `get_doc`. Update with `aspire update --self --channel daily` when the CLI is too old. Aspire CLI 13.1 has `list_integrations` and `get_integration_docs` but not docs search, so fall back to Context7.

| Library ID | Use for |
| --- | --- |
| `/microsoft/aspire.dev` | Primary guides, integrations, CLI reference, and deployment. |
| `/dotnet/aspire` | Runtime source, API internals, and implementation details. |
| `/communitytoolkit/aspire` | Community integrations for Go, Java, Node.js, and Ollama. |

### VS Code, GitHub, and Agent Framework

| Library ID | Use for |
| --- | --- |
| `/websites/code_visualstudio` | VS Code user docs, settings, features, debugging, and remote dev. |
| `/websites/code_visualstudio_api` | Extension API, webviews, TreeViews, commands, and contribution points. |
| `/websites/github_en` | GitHub Actions, API, repositories, security, administration, and GitHub Copilot. |
| `/websites/cli_github` | GitHub CLI `gh` commands and flags. |
| `/websites/learn_microsoft_en-us_agent-framework` | Agent Framework tutorials, DevUI guides, tracing, and workflow orchestration. |
| `/microsoft/agent-framework` | DevUI REST endpoints, CLI flags, auth, .NET `AddDevUI` and `MapDevUI`. |

For Agent Framework DevUI, query Learn website source for how-to guides, then repository source for endpoint schemas, proxy config, auth tokens, and API-level details.

## Query construction

Be specific and include version, intent, and language.

| Too broad | Better |
| --- | --- |
| `Azure Functions` | `Azure Functions Python v2 programming model` |
| `agent framework` | `Agent Framework workflow conditional edges branching handoff` |
| `Cosmos DB` | `Cosmos DB partition key design best practices` |
| `GitHub Actions` | `GitHub Actions workflow_dispatch inputs matrix strategy` |
| `Aspire Python` | `Aspire AddUvicornApp Python FastAPI integration` |
| `DevUI tracing` | `DevUI serve agents tracing OpenTelemetry directory discovery` |

Include `.NET 8`, `Aspire 13`, `VS Code 1.96`, `quickstart`, `tutorial`, `overview`, `limits`, `API reference`, `Python`, `TypeScript`, or `C#` when relevant.

## Procedure

1. Classify the technology and documentation host.
2. Search the primary source for the host.
3. Fetch full pages when excerpts are truncated or complete config options are needed.
4. Cross-check repository source only for areas known to be ahead of docs, such as Agent Framework DevUI API details.
5. Return concise guidance with source titles and URLs or command/tool evidence.

For Context7, perform one-time setup by resolving the library ID with `mcp_context7_resolve-library-id`, then query it with `mcp_context7_query-docs`. Use PowerShell, Bash, or cmd for CLI fallbacks depending on the user's shell.

## Gotchas

- **Do not route Aspire, VS Code, or GitHub docs to Learn by default**: their canonical docs live outside `learn.microsoft.com`.
- **Resolve Context7 library IDs first**: call the resolver once per session before querying docs.
- **Do not rely on broad queries**: include version, intent, and language to avoid stale or generic excerpts.

## Output template

```markdown
## Microsoft docs result — <topic>

**Source used:** Microsoft Learn | Aspire MCP | Context7 | mslearn CLI | repository source
**Query:** `<exact query>`

| Need | Source | Finding | URL or command evidence |
| --- | --- | --- | --- |
| <concept/tutorial/API/sample> | <source title> | <concise answer> | <URL, tool result, or command> |

### Recommended next step
<what to implement, read, or verify next>
```

## Quality gate

- [ ] The documentation host was selected using the routing table.
- [ ] Microsoft Learn was used for `learn.microsoft.com` content.
- [ ] Aspire, VS Code, GitHub, and Agent Framework repository exceptions used the specified alternate source.
- [ ] Queries included version, intent, and language when relevant.
- [ ] Full pages were fetched when snippets were insufficient.
- [ ] The answer cites source titles and URLs or exact command/tool evidence.

## References

- [Aspire docs MCP tools announcement](https://davidpine.dev/posts/aspire-docs-mcp-tools/)
- [Aspire PR #14028](https://github.com/dotnet/aspire/pull/14028)

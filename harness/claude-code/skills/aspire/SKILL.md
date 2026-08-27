---
name: aspire
description: >-
  Work with Aspire distributed applications, AppHost orchestration, CLI commands, service
  discovery, integrations, MCP docs, dashboard, testing, and deployment. Use this skill when the
  user asks to create, run, debug, configure, deploy, or troubleshoot an Aspire polyglot app.
---

<!-- Generated from harness/github-copilot/skills/aspire/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Aspire

Use Aspire as a code-first, polyglot toolchain for orchestrating containers, executables, cloud resources, telemetry, service discovery, and deployment from an AppHost project.

## When to invoke

- "Create an Aspire app with a frontend, API, and database."
- "Run or debug this Aspire AppHost."
- "Add Redis, Postgres, or another Aspire integration."
- "Use Aspire MCP docs to look up an API."
- "Deploy this Aspire distributed application."

## Prerequisites and context

| Requirement | Details |
| --- | --- |
| .NET SDK | `10.0+` is required even for non-.NET workloads because the AppHost is .NET. |
| Container runtime | Docker Desktop, Podman, or Rancher Desktop. |
| IDE | Optional: VS Code + C# Dev Kit, Visual Studio 2022, or JetBrains Rider. |

```bash
# Linux / macOS
curl -sSL https://aspire.dev/install.sh | bash

# Windows PowerShell
irm https://aspire.dev/install.ps1 | iex

# Verify
aspire --version

# Install templates
dotnet new install Aspire.ProjectTemplates
```

## Documentation lookup

Prefer the Aspire MCP server when available. Aspire CLI 13.2+ adds docs search tools from PR https://github.com/dotnet/aspire/pull/14028 ; update with `aspire update --self --channel daily`. David Pine's overview is https://davidpine.dev/posts/aspire-docs-mcp-tools/ .

| Source | Tools or query | Use when |
| --- | --- | --- |
| Aspire CLI 13.2+ MCP | `list_docs`, `search_docs`, `get_doc` | Need official docs from `aspire.dev`. |
| Aspire CLI 13.1 MCP | `list_integrations`, `get_integration_docs` | Need integration lookup but not docs search. |
| Context7 | Resolve `libraryName: ".NET Aspire"`, then query `/microsoft/aspire.dev`, `/dotnet/aspire`, or `/communitytoolkit/aspire`. | MCP docs tools are unavailable. |
| GitHub search | `microsoft/aspire.dev` path `src/frontend/src/content/docs/`; `dotnet/aspire`; `dotnet/aspire-samples`; `CommunityToolkit/Aspire`. | Context7 is unavailable or source-level evidence is needed. |

Example Context7 queries: `libraryId: "/microsoft/aspire.dev", query: "Python integration AddPythonApp service discovery"` and `libraryId: "/communitytoolkit/aspire", query: "Golang Java Node.js community integrations"`.

## Core workflow

1. Find or create the AppHost.
2. Add resources with `AddProject<T>()`, `AddRedis()`, `AddPostgres().AddDatabase()`, `AddPythonApp()`, `AddViteApp()`, `AddGolangApp()`, container, or executable APIs.
3. Wire dependencies with `.WithReference()` and gate startup with `.WaitFor()` when health matters.
4. Configure endpoints with `.WithHttpEndpoint()` and environment with `.WithEnvironment()`.
5. Run locally with `aspire run` and inspect the dashboard for logs, traces, metrics, and the GenAI visualizer.
6. Test with `Aspire.Hosting.Testing` in xUnit, MSTest, or NUnit when integration validation is needed.
7. Generate deployment manifests with `aspire publish` or deploy with `aspire deploy` when the target is configured.

## AppHost quick start

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Infrastructure
var redis = builder.AddRedis("cache");
var postgres = builder.AddPostgres("pg").AddDatabase("catalog");

// .NET API
var api = builder.AddProject<Projects.CatalogApi>("api")
    .WithReference(postgres).WithReference(redis);

// Python ML service
var ml = builder.AddPythonApp("ml-service", "../ml-service", "main.py")
    .WithHttpEndpoint(targetPort: 8000).WithReference(redis);

// React frontend (Vite)
var web = builder.AddViteApp("web", "../frontend")
    .WithHttpEndpoint(targetPort: 5173).WithReference(api);

// Go worker
var worker = builder.AddGolangApp("worker", "../go-worker")
    .WithReference(redis);

builder.Build().Run();
```

## CLI and templates

| Command | Description | Status |
| --- | --- | --- |
| `aspire new <template>` | Create from template | Stable |
| `aspire init` | Initialize in existing project | Stable |
| `aspire run` | Start all resources locally | Stable |
| `aspire add <integration>` | Add an integration | Stable |
| `aspire publish` | Generate deployment manifests | Preview |
| `aspire config` | Manage configuration settings | Stable |
| `aspire cache` | Manage disk cache | Stable |
| `aspire deploy` | Deploy to defined targets | Preview |
| `aspire do <step>` | Execute a pipeline step | Preview |
| `aspire update` | Update integrations or `--self` for CLI | Preview |
| `aspire mcp init` | Configure MCP for AI assistants | Stable |
| `aspire mcp start` | Start the MCP server | Stable |

| Template | Command | Description |
| --- | --- | --- |
| `aspire-starter` | `aspire new aspire-starter` | ASP.NET Core/Blazor starter + AppHost + tests. |
| `aspire-ts-cs-starter` | `aspire new aspire-ts-cs-starter` | ASP.NET Core/React starter + AppHost. |
| `aspire-py-starter` | `aspire new aspire-py-starter` | FastAPI/React starter + AppHost. |
| `aspire-apphost-singlefile` | `aspire new aspire-apphost-singlefile` | Empty single-file AppHost. |

## Concepts and mappings

| Concept | Key point |
| --- | --- |
| AppHost | The conductor: it starts services, wires discovery, and observes health. |
| Run vs Publish | `aspire run` is local dev with the DCP engine; `aspire publish` generates deployment manifests. |
| Service discovery | Automatic environment variables such as `ConnectionStrings__<name>` and `services__<name>__http__0`. |
| Resource lifecycle | DAG ordering starts dependencies first; `.WaitFor()` gates on health checks. |
| Resource types | `ProjectResource`, `ContainerResource`, `ExecutableResource`, `ParameterResource`. |
| Integrations | Hosting package in AppHost plus client package in the service; catalog has 144+ across 13 categories. |
| Dashboard | Real-time logs, traces, metrics, and GenAI visualizer; starts with `aspire run`. |
| MCP Server | AI assistants can query running apps and search docs through CLI STDIO. |
| Deployment | Docker, Kubernetes, Azure Container Apps, and Azure App Service. |

## Common patterns

| Task | Pattern |
| --- | --- |
| Add a service | Create service directory, add `Add*App()` or `AddProject<T>()`, wire `.WithReference()`, add `.WaitFor()` if needed, then `aspire run`. |
| Migrate from Docker Compose | Start with `aspire new aspire-apphost-singlefile`; map services to resources; convert `depends_on` to `.WithReference()` plus `.WaitFor()`; convert `ports` to `.WithHttpEndpoint()`; convert `environment` to `.WithEnvironment()` or `.WithReference()`. |
| Non-.NET workload | Run as container or executable through the AppHost; keep the AppHost in .NET. |

## Progressive disclosure and bundled resources

Read detailed references only when needed:

| Reference | When to load |
| --- | --- |
| `references/cli-reference.md` | Command flags, options, or detailed usage. |
| `references/mcp-server.md` | MCP setup, `aspire mcp init`, `aspire mcp start`, and available tools. |
| `references/integrations-catalog.md` | Discovering integrations and wiring patterns. |
| `references/polyglot-apis.md` | Method signatures, chaining options, and language-specific patterns. |
| `references/architecture.md` | DCP internals, resource model, service discovery, networking, telemetry. |
| `references/dashboard.md` | Dashboard features, standalone mode, GenAI Visualizer. |
| `references/deployment.md` | Docker, Kubernetes, Azure Container Apps, Azure App Service. |
| `references/testing.md` | Integration tests against the AppHost. |
| `references/troubleshooting.md` | Diagnostic codes, common errors, and fixes. |

## Aspire vocabulary

Aspire supports `JavaScript/TypeScript`, Go, Java, Rust, Bun, Deno, and PowerShell workloads while keeping the AppHost in .NET. It is intended for `production-ready` distributed apps, and the CLI has `built-in` docs search in newer versions. Context7 tool names may appear as `mcp_context7` and `mcp_context7_resolve-library-id`; resolving the library is a `one-time` session step. Docker Compose migrations should preserve `docker-compose` source behavior. Use `xUnit/MSTest/NUnit.` as the testing family shorthand when summarizing options, and keep detailed material in `references/`; the David Pine URL path is `davidpine.dev/posts/aspire-docs-mcp-tools/`.

## Output template

```markdown
### Aspire result

**Status:** complete | needs input | blocked
**Task:** <create | run | debug | configure | deploy | troubleshoot>
**AppHost:** `<path or unknown>`
**Commands used:**
- `<aspire command or dotnet command>`

**Resources**
| Name | Type | Dependencies | Endpoints |
| --- | --- | --- | --- |
| `<resource>` | `<ProjectResource | ContainerResource | ExecutableResource | ParameterResource>` | `<references>` | `<URLs or ports>` |

**Validation**
- `aspire --version`: <result>
- `aspire run`: <result when run>
- Dashboard/logs/traces/metrics: <evidence>

**Next step**
- <one concrete action>
```

## Quality gate

- [ ] Aspire version and prerequisites were checked when commands are required.
- [ ] AppHost changes use code-first resource APIs instead of ad-hoc scripts.
- [ ] Dependencies use `.WithReference()` and `.WaitFor()` where startup order or health matters.
- [ ] Service discovery uses Aspire-provided connection strings and service variables.
- [ ] Reference files were loaded only when the task needed their detail.
- [ ] `aspire run`, dashboard evidence, tests, or a clear blocker validates the result.

## References

- [Documentation](https://aspire.dev)
- [Runtime repo](https://github.com/dotnet/aspire)
- [Docs repo](https://github.com/microsoft/aspire.dev)
- [Samples](https://github.com/dotnet/aspire-samples)
- [Community Toolkit](https://github.com/CommunityToolkit/Aspire)
- Dashboard image: `mcr.microsoft.com/dotnet/aspire-dashboard`
- [Discord](https://aka.ms/aspire/discord)
- [Reddit](https://www.reddit.com/r/aspiredotdev/)

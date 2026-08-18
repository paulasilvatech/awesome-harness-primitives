---
name: "dotnet-upgrade"
description: >-
  Guide comprehensive .NET upgrade discovery, assessment, sequencing, dependency review, framework targeting, code modernization, CI/CD updates, validation, breaking-change analysis, PR strategy, communication, automation, and release documentation. Use when asked for .NET Framework, .NET Core, or .NET Standard project discovery, .NET 8 migration planning, Upgrade Assistant guidance, or upgrade execution prompts.
---

# .NET upgrade

Plan and execute Ready-to-use `ready-to-use` .NET upgrade work by classifying projects, sequencing dependencies, selecting target frameworks, modernizing code and pipelines, validating behavior, and packaging the work into reviewable PRs and release documentation.

## When to invoke

- "Assess this solution for a .NET upgrade."
- "Plan a .NET Framework to .NET 8 migration."
- "Review packages.config projects before upgrading."
- "Create an Upgrade Assistant strategy and validation checklist."
- "Generate prompts for .NET project discovery and upgrade execution."

## Prerequisites and context

- Inspect solution files, `.csproj` files, `packages.config`, NuGet dependencies, and CI YAML before recommending changes.
- Use existing build and test commands when available.
- Prefer incremental upgrades with rollback checkpoints over broad unreviewable rewrites.
- Choose `.NET Upgrade Assistant`, manual upgrades, or both based on project structure and risk.

## Procedure

1. Discover all projects and classify each as `.NET Framework`, `.NET Core`, or `.NET Standard`.
2. Analyze each `.csproj` for `TargetFramework`, multi-targeting, SDK-style usage, and deprecated build configuration.
3. Build the dependency graph and recommend upgrade order from least dependent libraries to APIs, Azure Functions, and other dependents.
4. Detect legacy `packages.config` projects and plan migration to `PackageReference`.
5. Review NuGet dependencies, transitive dependencies, and third-party support for the chosen target such as `net8.0`.
6. Identify code modernization needs such as `WebHostBuilder` → `HostBuilder` and `Startup.cs` → `Program.cs` refactoring.
7. Update CI/CD plans for SDK pinning, `UseDotNet@2`, `NuGetToolInstaller`, build validation, and feature-branch checks.
8. Define validation for builds, unit tests, integration tests, service connectivity, logging, telemetry, UAT, and production readiness.
9. Structure branches, commits, and PRs so each upgrade checkpoint is reviewable and revertible.
10. Produce release notes and stakeholder communication summarizing framework changes, dependency updates, and validation results.

## Project discovery and assessment

| Prompt name | Use it to produce |
| --- | --- |
| Project Classification Analysis | Identify all projects and classify by `.NET Framework`, `.NET Core`, `.NET Standard`; inspect `.csproj`, `TargetFramework`, and SDK usage. |
| Dependency Compatibility Review | Review external and internal dependencies for compatibility and complexity based on dependency graph depth. |
| Legacy Package Detection | Identify `packages.config` projects that need migration to `PackageReference`. |

## Upgrade strategy and sequencing

| Prompt name | Use it to produce |
| --- | --- |
| Project Upgrade Ordering | Upgrade order from least to most dependent components; isolate class library upgrades before API or Azure Function migrations. |
| Incremental Strategy Planning | Rollback checkpoints and whether to use `.NET Upgrade Assistant` or manual upgrades. |
| Progress Tracking Setup | Upgrade checklist for builds/tests/deployment readiness across all projects. |

## Framework targeting and code adjustments

| Prompt name | Use it to produce |
| --- | --- |
| Target Framework Selection | Correct `TargetFramework` for each project, for example `net8.0`; deprecated SDK or build configuration updates. |
| Code Modernization Analysis | Replacements for deprecated .NET APIs and third-party libraries, including `WebHostBuilder` → `HostBuilder`. |
| Async Pattern Conversion | Candidate synchronous calls to convert to async for performance and scalability. |

## NuGet and dependency management

| Prompt name | Use it to produce |
| --- | --- |
| Package Compatibility Analysis | Outdated or incompatible NuGet packages, compatible versions, libraries without .NET 8 support, and migration paths. |
| Shared Dependency Strategy | Handling shared dependency upgrades and alternatives in Microsoft-supported namespaces. |
| Transitive Dependency Review | Version conflict risks and resolution strategies after upgrade. |

## CI/CD and build pipeline updates

| Prompt name | Use it to produce |
| --- | --- |
| Pipeline Configuration Analysis | YAML build definition updates, SDK version pinning, `UseDotNet@2`, and `NuGetToolInstaller`. |
| Build Pipeline Modernization | Updated build pipeline snippets for .NET 8 migration and feature-branch validation builds. |
| CI Automation Enhancement | Automated test and build verification in CI pipelines. |

## Testing, breaking changes, and delivery

| Area | Prompts and expected output |
| --- | --- |
| Testing & Validation | Build Validation Strategy; Service Integration Verification for logging, telemetry, service connectivity, backward compatibility, runtime behavior; Deployment Readiness Check for UAT and production rollout. |
| Breaking Change Analysis | API Deprecation Detection using `.NET Upgrade Assistant` and API Analyzer; API Replacement Strategy for removed namespaces, `Startup.cs` → `Program.cs`; Regression Testing Focus for endpoints and critical functionality. |
| Version Control & Commit Strategy | Branching Strategy Planning, PR Structure Optimization with `Upgrade to .NET [Version]`, tagging strategies for breaking changes, and Code Review Guidelines. |
| Documentation & Communication | Upgrade Documentation Strategy, Stakeholder Communication, Progress Tracking Systems, dashboard or markdown checklist. |
| Tools & Automation | Upgrade Tool Selection for `.NET Upgrade Assistant`, `dotnet list package --outdated`, `dotnet migrate`, `graph.json`; Analysis Script Generation; Multi-Repository Validation. |
| Final Validation & Delivery | Final Solution Validation, Deployment Readiness Confirmation, post-upgrade build artifacts, Release Documentation, and enterprise-scale validation evidence. |

## Tooling commands

| Tool | Use |
| --- | --- |
| `.NET Upgrade Assistant` | Assess and automate framework migrations where project structure is supported. |
| `dotnet list package --outdated` | Identify outdated package versions before and after target selection. |
| `dotnet migrate` | Evaluate legacy migration needs where applicable. |
| `graph.json` | Visualize dependency graph and sequence upgrades. |

## Output template

```markdown
## .NET upgrade plan

**Status:** assessed | ready to upgrade | blocked
**Target:** `.NET [Version]` / `net8.0`
**Strategy:** `.NET Upgrade Assistant` | manual | hybrid

### Project inventory
| Project | Current type | Current TargetFramework | SDK-style | packages.config | Recommended target | Order |
| --- | --- | --- | --- | --- | --- | --- |
| `<project.csproj>` | `.NET Framework` | `<target>` | yes/no | yes/no | `net8.0` | 1 |

### Dependency and package findings
| Package/project | Issue | Migration path | Risk |
| --- | --- | --- | --- |
| `<dependency>` | <compatibility/version/conflict> | <replacement or version> | low/medium/high |

### Code and pipeline changes
- Code modernization: `WebHostBuilder` → `HostBuilder`, `Startup.cs` → `Program.cs`, async conversion candidates.
- CI/CD: `UseDotNet@2`, `NuGetToolInstaller`, build/test validation, feature-branch checks.

### Validation
- Build: <command/result>
- Unit tests: <command/result>
- Integration/UAT: <plan/result>
- Logging/telemetry/connectivity: <checks>
- Deployment readiness: <status>

### Delivery plan
- Branching strategy: <strategy>
- PR structure: `Upgrade to .NET [Version]`
- Rollback checkpoints: <checkpoints>
- Release notes: <summary>
```

## Quality gate

- [ ] Every project is classified as `.NET Framework`, `.NET Core`, or `.NET Standard`.
- [ ] Each `.csproj` has `TargetFramework` and SDK usage recorded.
- [ ] `packages.config` projects and `PackageReference` migration needs are identified.
- [ ] Upgrade order follows dependency direction from least to most dependent components.
- [ ] NuGet, transitive dependencies, and third-party .NET 8 support are reviewed.
- [ ] Code modernization includes deprecated APIs, `WebHostBuilder` → `HostBuilder`, async conversion, and `Startup.cs` → `Program.cs` where applicable.
- [ ] CI/CD guidance covers YAML SDK pinning, `UseDotNet@2`, `NuGetToolInstaller`, and validation builds.
- [ ] Validation covers build, unit/integration tests, logging, telemetry, service connectivity, UAT, deployment readiness, and regression testing.
- [ ] Branching, PR structure, code review focus, stakeholder communication, progress tracking, and release documentation are included.

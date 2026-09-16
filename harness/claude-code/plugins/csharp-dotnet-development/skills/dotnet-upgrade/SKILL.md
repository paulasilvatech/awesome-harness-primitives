---
name: dotnet-upgrade
description: >-
  Guide .NET upgrade discovery, dependency-aware sequencing, supported framework targeting,
  compatibility fixes, CI/CD updates, and validation. Use when assessing or upgrading .NET
  Framework, .NET Core, modern .NET, or shared .NET Standard projects, selecting a supported LTS,
  or choosing an upgrade workflow.
---

<!-- Generated from harness/github-copilot/plugins/csharp-dotnet-development/skills/dotnet-upgrade/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# .NET upgrade

Plan and execute .NET upgrade work by classifying projects, sequencing dependencies, selecting supported target frameworks, modernizing code and pipelines, validating behavior, and packaging the work into reviewable PRs and release documentation.

## When to invoke

- "Assess this solution for a .NET upgrade."
- "Plan a .NET Framework to the supported .NET LTS migration."
- "Review packages.config projects before upgrading."
- "Choose an upgrade workflow and create a validation checklist."
- "Generate prompts for .NET project discovery and upgrade execution."

## Prerequisites and context

- Inspect solution files, `.csproj` files, `packages.config`, NuGet dependencies, and CI YAML before recommending changes.
- Use existing build and test commands when available.
- Prefer incremental upgrades with rollback checkpoints over broad unreviewable rewrites.
- Verify Microsoft's support policy and the installed upgrade workflow before selecting tools or targets.
- The [Upgrade Assistant overview](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview), verified 2026-09-15, marks .NET Upgrade Assistant deprecated. Prefer the documented [GitHub Copilot upgrade workflow](https://learn.microsoft.com/en-us/dotnet/core/porting/github-copilot-upgrade/overview) when available and appropriate, or reviewed manual changes. Do not assume tool installation or project support.
- The [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core), verified 2026-09-15, lists .NET 10 as active LTS. Recheck at execution time; a preview or the highest installed SDK is not automatically the production target.

## Procedure

1. Discover selected solutions and C#, Visual Basic, and F# projects; classify `.NET Framework`, `.NET Core`, modern `.NET`, and `.NET Standard` libraries separately.
2. Analyze `TargetFramework`, `TargetFrameworks`, legacy `TargetFrameworkVersion`, imported properties, conditions, SDK-style usage, and build configuration. Static declarations are not evaluated MSBuild results.
3. Build the dependency graph and recommend upgrade order from least dependent libraries to APIs, Azure Functions, and other dependents.
4. Detect legacy `packages.config` projects and plan `PackageReference` conversion only where supported, preserving binding redirects and build assets.
5. Review NuGet dependencies, transitive dependencies, and third-party support for the selected supported target. Preserve .NET Framework consumers through compatible shared targets or multi-targeting; do not automatically replace .NET Standard 2.0 with 2.1.
6. Identify required API and app-model compatibility changes. Do not mechanically rewrite serializers, EF6, `Startup.cs`, or hosting models when the chosen target still supports the existing behavior.
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
| Incremental Strategy Planning | Rollback checkpoints and whether to use an installed Microsoft upgrade workflow, reviewed manual changes, or a combination. |
| Progress Tracking Setup | Upgrade checklist for builds/tests/deployment readiness across all projects. |

## Framework targeting and code adjustments

| Prompt name | Use it to produce |
| --- | --- |
| Target Framework Selection | A supported TFM for each project, such as `net10.0` for the verified LTS snapshot; preserve compatible targets for remaining consumers. |
| Code Modernization Analysis | Replacements for deprecated .NET APIs and third-party libraries, including `WebHostBuilder` → `HostBuilder`. |
| Async Pattern Conversion | Candidate synchronous calls to convert to async for performance and scalability. |

## NuGet and dependency management

| Prompt name | Use it to produce |
| --- | --- |
| Package Compatibility Analysis | Outdated or incompatible NuGet packages, compatible versions, libraries without selected-target support, and migration paths. |
| Shared Dependency Strategy | Handling shared dependency upgrades and alternatives in Microsoft-supported namespaces. |
| Transitive Dependency Review | Version conflict risks and resolution strategies after upgrade. |

## CI/CD and build pipeline updates

| Prompt name | Use it to produce |
| --- | --- |
| Pipeline Configuration Analysis | YAML build definition updates, SDK version pinning, `UseDotNet@2`, and `NuGetToolInstaller`. |
| Build Pipeline Modernization | Updated SDK/build-runner configuration for the selected target and feature-branch validation builds. |
| CI Automation Enhancement | Automated test and build verification in CI pipelines. |

## Testing, breaking changes, and delivery

| Area | Prompts and expected output |
| --- | --- |
| Testing & Validation | Build Validation Strategy; Service Integration Verification for logging, telemetry, service connectivity, backward compatibility, runtime behavior; Deployment Readiness Check for UAT and production rollout. |
| Breaking Change Analysis | Installed upgrade tooling and official breaking-change/analyzer evidence; required API replacements and regression tests for endpoints, authentication, serialization and critical behavior. |
| Version Control & Commit Strategy | Branching Strategy Planning, PR Structure Optimization with `Upgrade to .NET [Version]`, tagging strategies for breaking changes, and Code Review Guidelines. |
| Documentation & Communication | Upgrade Documentation Strategy, Stakeholder Communication, Progress Tracking Systems, dashboard or markdown checklist. |
| Tools & Automation | Verified installed upgrade workflow, SDK-appropriate package commands, evaluated project graphs, and bounded assessment scripts; no automatic global tool installation. |
| Final Validation & Delivery | Final Solution Validation, Deployment Readiness Confirmation, post-upgrade build artifacts, Release Documentation, and enterprise-scale validation evidence. |

## Tooling commands

| Tool | Use |
| --- | --- |
| Installed Microsoft upgrade workflow | Discover actual scenario/project support and permissions before use; use manual changes if unavailable. |
| SDK package-list command | Use the syntax supported by the installed SDK to review direct/transitive package compatibility. |
| Existing MSBuild or `dotnet` build/test workflow | Preserve legacy build requirements; do not assume every .NET Framework project builds with the SDK CLI. |
| `graph.json` | Visualize dependency graph and sequence upgrades. |

## Output template

```markdown
## .NET upgrade plan

**Status:** assessed | ready to upgrade | blocked
**Target:** selected runtime/TFM, support source and verification date
**Strategy:** installed Microsoft upgrade workflow | manual | hybrid

### Project inventory
| Project | Current type | Current TargetFramework | SDK-style | packages.config | Recommended target | Order |
| --- | --- | --- | --- | --- | --- | --- |
| `<project.csproj>` | `.NET Framework` | `<target>` | yes/no | yes/no | `<supported target>` | 1 |

### Dependency and package findings
| Package/project | Issue | Migration path | Risk |
| --- | --- | --- | --- |
| `<dependency>` | <compatibility/version/conflict> | <replacement or version> | low/medium/high |

### Code and pipeline changes
- Code modernization: required compatibility fixes, approved behavior changes, and preserved contracts.
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

- [ ] Every selected project is classified by framework family and application/library role.
- [ ] Effective targets, imports/conditions, SDK usage and unresolved evaluation are recorded.
- [ ] `packages.config` projects and `PackageReference` migration needs are identified.
- [ ] Upgrade order follows dependency direction from least to most dependent components.
- [ ] NuGet, transitive dependencies, remaining consumers and selected-target support are reviewed.
- [ ] Code modernization includes deprecated APIs, `WebHostBuilder` → `HostBuilder`, async conversion, and `Startup.cs` → `Program.cs` where applicable.
- [ ] CI/CD guidance covers YAML SDK pinning, `UseDotNet@2`, `NuGetToolInstaller`, and validation builds.
- [ ] Validation covers build, unit/integration tests, logging, telemetry, service connectivity, UAT, deployment readiness, and regression testing.
- [ ] Branching, PR structure, code review focus, stakeholder communication, progress tracking, and release documentation are included.
- [ ] Tool and runtime support claims have dated first-party evidence; unrun checks are explicit.

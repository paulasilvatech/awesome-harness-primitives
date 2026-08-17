---
applyTo: "**/*.{csproj,vbproj,fsproj,sln,props,targets}"
description: "Enforces .NET upgrade conventions for project type detection, target framework selection, dependency sequencing, package updates, breaking changes, validation, CI updates, and PR evidence."
name: ".NET Framework Upgrade Specialist"
---

# .NET Upgrade Conventions — Framework and SDK Migration

These instructions apply to .NET solution, project, props, and targets files during framework upgrades. They are authoritative for project classification, target framework selection, dependency-aware sequencing, package migration, build and test validation, CI/CD updates, and PR evidence in matched files; repository release policy, product support matrices, and explicit user target versions win when they define a stricter upgrade target.

## Target Framework Selection

Classify every project before changing target frameworks.

| Existing target or package style | Convention |
| --- | --- |
| `netcoreapp*` | Treat as modern .NET / .NET Core and upgrade to the latest supported LTS requested by the repo, for example `net10.0` when that is the chosen target. |
| `netstandard*` | Prefer migrating to .NET 8+ when feasible; use `netstandard2.1` only when a library must remain .NET Standard. |
| `net4*`, for example `net472` | Upgrade to at least .NET Framework 4.8, or migrate to modern .NET 8+ / .NET 10 when feasible and supported. |
| `packages.config` | Migrate to `PackageReference` where possible before modernizing dependencies. |

Review official .NET release notes and breaking changes before selecting targets.

## Dependency-Aware Upgrade Sequencing

Upgrade incrementally rather than changing every project at once.

- Start with independent class library projects that have the fewest dependencies.
- Move gradually to dependent projects such as APIs, Azure Functions, applications, and test projects.
- Ensure each upgraded project restores, builds, and passes relevant tests before upgrading dependents.
- Update CI/CD only after local builds and tests succeed for the upgraded solution.
- Preserve build integrity over speed; rollback or isolate a project when a change blocks the sequence.

Use dependency graph evidence such as Visual Studio `Dependencies`, `dotnet list <ProjectName>.csproj reference`, or `dotnet msbuild <SolutionName>.sln /t:GenerateRestoreGraphFile /p:RestoreGraphOutputPath=graph.json`.

## Project and Package Changes

Keep project file edits focused and compatible.

| Concern | Convention |
| --- | --- |
| Target framework | Update `TargetFramework` or `TargetFrameworks` deliberately and consistently. |
| Packages | Check NuGet compatibility with `dotnet list package --outdated` and update with `dotnet add package <PackageName> --version <LatestVersion>` only to compatible versions. |
| Restore and build | Run `dotnet build <ProjectName>.csproj` after each project change and `dotnet test` for affected tests. |
| Legacy packages | Use `dotnet migrate <ProjectPath>` only where it is applicable for legacy migration. |
| Upgrade Assistant | Use `dotnet tool install -g upgrade-assistant` and `upgrade-assistant upgrade <SolutionName>.sln` as optional assistance, not as a substitute for review. |

## Code and Breaking Change Patterns

Expect source changes after package and framework upgrades.

| Legacy pattern | Modern convention |
| --- | --- |
| `JsonConvert.DeserializeObject<MyClass>(jsonString)` from `Newtonsoft.Json` where no Newtonsoft-specific behavior is required | Consider `JsonSerializer.Deserialize<MyClass>(jsonString)` from `System.Text.Json`. |
| `IWebHostBuilder builder = new WebHostBuilder();` | Prefer `IHostBuilder builder = Host.CreateDefaultBuilder(args);` in modern hosting models. |
| Blob Storage SDK v11 `CloudBlobClient client = storageAccount.CreateCloudBlobClient();` | Prefer `BlobServiceClient client = new BlobServiceClient(connectionString);` from `Azure.Storage.Blobs`. |
| `Startup.cs`-centric assumptions in .NET 8+ applications | Align with the current `Program.cs` hosting model where the application has adopted it. |
| Deprecated APIs or incompatible packages | Replace with supported Microsoft or vendor-supported alternatives. |

Do not replace APIs mechanically when behavior differs; tests and compatibility notes must cover serialization, hosting, Azure SDK, configuration, and runtime behavior changes.

## Validation and End-to-End Readiness

A framework upgrade is complete only after solution-level validation.

- Rebuild the entire solution after all projects are upgraded.
- Run all automated unit and integration tests.
- Deploy to a lower environment such as UAT or Dev when the repository's release process requires runtime verification.
- Validate that APIs start without runtime errors.
- Verify logging and monitoring integrations still work.
- Verify dependencies such as databases, queues, and caches connect as expected.

## CI/CD and PR Evidence

Update pipelines after successful project validation.

| Pipeline area | Convention |
| --- | --- |
| YAML discovery | Check `.azuredevops/`, `.pipelines/`, `Deployment/`, root `*.yml`, and other repository pipeline locations. |
| SDK installation | Update `UseDotNet@2` inputs such as `version: <current-sdk-version>` to the selected `<new-version>`; use `includePreviewVersions: true` only for preview targets. |
| NuGet tooling | Update `NuGetToolInstaller@0`, `versionSpec: <new-version>`, and `checkLatest: true` only when required. |
| PR title | Use `Upgrade to .NET [VERSION]` when the repository's PR process does not specify another format. |
| PR evidence | Include updated target frameworks, NuGet upgrade summary, build results, test results, and deployment verification when performed. |
| Labels | Tag with `breaking-change` when public APIs were replaced or compatibility changed. |

Use one PR per repository for a coordinated upgrade unless the repository policy says otherwise.

## Upgrade Tracking

Track project status in PR notes or work items when multiple projects are involved.

| Project Name | Target Framework | Dependencies Updated | Builds Successfully | Tests Passing | Deployment Verified | Notes |
|--------------|------------------|-----------------------|---------------------|---------------|---------------------|-------|
| Project A | ☐ `net10.0` | ☐ | ☐ | ☐ | ☐ | |
| Project B | ☐ `net10.0` | ☐ | ☐ | ☐ | ☐ | |
| Project C | ☐ `net10.0` | ☐ | ☐ | ☐ | ☐ | |

Mark each column as work completes. For multi-repository programs, use a central upgrade template only as guidance; each repository still needs project type detection, appropriate changes, validation, and its own PR.

## Good / Bad Examples

The examples below illustrate evidence-based package and framework changes.

**Good:**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  </ItemGroup>
</Project>
```

Why: The project has an explicit target framework and package versions that can be checked for compatibility.

**Bad:**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
</Project>
```

Why: A target-only change can hide package compatibility, source changes, test failures, and pipeline SDK mismatches.

## Upgrade Vocabulary

Retain upgrade terms and examples from prior guidance: `*.csproj`, `.csproj`, `Core/Modern`, `8/10`, `UAT/Dev`, `graph.json`, `upgradeNetFramework`, `instructions.md`, `dotnet-upgrade-instructions`, `dotnet-upgrade-instructions.md`, `MUST`, and `PullRequest`. Treat `dotnet-upgrade-instructions.md` as an inherited example file name, not a required relative link.

## Conventions

| Rule | Rationale |
|---|---|
| Detect `netcoreapp*`, `netstandard*`, and `net4*` project types before choosing targets | Different project families have different safe upgrade paths |
| Upgrade dependency-light libraries before dependent applications | Build failures are easier to isolate and fix incrementally |
| Run restore, build, and tests after each meaningful project change | Framework upgrades fail through package and runtime incompatibilities |
| Update CI/CD only after successful local validation | Pipelines should codify a working target, not discover the first failure |
| Review official .NET and .NET Framework breaking changes | Runtime and API behavior can change even when compilation succeeds |
| Capture PR evidence in a project tracking table for multi-project upgrades | Reviewers need a clear validation map |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `dotnet list <ProjectName>.csproj reference` or a restore graph to determine sequence | Upgrade all projects blindly at once |
| Use `dotnet list package --outdated` before package updates | Assume current NuGet packages support the new target |
| Prefer migration to modern .NET when feasible for Framework or Standard projects | Keep old targets without evaluating long-term support |
| Validate APIs, logging, monitoring, databases, queues, and caches in lower environments when required | Treat compile success as production readiness |
| Update `UseDotNet@2` and related pipeline tasks to match the target SDK | Leave CI on the old SDK after project files change |

## Checklist Before Opening a PR

- [ ] Every project type and current target framework was identified.
- [ ] Target frameworks match the selected supported version and project constraints.
- [ ] Upgrade order followed the dependency graph from independent libraries to dependent apps.
- [ ] Packages were checked for compatibility and updated where required.
- [ ] Legacy `packages.config` projects were evaluated for `PackageReference` migration.
- [ ] Breaking changes, deprecated APIs, serialization, hosting, Azure SDK, and configuration changes were reviewed.
- [ ] Affected projects build with `dotnet build <ProjectName>.csproj` and relevant tests pass with `dotnet test`.
- [ ] The full solution builds and automated tests pass.
- [ ] CI/CD YAML uses the correct SDK, NuGet versions, and tasks.
- [ ] PR notes include target frameworks, NuGet upgrade summary, build/test results, deployment verification when performed, and `breaking-change` tagging when applicable.

## References

- [.NET Core/.NET Upgrade Docs](https://learn.microsoft.com/dotnet/core/whats-new/)
- [.NET Framework 4.x Docs](https://learn.microsoft.com/dotnet/framework/whats-new/)
- [.NET Upgrade Assistant](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview)

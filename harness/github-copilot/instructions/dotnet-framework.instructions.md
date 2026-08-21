---
applyTo: "**/*.csproj,**/*.cs"
description: "Enforces .NET Framework conventions for MSBuild, legacy and SDK-style project files, C# 7.3 compatibility, NuGet boundaries, Windows paths, async, configuration, exceptions, disposal, and performance."
---

# .NET Framework Conventions — Legacy-Compatible C#

These instructions apply to .NET Framework C# and project files matched by `**/*.csproj,**/*.cs`. They are authoritative for .NET Framework build commands, project-file shape, source inclusion, C# 7.3 compatibility, NuGet package boundaries, Windows environment assumptions, async, configuration, disposal, and performance; repository-specific solution files, CI scripts, and explicit project settings win when they are stricter.

## Build and Project File Shape

Build .NET Framework solutions and projects with `msbuild /t:rebuild` instead of `dotnet build` unless the repository explicitly targets SDK-style build flows. Check each `.csproj` before changing it because both legacy non-SDK projects and SDK-style projects can target .NET Framework versions such as `net48` or `net472`.

| Project type | Convention | Example |
| --- | --- | --- |
| Legacy non-SDK | Add every new `.cs` source file explicitly with `<Compile>` | `<Compile Include="Path\To\NewFile.cs" />` |
| Legacy non-SDK | Use `<TargetFrameworkVersion>` | `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>` |
| Legacy non-SDK | Expect explicit Debug/Release `<PropertyGroup>` sections | Configuration does not come from SDK defaults |
| Legacy non-SDK | Expect explicit `<OutputPath>` and `<IntermediateOutputPath>` | Build output paths are project-defined |
| SDK-style targeting Framework | Use SDK conventions when `<Project Sdk="Microsoft.NET.Sdk">` is present | `<TargetFramework>net48</TargetFramework>` |

Legacy projects do not automatically include files in the directory and do not have implicit imports for common namespaces or assemblies.

## NuGet and Dependency Boundaries

Do not install or update NuGet packages automatically in .NET Framework projects. Package changes often require coordinated edits to project files, `packages.config`, binding redirects, references, and Visual Studio metadata. When a package change is needed, ask the user to use Visual Studio NuGet Package Manager or the Visual Studio Package Manager Console. Recommend only packages compatible with .NET Framework or .NET Standard 2.0, not packages that require only .NET Core or .NET 5+.

## C# 7.3 Language Compatibility

This project is limited to C# 7.3 features unless a project file explicitly proves otherwise. Avoid unsupported C# 8.0+ features: using declarations (`using var stream = ...`), await using statements (`await using var resource = ...`), switch expressions (`variable switch { ... }`), null-coalescing assignment (`??=`), range and index operators (`array[1..^1]`, `array[^1]`), default interface methods, readonly members in structs, static local functions, nullable reference types (`string?`, `#nullable enable`).

Avoid unsupported C# 9.0+ features: records (`public record Person(string Name)`), init-only properties (`{ get; init; }`), top-level programs, pattern matching enhancements, and target-typed new expressions (`List<string> list = new()`). Avoid unsupported C# 10+ features: global using statements, file-scoped namespaces, record structs, and required members.

| Need | C# 7.3-compatible pattern |
| --- | --- |
| Resource cleanup | Traditional `using` statements with braces |
| Branching expression | Switch statements instead of switch expressions |
| Null default assignment | Explicit null checks instead of `??=` |
| Slicing | Manual indexing instead of range/index operators |
| Interface default behavior | Abstract classes or explicit interface implementations |

## Windows Environment and Configuration

Use Windows-style paths with backslashes such as `C:\path\to\file.cs` when suggesting terminal operations or project-file includes. Use Windows-appropriate commands for .NET Framework workflows. Access app settings through `ConfigurationManager.AppSettings`; store connection strings in `<connectionStrings>` instead of `<appSettings>`, and use `web.config` or `app.config` transformations for environment-specific settings.

## Async, DateTime, Strings, and Exceptions

- Use `ConfigureAwait(false)` in library code to avoid deadlocks: `await SomeAsyncMethod().ConfigureAwait(false)`.
- Avoid sync-over-async patterns such as `.Result`, `.Wait()`, and `.GetAwaiter().GetResult()`.
- Prefer `DateTimeOffset` for absolute timestamps; when using `DateTime`, specify `DateTimeKind.Utc` or `DateTimeKind.Local`.
- Use `CultureInfo.InvariantCulture` for serialization and parsing.
- Use `StringBuilder` for repeated string concatenation.
- Always specify `StringComparison`, for example `string.Equals(other, StringComparison.OrdinalIgnoreCase)`.
- Catch specific exception types, not generic `Exception`, unless rethrowing or adding cross-cutting logging at a boundary.
- Do not swallow exceptions; log or rethrow appropriately.

## Disposal, Memory, and Performance

Implement `IDisposable` properly for unmanaged resources and wrap disposable objects in traditional `using` statements. Keep individual objects under `85KB` when practical to avoid Large Object Heap allocation. Avoid boxing and unboxing in hot paths, use `Lazy<T>` for expensive initialization, use `string.Intern()` judiciously only for frequently repeated strings, and cache `MethodInfo` or `PropertyInfo` when reflection is unavoidable in hot paths.

## Compatibility Terminology

Preserve .NET Framework compatibility terms from the original guidance: `Async/Await` patterns require `ConfigureAwait(false)`, unsupported features are `NOT SUPPORTED`, and legacy project source inclusion `MUST` be explicit. Use `web.config/app.config` transformations, avoid `boxing/unboxing`, use `CultureInfo.InvariantCulture` for `serialization/parsing`, and log or `re-throw` exceptions appropriately.

## Good / Bad Examples

The examples below illustrate C# 7.3-compatible async library code.

**Good:**

```csharp
using (var stream = File.OpenRead(path))
{
    var result = await reader.ReadAsync(stream).ConfigureAwait(false);
    return result;
}
```

Why: The code uses a traditional `using` block, `await`, and `ConfigureAwait(false)` without C# 8 syntax.

**Bad:**

```csharp
using var stream = File.OpenRead(path);
return reader.ReadAsync(stream).Result;
```

Why: `using var` is unsupported in C# 7.3 and `.Result` risks deadlock.

## Conventions

| Rule | Rationale |
| --- | --- |
| Build with `msbuild /t:rebuild` for .NET Framework projects | The full MSBuild pipeline handles legacy project behavior |
| Detect legacy versus SDK-style `.csproj` before editing | Source inclusion and target framework elements differ |
| Keep code within C# 7.3 syntax | Unsupported language features break compilation |
| Do not install or update NuGet packages automatically | .NET Framework package changes require Visual Studio-aware coordination |
| Use Windows paths and configuration files deliberately | .NET Framework projects commonly depend on Windows and config transforms |
| Use safe async, disposal, string, DateTime, exception, and reflection patterns | Prevents deadlocks, leaks, globalization bugs, and hot-path regressions |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Add `<Compile Include="Path\To\NewFile.cs" />` in legacy non-SDK projects | Assume new files are automatically compiled |
| Use `<TargetFrameworkVersion>` in legacy projects and `<TargetFramework>` in SDK-style projects | Mix project-file conventions blindly |
| Use switch statements, explicit null checks, and traditional `using` blocks | Use switch expressions, `??=`, nullable reference types, records, or file-scoped namespaces |
| Recommend .NET Framework or .NET Standard 2.0-compatible packages | Recommend packages that require only .NET Core or .NET 5+ |
| Store connection strings in `<connectionStrings>` | Put connection strings in `<appSettings>` |
| Catch specific exceptions and clean up disposables | Swallow generic `Exception` or leak resources |

## Checklist Before Opening a PR

- [ ] The project was built or validated with `msbuild /t:rebuild` when a build is required.
- [ ] The `.csproj` was identified as legacy non-SDK or SDK-style before editing.
- [ ] New source files are included with `<Compile>` in legacy non-SDK projects.
- [ ] Code uses only C# 7.3-compatible syntax and avoids C# 8.0+, 9.0+, and 10+ features.
- [ ] No NuGet package install or update was attempted; compatibility guidance is .NET Framework or .NET Standard 2.0.
- [ ] Windows paths, configuration, and transforms are respected.
- [ ] Async, disposal, DateTime, string comparison, exception, and performance patterns follow the conventions above.

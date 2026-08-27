---
name: nuget-manager
description: >-
  Manage NuGet packages safely in .NET projects and solutions using the `dotnet` CLI. Use this
  skill when adding, removing, or updating package versions, verifying `PACKAGE_NAME`
  availability, working with `Directory.Packages.props`, or deciding when direct `.csproj` edits
  are allowed.
---

<!-- Generated from harness/github-copilot/plugins/dotnet-desktop-development/skills/nuget-manager/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# NuGet manager

Add and remove NuGet packages in projects/solutions. through the `dotnet` CLI, update existing package versions only after verifying the target version exists, and immediately restore to catch compatibility failures.

## When to invoke

- "Add this NuGet package to my project."
- "Remove Newtonsoft.Json from this .NET project."
- "Update a package version in Directory.Packages.props."
- "Verify that this NuGet version exists."
- "Fix package references in a .csproj."

## Prerequisites and context

| Requirement | Why |
| --- | --- |
| .NET SDK compatible with the target solution | Provides `dotnet add`, `dotnet remove`, `dotnet restore`, and `dotnet test` if needed. |
| `dotnet` on `PATH` | All add/remove operations must use the CLI. |
| `jq` or PowerShell | Needed to parse `dotnet package search <PACKAGE_NAME> --exact-match --format json` for exact version verification. |

Use `dotnet package search` for version lookup. Treat `.props` files as package metadata files, not general edit targets.

## Core rules

| Operation | Allowed method | Forbidden method |
| --- | --- | --- |
| Add package | `dotnet add [<PROJECT>] package <PACKAGE_NAME> [--version <VERSION>]` | Directly editing `.csproj`, `.props`, or `Directory.Packages.props`; NEVER direct-edit for adds. |
| Remove package | `dotnet remove [<PROJECT>] package <PACKAGE_NAME>` | Directly deleting `<PackageReference>` or `<PackageVersion>` entries. |
| Update existing version | Verify the version, locate the version owner, edit only the version string, run `dotnet restore`. | Changing versions without checking NuGet or restoring; DIRECT EDITING is ONLY for VERSION UPDATES. |
| Central package management | Edit `<PackageVersion Include="Package.Name" Version="1.2.3" />` in `Directory.Packages.props`. | Adding/removing central package entries by hand instead of using CLI-supported workflows when possible. |
| Per-project package management | Edit the `Version` on an existing `<PackageReference Include="Package.Name" Version="1.2.3" />`. | Moving packages between project and central management without a clear migration request. |

## Procedure

1. Identify the solution, project, and package operation: add, remove, or update version.
2. For add/remove, run the `dotnet` CLI command against the intended project or solution scope.
3. For version updates, verify the exact target version exists before editing.
4. Determine whether versions are centrally managed by searching for `Directory.Packages.props`; otherwise inspect individual `.csproj` files.
5. Change only the existing version string in the owning file.
6. Run `dotnet restore` on the project or solution immediately.
7. If restore fails, revert the version change and report the compatibility blocker.

## Commands and version verification

| Task | Command |
| --- | --- |
| Add package | `dotnet add src/MyProject/MyProject.csproj package Newtonsoft.Json` |
| Add specific version | `dotnet add src/MyProject/MyProject.csproj package <PACKAGE_NAME> --version <VERSION>` |
| Remove package | `dotnet remove src/MyProject/MyProject.csproj package Newtonsoft.Json` |
| Search exact package | `dotnet package search <PACKAGE_NAME> --exact-match --format json` and parse the JSON result. |
| Verify version with `jq` | `dotnet package search <PACKAGE_NAME> --exact-match --format json | jq -e '.searchResult[].packages[] | select(.version == "<VERSION>")'` |
| Verify version with PowerShell | `(dotnet package search <PACKAGE_NAME> --exact-match --format json | ConvertFrom-Json).searchResult.packages | Where-Object { $_.version -eq "<VERSION>" }` |
| Restore | `dotnet restore` |

## Examples

| User request | Correct action |
| --- | --- |
| "Add Serilog to the WebApi project" | Run `dotnet add src/WebApi/WebApi.csproj package Serilog`. |
| "Update Newtonsoft.Json to 13.0.3 in the whole solution" | Verify `13.0.3`, locate `Directory.Packages.props` or `.csproj`, update the version string, then run `dotnet restore`. |
| "Remove Newtonsoft.Json" | Run `dotnet remove [<PROJECT>] package Newtonsoft.Json` for each intended project. |

## Gotchas

- **Never add or remove packages by editing XML**: the CLI updates related restore metadata consistently.
- **Direct editing is only for version changes**: even then, edit the file that already owns the version.
- **Central package management changes the target file**: `Directory.Packages.props` overrides per-project expectations.
- **Restore immediately**: a version that exists on NuGet can still be incompatible with the project.

## Output template

```markdown
## NuGet package result

**Status:** complete | reverted | blocked
**Operation:** add | remove | update-version
**Package:** `<PACKAGE_NAME>`
**Target:** `<solution or project>`

| Step | Command or file | Result |
| --- | --- | --- |
| Verify | `<dotnet package search ...>` | pass | fail | not needed |
| Change | `<dotnet add/remove ...>` or `<file>` | <summary> |
| Restore | `dotnet restore` | pass | fail |

### Notes
- <compatibility issue, central package file, or revert detail>
```

## Quality gate

- [ ] Add and remove operations used `dotnet add package` or `dotnet remove package`.
- [ ] Direct file editing was limited to changing an existing package version.
- [ ] Target versions were verified with `dotnet package search <PACKAGE_NAME> --exact-match --format json` before editing.
- [ ] Version ownership was resolved to `Directory.Packages.props` or the correct `.csproj`.
- [ ] `dotnet restore` ran after the change, or failure to run was reported.
- [ ] Failed restores caused the version change to be reverted or clearly marked blocked.

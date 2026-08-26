---
name: "pester-migration"
description: >-
  Upgrade PowerShell Pester test suites across major versions v3 to v4, v4 to v5, and v5 to v6 while preserving test intent. Use when asked to migrate, modernize, or fix *.Tests.ps1 files after a Pester version bump, convert legacy Should or Invoke-Pester syntax, handle Discovery/Run failures, move setup into BeforeAll, migrate mocks, or adopt PesterConfiguration.
---

# Pester migration

Upgrade existing PowerShell Pester suites one major version at a time, using the correct migration guide for the source and target version, then rerun tests until the suite is green without changing what the tests assert.

## When to invoke

- "Migrate these Pester tests from v4 to v5."
- "Fix *.Tests.ps1 files that broke after upgrading Pester."
- "Convert legacy Invoke-Pester parameters to PesterConfiguration."
- "Why did my mocks stop working in Pester 6?"
- "Modernize this PowerShell test suite across Pester major versions."

## Prerequisites and context

- Pester test files usually end in `*.Tests.ps1` and use `Describe`, `Context`, `It`, and `Should`.
- Migrate one major jump at a time: v3→v4, then v4→v5, then v5→v6. Never skip a major version.
- Windows PowerShell 5.1 ships a Microsoft-signed built-in Pester 3; installing a newer module side-by-side may require `-SkipPublisherCheck`.
- Installation reference: https://pester.dev/docs/introduction/installation.

## Progressive disclosure and bundled resources

Load the reference for the exact jump before editing.

| Reference | When to load |
| --- | --- |
| `references/v3-to-v4.md` | `Should Be` → `Should -Be`, `Contain` → `FileContentMatch`, `Assert-VerifiableMocks` → `Assert-VerifiableMock`, and array assertion edge cases. |
| `references/v4-to-v5.md` | Discovery/Run split, `BeforeAll`, `$PSScriptRoot`, `BeforeDiscovery`, `-ForEach`, mock scoping, `Should -Throw` wildcards, and `Invoke-Pester` → `New-PesterConfiguration`. |
| `references/v5-to-v6.md` | PowerShell 5.1/7.4+, per-file discovery+run, empty `-ForEach`, duplicate setup blocks, name `<...>` templates, `Assert-MockCalled` removal, mocks no longer fall through, code-coverage tracer, and legacy `Invoke-Pester` params removal. |

Canonical migration source: https://pester.dev/docs/migrations/v4-to-v5.

## Version detection

Run these before editing:

```powershell
Get-Module Pester -ListAvailable | Select-Object Name, Version, Path
(Get-Module Pester).Version
```

Infer the suite's source version from code, not only the installed module.

| You see in tests or build scripts | Interpret as |
| --- | --- |
| `Should Be`, `Should Contain` without a dash | v3 or earlier; start with `references/v3-to-v4.md`. |
| `$MyInvocation.MyCommand.Path` and dot-sourcing at top level under `Describe` | v4; read `references/v4-to-v5.md`. |
| `Assert-MockCalled`, `Assert-VerifiableMock`, `Set-ItResult -Pending` | v4 or early v5; these are removed in v6. |
| `Invoke-Pester -Script ... -OutputFile ... -CodeCoverage ...` | Legacy invocation; map to config. |
| `BeforeAll { . $PSScriptRoot/... }`, `New-PesterConfiguration`, `Should -Invoke` | Already v5-style; assess v5→v6. |

Install target versions deliberately:

```powershell
Install-Module Pester -MaximumVersion 5.99.99 -Force
Install-Module Pester -Force
Remove-Module Pester; Import-Module Pester
```

## Migration workflow

1. **Baseline**: run `Invoke-Pester` on the current version and record pass/fail so migration regressions are distinguishable from pre-existing failures.
2. **Read the jump reference**: load only the reference file for the current major jump before editing.
3. **Edit file by file**: apply mechanical changes and structural changes in small reviewable patches.
4. **Switch Pester versions**: install/import the target major after source-compatible edits are complete.
5. **Run with detail**: use `Invoke-Pester -Output Detailed`; for hard v4→v5 failures use `-Output Diagnostic` and match symptoms to the reference tables.
6. **Fix to green**: rerun until results match the baseline or improve for documented reasons.
7. **Review the diff**: keep a branch and commit per file or concern so `git bisect` remains useful.

## Major-version cheat sheet

| Jump | Difficulty | Nature | Key work |
| --- | --- | --- | --- |
| v3 → v4 | Low | Assertion syntax rename. | `Should -Be`, `FileContentMatch`, `Assert-VerifiableMock`, array assertion review. |
| v4 → v5 | High | Fundamental runtime change. | Move setup into `BeforeAll`; discovery-time generation into `BeforeDiscovery`; use `$PSScriptRoot`; migrate `Invoke-Pester` to config. |
| v5 → v6 | Low–Medium | Deprecated features now throw. | Replace removed mock verbs, handle empty `-ForEach`, merge duplicate setup blocks, account for no mock fall-through. |

### v4 → v5 common fixes

```powershell
# BEFORE
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$here\Get-Thing.ps1"

# AFTER
BeforeAll { . $PSScriptRoot/Get-Thing.ps1 }

BeforeDiscovery { $cases = Get-Content $PSScriptRoot/cases.json | ConvertFrom-Json }
{ throw 'a long message' } | Should -Throw '*long*'
```

### v5 → v6 common fixes

```powershell
Should -Invoke Get-Thing -Times 1 -Exactly
Should -InvokeVerifiable
Mock Get-Thing { 'default' }
Mock Get-Thing -ParameterFilter { $Name -eq 'a' } -MockWith { 'a' }
Describe 'Optional' -ForEach $cases -AllowNullOrEmptyForEach { }
```

## Safety rules

- **Tests are the spec**: do not change intended behavior unless a documented breaking change requires it and the user accepts the new behavior.
- **Automated scripts are helpers, not authority**: scripts can help with `Should` and dot-sourcing replacements but produce false positives.
- **Preserve encoding**: keep UTF-8 versus ASCII and non-ASCII test names intact when scripting over `*.Tests.ps1`.
- **Do not bulk-edit unchecked**: run the suite after each meaningful concern.

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `-Output Detailed`
- `BeforeAll { . $PSScriptRoot/… }`
- `BeforeAll/BeforeEach/AfterAll/AfterEach`
- `DISCOVERS`
- `DISCOVERS/generates`
- `ForEach/-TestCases`
- `Install-Module`
- `Invoke-Pester -Script … -OutputFile … -CodeCoverage …`
- `Path/-Output`
- `Script/-OutputFile`
- `array-assertion`
- `backwards-compatible`
- `breaking-change`
- `data-driven`
- `differently-signed`
- `dot-source`
- `early-v5`
- `file/concern.**`
- `find-replace`
- `known-good`
- `pass/fail.`
- `passing/failing`
- `per-jump`
- `previously-deprecated`
- `re-import`
- `re-run`
- `script-automatable`
- `symptom-driven`
- `two-phase`
- `v3/v4`

PowerShellGet note: on Windows PowerShell 5.1, PowerShellGet may require `-SkipPublisherCheck` for side-by-side Pester installation.

## Output template

```markdown
## Pester migration result

**Status:** complete | needs fixes | blocked
**Source version:** <v3|v4|v5|unknown>
**Target version:** <v4|v5|v6>

### Files changed
| File | Migration applied | Validation |
| --- | --- | --- |
| `*.Tests.ps1` | <syntax/setup/mock/config change> | <pass/fail evidence> |

### Commands run
- `Get-Module Pester -ListAvailable | Select-Object Name, Version, Path`
- `Invoke-Pester <options>`

### Remaining issues
- <failure, symptom, or human decision>
```

## Quality gate

- [ ] Source and target Pester versions were detected from both installed modules and test syntax.
- [ ] Only one major jump was migrated at a time.
- [ ] The relevant `references/` guide was loaded before edits.
- [ ] Baseline and final `Invoke-Pester` results were recorded.
- [ ] `BeforeAll`, `BeforeDiscovery`, `$PSScriptRoot`, mocks, `-ForEach`, and `New-PesterConfiguration` were handled when applicable.
- [ ] Test intent and file encoding were preserved.

## References

- [Pester v4 to v5 migration](https://pester.dev/docs/migrations/v4-to-v5)
- Installation: https://pester.dev/docs/introduction/installation.

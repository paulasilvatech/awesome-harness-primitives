---
applyTo: '**/*.ps1,**/*.psm1'
description: 'Enforces PowerShell cmdlet and scripting conventions for naming, parameters, pipeline behavior, output, safety, help, and automation.'
---

# PowerShell Conventions — Cmdlets and Automation Scripts

These instructions apply to PowerShell scripts and modules matched by `**/*.ps1` and `**/*.psm1`. They are authoritative for idiomatic cmdlet shape, parameter contracts, pipeline behavior, output streams, safety gates, help, and formatting in those files; repository-specific security, deployment, or test primitives win when they define stricter automation requirements.

## Naming and Style

Use Microsoft PowerShell cmdlet conventions so scripts behave like built-in commands.

| Element | Convention |
| --- | --- |
| Function and cmdlet names | Approved `Verb-Noun` format; use `Get-Verb`, singular nouns, `PascalCase`, and no spaces or special characters |
| Parameters | `PascalCase`, clear names, singular unless the value is always multiple, and standard names such as `Path`, `Name`, and `Force` where they fit |
| Public variables | `PascalCase` when they are intentionally public API |
| Private variables | `camelCase` and meaningful names without abbreviations |
| Aliases | Avoid aliases in scripts; use full cmdlet and parameter names |

Use `Where-Object` instead of `?` or `where`, `ForEach-Object` instead of `%`, and `Get-ChildItem` instead of `gci`, `ls`, or `dir`. Custom aliases need explicit documentation because scripts must be readable outside the author's interactive shell.

## Parameter Design

Declare advanced functions with `[CmdletBinding()]` when they expose cmdlet behavior. Use common .NET types, validation attributes, and tab-completion-friendly choices.

| Concern | Rule | Rationale |
| --- | --- | --- |
| Required inputs | Mark required values with `[Parameter(Mandatory)]` and document their purpose | Non-interactive callers fail early instead of reaching prompts |
| Limited choices | Use `[ValidateSet('Dev', 'Test', 'Prod')]` or equivalent validation | Invalid values are rejected before the command mutates state |
| Null and empty values | Use `[ValidateNotNullOrEmpty()]` on required strings and arrays | Empty strings rarely represent valid automation intent |
| Boolean flags | Use `[switch]` for flags such as `$Force`, `$Quiet`, and `$PassThru` | Switch parameters integrate with PowerShell binding and default to absent |
| Switch state | Test `$SwitchName.IsPresent` when the distinction matters | Presence is explicit and avoids truthiness mistakes |

Do not declare `[bool]$Parameter` for command-line flags, do not assign defaults such as `[switch]$Quiet = [switch]$true`, and keep `$true` or `$false` only where parameter attributes require Boolean metadata such as `Mandatory = $true`.

## Pipeline and Output

Design pipeline functions around `begin`, `process`, and `end` blocks. Accept direct object input with `ValueFromPipeline`, accept property binding with `ValueFromPipelineByPropertyName`, and stream one output object at a time from `process` instead of building large arrays.

Return rich objects, not formatted text. Prefer `[PSCustomObject]` for structured output and `Write-Output` only when emitting data intentionally. Action cmdlets default to no output and add a `[switch]$PassThru` parameter when callers need the created or modified object. Use `Write-Verbose` and `Write-Warning` for status, never `Write-Host` for machine-readable data.

## Error Handling and Safety

Protect destructive and state-changing operations with PowerShell's confirmation model.

| Practice | Requirement |
| --- | --- |
| WhatIf and Confirm | Use `[CmdletBinding(SupportsShouldProcess = $true)]` or `[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]` for commands that change or remove state |
| Mutation boundary | Call `$PSCmdlet.ShouldProcess($Target, 'Action description')` as close as possible to the operation |
| Extra confirmation | Use `$PSCmdlet.ShouldContinue()` for high-impact follow-up prompts; allow `-Force` to bypass the extra prompt when appropriate |
| Error preferences | Use `-ErrorAction Stop` around operations whose failures must enter `catch` |
| Advanced-function errors | Prefer `$PSCmdlet.WriteError()` for non-terminating errors and `$PSCmdlet.ThrowTerminatingError()` for terminating errors |
| Error records | Construct `[System.Management.Automation.ErrorRecord]` with an exception, stable error ID, `[System.Management.Automation.ErrorCategory]`, and target object |

Use `try`/`catch` for recoverable operations and restore any changed `$ErrorActionPreference` in `end` or `finally`. Use `Read-Host` only for deliberate interactive UI; automation scripts accept all required input through parameters.

## Documentation and Help

Every public-facing function or cmdlet includes comment-based help inside the function. Include `.SYNOPSIS`, `.DESCRIPTION`, one or more `.EXAMPLE` entries, `.PARAMETER` entries for every public parameter, `.OUTPUTS`, and `.NOTES` when operational context matters. Keep examples practical and include `-Verbose`, `-WhatIf`, `-Confirm`, or `-PassThru` when those switches are part of the contract.


## Preserved Cmdlet Vocabulary

Keep the following API and stream names recognizable when refactoring existing examples because callers, tests, or readers may search for these exact identifiers.

| Vocabulary | Convention |
| --- | --- |
| `Begin/Process/End` | Treat this as the documented pipeline block pattern even when the prose uses lowercase `begin`, `process`, and `end`. |
| `Write-Error`, `throw`, `try/catch`, `ErrorVariable`, and `verbose/warning` | Preserve their distinctions: non-terminating error output, terminating exceptions, structured handling, captured errors, and status streams are different contracts. |
| `ALWAYS`, `NEVER`, `CORRECT`, and `WRONG` | Keep these labels only when reproducing compatibility guidance from older examples; normal prose should avoid unnecessary all-caps emphasis. |
| `[bool]`, `action-oriented`, and `modified/created` | Use `[bool]` only to explain the flag anti-pattern; switch names should be action-oriented and `-PassThru` returns the modified/created object. |
| `USERNAME` | `$env:USERNAME` is acceptable when a script needs the current Windows user, but keep it out of secrets and portable identity assumptions. |
| `ProfileType`, `ResourceConfiguration`, `ResourceStatus`, `LastUpdated`, and `UpdatedBy` | These sample names remain valid for examples of parameter validation and structured resource update output. |
| `Quiet.IsPresent` | Use `$Quiet.IsPresent` when showing switch presence checks. |
| `ActiveDirectory`, `Microsoft.ActiveDirectory.Management.ADException`, `ActiveDirectoryError`, `Remove-ADUser`, `UserAccount`, `UserExists`, `UserNotFound`, `ObjectNotFound`, `System.Exception`, and `UnexpectedError` | Preserve these names in Active Directory removal examples so exception-specific handling, stable error IDs, and target categories remain clear. |
| `<# ... #>` | Use this marker to demonstrate comment-based help blocks inside public functions. |
| `ForEach-Object` | Use the full pipeline iteration cmdlet name in scripts instead of `%`. |
| `Get-ChildItem` | Use the full child-item discovery cmdlet name in scripts instead of `gci`, `ls`, or `dir`. |

## Good / Bad Examples

The examples below illustrate safe switch handling, ShouldProcess placement, structured output, and error records.

**Good:**

```powershell
function Remove-CacheFiles {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$Path,

        [Parameter()]
        [switch]$PassThru
    )

    process {
        try {
            $files = Get-ChildItem -Path $Path -Filter '*.cache' -ErrorAction Stop
            if ($PSCmdlet.ShouldProcess($Path, 'Remove cache files')) {
                $files | Remove-Item -Force -ErrorAction Stop
                if ($PassThru.IsPresent) {
                    [PSCustomObject]@{ Path = $Path; Removed = $files.Count }
                }
            }
        } catch {
            $errorRecord = [System.Management.Automation.ErrorRecord]::new(
                $_.Exception,
                'RemovalFailed',
                [System.Management.Automation.ErrorCategory]::NotSpecified,
                $Path
            )
            $PSCmdlet.WriteError($errorRecord)
        }
    }
}
```

Why: The function uses an approved verb-noun name, parameter validation, a true `[switch]`, `ShouldProcess`, full cmdlet names, structured `PSCustomObject` output, and an explicit `ErrorRecord`.

**Bad:**

```powershell
function rmCaches($path, [bool]$quiet = $true) {
    $items = ls $path -Filter *.cache
    $items | rm -Force
    Write-Host "Removed $($items.Count) files"
}
```

Why: The function uses an unapproved name, aliases, an interactive-style Boolean flag, no validation, no `ShouldProcess`, and `Write-Host` for data that callers cannot consume.

## Conventions

| Rule | Rationale |
|---|---|
| Use approved `Verb-Noun` names with singular nouns and `PascalCase` | Users can discover commands consistently with built-in PowerShell |
| Use full cmdlet and parameter names instead of aliases | Scripts remain portable, readable, and safe in non-interactive automation |
| Model flags as `[switch]` parameters and check `.IsPresent` | PowerShell binding handles absent and present flags predictably |
| Support pipeline input with `ValueFromPipeline`, `ValueFromPipelineByPropertyName`, and `begin`/`process`/`end` blocks where appropriate | Commands compose with downstream cmdlets and stream data efficiently |
| Return `[PSCustomObject]` or typed objects and use `-PassThru` for action cmdlet output | Callers can sort, filter, serialize, and test results without parsing text |
| Gate destructive actions with `SupportsShouldProcess`, `ConfirmImpact`, `$PSCmdlet.ShouldProcess()`, and `$PSCmdlet.ShouldContinue()` when needed | `-WhatIf` and `-Confirm` prevent accidental data loss |
| Use `$PSCmdlet.WriteError()` and `$PSCmdlet.ThrowTerminatingError()` with `ErrorRecord` objects in advanced functions | Errors carry category, target, and stable IDs for callers |
| Avoid `Read-Host` in automation scripts | Non-interactive execution cannot satisfy prompts |
| Include comment-based help for public functions | Users and `Get-Help` receive accurate contracts and examples |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `Get-Verb` and approved `Verb-Noun` names such as `Get-UserProfile` | Invent names such as `rmCaches` or use plural nouns without need |
| Use `Get-ChildItem -Path $Path` and `Where-Object` | Use `gci`, `ls`, `dir`, `?`, `where`, or `%` in scripts |
| Use `[switch]$Force`, `[switch]$Quiet`, and `[switch]$PassThru` | Use `[bool]$Force` or default a switch with `[switch]$true` |
| Emit rich objects with `Write-Output` or implicit output | Emit parse-only status strings with `Write-Host` |
| Place `$PSCmdlet.ShouldProcess()` immediately before the change | Check confirmation far from the mutating command |
| Build `[System.Management.Automation.ErrorRecord]` values with categories and targets | Throw opaque strings from advanced functions when structured errors are needed |
| Accept required inputs as parameters | Prompt with `Read-Host` inside automation paths |

## Checklist Before Opening a PR

- [ ] Public functions use approved `Verb-Noun` names, singular nouns, and `PascalCase` parameters.
- [ ] Scripts use full cmdlet names and full parameter names, not aliases.
- [ ] Boolean command-line flags are `[switch]` parameters with no default assignment.
- [ ] Parameters use appropriate .NET types and validation attributes such as `[ValidateSet]` or `[ValidateNotNullOrEmpty()]`.
- [ ] Pipeline functions implement `begin`, `process`, and `end` blocks and stream one object at a time.
- [ ] Data output is structured with `[PSCustomObject]` or typed objects; status uses verbose or warning streams.
- [ ] Destructive commands support `-WhatIf` and `-Confirm` through `SupportsShouldProcess`, `ConfirmImpact`, and `$PSCmdlet.ShouldProcess()`.
- [ ] Advanced functions report errors through `$PSCmdlet.WriteError()` or `$PSCmdlet.ThrowTerminatingError()` with `ErrorRecord` details.
- [ ] Public functions include comment-based help with synopsis, description, examples, parameter docs, outputs, and notes.

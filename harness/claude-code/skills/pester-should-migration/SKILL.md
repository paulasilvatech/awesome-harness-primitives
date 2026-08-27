---
name: pester-should-migration
description: >-
  Convert classic Pester v5 `Should -...` assertions to Pester v6 `Should-*` assertion commands
  while preserving behavior. Use when asked to migrate, convert, rewrite, or modernize `Should
  -Be`, `Should -Not -Be`, `Should -Throw`, `Should -Invoke`, or other assertions in .Tests.ps1
  and PowerShell files.
argument-hint: File, folder, or test suite to migrate
---

<!-- Generated from harness/github-copilot/skills/pester-should-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Pester Should migration

Convert classic space-separated Pester assertions such as `Should -Be` to the Pester v6 command form such as `Should-Be`, using behavior-aware mappings instead of blind text replacement.

## When to invoke

- "Convert these Pester assertions to Should-* syntax."
- "Migrate `Should -Be` to Pester v6 style."
- "Rewrite `Should -Not -Be` calls in these .Tests.ps1 files."
- "Modernize Pester v5 assertions without changing test behavior."
- "Enable `Should.DisableV5` after converting assertions."

## Inputs

Use `$ARGUMENTS` as the file, folder, or suite scope to migrate. If `$ARGUMENTS` is empty, inspect the user's selected context or ask for a target before editing. Limit changes to PowerShell files, especially `*.Tests.ps1` and relevant `.ps1` helpers.

## Prerequisites and context

- Requires Pester v6+ for the new `Should-*` commands.
- The classic `Should -Be` style still works in v6, so migration is optional and incremental.
- Verified guidance originated against Pester 6.0.0-rc2; confirm current command behavior when exact semantics matter.
- Use the companion `pester-migration` skill when the suite also needs runtime, mock, or config migration across v3→v4→v5→v6.

## Progressive disclosure and bundled resources

- `references/assertion-map.md`: full operator-by-operator conversion table with before/after examples and workarounds.

Load it for any operator not listed in the quick mapping or when a behavioral gotcha applies.

## Conversion map

| Classic v5 | New v6 |
| --- | --- |
| `$x \| Should -Be 1` | `$x \| Should-Be 1` |
| `$x \| Should -Not -Be 1` | `$x \| Should-NotBe 1` |
| `$x \| Should -BeExactly 'A'` | `$x \| Should-BeString 'A' -CaseSensitive` |
| `$x \| Should -BeGreaterOrEqual 2` | `$x \| Should-BeGreaterThanOrEqual 2` |
| `$x \| Should -BeLessOrEqual 2` | `$x \| Should-BeLessThanOrEqual 2` |
| `$x \| Should -BeLike 'a*'` | `$x \| Should-BeLikeString 'a*'` |
| `$x \| Should -Match 're'` | `$x \| Should-MatchString 're'` |
| `$x \| Should -BeOfType [int]` | `$x \| Should-HaveType ([int])` |
| `$x \| Should -BeNullOrEmpty` | Choose `Should-BeNull`, `Should-BeEmptyString`, `Should-BeCollection -Count 0`, or `Should-BeFalsy`. |
| `$c \| Should -HaveCount 3` | `$c \| Should-BeCollection -Count 3` |
| `$c \| Should -Contain 2` | `$c \| Should-ContainCollection 2` |
| `{ ... } \| Should -Throw 'msg'` | `{ ... } \| Should-Throw -ExceptionMessage 'msg'` |
| `Should -Invoke Get-Thing` | `Should-Invoke Get-Thing` |
| `Should -InvokeVerifiable` | `Should-Invoke -Verifiable` |
| `Assert-MockCalled` | `Should-Invoke` when also completing broader v6 mock migration. |

## Procedure

1. Search only the requested scope for `Should -`, `Should -Not -`, and `Assert-MockCalled` in `*.Tests.ps1` and `.ps1` files.
2. Apply mechanical mappings only where the operator has identical behavior.
3. Stop and choose by intent for case sensitivity, truthiness, null-or-empty, collections, pipeline unwrapping, `Should -Exist`, file-content assertions, and `Should -BeIn`.
4. Run `Invoke-Pester -Path ./tests` or the smallest equivalent suite command.
5. If the suite is fully migrated and the user wants enforcement, set:

```powershell
$config = New-PesterConfiguration
$config.Should.DisableV5 = $true
```

## Behavioral gotchas

| Gotcha | Rule |
| --- | --- |
| Case sensitivity | `Should -Be` is case-insensitive; `Should -BeExactly` requires `Should-BeString -CaseSensitive`. Also map `BeLikeExactly` to `Should-BeLikeString -CaseSensitive` and `MatchExactly` to `Should-MatchString -CaseSensitive`. |
| Truthy/falsy | Classic `Should -BeTrue` and `Should -BeFalse` accept truthy/falsy values. New `Should-BeTrue` and `Should-BeFalse` are strict booleans; use `Should-BeTruthy` or `Should-BeFalsy` to preserve loose behavior. |
| Null or empty | `BeNullOrEmpty` has no single equivalent. Pick null, empty string, empty collection, whitespace, or falsy by test intent. |
| Collections | New `Should-Be` is a value assertion and errors when `-Expected` is a collection. Use `Should-BeCollection` for arrays and exact collection equality. |
| Pipeline unwrapping | Pipeline input unwraps `@(1)` to `1`, `@()` to `$null`, and re-collects typed arrays as `[object[]]`. Use `-Actual` when exact value or concrete type matters. |
| Missing equivalents | `Should -Exist` and `Should -FileContentMatch*` have no new counterpart. Keep classic form or rewrite with `Test-Path` and `Get-Content -Raw`. |
| BeIn direction | There is no `Should-BeIn`; reverse operands with `Should-ContainCollection` or keep the classic form. |

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- ` -> `
- ` and `
- ` as `
- `$collection | Should-ContainCollection $value`
- `$false`
- `$null`
- `$true`
- `$value | Should -BeIn $collection`
- `$x | Should-Be 1`
- `(Get-Content $p -Raw) | Should-MatchString 're'`
- `). The new `
- `*.ps1`
- `, and a typed collection (`
- `-Actual`
- `-BeFalse`
- `-Because`
- `-Not`
- `1, 2, 3 | Should-ContainCollection @(1, 2)`
- `Should`
- `Should -*`
- `Should -Contain`
- `Should -Not -BeNullOrEmpty`
- `Should-Be -Actual $x -Expected 1`
- `Should-HaveType`
- `Should-NotBe`
- `Should-NotBeEmptyString`
- `Should-NotBeNull`
- `Should-NotBeWhiteSpaceString`
- `Test-Path $p | Should-BeTrue`
- `[object[]]`
- `actual/expected`
- `case-sensitive`
- `https://pester.dev/docs/assertions/should-command`
- `https://pester.dev/docs/commands/Should-Be`
- `https://pester.dev/docs/migrations/v5-to-v6`
- `re-check`
- `re-collected`
- `single-item`
- `step-3--check-the-behavioral-gotchas-do-not-skip`
- `type-aware`
- `whole-collection`

## Output template

```markdown
## Pester Should migration result

**Status:** complete | needs human decision | blocked
**Scope:** `$ARGUMENTS`

### Assertion changes
| File | Converted | Left classic | Reason |
| --- | ---: | ---: | --- |
| `<file>.Tests.ps1` | <count> | <count> | <Should -Exist, BeNullOrEmpty decision, or none> |

### Validation
- `Invoke-Pester -Path ./tests`: <pass/fail/not run>

### Human decisions
- <truthy/falsy, null-or-empty, collection, or direction choice>
```

## Quality gate

- [ ] `$ARGUMENTS` or selected scope was consumed and limited to PowerShell test targets.
- [ ] `references/assertion-map.md` was used for non-trivial operators.
- [ ] No behavioral gotcha was converted by blind rename.
- [ ] `Should -Exist` and `Should -FileContentMatch*` were kept or rewritten intentionally.
- [ ] `Invoke-Pester` or the suite's existing test command was run after changes.
- [ ] Any `Should.DisableV5` enforcement happened only after remaining classic assertions were addressed.

## References

- [Should-Be command](https://pester.dev/docs/commands/Should-Be)
- [Should assertions concept](https://pester.dev/docs/assertions/should-command)
- [Pester v5 to v6 migration](https://pester.dev/docs/migrations/v5-to-v6)

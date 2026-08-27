---
name: refactor-method-complexity-reduce
description: >-
  Refactor a specified method to reduce cognitive complexity to a requested threshold or below by
  extracting focused helper methods while preserving behavior. Use when the user asks to reduce
  method complexity, simplify nested conditionals, split large if-else or switch chains, extract
  validation or type-specific handlers, and verify tests show failed=0.
argument-hint: "methodName and complexityThreshold, for example: CalculatePrice 15"
---

<!-- Generated from harness/github-copilot/plugins/code-quality-refactoring/skills/refactor-method-complexity-reduce/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Refactor method complexity reduce

Reduce a named method's cognitive complexity to the requested threshold by extracting cohesive helper methods, simplifying control flow, preserving all behavior and error handling, then compiling and verifying related tests explicitly report `failed=0`.

## When to invoke

- "Refactor this method to reduce cognitive complexity below 15."
- "Extract helpers from `${input:methodName}` until complexity is under `${input:complexityThreshold}`."
- "Simplify this nested if-else chain without changing behavior."
- "Reduce method complexity and verify tests show failed=0."

## Inputs

Use `$ARGUMENTS` as the method name and target complexity threshold. Accept the legacy placeholders `${input:methodName}` and `${input:complexityThreshold}` when they appear in user-provided text, but resolve them to concrete values before editing. If either value is missing, infer from the selected code or ask for only the missing value.

## Complexity reduction criteria

Inspect the target method for these complexity sources before editing:

| Source | Refactoring move |
| --- | --- |
| Deeply nested `if`/`else` blocks | Replace with guard clauses or extract branch handlers. |
| Long `switch` or type dispatch | Extract case-specific methods or strategy-like handlers. |
| Repeated validation | Extract `Validate*` helpers that preserve exception types and messages. |
| Complex boolean expressions | Extract predicate methods with names that explain the condition. |
| Loops with inner conditions | Extract loop body or filtering predicates. |
| Repeated transformations | Extract reusable conversion or mapping helpers. |

The main method should read as a high-level flow after refactoring. Helpers should have a single responsibility and use appropriate access levels such as `private`, `private static`, or `async` when matching the original language and project style.

## Procedure

Validation is `CRITICAL`: tests are `FAILED` unless the summary proves zero failures. It is `MANDATORY` that related tests `MUST` be checked; `NEVER` assume pass/fail status without reading the output.


1. Locate `${input:methodName}` and establish the baseline cognitive complexity if tooling is available.
2. Identify extraction opportunities: validation, type-specific processing, transformations, calculations, repeated code, and complex predicates.
3. Extract helper methods before rewriting the main flow, keeping helpers close to where they are used.
4. Simplify the main method with guard clauses, smaller orchestration calls, or switch expressions/statements where appropriate for the language and project.
5. Preserve input/output behavior, validation, exception types, exception messages, null handling, empty collection behavior, ordering, and side effects.
6. Compile with the project's existing build command or smallest available compile check.
7. Run related existing tests.
8. Read the test output summary and explicitly verify it contains `failed=0`, `pass/fail` counts, or the framework's exact zero-failure equivalent.
9. If failures appear, analyze each failure, fix the refactor, rerun tests, and repeat until zero failures.
10. Re-check cognitive complexity and confirm it is at or below `${input:complexityThreshold}`.

## Implementation rules

| Rule | Required behavior |
| --- | --- |
| Helper scope | Make helpers `static` only when they do not need instance state. |
| Parameter passing | Pass required values explicitly; do not add shared mutable state to avoid parameters. |
| Return values | Use tuples or small result objects only when they clarify multiple outputs and fit project conventions. |
| Local variables | Avoid unnecessary locals introduced only by extraction. |
| Error handling | Preserve original exception types and messages unless tests or user request demand a change. |
| Test repair | If tests fail, assume the refactor changed behavior until proven otherwise. |

## Gotchas

- **Running tests is not verification**: inspect the actual summary and confirm `failed=0`; do not infer success from command exit alone.
- **Null and empty collections break easily**: compare original guard behavior before extracting predicates.
- **Exception messages are behavior**: preserving type but changing message can still break callers or tests.
- **Complexity tools differ**: if no analyzer is available, report the structural changes and the closest available evidence.

## Output template

```markdown
## Complexity refactor result

**Status:** complete | tests failing | blocked
**Method:** <methodName>
**Target complexity:** <complexityThreshold>
**Final complexity:** <value or "not measured">

### Refactoring summary
- <helper extracted and responsibility>
- <control-flow simplification>

### Validation
- Compile: pass | fail | not available — <evidence>
- Tests: pass | fail | not run — <command and summary containing failed=0>
- Behavior notes: <preserved validation/error/null behavior>
```

## Quality gate

- [ ] The method name and complexity threshold were resolved from `$ARGUMENTS`, placeholders, selection, or user input.
- [ ] Complexity sources were identified before extraction.
- [ ] Extracted helpers are focused, named by responsibility, and use appropriate access levels.
- [ ] Original functionality, validation, error handling, exception types, and exception messages are preserved.
- [ ] Code compiles without errors.
- [ ] Existing related tests were run and the output was read to verify `failed=0`.
- [ ] Any failed tests were analyzed, fixed, and rerun until zero failures.
- [ ] Cognitive complexity is at or below the target threshold, or the inability to measure is explicitly reported.
- [ ] The output follows `## Output template` exactly.

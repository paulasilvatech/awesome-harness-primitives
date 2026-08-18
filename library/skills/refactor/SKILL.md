---
name: "refactor"
description: >-
  Improve existing code through surgical behavior-preserving refactoring. Use this skill when code is hard to understand or maintain, functions or classes are too large, code smells need addressing, adding features is difficult due to structure, or the user asks to clean up, refactor, or improve code without changing behavior.
license: "MIT"
---

# Refactor

Improve code structure, readability, and maintainability without changing external behavior. Treat refactoring as gradual evolution: identify one smell, apply one safe transformation, prove behavior stayed the same, then repeat.

## When to invoke

- "Refactor this function without changing behavior."
- "Clean up this code and make it easier to maintain."
- "This class is too large; split it safely."
- "Remove duplication and code smells from this module."
- "Improve this structure before I add a feature."

## Prerequisites and context

- Prefer existing automated tests. If none cover the target behavior, add characterization tests before changing structure.
- Work on a clean branch or record the current state with version control before substantial changes.
- Read `references/smells-patterns-operations.md` when selecting a concrete smell, pattern, or operation.

## Safe refactoring workflow

1. **Prepare**: inspect the current behavior, run or add tests, and note the current `git status`.
2. **Identify**: name the specific code smell, affected files, risk level, and intended refactoring operation.
3. **Refactor in small steps**: make one transformation at a time, such as Extract Function, Rename Variable, Move Method, Introduce Parameter Object, or Replace Conditional with Polymorphism.
4. **Verify after each step**: run the smallest relevant tests; if behavior changes, revert or narrow the step.
5. **Clean up**: update comments and documentation only where the structure or public API changed.

## Refactoring rules

| Rule | Apply it by | Failure signal |
| --- | --- | --- |
| Behavior is preserved | Keep public inputs, outputs, side effects, errors, and timing assumptions equivalent unless the user explicitly asks otherwise. | Tests require assertion changes that are not naming-only. |
| Small steps | Change one abstraction boundary, name, or duplicate cluster at a time. | A diff mixes extraction, feature work, dependency upgrades, and formatting. |
| Version control is your friend | Use `git status` and inspect diffs before and after meaningful steps. | You cannot explain which lines changed for structure only. |
| Tests are essential | Add characterization tests when existing coverage is missing. | You are "editing" critical code without a behavior oracle. |
| One thing at a time | Do not combine refactoring with features, bug fixes, or broad style rewrites. | The output includes new capabilities or altered business rules. |

## Code quality targets

| Area | Target |
| --- | --- |
| Functions | Small enough to scan, usually `< 50 lines`, with one responsibility and a descriptive name. |
| Duplication | Shared behavior extracted only when the duplication is real and stable, not coincidental. |
| Names | Variables, functions, classes, and modules describe domain intent rather than implementation trivia. |
| Constants | Magic numbers and strings become named constants when the value carries business meaning. |
| Structure | Related code is together, module boundaries are clear, and dependencies flow in one direction. |
| Type safety | Public APIs have explicit types; `any` and nullable values are justified and constrained. |
| Dead code | Remove only when tests, references, and search show it is truly unused. |

## Limits

- Do not refactor code that works, is stable, and will not change again without a clear purpose.
- Do not refactor critical production code without tests; add tests first.
- Do not refactor under a tight deadline when the safer move is a localized fix.
- Do not refactor "just because"; tie each change to readability, maintainability, testability, or a planned feature seam.

## Gotchas

- **Changing tests can hide behavior changes**: characterization tests should lock current behavior before restructuring.
- **Large diffs are hard to validate**: prefer many small mechanical changes over one rewrite.
- **Formatting churn obscures intent**: run formatters only if the project already uses them and the diff remains reviewable.
- **Premature abstraction creates worse code**: extract shared code only after the common concept is clear.

## Progressive disclosure and bundled resources

- `references/smells-patterns-operations.md`: open when choosing a specific smell, pattern, operation, or example before editing.

Legacy checklist labels to preserve when mapping older refactor notes: `PREPARE`, `IDENTIFY`, `REFACTOR`, `VERIFY`, and `CLEAN`. Treat Functions/classes or functions/classes complaints as oversized abstractions; treat numbers/strings complaints as magic value smells.

## Output template

```markdown
### Refactor result

**Status:** complete | partially complete | blocked
**Goal:** <maintainability problem addressed>
**Behavior guarantee:** <tests or checks that prove behavior was preserved>

| File | Smell addressed | Refactoring operation | Validation |
| --- | --- | --- | --- |
| `<path>` | `<smell>` | `<operation>` | `<test/check>` |

**Notes**
- <remaining risks or follow-up refactors>
```

## Quality gate

- [ ] The refactoring goal and code smell were named before editing.
- [ ] Existing behavior was understood through tests, characterization tests, or explicit inspection.
- [ ] Each change preserved public behavior, side effects, and error handling.
- [ ] No feature work, bug fix, dependency upgrade, or unrelated formatting was mixed in.
- [ ] Functions, classes, modules, names, duplication, magic values, dead code, and dependency direction were checked where relevant.
- [ ] Relevant tests or build checks passed after the final change.
- [ ] The final response names changed files, operations performed, validation, and remaining risk.

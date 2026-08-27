---
name: review-and-refactor
description: >-
  Review project code against repository instructions, identify maintainability issues, make
  focused refactorings without splitting existing files, and validate tests when available. Use
  this skill when the user asks for code cleanup, maintainability review, best-practice
  refactoring, standards-driven improvements, or a senior engineering pass over existing code.
---

<!-- Generated from harness/github-copilot/skills/review-and-refactor/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Review and refactor

Review the project like a senior maintainer: load repository guidance, inspect code for maintainability defects, apply focused refactorings in place, and validate the existing test suite when available.

## When to invoke

- "Review and refactor this code for maintainability."
- "Clean up this project while following the repo instructions."
- "Do a senior engineering pass and improve code quality."
- "Refactor this without changing behavior."
- "Apply best-practice improvements and run tests if available."

## Prerequisites and context

- Read repository guidance before changing code: `.github/instructions/*.md` and `.github/copilot-instructions.md` when they exist.
- Treat existing code behavior, public APIs, tests, and file layout as compatibility constraints.
- Use the project's existing build, lint, formatter, and test commands only. Do not add tools just to validate a refactor.
- Keep existing files intact: do not split code into new files or relocate modules unless the user explicitly asks.

## Procedure

1. Read applicable repository instructions from `.github/instructions/*.md` and `.github/copilot-instructions.md`.
2. Inspect the target code and determine the smallest behavior-preserving refactor that improves maintainability.
3. Preserve public interfaces, serialization shapes, route names, command names, and configuration keys unless the user explicitly requested an API change.
4. Refactor in place. Keep the existing files intact and avoid broad rewrites that obscure the real change.
5. Run the narrowest existing validation that covers the changed area. If no test command exists, perform a syntax, type, or build check when the project already provides one.
6. Report what changed, what was intentionally left unchanged, and which validation passed or failed.

## Refactoring criteria

| Area | Improve when | Preserve |
| --- | --- | --- |
| Naming | A name hides intent, mixes domains, or requires comments to explain | Public names consumed outside the edited unit unless migration is requested |
| Control flow | Nested conditionals, duplicated branches, or early error cases obscure the main path | Error semantics, ordering side effects, and short-circuit behavior |
| Duplication | Same calculation, validation, or mapping appears in multiple places | Deliberate duplication that isolates unrelated modules |
| Boundaries | A function has mixed abstraction levels or unrelated responsibilities | Existing file boundaries and module exports |
| Data handling | Transformations are implicit, repeated, or untyped where the language supports types | Wire formats, config keys, database schema, and persisted values |
| Tests | Behavior lacks coverage for the changed branch and tests already exist nearby | Test style, fixtures, naming conventions, and runner |

## Safe refactoring patterns

- Extract a local helper only when it reduces duplication or clarifies a repeated operation inside the same file.
- Replace comments that restate code with clearer names or simpler structure; keep comments that explain non-obvious constraints.
- Normalize guard clauses when they reduce nesting without changing execution order.
- Consolidate repeated literals into local constants when the value has domain meaning.
- Prefer small, reviewable edits over formatting an entire file.
- Keep imports sorted according to the repository's existing formatter or style.

## Anti-patterns

| Anti-pattern | Why it is wrong | Safer alternative |
| --- | --- | --- |
| Architecture churn | Moving files or splitting modules creates review noise and hidden breakage | Refactor within existing files unless explicitly authorized |
| Opportunistic feature work | New behavior makes validation ambiguous | Keep behavior unchanged and note future improvements separately |
| Style-only mass rewrite | Formatting unrelated lines hides the meaningful diff | Touch only code needed for the refactor |
| Ignoring instructions | Repository rules may override generic clean-code preferences | Load `.github/instructions/*.md` and `.github/copilot-instructions.md` first |
| Untested semantic change | A refactor that changes behavior is a bug unless requested | Run targeted tests or document the absence of validation |

## Gotchas

- **Do not split up the code**: the skill explicitly keeps existing files intact, so extraction into new modules is out of scope unless the user changes the task.
- **Instructions beat personal preference**: repository guidance can require patterns that look unusual; follow it over generic style advice.
- **Refactoring is not redesign**: preserve behavior and public contracts even when a different architecture would be cleaner.
- **Validation must be existing**: do not introduce a new linter, formatter, test framework, or dependency solely for this review.

## Output template

```markdown
## Review and refactor result

**Status:** complete | blocked
**Scope:** <files or project area reviewed>
**Instructions read:** `.github/instructions/*.md` <found/missing>, `.github/copilot-instructions.md` <found/missing>

### Changes made
| File | Refactor | Behavior impact |
| --- | --- | --- |
| `<path>` | <maintainability improvement> | none | <intentional change if requested> |

### Validation
| Command | Result | Evidence |
| --- | --- | --- |
| `<command or "not available">` | pass | fail | not run | <summary> |

### Notes
- <intentional non-change, blocker, or follow-up>
```

## Quality gate

- [ ] `.github/instructions/*.md` and `.github/copilot-instructions.md` were read when present.
- [ ] The refactor preserves existing behavior unless the user explicitly requested a behavior change.
- [ ] Existing files remain intact; no module split or relocation was performed.
- [ ] Public APIs, serialized formats, configuration keys, and file paths are preserved.
- [ ] The diff is focused on maintainability and avoids unrelated formatting churn.
- [ ] Existing tests, build, lint, or syntax checks were run when available.
- [ ] Any missing validation path is reported explicitly.

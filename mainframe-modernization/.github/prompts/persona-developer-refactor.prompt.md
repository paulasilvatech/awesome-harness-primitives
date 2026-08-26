---
name: "refactor"
description: "Improve internal structure behind passing tests without changing observable behavior or breaking REQ-ID traceability."
argument-hint: "target=<file-or-package> smell=<code-smell>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /refactor

## Objective

Improve the internal structure of existing code without changing what it does. A change that alters behavior is not a refactor—it belongs in `/implement` or `/fix-bug`. The result leaves every existing test passing with the same names and every `REQ-ID` link intact: one smell, one move, one PR.

> [!WARNING]
> If any output, assertion, or public signature changes, it is not a refactor. Stop and use `/implement` or `/fix-bug`.

## When to Invoke

When a named code smell is slowing the team down and the target has (or can quickly get) a passing test safety net. Run it on a dedicated `impl/<NNN>-<feature>` branch, separate from any feature or bug work.

## Preconditions

- The target file, package, or component exists and builds
- Its tests currently pass, or characterization tests can be added first
- No `/fix-bug` is pending on the same code—defects are fixed before refactoring from a clean baseline
- Any constraints in `plan.md` or ADRs (for example, "controllers stay thin") are known

## Inputs the Team Must Provide

- The target file, package, or component
- The motivation: the observed code smell (Long Method, Duplication, Primitive Obsession, Feature Envy, etc.)
- Any constraints from `plan.md` or ADRs that limit the change
- The area's current test coverage (run a coverage report if it is unknown)
- Ask the user for any missing item.

## What I Will Do

- Confirm the safety net—if line coverage is below 80%, write characterization tests first
- Name the smell precisely from the catalog and cite one or two lines of evidence
- Choose one Fowler move that fits and apply it as a single behavior-preserving step
- Run tests before and after every micro-step, keeping the suite green in each commit
- Move every `@implements REQ-NNN` annotation with its method, unchanged

## What I Will NOT Do

- Refactor without tests—that is a rewrite by another name
- Change behavior under the guise of refactoring—if any output or assertion changes, the work is void
- Make "small improvements" to neighboring code—I stay strictly within the named smell
- Rename or reshape a public API without a migration or deprecation plan
- Combine a refactor with a feature or bug fix in the same PR
- Invent a new behavior the spec does not describe—structural change only; requirement questions go to `/update-spec`

## Output Format

```markdown
### Named smell
Long Method — `FeeService.calculate()` spans 74 lines across three nested branches.

### Chosen refactoring
Extract Method — pull each branch into `applyExemption`, `applyCeiling`, and `applyRounding`.

### Diff
<before/after for every touched file>

### Test results
`./mvnw test` → 12 passing (the same names as before).

### Behavior-preservation note
Public API unchanged. No new throws clauses. No DB migration. No new environment variables.

### Commit message
refactor(fees): extract the fee-calculation steps

Splits calculate() into three private methods. No behavior change.
Refs: REQ-031
```

## Definition of Done

- [ ] Every test that passed before still passes, with the same names
- [ ] No public API change, new exception, or new dependency
- [ ] Coverage does not decrease
- [ ] One smell, one move, one PR
- [ ] All `@implements REQ-NNN` annotations remain present and correct
- [ ] The commit message uses the `refactor:` type and states "no behavior change"

## Prompt Body

You are the `@implementer`. The team wants a behavior-preserving structural improvement. Read [`refactor-safely`](../skills/refactor-safely/SKILL.md) before you start; it owns the safety-net, small-steps, and characterization-test procedures.

**Step 1 — Confirm the safety net.**
Check the target's line coverage. If it is below 80%, write characterization tests that lock in current behavior—including its quirks—before changing anything. Refactoring without tests is rewriting.

**Step 2 — Name the smell precisely.**
Choose from the catalog: Long Method, Large Class, Primitive Obsession, Data Clumps, Feature Envy, Shotgun Surgery, Divergent Change. Cite one or two lines of evidence. "Make it cleaner" is rejected.

**Step 3 — Choose one Fowler move.**
Pick the matching move—Extract Method, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object—and apply exactly one move per commit.

**Step 4 — Run tests before you touch anything.**
Confirm they pass. If any fail or are skipped, fix that first; never refactor a broken build.

**Step 5 — Apply the move.**
Prefer IDE refactoring tools (Extract, Rename, Move). Manual edits must preserve method signatures unless the move is Change Function Declaration with a migration plan.

**Step 6 — Run tests after every micro-step.**
The suite must be green in every commit. If it turns red and you do not know why, revert and take a smaller step. Move each `@implements REQ-NNN` annotation with its method.

**Step 7 — Stop when the smell is gone.**
Resist refactoring neighboring code. Each invocation is one chat, one PR, one smell.

If a genuine behavior change or a new requirement surfaces mid-refactor, stop and route it to `/implement`, `/fix-bug`, or `/update-spec`—do not fold it into this change.

## Invocation Example

```
/refactor target=backend/src/main/java/com/example/app/fees/FeeService.java smell=long-method
```

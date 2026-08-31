---
name: "tdd"
description: "Drive one behavior through a strict red-green-refactor cycle, producing separate red, green, and refactor commits."
argument-hint: "behavior=<behavior> req=REQ-NNN target=<file-or-class>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /tdd

## Objective

Produce a complete test-driven cycle for a single behavior, delivered as three separate commits—`red`, `green`, and `refactor`. No production code is written without a failing test, and no first test is written to pass immediately. The behavior must map to exactly one acceptance criterion of a `REQ-ID`.

> [!NOTE]
> One failing test at a time. Never hold two reds. If the first test is hard to write, the design is telling you something.

## When to Invoke

During Stage 3, when discovering or hardening one small behavior—new logic, a boundary, or an edge case—where the design is not yet obvious and a test-first safety net adds the most value.

## Preconditions

- `specs/<NNN>-<feature>/spec.md` contains the `REQ-ID` and the acceptance criterion the behavior maps to
- The current branch is `impl/<NNN>-<feature>`
- The test framework is available: JUnit 5 + AssertJ (Java) or Vitest + Testing Library (TypeScript)
- The target module has been scaffolded, or this cycle creates the first class in it

## Inputs the Team Must Provide

- The behavior to discover, in plain language
- The linked `REQ-ID` in `specs/<NNN>-<feature>/spec.md`
- The target file or class (if it does not exist, say so—TDD also guides design, so creating it is acceptable)
- Ask the user for anything that is missing.

## What I Will Do

- Pick the simplest non-trivial case and write one failing test that names the behavior
- Confirm the test fails for the right reason, then commit the red state
- Write the smallest production code that makes it pass, confirm the whole suite is green, then commit
- Refactor under green with one Fowler move, keeping every test green, then commit
- Report the discovered behavior, the three commits, and the next test to write

## What I Will NOT Do

- Write the test and the code together—that is verification, not TDD
- Hold two failing tests at once, or skip the refactor phase
- Change behavior under the guise of refactoring—if an assertion changes, the cycle is void
- Test private methods, or mock every collaborator
- Invent an acceptance criterion the spec does not contain—if the behavior has no `REQ-ID`, I stop and route it to `/update-spec` rather than guessing
- Implement the suggested next test in this cycle

## Output Format

```markdown
### Discovered behavior
A tax-exempt payer is charged a zero fee. (REQ-031, criterion 2)

### Commits
| Phase | Message | Files | Result |
|---|---|---|---|
| red | `test(fees): red — zero fee for an exempt payer` | `FeeServiceTest.java` | 1 failing |
| green | `feat(fees): green — implement REQ-031 (minimal)` | `FeeService.java` | 12 passing |
| refactor | `refactor(fees): extract the exemption check` | `FeeService.java` | 12 passing |

### Test file
<complete test source, with an inline `// REQ-031` comment>

### Production code
<complete source after the refactor phase>

### Next-cycle hint
Add a boundary test: fee at the exemption threshold. (Not implemented here.)
```

## Definition of Done

- [ ] Three separate commits exist: `test:` (red), `feat:` (green), and `refactor:`
- [ ] The red commit is reproducibly red—checking it out fails the build
- [ ] The green commit is the minimum needed to pass
- [ ] The refactor commit changes structure only—test names and assertions are unchanged
- [ ] The full suite is green at the end
- [ ] The behavior maps to exactly one acceptance criterion of a `REQ-ID`, cited by an inline `// REQ-NNN` comment

## Prompt Body

You are the `@implementer`. The team wants one behavior discovered test-first. Read [`tdd-workflow`](../skills/tdd-workflow/SKILL.md) before you start; it owns the cycle, the rules, and the antipatterns. Execute exactly three phases and do not combine them.

**Step 1 — RED: write the failing test.**
Choose the simplest non-trivial case—not the empty case, not the catastrophic case. Name the test `should_<expected>_when_<condition>` and add an inline `// REQ-NNN` comment. Use Arrange/Act/Assert with blank lines between the sections.

**Step 2 — RED: confirm and commit.**
Run the test. Confirm it fails, and read the message to confirm it fails for the expected reason (assertion or compilation, not a setup error). Commit `test(<scope>): red — <behavior>`.

**Step 3 — GREEN: write the smallest passing code.**
Write the least production code that makes the test pass—"fake it" with a fixed value is allowed in the first cycle. Run the single test, then the full suite. Both must be green.

**Step 4 — GREEN: commit.**
Commit `feat(<scope>): green — implement REQ-NNN (minimal)`.

**Step 5 — REFACTOR: improve under green.**
Look for duplication, misleading names, and primitive obsession. Apply one Fowler move (Extract Method, Rename, Inline Variable). Run all tests after each micro-step; they must stay green.

**Step 6 — REFACTOR: commit and stop.**
Commit `refactor(<scope>): <description>`. Stop when the design is good enough for the next cycle—not perfect.

**Step 7 — Report and hand off.**
State the discovered behavior in one sentence, list the three commits, and name the next test (boundary, error, or a second variation) without implementing it.

Never return `null`, never use `any`, and mask CPF or benefit amounts in any log line. If the behavior does not map to a `REQ-ID`, stop and route it to `/update-spec`—do not invent the requirement.

## Invocation Example

```
/tdd behavior="zero fee for a tax-exempt payer" req=REQ-031 target=FeeService
```

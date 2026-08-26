---
name: "create-tests"
description: "Generate a complete JUnit 5 or Vitest test class for one REQ-ID, covering happy-path, boundary, and negative cases."
argument-hint: "req=REQ-NNN class=<ClassUnderTest> framework=junit|vitest"
agent: "qa-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /create-tests

## Objective

Produce the test class for **one specific `REQ-ID`** in SIFAP 2.0. The output is ready-to-paste JUnit 5 (Java) or Vitest (TypeScript) covering the happy path, boundaries, and negative cases — and nothing more. The tests are written *during* implementation, carry the `REQ-ID` so CI can trace them, and fail with meaningful messages until production code exists. This prompt does not implement production code or edit the spec.

## When to Invoke

Right after `/test-strategy` assigns the `REQ-ID` to a layer, at the start of the red-green-refactor cycle for that requirement — before the production code is written, so the test drives the implementation.

## Preconditions

- The `REQ-ID` exists in `specs/<NNN>-<feature>/spec.md` with a complete EARS statement and acceptance criteria
- The target class or component is named (it may still be a stub)
- The test framework and any existing fixtures are known

## Inputs the Team Must Provide

- The `REQ-ID`, its full EARS statement, and its acceptance criteria
- The class or component under test
- The framework: JUnit 5 + AssertJ + Mockito (backend) or Vitest + Testing Library (frontend)
- Existing fixtures or builders to reuse (`src/test/resources/fixtures/`, `__fixtures__/`)

Ask the user for anything that is missing.

## What I Will Do

- Read [`../skills/tdd-workflow/SKILL.md`](../skills/tdd-workflow/SKILL.md) and drive the tests from behavior, not implementation
- Decompose the EARS statement into happy-path, boundary, and negative cases
- Reuse existing fixtures; never copy real PII
- Name every test by behavior and tag it with the `REQ-ID`
- Generate the complete, compilable test file plus any new fixture builder
- Run the tests and report that they fail for the right reason before implementation

## What I Will NOT Do

- Invent SIFAP behavior or expected values — every assertion is derivable from the EARS statement and acceptance criteria; unknown legacy edge cases are flagged for the team, never guessed
- Write or modify production code (`@builder` / `@implementer`) or change the requirement (`@requirements-engineer`)
- Emit a test without a `REQ-ID` tag — the `spec-traceability` job in `.github/workflows/spec-quality.yml` would not see it
- Put real PII or production credentials in fixtures
- Assert implementation details (private fields, exact SQL strings, log-message text) or use `Thread.sleep` / `setTimeout` for synchronization

## Output Format

Returned inline for review (nothing is committed automatically):

1. A test plan mapping each acceptance criterion to a test method:

```markdown
| Acceptance criterion | Test method | Type |
|----------------------|-------------|------|
| Valid request is accepted | should_accept_when_input_is_valid | happy path |
| Amount below the minimum is rejected | should_reject_when_amount_below_minimum | boundary |
| Mandatory field absent is rejected | should_reject_when_field_absent | negative |
```

2. The complete test file (illustrative shape):

```java
@Tag("REQ-014") // spec-quality.yml scans backend/src/test for REQ-IDs
class AmountRuleTest {

    @Test
    void should_reject_when_amount_below_minimum() {
        var rule = new AmountRule();

        var result = rule.evaluate(BigDecimal.ZERO);

        assertThat(result.rejected())
            .as("REQ-014: amounts at or below the minimum are rejected")
            .isTrue();
    }
}
```

3. Any new fixture builder (as a separate file).
4. The exact execution command, verified in the project (for example `./mvnw test -Dtest=AmountRuleTest`).
5. The expected failure messages the team should see before implementation.

## Definition of Done

- [ ] Every acceptance criterion has at least one named test
- [ ] At least one boundary case and one negative case are included
- [ ] Every test carries the `REQ-ID` as a tag and in the assertion description
- [ ] Tests fail before implementation, for the correct reason, with clear messages
- [ ] No production code is changed
- [ ] No real PII or production credentials appear in fixtures
- [ ] The test file compiles and runs in isolation

## Prompt Body

You are the `@qa-engineer`. The team has a requirement and a stub, and needs failing tests that describe the behavior before the code is written.

**Step 1 — Load the TDD discipline.**
Read [`../skills/tdd-workflow/SKILL.md`](../skills/tdd-workflow/SKILL.md). Start from the simplest nontrivial case, then add one variation at a time.

**Step 2 — Break the EARS statement into cases.**
Ubiquitous (`The system shall ...`) → 1 happy path + 1 boundary. Event-driven (`When ...`) → 1 happy path + 1 negative ("the event did not occur, so nothing changes"). State-driven (`While ...`) → 1 case per transition (in-state, exit-state, re-entry). Optional (`Where ...`) → flag on and flag off. Unwanted (`If ..., then the system shall not ...`) → at least 2 negative cases at different boundaries.

**Step 3 — Choose fixtures, not production data.**
Reuse existing builders; never copy real PII. Build fresh data per test — no shared mutable fixture state.

**Step 4 — Name tests by behavior.**
Use `should_<expected>_when_<condition>` (camelCase method names in JUnit, snake_case descriptions in Vitest). Structure the body as Arrange-Act-Assert or Given-When-Then so a reviewer reads it in ten seconds.

**Step 5 — Assert richly and tag the requirement.**
Use AssertJ chains (`assertThat(x).isEqualTo(y).as("REQ-XXX ...")`), never `assertTrue(x.equals(y))`. Tag with `@Tag("REQ-XXX")` in JUnit or `describe('REQ-XXX', ...)` in Vitest so `.github/workflows/spec-quality.yml` can trace the test.

**Step 6 — Mock only your own collaborators.**
Repositories, yes; framework classes, value objects, and pure functions, no. Do not mock the class under test.

**Step 7 — Run the tests.**
Execute the isolated command and confirm every test fails with a meaningful message (until `/speckit.implement` writes the production code). Report the exact command and the expected failures.

Every test carries its `REQ-ID`, fails first for the right reason, and touches no production code. No real PII enters a fixture. If an expected value cannot be derived from the spec, mark it as a `@Disabled` mystery and ask the team — do not fabricate it.

## Invocation Example

```
/create-tests req=REQ-NNN class=<ClassUnderTest> framework=junit
```

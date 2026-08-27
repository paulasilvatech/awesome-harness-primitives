---
description: >-
  Design or review JUnit 5 unit tests with parameterized tests, assertions, mocking, and
  maintainable organization.
argument-hint: "target=<class-or-test-file> scope=<unit-or-component>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

<!-- Generated from harness/github-copilot/prompts/java-junit.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /java-junit

## Objective

Design or review JUnit 5 unit tests for a Java class, package, or selected code so the tests are focused, maintainable, independent, and executable through the repository's existing Maven or Gradle workflow.

## When to Invoke

Use this prompt when adding new unit tests, refactoring existing JUnit tests, or reviewing whether Java tests cover behavior without coupling to execution order or implementation details.

## Preconditions

- The target Java production code or existing test file is available in the workspace.
- The project uses, or is intended to use, JUnit 5 through Maven or Gradle.
- Test changes are permitted in `src/test/java` or the repository's established test source tree.
- Existing project conventions, dependencies, and test commands are preferred over new tooling.

## Inputs the Team Must Provide

- `target` — the class, package, selected code, or test file to test or review.
- `scope` — `unit`, `component`, or another explicit boundary for what the tests may exercise.
- Existing build tool context — Maven or Gradle, including the command used to run the relevant tests.
- Any required collaborators, edge cases, or behavior that must be covered.
- Ask the user for anything that is missing, especially the target or test scope, and stop before editing if the missing information would change the test design.

## What I Will Do

- Inspect the target behavior and the existing test style before writing or changing tests.
- Place tests in the standard test source tree and follow the repository's Maven or Gradle layout.
- Use JUnit Jupiter annotations, assertions, lifecycle hooks, and parameterized sources where they improve clarity.
- Structure tests around Arrange-Act-Assert and one behavior per test.
- Use Mockito or the project's existing mocking framework to isolate dependencies when unit tests require test doubles.
- Run the smallest existing Maven or Gradle test command that validates the affected tests when command execution is available.

## What I Will NOT Do

- Add integration-test infrastructure, containers, external services, or database dependencies for a unit-test request.
- Change production code solely to make tests pass unless the requested scope includes implementation fixes.
- Introduce a new assertion or mocking library when the project already has a clear standard.
- Depend on test execution order except when an existing ordered-test contract is explicit and justified.
- Hide unstable tests with `@Disabled` without a reason and a clear follow-up.
- Test multiple unrelated behaviors in one method or assert private implementation details instead of observable behavior.

## Output Format

Return or apply the test changes, then report the result in this format:

```markdown
## JUnit Test Result

### Target
- `src/main/java/com/example/Calculator.java`

### Tests Added or Updated
- `CalculatorTests.add_should_returnSum_when_inputsArePositive`
- `CalculatorTests.divide_should_throwArithmeticException_when_divisorIsZero`
- `CalculatorTests.isValid_should_matchExpectedResult_when_valueComesFromCsvSource`

### Practices Applied
- Arrange-Act-Assert structure
- `@ParameterizedTest` with `@CsvSource`
- `assertThrows` for exception behavior
- Mockito isolation for `RateProvider`

### Validation
- Command: `mvn -Dtest=CalculatorTests test`
- Result: passed

### Notes
- No ordered tests were introduced.
```

## Definition of Done

- [ ] Tests compile under the repository's existing Maven or Gradle configuration.
- [ ] Test classes and methods use clear names that describe behavior and scenario.
- [ ] Each test focuses on one behavior and can run independently in any order.
- [ ] Parameterized tests are used for meaningful data variation, not for unrelated cases.
- [ ] Assertions are specific, readable, and include exception checks where behavior requires them.
- [ ] Mocks isolate external dependencies without mocking the unit under test.
- [ ] The relevant existing test command was run, or the reason it could not run is reported.

## Prompt Body

Follow these steps in order. Preserve existing project conventions unless they conflict with reliable JUnit 5 unit testing.

**Step 1 — Confirm the test boundary.**
Identify the class, method, package, or selected code under test. Determine whether the requested scope is a unit test or a broader component test. If the target or boundary is unclear, ask for it before editing.

**Step 2 — Check the project setup.**
Use the existing Maven or Gradle structure. Prefer `src/test/java` for test source code. Confirm that JUnit Jupiter is already available or expected through `junit-jupiter-api`, `junit-jupiter-engine`, and `junit-jupiter-params` when parameterized tests are needed. Use the repository's existing commands, usually `mvn test`, a targeted `mvn -Dtest=... test`, `gradle test`, or a targeted Gradle test task.

**Step 3 — Name and organize the tests.**
Use a `Test` or repository-standard suffix such as `CalculatorTests` for `Calculator`. Group tests by feature or component using packages. Use descriptive method names such as `methodName_should_expectedBehavior_when_scenario`. Add `@DisplayName` to clarify classes or methods when it improves readability.

**Step 4 — Structure each standard test.**
Use `@Test` for single-scenario tests. Apply Arrange-Act-Assert. Keep each method focused on one behavior. Avoid combining multiple conditions in one test. Keep tests independent, idempotent, and free of interdependencies.

**Step 5 — Use lifecycle hooks carefully.**
Use `@BeforeEach` and `@AfterEach` for per-test setup and teardown. Use `@BeforeAll` and `@AfterAll` for per-class setup and teardown, with static methods when required by the test instance lifecycle. Do not hide important Arrange steps in shared setup when doing so makes individual tests unclear.

**Step 6 — Add data-driven tests when the behavior varies by input.**
Use `@ParameterizedTest` for repeated behavior over multiple inputs. Use `@ValueSource` for simple literal values, `@CsvSource` for inline tabular examples, `@CsvFileSource` for classpath CSV data, `@EnumSource` for enum constants, and `@MethodSource` when arguments need a factory method that returns a `Stream`, `Collection`, or equivalent supported source.

**Step 7 — Choose precise assertions.**
Use static methods from `org.junit.jupiter.api.Assertions`, such as `assertEquals`, `assertTrue`, `assertNotNull`, `assertThrows`, and `assertDoesNotThrow`. Use AssertJ only when the project already uses it or when adding it is explicitly approved. Group related assertions with `assertAll` so one failure does not hide other checks. Add descriptive assertion messages when they clarify a failure.

**Step 8 — Isolate dependencies with mocks.**
Use Mockito or the repository's existing mocking framework for collaborators that make the test slow, nondeterministic, or external. Use `@Mock` and `@InjectMocks` when they simplify mock creation and injection. Prefer interfaces for mockable dependencies. Do not mock value objects or the behavior of the unit under test.

**Step 9 — Organize larger test classes.**
Use `@Nested` to group related scenarios. Use `@Tag` for categories such as `fast` or `integration` when the repository uses tags. Use `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` and `@Order` only when ordering is strictly necessary and documented. Use `@Disabled` only with a reason.

**Step 10 — Validate and report.**
Run the narrowest existing test command that covers the changed tests. If execution is unavailable, report the exact command that should be run and why it was not run. Summarize changed tests, practices applied, and any remaining coverage gaps.

## Invocation Example

```
/java-junit target=src/main/java/com/example/Calculator.java scope=unit
```

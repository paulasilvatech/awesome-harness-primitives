---
name: "java-junit"
description: "Write effective JUnit 5 unit and parameterized tests, deferring the best-practice checklist to the java-junit skill."
argument-hint: "class=<ClassUnderTest>"
agent: "qa-engineer"
tools: ["read", "search", "edit"]
---
# /java-junit

## Objective

Produce focused JUnit 5 tests — standard and parameterized — for a class or behavior, following Arrange-Act-Assert, descriptive naming, proper isolation, and REQ-ID traceability. The best-practice checklist lives in the [`java-junit`](../skills/java-junit/SKILL.md) skill; this prompt applies it to the SIFAP 2.0 backend without restating it.

> [!IMPORTANT]
> Write the tests alongside the code, never after the fact — the kit forbids retrofitted tests.

## When to Invoke

During Stage 3/4, while implementing backend business logic, once the behavior under test is defined by a REQ-ID and its acceptance criteria.

## Preconditions

- The class or behavior under test exists or is being written in the same change
- The backend module has `junit-jupiter` and `testcontainers` on the test classpath
- The REQ-ID(s) the tests must cover are known

## Inputs the Team Must Provide

- `class` — the class (or behavior) under test, for example `PaymentService`
- The REQ-ID(s) and acceptance criteria the tests must satisfy
- Ask the user for anything that is missing.

## What I Will Do

- Follow the JUnit 5 practices in the [`java-junit`](../skills/java-junit/SKILL.md) skill, applying them to the class under test
- Write one test per acceptance criterion, named `should_<expected>_when_<condition>`, each carrying an inline `// REQ-NNN` comment
- Use `@ParameterizedTest` with `@MethodSource`/`@CsvSource` for data-driven cases and Mockito for collaborators
- Use Testcontainers (real PostgreSQL 16) for anything that touches the database

## What I Will NOT Do

- Write tests after the production code, or skip a case for any acceptance criterion
- Substitute an in-memory database for the Testcontainers PostgreSQL integration path
- Test multiple behaviors in one method, or rely on test execution order
- Leave a test without a REQ-ID comment (it breaks spec-traceability)

## Output Format

A JUnit 5 test class, each case traceable to a REQ-ID:

```java
// REQ-042: reject inactive beneficiary
@Test
@DisplayName("rejects a payment line for an inactive beneficiary")
void should_reject_when_beneficiary_is_inactive() {
    // Arrange - Act - Assert
}
```

## Definition of Done

- [ ] One test exists per acceptance criterion of every linked REQ-ID
- [ ] Every test carries an inline `// REQ-NNN` comment
- [ ] Data-driven cases use `@ParameterizedTest`; collaborators are mocked
- [ ] Database tests use Testcontainers; `./mvnw test` is green

## Prompt Body

The [`java-junit`](../skills/java-junit/SKILL.md) skill owns the standard and parameterized-testing conventions — read it, then apply them to the class under test.

**Step 1 — Map the behavior.**
List every acceptance criterion for the linked REQ-IDs; each becomes one test.

**Step 2 — Apply the skill.**
Write the tests per the skill (AAA, `@DisplayName`, `assertAll`, `assertThrows`, `@ParameterizedTest`), mocking collaborators with Mockito.

**Step 3 — Respect the kit rules.**
Use Testcontainers with PostgreSQL 16 for database paths, add a `// REQ-NNN` comment to each test, and build with `./mvnw test`.

**Step 4 — Verify.**
Run the suite and confirm every case passes for the right reason.

## Invocation Example

```
/java-junit class=PaymentService
```

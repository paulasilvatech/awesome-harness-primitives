---
name: java-junit
description: >-
  Apply JUnit 5 best practices for Java tests, including Maven or Gradle setup, standard and
  parameterized tests, lifecycle hooks, assertions, Mockito isolation, tags, nested tests, and
  test commands. Use when asked for JUnit 5+ guidance or to write Java unit tests.
---

<!-- Generated from harness/github-copilot/plugins/mainframe-natural-adabas-classic/skills/java-junit/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# JUnit 5 testing

Guide Java test implementation by turning behavior requirements into focused JUnit 5 tests that use idiomatic project structure, per-test lifecycle hooks, data-driven parameterized data, assertions, mocking, human-readable organization, and build-tool validation.

## When to invoke

- "Write JUnit 5 tests for this Java class."
- "Show junit 5+ best practices for parameterized tests."
- "Convert these examples to `@ParameterizedTest`."
- "How should I use Mockito, tags, and nested tests in JUnit?"

## Project setup

| Concern | Rule |
| --- | --- |
| Structure | Use standard Maven or Gradle layout; put tests in `src/test/java`. |
| Dependencies | Include `junit-jupiter-api`, `junit-jupiter-engine`, and `junit-jupiter-params` for parameterized tests. |
| Commands | Run `mvn test` or `gradle test`; narrow with build-tool filters when needed. |
| Class names | Use a `Test` suffix, for example `CalculatorTest` for `Calculator`. |

## Test structure

| Feature | Use | Notes |
| --- | --- | --- |
| `@Test` | Standard test methods. | One behavior per test. |
| Arrange-Act-Assert | Test body shape. | Keep setup, action, and verification clear. |
| `methodName_should_expectedBehavior_when_scenario` | Descriptive naming. | Match existing project style if stronger. |
| `@BeforeEach` / `@AfterEach` | Per-test setup and teardown. | Reset mutable state. |
| `@BeforeAll` / `@AfterAll` | Per-class setup and teardown. | Static by default unless using a per-class lifecycle. |
| `@DisplayName` | Human-readable class or method names. | Useful for business-readable scenarios. |
| `@Nested` | Group related scenarios. | Keeps context-specific setup close to tests. |

## Data-driven tests

| Source | Use it for | Notes |
| --- | --- | --- |
| `@ParameterizedTest` | Any test run with multiple input rows. | Pair with exactly one source. |
| `@ValueSource` | Simple literal strings, ints, longs, doubles, classes, or booleans. | Best for one-parameter tests. |
| `@MethodSource` | Factory method returning `Stream`, `Collection`, iterable, or arguments. | Best for computed or named cases. |
| `@CsvSource` | Small inline comma-separated rows. | Keep rows readable. |
| `@CsvFileSource` | CSV file from the classpath. | Use for larger stable datasets. |
| `@EnumSource` | Enum constants. | Filter modes are useful for subsets. |

## Assertions and exceptions

| Need | Assertion |
| --- | --- |
| Equality | `assertEquals(expected, actual)`; baseline form `assertEquals`. |
| Truthiness | `assertTrue`, `assertFalse`. |
| Nullability | `assertNotNull`, `assertNull`. |
| Exception path | `assertThrows`. |
| No exception path | `assertDoesNotThrow`. |
| Multiple related checks | `assertAll` so all assertions run before failure. |
| Fluent style | AssertJ `assertThat(...).is...` only if the project already uses or accepts AssertJ. |

Import static methods from `org.junit.jupiter.api.Assertions`. Add descriptive messages when they make failure diagnostics clearer.

## Mocking and organization

| Technique | Use when | Avoid |
| --- | --- | --- |
| Mockito | Collaborators need isolation. | Mocking value objects or the class under test. |
| `@Mock` | Declare mock dependencies. | Manual mock setup repeated across tests. |
| `@InjectMocks` | Construct class under test from mocks. | Hiding complex construction that should be explicit. |
| Interfaces | Facilitate mocking and substitutions. | Introducing interfaces solely for trivial classes. |
| Packages | Group tests by feature or component. | Dumping all tests into one utility package. |
| `@Tag("fast")`, `@Tag("integration")` | Categorize suites; baseline shorthand `@Tag`. | Using tags to hide slow tests instead of fixing scope. |
| `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` and `@Order` | Only when order is strictly necessary. | Routine unit tests; independence is preferred. |
| `@Disabled` | Temporary skip with a reason. | Permanent silent skips. |

## Gotchas

- **Do not rely on execution order**: use `@TestMethodOrder` only for rare ordered workflows, not normal unit tests.
- **Do not mix behaviors in one parameterized test**: every row should verify the same rule.
- **Do not use `@SpringBootTest` for ordinary unit tests**: prefer plain JUnit and Mockito unless a Spring context is required.
- **Do not hide failing cases with `@Disabled`**: include a reason and track follow-up work.

## Output template

```markdown
## JUnit 5 test plan

**Target:** `<class or behavior>`
**Command:** `mvn test` or `gradle test`

| Test | Annotation | Data source | Behavior verified |
| --- | --- | --- | --- |
| `<methodName_should_expectedBehavior_when_scenario>` | `@Test` or `@ParameterizedTest` | `<none / ValueSource / MethodSource / CsvSource / CsvFileSource / EnumSource>` | `<single behavior>` |

### Notes
- Lifecycle: `<BeforeEach/AfterEach/BeforeAll/AfterAll or none>`
- Assertions: `<Assertions or AssertJ>`
- Isolation: `<Mockito mocks or real collaborators>`
```

## Quality gate

- [ ] Tests live in `src/test/java` and run with `mvn test` or `gradle test`.
- [ ] JUnit Jupiter dependencies include `junit-jupiter-api`, `junit-jupiter-engine`, and `junit-jupiter-params` when parameterized tests are used.
- [ ] Tests use `@Test` or `@ParameterizedTest` appropriately and follow Arrange-Act-Assert.
- [ ] Parameterized tests use the smallest suitable source annotation.
- [ ] Assertions are specific and include exception checks with `assertThrows` or `assertDoesNotThrow` where relevant.
- [ ] Mockito, tags, ordering, disabling, and `@Nested` are used only when they clarify the test suite.

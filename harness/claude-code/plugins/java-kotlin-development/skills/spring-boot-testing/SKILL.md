---
name: spring-boot-testing
description: >-
  Select and write effective Spring Boot 4 tests with JUnit 6, AssertJ, MockMvcTester,
  RestTestClient, Testcontainers, and focused test slices. Use when the user asks for Spring Boot
  testing guidance, unit tests, slice tests, integration tests, coverage priorities, migration
  from @MockBean, or testing best practices.
---

<!-- Generated from harness/github-copilot/plugins/java-kotlin-development/skills/spring-boot-testing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Spring Boot testing

Choose the narrowest Spring Boot testing technique that provides confidence, then write maintainable tests with JUnit 6, AssertJ-style assertions, modern Spring Boot 4 test APIs, and meaningful coverage.

## When to invoke

- "Write tests for this Spring Boot controller."
- "Should this use @WebMvcTest or @SpringBootTest?"
- "Migrate these tests from @MockBean to @MockitoBean."
- "Add repository tests with Testcontainers."
- "Improve Spring Boot test coverage without brittle tests."

## Prerequisites and context

- Use the project's existing test runner and build tool.
- Add dependencies only when the project lacks the required Spring Boot test starter.
- Read bundled references for detailed API examples rather than expanding the main skill.

## Test slice selection

| Scenario | Use | Reference |
| --- | --- | --- |
| Controller and HTTP semantics | `@WebMvcTest` with `MockMvcTester` | `references/webmvctest.md`, `references/mockmvc-tester.md` |
| Repository and JPA queries | `@DataJpaTest` with Testcontainers and a real database | `references/datajpatest.md`, `references/testcontainers-jdbc.md` |
| REST client and external APIs | `@RestClientTest` with `MockRestServiceServer` | `references/restclienttest.md` |
| JSON serialization and deserialization | `@JsonTest` | `references/test-slices-overview.md` |
| Business service logic | Plain JUnit plus Mockito, no Spring context | project tests |
| Full application wiring | `@SpringBootTest` with minimal context config | `references/test-slices-overview.md` |
| Spring Boot 4 HTTP integration | `RestTestClient` | `references/resttestclient.md` |

Decision tree:

```text
Testing a controller endpoint? -> @WebMvcTest with MockMvcTester
Testing repository queries? -> @DataJpaTest with Testcontainers (real DB)
Testing business logic in service? -> Plain JUnit + Mockito (no Spring context)
Testing external API client? -> @RestClientTest with MockRestServiceServer
Testing JSON mapping? -> @JsonTest
Need full integration test? -> @SpringBootTest with minimal context config
```

## Core principles

| Principle | Rule |
| --- | --- |
| Test Pyramid | Prefer Unit (fast) > Slice (focused) > Integration (complete). |
| Right Tool | Use the narrowest slice that proves the behavior. |
| AssertJ Style | Prefer fluent, readable assertions over verbose matchers. |
| Modern APIs | Prefer `MockMvcTester` and `RestTestClient` over legacy alternatives when available. |
| Coverage Order | Test main scenario, other valid paths, then exceptions/errors. |
| Refactor signal | If one method needs more than 5-7 test cases, recommend extracting smaller focused functions before adding brittle tests. |

## Spring Boot 4 highlights

- `RestTestClient`: modern alternative to `TestRestTemplate`.
- `@MockitoBean`: replaces deprecated `@MockBean`.
- `MockMvcTester`: AssertJ-style web test assertions.
- Modular starters: technology-specific test starters such as `spring-boot-starter-webmvc-test`.
- Context pausing: Spring Framework 7 can pause cached contexts.

## Test quality rules

- Create helper methods for common objects and mock setup to reduce redundancy.
- Use production-realistic scenarios: payment processing, order validation, discount calculations, error handling, external APIs, and databases.
- Use `@DisplayName` to state behavior: `@DisplayName("Should calculate discount for VIP customer")`.
- Avoid tests that only import classes or execute code without assertions.
- Aim for `80+%` coverage as a practical minimum, but prioritize meaningful assertions over numeric coverage.
- Use the Jacoco Maven plugin for coverage reporting when the project already uses Maven or JaCoCo.

Example display names:

```java
@Test
@DisplayName("Should calculate discount for VIP customer")
void shouldCalculateDiscountForVip() { }

@Test
@DisplayName("Should reject order when customer has insufficient credit")
void shouldRejectOrderForInsufficientCredit() { }
```

## Dependencies

Use only what the project needs:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>

<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-webmvc-test</artifactId>
  <scope>test</scope>
</dependency>

<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
```

## Progressive disclosure and bundled resources

- `references/test-slices-overview.md`: slice decision matrix and comparisons.
- `references/webmvctest.md`: web layer testing with MockMvc.
- `references/datajpatest.md`: data layer tests with Testcontainers.
- `references/restclienttest.md`: REST client testing.
- `references/mockmvc-tester.md`: AssertJ-style MockMvc usage.
- `references/mockmvc-classic.md`: traditional MockMvc for older projects.
- `references/resttestclient.md`: Spring Boot 4 REST client testing.
- `references/mockitobean.md`: dependency mocking with `@MockitoBean`.
- `references/assertj-basics.md`: scalar, string, boolean, and date assertions.
- `references/assertj-collections.md`: list, set, map, and array assertions.
- `references/testcontainers-jdbc.md`: PostgreSQL, MySQL, and JDBC containers.
- `references/instancio.md`: generating complex test objects with 3+ properties.
- `references/context-caching.md`: speeding up test suites.
- `references/sb4-migration.md`: Spring Boot 4 migration notes.

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `Exceptions/Errors**`
- `OrderRequest`
- WebMvc

## Output template

```markdown
## Spring Boot testing result

**Status:** tests-added | guidance-only | blocked
**Test strategy:** <unit/slice/integration and why>

| Target | Test type | Files changed | Main scenarios | Validation |
| --- | --- | --- | --- | --- |
| <class or endpoint> | <@WebMvcTest/@DataJpaTest/plain JUnit/etc.> | <test file> | <happy path, edge, error> | <command and result> |

### Notes
- <coverage, dependency, migration, or refactoring recommendation>
```

## Quality gate

- [ ] The narrowest useful test slice was selected and justified.
- [ ] Tests cover happy path, alternate valid paths, and error conditions where relevant.
- [ ] Assertions verify behavior, not just execution.
- [ ] Existing project conventions, fixtures, and build tools were preserved.
- [ ] `@MockBean` was not introduced for Spring Boot 4 code; use `@MockitoBean` where needed.
- [ ] Coverage goals focus on business-critical paths, complex algorithms, error handling, and integration points.
- [ ] Bundled references were consulted for detailed API usage when necessary.

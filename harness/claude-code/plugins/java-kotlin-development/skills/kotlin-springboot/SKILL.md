---
name: kotlin-springboot
description: >-
  Build, review, and test idiomatic Spring Boot applications written in Kotlin. Use this skill
  when the user asks for Spring Boot with Kotlin best practices, Kotlin JPA entities, coroutine
  controllers, configuration properties, validation, logging, or test slices.
---

<!-- Generated from harness/github-copilot/plugins/java-kotlin-development/skills/kotlin-springboot/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Spring Boot with Kotlin

Use Kotlin language features deliberately in Spring Boot applications: constructor injection, immutable DTOs, type-safe configuration, null-safety, coroutine boundaries, and focused tests. Produce high-quality code or review feedback that keeps Spring conventions while avoiding Java-shaped Kotlin.

## When to invoke

- "Show Spring Boot with Kotlin best practices."
- "Review this Kotlin Spring Boot service."
- "How should I write Kotlin JPA entities?"
- "Add coroutine support to this Spring Boot controller."
- "Set up tests for a Kotlin Spring Boot application."

## Project structure and build setup

| Area | Preferred pattern | Avoid |
| --- | --- | --- |
| Build tool | Use Maven `pom.xml` with `kotlin-maven-plugin`, or Gradle `build.gradle` with `org.jetbrains.kotlin.jvm`. | Mixing Java-only plugin defaults with Kotlin source sets. |
| Spring starters | Add normal starters such as `spring-boot-starter-web` and `spring-boot-starter-data-jpa`. | Replacing starters with hand-picked transitive dependencies. |
| JPA compiler support | Enable `kotlin-jpa` so entity classes become `open` without boilerplate. | Manually marking every entity and member `open` unless the build cannot use the plugin. |
| Package layout | Organize by feature/domain such as `com.example.app.order` and `com.example.app.user`. | Layer-only packages that scatter one feature across unrelated folders. |
| Configuration | Prefer `application.yml`, plus `application-dev.yml` and `application-prod.yml` profiles for environment-specific settings. | Hardcoded environment switches in Kotlin code. |

## Kotlin Spring coding patterns

| Concern | Use this | Why |
| --- | --- | --- |
| Dependency injection | Primary constructor parameters declared `private val`. | Constructor injection is explicit, testable, and idiomatic Kotlin. |
| Mutability | Prefer `val` over `var`; make DTOs immutable `data class` values. | Reduces incidental state and makes request/response models predictable. |
| Components | Keep Spring stereotypes: `@Service`, `@Repository`, `@RestController`. | Kotlin should not hide Spring's component model. |
| Configuration properties | Bind `@ConfigurationProperties` to immutable `data class` properties. | Gives type-safe, validated external configuration. |
| Secrets | Read secrets from environment variables, HashiCorp Vault, AWS Secrets Manager, or another secret manager. | Keeps secrets out of `application.yml` and source control. |
| Validation | Use Bean Validation / JSR 380 annotations such as `@Valid`, `@NotNull`, and `@Size` on request DTOs. | Keeps validation declarative and integrated with Spring MVC. |
| Error handling | Centralize response mapping with `@ControllerAdvice` and `@ExceptionHandler`. | Prevents each controller from inventing a response shape. |

## Web, service, and data layer rules

| Layer | Rule | Detail |
| --- | --- | --- |
| Controllers | Expose clear RESTful APIs with `data class` DTOs. | DTOs supply `equals()`, `hashCode()`, `toString()`, and `copy()` automatically. |
| Services | Put business logic in stateless `@Service` classes. | Keep mutable per-request state in method scope, not service fields. |
| Transactions | Place `@Transactional` on service functions or classes that own a unit of work. | Do not rely on repository method boundaries when multiple writes must commit together. |
| Entities | Define JPA entities as classes, not `data class`, and make them `open` through `kotlin-jpa`. | JPA proxies require non-final classes; data class equality is often wrong for mutable persistence identity. |
| Null safety | Use nullable types with `?` only for optional fields and absent relationships. | Let the type system document required versus optional state. |
| Repositories | Extend `JpaRepository` or `CrudRepository` for Spring Data JPA. | Keep query methods explicit and return nullable values where absence is valid. |
| Coroutines | Use `suspend` at web/service boundaries for non-blocking flows and choose coroutine-capable drivers. | A `suspend` controller still blocks if it calls blocking JDBC on the request thread. |

## Logging and testing

| Topic | Pattern |
| --- | --- |
| Logger | Declare a companion object logger with `LoggerFactory.getLogger(MyClass::class.java)`. |
| Message style | Use parameterized logging such as `logger.info("Processing user {}...", userId)`. |
| Unit tests | Use JUnit 5 by default; add Kotest for fluent assertions and MockK for Kotlin-native mocking when the project already accepts those dependencies. |
| Test slices | Use `@WebMvcTest` for controller slices and `@DataJpaTest` for repository slices. |
| Integration tests | Use Testcontainers for databases, message brokers, and other real dependencies. |
| Coroutine tests | Use structured concurrency with `coroutineScope` or `supervisorScope`; test suspending code with the project's coroutine test utilities. |

## Gotchas

- **Do not use `data class` for JPA entities**: generated equality and `copy()` conflict with persistence identity, proxies, and lazy relationships.
- **Do not skip `kotlin-jpa` for Hibernate entities**: final classes break proxying unless all relevant classes and methods are `open`.
- **Do not treat `suspend` as automatic scalability**: blocking repositories or clients still consume blocking resources.
- **Do not inject optional dependencies as nullable constructor parameters by default**: prefer explicit conditional beans or configuration flags.

## Output template

```markdown
## Kotlin Spring Boot result

**Status:** ready | needs changes | blocked
**Scope:** <project, package, file, or design area>

| Area | Recommendation | Evidence or example |
| --- | --- | --- |
| Build | <plugin/starter/configuration guidance> | `<file or command>` |
| Code | <Kotlin/Spring pattern> | `<class, annotation, or API>` |
| Tests | <test slice or integration strategy> | `<test command or framework>` |

### Next actions
- <concrete change 1>
- <concrete change 2>
```

## Quality gate

- [ ] Constructor injection uses primary constructors and `private val` for required dependencies.
- [ ] Kotlin DTOs and configuration properties are immutable unless mutation is justified.
- [ ] JPA entity guidance accounts for `open` classes and the `kotlin-jpa` plugin.
- [ ] Secrets are kept out of source and configuration files committed to Git.
- [ ] Validation, error handling, transactions, logging, and tests are addressed for the affected layer.
- [ ] Coroutine recommendations distinguish non-blocking APIs from blocking persistence or client calls.

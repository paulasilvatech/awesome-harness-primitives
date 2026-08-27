---
name: java-springboot
description: >-
  Apply Spring Boot best practices for project structure, dependency injection, configuration,
  REST controllers, DTO validation, services, transactions, Spring Data JPA, logging, testing, and
  security. Use when asked for Spring Boot guidance or to implement Java backend code.
---

<!-- Generated from harness/github-copilot/skills/java-springboot/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Spring Boot best practices

Turn Spring Boot implementation requests into high-quality Java applications with domain-oriented packages, explicit dependencies, externalized configuration, validated APIs, transactional services, safe persistence, structured logging, and focused tests.

## When to invoke

- "Show Spring Boot best practices for this service."
- "Refactor this controller, service, and repository."
- "How should I structure a Spring Boot application?"
- "Add validation, error handling, and tests to this Spring Boot endpoint."

## Project setup and package structure

| Concern | Preferred approach | Avoid |
| --- | --- | --- |
| Build tool | Maven `pom.xml` or Gradle `build.gradle`. | Manual dependency jars. |
| Dependencies | Spring Boot starters such as `spring-boot-starter-web` and `spring-boot-starter-data-jpa`. | Hand-picking transitive Spring libraries. |
| Packages | `feature/domain` packages such as `com.example.app.order` and `com.example.app.user`. | Layer-only packages such as `com.example.app.controller`, `com.example.app.service`, and `repository` for every domain. |
| Boundaries | Keep controller DTOs, service logic, repository contracts, and persistence models explicit. | Letting web, persistence, and domain concerns leak into each other. |

## Components and dependency injection

| Need | Use |
| --- | --- |
| Required dependencies | `constructor-based` injection with `private final` fields. |
| General bean | `@Component`. |
| Business operation | `@Service`. |
| Persistence adapter | `@Repository`. |
| MVC page controller | `@Controller`. |
| REST endpoint | `@RestController`. |

Do not use field injection for required collaborators. Constructor injection makes dependencies explicit, testable, and immutable.

## Configuration and secrets

| Concern | Rule |
| --- | --- |
| Files | Use `application.yml` or `application.properties`; prefer YAML for hierarchical settings when the project already uses it. |
| Type safety | Bind settings with `@ConfigurationProperties` to strongly-typed Java objects instead of scattering `@Value` keys. |
| Environments | Use Spring Profiles such as `application-dev.yml` and `application-prod.yml` for environment-specific configuration. |
| Secrets | Do not hardcode secrets. Use environment variables, HashiCorp Vault, AWS Secrets Manager, or the platform's secret store. |

## Web, validation, and error handling

| Area | Practice |
| --- | --- |
| REST API | Use clear resource-oriented endpoints and consistent status codes. |
| DTOs | Expose and consume DTOs; do not return JPA entities directly to clients. |
| Validation | Use Java Bean Validation / JSR 380 annotations such as `@Valid`, `@NotNull`, and `@Size` on request DTOs. |
| Errors | Centralize responses with `@ControllerAdvice` and `@ExceptionHandler`. |
| Sanitization | Prevent SQL injection with Spring Data JPA or parameterized queries; encode output to prevent Cross-Site Scripting (XSS). |

## Services and data access

| Area | Practice |
| --- | --- |
| Business logic | Put business rules in `@Service` classes, not controllers or repositories. |
| Statelessness | Keep services stateless except for injected dependencies. |
| Transactions | Apply `@Transactional` at the most granular service method that owns the unit of work. |
| Repositories | Extend `JpaRepository` or `CrudRepository` for standard persistence. |
| Complex queries | Use `@Query`, the JPA Criteria API, or projections. |
| Read models | Use DTO projections to fetch only needed columns. |

## Logging, tests, and security

| Topic | Rule |
| --- | --- |
| Logging API | Use SLF4J. Declare `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`. |
| Log messages | Prefer parameterized logging: `logger.info("Processing user {}...", userId);`. |
| Unit tests | Use JUnit 5 with Mockito for services and components. |
| Integration tests | Use `@SpringBootTest` when the full application context is required. |
| Test slices | Use `@WebMvcTest` for controllers and `@DataJpaTest` for repositories. |
| External dependencies in tests | Consider Testcontainers for real databases or brokers. |
| Authentication | Use Spring Security for authentication and authorization. |
| Passwords | Encode passwords with BCrypt. |

## Gotchas

- **Do not expose JPA entities from controllers**: lazy-loading, over-posting, and accidental schema coupling follow.
- **Do not put transactions on controllers**: service methods should own business transaction boundaries.
- **Do not concatenate user input into queries**: rely on Spring Data JPA, bound parameters, or criteria APIs.
- **Do not log secrets or raw PII**: parameterized logging helps performance, not data safety.

## Output template

```markdown
## Spring Boot implementation guidance

**Target:** <feature, class, or endpoint>

| Area | Recommendation | Concrete API or file |
| --- | --- | --- |
| Structure | <package/module choice> | `<package>` |
| Web | <controller/DTO/validation rule> | `@RestController`, `@Valid` |
| Service | <business logic and transaction boundary> | `@Service`, `@Transactional` |
| Data | <repository/query/projection rule> | `JpaRepository`, `@Query` |
| Tests | <unit/slice/integration strategy> | `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest` |

### Risks to avoid
- <anti-pattern and correction>
```

## Quality gate

- [ ] Dependencies use Maven or Gradle and Spring Boot starters where appropriate.
- [ ] Required dependencies use constructor injection and `private final` fields.
- [ ] Configuration is externalized through `application.yml` or `application.properties`, with secrets outside source code.
- [ ] Controllers use DTOs, validation, and centralized error handling.
- [ ] Business logic and transactions live in services, with `@Transactional` at the right boundary.
- [ ] Data access uses Spring Data repositories, safe queries, and projections when useful.
- [ ] Tests use the smallest appropriate level: unit, test slice, or integration.

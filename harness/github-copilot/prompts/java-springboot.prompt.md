---
name: 'java-springboot'
description: 'Guide Spring Boot application development with project structure, configuration, web, service, data, logging, testing, and security practices.'
agent: 'agent'
tools: ['read', 'search', 'edit', 'execute', 'web']
---

# /java-springboot

## Objective

Guide Spring Boot application development or review so project structure, dependency injection, externalized configuration, web APIs, service transactions, repositories, logging, testing, and security follow established high-quality Spring practices while preserving the application's chosen stack.

## When to Invoke

Use this prompt when creating, reviewing, or refactoring Spring Boot code, configuration, REST endpoints, services, repositories, tests, or security-sensitive application logic.

## Preconditions

- The Spring Boot target code, module, or selected files are available.
- The project build tool, package convention, persistence approach, and test framework can be inspected or provided.
- Edits are permitted when implementation changes are requested.
- Existing application stack choices take precedence; do not impose a fixed Java, Spring Boot, or database version unless the project already states it.

## Inputs the Team Must Provide

- `target` — the file, package, module, selected code, endpoint, service, or repository to build or review.
- Build context — Maven `pom.xml` or Gradle `build.gradle`, Spring Boot version if known, and test command.
- Persistence, security, configuration, and deployment constraints.
- Ask the user for anything that is missing, especially when missing context would affect edits.

## What I Will Do

- Organize code by feature or domain, such as `com.example.app.order` and `com.example.app.user`, instead of by generic layers when the project allows it.
- Use Spring Boot starters such as `spring-boot-starter-web` and `spring-boot-starter-data-jpa` where they match the application.
- Enforce constructor injection, `private final` dependency fields, appropriate stereotypes, DTO boundaries, Bean Validation, and global exception handling.
- Keep business logic in stateless `@Service` classes and place `@Transactional` at the most granular service method level.
- Use Spring Data JPA repositories, custom `@Query` or JPA Criteria API where needed, DTO projections, SLF4J parameterized logging, JUnit 5, Mockito, test slices, Spring Security, BCrypt, and safe input handling.

## What I Will NOT Do

- Expose JPA entities directly from controllers or accept request payloads without validation.
- Hardcode secrets in `application.yml`, `application.properties`, source code, or tests.
- Put transaction boundaries in controllers or repositories when the service layer owns the business operation.
- Replace the project's chosen build tool, database, security model, or secret-management approach without a clear request.
- Concatenate untrusted input into SQL or produce XSS-prone output.

## Output Format

Return or apply the Spring Boot changes with this structure:

```markdown
### Spring Boot Result

### Target
- `src/main/java/com/example/app/order` or `<target>`

### Applied or Recommended Practices
| Area | Practice | Evidence |
| --- | --- | --- |
| Project Setup & Structure | Use Maven `pom.xml` or Gradle `build.gradle`; organize by feature/domain | Package `com.example.app.order` |
| Dependency Injection & Components | Constructor injection with `private final`; use `@Component`, `@Service`, `@Repository`, `@Controller`, or `@RestController` | `OrderService(OrderRepository repository)` |
| Configuration | Use `application.yml` or `application.properties`, `@ConfigurationProperties`, profiles such as `application-dev.yml` and `application-prod.yml`, and environment variables, environment-specific profiles, or a secret manager | `OrderProperties` |
| Web Layer (Controllers) | RESTful APIs use DTOs, `@Valid`, `@NotNull`, `@Size`, `@ControllerAdvice`, and `@ExceptionHandler` | `OrderRequest` and `OrderResponse` |
| Service Layer | Stateless `@Service` with granular `@Transactional` | `createOrder` |
| Data Layer (Repositories) | Extend `JpaRepository` or `CrudRepository`; use `@Query`, Criteria API, and DTO projections | `OrderRepository` |
| Logging | Use SLF4J and `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);` with `logger.info("Processing user {}...", userId);` | `OrderController` |
| Testing | Use JUnit 5, Mockito, `@SpringBootTest`, `@WebMvcTest`, `@DataJpaTest`, and Testcontainers where useful | `OrderServiceTest` |
| Security | Use Spring Security, BCrypt, Spring Data JPA or parameterized queries, and output encoding | `SecurityConfig` |

### Validation
- Command: `<mvn test, gradle test, or not run>`
- Result: `<passed, failed, or not run with reason>`
```

## Definition of Done

- [ ] Code is organized consistently with the project's package structure and build tool.
- [ ] Required dependencies use constructor injection and immutable fields.
- [ ] Controllers use DTOs, validation, consistent error handling, and do not expose JPA entities.
- [ ] Transactions, repositories, queries, projections, configuration, logging, tests, and security practices are checked.
- [ ] Secrets are externalized through environment variables or a dedicated secret management tool such as HashiCorp Vault or AWS Secrets Manager when the project uses one.
- [ ] Validation evidence or a precise not-run reason is reported.

## Prompt Body

Follow these steps in order. Apply the project's existing stack rather than imposing a reference-project stack.

**Step 1 — Identify the target and build setup.** Locate the requested target. Determine whether the project uses Maven (`pom.xml`) or Gradle (`build.gradle`). Check Spring Boot starters such as `spring-boot-starter-web` and `spring-boot-starter-data-jpa`, package conventions, and current test commands.

**Step 2 — Review project structure and components.** Organize code by feature or domain, for example `com.example.app.order` and `com.example.app.user`, rather than generic packages such as `com.example.app.controller` and `com.example.app.service` when the repository supports that style. Use constructor-based injection for required dependencies, declare dependency fields `private final`, and apply `@Component`, `@Service`, `@Repository`, `@Controller`, and `@RestController` appropriately.

**Step 3 — Review configuration.** Use `application.yml` or `application.properties` for externalized configuration. Prefer `@ConfigurationProperties` for strongly typed Java objects (strongly-typed Java objects). Use Spring Profiles through files such as `application-dev.yml` and `application-prod.yml`. Do not hardcode secrets; use environment variables or a dedicated secret management tool such as HashiCorp Vault or AWS Secrets Manager when appropriate for the project.

**Step 4 — Review the Web Layer (Controllers).** Design clear RESTful APIs. Use DTOs to expose and consume data. Do not expose JPA entities directly to clients. Apply Java Bean Validation (JSR 380) with `@Valid`, `@NotNull`, and `@Size` on DTOs. Implement consistent errors with `@ControllerAdvice` and `@ExceptionHandler`.

**Step 5 — Review services and data access.** Encapsulate business logic in stateless `@Service` classes. Use `@Transactional` on service methods at the most granular useful level. Use Spring Data JPA by extending `JpaRepository` or `CrudRepository`. For complex queries, use `@Query` or the JPA Criteria API. Use DTO projections to fetch only necessary data.

**Step 6 — Review logging.** Use the SLF4J API. Declare loggers as `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`. Use parameterized logging such as `logger.info("Processing user {}...", userId);` instead of string concatenation. Preserve the exact logger example `logger.info("Processing user {}...", userId);`.

**Step 7 — Review testing.** Write unit tests for services and components using JUnit 5 and Mockito or the project's mocking framework. Use `@SpringBootTest` for integration tests that load the Spring application context. Use `@WebMvcTest` for controllers and `@DataJpaTest` for repositories. Consider Testcontainers for reliable integration tests with real databases, message brokers, or similar services.

**Step 8 — Review security.** Use Spring Security for authentication and authorization. Encode passwords with a strong hashing algorithm such as BCrypt. Prevent SQL injection with Spring Data JPA or parameterized queries. Prevent Cross-Site Scripting (XSS) by encoding output properly.

**Step 9 — Validate and report.** Apply approved edits or return findings. Run the smallest existing Maven or Gradle validation command when available. Report changes, evidence, and unresolved risks.

## Invocation Example

```
/java-springboot target=src/main/java/com/example/app/order
```

---
paths:
  - "**/*.java"
  - "**/*.kt"
---

<!-- Generated from harness/github-copilot/instructions/springboot.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for Spring Boot base applications covering dependency injection, configuration, package organization, services, logging, security, validation, builds, and useful Maven or Gradle commands.

# Spring Boot Conventions — Maintainable Base Applications

These instructions apply to Java and Kotlin Spring Boot files matched by the `applyTo` globs. They are authoritative for dependency injection, configuration, code organization, service design, logging, security, input handling, build verification, and common Maven or Gradle commands; project architecture, language-specific style, and security primitives win where they impose stricter rules.

## General Code Guidance

- Make only high-confidence suggestions when reviewing code changes.
- Write maintainable code and add comments only when they explain why a design decision was made.
- Handle edge cases with clear exception handling.
- When adding libraries or external dependencies, document their usage and purpose where the dependency is introduced.

## Dependency Injection and Configuration

- Use constructor injection for required dependencies.
- Declare dependency fields as `private final`.
- Use YAML files such as `application.yml` for externalized configuration.
- Use Spring profiles for environment-specific configuration such as `dev`, `test`, and `prod`.
- Use `@ConfigurationProperties` for type-safe configuration binding.
- Externalize secrets through environment variables or secret management systems.

## Code Organization and Service Layer

- Organize packages by feature or domain (`feature/domain`) rather than by technical layer.
- Keep controllers thin, services focused, and repositories simple.
- Make utility classes `final` with private constructors.
- Put business logic in `@Service`-annotated classes.
- Keep services stateless and testable.
- Inject repositories through constructors.
- Use service method signatures with domain IDs or DTOs; do not expose repository entities directly unless necessary.

## Logging, Security, and Input Handling

- Use SLF4J for all logging with `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`.
- Do not use concrete logging implementations such as Logback or Log4j2 directly.
- Do not use `System.out.println()` for application logging.
- Use parameterized logging such as `logger.info("User {} logged in", userId);`.
- Use Spring Data JPA or `NamedParameterJdbcTemplate` for parameterized queries to prevent SQL injection.
- Validate request bodies and parameters with JSR-380 annotations such as `@NotNull` and `@Size`.
- Use `BindingResult` when controller logic needs to inspect validation errors explicitly.

## Build, Verification, and Useful Commands

After adding or modifying code, verify the project builds and tests pass with the existing build tool.

| Gradle Command | Maven Command | Description |
| --- | --- | --- |
| `./gradlew bootRun` | `./mvnw spring-boot:run` | Run the application. |
| `./gradlew build` | `./mvnw package` | Build the application. |
| `./gradlew test` | `./mvnw test` | Run tests. |
| `./gradlew bootJar` | `./mvnw spring-boot:repackage` | Package the application as a JAR. |
| `./gradlew bootBuildImage` | `./mvnw spring-boot:build-image` | Package the application as a container image. |

If the project uses Maven, `mvn clean package` is an acceptable full verification command. If the project uses Gradle, use `./gradlew build` on Unix-like systems or `gradlew.bat build` on Windows.

## Good / Bad Examples

The examples below illustrate constructor injection, SLF4J, and focused service dependencies.

**Good:**

```java
@Service
public class UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public UserDto findUser(Long userId) {
        logger.info("Loading user {}", userId);
        return userRepository.findDtoById(userId);
    }
}
```

Why: The service is stateless, uses constructor injection, keeps dependencies `private final`, and logs through SLF4J with parameters.

**Bad:**

```java
@Service
public class UserService {
    @Autowired
    private UserRepository repository;

    public void findUser(String id) {
        System.out.println("Loading " + id);
    }
}
```

Why: The service uses field injection, mutable dependency fields, and `System.out.println()` instead of SLF4J.

## Conventions

| Rule | Rationale |
|---|---|
| Make only high-confidence review suggestions and comment on why decisions were made | Reviews stay actionable and code explains non-obvious choices |
| Use constructor injection and `private final` fields | Dependencies are explicit and immutable |
| Use `application.yml`, Spring profiles, `@ConfigurationProperties`, and external secret stores | Configuration stays typed, environment-specific, and safe |
| Organize by feature or domain with thin controllers, focused services, and simple repositories | Business boundaries stay clear |
| Keep utility classes `final` with private constructors | Utility classes cannot be instantiated or subclassed accidentally |
| Put business logic in stateless `@Service` classes and pass domain IDs or DTOs | Services remain testable and do not leak repository entities unnecessarily |
| Use SLF4J with parameterized messages | Logging stays implementation-independent and efficient |
| Use Spring Data JPA or `NamedParameterJdbcTemplate` with JSR-380 validation and `BindingResult` when needed | SQL injection and invalid request data are handled at boundaries |
| Run Maven or Gradle build and tests after code changes | Regressions are caught before review |

## Do / Do Not

| Do | Do not |
|---|---|
| Inject dependencies through constructors | Use field injection for required dependencies |
| Store required dependencies in `private final` fields | Leave service collaborators mutable without reason |
| Use `application.yml` and profiles such as `dev`, `test`, and `prod` | Hardcode environment-specific configuration |
| Bind configuration with `@ConfigurationProperties` | Parse unrelated configuration values manually throughout the code |
| Log with `LoggerFactory.getLogger(MyClass.class)` and `{}` placeholders | Use Logback, Log4j2, or `System.out.println()` directly |
| Validate requests with `@NotNull`, `@Size`, and related JSR-380 annotations | Trust request bodies or parameters without validation |
| Build with `./gradlew build`, `gradlew.bat build`, `./mvnw package`, or `mvn clean package` as appropriate | Skip build verification after code changes |

## Checklist Before Opening a PR

- [ ] Review comments and code changes are high-confidence and explain non-obvious decisions.
- [ ] Required dependencies use constructor injection and `private final` fields.
- [ ] Configuration uses `application.yml`, Spring profiles, `@ConfigurationProperties`, and externalized secrets.
- [ ] Packages are organized by feature or domain, with thin controllers, focused services, and simple repositories.
- [ ] Utility classes are `final` with private constructors.
- [ ] Business logic lives in stateless `@Service` classes with repository injection through constructors.
- [ ] Logging uses SLF4J, `LoggerFactory.getLogger(MyClass.class)`, parameterized messages, and no `System.out.println()`.
- [ ] Queries use Spring Data JPA or `NamedParameterJdbcTemplate`, and request data uses JSR-380 validation with `BindingResult` where needed.
- [ ] The appropriate Maven or Gradle command, such as `mvn clean package`, `./gradlew build`, or `gradlew.bat build`, passes.

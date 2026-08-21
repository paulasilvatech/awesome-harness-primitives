---
applyTo: "**/*.java,**/pom.xml,**/build.gradle,**/build.gradle.kts,**/application.properties,**/application.yaml,**/application.yml"
description: "Enforces Quarkus Java conventions for project structure, REST resources, Panache data access, configuration, security, and testing. Use when editing Quarkus source, build, or application configuration files."
---

# Quarkus Conventions — Java 17+ Applications

These instructions apply to Quarkus application source, Maven or Gradle build files, and `application.properties`, `application.yaml`, or `application.yml` configuration. They are authoritative for Java 17+ Quarkus 3.x structure, REST resources, data access, configuration, testing, security, and runtime conventions in matched files; project architecture, organization security policy, and deployment primitives win where they define stricter requirements.

## Project Context and Development Standards

Target high-quality Quarkus applications with clean architecture, maintainability, and performance.

| Concern | Convention |
| --- | --- |
| Quarkus version | Use Quarkus 3.x unless the repository pins another supported version. |
| Java version | Use Java 17 or later features when appropriate, including records and sealed classes. |
| Build tools | Use Maven or Gradle through `pom.xml`, `build.gradle`, or `build.gradle.kts`. |
| Comments | Write clear comments for classes, methods, and complex logic where they add context; do not narrate obvious code. |
| Public APIs | Use Javadoc for public APIs and public methods that consumers call. |
| Style | Follow Java, Jakarta EE, and MicroProfile conventions; avoid the misspelling `Jarkarta EE`. |

## Naming and Code Style

| Element | Convention | Example |
| --- | --- | --- |
| Class names | `PascalCase` | `ProductService`, `ProductResource` |
| Methods and variables | `camelCase` | `findProductById`, `isProductAvailable` |
| Constants | `ALL_CAPS` | `DEFAULT_PAGE_SIZE` |
| JSON media type | Use `MediaType.APPLICATION_JSON` in REST resources. | `@Produces(MediaType.APPLICATION_JSON)` |

Keep package organization clear and business-oriented. Prefer concise, intention-revealing names over generic suffixes when the role is already obvious from context.

## Quarkus Runtime and CDI Patterns

- Use Quarkus Dev Mode for fast development cycles.
- Implement build-time optimizations through Quarkus extensions and best practices.
- Configure native builds with GraalVM and the `quarkus-maven-plugin` when native images are a project requirement.
- Use Quarkus logging through JBoss, SLF4J, SL4J compatibility bridges when required, or JUL consistently.
- Use `@ApplicationScoped` for singleton-like CDI beans instead of `@Singleton`.
- Use `@Inject` for dependency injection, and prefer constructor injection when the codebase supports it.
- Use `@Transactional` on service methods that modify data.

## REST Resources and Error Handling

Build REST resources with Jakarta REST conventions and explicit HTTP behavior.

| Concern | Convention |
| --- | --- |
| Routing | Use JAX-RS annotations such as `@Path`, `@GET`, and `@POST`; choose descriptive endpoint paths. |
| Content type | Use `@Consumes(MediaType.APPLICATION_JSON)` and `@Produces(MediaType.APPLICATION_JSON)` for JSON resources. |
| Status codes | Return proper HTTP status codes such as `200`, `201`, `400`, `404`, and `500`. |
| Complex responses | Use the `Response` class when status, headers, or body need explicit control. |
| Validation | Validate input parameters with Bean Validation annotations. |
| Public APIs | Implement rate limiting for public endpoints where abuse is plausible. |
| Exceptions | Include proper error handling with try-catch blocks only where the resource can add context or translate errors. |

## Data Access and Transactions

Prefer Quarkus Panache for persistence unless the repository has a different standard.

- Prefer Panache entities that extend `PanacheEntity` for simple CRUD-oriented models.
- Use Panache repositories with `PanacheRepository<T>` for complex queries or when entity classes should stay persistence-light.
- Prefer Panache repositories over traditional JPA repositories unless compatibility requires otherwise.
- Use named queries for complex database operations when they improve readability or reuse.
- Implement pagination for list endpoints; use constants such as `DEFAULT_PAGE_SIZE` for limits.
- Put `@Transactional` on service methods that modify the database, not on read-only helper methods by habit.

## Configuration, Security, and Secrets

| Area | Convention |
| --- | --- |
| Configuration files | Use `application.properties` or `application.yaml` for simple configuration. |
| Type safety | Use `@ConfigProperty` for typed configuration injection and configuration classes where values need structure. |
| Secrets | Prefer environment variables or the platform secret store for sensitive data; do not hardcode configuration values. |
| Profiles | Use Quarkus profiles for `dev`, `test`, and `prod`. |
| Security extensions | Use Quarkus Security extensions such as `quarkus-smallrye-jwt` or `quarkus-oidc`. |
| Authorization | Implement role-based access control (RBAC) with MicroProfile JWT or OIDC. |
| Inputs | Validate all input parameters before using them in business logic or queries. |

## Testing

Use the Quarkus testing tools that match the test boundary.

| Test type | Convention |
| --- | --- |
| Integration tests | Use `@QuarkusTest`. |
| Unit tests | Use JUnit 5. |
| Native build tests | Use `@QuarkusIntegrationTest`. |
| External dependencies | Mock or provide dependencies through `@QuarkusTestResource`. |
| REST endpoints | Use RestAssured in `@QuarkusTest` tests. |
| Database-modifying tests | Use `@Transactional` when test setup or assertions require a transaction. |
| Database integration | Use Testcontainers for database integration tests; preserve `test-containers` terminology when documenting older guidance. |

Do not use field injection in tests when constructor injection or framework-supported injection keeps dependencies explicit. Do not ignore exceptions in tests or application code.

## Good / Bad Examples

The examples below illustrate a JSON REST resource with validation and service-level transaction boundaries.

**Good**

```java
@Path("/products")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class ProductResource {
    @Inject ProductService service;

    @POST
    public Response create(@Valid ProductRequest request) {
        Product product = service.create(request);
        return Response.status(201).entity(product).build();
    }
}

@ApplicationScoped
class ProductService {
    @Transactional
    Product create(ProductRequest request) {
        return Product.persistFrom(request);
    }
}
```

Why: the resource owns HTTP shape and validation, while the service owns the write transaction.

**Bad**

```java
@Path("/products")
public class ProductResource {
    @POST
    public Product create(ProductRequest request) {
        try {
            return Product.persistFrom(request);
        } catch (Exception ignored) {
            return null;
        }
    }
}
```

Why: the code omits JSON content annotations, validation, status codes, transaction boundaries, and proper exception handling.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use Quarkus 3.x with Java 17 or later unless the project pins a different supported baseline. | Code can rely on modern Quarkus and Java language capabilities. |
| Follow Java naming conventions: `PascalCase`, `camelCase`, and `ALL_CAPS`. | Consistent names keep APIs and implementations readable. |
| Prefer `@ApplicationScoped`, `@Inject`, Quarkus Dev Mode, extensions, and Quarkus logging. | Code works with Quarkus CDI and build-time optimization. |
| Use JAX-RS annotations, Bean Validation, `Response`, and explicit status codes in resources. | HTTP APIs stay predictable for clients. |
| Prefer Panache entities and `PanacheRepository<T>` with `@Transactional` on modifying service methods. | Persistence code stays concise while transaction boundaries remain clear. |
| Use `@ConfigProperty`, environment variables, and profiles for configuration. | Configuration stays type-safe and secrets stay outside source. |
| Test with `@QuarkusTest`, JUnit 5, `@QuarkusIntegrationTest`, RestAssured, `@QuarkusTestResource`, and Testcontainers where appropriate. | Tests match Quarkus runtime behavior without over-mocking. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `@Consumes(MediaType.APPLICATION_JSON)` and `@Produces(MediaType.APPLICATION_JSON)` for JSON resources. | Return ambiguous content types from REST endpoints. |
| Validate inputs with Bean Validation and return meaningful HTTP status codes. | Ignore exceptions or return `null` from error paths. |
| Put write transactions in services. | Scatter `@Transactional` across controllers or unrelated helpers. |
| Use environment variables for sensitive data. | Hardcode configuration values or secrets. |
| Use constructor injection in tests when feasible. | Use field injection in tests by default. |
| Implement rate limiting for public endpoints. | Expose public endpoints without abuse controls. |

## Checklist Before Opening a PR

- [ ] Code targets Quarkus 3.x and Java 17+ or the repository-pinned equivalent.
- [ ] Names follow `PascalCase`, `camelCase`, and `ALL_CAPS` conventions.
- [ ] REST resources use JAX-RS annotations, JSON media types, validation, and proper status codes.
- [ ] Data access uses Panache or the project standard, with pagination for list endpoints.
- [ ] Modifying operations use `@Transactional` at the service boundary.
- [ ] Configuration uses `application.properties`, `application.yaml`, profiles, and `@ConfigProperty` without hardcoded secrets.
- [ ] Security uses appropriate Quarkus extensions, RBAC, and input validation.
- [ ] Tests use the appropriate Quarkus, JUnit 5, RestAssured, and Testcontainers patterns.

---
description: "Use when designing or reviewing Modular Monolith architecture, package-by-feature boundaries, JPA mapping, and Strangler Fig migration."
applyTo: "backend/src/main/java/**,backend/pom.xml,backend/build.gradle*"
---

# Modular Monolith Architecture Guide

This file activates when you work on Java source files or backend build configurations. It teaches the target architecture: a **Modular Monolith** — not microservices — with package-by-feature boundaries, bounded contexts, Adabas FDT to JPA mapping, Spring Boot 3.3 architectural conventions, and the Strangler Fig migration shape. It does **not** define controller, DTO, validation, or error-response details, which belong to [`backend.instructions.md`](backend.instructions.md); security belongs to [`security.instructions.md`](security.instructions.md); schema migrations belong to [`database.instructions.md`](database.instructions.md); and legacy-source reading belongs to [`natural-adabas.instructions.md`](natural-adabas.instructions.md).

## Core Principle: One Deployable, Many Modules

The target system is a single Spring Boot application with clear internal module boundaries. Each bounded context is a Maven module (or top-level package) that owns its domain, repository, and service layers.

Why a Modular Monolith rather than microservices:

- **Workshop constraint**: 8 hours is not enough time to manage distributed systems, service discovery, and inter-service communication.
- **Complexity budget**: A monolith with strong module boundaries provides 80% of the benefits of microservices (team autonomy, clear ownership) at 20% of the operational cost.
- **Migration path**: A well-structured Modular Monolith can be decomposed into microservices later if necessary. The reverse is much harder.

## Package-by-Feature Structure

Organize code by business capability, not by technical layer:

```
src/main/java/com/example/app/
├── <feature>/                  # Bounded context defined by the team
│   ├── <Feature>Controller.java
│   ├── <Feature>Service.java
│   ├── <Feature>Repository.java
│   ├── <Feature>.java
│   └── <Feature>Dto.java
├── shared/                     # Shared kernel
│   ├── audit/                  # Cross-cutting: audit trail
│   └── exception/              # Cross-cutting: error handling
└── Application.java            # Spring Boot entry point
```

Rules:

- A module MUST **NEVER** directly import internal classes from another module. Use interfaces or events.
- The `shared/` package contains only cross-cutting concerns (audit, exceptions, base entities).
- Each module has its own `*Repository`, `*Service`, and `*Controller`.

## Bounded Context Boundaries

When deciding where to draw module boundaries, ask:

1. **Who owns this data?** If two features share the same table, they may belong to the same context.
2. **What changes together?** Features modified in the same sprint belong together.
3. **What can fail independently?** If Feature A failing MUST NOT break Feature B, they belong to separate contexts.

A common pattern in Natural/Adabas legacy modernization is that each Adabas file (FNR) often maps to a bounded context, although some files contain shared reference data that belongs in a shared kernel.

## JPA Mapping from Adabas FDT

### Simple Fields

| Adabas Format | Java Type | JPA Annotation |
|---|---|---|
| `A` (alphanumeric) | `String` | `@Column(length = N)` |
| `N` (numeric, no decimal) | `Long` or `Integer` | `@Column` |
| `N` (numeric, with decimal) | `BigDecimal` | `@Column(precision = P, scale = S)` |
| `P` (packed decimal) | `BigDecimal` | `@Column(precision = P, scale = S)` |
| `D` (date) | `LocalDate` | `@Column` |
| `T` (time/datetime) | `LocalDateTime` | `@Column` |
| `B` (binary) | `byte[]` | `@Column` / `@Lob` |

### MU (Multiple-Value) Fields → JSONB

```java
@Column(columnDefinition = "jsonb")
@JdbcTypeCode(SqlTypes.JSON)
private List<String> alternateNames;  // Was MU field in Adabas
```

Or use `@ElementCollection` if query capability is required:

```java
@ElementCollection
@CollectionTable(name = "person_alternate_names")
private List<String> alternateNames;
```

### PE (Periodic Groups) → @OneToMany

```java
@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
@JoinColumn(name = "person_id")
private List<AddressHistory> addressHistory;  // Was PE group
```

Where `AddressHistory` is an `@Entity` with its own table.

## Spring Boot 3.3 Conventions

- **Constructor injection**: No field-level `@Autowired`. Use `@RequiredArgsConstructor` (Lombok) or explicit constructors.
- **Records for DTOs**: `public record ResourceDto(Long id, String label) {}`
- **Validation in the controller layer**: `@Valid @RequestBody ResourceDto dto` with Bean Validation annotations on the DTO.
- **@Transactional only in the service layer**: NEVER in repositories, NEVER in controllers.
- **Optional for nullable returns**: `Optional<Resource> findById(Long id)` — NEVER return `null` from public methods.
- **Sealed interfaces for type unions**: `sealed interface ResourceState permits StateA, StateB {}`

## Error Handling Pattern

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ProblemDetail> handleNotFound(EntityNotFoundException ex) {
        ProblemDetail detail = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(detail);
    }
}
```

Use `ProblemDetail` (RFC 7807) for all error responses.

## Strangler Fig Pattern

When the modern system must coexist with the legacy system:

1. **Facade**: All requests pass through a routing layer
2. **New path**: New or migrated features are handled by the Spring Boot modules
3. **Legacy path**: Unmigrated features are proxied to the legacy system
4. **Gradual migration**: As each feature is migrated, its route switches from legacy to modern

This pattern applies even within the workshop scope: teams may not migrate everything, and that is acceptable. The architecture MUST support partial migration gracefully.

## Conventions

| Rule | Rationale |
|---|---|
| One Spring Boot deployable with many internal modules | Preserves workshop delivery speed while keeping boundaries explicit |
| Package by business capability | Modules map to bounded contexts instead of technical layers |
| Module internals stay private; cross-module access uses interfaces or events | Prevents hidden coupling between contexts |
| Adabas FDT types map deliberately to Java/JPA types | Avoids silent truncation, precision loss, and incorrect relationships |
| `@Transactional` only in services and constructor injection everywhere | Keeps persistence boundaries and dependencies explicit |
| `ProblemDetail` for errors | Gives every module one machine-readable error shape |

## Do / Do Not

| Do | Do not |
|---|---|
| Keep one Spring Boot application with clear internal modules | Create separate Spring Boot applications or microservices for each context |
| Put business logic in Java services | Move business logic into PostgreSQL stored procedures or functions |
| Use JPA/JPQL or Spring Data derived queries | Concatenate strings to build SQL |
| Use constructor injection | Use field injection with `@Autowired` |
| Return `Optional` when a result may be absent | Return `null` from public methods |
| Support partial migration with a Strangler Fig facade | Assume the whole legacy system is migrated at once |

## Checklist Before Opening a PR

- [ ] New code is inside one Spring Boot deployable and organized by business capability
- [ ] No module imports another module's internal classes directly; interfaces or events define the boundary
- [ ] Repositories, services, controllers, entities, and DTOs stay inside the owning module or shared kernel
- [ ] Adabas FDT fields were mapped to Java/JPA types with precision, MU, PE, and descriptor semantics preserved
- [ ] `@Transactional` appears only in services, dependencies use constructor injection, and public methods do not return `null`
- [ ] The design can coexist with unmigrated legacy paths through the Strangler Fig routing shape

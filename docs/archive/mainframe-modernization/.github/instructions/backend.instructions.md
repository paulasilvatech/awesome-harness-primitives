---
description: "Use when implementing backend APIs, services, controllers, request validation, error handling, and business service boundaries."
applyTo: "backend/src/main/java/**,backend/src/test/java/**"
---

# Backend Conventions — Controllers, Services, and Validation

This file activates when you edit Java sources or tests under `backend/`. It teaches how to shape controllers, DTOs, the service layer, request validation, and error responses for a Java 21 + Spring Boot 3.3 application. It does **not** decide module boundaries or JPA/FDT mapping — those belong to [`modular-monolith.instructions.md`](modular-monolith.instructions.md) — and it does not cover authentication, which belongs to [`security.instructions.md`](security.instructions.md).

> [!NOTE]
> `backend/` does not exist yet. The team creates it from scratch in Stage 3. Treat the rules below as the conventions the code must follow the moment it is written.

## Layering and Boundaries

Requests flow one direction: `Controller → Service → Repository`. Keep controllers thin (HTTP mapping only) and put every business rule in the service.

- `@Transactional` lives **only** in the service layer — never in a controller or repository; reads use `@Transactional(readOnly = true)`.
- Public methods never return `null`; model absence with `Optional`.
- Keep controllers and services package-private to their module so no other module imports internals.

## Controllers and REST Endpoints

Paths follow `/api/v1/{resource}` (plural, kebab-case for multi-word resources). Every endpoint carries OpenAPI annotations and returns the correct status code — `201` on create, `204` on delete, `409` on conflict, and `PATCH` for partial updates.

```java
@RestController
@RequestMapping("/api/v1/resources")
@RequiredArgsConstructor
class ResourceController {

    private final ResourceService resourceService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED) // 201 on creation
    @Operation(summary = "Register a resource")
    @ApiResponse(responseCode = "201", description = "Created")
    @ApiResponse(responseCode = "409", description = "Duplicate resource")
    ResourceResponse create(@Valid @RequestBody CreateResourceRequest request) {
        return resourceService.create(request);
    }
}
```

## DTOs and Validation

Expose Java 21 `record` DTOs, never JPA entities. Validate at the controller boundary with Bean Validation on the request record.

```java
public record CreateResourceRequest(
    @NotBlank @Size(max = 120) String label,
    @NotNull @Positive BigDecimal amount) {}
```

## Service Layer

The service coordinates the transaction, enforces invariants, and translates persistence results into DTOs.

```java
@Service
@RequiredArgsConstructor
class ResourceService {

    private final ResourceRepository resourceRepository;

    @Transactional(readOnly = true)
    ResourceResponse getById(UUID id) {
        return resourceRepository.findById(id)
            .map(ResourceResponse::from)
            .orElseThrow(() -> new ResourceNotFoundException(id));
    }

    @Transactional
    ResourceResponse create(CreateResourceRequest request) {
        resourceRepository.findByLabel(request.label()).ifPresent(existing -> {
            throw new ResourceConflictException(request.label());
        });
        return ResourceResponse.from(resourceRepository.save(Resource.from(request)));
    }
}
```

## Error Handling

Return RFC 7807 `ProblemDetail` from a single `@RestControllerAdvice`, map validation failures to `400`, and attach a correlation ID so logs and responses can be joined.

```java
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        return problem(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    private ProblemDetail problem(HttpStatus status, String detail) {
        ProblemDetail body = ProblemDetail.forStatusAndDetail(status, detail);
        body.setProperty("correlationId", MDC.get("correlationId"));
        return body;
    }
}
```

## Logging and Sensitive Data

> [!WARNING]
> Never log CPF, benefit amounts, tokens, or other sensitive values. Log identifiers and the correlation ID instead, and mask any regulated field before it reaches a log or error message.

```java
// Wrong: log.info("payment for CPF {} amount {}", cpf, amount);
log.info("payment processed correlationId={} resourceId={}", correlationId, id);
```

## Conventions

| Rule | Rationale |
|---|---|
| Controllers `PascalCase`; routes `/api/v1/{resource}` in kebab-case | Predictable, versioned HTTP surface |
| `@Transactional` only in services | Repositories and controllers stay side-effect-honest |
| Records for request/response DTOs | Immutable, boundary-explicit contracts |
| `@Valid` + Bean Validation in controllers | Reject bad input before it reaches business logic |
| `Optional` for absent results | Eliminates `NullPointerException` from public APIs |
| `ProblemDetail` (RFC 7807) for every error | One machine-readable error shape |

## Do / Do Not

| Do | Do not |
|---|---|
| Return `201`/`204`/`409` where they apply | Return `200` for every outcome |
| Throw domain exceptions mapped in the advice | Return raw stack traces or `Map<String,Object>` errors |
| Inject dependencies by constructor | Use field `@Autowired` |
| Mask CPF and amounts in logs | Log entities, request bodies, or tokens |

## Checklist Before Opening a PR

- [ ] Every endpoint uses `/api/v1/{resource}`, the right verb, and the right status code
- [ ] Every endpoint has OpenAPI annotations and a validated `record` request body
- [ ] `@Transactional` appears only in services; no public method returns `null`
- [ ] Errors flow through the `@RestControllerAdvice` as `ProblemDetail` with a correlation ID
- [ ] No sensitive data (CPF, amounts, tokens) reaches logs or error payloads
- [ ] Tests cover the happy path, a validation failure, and an auth failure (see [`tests.instructions.md`](tests.instructions.md))

---
name: "implement-rest-controller"
description: "Implements a Spring REST controller from an OpenAPI endpoint definition and connects it to the bounded context services."
argument-hint: "endpoint=\"<METHOD /api/v1/resource>\" context=<context> service=<Service>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /implement-rest-controller

## Objective

Generate a Spring Boot REST controller from an OpenAPI endpoint definition. The controller is a thin adapter: it validates input, delegates to a service, and returns the response. It contains no business logic.

## When to Invoke

After the service layer for a bounded context exists, when the team is ready to expose it as a REST API.

## Preconditions

- The OpenAPI definition created by the team contains the endpoint
- The bounded context service class (or its interface) exists
- The request/response DTOs are defined (or will be generated as records)

## Inputs the Team Must Provide

- The endpoint to implement (method + path from the OpenAPI definition)
- The bounded context and target package
- The service class to delegate to

## What I Will Do

- Read the OpenAPI definition for the specified endpoint
- Generate a `@RestController` class with the appropriate annotations
- Create request/response record DTOs with Jakarta Bean Validation
- Connect the controller to the service through constructor injection
- Add `@ControllerAdvice` error handling if it is not already present
- Run a build to verify compilation

## What I Will NOT Do

- Put business logic in the controller — it delegates to the service layer
- Skip input validation — every endpoint has `@Valid` on its request body
- Use field injection with `@Autowired` — use constructor injection only
- Hardcode error messages — use RFC 7807 `ProblemDetail` responses
- Fabricate endpoint behavior not defined in the OpenAPI specification

## Output Format

Java files:

1. Controller at `src/main/java/[package]/api/[Name]Controller.java`
2. Request/response DTOs at `src/main/java/[package]/api/dto/[Name]Request.java` and `[Name]Response.java`
3. Global exception handler at `src/main/java/[package]/shared/exception/GlobalExceptionHandler.java` (if it does not exist)

## Definition of Done

- [ ] The controller compiles without errors
- [ ] The OpenAPI `operationId` is referenced in the Javadoc
- [ ] The request DTO has Jakarta Bean Validation annotations (`@NotNull`, `@Size`, etc.)
- [ ] The response uses the correct HTTP status codes (201 for POST, 200 for GET, 204 for DELETE)
- [ ] The controller body contains no business logic — only validation, delegation, and response mapping
- [ ] Error responses use RFC 7807 `ProblemDetail`
- [ ] Related REQ-IDs are documented in the Javadoc

## Prompt Body

You are the `@builder`. The team needs a REST controller for an endpoint defined in the OpenAPI specification.

**Step 1 — Read the OpenAPI definition.**
Open the OpenAPI definition identified by the team. Find the specified endpoint. Extract:

- HTTP method and path
- Operation ID and summary
- Request body schema (if any)
- Response schema
- Path/query parameters
- Related REQ-IDs (from the description or tags)

**Step 2 — Generate request/response records.**
Create Java records for the request and response:

```java
public record [RequestName](
    @NotNull [FieldType] [requiredField],
    @Size(max = [maxLength]) String [optionalTextField]
) {}

public record [ResponseName](
    [FieldType] [field]
) {}
```

Use Jakarta Bean Validation annotations based on field types and any constraints in the OpenAPI schema.

**Step 3 — Generate the controller.**
Create the controller class:

```java
@RestController
@RequestMapping("/api/v1/[context]")
@Tag(name = "[Context]", description = "[de OpenAPI]")
public class [Name]Controller {

    private final [Service] service;

    public [Name]Controller([Service] service) {
        this.service = service;
    }

    /**
    * [OpenAPI operation summary].
     *
     * <p>OpenAPI operationId: {@code [operationId]}</p>
    * <p>Implements: REQ-NNN</p>
     */
    @PostMapping  // or @GetMapping, etc.
    @Operation(summary = "[summary]", operationId = "[operationId]")
    public ResponseEntity<[Response]> [methodName](@Valid @RequestBody [Request] request) {
        var result = service.[method](/* map request to domain */);
        return ResponseEntity.status(HttpStatus.CREATED).body(/* map domain to response */);
    }
}
```

**Step 4 — Ensure error handling exists.**
Check whether `GlobalExceptionHandler` exists in the shared package. If not, generate it with handlers for:

- `MethodArgumentNotValidException` → 400 with validation details
- `EntityNotFoundException` → 404
- `IllegalStateException` → 409 (conflict)
- `Exception` → 500 (catch-all with a safe error message and no exposed stack trace)

All error responses use `ProblemDetail` (RFC 7807).

**Step 5 — Verify compilation.**
Run `mvn compile` (or the equivalent build command). Report and fix any errors.

If the service interface does not yet exist, generate a minimal interface with the required method signature and a TODO implementation. The team will fill in the logic.

## Invocation Example

```
/implement-rest-controller endpoint="<METHOD /api/v1/resource>" context=<context> service=<Service>
```

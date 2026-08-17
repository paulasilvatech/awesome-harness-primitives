---
name: "java-springboot"
description: "Apply Spring Boot best practices for the SIFAP 2.0 backend, deferring the detailed checklist to the java-springboot skill."
argument-hint: "target=<file-or-module>"
agent: "implementer"
tools: ["read", "search", "edit"]
---
> [!NOTE]
> Reference snapshot: this file is kept as a quality example for primitive authors. It is not installed from this repository as an active primitive.

# /java-springboot

## Objective

Guide building or reviewing a Spring Boot slice for the SIFAP 2.0 backend — package-by-feature layout, constructor injection, DTOs, a global exception handler, service-layer transactions, and test slices — so the code matches the kit's fixed stack. The detailed checklist lives in the skill `java-springboot`; this prompt applies it without restating it.

> [!IMPORTANT]
> The stack is fixed: Java 21 + Spring Boot 3.3 + JPA/Hibernate + PostgreSQL 16. Do not offer another framework or database as an alternative.

## When to Invoke

During Stage 3/4, while building or reviewing a backend module, once the bounded context the code belongs to is known.

## Preconditions

- The `backend/` module is scaffolded (see `/create-spring-boot-java-project`)
- The bounded context and its package are identified (see the `modular-monolith` instruction)
- The REQ-IDs the module implements are known

## Inputs the Team Must Provide

- `target` — the file or module to build or review
- The bounded context it belongs to and the REQ-IDs it serves
- Ask the user for anything that is missing.

## What I Will Do

- Follow the best practices in the skill `java-springboot`, applying them to the target
- Enforce constructor injection, `private final` fields, DTO boundaries, and `@Valid` request records
- Keep `@Transactional` in the service layer and route data access through Spring Data JPA
- Point secrets at environment variables backed by Azure Key Vault and Managed Identity

## What I Will NOT Do

- Substitute Quarkus, Micronaut, MongoDB, Redis, or any non-kit component
- Recommend HashiCorp Vault or AWS Secrets Manager (the kit uses Azure Key Vault)
- Expose JPA entities directly from a controller or return `null` from a public method
- Put `@Transactional` on a repository or hardcode a secret

## Output Format

The built or reviewed code plus a short conformance note:

```markdown
### Applied
- Constructor injection + `private final` on `PaymentService`
- `/api/v1/payments` controller with `@Valid PaymentRequest` and OpenAPI annotations
- `@Transactional` on the service method only

### Flagged
- `PaymentController` returned the JPA entity → replaced with a `PaymentResponse` DTO
```

## Definition of Done

- [ ] Code is organized by feature, with constructor injection and immutable fields
- [ ] REST paths use `/api/v1/{resource}` and every endpoint has OpenAPI annotations and `@Valid`
- [ ] `@Transactional` appears only in the service layer; no entity is exposed
- [ ] Secrets come from the environment (Azure Key Vault), never hardcoded

## Prompt Body

The skill `java-springboot` owns the layered best practices — read it, then apply them to the target.

**Step 1 — Place the code.**
Confirm the feature package and bounded context; organize by domain, not by layer.

**Step 2 — Apply the skill.**
Build or review the web, service, and data layers per the skill: DTOs at the boundary, a `@ControllerAdvice` exception handler, `@ConfigurationProperties` for typed config, and SLF4J parameterized logging.

**Step 3 — Respect the kit rules.**
Hold to Java 21 + Spring Boot 3.3 + PostgreSQL 16, source secrets from Azure Key Vault, and validate every input with `@Valid`.

**Step 4 — Report.**
List the practices applied and any violations you corrected.

## Invocation Example

```
/java-springboot target=backend/src/main/java/com/sifap/payment
```

---
name: sifap-backend
description: >-
  Defines SIFAP Java 21 and Spring Boot 3.3 backend boundaries, validation, transactions, errors,
  and data exposure. Use when editing backend Java source.
paths:
  - backend/src/main/java/**
  - backend/pom.xml
  - backend/build.gradle*
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/mainframe-natural-adabas-classic/instructions/sifap-backend.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# SIFAP backend conventions - Java service boundaries

These instructions apply to the workshop Java 21 and Spring Boot 3.3 compatibility baseline. They are
authoritative for controller, service, transaction, DTO, and error boundaries; approved requirements,
ADRs, and target-code conventions win for feature behavior.

## Service and API boundaries

- Keep controllers thin: validate, authorize, map, delegate, and form the HTTP response.
- Put business invariants and transaction boundaries in application services.
- Expose DTOs, not persistence entities, across API boundaries.
- Use constructor injection and explicit package/module boundaries.
- Return `Optional<T>` for absence-oriented repository lookups when useful; do not require every public
  method to return `Optional`, and never use it as a parameter type.

## Validation and errors

- Validate inputs at system boundaries and enforce domain invariants in the owning domain/application code.
- Use RFC 7807 `ProblemDetail` without stack traces, secrets, CPF, amounts, or internal implementation data.
- Use `/api/v1/{resource}` only when the approved contract defines that resource and version.
- Keep auth failures distinct from validation, not-found, conflict, and internal errors.

## Conventions

| Rule | Rationale |
| --- | --- |
| Transactions belong to services | Business operations own atomicity. |
| DTOs define API boundaries | Persistence changes do not leak into contracts. |
| Constructor injection is required | Dependencies stay explicit and testable. |
| Absence semantics are contextual | `Optional` remains useful without becoming a universal return type. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Follow approved REQ-IDs and contracts | Generate CRUD behavior without requirements |
| Preserve exact financial precision | Use `float` or `double` for money |
| Return safe machine-readable errors | Expose stack traces or sensitive values |
| Use nearby module conventions | Introduce a new dependency without an ADR |

## Checklist Before Opening a PR

- [ ] The change maps to approved requirements and stays inside the owning module.
- [ ] Controllers, services, repositories, DTOs, and transaction boundaries are correctly separated.
- [ ] Validation, authorization, and error behavior cover positive and negative paths.
- [ ] Financial values preserve explicit precision and rounding semantics.
- [ ] Focused tests and the applicable build pass.
- [ ] No sensitive data, placeholder behavior, or unrelated dependency was introduced.

---
name: aspnet-minimal-api-openapi
description: >-
  Create or review ASP.NET Minimal API endpoints with typed results, DTO validation, endpoint
  groups, filters, ProblemDetails, and OpenAPI documentation. Use this skill when asked to add
  Minimal APIs, document endpoints with Swagger/OpenAPI, use .NET 9 built-in OpenAPI, or design
  request and response types.
---

<!-- Generated from harness/github-copilot/skills/aspnet-minimal-api-openapi/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# ASP.NET Minimal API with OpenAPI

Create well-structured ASP.NET Minimal API endpoints by grouping routes, modeling request and response DTOs, returning typed results, and documenting operations so generated OpenAPI describes real behavior.

Use it for OpenAPI/Swagger documentation and strongly-typed endpoint design.
Treat endpoint filters as the cross-cutting extension point.

## When to invoke

- "Create an ASP.NET Minimal API endpoint with OpenAPI docs."
- "Add Swagger documentation for this Minimal API."
- "Use typed results for these endpoints."
- "Group these Minimal API routes."
- "Document request and response models in .NET 9 OpenAPI."

## API organization

| Concern | Recommended approach | Why it matters |
| --- | --- | --- |
| Related endpoints | Group related endpoints using `MapGroup()` extension. | Keeps shared route prefixes, tags, authorization, filters, and metadata consistent. |
| Cross-cutting behavior | Use endpoint filters for validation, logging, authorization checks, or other concerns that do not belong in handlers. | Prevents duplicated handler boilerplate. |
| Large APIs | Structure larger APIs with separate endpoint classes or extension methods. | Keeps `Program.cs` small and discoverable. |
| Complex domains | Consider feature-based folders. | Collocates endpoint mapping, DTOs, validation, and tests by capability. |

Keep handlers thin: parse typed input, call application services, map domain outcomes to HTTP results, and attach metadata.

## Request and response types

| Topic | Rule |
| --- | --- |
| DTOs | Define explicit request and response DTOs/models instead of accepting anonymous shapes. |
| Immutability | Use record types for immutable request/response objects when mutation is unnecessary. |
| Names | Use meaningful property names that align with API design standards and the public contract. |
| Validation | Create clear model classes with `[Required]` and other validation attributes to enforce constraints. |
| Nullability | Leverage nullable annotations and init-only properties so required and optional data are visible in C# and OpenAPI. |
| Errors | Use `ProblemDetailsService` and StatusCodePages to get standard error responses. |

Do not leak EF entities or internal domain models as public API contracts unless the project explicitly treats them as contracts.

## Typed result handling

| Need | API | Guidance |
| --- | --- | --- |
| Multiple outcomes | `Results<T1, T2>` | Represent success, validation, not-found, and error outcomes in the method signature. |
| Strong response metadata | `TypedResults` | Prefer `TypedResults` instead of `Results` so response types flow into OpenAPI. |
| Route parameters | Strongly-typed route parameters | Use explicit type binding such as `int id`, `Guid id`, or custom binders where supported. |
| Standard errors | `TypedResults.Problem`, `TypedResults.ValidationProblem`, `TypedResults.NotFound` | Align runtime behavior with documented OpenAPI responses. |

## OpenAPI documentation

| Documentation item | How to express it |
| --- | --- |
| Operation name | Add operationIds using `WithName`. |
| Summary and description | Define operation summary and description on the endpoint metadata supported by the target .NET version. |
| Request/response content types | Set proper content types for requests and responses. |
| Property and parameter descriptions | Add descriptions to properties and parameters with `[Description()]`. |
| Document-wide metadata | Use document transformers to add servers, tags, security schemes, and other document-level elements. |
| Schema customization | Use schema transformers to apply customizations to OpenAPI schemas. |
| Built-in support | Use the built-in OpenAPI document support added in .NET 9 when the project targets it. |

## Output template

```markdown
## ASP.NET Minimal API result

**Status:** created | reviewed | blocked
**Endpoint group:** `<route group or feature>`

| Endpoint | Request type | Response types | OpenAPI metadata |
| --- | --- | --- | --- |
| `<METHOD /route>` | `<DTO or none>` | `Results<T1, T2>` | `WithName`, summary, description, content types |

### Implementation notes
- Grouping: `<MapGroup decision>`
- Validation: `<attributes/filter/service>`
- Error shape: `<ProblemDetails/StatusCodePages behavior>`

### Validation
- `<build/test/openapi command>`: pass | fail | not run
```

## Quality gate

- [ ] Related endpoints are grouped with `MapGroup()` or the absence of grouping is justified.
- [ ] Request and response contracts use explicit DTOs/models with meaningful names.
- [ ] Validation attributes such as `[Required]` are applied where the public contract requires them.
- [ ] Handlers return `TypedResults` and `Results<T1, T2>` where multiple response types are possible.
- [ ] Standard errors use `ProblemDetailsService`, StatusCodePages, or typed problem results.
- [ ] OpenAPI includes operationIds through `WithName`, summaries/descriptions, content types, and useful schema metadata.
- [ ] Document transformers or schema transformers are used only when endpoint-level metadata is insufficient.

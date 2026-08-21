---
name: 'aspnet-minimal-api-openapi'
description: 'Create ASP.NET Minimal API endpoints with complete OpenAPI documentation.'
agent: 'agent'
tools: ['read', 'search', 'edit']
---

# /aspnet-minimal-api-openapi

## Objective

Create or review ASP.NET Minimal API endpoints with well-structured endpoints and strong request and response types, clear organization, validation, standard errors, typed results, and complete OpenAPI/Swagger documentation.

## When to Invoke

Use this prompt when adding, refactoring, or reviewing ASP.NET Minimal API routes, endpoint groups, DTOs, validation, typed results, or OpenAPI document customizations.

## Preconditions

- The ASP.NET project, endpoint target, or selected code is available.
- The intended route, request model, response model, status codes, and validation requirements are known or can be requested.
- The project targets a .NET version whose OpenAPI features are known, especially built-in OpenAPI document support added in .NET 9 when used.
- Edits are permitted when endpoint implementation is requested.

## Inputs the Team Must Provide

- `target` — the endpoint, route group, selected code, or feature to create or document.
- Route pattern, HTTP methods, request and response schemas, status codes, and validation rules.
- Authentication, authorization, error-response, and OpenAPI customization requirements.
- Existing test or build command.
- Ask the user for anything that is missing before inventing endpoint semantics.

## What I Will Do

- Group related endpoints with `MapGroup()` and use endpoint filters for cross-cutting concerns.
- Structure larger APIs with separate endpoint classes and feature-based folders when complexity warrants it.
- Define explicit request and response DTOs/models, including record types, validation attributes, meaningful names, and nullable/init-only C# features.
- Return `TypedResults` and `Results<T1, T2>` for strongly typed multiple response types.
- Document OpenAPI summaries, descriptions, operationIds through `WithName`, content types, property and parameter descriptions, document transformers, schema transformers, servers, tags, and security schemes.

## What I Will NOT Do

- Return anonymous or loosely typed responses when explicit models are required.
- Skip validation or standard error handling for request data.
- Use `Results` when `TypedResults` provides stronger response typing (strongly-typed responses).
- Claim .NET 9 built-in OpenAPI support is available when the project targets an older version without the necessary package or setup.
- Invent API behavior, response contracts, or security requirements not provided by the user or code.

## Output Format

Return or apply endpoint changes with this structure:

```markdown
### ASP.NET Minimal API OpenAPI Result

### Target
- `<route group, endpoint class, or file>`

### Endpoint Contract
| Method | Route | Request | Responses | OperationId |
| --- | --- | --- | --- | --- |
| POST | `/orders` | `CreateOrderRequest` | `Results<Created<OrderResponse>, ValidationProblem, ProblemHttpResult>` | `CreateOrder` |

### Practices Applied
- Related endpoints grouped with `MapGroup()`.
- Cross-cutting concerns implemented with endpoint filters where appropriate.
- Request and response DTOs/models are explicit records or classes with `[Required]` and other validation attributes.
- Standard errors use ProblemDetailsService and StatusCodePages.
- Route parameters use strong typing and explicit type binding.
- Responses use `TypedResults` and `Results<T1, T2>`.
- OpenAPI includes summary, description, `WithName`, `[Description()]`, content types, document transformers, schema transformers, servers, tags, and security schemes as applicable.

### Validation
- Command: `<dotnet build, dotnet test, or not run>`
- Result: `<passed, failed, or not run with reason>`
```

## Definition of Done

- [ ] Endpoints are grouped, typed, validated, and organized consistently.
- [ ] Request and response contracts are explicit and documented.
- [ ] Multiple status codes are represented with typed result unions.
- [ ] Standard ProblemDetails and StatusCodePages behavior is configured or called out.
- [ ] OpenAPI metadata is complete for operations, parameters, properties, content types, and security where applicable.
- [ ] Validation evidence or a precise not-run reason is reported.

## Prompt Body

Follow these steps in order. Preserve existing API behavior unless the request asks for a new contract.

**Step 1 — Establish the API contract.** Identify the route, method, request and response models, status codes, validation rules, authentication and authorization needs, and OpenAPI expectations. Ask for missing semantics before editing.

**Step 2 — Organize the API.** Group related endpoints using `MapGroup()`. Use endpoint filters for cross-cutting concerns. Structure larger APIs with separate endpoint classes. Consider a feature-based folder structure for complex APIs.

**Step 3 — Define request and response types.** Create explicit DTOs/models with clear validation attributes. Use record types for immutable request/response objects when appropriate. Use meaningful property names aligned with API design standards. Apply `[Required]` and other validation attributes. Use the ProblemDetailsService and StatusCodePages for standard error responses.

**Step 4 — Apply strong type handling.** Use strongly typed route parameters with explicit type binding. Use `Results<T1, T2>` to represent multiple response types. Return `TypedResults` instead of `Results` for strongly typed responses. Leverage C# 10+ features such as nullable annotations and init-only properties.

**Step 5 — Complete OpenAPI documentation.** Use built-in OpenAPI document support added in .NET 9 when the project supports it. Define operation summary and description. Add operationIds with `WithName`. Add descriptions to properties and parameters with `[Description()]`. Set proper content types for requests and responses. Use document transformers to add servers, tags, and security schemes. Use schema transformers to customize OpenAPI schemas.

**Step 6 — Validate and report.** Run the smallest existing build or test command when available. Report changed endpoints, OpenAPI coverage, validation evidence, and remaining assumptions.

## Invocation Example

```
/aspnet-minimal-api-openapi target=src/Api/OrdersEndpoints.cs route=/orders
```

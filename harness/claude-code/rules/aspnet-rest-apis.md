---
paths:
  - "**/*.cs"
  - "**/*.json"
---

<!-- Generated from harness/github-copilot/instructions/aspnet-rest-apis.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces ASP.NET Core REST API conventions for resource design, controllers, Minimal APIs, data access, authentication, validation, documentation, logging, testing, performance, and deployment.

# ASP.NET REST API Conventions — Controllers, Minimal APIs, and Operations

These instructions apply to C# and JSON files that define ASP.NET Core REST APIs. They are authoritative for REST resource design, controller-based APIs, Minimal APIs, data access boundaries, authentication and authorization, validation, error handling, documentation, observability, testing, performance, and deployment; broader C#, security, and hosting primitives win where they define stricter project-wide rules. Use ASP.NET Core 10 conventions when the target project is on that stack, and preserve educational explanations only in samples or learning-oriented code.

## API Design Fundamentals

- Design meaningful resource-oriented URLs and use HTTP verbs according to REST semantics.
- Explain REST architectural principles when adding instructional samples, but keep production code focused on implementation.
- Use status codes, content negotiation, and response formatting consistently.
- Choose controller-based APIs when attributes, filters, or established controller conventions improve clarity.
- Choose Minimal APIs when the endpoint set is small, route-group organization is clear, or reduced ceremony improves readability.
- Keep both approaches consistent in authentication, validation, versioning, documentation, and error responses.

## Project Structure and Configuration

- Use appropriate ASP.NET Core 10 Web API templates for new samples or scaffolding.
- Organize code with feature folders or domain-driven design principles where the project structure supports it.
- Keep models, services, and data access layers separated.
- Keep `Program.cs` understandable: routing, middleware, dependency injection, configuration, and environment-specific settings should be easy to review.
- Explain generated files and folders only when the change is intentionally educational.

## Controller-Based APIs

- Use RESTful controllers with resource names and HTTP verb attributes that match the operation.
- Prefer attribute routing when endpoint shape matters.
- Use `[ApiController]` so model binding, validation, and error behavior are explicit.
- Use dependency injection for controllers instead of constructing services manually.
- Select action return types intentionally: `IActionResult`, `ActionResult<T>`, or specific result types depending on the contract and readability.

## Minimal APIs

- Use Minimal API syntax for endpoint sets where route handlers remain readable.
- Organize larger Minimal API applications with route groups.
- Use endpoint routing, parameter binding, validation, and dependency injection deliberately.
- Keep route handlers thin; delegate business logic to services.
- Compare with controller-based APIs only when the tradeoff affects maintainability or project consistency.

## Data Access, Authentication, and Authorization

- Use Entity Framework Core for data access when it matches the project stack.
- Choose SQL Server, SQLite, or In-Memory storage deliberately for development and production scenarios.
- Use the repository pattern only when it provides a real boundary or improves testability.
- Apply migrations and data seeding through established EF Core mechanisms.
- Use efficient query patterns to avoid unbounded reads, N+1 behavior, and unnecessary tracking.
- Implement authentication using JWT tokens, OAuth 2.0, OpenID Connect, or Microsoft Entra ID as required.
- Use role-based and policy-based authorization consistently across controllers and Minimal APIs.

## Validation, Error Responses, and Documentation

- Validate input with data annotations or FluentValidation.
- Customize validation responses only when the API contract requires it.
- Use global exception handling middleware for unexpected failures.
- Return consistent standardized errors with Problem Details aligned to RFC 9457.
- Version APIs intentionally and document versioning for controller-based and Minimal APIs.
- Maintain Swagger/OpenAPI metadata for endpoints, parameters, responses, authentication, and consumer-facing documentation.

## Logging, Monitoring, Performance, and Deployment

- Use structured logging with Serilog or configured providers.
- Use Application Insights for telemetry collection when available.
- Include custom telemetry and correlation IDs when request tracking or distributed diagnostics require them.
- Monitor API performance, errors, and usage patterns.
- Use asynchronous programming for I/O-bound work.
- Apply caching strategies such as in-memory, distributed, and response caching when they match the data lifetime.
- Use pagination, filtering, sorting, compression, and benchmarks for large data sets and performance-sensitive endpoints.
- Containerize APIs with .NET's built-in container support where appropriate: `dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer`.
- Keep CI/CD, Azure App Service, Azure Container Apps, health checks, readiness probes, and environment-specific deployment settings explicit.

## Testing REST APIs

- Unit test controllers, Minimal API endpoint logic, and services.
- Use integration tests for endpoint routing, serialization, validation, authentication, and authorization.
- Mock dependencies where doing so isolates behavior without hiding contract issues.
- Apply test-driven development principles when the project workflow expects them.

## Good / Bad Examples

The examples below illustrate thin route handlers and standardized responses.

**Good:**

```csharp
app.MapGet("/orders/{id:guid}", async (Guid id, IOrderService orders) =>
{
    var order = await orders.FindAsync(id);

    return order is null ? Results.NotFound() : Results.Ok(order);
});
```

Why: The Minimal API endpoint uses route constraints, DI, async service delegation, and explicit status outcomes.

**Bad:**

```csharp
app.MapGet("/getOrder", () => db.Orders.ToList());
```

Why: The endpoint is not resource-oriented, hides data access inside the handler, and returns an unbounded data set.


- Keep Deployment and DevOps concerns explicit for ASP.NET Core API delivery.
## Conventions

| Rule | Rationale |
| --- | --- |
| Design resource-oriented URLs with correct HTTP verbs and status codes | API consumers get predictable REST semantics |
| Keep controllers and Minimal API handlers thin | Business logic stays testable in services |
| Use `[ApiController]`, route groups, binding, validation, and DI intentionally | Framework behavior remains explicit and consistent |
| Use EF Core, migrations, seeding, and efficient queries deliberately | Data access stays reliable and performant |
| Secure both controller-based and Minimal APIs with JWT, OAuth 2.0, OpenID Connect, Microsoft Entra ID, roles, and policies as required | Authorization gaps should not depend on endpoint style |
| Use FluentValidation or data annotations plus Problem Details under RFC 9457 | Input and error contracts stay standardized |
| Maintain Swagger/OpenAPI and API versioning metadata | Consumers can discover and migrate API contracts |
| Test units, integrations, authentication, and authorization paths | Critical API behavior is verified before deployment |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use resource nouns and HTTP verbs | Create action-style URLs such as `/getOrder` |
| Use controllers or Minimal APIs based on project needs | Mix styles randomly without organization |
| Delegate business logic to services | Put business rules directly in route handlers or controllers |
| Return `ActionResult<T>`, `IActionResult`, or specific results intentionally | Return whatever shape happens to serialize |
| Use Problem Details for standardized errors | Throw raw exceptions for expected validation failures |
| Document authentication and responses in Swagger/OpenAPI | Leave secured endpoints undocumented |
| Add pagination, filtering, and sorting for large data sets | Return unbounded collections from public endpoints |
| Add health checks and readiness probes for deployed APIs | Deploy without operational checks |

## Checklist Before Opening a PR

- [ ] Endpoints use resource-oriented routes, appropriate HTTP verbs, status codes, content negotiation, and response formatting.
- [ ] Controllers or Minimal APIs are chosen intentionally and organized consistently.
- [ ] Models, services, and data access are separated and route handlers remain thin.
- [ ] EF Core usage, migrations, seeding, and query patterns are efficient for the expected data size.
- [ ] Authentication and authorization work consistently for controller-based and Minimal APIs.
- [ ] Validation uses data annotations or FluentValidation and errors use Problem Details under RFC 9457.
- [ ] Swagger/OpenAPI and API versioning metadata are accurate.
- [ ] Unit and integration tests cover endpoint behavior, authentication, and authorization.
- [ ] Performance features and deployment concerns such as caching, compression, health checks, readiness probes, and container publishing are addressed where relevant.

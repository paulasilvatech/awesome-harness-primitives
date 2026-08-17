---
applyTo: "**/*.cs"
description: "Enforces C# application conventions for language features, formatting, nullable reference types, data access, authentication, API documentation, logging, testing, performance, and deployment."
---

# C# Conventions — Application Code and APIs

These instructions apply to C# source files matched by `**/*.cs`. They are authoritative for idiomatic C# style, nullable reference handling, comments, formatting, testing expectations, and common ASP.NET Core application concerns in matched files; project-specific architecture, API, security, and test primitives win where they define stricter rules. Treat these as passive conventions for implementation and review, not as a project-creation workflow.

## Language and Maintainability

- Use the latest C# version configured by the repository; when the project already targets the current toolchain, use C# 14 features where they improve clarity.
- Write clear, maintainable code and make only high confidence suggestions when reviewing code changes.
- Add comments for why non-obvious design decisions were made; do not restate what the code already says.
- For libraries or external dependencies, mention their usage and purpose when a comment prevents misuse.
- Handle edge cases with explicit exception handling and predictable failure paths.
- Use pattern matching and switch expressions where they simplify branching.
- Use `nameof` instead of string literals when referring to member names.

## Naming and Formatting

| Element | Convention |
| --- | --- |
| Component names, method names, public members | `PascalCase` |
| Private fields and local variables | `camelCase` |
| Interfaces | Prefix with `I`, for example `IUserService` |

- Apply the code-formatting style defined in `.editorconfig`.
- Prefer file-scoped namespace declarations and single-line using directives.
- Insert a newline before the opening curly brace of code blocks such as `if`, `for`, `while`, `foreach`, `using`, and `try`.
- Keep the final return statement of a method on its own line.
- Create XML doc comments for public APIs; include `<example>` and `<code>` blocks when examples make API usage clearer.

## Nullable Reference Types

- Declare values non-nullable by default and validate `null` at external entry points.
- Use `is null` and `is not null` instead of `== null` and `!= null`.
- Trust C# null annotations; do not add defensive null checks when the type system proves the value cannot be null.

## Project Structure and ASP.NET Core

- Organize code with feature folders or domain-driven design principles when the project structure supports it.
- Keep models, services, and data access layers separated so business logic does not leak into transport or persistence code.
- Keep `Program.cs` and configuration understandable, including environment-specific settings in ASP.NET Core 10 projects.
- Explain generated files and folders only when authoring educational sample code; production changes should follow the existing project structure.

## Data Access, Authentication, and Authorization

- Use Entity Framework Core data access patterns deliberately; document whether SQL Server, SQLite, or In-Memory storage is intended for development or production.
- Use the repository pattern only when it improves testability or abstracts a real persistence boundary.
- Implement database migrations and data seeding through established EF Core mechanisms.
- Shape queries to avoid common performance issues such as unbounded result sets and repeated database round trips.
- Implement authentication using JWT tokens, OAuth 2.0, OpenID Connect, or Microsoft Entra ID when the app requires protected flows.
- Secure controller-based APIs and Minimal APIs consistently with role-based or policy-based authorization.

## Validation, Errors, Documentation, and Observability

- Validate models with data annotations or FluentValidation and customize validation responses only when the API contract requires it.
- Use global exception handling middleware to produce consistent error responses.
- Use Problem Details for standardized error responses and align with RFC 9457.
- Document APIs with Swagger/OpenAPI, including endpoints, parameters, responses, authentication, and API versioning for controller-based and Minimal APIs.
- Use structured logging with Serilog or another provider when the project has it configured.
- Use Application Insights, custom telemetry, and correlation IDs when monitoring API performance, errors, and usage patterns.

## Testing, Performance, and Deployment

- Include tests for critical paths of the application.
- Follow nearby test style for method names and capitalization; do not emit `Act`, `Arrange`, or `Assert` comments.
- Use unit tests for services and focused integration tests for API endpoints, authentication, and authorization logic.
- Mock dependencies where effective instead of testing unrelated infrastructure.
- Use asynchronous programming for I/O, plus caching, pagination, filtering, sorting, compression, and benchmarks when the scenario requires performance work.
- Containerize APIs with .NET's built-in container support when appropriate: `dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer`.
- Keep CI/CD, Azure App Service, Azure Container Apps, health checks, readiness probes, and environment-specific deployment configuration explicit when deployment code is in scope.

## Good / Bad Examples

The examples below illustrate nullable handling, `nameof`, clear returns, and avoiding redundant comments.

**Good:**

```csharp
public string FormatDisplayName(User user)
{
    ArgumentNullException.ThrowIfNull(user);

    if (user.DisplayName is not null)
    {
        return user.DisplayName;
    }

    return user.Email;
}
```

Why: The method validates an entry-point argument, uses nullable annotations directly, and leaves the final return on its own line.

**Bad:**

```csharp
public string FormatDisplayName(User user)
{
    // Check if user is null.
    if (user == null) throw new Exception("user");
    return user.DisplayName ?? user.Email;
}
```

Why: The comment repeats the code, the null check ignores preferred syntax, and the exception does not use `nameof` or a specific exception type.


- Preserve in-memory options and test-driven development terms when documenting storage and testing choices.

- Keep Deployment and DevOps concerns explicit when publishing or operating .NET services.
## Conventions

| Rule | Rationale |
| --- | --- |
| Use the repository's configured modern C# version, including C# 14 only when supported | Prevents language-version drift while allowing current idioms |
| Follow `.editorconfig`, file-scoped namespaces, single-line using directives, and brace/newline rules | Formatting stays consistent across contributors |
| Use `PascalCase`, `camelCase`, and `IInterface` naming consistently | Readers can infer symbol roles without local explanation |
| Trust nullable reference annotations and use `is null` / `is not null` | Null handling stays precise and idiomatic |
| Keep models, services, and data access separated | Application logic remains testable and maintainable |
| Use EF Core, JWT, OAuth 2.0, OpenID Connect, Microsoft Entra ID, Swagger/OpenAPI, and Problem Details according to project needs | Common ASP.NET Core concerns stay explicit and interoperable |
| Cover critical paths with tests and omit `Act`/`Arrange`/`Assert` comments | Tests verify behavior without noisy structure comments |
| Use `dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer` when relying on .NET container publishing | Container builds remain reproducible without an unnecessary Dockerfile |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Add comments that explain why a design choice exists | Add comments that merely narrate obvious code |
| Use `nameof` for member-name references | Hardcode member names in strings |
| Validate nulls at entry points | Scatter redundant null checks after non-null annotations |
| Use feature folders or domain-driven organization when it matches the project | Mix models, services, and data access into one unstructured folder |
| Use data annotations or FluentValidation for model validation | Let invalid input reach business logic unchecked |
| Use structured logging, correlation IDs, and Application Insights where configured | Log unstructured messages that cannot be traced |
| Follow nearby test naming and capitalization | Reformat tests into a different local style |
| Add health checks and readiness probes for deployed services | Deploy APIs with no operational signal |

## Checklist Before Opening a PR

- [ ] C# syntax and language features match the repository SDK and language version.
- [ ] Formatting follows `.editorconfig`, file-scoped namespaces, single-line using directives, and brace placement rules.
- [ ] Public APIs have useful XML docs with `<example>` or `<code>` where needed.
- [ ] Nullable reference types are respected with `is null` / `is not null` checks at entry points.
- [ ] Data access, validation, authentication, authorization, logging, and monitoring stay in the appropriate layers.
- [ ] API changes update Swagger/OpenAPI, API versioning, and Problem Details behavior where applicable.
- [ ] Critical paths have tests that follow nearby naming style and avoid `Act`, `Arrange`, and `Assert` comments.
- [ ] Performance and deployment changes include appropriate caching, pagination, health checks, readiness probes, or container publishing validation.

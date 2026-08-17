---
applyTo: '**/*.razor,**/*.razor.cs,**/*.razor.css'
description: 'Enforces Blazor component conventions for Razor structure, naming, state, validation, performance, caching, API integration, testing, security, and API documentation.'
name: 'Blazor Conventions'
---

# Blazor Conventions — Component UI and Integration

This file applies to Blazor Razor components, code-behind files, and component-scoped CSS. It is authoritative for Blazor component structure, lifecycle usage, state, validation, rendering, and API integration in the matched files; broader project architecture, backend security, and testing primitives remain authoritative where they define stricter project-wide rules.

## Component Structure and Separation of Concerns

Write idiomatic, efficient Blazor and C# code that follows .NET and Blazor conventions.

- Use Razor Components for component-based UI development.
- Keep small components readable with inline functions when the logic is simple.
- Move complex logic into code-behind files or service classes instead of growing markup-heavy components.
- Keep components, services, API clients, and validation concerns separated.
- Use `async`/`await` for UI actions, API calls, and any operation that could block the UI thread.

## Naming and C# Style

| Element | Convention |
| --- | --- |
| Components | `PascalCase` |
| Methods | `PascalCase` |
| Public members | `PascalCase` |
| Private fields | `camelCase` |
| Local variables | `camelCase` |
| Interfaces | Prefix with `I`, for example `IUserService` |

Use current C# features supported by the project, including record types, pattern matching, global usings, and C# 14 features when the target SDK supports them.

## Lifecycle, Binding, and Dependency Injection

- Use Blazor lifecycle methods intentionally, especially `OnInitializedAsync` for initial asynchronous loading and `OnParametersSetAsync` for parameter-driven updates.
- Use `@bind` where two-way binding is the clearest expression of form state.
- Use Blazor Dependency Injection for services instead of manually constructing service dependencies inside components.
- Prefer `EventCallback` for user interactions and component-to-parent notifications.
- Pass only the minimal data needed through `EventCallback` payloads.

## Error Handling, Validation, and User Feedback

- Handle errors in Blazor pages and API calls instead of allowing silent failures.
- Use backend logging for server-side error tracking.
- Capture UI-level errors in Blazor with tools such as `ErrorBoundary` when a component subtree can fail independently.
- Validate forms with FluentValidation or DataAnnotations.
- When an API call fails, catch the error and provide useful feedback in the UI.

## API Integration and Documentation

- Use `HttpClient` or another appropriate injected service for calls to external APIs and backend APIs.
- Keep API communication behind services when it would otherwise add networking details directly to components.
- Document backend API services with Swagger/OpenAPI.
- Add XML documentation for API models and API methods when those comments improve generated Swagger documentation.

## Rendering and Performance

- Choose Blazor Server or Blazor WebAssembly based on project requirements rather than assuming one hosting model fits every application.
- Reduce unnecessary renders by keeping state changes focused and using `StateHasChanged()` only when an explicit render is required.
- Use `ShouldRender()` when a component has a clear, measurable reason to skip rerendering.
- Minimize the component render tree by avoiding avoidable nested components, repeated fragments, or redundant state updates.
- Keep interaction handlers efficient and avoid passing more data than the handler needs.
- Profile performance issues with IDE diagnostics tools or cross-platform tools such as `dotnet-trace` and `dotnet-counters`.

## Caching and State Management

| Scenario | Preferred approach |
| --- | --- |
| Frequently used server-side data | In-memory caching with `IMemoryCache` for lightweight Blazor Server caching |
| WebAssembly state between user sessions | `localStorage` or `sessionStorage` |
| Larger applications with shared state across users or clients | Distributed cache such as Redis or SQL Server Cache |
| Data that rarely changes | Cache API responses to avoid redundant calls |
| Basic component state sharing | Cascading Parameters and `EventCallback` |
| Complex application state | Fluxor or BlazorState when application complexity justifies it |
| WebAssembly client-side persistence | Blazored.LocalStorage or Blazored.SessionStorage |
| Server-side per-user session state | Scoped services and the StateContainer pattern |

Use state and cache mechanisms to improve user experience while minimizing unnecessary rerenders.

## Testing and Debugging

- Keep unit and integration tests runnable across Visual Studio, VS Code, and JetBrains Rider so contributors are not gated on a paid SKU.
- Test Blazor components and services with xUnit, NUnit, or MSTest.
- Mock dependencies with Moq or NSubstitute.
- Debug UI issues with browser developer tools.
- Debug backend and server-side issues with the IDE debugger.

## Security and Authentication

- Implement authentication and authorization when the Blazor application requires protected user flows.
- Use ASP.NET Identity or JWT tokens for API authentication as appropriate for the application.
- Use HTTPS for all web communication.
- Configure CORS policies deliberately for the required origins instead of relying on permissive defaults.

## Good / Bad Examples

The examples below illustrate separating API work, validation feedback, and rendering state from component markup.

**Good:**

```razor
@inject IUserService UserService

@if (loadError is not null)
{
    <ErrorBoundary>
        <p role="alert">@loadError</p>
    </ErrorBoundary>
}
else if (users is null)
{
    <p>Loading users...</p>
}
else
{
    <UserList Users="users" OnSelected="HandleSelected" />
}

@code {
    private IReadOnlyList<UserDto>? users;
    private string? loadError;

    protected override async Task OnInitializedAsync()
    {
        try
        {
            users = await UserService.GetUsersAsync();
        }
        catch (HttpRequestException)
        {
            loadError = "Users could not be loaded.";
        }
    }

    private Task HandleSelected(UserDto user) => UserService.SelectAsync(user.Id);
}
```

Why: The component uses DI, asynchronous lifecycle loading, API error handling, user feedback, and `EventCallback`-style interaction without embedding networking details in the UI.

**Bad:**

```razor
@code {
    private List<UserDto> users = new();

    protected override void OnInitialized()
    {
        var client = new HttpClient();
        users = client.GetFromJsonAsync<List<UserDto>>("/api/users").Result!;
        StateHasChanged();
    }
}
```

Why: The component manually creates dependencies, blocks the UI thread, omits error handling, and forces a render instead of using Blazor's asynchronous lifecycle conventions.

## Conventions

| Rule | Rationale |
|---|---|
| Keep simple component logic inline and move complex logic to code-behind or services | Components stay readable and maintain separation of concerns |
| Use `PascalCase` for components, methods, and public members; use `camelCase` for private fields and locals | C# and Blazor code remains idiomatic and consistent |
| Use lifecycle methods, `@bind`, DI, and `EventCallback` according to Blazor conventions | Components integrate with the framework instead of fighting it |
| Handle API and UI errors and validate forms with FluentValidation or DataAnnotations | Users receive feedback and invalid data is rejected early |
| Use async APIs for blocking work and optimize rerenders with focused state changes, `StateHasChanged()`, and `ShouldRender()` | UI remains responsive and render work stays bounded |
| Choose caching and state mechanisms that fit the hosting model and data-sharing needs | State remains durable where needed without adding unnecessary complexity |
| Keep tests cross-IDE and use xUnit, NUnit, or MSTest with Moq or NSubstitute | Contributors can validate behavior without a paid IDE dependency |
| Use authentication, authorization, HTTPS, and deliberate CORS policies for protected apps | User flows and API access remain secure |
| Maintain Swagger/OpenAPI and useful XML documentation for backend APIs | API consumers get accurate discoverable contracts |

## Do / Do Not

| Do | Do not |
|---|---|
| Use Razor Components for component-based UI | Put unrelated UI, networking, and domain logic into one component |
| Inject services through Blazor DI | Instantiate service and API dependencies manually inside components |
| Use `OnInitializedAsync` and `OnParametersSetAsync` for asynchronous and parameter-driven work | Block lifecycle methods with `.Result` or `.Wait()` |
| Use `@bind` when it clearly expresses form state | Reimplement simple two-way binding with unnecessary plumbing |
| Use `EventCallback` with minimal payloads | Pass large mutable objects when only an identifier or small value is needed |
| Validate forms with FluentValidation or DataAnnotations | Accept form input without explicit validation |
| Cache stable data with the cache mechanism that matches the hosting model | Re-fetch unchanged data on every render or interaction |
| Profile performance with IDE diagnostics, `dotnet-trace`, or `dotnet-counters` | Guess at render or runtime bottlenecks without measurement |
| Use HTTPS and deliberate CORS policies | Allow insecure or overly broad API communication defaults |

## Checklist Before Opening a PR

- [ ] Components use Razor Components idiomatically and keep complex logic in code-behind or services.
- [ ] Names follow `PascalCase`, `camelCase`, and `IInterface` conventions.
- [ ] Lifecycle methods, `@bind`, DI, and `EventCallback` are used where they fit the component behavior.
- [ ] API calls and UI failures have error handling and user feedback.
- [ ] Forms use FluentValidation or DataAnnotations when validation is required.
- [ ] Rendering changes avoid unnecessary rerenders and use `StateHasChanged()` or `ShouldRender()` only when justified.
- [ ] Caching and state management match Blazor Server or Blazor WebAssembly requirements.
- [ ] Tests can run in Visual Studio, VS Code, and JetBrains Rider using the approved test and mock frameworks.
- [ ] Protected flows use authentication, authorization, HTTPS, and deliberate CORS configuration.
- [ ] Backend API documentation remains accurate through Swagger/OpenAPI and useful XML comments.

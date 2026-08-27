---
paths:
  - "**/*.razor"
  - "**/*.razor.cs"
  - "**/*.razor.css"
---

<!-- Generated from harness/github-copilot/instructions/oqtane.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for Oqtane and Blazor modules covering component structure, client/server module patterns, services, controllers, repositories, validation, performance, caching, state, testing, and security.

# Oqtane Module Conventions — Blazor Client and Server Modules

These instructions apply to Oqtane and Blazor Razor components, code-behind files, and component CSS matched by the `applyTo` globs. They are authoritative for Oqtane module structure, Blazor component patterns, client/server service boundaries, controllers, repositories, validation, performance, caching, state, testing, and security in those files; core Oqtane framework behavior, project architecture, and stricter Blazor or C# primitives win where they define narrower rules.

## Blazor Component Structure

- Write idiomatic and efficient Blazor and C#.
- Use Razor Components and Blazor Components for component-based UI development.
- Keep simple components readable with inline functions.
- Move complex processing into code-behind files or service classes.
- Separate components, services, repositories, API calls, validation, and module business logic.
- Use `async`/`await` for UI actions, API calls, and any operation that could block the UI; preserve the baseline `Async/await` and `async/await` non-blocking expectation for every module-specific interaction.

## Naming and Language Conventions

| Element | Convention |
| --- | --- |
| Component names | `PascalCase` |
| Method names | `PascalCase` |
| Public members | `PascalCase` |
| Private fields | `camelCase` |
| Local variables | `camelCase` |
| Interfaces | Prefix with `I`, for example `IUserService` |

Use the latest C# version supported by the project. The original convention calls out C# 13 features such as record types, pattern matching, and global usings; use those features only when the target SDK supports them.

## Oqtane Client and Server Module Patterns

Follow the base classes and patterns from the main Oqtane framework at <https://github.com/oqtane/oqtane.framework>.

| Area | Convention |
| --- | --- |
| Client project | Keep modules under the `modules` folder |
| Client action | Put each action in a separate Razor file that inherits from `ModuleBase` |
| Default action | Use `index.razor` as the default action |
| Client service | For complex client processing such as getting data, create one service class per module in the `services` folder |
| Service inheritance | Client services inherit from `ServiceBase` |
| Endpoint calls | Client services call server endpoints through `ServiceBase` methods |
| Server project | Expose MVC Controllers matching the client service calls |
| Controller behavior | Controllers call server-side services or repositories managed by DI |
| Repository pattern | Use one repository class per module to match controllers |

Keep module client/server contracts aligned so a client service method has a clear server endpoint and repository path.

## Lifecycle, Binding, and API Integration

- Use Blazor lifecycle methods intentionally, especially `OnInitializedAsync` and `OnParametersSetAsync`.
- Use `@bind` for clear two-way form state.
- Use Blazor Dependency Injection for services instead of constructing dependencies in components.
- Use service base methods to communicate with external APIs or server project backends.
- Handle API calls with `try`/`catch` (`try-catch`) and provide useful UI feedback when they fail.
- Use `EventCallbacks` for user interactions and pass only minimal data.

## Error Handling, Validation, Logging, and Security

- Implement error handling for Blazor pages and API calls.
- Use built-in Oqtane logging methods from base classes where available.
- Use backend logging for error tracking.
- Capture UI-level errors with tools such as `ErrorBoundary` when a component subtree can fail independently.
- Validate forms with FluentValidation or DataAnnotations.
- Implement authentication and authorization using built-in Oqtane base class members such as `User.Roles`.
- Use HTTPS for all web communication.
- Configure CORS policies deliberately.

## Rendering, Caching, and State

| Concern | Preferred approach |
| --- | --- |
| Hosting model | Choose Blazor Server or WebAssembly based on requirements |
| Rendering | Reduce unnecessary renders and re-renders; use `StateHasChanged()` only when an explicit render is needed |
| Render suppression | Use `ShouldRender()` when there is a measurable reason to skip rerendering |
| Render tree | Avoid redundant nested components and avoidable rerenders |
| Frequent server-side data | Use `IMemoryCache` for lightweight in-memory Blazor Server caching |
| WebAssembly persistence | Use `localStorage`, `sessionStorage`, Blazored.LocalStorage, or Blazored.SessionStorage |
| Larger shared state | Consider distributed cache such as Redis or SQL Server Cache |
| Stable API responses | Cache responses to avoid redundant calls |
| Basic state sharing | Use Cascading Parameters and `EventCallbacks` |
| Client-side persistence | Use browser-backed storage only for client-side state that is safe to keep locally |
| Oqtane state | Use base class state such as `PageState` and `SiteState` when appropriate |
| Complex state | Avoid extra dependencies such as Fluxor or BlazorState unless complexity justifies them |
| Server-side per-user state | Use scoped services and the StateContainer pattern |

## Testing and Debugging

- The original convention requires unit and integration testing in Visual Studio Enterprise.
- Test Blazor components and services with xUnit, NUnit, or MSTest.
- Mock dependencies with Moq or NSubstitute.
- Debug Blazor UI issues with browser developer tools.
- Debug backend and server-side issues with Visual Studio debugging tools.
- Use Visual Studio diagnostics tools for performance profiling and optimization.

## Good / Bad Examples

The examples below illustrate Oqtane client service separation and safe component loading.

**Good:**

```razor
@inherits ModuleBase
@inject ICustomerService CustomerService

@if (loadError is not null)
{
    <p role="alert">@loadError</p>
}
else
{
    <CustomerList Customers="customers" />
}

@code {
    private IReadOnlyList<CustomerDto> customers = [];
    private string? loadError;

    protected override async Task OnInitializedAsync()
    {
        try
        {
            customers = await CustomerService.GetCustomersAsync();
        }
        catch (HttpRequestException)
        {
            loadError = "Customers could not be loaded.";
        }
    }
}
```

Why: The module inherits from `ModuleBase`, uses DI, loads asynchronously, delegates data access to a service, and gives UI feedback on failure.

**Bad:**

```razor
@code {
    protected override void OnInitialized()
    {
        var client = new HttpClient();
        customers = client.GetFromJsonAsync<List<CustomerDto>>("/api/customer").Result!;
        StateHasChanged();
    }
}
```

Why: The component manually constructs dependencies, blocks the UI thread, bypasses Oqtane service patterns, and forces a render unnecessarily.

## Conventions

| Rule | Rationale |
|---|---|
| Follow Oqtane framework base classes and module patterns from the main Oqtane repo | Modules align with the host framework instead of inventing parallel structure |
| Put each client module action in its own Razor file inheriting `ModuleBase`, with `index.razor` as the default action | Navigation and action discovery stay predictable |
| Use one client `ServiceBase` service, one MVC Controller, and one repository class per module where data access is needed | Client calls, endpoints, and persistence remain aligned |
| Use `PascalCase`, `camelCase`, `I` interface prefixes, and supported C# features | Oqtane code remains idiomatic C# and Blazor |
| Use Blazor lifecycle methods, `@bind`, DI, service base calls, and `EventCallbacks` intentionally | Components integrate with Blazor instead of fighting it |
| Handle errors, validate forms, log through Oqtane/backend mechanisms, and surface UI feedback | Failures are diagnosable and visible to users |
| Choose rendering, caching, and state mechanisms that fit Blazor Server, WebAssembly, and Oqtane state | Performance improves without unnecessary dependencies |
| Use Oqtane authentication/authorization members such as `User.Roles`, HTTPS, and deliberate CORS | Module access and communication stay secure |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `ModuleBase` and `ServiceBase` for Oqtane module code | Build module actions as unrelated standalone components |
| Keep complex client processing in one service class per module | Put data-fetching logic directly into large Razor files |
| Match client services to MVC Controllers and repositories | Let client and server module contracts drift |
| Use `OnInitializedAsync` and `OnParametersSetAsync` for lifecycle work | Block lifecycle methods with `.Result` or `.Wait()` |
| Use `PageState` and `SiteState` when Oqtane base state fits | Add Fluxor or BlazorState without justified complexity |
| Test with Visual Studio Enterprise, xUnit, NUnit, or MSTest and mocks | Skip component and service tests for module behavior |
| Authorize with Oqtane members such as `User.Roles` | Trust the UI to hide unauthorized actions without server checks |

## Checklist Before Opening a PR

- [ ] Razor module actions inherit from `ModuleBase` and `index.razor` remains the default action where applicable.
- [ ] Complex client processing lives in a module service under `services` that inherits from `ServiceBase`.
- [ ] Client service methods align with server MVC Controllers and repositories managed by DI.
- [ ] Names follow `PascalCase`, `camelCase`, and `IInterface` conventions.
- [ ] Lifecycle methods, `@bind`, DI, service base calls, and `EventCallbacks` are used appropriately.
- [ ] API calls, pages, and UI components handle errors and provide user feedback.
- [ ] Forms use FluentValidation or DataAnnotations where validation is needed.
- [ ] Rendering avoids unnecessary `StateHasChanged()` calls and uses `ShouldRender()` only with a clear reason.
- [ ] Caching and state choices match Blazor Server, WebAssembly, and Oqtane base state requirements.
- [ ] Tests and debugging follow Visual Studio Enterprise, xUnit, NUnit, MSTest, Moq, NSubstitute, browser developer tools, and diagnostics tool expectations.
- [ ] Authentication, authorization, HTTPS, and CORS are configured deliberately.

## References

- Main Oqtane framework repository: https://github.com/oqtane/oqtane.framework

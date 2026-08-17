---
applyTo: '**/*.cshtml,**/*.cshtml.cs'
description: 'Conventions for ASP.NET Core Razor Pages covering PageModels, handlers, model binding, overposting prevention, security, validation, dependency injection, Entity Framework Core, state, and testing.'
---

# C# Razor Pages Conventions — Handler-Based Pages

These instructions apply to ASP.NET Core Razor Pages `.cshtml` and `.cshtml.cs` files matched by the `applyTo` globs. They are authoritative for PageModel shape, handler methods, binding, validation, security, dependency injection, Entity Framework Core usage, state management, and tests in Razor Pages; broader ASP.NET Core architecture, domain services, and security primitives win where they impose stricter application-wide rules.

## PageModel Responsibilities and Naming

- Write idiomatic, efficient Razor Pages and C#.
- Use handler-based `PageModel` classes instead of forcing MVC controller patterns into pages.
- Keep PageModels focused on request/response orchestration.
- Put business logic in injected domain services.
- Keep trivial handlers inline; use a mediator such as MediatR when a page has many handlers or dependencies.
- Use `async`/`await` end-to-end so handlers do not block the request pipeline.

| Element | Convention |
| --- | --- |
| PageModel classes | `PascalCase`, for example `CreateModel` |
| Handler methods | `PascalCase`, for example `OnPostAsync`, `OnPostDeleteAsync` |
| Public members | `PascalCase` |
| Private fields and locals | `camelCase`, with `_` prefix on private fields per the .NET convention (`_context`, `_logger`) |
| Interfaces | Prefix with `I`, for example `IEmailService` |
| Named handler route value | Drop `OnPost` and `Async`; `OnPostJoinListAsync` is reached as `handler=JoinList` |

Preserve the interface example `IEmailService` and the end-to-end async marker `async/await` in Razor Pages guidance.

## Model Binding and Overposting

- Do not put `[BindProperty]` on EF or domain entities directly; posted extra fields such as `IsAdmin` or `Secret` can be bound even if the form does not render them.
- Bind to a dedicated Input Model or View Model that exposes only properties the page may accept, then map to the entity.
- Use `TryUpdateModelAsync<T>` with an explicit allow-list in edit scenarios when it is clearer than a separate Input Model.
- Avoid `[Bind]` for edits because excluded properties reset to `default(T)` instead of staying unchanged.
- Do not enable `[BindProperty(SupportsGet = true)]` broadly; opt in per property and validate route or query values.
- For custom types, including strongly-typed IDs, implement `TryParse` or a `TypeConverter` so route and query binding succeeds.
- Use `[BindProperty(SupportsGet = true)]` only per-property, then validate the value.
- Use `[BindRequired]` when a form source value must be present and `[Required]` when the bound value must not be null/empty. `[BindRequired]` applies only to form binding, while JSON and XML use input formatters.

## Handler Methods and Request Flow

- Use Post-Redirect-Get on successful POSTs: return `RedirectToPage("./Index")`, not `Page()`.
- Return `Page()` only when validation fails and the form needs to re-render.
- Guard every persistence path with `if (!ModelState.IsValid) return Page();`.
- Use handler parameters such as `OnGetAsync(int id)` for single-request route or query values.
- Use `[BindProperty]` for POST data that must round-trip back to the view on validation errors.
- Use `asp-page-handler` on submit buttons for named handlers such as `OnPostDeleteAsync` and `OnPostApproveAsync`.
- Add a lightweight `OnHead` when `OnGet` is expensive because Razor Pages falls back to `OnGet` for HEAD requests.
- Do not use `[ActionFilter]` attributes on page handlers; use `IPageFilter`, `IAsyncPageFilter`, or global `options.Conventions` in `Program.cs`.

## Project Structure and Security

- Put shared layouts, partials, and templates in `Pages/Shared/`; Razor resolves upward through `Pages/`, not MVC's `Views/Shared/`.
- Set `Layout` in `Pages/_ViewStart.cshtml`.
- Put `@namespace`, `@addTagHelper`, and shared directives in `Pages/_ViewImports.cshtml`.
- Keep `.cshtml` and `.cshtml.cs` files colocated.
- Trust Razor's default `@` expression HTML encoding. Don't reach for `@Html.Raw()` on user-supplied content because it disables encoding and can create XSS.
- Use `<form method="post">` and the Form Tag Helper so antiforgery tokens are injected automatically.
- For AJAX or `fetch`, render `@Html.AntiForgeryToken()` and send it as the `RequestVerificationToken` header.
- Do not commit secrets to `appsettings.json`; use `appsettings.{Environment}.json`, User Secrets with `dotnet user-secrets`, Azure Key Vault, or environment variables, and bind via `IOptions<T>`.

## Dependency Injection, EF Core, and State

- Avoid the scoped-in-singleton captive dependency trap; a singleton must not hold a scoped service such as an EF `DbContext`.
- Do not register a `DbContext` as `Singleton`; the default `AddDbContext` registration is `Scoped`.
- Project EF entities to DTOs or View Models with `.Select(...)` before returning data to the view, so views do not trigger lazy-loading re-renders or serialization cycles.
- Use `.AsNoTracking()` for read-only list and details queries.
- Prefer `FindAsync(key)` and `FindAsync` over `FirstOrDefaultAsync(x => x.Id == key)` for primary-key lookups without `Include`.
- Use `TempData` for one-shot, read-once, cookie-serialized cross-redirect messages such as flash notifications after PRG.
- Use `ISession` for per-user session state, `HttpContext.Items` for per-request data, and request-scoped DI services for shared state within one request.
- Use `TempData.Keep()` or `TempData.Peek()` when a value must survive multiple redirects.

## Testing

- Unit-test `PageModel` classes directly with mocked dependencies from Moq or NSubstitute.
- Assert returned `IActionResult` types such as `PageResult`, `RedirectToPageResult`, and `NotFoundResult`.
- Use `WebApplicationFactory<TEntryPoint>` from `Microsoft.AspNetCore.Mvc.Testing` for integration tests covering routing, model binding, and antiforgery.
- Populate `PageModel.ModelState.AddModelError(...)` manually when unit tests need invalid model state; the binding pipeline does not run in unit tests.

## Good / Bad Examples

The examples below illustrate safe POST flow and overposting prevention.

**Good:**

```csharp
public async Task<IActionResult> OnPostAsync()
{
    if (!ModelState.IsValid)
    {
        return Page();
    }

    await _service.CreateAsync(Input);
    return RedirectToPage("./Index");
}
```

Why: The handler validates server-side, delegates business work, and uses Post-Redirect-Get on success.

**Bad:**

```csharp
[BindProperty]
public User Entity { get; set; } = default!;

public IActionResult OnPost()
{
    _context.Users.Add(Entity);
    _context.SaveChanges();
    return Page();
}
```

Why: The handler binds directly to an entity, allows overposting, skips validation, performs business work in the PageModel, and returns `Page()` after a successful POST.

## Conventions

| Rule | Rationale |
|---|---|
| Keep PageModels handler-based and focused on request/response orchestration | Razor Pages stays aligned with the framework |
| Use Input Models, View Models, `TryUpdateModelAsync<T>` allow-lists, and careful `[BindProperty]` usage | Overposting and accidental resets are prevented |
| Use PRG with `RedirectToPage("./Index")` after successful POSTs | Browser refresh does not resubmit forms |
| Guard persistence with `ModelState.IsValid` and server-side validation | Client validation can be bypassed |
| Use Razor encoding, antiforgery helpers, User Secrets, Azure Key Vault, environment variables, and `IOptions<T>` | XSS, CSRF, and secret leaks are reduced |
| Keep shared Razor files under `Pages/Shared/` and directives in `Pages/_ViewStart.cshtml` or `Pages/_ViewImports.cshtml` | Razor Pages discovery remains predictable |
| Keep EF `DbContext` scoped, project entities to DTOs or View Models, and use `.AsNoTracking()` for reads | Data access avoids lifetime, tracking, and lazy-loading problems |
| Test PageModels directly and use `WebApplicationFactory<TEntryPoint>` for full pipeline tests | Handler behavior and routing are both covered |

## Do / Do Not

| Do | Do not |
|---|---|
| Bind POSTs to focused Input Models | Put `[BindProperty]` directly on EF entities |
| Use `TryUpdateModelAsync<T>` with an explicit allow-list for edits when needed | Use `[Bind]` and accidentally reset excluded properties |
| Add `asp-page-handler` for named handler buttons | Expect plain buttons to route to `OnPostDeleteAsync` automatically |
| Implement `TryParse` or `TypeConverter` for strongly typed IDs | Let custom route values silently fail binding |
| Use `IPageFilter`, `IAsyncPageFilter`, or `options.Conventions` | Add `[ActionFilter]` to page handlers |
| Render antiforgery tokens for AJAX with `@Html.AntiForgeryToken()` and `RequestVerificationToken` | Send cookie-authenticated mutations without antiforgery |
| Use `TempData.Keep()` or `TempData.Peek()` deliberately | Treat `TempData` as long-lived session storage |

## Checklist Before Opening a PR

- [ ] PageModels use Razor Pages handlers and delegate business logic to injected services.
- [ ] Names follow `PascalCase`, `_camelCase`, `IInterface`, and named-handler route conventions.
- [ ] POST binding uses Input Models, View Models, or explicit `TryUpdateModelAsync<T>` allow-lists instead of direct EF entity binding.
- [ ] GET binding with `[BindProperty(SupportsGet = true)]`, `[BindRequired]`, `[Required]`, `TryParse`, and `TypeConverter` is used only where appropriate.
- [ ] Successful POST handlers return `RedirectToPage("./Index")` or another PRG redirect, while validation failures return `Page()`.
- [ ] Persistence paths check `ModelState.IsValid`.
- [ ] Shared files, layouts, imports, and colocated `.cshtml`/`.cshtml.cs` files follow Razor Pages structure.
- [ ] Razor encoding, antiforgery, secret storage, and `IOptions<T>` conventions are respected.
- [ ] EF queries project to DTOs or View Models, use `.AsNoTracking()` for reads, and use `FindAsync(key)` for primary-key lookups when appropriate.
- [ ] State uses `TempData`, `ISession`, `HttpContext.Items`, or request-scoped DI for the correct lifetime.
- [ ] Unit and integration tests cover PageModel results, `ModelState`, routing, binding, and antiforgery as needed.

---
paths:
  - "**/*.xaml"
  - "**/*.cs"
---

<!-- Generated from harness/github-copilot/instructions/dotnet-maui.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces .NET MAUI conventions for XAML, C# views, ViewModels, lifecycle, navigation, layout, resources, storage, security, performance, and tests.

# .NET MAUI Conventions — Modern Cross-Platform UI

These instructions apply to .NET MAUI XAML and C# files matched by `**/*.xaml,**/*.cs`. They are authoritative for MAUI UI composition, MVVM separation, lifecycle, navigation, layout, resources, binding, performance, storage, and platform-safe API choices; repository-wide C#, security, and test conventions win where they define stricter rules. Use the language version supported by the repository's target .NET SDK and settings, and avoid preview language features unless the project already enables them.

## Structure, MVVM, and Naming

- Write idiomatic, efficient .NET MAUI and C# code that follows .NET and .NET MAUI conventions.
- Keep UI Views focused on layout and bindings; put logic in ViewModels and services.
- Use async/await for I/O and long-running work so the UI thread remains responsive.
- Structure components and services with Separation of Concerns.
- Prefer DI-managed services for shared state and cross-cutting concerns; keep ViewModels scoped to navigation/page lifetimes.

| Element | Convention |
| --- | --- |
| Components, methods, public members | `PascalCase` |
| Private fields and local variables | `camelCase` |
| Interfaces | Prefix with `I`, for example `IUserService` |

## Lifecycle and Navigation

- Use .NET MAUI built-in lifecycle methods such as `OnAppearing` and `OnDisappearing` for page visibility work.
- Use Shell as the primary navigation host.
- Register routes with `Routing.RegisterRoute(...)` and navigate with `Shell.Current.GoToAsync(...)`.
- Set `MainPage` once at startup and avoid changing it frequently.
- Do not mix Shell navigation with `NavigationPage`, `TabbedPage`, or `FlyoutPage`; keep the deprecated combined pattern `NavigationPage/TabbedPage/FlyoutPage.` out of new code.
- Do not nest tabs inside Shell.

## Modern Controls and Layout

- NEVER use `ListView`; use `CollectionView`.
- NEVER use `TableView`; prefer `CollectionView` or layouts such as `Grid` and `VerticalStackLayout` (`Grid/VerticalStackLayout.` in shorthand notes).
- NEVER use `Frame`; use `Border`.
- NEVER use `*AndExpand` layout options; use `Grid` and explicit sizing.
- NEVER place `ScrollView` or `CollectionView` inside `StackLayout`, `VerticalStackLayout`, or `HorizontalStackLayout` (`StackLayout/VerticalStackLayout/HorizontalStackLayout`); use `Grid` as the parent layout to preserve scrolling and virtualization.
- NEVER use renderers; use handlers.
- NEVER set `BackgroundColor`; use `Background` because it supports gradients, brushes, gradients/brushes, and modern APIs.
- Prefer `VerticalStackLayout` and `HorizontalStackLayout` over `StackLayout Orientation="..."`.
- Use `BindableLayout` for small, non-scrollable lists of ≤20 items; use `CollectionView` for larger or scrollable lists.
- Prefer `Grid` for complex layouts and subdivided space.

## Binding and Performance

- Use data binding effectively with `{Binding}` and MVVM patterns.
- Prefer compiled bindings: set `x:DataType` on pages, views, and templates (`pages/views/templates.` in migration notes).
- Prefer expression-based bindings in C# where possible.
- Consider `MauiStrictXamlCompilation=true`, especially in CI, when the project can support stricter XAML compilation.
- Use binding modes intentionally: `OneTime` for values that do not change and `TwoWay` only for editable values.
- Avoid binding static constants; set them directly.
- Avoid deep layout nesting, especially nested StackLayouts.
- Update UI from background work with `Dispatcher.Dispatch()` or `Dispatcher.DispatchAsync()`.
- Prefer `BindableObject.Dispatcher` when you have a Page, View, or BindableObject reference.
- Inject `IDispatcher` through DI in services or ViewModels without direct BindableObject access.
- Use `MainThread.BeginInvokeOnMainThread(...)` only as a fallback when no Dispatcher is available.
- Avoid obsolete `Device.BeginInvokeOnMainThread` patterns.

## Resources, APIs, Storage, and Security

- Place images in `Resources/Images/`, fonts in `Resources/Fonts/`, and raw assets in `Resources/Raw/`.
- NEVER reference images as `.svg` at runtime; use PNG/JPG resources such as `<Image Source="logo.png" />`.
- Use appropriately sized images to avoid memory bloat.
- Use `HttpClient` or appropriate services for external APIs and backend communication.
- Wrap API calls in try-catch where failures are recoverable and provide user-friendly UI feedback.
- Use `SecureStorage` for secrets such as tokens and refresh tokens; handle unsupported devices, key changes, and corruption by clearing/resetting state and re-authenticating.
- Avoid storing secrets in `Preferences`.
- Use OAuth or JWT tokens for API authentication when needed.
- Use HTTPS for web communication and configure CORS deliberately on the server side.

## Errors, Validation, Testing, and Pitfalls

- Implement error handling for .NET MAUI pages and API calls.
- Log app-level errors and surface user-friendly messages for recoverable failures.
- Validate forms with FluentValidation or DataAnnotations.
- Test components and services with xUnit, NUnit, or MSTest.
- Use Moq or NSubstitute to mock dependencies.
- Prevent gesture recognizer conflicts between parent and child views; use `InputTransparent = true` where needed.
- Unsubscribe events and dispose resources to avoid memory leaks.
- Test on physical devices when behavior depends on real hardware, OS services, performance, or platform-specific rendering.

## Good / Bad Examples

The examples below illustrate modern layout, compiled binding, and control selection.

**Good:**

```xml
<Grid RowDefinitions="Auto,*">
  <Label Text="People" />
  <CollectionView Grid.Row="1" ItemsSource="{Binding People}" x:DataType="vm:PeopleViewModel" />
</Grid>
```

Why: `Grid` hosts the scrollable `CollectionView`, compiled binding is enabled with `x:DataType`, and the layout preserves virtualization.

**Bad:**

```xml
<VerticalStackLayout>
  <Frame BackgroundColor="White">
    <ListView ItemsSource="{Binding People}" />
  </Frame>
</VerticalStackLayout>
```

Why: The markup combines deprecated `Frame`, deprecated `ListView`, `BackgroundColor`, and a scrollable control inside a stack layout.


- Treat `borders/backgrounds.` as the migration shorthand for replacing `Frame` with `Border`.
## Conventions

| Rule | Rationale |
| --- | --- |
| Keep Views focused on layout and bindings, with logic in ViewModels and services | MVVM keeps UI code testable and maintainable |
| Use Shell, `Routing.RegisterRoute(...)`, and `Shell.Current.GoToAsync(...)` consistently | Mixing navigation hosts causes broken stacks and unpredictable behavior |
| Replace `ListView`, `TableView`, `Frame`, `*AndExpand`, renderers, and `BackgroundColor` with modern APIs | Deprecated APIs reduce compatibility and performance |
| Use `Grid` around `ScrollView` and `CollectionView` | Stack parents can break scrolling and virtualization |
| Use compiled bindings with `x:DataType` and consider `MauiStrictXamlCompilation=true` | Binding errors surface earlier and run faster |
| Use `Dispatcher.Dispatch()` / `Dispatcher.DispatchAsync()` or injected `IDispatcher` for UI updates | UI state must be changed on the UI thread |
| Store secrets in `SecureStorage`, not `Preferences` | Preferences are not a secure secret store |
| Test services and components with xUnit, NUnit, or MSTest plus Moq or NSubstitute | Behavior stays verifiable outside the app shell |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `CollectionView` for scrollable lists | Use deprecated `ListView` or `TableView` |
| Use `Border` for containers | Use deprecated `Frame` |
| Use PNG/JPG resources from `Resources/Images/` | Reference `.svg` files at runtime |
| Use Shell navigation consistently | Mix Shell with `NavigationPage`, `TabbedPage`, or `FlyoutPage` |
| Use `Background` for fills, gradients, and brushes | Set `BackgroundColor` on modern controls |
| Use `OneTime` and `TwoWay` binding modes intentionally | Use two-way binding for values that never change |
| Use `SecureStorage` for tokens | Put tokens or refresh tokens in `Preferences` |
| Unsubscribe events and dispose resources | Leave handlers alive after page close |

## Checklist Before Opening a PR

- [ ] Views contain layout and bindings while ViewModels and services contain logic.
- [ ] Names follow `PascalCase`, `camelCase`, and `IInterface` conventions.
- [ ] Shell routes use `Routing.RegisterRoute(...)` and `Shell.Current.GoToAsync(...)` without mixed navigation hosts.
- [ ] Deprecated `ListView`, `TableView`, `Frame`, `*AndExpand`, renderers, `BackgroundColor`, and runtime `.svg` references are absent.
- [ ] Scrollable controls are hosted by `Grid`, not stack layouts.
- [ ] Bindings use `x:DataType`, intentional modes, and `MauiStrictXamlCompilation=true` where supported.
- [ ] UI updates from background work use Dispatcher APIs, not `Device.BeginInvokeOnMainThread`.
- [ ] Secrets use `SecureStorage`, API calls handle recoverable failures, and HTTPS is used.
- [ ] Tests cover components or services with the project test and mocking frameworks.
- [ ] Real-device and real-device testing is done when emulator-only coverage is insufficient.

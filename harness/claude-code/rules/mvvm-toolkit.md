---
paths:
  - "**/*.cs"
  - "**/*.xaml"
  - "**/*.csproj"
---

<!-- Generated from harness/github-copilot/instructions/mvvm-toolkit.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces CommunityToolkit.Mvvm conventions for ViewModels, source-generated properties, commands, messaging, validation, dependency injection, and XAML binding.

# MVVM Toolkit Conventions — CommunityToolkit.Mvvm Applications

These instructions apply to C#, XAML, and project files in applications that reference `CommunityToolkit.Mvvm`, including WPF, WinUI 3, .NET MAUI, Uno Platform, and Avalonia. They are authoritative for Toolkit package choice, ViewModel base classes, source-generated properties, commands, messaging, validation, DI, and binding; platform-specific UI and app architecture primitives win when they set stricter lifecycle or XAML rules.

## Package, Language, and ViewModel Base Classes

Reference `CommunityToolkit.Mvvm` 8.x or newer. Do not install legacy `Microsoft.Toolkit.Mvvm` 7.x for new projects. Use a C# `LangVersion` that supports source generators.

Inherit ViewModels from `ObservableObject` by default. Use `ObservableValidator` only when the ViewModel needs `INotifyDataErrorInfo` for forms, settings, or input validation. Use `ObservableRecipient` only when the ViewModel sends or receives `IMessenger` messages. Do not hand-implement `INotifyPropertyChanged` when toolkit base classes work; when inheritance is impossible, such as in a custom control, apply `[ObservableObject]` or `[INotifyPropertyChanged]` at class level.

## Properties and Generated Notifications

Declare every type using `[ObservableProperty]` as `partial`, including enclosing nested types. Apply `[ObservableProperty]` to private fields named `name`, `_name`, or `m_name`, never PascalCase; let the generator emit the public property. Do not write manual `SetProperty(ref field, value)` boilerplate for qualifying fields. Use `[NotifyPropertyChangedFor(nameof(Derived))]` for derived values and `[NotifyCanExecuteChangedFor(nameof(XxxCommand))]` so commands reevaluate when inputs change. Use `OnXxxChanging` and `OnXxxChanged` partial methods for side effects instead of subscribing to your own `PropertyChanged`. Use `[property: SomeAttribute]`, `[JsonIgnore]`, and `[JsonPropertyName(...)]` to forward attributes to generated properties.

## Commands

Use `[RelayCommand]` on instance methods instead of manually constructing `RelayCommand` or `AsyncRelayCommand`. Command methods return `void`, `Task`, or `Task<T>`; never `async void`. Add a `CancellationToken` parameter for cancellable async work and set `IncludeCancelCommand = true` when a paired `XxxCancelCommand` is needed. Use `CanExecute = nameof(...)` plus `[NotifyCanExecuteChangedFor]` on inputs. Keep `AllowConcurrentExecutions` false unless overlapping invocations are explicitly safe. Use the default await-and-rethrow error policy; set `FlowExceptionsToTaskScheduler = true` only when the UI binds to `ExecutionTask` for errors. Bind `IsRunning`, `ExecutionTask.Status`, and `ExecutionTask.Exception` rather than blocking the UI thread.

## Messaging, DI, and Validation

Default to `WeakReferenceMessenger.Default`. Use `StrongReferenceMessenger.Default` only after profiling shows the messenger is hot and lifetime guarantees are documented. Register with static `(recipient, message)` lambdas; do not capture `this`. Prefer `IRecipient<TMessage>` on `ObservableRecipient` ViewModels and use `RegisterAll(this)` with `IsActive = true` on activation and `IsActive = false` on deactivation. Inheritance is not considered for delivery, so register each concrete message type. Use channel tokens through `int`, `string`, or `Guid` overloads to scope messages.

Use `Microsoft.Extensions.DependencyInjection`, preferably with `Host.CreateDefaultBuilder()`, in the composition root such as `App.xaml.cs`. Register `IMessenger` once with `services.AddSingleton<IMessenger>(WeakReferenceMessenger.Default)`. Use `AddSingleton<T>()` for shell/main-window ViewModels, settings, file/HTTP services, and shared `IMessenger`; `AddTransient<T>()` for per-page or per-document ViewModels; and `AddScoped<T>()` only with explicit `IServiceScope`. Inject dependencies through constructors and do not call `Ioc.Default.GetService<T>()` from ViewModels or services.

For validation, use `ObservableValidator` with `[NotifyDataErrorInfo]`, `[Required]`, `[Range]`, `[EmailAddress]`, `[MinLength]`, `[MaxLength]`, and `[CustomValidation]`. Call `ValidateAllProperties()` before submit, check `HasErrors`, reset with `ClearAllErrors()`, and call `ValidateProperty(value, nameof(Other))` from `OnXxxChanged` for cross-property rules.

## XAML Binding

For WinUI 3 and UWP, prefer `{x:Bind}` over `{Binding}` and set `Mode=OneWay` or `Mode=TwoWay` explicitly because `{x:Bind}` defaults to `OneTime`. Bind `Command="{x:Bind ViewModel.SaveCommand}"` to generated command properties. Surface async progress and errors through command status properties instead of blocking.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `(r, m) => r.OnX(m)` `.csproj` `AddSingleton<T>()` `ObservableRecipient(messenger)` `OnDeactivated` `OnNavigatedFrom` `OnNavigatedTo` `RaisePropertyChanged(nameof(X))` `UnregisterAll` `async-command` `derived/computed` `enable/disable` `end-to-end` `false` `mvvm-toolkit` `partial-method` `progress/errors` `re-evaluate` `side-effects` `static` `sub-system` `true`.

Use DataAnnotation attributes with `ObservableValidator` and `[NotifyDataErrorInfo]`.

## Good / Bad Examples

The examples below show source-generated property and command usage.

**Good:**

```csharp
public partial class ProfileViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    private string name = string.Empty;

    [RelayCommand(CanExecute = nameof(CanSave))]
    private Task SaveAsync(CancellationToken token) => service.SaveAsync(Name, token);
}
```

Why: The ViewModel is partial, uses generator-friendly fields, connects command state, and returns `Task`.

**Bad:**

```csharp
public class ProfileViewModel : INotifyPropertyChanged
{
    [ObservableProperty] private string Name;
    [RelayCommand] private async void Save() { await service.SaveAsync(Name); }
}
```

Why: It hand-implements notification, uses a PascalCase field that collides with generated output, and exposes `async void` failure behavior.

## Conventions

| Rule | Rationale |
|---|---|
| Use `CommunityToolkit.Mvvm` 8.x+ instead of `Microsoft.Toolkit.Mvvm` | New projects should use supported source-generator APIs |
| Choose `ObservableObject`, `ObservableValidator`, or `ObservableRecipient` by behavior | Base classes should reflect notification, validation, or messaging needs |
| Use `[ObservableProperty]`, notification attributes, and partial hooks | Generated code removes boilerplate and keeps dependencies explicit |
| Use `[RelayCommand]` with `Task` and cancellation support | Commands remain testable, cancellable, and exception-aware |
| Register messengers and dependencies through DI | Hidden service locators break tests and lifecycle control |
| Use `WeakReferenceMessenger` by default and static handlers | Recipients avoid leaks and closure allocations |
| Use Toolkit validation attributes and APIs for forms | Validation state is consistent with XAML binding |

## Do / Do Not

| Do | Do not |
|---|---|
| Declare generated ViewModels as `partial` | Use `[ObservableProperty]` in non-partial types |
| Name backing fields `name`, `_name`, or `m_name` | Use `[ObservableProperty] private string Name;` |
| Use `[NotifyPropertyChangedFor]` and `[NotifyCanExecuteChangedFor]` | Manually raise duplicate notifications beside generated properties |
| Inject services through constructors | Call `Ioc.Default.GetService<T>()` inside ViewModels |
| Use static messenger lambdas and deactivate recipients | Capture `this` or leave `StrongReferenceMessenger` registrations pinned |
| Return `Task` from async commands | Use `async void` on `[RelayCommand]` methods |
| Replace mutated reference instances | Mutate the same reference held by an `[ObservableProperty]` field and expect notification |

## Checklist Before Opening a PR

- [ ] Project references `CommunityToolkit.Mvvm` 8.x+ and not legacy `Microsoft.Toolkit.Mvvm`.
- [ ] ViewModels use the correct Toolkit base class or class-level generator attribute.
- [ ] Generated properties are in partial types with valid backing field names and notification attributes.
- [ ] Commands use `[RelayCommand]`, `Task`, cancellation, `CanExecute`, and concurrency/error options correctly.
- [ ] Messaging uses `IMessenger`, `WeakReferenceMessenger`, static handlers, activation, deactivation, and channel tokens where needed.
- [ ] DI registration and lifetimes are defined in the composition root without `Ioc.Default.GetService<T>()` inside constructed types.
- [ ] Validation and XAML bindings surface errors, progress, and command state without blocking the UI.

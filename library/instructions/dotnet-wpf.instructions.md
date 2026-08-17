---
applyTo: '**/*.xaml,**/*.cs'
description: 'Conventions for .NET WPF applications covering MVVM structure, XAML, data binding, commands, responsiveness, performance, and testable ViewModels.'
---

# .NET WPF Conventions — MVVM Desktop Applications

These instructions apply to WPF XAML and C# files matched by the `applyTo` globs. They are authoritative for MVVM structure, XAML binding, UI responsiveness, command patterns, ViewModel testability, and WPF performance; broader C# style, product architecture, and accessibility primitives win where they define stricter requirements.

## Project Shape and Preferred Technologies

Target high-quality, maintainable desktop applications built with C# and WPF, .NET 8.0 or later when the project supports it, and XAML UI components. Prefer MVVM for separation of View, ViewModel, and Model concerns. Use `CommunityToolkit.Mvvm` or a custom `RelayCommand` implementation for boilerplate such as `INotifyPropertyChanged`, `ObservableObject`, `[ObservableProperty]`, `[RelayCommand]`, and `ICommand`.

## MVVM Structure

- Keep business logic out of code-behind; place it in ViewModels or injected services.
- Generate or implement `INotifyPropertyChanged` consistently for bindable state.
- Expose user actions through `ICommand`, `RelayCommand`, or `[RelayCommand]` instead of click handlers.
- Produce testable ViewModels by injecting dependencies and avoiding direct UI object access.
- Use ViewModel-first binding where practical.
- Use Dependency Injection with .NET or third-party containers such as Autofac or SimpleInjector when the application has multiple services.
- Avoid static event handlers unless their lifetime and detachment behavior are explicit.

## XAML and Binding

- Bind XAML controls to ViewModel properties and commands rather than tightly coupling UI elements to code-behind.
- Use `ObservableCollection<T>` for item collections that the UI must observe.
- Preserve `ObservableCollection` as the collection family for UI-observed state.
- Use `UpdateSourceTrigger=PropertyChanged` when text input must update the ViewModel as the user types.
- Prefer `nameof` over magic strings when referring to property names in C#.
- Name XAML controls with `PascalCase` and keep binding paths in `camelCase` or project-established property casing.
- Keep XAML semantic and readable; extract reusable styles or controls when markup becomes tightly coupled.

## Responsiveness and Performance

- Use `async`/`await` (`Async/await`) for non-blocking UI operations and data loading.
- Add loading indicators for operations that may visibly delay interaction.
- Enable UI virtualization for large `ListView`, `DataGrid`, or items controls.
- Avoid expensive work on the UI thread.
- Keep ViewModel state updates focused so property change notifications do not refresh unrelated UI.

## Testing and Maintainability

- Unit test ViewModels directly by asserting property changes, command availability, and service interactions.
- Mock service dependencies rather than constructing real infrastructure in ViewModel tests.
- Keep Views thin enough that most behavior can be validated without UI automation.
- Use code-behind only for view-specific concerns that cannot be expressed cleanly in XAML or bindings.

## Good / Bad Examples

The examples below illustrate command-based MVVM instead of code-behind business logic.

**Good:**

```csharp
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string userName = string.Empty;

    [RelayCommand]
    private async Task LoginAsync()
    {
        await authenticationService.LoginAsync(UserName);
    }
}
```

```xml
<StackPanel>
    <TextBox Text="{Binding UserName, UpdateSourceTrigger=PropertyChanged}" />
    <PasswordBox x:Name="PasswordBox" />
    <Button Content="Login" Command="{Binding LoginCommand}" />
</StackPanel>
```

Why: State and behavior live in a testable ViewModel, and the view binds to properties and commands.

**Bad:**

```csharp
private void LoginButton_Click(object sender, RoutedEventArgs e)
{
    var userName = UserNameTextBox.Text;
    authenticationService.Login(userName);
}
```

Why: Business behavior is tied to code-behind and UI controls, which makes testing and reuse harder.

## Conventions

| Rule | Rationale |
|---|---|
| Use MVVM with clear View, ViewModel, and service separation | UI behavior remains testable and maintainable |
| Use `INotifyPropertyChanged`, `ObservableObject`, `ObservableCollection<T>`, and `ICommand` consistently | WPF binding updates stay predictable |
| Prefer `CommunityToolkit.Mvvm` or a clear custom `RelayCommand` | Boilerplate is reduced without hiding command behavior |
| Keep XAML bound to ViewModel properties and commands | Views stay declarative and code-behind remains thin |
| Use `async`/`await`, loading indicators, and virtualization for expensive or large UI work | Desktop applications stay responsive |
| Use Dependency Injection with .NET, Autofac, or SimpleInjector when dependencies grow | ViewModels stay testable and lifetimes are explicit |
| Use `nameof` instead of magic strings | Refactoring does not silently break bindings or notifications |

## Do / Do Not

| Do | Do not |
|---|---|
| Put login, save, and load behavior in ViewModels or services | Put business logic in code-behind click handlers |
| Bind buttons to `LoginCommand` or another `ICommand` | Wire every interaction through direct event handlers |
| Use `ObservableCollection<T>` for UI-observed collections | Bind changing item lists to collections that do not notify |
| Load data asynchronously and show a spinner when needed | Block the UI thread during I/O |
| Enable virtualization for large lists | Render large collections without virtualization |
| Unit-test ViewModels with mocked dependencies | Require UI automation for ordinary business behavior |
| Use WPF and XAML patterns | Suggest WinForms or UWP approaches for WPF files |

## Checklist Before Opening a PR

- [ ] WPF code follows MVVM with business behavior in ViewModels or services, not code-behind.
- [ ] Bindable state implements `INotifyPropertyChanged` through `CommunityToolkit.Mvvm` or a consistent custom pattern.
- [ ] User actions are exposed through `ICommand`, `RelayCommand`, or `[RelayCommand]`.
- [ ] XAML uses bindings, `ObservableCollection<T>`, and `UpdateSourceTrigger=PropertyChanged` where appropriate.
- [ ] Dependency Injection is used when ViewModels require services.
- [ ] Long-running work uses `async`/`await`, loading indicators, and avoids UI thread blocking.
- [ ] Large item controls use virtualization where applicable.
- [ ] ViewModels are unit-testable without direct UI object dependencies.

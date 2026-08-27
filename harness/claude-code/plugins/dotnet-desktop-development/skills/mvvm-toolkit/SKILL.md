---
name: mvvm-toolkit
description: >-
  CommunityToolkit.Mvvm core guidance for ViewModels, source generators, observable properties,
  commands, validation, and base-class selection. Use this skill when authoring or reviewing code
  that uses CommunityToolkit.Mvvm 8.x, ObservableObject, ObservableValidator, ObservableRecipient,
  ObservableProperty, RelayCommand, AsyncRelayCommand, NotifyPropertyChangedFor,
  NotifyCanExecuteChangedFor, or NotifyDataErrorInfo across WPF, WinUI 3, MAUI, Uno, and Avalonia.
---

<!-- Generated from harness/github-copilot/plugins/dotnet-desktop-development/skills/mvvm-toolkit/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# CommunityToolkit.Mvvm core

Author or review `CommunityToolkit.Mvvm` 8.x ViewModels by choosing the right base class, applying source-generator attributes correctly, wiring commands and validation, and avoiding generator diagnostics and notification bugs.

## When to invoke

- "Create a ViewModel with CommunityToolkit.Mvvm."
- "Review my ObservableProperty and RelayCommand usage."
- "Why did MVVMTK0008 or MVVMTK0042 appear?"
- "Add validation with ObservableValidator and NotifyDataErrorInfo."
- "Fix CanExecute updates for an MVVM Toolkit command."

## Prerequisites and context

Install the toolkit package in the project that owns the ViewModels:

```xml
<ItemGroup>
  <PackageReference Include="CommunityToolkit.Mvvm" Version="8.*" />
</ItemGroup>
```

Targets include `netstandard2.0`, `netstandard2.1`, and `net6.0`+. The package works on .NET, .NET Framework, and Mono. Source generators ship with the NuGet package; no extra analyzer reference is required.

```csharp
using CommunityToolkit.Mvvm.ComponentModel;   // ObservableObject, ObservableValidator, ObservableRecipient, [ObservableProperty]
using CommunityToolkit.Mvvm.Input;             // [RelayCommand], RelayCommand, AsyncRelayCommand
```

## Generator rules

Every type that uses `[ObservableProperty]` or `[RelayCommand]`, and every enclosing type if nested, must be declared `partial`. Without `partial`, generators emit `MVVMTK0008` or `MVVMTK0042`.

| Attribute or API | Applied to | Generates or does |
| --- | --- | --- |
| `[ObservableProperty]` | private field | Public `INotifyPropertyChanged` property plus `OnXxxChanging` and `OnXxxChanged` partial-method hooks. |
| `[NotifyPropertyChangedFor(nameof(Other))]` | observable field | Also raises `PropertyChanged` for a dependent property. |
| `[NotifyCanExecuteChangedFor(nameof(MyCommand))]` | observable field | Calls `MyCommand.NotifyCanExecuteChanged()` when the field changes. |
| `[NotifyDataErrorInfo]` | observable field on `ObservableValidator` | Calls `ValidateProperty(value)` from the generated setter. |
| `[NotifyPropertyChangedRecipients]` | observable field on `ObservableRecipient` | Calls `Broadcast(old, new)` after the change. |
| `[RelayCommand]` | instance method | Lazy `RelayCommand` or `AsyncRelayCommand`, exposed as `IRelayCommand` or `IAsyncRelayCommand`. |
| `[RelayCommand(CanExecute = nameof(CanX))]` | instance method | Wires `CanExecute` to a method or property. |
| `[RelayCommand(IncludeCancelCommand = true)]` | async method with `CancellationToken` | Generates `XxxCancelCommand`. |
| `[RelayCommand(AllowConcurrentExecutions = true)]` | async method | Allows queued or parallel invocations; default disables while running. |
| `[RelayCommand(FlowExceptionsToTaskScheduler = true)]` | async method | Surfaces exceptions through `ExecutionTask` instead of awaiting and rethrowing. |
| `[property: SomeAttr]` | observable field or `[RelayCommand]` method | Forwards `SomeAttr` to the generated property, such as `[JsonIgnore]`. |

Naming rules:

| Source name | Generated name |
| --- | --- |
| field `name`, `_name`, or `m_name` | property `Name` |
| method `LoadAsync` | command `LoadCommand` |
| method `OnSave` | command `SaveCommand` |

## ViewModel patterns

Simple generated property:

```csharp
public partial class ContactViewModel : ObservableObject
{
    [ObservableProperty]
    private string? name;
}
```

Partial hooks are optional and have zero runtime cost when unimplemented. Both `(value)` and `(oldValue, newValue)` overloads are available.

```csharp
[ObservableProperty]
private string? name;

partial void OnNameChanged(string? value) =>
    Logger.LogInformation("Name changed to {Name}", value);
```

Use dependent notifications and command invalidation together when editable fields drive both computed display and button state.

```csharp
[ObservableProperty]
[NotifyPropertyChangedFor(nameof(FullName))]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
private string? firstName;

[ObservableProperty]
[NotifyPropertyChangedFor(nameof(FullName))]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
private string? lastName;

public string FullName => $"{FirstName} {LastName}".Trim();
```

Wrap non-observable models with `SetProperty` and a static lambda to avoid captured-state allocations.

```csharp
public sealed class ObservableUser(User user) : ObservableObject
{
    public string Name
    {
        get => user.Name;
        set => SetProperty(user.Name, value, user, (u, n) => u.Name = n);
    }
}
```

## Commands

Use `[RelayCommand]` for most command properties. Reach for manual `RelayCommand` or `AsyncRelayCommand` constructors only when you must own the command lifetime explicitly or compose commands from non-trivial sources.

```csharp
[RelayCommand]
private void Refresh() => Items.Reset();

[RelayCommand]
private async Task LoadAsync()
{
    foreach (var item in await service.GetItemsAsync())
        Items.Add(item);
}

[RelayCommand(IncludeCancelCommand = true)]
private async Task DownloadAsync(CancellationToken token)
{
    await using var stream = await http.GetStreamAsync(url, token);
}

[RelayCommand(CanExecute = nameof(CanSave))]
private Task SaveAsync() => repo.SaveAsync(Name!);

private bool CanSave() => !string.IsNullOrWhiteSpace(Name);
```

## Base class selection

| Base class | Use when |
| --- | --- |
| `ObservableObject` | Default: `INotifyPropertyChanged`, `INotifyPropertyChanging`, `SetProperty` overloads, and `SetPropertyAndNotifyOnCompletion` for `Task` properties. |
| `ObservableValidator` | The ViewModel needs `INotifyDataErrorInfo`, forms, or settings validation. |
| `ObservableRecipient` | The ViewModel sends or receives `IMessenger` messages. |

C# is single-inheritance. `ObservableValidator` and `ObservableRecipient` both extend `ObservableObject`, so combine validation and messaging through composition, such as injecting `IMessenger` into an `ObservableValidator`.

## Validation

Use `ObservableValidator` plus `[NotifyDataErrorInfo]` and `System.ComponentModel.DataAnnotations` attributes for generated validation setters.

```csharp
using System.ComponentModel.DataAnnotations;

public sealed partial class RegistrationViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required, MinLength(2), MaxLength(100)]
    private string? name;

    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required, EmailAddress]
    private string? email;

    [RelayCommand]
    private void Submit()
    {
        ValidateAllProperties();
        if (HasErrors) return;
    }
}
```

Other validation APIs: `TrySetProperty`, `ValidateProperty(value, name)`, `ClearAllErrors()`, and `GetErrors(propertyName)`. Custom rules can use `[CustomValidation]` methods or custom `ValidationAttribute` subclasses.

## Pitfalls

| Pitfall | Why it breaks | Fix |
| --- | --- | --- |
| Missing `partial` on a class or enclosing type | Generators cannot emit members; `MVVMTK0008` / `MVVMTK0042`. | Mark each type in the nesting chain `partial`. |
| `[ObservableProperty] private string Name;` | PascalCase field collides with generated property. | Use `name`, `_name`, or `m_name`. |
| `async void` method with `[RelayCommand]` | It becomes a sync `RelayCommand`; exceptions are unobserved. | Return `Task` so the generator creates `IAsyncRelayCommand`. |
| Missing `[NotifyCanExecuteChangedFor]` | Buttons remain disabled even when `CanSave()` changes. | Add the attribute to every observable field that affects `CanExecute`. |
| Mutating the same reference held by an `[ObservableProperty]` field | `EqualityComparer<T>.Default` sees the same reference and no notification fires. | Replace the instance or expose observable child properties. |

## Progressive disclosure and bundled resources

Read references only when the current task needs deeper detail.

- `references/source-generators.md`: full source-generator attribute reference and generated-code samples.
- `references/relaycommand-cookbook.md`: sync, async, cancellable, concurrency, and error-surfacing recipes.
- `references/validation.md`: full `ObservableValidator` surface area.
- `references/end-to-end-walkthrough.md`: Notes app sample with DI wiring, View code-behind, XAML, unit tests, and `[NotifyCanExecuteChangedFor]`.
- `references/troubleshooting.md`: `MVVMTK0xxx` diagnostics and additional pitfalls.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `mvvm-toolkit-messenger` | skill | The task centers on `IMessenger` pub/sub patterns. |
| `mvvm-toolkit-di` | skill | The task centers on `Microsoft.Extensions.DependencyInjection` wiring. |


## End-to-end mini walkthrough

Use this two-pane notes pattern when the user needs a compact sample that combines generators, commands, messenger calls, and `[NotifyCanExecuteChangedFor]`.

```csharp
public sealed partial class NoteViewModel(INotesService notes, IMessenger messenger)
    : ObservableRecipient(messenger)
{
    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    [NotifyCanExecuteChangedFor(nameof(DeleteCommand))]
    private string? filename;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    private string? text;

    [RelayCommand(CanExecute = nameof(CanSave))]
    private Task SaveAsync()
    {
        Messenger.Send(new NoteSavedMessage(Filename!));
        return notes.SaveAsync(Filename!, Text!);
    }

    [RelayCommand(CanExecute = nameof(CanDelete))]
    private Task DeleteAsync() => notes.DeleteAsync(Filename!);

    private bool CanSave() =>
        !string.IsNullOrWhiteSpace(Filename) && !string.IsNullOrEmpty(Text);

    private bool CanDelete() => !string.IsNullOrWhiteSpace(Filename);
}
```

Preserve terminology around hooks and command behavior: `single-arg`, `two-arg`, `Async`, `queued/parallel`, `allocation-free`, `to-end`, `true`, and messenger `pub/sub**` patterns.

## Output template

```markdown
## MVVM Toolkit result

**Status:** implemented | reviewed | blocked
**Target:** `<ViewModel or file>`
**Base class:** `ObservableObject | ObservableValidator | ObservableRecipient`

### Generated members used
| Source | Generated member | Notes |
| --- | --- | --- |
| `[ObservableProperty] private <field>;` | `<Property>` | `<dependent notifications or validation>` |
| `[RelayCommand] <method>` | `<MethodCommand>` | `<CanExecute/cancellation/concurrency>` |

### Validation
- `partial` declarations: pass | fail
- Commands update `CanExecute`: pass | fail | not applicable
- Validation APIs: pass | fail | not applicable
```

## Quality gate

- [ ] Every generator target and enclosing type is `partial`.
- [ ] Observable fields use `name`, `_name`, or `m_name` naming and do not collide with generated properties.
- [ ] Async commands return `Task`, not `async void`.
- [ ] Fields that affect `CanExecute` include `[NotifyCanExecuteChangedFor]`.
- [ ] Validation ViewModels inherit `ObservableValidator` and call `ValidateAllProperties()` before submit when needed.
- [ ] The selected base class matches the actual need: object, validator, or recipient.
- [ ] Referenced bundled files exist and are read only when needed.

## References

- Toolkit overview: https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/
- WinUI MVVM Toolkit tutorial: https://learn.microsoft.com/en-us/windows/apps/tutorials/winui-mvvm-toolkit/intro
- Source: https://github.com/CommunityToolkit/dotnet
- Samples: https://github.com/CommunityToolkit/MVVM-Samples

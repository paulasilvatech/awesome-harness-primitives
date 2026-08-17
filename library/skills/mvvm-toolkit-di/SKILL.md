---
name: mvvm-toolkit-di
description: >-
  Wire CommunityToolkit.Mvvm ViewModels into Microsoft.Extensions.DependencyInjection for XAML apps. Use this skill when standing up a .NET Generic Host composition root for WPF, WinUI 3, .NET MAUI, Uno, or Avalonia; choosing Singleton, Transient, or Scoped lifetimes; registering IMessenger; resolving ViewModels in Views; using keyed services; adding test seams; or replacing legacy Ioc.Default service-locator code.
---

# CommunityToolkit.Mvvm dependency injection

Use this skill to turn a XAML app's services, messengers, Views, and ViewModels into one validated `Microsoft.Extensions.DependencyInjection` graph that is built once at startup and resolved through constructors, with a report of registrations, lifetimes, and any remaining `Ioc.Default` escape hatches.

## When to invoke

- "Stand up dependency injection for a WPF, WinUI 3, .NET MAUI, Uno, or Avalonia app."
- "Choose service and ViewModel lifetimes for CommunityToolkit.Mvvm."
- "Register IMessenger and inject it into ObservableRecipient ViewModels."
- "Resolve a page ViewModel from DI without using a service locator."
- "Fix Unable to resolve service for type X while attempting to activate Y."

## Composition root

The MVVM Toolkit deliberately ships no DI container. Compose it with `Microsoft.Extensions.DependencyInjection`, the same container ASP.NET Core, Worker services, and the .NET Generic Host use. Build the service provider once at startup, preferably with `Host.CreateDefaultBuilder()`, register services and ViewModels, inject through constructors, and avoid `Ioc.Default.GetService<T>()` in user code.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using CommunityToolkit.Mvvm.Messaging;

public partial class App : Application
{
    public IHost Host { get; }

    public App()
    {
        Host = Microsoft.Extensions.Hosting.Host
            .CreateDefaultBuilder()
            .ConfigureServices((_, services) =>
            {
                services.AddSingleton<IFilesService, FilesService>();
                services.AddSingleton<ISettingsService, SettingsService>();
                services.AddSingleton<IMessenger>(WeakReferenceMessenger.Default);

                services.AddSingleton<ShellViewModel>();
                services.AddTransient<ContactViewModel>();
                services.AddTransient<EditorViewModel>();
            })
            .Build();
    }

    public static T GetService<T>() where T : class =>
        ((App)Current).Host.Services.GetRequiredService<T>();
}
```

Generic Host gives the app `appsettings.json` binding through `Microsoft.Extensions.Configuration`, logging through `Microsoft.Extensions.Logging`, `IHostedService` support for background work, and scope validation in development builds. WPF and Windows Forms must integrate the host lifetime with the app lifetime; see the WPF Generic Host reference in `## References`.

When zero extra host behavior is needed, use a bare container and still build it only once:

```csharp
var services = new ServiceCollection();
services.AddSingleton<IFilesService, FilesService>();
services.AddTransient<ContactViewModel>();
ServiceProvider provider = services.BuildServiceProvider();
```

## Constructor injection and View resolution

Inject services and child ViewModels through the constructor so dependencies are explicit, tests can pass fakes directly, startup graph validation finds missing registrations, and missing services fail immediately instead of at first use.

```csharp
public sealed partial class ContactViewModel(
    IFilesService files,
    IMessenger messenger,
    ILogger<ContactViewModel> logger)
    : ObservableRecipient(messenger)
{
    [ObservableProperty]
    private string? name;

    [RelayCommand]
    private async Task SaveAsync()
    {
        logger.LogInformation("Saving {Name}", Name);
        await files.SaveAsync(Name!);
    }
}
```

Resolve the page's root ViewModel in code-behind, then let the ViewModel pull its own dependencies:

```csharp
public sealed partial class ContactPage : Page
{
    public ContactViewModel ViewModel { get; }

    public ContactPage()
    {
        ViewModel = App.GetService<ContactViewModel>();
        InitializeComponent();
    }
}
```

Bind in XAML with `{x:Bind ViewModel.Xxx}` for compiled bindings or `{Binding Xxx}` against `DataContext`. For navigation frameworks such as WinUI 3 `Frame.Navigate`, MAUI Shell, Prism, and MVVMCross, let the framework resolve the page and let the page resolve its ViewModel from DI. Do not `new` ViewModels manually.

## Lifetimes, messenger, and keyed services

| Need | Registration | Rule |
| --- | --- | --- |
| App lifetime service or shell VM | `AddSingleton<T>` | Use for shell/main-window VM, settings, file/HTTP services, shared `IMessenger`, and app-wide caches. |
| Fresh page, document, or editor VM | `AddTransient<T>` | Use for per-page or per-document ViewModels so each resolve gets a fresh instance. |
| Per-window or per-flow lifetime | `AddScoped<T>` | Use rarely in client apps and only with an explicit `IServiceScope`. |
| Shared weak messenger | `services.AddSingleton<IMessenger>(WeakReferenceMessenger.Default)` | Default choice for most apps. |
| Strong messenger | `services.AddSingleton<IMessenger>(StrongReferenceMessenger.Default)` | Use only when strong subscriptions are intentional and lifecycle is controlled. |
| Multiple implementations | `AddKeyedSingleton<IExporter, CsvExporter>("csv")` | .NET 8+ keyed services support named dependencies. |

```csharp
services.AddSingleton<ShellViewModel>();
services.AddTransient<NoteViewModel>();
services.AddScoped<DialogService>();
services.AddSingleton<IMessenger>(WeakReferenceMessenger.Default);
services.AddSingleton<IMessenger>(StrongReferenceMessenger.Default);
```

```csharp
services.AddKeyedSingleton<IExporter, CsvExporter>("csv");
services.AddKeyedSingleton<IExporter, JsonExporter>("json");

public sealed partial class ExportViewModel(
    [FromKeyedServices("csv")] IExporter csvExporter,
    [FromKeyedServices("json")] IExporter jsonExporter)
    : ObservableObject { /* ... */ }
```

For per-window messengers, register keyed services or scoped instances and inject them into per-window ViewModels.

## Testing seams and legacy Ioc

Constructor-injected dependencies are trivial to swap in tests. With `Moq`:

```csharp
[Fact]
public async Task Save_calls_files_service()
{
    var files = new Mock<IFilesService>();
    var messenger = new WeakReferenceMessenger();
    var logger = NullLogger<ContactViewModel>.Instance;

    var vm = new ContactViewModel(files.Object, messenger, logger)
    {
        Name = "Ada"
    };

    await vm.SaveCommand.ExecuteAsync(null);

    files.Verify(f => f.SaveAsync("Ada"), Times.Once);
}
```

If a test must mock `Ioc.Default` or static state, the ViewModel is using a service locator; refactor to constructor injection.

`CommunityToolkit.Mvvm.DependencyInjection.Ioc` is an escape hatch for cases where constructor injection is impossible, such as XAML-instantiated VMs for design-time data, `ValueConverter`s, and control templates.

```csharp
Ioc.Default.ConfigureServices(
    new ServiceCollection()
        .AddSingleton<IFilesService, FilesService>()
        .AddTransient<ContactViewModel>()
        .BuildServiceProvider());

var files = Ioc.Default.GetRequiredService<IFilesService>();
```

Inside ViewModels, services, and any class the DI container can construct, prefer constructor injection.

## Gotchas

- **`Ioc.Default.GetService<T>()` inside a VM constructor hides dependencies**: it breaks unit tests and prevents startup graph validation.
- **Everything `Singleton` shares state**: a per-document VM registered as singleton becomes shared state across all documents. Use `AddTransient` for per-instance VMs.
- **Multiple `BuildServiceProvider()` calls create multiple containers**: singletons are not shared. Build once at startup.
- **Capturing `IServiceProvider` in long-lived objects is a service locator**: inject the specific dependencies instead.
- **No scope validation delays failures**: use `Host.CreateDefaultBuilder()` so `ValidateScopes` and `ValidateOnBuild` catch mistakes in development.
- **Resolving scoped services from the root provider promotes them silently**: change the lifetime or resolve from an explicit `IServiceScope`.

## Progressive disclosure and bundled resources

Read `references/dependency-injection.md` when the task needs deeper coverage of Generic Host setup, lifetimes, keyed services, testing patterns, or legacy Ioc migration.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `mvvm-toolkit` | skill | The task concerns source generators, `ObservableObject`, `[ObservableProperty]`, `[RelayCommand]`, or ViewModel authoring rather than DI wiring. |
| `mvvm-toolkit-messenger` | skill | The task concerns Messenger pub/sub surface area rather than the one-time `IMessenger` registration. |


## Compatibility vocabulary

Preserve these source terms when searching or migrating existing code: `ObservableRecipient`, `MyViewModel`, `Shell/main-window`, `fakes/mocks`, and `service/VM`. They often appear in older examples that also mention `ObservableObject`, `Ioc.Default`, or constructor injection.

## Output template

```markdown
### MVVM Toolkit DI result

**Status:** complete | needs changes | blocked
**App type:** WPF | WinUI 3 | .NET MAUI | Uno | Avalonia | other
**Composition root:** `Host.CreateDefaultBuilder()` | `ServiceCollection` | existing provider

| Registration | Lifetime | Reason | Notes |
| --- | --- | --- | --- |
| `<service or ViewModel>` | `Singleton` | `<app-wide state or shell>` | `<dependency or scope note>` |
| `<service or ViewModel>` | `Transient` | `<per-page/per-document>` | `<dependency or scope note>` |

**View resolution**
- `<View>` resolves `<ViewModel>` through `<App.GetService<T>() or framework hook>`.

**Messenger**
- `IMessenger`: `WeakReferenceMessenger.Default` | `StrongReferenceMessenger.Default` | keyed/scoped `<reason>`

**Validation**
- `BuildServiceProvider()` count: `<count and location>`
- `Ioc.Default` usage: `<none or justified escape hatch>`
- Startup graph validation: `<enabled or recommendation>`
```

## Quality gate

- [ ] `name` is `mvvm-toolkit-di` and matches the parent directory.
- [ ] The service provider is built once at startup.
- [ ] ViewModels use constructor injection instead of `Ioc.Default.GetService<T>()`.
- [ ] `IMessenger` is registered once and injected where needed.
- [ ] Singleton, Transient, and Scoped lifetimes match XAML app state boundaries.
- [ ] Views resolve root ViewModels through DI or the navigation framework, not manual `new` calls.
- [ ] Keyed services are limited to .NET 8+ scenarios and have explicit keys.
- [ ] Tests can inject fakes such as `Moq`, `WeakReferenceMessenger`, and `NullLogger<ContactViewModel>`.
- [ ] Any `Ioc.Default` usage is documented as an escape hatch.

## References

- [Dependency injection in .NET](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
- [Dependency injection usage](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-usage)
- [MVVM Toolkit Ioc](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/ioc)
- [Generic Host](https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host)
- [Use the .NET Generic Host in a WPF app](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/app-development/how-to-use-host-builder)

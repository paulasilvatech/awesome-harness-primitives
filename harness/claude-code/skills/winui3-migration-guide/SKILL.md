---
name: winui3-migration-guide
description: >-
  Maps UWP APIs and patterns to WinUI 3 and Windows App SDK equivalents with migration rules for
  namespaces, threading, windowing, dialogs, pickers, sharing, printing, background tasks,
  settings, tests, and common GitHub Copilot mistakes. Use this skill when migrating UWP apps to
  WinUI 3, reviewing generated WinUI 3 code, replacing Windows.UI.Xaml, CoreDispatcher,
  CoreWindow, MessageDialog, or GetForCurrentView patterns.
---

<!-- Generated from harness/github-copilot/skills/winui3-migration-guide/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# WinUI 3 migration guide

Migrate UWP code to WinUI 3 / Windows App SDK by replacing legacy APIs with desktop-safe equivalents. Review generated code for UWP-only patterns and produce concrete before/after guidance.

## When to invoke

- "Migrate this UWP app to WinUI 3."
- "Replace Windows.UI.Xaml APIs with Microsoft.UI.Xaml."
- "Fix this ContentDialog for WinUI 3."
- "Review this generated code for UWP patterns."
- "Convert CoreDispatcher, CoreWindow, and GetForCurrentView usage."

## Namespace changes

All `Windows.UI.Xaml.*` namespaces move to `Microsoft.UI.Xaml.*`.

| UWP namespace | WinUI 3 namespace |
| --- | --- |
| `Windows.UI.Xaml` | `Microsoft.UI.Xaml` |
| `Windows.UI.Xaml.Controls` | `Microsoft.UI.Xaml.Controls` |
| `Windows.UI.Xaml.Media` | `Microsoft.UI.Xaml.Media` |
| `Windows.UI.Xaml.Input` | `Microsoft.UI.Xaml.Input` |
| `Windows.UI.Xaml.Data` | `Microsoft.UI.Xaml.Data` |
| `Windows.UI.Xaml.Navigation` | `Microsoft.UI.Xaml.Navigation` |
| `Windows.UI.Xaml.Shapes` | `Microsoft.UI.Xaml.Shapes` |
| `Windows.UI.Composition` | `Microsoft.UI.Composition` |
| `Windows.UI.Input` | `Microsoft.UI.Input` |
| `Windows.UI.Colors` | `Microsoft.UI.Colors` |
| `Windows.UI.Text` | `Microsoft.UI.Text` |
| `Windows.UI.Core` | `Microsoft.UI.Dispatching` for dispatcher work |

## High-risk GitHub Copilot mistakes

Use WRONG/CORRECT examples for subtle migrations, especially File/Folder picker ownership and dialog threading issues.

| Mistake | Why it fails | Correct pattern |
| --- | --- | --- |
| `ContentDialog` without `XamlRoot` | Throws `InvalidOperationException` in WinUI 3. | Set `XamlRoot = this.Content.XamlRoot` before `ShowAsync()`. |
| `Windows.UI.Popups.MessageDialog` | UWP API, not available in WinUI 3 desktop. | Use `ContentDialog` with `PrimaryButtonText`, `CloseButtonText`, and `ContentDialogResult.Primary`. |
| `CoreDispatcher.RunAsync` | `CoreDispatcher` does not exist in WinUI 3. | Use `DispatcherQueue.TryEnqueue()` or `DispatcherQueue.TryEnqueue(DispatcherQueuePriority.High, ...)`. |
| `Window.Current` | No current-window singleton in WinUI 3 desktop. | Store `public static Window MainWindow { get; private set; }` in `App` during `OnLaunched`. |
| Pickers without HWND initialization | Desktop pickers need an owner window. | Use `WinRT.Interop.WindowNative.GetWindowHandle(App.MainWindow)` and `WinRT.Interop.InitializeWithWindow.Initialize(picker, hwnd)`. |

```csharp
// Correct ContentDialog pattern
var dialog = new ContentDialog
{
    Title = "Confirm",
    Content = "Are you sure?",
    PrimaryButtonText = "Yes",
    CloseButtonText = "No",
    XamlRoot = this.Content.XamlRoot
};
var result = await dialog.ShowAsync();
if (result == ContentDialogResult.Primary)
{
    // User confirmed
}
```

```csharp
// Correct DispatcherQueue pattern
DispatcherQueue.TryEnqueue(() =>
{
    StatusText.Text = "Done";
});

DispatcherQueue.TryEnqueue(DispatcherQueuePriority.High, () =>
{
    ProgressBar.Value = 100;
});
```

```csharp
// Correct picker pattern
var picker = new FileOpenPicker();
var hwnd = WinRT.Interop.WindowNative.GetWindowHandle(App.MainWindow);
WinRT.Interop.InitializeWithWindow.Initialize(picker, hwnd);
picker.FileTypeFilter.Add(".txt");
var file = await picker.PickSingleFileAsync();
```

## Windowing migration

| UWP API or pattern | WinUI 3 / Windows App SDK replacement |
| --- | --- |
| `Window.Current` | Track `App.MainWindow` or pass a `Window` reference explicitly. |
| `ApplicationView.TryResizeView()` | `AppWindow.Resize()` |
| `AppWindow.TryCreateAsync()` | `AppWindow.Create()` |
| `AppWindow.TryShowAsync()` | `AppWindow.Show()` |
| `AppWindow.TryConsolidateAsync()` | `AppWindow.Destroy()` |
| `AppWindow.RequestMoveXxx()` | `AppWindow.Move()` |
| `AppWindow.GetPlacement()` | `AppWindow.Position` property |
| `AppWindow.RequestPresentation()` | `AppWindow.SetPresenter()` |
| `CoreApplicationViewTitleBar` | `AppWindowTitleBar` |
| `CoreApplicationView.TitleBar.ExtendViewIntoTitleBar` | `AppWindow.TitleBar.ExtendsContentIntoTitleBar` |

```csharp
public partial class App : Application
{
    public static Window MainWindow { get; private set; }

    protected override void OnLaunched(LaunchActivatedEventArgs args)
    {
        MainWindow = new MainWindow();
        MainWindow.Activate();
    }
}
```

## Threading and view APIs

| UWP pattern | WinUI 3 equivalent |
| --- | --- |
| `CoreDispatcher.RunAsync(priority, callback)` and `Dispatcher.RunAsync(CoreDispatcherPriority.Normal, callback)` | `DispatcherQueue.TryEnqueue(priority, callback)`; map `CoreDispatcherPriority` values such as `CoreDispatcherPriority.Normal` to `DispatcherQueuePriority` where needed. |
| `Dispatcher.HasThreadAccess` | `DispatcherQueue.HasThreadAccess` |
| `CoreDispatcher.ProcessEvents()` | No equivalent; restructure async code. |
| `CoreWindow.GetForCurrentThread()` | Use `DispatcherQueue.GetForCurrentThread()` when appropriate. |
| `UIViewSettings.GetForCurrentView()` | Use `AppWindow` properties. |
| `ApplicationView.GetForCurrentView()` | `AppWindow.GetFromWindowId(windowId)` |
| `DisplayInformation.GetForCurrentView()` | Win32 `GetDpiForWindow()` or `XamlRoot.RasterizationScale`. |
| `CoreApplication.GetCurrentView()` | Not available; track windows manually. |
| `SystemNavigationManager.GetForCurrentView()` | Handle back navigation in `NavigationView` directly. |

Key difference: UWP uses `ASTA` (Application STA) with built-in reentrancy blocking. WinUI 3 uses standard `STA` without that protection, so review async code for reentrancy when messages are pumped.

## Dialogs, pickers, background work, and settings

| Scenario | UWP pattern | WinUI 3 replacement |
| --- | --- | --- |
| Confirmation dialog | `MessageDialog` | `ContentDialog` with `XamlRoot`. |
| File or folder picker | `FileOpenPicker` without owner | Initialize with `InitializeWithWindow.Initialize(picker, hwnd)`. |
| Background task | `IBackgroundTask`, for example `MyTask` implementing `Run(IBackgroundTaskInstance taskInstance)` | `Microsoft.Windows.AppLifecycle` and `AppInstance.GetCurrent().GetActivatedEventArgs()`. |
| Notification activation | UWP background activation | Check `args.Kind == ExtendedActivationKind.AppNotification`. |
| Packaged simple settings | `ApplicationData.Current.LocalSettings` | Keep `ApplicationData.Current.LocalSettings`. |
| Unpackaged simple settings | `ApplicationData.Current.LocalSettings` assumption | Use JSON file in `LocalApplicationData`. |
| Packaged local files | `ApplicationData.Current.LocalFolder` | Keep `ApplicationData.Current.LocalFolder`. |
| Unpackaged local files | UWP app data assumptions | Use `Environment.GetFolderPath(SpecialFolder.LocalApplicationData)`. |

```csharp
using Microsoft.Windows.AppLifecycle;

var args = AppInstance.GetCurrent().GetActivatedEventArgs();
if (args.Kind == ExtendedActivationKind.AppNotification)
{
    // Handle background activation
}
```

## Testing and project migration

| UWP | WinUI 3 |
| --- | --- |
| Unit Test App (Universal Windows) | **Unit Test App (WinUI in Desktop)** |
| Standard MSTest project with UWP types | Use WinUI test app for XAML runtime. |
| `[TestMethod]` for all tests | `[TestMethod]` for logic, `[UITestMethod]` for XAML/UI tests. |
| Class Library (Universal Windows) | **Class Library (WinUI in Desktop)** |

```csharp
[UITestMethod]
public void TestMyControl()
{
    var control = new MyLibrary.MyUserControl();
    Assert.AreEqual(expected, control.MyProperty);
}
```

`[UITestMethod]` runs the test on the XAML UI thread, which is required for instantiating any `Microsoft.UI.Xaml` type. Update the project file to target `net10.0-windows10.0.22621.0` and set `<UseWinUI>true</UseWinUI>` when that target framework is appropriate for the app.

## Migration checklist

- [ ] Replace `Windows.UI.Xaml.*` using directives with `Microsoft.UI.Xaml.*`.
- [ ] Replace `Windows.UI.Colors` with `Microsoft.UI.Colors`.
- [ ] Replace `CoreDispatcher.RunAsync` with `DispatcherQueue.TryEnqueue`.
- [ ] Replace `Window.Current` with `App.MainWindow` or explicit window references.
- [ ] Add `XamlRoot` to all `ContentDialog` instances.
- [ ] Initialize pickers with `InitializeWithWindow.Initialize(picker, hwnd)`.
- [ ] Replace `MessageDialog` with `ContentDialog`.
- [ ] Replace `ApplicationView` and `CoreWindow` with `AppWindow` patterns.
- [ ] Replace `CoreApplicationViewTitleBar` with `AppWindowTitleBar`.
- [ ] Replace `GetForCurrentView()` calls with `AppWindow` or explicit window equivalents.
- [ ] Update interop for Share and Print managers.
- [ ] Replace `IBackgroundTask` with `AppLifecycle` activation where applicable.
- [ ] Update TFM and WinUI project settings: `net10.0-windows10.0.22621.0`, `<UseWinUI>true</UseWinUI>`.
- [ ] Migrate unit tests to **Unit Test App (WinUI in Desktop)** and use `[UITestMethod]` for XAML tests.
- [ ] Test packaged and unpackaged configurations.

## Gotchas

- **Do not keep UWP singleton assumptions**: desktop WinUI 3 can have different window ownership and requires explicit HWND/XamlRoot handling.
- **Do not use `CoreDispatcher.ProcessEvents()`**: there is no equivalent; change the async design instead of forcing reentrancy.
- **Do not assume packaged APIs work unpackaged**: settings and file storage differ for unpackaged apps.

## Output template

````markdown
## WinUI 3 migration review — <file, feature, or project>

**Status:** ready | changes required | blocked
**Scope:** <UWP APIs or files reviewed>

| Area | UWP pattern found | WinUI 3 replacement | Evidence | Action |
| --- | --- | --- | --- | --- |
| Dialogs | `MessageDialog` | `ContentDialog` with `XamlRoot` | `<file:line>` | Replace dialog construction |

### Code changes
```csharp
<before/after or corrected WinUI 3 snippet>
```

### Validation
- Packaged configuration: pass | not run | blocked
- Unpackaged configuration: pass | not run | blocked
- XAML/UI tests using `[UITestMethod]`: pass | not run | blocked
````

## Quality gate

- [ ] Every `Windows.UI.Xaml.*` namespace is migrated to `Microsoft.UI.Xaml.*`.
- [ ] Dialogs set `XamlRoot` and avoid `MessageDialog`.
- [ ] Pickers are initialized with an owner HWND.
- [ ] `CoreDispatcher`, `CoreWindow`, `ApplicationView`, and `GetForCurrentView()` usages are replaced or explicitly justified.
- [ ] Window state uses `AppWindow`, explicit `Window` references, or `App.MainWindow` rather than `Window.Current`.
- [ ] Background activation uses `Microsoft.Windows.AppLifecycle` where UWP `IBackgroundTask` no longer applies.
- [ ] Test projects use WinUI 3 desktop test templates and `[UITestMethod]` for XAML interaction.

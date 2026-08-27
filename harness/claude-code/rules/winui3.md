---
paths:
  - "**/*.xaml"
  - "**/*.cs"
  - "**/*.csproj"
---

<!-- Generated from harness/github-copilot/instructions/winui3.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces WinUI 3 and Windows App SDK conventions for XAML, namespaces, threading, windowing, dialogs, MVVM, project setup, styling, accessibility, testing, and resources.

# WinUI 3 Conventions — Windows App SDK Desktop Apps

These instructions apply to WinUI 3 XAML, C# code, and project files for Windows App SDK desktop applications. They are authoritative for avoiding legacy UWP APIs, using Microsoft.UI namespaces, threading, windowing, dialogs, MVVM, binding, styling, accessibility, performance, tests, and resources in matched files; project-specific UX, security, localization, and test primitives win when they define stricter app-wide standards.

## Windows App SDK API Boundaries

Use Windows App SDK and WinUI 3 APIs, not legacy UWP APIs. Replace `Windows.UI.Popups.MessageDialog` with `ContentDialog` and set `dialog.XamlRoot = this.Content.XamlRoot` before `ShowAsync()`. Replace `CoreDispatcher.RunAsync` and `Dispatcher.RunAsync` with `DispatcherQueue.TryEnqueue`. Track the main window through `App.MainWindow` instead of `Window.Current`. Use `Microsoft.UI.Xaml.*`, `Microsoft.UI.Composition`, and `Microsoft.UI.Colors`, not `Windows.UI.Xaml.*`, `Windows.UI.Composition`, or `Windows.UI.Colors`. Use `Microsoft.UI.Windowing.AppWindow`, `AppWindowTitleBar`, and `AppWindow` APIs instead of `ApplicationView`, `CoreWindow`, `CoreApplicationViewTitleBar`, or `GetForCurrentView()` patterns such as `UIViewSettings.GetForCurrentView()`.

Use `IPrintManagerInterop` and `IDataTransferManagerInterop` with a window handle for print and share. Use `Microsoft.Windows.AppLifecycle` activation instead of UWP `IBackgroundTask`. Use `OAuth2Manager` for authentication when Windows App SDK 1.7+ is available instead of `WebAuthenticationBroker`.

## XAML, Binding, and Layout

The default XAML namespace maps to `Microsoft.UI.Xaml`. Prefer `{x:Bind}` over `{Binding}` for compiled, type-safe, higher-performance binding; under NativeAOT only `{x:Bind}` works. Set `x:DataType` on `DataTemplate` when using `{x:Bind}` and on Page/UserControl when compile-time validation is useful. Use `Mode=OneWay` for dynamic values, `Mode=OneTime` for static values, and `Mode=TwoWay` only for editable inputs. Set static constants directly in XAML.

Use a 4px grid system for margins, padding, and spacing: 4, 8, 12, 16, and 24. Prefer `Grid` over deeply nested `StackPanel` chains. Use `Auto` for content-sized rows or columns, `*` for proportional sizing, and avoid fixed pixel sizes. Use `VisualStateManager` with `AdaptiveTrigger` at 640px and 1008px. Use `ControlCornerRadius` for 4px controls and `OverlayCornerRadius` for 8px cards, dialogs, and flyouts.

## Threading, Windowing, Dialogs, and Pickers

Use `DispatcherQueue.HasThreadAccess` before dispatching UI updates and `DispatcherQueue.TryEnqueue(() => { ... })` for background-thread UI work. `TryEnqueue` returns `bool`, not `Task`; treat it as fire-and-forget. WinUI 3 uses standard STA, not ASTA, so avoid async code that accidentally pumps messages.

Get an `AppWindow` from `WindowNative.GetWindowHandle`, `Win32Interop.GetWindowIdFromWindow`, and `AppWindow.GetFromWindowId`. Use `AppWindow` for resize, move, title, presenter operations, and `AppWindow.TitleBar` custom title bar properties. Initialize file and folder pickers with `WinRT.Interop.InitializeWithWindow.Initialize(picker, hwnd)` using a `hwnd` from `WindowNative.GetWindowHandle(App.MainWindow)`.

## MVVM, Project Setup, and C# Style

Use `CommunityToolkit.Mvvm` with `[ObservableProperty]` and `[RelayCommand]` for MVVM infrastructure. Use `Microsoft.Extensions.DependencyInjection` for services and ViewModels. Keep Views focused on layout and bindings; keep logic in ViewModels and services. Use `async`/`await` for I/O and long-running work.

Target `net10.0-windows10.0.22621.0` or the appropriate TFM for the project's SDK, set `<UseWinUI>true</UseWinUI>`, reference a stable `Microsoft.WindowsAppSDK` NuGet package, and use `System.Text.Json` source generators for JSON serialization. Use file-scoped namespaces, nullable reference types, `is null` / `is not null`, pattern matching, PascalCase for types/methods/properties, camelCase for private fields, Allman braces, explicit built-in types, and `var` only when the type is obvious.

## Typography, Theming, Materials, Motion, and Controls

Use built-in TextBlock styles: `CaptionTextBlockStyle`, `BodyTextBlockStyle`, `BodyStrongTextBlockStyle`, `SubtitleTextBlockStyle`, `TitleTextBlockStyle`, `TitleLargeTextBlockStyle`, and `DisplayTextBlockStyle`. Keep Segoe UI Variable as the default font and use sentence casing for UI text.

Use `{ThemeResource}` for brushes and colors so Light, Dark, and High Contrast themes work. Do not hardcode `#FFFFFF`, `Colors.White`, `FontSize`, `FontWeight`, or `FontFamily` when built-in resources fit. Use `TextFillColorPrimaryBrush`, `CardBackgroundFillColorDefaultBrush`, `CardStrokeColorDefaultBrush`, `ControlStrokeColorDefaultBrush`, `SystemAccentColor`, and `Light1`–`Light3` or `Dark1`–`Dark3` variants.

Use `MicaBackdrop` for app window backdrop, Acrylic only for transient flyouts, menus, and navigation panes, `LayerFillColorDefaultBrush` over Mica, and `ThemeShadow` plus Z-axis `Translation` for elevation: cards 4–8 px, flyouts 32 px, dialogs 128 px. Prefer `EntranceThemeTransition`, `RepositionThemeTransition`, `ContentThemeTransition`, and `AddDeleteThemeTransition` over custom storyboard animations.

Use `NavigationView`, `InfoBar`, `TeachingTip`, `NumberBox`, `ToggleSwitch`, `ItemsView`, `ListView`, `GridView`, `ItemsRepeater`, and `Expander` for their intended controls. Prefer `ItemsView` for modern collections, `ListView`/`GridView` for standard virtualized lists and built-in selection, and `ItemsRepeater` only for fully custom virtualizing layouts.

## Accessibility, Performance, Settings, Error Handling, Testing, and Resources

Set `AutomationProperties.Name` on interactive controls, `AutomationProperties.HeadingLevel` on section headers, and `AutomationProperties.AccessibilityView="Raw"` on decorative elements. Ensure keyboard navigation with Tab, Enter, Space, and arrow keys and meet WCAG contrast.

Use `x:Load` or `x:DeferLoadStrategy` for deferred UI, virtualization for large lists, async I/O, and no UI thread blocking. For packaged apps, `ApplicationData.Current.LocalSettings` works; for unpackaged apps, use a custom settings file such as JSON under `Environment.GetFolderPath(SpecialFolder.LocalApplicationData)` and check packaging status before assuming `ApplicationData` exists.

Wrap `async void` event handlers in try/catch, use `InfoBar` with `Severity = Error` for routine user-facing errors, and handle `App.UnhandledException` for logging and graceful recovery. For tests that instantiate `Microsoft.UI.Xaml` controls, pages, or user controls, use a Unit Test App (WinUI in Desktop) project and `[UITestMethod]`; use `[TestMethod]` for pure logic. Put testable business logic in a Class Library (WinUI in Desktop) project and build before test discovery. Store strings in `Resources.resw`, use `x:Uid`, and reference DPI-qualified images such as `logo.scale-200.png` through `ms-appx:///Assets/logo.png`.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `== null` `AdaptiveTrigger` `ApplicationData` `ControlCornerRadius` `DataTransferManager` `File/Folder` `NEVER` `OnLaunched` `OverlayCornerRadius` `PrintManager` `Share/Print**` `VisualStateManager` `Window` `Windows.UI.Xaml` `in-app` `on/off` `reflection-based` `rows/columns`.

Include `DataContext` considerations when using `{Binding}`; prefer `NumberBox` over `TextBox` for numeric input and `ToggleSwitch` over `CheckBox` for on/off settings.

## Good / Bad Examples

The examples below show safe dialog and threading conventions.

**Good:**

```csharp
var dialog = new ContentDialog { XamlRoot = Content.XamlRoot, Title = "Saved" };
await dialog.ShowAsync();
DispatcherQueue.TryEnqueue(() => StatusText.Text = "Done");
```

Why: It uses WinUI 3 dialog rooting and `DispatcherQueue` instead of UWP APIs.

**Bad:**

```csharp
await new Windows.UI.Popups.MessageDialog("Saved").ShowAsync();
await Window.Current.Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () => { });
```

Why: It uses UWP dialog, `Window.Current`, and dispatcher patterns that are wrong for WinUI 3 desktop apps.

## Conventions

| Rule | Rationale |
|---|---|
| Use Windows App SDK APIs and `Microsoft.UI.*` namespaces | UWP APIs are missing or incorrect in WinUI 3 desktop apps |
| Set `XamlRoot` before every `ContentDialog.ShowAsync()` | Dialogs need the correct visual tree root to render |
| Use `DispatcherQueue.TryEnqueue` and check `HasThreadAccess` | UI updates must run on the UI thread without assuming a `Task` return |
| Prefer `{x:Bind}` and typed templates | Binding errors surface at compile time and NativeAOT remains compatible |
| Keep View logic in ViewModels and services | Views remain layout-focused and testable |
| Use theme resources, built-in typography, and semantic controls | Apps support accessibility, theming, and platform consistency |
| Use WinUI test app infrastructure for XAML tests | Plain MSTest or xUnit projects lack XAML runtime and UI thread support |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `Microsoft.UI.Xaml.*` | Use `Windows.UI.Xaml.*` |
| Use `AppWindow` and `AppWindowTitleBar` | Use `ApplicationView`, `CoreWindow`, or `CoreApplicationViewTitleBar` |
| Initialize pickers and share/print APIs with a window handle | Call UWP picker, share, or print APIs without interop |
| Use `{ThemeResource}` and built-in TextBlock styles | Hardcode colors, fonts, weights, or sizes |
| Use `InfoBar` for routine errors | Use `ContentDialog` for every error message |
| Use Unit Test App (WinUI in Desktop) for XAML tests | Instantiate WinUI 3 XAML types from plain MSTest or xUnit projects |

## Checklist Before Opening a PR

- [ ] No legacy UWP API, `Windows.UI.*` namespace, `Window.Current`, `CoreWindow`, or `GetForCurrentView()` pattern remains.
- [ ] Dialogs, pickers, share, and print APIs have the correct `XamlRoot` or window handle.
- [ ] UI-thread updates use `DispatcherQueue` correctly.
- [ ] XAML uses `{x:Bind}`, `x:DataType`, binding modes, layout, spacing, and controls appropriately.
- [ ] MVVM, DI, C# style, project TFM, `<UseWinUI>true</UseWinUI>`, and `Microsoft.WindowsAppSDK` references are correct.
- [ ] Theme, typography, materials, motion, accessibility, localization, and resources follow platform conventions.
- [ ] Tests use the correct WinUI test project type when XAML runtime is required.

---
applyTo: "**/*.csproj,**/*.cs,**/*.xaml"
description: "Enforces .NET MAUI 9 to .NET MAUI 10 upgrade conventions for target frameworks, package compatibility, breaking API replacements, obsolete controls, deprecated async APIs, media picking, handlers, and validation."
---

# .NET MAUI 10 Upgrade Conventions — .NET 9 Migration Compatibility

These instructions apply to .NET MAUI project files, C# code, and XAML that are being upgraded from .NET 9 to .NET 10. They are authoritative for TargetFramework updates, CommunityToolkit compatibility, .NET MAUI 10 BREAKING changes, OBSOLETE and DEPRECATED API migrations, ListView/TableView replacement, CollectionView behavior, MediaPicker return-shape changes, and validation expectations in matched files; official .NET MAUI and CommunityToolkit documentation wins where vendor behavior differs, and broader project build, architecture, testing, or security primitives win where they define stricter repository-wide rules.

## Target Frameworks and Package Compatibility

Target .NET 10 deliberately and keep platform targets buildable on the machines that will compile the app.

| Concern | Convention |
| --- | --- |
| Single platform | Use `<TargetFramework>net10.0</TargetFramework>`. |
| Multi-platform | Use `<TargetFrameworks>net10.0-android;net10.0-ios;net10.0-maccatalyst;net10.0-windows10.0.19041.0</TargetFrameworks>` when every target is buildable in the environment. |
| Linux, GitHub Codespaces, WSL, and Copilot builds | Start with `net10.0-android`, conditionally add `net10.0-ios` and `net10.0-maccatalyst` when `!$([MSBuild]::IsOSPlatform('linux'))`, and conditionally add `net10.0-windows10.0.19041.0` when `$([MSBuild]::IsOSPlatform('windows'))`. |
| CommunityToolkit.Maui | Update to 12.3.0 or later when the app uses it; older versions are not compatible with .NET 10. |
| Microsoft.Maui.Controls | Pin to a .NET 10 compatible package such as `10.0.0` when the project manages the package explicitly. |
| SDK floor | Use .NET SDK `10.0.100` or later and run `dotnet workload update` after installing or switching SDKs. |

Keep the project file shape explicit: `Microsoft.NET.Sdk` remains the MAUI project SDK, `PropertyGroup` remains the home for TargetFramework properties, and package changes remain normal `NuGet` dependency changes rather than ad hoc file edits.

Use these commands as migration checks, not as blind edits:

```bash
dotnet add package CommunityToolkit.Maui --version 12.3.0
dotnet add package Microsoft.Maui.Controls --version 10.0.0
dotnet add package CommunityToolkit.Mvvm --version 8.3.0
dotnet list package --outdated
dotnet --version
dotnet workload update
```

Do not pipe `dotnet list package --outdated` into automatic package updates without reviewing each package; transitive MAUI, Android, iOS, Windows, and toolkit compatibility can differ by platform.

## Breaking Changes and Priority Rules

Treat the upgrade as a compatibility migration, not a cosmetic refactor.

| Priority | Required response |
| --- | --- |
| P0 — Breaking/Critical | Fix `MessagingCenter`, `ListView`, `TableView`, `TextCell`, `ImageCell`, `EntryCell`, `SwitchCell`, `ViewCell`, `ContextActions`, and platform-specific ListView code before shipping. |
| P1 — Deprecated APIs | Replace animation methods, dialog methods, `Page.IsBusy`, and MediaPicker single-selection APIs so `CS0618` does not remain in normal build output. |
| P2 — Recommended changes | Prefer `Application.CreateWindow` over `Application.MainPage` during the upgrade when the app initialization code is already being touched. |

Common compiler indicators are `CS0122` for `MessagingCenter` becoming inaccessible because it is now `internal`, and `CS0618` for obsolete controls or methods. Keep `CRITICAL`, `REQUIRED`, `MAJOR`, `BREAKING`, `DEPRECATED`, and `OBSOLETE` meanings strict: use them only where compatibility, runtime behavior, or future removal is at stake.

## MessagingCenter Replacement

Replace `MessagingCenter` with `CommunityToolkit.Mvvm` `WeakReferenceMessenger` from `CommunityToolkit.Mvvm.Messaging`. The new model is type-safe, avoids magic strings, improves IntelliSense, and is easier to refactor, but it changes subscription behavior.

| Old pattern | Required .NET 10 pattern |
| --- | --- |
| `MessagingCenter.Send(this, "UserLoggedIn", userData)` | `WeakReferenceMessenger.Default.Send(new UserLoggedInMessage(userData));` |
| `MessagingCenter.Send<App, string>(this, "StatusChanged", "Active")` | `WeakReferenceMessenger.Default.Send(new StatusChangedMessage("Active"));` |
| `MessagingCenter.Subscribe<App, UserData>(this, "UserLoggedIn", handler)` | `WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (recipient, message) => { ... });` |
| `MessagingCenter.Unsubscribe<App, UserData>(this, "UserLoggedIn")` | `WeakReferenceMessenger.Default.Unregister<UserLoggedInMessage>(this);` or `WeakReferenceMessenger.Default.UnregisterAll(this);` |

Define message classes that carry the payload explicitly:

```csharp
public sealed class UserLoggedInMessage
{
    public UserLoggedInMessage(User user) => User = user;

    public User User { get; }
}
```

Do not register the same message type more than once for the same recipient. `WeakReferenceMessenger` throws `InvalidOperationException` on duplicate registrations, while `MessagingCenter` allowed duplicate subscriptions. If code registers in a constructor and again in `OnAppearing`, unregister before re-registering or combine the work into one registration:

```csharp
WeakReferenceMessenger.Default.Unregister<UserLoggedInMessage>(this);
WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (r, m) => Handler1(m));

WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (r, m) =>
{
    Handler1(m);
    Handler2(m);
});
```

Unregister in lifecycle paths such as `OnDisappearing` when the recipient should stop receiving messages; forgetting to unregister can preserve stale page behavior and make runtime crashes hard to diagnose.

When converting old examples, keep the lifecycle and state responsibilities visible: `InitializeComponent` still initializes the page, sender code such as `LoginAsync` or `AuthService.LoginAsync` still owns authentication, and receiver state such as `CurrentUser` still belongs in the page or ViewModel that consumes the message.

## ListView, TableView, Cells, and CollectionView Migration

Migrate `ListView` and `TableView` to `CollectionView` or a small `BindableLayout` settings layout. This is a MAJOR migration because it changes selection, grouping, context actions, sizing, virtualization, platform configuration, and test expectations; it CANNOT be a find-replace or find/replace-only task.

| Legacy MAUI 9 API | .NET 10 replacement |
| --- | --- |
| `ListView` | `CollectionView` |
| `TableView` | `CollectionView`, or `VerticalStackLayout` with `BindableLayout` for small settings pages |
| `TextCell` | Custom `DataTemplate` with `Label` controls |
| `ImageCell` | Custom `DataTemplate` with `Image` plus labels |
| `EntryCell` | Custom `DataTemplate` with `Entry` |
| `SwitchCell` | Custom `DataTemplate` with `Switch` |
| `ViewCell` | Plain `DataTemplate` content |
| `ItemSelected` | `SelectionChanged` |
| `SelectedItemChangedEventArgs` and `e.SelectedItem` | `SelectionChangedEventArgs` and `e.CurrentSelection.FirstOrDefault()` |
| `ContextActions` | `SwipeView` |
| `IsGroupingEnabled="True"` | `IsGrouped="true"` or `IsGrouped="True"` consistently with project XAML style |
| `GroupDisplayBinding` | `GroupHeaderTemplate` |
| `HasUnevenRows` and `HasUnevenRows="False"` | `CollectionView` auto-sizes; use `ItemSizingStrategy` when measurement cost matters |
| Manual empty-state layout | Built-in `EmptyView` |

Set selection deliberately because `CollectionView` defaults to `SelectionMode="None"`. Use `SelectionMode="Single"` or `SelectionMode="Multiple"` only when selection behavior is required, and clear `((CollectionView)sender).SelectedItem = null;` only when the UI should visually deselect after acting.

Check `CurrentSelection.Count` before reading the selected item. Cast the selected item to the real item type, not a placeholder such as `MyItem`, and keep selection code null-safe because `SelectionChanged` can fire for deselection as well as selection.

Grouped lists need `CollectionView.GroupHeaderTemplate`; simple settings pages with fewer than about 20 items may use `VerticalStackLayout` plus `BindableLayout`, while longer or grouped settings pages should use `CollectionView`. Use `SwipeView` for destructive actions, but provide an alternate desktop affordance such as buttons or a right-click menu because SwipeView requires touch input and may not work with mouse/trackpad on Windows.

For item measurement, keep the default `ItemSizingStrategy="MeasureAllItems"` when heights vary and use `ItemSizingStrategy="MeasureFirstItem"` when rows are visually uniform and large-list performance matters. Keep templates shallow; prefer `Grid` or a simple `VerticalStackLayout` over deeply nested layouts.

Use the specific CollectionView and XAML members below rather than carrying ListView-era behavior forward:

| Scenario | Use these APIs and properties | Avoid |
| --- | --- | --- |
| Empty state | `CollectionView.EmptyView` with a small `ContentView` | Manual placeholder views disconnected from the list state |
| Header and footer | `CollectionView.Header` and `CollectionView.Footer` | Fake first or last data items |
| Item spacing | `CollectionView.ItemsLayout`, `ItemsLayout`, `LinearItemsLayout`, and `ItemSpacing` | Padding hacks inside every child item |
| Pull to refresh | Wrap in `RefreshView` with `IsRefreshing` and `RefreshCommand` | Old ListView refresh assumptions |
| Infinite scroll | `RemainingItemsThreshold` and `RemainingItemsThresholdReachedCommand` such as `LoadMoreCommand` | Scroll event polling |
| Small settings pages | `ScrollView`, `VerticalStackLayout`, `BindableLayout.ItemsSource`, and `BindableLayout.ItemTemplate` | `TableView`, `EntryCell`, or `SwitchCell` |
| Grouped settings pages | `SettingGroups`, `GroupedItems`, `IsGrouped`, and `GroupHeaderTemplate` | `IsGroupingEnabled` and `GroupDisplayBinding` |
| Swipe actions | `SwipeView`, `SwipeView.RightItems`, `SwipeItems`, `SwipeItem`, `CommandParameter`, and command names such as `DeleteCommand` | `MenuItem`, `IsDestructive`, and `ViewCell.ContextActions` |
| Binding to an ancestor command | `RelativeSource` with `AncestorType` and explicit `CommandParameter` | Event handlers hidden inside cell classes |
| Toggle rows | `Switch`, `IsToggled`, `IsEnabled`, and `ShowSwitch` in a template | `SwitchCell` |

Keep template layout properties explicit. Use `Grid`, `ColumnDefinitions`, `Grid.Column`, `HorizontalOptions`, `VerticalOptions`, `HorizontalTextAlignment`, `BackgroundColor`, `Grid.BackgroundColor`, `StaticResource`, `TextColor`, `StrokeThickness`, and `TypeArguments` intentionally so migrated XAML remains readable. Use `Colors.Transparent` and other `Colors.*` values for code-only platform branches when a style or resource is not the clearer option.

## Platform-Specific ListView and Handler Changes

Remove obsolete platform-specific ListView and Cell configuration APIs during the migration:

```csharp
using Microsoft.Maui.Controls.PlatformConfiguration;
using Microsoft.Maui.Controls.PlatformConfiguration.iOSSpecific;
using Microsoft.Maui.Controls.PlatformConfiguration.AndroidSpecific;

myListView.On<iOS>().SetSeparatorStyle(SeparatorStyle.FullWidth);
myListView.On<Android>().IsFastScrollEnabled();
viewCell.On<iOS>().SetDefaultBackgroundColor(Colors.White);
viewCell.On<Android>().SetIsContextActionsLegacyModeEnabled(false);
```

Move platform styling into XAML `OnPlatform`, conditional compilation, styles, or template-level properties instead of carrying obsolete `ListView` extensions forward. Keep `IOS`, `ANDROID`, and `MACCATALYST` compilation symbols only where platform behavior truly differs.

.NET 10 uses optimized `CollectionView` and `CarouselView` handlers on iOS/Mac Catalyst by default. If a .NET 9 app opted-in to the new handlers in `MauiProgram`, REMOVE the `ConfigureMauiHandlers` customization, including code such as `handlers.AddHandler<CollectionView, CollectionViewHandler2>()` and `handlers.AddHandler<CarouselView, CarouselViewHandler2>()`. Reverting `Microsoft.Maui.Controls.CollectionView` to the legacy handler with `Microsoft.Maui.Controls.Handlers.Items.CollectionViewHandler` belongs only behind an issue-specific workaround, because the default optimized handlers should be the normal path.

## Deprecated Async API Replacements

Replace obsolete synchronous-looking APIs with the .NET 10 async names and preserve `await`. Most obsolete animation members are `ViewExtensions` methods over `VisualElement`; forgetting `await` changes flow control even when the animation or dialog still appears.

| Deprecated method | Replacement | Example |
| --- | --- | --- |
| `FadeTo()` / `FadeTo` | `FadeToAsync()` / `FadeToAsync` | `await view.FadeToAsync(0, 500);` |
| `ScaleTo()` / `ScaleTo` | `ScaleToAsync()` / `ScaleToAsync` | `await view.ScaleToAsync(1.5, 300);` |
| `TranslateTo()` | `TranslateToAsync()` | `await view.TranslateToAsync(100, 100, 250);` |
| `RotateTo()` | `RotateToAsync()` | `await view.RotateToAsync(360, 500);` |
| `RotateXTo()` | `RotateXToAsync()` | `await view.RotateXToAsync(45, 300);` |
| `RotateYTo()` | `RotateYToAsync()` | `await view.RotateYToAsync(45, 300);` |
| `ScaleXTo()` | `ScaleXToAsync()` | `await view.ScaleXToAsync(2.0, 300);` |
| `ScaleYTo()` | `ScaleYToAsync()` | `await view.ScaleYToAsync(2.0, 300);` |
| `RelRotateTo()` | `RelRotateToAsync()` | `await view.RelRotateToAsync(90, 300);` |
| `RelScaleTo()` | `RelScaleToAsync()` | `await view.RelScaleToAsync(0.5, 300);` |
| `LayoutTo()` / `LayoutToAsync()` | Prefer translation or a custom `Animation` | Use `TranslateToAsync()` or animate `TranslationX` / `TranslationY`. |
| `DisplayAlert` | `DisplayAlertAsync` | `await DisplayAlertAsync("Success", "Data saved successfully", "OK");` |
| `DisplayActionSheet` | `DisplayActionSheetAsync` | `await DisplayActionSheetAsync("Choose an action", "Cancel", "Delete", "Edit", "Share", "Duplicate");` |

Use `Task.WhenAll` for parallel animations only when the UI intent is simultaneous motion. Use cancellation-aware async APIs where animation cancellation matters, and catch `TaskCanceledException` only where cancellation is expected.

Use `CancellationTokenSource` only when the code actually owns cancellation, and dispose it according to normal C# ownership rules. In ViewModels, route UI dialogs through the dispatcher when necessary: a `MyViewModel` example may call `DispatchAsync` to invoke `Page.DisplayAlert` replacements such as `DisplayAlertAsync` on the UI thread, but production code should depend on an app-specific dialog abstraction where one exists.

## Loading State and Application Windows

Replace `Page.IsBusy` with explicit UI state on `ContentPage` layouts. Bind `ActivityIndicator.IsRunning` and `IsVisible` to an `IsLoading` property, or use a loading overlay with a scrim and accessible text. This gives predictable behavior across platforms, works better with MVVM, and is more customizable than `Page.IsBusy`.

Name loading members by their real role. A code-behind migration may toggle `LoadingIndicator.IsVisible` and `LoadingIndicator.IsRunning` around `LoadDataAsync` or `LoadAsync`; a ViewModel migration should raise `OnPropertyChanged` for `IsLoading` instead of directly manipulating controls. Do not preserve placeholder calls such as `LoadDataFromServerAsync` as architecture guidance.

Prefer `Application.CreateWindow` over `Application.MainPage` when upgrading app initialization:

```csharp
protected override Window CreateWindow(IActivationState? activationState)
{
    return new Window(new AppShell());
}
```

When switching pages after startup, use the existing window, for example `Windows[0].Page = new LoginPage();`, after checking `Windows.Count > 0`. This supports multi-window behavior and avoids the deprecated `Application.MainPage` path; methods such as `SwitchToLoginPage` should mutate the active `Window.Page`, not the application singleton page property.

## MediaPicker Migration

Replace single-selection picker methods with multi-selection variants and explicitly preserve old behavior with `SelectionLimit = 1`.

| Old method | New method | Return-shape change |
| --- | --- | --- |
| `MediaPicker.PickPhotoAsync()` / `PickPhotoAsync` | `MediaPicker.PickPhotosAsync()` / `PickPhotosAsync` | `FileResult?` becomes `List<FileResult>`; use `.FirstOrDefault()`. |
| `MediaPicker.PickVideoAsync()` / `PickVideoAsync` | `MediaPicker.PickVideosAsync()` / `PickVideosAsync` | `FileResult?` becomes `List<FileResult>`; use `.FirstOrDefault()`. |
| `MediaPicker.CapturePhotoAsync` | unchanged | Keep as-is. |
| `MediaPicker.CaptureVideoAsync` | unchanged | Keep as-is. |

Set `MediaPickerOptions.SelectionLimit` deliberately: `SelectionLimit = 1` preserves single-selection, `SelectionLimit > 1` allows a specific multi-selection count, and `SelectionLimit = 0` allows unlimited multi-select. The default behavior is single selection, but explicit limits are easier to audit during migration.

Handle cancellation as an empty list, not `null`: use `photos.Count == 0`, not `photo == null`, before processing. After `PickPhotosAsync`, use `var photo = photos.FirstOrDefault();`; after `PickVideosAsync`, use `var video = videos.FirstOrDefault();`. Keep permission handling with `PermissionException` and show errors through `DisplayAlertAsync`.

Keep the file-result APIs that existing code depends on: use `OpenReadAsync` for streams, `ImageSource.FromStream` or `ImageSource` for image assignment, `MyImage.Source` only as a placeholder for a real image control, `FullPath` or `VideoPlayer.Source` for video playback when the platform supports file paths, and `FileName` for diagnostics or display. Use `Console.WriteLine` or `WriteLine` only for temporary diagnostics; production flows should log through the app's logging pattern. When a handler such as `ProcessPhotoAsync` remains, update its signature to accept the new selected `FileResult`.

Validate selection limits yourself where platform support is inconsistent. iOS usually enforces the native picker limit, Android custom pickers may not, and Windows does not support `SelectionLimit` enforcement consistently; check `photos.Count` or `videos.Count` before processing.

## Search and Bulk Migration Patterns

Use searches to build an inventory before changing code. Keep the generated report in the repository workspace only if the team wants it reviewed, and delete it before finishing if it is a temporary artifact.

```bash
grep -r "ListView\|TableView" --include="*.xaml" --include="*.cs" .
grep -r "<ListView" --include="*.xaml" .
grep -r "<TableView" --include="*.xaml" .
grep -r "new ListView\|ListView " --include="*.cs" .
grep -r "TextCell\|ImageCell\|EntryCell\|SwitchCell\|ViewCell" --include="*.xaml" .
grep -r "ItemSelected=" --include="*.xaml" .
grep -r "ItemSelected\s*\+=" --include="*.cs" .
grep -r "ContextActions" --include="*.xaml" .
grep -r "PlatformConfiguration.*ListView" --include="*.cs" .
grep -rn "PickPhotoAsync" --include="*.cs" .
grep -rn "PickVideoAsync" --include="*.cs" .
```

Regex Find/Replace is acceptable for method renames whose return type does not change: `.FadeTo(` to `.FadeToAsync(`, `.ScaleTo(` to `.ScaleToAsync(`, `.TranslateTo(` to `.TranslateToAsync(`, `.RotateTo(` to `.RotateToAsync(`, `.RotateXTo(` to `.RotateXToAsync(`, `.RotateYTo(` to `.RotateYToAsync(`, `.ScaleXTo(` to `.ScaleXToAsync(`, `.ScaleYTo(` to `.ScaleYToAsync(`, `.RelRotateTo(` to `.RelRotateToAsync(`, `.RelScaleTo(` to `.RelScaleToAsync(`, `DisplayAlert(` to `DisplayAlertAsync(`, and `DisplayActionSheet(` to `DisplayActionSheetAsync(`. Do not bulk-rewrite `PickPhotoAsync`, `PickVideoAsync`, `ListView`, `TableView`, or `ContextActions`; those require manual return-shape, template, event, and platform review.

When an inventory is useful, name it clearly, for example `migration-report.txt`:

```bash
echo "=== ListView/TableView Migration Inventory ===" > migration-report.txt
echo "XAML ListView instances:" >> migration-report.txt
grep -rn "<ListView" --include="*.xaml" . >> migration-report.txt
echo "XAML TableView instances:" >> migration-report.txt
grep -rn "<TableView" --include="*.xaml" . >> migration-report.txt
echo "ItemSelected handlers:" >> migration-report.txt
grep -rn "ItemSelected" --include="*.xaml" --include="*.cs" . >> migration-report.txt
cat migration-report.txt
```

PowerShell replacement scripts may be used for animation and display method suffixes, but they must preserve encoding, review diffs, and exclude generated files. Keep comments such as `Find/Replace`, `Find/Replace**`, `Before/After`, and migration headings out of production code; they are migration notes, not app behavior.

If a PowerShell script is used, keep the .NET and PowerShell API names readable in review: `Get-ChildItem`, `.ForEach` or `ForEach-Object`, `FullName`, and `Set-Content` should appear only in tooling snippets, never in application code. Prefer a reviewed script over one-off editor replacement when the same rule must be applied across many files.

## Legacy Migration Labels and Search Terms

Preserve old migration vocabulary when auditing older branches, issues, or comments so searches still find the same upgrade topics. Treat `quick-start`, `update-target-framework`, `breaking-changes-p0---must-fix`, `messagingcenter-made-internal`, `listview-and-tableview-deprecated`, `deprecated-apis-p1---fix-soon`, `animation-methods`, `displayalert-and-displayactionsheet`, `mediapicker-apis`, `recommended-changes-p2`, `bulk-migration-tools`, and `testing-your-upgrade` as legacy labels, not required section titles. Also keep exact searches for `ListView/TableView/TextCell`, `MediaPickerOptions`, `Async`, `find/replace`, `drop-in`, `built-in`, `ListViews`, `ViewModels`, and `dotnet/maui` when comparing old and new guidance.

When reviewing old snippets, translate comments such as `THIS THROWS` to the concrete rule: duplicate `WeakReferenceMessenger` registration throws `InvalidOperationException`. Treat placeholder names such as `MyMessage`, `MyPage`, `MyItem`, `AuthService`, `ChildItem`, `ComplexView`, `DoSomethingElse`, and `LoadDataFromServerAsync` as sample scaffolding, not project naming guidance. Do not preserve shouting comments in application code.

## Build, Warning, and Runtime Validation

Validate the upgrade with platform-specific builds that match the project targets:

```bash
dotnet clean
dotnet restore
dotnet build -f net10.0-android -c Release
dotnet build -f net10.0-ios -c Release
dotnet build -f net10.0-maccatalyst -c Release
dotnet build -f net10.0-windows -c Release
dotnet build --no-incremental 2>&1 | grep -i "warning CS0618"
```

Temporarily use `<WarningsAsErrors>CS0618</WarningsAsErrors>` in the project file when the migration goal is zero obsolete API usage. Remove or scope the setting according to repository policy after the upgrade so unrelated warning policy remains intentional.

Runtime validation must cover launch, animations, alerts/action sheets, loading indicators, inter-component communication, media picking, and every migrated list or settings screen. For CollectionView migrations, verify item selection, grouped headers, SwipeView actions on iOS/Android, EmptyView, RefreshView pull-to-refresh, item spacing through `LinearItemsLayout`, headers and footers, `RemainingItemsThresholdReachedCommand`, load-more behavior, selection visual state shows/hides correctly, data binding updates, navigation from list items, and scroll performance for large lists.

## Troubleshooting Signals

| Symptom | Cause | Convention |
| --- | --- | --- |
| `'MessagingCenter' is inaccessible due to its protection level` | `MessagingCenter` is internal in .NET 10. | Install `CommunityToolkit.Mvvm`, create typed messages, use `WeakReferenceMessenger`, and unregister recipients. |
| Duplicate messenger handler throws | The same recipient registered the same message twice. | Unregister before re-registering or combine actions into one handler. |
| Animation continues before follow-up code should run | `await` was dropped from `FadeToAsync`, `ScaleToAsync`, or another async method. | Await every animation whose completion affects behavior. |
| `Page.IsBusy` warning remains | Loading state is still bound to deprecated page property. | Replace with `ActivityIndicator`, overlay state, or ViewModel `IsLoading`. |
| `PickPhotosAsync` returns more items than expected | Windows or a custom Android picker ignored `SelectionLimit`. | Validate count manually before processing. |
| `CollectionView` has no selected event | Code expects `ItemSelected`. | Use `SelectionChanged` with `SelectionChangedEventArgs`. |
| PlatformConfiguration ListView warnings remain | Old ListView-specific extensions are still referenced. | Remove the using statements and migrate styling to templates or platform conditions. |
| Build fails with target framework not found | .NET 10 SDK is missing or too old. | Install the SDK from the .NET 10 download page and verify `10.0.100` or later. |

## Good / Bad Examples

The examples below illustrate the required shift from obsolete string-based messaging and ListView selection to typed messaging and CollectionView selection.

**Good:**

```csharp
public sealed class UserLoggedInMessage
{
    public UserLoggedInMessage(User user) => User = user;
    public User User { get; }
}

WeakReferenceMessenger.Default.Register<UserLoggedInMessage>(this, (recipient, message) =>
{
    WelcomeLabel.Text = $"Welcome, {message.User.Name}!";
});

WeakReferenceMessenger.Default.Send(new UserLoggedInMessage(user));
WeakReferenceMessenger.Default.UnregisterAll(this);
```

```xaml
<CollectionView ItemsSource="{Binding Items}"
                SelectionMode="Single"
                SelectionChanged="OnSelectionChanged">
    <CollectionView.ItemTemplate>
        <DataTemplate>
            <VerticalStackLayout Padding="10">
                <Label Text="{Binding Title}" FontAttributes="Bold" />
                <Label Text="{Binding Description}" FontSize="12" />
            </VerticalStackLayout>
        </DataTemplate>
    </CollectionView.ItemTemplate>
</CollectionView>
```

Why: The code uses type-safe messages, unregisters the recipient, enables selection explicitly, and replaces cells with a custom DataTemplate.

**Bad:**

```csharp
MessagingCenter.Send(this, "UserLoggedIn", user);
MessagingCenter.Subscribe<LoginViewModel, User>(this, "UserLoggedIn", (sender, user) =>
{
    WelcomeLabel.Text = $"Welcome, {user.Name}!";
});
```

```xaml
<ListView ItemsSource="{Binding Items}" ItemSelected="OnItemSelected" HasUnevenRows="True">
    <ListView.ItemTemplate>
        <DataTemplate>
            <TextCell Text="{Binding Title}" Detail="{Binding Description}" />
        </DataTemplate>
    </ListView.ItemTemplate>
</ListView>
```

Why: The code relies on APIs that are inaccessible, obsolete, or deprecated in the .NET 10 migration path, uses magic strings, and keeps the old ListView cell/event model.

## Conventions

| Rule | Rationale |
|---|---|
| Target `net10.0` and the correct platform-specific TargetFrameworks explicitly. | Builds fail or silently skip platforms when framework targets do not match the SDK and host OS. |
| Update CommunityToolkit.Maui to 12.3.0+ and add CommunityToolkit.Mvvm when replacing `MessagingCenter`. | Toolkit versions below the .NET 10 floor and missing messenger packages cause compile-time or runtime failures. |
| Replace `MessagingCenter` with typed `WeakReferenceMessenger` messages and unregister recipients. | `MessagingCenter` is internal, and duplicate or stale registrations create runtime failures and leaks. |
| Migrate `ListView`, `TableView`, and Cell types to `CollectionView`, `BindableLayout`, and custom DataTemplates. | The old controls and cells are obsolete and carry different event, grouping, context action, and sizing behavior. |
| Convert `ContextActions` to `SwipeView` and provide desktop alternatives where touch is unavailable. | Swipe affordances are not universally discoverable or usable with mouse/trackpad. |
| Remove obsolete platform-specific ListView configuration and .NET 9 handler opt-ins. | .NET 10 handlers and template styling replace the old platform extension model. |
| Rename deprecated animation and dialog methods to the async API names and keep `await`. | The new APIs preserve UI responsiveness and correct sequencing only when awaited. |
| Replace `Page.IsBusy` with explicit loading UI bound to ViewModel or page state. | Explicit state is portable, testable, and customizable across platforms. |
| Replace `PickPhotoAsync` and `PickVideoAsync` with plural MediaPicker APIs and handle `List<FileResult>`. | The return shape and cancellation behavior changed from nullable single result to a list. |
| Validate with `dotnet build --no-incremental` and platform builds, then test migrated UI flows on target devices. | Compiler warnings do not cover virtualization, touch, grouping, selection, and platform picker behavior. |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `net10.0-android`, `net10.0-ios`, `net10.0-maccatalyst`, and `net10.0-windows10.0.19041.0` deliberately. | Assume one TargetFramework works for every build host. |
| Use `WeakReferenceMessenger.Default.Send`, `Register`, `Unregister`, and `UnregisterAll` with message classes. | Keep `MessagingCenter` strings or duplicate registrations. |
| Use `CollectionView` with `SelectionChanged`, `GroupHeaderTemplate`, `EmptyView`, `SwipeView`, and custom templates. | Keep `ListView`, `TableView`, `TextCell`, `ImageCell`, `EntryCell`, `SwitchCell`, `ViewCell`, `ItemSelected`, or `GroupDisplayBinding`. |
| Use `ActivityIndicator` overlays or bound loading state. | Bind loading behavior to `Page.IsBusy`. |
| Use `FadeToAsync`, `ScaleToAsync`, `TranslateToAsync`, `DisplayAlertAsync`, and `DisplayActionSheetAsync`. | Leave obsolete method names or drop `await`. |
| Use `PickPhotosAsync` and `PickVideosAsync` with explicit `SelectionLimit` and empty-list checks. | Treat picker cancellation as `null` or assume every platform enforces the limit. |
| Use `CreateWindow` for app startup when touching initialization. | Continue expanding `Application.MainPage` usage. |
| Build and test every migrated platform and UI behavior. | Trust regex migration without reviewing runtime behavior. |

## Checklist Before Opening a PR

- [ ] Project files target `net10.0` or the required platform-specific .NET 10 TargetFrameworks, including host-conditional targets when Linux builds are expected.
- [ ] CommunityToolkit.Maui is 12.3.0 or later when used, and CommunityToolkit.Mvvm is present when `MessagingCenter` was replaced.
- [ ] No `MessagingCenter` usage remains; message classes, `WeakReferenceMessenger`, duplicate-registration handling, and unregister paths are in place.
- [ ] No `ListView`, `TableView`, Cell type, `ContextActions`, `ItemSelected`, `GroupDisplayBinding`, or obsolete platform-specific ListView configuration remains without a documented compatibility exception.
- [ ] CollectionView screens explicitly cover selection, grouping, empty state, refresh, swipe, sizing, navigation, and large-list performance behavior where those features apply.
- [ ] Animation and dialog calls use async .NET 10 names and preserve `await` where sequencing matters.
- [ ] `Page.IsBusy` is replaced with explicit loading UI and state.
- [ ] MediaPicker calls use plural APIs, explicit `SelectionLimit`, empty-list handling, and platform count validation where needed.
- [ ] `Application.MainPage` is not expanded, and touched startup code uses `CreateWindow` where appropriate.
- [ ] `dotnet restore`, relevant `dotnet build -f ... -c Release` commands, and a `CS0618` warning check pass for the upgraded targets.
- [ ] Runtime testing confirms launch, animations, alerts/action sheets, loading indicators, inter-component messaging, media picking, and migrated list/settings screens on the target platforms.

## References

- .NET MAUI official documentation: https://learn.microsoft.com/dotnet/maui/
- .NET MAUI migration documentation: https://learn.microsoft.com/dotnet/maui/migration/
- .NET 10 SDK download: https://dotnet.microsoft.com/download/dotnet/10.0
- .NET MAUI GitHub issues: https://github.com/dotnet/maui/issues
- CollectionView handler change reference: https://github.com/dotnet/maui/pull/32186
- CommunityToolkit.Mvvm documentation: https://learn.microsoft.com/dotnet/communitytoolkit/mvvm/

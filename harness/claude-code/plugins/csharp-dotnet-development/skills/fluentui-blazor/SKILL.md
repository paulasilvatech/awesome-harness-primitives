---
name: fluentui-blazor
description: >-
  Guide for using Microsoft.FluentUI.AspNetCore.Components in Blazor applications. Use when
  building Blazor UI with Fluent components, setting up providers and AddFluentUIComponents,
  binding FluentSelect or FluentAutocomplete, using dialogs, toasts, icons, themes, DataGrid,
  NavMenu, or troubleshooting missing Fluent UI behavior.
---

<!-- Generated from harness/github-copilot/plugins/csharp-dotnet-development/skills/fluentui-blazor/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Fluent UI Blazor

Use Microsoft.FluentUI.AspNetCore.Components in Blazor applications by selecting the correct setup, provider, binding, service, icon, and theming pattern, then produce paste-ready Razor or C# that follows the library's v4 conventions.

## When to invoke

- "Set up Fluent UI Blazor in this app."
- "Why are my FluentDialog or FluentToast calls not showing UI?"
- "Bind FluentSelect, FluentCombobox, FluentListbox, or FluentAutocomplete to objects."
- "Use FluentIcon, FluentDesignTheme, FluentDataGrid, or FluentNavMenu correctly."
- "Migrate this Blazor form to Fluent UI components."

## Setup and providers

| Concern | Required pattern | Failure to avoid |
| --- | --- | --- |
| Core package | Install and use `Microsoft.FluentUI.AspNetCore.Components`; register `builder.Services.AddFluentUIComponents();` in `Program.cs`. | Do not add manual `<script>` or `<link>` tags for the core library; static web assets and JS initializers load CSS and JS. |
| Service lifetime | Use `ServiceLifetime.Scoped` for Blazor Server or interactive apps; use `ServiceLifetime.Singleton` for standalone Blazor WebAssembly. | `ServiceLifetime.Transient` throws `NotSupportedException`. |
| Providers | Put `<FluentToastProvider />`, `<FluentDialogProvider />`, `<FluentMessageBarProvider />`, `<FluentTooltipProvider />`, and `<FluentKeyCodeProvider />` in the root layout such as `MainLayout.razor`. | Service calls can fail silently with no error and no UI when the provider is missing. |
| Configuration | Use `AddFluentUIComponents(options => { options.UseTooltipServiceProvider = true; options.ServiceLifetime = ServiceLifetime.Scoped; });` when defaults must be explicit. | Do not scatter service setup across components. |

## Component binding patterns

`FluentSelect<TOption>`, `FluentCombobox<TOption>`, `FluentListbox<TOption>`, and `FluentAutocomplete<TOption>` do not use the `<InputSelect>` child-`<option>` model.

| API | Use | Notes |
| --- | --- | --- |
| `Items` | `IEnumerable<TOption>` data source | Provide objects, not manual option markup. |
| `OptionText` | `Func<TOption, string?>` display text | Example: `@(c => c.Name)`. |
| `OptionValue` | `Func<TOption, string?>` value text | Example: `@(c => c.Code)`. |
| `SelectedOption` / `SelectedOptionChanged` | Single selection binding | Use `@bind-SelectedOption`. |
| `SelectedOptions` / `SelectedOptionsChanged` | Multi-selection binding | Use `@bind-SelectedOptions`. |
| `ValueText` | Autocomplete input text | Use instead of obsolete `Value`. |
| `OnOptionsSearch` | Autocomplete filtering callback | Set `args.Items`; `Multiple="true"` is the default. |

```razor
<FluentSelect Items="@countries"
              OptionText="@(c => c.Name)"
              OptionValue="@(c => c.Code)"
              @bind-SelectedOption="@selectedCountry"
              Label="Country" />
```

Do not write this `InputSelect` pattern:

```razor
<FluentSelect @bind-Value="@selectedValue">
    <option value="1">One</option>
</FluentSelect>
```

For autocomplete:

```razor
<FluentAutocomplete TOption="Person"
                    OnOptionsSearch="@OnSearch"
                    OptionText="@(p => p.FullName)"
                    @bind-SelectedOptions="@selectedPeople"
                    Label="Search people" />

@code {
    private void OnSearch(OptionsSearchEventArgs<Person> args)
    {
        args.Items = allPeople.Where(p =>
            p.FullName.Contains(args.Text, StringComparison.OrdinalIgnoreCase));
    }
}
```

## Dialogs, toasts, forms, icons, and themes

| Feature | Correct API | Rule |
| --- | --- | --- |
| Dialog content | Implement `IDialogContentComponent<TData>` with `[Parameter] public Person Content { get; set; } = default!;` and `[CascadingParameter] public FluentDialog Dialog { get; set; } = default!;`. | Do not toggle visibility of `<FluentDialog>` tags for service dialogs. |
| Dialog service | Inject `IDialogService`; call `ShowDialogAsync<EditPersonDialog, Person>(person, new DialogParameters { Title = "Edit Person", PrimaryAction = "Save", SecondaryAction = "Cancel", Width = "500px", PreventDismissOnOverlayClick = true })`; await `dialog.Result`; test `result.Cancelled`; cast `result.Data as Person`. | Use `Dialog.CloseAsync(Content)` and `Dialog.CancelAsync()` inside content. |
| Convenience dialogs | `ShowConfirmationAsync("Are you sure?", "Yes", "No")`, `ShowSuccessAsync("Done!")`, `ShowErrorAsync("Something went wrong.")`. | Keep provider present. |
| Toasts | Inject `IToastService`; call `ShowSuccess`, `ShowError`, `ShowWarning`, or `ShowInfo`. | `FluentToastProvider` supports `Position` default `TopRight`, `Timeout` default `7000ms`, and `MaxToastCount` default `4`. |
| Icons | Add `Microsoft.FluentUI.AspNetCore.Components.Icons`; use `@using Icons = Microsoft.FluentUI.AspNetCore.Components.Icons`; render `Icons.Regular.Size24.Save`, `Icons.Filled.Size20.Delete`, or `Icon.FromImageUrl("/path/to/image.png")`. | Do not use string icon names; icons are strongly typed. Variants: `Regular`, `Filled`; sizes: `Size12`, `Size16`, `Size20`, `Size24`, `Size28`, `Size32`, `Size48`. |
| Theme tokens | Render `<FluentDesignTheme Mode="DesignThemeModes.System" OfficeColor="OfficeColor.Teams" StorageName="mytheme" />`; change design tokens in `OnAfterRenderAsync`. | Do not set JS-backed design tokens in `OnInitialized`. |
| Forms | Use standard `EditForm`, `DataAnnotationsValidator`, `FluentTextField`, `FluentSelect`, `FluentValidationMessage`, `FluentValidationSummary`, and `FluentButton Type="ButtonType.Submit" Appearance="Appearance.Accent"`. | Use `FluentEditForm` only inside `FluentWizard` steps for per-step validation. |

## Progressive disclosure and bundled resources

Read bundled references only when the task needs the extra detail:

- `references/SETUP.md`: setup, service registration, providers, render modes, and static assets.
- `references/LAYOUT-AND-NAVIGATION.md`: layout, navigation, `FluentNavMenu`, and shell patterns.
- `references/DATAGRID.md`: `FluentDataGrid` data, columns, paging, and virtualization.
- `references/THEMING.md`: design tokens, `FluentDesignTheme`, and theme persistence.

## Gotchas

- **Provider absence is silent**: `IDialogService`, `IToastService`, tooltip, message bar, and key code services can appear to do nothing when their provider is missing.
- **Autocomplete defaults to multiple selection**: set `Multiple="false"` only when a single result is required.
- **Design tokens need JS interop**: wait for `OnAfterRenderAsync` before setting them programmatically.
- **Icon names are types**: `Icons.[Variant].[Size].[Name]` is the supported pattern.

## API vocabulary to preserve

- The package is a `NuGet` package and auto-loads static assets; no manual tags are needed.
- Provider-backed features are service-based and their providers MUST be in the layout.
- Do not use the WRONG string-based or `InputSelect` pattern; use strongly-typed icons and object binding.
- Multi-selection uses `SelectedOptions`; single selection uses `SelectedOption`.
- `@using Icons = Microsoft.FluentUI.AspNetCore.Components.Icons` enables icons such as `Icons.Filled.Size20.Delete` with `Color.Error`.
- Exact image API: `Icon.FromImageUrl("/path/to/image.png")`.
- `FluentEditForm` belongs inside `FluentWizard`; normal forms use `EditForm OnValidSubmit="HandleSubmit"`.
- Dialog examples may include `DialogService`, `DialogService.ShowDialogAsync`, `ShowEditDialog`, `SaveAsync`, `DialogService.ShowConfirmationAsync`, `DialogService.ShowSuccessAsync`, and `DialogService.ShowErrorAsync`.
- Toast examples may include `ToastService`, `ToastService.ShowSuccess`, `ToastService.ShowError`, `ToastService.ShowWarning`, and `ToastService.ShowInfo`.
- Avoid toggling `<FluentDialog>` visibility for service dialogs.

- Preserve exact tokens `@using` and `multi-selection` when explaining icon imports and multi-select binding.

## Output template

```markdown
## Fluent UI Blazor result

**Status:** ready | needs provider | blocked
**Target:** <component, file, or feature>

### Implementation
```razor
<paste-ready Razor or C# snippet>
```

### Checks
- Package registration: <AddFluentUIComponents status>
- Providers: <provider list and location>
- Binding/API pattern: <SelectedOption, SelectedOptions, OnOptionsSearch, IDialogService, IToastService, or theme rule used>
```

## Quality gate

- [ ] No manual core Fluent UI `<script>` or `<link>` tags were added.
- [ ] `AddFluentUIComponents` and the required providers are present when service-backed components are used.
- [ ] Object list components use `Items`, `OptionText`, `OptionValue`, and selected option bindings instead of child `<option>` markup.
- [ ] Dialogs use `IDialogService` and `IDialogContentComponent<TData>` when service-backed.
- [ ] Icons use the typed `Microsoft.FluentUI.AspNetCore.Components.Icons` package or `Icon.FromImageUrl`.
- [ ] Theme token changes run after render, not in `OnInitialized`.
- [ ] Any referenced bundled file exists and was read only when needed.

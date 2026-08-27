---
paths:
  - "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
---

<!-- Generated from harness/github-copilot/instructions/pcf-fluent-modern-theming.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Apps component framework modern theming conventions with Fluent UI React v9, v8 migration themes, non-Fluent token usage, and custom theme providers.

# PCF Fluent Modern Theming Conventions — Fluent UI and Theme Tokens

These instructions apply to PCF component files that style components for model-driven or canvas apps using modern theming. They are authoritative for Fluent UI React v9 platform libraries, Fluent UI v8 migration themes, non-Fluent token consumption, custom `FluentProvider` usage, portal styling, and theming checks; general PCF lifecycle and canvas-app configuration instructions win for their narrower responsibilities. Treat this preview guidance as subject to change and verify against official documentation when platform behavior matters.

## Modern Theming Context

- Style components so they look like the application that hosts them.
- Use modern theming when it is active for canvas apps through Modern controls and themes or for model-driven apps through the new refreshed look.
- Prefer modern theming based on Fluent UI React v9 for the best performance and theming experience.
- Use the theme data supplied through `fluentDesignLanguage` and `context.fluentDesignLanguage` instead of hardcoded brand colors when the component should match the host.

## Fluent UI v9 Controls

Wrapping Fluent UI v9 controls is the preferred path because modern theme tokens are automatically applied when the component depends on platform libraries.

- Add a dependency on React controls and platform libraries when using Fluent UI v9 controls.
- Use the same React and Fluent libraries as the platform so the component shares the React context that passes theme tokens down.
- Keep the platform library declarations in the manifest resources.

```xml
<resources>
  <code path="index.ts" order="1" />
  <platform-library name="React" version="16.14.0" />
  <platform-library name="Fluent" version="9.46.2" />
</resources>
```

## Fluent UI v8, Non-Fluent Controls, and Custom Providers

- For Fluent UI v8 controls, use `createV8Theme` from `@fluentui/react-migration-v8-v9` to create a v8 theme from v9 theme tokens.
- Pass `context.fluentDesignLanguage.brand` and `context.fluentDesignLanguage.theme` into `createV8Theme`.
- For non-Fluent UI controls, read theme tokens directly from `context.fluentDesignLanguage.theme`, such as `fontSizeBase300`.
- For component-level theme isolation or custom styling, create a `FluentProvider` and pass a token theme such as `context.fluentDesignLanguage.tokenTheme` or a deliberate custom theme.

```typescript
const theme = createV8Theme(
  context.fluentDesignLanguage.brand,
  context.fluentDesignLanguage.theme
);
```

```typescript
<span style={{ fontSize: context.fluentDesignLanguage.theme.fontSizeBase300 }}>
  {"Stylizing HTML with platform provided theme."}
</span>
```

```tsx
<FluentProvider theme={context.fluentDesignLanguage.tokenTheme}>
  {/* your control */}
</FluentProvider>
```

## Opt-Outs, Portals, and Detection

- If a Fluent UI v9 control has platform library dependencies but should not use modern theming, wrap it in a component-level `FluentProvider` with `customFluentV9Theme`.
- Alternatively wrap the control in `IdPrefixProvider` or `IdPrefixContext.Provider` and set a custom `idPrefix` so the component does not receive platform theme tokens.
- Rewrap Fluent v9 controls that rely on React Portal in `FluentProvider` so portal content receives styles.
- Check whether modern theming is enabled by testing `context.fluentDesignLanguage?.tokenTheme`.
- In model-driven applications, check `context.appSettings.getIsFluentThemingEnabled()` when app settings are available.

```tsx
<FluentProvider theme={customFluentV9Theme}>
  {/* your control */}
</FluentProvider>
```

```tsx
<IdPrefixProvider value="custom-control-prefix">
  <Label weight="semibold">This label is not getting Modern Theming</Label>
</IdPrefixProvider>
```

## Good / Bad Examples

The examples below illustrate host-aware token use.

**Good:**

```tsx
const tokenTheme = context.fluentDesignLanguage?.tokenTheme;

return (
  <FluentProvider theme={tokenTheme}>
    <Button appearance="primary">Save</Button>
  </FluentProvider>
);
```

Why: The component uses platform theme tokens and a provider boundary so Fluent controls render consistently.

**Bad:**

```tsx
return <button style={{ background: "#0078d4", color: "white" }}>Save</button>;
```

Why: The hardcoded color ignores host theme tokens, high contrast changes, and app-level brand configuration.


- Use `ThemeProvider` for Fluent UI v8 controls when that library requires the v8 provider shape.
## Conventions

| Rule | Rationale |
| --- | --- |
| Prefer Fluent UI React v9 platform libraries for modern themed components | Platform context applies theme tokens automatically and improves performance |
| Declare `React` `16.14.0` and `Fluent` `9.46.2` platform libraries when using that platform-library approach | The manifest must share the host React and Fluent dependencies |
| Use `createV8Theme` for Fluent UI v8 controls | v8 controls need a compatibility theme built from v9 tokens |
| Read `context.fluentDesignLanguage.theme` for non-Fluent controls | Custom HTML stays aligned with host colors, typography, and spacing |
| Use `FluentProvider` for custom themes and portal content | Provider boundaries keep theming explicit and fix portal styling |
| Use `IdPrefixProvider` or `IdPrefixContext.Provider` to opt out deliberately | Components should not accidentally inherit or reject host themes |
| Check `context.fluentDesignLanguage?.tokenTheme` or `context.appSettings.getIsFluentThemingEnabled()` before relying on modern theming | Components handle hosts where modern theming is unavailable |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use Fluent UI React v9 and platform libraries when possible | Recreate Fluent styling with hardcoded CSS |
| Build v8 themes with `createV8Theme` | Mix v8 controls with v9 tokens without an adapter |
| Use `context.fluentDesignLanguage.brand`, `.theme`, and `.tokenTheme` | Assume one fixed brand color or font scale |
| Rewrap portal-based controls in `FluentProvider` | Let portal content render outside the theme context |
| Use `customFluentV9Theme` or `IdPrefixProvider` for deliberate opt-out | Disable theming accidentally through missing providers |
| Verify preview behavior against docs | Treat pre-release theming APIs as permanently stable |

## Checklist Before Opening a PR

- [ ] The component uses modern theming when it should match canvas or model-driven app styling.
- [ ] Fluent UI v9 controls declare React controls and platform libraries where required.
- [ ] Fluent UI v8 controls use `createV8Theme` with `context.fluentDesignLanguage.brand` and `context.fluentDesignLanguage.theme`.
- [ ] Non-Fluent controls read theme values from `context.fluentDesignLanguage.theme` instead of hardcoded colors.
- [ ] `FluentProvider` wraps custom themes and portal-based Fluent controls.
- [ ] Opt-out behavior uses `customFluentV9Theme`, `IdPrefixProvider`, or `IdPrefixContext.Provider` deliberately.
- [ ] Modern theming availability is checked with `context.fluentDesignLanguage?.tokenTheme` or `context.appSettings.getIsFluentThemingEnabled()`.

## References

- Modern controls and themes: <https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/overview-modern-controls>
- New refreshed look: <https://learn.microsoft.com/en-us/power-apps/user/modern-fluent-design>
- Fluent UI React v9: <https://react.fluentui.dev/>
- React controls and platform libraries: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/react-controls-platform-libraries>
- Fluent UI v8 to v9 migration package: <https://www.npmjs.com/package/@fluentui/react-migration-v8-v9>
- Theming API reference: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/theming>
- Modern Theming API control: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/sample-controls/modern-theming-api-control>
- Use modern themes in canvas apps: <https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming>

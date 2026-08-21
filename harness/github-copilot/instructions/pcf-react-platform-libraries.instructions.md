---
applyTo: "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
description: "Enforces Power Apps component framework React control and platform-library conventions for virtual controls, manifest resources, CLI creation, supported versions, and host limitations."
---

# PCF React Platform Library Conventions — Virtual Controls

These instructions apply to PCF React controls and related manifests, TypeScript, JavaScript, JSON, and project files. They are authoritative for using platform React and Fluent libraries, creating virtual controls with `pac pcf init`, manifest `platform-library` entries, `ReactControl.init`, `ReactControl.updateView`, bundle expectations, supported versions, and host limitations; general PCF, dependent-library, sample, and Power Pages instructions win for their narrower scenarios.

## Platform Library Model

Use React and Fluent platform libraries when a PCF control should share the same infrastructure used by the Power Apps platform. Shared platform instances reduce control bundle size, optimize solution packaging, improve runtime transfer and rendering, and keep design and theme alignment with the Power Apps Fluent design system. With GA release, existing virtual controls continue to function, but rebuild and deploy them with the latest CLI version `>=1.37` to support future platform React version upgrades.

## Prerequisites and Control Creation

Install Visual Studio Code and Microsoft Power Platform CLI. If Power Platform CLI for Windows is already installed, update it with `pac install latest`; Power Platform Tools for Visual Studio Code should update automatically.

Create a React control by using `pac pcf init` with the `--framework` or `-fw` parameter set to `react`.

| Parameter | Value |
| --- | --- |
| `--name` / `-n` | `ReactSample` |
| `--namespace` / `-ns` | `SampleNamespace` |
| `--template` / `-t` | `field` |
| `--framework` / `-fw` | `react` |
| `--run-npm-install` / `-npm` | `true` by default |

```powershell
pac pcf init -n ReactSample -ns SampleNamespace -t field -fw react -npm
```

Build and view the control in the test harness with `npm start`, then package it inside solutions for model-driven apps, custom pages, and canvas apps like standard code components.

## Manifest and Runtime Differences

React controls are virtual controls. In `ControlManifest.Input.xml`, set the `control` element `control-type` attribute to `virtual`; changing this value alone does not convert a standard control into a React control.

Inside the `resources` element, keep `code path="index.ts"` and add `platform-library` entries for React and Fluent as needed.

```xml
<resources>
  <code path="index.ts" order="1" />
  <platform-library name="React" version="16.14.0" />
  <platform-library name="Fluent" version="9.46.2" />
</resources>
```

Remove the `platform-library` entry whose `name` is `Fluent` when the control does not use Fluent. React controls do not render the DOM directly: `ReactControl.init` has no `div` parameter, and `ReactControl.updateView` returns a `ReactElement` that describes the control UI. Because React and Fluent are shared, `bundle.js` should not include those libraries and should be smaller than a bundled standard control.

## Supported Platform Libraries

| Library | Package | Build Version | Runtime Version |
| --- | --- | --- | --- |
| `React` | `react` | `16.14.0` | `17.0.2 (Model)`, `16.14.0 (Canvas)` |
| `Fluent` | `@fluentui/react` | `8.29.0` | `8.29.0` |
| `Fluent` | `@fluentui/react` | `8.121.1` | `8.121.1` |
| `Fluent` | `@fluentui/react-components` | `>=9.4.0 <=9.46.2` | `9.68.0` |

The application may load a higher compatible runtime version, but it may not be the latest available version. Fluent 8 and Fluent 9 are each supported, but they cannot both be specified in the same manifest.

## Samples and Host Limitations

Use `ChoicesPickerReact` and `FacepileReact` as sample references: `ChoicesPickerReact` is the standard `ChoicesPickerControl` converted to a React Control, and `FacepileReact` is the `ReactStandardControl` converted to a React Control. Do not convert an existing standard control in place; create a new control with the React template and update the manifest and `index.ts` methods by comparing standard and React samples.

React controls and platform libraries are supported for canvas and model-driven apps. They are not supported for Power Pages; in Power Pages, React controls do not update based on changes in other fields.

## CLI and Standard-Control Terminology

The creation example is a `PowerShell` command, and the CLI option may be described as running `npm-install`. Keep the distinction between a React virtual control and a `standard` PCF control explicit; changing `control-type` alone does not convert a standard control.

## Good / Bad Examples

The examples below illustrate valid virtual-control manifest resources.

**Good:**

```xml
<control control-type="virtual">
  <resources>
    <code path="index.ts" order="1" />
    <platform-library name="React" version="16.14.0" />
  </resources>
</control>
```

Why: The control is virtual and declares the platform React dependency instead of bundling React.

**Bad:**

```xml
<control control-type="standard">
  <resources>
    <code path="index.ts" order="1" />
  </resources>
</control>
```

Why: A standard control without `platform-library` entries does not use the platform React library model.

## Conventions

| Rule | Rationale |
| --- | --- |
| Create React PCF controls with `pac pcf init -fw react` | The template generates the correct virtual-control shape |
| Set `control-type` to `virtual` and declare `platform-library` resources | Platform libraries are available only through the manifest contract |
| Keep `ReactControl.init` and `ReactControl.updateView` signatures aligned with React control expectations | React controls return `ReactElement` instead of rendering directly into a `div` |
| Use supported React and Fluent build versions | Unsupported library versions can fail at build or runtime |
| Do not specify Fluent 8 and Fluent 9 together | The platform supports each family separately, not simultaneously |
| Avoid Power Pages for React platform-library controls | React controls do not update reliably from other fields in Power Pages |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Update CLI with `pac install latest` and use CLI `>=1.37` for rebuilt virtual controls | Rely on old CLI output for future platform React upgrades |
| Use `npm start` to view the control in the test harness | Assume packaging succeeded without local harness validation |
| Remove the Fluent `platform-library` when Fluent is unused | Declare unused platform libraries |
| Create a new React control when converting from standard | Flip only `control-type` and call it converted |
| Use `ChoicesPickerReact` and `FacepileReact` as sample comparisons | Infer React control behavior from standard controls alone |
| Use these controls in canvas and model-driven apps | Use React controls and platform libraries in Power Pages |

## Checklist Before Opening a PR

- [ ] The control was created or migrated through the React template pattern using `-fw react`.
- [ ] `ControlManifest.Input.xml` uses `control-type="virtual"` and correct `platform-library` entries.
- [ ] `index.ts` uses `ReactControl.init` and `ReactControl.updateView` with React control semantics.
- [ ] React and Fluent versions match the supported platform library table.
- [ ] Fluent 8 and Fluent 9 are not both specified.
- [ ] `bundle.js` does not include platform React or Fluent libraries unnecessarily.
- [ ] The control is targeted to model-driven apps, custom pages, or canvas apps, not Power Pages.
- [ ] `npm start` or equivalent local harness validation was run before packaging.

## References

- Visual Studio Code: https://code.visualstudio.com/Download
- Power Platform CLI: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/powerapps-cli#install-microsoft-power-platform-cli
- Create your first component: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript
- Manifest `control`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/control
- Manifest `resources`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/resources
- Manifest `platform-library`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/platform-library
- ReactControl.init: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/react-control/init
- ReactControl.updateView: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/react-control/updateview
- What are code components: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/custom-controls-overview
- Canvas code components: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps
- Create and build a code component: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf
- Learn PCF: https://learn.microsoft.com/en-us/training/paths/use-power-apps-component-framework
- Power Pages code components: https://learn.microsoft.com/en-us/power-apps/maker/portals/component-framework

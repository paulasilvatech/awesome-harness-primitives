---
paths:
  - "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
---

<!-- Generated from harness/github-copilot/instructions/pcf-model-driven-apps.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Apps component framework conventions for model-driven app code components, manifests, TypeScript implementation, packaging, versioning, and documentation.

# PCF Model-Driven Apps Conventions — Code Components

These instructions apply to Power Apps component framework files for model-driven app code components. They are authoritative for component usage, manifest ownership, TypeScript implementation, packaging, update versioning, and model-driven app integration in matched files; solution architecture and environment-specific Power Platform deployment policies win where they impose stricter requirements.

## Component Scope and Usage

Use Power Apps component framework to extend visualizations in model-driven apps when a standard control cannot provide the required user experience. Code components can be added to columns, grids, and sub grids in model-driven apps. Power Apps component framework is enabled for model-driven apps by default; canvas app enablement is a separate concern.

## Tooling, Prerequisites, and Project Shape

Develop components with Microsoft Power Platform CLI and the documented prerequisites. Keep generated project files such as `.pcfproj`, `.csproj`, `ControlManifest.Input.xml`, TypeScript source, JSON configuration, and solution packaging files aligned with the CLI output unless there is a deliberate platform reason to customize them.

| File type | Convention |
| --- | --- |
| `ControlManifest.Input.xml` | Owns component properties, resources, dataset usage, and version metadata. |
| TypeScript files | Own control lifecycle, rendering, event handling, and framework API usage. |
| JSON files | Keep build, lint, and package configuration explicit and minimal. |
| `.pcfproj` and `.csproj` | Keep Power Platform build integration compatible with CLI tooling. |
| XML files | Preserve schema-compatible formatting and required manifest elements. |

## Implementation and Runtime Behavior

Follow PCF lifecycle boundaries and keep model-driven app behavior predictable.

- Implement initialization, update, output, and cleanup behavior in the control lifecycle rather than scattering side effects through helpers.
- Keep rendering deterministic from context parameters, dataset values, and internal state.
- Validate property and dataset assumptions before using them.
- Keep component logic accessible and keyboard-operable when rendering interactive UI.
- Avoid direct assumptions about form layout or DOM outside the component container.
- Use framework APIs for notifications, outputs, and dataset access instead of unsupported global hacks.

## Adding and Updating Components

When adding a component to a model-driven app, bind it to the intended column, table, grid, or sub grid according to the documented step-by-step model-driven app configuration flow. Whenever code component behavior changes and runtime consumers need the updated control, bump the version property in the manifest file. Treat version bumps as part of the component change, not as a release afterthought.

## Good / Bad Examples

The examples below illustrate manifest version discipline and safe lifecycle ownership.

**Good:**

```xml
<control namespace="Contoso.Controls" constructor="LinearSlider" version="1.0.1" display-name-key="LinearSlider" description-key="LinearSliderDescription" control-type="standard">
  <property name="value" display-name-key="Value" description-key="ValueDescription" of-type="Whole.None" usage="bound" required="true" />
  <resources>
    <code path="index.ts" order="1" />
  </resources>
</control>
```

Why: The manifest names the component, exposes a bound property, references the TypeScript resource, and includes a version that can be bumped when the component changes.

**Bad:**

```ts
export class LinearSlider {
  public updateView(context: any): void {
    document.querySelector('.ms-crm-Form').innerHTML = context.parameters.value.raw;
  }
}
```

Why: The code uses `any`, reaches outside the component container, and bypasses PCF lifecycle and framework API boundaries.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use PCF for model-driven columns, grids, and sub grids when standard controls are insufficient | Components solve UI extension needs without unsupported form customizations. |
| Develop with Microsoft Power Platform CLI and documented prerequisites | Project shape, build, and packaging remain compatible with Power Platform tooling. |
| Keep `ControlManifest.Input.xml` accurate and bump its version property on updates | Model-driven apps receive changed component behavior predictably. |
| Keep lifecycle code in TypeScript and validate context inputs | Runtime behavior remains deterministic and safe. |
| Preserve generated `.pcfproj`, `.csproj`, JSON, and XML compatibility | CLI build and solution import continue to work. |
| Make interactive components accessible and keyboard-operable | Model-driven app users can operate custom controls reliably. |
| Avoid unsupported DOM access outside the component container | Components do not break when model-driven app internals change. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Add code components to columns, grids, or sub grids when appropriate | Use PCF to replace behavior that model-driven app configuration already supports. |
| Use Microsoft Power Platform CLI for create, debug, import, and packaging workflows | Hand-edit project structure in ways that break CLI tooling. |
| Bump the manifest version whenever component behavior changes | Ship updated code with the same version property. |
| Keep logic inside PCF lifecycle methods and helpers they own | Manipulate unrelated model-driven app DOM directly. |
| Validate context parameters and dataset values | Assume every property is present and typed. |
| Use framework APIs for outputs and notifications | Depend on unsupported globals or form internals. |

## Checklist Before Opening a PR

- [ ] The component is intended for a model-driven app column, grid, or sub grid.
- [ ] Power Platform CLI project files remain compatible with the documented PCF workflow.
- [ ] `ControlManifest.Input.xml` accurately describes properties, resources, datasets, and version metadata.
- [ ] The manifest version property is bumped for runtime behavior changes.
- [ ] TypeScript lifecycle methods validate context parameters before use.
- [ ] Interactive UI is accessible and keyboard-operable.
- [ ] The component avoids direct DOM access outside its container.
- [ ] Build and packaging configuration in JSON, `.pcfproj`, and `.csproj` files remains minimal and explicit.

## References

- Microsoft Power Platform CLI: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/get-powerapps-cli
- Code components for canvas apps: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps
- PCF prerequisites: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf#prerequisites
- Create your first code component: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript
- Add code components to model-driven apps: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/add-custom-controls-to-a-field-or-entity
- Linear slider control image: https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/media/add-slider.png
- Data Set Grid component image: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/add-dataset-component.png
- Power Apps component framework overview: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview
- Learn Power Apps component framework: https://learn.microsoft.com/en-us/training/paths/use-power-apps-component-framework

---
paths:
  - "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
---

<!-- Generated from harness/github-copilot/instructions/pcf-code-components.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Apps component framework code component conventions for manifests, TypeScript lifecycle methods, resources, outputs, state, cleanup, packaging, and solution reuse.

# PCF Code Component Conventions — Manifest, Lifecycle, and Resources

These instructions apply to Power Apps component framework component files matched by the PCF TypeScript, XML, project, and resource globs. They are authoritative for code component structure, `ControlManifest.Input.xml`, lifecycle methods, resources, outputs, state, cleanup, and solution packaging; canvas-app, event, and theming instructions win for their narrower PCF concerns. Code components are solution components that can be imported into environments and used in model-driven and canvas apps, with identical definition and implementation but different configuration surfaces.

## Component Shape and Manifest

Code components consist of three core elements: manifest, component implementation, and resources.

- Define metadata in `ControlManifest.Input.xml`.
- Use the manifest to declare the component name, constructor, namespace, data kind, configurable properties, and required resource files.
- Declare whether configured data is a `field` or a `dataset`.
- Treat manifest properties as configuration columns whose runtime values are available to the component through `context.parameters.<property name from manifest>`.
- Keep manifest metadata accurate so the application filters valid components for the current configuration context.
- Preserve the relationship between the manifest namespace and constructor and the runtime object creation pattern `new <"namespace on manifest">.<"constructor on manifest">()`.

## TypeScript Implementation Lifecycle

- Implement code components in TypeScript.
- Use the Power Platform CLI to auto-generates or generate the initial `index.ts` stub with `pac pcf init`.
- Implement the required lifecycle methods `init`, `updateView`, and `destroy`.
- Implement `getOutputs` when the component writes values back to the host.
- Keep `init(context, notifyOutputChanged, state, container)` focused on setup, initial context capture, event wiring, and DOM mounting.
- Use `updateView(context)` to reflect app data changes in the component UI.
- Call `notifyOutputChanged` when user interaction changes data that the host should retrieve asynchronously.
- Return changed values from `getOutputs` for `field` components and other output-enabled properties.
- Implement `destroy` to detach event handlers and release resources when the page closes.

| Method | Requirement | Purpose |
| --- | --- | --- |
| `init` | Required | Called when the page loads and receives `context`, `notifyOutputChanged`, `state`, and `container`. |
| `updateView` | Required | Called when app data changes and passes the new context object. |
| `getOutputs` | Optional | Returns changed values after `notifyOutputChanged`. |
| `destroy` | Required | Runs when the page closes and must remove cleanup code such as event handlers. |

## Context, State, and Data Flow

- Read inputs through `context.parameters.<property name from manifest>`.
- Use the framework APIs available on `context` instead of assuming host-specific globals.
- Treat `container` as the HTML div element where the component appends or mounts UI.
- Use `setControlState` only for component data that should be available during the next page load in the same session.
- Remember that memory allocated by a code component is cleared when the user navigates away, except browser-retained references such as event handlers if `destroy` fails to remove them.

## Resources and Packaging

- Declare resources in the manifest `resources` node.
- Include at least one `code` resource; the generated `index.ts` file is the usual code resource.
- Declare additional CSS files, image web resources, and Resx web resources for localization when the component requires them.
- Package and distribute code components through solutions so they can be imported into different environments.

## Good / Bad Examples

The examples below illustrate lifecycle and output discipline.

**Good:**

```typescript
public init(context, notifyOutputChanged, state, container): void {
  this.notifyOutputChanged = notifyOutputChanged;
  this.container = container;
  this.input = context.parameters.sampleProperty.raw ?? "";
}

public updateView(context): void {
  this.input = context.parameters.sampleProperty.raw ?? "";
  this.render();
}

public destroy(): void {
  this.button?.removeEventListener("click", this.onClick);
}
```

Why: The component reads through `context.parameters`, updates when context changes, and cleans up event handlers.

**Bad:**

```typescript
public updateView(context): void {
  document.body.appendChild(document.createElement("button"));
}
```

Why: The component ignores `container`, leaks DOM on every update, and has no cleanup path in `destroy`.


- Preserve sample namespace patterns such as `SampleNameSpace`, `LinearInputComponent`, and `SampleNameSpace.LinearInputComponent` when explaining manifest constructor mapping.
## Conventions

| Rule | Rationale |
| --- | --- |
| Keep manifest, implementation, and resources aligned | The platform discovers and configures components from manifest metadata |
| Use `ControlManifest.Input.xml` to define `field`, `dataset`, properties, and resources | Runtime behavior depends on accurate manifest declarations |
| Implement `init`, `updateView`, and `destroy`; add `getOutputs` for outputs | The framework lifecycle requires predictable setup, rendering, output, and cleanup |
| Call `notifyOutputChanged` before expecting the host to call `getOutputs` | Output propagation is asynchronous and host-controlled |
| Use `setControlState` only for same-session component state | State persistence stays intentional and bounded |
| Remove event handlers in `destroy` | Browser-retained handlers can leak memory after page close |
| Use solution packaging for distribution | Code components are solution components imported into environments |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Generate stubs with `pac pcf init` and refine them | Invent lifecycle signatures that do not match the framework |
| Read configuration from `context.parameters.<property name from manifest>` | Hardcode property values or depend on host globals |
| Append UI into the provided `container` | Attach component UI arbitrarily to `document.body` |
| Declare CSS, image web resources, and Resx web resources in the manifest | Load undeclared resources and hope packaging finds them |
| Use `notifyOutputChanged` and `getOutputs` for user changes | Mutate host data without notifying the framework |
| Clean up in `destroy` | Leave event handlers, timers, or subscriptions alive |

## Checklist Before Opening a PR

- [ ] `ControlManifest.Input.xml` declares component name, namespace, constructor, `field` or `dataset`, properties, and resources accurately.
- [ ] TypeScript implementation includes `init`, `updateView`, `destroy`, and `getOutputs` when outputs are needed.
- [ ] Runtime input reads use `context.parameters.<property name from manifest>`.
- [ ] User changes call `notifyOutputChanged` before outputs are retrieved.
- [ ] `setControlState` is used only for same-session state that genuinely needs persistence.
- [ ] `destroy` removes event handlers and cleanup code.
- [ ] Resources include at least one code resource and any CSS, image web resources, or Resx web resources required.
- [ ] Packaging expectations for solution import and environment reuse are preserved.

## Related Primitives

- `pcf-canvas-apps` instruction: use it for canvas app enablement, import, Studio safety, and maker configuration conventions.
- `pcf-events` instruction: use it for custom event declaration and handling.
- `pcf-fluent-modern-theming` instruction: use it for Fluent UI theming and platform library conventions.

## References

- Manifest schema reference: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/>
- Resources element: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/resources>
- Power Platform CLI: <https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction>
- Create and build a code component: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf>
- Package and distribute extensions using solutions: <https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm>

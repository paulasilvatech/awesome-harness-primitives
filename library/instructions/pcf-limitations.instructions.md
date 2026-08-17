---
applyTo: "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
description: "Enforces Power Apps Component Framework limitations for Canvas Apps, Dataverse APIs, bundled libraries, storage, authentication, and platform references."
---

# Power Apps Component Framework Conventions — Platform Limitations

These instructions apply to Power Apps Component Framework code components, manifests, build files, and related TypeScript or JavaScript assets. They are authoritative for PCF limitations around Canvas Apps, Dataverse-dependent APIs, external libraries, browser storage, and custom authentication; official Microsoft Power Apps Component Framework documentation wins where platform availability changes.

## Canvas App API Boundaries

Microsoft Dataverse-dependent APIs, including WebAPI, are not available for Power Apps canvas applications yet. Check individual API availability in the Power Apps component framework API reference before using an API from a component intended for Canvas Apps, model-driven apps, or Power Pages.

Never assume a PCF API is available in every host. Model host-specific behavior explicitly and fail gracefully when the host does not expose the required capability.

## Libraries and Bundling

Code components should either use React controls and platform libraries or bundle all external library code into the primary component-specific bundle. Keep the dependency graph small because PCF bundles affect load time, supportability, and platform compatibility.

Use the Power Apps command line interface patterns for bundling external library content when a component needs a dependency. The Angular flip component sample demonstrates component-specific bundling for external library content.

## Browser Storage and Client Data

Do not use HTML web storage objects such as `window.localStorage` or `window.sessionStorage` to store component data. Data stored locally on a user's browser or mobile client is not secure, is not guaranteed to be reliably available, and may violate host expectations.

Keep durable data in Dataverse, connectors, or host-supported APIs according to the app type. Keep transient UI state in component state only for the current rendering session.

## Authentication and Integration

Custom auth in code components is not supported in Power Apps canvas applications. Use connectors to get data and take actions instead of embedding custom OAuth flows, tokens, or credential prompts inside the PCF component.

## Good / Bad Examples

The examples below illustrate avoiding unsupported storage in a component.

**Good:**

```ts
this.currentFilter = context.parameters.filter.raw ?? undefined;
notifyOutputChanged();
```

Why: The component keeps transient state in memory and communicates through the PCF output contract.

**Bad:**

```ts
window.localStorage.setItem("pcf-filter", JSON.stringify(filter));
```

Why: `window.localStorage` is not a secure or reliable persistence mechanism for PCF component data.

## Conventions

| Rule | Rationale |
|---|---|
| Verify PCF API availability for the target host before using Dataverse-dependent APIs or WebAPI | Canvas Apps do not expose every Dataverse-dependent API. |
| Use React controls and platform libraries or bundle external libraries into the primary component bundle | PCF components must carry their runtime dependencies predictably. |
| Avoid `window.localStorage` and `window.sessionStorage` for component data | Browser and mobile local storage is insecure and unreliable for business data. |
| Use connectors instead of custom auth in Canvas App code components | Canvas Apps do not support custom authentication inside PCF components. |
| Keep host-specific behavior explicit | Components fail predictably when platform capabilities differ. |

## Do / Do Not

| Do | Do not |
|---|---|
| Check the Power Apps component framework API reference for individual API availability | Assume WebAPI or another Dataverse-dependent API works in Canvas Apps. |
| Use platform libraries or bundle external library content into the component-specific bundle | Depend on libraries that are not included or platform-provided. |
| Use connectors for Canvas App data access and actions | Embed custom auth flows in a Canvas App code component. |
| Keep durable data in supported platform stores | Store business data in `window.localStorage` or `window.sessionStorage`. |
| Reference official PCF samples for bundling patterns | Invent unsupported packaging behavior. |

## Checklist Before Opening a PR

- [ ] Target host availability was checked for every PCF API used by the component.
- [ ] Canvas App components do not rely on Dataverse-dependent APIs or WebAPI when unavailable.
- [ ] External libraries are either platform libraries or bundled into the primary component bundle.
- [ ] The component does not use `window.localStorage` or `window.sessionStorage` for data storage.
- [ ] Canvas App integrations use connectors rather than custom auth inside the component.
- [ ] Host-specific limitations are documented in code or component documentation where relevant.

## References

- [Power Apps component framework API reference](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/)
- [React controls and platform libraries](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/react-controls-platform-libraries)
- [Angular flip component sample](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/sample-controls/angular-flip-control)
- [Power Apps component framework overview](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview)

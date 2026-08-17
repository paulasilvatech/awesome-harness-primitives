---
applyTo: "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
description: "Enforces Power Apps Component Framework overview conventions for capabilities, limitations, web-resource differences, APIs, licensing, and packaging. Use when building or documenting PCF code components."
---

# Power Apps Component Framework Conventions — Code Component Fundamentals

These instructions apply to TypeScript, JavaScript, JSON, XML, `.pcfproj`, and `.csproj` files that implement or describe Power Apps Component Framework code components. They are authoritative for PCF capabilities, limitations, lifecycle expectations, APIs, licensing declarations, and solution packaging in matched files; Power Platform solution architecture and tenant licensing policy win where they define stricter requirements.

## Capabilities, Limits, and Web Resource Differences

Power Apps component framework enables professional developers and app makers to create code components for model-driven and canvas apps. Use code components to enhance forms, views, dashboards, and canvas app screens, such as replacing a numeric text column with a `dial` or `slider`, or transforming a dataset list into a `Calendar` or `Map` experience.

PCF works on Unified Interface and is not supported on the legacy web client. PCF is not supported for on-premises environments. Unlike HTML web resources, code components render as part of the same context, load with other components, and provide a seamless user experience. Components can be reused across tables and forms, moved across environments, made available through AppSource, and bundled with HTML, CSS, and TypeScript files into a single solution package.

## Framework APIs and Development Benefits

Use PCF APIs for component lifecycle management, contextual data and metadata access, server access through Web API, utility and data formatting methods, device features such as camera, location, and microphone, and user experience elements such as dialogs, lookups, and full-page rendering. Design components for modern web practices, performance, reusability, single-solution packaging, and being destroyed and reloaded for performance reasons while preserving state.

## Licensing and External Services

| Component type | Convention |
| --- | --- |
| Premium code components | Components that connect to external services or data directly through the user's browser client, not through connectors, are premium; apps using them become premium and end-users require Power Apps licenses. |
| Standard code components | Components that do not connect to external services or data keep apps standard when only standard features are used; end-users require at least an Office 365 license. |
| Dataverse model-driven apps | End users require Power Apps licenses when code components are used in model-driven apps connected to Microsoft Dataverse. |

Declare premium external service usage in the manifest when required.

```xml
<external-service-usage enabled="true">
  <domain>www.microsoft.com</domain>
</external-service-usage>
```

## Good / Bad Examples

The examples below illustrate declaring external service usage.

**Good**

```xml
<external-service-usage enabled="true">
  <domain>www.microsoft.com</domain>
</external-service-usage>
```

Why: the manifest declares browser-client external service access that affects premium licensing.

**Bad**

```xml
<control namespace="Sample" constructor="MapControl" version="1.0.0" />
```

Why: an externally connected component without `external-service-usage` hides licensing impact from makers and reviewers.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use PCF for model-driven and canvas app code components that improve forms, views, dashboards, and canvas screens. | Components integrate with Power Apps surfaces instead of acting like isolated web resources. |
| Respect Unified Interface and on-premises support limitations. | Unsupported clients and environments create deployment failures. |
| Use framework APIs for lifecycle, context, Web API, formatting, device features, dialogs, lookups, and full-page rendering. | Components behave consistently inside the Power Apps runtime. |
| Bundle HTML, CSS, and TypeScript into solution packages. | Components can move across environments and AppSource distribution. |
| Declare external browser-client service usage in the manifest. | Premium licensing implications are explicit. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `dial`, `slider`, `Calendar`, or `Map` style components when they improve user experience. | Rebuild simple standard controls without a user-experience reason. |
| Preserve state across destroy and reload cycles. | Assume component instances live for the full app session. |
| Use Web API and contextual metadata through PCF APIs. | Treat PCF like a standalone HTML web resource. |
| Confirm license impact for external services and Dataverse model-driven apps. | Ship components that silently make apps premium. |
| Package reusable components for movement across environments. | Leave code, CSS, or metadata outside the solution package. |

## Checklist Before Opening a PR

- [ ] The component targets supported Power Apps surfaces and does not require legacy web client or on-premises support.
- [ ] PCF lifecycle, context, metadata, Web API, utility, formatting, device, and UX APIs are used appropriately.
- [ ] The component can be destroyed and reloaded while preserving required state.
- [ ] HTML, CSS, TypeScript, manifest, and project files are packaged into the solution.
- [ ] External-service usage and premium licensing implications are declared and documented.
- [ ] Dataverse model-driven app licensing impact is understood for end users.

## References

- What are code components?: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/custom-controls-overview
- Code components for canvas apps: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps
- Create and build a code component: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/create-custom-controls-using-pcf
- Learn Power Apps component framework: https://learn.microsoft.com/en-us/training/paths/use-power-apps-component-framework
- Use code components in Power Pages: https://learn.microsoft.com/en-us/power-apps/maker/portals/component-framework
- Create components with Power Apps Component Framework - Training: https://learn.microsoft.com/en-us/training/paths/create-components-power-apps-component-framework/
- Microsoft Certified: Power Platform Developer Associate: https://learn.microsoft.com/en-us/credentials/certifications/power-platform-developer-associate/

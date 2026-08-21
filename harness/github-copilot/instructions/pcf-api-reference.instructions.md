---
applyTo: "**/*.{ts,tsx,js}"
description: "Enforces Power Apps Component Framework API conventions and availability checks for model-driven and canvas apps."
---

# Power Apps Component Framework Conventions — API Availability

These instructions apply to TypeScript and JavaScript code for Power Apps Component Framework (PCF) code components. They are authoritative for PCF API availability, namespace usage, lifecycle methods, platform compatibility, type safety, null checks, error handling, and performance in matched files; project-specific component architecture and Dataverse security rules win when they define stricter target-app behavior.

## API Availability

Check API availability for the target platform before using an interface. `AttributeMetadata` is model-driven only; the other listed interfaces are available in both model-driven apps and canvas apps.

| API | Model-driven apps | Canvas apps |
|---|---|---|
| AttributeMetadata | Yes | No |
| Client | Yes | Yes |
| Column | Yes | Yes |
| ConditionExpression | Yes | Yes |
| Context | Yes | Yes |
| DataSet | Yes | Yes |
| Device | Yes | Yes |
| Entity | Yes | Yes |
| Events | Yes | Yes |
| Factory | Yes | Yes |
| Filtering | Yes | Yes |
| Formatting | Yes | Yes |
| ImageObject | Yes | Yes |
| Linking | Yes | Yes |
| Mode | Yes | Yes |
| Navigation | Yes | Yes |
| NumberFormattingInfo | Yes | Yes |
| Paging | Yes | Yes |
| Popup | Yes | Yes |
| PopupService | Yes | Yes |
| PropertyHelper | Yes | Yes |
| Resources | Yes | Yes |
| SortStatus | Yes | Yes |
| StandardControl | Yes | Yes |
| UserSettings | Yes | Yes |
| Utility | Yes | Yes |
| WebApi | Yes | Yes |

## Context and Data APIs

The `Context` object is passed to component lifecycle methods and exposes `Client`, `Device`, `Factory`, `Formatting`, `Mode`, `Navigation`, `Resources`, `UserSettings`, `Utils`, and `WebApi`. Use `context.client.getFormFactor()` and `context.client.isOffline()` to adapt behavior. Use `context.userSettings.locale`, number formatting, security roles, and `NumberFormattingInfo` for user-specific display. Use `context.utils.getEntityMetadata`, `context.utils.hasEntityPrivilege`, and `context.utils.lookupObjects` when metadata or lookup behavior is needed.

Use `DataSet`, `Column`, `Entity`, `Filtering`, `Linking`, `Paging`, and `SortStatus` for tabular data. Access records through `context.parameters.dataset.records` and sorting through `context.parameters.dataset.sorting`; check null or undefined before reading optional API objects.

## UI, Metadata, and Lifecycle APIs

Use `Popup`, `PopupService`, and `Mode` for UI behavior and rendering mode. Use `AttributeMetadata` only in model-driven components for detailed column metadata, and `PropertyHelper` for property metadata helpers. Implement `StandardControl` lifecycle methods consistently: `init()` initializes the component, `updateView()` updates the UI when context changes, `getOutputs()` returns output values, and `destroy()` cleans up resources.

## WebApi, Device, and Formatting Patterns

Use `context.webAPI.retrieveMultipleRecords("account", "?$select=name")` for retrieve queries and `context.webAPI.createRecord("contact", data)` for create operations. Use `context.device.captureImage()` and `context.device.getCurrentPosition()` only after confirming the target app and device support the capability. Use `context.formatting.formatDateLong(date)` and `context.formatting.formatDecimal(value)` instead of hand-coded locale formatting.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `null/undefined` `try-catch`.

Keep TypeScript definitions accurate so IntelliSense exposes the PCF API surface correctly.

## Good / Bad Examples

The examples below show target-platform and null-safe API usage.

**Good:**

```typescript
const formFactor = context.client.getFormFactor();
const userLocale = context.userSettings.locale;
const records = context.parameters.dataset?.records ?? {};
```

Why: The code uses PCF context APIs and guards optional dataset access.

**Bad:**

```typescript
const metadata = context.parameters.field.attributes;
const name = context.parameters.dataset.records[id].getValue('name');
```

Why: It assumes model-driven metadata and dataset records are always available, which can break canvas apps or empty states.

## Conventions

| Rule | Rationale |
|---|---|
| Verify API availability for model-driven apps and canvas apps | PCF components can run in different hosts with different capabilities |
| Use `Context` lifecycle data instead of globals | Components stay portable across Power Apps hosts |
| Implement `init()`, `updateView()`, `getOutputs()`, and `destroy()` cleanly | The framework relies on predictable lifecycle behavior |
| Use TypeScript and generated PCF types | API misuse is caught before runtime |
| Check null and undefined before reading context members | Canvas/model-driven differences and empty data sets do not crash components |
| Wrap WebApi, device, and navigation calls in error handling | Host API failures produce recoverable UI states |
| Cache API results only when the data is stable and invalidation is clear | Repeated calls hurt performance, but stale data breaks correctness |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `context.webAPI.retrieveMultipleRecords` and `createRecord` for Dataverse access | Bypass the PCF `WebApi` with ad hoc host calls |
| Use `context.formatting.formatDateLong` and `formatDecimal` | Hand-code date or number formatting |
| Use `context.device.captureImage` and `getCurrentPosition` behind capability checks | Assume every host has the same device APIs |
| Clean up listeners and resources in `destroy()` | Leave timers, subscriptions, or DOM handlers alive |
| Test in the target model-driven or canvas environment | Assume behavior is identical across app types |
| Use `AttributeMetadata` only for model-driven apps | Use model-driven-only APIs in canvas components |

## Checklist Before Opening a PR

- [ ] Target app type is known and every PCF API used is available for that platform.
- [ ] `Context`, `Client`, `Device`, `Formatting`, `Navigation`, `Resources`, `UserSettings`, `Utility`, and `WebApi` usage is typed and null-safe.
- [ ] Dataset code handles `DataSet`, `Column`, `Entity`, `Filtering`, `Linking`, `Paging`, and `SortStatus` correctly.
- [ ] `StandardControl` lifecycle methods `init()`, `updateView()`, `getOutputs()`, and `destroy()` remain focused and complete.
- [ ] WebApi, device, and navigation calls have error handling and appropriate caching.
- [ ] Component behavior was tested in the target model-driven or canvas environment.

## References

- Power Apps component framework API reference: https://learn.microsoft.com/power-apps/developer/component-framework/reference/
- PowerApps-Samples component framework repository: https://github.com/microsoft/PowerApps-Samples/tree/master/component-framework

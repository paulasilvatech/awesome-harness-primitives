---
paths:
  - "**/*.xml"
---

<!-- Generated from harness/github-copilot/instructions/pcf-manifest-schema.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Apps Component Framework ControlManifest.Input.xml schema conventions for manifest elements, resources, features, platform libraries, validation, and data types.

# PCF Manifest Schema Conventions — Control Metadata

These instructions apply to XML Power Apps Component Framework manifests, especially `ControlManifest.Input.xml`. They are authoritative for manifest element usage, schema attributes, resource declarations, feature declarations, platform availability, and validation in matched XML files; official PCF schema validation and project-specific component requirements win when they impose stricter constraints.

## Root, Control, and Core Elements

A PCF manifest is the metadata contract for a code component. Keep the root and component identity explicit.

| Element | Purpose | Required or common attributes | Availability |
| --- | --- | --- | --- |
| `manifest` | Root element containing the entire component definition | None beyond schema-valid children | Model-driven apps, canvas apps, portals |
| `control` | Component identity, namespace, version, display, and type | `namespace`, `constructor`, `version`, `display-name-key`, `description-key`, `control-type` (`standard` or `virtual`) | Model-driven apps, canvas apps, portals |
| `code` | Resource file implementing component logic | `path`, `order` (typically `1`) | Model-driven apps, canvas apps, portals |

Use semantic versions such as `1.0.0` for component `version` and resource versions. Use localization resource keys rather than hardcoded display strings.

## Properties, Type Groups, and Datasets

Model component input, output, and tabular data precisely.

| Element | Convention | Key attributes |
| --- | --- | --- |
| `property` | Define an input or bound property with the most specific data type available. | `name`, `display-name-key`, `description-key`, `of-type`, `usage` (`bound` or `input`), `required`, `of-type-group`, `default-value` |
| `type-group` | Group accepted types when one property can accept multiple data types. | `name`; child `type` values such as `Whole.None`, `Currency`, `FP`, `Decimal` |
| `data-set` | Define a dataset property for tabular data. | `name`, `display-name-key`, `description-key` |

Common `of-type` values include `SingleLine.Text`, `Multiple`, `SingleLine.TextArea`, `SingleLine.Email`, `SingleLine.Phone`, `SingleLine.Url`, `SingleLine.Ticker`, `Whole.None`, `Currency`, `FP`, `Decimal`, `DateAndTime.DateAndTime`, `DateAndTime.DateOnly`, `TwoOptions`, `Lookup.Simple`, `OptionSet`, `MultiSelectOptionSet`, and `Enum`.

## Resources and Localization

Keep all component resources in the `resources` container and organize them by purpose.

| Element | Purpose | Attributes |
| --- | --- | --- |
| `resources` | Container for code, CSS, images, and localization files | Child elements only |
| `css` | Stylesheet resource | `path`, `order` |
| `img` | Image resource | `path` |
| `resx` | Localization resource file | `path`, `version` |

Organize resources in folders such as `css/`, `img/`, and `strings/`. Scope CSS to avoid conflicts with host applications.

## Features, Dependencies, Libraries, Events, and Actions

Declare platform interaction explicitly so the host can enforce availability and permissions.

| Element | Convention | Availability |
| --- | --- | --- |
| `feature-usage` | Container for `uses-feature` declarations. | Model-driven apps, canvas apps |
| `uses-feature` | Declare platform features with `name` and `required`; common feature names include `Device.captureAudio`, `Device.captureImage`, `Device.captureVideo`, `Device.getBarcodeValue`, `Device.getCurrentPosition`, `Device.pickFile`, `Utility.lookupObjects`, and `WebAPI`. | Varies by feature and platform |
| `dependency` | Declare external dependencies required by the component. | Model-driven apps, canvas apps |
| `external-service-usage` | Declare external services with `enabled`. | Model-driven apps, canvas apps |
| `platform-library` | Reference platform-provided libraries using `name` and `version`, such as `React` or `Fluent`. | Model-driven apps, canvas apps |
| `event` | Define custom events with `name`, `display-name-key`, and `description-key`. | Model-driven apps, canvas apps |
| `platform-action` | Define platform actions a component can invoke. | Model-driven apps |

Mark features as required only when the component cannot function without them.

## Platform Availability and Validation

Test every manifest in the target host environment.

- Treat Model-driven apps as fully supported for most manifest elements.
- Treat canvas apps as supported with limitations, especially for datasets and specific Device APIs.
- Treat portals and Power Pages support as platform-specific and verify each feature.
- Validate manifests during build; missing required elements and invalid attribute values should fail.
- Use `pac pcf` commands to validate manifest structure before shipping.

## Good / Bad Examples

The examples below illustrate a compact manifest with localized metadata, typed properties, resources, feature usage, and platform libraries.

**Good:**

```xml
<manifest>
  <control namespace="SampleNamespace" constructor="SampleControl" version="1.0.0" display-name-key="Sample_Display_Key" description-key="Sample_Desc_Key" control-type="standard">
    <property name="sampleProperty" display-name-key="Property_Display_Key" description-key="Property_Desc_Key" of-type="SingleLine.Text" usage="bound" required="true" />
    <type-group name="numbers"><type>Whole.None</type><type>Currency</type><type>FP</type><type>Decimal</type></type-group>
    <property name="numericProperty" display-name-key="Numeric_Display_Key" of-type-group="numbers" usage="bound" />
    <data-set name="dataSetProperty" display-name-key="Dataset_Display_Key" />
    <event name="onCustomEvent" display-name-key="Event_Display_Key" description-key="Event_Desc_Key" />
    <resources>
      <code path="index.ts" order="1" />
      <css path="css/SampleControl.css" order="1" />
      <img path="img/icon.png" />
      <resx path="strings/SampleControl.1033.resx" version="1.0.0" />
    </resources>
    <feature-usage><uses-feature name="WebAPI" required="true" /><uses-feature name="Device.captureImage" required="false" /></feature-usage>
    <platform-library name="React" version="16.8.6" />
    <platform-library name="Fluent" version="8.29.0" />
  </control>
</manifest>
```

Why: The manifest uses schema elements deliberately, avoids hardcoded display text, declares resources, and identifies required features.

**Bad:**

```xml
<control namespace="SampleNamespace" constructor="SampleControl" version="1" display-name-key="Sample" control-type="standard">
  <property name="value" of-type="SingleLine.Text" usage="bound" />
</control>
```

Why: The fragment lacks the `manifest` root, descriptions, semantic versioning, resource keys, resources, and feature declarations.

## Schema Vocabulary

Retain schema terms reviewers search for: `TypeScript/JavaScript`, `TypeScript`, `JavaScript`, `true/false`, `type-groups`, and `Date/Time**` from the prior data type headings.

## Conventions

| Rule | Rationale |
|---|---|
| Keep `ControlManifest.Input.xml` metadata complete and schema-valid | The host discovers component behavior from the manifest |
| Use semantic versions and localized resource keys | Component upgrades and UI text remain maintainable |
| Choose the most specific `of-type` or `of-type-group` | Makers get correct configuration and data binding behavior |
| Declare every platform feature in `feature-usage` | Runtime permissions and platform availability stay explicit |
| Keep code, CSS, images, and `.resx` files under `resources` | Packaging and load order remain predictable |
| Validate with `pac pcf` and target-host testing | Schema validity alone does not prove platform behavior |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `display-name-key` and `description-key` for user-facing text | Hardcode display names directly in the manifest |
| Mark `required` only for essential properties and features | Make optional capabilities block component use |
| Scope CSS and organize resources under `css/`, `img/`, and `strings/` | Let styles or assets conflict with host applications |
| Use `platform-library` for supported platform React or Fluent versions | Bundle duplicate platform libraries without need |
| Test in Model-driven apps, canvas apps, portals, or Power Pages as applicable | Assume every manifest element behaves the same on every platform |

## Checklist Before Opening a PR

- [ ] `manifest` and `control` elements are present and schema-valid.
- [ ] `namespace`, `constructor`, `version`, `display-name-key`, `description-key`, and `control-type` are correct.
- [ ] Properties use specific `of-type` or `of-type-group` values and correct `usage`.
- [ ] Dataset properties are only used where the target platform supports them.
- [ ] `resources` includes required `code`, `css`, `img`, and `resx` entries with valid paths and order.
- [ ] `feature-usage` declares every Device, Utility, or `WebAPI` feature the component uses.
- [ ] Dependencies, external services, platform libraries, events, and platform actions are declared when used.
- [ ] CSS is scoped and resources are organized in `css/`, `img/`, and `strings/` where applicable.
- [ ] `pac pcf` validation and target-platform testing pass.

---
applyTo: "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
description: "Enforces Power Pages conventions for using PCF code components, supported field types, unsupported APIs, model-driven field setup, form metadata, and portal Web API usage."
---

# PCF Power Pages Conventions — Portal Code Components

These instructions apply to PCF code components and manifest/project files intended for Power Pages. They are authoritative for Power Pages host eligibility, supported Dataverse field types, unsupported PCF APIs, model-driven field setup, Design Studio and Portals Management configuration, and portal Web API usage; general PCF implementation and non-Power Pages host instructions win for canvas or model-driven-only behavior.

## Host Prerequisites and Component Eligibility

Use Power Pages code components only when the environment and site meet the documented prerequisites: system administrator privileges are required to enable the feature, the Power Pages site version must be `9.3.3.x` or higher, and the starter site package must be `9.2.2103.x` or higher. Code components are available for web browsers using the client option of `Web`.

## Supported Field Types and Formats

Power Pages supports a restricted set of bound field types and formats. Keep component manifests and form configuration within these supported types.

| Supported type or format |
| --- |
| `Currency` |
| `DateAndTime.DateAndTime` |
| `DateAndTime.DateOnly` |
| `Decimal` |
| `Enum` |
| `Floating Point Number` |
| `Multiple` |
| `OptionSet` |
| `SingleLine.Email` |
| `SingleLine.Phone` |
| `SingleLine.Text` |
| `SingleLine.TextArea` |
| `SingleLine.Ticker` |
| `SingleLine.URL` |
| `TwoOptions` |
| `Whole` |

## Unsupported APIs and Restrictions

Do not use unsupported PCF APIs or manifest features in Power Pages components.

| Unsupported item | Restriction |
| --- | --- |
| `Device.captureAudio` | Not supported in Power Pages |
| `Device.captureImage` | Not supported in Power Pages |
| `Device.captureVideo` | Not supported in Power Pages |
| `Device.getBarcodeValue` | Not supported in Power Pages |
| `Device.getCurrentPosition` | Not supported in Power Pages |
| `Device.pickFile` | Not supported in Power Pages |
| `Utility` | Not supported in Power Pages |
| `uses-feature` | Must not be set to true |
| Value elements | Value elements not supported by PCF in Power Pages must not be used |
| Multiple bound fields | PCF controls bound to multiple fields in a form are not supported |

## Model-Driven and Power Pages Configuration

Create and package the code component with the standard Power Apps component framework workflow. Add the component to a field in a model-driven app before enabling it on a Power Pages form. In Data workspace, select the Dataverse form field, choose `+ Component`, select the component for the field, then save and publish the form.

Enable the component in Power Pages Design Studio by adding the form to a page, selecting the configured field, choosing `Edit field`, and enabling `Enable custom component`. The setup diagram remains an authoritative visual reference: https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/steps.png . The form component and add-component screenshots remain source references: https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/add-component-to-form.png and https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/enable-code-component.png .

## Portals Management App Metadata

When using the Portals Management app, configure Basic Form Metadata for the field: open `Portals Management`, select `Basic Forms`, open the target form, go to `Related`, select `Basic Form Metadata`, create `New Basic Form Metadata`, set `Type` to `Attribute`, set `Attribute Logical Name`, enter `Label`, set `Control Style` to `Code Component`, then save and close. Treat these values as metadata conventions that must remain consistent with the Dataverse form field.

## Portal Web API Components

A code component on a webpage may use the portal Web API to perform create, retrieve, update, and delete actions. Keep portal Web API usage aligned with Power Pages security and table permissions, and do not assume model-driven app APIs behave identically in the portal host.

## Good / Bad Examples

The examples below illustrate avoiding unsupported manifest features in Power Pages.

**Good:**

```xml
<property name="email" display-name-key="Email" of-type="SingleLine.Email" usage="bound" required="true" />
```

Why: The property uses a supported Power Pages field format and binds to one field.

**Bad:**

```xml
<feature-usage>
  <uses-feature name="Utility" required="true" />
</feature-usage>
```

Why: `uses-feature` must not be set to true and `Utility` is not supported in Power Pages.

## Conventions

| Rule | Rationale |
| --- | --- |
| Verify site `9.3.3.x` and package `9.2.2103.x` or higher before using PCF in Power Pages | Older sites cannot host the feature reliably |
| Bind only supported field types and formats | Unsupported Dataverse types fail or render inconsistently |
| Avoid `Device.*`, `Utility`, true `uses-feature`, unsupported value elements, and multiple bound fields | These APIs and manifest shapes are not supported in Power Pages |
| Add the code component to a model-driven field before enabling it in Power Pages | Power Pages consumes the field configuration from the Dataverse form |
| Use Design Studio or Portals Management metadata deliberately | The portal form must explicitly enable the custom component |
| Use portal Web API only with portal security assumptions | CRUD behavior depends on Power Pages permissions and context |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use supported formats such as `SingleLine.Email`, `OptionSet`, `TwoOptions`, and `Whole` | Bind a Power Pages component to unsupported field shapes |
| Configure the field in a model-driven app first | Expect Power Pages to discover an unconfigured PCF control automatically |
| Enable `Enable custom component` in Design Studio when using that path | Publish the form without enabling the custom component |
| Set `Control Style` to `Code Component` in Basic Form Metadata | Leave the field as a default portal control |
| Use portal Web API for page-level CRUD customizations | Assume unsupported PCF Device APIs work in the portal |
| Keep one bound field per Power Pages PCF control | Bind one control to multiple fields in a form |

## Checklist Before Opening a PR

- [ ] The Power Pages site and starter package meet minimum supported versions.
- [ ] The component uses only supported Power Pages field types and formats.
- [ ] No unsupported `Device.*`, `Utility`, true `uses-feature`, unsupported value elements, or multi-field binding is introduced.
- [ ] The code component is added to the Dataverse field in the model-driven app form.
- [ ] Design Studio or Portals Management metadata enables the custom component on the Power Pages form.
- [ ] Portal Web API usage respects Power Pages permissions and CRUD constraints.

## References

- Power Pages setup diagram: https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/steps.png
- Add form: https://learn.microsoft.com/en-us/power-pages/getting-started/add-form
- Site version `9.3.3.x`: https://learn.microsoft.com/en-us/power-apps/maker/portals/versions/version-9.3.3.x
- Starter package `9.2.2103.x`: https://learn.microsoft.com/en-us/power-apps/maker/portals/versions/package-version-9.2.2103
- Create first component: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/implementing-controls-using-typescript
- Property remarks: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/property#remarks
- Device.captureAudio: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/captureaudio
- Device.captureImage: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/captureimage
- Device.captureVideo: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/capturevideo
- Device.getBarcodeValue: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/getbarcodevalue
- Device.getCurrentPosition: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/getcurrentposition
- Device.pickFile: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/device/pickfile
- Utility: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/utility
- uses-feature: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/uses-feature
- Unsupported value elements: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/property#value-elements-that-are-not-supported
- Add code component to a column: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/add-custom-controls-to-a-field-or-entity#add-a-code-component-to-a-column
- Add code components to a column or table: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/add-custom-controls-to-a-field-or-entity
- Data workspace forms: https://learn.microsoft.com/en-us/power-pages/configure/data-workspace-forms
- Add component image: https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/add-component-to-form.png
- Enable component image: https://learn.microsoft.com/en-us/power-pages/configure/media/component-framework/enable-code-component.png
- Portals Management: https://learn.microsoft.com/en-us/power-pages/configure/portal-management-app
- Portal Web API overview: https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview
- Sample portal Web API component: https://learn.microsoft.com/en-us/power-pages/configure/implement-webapi-component
- Tutorial: https://learn.microsoft.com/en-us/power-pages/configure/component-framework-tutorial
- PCF overview: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview

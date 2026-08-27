---
paths:
  - "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
---

<!-- Generated from harness/github-copilot/instructions/pcf-dependent-libraries.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Apps component framework dependent-library conventions for shared Library Controls, feature flags, Webpack externals, manifest dependencies, and on-demand loading.

# PCF Dependent Library Conventions — Shared Library Controls

These instructions apply to Power Apps component framework projects matched by the PCF TypeScript, JavaScript, manifest, and project-file globs. They are authoritative for using dependent libraries, Library Controls, feature flags, Webpack externals, manifest `dependency` resources, and on-demand loading; broader PCF packaging, React platform-library, Power Pages, and solution deployment guidance wins where it defines a more specific host behavior.

## Library Control Ownership

Use a dependent library when several model-driven app components need the same large or prebuilt library. Keep the library in one Library Control and make dependent controls reference it instead of bundling duplicate copies into every control. This improves load time, runtime transfer, scripting, control rendering, and maintenance because the shared library is loaded once and independently maintained.

| Pattern | Convention | Rationale |
| --- | --- | --- |
| Library component | Create a Library component that contains the reusable library or shared function | The dependency has a single owner and deployment unit |
| Dependent component | Configure controls to depend on the Library Control | Consumers avoid bundling duplicate library files |
| Default loading | Let the dependency load with the component unless size or timing requires otherwise | Simple controls remain predictable |
| On-demand loading | Use `load-type="onDemand"` for large or rarely used dependencies | Complex controls pay the load cost only when required |

The before/after diagrams remain part of the source guidance: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-before-example.png and https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-after-example.png . The on-demand loading diagram is https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-on-demand-load.png .

## Feature Flags and Build Configuration

Add `featureconfig.json` at the component project root to override generated feature flags without editing `node_modules`.

| Flag | Value | Meaning |
| --- | --- | --- |
| `pcfResourceDependency` | `on` | Enables the component to consume a library resource |
| `pcfAllowCustomWebpack` | `on` for Library Controls that define externals | Enables a custom Webpack configuration |
| `pcfAllowCustomWebpack` | `off` for dependent controls that only consume the library | Keeps dependent controls on the default bundling path |

```json
{
  "pcfResourceDependency": "on",
  "pcfAllowCustomWebpack": "off"
}
```

Use `pcfAllowCustomWebpack` with care because it changes the build process. The original feature flags default to `off`; turn on only the capability required by the component.

## Webpack Externals

The PCF build uses Webpack to bundle code and dependencies into deployable assets. In the Library Control project, add `webpack.config.js` in the project root and mark the shared library alias as `externals` so the dependent control does not rebundle it.

```javascript
/* eslint-disable */
"use strict";

module.exports = {
  externals: {
    "myLib": "myLib"
  },
};
```

Keep the manifest alias, import name, and Webpack external name aligned. A mismatched alias causes the control to build but fail at runtime when the library cannot be resolved.

## Manifest Dependencies and On-Demand Loading

Register dependencies inside the manifest `resources` element with a `dependency` element. Order dependencies before the code resource when the code uses the library during initialization.

```xml
<resources>
  <dependency
    type="control"
    name="samples_SampleNS.SampleStubLibraryPCF"
    order="1"
  />
  <code path="index.ts" order="2" />
</resources>
```

For on-demand loading, add `platform-action`, `feature-usage`, and `uses-feature` under the `control` element, then set `load-type="onDemand"` on the `dependency` element.

```xml
<platform-action action-type="afterPageLoad" />
<feature-usage>
  <uses-feature name="Utility" required="true" />
</feature-usage>
<dependency type="control" name="samples_SampleNamespace.StubLibrary" load-type="onDemand" />
```

## Preview and Load-Type Notes

Dependent libraries were documented as `pre-release` guidance and may change; keep manifest changes conservative and aligned with current Microsoft documentation. Preserve both XML spellings: the manifest attribute uses `load-type="onDemand"`, and prose may refer to `onDemand` loading.

## Good / Bad Examples

The examples below illustrate keeping library ownership outside the consuming control bundle.

**Good:**

```xml
<resources>
  <dependency type="control" name="samples_SampleNamespace.StubLibrary" order="1" />
  <code path="index.ts" order="2" />
</resources>
```

Why: The control declares a manifest dependency and keeps the shared library in the Library Control.

**Bad:**

```javascript
import "./vendor/my-large-library.js";
```

Why: Every control bundles its own copy, increasing solution size and load time.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use a Library Control for shared prebuilt libraries used by multiple PCF controls | Prevents duplicate bundles and reduces runtime transfer |
| Keep `featureconfig.json` in the project root and never edit generated `node_modules` files | Feature flags remain explicit and source-controlled |
| Configure `pcfResourceDependency` and `pcfAllowCustomWebpack` only as needed | Avoids enabling preview build behavior without a concrete dependency |
| Register manifest `dependency` resources before dependent `code` resources | The library is available before consuming code runs |
| Use Webpack `externals` for the library alias in the Library Control | The shared library is excluded from dependent bundles |
| Use `load-type="onDemand"` only with the required `platform-action`, `feature-usage`, and `uses-feature` configuration | On-demand dependencies need platform support to load reliably |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Put reusable library code in a Library Control | Copy the same large library into each component |
| Preserve the same alias in `externals`, imports, and manifest configuration | Rename `myLib` in one place and not the others |
| Set `pcfResourceDependency` to `on` when consuming a library resource | Leave the dependent-library feature disabled |
| Add `pcfAllowCustomWebpack` only where custom bundling is required | Turn on custom Webpack for every control by habit |
| Use `load-type="onDemand"` for large optional dependencies | Delay-load a required startup dependency without reason |
| Keep `code path="index.ts"` ordered after its dependency | Let initialization race ahead of dependency loading |

## Checklist Before Opening a PR

- [ ] Shared libraries used by more than one control live in a Library Control.
- [ ] `featureconfig.json` declares only the required `pcfResourceDependency` and `pcfAllowCustomWebpack` flags.
- [ ] `webpack.config.js` marks the shared library alias as `externals` when custom bundling is required.
- [ ] `ControlManifest.Input.xml` registers the `dependency` inside `resources` with correct `type`, `name`, and `order`.
- [ ] On-demand dependencies include `platform-action`, `feature-usage`, `uses-feature`, and `load-type="onDemand"`.
- [ ] Dependent controls no longer bundle duplicate library files.

## References

- Webpack: https://webpack.js.org/
- Webpack externals: https://webpack.js.org/configuration/externals/
- Manifest `dependency`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/dependency
- Manifest `resources`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/resources
- Manifest `control`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/control
- Manifest `platform-action`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/platform-action
- Manifest `feature-usage`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/feature-usage
- Manifest `uses-feature`: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/uses-feature
- Tutorial: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/tutorial-use-dependent-libraries
- Before diagram: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-before-example.png
- After diagram: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-after-example.png
- On-demand diagram: https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/dependent-library-on-demand-load.png

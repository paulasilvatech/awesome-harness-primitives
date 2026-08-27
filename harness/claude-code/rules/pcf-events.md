---
paths:
  - "**/*.{ts,tsx,js,json,xml,pcfproj,csproj}"
---

<!-- Generated from harness/github-copilot/instructions/pcf-events.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Apps component framework event conventions for manifest event declarations, canvas Power Fx handlers, model-driven addEventHandler usage, payloads, callbacks, and event raising.

# PCF Event Conventions — Custom Events and Host Handlers

These instructions apply to PCF component files that define or handle custom events for canvas apps and model-driven apps. They are authoritative for event manifest declarations, component data flow, canvas Power Fx handlers, model-driven `addEventHandler` registration, payloads, callbacks, and event invocation; general PCF lifecycle and canvas app instructions win for broader component implementation and environment setup. Treat event APIs as preview and pre-release behavior and verify host availability before relying on custom event features.

## Component Data Flow and Event Scope

- Use the standard PCF data flow for ordinary value updates: inputs flow from the hosting app into the control, updated data flows out to the hosting form or page, and bound-field updates trigger the `OnChange` event.
- Use custom events only when field updates are not enough for the scenario.
- Remember that custom events occur separately for each instance of a code component in the app.
- Keep events purposeful: a custom event should represent a meaningful interaction or programmatic condition the host needs to handle.

## Manifest Event Declarations

- Define custom events in the manifest with the `event` element.
- Provide stable `name`, `display-name-key`, and `description-key` values.
- Keep related properties and events together so makers understand the event contract.
- Use manifest data so the hosting application can expose and react to events correctly.

```xml
<property
  name="sampleProperty"
  display-name-key="Property_Display_Key"
  description-key="Property_Desc_Key"
  of-type="SingleLine.Text"
  usage="bound"
  required="true"
/>
<event
  name="customEvent1"
  display-name-key="customEvent1"
  description-key="customEvent1"
/>
<event
  name="customEvent2"
  display-name-key="customEvent2"
  description-key="customEvent2"
/>
```

## Canvas App Event Handling

- Let makers configure canvas app event responses with Power Fx expressions on the PCF control properties pane.
- Keep event names and descriptions maker-friendly because they appear in the designer.
- Prefer normal bound-field `OnChange` behavior when a data update is the only signal the app needs.

## Model-Driven App Event Handling

- Use the model-driven Client API `addEventHandler` method to associate handlers with custom events.
- Retrieve the control through the form context and register each event handler explicitly.
- Register handlers per component instance; do not assume one registration covers every instance.

```javascript
const controlName1 = "cr116_personid";

this.onLoad = function (executionContext) {
  const formContext = executionContext.getFormContext();

  const sampleControl1 = formContext.getControl(controlName1);
  sampleControl1.addEventHandler("customEvent1", this.onSampleControl1CustomEvent1);
  sampleControl1.addEventHandler("customEvent2", this.onSampleControl1CustomEvent2);
}
```

## Payloads, Callbacks, and Invocation

- For model-driven apps, pass a payload with the event when the handler needs more context.
- Include callback functions in payloads only when the handler must call back into the component.
- Document payload shape so handlers know properties such as `message` and `callBackFunction`.
- Use the PCF Events API when calling events from component code.

```javascript
this.onSampleControl1CustomEvent1 = function (params) {
   //alert(`SampleControl1 Custom Event 1: ${params}`);
   alert(`SampleControl1 Custom Event 1`);
}.bind(this);

this.onSampleControl2CustomEvent2 = function (params) {
  alert(`SampleControl2 Custom Event 2: ${params.message}`);
  // prevent the default action for the event
  params.callBackFunction();
}
```

## Good / Bad Examples

The examples below illustrate when to use events instead of bound-field updates.

**Good:**

```xml
<event
  name="bundleCompleted"
  display-name-key="BundleCompleted_Display_Key"
  description-key="BundleCompleted_Description_Key"
/>
```

Why: The event name represents a meaningful interaction that another canvas or model-driven app area can handle without pretending it is a field value change.

**Bad:**

```xml
<event
  name="click"
  display-name-key="click"
  description-key="click"
/>
```

Why: The event is too generic for makers and scripts to understand, and a normal control interaction or bound value update may already cover it.


- Treat JavaScript event handlers as host integration code with stable names and documented payloads.
## Conventions

| Rule | Rationale |
| --- | --- |
| Prefer bound-field updates and `OnChange` for ordinary data flow | Existing host behavior is simpler and more predictable |
| Define custom events with manifest `event` elements | Hosts discover event contracts from manifest metadata |
| Use maker-friendly `display-name-key` and `description-key` values | Canvas designers and model-driven customizers need clear event choices |
| Configure canvas app handlers through Power Fx | Canvas apps expose event behavior in the control properties pane |
| Use `addEventHandler` for model-driven custom events | Model-driven apps bind handlers through the Client API |
| Pass payloads and callbacks only for complex model-driven scenarios | Event contracts stay understandable and testable |
| Treat each component instance independently | Events are raised and handled per instance |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use custom events for meaningful interactions beyond field updates | Create events for every click or implementation detail |
| Keep event names stable and descriptive | Rename event names casually after makers or scripts depend on them |
| Document payload properties such as `message` and `callBackFunction` | Pass undocumented objects to host scripts |
| Register model-driven handlers with `formContext.getControl(...).addEventHandler(...)` | Assume handlers are globally registered |
| Use Power Fx for canvas app event behavior | Expect canvas apps to use model-driven Client API handlers |
| Verify preview event API availability | Assume every host supports every event feature |

## Checklist Before Opening a PR

- [ ] Bound-field updates and `OnChange` are used when custom events are not necessary.
- [ ] Manifest events use stable `name`, `display-name-key`, and `description-key` values.
- [ ] Canvas app behavior can be configured with Power Fx on the control properties pane.
- [ ] Model-driven handlers use `addEventHandler` on the correct control instance.
- [ ] Payloads and callbacks are documented, including `message` and `callBackFunction` when present.
- [ ] Event behavior is verified per component instance.
- [ ] Preview API availability is checked for the target host.

## Related Primitives

- `pcf-code-components` instruction: use it for general manifest, lifecycle, resources, outputs, state, and cleanup rules.
- `pcf-canvas-apps` instruction: use it for canvas app enablement, import, and Studio security conventions.

## References

- Event element: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/event>
- Component events OnChange example image: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/component-events-onchange-example.png>
- Custom events in canvas designer image: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/custom-events-in-canvas-designer.png>
- addEventHandler method: <https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/clientapi/reference/controls/addeventhandler>
- Passing payload in events image: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/media/passing-payload-in-events.png>
- Events API: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/reference/events>
- Tutorial: Define a custom event in a component: <https://learn.microsoft.com/en-us/power-apps/developer/component-framework/tutorial-define-event>

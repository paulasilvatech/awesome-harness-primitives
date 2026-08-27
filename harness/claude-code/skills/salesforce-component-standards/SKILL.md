---
name: salesforce-component-standards
description: >-
  Apply Salesforce UI component standards for Lightning Web Components, Aura, Visualforce, SLDS 2,
  WCAG 2.1 AA, secure Apex access, component communication, XSS, CSRF, FLS/CRUD, view state, and
  Jest tests. Use when building or reviewing Salesforce LWC, Aura components, Visualforce pages,
  or Apex controllers used by UI components.
---

<!-- Generated from harness/github-copilot/skills/salesforce-component-standards/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Salesforce component standards

Review or build Salesforce UI components with platform-specific rules for data access, security, SLDS 2 styling, accessibility, component communication, performance, and tests.

## When to invoke

- "Review this Lightning Web Component for Salesforce standards."
- "Build an LWC that follows SLDS 2 and accessibility rules."
- "Check this Aura component and Apex controller for FLS/CRUD."
- "Audit this Visualforce page for XSS and CSRF issues."
- "Add Jest tests for this Salesforce component."

## LWC data access

| Use case | Pattern | Why |
| --- | --- | --- |
| Read one record reactively | `@wire(getRecord, { recordId, fields })` | Lightning Data Service is cached and reactive. |
| Standard CRUD form | `<lightning-record-form>` or `<lightning-record-edit-form>` | Built-in FLS, CRUD, and accessibility. |
| Complex server query or filtered list | `@wire(apexMethodName, { param })` on `cacheable=true` Apex | Cacheable wire re-runs when params change. |
| User-triggered DML or non-cacheable call | Imperative `apexMethodName(params).then(...).catch(...)` | DML cannot be wired unless `@AuraEnabled(cacheable=true)` and read-only. |
| Cross-component communication without shared parent | Lightning Message Service (LMS) | Decoupled across DOM boundaries. |
| Multi-object graph relationships | GraphQL `@wire(gql, { query, variables })` | Fetch related data in one round trip. |

## LWC security, styling, and communication

| Area | Rule |
| --- | --- |
| XSS | Never assign raw user data to `innerHTML`; use template `{expression}` binding. |
| Apex permissions | `@AuraEnabled` methods enforce CRUD/FLS using `WITH USER_MODE` in SOQL or explicit `Schema.sObjectType` checks. |
| Org IDs | Do not hardcode org-specific IDs in component JavaScript; query them or pass as props. |
| `@api` input | Validate type and range before using parent-supplied values in SOQL or Apex parameters. |
| SLDS 2 | Use `<lightning-*>` base components such as `lightning-button`, `lightning-input`, `lightning-datatable`, and `lightning-card`. |
| Colors | Do not hardcode `color: #FF3366`; use semantic SLDS tokens such as `var(--slds-c-button-brand-color-background)`. |
| CSS overrides | Do not override SLDS classes with `!important`; compose with custom CSS properties. |
| Modes | Test custom CSS in light mode and dark mode. |
| Parent to child | Use an `@api` property or an `@api` method. |
| Child to parent | Use `CustomEvent` and `this.dispatchEvent(new CustomEvent('eventname', { detail: data }))`. |
| Siblings/unrelated | Use Lightning Message Service. |
| Never use | `document.querySelector`, `window.*`, or Pub/Sub libraries for component communication. |
| Flow screen components | Events reaching Flow need `bubbles: true` and `composed: true`; expose `@api value` for two-way binding. |

## Accessibility and performance

Every LWC must satisfy WCAG 2.1 AA checks:

- [ ] Inputs have `<label>` or `aria-label`; placeholder text is not the only label.
- [ ] Icon-only buttons have `alternative-text` or `aria-label`.
- [ ] Interactive elements work with Tab, Enter, Space, and Escape.
- [ ] Color is not the only status indicator; pair it with text, icon, or `aria-*` attributes.
- [ ] Error messages are connected to inputs with `aria-describedby`.
- [ ] Modal focus moves inside on open and returns on close.

Performance rules:

- Avoid DML, heavy computation, or rendering state mutation in `connectedCallback` because it runs on every DOM attach.
- Guard `renderedCallback` with a boolean to prevent infinite render loops.
- Do not set reactive properties in `renderedCallback` unless necessary and guarded.
- Paginate or stream large datasets instead of storing them all in component state.

## Aura and Visualforce

| Technology | Rule |
| --- | --- |
| Aura vs LWC | New components should be LWC unless the target is Aura-only, such as extending `force:appPage` or using legacy Aura-specific events. |
| Aura controllers | `@AuraEnabled` methods must use `with sharing` and enforce CRUD/FLS; Aura does not enforce them automatically. |
| Aura output | Avoid unescaped `{!v.something}` in raw helpers; use `<ui:outputText value="{!v.text}" />` or escaping components. |
| Aura events | Prefer component events for parent-child; application events broadcast to the whole app and should be rare. |
| Hybrid stacks | Use Lightning Message Service between LWC and Aura. |
| Visualforce XSS | Never use `<apex:outputText value="{!userInput}" escape="false" />` for user-controlled data. |
| Visualforce CSRF | Use `<apex:form>` for postbacks; do not use raw `<form method="POST">`. |
| SOQL injection | Bind URL parameters: `WHERE Name = :nameParam`; do not concatenate `ApexPages.currentPage().getParameters().get('name')`. |
| View state | Keep view state under `135 KB`, use `transient`, avoid persisting large collections, and set `readonly="true"` on read-only pages. |
| Custom controllers | Standard controllers enforce FLS for bound fields; custom controllers must check `Schema.sObjectType.Account.fields.Revenue__c.isAccessible()` and DML permissions such as `Schema.sObjectType.Account.isDeletable()`. |

## Jest requirements

Every component with user interaction or Apex data retrieval needs Jest tests covering render, data, event, and error behavior.

```javascript
it('renders the component with correct title', async () => { /* ... */ });
it('calls apex method and displays results', async () => { /* wire mock */ });
it('dispatches event when button is clicked', async () => { /* ... */ });
it('shows error state when apex call fails', async () => { /* error path */ });
```

Use `@salesforce/sfdx-lwc-jest` utilities: `setImmediate` plus `emit({ data, error })` for wire adapter mocking, and `jest.mock('@salesforce/apex/MyClass.myMethod', ...)` for Apex method mocking.

## Anti-patterns

| Anti-pattern | Technology | Risk | Fix |
| --- | --- | --- | --- |
| `innerHTML` with user data | LWC | XSS | Use template bindings `{expression}`. |
| Hardcoded hex colors | LWC/Aura | Dark-mode and SLDS 2 breakage | Use SLDS CSS custom properties. |
| Missing `aria-label` on icon buttons | LWC/Aura/VF | Accessibility failure | Add `alternative-text` or `aria-label`. |
| No guard in `renderedCallback` | LWC | Infinite rerender loop | Add a `hasRendered` boolean guard. |
| Application event for parent-child | Aura | Unnecessary broadcast | Use component event. |
| `escape="false"` on user data | Visualforce | XSS | Remove it or sanitize rich text with a whitelist. |
| Raw `<form>` postback | Visualforce | CSRF vulnerability | Use `<apex:form>`. |
| No `with sharing` | VF / Apex | Data exposure | Add `with sharing`. |
| FLS not checked | VF / Apex | Privilege escalation | Add `Schema.sObjectType` checks. |
| SOQL concatenated with URL param | VF / Apex | SOQL injection | Use bind variables. |

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `<apex:page>`
- `<c:something>`
- `<div>`
- `ALWAYS`
- `ERROR`
- `FROM`
- `HTML`
- `NEVER`
- `SELECT`
- `auto-escapes`
- `auto-escaping`
- `built-in`
- `color: var(--slds-c-button-brand-color-background)`
- `component-by-component`
- `icon-only`
- `re-fires`
- `re-render`
- `round-trip`
- `server-side`
- `this.template.querySelector('.el').innerHTML = userValue`
- `view-state`
- `wire`
- `ApexPages.Message`
- `ApexPages.Severity.ERROR`
- `NoAccessException`
- `System.NoAccessException`

## Output template

```markdown
## Salesforce component standards result

**Status:** pass | fixes required | blocked
**Scope:** <LWC/Aura/Visualforce/Apex files>

| Area | Finding | Severity | Evidence | Required fix |
| --- | --- | --- | --- | --- |
| Security | <finding> | <High/Medium/Low> | <file/line or snippet> | <fix> |
| Accessibility | <finding> | <High/Medium/Low> | <file/line or snippet> | <fix> |
| Tests | <finding> | <High/Medium/Low> | <file/line or snippet> | <fix> |

### Validation
- <Jest, Apex test, manual accessibility, or code review check>
```

## Quality gate

- [ ] LWC data access uses the narrowest safe pattern.
- [ ] User-controlled data is escaped and never assigned to `innerHTML` or `escape="false"`.
- [ ] Apex exposed to UI enforces sharing, CRUD, and FLS with `WITH USER_MODE` or `Schema.sObjectType` checks.
- [ ] SLDS 2 tokens and base components are used instead of hardcoded styles.
- [ ] WCAG 2.1 AA keyboard, label, focus, and color checks pass.
- [ ] Component communication avoids global DOM and Pub/Sub shortcuts.
- [ ] Visualforce postbacks use `<apex:form>` and view state stays under `135 KB`.
- [ ] Jest tests cover render, Apex success, event dispatch, and Apex failure paths where applicable.

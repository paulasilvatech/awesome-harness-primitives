---
paths:
  - force-app/main/default/lwc/**
---

<!-- Generated from harness/github-copilot/instructions/lwc.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Lightning Web Components conventions for Salesforce component structure, SLDS, reactivity, data access, events, accessibility, performance, and tests.

# LWC Conventions — Salesforce Lightning Components

These instructions apply to Lightning Web Components under `force-app/main/default/lwc/**`. They are authoritative for LWC folder structure, Lightning base component usage, SLDS styling, scoped CSS, reactivity, events, wire services, error handling, conditional rendering, accessibility, performance, and Jest tests; Salesforce platform rules, org metadata requirements, and project-specific Salesforce conventions win where they are stricter.

## General Instructions

- Each LWC should reside in its own folder under `force-app/main/default/lwc/`.
- The folder name should match the component name (e.g., `myComponent` folder for the `myComponent` component).
- Each component folder should contain the following files:
    - `myComponent.html`: The HTML template file.
    - `myComponent.js`: The JavaScript controller file.
    - `myComponent.js-meta.xml`: The metadata configuration file.
    - Optional: `myComponent.css` for component-specific styles.
    - Optional: `myComponent.test.js` for Jest unit tests.

## Core Principles

### 1. Use Lightning Components Over HTML Tags
Always prefer Lightning Web Component library components over plain HTML elements for consistency, accessibility, and future-proofing.

#### Recommended Approach
```html
<!-- Use Lightning components -->
<lightning-button label="Save" variant="brand" onclick={handleSave}></lightning-button>
<lightning-input type="text" label="Name" value={name} onchange={handleNameChange}></lightning-input>
<lightning-combobox label="Type" options={typeOptions} value={selectedType}></lightning-combobox>
<lightning-radio-group name="duration" label="Duration" options={durationOptions} value={duration} type="radio"></lightning-radio-group>
```

#### Avoid Plain HTML
```html
<!-- Avoid these -->
<button onclick={handleSave}>Save</button>
<input type="text" onchange={handleNameChange} />
<select onchange={handleTypeChange}>
    <option value="option1">Option 1</option>
</select>
```

### 2. Lightning Component Mapping Guide

| HTML Element | Lightning Component | Key Attributes |
|--------------|-------------------|----------------|
| `<button>` | `<lightning-button>` | `variant`, `label`, `icon-name` |
| `<input>` | `<lightning-input>` | `type`, `label`, `variant` |
| `<select>` | `<lightning-combobox>` | `options`, `value`, `placeholder` |
| `<textarea>` | `<lightning-textarea>` | `label`, `max-length` |
| `<input type="checkbox">` | `<lightning-input type="checkbox">` | `checked`, `label` |
| `<input type="radio">` | `<lightning-radio-group>` | `options`, `type`, `name` |
| `<input type="toggle">` | `<lightning-input type="toggle">` | `checked`, `variant` |
| Custom pills | `<lightning-pill>` | `label`, `name`, `onremove` |
| Icons | `<lightning-icon>` | `icon-name`, `size`, `variant` |

### 3. Lightning Design System Compliance

#### Use SLDS Utility Classes
Always use Salesforce Lightning Design System utility classes with the `slds-var-` prefix for modern implementations:

```html
<!-- Spacing -->
<div class="slds-var-m-around_medium slds-var-p-top_large">
    <div class="slds-var-m-bottom_small">Content</div>
</div>

<!-- Layout -->
<div class="slds-grid slds-wrap slds-gutters_small">
    <div class="slds-col slds-size_1-of-2 slds-medium-size_1-of-3">
        <!-- Content -->
    </div>
</div>

<!-- Typography -->
<h2 class="slds-text-heading_medium slds-var-m-bottom_small">Section Title</h2>
<p class="slds-text-body_regular">Description text</p>
```

#### SLDS Component Patterns
```html
<!-- Card Layout -->
<article class="slds-card slds-var-m-around_medium">
    <header class="slds-card__header">
        <h2 class="slds-text-heading_small">Card Title</h2>
    </header>
    <div class="slds-card__body slds-card__body_inner">
        <!-- Card content -->
    </div>
    <footer class="slds-card__footer">
        <!-- Card actions -->
    </footer>
</article>

<!-- Form Layout -->
<div class="slds-form slds-form_stacked">
    <div class="slds-form-element">
        <lightning-input label="Field Label" value={fieldValue}></lightning-input>
    </div>
</div>
```

### 4. Avoid Custom CSS

#### Use SLDS Classes
```html
<!-- Color and theming -->
<div class="slds-theme_success slds-text-color_inverse slds-var-p-around_small">
    Success message
</div>

<div class="slds-theme_error slds-text-color_inverse slds-var-p-around_small">
    Error message
</div>

<div class="slds-theme_warning slds-text-color_inverse slds-var-p-around_small">
    Warning message
</div>
```

#### Avoid Custom CSS (Anti-Pattern)
```css
/* Don't create custom styles that override SLDS */
.custom-button {
    background-color: red;
    padding: 10px;
}

.my-special-layout {
    display: flex;
    justify-content: center;
}
```

#### When Custom CSS is Necessary
If you must use custom CSS, follow these guidelines:
- Use CSS custom properties (design tokens) when possible
- Prefix custom classes to avoid conflicts
- Never override SLDS base classes

```css
/* Custom CSS example */
.my-component-special {
    border-radius: var(--lwc-borderRadiusMedium);
    box-shadow: var(--lwc-shadowButton);
}
```

### 5. Component Architecture Best Practices

#### Reactive Properties
```javascript
import { LightningElement, track, api } from 'lwc';

export default class MyComponent extends LightningElement {
    // Use @api for public properties
    @api recordId;
    @api title;

    // Primitive properties (string, number, boolean) are automatically reactive
    // No decorator needed - reassignment triggers re-render
    simpleValue = 'initial';
    count = 0;

    // Computed properties
    get displayName() {
        return this.name ? `Hello, ${this.name}` : 'Hello, Guest';
    }

    // @track is NOT needed for simple property reassignment
    // This will trigger reactivity automatically:
    handleUpdate() {
        this.simpleValue = 'updated'; // Reactive without @track
        this.count++; // Reactive without @track
    }

    // @track IS needed when mutating nested properties without reassignment
    @track complexData = {
        user: {
            name: 'John',
            preferences: {
                theme: 'dark'
            }
        }
    };

    handleDeepUpdate() {
        // Requires @track because we're mutating a nested property
        this.complexData.user.preferences.theme = 'light';
    }

    // BETTER: Avoid @track by using immutable patterns
    regularData = {
        user: {
            name: 'John',
            preferences: {
                theme: 'dark'
            }
        }
    };

    handleImmutableUpdate() {
      // No @track needed - we're creating a new object reference
      this.regularData = {
        ...this.regularData,
        user: {
          ...this.regularData.user,
          preferences: {
            ...this.regularData.user.preferences,
            theme: 'light'
          }
        }
      };
    }

    // Arrays: @track is needed only for mutating methods
    @track items = ['a', 'b', 'c'];

    handleArrayMutation() {
      // Requires @track
      this.items.push('d');
      this.items[0] = 'z';
    }

    // BETTER: Use immutable array operations
    regularItems = ['a', 'b', 'c'];

    handleImmutableArray() {
      // No @track needed
      this.regularItems = [...this.regularItems, 'd'];
      this.regularItems = this.regularItems.map((item, idx) =>
        idx === 0 ? 'z' : item
      );
    }

    // Use @track only for complex objects/arrays when you mutate nested properties.
    // For example, updating complexObject.details.status without reassigning complexObject.
    @track complexObject = {
      details: {
        status: 'new'
      }
    };
}
```

#### Event Handling Patterns
```javascript
// Custom event dispatch
handleSave() {
    const saveEvent = new CustomEvent('save', {
        detail: {
            recordData: this.recordData,
            timestamp: new Date()
        }
    });
    this.dispatchEvent(saveEvent);
}

// Lightning component event handling
handleInputChange(event) {
    const fieldName = event.target.name;
    const fieldValue = event.target.value;

    // For lightning-input, lightning-combobox, etc.
    this[fieldName] = fieldValue;
}

handleRadioChange(event) {
    // For lightning-radio-group
    this.selectedValue = event.detail.value;
}

handleToggleChange(event) {
    // For lightning-input type="toggle"
    this.isToggled = event.detail.checked;
}
```

### 6. Data Handling and Wire Services

#### Use @wire for Data Access
```javascript
import { getRecord } from 'lightning/uiRecordApi';
import { getObjectInfo } from 'lightning/uiObjectInfoApi';

const FIELDS = ['Account.Name', 'Account.Industry', 'Account.AnnualRevenue'];

export default class MyComponent extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    record;

    @wire(getObjectInfo, { objectApiName: 'Account' })
    objectInfo;

    get recordData() {
        return this.record.data ? this.record.data.fields : {};
    }
}
```

### 7. Error Handling and User Experience

#### Implement Proper Error Boundaries
```javascript
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class MyComponent extends LightningElement {
    isLoading = false;
    error = null;

    async handleAsyncOperation() {
        this.isLoading = true;
        this.error = null;

        try {
            const result = await this.performOperation();
            this.showSuccessToast();
        } catch (error) {
            this.error = error;
            this.showErrorToast(error.body?.message || 'An error occurred');
        } finally {
            this.isLoading = false;
        }
    }

    performOperation() {
        // Developer-defined async operation
    }

    showSuccessToast() {
        const event = new ShowToastEvent({
            title: 'Success',
            message: 'Operation completed successfully',
            variant: 'success'
        });
        this.dispatchEvent(event);
    }

    showErrorToast(message) {
        const event = new ShowToastEvent({
            title: 'Error',
            message: message,
            variant: 'error',
            mode: 'sticky'
        });
        this.dispatchEvent(event);
    }
}
```

### 8. Performance Optimization

#### Conditional Rendering
Prefer `lwc:if`, `lwc:elseif` and `lwc:else` for conditional rendering (API v58.0+). Legacy `if:true` / `if:false` are still supported but should be avoided in new components.

```html
<!-- Use template directives for conditional rendering -->
<template lwc:if={isLoading}>
    <lightning-spinner alternative-text="Loading..."></lightning-spinner>
</template>
<template lwc:elseif={error}>
    <div class="slds-theme_error slds-text-color_inverse slds-var-p-around_small">
        {error.message}
    </div>
</template>
<template lwc:else>
    <template for:each={items} for:item="item">
        <div key={item.id} class="slds-var-m-bottom_small">
            {item.name}
        </div>
    </template>
</template>
```

```html
<!-- Legacy approach (avoid in new components) -->
<template if:true={isLoading}>
    <lightning-spinner alternative-text="Loading..."></lightning-spinner>
</template>
<template if:true={error}>
    <div class="slds-theme_error slds-text-color_inverse slds-var-p-around_small">
        {error.message}
    </div>
</template>
<template if:false={isLoading}>
  <template if:false={error}>
    <template for:each={items} for:item="item">
        <div key={item.id} class="slds-var-m-bottom_small">
            {item.name}
        </div>
    </template>
  </template>
</template>
```

### 9. Accessibility Best Practices

#### Use Proper ARIA Labels and Semantic HTML
```html
<!-- Use semantic structure -->
<section aria-label="Product Selection">
    <h2 class="slds-text-heading_medium">Products</h2>

    <lightning-input
        type="search"
        label="Search Products"
        placeholder="Enter product name..."
        aria-describedby="search-help">
    </lightning-input>

    <div id="search-help" class="slds-assistive-text">
        Type to filter the product list
    </div>
</section>
```

## Common Anti-Patterns to Avoid
- **Direct DOM Manipulation**: Never use `document.querySelector()` or similar
- **jQuery or External Libraries**: Avoid non-Lightning compatible libraries
- **Inline Styles**: Use SLDS classes instead of `style` attributes
- **Global CSS**: All styles should be scoped to the component
- **Hardcoded Values**: Use custom labels, custom metadata, or constants
- **Imperative API Calls**: Prefer `@wire` over imperative `import` calls when possible
- **Memory Leaks**: Always clean up event listeners in `disconnectedCallback()`


## Good / Bad Examples

The examples below illustrate Lightning base components, SLDS utility classes, and modern conditional rendering.

**Good:**

```html
<template lwc:if={isLoading}>
    <lightning-spinner alternative-text="Loading..."></lightning-spinner>
</template>
<template lwc:else>
    <lightning-input label="Name" value={name} onchange={handleNameChange}></lightning-input>
    <lightning-button label="Save" variant="brand" onclick={handleSave}></lightning-button>
</template>
```

Why: The template uses Lightning base components, accessible labels, and `lwc:if` / `lwc:else` instead of legacy directives.

**Bad:**

```html
<input type="text" onchange={handleNameChange} />
<button style="background:red" onclick={handleSave}>Save</button>
<template if:true={isLoading}>Loading</template>
```

Why: The template bypasses Lightning accessibility, uses inline styles instead of SLDS, and relies on legacy conditional rendering.

## Conventions

| Rule | Rationale |
|---|---|
| Keep each component in its own folder under `force-app/main/default/lwc/` with matching `.html`, `.js`, `.js-meta.xml`, optional `.css`, and optional `.test.js` files | Salesforce metadata discovery and Jest tests depend on predictable component structure |
| Prefer Lightning base components such as `lightning-button`, `lightning-input`, `lightning-combobox`, `lightning-radio-group`, `lightning-pill`, and `lightning-icon` | Base components provide Salesforce consistency, accessibility, and future compatibility |
| Use SLDS utility classes with the `slds-var-` prefix and SLDS component patterns before custom CSS | Design System classes keep spacing, layout, typography, and themes consistent |
| Scope any necessary custom CSS, prefix custom classes, use design tokens such as `--lwc-borderRadiusMedium`, and never override SLDS base classes | Component styles stay isolated and theme-compatible |
| Use `@api` for public properties and prefer immutable reassignment over `@track` for nested data and arrays | Reactivity stays explicit and rerenders remain predictable |
| Use CustomEvent `detail` payloads and read `event.detail.value` or `event.detail.checked` for Lightning inputs | Events remain consistent across parent-child and base component interactions |
| Prefer `@wire` with UI API adapters such as `getRecord` and `getObjectInfo` for Salesforce data access | Wire services manage lifecycle, caching, and reactive parameters |
| Show loading, success, and sticky error toasts with `ShowToastEvent` around async work | Users receive feedback and failed operations remain visible |
| Use `lwc:if`, `lwc:elseif`, and `lwc:else` for API v58.0+ conditional rendering | New templates avoid legacy `if:true` / `if:false` complexity |
| Use semantic HTML, labels, ARIA helpers, and keyboard-operable Lightning components | LWC output remains accessible on the Salesforce Platform |

## Do / Do Not

| Do | Do not |
|---|---|
| Use Lightning base components for buttons, inputs, selects, textareas, toggles, pills, and icons | Replace base components with plain HTML controls without a platform reason |
| Use `slds-grid`, `slds-wrap`, `slds-card`, `slds-form`, and `slds-var-*` utilities | Use inline styles or global CSS for standard layout and spacing |
| Reassign objects and arrays immutably to trigger reactivity | Mutate nested properties without `@track` or a new object reference |
| Use `@wire(getRecord, { recordId: '$recordId', fields: FIELDS })` for record data | Prefer imperative API calls when a wire adapter fits |
| Dispatch `ShowToastEvent` for success and error feedback | Swallow errors or leave users without visible state |
| Clean up event listeners in `disconnectedCallback()` | Leave listeners that can leak memory |
| Use `lwc:if` / `lwc:elseif` / `lwc:else` in new components | Add legacy `if:true` / `if:false` templates to new code |
| Use custom labels, custom metadata, or constants for configurable values | Hard-code user-facing strings, org-specific values, or magic constants |

## Checklist Before Opening a PR

- [ ] Each LWC folder and file name matches the component name under `force-app/main/default/lwc/`.
- [ ] Required `.html`, `.js`, and `.js-meta.xml` files exist, with optional `.css` and `.test.js` only when needed.
- [ ] Lightning base components are used instead of plain controls wherever they fit.
- [ ] SLDS utilities and component patterns provide layout, spacing, typography, and themes before custom CSS.
- [ ] Custom CSS is scoped, prefixed, token-based, and does not override SLDS base classes.
- [ ] Public API, reactive state, `@track`, immutable updates, events, and wire services follow LWC conventions.
- [ ] Async operations expose loading, success, and error states with `ShowToastEvent` where appropriate.
- [ ] Conditional rendering uses `lwc:if`, `lwc:elseif`, and `lwc:else` for new API v58.0+ components.
- [ ] Accessibility labels, semantic regions, ARIA helpers, and keyboard behavior are verified.
- [ ] Jest tests cover behavior when `.test.js` is present or when component logic changes.

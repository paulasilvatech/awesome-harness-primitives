---
applyTo: "**/*.{ts,tsx,js,jsx,json,less,css}"
description: "Enforces Power BI custom visual conventions for pbiviz projects, TypeScript, React, D3, formatting models, interactivity, testing, performance, and packaging."
---

# Power BI Custom Visuals Conventions — Visual Framework and Web Rendering

These instructions apply to TypeScript, JavaScript, JSON, LESS, and CSS files that implement Microsoft Power BI custom visuals. They are authoritative for `pbiviz` project shape, Power BI visual lifecycle code, TypeScript configuration, React and D3 integration, formatting panes, selections, tooltips, landing pages, tests, and rendering performance in matched files; broader project security, accessibility, package-management, and release primitives win where they define stricter rules.

## Project Initialization and Configuration

Use the Power BI custom visuals toolchain instead of hand-assembling a visual package.

| Concern | Convention |
| --- | --- |
| Tooling | Install with `npm install -g powerbi-visuals-tools`, scaffold with `pbiviz new MyCustomVisual`, and run locally with `pbiviz start`. |
| API package | Import the visual API from `powerbi-visuals-api`; keep API aliases explicit so lifecycle signatures remain readable. |
| Source entry | Keep the visual entry at `src/visual.ts`; import visual styles from `style/visual.less`. |
| TypeScript target | Configure `jsx: "react"`, `types: ["react", "react-dom"]`, `allowJs: false`, `emitDecoratorMetadata: true`, `experimentalDecorators: true`, `target: "es6"`, `sourceMap: true`, `moduleResolution: "node"`, and `declaration: true`. |
| Compiler output | Use `outDir: "./.tmp/build/"`; the token `tmp/build/` identifies the generated build folder and must not be treated as source. |
| Libraries | Include `lib: ["es2015", "dom"]` for browser and ES2015 APIs. |

## Visual Lifecycle and Data Views

Every visual class implements `IVisual` and treats `update` as an idempotent render request driven by `VisualUpdateOptions`.

| API | Convention |
| --- | --- |
| `VisualConstructorOptions` | Read `options.element` into a private `HTMLElement` such as `target` or `element`; read `options.host` into `IVisualHost` when selections, colors, events, or tooltips are needed. |
| `VisualUpdateOptions` | Read `options.dataViews[0]`, check for missing data, and use `options.viewport.width` and `options.viewport.height` for layout. |
| `DataView` | Guard absent `dataView`, `dataView.single`, `dataView.categorical`, `categorical.categories[0]`, and `categorical.values[0]` before rendering. |
| `DataViewSingle` | Use `singleDataView.value.toString()` only after checking `singleDataView` and `singleDataView.value`. |
| `getFormattingModel()` | Return `this.formattingSettingsService.buildFormattingModel(this.formattingSettings)` when the visual exposes modern formatting pane settings. |

Keep update methods short. Transform Power BI `DataView` objects into visual-specific models before rendering React components or D3 selections.

## React Visual Integration

Use React only for component UI and keep Power BI host interactions in the visual wrapper.

| Pattern | Convention |
| --- | --- |
| Imports | Use `import * as React from "react"` and `import * as ReactDOM from "react-dom"`; the `react-dom` dependency owns mounting. |
| Root component | Create a `React.ComponentElement<any, any>` from `React.createElement(ReactCircleCard, props)` and render it into `options.element` with `ReactDOM.render`. |
| Component file | Import components from `src/component`; keep CSS classes such as `react-circle-card` and `data-point` stable for styling and tests. |
| Props | Define `ReactCircleCardProps` with arrays such as `data: number[]`, `categories: string[]`, and optional `size` and `color`. |
| Data parsing | Use `dataView.categorical?.values?.[0]?.values || []` and `dataView.categorical?.categories?.[0]?.values || []` to create props only after `dataView` exists. |
| Rendering edge cases | Handle empty `data` and empty `categories` without throwing; avoid `Math.max(...data)` and `Math.min(...data)` when arrays may be empty. |

## D3 Rendering and Data Joins

Use D3 for scalable SVG rendering, transitions, and data joins; keep selections typed and update-friendly.

| D3 element | Convention |
| --- | --- |
| Selection type | Define `type Selection<T extends d3.BaseType> = d3.Selection<T, any, any, any>` when using typed D3 selections. |
| SVG root | Create an `svg` with class `visual-svg`, then append a `g` with class `visual-container`. |
| Scales | Use `d3.scaleBand().domain(...).range([0, width]).padding(0.1)` and `d3.scaleLinear().domain([0, d3.max(data, d => d.value)]).range([height, 0])`; handle undefined maxima. |
| Data join | Use `selectAll('.bar').data(data)`, `enter().append('rect')`, `merge(bars)`, and `exit().remove()` so repeated updates converge. |
| Bar attributes | Set `x`, `y`, `width`, `height`, and `fill` from transformed data; protect `xScale(d.category)` and `yScale(d.value)` from undefined values. |
| Interactive circles | Use `.data-circle` elements, `cx`, `cy`, `r`, `fill`, `stroke`, and `stroke-width`; preserve template strings such as `${d.strokeWidth}px`. |

Do not append new SVG roots on every `update`. Create long-lived containers in the constructor and update attributes and data-bound elements in place.

Preserve `${d.strokeWidth}px` when documenting D3 stroke-width template strings.

## Formatting, Interactivity, Dialogs, and Tooltips

Use supported Power BI utility packages for formatting, selection, color, and tooltips.

| Feature | Convention |
| --- | --- |
| Formatting model | Import `formattingSettings` from `powerbi-visuals-utils-formattingmodel`; extend `formattingSettings.CompositeFormattingSettingsModel`, define `formattingSettings.SimpleCard[]`, and create cards such as `ColorCardSettings`, `DataPointCardSettings`, and `GeneralCardSettings`. |
| Formatting controls | Use `formattingSettings.ColorPicker` with `name: "defaultColor"`, `displayName: "Default color"`, and `value: { value: "#3498db" }`; use `formattingSettings.ToggleSwitch` for boolean options such as `showAllDataPoints`. |
| Selections | Import `interactivitySelectionService` and `baseBehavior` from `powerbi-visuals-utils-interactivityutils`; model `VisualDataPoint extends interactivitySelectionService.SelectableDataPoint` with `value`, `category`, `color`, and `selectionId: ISelectionId`. |
| Selection manager | Create `ISelectionManager` with `this.host.createSelectionManager()`; call `this.selectionManager.select(d.selectionId, event.ctrlKey)` for click selection. |
| Behavior | Extend `baseBehavior.BaseBehavior<VisualDataPoint>` and implement `bindClick()` plus `bindContextMenu()` with `handleSelection`, `handleClearSelection`, and `handleContextMenu`. |
| Dialogs | Use `DialogConstructorOptions`, `DialogAction.Save`, `DialogAction.Cancel`, `DialogUtils.closeDialog(action, data)`, and a React `DialogContent` rendered into the supplied dialog container. |
| Conditional formatting | Use `ColorHelper` from `powerbi-visuals-utils-colorutils` with `options.host.colorPalette`, `{ objectName: "dataPoint", propertyName: "fill" }`, and default `"#3498db"`. |
| Tooltips | Use `createTooltipServiceWrapper`, `ITooltipServiceWrapper`, and `TooltipEventArgs<VisualDataPoint>` from `powerbi-visuals-utils-tooltiputils`; include fields such as `Category`, `Value`, and `Percentage`. |

For tooltip strings, keep formatting deterministic and preserve examples such as `${d.category}: ${d.value}` and `${((dataPoint.value / this.totalValue) * 100).toFixed(1)}%` when documenting category/value and percentage content.

## Visual API and Example Name Inventory

Preserve framework and example identifiers that Power BI developers search for when applying these conventions.

| Identifier | Convention |
| --- | --- |
| `VisualFormattingSettingsModel`, `FormattingModel`, `ColorCardSettings`, `DataPointCardSettings`, `GeneralCardSettings` | Use these names around formatting pane models and return `powerbi.visuals.FormattingModel` from `getFormattingModel()`. |
| `VisualBehavior`, `AdvancedD3Visual`, `OptimizedVisual`, `CustomDialog` | Use these names for examples covering behavior binding, D3 interaction, queued rendering, and dialog integration. |
| `HandleLandingPage`, `SampleLandingPage`, `LandingPage`, `LandingPageRemoved` | Keep landing-page code and tests aligned with the existing naming pattern when refactoring. |
| `PrimitiveValue`, `ISelectionId`, `ISelectionManager`, `IVisualHost`, `IViewport` | Keep Power BI host types explicit in data points, selections, and test hosts. |
| `React.FC` | Use for function component examples when the project already uses React type aliases; typed props remain required either way. |
| `MouseEvent` and `KeyboardEvent` | Use native DOM events in `VisualTestUtils.d3Click` and `VisualTestUtils.d3KeyEvent` helpers. |

## Landing Page and Empty Data States

Render an explicit landing page when no data roles are populated and remove it once data appears.

| State | Convention |
| --- | --- |
| Empty metadata | Check `!options.dataViews || !options.dataViews[0]?.metadata?.columns?.length` before showing onboarding content. |
| Landing flags | Track `isLandingPageOn`, `LandingPageRemoved`, and `LandingPage` consistently so the landing page is not appended repeatedly. |
| DOM shape | Create a `landing-page` wrapper containing `landing-page-content`, a heading, an instruction such as "Add data to get started", and a `landing-page-icon`. |
| Removal | Call `this.LandingPage.remove()` once when data becomes available. |

## Test Harness and Component Tests

Use the established webpack, Jest, Testing Library, and Power BI test utility patterns.

| Test concern | Convention |
| --- | --- |
| Webpack | Use `devtool: 'source-map'`, `mode: 'development'`, `ts-loader` for `.tsx?`, `json-loader` for `.json`, and `coverage-istanbul-loader` with `enforce: 'post'` on `src`. |
| Generated test output | Write webpack test output to `.tmp/test`; the token `tmp/test` marks generated output. |
| Externals | Set `"powerbi-visuals-api": '{}'` and use `webpack.ProvidePlugin({ 'powerbi-visuals-api': null })` for tests that mock the host API. |
| Resolve | Resolve `['.tsx', '.ts', '.js', '.css']`. |
| DOM testing | Use `@testing-harness/github-copilot/react`, `@testing-harness/github-copilot/jest-dom`, `render`, `screen`, `toBeInTheDocument`, `querySelectorAll`, `toHaveLength`, `toHaveStyle`, and `toBeNull`. |
| Visual utilities | Keep `VisualTestUtils.d3Click`, `VisualTestUtils.d3KeyEvent`, `createVisualHost`, and `createUpdateOptions` available for host-level tests. |
| Host mocks | Mock `SelectionIdBuilder`, `SelectionManager`, `ColorPalette`, `EventService`, `TooltipService`, `IViewport`, `VisualDataChangeOperationKind.Create`, and `VisualUpdateType.Data`. |

## Performance and Data Reduction

Reduce data before rendering and schedule expensive work carefully.

| Pattern | Convention |
| --- | --- |
| Capabilities data reduction | In `dataViewMappings`, use `categorical`, `categories`, `for: { in: "category" }`, `dataReductionAlgorithm.window.count: 300`, `values.group.by: "series"`, `select.for.in: "measure"`, and `dataReductionAlgorithm.top.count: 100` when visuals cannot render unlimited points. |
| Render queue | Use `requestAnimationFrame`, `animationFrameId`, and a `renderQueue` when multiple updates arrive faster than the browser can paint. |
| Change detection | Compare transformed data before rerendering; if using `JSON.stringify`, document that the data size is bounded by reduction settings. |
| D3 update pattern | Reuse selections and remove exits rather than clearing the entire SVG. |
| React update pattern | Recreate props and rerender the React root only when parsed Power BI data or formatting settings changed. |

## Good / Bad Examples

The examples below illustrate update-safe rendering.

**Good:**

```typescript
public update(options: VisualUpdateOptions): void {
    const dataView: DataView | undefined = options.dataViews?.[0];

    if (!dataView?.categorical?.categories?.[0] || !dataView.categorical.values?.[0]) {
        this.showLandingPage(options);
        return;
    }

    const dataPoints = this.transformData(dataView);
    this.renderChart(dataPoints, options.viewport.width, options.viewport.height);
}
```

Why: The visual validates the `DataView`, handles the empty state, transforms data before rendering, and uses viewport dimensions from Power BI.

**Bad:**

```typescript
public update(options: VisualUpdateOptions): void {
    const values = options.dataViews[0].categorical.values[0].values;
    d3.select(this.target).append("svg");
    ReactDOM.render(React.createElement(ReactCircleCard, { data: values }), this.target);
}
```

Why: The visual assumes data exists, appends a new SVG on every update, mixes D3 and React ownership of the same target, and bypasses explicit parsing and empty-state handling.

## Conventions

| Rule | Rationale |
|---|---|
| Use `powerbi-visuals-tools`, `pbiviz new`, `pbiviz start`, `powerbi-visuals-api`, `src/visual.ts`, and `style/visual.less` | The visual stays compatible with the Power BI packaging and host lifecycle |
| Implement `IVisual` with guarded constructor and `update` logic using `VisualConstructorOptions`, `VisualUpdateOptions`, `DataView`, and viewport dimensions | Host-driven updates do not crash on missing data or resize-only events |
| Keep React components behind typed props and render them through `ReactDOM.render` from the wrapper visual | React remains a presentation layer, not the owner of Power BI host services |
| Use D3 typed selections, stable SVG containers, and enter/merge/exit data joins | Repeated updates converge without duplicated DOM nodes |
| Use utility packages for formatting, selections, colors, interactivity, and tooltips | The visual behaves consistently with Power BI expectations |
| Show a landing page when no data roles are assigned | Users receive a clear setup state instead of a blank visual |
| Test with webpack, Jest, Testing Library, and mocked Power BI host services | Rendering, interactivity, and formatting behavior fail before packaging |
| Use data reduction, `requestAnimationFrame`, and bounded change detection for large datasets | Visuals remain responsive inside Power BI reports |

## Do / Do Not

| Do | Do not |
|---|---|
| Guard every access to `options.dataViews[0]`, `dataView.single`, and `dataView.categorical` | Assume Power BI always supplies populated data views |
| Transform `DataView` into `VisualDataPoint` or component props before rendering | Bind raw Power BI objects directly throughout React or D3 code |
| Reuse `visual-svg`, `visual-container`, `.bar`, and `data-circle` selections | Append new root DOM nodes on every `update` |
| Use `ISelectionManager`, `ISelectionId`, and utility behaviors for selection and context menus | Implement host selection state with ad hoc CSS classes only |
| Use `ColorHelper`, formatting cards, and `getFormattingModel()` for user-configurable appearance | Hardcode colors and settings that should appear in the formatting pane |
| Add tooltips with `createTooltipServiceWrapper` | Build unmanaged HTML-only tooltips that ignore Power BI services |
| Keep generated `.tmp/build/` and `.tmp/test` output out of source review | Treat generated build and test output as authored code |
| Use `dataReductionAlgorithm` limits and render queues for large visuals | Let unbounded categories, series, or synchronous renders freeze reports |

## Checklist Before Opening a PR

- [ ] The project uses `powerbi-visuals-tools`, `powerbi-visuals-api`, `src/visual.ts`, and `style/visual.less` with the expected TypeScript compiler options.
- [ ] `IVisual` constructor and `update` code guard missing `DataView`, `DataViewSingle`, categorical categories, categorical values, and viewport changes.
- [ ] React components have typed props, handle empty arrays, and keep host service access in the visual wrapper.
- [ ] D3 code uses typed selections, stable containers, scale guards, and enter/merge/exit joins.
- [ ] Formatting model, color, selection, context menu, dialog, and tooltip code use supported Power BI utility packages.
- [ ] Landing page code handles empty metadata and removes the `landing-page` once data exists.
- [ ] Tests cover React rendering, empty data, Power BI host utilities, selection events, and update options.
- [ ] Performance-sensitive visuals define data reduction limits and avoid unnecessary rerenders.
- [ ] Generated `.tmp/build/`, `.tmp/test`, and dependency folders such as `node_modules` are not edited as source.
- [ ] No unrelated edits, relative primitive links, or leftover placeholders remain.

---
name: react19-source-patterns
description: >-
  Apply React 19 source-file migration patterns for root APIs, hydration, unmounting, findDOMNode,
  forwardRef, defaultProps, useRef initial values, legacy context, string refs, propTypes
  comments, and unused React imports. Use this skill when fixing React 19 source migration issues.
---

<!-- Generated from harness/github-copilot/skills/react19-source-patterns/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# React 19 source migration patterns

Migrate React source files away from React 19 removed and changed APIs by choosing the right before/after pattern, preserving behavior, and summarizing the code-level transformations.

Keep `createRef()` available for class component refs, and migrate provider/consumer pairs together for legacy context.

## When to invoke

- "Fix React 19 source migration issues."
- "Convert ReactDOM.render to createRoot."
- "Replace findDOMNode and string refs for React 19."
- "Modernize forwardRef and useRef for React 19."
- "Handle defaultProps and propTypes during React 19 migration."

## Quick reference table

| Pattern | Action | Reference |
| --- | --- | --- |
| `ReactDOM.render(...)` | Replace with `createRoot().render()`. | `references/api-migrations.md` |
| `ReactDOM.hydrate(...)` | Replace with `hydrateRoot(...)`. | `references/api-migrations.md` |
| `unmountComponentAtNode` | Replace with `root.unmount()`. | Inline fix; keep or introduce a saved root reference. |
| `ReactDOM.findDOMNode` | Replace with a direct ref. | Inline fix; refactor class components to hold DOM refs. |
| `forwardRef(...)` wrapper | Prefer ref as direct prop when targeting React 19. | `references/api-migrations.md` |
| `Component.defaultProps = {}` | Replace function component defaults with ES6 default params. | `references/api-migrations.md` |
| `useRef()` no arg | Replace with `useRef(null)`. | Inline fix: add `null`. |
| Legacy Context | Replace `contextTypes`, `childContextTypes`, and `getChildContext` with `createContext`. | `references/api-migrations.md#legacy-context` |
| String refs `this.refs.x` | Replace with `React.createRef()` or callback refs. | `references/api-migrations.md#string-refs` |
| `import React from 'react'` unused | Remove only when no `React.` usage remains in the file. | Verify per file. |

## Source migration rules

| API or pattern | Correct React 19 replacement | Verification |
| --- | --- | --- |
| `ReactDOM.render(<App />, el)` | `import { createRoot } from 'react-dom/client'; const root = createRoot(el); root.render(<App />);` | Confirm the root is created once per container. |
| `ReactDOM.hydrate(<App />, el)` | `import { hydrateRoot } from 'react-dom/client'; hydrateRoot(el, <App />);` | Keep server-rendered markup assumptions intact. |
| `unmountComponentAtNode(container)` | Save the root from `createRoot(container)` and call `root.unmount()`. | Refactor ownership if no root reference exists. |
| `findDOMNode(componentRef)` | Attach a direct DOM ref and read `ref.current`. | Avoid replacing it with document queries. |
| `forwardRef` | Accept `ref` as a direct prop for React 19 components. | Preserve `useImperativeHandle` behavior when present. |
| Function `defaultProps` | Use parameter defaults or nullish coalescing. | Preserve `null` versus `undefined` behavior. |
| `useRef()` | `useRef(null)` | Check any TypeScript type expectations. |
| Legacy context | `React.createContext`, provider value, and `useContext` or `static contextType`. | Migrate provider and consumers together. |
| String refs | `React.createRef()` fields or callback refs. | Pair `ref="x"` with `this.refs.x`. |

## PropTypes rule

Do **not** remove `.propTypes` assignments just because React 19 stops running built-in runtime checking. The `prop-types` package still works as a standalone validator and remains useful for documentation and IDE tooling.

Add this comment above any `.propTypes` block that remains:

```jsx
// NOTE: React 19 no longer runs propTypes validation at runtime.
// PropTypes kept for documentation and IDE tooling only.
```

## Progressive disclosure and bundled resources

- `references/api-migrations.md`: complete before/after code for root APIs, `findDOMNode`, `forwardRef` with `useImperativeHandle`, `defaultProps`, `useRef`, legacy context, string refs, and unused React imports.

## Gotchas

- **Do not remove `import React from 'react'` blindly**: keep it when the file uses `React.Component`, `React.createRef`, `React.createContext`, `React.useState`, or any other `React.` API.
- **Class component `defaultProps` needs judgment**: function component defaults are the primary removal target; preserve behavior for classes unless a safe refactor is clear.
- **`useImperativeHandle` remains valid**: only the `forwardRef` wrapper changes when ref becomes a prop.
- **Legacy context is cross-file**: provider and consumer migrations must be coordinated.

## Output template

```markdown
## React 19 source migration result

**Status:** migrated | planned | blocked
**Scope:** `<files or components>`

| File | Pattern | Replacement | Notes |
| --- | --- | --- | --- |
| `<path>` | `ReactDOM.render(...)` | `createRoot().render()` | `<root ownership>` |

### PropTypes
- `<file>`: kept with React 19 note | not present | removed for another justified reason

### Validation
- Migration scan: `<remaining hits or none>`
- Tests/build: `<command and result, or not run>`
```

## Quality gate

- [ ] Every changed API is mapped to the React 19 replacement table above.
- [ ] `references/api-migrations.md` was consulted for non-trivial changes.
- [ ] `.propTypes` assignments are preserved unless there is a separate, explicit reason to remove them.
- [ ] Remaining `import React from 'react'` lines are justified by `React.` usage; removed imports have no `React.` usage.
- [ ] `useRef()` calls in scope now pass an explicit initial value such as `null`.
- [ ] Root API migrations preserve root ownership for later `root.unmount()`.
- [ ] Follow-up scans or tests are reported.

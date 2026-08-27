---
name: react18-string-refs
description: >-
  Migrate React string refs, ref="name" assignments, and this.refs.name access to
  React.createRef(), callback refs, or child ref forwarding. Use this skill when migrating React
  18.3.1 warnings or React 19 removals involving single refs, multiple refs, list refs, callback
  refs, or refs passed to child components.
---

<!-- Generated from harness/github-copilot/skills/react18-string-refs/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# React 18 string refs migration

Convert deprecated React string refs into explicit refs by pairing every `ref="name"` assignment with its `this.refs.name` access, choosing the correct fixed, dynamic, callback, or child-component pattern, and producing a migration summary.

## When to invoke

- "Migrate these React string refs."
- "Fix React 18.3.1 warnings about string refs."
- "Prepare this class component for React 19 refs."
- "Convert this.refs usage to createRef."
- "Handle string refs inside a list."
- "Fix the multiple-refs-in-list migration."

## String ref inventory

String refs use `ref="myInput"` or `ref='myInput'` in JSX and access the node through `this.refs.myInput`. They were deprecated in React 16.3, warn in React 18.3.1, and are removed in React 19.

Run both scans and migrate each pair together:

```bash
# Find all string ref assignments in JSX
grep -rn 'ref="' src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."

# Find all this.refs accessors
grep -rn "this\.refs\." src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."
```

Also scan for single-quoted refs when the codebase uses them:

```bash
grep -rn "ref='" src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."
```

## Migration pattern map

| Pattern | Use when | Required transformation |
| --- | --- | --- |
| Single ref on a DOM element | One class component owns one fixed DOM node. | Add `refName = React.createRef();`, replace `ref="refName"` with `ref={this.refName}`, and replace `this.refs.refName` with `this.refName.current`. |
| Multiple refs in one component | A class has several fixed inputs, buttons, or containers. | Create one `React.createRef()` field per string ref; do not reuse a single ref object. |
| Refs in a list / dynamic refs | A `map()` or loop builds names such as ``ref={`tab_${i}`}``. | Use a `Map` keyed by stable item IDs or a callback ref collection; avoid index-only keys when items can reorder. |
| Callback refs | The component needs attach/detach behavior or a dynamic collection. | Store the DOM node directly, not in `.current`; prefer a stable class field function over an inline callback. |
| Ref passed to a child component | The ref targets a custom component instead of a DOM element. | Update the child too: React 18 needs `forwardRef`; React 19 can receive `ref` as a direct prop. |

Read `references/patterns.md` when implementing the full before/after examples for `single-ref`, `multiple-refs`, `list-refs`, `callback-refs`, and `forwarded-refs`.

## Migration rules

1. Pair every `ref="name"` with every `this.refs.name` usage before editing.
2. Add `refName = React.createRef();` as a class field, or initialize it in the constructor when the project does not use class fields.
3. Replace `ref="refName"` with `ref={this.refName}` in JSX.
4. Replace `this.refs.refName` with `this.refName.current` everywhere.
5. Add null checks such as `this.refName.current?.focus()` when the old code could run before mount or after unmount.
6. For list refs, key the ref collection by the same stable identity used for rendering, such as `tab.id`, not by a transient index unless the list is truly static.
7. For callback refs, remember that `this.tabRefs[i]` is the element itself; do not append `.current`.

## Progressive disclosure and bundled resources

- `references/patterns.md`: complete before/after migrations for single DOM refs, multiple refs, dynamic list refs, callback refs, and child component refs.

## Gotchas

- **Do not migrate only one side**: changing `ref="name"` without changing `this.refs.name`, or the reverse, leaves broken runtime access.
- **Dynamic refs are not fixed refs**: ``ref={`tab_${i}`}`` needs a ref collection, not one `tabRef` field.
- **Callback refs store nodes directly**: `this.inputEl?.focus()` is correct; `this.inputEl.current` is not.
- **Child refs may require child changes**: a ref on `<MyInput />` does not automatically point at the inner `<input>` unless the child forwards or accepts it.

## Output template

```markdown
## React string ref migration

**Status:** migrated | planned | blocked
**Scope:** `<files or component>`

| Component | String refs found | Replacement pattern | Notes |
| --- | --- | --- | --- |
| `<Component>` | `ref="name"`, `this.refs.name` | `React.createRef()` | `<null checks, child changes, or list key>` |

**Validation**
- String ref scan: `<remaining hits or none>`
- `this.refs` scan: `<remaining hits or none>`
- Tests/build: `<command and result, or not run>`
```

## Quality gate

- [ ] Every `ref="name"` or `ref='name'` hit was paired with matching `this.refs.name` access before editing.
- [ ] Fixed refs use distinct `React.createRef()` fields or constructor assignments.
- [ ] Dynamic list refs use a `Map`, object, or callback collection keyed by a stable identity.
- [ ] Callback ref migrations do not incorrectly use `.current`.
- [ ] Child component refs update the child with `forwardRef` for React 18 or direct `ref` prop handling for React 19.
- [ ] `references/patterns.md` was consulted for any non-trivial pattern.
- [ ] Follow-up scans show no remaining string refs in the migrated scope, or remaining hits are explicitly justified.

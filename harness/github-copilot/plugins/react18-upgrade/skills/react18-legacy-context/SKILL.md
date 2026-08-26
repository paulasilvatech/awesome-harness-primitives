---
name: "react18-legacy-context"
description: >-
  Migrate React legacy context API usage from contextTypes, childContextTypes, and getChildContext to modern createContext. Use this skill when touching legacy context in class or function components because provider and every consumer must be updated together to avoid React 18 warnings and React 19 runtime failures.
---

# React 18 legacy context migration

Coordinate the cross-file migration from React legacy context to modern `createContext` by finding the provider, every consumer, the new context module, and verification steps before editing any single file.

## When to invoke

- "Migrate this React legacy context to createContext."
- "Remove contextTypes and childContextTypes from these components."
- "Update getChildContext before React 19."
- "Fix React 18 legacy context warnings."
- "Convert class context consumers to contextType or useContext."

## Migration facts

| Legacy API | Modern replacement | Rule |
| --- | --- | --- |
| `childContextTypes` plus `getChildContext` | A `createContext` object and provider `value`. | Update the provider and exported context together. |
| `contextTypes` on class consumers | `static contextType = SomeContext` for one context, or `<SomeContext.Consumer>` for multiple contexts. | Every consumer must move to the same context object. |
| Function component legacy access | `useContext(SomeContext)`. | Use hooks only in function components. |
| `this.context` usage | Modern `this.context` through `contextType`, or render-prop consumer for multiple contexts. | Audit each usage because it may be legacy or already modern. |

Legacy context was deprecated in React 16.3, warns in React 18.3.1, and is removed in React 19.

## Scan commands

```bash
# Find all providers
grep -rn "childContextTypes\|getChildContext" src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."

# Find all consumers
grep -rn "contextTypes\s*=" src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."

# Find this.context usage (may be legacy or modern - check which)
grep -rn "this\.context\." src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."
```

## Procedure

1. Find the provider by scanning for `childContextTypes` and `getChildContext`.
2. Find all consumers by scanning for `contextTypes` and related `this.context` usage.
3. Create the context file using the standard shape from `references/context-file-template.md`.
4. Update the provider to render the modern context provider with the correct `value`.
5. Update each class consumer to `contextType` or a context consumer, and each function component to `useContext`.
6. Verify the app and confirm no legacy context warnings remain.

## Cross-file coordination rules

| Situation | Required handling |
| --- | --- |
| One legacy context | Use `references/single-context.md` and migrate provider plus all consumers in one change set. |
| Multiple legacy contexts | Use `references/multi-context.md`; avoid assigning multiple `contextType` values to one class. |
| Provider only found | Do not stop after provider migration; consumers will read from the wrong context or `undefined`. |
| Consumer only found | Locate the matching provider before replacing context access. |
| Tests excluded from scan | Exclude `.test.` files in discovery, then update tests only if they instantiate changed components. |

## Progressive disclosure and bundled resources

- `references/single-context.md`: complete migration for one context such as theme or auth, including provider, class consumer, and function consumer.
- `references/multi-context.md`: nested providers and consumers of different contexts.
- `references/context-file-template.md`: standard file structure for a new context module.

## Gotchas

- **This is always a cross-file migration**: migrating only the provider or only consumers causes runtime failure.
- **Class components support only one `contextType`**: use consumers or wrapper components for multiple contexts.
- **`this.context` is ambiguous**: inspect whether it comes from legacy `contextTypes` or modern `contextType` before editing.
- **React 18 warnings are future failures**: React 19 removes the legacy API.

## Output template

```markdown
### React legacy context migration

**Status:** complete | needs consumers | blocked
**Context:** `<context name>`
**Provider:** `<file path>`
**Consumers updated:** `<count>`

| File | Role | Change |
| --- | --- | --- |
| `<path>` | provider | `getChildContext` to provider `value` |
| `<path>` | class consumer | `contextTypes` to `contextType` |
| `<path>` | function consumer | legacy access to `useContext` |

**Validation**
- Provider scan: `<command/result>`
- Consumer scan: `<command/result>`
- React warnings: none | remaining
```

## Quality gate

- [ ] Provider scan for `childContextTypes` and `getChildContext` was run.
- [ ] Consumer scan for `contextTypes` was run.
- [ ] `this.context` usage was audited for legacy versus modern context.
- [ ] A context file was created or reused with `createContext`.
- [ ] Provider and every consumer were updated in the same migration.
- [ ] Class components use `contextType` or consumers; function components use `useContext`.
- [ ] Multiple-context consumers follow `references/multi-context.md` rather than invalid multiple `contextType` assignments.
- [ ] Verification confirms no legacy context warnings remain.

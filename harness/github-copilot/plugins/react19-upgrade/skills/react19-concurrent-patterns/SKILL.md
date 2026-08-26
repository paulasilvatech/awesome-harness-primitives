---
name: "react19-concurrent-patterns"
description: >-
  Preserve React 18 concurrent patterns and adopt React 19 APIs including useTransition, useDeferredValue, Suspense, use(), useOptimistic, useActionState, useFormStatus, and Actions. Use when reviewing React 19 migrations, auditing concurrent rendering, cleaning up Suspense data fetching, or adopting post-migration APIs.
---

# React 19 concurrent patterns

Protect working React 18 concurrent rendering code during migration, then introduce React 19 APIs only after the migration is stable and the application behavior is covered by tests or review.

## When to invoke

- "Review React 19 concurrent patterns before migration."
- "Make sure useTransition and Suspense were not broken."
- "Adopt React 19 Actions after the upgrade."
- "Use React 19 use() for data fetching or context."
- "Audit useDeferredValue, startTransition, and Suspense changes."

## Preserve React 18 patterns

These patterns already work in React 19. Do not rewrite them merely because React changed versions.

| Pattern | Keep | Verify |
| --- | --- | --- |
| Root rendering | `createRoot` from `react-dom/client` | `ReactDOM.render` is gone and `root.render(<React.StrictMode><App /></React.StrictMode>)` still wraps the app if it did before. |
| Transitions | `const [isPending, startTransition] = useTransition();` | Expensive state updates still run inside `startTransition`. |
| Deferred values | `const deferredQuery = useDeferredValue(query);` | The deferred value is still used for expensive children or filtering. |
| Code splitting | `React.lazy(() => import('./LazyComponent'))` with `<Suspense fallback={<Spinner />}>` | Fallback and lazy import boundaries remain in place. |

The createRoot example below is the CORRECT React 19 root shape; preserve it DURING migration unless a separate review approves a concurrent-mode behavior change.

```jsx
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

```jsx
const [isPending, startTransition] = useTransition();

function handleClick() {
  startTransition(() => {
    setFilteredResults(computeExpensiveFilter(input));
  });
}
```

## React 19 adoption map

Adopt these after the migration stabilizes, not during the mechanical upgrade.

| API | Use when | Read first |
| --- | --- | --- |
| `use()` | Components consume a promise or context in React 19-supported patterns. | `references/react19-use.md` |
| Actions | Form submissions or mutations need integrated pending, result, and error handling. | `references/react19-actions.md` |
| `useActionState` | A form action needs state derived from the previous submission result. | `references/react19-actions.md` |
| `useFormStatus` | A submit button or nested component needs pending status from its nearest form. | `references/react19-actions.md` |
| `useOptimistic` | UI should show an optimistic value while a mutation is pending. | `references/react19-actions.md` |
| Suspense data fetching | A component tree should suspend on async data rather than hand-roll loading state. | `references/react19-suspense.md` |

## Migration safety rules

Run a targeted search before and after migration review:

```bash
grep -rn "useTransition\|useDeferredValue\|Suspense\|startTransition" \
  src/ --include="*.js" --include="*.jsx" | grep -v "\.test\."
```

If migration touched these files, review the diff. A mechanical React 19 migration should update API surfaces such as `forwardRef` or `defaultProps`; it should not alter concurrent mode logic without a separate reason and verification.

## Criteria

### Preserve

- [ ] Existing `createRoot` usage remains correct.
- [ ] `useTransition`, `startTransition`, and `isPending` semantics are unchanged unless the user asked for a behavioral refactor.
- [ ] `useDeferredValue` still gates expensive rendering or filtering.
- [ ] `Suspense` fallbacks and `React.lazy` boundaries still cover code-split components.

### Adopt

- [ ] New React 19 APIs are introduced in a post-migration cleanup or explicitly requested refactor.
- [ ] Each new `use()`, Action, `useActionState`, `useFormStatus`, `useOptimistic`, or Suspense data-fetching change has a reason and a validation path.
- [ ] Loading, pending, optimistic, error, and retry behavior remain observable in tests or manual verification.

## Progressive disclosure and bundled resources

| Resource | Use it when |
| --- | --- |
| `references/react19-use.md` | Introducing or reviewing `use()` for promises or context. |
| `references/react19-actions.md` | Introducing Actions, `useActionState`, `useFormStatus`, or `useOptimistic`. |
| `references/react19-suspense.md` | Moving data loading into Suspense patterns. |

## Gotchas

- **Do not combine migration and redesign**: concurrent logic changes should be a separate, reviewable step.
- **Suspense fallback changes are behavior changes**: users may see different loading UI or error boundaries.
- **Optimistic UI needs rollback**: `useOptimistic` must have a clear failure path when the server rejects the action.

## Output template

```markdown
## React 19 concurrent patterns result

**Status:** preserved | adopted | needs review | blocked
**Scope:** <files or components reviewed>

### Preserved patterns
| Pattern | Evidence | Action |
| --- | --- | --- |
| `useTransition` | <file/line or none> | kept | changed with reason |

### React 19 APIs
| API | File | Reason | Validation |
| --- | --- | --- | --- |
| `useOptimistic` | <file> | <why> | <test/manual check> |

### Commands
```bash
<grep or test command>
```
```

## Quality gate

- [ ] Existing React 18 concurrent patterns were searched and reviewed before modification.
- [ ] Migration-only work did not alter `useTransition`, `useDeferredValue`, `Suspense`, or `startTransition` behavior.
- [ ] New React 19 APIs were adopted only when requested or after migration stabilization.
- [ ] The relevant bundled reference was read before adding `use()`, Actions, or Suspense data fetching.
- [ ] The result includes concrete file evidence and validation.

---
description: "Use when building frontend UI components, pages, client interactions, component state, accessibility, and user-facing flows."
applyTo: "frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**"
---

# Frontend Conventions — Component Craft and Interaction

This file activates when you build UI under `frontend/app/**` or `frontend/components/**`. It focuses on component craft, client interaction, component state, accessibility execution, and user-facing flows. It owns how components behave for users; [`frontend-spec.instructions.md`](frontend-spec.instructions.md) owns the platform contract for Next.js 15 App Router, strict TypeScript, Tailwind/shadcn styling, Server Components, and Server Actions — follow that file for those topics and do not restate them here.

> [!NOTE]
> `frontend/` does not exist yet; the team scaffolds it in Stage 3. These are the conventions the components must follow as they are written.

## Component Craft

Build small, single-responsibility components with named exports and typed props. Prefer composition over a growing prop list, and keep presentational components free of data fetching.

```tsx
import type { ResourceDto } from '@/types/resource';

export function ResourceCard({ resource }: { resource: ResourceDto }) {
  return (
    <article className="rounded-lg border p-4">
      <h3 className="font-semibold">{resource.label}</h3>
      <p className="text-muted-foreground">{formatBRL(resource.amount)}</p>
    </article>
  );
}
```

Keep the `'use client'` surface as small as possible: a Server Component fetches the data and passes it to a small Client Component that handles interaction (see [`frontend-spec.instructions.md`](frontend-spec.instructions.md)).

## Component State

Default to local `useState`. Lift state to the nearest common parent when siblings must share it. Reach for Context **only** for genuinely shared client state, and add a state-management library only with an ADR that justifies the dependency.

```tsx
'use client';

import { useState } from 'react';

export function ResourceFilter({ onFilter }: { onFilter: (term: string) => void }) {
  const [term, setTerm] = useState('');
  return (
    <label className="flex flex-col gap-1">
      <span>Filter resources</span>
      <input
        value={term}
        onChange={(event) => { setTerm(event.target.value); onFilter(event.target.value); }}
      />
    </label>
  );
}
```

Inputs are controlled (`value` + `onChange`). Derive values during render instead of mirroring props into state.

## Client Interaction and Async Flows

Mutations go through server actions, not client `fetch` (see [`frontend-spec.instructions.md`](frontend-spec.instructions.md)). Wrap the call in `useTransition` to drive a disabled/pending state, and reflect it with `aria-busy`.

```tsx
'use client';

import { useTransition } from 'react';
import { Button } from '@/components/ui/button';

export function ArchiveButton({ id, onArchive }: { id: string; onArchive: (id: string) => Promise<void> }) {
  const [isPending, startTransition] = useTransition();
  return (
    <Button
      type="button"
      disabled={isPending}
      aria-busy={isPending}
      onClick={() => startTransition(() => onArchive(id))}
    >
      {isPending ? 'Archiving…' : 'Archive'}
    </Button>
  );
}
```

## User-Facing Flows

Every async view renders three explicit states — **loading**, **empty**, and **error** — never a blank screen. Confirm destructive actions, and format money and dates with an explicit locale so output is deterministic.

```tsx
if (isLoading) return <Spinner aria-label="Loading resources" />;
if (resources.length === 0) return <EmptyState message="No resources yet" />;
if (error) return <ErrorState onRetry={refetch} />;
```

## Accessibility (WCAG 2.1 AA)

| Requirement | How to satisfy it |
|---|---|
| Labels | Every input has a `<label htmlFor>` or `aria-label` |
| Keyboard | All interactive elements reachable and operable via Tab/Enter/Space |
| Focus | Move focus into a dialog on open; return it to the trigger on close |
| Contrast | Text ≥ 4.5:1, large text ≥ 3:1 |
| Structure | One `<h1>` per page, logical heading order, landmark regions |
| Color | Never the only signal — pair it with text or an icon |

Use semantic elements (`<button>`, `<nav>`, `<table>`) before reaching for ARIA; add ARIA only when native semantics are missing.

## Conventions

| Rule | Rationale |
|---|---|
| Named exports for components | Consistent imports; tree-shakeable |
| Typed props, no `any` | Failures surface at compile time |
| Local `useState`, Context only when shared | Minimal, predictable state graph |
| Colocate the test beside the component | Behavior and coverage stay together |
| Explicit loading/empty/error states | No dead ends in the UI |

## Do / Do Not

| Do | Do not |
|---|---|
| Push `'use client'` to the smallest leaf | Mark a whole page `'use client'` |
| Mutate through a server action | `fetch` a mutation from the client |
| Label every control | Rely on placeholder text as the label |
| Format money/dates with a locale | Render raw numbers or ISO strings to users |

## Checklist Before Opening a PR

- [ ] Components use named exports and fully typed props
- [ ] `'use client'` is confined to the smallest interactive component
- [ ] Shared state uses Context only when justified; no unapproved state library
- [ ] Async views render loading, empty, and error states
- [ ] Inputs are labeled, keyboard-operable, and meet AA contrast
- [ ] A colocated Testing Library test covers the interaction (see [`tests.instructions.md`](tests.instructions.md))

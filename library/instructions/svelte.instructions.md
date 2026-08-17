---
applyTo: '**/*.svelte,**/*.ts,**/*.js,**/*.css,**/*.scss,**/*.json'
description: 'Enforces Svelte 5 and SvelteKit 2 conventions for runes reactivity, routing, load functions, form actions, remote functions, TypeScript, styling, performance, errors, security, and accessibility.'
---

# Svelte and SvelteKit Conventions — Runes and Full-Stack UI

These instructions apply to Svelte 5.x and SvelteKit 2.x components, routes, scripts, styles, and configuration. They are authoritative for runes-based reactivity, SvelteKit routing, load functions, form actions, remote functions, TypeScript, styling, performance, error handling, security, and accessibility in matched files; project-specific design system, deployment, security, and testing rules win where they are stricter.

## Architecture and Component Design

Use Svelte 5 runes and SvelteKit 2 for full-stack applications with TypeScript, component-scoped styling, progressive enhancement, Vite tooling, and performance-first behavior.

- Use Svelte 5 runes for all reactivity instead of legacy stores.
- Organize components by feature or domain.
- Separate presentation components from logic-heavy components.
- Extract reusable logic into composable functions.
- Compose components with slots, snippets, and children snippets.
- Use SvelteKit file-based routing with proper load functions.
- Use `<script lang="ts">` and TypeScript annotations by default.
- Keep components small, focused, testable, and reusable.
- Use `{#snippet}` blocks for reusable template logic.
- Prefer attachments (`{@attach}`, Svelte 5.29+) over actions (`use:`) for DOM interaction and third-party integration because attachments react to state and compose cleanly.
- Use PascalCase for components and camelCase for functions and variables.
- Document complex components and logic with JSDoc comments.

## Reactivity and State

| Rune or state API | Convention |
| --- | --- |
| `$state()` | Use for reactive local component state. |
| `$derived()` | Use for computed values and expensive calculations. |
| `$derived.by()` | Use for complex computations beyond simple expressions. |
| `$effect()` | Use sparingly for side effects such as analytics, logging, and DOM manipulation; prefer `$derived()` or function bindings for state sync. |
| `$effect.pre()` | Use before DOM updates, such as scroll position handling. |
| `$effect.root()` | Use for manually controlled effects outside component lifecycle. |
| `$effect.tracking()` | Use in abstractions to conditionally create reactive listeners. |
| `untrack()` | Read state without dependencies and prevent loops when reading and writing the same state in effects. |
| `$props()` | Define component props with destructuring and TypeScript annotations. |
| `$bindable()` | Enable two-way data binding between components. |
| Function bindings | Use `bind:value={() => value, (v) => (value = v)}` when a binding must derive or validate the value. |
| Optimistic UI | Override derived values directly for optimistic UI patterns in Svelte 5.25+. |

Use type-safe context with `createContext()` over raw `setContext` and `getContext`. Avoid global `$state` modules for SSR because they can leak data across requests; use context for per-request reactive state. Read SvelteKit app and navigation state from `$app/state` (`page`, `navigating`, `updated`); `$app/stores` is legacy for SvelteKit < 2.12. Keep complex state normalized and persist client-side data deliberately. Remember that async code in effects does not track dependencies after `await`.

## SvelteKit Routing, Data, Forms, and Remote Functions

- Use `+page.svelte` for page components with proper SEO.
- Use `+layout.svelte` for shared layouts and navigation.
- Use `+page.server.ts` for server-side data loading, API calls, and form actions.
- Use `+server.ts` for API endpoints and server-side logic.
- Use load functions for server-side and universal data fetching.
- Implement loading, error, and success states.
- Handle streaming data with promises in server load functions.
- Use `invalidate()` and `invalidateAll()` for cache management.
- Implement optimistic updates, offline handling, and network error handling where user experience requires them.
- Use SvelteKit form actions for server-side form handling.
- Use progressive enhancement with `use:enhance`.
- Use `bind:value` for controlled form inputs.
- Validate data both client-side and server-side.
- Handle file uploads and complex forms with accessible labels and ARIA attributes.

Remote functions are experimental in SvelteKit 2.27+. Use them for type-safe client-server calls that always run on the server only when opt-in flags are enabled: `kit.experimental.remoteFunctions` and `compilerOptions.experimental.async` in `svelte.config.js`. Define remote functions in `.remote.ts` files as `query`, `form`, `command`, or `prerender`; remote files may import `$lib/server` modules for secrets and DB access but must not live inside `src/lib/server`.

```ts
import { query } from '$app/server';
import * as db from '$lib/server/database';

export const getPosts = query(async () => {
  return await db.sql`SELECT title, slug FROM post ORDER BY published_at DESC`;
});
```

Read data with `query` and resolve it directly in markup with `await getPosts()`.

## Styling, Transitions, TypeScript, and Performance

| Area | Convention |
| --- | --- |
| Styling | Use component-scoped `<style>` blocks, CSS custom properties, `class:` directives, BEM or utility-first conventions, mobile-first responsive design, and `:global()` only for truly global styles. |
| Transitions | Use `transition:`, `in:`, `out:`, `animate:` with `flip`, custom transitions, `|local`, and keyed `{#each}` blocks for list animations. |
| TypeScript | Enable strict mode, type props as `let { name }: { name: string } = $props()`, type handlers and refs, use generated `$types.ts`, use generics for reusable components, and run `svelte-check`. |
| Lists | Use keyed `{#each}` blocks for efficient rendering. |
| Lazy loading | Use dynamic `import()`; in Svelte 5 components are dynamic by default, so assign the imported component to a capitalized variable and render `<Component />` without `<svelte:component>` in runes mode. |
| Computation | Use `$derived()` and `$derived.by()` for expensive computations and avoid `$effect()` for derived state. |
| Bundles | Leverage SvelteKit code splitting, preloading, tree shaking, and proper imports. |

## Error Handling, Security, and Accessibility

- Implement `+error.svelte` pages for route-level errors.
- Use `<svelte:boundary>` (Svelte 5.3+) to contain rendering and effect errors, with a `failed` snippet and `reset` or an `onerror` handler.
- Use try/catch in load functions and form actions.
- Provide meaningful error messages and fallback UI.
- Log errors appropriately for debugging.
- Handle validation errors in forms with user feedback.
- Use SvelteKit `error()` and `redirect()` helpers for proper responses.
- With experimental `await` syntax in Svelte 5.36+ and `experimental.async`, show first-render UI with a `<svelte:boundary>` `pending` snippet and later loading states with `$effect.pending()`.
- Sanitize user inputs to prevent XSS.
- Use `@html` carefully and validate HTML content.
- Validate and sanitize data in load functions and form actions.
- Use semantic HTML, proper heading hierarchy, keyboard navigation, ARIA labels/descriptions, color contrast that meets WCAG guidelines, and focus management for dynamic content.

## Good / Bad Examples

The examples below illustrate derived state without effect-based synchronization.

**Good:**

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
</script>

<button onclick={() => count += 1}>{doubled}</button>
```

Why: The computed value is derived directly from state without synchronization effects.

**Bad:**

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $state(0);
  $effect(() => {
    doubled = count * 2;
  });
</script>
```

Why: `$effect()` is being used to synchronize derived state that `$derived()` handles more safely.

## Svelte Compatibility Vocabulary

Preserve Svelte terms `NOTE`, `children`, `component-based`, `cross-request`, `enter/exit`, `high-quality`, `parent-child`, `reading/writing`, `src/routes/blog/data.remote.ts`, and `tsconfig.json` when updating Svelte 5 and SvelteKit 2 guidance.


## Conventions

| Rule | Rationale |
| --- | --- |
| Use runes such as `$state`, `$derived`, `$effect`, `$props`, and `$bindable` instead of legacy stores for component reactivity | Svelte 5 reactivity is built around runes |
| Prefer `$derived()` over `$effect()` for computed values | Effects are for side effects and can create synchronization bugs |
| Use context instead of global `$state` modules for SSR-shared state | Global mutable state can leak across requests |
| Use `+page.server.ts`, `+server.ts`, form actions, and load functions for server work | SvelteKit file conventions keep data boundaries clear |
| Use remote functions only with explicit experimental opt-in | Experimental `query`, `form`, `command`, and `prerender` APIs may change |
| Use strict TypeScript, generated `$types.ts`, and `svelte-check` | Type errors surface before runtime |
| Use keyed `{#each}`, dynamic imports, and code splitting | Rendering and bundle performance stay predictable |
| Use `<svelte:boundary>`, `+error.svelte`, `error()`, and `redirect()` for failures | Errors get proper boundaries and HTTP semantics |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `$derived.by()` for multi-statement computed values | Put derived state synchronization in `$effect()` |
| Use `createContext()` for shared reactive state | Use raw `setContext`/`getContext` when a typed helper fits |
| Read app state from `$app/state` in modern SvelteKit | Use `$app/stores` unless targeting SvelteKit < 2.12 |
| Use `use:enhance` for progressive forms | Replace server actions with client-only form handling |
| Keep remote `.remote.ts` files outside `src/lib/server` | Place remote function files inside `src/lib/server` |
| Render dynamic imports as `<Component />` in runes mode | Use `<svelte:component>` for Svelte 5 dynamic components |
| Validate both client-side and server-side | Trust client-side validation alone |
| Use `@html` only with validated content | Render untrusted HTML directly |

## Checklist Before Opening a PR

- [ ] Components use Svelte 5 runes with `<script lang="ts">` and avoid legacy stores for component reactivity.
- [ ] `$derived()` or `$derived.by()` handles computed state; `$effect()` is reserved for side effects with cleanup where needed.
- [ ] Shared state uses typed context and avoids SSR-leaking global `$state` modules.
- [ ] Routes, layouts, load functions, form actions, API endpoints, and errors use `+page.svelte`, `+layout.svelte`, `+page.server.ts`, `+server.ts`, and `+error.svelte` appropriately.
- [ ] Remote functions are used only with `kit.experimental.remoteFunctions` and `compilerOptions.experimental.async` opt-in, and `.remote.ts` files are outside `src/lib/server`.
- [ ] Forms use `use:enhance`, `bind:value`, validation, accessible labels, and clear success/error states.
- [ ] Styling, transitions, keyed lists, dynamic imports, tree shaking, and preloading follow the conventions above.
- [ ] `svelte-check` and strict TypeScript pass where configured.
- [ ] Security and accessibility checks cover input sanitization, `@html`, semantic HTML, keyboard navigation, ARIA, contrast, and focus management.

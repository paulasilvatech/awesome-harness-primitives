---
applyTo: '**/*.tsx,**/*.ts,**/*.jsx,**/*.js,**/*.css'
description: 'Conventions for Next.js App Router applications with Tailwind CSS, TypeScript, server/client boundaries, styling, state, data fetching, security, and performance.'
---

# Next.js + Tailwind Conventions — App Router UI

These instructions apply to high-quality Next.js application code, React components, JavaScript, TypeScript, JSX, TSX, and CSS files matched by the `applyTo` globs. They are authoritative for App Router structure, Tailwind styling, component state, data fetching, security hygiene, performance, and user-facing UI conventions; project-specific architecture, design-system tokens, and test primitives win where they impose stricter rules.

## Architecture and Component Boundaries

- Use the latest supported Next.js App Router conventions for routing, layouts, loading UI, and error boundaries.
- Prefer React Server Components by default and add `'use client'` only at the smallest interactive boundary.
- Group routes by feature or domain (`feature/domain`) so related pages, layouts, loading states, and errors stay together.
- Implement error boundaries with `error.tsx` where failures need a user-facing recovery path.
- Leverage static optimization where possible; opt into dynamic rendering only when request-time data, headers, cookies, or personalization require it.
- Keep semantic HTML structure in components before styling them with Tailwind utilities.

## TypeScript and Runtime Validation

Use TypeScript as the default safety net and Zod or equivalent schema validation at runtime boundaries.

| Concern | Convention |
| --- | --- |
| Compiler posture | Keep strict mode enabled |
| Component props | Define clear types or interfaces |
| Error handling | Use type guards for unknown failures |
| Runtime input | Validate with `Zod` or a comparable schema library |
| External data | Parse and narrow before rendering or mutating state |

Avoid `any` in application code. Use `unknown` at boundaries, then validate and narrow.

## Tailwind Styling and Responsive Design

- Use Tailwind CSS utilities with a consistent color palette and spacing scale.
- Build responsive layouts with mobile-first classes and container query patterns when component size matters more than viewport size.
- Support dark mode deliberately instead of relying on untested color inversions.
- Keep styling close to the component while preserving semantic HTML.
- Extract repeated utility combinations into components or design-system primitives when repetition obscures intent.
- Use accessible contrast and visible focus states for interactive elements.

## State Management and Async UI

- Treat React Server Components as the default place for server state.
- Use React hooks for local client state and lift state only to the nearest common owner.
- Render explicit loading and error states with `loading.tsx`, Suspense, or component-level fallbacks.
- Use optimistic updates only when rollback and failure messaging are clear.
- Keep retry logic bounded and visible to the user.

## Data Fetching, Caching, and Invalidation

- Fetch directly in Server Components when data is server-only or database-backed.
- Use React Suspense for loading states where streaming or deferred UI improves experience.
- Define cache invalidation strategies when data can change after render.
- Keep mutation paths secure and validate inputs before writes.
- Avoid duplicating server data into client state unless the user interaction requires it.

## Security and API Handling

- Validate and sanitize all input crossing route handlers, server actions, and API route boundaries.
- Check authentication and authorization before reading or mutating protected data.
- Apply CSRF protection where cookie-authenticated mutations can be triggered cross-site.
- Rate limit public or abuse-prone endpoints.
- Handle API route failures without leaking stack traces, secrets, or internal system details.

## Performance

- Use `next/image` for image optimization and `next/font` for font optimization when the project uses Next.js-managed assets.
- Let Next.js route prefetching work for likely navigations; avoid prefetching large or sensitive routes unnecessarily.
- Split heavy client-only code behind dynamic imports or smaller client components.
- Monitor bundle size and avoid pulling server-only dependencies into client bundles.
- Keep Tailwind class usage intentional so generated CSS and component markup stay reviewable.

## Good / Bad Examples

The examples below illustrate a small server/client boundary with typed props and Tailwind styling.

**Good:**

```tsx
type ProductCardProps = {
  name: string;
  priceLabel: string;
};

export function ProductCard({ name, priceLabel }: ProductCardProps) {
  return (
    <article className="rounded-lg border bg-background p-4 text-foreground">
      <h2 className="text-lg font-semibold">{name}</h2>
      <p className="text-sm text-muted-foreground">{priceLabel}</p>
    </article>
  );
}
```

Why: The component has typed props, semantic HTML, accessible text, and focused Tailwind utilities without unnecessary client JavaScript.

**Bad:**

```tsx
'use client';

export default function Card(props: any) {
  return <div onClick={() => fetch('/api/buy')}>{props.name}</div>;
}
```

Why: The component widens the client surface, uses `any`, lacks semantic interaction, and performs an unsafe mutation from a click handler.

## Conventions

| Rule | Rationale |
|---|---|
| Use App Router patterns with Server Components by default | Server rendering reduces client JavaScript and matches modern Next.js architecture |
| Keep `'use client'` at the smallest interactive boundary | Client bundles stay small and server-only code remains server-side |
| Keep TypeScript strict and validate runtime input with `Zod` or an equivalent schema | Compile-time and runtime failures are caught before unsafe data is trusted |
| Use Tailwind utilities with semantic HTML, responsive patterns, dark mode, and visible focus states | UI remains accessible, maintainable, and adaptable |
| Render loading, error, and retry states for asynchronous flows | Users do not encounter blank or unrecoverable screens |
| Validate authentication, authorization, CSRF, rate limiting, and sanitization at API boundaries | Protected data and mutation endpoints remain safe |
| Use `next/image`, `next/font`, route prefetching, code splitting, and bundle checks intentionally | Performance optimizations are applied without accidental client bloat |

## Do / Do Not

| Do | Do not |
|---|---|
| Group routes by feature or domain | Scatter related pages and layouts by technical layer only |
| Use Server Components for server state | Move database or server-only data fetching into broad client components |
| Define clear prop types and type guards | Use `any` to bypass strict TypeScript |
| Validate external input with `Zod` or equivalent | Trust route params, forms, or API payloads without validation |
| Use Tailwind with semantic elements and focus states | Replace semantics with styled `div` elements for controls |
| Add explicit loading and error UI | Leave async states as blank screens |
| Optimize images, fonts, and bundles with Next.js primitives | Import heavy client dependencies into shared components without review |

## Checklist Before Opening a PR

- [ ] Routes and components follow App Router conventions and are grouped by feature or domain.
- [ ] Server Components are the default and `'use client'` appears only at necessary interactive boundaries.
- [ ] TypeScript remains strict, props are typed, and runtime inputs are validated.
- [ ] Tailwind styling uses semantic HTML, responsive behavior, dark mode support, and accessible focus/contrast.
- [ ] Async views provide loading, error, retry, and optimistic-update rollback behavior where relevant.
- [ ] API routes, route handlers, or server actions validate input, authorization, CSRF exposure, and rate limits.
- [ ] Images, fonts, route prefetching, code splitting, and bundle size are handled intentionally.

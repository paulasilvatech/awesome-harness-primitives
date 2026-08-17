---
applyTo: '**/*.tsx,**/*.ts,**/*.jsx,**/*.js,**/*.css'
description: 'Enforces Next.js App Router conventions for Next.js 16.1.1, Server and Client Components, async request APIs, Route Handlers, Cache Components, tooling, structure, security, and testing.'
---

# Next.js Conventions — App Router 16.1.1

These instructions apply to Next.js App Router applications using TypeScript, React components, route handlers, styles, and configuration aligned with Next.js 16.1.1. They are authoritative for App Router structure, Server and Client Component boundaries, async request APIs, Route Handlers, Cache Components, tooling updates, security, testing, and performance in matched files; current official Next.js documentation and project-specific architecture, deployment, and security rules win where they are stricter.

## Project Structure and Naming

Use the `app/` directory for all new projects and prefer it over legacy `pages/` routing. Use top-level folders deliberately: `app/` for routing, layouts, pages, and route handlers; `public/` for static assets; `lib/` for shared utilities, API clients, and logic; `components/` for reusable UI; `contexts/` for React providers; `styles/` for global and modular stylesheets; `hooks/` for custom hooks; and `types/` for TypeScript definitions. Optionally use `src/` to separate source from config files.

| Naming target | Convention |
| --- | --- |
| Route groups | Parentheses, such as `(admin)`, without affecting the URL path. |
| Private folders | Prefix with `_`, such as `_internal`, to opt out of routing and signal implementation details. |
| Feature folders | Group large app areas by feature, such as `app/dashboard/` and `app/auth/`. |
| Components | `PascalCase` files and exports, such as `UserCard.tsx`. |
| Hooks and utilities | `camelCase`, such as `useUser.ts`. |
| Static assets | `snake_case` or `kebab-case`, such as `logo_dark.svg`. |
| Context providers | `XyzProvider`, such as `ThemeProvider`. |
| Variables/functions | `camelCase`. |
| Types/interfaces | `PascalCase`. |
| Constants | `UPPER_SNAKE_CASE`. |

Colocate components, styles, and tests near use sites without creating deeply nested structures. Place shared components in `components/`, route-specific components in route folders, and co-located tests beside components such as `UserCard.test.tsx`.

## Server and Client Components

Server Components are the default for data fetching, heavy logic, and non-interactive UI. Add `'use client'` only for interactivity, state, hooks, browser APIs, or client-only libraries. Never use `next/dynamic` with `{ ssr: false }` inside a Server Component because it is unsupported and causes build or runtime errors.

Move client-only logic into a dedicated Client Component and import that component directly from the Server Component. Compose related client-only elements, such as a navbar with a profile dropdown, inside one Client Component when that keeps the boundary clear.

```tsx
import DashboardNavbar from "@/components/DashboardNavbar";

export default async function DashboardPage() {
  return (
    <>
      <DashboardNavbar />
    </>
  );
}
```

Use TypeScript interfaces for props, prefer explicit prop types and default values, create a component when UI is reused, complex, self-contained, or improves readability/testability, and keep files production-focused instead of adding example/demo files such as `ModalExample.tsx` unless explicitly requested for a live example, Storybook story, or documentation component.

## App Router Request APIs and Route Handlers

In Next.js 16 App Router, assume request-bound data is async in Server Components and Route Handlers. Await APIs such as `cookies()`, `headers()`, and `draftMode()`. Treat `params` and `searchParams` as possibly Promises in Server Components and await them instead of assuming plain objects. Accessing cookies, headers, or searchParams opts the route into dynamic behavior; read them intentionally and isolate dynamic parts behind `Suspense` boundaries when appropriate.

For API routes, place Route Handlers in `app/api/`, export async functions named after HTTP verbs such as `GET` and `POST`, use Web `Request` and `Response` APIs, and use `NextRequest` or `NextResponse` for advanced features. Use dynamic segments such as `app/api/users/[id]/route.ts`, validate and sanitize input with libraries such as `zod` or `yup`, return appropriate HTTP status codes, and protect sensitive routes with middleware or server-side session checks. Prefer API Routes over Edge Functions unless ultra-low latency or geographic distribution is required.

Do not call your own Route Handlers from Server Components with `fetch('/api/...')` just to reuse logic. Extract shared logic into `lib/` and call it directly to avoid extra server hops.

## Tooling, Environment, Caching, and Performance

- Use TypeScript for all code and enable `strict` mode in `tsconfig.json`.
- Use ESLint and Prettier with the official Next.js ESLint config; in Next.js 16, run ESLint through the ESLint CLI instead of `next lint`.
- Store secrets in `.env.local` and never commit them.
- `serverRuntimeConfig` and `publicRuntimeConfig` are removed; use environment variables instead.
- `NEXT_PUBLIC_` variables are inlined at build time, so changing them after build does not affect a deployed build.
- When runtime env evaluation is needed in a dynamic context, follow Next.js guidance such as calling `connection()` before reading `process.env`.
- Turbopack is the default dev bundler; configure it with top-level `turbopack` in `next.config.*`, not removed `experimental.turbo`.
- Enable stable typed routes with `typedRoutes` when TypeScript is used.
- Use built-in Image and Font optimization.
- Use Suspense and loading states for async data.
- Avoid large client bundles by keeping most logic in Server Components.

Prefer Cache Components for memoization and caching in the App Router. Enable `cacheComponents: true` in `next.config.*` and use the `use cache` directive for cached components or functions. Use `cacheTag(...)` for tags and `cacheLife(...)` for lifetimes. Prefer `revalidateTag(tag, 'max')` for stale-while-revalidate, avoid the deprecated single-argument `revalidateTag(tag)`, use `updateTag(...)` inside Server Actions when read-your-writes or immediate consistency is required, and avoid `unstable_cache` for new code because it is legacy.

## Security, Testing, Accessibility, and Documentation

Sanitize all user input, use HTTPS in production, set secure HTTP headers, and prefer server-side authorization for Server Actions and Route Handlers. Never trust client input. Use Jest, React Testing Library, or Playwright for critical logic and components. Use semantic HTML and ARIA attributes and test with screen readers. Write clear README content and useful comments, and document public APIs and components.

## Good / Bad Examples

The examples below illustrate Client Component boundaries in Server Components.

**Good:**

```tsx
import DashboardNavbar from "@/components/DashboardNavbar";

export default async function DashboardPage() {
  return <DashboardNavbar />;
}
```

Why: Client-only behavior is isolated in a Client Component imported directly by the Server Component.

**Bad:**

```tsx
import dynamic from "next/dynamic";

const DashboardNavbar = dynamic(() => import("@/components/DashboardNavbar"), { ssr: false });

export default function DashboardPage() {
  return <DashboardNavbar />;
}
```

Why: `next/dynamic` with `{ ssr: false }` inside a Server Component is unsupported.

## Next.js Compatibility Vocabulary

Preserve Next.js terms ` (e.g., `, `Request/Response`, `Types/Interfaces`, `Variables/Functions`, `[param]`, `app/api/users/route.ts`, `await`, `build/runtime`, `component/function`, `cookies/headers/searchParams`, `get_library_docs`, `index.ts`, `legacy/deprecated.`, `logic/UI`, `memoization/caching**`, `package/library`, `resolve_library_id`, `server-rendered`, `server/client`, `single-export`, `up-to-date`, `user-profile`, `user-profile/`, and `utilities/hooks` when aligning this file with current documentation.


## Conventions

| Rule | Rationale |
| --- | --- |
| Use `app/` and App Router for new work | Next.js routing, layouts, and data patterns are centered on App Router |
| Keep Server Components as the default and minimize `'use client'` | Client bundles stay small and server data access remains direct |
| Await `cookies()`, `headers()`, `draftMode()`, `params`, and `searchParams` where applicable | Next.js 16 request APIs are async and dynamic rendering should be deliberate |
| Extract shared logic into `lib/` instead of calling local Route Handlers | Server Components avoid unnecessary HTTP hops |
| Use Cache Components, `use cache`, `cacheTag`, `cacheLife`, `revalidateTag(tag, 'max')`, and `updateTag` intentionally | Caching and revalidation semantics remain current and predictable |
| Use ESLint CLI, top-level `turbopack`, and `typedRoutes` | Tooling matches Next.js 16 behavior |
| Treat `NEXT_PUBLIC_` as build-time public config | Runtime changes do not update already built client bundles |
| Avoid demo files unless explicitly requested | The codebase stays production-focused |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Import Client Components directly from Server Components | Use `next/dynamic` with `{ ssr: false }` in Server Components |
| Await request-bound APIs and route props when needed | Treat cookies, headers, params, or searchParams as always synchronous plain data |
| Validate Route Handler input with `zod` or `yup` | Trust raw request bodies or query strings |
| Use `revalidateTag(tag, 'max')` for stale-while-revalidate | Use deprecated single-argument `revalidateTag(tag)` in new code |
| Use `updateTag(...)` inside Server Actions for immediate consistency | Reach for `unstable_cache` in new implementations |
| Configure Turbopack through `turbopack` | Use removed `experimental.turbo` |
| Store secrets in `.env.local` | Commit secrets or rely on removed runtime config APIs |

## Checklist Before Opening a PR

- [ ] New routing uses `app/`, route groups, private folders, and feature folders intentionally.
- [ ] Component, hook, utility, asset, type, interface, provider, and constant names follow the conventions above.
- [ ] `'use client'` is limited to interactive components and no Server Component uses `next/dynamic` with `{ ssr: false }`.
- [ ] `cookies()`, `headers()`, `draftMode()`, `params`, and `searchParams` are awaited or isolated where Next.js 16 requires async request handling.
- [ ] Route Handlers live in `app/api/`, export HTTP verb functions, validate input, return proper status codes, and enforce authorization.
- [ ] Server Components call shared `lib/` logic directly instead of fetching local API routes for reuse.
- [ ] Cache Components use `cacheComponents`, `use cache`, `cacheTag`, `cacheLife`, `revalidateTag(tag, 'max')`, or `updateTag` deliberately.
- [ ] TypeScript strict mode, ESLint CLI, Prettier, top-level `turbopack`, and `typedRoutes` are configured where applicable.
- [ ] Secrets are not committed, `NEXT_PUBLIC_` usage is build-time safe, and removed runtime config APIs are absent.
- [ ] Tests, accessibility, documentation, and public API comments cover changed critical behavior.

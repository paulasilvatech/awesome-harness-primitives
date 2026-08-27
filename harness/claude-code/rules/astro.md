---
paths:
  - "**/*.astro"
  - "**/*.ts"
  - "**/*.js"
  - "**/*.md"
  - "**/*.mdx"
---

<!-- Generated from harness/github-copilot/instructions/astro.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Astro 7 conventions for content-driven websites, islands architecture, Content Layer API, TypeScript, routing, actions, sessions, performance, styling, SEO, and images.

# Astro Development Conventions — Content-Driven Islands

These instructions apply to Astro components, TypeScript, JavaScript, Markdown, and MDX in Astro 7.x projects. They are authoritative for server-first Astro architecture, Islands Architecture, Content Layer API, TypeScript integration, selective hydration, server islands, actions, sessions, API routes, styling, SEO, images, and data fetching; project-specific framework, accessibility, deployment, and security policies win when stricter.

## Architecture and Project Context

Use Astro 7.x for content-driven websites such as blogs, marketing sites, e-commerce, and documentation. Default to server-first rendering and static site generation (SSG), add server-side rendering (SSR) only for dynamic requirements, and use multiple UI frameworks such as React, Vue, Svelte, or Solid only where interactivity requires them.

- Embrace Islands Architecture: server-render by default and hydrate selectively.
- Use Content Collections and the Content Layer API for type-safe Markdown and MDX.
- Structure projects by feature or content type for scalability.
- Use component-based architecture with clear separation of concerns.
- Implement progressive enhancement.
- Prefer Multi-Page App (MPA) patterns over Single-Page App (SPA) patterns.
- Default to zero JavaScript and add interactivity only where needed.

## TypeScript, Components, and Content Collections

Extend Astro's base config in `tsconfig.json`, include generated types, and run `astro sync` after changing collections or config.

```json
{
  "extends": "astro/tsconfigs/base",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}
```

| Area | Convention |
| --- | --- |
| Types | Use TypeScript for props and content; generated types live in `.astro/types.d.ts`. |
| Components | Use `.astro` components for static server-rendered content and import framework components only for interactivity. |
| Structure | Keep frontmatter at the top and template below; use PascalCase component names. |
| HTML | Write valid, fully closed HTML; the compiler errors on unclosed tags and does not auto-correct invalid nesting such as block elements inside `<p>`. |
| Collections | Define collections in `src/content.config.ts` with `defineCollection`, `glob()`, `file()`, and schema validation. |
| Zod | Import `z` from `astro/zod`, not `astro:content`; prefer top-level helpers such as `z.email()` and `z.url()`. |
| Queries | Use type-safe `getCollection()` and `getEntry()`. |

```typescript
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { blog };
```

## Routing, Transitions, Server Islands, Actions, and Sessions

- Enable view transitions and client-side routing with `<ClientRouter />` in the layout `<head>` and `import { ClientRouter } from 'astro:transitions'`.
- Customize animations with CSS and `view-transition-name`.
- Preserve component state across navigations with persistent islands and `transition:persist`.
- Use `server:defer` to render a server island on demand without blocking the rest of the page; provide fallback content with `slot="fallback"` and configure an SSR adapter for on-demand rendering.

```astro
---
import Avatar from '../components/Avatar.astro';
---
<Avatar server:defer>
  <div slot="fallback">Loading…</div>
</Avatar>
```

- Define type-safe server functions in `src/actions/index.ts`; prefer actions over ad-hoc API routes for mutations and form handling.
- Validate action input with Zod and set `accept: 'form'` for HTML form submissions.
- Call actions from the client via `astro:actions` and handle `{ data, error }`.

```typescript
import { defineAction } from 'astro:actions';
import { z } from 'astro/zod';

export const server = {
  subscribe: defineAction({
    accept: 'form',
    input: z.object({ email: z.email() }),
    handler: async ({ email }) => {
      return { success: true };
    },
  }),
};
```

- Read and write server-side state with `Astro.session` (`get`, `set`) instead of overloading cookies; configure SSR session storage.
- Use `Astro.session` for carts, flash messages, and other per-visitor data that should not live on the client.
- Create API routes in `src/pages/api/` for dynamic functionality, use proper HTTP methods and status codes, validate requests, handle errors, secure environment variables, and use middleware for authentication or request processing.

## Performance, Styling, SEO, Images, and Data

| Concern | Convention |
| --- | --- |
| Hydration | Use client directives strategically: `client:load`, `client:idle`, and `client:visible`. |
| Assets | Optimize static assets with Astro's built-in optimization and lazy load images and components. |
| Content performance | Leverage Content Layer API for faster content loading and builds. |
| Bundle size | Minimize client-side JavaScript and avoid unnecessary framework imports. |
| Styling | Use scoped styles by default, CSS custom properties for theming, Sass or Less only when needed, and mobile-first responsive design. |
| Accessibility | Use semantic HTML and proper ARIA attributes. |
| Whitespace | Astro strips whitespace using JSX rules by default (`compressHTML: 'jsx'`); add explicit `{" "}` between inline elements when visible space is required. |
| Interactivity | Use framework components, Web Components, stores, or custom events for island state and client behavior. |
| SEO | Manage page titles, descriptions, Open Graph, Twitter Card metadata, sitemaps, semantic structure, and JSON-LD structured data. |
| Images | Use Astro's `<Image />` component, responsive `srcset`, WebP, AVIF, lazy loading, build-time optimization, and proper `alt` text. |
| Data fetching | Fetch data at build time in frontmatter, use dynamic imports for conditional loading, cache expensive operations during builds, use Astro's built-in `fetch`, and provide loading states and fallbacks. |

## Good / Bad Examples

The examples below illustrate selective hydration.

**Good:**

```astro
---
import StaticHero from '../components/StaticHero.astro';
import SearchBox from '../components/SearchBox.tsx';
---
<StaticHero />
<SearchBox client:idle />
```

Why: Static content stays server-rendered and only the interactive search island hydrates.

**Bad:**

```astro
---
import App from '../components/App.tsx';
---
<App client:load />
```

Why: Hydrating the whole page as a client app defeats Astro's server-first MPA model.

## Astro Compatibility Vocabulary

Preserve Astro terms `NOTE`, `Markdown/MDX`, `astro:transitions`, `auto-generated`, `file-based`, `framework-agnostic`, `fully-closed`, `high-quality`, and `utility-first`. The Zod import warning remains ` (not from ` `) and prefer top-level Zod helpers such as ` when maintaining migrated wording around `astro/zod` and `astro:content`.


## Conventions

| Rule | Rationale |
| --- | --- |
| Server-render by default and hydrate islands selectively | Astro performance depends on shipping little or no JavaScript by default |
| Use Content Collections and the Content Layer API | Content becomes typed, validated, and faster to build |
| Run `astro sync` after config or collection changes | Generated types in `.astro/types.d.ts` stay accurate |
| Import `z` from `astro/zod` and loaders from `astro/loaders` | Astro 7 content schemas use the current APIs |
| Use `ClientRouter`, `transition:persist`, `server:defer`, actions, and `Astro.session` only for their intended routing, island, mutation, and state needs | Advanced runtime features remain deliberate and maintainable |
| Keep HTML valid and explicit about whitespace | Astro's compiler and JSX whitespace behavior are strict |
| Use `<Image />`, semantic HTML, metadata, and structured data | Pages remain performant, accessible, and discoverable |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `.astro` components for static content | Import a framework component when no interactivity exists |
| Use `client:idle` or `client:visible` for non-critical islands | Hydrate everything with `client:load` by default |
| Define mutations in `src/actions/index.ts` | Create ad-hoc API routes for simple form actions |
| Use `Astro.session` for server-side visitor state | Overload cookies with application state |
| Add `slot="fallback"` for `server:defer` islands | Leave deferred server content with no loading state |
| Use `glob()` or `file()` loaders in `src/content.config.ts` | Query untyped Markdown manually |
| Add explicit `{" "}` where inline whitespace must render | Assume JSX whitespace compression preserves every visual space |

## Checklist Before Opening a PR

- [ ] Astro code follows server-first Islands Architecture and avoids unnecessary client JavaScript.
- [ ] TypeScript extends `astro/tsconfigs/base`, includes `.astro/types.d.ts`, and `astro sync` was run after collection or config changes.
- [ ] Content collections use `src/content.config.ts`, `defineCollection`, `glob()` or `file()`, and `z` from `astro/zod`.
- [ ] Components use focused `.astro` files or framework islands only when interactivity requires them.
- [ ] View transitions, `ClientRouter`, `transition:persist`, `server:defer`, actions, and `Astro.session` are used only where their runtime behavior is needed.
- [ ] API routes, middleware, environment variables, and SSR behavior are validated and secure.
- [ ] Styling is scoped, responsive, accessible, and explicit about JSX whitespace where needed.
- [ ] SEO metadata, sitemaps, Open Graph, Twitter Card, JSON-LD, and image optimization are correct for changed pages.

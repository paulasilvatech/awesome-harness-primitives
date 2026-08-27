---
name: markstream-install
description: >-
  Install and configure Markstream streaming Markdown renderers for Vue, React, Svelte, Angular,
  Nuxt, Next.js, and Vue 2 applications. Use when adding streaming Markdown to AI chat or document
  interfaces, repairing Markstream styles or SSR, or choosing static, smooth-streaming, or
  externally parsed AST input.
license: MIT
metadata:
  compatibility: >-
    JavaScript or TypeScript frontend project using Vue 3, Nuxt 3/4, Vue 2.6/2.7, React 18+,
    Next.js, Angular 20+, or Svelte 5.
  documentation: "https://markstream.simonhe.me/"
  source: "https://github.com/Simon-He95/markstream-vue"
---

<!-- Generated from harness/github-copilot/plugins/web-framework-development/skills/markstream-install/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Markstream install

Integrates the smallest correct Markstream package into an existing frontend, wires package CSS in the right order, preserves safe rendering defaults, and validates static and streaming Markdown output.

## When to invoke

- "Add streaming Markdown rendering to this AI chat."
- "Install Markstream in my Vue, React, Svelte, Angular, Nuxt, or Next.js app."
- "Fix missing Markstream styles or SSR errors."
- "Replace our Markdown renderer with Markstream."
- "Should this use content, smooth streaming, or nodes?"

## Prerequisites and context

Inspect the host application before changing dependencies:

- Framework and version in `package.json`.
- Package manager lockfile.
- SSR mode: Nuxt, Next.js, server components, or static SPA.
- Reset, Tailwind, UnoCSS, or design-system style order.
- Requested optional peers: code highlighting, enhanced File/Diff surfaces, Monaco, Mermaid, D2, infographic blocks, or KaTeX.

Read `references/scenarios.md` before choosing packages or peers. Official sources are https://markstream.simonhe.me/ and https://github.com/Simon-He95/markstream-vue .

## Procedure

1. Inspect the host application and identify the exact framework boundary.
2. Install exactly one framework package and only the optional peers required by the requested UI.
3. Import Markstream CSS explicitly after resets; use a component layer for Tailwind or UnoCSS.
4. Add the smallest renderer that matches the input model: `content`, smooth streaming, or `nodes` plus `final`.
5. Apply framework-specific SSR and client boundaries.
6. Preserve safe HTML and strict Mermaid defaults unless the user explicitly requires a trusted exception.
7. Run the smallest relevant build, typecheck, or test command.

## Package selection

| Host | Package | Notes |
| --- | --- | --- |
| Vue 3 | `markstream-vue` | Use `mode="chat"`, `mode="docs"`, or `mode="minimal"`. |
| Nuxt 3/4 | `markstream-vue` | Keep browser-only optional peers behind client boundaries. |
| React 18+ | `markstream-react` | Use the root entry inside a `'use client'` component for live SSE or WebSocket streams. |
| Next.js | `markstream-react`, `markstream-react/next`, or `markstream-react/server` | Use `/next` for SSR-first HTML with hydration and `/server` for server-only rendering. |
| Svelte 5 | `markstream-svelte` | Do not use for older Svelte apps. |
| Angular 20+ | `markstream-angular` | Confirm the app meets the current package requirement. |
| Vue 2.6/2.7 | `markstream-vue2` | Vue CLI 4 and Webpack 4 may need direct CSS import from `dist`. |

Install examples:

```bash
npm install markstream-vue
npm install markstream-react
npm install markstream-svelte
npm install markstream-angular
npm install markstream-vue2
```

## Styling and renderer rules

Import application resets before Markstream styles. Do not rely on component imports to inject CSS.

```css
@import 'markstream-vue/index.css' layer(components);
@import 'katex/dist/katex.min.css';
```

Use the matching package subpath for React, Svelte, Angular, or Vue 2. For Webpack 4-based Vue 2 applications, use:

```ts
import 'markstream-vue2/dist/index.css'
```

For Vue 3 streaming chat, start with:

```vue
<MarkdownRender
  mode="chat"
  :content="markdown"
  :final="false"
  smooth-streaming="auto"
  :fade="false"
  typewriter
/>
```

For completed history, keep the mode and switch pacing off:

```vue
<MarkdownRender
  mode="chat"
  :content="markdown"
  :final="true"
  :smooth-streaming="false"
  :fade="true"
  :typewriter="false"
/>
```

In React, Svelte, and Angular, use equivalent camelCase or framework binding syntax: `smoothStreaming="auto"`, `fade=false`, `typewriter=true` while streaming; `smoothStreaming=false` and `typewriter=false` for completed history.

## Input and security choices

| Choice | Use when | Avoid when |
| --- | --- | --- |
| `content` | Static documents and most streaming chat. | Another layer already owns parsing. |
| Smooth streaming | Token delivery is irregular and the UI should pace output. | Completed chat history. |
| `nodes` plus `final` | A worker, shared AST store, custom transform, or application layer already owns parsing. | The app only has Markdown text. |
| HTML policy `safe` | Default for all untrusted content. | Only broaden for an explicit trusted legacy surface. |
| Mermaid strict mode | Default for diagrams from users or models. | Only relax for a scoped trusted surface. |

## Gotchas

- **Do not install every optional peer**: install Monaco, Mermaid, D2, KaTeX, or infographic support only when requested.
- **Do not assume Vue because the source repo is named `markstream-vue`**: select the framework-specific package.
- **Do not run browser-only peers during SSR**: isolate them behind Nuxt client boundaries or Next.js client components.
- **Do not add a second virtualizer blindly**: for long Vue 3 conversations or an existing message virtualizer, consult the performance guide first.

## Progressive disclosure and bundled resources

- `references/scenarios.md`: package choice, optional peer, and scenario matrix.

## Markstream mode vocabulary

Markstream has `built-in` smooth streaming for chat and `non-chat` surfaces such as docs or minimal renderers. Keep those distinctions when choosing modes.

## Output template

```markdown
### Markstream install result

**Status:** installed | plan only | blocked
**Framework:** <Vue 3 | Nuxt | React | Next.js | Svelte 5 | Angular | Vue 2>
**Package:** `<markstream package>`
**Optional peers:** <none | list>
**CSS location:** `<file and import order>`
**Streaming input:** `content` | `nodes` plus `final` | static

**Changes**
- <dependency change>
- <renderer/component change>
- <style import change>

**Validation**
- `<build/typecheck/test command>`: pass | fail
```

## Quality gate

- [ ] The selected package matches the detected framework.
- [ ] Only requested optional peers were added.
- [ ] CSS imports are explicit and load after resets.
- [ ] Tailwind or UnoCSS imports use a component layer when needed.
- [ ] SSR pages do not evaluate browser-only peers on the server.
- [ ] Static content and at least one incremental update render correctly.
- [ ] HTML policy remains `safe` and Mermaid remains strict unless a scoped trusted exception is documented.

## References

- [Installation](https://markstream.simonhe.me/guide/installation)
- [AI chat and streaming](https://markstream.simonhe.me/guide/ai-chat-streaming)
- [Performance](https://markstream.simonhe.me/guide/performance)
- [Troubleshooting](https://markstream.simonhe.me/guide/troubleshooting)
- [Component overrides](https://markstream.simonhe.me/guide/component-overrides)

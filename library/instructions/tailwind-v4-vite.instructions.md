---
applyTo: "vite.config.ts,vite.config.js,**/*.css,**/*.tsx,**/*.ts,**/*.jsx,**/*.js"
description: "Enforces Tailwind CSS v4+ conventions for Vite projects using @tailwindcss/vite, CSS-first configuration, migration, verification, and troubleshooting."
---

# Tailwind CSS v4 Vite Conventions — CSS-First Setup

These instructions apply to Vite configuration, CSS, TypeScript, JavaScript, TSX, and JSX files in projects that use Tailwind CSS v4 or newer. They are authoritative for `@tailwindcss/vite` setup, CSS-first configuration, imports, migration from Tailwind v3, verification, and troubleshooting; official Tailwind documentation wins when v4 installation or upgrade behavior changes.

Instructions for installing and configuring Tailwind CSS version 4 and above using the official Vite plugin. Tailwind CSS v4 introduces a simplified setup that eliminates the need for PostCSS configuration and tailwind.config.js in most cases.

## Key Changes in Tailwind CSS v4

- **No PostCSS configuration required** when using the Vite plugin
- **No tailwind.config.js required** - configuration is done via CSS
- **New @tailwindcss/vite plugin** replaces the PostCSS-based approach
- **CSS-first configuration** using `@theme` directive
- **Automatic content detection** - no need to specify content paths

## Installation Conventions

### Dependencies

Install `tailwindcss` and the `@tailwindcss/vite` plugin:

```bash
npm install tailwindcss @tailwindcss/vite
```

### Vite Plugin

Add the `@tailwindcss/vite` plugin to your Vite configuration file:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

For React projects with Vite:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

### Tailwind CSS Import

Add the Tailwind CSS import to your main CSS file (e.g., `src/index.css` or `src/App.css`):

```css
@import "tailwindcss";
```

### Entry Point Import

Ensure your main CSS file is imported in your application entry point:

```typescript
// src/main.tsx or src/main.ts
import './index.css'
```

### Development Server

Run the development server to verify installation:

```bash
npm run dev
```

## Tailwind v4 Anti-Patterns

### Do NOT Create tailwind.config.js

Tailwind v4 uses CSS-first configuration. Do not create a `tailwind.config.js` file unless you have specific legacy requirements.

```javascript
//  NOT NEEDED in Tailwind v4
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Do NOT Create postcss.config.js for Tailwind

When using the `@tailwindcss/vite` plugin, PostCSS configuration for Tailwind is not required.

```javascript
//  NOT NEEDED when using @tailwindcss/vite
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Do NOT Use Old Directives

The old `@tailwind` directives are replaced by a single import:

```css
/*  OLD - Do not use in Tailwind v4 */
@tailwind base;
@tailwind components;
@tailwind utilities;

/*  NEW - Use this in Tailwind v4 */
@import "tailwindcss";
```

## CSS-First Configuration (Tailwind v4)

### Custom Theme Configuration

Use the `@theme` directive in your CSS to customize your design tokens:

```css
@import "tailwindcss";

@theme {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --font-sans: 'Inter', system-ui, sans-serif;
  --radius-lg: 0.75rem;
}
```

### Adding Custom Utilities

Define custom utilities directly in CSS:

```css
@import "tailwindcss";

@utility content-auto {
  content-visibility: auto;
}

@utility scrollbar-hidden {
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }
}
```

### Adding Custom Variants

Define custom variants in CSS:

```css
@import "tailwindcss";

@variant hocus (&:hover, &:focus);
@variant group-hocus (:merge(.group):hover &, :merge(.group):focus &);
```

## Installation Verification

After installation, verify:

- [ ] `tailwindcss` and `@tailwindcss/vite` are in `package.json` dependencies
- [ ] `vite.config.ts` includes the `tailwindcss()` plugin
- [ ] Main CSS file contains `@import "tailwindcss";`
- [ ] CSS file is imported in the application entry point
- [ ] Development server runs without errors
- [ ] Tailwind utility classes (e.g., `text-blue-500`, `p-4`) render correctly

## Example Usage

Test the installation with a simple component:

```tsx
export function TestComponent() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <h1 className="text-3xl font-bold text-blue-600 underline">
        Hello, Tailwind CSS v4!
      </h1>
    </div>
  )
}
```

## Troubleshooting

### Styles Not Applying

1. Verify CSS import statement is `@import "tailwindcss";` (not old directives)
2. Ensure CSS file is imported in your entry point
3. Check Vite config includes the `tailwindcss()` plugin
4. Clear Vite cache: `rm -rf node_modules/.vite && npm run dev`

### Plugin Not Found Error

If you see "Cannot find module '@tailwindcss/vite'":

```bash
npm install @tailwindcss/vite
```

### TypeScript Errors

If TypeScript cannot find types for the Vite plugin, ensure you have the correct import:

```typescript
import tailwindcss from '@tailwindcss/vite'
```

## Migration from Tailwind v3

If migrating from Tailwind v3:

1. Remove `tailwind.config.js` (move customizations to CSS `@theme`)
2. Remove `postcss.config.js` (if only used for Tailwind)
3. Uninstall old packages: `npm uninstall postcss autoprefixer`
4. Install new packages: `npm install tailwindcss @tailwindcss/vite`
5. Replace `@tailwind` directives with `@import "tailwindcss";`
6. Update Vite config to use `@tailwindcss/vite` plugin

## Source References

- Official Documentation: https://tailwindcss.com/docs/installation/using-vite
- Tailwind CSS v4 Upgrade Guide: https://tailwindcss.com/docs/upgrade-guide

## Conventions

| Rule | Rationale |
| --- | --- |
| Install `tailwindcss` and `@tailwindcss/vite` with `npm install tailwindcss @tailwindcss/vite` | Tailwind v4's Vite integration uses the official plugin instead of PostCSS wiring |
| Add `tailwindcss()` to `vite.config.ts` or `vite.config.js`, alongside `react()` when using React | Vite must run Tailwind through the v4 plugin pipeline |
| Import Tailwind once with `@import "tailwindcss";` in the main CSS file | v4 replaces the old `@tailwind base`, `@tailwind components`, and `@tailwind utilities` directives |
| Import the main CSS file from `src/main.tsx`, `src/main.ts`, or the actual entry point | Tailwind utilities cannot render if the CSS bundle is not included |
| Use CSS-first `@theme`, `@utility`, and `@variant` directives for customization | Tailwind v4 no longer requires `tailwind.config.js` for common configuration |
| Avoid `postcss.config.js`, `tailwind.config.js`, `postcss`, and `autoprefixer` unless a legacy need is explicit | Extra v3-era config adds confusion and can break v4 expectations |
| Verify with `npm run dev` and a visible utility such as `text-blue-500` or `p-4` | Installation is only complete when Vite compiles and utilities render |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Configure Tailwind through `@tailwindcss/vite` | Configure Tailwind v4 as a PostCSS plugin by default |
| Use `@theme` for tokens such as `--color-primary`, `--font-sans`, and `--radius-lg` | Recreate a v3 `theme.extend` block without a migration reason |
| Use `@utility content-auto` and similar CSS utilities for custom behavior | Hide custom utilities in stale JavaScript configuration |
| Use `@variant hocus` and `@variant group-hocus` for custom variants | Keep old plugin-based variants when CSS-first variants are clearer |
| Clear the Vite cache with `rm -rf node_modules/.vite && npm run dev` only when troubleshooting local cache problems | Delete unrelated generated or dependency files as a routine fix |

## Checklist Before Opening a PR

- [ ] `tailwindcss` and `@tailwindcss/vite` are present in `package.json`.
- [ ] `vite.config.ts` or `vite.config.js` imports `tailwindcss` from `@tailwindcss/vite` and includes `tailwindcss()` in `plugins`.
- [ ] The main CSS file contains `@import "tailwindcss";` and no v3 `@tailwind` directive trio.
- [ ] The application entry point imports the main CSS file.
- [ ] Custom tokens, utilities, and variants use `@theme`, `@utility`, and `@variant` where needed.
- [ ] v3-only `tailwind.config.js`, Tailwind PostCSS config, `postcss`, and `autoprefixer` are removed unless explicitly justified.
- [ ] `npm run dev` succeeds and utility classes such as `text-blue-500`, `p-4`, `min-h-screen`, and `bg-gray-100` render.

## References

- Official Tailwind CSS Vite installation: https://tailwindcss.com/docs/installation/using-vite
- Tailwind CSS v4 Upgrade Guide: https://tailwindcss.com/docs/upgrade-guide

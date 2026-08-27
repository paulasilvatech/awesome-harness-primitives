---
paths:
  - "**/*.vue"
  - "**/*.ts"
  - "**/*.js"
  - "**/*.css"
  - "**/*.scss"
---

<!-- Generated from harness/github-copilot/instructions/vue.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Vue 3 conventions for Composition API, script setup, reactivity, macros, components, routing, Pinia, styling, testing, SSR, performance, and security.

# Vue 3 Conventions — Composition API Applications

These instructions apply to Vue single-file components, TypeScript or JavaScript support code, styles, composables, stores, and router files. They are authoritative for Vue 3 authoring style, compiler macros, reactivity, templates, built-in components, Pinia, Vue Router, TypeScript, testing, performance, SSR, accessibility, and security; project-specific architecture, design-system, or framework instructions win when they set narrower component, route, or styling rules.

## Project Baseline and Component Design

Default to Vue 3.4+ and use Vue 3.5+ features such as `useTemplateRef`, `useId`, and reactive props destructuring only when the project version allows. Use `<script setup lang="ts">` SFCs, TypeScript, Pinia, Vue Router, Vite, Vitest, and Vue Test Utils or Testing Library for Vue unless the project has an established alternative.

- Order SFCs as `<script setup>`, then `<template>`, then `<style scoped>`.
- Keep one responsibility per component; split large components into smaller components plus composables.
- Name components in `PascalCase` and use multi-word names such as `UserCard`, not `Card`, to avoid native element collisions.
- Co-locate component-specific types; move shared types into a `types/` module.
- Avoid mixing Options API and Composition API arbitrarily.

## Compiler Macros and Public Component Contracts

Compiler macros require no imports. Type component contracts through `defineProps<T>()`, `withDefaults(defineProps<T>(), { ... })`, `defineEmits<{ change: [id: number]; update: [value: string] }>()`, `defineModel<T>()`, `defineExpose({ ... })`, `defineSlots<{ default(props: { item: T }): any }>()`, and `defineOptions({ name, inheritAttrs })`. Use `defineModel<T>()` for component `v-model`, including multiple models, arguments, and modifiers. Expose nothing by default; `defineExpose` is for intentional imperative APIs only. Never mutate props directly; emit an event, use `defineModel`, or derive local state with `computed` or `ref`.

## Reactivity, Watchers, and Composables

| Need | Preferred API |
| --- | --- |
| Primitive or replaceable value | `ref()` with `.value` in script |
| Deep reactive object or collection | `reactive()` without direct destructuring; use `toRefs()` or `toRef()` |
| Derived value | Pure `computed()`; use writable `computed({ get, set })` only for two-way derived state |
| Explicit side effect | `watch(source, cb, options)` |
| Auto-tracked side effect | `watchEffect(cb)` |
| Large or externally managed object | `shallowRef`, `shallowReactive`, `toRaw`, or `markRaw` |
| Immutable shared state | `readonly()` |
| Grouped effects | `effectScope()` |
| Debounced, throttled, or storage ref | `customRef` |

Use watcher options deliberately: `{ immediate: true }`, `{ deep: true }`, `{ once: true }`, and `flush: 'post'` when DOM updates must complete first. Register cleanup with `onCleanup` or `onWatcherCleanup`, and stop manual watchers with their returned handle when they outlive their natural scope.

Extract reusable stateful logic into synchronous `useXxx()` composables under `composables/`. Accept refs or getters and normalize with `toValue()` and `MaybeRefOrGetter`; return refs, computed values, and async actions. Set up and tear down with `onMounted`, `onUnmounted`, or `tryOnScopeDispose`, and use VueUse utilities such as `useStorage`, `useEventListener`, and `useDebounceFn` rather than reimplementing common behavior.

## Lifecycle, Templates, Slots, and Built-in Components

Use `onMounted`, `onBeforeMount`, `onUpdated`, `onBeforeUnmount`, `onUnmounted`, `onActivated`, `onDeactivated`, and `onErrorCaptured` for their intended lifecycle points. Clean up timers, listeners, observers, and subscriptions in `onUnmounted`; guard `window` and `document` for SSR and run browser-only APIs in `onMounted`.

Templates need stable unique `:key` values on `v-for`; never use an array index when items can reorder or mutate. Do not put `v-if` and `v-for` on the same element; filter with `computed`. Use `v-show` for frequent toggles and `v-if` for conditional mounting. Move heavy expressions into `computed` or methods. Use `:` and `@` shorthands consistently, group nodes with `<template>`, and use `v-memo` or `v-once` only for measured render savings.

Use named slots, scoped slots with `<slot :item="item" />` and `#default="{ item }"`, fallback content, `v-slot` or `#` shorthand, and dynamic slot names when appropriate. Use `<Teleport to="body">` for modals, toasts, and tooltips escaping stacking contexts; `<Suspense>` with `#default` and `#fallback` for async setup and lazy components; `<Transition>` and `<TransitionGroup>` for enter, leave, and list animation; `<KeepAlive include exclude max>` with `onActivated` and `onDeactivated`; `<component :is="...">` and `defineAsyncComponent(() => import('...'))` for dynamic and lazy components.

## Provide/Inject, Pinia, and Routing

Type injections with `InjectionKey<T>` and `Symbol`; provide a default or assert presence. Provide `readonly()` state plus explicit updater functions, and reserve injection for cross-cutting concerns. Use Pinia for app-wide shared state and keep component-only state local with `ref` or `reactive`. Prefer setup stores via `defineStore('user', () => { ... })`; keep actions async and side-effectful, getters pure and synchronous, stores serializable for SSR, and destructuring reactive with `storeToRefs()`. Use `$patch`, `$reset`, `$subscribe`, and `$onAction` deliberately.

Define Vue Router routes with lazy `component: () => import('...')`. Use `beforeEach`, `beforeEnter`, and `beforeRouteLeave` for auth and unsaved-change checks and resolve or `next()` exactly once. Type and use `route.meta`, read params/query through `useRoute()`, navigate with `useRouter()`, treat `route.params` as reactive, configure `scrollBehavior`, and enable typed routes where available.

## Forms, Styling, Accessibility, Performance, SSR, and Security

Bind native inputs with `v-model` and custom inputs with `defineModel`; use `.lazy`, `.number`, and `.trim` modifiers. Use Zod or Yup with VeeValidate or FormKit for non-trivial forms. Client validation is UX only; validate and sanitize on the server.

Default to `<style scoped>` with `:deep()`, `:slotted()`, and `:global()` only when needed. Use `v-bind()` in styles for reactive CSS and prefer CSS custom properties for theming; consider `<style module>` for larger teams.

Use semantic HTML before ARIA. Ensure keyboard operability, visible focus, route-change focus management, dialog focus traps, `aria-label` for icon-only controls, associated labels for inputs, and accessible names.

Code-split routes and heavy components with `defineAsyncComponent` and dynamic `import()`. Use `computed` caching, `v-memo`, `v-once`, `shallowRef`, and `shallowReactive` for measured problems; virtualize long lists with `vue-virtual-scroller`; paginate or window large data; avoid inline object/array literals in templates. Prefer Nuxt for SSR/SSG/hybrid rendering unless hand-rolled SSR is justified. Keep stores request-scoped, avoid module-level shared mutable state, and prevent hydration mismatches.

Never render untrusted input with `v-html`; sanitize with DOMPurify if unavoidable. Validate dynamic `:is`, `:href`, and `:src` values and block `javascript:` schemes. Keep secrets server-side and expose only intentional `VITE_` env vars. Apply CSP, CSRF, and XSS protections at the app layer.

## Testing and Tooling

Unit-test composables as plain functions and component-test observable behavior with Vue Test Utils or Testing Library. Mock stores with `createTestingPinia`, stub router and async boundaries where needed, and cover critical journeys with Playwright or Cypress. Use Vite with the official Vue plugin, `vue-tsc` in CI, ESLint with `eslint-plugin-vue`, Prettier, Volar or the Vue official extension, and `import.meta.env` for environment access.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: ` (v-bind) and ` ` (v-on) shorthands consistently; group nodes with ` `<KeepAlive>` `<Teleport to="body">` `<script setup lang="ts" generic="T">` `<style>` `CSRF/XSS` `Teleport/Suspense/Transition/KeepAlive` `Volar/Vue` `Zod/Yup` `app.config.errorHandler` `app.use(...)` `async/lazy` `async/side` `auto-tracked` `auto-unwrapped` `build/dev.` `class-name` `code-split` `code-split/lazy` `component-tree` `composables/libraries` `cross-component` `debounced/throttled` `deep-reactive` `defineExpose({ ... })` `defineModel/defineSlots/defineOptions` `defineOptions({ name, inheritAttrs })` `defineSlots<{ default(props: { item: T }): any }>()` `end-to-end` `enter/leave` `exclude` `externally-managed` `hand-roll` `include` `inject(key)` `interface/type` `loading/error` `main.ts` `mounted` `named/scoped` `non-reactive` `objects/collections` `opening/closing` `overflow/stacking` `per-route` `production-grade` `props/emits/slots` `provide(key, value)` `provide/inject` `re-implementing` `re-rendering` `ref-or-plain` `ref<HTMLInputElement | null>(null)` `ref<User | null>(null)` `refs/computed` `refs/getters` `requiresAuth` `setup()` `shared/cross-component` `side-effect` `storage-backed` `time-to-interactive` `timers/listeners` `type-checking` `undefined` `unsaved-changes` `updated` `useTemplateRef<HTMLInputElement>('input')` `user-friendly` `v-click-outside` `v-focus` `v-on`.

## Good / Bad Examples

The examples below show safe prop updates and derived state.

**Good:**

```vue
<script setup lang="ts">
const model = defineModel<string>();
const normalized = computed(() => model.value.trim().toLowerCase());
</script>
```

Why: The component uses the Vue 3 model contract and a pure computed value instead of mutating props.

**Bad:**

```vue
<script setup>
const props = defineProps(['value']);
props.value = props.value.trim();
watch(() => props.value, value => local = value);
</script>
```

Why: It mutates props, loses type safety, and uses a watcher for derived state that belongs in `computed`.

## Conventions

| Rule | Rationale |
|---|---|
| Default to `<script setup lang="ts">` and Composition API | Vue 3 inference, performance, and tooling are strongest in this style |
| Use compiler macros for typed props, emits, models, slots, options, and exposes | Component contracts stay explicit without runtime boilerplate |
| Use `computed` for derivation and `watch` only for side effects | Reactive graphs stay predictable and side effects stay visible |
| Preserve reactivity with `toRef`, `toRefs`, and `storeToRefs` when destructuring | Direct destructuring silently breaks updates |
| Keep templates simple, keyed, and free of `v-if` plus `v-for` conflicts | Rendering remains correct and maintainable |
| Keep Pinia stores domain-scoped and serializable | Shared state remains testable and SSR-safe |
| Guard browser APIs and request-scoped state in SSR | Hydration and cross-request leaks are avoided |
| Sanitize `v-html` and validate dynamic URLs | XSS and `javascript:` injection are blocked |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `defineProps<T>()`, `defineEmits`, and `defineModel<T>()` | Use untyped runtime props or mutate props directly |
| Use `computed` for derived values | Use `watch` to mirror values that can be derived |
| Use stable domain keys in `v-for` | Use array indexes for reorderable or mutable lists |
| Use `onWatcherCleanup` or `onCleanup` for async effects | Let stale fetches, timers, or listeners leak |
| Use `storeToRefs()` when destructuring Pinia stores | Destructure stores directly and lose reactivity |
| Use semantic HTML and labels | Rely on ARIA to replace native semantics |
| Code-split routes and virtualize long lists when needed | Add unbounded deep reactivity over large datasets |
| Use `VITE_` only for intentional public env vars | Put secrets in client-side code |

## Checklist Before Opening a PR

- [ ] SFC order, component naming, and TypeScript contracts follow the conventions above.
- [ ] Compiler macros are typed and props are not mutated directly.
- [ ] Reactivity uses `ref`, `reactive`, `computed`, `watch`, cleanup, and destructuring helpers correctly.
- [ ] Templates have stable keys, no same-element `v-if` plus `v-for`, and no heavy inline logic.
- [ ] Composables clean up effects and expose async work as actions.
- [ ] Pinia stores, routes, navigation guards, and route metadata are typed and SSR-safe where applicable.
- [ ] Forms validate on the client for UX and on the server for trust.
- [ ] Accessibility, security, performance, SSR, tests, `vue-tsc`, ESLint, and Prettier expectations are satisfied.

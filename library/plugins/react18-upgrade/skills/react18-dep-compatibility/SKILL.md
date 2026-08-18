---
name: react18-dep-compatibility
description: >-
  Check React 18.3.1 and React 19 dependency compatibility before npm installs, peer-dependency resolutions, or upgrade plans. Use when reviewing a React upgrade matrix, resolving npm peer conflicts, choosing minimum compatible package versions, deciding on --legacy-peer-deps, or separating a react-router v5 to v6 migration.
---

# React dependency compatibility

Review this matrix before `npm install`. Map installed React ecosystem packages to the minimum versions known to work with React 18.3.1 or React 19, then recommend safe upgrade, migration, or documented peer-dependency exception paths without hiding real concurrent-rendering risks.

## When to invoke

- "Review this dependency matrix before I run npm install for React 18."
- "Can I use --legacy-peer-deps for this React peer conflict?"
- "What versions of Testing Library, Apollo, Emotion, and Redux do I need for React 19?"
- "Assess the risk of migrating react-router v5 to v6."
- "Resolve npm peer dependency conflicts during a React upgrade."

## Prerequisites and context

- Inspect `package.json`, lockfiles, and npm conflict output before recommending versions.
- Prefer package-specific minimum compatible versions over blanket `--legacy-peer-deps`.
- Treat `react-router` v5 to v6 as a `SEPARATE` migration sprint, not a peer-dependency cleanup.
- Read `references/apollo-details.md` for Apollo concurrent mode and `MockedProvider` changes when Apollo is present.
- Read `references/router-migration.md` before changing route definitions or navigation code.

## Core compatibility matrix

| Package | React 17 current | React 18.3.1 minimum | React 19 minimum | Notes |
| --- | --- | --- | --- | --- |
| `react` | 17.x | `18.3.1` | `19.0.0` | Pin exactly to `18.3.1` for the R18 orchestra. |
| `react-dom` | 17.x | `18.3.1` | `19.0.0` | Must match `react` exactly. |

| Area | Package | React 18 minimum | React 19 minimum | Compatibility rule |
| --- | --- | --- | --- | --- |
| Testing | `@testing-library/react` | `14.0.0` | `16.0.0` | RTL 13 uses `ReactDOM.render` internally and is broken for React 18 roots. |
| Testing | `@testing-library/jest-dom` | `6.0.0` | `6.0.0` | v5 works in many cases, but v6 carries React 18 matcher updates. |
| Testing | `@testing-library/user-event` | `14.0.0` | `14.0.0` | v13 is mostly sync; v14 is async and requires `await user.click(...)`. |
| Testing | `jest` | `27.x` | `27.x` | Use Jest 27+ with jsdom 16+ for React 18. |
| Testing | `jest-environment-jsdom` | `27.x` | `27.x` | Keep this package aligned with `jest`. |
| Apollo | `@apollo/client` | `3.8.0` | `3.11.0` | 3.8 adds `useSyncExternalStore` for concurrent mode. |
| Apollo | `graphql` | `15.x` | `16.x` | Apollo 3.8+ peers allow GraphQL 15 or 16; verify installed peer range. |
| Emotion | `@emotion/react` | `11.10.0` | `11.13.0` | 11.10 adds React 18 concurrent mode support. |
| Emotion | `@emotion/styled` | `11.10.0` | `11.13.0` | Match `@emotion/react`. |
| Emotion | `@emotion/cache` | `11.10.0` | `11.13.0` | Upgrade when used directly. |
| Router | `react-router-dom` | `v6.0.0` | `v6.8.0` | v5 to v6 is breaking; read `references/router-migration.md`. |
| Router | `react-router-dom` v5 | `5.3.4` workaround | Not supported | Legacy peer workaround only; not a React 19 path. |
| Redux | `react-redux` | `8.0.0` | `9.0.0` | v7 works only on legacy roots and can break concurrent mode. |
| Redux | `redux` | `4.x` | `5.x` | Redux core is framework-agnostic; `react-redux` is the key package. |
| Redux | `@reduxjs/toolkit` | `1.9.0` | `2.0.0` | RTK 1.9 is tested against React 18. |
| Data fetching | `react-query` / `@tanstack/react-query` | `4.0.0` | `5.0.0` | v3 does not support concurrent mode. |
| Forms | `react-hook-form` | `7.0.0` | `7.43.0` | v6 has concurrent mode issues. |
| Forms | `formik` | `2.2.9` | `2.4.0` | v2.2.9 patched React 18 issues. |
| UI input | `react-select` | `5.0.0` | `5.8.0` | v4 commonly conflicts with React 18 peers. |
| Date input | `react-datepicker` | `4.8.0` | `6.0.0` | v4.8+ added React 18 support. |
| Drag/drop | `react-dnd` | `16.0.0` | `16.0.0` | v15 and below have React 18 concurrent mode issues. |
| Runtime types | `prop-types` | any | any | Standalone package; unaffected by React version. |

## Conflict resolution decision tree

```text
npm ls shows peer conflict for package X
        │
        ▼
Does package X have a version that supports the target React version?
  YES → install X@<min-compatible-version> and rerun npm install
  NO  ↓
        │
Is package X critical to the app?
  YES → check GitHub issues for a React 18/19 `branch/fork`, or maintainer PR
      → last resort: --legacy-peer-deps with documented reason
  NO  → remove or replace the package
```

Use `npm ls <package>`, `npm explain <package>`, and the lockfile to find the real peer owner before changing top-level dependencies.

## `--legacy-peer-deps` rules

Only use `--legacy-peer-deps` when all of these are true:

- The package has no compatible release for the target React version.
- The package is actively maintained or has a credible near-term fix.
- The conflict is only a peer-dependency declaration mismatch, not a real API or concurrent-mode incompatibility.
- The use is documented in `package.json` comments where allowed by tooling, or in `MIGRATION.md`, with the package name, conflict, risk, and removal plan.

Never use `--legacy-peer-deps` to skip Testing Library, Apollo, Redux, router, or ReactDOM API incompatibilities that have known migration paths.

## Progressive disclosure and bundled resources

| Resource | Use when |
| --- | --- |
| `references/apollo-details.md` | Apollo Client, `MockedProvider`, cache, or concurrent mode behavior is in scope. |
| `references/router-migration.md` | Any `react-router-dom` v5 to v6 route, hook, redirect, or navigation change is in scope. |

## Gotchas

- **React and ReactDOM must match exactly**: mismatched minor or major versions create misleading runtime and test failures.
- **Testing Library upgrades change APIs**: `@testing-library/user-event` v14 actions are async; update tests with `await`.
- **Router migration is not just a version bump**: `Switch`, `Redirect`, route props, and history patterns need code changes.
- **Peer conflicts can be stale metadata**: verify whether the package actually calls removed ReactDOM APIs before accepting an exception.

## Output template

```markdown
## React dependency compatibility result

**Status:** compatible | changes required | blocked
**Target React version:** React 18.3.1 | React 19
**Package manager evidence:** `<package.json / lockfile / npm output reviewed>`

| Package | Current | Required minimum | Action | Reason |
| --- | --- | --- | --- | --- |
| `<package>` | `<version>` | `<version>` | upgrade | <compatibility reason> |

### Exceptions
- `<package>`: `--legacy-peer-deps` allowed | not allowed — <reason and removal plan>
```

## Quality gate

- [ ] `react` and `react-dom` are pinned to the same target version.
- [ ] Every listed dependency was compared against the React 18.3.1 or React 19 minimum matrix.
- [ ] `--legacy-peer-deps` is recommended only with a documented package-specific reason.
- [ ] `react-router-dom` v5 to v6 work is called out as a separate migration when present.
- [ ] Apollo and router bundled references are used when those packages are in scope.
- [ ] The output follows `## Output template` exactly.

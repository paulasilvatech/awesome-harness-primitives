---
description: "Defines the SIFAP Next.js 15, React 19, strict TypeScript, accessibility, session, and sensitive-data UI baseline. Use when editing frontend application source."
applyTo: "frontend/**/*.ts,frontend/**/*.tsx,frontend/**/*.css,frontend/package.json,frontend/next.config.*"
---

# SIFAP frontend conventions - Accessible server-first UI

These instructions apply to the workshop Next.js 15 App Router and React 19 compatibility baseline. They
are authoritative for server/client boundaries, strict typing, accessibility, and data exposure; the
approved UX artifacts and requirements define actual screens and flows.

## Component and data boundaries

- Use Server Components by default and keep client islands as small as practical.
- Authorize Server Actions and route handlers as public entry points; never rely on hidden UI alone.
- Verify and decrypt session state. The presence of a cookie is not authentication.
- Keep secrets and privileged backend calls on the server.
- Represent loading, empty, error, success, and permission-denied states explicitly.

## UI and accessibility

- Meet WCAG 2.2 AA for the implemented flow and test keyboard, focus, labels, errors, and announcements.
- Use semantic HTML before ARIA and do not use color as the only signal.
- Use strict TypeScript without `any` or suppressed errors; follow App Router export requirements.
- Mask CPF and financial values unless an approved requirement and authorization allow display.
- Follow the repository's established design system; do not invent a competing visual stack.

## Conventions

| Rule | Rationale |
| --- | --- |
| Server-first rendering is the default | Secrets and data access stay out of the client bundle. |
| Authorization runs close to data and mutations | Route hiding alone cannot protect resources. |
| WCAG 2.2 AA is the accessibility baseline | New flows include current keyboard and interaction requirements. |
| Explicit UI states are required | Users are not left with blank or ambiguous outcomes. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use verified session helpers and a DAL | Trust any cookie named `session` |
| Test behavior by role and label | Depend on snapshot-only tests |
| Use approved design tokens and components | Add an unapproved state or UI library |
| Format values with explicit locale rules | Expose raw regulated values |

## Checklist Before Opening a PR

- [ ] Server/client boundaries and authorization are explicit and tested.
- [ ] Strict TypeScript passes with no `any` or suppression.
- [ ] Loading, empty, error, success, and denied states are handled.
- [ ] The flow meets applicable WCAG 2.2 AA keyboard and screen-reader behavior.
- [ ] Sensitive data is masked or access-gated by an approved requirement.
- [ ] Vitest/Testing Library and the production build pass for the changed slice.

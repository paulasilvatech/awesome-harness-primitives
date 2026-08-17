---
applyTo: "**/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.css,**/*.scss,**/*.json"
description: "Enforces TanStack Start, React, Shadcn/ui, Tailwind CSS, Zod, routing, data fetching, accessibility, and import conventions."
---

# TanStack Start Conventions — Shadcn Tailwind Applications

These instructions apply to files matched by `**/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.css,**/*.scss,**/*.json`. They are authoritative for tanstack start code, configuration, examples, validation commands, API names, and runtime constraints in those files; stricter repository-specific security, deployment, testing, or platform primitives win on conflict. Treat the rules as passive conventions injected into matching files, not as a step-by-step workflow.

Use strict TypeScript and modern React patterns for TanStack Start applications.

## Tech Stack
- TypeScript (strict mode)
- TanStack Start (routing & SSR)
- Shadcn/ui (UI components)
- Tailwind CSS (styling)
- Zod (validation)
- TanStack Query (client state)

## Code Style Rules

- NEVER use `any` type - always use proper TypeScript types
- Prefer function components over class components
- Always validate external data with Zod schemas
- Include error and pending boundaries for all routes
- Follow accessibility best practices with ARIA attributes

## Component Patterns

Use function components with proper TypeScript interfaces:

```typescript
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export default function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} className={cn(buttonVariants({ variant }))}>
      {children}
    </button>
  );
}
```

## Data Fetching

Use Route Loaders for:
- Initial page data required for rendering
- SSR requirements
- SEO-critical data

Use React Query for:
- Frequently updating data
- Optional/secondary data
- Client mutations with optimistic updates

```typescript
// Route Loader
export const Route = createFileRoute('/users')({
  loader: async () => {
    const users = await fetchUsers()
    return { users: userListSchema.parse(users) }
  },
  component: UserList,
})

// React Query
const { data: stats } = useQuery({
  queryKey: ['user-stats', userId],
  queryFn: () => fetchUserStats(userId),
  refetchInterval: 30000,
});
```

## Zod Validation

Always validate external data. Define schemas in `src/lib/schemas.ts`:

```typescript
export const userSchema = z.object({
  id: z.string(),
  name: z.string().min(1).max(100),
  email: z.string().email().optional(),
  role: z.enum(['admin', 'user']).default('user'),
})

export type User = z.infer<typeof userSchema>

// Safe parsing
const result = userSchema.safeParse(data)
if (!result.success) {
  console.error('Validation failed:', result.error.format())
  return null
}
```

## Routes

Structure routes in `src/routes/` with file-based routing. Always include error and pending boundaries:

```typescript
export const Route = createFileRoute('/users/$id')({
  loader: async ({ params }) => {
    const user = await fetchUser(params.id);
    return { user: userSchema.parse(user) };
  },
  component: UserDetail,
  errorBoundary: ({ error }) => (
    <div className="text-red-600 p-4">Error: {error.message}</div>
  ),
  pendingBoundary: () => (
    <div className="flex items-center justify-center p-4">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
    </div>
  ),
});
```

## UI Components

Always prefer Shadcn/ui components over custom ones:

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>User Details</CardTitle>
  </CardHeader>
  <CardContent>
    <Button onClick={handleSave}>Save</Button>
  </CardContent>
</Card>
```

Use Tailwind for styling with responsive design:

```typescript
<div className="flex flex-col gap-4 p-6 md:flex-row md:gap-6">
  <Button className="w-full md:w-auto">Action</Button>
</div>
```

## Accessibility

Use semantic HTML first. Only add ARIA when no semantic equivalent exists:

```typescript
//  Good: Semantic HTML with minimal ARIA
<button onClick={toggleMenu}>
  <MenuIcon aria-hidden="true" />
  <span className="sr-only">Toggle Menu</span>
</button>

//  Good: ARIA only when needed (for dynamic states)
<button
  aria-expanded={isOpen}
  aria-controls="menu"
  onClick={toggleMenu}
>
  Menu
</button>

//  Good: Semantic form elements
<label htmlFor="email">Email Address</label>
<input id="email" type="email" />
{errors.email && (
  <p role="alert">{errors.email}</p>
)}
```

## File Organization

```
src/
├── components/ui/    # Shadcn/ui components
├── lib/schemas.ts    # Zod schemas
├── routes/          # File-based routes
└── routes/api/      # Server routes (.ts)
```

## Import Standards

Use `@/` alias for all internal imports:

```typescript
//  Good
import { Button } from '@/components/ui/button'
import { userSchema } from '@/lib/schemas'

//  Bad
import { Button } from '../components/ui/button'
```

## Adding Components

Install Shadcn components when needed:

```bash
npx shadcn@latest add button card input dialog
```

## Common Patterns

- Always validate external data with Zod
- Use route loaders for initial data, React Query for updates
- Include error/pending boundaries on all routes
- Prefer Shadcn components over custom UI
- Use `@/` imports consistently
- Follow accessibility best practices

## Good / Bad Examples

The examples below show the boundary between an acceptable convention and the closest common anti-pattern.

**Good:**

```typescript
export const Route = createFileRoute('/users')({
  loader: async () => ({ users: userListSchema.parse(await fetchUsers()) }),
  component: UserList,
  errorBoundary: ({ error }) => <ErrorState message={error.message} />,
  pendingBoundary: () => <Spinner aria-label="Loading users" />,
});
```

Why: The route validates loader data and defines pending and error boundaries.

**Bad:**

```typescript
export const Route = createFileRoute('/users')({
  component: () => <Users data={(window as any).users} />,
});
```

Why: The route relies on `any`, global data, and no loading or error state.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use strict TypeScript with no `any`, function components, typed props, and `@/` imports. | Static types and stable imports make refactors safer. |
| Use route loaders for SSR data and TanStack Query for updates. | Data ownership matches render timing. |
| Validate external data with Zod schemas in `src/lib/schemas.ts`. | Runtime validation protects typed state. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use strict TypeScript with no `any`, function components, typed props, and `@/` imports. | Do not ignore this rule: Use strict TypeScript with no `any`, function components, typed props, and `@/` imports. |
| Use route loaders for SSR data and TanStack Query for updates. | Do not ignore this rule: Use route loaders for SSR data and TanStack Query for updates. |
| Validate external data with Zod schemas in `src/lib/schemas.ts`. | Do not ignore this rule: Validate external data with Zod schemas in `src/lib/schemas.ts`. |

## Checklist Before Opening a PR

- [ ] The change stays inside the matched `applyTo` scope.
- [ ] The authoritative conventions above are applied to new or modified code.
- [ ] Named commands, paths, API names, configuration keys, and version constraints remain intact.
- [ ] Relevant validation, linting, build, or test commands from this instruction pass.
- [ ] No secrets, unsupported APIs, placeholder prompt references, or relative primitive links were added.

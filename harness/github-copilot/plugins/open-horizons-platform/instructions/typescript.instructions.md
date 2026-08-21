---
applyTo: "**/*.ts,**/*.tsx"
description: "Use when editing Open Horizons Backstage TypeScript packages, React pages, plugins, API clients, and tests."
---

# TypeScript Conventions — Backstage App, Plugins, and API Clients

This file activates when you edit TypeScript or TSX files in the Backstage workspace and related plugin packages. It teaches Open Horizons conventions for Backstage routes, plugin registration, React components, typed API clients, SSE parsing, package scripts, and validation. It does **not** cover container packaging for TypeScript services, which belongs to the `dockerfile` instructions, local service orchestration, which belongs to the `docker-compose` instructions, Python agent APIs consumed by Backstage, which belong to the `python` instructions, or Kubernetes runtime manifests, which belong to the `kubernetes` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: "**/*.ts,**/*.tsx"` for existing local patterns.
2. This `typescript` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for typescript conventions — backstage app, plugins, and api clients. Use the `backstage-deployment` and `test-coverage` skills for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!NOTE]
> The Backstage workspace uses Node `22 || 24`, Yarn `4.4.1`, TypeScript `~5.8.0`, React 18, and Backstage CLI lint, build, and test commands from `backstage/package.json`.

## Backstage Routes and Plugins

Register app routes through `createApp`, `FlatRoutes`, route refs, and Backstage plugin pages. Keep backend plugin registration in the backend package.

```tsx
// Wrong: bypasses Backstage routing and app composition.
window.location.href = '/ai-chat';
```

```tsx
const routes = (
  <FlatRoutes>
    <Route path="/ai-chat" element={<AiChatPage />} />
    <Route path="/catalog" element={<CatalogIndexPage />} />
  </FlatRoutes>
);
```

## React Components

Use function components, typed props, and existing Backstage and Material UI v4 patterns. Keep shared visual components under `backstage/packages/app/src/components/shared` when they are reused.

```tsx
// Wrong: untyped props and class component for new UI.
class StatusCard extends React.Component<any> {
  render() {
    return <div>{this.props.status}</div>;
  }
}
```

```tsx
interface StatusCardProps {
  title: string;
  status: 'healthy' | 'degraded' | 'down';
}

export function StatusCard({ title, status }: StatusCardProps) {
  return <StyledCard title={title}>{status}</StyledCard>;
}
```

> [!WARNING]
> Do not hardcode secrets, customer endpoints, PATs, or Azure OpenAI keys in frontend or backend TypeScript. Route backend calls through Backstage proxy or configuration.

## API Clients and SSE Parsing

Use typed payloads, `credentials: 'include'`, `response.ok` checks, and defensive stream parsing. The AI Chat service parses `data: ` lines and ignores incomplete buffered JSON.

```ts
// Wrong: untyped fetch, no credentials, no response check.
const data = await fetch('/api/proxy/agent-api/api/agents/info').then(r => r.json());
```

```ts
export async function fetchSystemInfo(): Promise<SystemInfo> {
  const res = await fetch(`${AGENT_API_BASE}/api/agents/info`, {
    credentials: 'include',
  });
  if (!res.ok) throw new Error(`Info API error: ${res.status}`);
  return res.json();
}
```

## Type Safety

Prefer exported interfaces for API contracts and `Record<string, unknown>` for untrusted tool inputs. Avoid `any`; if an integration requires a local cast, explain why nearby.

```ts
// Wrong: any spreads untrusted tool input through the app.
export interface ToolCall {
  name: string;
  input: any;
}
```

```ts
export interface ToolCall {
  name: string;
  input: Record<string, unknown>;
  result?: string;
}
```

> [!IMPORTANT]
> Keep TypeScript source under paths included by `backstage/tsconfig.json`: `packages/*/src`, `plugins/*/src`, plugin `dev`, `migrations`, or `config.d.ts`.

## Formatting and Validation

Use Backstage CLI and workspace commands. Do not add unrelated ESLint or Prettier configurations; the root Backstage package already delegates Prettier to `@backstage/cli/config/prettier`.

```bash
# Wrong: one-off formatter outside the workspace configuration.
npx prettier --write backstage/packages/app/src/App.tsx
```

```bash
cd backstage
yarn workspace app lint
yarn workspace app test
yarn build:all
```

## Conventions

| Rule | Rationale |
|---|---|
| Keep TypeScript in Backstage workspace `packages/*` and `plugins/*` source paths | The repo `tsconfig.json` and Backstage CLI only include those locations. |
| Register UI through Backstage app and plugin APIs | App composition, permissions, and navigation stay consistent. |
| Use typed interfaces for API payloads and SSE chunks | Frontend and FastAPI contracts remain reviewable. |
| Use `credentials: 'include'` for Backstage-proxied API calls | Authenticated Backstage sessions must flow to backend routes. |
| Check `response.ok` and missing stream bodies before parsing | User-facing errors are clearer and stream clients avoid null dereferences. |
| Use Backstage CLI lint, test, and build scripts | Validation matches the repository toolchain. |

## Do / Do Not

| Do | Do not |
|---|---|
| Prefer function components and hooks | Add new class components. |
| Keep plugin-specific UI inside the plugin package | Put every page in the app package by default. |
| Use `Record<string, unknown>` for untrusted tool data | Use `any` across API boundaries. |
| Run targeted workspace checks before broad builds | Add new lint or formatter tools for a single change. |

## Checklist Before Opening a PR

- [ ] Code lives under a package or plugin path included by `backstage/tsconfig.json`.
- [ ] Routes and plugin registrations use Backstage APIs.
- [ ] API clients are typed, check `response.ok`, and include credentials when proxied.
- [ ] No secrets or tenant-specific endpoints are hardcoded.
- [ ] Existing Backstage lint, test, or build commands are used for validation where feasible.
- [ ] Shared UI is placed in shared components only when reused.

---
applyTo: "**/*.ts,**/*.js,**/host.json,**/local.settings.json,**/function.json,**/package.json"
description: "Conventions for Azure Functions apps in TypeScript and JavaScript, including Node.js async patterns, dependency choices, function layout, and API documentation."
---

# Azure Functions TypeScript Conventions — Node.js APIs

These instructions apply to Azure Functions TypeScript and JavaScript source, host configuration, local settings, function metadata, and package manifests. They are authoritative for Node.js coding style, dependency choices, function file layout, `@azure/functions@4` usage, and API documentation expectations in matched files; project-specific API contracts, security policies, and deployment conventions win when they impose stricter requirements.

## Runtime and Language Style

Generate modern TypeScript code for Node.js and keep the event loop non-blocking.

- Use `async/await` for asynchronous code instead of callback pyramids or promise chains that obscure control flow.
- Use Node.js async APIs, especially `node:fs/promises` instead of `fs`, when file access is required.
- Avoid blocking the event loop with synchronous file, crypto, compression, process, or network operations inside a function invocation.
- Prefer TypeScript types for request bodies, route parameters, query values, and response payloads so function boundaries stay explicit.
- Keep JavaScript changes consistent with the TypeScript conventions when a project intentionally uses `.js` files.

## Dependencies and Built-in Modules

Whenever possible, use Node.js v22 LTS built-in modules instead of external packages.

| Need | Preferred choice | Rationale |
| --- | --- | --- |
| File system | `node:fs/promises` | Async built-in APIs avoid blocking and do not add dependencies. |
| URLs and query parsing | `node:url` and standard `URL` APIs | Built-in parsing is portable and maintained with Node.js. |
| Crypto | `node:crypto` async or Web Crypto APIs | Built-in primitives reduce supply-chain risk. |
| HTTP clients | Built-in `fetch` when it satisfies the requirement | Avoids unnecessary HTTP client dependencies. |
| Extra packages | Ask before adding any extra dependencies | Dependencies affect cold start, security review, licensing, and deployment size. |

Do not add a dependency for functionality already covered by stable Node.js v22 LTS APIs unless the project owner accepts the tradeoff.

## Function App Structure

The API is built using Azure Functions with the `@azure/functions@4` package.

- Put each endpoint in its own function file.
- Name endpoint files with `src/functions/<resource-name>-<http-verb>.ts` so routing intent is visible in the file tree.
- Keep trigger registration, request parsing, validation handoff, business call, and response shaping easy to follow in each file.
- Share reusable business logic through services or modules outside the function entry file rather than duplicating it across endpoints.
- Keep `host.json`, `local.settings.json`, `function.json`, and `package.json` changes consistent with the runtime model and deployment target.

## API Contracts and Documentation

When making changes to the API, update the OpenAPI schema if it exists and update `README.md` accordingly.

| Change | Required documentation |
| --- | --- |
| New endpoint | OpenAPI path, request schema, response schema, status codes, authentication notes, and `README.md` usage notes. |
| Changed request or response | OpenAPI schema and examples, plus `README.md` migration or usage details. |
| Removed endpoint or behavior | OpenAPI removal or deprecation note and `README.md` compatibility note. |
| Configuration change | `README.md` local setup and environment variable guidance; do not commit secrets in `local.settings.json`. |

## Good / Bad Examples

The examples below illustrate async Node.js and one-file-per-endpoint conventions.

**Good:**

```ts
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions"
import { readFile } from "node:fs/promises"

export async function productsGet(request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> {
  const body = await readFile("config/products.json", "utf8")
  return { status: 200, jsonBody: JSON.parse(body) }
}

app.http("products-get", {
  methods: ["GET"],
  authLevel: "function",
  route: "products",
  handler: productsGet,
})
```

Why: The endpoint uses `@azure/functions@4`, async file I/O, clear response typing, and a handler name that matches `src/functions/<resource-name>-<http-verb>.ts`.

**Bad:**

```ts
import { app } from "@azure/functions"
import fs from "fs"

app.http("products", {
  methods: ["GET", "POST", "DELETE"],
  handler: () => ({ body: fs.readFileSync("config/products.json", "utf8") }),
})
```

Why: The function combines multiple endpoints, uses blocking `fs` I/O, and hides request-specific behavior in one broad handler.

## Conventions

| Rule | Rationale |
| --- | --- |
| Generate modern TypeScript for Node.js | Function code remains maintainable and type-checkable |
| Use `async/await` and async Node.js APIs such as `node:fs/promises` | Invocations do not block the event loop while waiting on I/O |
| Prefer Node.js v22 LTS built-in modules over external packages | Built-ins reduce cold start, deployment size, licensing, and supply-chain risk |
| Ask before adding extra dependencies | Dependency changes are product and operations decisions, not formatting choices |
| Use `@azure/functions@4` for the Azure Functions API model | The code matches the current package expected by the project |
| Put each endpoint in `src/functions/<resource-name>-<http-verb>.ts` | Endpoint ownership, routing, and review scope stay obvious |
| Update OpenAPI schema and `README.md` when the API changes | Consumers and contributors keep an accurate contract and usage guide |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `async/await` with non-blocking Node.js APIs | Use synchronous `fs` or other blocking APIs inside function invocations |
| Prefer `node:fs/promises`, `node:url`, `node:crypto`, and built-in `fetch` when sufficient | Add packages for functionality already provided by Node.js v22 LTS |
| Ask before adding dependencies | Add convenience dependencies without approval |
| Create one function file per endpoint using `src/functions/<resource-name>-<http-verb>.ts` | Put unrelated HTTP verbs or resources into one catch-all function file |
| Use `@azure/functions@4` imports and registration style | Mix old programming models without a migration reason |
| Update OpenAPI and `README.md` for API changes | Ship endpoint changes with stale schema or usage documentation |

## Checklist Before Opening a PR

- [ ] TypeScript or JavaScript code uses modern Node.js async patterns and `async/await`.
- [ ] File, network, crypto, and other I/O work avoids blocking APIs such as synchronous `fs` calls.
- [ ] Node.js v22 LTS built-in modules are used where they satisfy the requirement.
- [ ] Any new dependency was explicitly approved.
- [ ] Azure Functions code uses `@azure/functions@4` conventions.
- [ ] Each endpoint has its own file named `src/functions/<resource-name>-<http-verb>.ts`.
- [ ] API changes update the OpenAPI schema when present and update `README.md`.
- [ ] Configuration changes avoid committing secrets in `local.settings.json`.

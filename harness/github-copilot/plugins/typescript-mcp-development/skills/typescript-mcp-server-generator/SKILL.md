---
name: "typescript-mcp-server-generator"
description: >-
  Generate complete TypeScript MCP server projects with MCP TypeScript SDK v2 packages, tools, resources, prompts, transports, configuration, testing, migration guidance, and documentation. Use this skill when the user asks to generate a TypeScript MCP server, create an MCP tool server, migrate an MCP server from v1 to v2, or choose stdio versus HTTP transport.
---

# TypeScript MCP server generator

Generate a production-ready Model Context Protocol server in TypeScript using MCP TypeScript SDK v2, explicit transport selection, full Zod schemas, typed tool handlers, and runnable project commands.

## When to invoke

- "Generate a TypeScript MCP server."
- "Create an MCP server with tools and resources."
- "Build an HTTP MCP server in Node."
- "Migrate this MCP server from v1 to v2."
- "Add stdio transport to a TypeScript MCP project."

## Prerequisites and context

- Target Node.js `20+` and ESM-first TypeScript with `"type": "module"`.
- Use MCP TypeScript SDK v2 focused packages; the v1 monolithic `@modelcontextprotocol/sdk` package is retired.
- Choose either HTTP Streamable HTTP transport or stdio. SSE and WebSocket transports were removed in v2 and must not be generated.

## Package and runtime choices

| Need | Package or setting | Notes |
| --- | --- | --- |
| Server implementation | `@modelcontextprotocol/server` | Provides `McpServer`; stdio transport is under `@modelcontextprotocol/server/stdio`. |
| Plain Node HTTP | `@modelcontextprotocol/node` | Use `NodeStreamableHTTPServerTransport`. |
| Framework HTTP | `@modelcontextprotocol/express`, `@modelcontextprotocol/hono`, or `@modelcontextprotocol/fastify` | Install the peer framework too, such as `@modelcontextprotocol/express` + `express`. |
| Web Standard runtimes | `@modelcontextprotocol/server` | Use `WebStandardStreamableHTTPServerTransport`. |
| Shared protocol schemas | `@modelcontextprotocol/core` | Import `*Schema` constants from here, not from `sdk/types.js`. |
| Validation | `zod@^4.2` | v2 requires Zod 4.2+; do not use `zod@3`. |
| Development runner | `tsx` or `ts-node` | Prefer `tsx` for ESM development. |
| Module system | `"type": "module"` | CommonJS is shipped, so `require()` works if needed, but new projects should be ESM-first. |

## Project structure

```text
mcp-server/
├── package.json
├── tsconfig.json
├── .gitignore
├── README.md
└── src/
    ├── index.ts
    ├── server.ts
    ├── tools/
    │   └── greet.ts
    ├── resources/
    ├── prompts/
    └── config.ts
```

Initialize with `npm init`, install runtime dependencies such as `@modelcontextprotocol/server`, `zod@^4.2`, and the chosen transport package, then add dev dependencies such as `tsx` and `typescript`.

## Server implementation rules

| Concern | Rule |
| --- | --- |
| Server | Use `McpServer` from `@modelcontextprotocol/server`; set server name and version. |
| Tool registration | Use `registerTool()` with a config object; v1 variadic `.tool()` signatures are gone. |
| Tool schemas | Use complete Zod objects such as `z.object({ name: z.string() })`; raw shape objects are deprecated. |
| Tool metadata | Provide clear `title` and `description` fields. |
| Tool result | Return `content` and `structuredContent` where structured data exists. |
| Handler context | Use the second structured `ctx` parameter: `ctx.mcpReq.signal`, `ctx.mcpReq.id`, `ctx.mcpReq.send(...)`, `ctx.mcpReq.notify(...)`. |
| HTTP headers | v2 uses Web Standard `Headers`/`Request`; read headers with `ctx.http?.req?.headers.get('x-custom')`. |
| Errors | Use `ProtocolError`, `SdkError`, and `SdkHttpError` with `.status`; do not use v1 `McpError`, `ErrorCode`, or `StreamableHTTPError`. |
| Cleanup | Handle transport close events and async resource cleanup. |
| Configuration | Use environment variables for ports, API keys, and feature switches. |

```typescript
server.registerTool('greet', {
  title: 'Greet user',
  description: 'Greet user',
  inputSchema: z.object({ name: z.string() })
}, async ({ name }, ctx) => {
  return {
    content: [{ type: 'text', text: `Hello, ${name}!` }],
    structuredContent: { greeting: `Hello, ${name}!`, requestId: ctx.mcpReq.id }
  };
});
```

## Resources, prompts, and advanced features

| Feature | Rule |
| --- | --- |
| Resources | Add `registerResource()` with `ResourceTemplate` for dynamic URIs. |
| Prompts | Add `registerPrompt()` with argument schemas in the same config-object style as `registerTool()`. |
| Completion | Use `completable(z.string(), callback).optional()`; apply `.optional()` outside the `completable()` wrapper. |
| LLM-assisted tools | Use the multi-round `input_required` pattern; the v2 sampling subsystem is deprecated. |
| Dynamic tools | Support enable/disable capabilities and notification debouncing for bulk updates when needed. |
| Resource links | Prefer links for large data references instead of embedding bulky content in tool responses. |

## Transport configuration

| Transport | Use when | Required details |
| --- | --- | --- |
| HTTP | Browser, remote, or multi-client usage. | Port from environment, CORS if browser clients need it, stateless versus stateful sessions, DNS rebinding protection for local servers, strict `Content-Type` handling because v2 rejects non-`application/json` POST bodies, and connection URL `http://localhost:PORT/mcp`. |
| stdio | Local editor or CLI host launches the server process. | Clean stdin/stdout handling, logs on stderr, environment-based config, and process lifecycle management. |

## Migration from v1

1. Run the official codemod:

   ```bash
   npx @modelcontextprotocol/codemod@latest v1-to-v2 .
   ```

2. Search for `@mcp-codemod-error` markers that need manual judgment.
3. Choose the v2 transport; do not recreate SSE or WebSocket.
4. Replace `McpError + ErrorCode` checks with `ProtocolError`, `SdkError`, or `SdkHttpError`; HTTP status is `error.status`, not `error.code`.
5. Remove deprecated `Server.createMessage()`, `listRoots()`, `sendLoggingMessage()`, and `roots`/`sampling`/`logging` capability fields from new code.

## Testing guidance

- Add scripts for `npm start`, `npm run dev`, `npm run build`, and `npm test` when the generated project includes tests.
- Run the server with `npm start` or `npx tsx src/index.ts`.
- Inspect with `npx @modelcontextprotocol/inspector`.
- Include example tool invocations and expected `content`/`structuredContent` output in `README.md`.

Resource/Prompt generation may be included when useful. Stdio examples should import `StdioServerTransport`; stdio-based servers must keep stdout protocol-clean. Use TypeScript/Node.js project defaults, high-level `McpServer` APIs, async/await, and try-catch around external work. Remember that v1 called the handler context `extra`; v2 replaces it with `ctx`. Install adapter peers explicitly, for example `npm install @modelcontextprotocol/express express`. Migration command spelling must remain `npx @modelcontextprotocol/codemod@latest v1-to-v2 .`. A simple development command may be `npx tsx server.ts`. Schema examples may be shown as `z.object({...})`; do not pass raw `{ name: z.string() }` shapes.

## Output template

```markdown
## TypeScript MCP server result

**Status:** generated | migrated | blocked
**Transport:** http | stdio
**Runtime:** Node.js 20+

| Artifact | Path | Notes |
| --- | --- | --- |
| Package config | `package.json` | `<dependencies/scripts>` |
| Server entry | `src/index.ts` | `<transport>` |
| Tools | `src/tools/<tool>.ts` | `<schemas/results>` |
| Docs | `README.md` | `<run and inspector commands>` |

**Commands**
- `npm install ...`: <pass/fail/not run>
- `npm run build`: <pass/fail/not run>
- `npx @modelcontextprotocol/inspector`: <usage documented/not run>
```

## Quality gate

- [ ] Project uses Node.js `20+`, TypeScript, and `"type": "module"` unless the user requested otherwise.
- [ ] v2 packages are used: `@modelcontextprotocol/server`, transport package, `@modelcontextprotocol/core` when schemas are needed, and `zod@^4.2`.
- [ ] No new SSE, WebSocket, v1 `.tool()` signatures, raw schema shapes, `McpError`, `ErrorCode`, `StreamableHTTPError`, `Server.createMessage()`, `listRoots()`, `sendLoggingMessage()`, `roots`, `sampling`, or `logging` capability fields are generated.
- [ ] At least one useful tool has a full Zod input schema, error handling, `content`, and `structuredContent`.
- [ ] Transport configuration includes lifecycle, environment, and HTTP/stdout details.
- [ ] README includes run commands, MCP Inspector command, HTTP URL when relevant, and example tool invocations.

---
paths:
  - "**/*.ts"
  - "**/*.js"
  - "**/package.json"
---

<!-- Generated from harness/github-copilot/instructions/typescript-mcp-server.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Model Context Protocol TypeScript SDK conventions for tools, resources, prompts, transports, schemas, errors, and testing.

# TypeScript MCP Server Conventions — SDK Servers

These instructions apply to files matched by `**/*.ts,**/*.js,**/package.json`. They are authoritative for typescript mcp server code, configuration, examples, validation commands, API names, and runtime constraints in those files; stricter repository-specific security, deployment, testing, or platform primitives win on conflict. Treat the rules as passive conventions injected into matching files, not as a step-by-step workflow.

## SDK Registration and Capabilities

- Use the **@modelcontextprotocol/sdk** npm package: `npm install @modelcontextprotocol/sdk`
- Import from specific paths: `@modelcontextprotocol/sdk/server/mcp.js`, `@modelcontextprotocol/sdk/server/stdio.js`, etc.
- Use `McpServer` class for high-level server implementation with automatic protocol handling
- Use `Server` class for low-level control with manual request handlers
- Use **zod** for input/output schema validation: `npm install zod@3`
- Always provide `title` field for tools, resources, and prompts for better UI display
- Use `registerTool()`, `registerResource()`, and `registerPrompt()` methods (recommended over older APIs)
- Define schemas using zod: `{ inputSchema: { param: z.string() }, outputSchema: { result: z.string() } }`
- Return both `content` (for display) and `structuredContent` (for structured data) from tools
- For HTTP servers, use `StreamableHTTPServerTransport` with Express or similar frameworks
- For local integrations, use `StdioServerTransport` for stdio-based communication
- Create new transport instances per request to prevent request ID collisions (stateless mode)
- Use session management with `sessionIdGenerator` for stateful servers
- Enable DNS rebinding protection for local servers: `enableDnsRebindingProtection: true`
- Configure CORS headers and expose `Mcp-Session-Id` for browser-based clients
- Use `ResourceTemplate` for dynamic resources with URI parameters: `new ResourceTemplate('resource://{param}', { list: undefined })`
- Support completions for better UX using `completable()` wrapper from `@modelcontextprotocol/sdk/server/completable.js`
- Implement sampling with `server.server.createMessage()` to request LLM completions from clients
- Use `server.server.elicitInput()` to request additional user input during tool execution
- Enable notification debouncing for bulk updates: `debouncedNotificationMethods: ['notifications/tools/list_changed']`
- Dynamic updates: call `.enable()`, `.disable()`, `.update()`, or `.remove()` on registered items to emit `listChanged` notifications
- Use `getDisplayName()` from `@modelcontextprotocol/sdk/shared/metadataUtils.js` for UI display names
- Test servers with MCP Inspector: `npx @modelcontextprotocol/inspector`

## Best Practices

- Keep tool implementations focused on single responsibilities
- Provide clear, descriptive titles and descriptions for LLM understanding
- Use proper TypeScript types for all parameters and return values
- Implement comprehensive error handling with try-catch blocks
- Return `isError: true` in tool results for error conditions
- Use async/await for all asynchronous operations
- Close database connections and clean up resources properly
- Validate input parameters before processing
- Use structured logging for debugging without polluting stdout/stderr
- Consider security implications when exposing file system or network access
- Implement proper resource cleanup on transport close events
- Use environment variables for configuration (ports, API keys, etc.)
- Document tool capabilities and limitations clearly
- Test with multiple clients to ensure compatibility

## Common Patterns

### Basic Server Setup (HTTP)
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';

const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
});

const app = express();
app.use(express.json());

app.post('/mcp', async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: undefined,
        enableJsonResponse: true
    });
    
    res.on('close', () => transport.close());
    
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
});

app.listen(3000);
```

### Basic Server Setup (stdio)
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new McpServer({
    name: 'my-server',
    version: '1.0.0'
});

// ... register tools, resources, prompts ...

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Simple Tool
```typescript
import { z } from 'zod';

server.registerTool(
    'calculate',
    {
        title: 'Calculator',
        description: 'Perform basic calculations',
        inputSchema: { a: z.number(), b: z.number(), op: z.enum(['+', '-', '*', '/']) },
        outputSchema: { result: z.number() }
    },
    async ({ a, b, op }) => {
        const result = op === '+' ? a + b : op === '-' ? a - b : 
                      op === '*' ? a * b : a / b;
        const output = { result };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);
```

### Dynamic Resource
```typescript
import { ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';

server.registerResource(
    'user',
    new ResourceTemplate('users://{userId}', { list: undefined }),
    {
        title: 'User Profile',
        description: 'Fetch user profile data'
    },
    async (uri, { userId }) => ({
        contents: [{
            uri: uri.href,
            text: `User ${userId} data here`
        }]
    })
);
```

### Tool with Sampling
```typescript
server.registerTool(
    'summarize',
    {
        title: 'Text Summarizer',
        description: 'Summarize text using LLM',
        inputSchema: { text: z.string() },
        outputSchema: { summary: z.string() }
    },
    async ({ text }) => {
        const response = await server.server.createMessage({
            messages: [{
                role: 'user',
                content: { type: 'text', text: `Summarize: ${text}` }
            }],
            maxTokens: 500
        });
        
        const summary = response.content.type === 'text' ? 
            response.content.text : 'Unable to summarize';
        const output = { summary };
        return {
            content: [{ type: 'text', text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);
```

### Prompt with Completion
```typescript
import { completable } from '@modelcontextprotocol/sdk/server/completable.js';

server.registerPrompt(
    'review',
    {
        title: 'Code Review',
        description: 'Review code with specific focus',
        argsSchema: {
            language: completable(z.string(), value => 
                ['typescript', 'python', 'javascript', 'java']
                    .filter(l => l.startsWith(value))
            ),
            code: z.string()
        }
    },
    ({ language, code }) => ({
        messages: [{
            role: 'user',
            content: {
                type: 'text',
                text: `Review this ${language} code:\n\n${code}`
            }
        }]
    })
);
```

### Error Handling
```typescript
server.registerTool(
    'risky-operation',
    {
        title: 'Risky Operation',
        description: 'An operation that might fail',
        inputSchema: { input: z.string() },
        outputSchema: { result: z.string() }
    },
    async ({ input }) => {
        try {
            const result = await performRiskyOperation(input);
            const output = { result };
            return {
                content: [{ type: 'text', text: JSON.stringify(output) }],
                structuredContent: output
            };
        } catch (err: unknown) {
            const error = err as Error;
            return {
                content: [{ type: 'text', text: `Error: ${error.message}` }],
                isError: true
            };
        }
    }
);
```

## Good / Bad Examples

The examples below show the boundary between an acceptable convention and the closest common anti-pattern.

**Good:**

```typescript
server.registerTool('calculate', { title: 'Calculator', inputSchema: { a: z.number(), b: z.number() }, outputSchema: { result: z.number() } }, async ({ a, b }) => {
  const output = { result: a + b };
  return { content: [{ type: 'text', text: JSON.stringify(output) }], structuredContent: output };
});
```

Why: The tool has metadata, zod schemas, display content, and structured content.

**Bad:**

```typescript
server.tool('calculate', async (args: any) => String(args.a + args.b));
```

Why: The tool uses an older shape, `any`, and ambiguous text only.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `@modelcontextprotocol/sdk` imports from specific paths. | Specific ESM paths match SDK packaging. |
| Use `registerTool()`, `registerResource()`, and `registerPrompt()` with `title` and zod schemas. | Modern registration improves UX and validation. |
| Return `content` plus `structuredContent` and set `isError: true` for handled failures. | Clients need display, data, and error signals. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `@modelcontextprotocol/sdk` imports from specific paths. | Do not ignore this rule: Use `@modelcontextprotocol/sdk` imports from specific paths. |
| Use `registerTool()`, `registerResource()`, and `registerPrompt()` with `title` and zod schemas. | Do not ignore this rule: Use `registerTool()`, `registerResource()`, and `registerPrompt()` with `title` and zod schemas. |
| Return `content` plus `structuredContent` and set `isError: true` for handled failures. | Do not ignore this rule: Return `content` plus `structuredContent` and set `isError: true` for handled failures. |

## Checklist Before Opening a PR

- [ ] The change stays inside the matched `applyTo` scope.
- [ ] The authoritative conventions above are applied to new or modified code.
- [ ] Named commands, paths, API names, configuration keys, and version constraints remain intact.
- [ ] Relevant validation, linting, build, or test commands from this instruction pass.
- [ ] No secrets, unsupported APIs, placeholder prompt references, or relative primitive links were added.

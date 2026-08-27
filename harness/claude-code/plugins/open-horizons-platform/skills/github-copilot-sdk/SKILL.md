---
name: github-copilot-sdk
description: >-
  Builds applications with the GitHub Copilot SDK using explicit client lifecycle, sessions,
  permissions, streaming, tools, and MCP integration. Use when embedding Copilot in an
  application, creating sessions, handling events, registering tools, or troubleshooting SDK
  behavior.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/github-copilot-sdk/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GitHub Copilot SDK

Use the Copilot SDK with explicit permissions, lifecycle management, and completion handling.

## When to invoke

- Embed Copilot in a TypeScript, Python, Go, or .NET application.
- Create or resume Copilot SDK sessions.
- Stream responses and tool events.
- Register custom tools or MCP servers.

## Prerequisites and context

- GitHub Copilot CLI is installed, authenticated, and available to the runtime.
- Select a supported language runtime and repository package-management convention.
- Define the permission policy before enabling tools or filesystem/process access.

## Procedure

1. Verify CLI availability and authentication.
2. Install the language SDK using the repository's package manager.
3. Create a client with an explicit permission handler.
4. Start the client and create or resume a session before sending a prompt.
5. Register only the required tools and MCP servers with typed schemas.
6. For streaming, handle content deltas, tool events, errors, and the session-idle completion signal.
7. Stop/dispose the session and client on success, error, cancellation, and process shutdown.
8. Validate permission denial, tool failure, cancellation, and normal completion paths.

## Installation

| Language | Package command |
| --- | --- |
| TypeScript | `npm install @github/copilot-sdk` |
| Python | `pip install github-copilot-sdk` |
| Go | `go get github.com/github/copilot-sdk/go` |
| .NET | `dotnet add package GitHub.Copilot.SDK` |

Minimal TypeScript shape:

```typescript
const client = new CopilotClient({ permissionHandler: approveRequired });
await client.start();
const session = await client.createSession();
const response = await session.sendAndWait({ prompt: "Summarize this repository" });
console.log(response?.data.content);
await client.stop();
```

For streaming, process `assistant.message_delta` and treat `session.idle` as completion; do not
assume the first text event is the final response.

## Output template

```markdown
## GitHub Copilot SDK result

**Status:** IMPLEMENTED | BLOCKED
**Language:** <TypeScript | Python | Go | .NET>

### Integration
- Client lifecycle: <start/stop behavior>
- Session: <create/resume behavior>
- Permissions: <handler and denied path>
- Tools or MCP: <registered surface or none>
- Streaming: <events and completion signal>

### Validation
- <test/command and result>
```

## Limits

- Do not approve every tool by default in production.
- Do not leave clients, sessions, processes, or streams undisposed.
- Do not expose secrets in prompts, tool schemas, logs, or MCP configuration.
- Verify SDK APIs against current official documentation before version-sensitive implementation.

## Progressive disclosure and bundled resources

- [Extended SDK guide](references/extended-guide.md): tools, MCP, session management, events, and language-specific examples.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `mcp-cli` | `skill` | MCP server discovery or testing is required. |
| `mcp-ecosystem` | `skill` | The Open Horizons MCP ecosystem is the target. |
| `github-cli` | `skill` | GitHub authentication or repository API work is separate from SDK use. |

## Quality gate

- [ ] CLI availability and authentication are checked.
- [ ] Permission handling is explicit and tested.
- [ ] A session exists before messages are sent.
- [ ] Streaming handles deltas, errors, and idle completion.
- [ ] Client and session resources are disposed on every exit path.

## References

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)

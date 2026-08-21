---
name: "copilot-sdk"
description: >-
  Build agentic applications with GitHub Copilot SDK. Use when embedding AI agents in apps, creating
  custom tools, implementing streaming responses, managing sessions, connecting to MCP servers, or
  creating custom agents. Triggers on Copilot SDK, GitHub SDK, agentic app, embed Copilot,
  programmable agent, MCP server, custom agent.
---

# GitHub Copilot SDK

Build agentic applications with the GitHub Copilot SDK by installing the appropriate language package, creating sessions, handling permissions, streaming events, registering tools, and connecting MCP servers.

## When to invoke

- "Build an app with the GitHub Copilot SDK."
- "Embed GitHub Copilot in this TypeScript service."
- "Create a custom Copilot agent with tools."
- "Stream Copilot SDK responses in Python."
- "Connect a Copilot SDK session to an MCP server."

Embed Copilot's agentic workflows in any application using Python, TypeScript, Go, or .NET.

## Overview

The GitHub Copilot SDK exposes the same engine behind Copilot CLI: a production-tested agent runtime you can invoke programmatically. No need to build your own orchestration - you define agent behavior, Copilot handles planning, tool invocation, file edits, and more.

## Prerequisites

1. **GitHub Copilot CLI** installed and authenticated ([Installation guide](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli))
2. **Language runtime**: Node.js 18+, Python 3.8+, Go 1.21+, or .NET 8.0+

Verify CLI: `copilot --version`

## Installation

### Node.js/TypeScript
```bash
mkdir copilot-demo && cd copilot-demo
npm init -y --init-type module
npm install @github/copilot-sdk tsx
```

### Python
```bash
pip install github-copilot-sdk
```

### Go
```bash
mkdir copilot-demo && cd copilot-demo
go mod init copilot-demo
go get github.com/github/copilot-sdk/go
```

### .NET
```bash
dotnet new console -n CopilotDemo && cd CopilotDemo
dotnet add package GitHub.Copilot.SDK
```

## Quick Start

### TypeScript
```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
});

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await client.stop();
process.exit(0);
```

Run: `npx tsx index.ts`

### Python
```python
import asyncio
from copilot import CopilotClient, PermissionHandler

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
    })
    response = await session.send_and_wait({"prompt": "What is 2 + 2?"})

    print(response.data.content)
    await client.stop()

asyncio.run(main())
```

### Go
```go
package main

import (
    "fmt"
    "log"
    "os"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    client := copilot.NewClient(nil)
    if err := client.Start(); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    session, err := client.CreateSession(&copilot.SessionConfig{
        OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
        Model:               "gpt-4.1",
    })
    if err != nil {
        log.Fatal(err)
    }

    response, err := session.SendAndWait(copilot.MessageOptions{Prompt: "What is 2 + 2?"}, 0)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(*response.Data.Content)
    os.Exit(0)
}
```

### .NET (C#)
```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
});

var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = "What is 2 + 2?" });
Console.WriteLine(response?.Data.Content);
```

Run: `dotnet run`

## Streaming Responses

Enable real-time output for better UX:

### TypeScript
```typescript
import { CopilotClient, approveAll, SessionEvent } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
    if (event.type === "session.idle") {
        console.log(); // New line when done
    }
});

await session.sendAndWait({ prompt: "Tell me a short joke" });

await client.stop();
process.exit(0);
```

### Python
```python
import asyncio
import sys
from copilot import CopilotClient, PermissionHandler
from copilot.generated.session_events import SessionEventType

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
        "streaming": True,
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()
        if event.type == SessionEventType.SESSION_IDLE:
            print()

    session.on(handle_event)
    await session.send_and_wait({"prompt": "Tell me a short joke"})
    await client.stop()

asyncio.run(main())
```
## Extended reference

Additional detailed guidance was moved to [references/extended-guide.md](references/extended-guide.md) to keep this skill within the progressive-disclosure budget.

## Progressive disclosure and bundled resources

- `references/extended-guide.md`: detailed SDK patterns that were moved out of SKILL.md to keep the main skill concise.

## Output template

````markdown
## GitHub Copilot SDK result

**Status:** implemented | guidance only | blocked
**Language:** TypeScript | Python | Go | .NET

### Key code
```{{language}}
{{minimal_sdk_example}}
```

### Validation
- Install command: `{{package_install_command}}`
- Run command: `{{run_command}}`
- Session behavior: `{{sendAndWait_or_streaming_result}}`
````

## Quality gate

- [ ] GitHub Copilot CLI is installed and authenticated before SDK code is expected to run.
- [ ] The language runtime and package manager match the selected SDK package.
- [ ] Permission handling is explicit, such as `approveAll`, `PermissionHandler.approve_all`, or the language equivalent.
- [ ] Streaming code handles both message delta events and session idle completion.
- [ ] The client or session is stopped or disposed so processes do not linger.

## References

- https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli

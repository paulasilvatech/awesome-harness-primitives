---
applyTo: "**/*.py,**/python/**"
description: "Use when editing Python FastAPI services, agent runtime modules, middleware, tools, tests, and validation scripts in Open Horizons."
---

# Python Conventions — FastAPI Agent APIs, Middleware, Tools, and Validators

This file activates when you edit Python files anywhere in the repository, including `backstage/server/agent-api/`, Foundry services, MCP tooling, and validation scripts. It teaches Open Horizons conventions for FastAPI endpoints, Pydantic models, Azure identity, agent middleware, structured logging, tests, and safe automation. It does **not** cover Bash wrappers around Python scripts, which belong to the `shell` instructions, container packaging, which belongs to the `dockerfile` instructions, Kubernetes runtime configuration, which belongs to the `kubernetes` instructions, TypeScript Backstage clients, which belong to the `typescript` instructions, or Copilot primitive schemas, which belong to the `agent-files` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: "**/*.py,**/python/**"` for existing local patterns.
2. This `python` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for python conventions — fastapi agent apis, middleware, tools, and validators. Use the `test-coverage` and relevant implementation skills for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!IMPORTANT]
> Python services are part of the agentic execution layer. Treat tool execution, hooks, memory, trajectory logging, and cost tracking as governed runtime surfaces.

## FastAPI and Pydantic Models

Define explicit request and response models for public API boundaries. The agent API uses `BaseModel` for chat requests and streaming chunks.

```python
# Wrong: untyped body and ambiguous return contract.
@app.post("/api/agents/chat")
async def chat(request: dict):
    return await run_agent(request["message"])
```

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    user: str | None = None
    agent: str | None = None

@app.post("/api/agents/chat")
async def chat(request: ChatRequest):
    return await stream_agent_response(request)
```

## Configuration and Identity

Read configuration from environment variables and prefer Azure identity when API keys are absent. Never hardcode endpoints, credentials, tenants, or tokens.

```python
# Wrong: committed credential and tenant-specific endpoint.
client = AzureOpenAI(
    azure_endpoint="https://customer.openai.azure.com/",
    api_key="sk-example",
)
```

```python
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")

credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_ad_token=token.token,
    api_version=AZURE_OPENAI_API_VERSION,
)
```

> [!WARNING]
> Do not log prompts, tool arguments, tokens, connection strings, JWTs, or customer data unless they are redacted and explicitly needed for an audit trail.

## Logging and Observability

Agent APIs currently use standard logging and middleware audit structures; newer services may use `structlog` when already present. Log stable event names and IDs, not sensitive payloads.

```python
# Wrong: logs the entire user prompt and tool arguments.
logger.info("request=%s tool_args=%s", request.message, tool_input)
```

```python
logger.info(
    "Routing to agent: %s (%s)",
    agent_name,
    agent_config.display_name,
)
trajectory_id = trajectory_logger.start(
    agent=agent_name,
    user=request.user or "anonymous",
    message=clean_message,
)
```

## Error Handling

Return actionable HTTP errors at API edges and keep internal unexpected details out of responses. In middleware and validators, catch narrowly when possible and document defensive broad catches.

```python
# Wrong: leaks exception details to the caller.
except Exception as exc:
    raise HTTPException(status_code=500, detail=str(exc))
```

```python
except ServiceUnavailableError as exc:
    logger.warning("dependency_unavailable", extra={"dependency": exc.dependency})
    raise HTTPException(status_code=503, detail="Agent dependency unavailable") from exc
except Exception as exc:  # noqa: BLE001 - API edge converts unexpected failures
    logger.exception("agent_chat_failed")
    raise HTTPException(status_code=500, detail="Internal server error") from exc
```

> [!NOTE]
> A broad catch is acceptable in hook pipelines and API boundaries only when it prevents a governance or observability failure from crashing the caller and logs the reason.

## Tool Hooks and Governance

All agent tool calls flow through the hook pipeline. Preserve deny patterns, post-use redaction, bounded audit buffers, and explicit risk classification.

```python
# Wrong: bypasses governance and audit for a tool call.
result = await tool.execute(arguments)
```

```python
pre = tool_hooks.pre_tool_use(agent=agent_name, tool=tool_name, args=arguments)
if not pre.allowed:
    return {"error": pre.reason}
result = await tool.execute(arguments)
post = tool_hooks.post_tool_use(agent=agent_name, tool=tool_name, result=str(result))
return post.result
```

## Tests and Validation Scripts

Use pytest for Python behavior tests and keep validation scripts deterministic. The strict agent validator is a repository gate and must remain runnable with Python 3.11+.

```python
# Wrong: test depends on real Azure credentials.
def test_chat_calls_openai():
    assert create_openai_client().models.list()
```

```python
def test_classify_read_only_tool():
    assert classify_tool("list_pods") == ToolClass.READ_ONLY
```

## Conventions

| Rule | Rationale |
|---|---|
| Use Pydantic models at FastAPI request and response boundaries | Agent clients and SSE consumers need stable contracts. |
| Prefer `DefaultAzureCredential` fallback over committed API keys | Workload Identity and Managed Identity are the platform standard. |
| Keep logs structured around event names, IDs, and agent names | Observability dashboards need consistent low-risk fields. |
| Preserve tool hook enforcement for every agent tool call | Governance, redaction, and audit trails are core platform behavior. |
| Keep validation scripts deterministic and non-interactive | CI, IssueOps, and cloud agents run them without a terminal. |
| Use Python 3.11+ syntax and type hints | The repo standard and CI runtime expect modern typing. |

## Do / Do Not

| Do | Do not |
|---|---|
| Model untrusted JSON with Pydantic or explicit narrowing | Pass raw dictionaries deep into agent logic. |
| Return generic external error messages and log internal context safely | Expose stack traces or secret-bearing exception strings. |
| Keep async endpoints non-blocking | Add long synchronous shell or network work inside request handlers. |
| Add focused pytest tests for hooks, validators, and parsing logic | Require live Azure or GitHub services for unit tests. |

## Checklist Before Opening a PR

- [ ] FastAPI endpoints use explicit models and stable paths.
- [ ] Configuration comes from environment or managed identity, not committed values.
- [ ] Logs avoid prompts, secrets, tokens, and raw tool arguments.
- [ ] Tool calls still pass through pre/post governance hooks.
- [ ] Tests or validation scripts run without cloud credentials when possible.
- [ ] Python syntax and type hints are compatible with Python 3.11+.

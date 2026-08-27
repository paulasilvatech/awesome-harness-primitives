<!-- Generated from harness/github-copilot/instructions/agent-safety.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces safety and governance conventions for AI agent systems, tool-calling LLMs, and multi-agent orchestration. Use when code defines agents, tools, policies, guardrails, or audit behavior.

# Agent Safety Conventions — Governed Tool-Calling Systems

These instructions apply to code, configuration, and documentation that define AI agents, tool-calling LLMs, governance policies, guardrails, or multi-agent orchestration. They are authoritative for safety boundaries, tool authorization, content checks, delegation limits, audit logging, and framework integration in matched files; organization security policy and compliance requirements win where they define stricter controls.

## Core Governance Principles

| Principle | Convention |
| --- | --- |
| Fail closed | If a governance check errors or is ambiguous, deny the action rather than allowing it. |
| Policy as configuration | Define governance rules in YAML/JSON files, not hardcoded application logic. |
| Least privilege | Give agents only the minimum tool access needed for the task. |
| Append-only audit | Never modify or delete audit trail entries; immutability enables compliance. |

## Tool Access Controls

- Define an explicit allowlist of tools each agent can use; never give unrestricted tool access by default.
- Separate tool registration from tool authorization: frameworks know what tools exist, while policy controls which tools are allowed.
- Use blocklists for known-dangerous operations such as shell execution, file deletion, and database DDL.
- Require human-in-the-loop approval for high-impact tools such as send email, deploy, or delete records.
- Enforce rate limits on tool calls per request to prevent infinite loops and resource exhaustion.

## Content Safety and Argument Filtering

Scan user inputs before passing them to the agent, and scan generated tool arguments before execution.

| Check | Convention |
| --- | --- |
| Threat signals | Detect data exfiltration, prompt injection, and privilege escalation. |
| Sensitive patterns | Filter API keys, credentials, PII, and SQL injection indicators. |
| Pattern lists | Store regex pattern lists in updatable configuration, not code. |
| Coverage | Check both the user's original prompt and the agent's generated tool arguments. |

Do not rely only on output guardrails after generation. pre-execution governance and every governance-check is the control point that prevents unsafe tool calls.

## Multi-Agent Safety

- Give each agent in a multi-agent system its own governance policy.
- When agents delegate to other agents, compose the most restrictive policy from either agent.
- Track trust scores for agent delegates, degrade trust on failures, and require ongoing good behavior.
- Never allow an inner agent to have broader permissions than the outer agent that called it.
- Do not allow agents to self-modify their own governance policies.
- Decay trust scores over time so stale trust does not authorize risky behavior indefinitely.

## Audit and Observability

Log decisions and metadata, not raw prompts.

| Event | Required fields |
| --- | --- |
| Tool call | timestamp, agent ID, tool name, allow/deny decision, policy name |
| Governance violation | matched rule and evidence |
| Session boundary | `start/end` markers for correlation |
| Export format | JSON Lines for integration with log aggregation systems |

Keep audit trails append-only and ensure logging does not leak user content, secrets, or sensitive prompt text.

## Framework-Specific Patterns

| Framework | Convention |
| --- | --- |
| PydanticAI | Use `@agent.tool` with a governance decorator wrapper; PydanticAI's upcoming Traits feature is designed for this pattern. |
| CrewAI | Apply governance at the Crew level to cover all agents; use `before_kickoff` callbacks for policy validation. |
| OpenAI Agents SDK | Wrap `@function_tool` with governance and use handoff guards for multi-agent trust. |
| **LangChain/LangGraph** | Use `RunnableBinding` or tool wrappers for governance and apply checks at graph edges. |
| AutoGen | Implement governance in the `ConversableAgent.register_for_execution` hook. |

## Good / Bad Examples

The examples below illustrate guarded tools and explicit policies.

**Good**

```python
@govern(policy)
async def search(query: str) -> str:
    ...
```

```yaml
name: my-agent
allowed_tools: [search, summarize]
blocked_patterns: ["(?i)(api_key|password)\\s*[:=]"]
max_calls_per_request: 25
```

```python
final_policy = compose_policies(org_policy, team_policy, agent_policy)
```

Why: the tool is protected, the policy uses an allowlist, filters content, rate-limits calls, and composes org, team, and agent constraints with most-restrictive-wins semantics (`restrictive-wins`) instead of relying only on agent-level policy.

**Bad**

```python
async def search(query: str) -> str:
    ...
```

```yaml
name: my-agent
allowed_tools: ["*"]
```

```python
final_policy = agent_policy
```

Why: the tool has no governance wrapper, the policy grants unrestricted access, and the composition ignores organization constraints.

## Conventions

| Rule | Rationale |
| --- | --- |
| Fail closed on ambiguous or failing governance checks. | Uncertain safety decisions must not become implicit authorization. |
| Keep policy in YAML or JSON configuration with explicit allowlists and blocklists. | Governance can be reviewed and updated without code changes. |
| Check tool names and tool arguments before execution. | Unsafe behavior often hides in generated parameters, not only in selected tools. |
| Apply most-restrictive-wins composition in multi-agent delegation. | Inner agents cannot escalate beyond the caller or organization policy. |
| Log decisions, violations, and session boundaries as append-only JSON Lines metadata. | Compliance and incident response need immutable, correlatable evidence without prompt leakage. |
| Integrate governance through framework extension points such as decorators, callbacks, handoff guards, graph edges, and execution hooks. | Safety controls run consistently at the point where tools execute. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Define `allowed_tools` per agent. | Grant `allowed_tools: ["*"]` unless a reviewed policy explicitly permits it. |
| Use human-in-the-loop approval for deploy, delete records, send email, and similar high-impact actions. | Let agents execute high-impact tools without approval. |
| Filter prompt and argument content for API keys, credentials, PII, SQL injection, prompt injection, and data exfiltration. | Rely only on post-generation output guardrails. |
| Log allow/deny decisions and matched evidence. | Log raw prompts or sensitive user content in audit trails. |
| Decay delegate trust scores over time. | Treat stale trust as permanent authorization. |

## Checklist Before Opening a PR

- [ ] Governance checks fail closed and deny ambiguous actions.
- [ ] Agent policies are YAML or JSON configuration, not hardcoded rules.
- [ ] Every agent has least-privilege tool allowlists and relevant dangerous-operation blocklists.
- [ ] High-impact tools require human-in-the-loop approval.
- [ ] User prompts and generated tool arguments are checked before execution.
- [ ] Multi-agent delegation applies most-restrictive policy composition and prevents permission escalation.
- [ ] Trust scores degrade on failures and decay over time.
- [ ] Audit logs are append-only JSON Lines with tool-call metadata, violations, and session boundaries but no raw prompts.
- [ ] Framework integrations enforce governance at tool execution or graph-edge boundaries.

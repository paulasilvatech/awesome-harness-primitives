---
applyTo: "backstage/server/agent-api*/*.py,backstage/server/agent-api*/**/*.py,docs/aeg-feature-scaffold/orchestrator/**/*.py,mcp-servers/src/**/*.ts,policies/**/*.rego,policies/kubernetes/**/*.yaml"
description: "Use when editing Open Horizons agent runtimes, tools, orchestration, or policy code that requires safety and governance controls."
---

# Agent Runtime Safety

These rules apply to executable agent, tool, orchestration, and policy surfaces. Copilot primitive Markdown is governed by the primitive-authoring instructions instead.

## Conventions

- Treat model output, tool arguments, remote content, checkpoint data, and MCP responses as untrusted input.
- Authorize every tool call at execution time using the authenticated actor, service identity, requested operation, target, and environment.
- Deny on missing identity, policy failure, malformed arguments, ambiguous scope, exhausted budgets, or unavailable approval evidence.
- Keep delegated agents within the caller's effective permissions, budgets, and data boundary.
- Require explicit human approval for deployments, destructive operations, privilege changes, external publication, and other high-impact mutations.
- Bound iterations, tool calls, payload sizes, timeouts, retries, and result sizes.
- Keep secrets, credentials, raw prompts, customer content, and sensitive tool results out of logs. Record correlation IDs, policy versions, decisions, and redacted evidence.
- Preserve append-only audit evidence for authorization, approval, tool execution, and policy decisions.
- Keep read-only and mutating tools distinct; a read-only route must not gain mutation through generic shell, HTTP, or MCP access.
- Test allow, deny, malformed, unavailable-policy, replay, and approval-expiry paths without live credentials.

## Verification

- Safety checks execute immediately before the protected action and fail closed.
- Tests prove that delegation, retries, and alternate tool transports cannot bypass authorization.
- Audit records are useful for correlation without containing sensitive payloads.

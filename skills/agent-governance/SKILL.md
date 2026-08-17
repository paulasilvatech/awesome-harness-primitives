---
name: "agent-governance"
description: >-
  Patterns and techniques for adding governance, safety, and trust controls to AI agent systems. Use
  this skill when: - Building AI agents that call external tools (APIs, databases, file systems) -
  Implementing policy-based access controls for agent tool usage - Adding semantic intent
  classification to detect dangerous prompts - Creating trust scoring systems for multi-agent
  workflows - Building audit trails for agent actions and decisions - Enforcing rate limits, content
  filters, or tool restrictions on agents - Working with any agent framework (PydanticAI, CrewAI,
  OpenAI Agents, LangChain, AutoGen)
---
# Agent Governance Patterns

Patterns for adding safety, trust, and policy enforcement to AI agent systems.

## Overview

Governance patterns ensure AI agents operate within defined boundaries — controlling which tools they can call, what content they can process, how much they can do, and maintaining accountability through audit trails.

```
User Request → Intent Classification → Policy Check → Tool Execution → Audit Log
                     ↓                      ↓               ↓
              Threat Detection         Allow/Deny      Trust Update
```

## When to Use

- **Agents with tool access**: Any agent that calls external tools (APIs, databases, shell commands)
- **Multi-agent systems**: Agents delegating to other agents need trust boundaries
- **Production deployments**: Compliance, audit, and safety requirements
- **Sensitive operations**: Financial transactions, data access, infrastructure management

---

## Bundled Resources

- [Agent governance pattern implementations](references/pattern-implementations.md) — For concrete policy, classifier, decorator, trust scoring, audit trail, or framework integration implementations, read this reference before writing code.

## Governance Levels

Match governance strictness to risk level:

| Level | Controls | Use Case |
|-------|----------|----------|
| **Open** | Audit only, no restrictions | Internal dev/testing |
| **Standard** | Tool allowlist + content filters | General production agents |
| **Strict** | All controls + human approval for sensitive ops | Financial, healthcare, legal |
| **Locked** | Allowlist only, no dynamic tools, full audit | Compliance-critical systems |

---

## Best Practices

| Practice | Rationale |
|----------|-----------|
| **Policy as configuration** | Store policies in YAML/JSON, not hardcoded — enables change without deploys |
| **Most-restrictive-wins** | When composing policies, deny always overrides allow |
| **Pre-flight intent check** | Classify intent *before* tool execution, not after |
| **Trust decay** | Trust scores should decay over time — require ongoing good behavior |
| **Append-only audit** | Never modify or delete audit entries — immutability enables compliance |
| **Fail closed** | If governance check errors, deny the action rather than allowing it |
| **Separate policy from logic** | Governance enforcement should be independent of agent business logic |

---

## Quick Start Checklist

```markdown
## Agent Governance Implementation Checklist

### Setup
- [ ] Define governance policy (allowed tools, blocked patterns, rate limits)
- [ ] Choose governance level (open/standard/strict/locked)
- [ ] Set up audit trail storage

### Implementation
- [ ] Add @govern decorator to all tool functions
- [ ] Add intent classification to user input processing
- [ ] Implement trust scoring for multi-agent interactions
- [ ] Wire up audit trail export

### Validation
- [ ] Test that blocked tools are properly denied
- [ ] Test that content filters catch sensitive patterns
- [ ] Test rate limiting behavior
- [ ] Verify audit trail captures all events
- [ ] Test policy composition (most-restrictive-wins)
```

---

## Related Resources

- [Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) — Full governance framework
- [AgentMesh Integrations](https://github.com/microsoft/agent-governance-toolkit/tree/main/packages/agentmesh-integrations) — Framework-specific packages
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

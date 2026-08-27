---
name: agent-governance
description: >-
  Design governance, safety, policy enforcement, trust scoring, and audit controls for AI agent
  systems. Use when building agents with external tools, policy-based tool access, semantic intent
  classification, dangerous prompt detection, multi-agent trust workflows, rate limits, content
  filters, or audit trails across PydanticAI, CrewAI, OpenAI Agents, LangChain, or AutoGen.
---

<!-- Generated from harness/github-copilot/plugins/agent-governance/skills/agent-governance/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Agent governance patterns

Add governance controls to AI agent systems so tool use, content handling, delegation, rate, and accountability stay inside explicit safety and trust boundaries.

## When to invoke

- "Add governance to an agent that calls external tools."
- "Implement policy-based access control for agent tools."
- "Detect dangerous prompts before tool execution."
- "Create trust scoring for a multi-agent workflow."
- "Add audit trails, rate limits, content filters, or tool restrictions."

## Governance flow

```text
User Request → Intent Classification → Policy Check → Tool Execution → Audit Log
                     ↓                      ↓               ↓
              Threat Detection         Allow/Deny      Trust Update
```

Apply controls before tool execution, update trust after outcomes, and write audit records for both allowed and denied actions.

## Governance levels

| Level | Controls | Use case |
| --- | --- | --- |
| Open | Audit only, no restrictions. | Internal dev/testing. |
| Standard | Tool allowlist plus content filters. | General production agents. |
| Strict | All controls plus human approval for sensitive operations. | Financial, healthcare, legal. |
| Locked | Allowlist only, no dynamic tools, full audit. | Compliance-critical systems. |

## Control patterns

| Pattern | Rule | Failure mode prevented |
| --- | --- | --- |
| Policy as configuration | Store policies in YAML/JSON, not hardcoded. | Code deploy required for every policy change. |
| Most-restrictive-wins | Deny always overrides allow when composing policies. | A permissive policy bypasses a stricter one. |
| Pre-flight intent check | Classify intent before tool execution. | Dangerous action is detected only after side effects. |
| Tool allowlist | Permit only named tools for each role, context, or trust level. | Dynamic tool access expands beyond review. |
| Content filter | Block secrets, prompt injection, unsafe content, or regulated data flows. | Agent processes content it must not handle. |
| Human approval | Require approval for high-impact or irreversible operations. | Agent autonomously performs sensitive changes. |
| Rate limit | Bound requests, tool calls, tokens, or cost by actor and time window. | Runaway agent loops or cost spikes. |
| Trust decay | Decay trust scores over time. | Old good behavior grants permanent privilege. |
| Append-only audit | Never modify or delete audit entries. | Compliance evidence can be rewritten. |
| Fail closed | Deny action when governance checks error. | Safety system outage becomes allow-all. |
| Separate policy from logic | Keep enforcement independent from agent business logic. | Business code accidentally bypasses governance. |

## Implementation checklist

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

## Framework integration cues

| Framework | Integration seam |
| --- | --- |
| PydanticAI | Wrap tools or dependencies with a policy check before invocation. |
| CrewAI | Gate crew tools and delegation tasks by role and trust level. |
| OpenAI Agents | Enforce tool allowlists and approval steps before tool calls execute. |
| LangChain | Wrap tools, callbacks, and chains with policy and audit middleware. |
| AutoGen | Gate inter-agent messages, delegation, and tool execution. |

Read `references/pattern-implementations.md` before writing code for policy objects, classifiers, decorators, trust scoring, audit trails, or framework-specific examples.

## Criteria

- [ ] The agent's external tools, APIs, databases, file systems, and shell access are inventoried.
- [ ] Each tool has an allow, deny, approval, and audit rule.
- [ ] Intent classification runs before side-effecting tools.
- [ ] Dangerous prompt, sensitive data, and content filter rules are explicit.
- [ ] Trust scores have update and decay rules.
- [ ] Audit records are append-only and include actor, intent, tool, decision, timestamp, and outcome.
- [ ] Governance errors fail closed.

## Gotchas

- **Do not hardcode policy in tool bodies**: policy must be reviewable and changeable outside business logic.
- **Do not rely on audit-only for production sensitive operations**: audit after harm is not prevention.
- **Do not let dynamic tool discovery bypass allowlists**: discovered tools still need explicit policy.
- **Do not delete audit entries**: corrections should append compensating records.

## Progressive disclosure and bundled resources

- `references/pattern-implementations.md`: concrete implementations for policy, classifier, decorator, trust scoring, audit trail, and framework integration.

## Environment shorthand

Use open governance for `dev/testing`; increase controls before production.

## Output template

```markdown
## Agent governance plan

**Status:** ready | implemented | blocked
**Governance level:** open | standard | strict | locked
**Agent/framework:** <name>

| Control | Decision | Evidence or implementation |
| --- | --- | --- |
| Tool allowlist | <rule> | <policy path or code seam> |
| Intent classifier | <rule> | <classifier/prompt/model> |
| Human approval | <rule> | <approval path> |
| Audit trail | <rule> | <storage/export> |
| Trust scoring | <rule> | <update/decay formula> |

### Validation
- Blocked tool denied: pass | fail
- Content filter tested: pass | fail
- Rate limit tested: pass | fail
- Audit event captured: pass | fail
```

## Quality gate

- [ ] Governance level is selected based on risk: open, standard, strict, or locked.
- [ ] Policies are configuration or data, not scattered hardcoded conditionals.
- [ ] Most-restrictive-wins behavior is implemented or specified.
- [ ] Side-effecting tool calls require pre-flight intent and policy checks.
- [ ] Audit logging is append-only and records allowed and denied actions.
- [ ] Trust scoring includes decay over time.
- [ ] Fail-closed behavior is tested for policy, classifier, and audit failures.

## References

- [Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
- [AgentMesh Integrations](https://github.com/microsoft/agent-governance-toolkit)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---
name: diagnose
description: >-
  Diagnose AI workflows across prompt quality, context efficiency, tool health, architecture
  fitness, and safety and reliability, producing a 1-5 scored report with critical findings and
  prioritized remediation. Use when the user asks for AI workflow diagnostics, an agent audit,
  prompt health check, tool quality review, workflow risk scan, or remediation plan.
---

<!-- Generated from harness/github-copilot/skills/diagnose/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AI workflow diagnostics

Audit an AI workflow systematically across five quality dimensions, assign evidence-backed scores, and return a prioritized remediation plan focused on the highest-risk failures.

## When to invoke

- "Run AI workflow diagnostics on this agent."
- "Audit this prompt and tool setup."
- "Health-check this workflow before production."
- "Score this multi-agent architecture."
- "Find hidden safety and reliability risks in this AI workflow."

## Inputs

Use the workflow description, prompt text, tool list, agent configuration, logs, evaluations, or architecture notes the user provides. If evidence is missing for a dimension, score conservatively and state what evidence was unavailable.

## Diagnostic dimensions

| Dimension | Evaluate | Common evidence |
| --- | --- | --- |
| Prompt Quality | Role, context, instructions, output zones, explicit output schema, instruction clarity, edge cases, anti-patterns such as wall of text, contradictions, and implicit format. | Prompt body, system/developer instructions, examples, output contract. |
| Context Efficiency | Context budget allocation, attention gradient awareness, context window utilization, explicit state, memory strategy. | Retrieved files, conversation state, memory usage, summarization strategy. |
| Tool Health | Tool count, description quality, input/output/error schema completeness, graceful error handling, idempotency, retry safety. | Tool manifests, MCP server definitions, function schemas, scripts. |
| Architecture Fitness | Topology, single-agent versus multi-agent justification, agent boundaries, handoff protocols, observability, cost awareness. | Agent diagrams, routing rules, task decomposition, logs, budgets. |
| Safety & Reliability | Input validation, output filtering, PII handling, content policy, cost controls, error recovery, evaluation strategy. | Guardrails, validation code, privacy boundaries, golden tests, fallback behavior. |

## Scoring guide

| Score | Meaning | Recommended action |
| --- | --- | --- |
| 5 | Production-excellent | No action needed. |
| 4 | Good with minor gaps | Polish prompt clarity or output schema. |
| 3 | Functional but risky | Add error handling or reduce complexity. |
| 2 | Significant issues | Immediate attention — add retries/guards. |
| 1 | Broken or missing | Rebuild from scratch with clear structure. |

## Criteria

### Prompt quality

- [ ] Role, context, instructions, and output zones are explicit.
- [ ] Output schema is defined rather than implied.
- [ ] Instructions are specific and non-contradictory.
- [ ] Edge cases and failure modes are addressed.
- [ ] The prompt avoids wall-of-text structure and hidden format requirements.

### Context efficiency

- [ ] Context budget is planned rather than ad hoc.
- [ ] Critical information appears at the start or end, not buried in the middle.
- [ ] Retrieved context is relevant and not wasteful.
- [ ] State management is explicit.
- [ ] Memory strategy matches conversation length and task durability.

### Tool health

- [ ] Tool count is appropriate: 3-7 is ideal; 13+ is problematic unless strongly justified.
- [ ] Tool descriptions are specific enough for routing.
- [ ] Schemas define inputs, outputs, and errors.
- [ ] Tools handle errors gracefully.
- [ ] Side-effecting tools are idempotent or protected against unsafe retries.
- [ ] Scope attribution distinguishes project-configured tools from agent-level tools; flag overhead only for tools the project can control.

### Architecture fitness

- [ ] The topology fits the task; multi-agent design is justified by real boundaries.
- [ ] Agent responsibilities do not overlap confusingly.
- [ ] Handoffs are structured and observable.
- [ ] Decisions are logged or reconstructable.
- [ ] Cost is budgeted rather than unbounded.

### Safety and reliability

- [ ] Inputs are validated before use.
- [ ] Output filtering handles PII and policy risks contextually; data between a user's own frontend and backend is lower risk than data exposed to external services.
- [ ] Cost ceilings or stop conditions exist.
- [ ] Errors have recovery paths or fallbacks.
- [ ] Evaluation uses golden tests, regression cases, or measurable checks rather than "it seems to work".

## Prioritization rules

| Finding type | Severity bias |
| --- | --- |
| User data leakage, unsafe external sharing, or secret exposure | Critical regardless of other scores. |
| Tool side effects without validation or idempotency | High. |
| Missing output schema in a production workflow | Medium to high depending on downstream automation. |
| Multi-agent overlap causing duplicate work or contradictory actions | Medium. |
| Excessive context with no failure yet | Low to medium; optimize after correctness risks. |

Check attention at `start/end`, avoid `ad-hoc` state, account for `built-in` agent-level tools, identify unsafe `side-effect` tools, and recommend `retries/guards` where recovery is missing.

## Output template

```markdown
╔══════════════════════════════════════╗
║          WORKFLOW DIAGNOSTIC        ║
╠══════════════════════════════════════╣
║ Prompt Quality       ████░  4/5     ║
║ Context Efficiency   ███░░  3/5     ║
║ Tool Health          ██░░░  2/5     ║
║ Architecture         ████░  4/5     ║
║ Safety & Reliability ██░░░  2/5     ║
╠══════════════════════════════════════╣
║ Overall Score:       15/25          ║
╚══════════════════════════════════════╝

CRITICAL FINDINGS:
1. <most severe issue — immediate action needed>
2. <second most severe>
3. <third>

RECOMMENDED ACTIONS:
1. <specific remediation for finding #1>
2. <specific remediation for finding #2>
3. <specific remediation for finding #3>
```

## Quality gate

- [ ] All five dimensions were scored from 1 to 5.
- [ ] Every score has evidence or explicitly notes missing evidence.
- [ ] Tool overhead findings distinguish project-configured tools from agent-level tools.
- [ ] Safety findings scope PII and external exposure risks contextually.
- [ ] Critical findings are ordered by severity, not by dimension order.
- [ ] Recommended actions are concrete and tied to findings.
- [ ] The overall score equals the sum of the five dimension scores out of 25.

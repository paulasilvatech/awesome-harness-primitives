---
description: "Review an existing agentic system design against current best practices: model routing, prompt and semantic caching, short and long term memory, context budgeting, tools and MCP hygiene, identity and guardrails, evaluation, observability, and cost control. Flags anti-patterns and produces a prioritized findings list with fixes."
agent: agent
argument-hint: "what to review, for example our current Foundry agent design or a design doc path"
---

# Review Agentic Architecture

Review `${input:target:the agent design or document to review}` against the agentic best-practice framework and report findings.

## First step, always

Load `agentic-architecture-patterns` before reviewing or drafting findings, and follow its seven decisions and anti-pattern list. Load the companion skills as needed to check specifics: `azure-managed-redis-cache` (cache and memory), `foundry-agent-blueprint` (Foundry wiring), `azure-api-center` (tool governance), and `apim-ai-gateway` (gateway controls).

## Checks

For each of the seven decisions, confirm the design has a deliberate, sourced choice and flag gaps:

1. Model routing: are tasks routed by class, or does one expensive model serve everything?
2. Caching: is there prompt caching on stable prefixes and semantic caching on repeated requests, with scoped keys and a threshold?
3. Memory: are short term thread state and long term durable memory separated, scoped by tenant and user, with a write and read policy?
4. Context curation: is the window budgeted, with retrieval ranked and history compacted?
5. Tools and MCP: is the tool surface small and well described, validated at the boundary, and governed?
6. Identity and guardrails: agent identity, managed identity (no shared secrets), Content Safety and Prompt Shields, approval for high-impact actions, tenant isolation?
7. Evaluation, observability, and cost: an eval set in CI, OpenTelemetry GenAI tracing, and spend attributed by model class and tenant?

## Output

Produce a prioritized findings list. For each finding: the location, the issue, the severity (blocker, major, minor), the recommended fix, and a source (Microsoft Learn or the relevant skill). Call out the anti-patterns explicitly. Do not alter production code or audited numbers; hand fixes to the `AI-Native Engineer` agent.

Output concisely: return only the findings table, open questions or assumptions, and critical validation gaps. Do not narrate the process steps.

## Rules

- Never fabricate limits, prices, or benchmarks. Cite sources or state assumptions.
- Write "GitHub Copilot", never "Copilot" alone. No em dashes.

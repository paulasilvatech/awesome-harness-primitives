---
description: "Design a production agentic system on GitHub platform and Azure AI Foundry end to end: resolve model routing, prompt and semantic caching, short and long term memory, context curation, tools and MCP, identity and guardrails, evaluation, observability, and cost, then produce the architecture document and diagrams. Routes to the AI-Native Engineer agent and its companion skills."
agent: agent
argument-hint: "the system to design, for example an agentic RAG service on Foundry with a Redis semantic cache"
---

# Design Agentic System

Design `${input:system:the agentic system to design, for example an agentic RAG service on Foundry}` as a production architecture on the GitHub platform and Azure AI Foundry.

## First step, always

Use the `AI-Native Engineer` agent persona. Load `agentic-architecture-patterns` before clarifying, designing, generating, or editing. Then load the companion skills that match the design: `azure-managed-redis-cache`, `foundry-agent-blueprint`, `azure-api-center`, `apim-ai-gateway`, and `azure-architecture-diagrams`. Apply the `paulasilva-ms` design system to any rendered output.

## Steps

1. Clarify scope: use case, scale, latency and cost targets, data sensitivity, identity model, and where it runs (GitHub Actions, Container Apps, AKS, or Foundry hosted). Ask only for what is missing.
2. Walk the seven decisions in order (model routing, caching, memory, context curation, tools and MCP, identity and guardrails, evaluation and observability and cost). Record each choice with its rationale and source.
3. Map each decision to a concrete service and note managed identity and network posture.
4. Produce `{system}_AI_Architecture.md`: executive summary, the agentic decision record, the service mapping, the diagrams (context, component, deployment, and a sequence for the critical path), a phased path (MVP then target), a non-functional analysis, risks and mitigations, and a References section.
5. Render the diagrams with `azure-architecture-diagrams` using the official Azure, Microsoft, and GitHub icons. Keep `.drawio` sources under `output/` and embed exported SVG.

## Rules

- Never fabricate limits, prices, or benchmarks. Verify against Microsoft Learn and the model card, cite them, or state the value as an explicit assumption. End the document with a References section.
- Write "GitHub Copilot", never "Copilot" alone. No em dashes. Do not modify or re-color official product icons.
- Prefer managed identity over keys, least privilege, and private networking where the requirement calls for it.

## Done when

- The architecture document exists with all seven decisions resolved and traced to sources.
- The four diagrams render and every icon resolves.
- The phased path and the non-functional analysis are present, and every data claim is sourced.

## Output

Output concisely: return only the architecture document path, diagram artifact path(s), validation status, and any critical findings or blockers. Do not narrate the process steps.

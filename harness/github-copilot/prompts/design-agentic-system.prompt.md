---
name: 'design-agentic-system'
description: 'Design a production agentic system on GitHub and Azure AI Foundry with architecture documentation and diagrams.'
agent: 'agent'
argument-hint: 'the system to design, for example an agentic RAG service on Foundry with a Redis semantic cache'
---

# /design-agentic-system

## Objective

Design a production agentic system on the GitHub platform and Azure AI Foundry, producing an architecture document, resolved agentic decisions, concrete service mapping, official-icon diagrams, a phased path, non-functional analysis, risks, mitigations, and sourced references.

## When to Invoke

Use this prompt when a user asks to design an agentic system, agentic RAG service, Foundry-based platform, tool-using AI system, MCP-enabled architecture, semantic-cache architecture, or production AI architecture on GitHub and Azure.

## Preconditions

- The system to design is provided through `${input:system:the agentic system to design, for example an agentic RAG service on Foundry}` or the prompt argument.
- The `AI-Native Engineer` agent persona is available or can be followed as the role.
- The `agentic-architecture-patterns` skill is available before clarification, design, generation, or editing.
- Companion skills are available as needed: `azure-managed-redis-cache`, `foundry-agent-blueprint`, `azure-api-center`, `apim-ai-gateway`, and `azure-draw-io-diagram-generator`.
- Output under the requested document path and `output/` for diagrams is permitted.

## Inputs the Team Must Provide

- `system` — the agentic system to design.
- Use case, scale, latency and cost targets, data sensitivity, identity model, and runtime location such as GitHub Actions, Container Apps, AKS, or Foundry hosted.
- Required services, constraints, compliance needs, and critical user or data flows.
- Ask only for missing information that changes architecture decisions.

## What I Will Do

- Use the `AI-Native Engineer` persona and load `agentic-architecture-patterns` before clarifying, designing, generating, or editing.
- Load companion skills that match the design: `azure-managed-redis-cache`, `foundry-agent-blueprint`, `azure-api-center`, `apim-ai-gateway`, and `azure-draw-io-diagram-generator`.
- Walk seven decisions in order: model routing, caching, memory, context curation, tools and MCP, identity and guardrails, evaluation and observability and cost.
- Map each decision to concrete services, managed identity, and network posture.
- Produce `{system}_AI_Architecture.md` and render diagrams using official Azure, Microsoft, and GitHub icons.

## What I Will NOT Do

- Fabricate limits, prices, benchmarks, model-card claims, or Microsoft Learn facts.
- Use keys where managed identity and least privilege are appropriate for the requirement.
- Ignore private networking where the requirement calls for it.
- Modify or recolor official product icons.
- Write “Copilot” without “GitHub Copilot”.
- Omit references for data claims.

## Output Format

Return only the concise architecture delivery report:

```markdown
### Agentic System Design Result

### Architecture Document
- `{system}_AI_Architecture.md`

### Diagram Artifacts
- Context diagram: `output/<system>-context.drawio` and `output/<system>-context.svg`
- Component diagram: `output/<system>-component.drawio` and `output/<system>-component.svg`
- Deployment diagram: `output/<system>-deployment.drawio` and `output/<system>-deployment.svg`
- Critical-path sequence: `output/<system>-sequence.drawio` and `output/<system>-sequence.svg`

### Required Document Sections
- Executive summary
- Agentic decision record
- Service mapping
- Diagrams: context, component, deployment, and sequence for the critical path
- Phased path: MVP then target
- Non-functional analysis
- Risks and mitigations
- References section

### Validation Status
- All seven decisions resolved and traced to sources: `<passed|failed>`
- Four diagrams render and every icon resolves: `<passed|failed>`
- Data claims sourced from Microsoft Learn, model card, or explicit assumption: `<passed|failed>`
- Managed identity, least privilege, and private networking considered: `<passed|failed>`

### Critical Findings or Blockers
- `<finding or none>`
```

## Definition of Done

- [ ] The architecture document exists as `{system}_AI_Architecture.md`.
- [ ] All seven decisions are resolved, rationalized, and traced to sources.
- [ ] Concrete services, managed identity, and network posture are mapped.
- [ ] Context, component, deployment, and critical-path sequence diagrams render with official icons.
- [ ] The phased path, non-functional analysis, risks, mitigations, and References section are present.
- [ ] Every data claim is sourced or labeled as an explicit assumption.

## Prompt Body

Follow these steps in order. Do not clarify, design, generate, or edit before loading the required agentic architecture patterns.

**Step 1 — Assume the role and load skills.** Use the `AI-Native Engineer` agent persona. Load `agentic-architecture-patterns` before clarifying, designing, generating, or editing. Then load companion skills that match the design: `azure-managed-redis-cache`, `foundry-agent-blueprint`, `azure-api-center`, `apim-ai-gateway`, and `azure-draw-io-diagram-generator`. Apply the `paulasilva-ms` design system to rendered output.

**Step 2 — Clarify scope.** Clarify use case, scale, latency and cost targets, data sensitivity, identity model, and where it runs: GitHub Actions, Container Apps, AKS, or Foundry hosted. Ask only for what is missing.

**Step 3 — Resolve the seven agentic decisions.** Walk decisions in this order: model routing, caching, memory, context curation, tools and MCP, identity and guardrails, evaluation and observability and cost. Record each choice with its rationale and source.

**Step 4 — Map decisions to services.** Map each decision to a concrete service and note managed identity and network posture. Prefer managed identity over keys, least privilege, and private networking where the requirement calls for it.

**Step 5 — Produce the architecture document.** Create `{system}_AI_Architecture.md` with executive summary, the agentic decision record, service mapping, diagrams, a phased path from MVP to target, non-functional analysis, risks and mitigations, and a References section. Never fabricate limits, prices, or benchmarks. Verify against Microsoft Learn and the model card, cite them, or state the value as an explicit assumption.

**Step 6 — Render diagrams.** Render diagrams with `azure-draw-io-diagram-generator` using permitted current official Azure, Microsoft, and GitHub assets with source, terms, retrieval date, usage basis, and SHA-256 provenance. Produce context, component, deployment, and a sequence for the critical path. Keep `.drawio` sources under `output/`, export self-contained SVG, preserve artwork and aspect ratio, and use neutral shapes for generic concepts. Write “GitHub Copilot”, never “Copilot” alone. Do not use em dashes.

**Step 7 — Validate and report.** Confirm the document exists, all seven decisions are traced, all four diagrams render, every icon resolves, the phased path and non-functional analysis are present, and every data claim is sourced. Return only the architecture document path, diagram artifact paths, validation status, and critical findings or blockers.

## Invocation Example

```
/design-agentic-system system="agentic RAG service on Foundry with a Redis semantic cache"
```

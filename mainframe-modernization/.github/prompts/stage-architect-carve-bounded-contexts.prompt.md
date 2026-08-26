---
name: "carve-bounded-contexts"
description: "Evaluates the Stage 1 boundary hypotheses and decides bounded contexts for the Modular Monolith."
argument-hint: "report=01-archaeology/discovery-report.md"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /carve-bounded-contexts

## Objective

Transform the boundary hypotheses from the Stage 1 discovery report into evaluated and decided bounded contexts. Each context receives a name, responsibilities, owned data, and inter-context communication rules.

## When to Invoke

At the beginning of Stage 2, immediately after reviewing the Stage 1 discovery report.

## Preconditions

- `01-archaeology/discovery-report.md` exists with at least 3 boundary hypotheses
- The team reviewed the discovery report and is ready to make architectural decisions

## Inputs the Team Must Provide

- Path to the discovery report
- Any additional team constraints or preferences

## What I Will Do

- Read the boundary hypotheses from the discovery report
- Evaluate each hypothesis against three criteria: cohesion, coupling, and frequency of change
- Present the analysis for each hypothesis to the team
- Document rejections with rationale
- Formalize accepted contexts with names, responsibilities, and data ownership

## What I Will NOT Do

- Automatically decide which hypotheses to accept — the team makes the final decision
- Propose microservices — this is a Modular Monolith
- Fabricate business context for the hypotheses — I work only with what Stage 1 discovered
- Skip the evaluation criteria — every hypothesis receives the complete analysis

## Output Format

A Markdown file at `02-modern-spec/bounded-contexts.md`:

```markdown
# Bounded Context Map
## Evaluation Criteria
## Hypothesis Evaluation
### [Hypothesis Name] — ACCEPTED / REJECTED
## Final Bounded Contexts
### [Context Name]
- Responsibility:
- Owned data (DDMs/tables):
- Public interface:
- Why it is a separate context:
## Inter-Context Communication
## Context Map Mermaid Diagram
```

## Definition of Done

- [ ] Every discovery-report hypothesis is evaluated against the three criteria
- [ ] Rejected hypotheses have documented rationale
- [ ] 2–5 bounded contexts are finalized with business-language names
- [ ] Each context has a responsibility paragraph, owned-data list, and public-interface outline
- [ ] A Mermaid context-map diagram shows relationships between contexts
- [ ] No context is an isolated island — communication paths are defined

## Prompt Body

You are the `@architect`. The team is starting Stage 2 and needs to decide bounded contexts for the Modular Monolith.

**Step 1 — Read the discovery report.**
Open `01-archaeology/discovery-report.md`. Extract the boundary-hypothesis section. List each hypothesis with its name, included programs, owned DDMs, and rationale.

**Step 2 — Evaluate against three criteria.**
For each hypothesis, analyze:

**Cohesion** — Do the business rules in this group relate to the same business capability? Check by reviewing the confirmed rules in `01-archaeology/business-rules-catalog.md` that belong to this group. High cohesion = strong candidate.

**Coupling** — How many dependencies cross this boundary? Check the dependency map in `01-archaeology/dependency-map.md`. Count edges that would cross between this context and others. Low coupling = strong candidate. High coupling suggests the boundary may be misplaced.

**Frequency of change** — In the legacy system, which programs in this group were likely modified together? Use file-naming patterns and call relationships as proxies. Programs that call one another extensively probably change together and belong in the same context.

Present each evaluation as a scorecard: High/Medium/Low for each criterion.

**Step 3 — Present to the team for a decision.**
For each hypothesis, present:

- The scorecard
- A recommendation (accept, reject, or merge with another hypothesis)
- The rationale

Then ask the team: "Do you accept this recommendation? If not, what would you change?"

The team makes the final decision. If the team overrides your recommendation, document its rationale.

**Step 4 — Formalize accepted contexts.**
For each accepted bounded context, write:

- **Name**: A team-confirmed business-language name, not a technical service name
- **Responsibility**: One paragraph describing what this context owns
- **Owned data**: Which DDMs/tables belong exclusively to this context
- **Public interface**: Which operations this context exposes to other contexts (method signatures or event names — not implementation)
- **Why it's its own context**: One sentence connecting it to the evaluation criteria

**Step 5 — Define inter-context communication.**
For each pair of contexts that needs to communicate, specify:

- The direction (A calls B, or bidirectional)
- The mechanism: in-process method call through an interface, domain event, or shared-kernel type
- The exchanged data (IDs only? Complete DTOs? Events?)

Reinforce that this is a Modular Monolith. Communication is in-process, not HTTP between services.

**Step 6 — Draw the context map.**
Create a Mermaid diagram showing all contexts as boxes, with labeled arrows for communication relationships. Use the kit color palette: fill `#0f172a`, stroke `#334155`, text `#e2e8f0`.

**Step 7 — Write the output.**
Write to `02-modern-spec/bounded-contexts.md`.

## Invocation Example

```
/carve-bounded-contexts report=01-archaeology/discovery-report.md
```

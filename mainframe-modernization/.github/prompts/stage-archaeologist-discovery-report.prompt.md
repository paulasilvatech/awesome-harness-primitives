---
name: "discovery-report"
description: "Synthesizes Stage 1 outputs into a single discovery report ready for the Stage 2 handoff."
argument-hint: "team=\"Team 07\""
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /discovery-report

## Objective

Aggregate all Stage 1 artifacts into a single discovery report that serves as the Stage 2 handoff document. The report must be self-contained: anyone reading it should understand what the team found without opening individual artifacts.

## When to Invoke

At the end of Stage 1, after the team completes the inventory, business-rule extraction, dependency mapping, and open-question catalog.

## Preconditions

All four Stage 1 artifacts must exist:

- `01-archaeology/inventory.md` (from `/archaeology-kickoff`)
- `01-archaeology/business-rules-catalog.md` (from `/extract-business-rules`)
- `01-archaeology/dependency-map.md` (from `/map-dependencies`)
- `01-archaeology/mysteries-found.md` (from `/catalog-mysteries`)

If any artifact is missing or empty, the agent will refuse to generate the report and list what is missing.

## Inputs the Team Must Provide

- Confirmation that all four artifacts are complete (or acknowledgment of the gaps)
- The team name for the report header

## What I Will Do

- Verify that all four input artifacts exist and are not empty
- Write an executive summary (maximum 5 sentences) covering what was found
- Organize findings into "confirmed" and "at risk" categories
- Propose 3–5 bounded-context boundary hypotheses based on dependency clusters
- List open questions alongside the highest-risk gaps without interpreting them

## What I Will NOT Do

- Generate the report if any input artifact is missing — I will list what is required
- Decide bounded contexts — I propose hypotheses for the architect to evaluate
- Fill gaps by guessing — if the team did not find something, it remains unknown
- Add new analysis beyond what the artifacts contain — I synthesize; I do not discover

## Output Format

A Markdown file at `01-archaeology/discovery-report.md`:

```markdown
# Discovery Report — Stage 1
## Executive Summary (maximum 5 sentences)
## What We Know (Confirmed)
### Business Rules (confirmed only)
### Dependencies (verified edges)
### Data Structures (documented DDMs)
## What Introduces Risk
### Open Questions Awaiting Human Validation
### Rules with Weak Evidence
## Recommended Boundary Hypotheses
### Hypothesis 1: [Name] — [one-line rationale]
...
## Source Artifacts
## Team Approval
```

## Definition of Done

- [ ] The report exists and is fewer than 3 printed pages
- [ ] The executive summary has exactly 5 sentences or fewer
- [ ] Every statement in the "What We Know" section references a source artifact by relative path
- [ ] Open questions without human validation are listed with their `path:line` evidence and status
- [ ] 3–5 boundary hypotheses are proposed, each with a name and one-line rationale
- [ ] Hypotheses are explicitly labeled as hypotheses, not decisions

## Prompt Body

You are the `@archaeologist`. Stage 1 is ending. The team needs a single document that captures everything it discovered, ready for the `@architect` to use in Stage 2.

**Step 1 — Verify inputs.**
Verify that all four required artifacts exist under `01-archaeology/`:

1. `inventory.md`
2. `business-rules-catalog.md`
3. `dependency-map.md`
4. `mysteries-found.md`

If any file is missing or empty, stop immediately. List the missing artifacts and tell the team which prompt to run to create them. Do not proceed with a partial report.

**Step 2 — Write the executive summary.**
Read all four artifacts. Write exactly 5 sentences or fewer that answer:

1. How large is the legacy codebase? (programs, DDMs, lines of code if counted)
2. How many confirmed business rules were found?
3. How connected is the system? (dense call graph vs. isolated programs)
4. What is the greatest risk when entering Stage 2? (the recorded open question with the highest impact)
5. What is the team's confidence level for modernization? (high/medium/low, based on evidence)

**Step 3 — Build the "What We Know" section.**
From the business-rule catalog, extract only rules classified as "confirmed." List them with their EARS notation candidates and source references.

From the dependency map, list verified program-to-program and program-to-data edges. Include total counts.

From the inventory, summarize the documented DDM structures.

Every statement must cite its source artifact: `[See business-rules-catalog.md, Rule #3](../../01-archaeology/business-rules-catalog.md)`.

**Step 4 — Build the "What Introduces Risk" section.**
From the open-question catalog, extract only rows whose status does not record
human validation. Preserve the question, `path:line` evidence, impact, unconfirmed
hypothesis, owner, and status. Do not add an answer, resolution path, or
interpretation.

From the business-rule catalog, extract rules classified as "inferred" (code only, without documentation support). They are not confirmed and introduce risk if used as a basis for requirements.

**Step 5 — Propose boundary hypotheses.**
Analyze the dependency map for clusters — groups of programs strongly connected to one another and weakly connected to other groups. Each cluster is a candidate bounded context.

For each hypothesis, provide:

- A business-language name (not technical jargon)
- Which programs belong to it
- Which DDMs it owns
- A one-line rationale explaining why this is a natural boundary

Propose 3–5 hypotheses. Explicitly label them as hypotheses, not decisions. The `@architect` in Stage 2 will evaluate and decide.

**Step 6 — List source artifacts.**
At the end of the report, list all four source artifacts with relative paths so anyone can navigate to the details.

**Step 7 — Add team sign-off.**
Add a team sign-off section: "Reviewed by: [names], Date: [date], Confidence: [high/medium/low]." Leave it blank for the team to complete.

Write the complete report to `01-archaeology/discovery-report.md`. The report must be self-contained and fewer than 3 printed pages.

## Invocation Example

```
/discovery-report team="Team 07"
```

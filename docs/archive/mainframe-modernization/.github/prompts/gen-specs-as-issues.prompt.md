---
name: "gen-specs-as-issues"
description: "Identify gaps between the SIFAP legacy behavior and the modern spec, prioritize them, and open EARS-backed GitHub issues with legacy traceability."
argument-hint: "area=<focus-area> repo=<owner/name>"
agent: "requirements-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /gen-specs-as-issues

## Objective

Find missing or under-specified behavior for the SIFAP 2.0 modernization, prioritize it, and turn the top items into detailed GitHub issues. Each issue is an EARS specification with a unique REQ-ID and a mandatory `source_legacy:` line, so every requirement stays traceable from legacy Natural/Adabas code to the modern system.

> [!IMPORTANT]
> The `legacy-traceability` CI job rejects any requirement without a `source_legacy:` line. Every issue this command opens must cite a legacy artifact or be justified as `[GREENFIELD]`.

## When to Invoke

During Stage 2 (specification) or Stage 4 (evolution), when the team needs to convert observed gaps into a prioritized, trackable backlog of specifications.

## Preconditions

- The pair has read the relevant legacy programs — the HARD GATE in [`LEGACY-EXPLORATION-CHECKLIST.md`](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md)
- The modern specification under `02-modern-spec/` (and any `specs/`) is available to compare against
- The team is authenticated to the target GitHub repository

## Inputs the Team Must Provide

- `area` — the focus area or bounded context to analyze (for example, payment inspection)
- `repo` — the `owner/name` of the GitHub repository for the issues
- The legacy programs relevant to the area, under `01-archaeology/legacy-sifap/`
- Ask the user for anything that is missing.

## What I Will Do

- Compare legacy behavior in the focus area against the modern spec and list the gaps
- Score each gap by impact and risk, and select the top items to file
- Write each issue as an EARS requirement following [`requirements.instructions.md`](../instructions/requirements.instructions.md)
- Assign a unique REQ-ID and a `source_legacy:` line, then open the issues via the `gh` CLI

## What I Will NOT Do

- Write a requirement without a `source_legacy:` line (or an explicit `[GREENFIELD]` justification)
- Invent behavior that is absent from both the legacy system and the modern spec
- Open issues before the team confirms the prioritized list
- Assign a `spec/` branch to implementation work — these are Stage-2 spec issues on `spec/<NNN>-<feature>`

## Output Format

```markdown
### Gap analysis — <area>
Gaps found: 6 · Selected to file: 3

### Issues to create
- [SPEC][REQ-014] When a payment exceeds the daily limit, the system shall flag it for review
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/SIFAP-P.NSP
  branch: spec/014-daily-limit-review
```

## Definition of Done

- [ ] Each selected gap is written in EARS notation with a unique REQ-ID
- [ ] Each issue carries a `source_legacy:` line (or a `[GREENFIELD]` justification)
- [ ] Each issue names a `spec/<NNN>-<feature>` branch
- [ ] Issues are created via `gh` only after the team confirms the list

## Prompt Body

You produce a prioritized, traceable specification backlog. The EARS notation and REQ-ID rules live in [`requirements.instructions.md`](../instructions/requirements.instructions.md); use the [`ears-validate`](../skills/ears-validate/SKILL.md) skill to check each statement before you file it.

**Step 1 — Establish the baseline.**
Read the legacy programs for `area` under `01-archaeology/legacy-sifap/` and the modern spec under `02-modern-spec/`. Confirm the reading gate in the [checklist](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md) is met.

**Step 2 — Find and score gaps.**
List behavior present in the legacy system but missing or vague in the modern spec. Score by impact and risk; select the top items.

**Step 3 — Write EARS requirements.**
For each selected gap, write an EARS statement, assign the next REQ-ID, and add the `source_legacy:` line pointing at the legacy artifact. Validate with [`ears-validate`](../skills/ears-validate/SKILL.md).

**Step 4 — Confirm, then file.**
Present the list with proposed `spec/<NNN>-<feature>` branches. After approval, open the issues with `gh`.

## Invocation Example

```
/gen-specs-as-issues area="payment inspection" repo=my-org/sifap-2
```

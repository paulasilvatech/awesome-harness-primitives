---
name: "generate-docs"
description: "Generate one developer-facing document (README, runbook, API reference, or ADR skeleton) for a SIFAP 2.0 module, faithful to the code and the doc style guide."
argument-hint: "type=readme|runbook|api-reference|adr module=<folder> audience=<who>"
agent: "tech-writer"
tools: ["read", "search", "edit"]
---
# /generate-docs

## Objective

Produce one of four document types for a SIFAP 2.0 module — a **README**, a
**runbook**, an **API reference**, or an **ADR skeleton** — using the project's
standard frontmatter, terminology, and tone. The document is concise, navigable,
and faithful to reality: no marketing language, no aspirational claims, and every
command verified against the code.

## When to Invoke

In Stage 3 or 4, once a module the team created has enough code to document, or
when an existing document must be regenerated after a change.

## Preconditions

- The target module exists under `backend/`, `frontend/`, `infra/`, or another area the team created
- The code sources of truth are readable (`pom.xml`, `package.json`, `application.yml`, controllers, the OpenAPI spec, migrations)
- The conventions in [`../../docs/DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) apply to everything produced outside `.github/`

## Inputs the Team Must Provide

- The document type: `readme`, `runbook`, `api-reference`, or `adr`
- The target module folder
- The audience (for example, "new contributor, week 1"; "on-call SRE at 03:00"; "external API consumer")
- The linked `REQ-ID` values, if applicable

Ask the user for anything that is missing.

## What I Will Do

- Choose the correct template for the requested type
- Read the code as the source — `pom.xml`, `package.json`, `application.yml`, controllers, the OpenAPI spec, migrations — and cite exact strings
- Apply the standard frontmatter (`title`, `audience`, `last_reviewed`, `owner`, `linked_reqs`)
- Keep within size limits, add cross-links, and set `last_reviewed` to today
- Verify every command is executable in the team's repository
- Apply the style guide via [`../skills/doc-style-lint/SKILL.md`](../skills/doc-style-lint/SKILL.md); for an ADR, follow [`../skills/adr-draft/SKILL.md`](../skills/adr-draft/SKILL.md)

## What I Will NOT Do

- Invent domain names, endpoints, modules, or legacy mappings — I write only what the code and the team confirm
- Use marketing language or claim capabilities that do not exist yet
- Add an inline markdownlint pragma or tell the reader to add one — the root config already relaxes those rules (style guide §9)
- Add emojis or saturated-color diagrams — I use GFM alerts and the neutral Mermaid palette
- Write requirements or make architecture decisions — those are redirected to the requirements and architect personas

## Output Format

The document at its canonical path:

- README → `<module-folder>/README.md`
- Runbook → `docs/runbooks/<short-slug>.md`
- API reference → `docs/api/<service>/<endpoint-slug>.md`
- ADR → `docs/adr/<NNNN>-<title>.md` (copied from `docs/adr/0000-template.md`)

README template (illustrative):

````markdown
---
title: "disburse-retry"
audience: "new contributor, week 1"
last_reviewed: "2026-05-04"
owner: "@alex"
linked_reqs: [REQ-042]
---

# disburse-retry

Purpose confirmed in the code and specification.

## Quick start
A verified executable command.

## Public API
| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/v1/disbursements/{id}/retry | Retry a failed disbursement |

## Tests
A verified command (for example, `./mvnw -pl disburse test`).

## Legacy lineage
`<program>.NSP` and the team-confirmed evidence, when applicable.

---

### Continue reading
Navigation footer per style guide section 8.
````

Runbook, API reference, and ADR reuse the same frontmatter with their own
sections (runbook: When this appears, Severity, Diagnose, Mitigate, Verify, Escalate).

## Definition of Done

- [ ] Frontmatter is complete (`title`, `audience`, `last_reviewed`, `owner`, `linked_reqs`)
- [ ] Every command in the document can be copied and executed
- [ ] The size is within the limit (README ≤ 80 lines, ADR ≤ 2 pages)
- [ ] At least two cross-links to related documents are present
- [ ] Legacy lineage is named only where the team confirmed it
- [ ] No marketing language, aspirational claims, emojis, or markdownlint pragmas
- [ ] The document is at the canonical path and ends with the section 8 navigation footer

## Prompt Body

You are the `@tech-writer`. The team asked for one document, faithful to the code
and the style guide.

**Step 1 — Pick the template.**
README for "what is this and how do I run it." Runbook for "production broke at
03:00; what do I do?" API reference for "I will consume this from another
service." ADR for "we chose X over Y and need to record why" — for an ADR, use the
`adr-draft` skill and copy `docs/adr/0000-template.md`.

**Step 2 — Read the code, not memory.**
Open `pom.xml`, `package.json`, `application.yml`, controllers, the OpenAPI spec,
and migrations. Cite exact strings. Do not invent domain names or endpoints.

**Step 3 — Apply frontmatter and size limits.**
Add `title`, `audience`, `last_reviewed`, `owner`, and `linked_reqs`. Respect the
limits: README ≤ 1 page (~80 lines), runbook ≤ 1 page per scenario, API reference
per endpoint, ADR ≤ 2 pages.

**Step 4 — Verify every command.**
Confirm each command exists and runs in the team's repository (`Makefile`,
`package.json`, `pom.xml`). Never write "run the tests" without the exact command.

**Step 5 — Cross-link and date.**
Link README to CODEMAP, `spec.md`, and the runbook; runbook to dashboards and
alert names; ADR to superseded or superseding ADRs. Set `last_reviewed` to today —
drift begins the moment the document is written.

**Step 6 — Style pass.**
Run the `doc-style-lint` skill: active voice, no emojis, neutral Mermaid, GFM
alerts, and the section 8 navigation footer. Never add a markdownlint pragma.

Domain terms may stay in PT-BR, but explanations are in English. State current
reality; document plans separately.

## Invocation Example

```
/generate-docs type=runbook module=backend/disburse audience="on-call SRE"
```

---
name: "setup-project"
description: "Initialize a project's Copilot context-engineering scaffold: AGENTS.md, CODEMAP.md, and the .github instructions, prompts, and agents baseline."
argument-hint: "root=<repo-root>"
agent: "tech-lead"
tools: ["read", "search", "edit", "execute"]
---
# /setup-project

## Objective

Bootstrap the Copilot context-engineering scaffold for a project that lacks one:
`AGENTS.md`, `CODEMAP.md`, `.github/copilot-instructions.md`, and baseline
`.github/instructions/`, `.github/prompts/`, and `.github/agents/` files. The
result is stack-specific, scoped, and secret-free — ready for the team to extend.

## When to Invoke

At the start of a project, or when an existing project lacks a Copilot context
surface. In this workshop the team creates `backend/`, `frontend/`, and `infra/`
from scratch in Stage 3 — this prompt scaffolds the context files, never an
application prototype.

## Preconditions

- A repository root the team can write to
- Agreement to use the approved toolchain in [`../copilot-instructions.md`](../copilot-instructions.md) (VS Code, GitHub Copilot Ask/Plan/Agent, Copilot CLI, Spec-Kit, GitHub, Docker Compose, Terraform)

## Inputs the Team Must Provide

- The repository root path
- The primary stack, if it cannot be detected from manifests

Ask the user for anything that is missing.

## What I Will Do

- Detect the stack from `package.json`, `pom.xml`, `requirements.txt`, or `*.csproj`
- Create `AGENTS.md` with a stack summary and the verified build, test, and lint commands
- Create a `CODEMAP.md` skeleton with `## Modules`, `## Data Flow`, and `## External Integrations`
- Create `.github/copilot-instructions.md` with the team's language, tone, and security rules
- Add baseline `.github/instructions/*.instructions.md` files, each with a specific `applyTo:` scope
- Stage the changes without committing, and print the created files
- Recommend running [`/audit-context`](persona-technical-lead-audit-context.prompt.md) and the [`../skills/context-audit/SKILL.md`](../skills/context-audit/SKILL.md) skill afterward

## What I Will NOT Do

- Create an application prototype, `backend/`, `frontend/`, or `infra/` — those are the team's Stage 3 work
- Write a generic `AGENTS.md` — it must reflect the detected stack
- Use `applyTo: "**"` — every instructions file gets a specific glob
- Commit, or write any secret, credential, or `TODO` placeholder into the scaffold
- Add a tool outside the approved toolchain — an exception is redirected to an ADR via [`../skills/adr-draft/SKILL.md`](../skills/adr-draft/SKILL.md)

## Output Format

A created-file report printed after staging. Example (illustrative):

```markdown
## Scaffold created — 6 files staged

- /repo/AGENTS.md
- /repo/CODEMAP.md
- /repo/.github/copilot-instructions.md
- /repo/.github/instructions/backend.instructions.md   (applyTo: backend/**/*.java)
- /repo/.github/instructions/frontend.instructions.md  (applyTo: frontend/**/*.ts)
- /repo/.github/prompts/README.md

Suggested first commit: "chore: add Copilot context-engineering scaffold"

Follow-up (manual):
1. Fill CODEMAP.md once the first module exists.
2. Run /audit-context to verify scopes.
3. Review copilot-instructions.md security rules with the team.
```

## Definition of Done

- [ ] `AGENTS.md` is specific to the detected stack, not generic
- [ ] Every instructions file has a specific `applyTo:` scope (no `**`)
- [ ] No secrets, credentials, or `TODO` placeholders are present
- [ ] `.gitignore` is updated if new folders need tracking rules
- [ ] Changes are staged but not committed, with the file list printed
- [ ] A suggested commit message and three manual follow-ups are included

## Prompt Body

You are the `@tech-lead`. The team wants a clean Copilot context scaffold to build
on.

**Step 1 — Detect the stack.**
Inspect `package.json`, `pom.xml`, `requirements.txt`, and `*.csproj` to identify
languages, frameworks, and the build, test, and lint commands. If nothing is
detectable, ask the team for the primary stack.

**Step 2 — Write AGENTS.md.**
Summarize the detected stack, code conventions, and the verified build, test, and
lint commands. Keep it specific — a newcomer should learn the stack from this file
alone.

**Step 3 — Write the CODEMAP.md skeleton.**
Create `CODEMAP.md` with `## Modules`, `## Data Flow`, and `## External
Integrations`. Leave the module list for the team to populate through
[`/update-codemap`](persona-tech-writer-update-codemap.prompt.md) once modules exist.

**Step 4 — Write copilot-instructions.md.**
Record the team's language, tone, security rules, and the approved toolchain. Do
not restate the whole global file — link to it and add only what is
project-specific.

**Step 5 — Add scoped instruction files.**
For each detected area, add a `*.instructions.md` file with a specific `applyTo:`
glob (for example, `backend/**/*.java`, `frontend/**/*.ts`). Follow the
conventions in [`../instructions/README.md`](../instructions/README.md). Never use
`applyTo: "**"`.

**Step 6 — Stage and report.**
Stage the changes with git but do not commit. Print the absolute paths of created
files, a suggested first commit message, and three manual follow-ups.

Never write a secret or a placeholder into the scaffold, and never scaffold an
application prototype — the team owns that.

## Invocation Example

```
/setup-project root=.
```

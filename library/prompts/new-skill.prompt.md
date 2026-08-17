---
name: 'new-skill'
description: 'Scaffold a new GitHub Copilot Agent Skill using the skill-creator skill workflow.'
agent: 'agent'
argument-hint: 'skill name and what it should do'
---

# /new-skill

## Objective

Scaffold a new GitHub Copilot Agent Skill under `library/skills/` by routing the authoring workflow through the `skill-creator` skill and aligning the result with the current `skill.template.md` structure, validation expectations, progressive-disclosure model, and description quality bar.

## When to Invoke

Use this prompt when a user asks to create, scaffold, draft, or validate a new reusable GitHub Copilot Agent Skill for this repository.

## Preconditions

- The `skill-creator` primitive is available as a skill in VS Code.
- The requested skill name, purpose, and activation triggers are known or can be requested.
- Edits under `library/skills/<name>/` are permitted.
- The author can add `references/`, `assets/`, or `scripts/` only when real content requires those bundled resources.

## Inputs the Team Must Provide

- Skill name — lowercase, hyphenated, and used as the folder name and frontmatter `name`.
- Purpose — what the skill does.
- Concrete triggers — keywords and phrases that should activate it.
- Whether the skill needs `references/` for on-demand Markdown, `assets/` for templates or static resources, or `scripts/` for runnable helpers.
- Ask the user for anything that is missing, and stop if the required authoring primitive is unavailable.

## What I Will Do

- Route the request to `skill-creator` (type: skill) before drafting or editing the skill.
- Create `library/skills/<name>/SKILL.md` with valid frontmatter on line 1 and a folder name that equals `name`.
- Use the current mandatory skill spine: `## When to invoke`, at least one real domain section with a freely titled heading, `## Output template`, and `## Quality gate`.
- Include conditional sections such as `## Inputs`, `## Prerequisites and context`, `## Procedure`, `## Criteria`, `## Examples`, `## Limits`, `## Gotchas`, `## Troubleshooting`, `## Progressive disclosure and bundled resources`, `## Related primitives`, and `## References` only when their trigger is earned by real content.
- Keep `description` within 1024 characters, state what the skill does and when to use it, and enrich it with concrete trigger language.

## What I Will NOT Do

- Draft or edit the skill if `skill-creator` is unavailable in VS Code.
- Use the obsolete `## When to use` heading or a generic `## Workflow`/`## References` skeleton when the current template requires different sections.
- Add dangling references to `references/`, `assets/`, or `scripts/` resources that do not exist.
- Add sandbox home paths, `/mnt/...` paths, hard platform-product dependencies, unsupported metrics, or unverified claims.
- Narrate process steps in the final response when the requested output is a concise path and validation status.

## Output Format

Return only the concise creation result:

```markdown
### New Skill Result

### Skill Path
- `library/skills/<name>/SKILL.md`

### Validation Status
- Frontmatter starts on line 1: `<passed|failed>`
- Folder name equals `name`: `<passed|failed>`
- Mandatory sections present in order: `## When to invoke`, `<domain section>`, `## Output template`, `## Quality gate`: `<passed|failed>`
- Conditional sections earned by real content: `<passed|failed>`
- Bundled resources under `references/`, `assets/`, or `scripts/` exist and are referenced only when needed: `<passed|failed|not applicable>`
- Script check: `<command and result, or not applicable>`

### Critical Findings or Blockers
- `<finding or none>`
```

## Definition of Done

- [ ] The request was routed to `skill-creator` before drafting or editing.
- [ ] `library/skills/<name>/SKILL.md` exists and frontmatter parses from line 1.
- [ ] Folder name matches `name`, and `description` is rich with positive triggers and within 1024 characters.
- [ ] The delivered skill uses `## When to invoke`, at least one real domain section, `## Output template`, and `## Quality gate`.
- [ ] Every referenced file in `references/`, `assets/`, or `scripts/` exists, and any script is self-contained and runnable in this environment.
- [ ] The final response includes only the skill path, validation status, and critical findings or blockers.

## Prompt Body

Follow these steps in order. This prompt is a meta-primitive for authoring skills and must track the current skill template.

**Step 1 — Route through the authoring skill.** Load and use `skill-creator` (type: skill) before drafting or editing. If `skill-creator` is unavailable in VS Code, stop and report that the required authoring primitive is missing.

**Step 2 — Collect the required inputs.** Ask for missing skill name, purpose, activation triggers, and bundled resource needs. Validate that the name is lowercase and hyphenated. Treat it as the folder name and the frontmatter `name`.

**Step 3 — Create the skill location and frontmatter.** Create `library/skills/<name>/SKILL.md` with frontmatter on line 1:

```markdown
---
name: <name>
description: "<what it does>. Use this skill when <triggers and keywords>."
---
```

Keep `description` within 1024 characters and use concrete positive trigger phrases.

**Step 4 — Use the current skill section map.** After the H1 and overview, include `## When to invoke`, at least one freely titled domain section that carries real rules, commands, patterns, examples, or decision criteria, `## Output template`, and `## Quality gate`. Add optional frontmatter such as `user-invocable`, `argument-hint`, or `allowed-tools` only for concrete need. Include `## Inputs` when `argument-hint` is set. Use `## Procedure` only when order is load-bearing. Use `## Criteria` for reviews or evaluations. Add examples, limits, gotchas, troubleshooting, progressive disclosure, related primitives, or references only when their trigger is real.

**Step 5 — Add bundled resources only when needed.** Add `references/`, `assets/`, or `scripts/` only if the skill needs on-demand Markdown, templates/static resources, or runnable helpers. Reference each resource from `SKILL.md` and avoid dangling links. Keep `SKILL.md` focused and push depth into `references/` for progressive disclosure. Make scripts self-contained, prefer the standard library, and ensure they run in this environment.

**Step 6 — Enforce authoring rules.** Keep the skill portable: no sandbox home paths, no `/mnt/...` paths, no hard platform-product dependency unless the skill truly requires it. Write in English. Use “GitHub Copilot” rather than bare “Copilot”. Do not use em dashes. Never fabricate metrics.

**Step 7 — Validate and report.** Confirm that the skill appears in the available-skills list when frontmatter parsing is available. Check that the folder name matches `name`, every referenced file exists, and any script runs. Return only the skill path, validation status, and critical findings or blockers.

## Invocation Example

```
/new-skill name=api-contract-review purpose="review API contracts" triggers="review OpenAPI, API compatibility, breaking changes"
```

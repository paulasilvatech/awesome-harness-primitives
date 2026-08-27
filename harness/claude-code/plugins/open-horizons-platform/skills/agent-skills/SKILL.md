---
name: agent-skills
description: >-
  Applies current portable Agent Skill conventions for discovery metadata, progressive disclosure,
  bundled resources, safety, and validation. Use when creating or updating SKILL.md.
paths:
  - "**/skills/**/SKILL.md"
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/agent-skills.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Agent Skill Conventions - Portable On-Demand Capabilities

These instructions apply to `SKILL.md` files matched by
`**/skills/**/SKILL.md`. They are authoritative for repository Skill identity,
discovery metadata, body shape, bundled resources, and quality gates; the Agent
Skills standard and `.github/harness/COPILOT-HARNESS.md` win for runtime format,
while the `skill-creator` skill owns the ordered creation, repair, audit, and
validation workflow.

## Skill Responsibility

Use a `skill` for a reusable capability, procedure, review method, or task-specific knowledge package that may include scripts and resources. Use `instructions` for passive conventions, an `agent` for persona and judgment, and a `prompt` for a user-invoked VS Code action.

Author the canonical package at `.github/skills/<name>/`. This repository has no
primitive mirror or synchronization manifest; do not create or maintain a
second copy.

## Discovery Metadata

- `name` is required, uses kebab-case, is 1-64 characters, contains no double hyphen, and exactly matches the parent directory.
- `description` is required, is 1-1024 characters, and states both what the skill does and when it should load.
- Keep positive trigger terms in the description. Put exclusions and non-goals in `## Limits`.
- Add `argument-hint` only when user arguments change execution; consume and validate `$ARGUMENTS` in `## Inputs`.
- Add `allowed-tools`, invocation controls, license metadata, tags, or metadata only for a concrete need supported by the target surfaces.

## Body and Progressive Disclosure

Follow the established same-type structure. Every delivered Skill contains:

1. One H1 and a concise summary
2. `## When to invoke`
3. At least one freely titled domain section
4. `## Output template`
5. `## Quality gate`

Add `## Procedure` only when order is load-bearing and `## Criteria` when judgment is primary. Add prerequisites, limits, gotchas, troubleshooting, examples, related primitives, or references only when they carry real content.

Keep `SKILL.md` under 500 lines and preferably under 200. Move detailed reference material to `references/`, deterministic automation to `scripts/`, static output assets to `assets/`, and modifiable scaffolds to `templates/`. Reference bundled resources with relative links from inside the same Skill package.

## Scripts, Safety, and Portability

- Reuse the repository's existing runtimes and dependencies where possible.
- Give scripts a clear interface, explicit errors, safe path handling, and help text when directly executable.
- Keep credentials out of files and logs; use existing credential providers and environment configuration.
- Require explicit confirmation or a deliberate flag for irreversible actions.
- Document network access, data leaving the workspace, platform assumptions, and non-obvious failure modes.
- Do not claim cross-surface portability until representative behavior is verified.

## Freshness and Validation

Use the local harness contract first. Verify first-party VS Code, GitHub, or
Agent Skills documentation when the user requests current behavior, a relevant
version changed, sources conflict, or the local contract marks behavior
unresolved.

Run:

```sh
python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict
python3 .github/skills/verify-skills.py
python3 scripts/update-copilot-inventory.py --check
```

Also execute changed bundled scripts or focused tests that cover their behavior.

## Conventions

| Rule | Rationale |
| --- | --- |
| Route Skill work to `skill-creator`. | One workflow owns packaging, validation, and quality decisions. |
| Keep discovery metadata concise and trigger-rich. | Copilot decides whether to load the body from `name` and `description`. |
| Keep the core body small and move detail into typed resources. | Progressive disclosure protects context budget. |
| Include only conditional sections that have concrete content. | Empty scaffolding weakens activation and usability. |
| Validate the package and repository inventory. | A readable `SKILL.md` alone does not prove resources or discovery metadata are correct. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Teach repository-specific or non-obvious knowledge. | Repeat generic language or framework tutorials. |
| Use a procedure for ordered execution and criteria for judgment. | Force open-ended review into rigid steps. |
| Link only to resources bundled inside the same Skill. | Use relative links to other primitives or external package paths. |
| Keep gotchas proactive and troubleshooting reactive. | Mix preventive constraints with vague recovery advice. |
| Test scripts and report blocked checks honestly. | Treat readable Markdown as proof the Skill works. |

## Checklist Before Opening a PR

- [ ] `name` is valid, matches the directory, and `description` states what and when.
- [ ] The Skill owns a reusable capability rather than passive conventions or persona.
- [ ] Mandatory sections appear once and in template order.
- [ ] Optional metadata and sections are justified by actual behavior.
- [ ] Bundled resources use the correct directory and valid relative links.
- [ ] Scripts have explicit input, output, errors, safety boundaries, and focused tests.
- [ ] No secret, private content, hidden network transfer, or unsafe default is present.
- [ ] Current compatibility claims have dated first-party evidence.
- [ ] The three repository-owned primitive gates pass.

## References

- Agent Skills standard: https://agentskills.io/
- VS Code Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills

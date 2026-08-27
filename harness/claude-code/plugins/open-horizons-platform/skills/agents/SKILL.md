---
name: agents
description: >-
  Applies current repository conventions for custom-agent metadata, tool scope, body structure,
  runtime boundaries, and validation. Use when creating or updating an agent.
paths:
  - "**/*.agent.md"
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/agents.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Custom Agent Conventions - Focused Runtime Personas

These instructions apply to custom-agent files matched by `**/*.agent.md`. They
are authoritative for this repository's agent naming, metadata, tool policy,
body contract, and validation. Use `.github/harness/COPILOT-HARNESS.md` as the
local runtime contract. Apply first-party target-surface documentation only
after checking the documented local divergence.

## Agent Responsibility

Use an `agent` for a reusable persona, judgment boundary, operating posture, or deliberately restricted tool policy. Put passive file conventions in `instructions`, reusable procedures or capabilities in a `skill`, and explicit VS Code actions in a `prompt`.

Author the canonical source at `.github/agents/<name>.agent.md`. The filename is the discovery key on every surface, so keep it kebab-case and stable.

## Metadata and Discovery

- Keep `description` non-empty, concise, and explicit about what the agent does and when it should be selected.
- Keep one identity per agent. Omit `name`, or set it to the exact kebab-case filename slug; never use a title-style display name such as `"Azure AVM Bicep mode"`.
- Omit `model` unless a fixed, verified model is a deployment requirement.
- Treat `tools` as an allow-list filter. Omit it for full inherited capability or list only verified tool tokens required by the agent.
- Use `user-invocable`, `disable-model-invocation`, and `mcp-servers` only when the behavior is intentional and supported by the target runtime.
- Do not use `agents`; the local harness records it as unsupported agent
  frontmatter. Use body-level handoff guidance and a supported delegation tool
  when delegation is intentional.
- Treat `argument-hint` and `handoffs` as VS Code-specific. The local harness
  records them as ignored by the tested Copilot CLI.
- Do not depend on `target` for Copilot CLI routing without new runtime evidence; the tested CLI ignored it.

## Tool Scope

Use the surface-aware vocabulary from
`.github/harness/COPILOT-HARNESS.md`. Common focused sets are:

| Agent posture | Typical tools |
| --- | --- |
| Read-only dual-surface review | `read`, `search`, `grep`, `glob` |
| Editing | Read-only set plus `edit` |
| Command execution | Add `execute` only when commands are required |
| Delegation | Add `agent` only when the agent owns orchestration |
| Dual-surface web verification | `web` plus `web_fetch` and/or `web_search` |

Official aliases include `read`, `search`, `edit`, `execute`, `agent`, `web`,
and `todo`. The tested local CLI exposes companion spellings such as `grep`,
`glob`, `web_fetch`, and `web_search`. For dual-surface capability, keep both
spellings where the local harness records unresolved divergence. Do not treat
official aliases as universally invalid, and do not assume an alias expanded in
the tested local CLI when it did not.

Tool availability is not approval. VS Code permission levels, per-tool approval, URL approval, terminal
approval, sandboxing, and managed organizational rules are session or policy controls; do not add a
`permissions` frontmatter field.

## Body Contract

Use the established same-type structure. Keep the mandatory spine in order:

1. `## Mission`
2. `## Activation and Scope`
3. `## Operating Principles`
4. `## What This Agent Knows`
5. `## What This Agent Does NOT Know`
6. Freely titled domain sections and an ordered procedure only when needed
7. `## Output Format`
8. `## Definition of Done`
9. `## Anti-Patterns This Agent Rejects`
10. `## Integrations and Handoffs` only when another named primitive participates

State an explicit write policy under activation and scope. Keep the knowledge boundary separate from behavioral prohibitions. Make output and completion criteria observable, and keep the body at or below 30,000 characters.

## Freshness and Runtime Testing

Use the local harness evidence before external research. Verify first-party
documentation when a changed field or behavior is unresolved, the target
version changed, sources conflict, or the user requests current behavior. Do
not add unverified compatibility claims to the agent.

Test representative invocations in every surface the agent claims to support. Confirm the effective tool set, not just the YAML spelling.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep the canonical source under `.github/agents/`. | The repository has one versioned primitive source. |
| Define one focused persona and authority boundary. | Selection and handoff behavior stay predictable. |
| Omit optional metadata unless it changes verified behavior. | Surface-specific or stale fields do not create false confidence. |
| Grant the smallest effective tool set. | The allow-list cannot silently remove a required capability. |
| Separate known facts, unknowns, behavior, output, and done criteria. | Agents do not invent local state or hide incomplete work. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use the agent template and same-type references. | Copy structure from prompts, skills, or legacy tutorials. |
| Verify target-surface fields and tool tokens. | Assume a VS Code field works in Copilot CLI. |
| Reference companion primitives by installed name and type. | Link to another primitive with a relative path. |
| Report unverified behavior as unknown. | Describe a warning, fallback, or unsupported field as a guarantee. |
| Regenerate the repository inventory after adding or renaming an agent. | Let `name` and the filename drift into two competing identities. |

## Checklist Before Opening a PR

- [ ] The agent has a valid kebab-case canonical filename and a non-empty discovery description.
- [ ] Optional metadata is present only for a concrete, verified runtime need.
- [ ] Every listed tool token grants the intended capability in the target runtime.
- [ ] The mandatory agent sections appear once and in template order.
- [ ] Activation includes expected inputs, authority, writable paths, protected paths, and handoff conditions.
- [ ] Knowledge gaps are discovered or reported rather than invented.
- [ ] Output format, definition of done, and rejected anti-patterns are concrete.
- [ ] Local harness or first-party evidence supports compatibility claims.
- [ ] `python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict` passes.
- [ ] `python3 .github/skills/verify-skills.py` passes.
- [ ] `python3 scripts/update-copilot-inventory.py --check` passes.

## References

- VS Code custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- GitHub custom agent configuration: https://docs.github.com/en/copilot/reference/custom-agents-configuration

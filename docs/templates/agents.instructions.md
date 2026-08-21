---
applyTo: "**/*.agent.md"
description: "Applies current repository conventions for custom-agent metadata, tool scope, body structure, runtime boundaries, and validation. Use when creating or updating an agent."
---

# Custom Agent Conventions - Focused Runtime Personas

These instructions apply to custom-agent files matched by `**/*.agent.md`. They are authoritative for this repository's agent naming, metadata, tool policy, body contract, and validation. Use `docs/COPILOT-HARNESS-SPEC.md` as the maintained Copilot CLI contract; when dated evidence in `docs/HARNESS-VALIDATION.md` contradicts it, update the spec before dependent guidance. Apply first-party target-surface documentation only after its behavior is verified and the local evidence is updated.

## Agent Responsibility

Use an `agent` for a reusable persona, judgment boundary, operating posture, or deliberately restricted tool policy. Put passive file conventions in `instructions`, reusable procedures or capabilities in a `skill`, and explicit VS Code actions in a `prompt`.

Author the canonical source at `harness/github-copilot/agents/<name>.agent.md`. Install declared repository agents through `python3 harness/github-copilot/scripts/sync_installed_primitives.py`; do not edit `.github/agents/` independently.

## Metadata and Discovery

- Keep `description` non-empty, concise, and explicit about what the agent does and when it should be selected.
- Omit `name` when the filename already provides the intended display name.
- Omit `model` unless a fixed, verified model is a deployment requirement.
- Treat `tools` as an allow-list filter. Omit it for full inherited capability or list only verified tool tokens required by the agent.
- Use `user-invocable`, `disable-model-invocation`, and `mcp-servers` only when the behavior is intentional and supported by the target runtime.
- Use the VS Code-only `agents` field only for an explicit subagent allow-list. When `tools` is restricted, include the `agent` tool or the allow-list cannot be invoked.
- Treat `argument-hint` and `handoffs` as VS Code-specific. The tested Copilot CLI version records them as ignored in `docs/HARNESS-VALIDATION.md`.
- Do not depend on `target` for Copilot CLI routing without new runtime evidence; the tested CLI ignored it.

## Tool Scope

Use exact Copilot CLI tokens from `docs/COPILOT-HARNESS-SPEC.md`. Common focused sets are:

| Agent posture | Typical tools |
| --- | --- |
| Read-only review | `read`, `grep`, `glob` |
| Editing | Read-only set plus `edit` |
| Command execution | Add `execute` only when commands are required |
| Delegation | Add `agent` only when the agent owns orchestration |
| Web verification | Add `web_fetch`; add `web_search` only when locating a first-party source is necessary |

Do not use no-op aliases such as `search`, `web`, `todo`, `all`, `terminal`, `run`, `codebase`, `changes`, `fetch`, `githubRepo`, or `search/codebase`. Unrecognized tokens are silently dropped and can leave an agent unable to perform its task.

A deliberately `target: vscode` agent may use the current VS Code aliases `search`, `web`, or `todo`.
Cross-surface agents must use the measured Copilot CLI-safe spellings until dated runtime evidence changes.

Tool availability is not approval. VS Code permission levels, per-tool approval, URL approval, terminal
approval, sandboxing, and managed organizational rules are session or policy controls; do not add a
`permissions` frontmatter field.

## Body Contract

Start from `docs/templates/agent.template.md`. Keep the mandatory spine in order:

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

Use dated local evidence before external research. Verify first-party documentation when a changed field or behavior is unverified, the target version changed, sources conflict, the user requests current behavior, or the recorded evidence is older than 90 days. Record the source URL, date, target surface, result, and divergence in `docs/HARNESS-VALIDATION.md`; do not add undated compatibility claims to the agent.

Test representative invocations in every surface the agent claims to support. Confirm the effective tool set, not just the YAML spelling.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep the canonical source under `harness/github-copilot/agents/`. | Installed and plugin copies remain reproducible. |
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
| Synchronize generated copies with repository scripts. | Hand-edit `.github/agents/` or plugin-local agents. |

## Checklist Before Opening a PR

- [ ] The agent has a valid kebab-case canonical filename and a non-empty discovery description.
- [ ] Optional metadata is present only for a concrete, verified runtime need.
- [ ] Every listed tool token grants the intended capability in the target runtime.
- [ ] The mandatory agent sections appear once and in template order.
- [ ] Activation includes expected inputs, authority, writable paths, protected paths, and handoff conditions.
- [ ] Knowledge gaps are discovered or reported rather than invented.
- [ ] Output format, definition of done, and rejected anti-patterns are concrete.
- [ ] Dated evidence supports current compatibility claims.
- [ ] `python3 harness/github-copilot/scripts/validate_primitives.py --strict` passes.
- [ ] Catalog and declared installed or plugin copies are synchronized.

## References

- VS Code custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- GitHub custom agent configuration: https://docs.github.com/en/copilot/reference/custom-agents-configuration

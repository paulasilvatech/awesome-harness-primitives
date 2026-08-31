---
paths:
  - harness/claude-code/**
  - ".claude/**"
  - CLAUDE.md
  - ".claude-plugin/marketplace.json"
  - docs/catalog/claude-code.md
  - docs/CLAUDE-CODE-*.md
  - ".github/workflows/validate-primitives.yml"
---

<!-- Generated from harness/github-copilot/instructions/claude-code-harness.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Governs generated Claude Code primitives, installed mirrors, evidence, and validation. Use when changing harness/claude-code, .claude, CLAUDE.md, the Claude marketplace, or Claude harness documentation.

# Claude Code Harness Conventions - Generated and Verifiable

These instructions apply to the generated Claude Code harness, its installed repository copies, marketplace, catalog, documentation, and CI integration. They are authoritative for source ownership, conversion boundaries, generated-file hygiene, and Claude-specific validation; repository-wide governance owns shared precedence, while `docs/CLAUDE-CODE-HARNESS-SPEC.md` wins for Claude Code runtime and schema details.

## Authoritative Sources and Precedence

Use these sources in order:

1. `harness/github-copilot/` for reusable primitive content.
2. `docs/CLAUDE-CODE-HARNESS-SPEC.md` for Claude Code discovery, schema, conversion, and validation contracts.
3. `docs/CLAUDE-CODE-VALIDATION.md` for dated first-party and runtime evidence.
4. `harness/claude-code/scripts/convert_from_copilot.py` for deterministic type and field conversion.
5. `harness/claude-code/manifests/installed-primitives.json` for repository-installed Claude copies.

When dated evidence contradicts the specification or converter, update the specification first, then the converter and generated outputs.

## Source Ownership and Generated Surfaces

- Treat `harness/claude-code/{agents,rules,skills,commands,hooks,plugins}/` as generated output.
- Edit reusable primitive content under `harness/github-copilot/`, then run the Claude converter.
- Treat `.claude-plugin/marketplace.json`, `harness/claude-code/settings.json`, and `docs/catalog/claude-code.md` as generated files.
- Generate `CLAUDE.md`, `.claude/settings.json`, and other `.claude/` copies from the installed-copy manifest; do not maintain them independently.
- Keep `harness/claude-code/scripts/`, `harness/claude-code/manifests/`, and Claude-specific documentation as maintained source.
- Exclude local metadata, Python caches, and build output such as `.DS_Store`, `__pycache__/`, `obj/`, and `bin/` from generated primitives.

## Type Routing

| Copilot source | Claude Code output |
| --- | --- |
| `agents/*.agent.md` | `agents/*.md` subagents |
| `instructions/*.instructions.md` | `rules/*.md` path-scoped rules |
| `skills/*/SKILL.md` | `skills/*/SKILL.md` skills |
| `prompts/*.prompt.md` | `commands/*.md` legacy-compatible slash commands |
| `plugins/*/plugin.json` | `plugins/*/.claude-plugin/plugin.json` packages |
| `hooks/*/hooks.json` | `hooks/*/hooks.json` Claude hook packages |

Preserve source meaning while translating only fields, tools, paths, and hook events with documented Claude Code equivalents. Report dropped surface-specific capabilities instead of inventing success-shaped replacements.

Workspace-kit skills that intentionally publish Copilot customizations use a generated `copilot-components/` payload. Keep that compatibility payload isolated from Claude Code discovery and rewrite only the publisher's source root during conversion.

## Project Hook Activation

Mirror the repository's existing Copilot hook activation policy:

- Aggregate Copilot hooks without `disableAllHooks: true` into `harness/claude-code/settings.json`.
- Install the matching generated hook packages under `.claude/hooks/`.
- Keep intrusive hooks that are disabled on the Copilot side disabled on the Claude side.
- Validate the generated project settings and installed hook paths together.

## Freshness and Validation

Verify volatile Claude Code behavior against known first-party `code.claude.com` pages when the installed version differs from recorded evidence, the documentation changes, or a claim is marked unverified. Record the URL, version, date, result, and divergence in `docs/CLAUDE-CODE-VALIDATION.md`.

Run these checks after any canonical primitive or Claude harness change:

```sh
python3 harness/claude-code/scripts/convert_from_copilot.py --check
python3 harness/claude-code/scripts/validate_primitives.py --strict
python3 harness/claude-code/scripts/generate_catalog.py --check
python3 harness/github-copilot/scripts/sync_installed_primitives.py \
  --manifest harness/claude-code/manifests/installed-primitives.json --check
```

Use `claude plugin validate --strict` for runtime validation when Claude Code is installed. Keep CI aligned with the deterministic Python checks.

## Conventions

| Rule | Rationale |
| --- | --- |
| Convert from canonical Copilot sources instead of editing generated Claude primitives. | A single content source prevents silent cross-harness drift. |
| Keep Claude-specific contracts and evidence in their dedicated documents. | Surface-specific behavior stays explicit and refreshable. |
| Reject generated build output and local metadata. | Machine-specific files are not portable primitive content. |
| Synchronize declared `CLAUDE.md`, settings, hooks, and other `.claude/` copies from the manifest. | Repository discovery paths and guardrails remain reproducible. |
| Run conversion, validation, catalog, and mirror checks together. | Structural validity alone does not prove freshness or installation completeness. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Update canonical Copilot content, then regenerate Claude outputs. | Hand-edit files under generated Claude primitive roots. |
| Record current Claude Code evidence with a date and version. | Present undated assumptions as supported runtime behavior. |
| Preserve unsupported-tool and unsupported-hook reports. | Silently drop capabilities without surfacing the loss. |
| Validate the marketplace and representative plugins with Claude Code when available. | Treat the local Python validator as proof of runtime loading. |
| Keep generated copies free of `obj/`, `bin/`, caches, and OS metadata. | Package build artifacts or `.DS_Store` files as skill resources. |

## Checklist Before Opening a PR

- [ ] Canonical content changes were made under `harness/github-copilot/`, not generated Claude primitive roots.
- [ ] Claude-specific runtime claims match dated evidence in `docs/CLAUDE-CODE-VALIDATION.md`.
- [ ] Conversion, strict validation, catalog drift, and installed-copy drift checks pass.
- [ ] `.claude-plugin/marketplace.json`, `docs/catalog/claude-code.md`, `CLAUDE.md`, `.claude/settings.json`, installed hook scripts, and other declared `.claude/` copies are synchronized.
- [ ] Generated primitives contain no local metadata, caches, build output, unresolved placeholders, or unsupported fields.
- [ ] Runtime plugin validation was run when Claude Code was available, or the unrun check is reported.

## References

- [Claude Code customization overview](https://code.claude.com/docs/en/features-overview)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)

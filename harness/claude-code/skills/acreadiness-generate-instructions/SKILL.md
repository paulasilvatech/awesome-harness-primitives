---
name: acreadiness-generate-instructions
description: >-
  Generate tailored AI agent instruction files with the AgentRC instructions command, including
  .github/copilot-instructions.md, AGENTS.md, scoped .github/instructions/*.instructions.md files
  with applyTo globs, and optional CLAUDE.md output. Use after /acreadiness-assess to close AI
  Tooling gaps or when the user wants to create, regenerate, refresh, preview, or choose output
  options for custom instructions.
argument-hint: >-
  [--output .github/copilot-instructions.md|AGENTS.md] [--strategy flat|nested] [--areas | --area
  <name>] [--apply-to <glob>] [--claude-md] [--dry-run]
---

<!-- Generated from harness/github-copilot/skills/acreadiness-generate-instructions/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AgentRC instruction generation

Generate or refresh repository instruction files through AgentRC's Measure → Generate → Maintain loop, choosing the right output target, strategy, and scoped `applyTo` layout for GitHub Copilot and other agents.

## When to invoke

- "Generate Copilot instructions for this repo."
- "Refresh our AI agent instructions after acreadiness assess."
- "Create AGENTS.md and scoped instructions."
- "Use AgentRC instructions with nested strategy."
- "Add per-area .instructions.md files with applyTo globs."

## Inputs

Use `$ARGUMENTS` as command-line options for AgentRC generation. Validate supported flags before running anything: `--output`, `--strategy`, `--areas`, `--area`, `--areas-only`, `--apply-to`, `--claude-md`, `--dry-run`, and `--force` when overwriting is confirmed. If `$ARGUMENTS` is empty, default to `.github/copilot-instructions.md` and ask which strategy to use unless the user already specified one.

## Output options

| File | Scope | When to use |
| --- | --- | --- |
| `.github/copilot-instructions.md` | Always-on, whole workspace | Default and recommended for GitHub Copilot in VS Code. |
| `AGENTS.md` | Always-on, whole workspace | Multi-agent repositories using GitHub Copilot, Claude, Cursor, or other agents. |
| `.github/instructions/*.instructions.md` | Scoped by `applyTo` glob | Per-topic or per-area rules in monorepos and multi-stack repositories. |
| `CLAUDE.md` | Claude-specific | Add via `--claude-md`; nested strategy only. |

## Strategy choices

| Strategy | Shape | Use when |
| --- | --- | --- |
| `flat` | One `.github/copilot-instructions.md` or chosen output file. | Small or medium repos with one stack; simple review in one PR. |
| `nested` | Hub `.github/copilot-instructions.md` plus per-topic `.github/instructions/<topic>.instructions.md` files. | Large repos, multi-stack repos, monorepos, or repos with more than 5 top-level directories. |

For GitHub Copilot, native scoped files live in `.github/instructions/` with `applyTo` frontmatter. AgentRC's default nested layout writes `.agents/` for agent-agnostic repositories; rewrite to `.github/instructions/` when the main output is `.github/copilot-instructions.md`. If `--output AGENTS.md` is chosen, keep AgentRC's native `.agents/` layout.

## Area-scoped instructions

When `agentrc.config.json` declares areas, default to offering per-area `.instructions.md` files. Each area file must be lowercase kebab-case and start with `applyTo` frontmatter.

```markdown
---
applyTo: "apps/frontend/**"
---

# Frontend area instructions

...AgentRC-generated content for this area...
```

| Kind | Filename example | `applyTo` example | Source |
| --- | --- | --- | --- |
| Topic | `testing.instructions.md` | `**/*.{test,spec}.{ts,tsx,js}` | AgentRC `--strategy nested` topic split. |
| Area | `frontend.instructions.md` | `apps/frontend/**` | `agentrc.config.json` areas plus `--areas`. |

## Procedure

1. Pick the target file. Default to `.github/copilot-instructions.md`; switch to `AGENTS.md` only for multi-agent, Claude, Cursor, or explicit user request.
2. Ask which strategy to use, `flat` or `nested`, unless supplied by user or `$ARGUMENTS`. Recommend `nested` when the repo has more than 5 top-level directories, multiple stacks, or monorepo tooling such as turbo, nx, or pnpm workspaces.
3. Read `agentrc.config.json` to discover areas. If areas exist, ask whether to generate per-area `.instructions.md` files; default to yes. If an area lacks `paths`, ask for a glob such as `src/api/**`. If `--apply-to <glob>` is supplied for a single area, use it verbatim.
4. Run a dry run first:

   ```bash
   npx -y github:microsoft/agentrc instructions --output <file> --strategy <flat|nested> [--areas|--area <name>] [--claude-md] --dry-run
   ```

5. Show a short summary of files to create or overwrite, area count and their `applyTo` globs, and the model used, default `claude-sonnet-4.6`.
6. On confirmation, run the same command without `--dry-run`, adding `--force` only if overwriting existing files was confirmed.
7. Post-process layout for GitHub Copilot output:
   - If `--output` ends in `copilot-instructions.md` and strategy is `nested`, move or rewrite `.agents/<topic>.md` to `.github/instructions/<topic>.instructions.md`, add suitable `applyTo`, and delete now-empty `.agents/`.
   - If `--areas` or `--area <name>` was used, write `.github/instructions/<area>.instructions.md` for each area using `paths` from `agentrc.config.json` unless overridden by `--apply-to`.
   - If `--output AGENTS.md` was chosen, keep `.agents/` for nested output.
8. Verify by reading generated files back and summarize detected stack, conventions captured, length, and `.instructions.md` files with their globs.
9. Suggest next steps: rerun the `assess` skill to confirm AI Tooling improved; consolidate if both `copilot-instructions.md` and `AGENTS.md` already exist.

## Topic applyTo defaults

| Topic | Default `applyTo` |
| --- | --- |
| `testing` | `**/*.{test,spec}.{ts,tsx,js,jsx,mjs,cjs}` |
| `style` / `code-quality` / `formatting` | `**/*.{ts,tsx,js,jsx,mjs,cjs,py,go,rs,java,kt,cs}` |
| `build` / `ci` | `**/{package.json,turbo.json,nx.json,.github/workflows/**}` |
| `docs` | `**/*.md` |
| `security` | `**` |
| anything else / hub-level | `**` |

## Gotchas

- **Always dry-run first**: instruction files are repository policy and should be reviewed before overwrite.
- **Do not run non-interactively in CI**: generated instructions should land through a PR.
- **Copilot scoped files are not `.agents/`**: use `.github/instructions/*.instructions.md` with `applyTo` when targeting `.github/copilot-instructions.md`.
- **AgentRC reads actual code**: do not replace generated content with generic templates.

This is the highest-leverage AgentRC action for AI Tooling. VS Code auto-discovers `.github/instructions/*.instructions.md`; examples include `.github/instructions/frontend.instructions.md`, `.github/instructions/api.instructions.md`, and `.github/instructions/infra.instructions.md`. per-language guidance belongs in scoped files when useful. For monorepos, `agentrc instructions --areas` can generate area-scoped content. In a single-area call, `--apply-to` overrides the area path. Nested Copilot output may require move/rewrite from `.agents/` into `.github/instructions/`. Present the flat versus nested trade-off for small/medium repositories and detect turbo/nx/pnpm workspaces. Area files MUST include `applyTo`.

## Output template

```markdown
## AgentRC instruction generation result

**Status:** generated | previewed | blocked
**Target:** `.github/copilot-instructions.md` | `AGENTS.md`
**Strategy:** `flat` | `nested`

| File | Scope | applyTo | Status |
| --- | --- | --- | --- |
| `<path>` | `<root/topic/area/Claude>` | `<glob or always-on>` | `<created/updated/previewed>` |

**Command**
`npx -y github:microsoft/agentrc instructions --output <file> --strategy <flat|nested> ...`

**Synopsis:** <stack detected, conventions captured, length>
**Next steps:** <assess rerun or consolidation advice>
```

## Quality gate

- [ ] `$ARGUMENTS` was parsed and unsupported options were rejected or ignored safely.
- [ ] The target defaulted to `.github/copilot-instructions.md` unless the user requested `AGENTS.md` or multi-agent output.
- [ ] Strategy was supplied or confirmed before generation.
- [ ] `agentrc.config.json` areas and `paths` were read when area output was requested or available.
- [ ] A dry run was shown before any overwrite or generation.
- [ ] GitHub Copilot nested output was rewritten to `.github/instructions/*.instructions.md` with `applyTo` frontmatter.
- [ ] `AGENTS.md` nested output kept `.agents/` when chosen.
- [ ] Generated files were read back and summarized with lengths and globs.

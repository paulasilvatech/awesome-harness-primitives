# Primitive Templates

Copy-paste starting points for every primitive type in this repository. `docs/COPILOT-HARNESS-SPEC.md`
remains the authority on **frontmatter**; these templates standardize the **body** and the way primitives
reference each other.

| Template | Produces | Discovered by |
| --- | --- | --- |
| [agent.template.md](agent.template.md) | `library/agents/<name>.agent.md` | Copilot CLI + VS Code |
| [instructions.template.md](instructions.template.md) | `library/instructions/<name>.instructions.md` | Copilot CLI + VS Code |
| [skill.template.md](skill.template.md) | `library/skills/<name>/SKILL.md` | Copilot CLI + VS Code |
| [prompt.template.md](prompt.template.md) | `.github/prompts/<name>.prompt.md` | **VS Code only** — not a CLI primitive |

## The six-block contract

Every primitive answers the same six questions. Only the section names change per type.

| Block | Question | Agent | Instructions | Skill | Prompt |
| --- | --- | --- | --- | --- | --- |
| 1. Identity | What is it? | H1 + `## Mission` | H1 + scope paragraph | H1 + summary paragraph | H1 + `## Objective` |
| 2. Activation | When does it engage? | `description` ("Use when …") | `applyTo` globs | `description` (WHAT + WHEN) | `## When to Invoke` |
| 3. Procedure | What does it do? | `## Operating Principles` | `## Conventions` | `## Workflow` | `## Prompt Body` |
| 4. Limits | What must it never do? | `## Out of Scope` + `## Anti-Patterns` | `## Do / Do Not` | `## Rules` | `## What I Will NOT Do` |
| 5. Verification | How do we know it worked? | `## Definition of Done` | `## Checklist Before Opening a PR` | `## Quality Gate` | `## Definition of Done` |
| 6. Integration | What does it connect to? | `## Related Primitives` | `## Related Primitives` | `## Related Primitives` | `## Related Primitives` |

Blocks 1, 2, 4, and 5 are mandatory. Block 3 may be merged into block 1 for very small primitives.
Block 6 is omitted only when the primitive genuinely stands alone.

## Cross-primitive references

Only two couplings in the harness are declarative and machine-verifiable:

- `plugin.json` → `extensions["com.github.copilot"].agents` / `.skills`
- `hooks.json` → event names

Everything else is **semantic**: a skill activates because its `description` matches the context, not because
another file links to it. Therefore:

- **Reference by name and type, never by relative path.** Write ``the `iac-review` skill``, not
  ``[roundup](../../library/skills/roundup/SKILL.md)``. Primitives are installed standalone into `.github/…` or
  `~/.copilot/…`, so `../` targets do not survive installation and nothing resolves them at runtime.
- **The only allowed relative paths are inside a skill's own directory** (`scripts/`, `references/`,
  `assets/`), which the runtime loads on demand.
- **Never reference a `*.prompt.md` file from a CLI primitive.** Prompt files are not discovered by the
  Copilot CLI. Convert the prompt to a user-invocable skill instead.
- **Declare the real bundle in `plugin.json`** when a set of primitives ships together.

## Authoring rules that apply to all types

- Write everything in English. No emojis.
- Replace every `<PLACEHOLDER>` and delete the leading `<!-- AUTHORING … -->` comment block.
- `tools:` is an allow-list, not a grant. Unrecognized tokens are dropped **silently** — `search`, `web`,
  `codebase`, `terminal`, `all`, and `fetch` grant nothing in the CLI. Spell out `grep`, `glob`,
  `web_fetch`, `web_search`. (VS Code prompt files use a different tool vocabulary; see that template.)
- Validate before opening a PR:

  ```sh
  python3 library/scripts/validate_primitives.py
  python3 library/scripts/generate_catalog.py --check
  ```

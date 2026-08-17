# Contributing

`docs/COPILOT-HARNESS-SPEC.md` is the authority for every primitive format. Run the validator before opening a PR:

```sh
python3 library/scripts/validate_primitives.py
python3 library/scripts/validate_primitives.py --strict
python3 library/scripts/validate_primitives.py --kind agents
python3 library/scripts/validate_primitives.py --kind instructions
python3 library/scripts/validate_primitives.py --kind skills
python3 library/scripts/validate_primitives.py --kind plugins
python3 library/scripts/validate_primitives.py --kind hooks
```

Regenerate the catalog after primitive changes:

```sh
python3 library/scripts/generate_catalog.py
python3 library/scripts/generate_catalog.py --check
```

## Body structure shared by all types

Frontmatter rules differ per type, but every primitive answers the same six questions. The templates in [docs/templates/](docs/templates) encode this structure, and the validator reports drift at `INFO` — advisory only, since the CLI never validates a primitive body.

| Block | Question | Agent | Instructions | Skill |
| --- | --- | --- | --- | --- |
| Identity | What is it? | H1 + `## Mission` | H1 + scope paragraph | H1 + summary |
| Activation | When does it engage? | `description` | `applyTo` globs | `description` (WHAT + WHEN) |
| Procedure | What does it do? | `## Operating Principles` | `## Conventions` | `## Workflow` |
| Limits | What must it never do? | `## Out of Scope` | `## Do / Do Not` | `## Rules` |
| Verification | How do we know it worked? | `## Definition of Done` | `## Checklist Before Opening a PR` | `## Quality Gate` |
| Integration | What does it connect to? | `## Related Primitives` | `## Related Primitives` | `## Related Primitives` |

Cross-primitive references use the **name and type**, never a relative path: a primitive is installed standalone into `.github/…` or `~/.copilot/…`, so `../` targets do not survive installation and nothing resolves them at runtime. Only a skill's own bundled resources (`scripts/`, `references/`, `assets/`) may be linked relatively. Never reference a `*.prompt.md` file from a CLI primitive — prompt files are a VS Code feature the Copilot CLI does not discover; convert the prompt to a user-invocable skill instead.

| Rule | Reports |
| --- | --- |
| `AG018`, `IN010`, `SK013` | Relative link that does not survive installation |
| `AG019`, `IN011`, `SK014` | Reference to a `*.prompt.md` file |
| `AG020`, `IN012`, `SK015` | Body does not open with a single H1 |

## Agents

- Start from [the agent template](docs/templates/agent.template.md), then add source files under `library/agents/*.agent.md`; install copies in `.github/agents/` or `~/.copilot/agents/`.
- Filename must match `^[A-Za-z0-9._-]+\.agent\.md$`.
- Frontmatter requires non-empty `description`; optional keys include `name`, `tools`, `model`, `target`, `user-invocable`, `disable-model-invocation`, and `mcp-servers`.
- Body must be non-empty and at most 30,000 characters.
- PR-gating rule IDs: `AG001`, `AG002`, `AG003`, `AG005`, `AG006`, `AG007`, `AG008`, `AG012`, `AG014`.

## Instructions

- Start from [the instructions template](docs/templates/instructions.template.md), then add source files under `library/instructions/*.instructions.md`; install copies in `.github/instructions/` or `~/.copilot/instructions/`.
- Filename must match `^[A-Za-z0-9._-]+\.instructions\.md$`.
- Frontmatter is optional, but reusable modules should include `applyTo`; recognized keys are `applyTo`, `description`, `name`, and `excludeAgent`.
- Body must be non-empty.
- PR-gating rule IDs: `IN001`, `IN002`, `IN005`, `IN006`, `IN009`.

## Skills

- Start from [the skill template](docs/templates/skill.template.md), then add each skill under `library/skills/<name>/SKILL.md`; install copies in `.github/skills/<name>/` or `~/.copilot/skills/<name>/`.
- Directory and frontmatter `name` must match; names must be 1–64 characters, kebab-case, and not contain `--`.
- Frontmatter requires `name` and `description`; descriptions must be 1–1024 characters and state what the skill does and when to use it.
- Body must be non-empty; move large resources into bundled files referenced from the skill.
- PR-gating rule IDs: `SK001`, `SK002`, `SK003`, `SK004`, `SK007`, `SK009`, `SK010`, `SK011`.

## Plugins

- Add each plugin under `library/plugins/<name>/plugin.json` unless the spec-supported manifest location is needed.
- `name` is required, max 64 characters, and must be kebab-case/dot-case; `version` should be semver; `description` should be present and at most 1024 characters.
- Keep component paths valid relative to the manifest directory or repo root.
- PR-gating rule IDs: `PL001`, `PL002`, `PL003`, `PL008`.

## Hooks

- Add each hook package under `library/hooks/<name>/hooks.json`; install copies as `.github/hooks/*.json` or `~/.copilot/hooks/*.json`.
- JSON must use `version: 1` and a `hooks` object.
- Prefer native camelCase events such as `sessionStart`, `preToolUse`, `postToolUse`, and `postResult`.
- Each hook entry must define `bash`, `powershell`, `command`, or HTTP `url`; referenced scripts must exist and be executable.
- PR-gating rule IDs: `HK001`, `HK002`, `HK003`, `HK004`, `HK006`, `HK008`, `HK009`.

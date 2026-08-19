# Contributing

Repository governance defines source precedence and freshness. `docs/COPILOT-HARNESS-SPEC.md` is the
authority for runtime format, while `docs/HARNESS-VALIDATION.md` records tested versions, dates,
divergences, and unverified behavior. Run the validator before opening a PR:

```sh
python3 library/scripts/validate_primitives.py
python3 library/scripts/validate_primitives.py --strict
python3 library/scripts/validate_primitives.py --kind agents
python3 library/scripts/validate_primitives.py --kind instructions
python3 library/scripts/validate_primitives.py --kind skills
python3 library/scripts/validate_primitives.py --kind prompts
python3 library/scripts/validate_primitives.py --kind plugins
python3 library/scripts/validate_primitives.py --kind hooks
```

Regenerate the catalog after primitive changes:

```sh
python3 library/scripts/generate_catalog.py
python3 library/scripts/generate_catalog.py --check
python3 library/scripts/sync_plugin_components.py --check
python3 library/scripts/sync_installed_primitives.py --check
```

## Body structure shared by all types

Frontmatter rules differ per type, but every primitive answers the same six questions. The templates in [docs/templates/](docs/templates) encode this structure, and the validator reports drift at `INFO` — advisory only, since the CLI never validates a primitive body.

| Block | Question | Agent | Instructions | Skill | Prompt |
| --- | --- | --- | --- | --- | --- |
| Identity | What is it? | H1 + `## Mission` | H1 + authority paragraph | H1 + summary | H1 + `## Objective` |
| Activation | When does it engage? | `description` + `## Activation and Scope` | `applyTo` + `description` | `description` + `## When to invoke` | `## When to Invoke` |
| Knowledge or procedure | What does it know or do? | Principles, knowledge boundary, optional procedure | Freely titled domain sections | Domain sections plus optional procedure or criteria | `## Prompt Body` |
| Limits | What must it never do? | Write policy + anti-patterns | `## Do / Do Not` | Optional `## Limits` and gotchas | `## What I Will NOT Do` |
| Output | What does it return? | `## Output Format` | Constrains matching work | `## Output template` | `## Output Format` |
| Verification | How do we know it worked? | `## Definition of Done` | `## Checklist Before Opening a PR` | `## Quality gate` | `## Definition of Done` |

Cross-primitive references use the **name and type**, never a relative path: a primitive is installed standalone into `.github/…` or `~/.copilot/…`, so `../` targets do not survive installation and nothing resolves them at runtime. Only a skill's own bundled resources (`scripts/`, `references/`, `assets/`) may be linked relatively. Never reference a `*.prompt.md` file from a CLI primitive — prompt files are a VS Code feature the Copilot CLI does not discover; convert the prompt to a user-invocable skill instead.

## Current-platform claims

Use local manifests, the harness spec, and dated evidence before external research. Verify a known
first-party source when the user requests current or latest behavior, a relevant target version changed,
local sources conflict, a claim is unverified, or affected evidence is older than 90 days. Record the URL,
product or version, verification date, result, and divergence in `docs/HARNESS-VALIDATION.md`; then update
the spec and dependent guidance. Never refresh a date without repeating the check.

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
- PR-gating rule IDs: `AG001`, `AG002`, `AG003`, `AG005`, `AG006`, `AG007`, `AG008`, `AG012`, `AG014`, `AG017`, `AG021`.

## Instructions

- Start from [the instructions template](docs/templates/instructions.template.md), then add source files under `library/instructions/*.instructions.md`; install copies in `.github/instructions/` or `~/.copilot/instructions/`.
- Filename must match `^[A-Za-z0-9._-]+\.instructions\.md$`.
- Frontmatter is optional, but reusable modules should include `applyTo`; recognized keys are `applyTo`, `description`, `name`, and `excludeAgent`.
- Body must be non-empty.
- PR-gating rule IDs: `IN001`, `IN002`, `IN005`, `IN006`, `IN009`, `IN013`.

## Skills

- Start from [the skill template](docs/templates/skill.template.md), then add each skill under `library/skills/<name>/SKILL.md`; install copies in `.github/skills/<name>/` or `~/.copilot/skills/<name>/`.
- Directory and frontmatter `name` must match; names must be 1–64 characters, kebab-case, and not contain `--`.
- Frontmatter requires `name` and `description`; descriptions must be 1–1024 characters and state what the skill does and when to use it.
- Body must be non-empty; move large resources into bundled files referenced from the skill.
- PR-gating rule IDs: `SK001`, `SK002`, `SK003`, `SK004`, `SK007`, `SK009`, `SK010`, `SK011`, `SK016`.

## Prompts

- Start from [the prompt template](docs/templates/prompt.template.md), then add source files under `library/prompts/*.prompt.md`.
- Prompt files are local VS Code actions and are not discovered by Agent Host or Copilot CLI.
- This repository requires kebab-case filename and matching `name`, a non-empty `description`, valid prompt metadata, and the ten mandatory sections in template order.
- Static validation checks local metadata and structure; use **Chat: Run Prompt** to verify runtime inputs, tools, destination behavior, and side effects.
- Declare `.github/prompts/` publication in `library/installed-primitives.json` only when workspace discovery is required.
- PR-gating rule IDs: `PR001` through `PR008`.

## Plugins

- Add each plugin under `library/plugins/<name>/plugin.json` unless the spec-supported manifest location is needed.
- `name` is required, max 64 characters, and must be kebab-case/dot-case; `version` should be semver; `description` should be present and at most 1024 characters.
- Keep component paths valid relative to the manifest directory or repo root.
- **The shared library is the source of truth.** Files under a plugin that also exist in
  `library/{agents,instructions,skills}` are *generated copies* — plugins must be self-contained
  because upward-relative references (`../../agents/...`) do not resolve at install time. Edit the
  library original, then run `python3 library/scripts/sync_plugin_components.py` to regenerate. Never
  hand-edit a plugin copy: `--check` runs in CI and fails the build on drift.
- PR-gating rule IDs: `PL001`, `PL002`, `PL003`, `PL008`.

## Hooks

- Add each hook package under `library/hooks/<name>/hooks.json`; install copies as `.github/hooks/*.json` or `~/.copilot/hooks/*.json`.
- JSON must use `version: 1` and a `hooks` object.
- Prefer native camelCase events such as `sessionStart`, `preToolUse`, `postToolUse`, and `postResult`.
- Each hook entry must define `bash`, `powershell`, `command`, or HTTP `url`; referenced scripts must exist and be executable.
- **Script paths resolve from the workspace root**, never from the config file's directory — for
  user-level hooks too. Keep library packages self-consistent under `hooks/<name>/…` and use absolute
  paths for anything installed globally.
- Set `timeoutSec` to fit the worst case: a hook that scans the working tree is killed silently when it
  overruns, producing no output and no error.
- `disableAllHooks: true` inside a hook file is **file-scoped** — use it to ship a hook off by default;
  sibling hooks keep running. The same key in `config.json`/`settings.json` is the global kill switch.
- Repository hooks are skipped without warning until the workspace is in `trustedFolders`; see the
  [README](README.md#hooks) before concluding a hook is broken.
- Both `library/hooks/*/hooks.json` and this repo's installed `.github/hooks/*.json` are validated.
- PR-gating rule IDs: `HK001`, `HK002`, `HK003`, `HK004`, `HK006`, `HK008`, `HK009`.

## Generated and installed copies

- `library/installed-primitives.json` declares canonical sources that this repository installs under
  `.github/` or publishes as compatibility guidance.
- Run `python3 library/scripts/sync_installed_primitives.py` after changing a declared source.
- Never resolve drift by editing both source and target; regenerate, then run `--check`.
- Plugin-local agents and skills remain owned by `sync_plugin_components.py`.

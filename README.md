# Copilot Primitives

[![Validate primitives](https://github.com/paulasilvatech/copilot-primitives/actions/workflows/validate-primitives.yml/badge.svg)](https://github.com/paulasilvatech/copilot-primitives/actions/workflows/validate-primitives.yml)

A curated, spec-validated collection of GitHub Copilot CLI primitives for the Copilot CLI harness. The repository currently contains **224 agents**, **192 instruction files**, **407 skills**, **93 plugin manifests**, and **8 hook packages**, validated against Copilot CLI **1.0.81-0**.

For a generated, alphabetized inventory, see [docs/CATALOG.md](docs/CATALOG.md). `docs/COPILOT-HARNESS-SPEC.md` is the canonical format and discovery reference, and [docs/templates/](docs/templates) holds the authoring templates for each primitive type.

## Repository layout

```text
.
├── library/
│   ├── agents/                  # Source *.agent.md files
│   ├── instructions/            # Source *.instructions.md files
│   ├── skills/<name>/SKILL.md   # Source skill directories
│   ├── plugins/<name>/plugin.json
│   ├── hooks/<name>/hooks.json
│   └── scripts/
│       ├── check_links.py
│       ├── generate_catalog.py
│       └── validate_primitives.py
└── docs/
    ├── CATALOG.md
    ├── COPILOT-HARNESS-SPEC.md
    └── templates/               # Authoring templates per primitive type
```

## Primitive types

| Type | Source in this repo | CLI discovery path | Format |
| --- | --- | --- | --- |
| Agents | `library/agents/*.agent.md` | `.github/agents/*.agent.md`, `~/.copilot/agents/*.agent.md`, organization `.github`/`.github-private` `agents/*.agent.md`, or `<plugin-root>/agents/*.agent.md` | Markdown with YAML frontmatter |
| Instructions | `library/instructions/*.instructions.md` | `.github/instructions/**/*.instructions.md`, `~/.copilot/instructions/**/*.instructions.md`, `.github/copilot-instructions.md`, `~/.copilot/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Markdown with optional YAML frontmatter |
| Skills | `library/skills/<name>/SKILL.md` | `.github/skills/<name>/SKILL.md`, `~/.copilot/skills/<name>/SKILL.md`, `.claude/skills/`, `.agents/skills/`, or `<plugin-root>/skills/<name>/SKILL.md` | `SKILL.md` with YAML frontmatter |
| Plugins | `library/plugins/<name>/plugin.json` | Manifest discovery: `.plugin/plugin.json`, `plugin.json`, `.github/plugin/plugin.json`, or `.claude-plugin/plugin.json`; marketplace discovery: `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, or `.claude-plugin/marketplace.json` | JSON manifest |
| Hooks | `library/hooks/<name>/hooks.json` | `.github/hooks/*.json`, `~/.copilot/hooks/*.json`, policy directories, settings `hooks`, or `<plugin-root>/hooks.json` / `<plugin-root>/hooks/hooks.json` | JSON (`version: 1`) |
| Prompts *(VS Code only)* | `library/prompts/*.prompt.md` | **Not a CLI primitive** — `.github/prompts/` is read by VS Code chat only | Markdown with YAML frontmatter |

Every type above is loaded by the Copilot CLI harness except **prompts**: agents running on the Agent
Host do not use prompt files. They are kept here for VS Code users — see
[library/prompts/README.md](library/prompts/README.md) for how to convert one into a skill, which works
in both surfaces.

## Install and usage

### Plugins

This repository publishes **70 installable plugin entries** through `.github/plugin/marketplace.json`.

```sh
copilot plugin marketplace add paulasilvatech/copilot-primitives
```

Then use the in-session plugin commands:

```text
/plugin install <name>
/plugin
```

### Agents

```sh
mkdir -p .github/agents
cp library/agents/accessibility.agent.md .github/agents/
mkdir -p ~/.copilot/agents
cp library/agents/accessibility.agent.md ~/.copilot/agents/
```

```text
/agent accessibility
```

### Instructions

```sh
mkdir -p .github/instructions
cp library/instructions/markdown.instructions.md .github/instructions/
mkdir -p ~/.copilot/instructions
cp library/instructions/markdown.instructions.md ~/.copilot/instructions/
```

Files with `applyTo` globs are auto-applied to matching paths and can be managed with `/instructions`.

### Skills

```sh
mkdir -p .github/skills
cp -R library/skills/roundup .github/skills/
mkdir -p ~/.copilot/skills
cp -R library/skills/roundup ~/.copilot/skills/
```

Manage loaded skills with `/skills`.

### Hooks

```sh
# Repository scope — applies to everyone working in this repo.
# Copy the whole package: the config references its scripts by workspace-relative path.
mkdir -p .github/hooks hooks
cp -R library/hooks/secrets-scanner hooks/
cp library/hooks/secrets-scanner/hooks.json .github/hooks/secrets-scanner.json

# User scope — applies to every repo you open.
# Rewrite the script path to an absolute one first; see the note on path resolution below.
mkdir -p ~/.copilot/hooks
cp library/hooks/secrets-scanner/hooks.json ~/.copilot/hooks/secrets-scanner.json
```

Copilot CLI merges all hook sources and runs every hook registered for an event.

> **`bash`/`command` paths always resolve from the workspace root** — for repository *and* user-level
> hooks alike. The shipped configs use `hooks/<name>/<script>`, so a repo-scope install needs the
> package copied to `hooks/<name>/` as shown. A user-scope hook using that relative path would only
> work in repos that happen to contain it, so **replace it with an absolute path** (for example
> `~/.copilot/hooks/secrets-scanner/scan-secrets.sh`) when installing globally. Verified on CLI 1.0.81-0.

> **Repository hooks only run in a trusted folder.** `.github/hooks/*.json` is skipped silently — with
> no warning — until the workspace is listed in `trustedFolders` in `~/.copilot/config.json`. Accepting
> the trust prompt in an interactive session writes that entry for you, so this is invisible day to day.
> In CI, containers, or `-p` automation with a fresh `COPILOT_HOME`, seed it yourself:
>
> ```sh
> printf '{"trustedFolders":["%s"]}\n' "$PWD" > "$COPILOT_HOME/config.json"
> ```
>
> User-level hooks (`~/.copilot/hooks/`) are unaffected by trust. See
> [docs/HARNESS-VALIDATION.md](docs/HARNESS-VALIDATION.md).

Four packages ship enabled; the four intrusive ones (`attester-import-check`, `fix-broken-links`,
`session-auto-commit`, `tool-guardian`) ship with `"disableAllHooks": true` in this repo's own
`.github/hooks/`. That key is **file-scoped** — it disables only its own file, leaving sibling hooks
running — so removing it is how you switch one on.

## Validation

Run the repository validator:

```sh
python3 library/scripts/validate_primitives.py
```

Useful options:

- `--strict` — fail on warnings as well as errors.
- `--json` — emit a machine-readable JSON report.
- `--kind <agents|instructions|skills|plugins|hooks>` — validate only one primitive kind; repeat for multiple kinds.
- `--root <path>` and `--quiet` — validate another root or print only errors plus the summary.

The `hooks` kind covers both the distributable packages under `library/hooks/*/hooks.json` and this
repository's own installed configs in `.github/hooks/*.json` — the ones the CLI actually executes.
Script paths are resolved against the root each set is deployed from, so a broken `bash` path in an
installed config fails CI (`HK008`).

Severity model: **ERROR** fails validation and CI; **WARNING** is valid/loadable but risky or incomplete; **INFO** is compatibility detail. CI runs the default validator as the gate, posts `--strict` output as a non-gating PR summary, and fails if `docs/CATALOG.md` drifts from the generated catalog.

Regenerate or check the catalog with:

```sh
python3 library/scripts/generate_catalog.py
python3 library/scripts/generate_catalog.py --check
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For new primitives, start from the [authoring templates](docs/templates/README.md). The canonical authority for primitive formats remains [docs/COPILOT-HARNESS-SPEC.md](docs/COPILOT-HARNESS-SPEC.md).

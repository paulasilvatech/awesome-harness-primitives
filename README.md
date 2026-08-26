# Copilot Primitives

[![Validate primitives](https://github.com/paulasilvatech/copilot-primitives/actions/workflows/validate-primitives.yml/badge.svg)](https://github.com/paulasilvatech/copilot-primitives/actions/workflows/validate-primitives.yml)

A curated, spec-validated collection of GitHub Copilot CLI primitives for the Copilot CLI harness. The shared harness currently contains **228 agents**, **195 instruction files**, **481 skills**, **48 VS Code prompts**, **136 plugin manifests**, and **8 reusable hook packages**, validated against GitHub Copilot CLI **1.0.81-4**. Self-contained plugins add plugin-owned primitives; the generated content audit reports both scopes without double-counting generated copies.

For a generated, alphabetized inventory, see [docs/CATALOG.md](docs/CATALOG.md). The [primitive content audit](docs/PRIMITIVE-CONTENT-AUDIT.md) separates structural coverage from semantic freshness review, the [capability audit](docs/PRIMITIVE-CAPABILITIES.md) tracks agent and prompt tool policy, and the [redundancy audit](docs/PRIMITIVE-REDUNDANCY.md) blocks unclassified overlap. `docs/COPILOT-HARNESS-SPEC.md` is the canonical format and discovery reference, and [docs/templates/](docs/templates) holds the authoring templates for each primitive type.

## Repository layout

```text
.
├── harness/github-copilot/
│   ├── agents/                  # Source *.agent.md files
│   ├── instructions/            # Source *.instructions.md files
│   ├── skills/<name>/SKILL.md   # Source skill directories
│   ├── prompts/                 # Source VS Code *.prompt.md files
│   ├── plugins/<name>/plugin.json
│   ├── hooks/<name>/hooks.json
│   ├── manifests/
│   │   ├── installed-primitives.json # Canonical-to-installed copy manifest
│   │   └── plugin-sources.json       # Canonical source ownership for flat plugins
│   └── scripts/
│       ├── audit_primitive_capabilities.py
│       ├── audit_primitive_content.py
│       ├── audit_primitive_redundancy.py
│       ├── audit_plugins.py
│       ├── check_links.py
│       ├── generate_catalog.py
│       ├── normalize_plugin_manifests.py
│       ├── sync_installed_primitives.py
│       ├── sync_plugin_components.py
│       └── validate_primitives.py
└── docs/
    ├── CATALOG.md
    ├── COPILOT-HARNESS-SPEC.md
    ├── PRIMITIVE-CAPABILITIES.md
    ├── PRIMITIVE-CONTENT-AUDIT.md
    ├── PRIMITIVE-REDUNDANCY.md
    └── templates/               # Authoring templates per primitive type
```

## Primitive types

| Type | Source in this repo | CLI discovery path | Format |
| --- | --- | --- | --- |
| Agents | `harness/github-copilot/agents/*.agent.md` | `.github/agents/*.agent.md`, `~/.copilot/agents/*.agent.md`, organization `.github`/`.github-private` `agents/*.agent.md`, or `<plugin-root>/agents/*.agent.md` | Markdown with YAML frontmatter |
| Instructions | `harness/github-copilot/instructions/*.instructions.md` | `.github/instructions/**/*.instructions.md`, `~/.copilot/instructions/**/*.instructions.md`, `.github/copilot-instructions.md`, `~/.copilot/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Markdown with optional YAML frontmatter |
| Skills | `harness/github-copilot/skills/<name>/SKILL.md` | `.github/skills/<name>/SKILL.md`, `~/.copilot/skills/<name>/SKILL.md`, `.claude/skills/`, `.agents/skills/`, or `<plugin-root>/skills/<name>/SKILL.md` | `SKILL.md` with YAML frontmatter |
| Plugins | `harness/github-copilot/plugins/<name>/plugin.json` | Manifest discovery: `.plugin/plugin.json`, `plugin.json`, `.github/plugin/plugin.json`, or `.claude-plugin/plugin.json`; marketplace discovery: `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, or `.claude-plugin/marketplace.json` | JSON manifest |
| Hooks | `harness/github-copilot/hooks/<name>/hooks.json` | `.github/hooks/*.json`, `~/.copilot/hooks/*.json`, policy directories, settings `hooks`, or `<plugin-root>/hooks.json` / `<plugin-root>/hooks/hooks.json` | JSON (`version: 1`) |
| Prompts *(VS Code only)* | `harness/github-copilot/prompts/*.prompt.md` | **Not a CLI primitive** — `.github/prompts/` is read by VS Code chat only | Markdown with YAML frontmatter |

Every type above is loaded by the Copilot CLI harness except **prompts**: agents running on the Agent
Host do not use prompt files. They are kept here for VS Code users — see
[the prompt contract](docs/templates/README.md#prompt) for when to convert one into a skill, which works
across skills-compatible surfaces.

## Repository governance

The canonical repository-wide instructions live at
`harness/github-copilot/instructions/copilot-repository-governance.instructions.md`. The installed
`.github/copilot-instructions.md` file and the other declared repository customizations are generated
from `harness/github-copilot/manifests/installed-primitives.json`:

```sh
python3 harness/github-copilot/scripts/sync_installed_primitives.py
python3 harness/github-copilot/scripts/sync_installed_primitives.py --check
```

Do not hand-edit a declared `.github/` mirror. Runtime and first-party documentation checks are recorded
with dates in `docs/HARNESS-VALIDATION.md`; stable schema and discovery rules belong in
`docs/COPILOT-HARNESS-SPEC.md`.

## Install and usage

### Plugins

This repository publishes **100 installable plugin entries** through `.github/plugin/marketplace.json`. Every package keeps agents, skills, hooks, extensions, and MCP configuration directly under its plugin root. See the generated [plugin marketplace audit](docs/PLUGIN-AUDIT.md) for component counts, ownership mode, and package-level coverage, and the [primitive content audit](docs/PRIMITIVE-CONTENT-AUDIT.md) for the shared components that are not yet referenced by a plugin.

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
cp harness/github-copilot/agents/accessibility.agent.md .github/agents/
mkdir -p ~/.copilot/agents
cp harness/github-copilot/agents/accessibility.agent.md ~/.copilot/agents/
```

```text
/agent accessibility
```

### Instructions

```sh
mkdir -p .github/instructions
cp harness/github-copilot/instructions/markdown.instructions.md .github/instructions/
mkdir -p ~/.copilot/instructions
cp harness/github-copilot/instructions/markdown.instructions.md ~/.copilot/instructions/
```

Files with `applyTo` globs are auto-applied to matching paths and can be managed with `/instructions`.

### Skills

```sh
mkdir -p .github/skills
cp -R harness/github-copilot/skills/roundup .github/skills/
mkdir -p ~/.copilot/skills
cp -R harness/github-copilot/skills/roundup ~/.copilot/skills/
```

Manage loaded skills with `/skills`.

### Hooks

```sh
# Repository scope — applies to everyone working in this repo.
# Copy the whole package: the config references its scripts by workspace-relative path.
mkdir -p .github/hooks hooks
cp -R harness/github-copilot/hooks/secrets-scanner hooks/
cp harness/github-copilot/hooks/secrets-scanner/hooks.json .github/hooks/secrets-scanner.json

# User scope — applies to every repo you open.
# Rewrite the script path to an absolute one first; see the note on path resolution below.
mkdir -p ~/.copilot/hooks
cp harness/github-copilot/hooks/secrets-scanner/hooks.json ~/.copilot/hooks/secrets-scanner.json
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
python3 harness/github-copilot/scripts/validate_primitives.py
```

Useful options:

- `--strict` — fail on warnings as well as errors.
- `--json` — emit a machine-readable JSON report.
- `--kind <agents|instructions|skills|prompts|plugins|hooks>` — validate only one primitive kind; repeat for multiple kinds.
- `--root <path>` and `--quiet` — validate another root or print only errors plus the summary.

The `hooks` kind covers both the distributable packages under `harness/github-copilot/hooks/*/hooks.json` and this
repository's own installed configs in `.github/hooks/*.json` — the ones the CLI actually executes.
Script paths are resolved against the root each set is deployed from, so a broken `bash` path in an
installed config fails CI (`HK008`).

Severity model: **ERROR** is invalid against the harness or a mandatory repository contract;
**WARNING** is loadable but risky or incomplete; **INFO** is compatibility detail. CI runs strict
validation and fails on errors, warnings, catalog drift, plugin-copy drift, or installed-copy drift.

Regenerate or check the catalog with:

```sh
python3 harness/github-copilot/scripts/generate_catalog.py
python3 harness/github-copilot/scripts/generate_catalog.py --check
```

Check generated distribution surfaces with:

```sh
python3 harness/github-copilot/scripts/normalize_plugin_manifests.py --check
python3 harness/github-copilot/scripts/audit_plugins.py --check
python3 harness/github-copilot/scripts/audit_primitive_content.py --check
python3 harness/github-copilot/scripts/audit_primitive_capabilities.py --check
python3 harness/github-copilot/scripts/audit_primitive_redundancy.py --check
python3 harness/github-copilot/scripts/sync_plugin_components.py --check
python3 harness/github-copilot/scripts/sync_installed_primitives.py --check
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For new primitives, start from the [authoring templates](docs/templates/README.md). The canonical authority for primitive formats remains [docs/COPILOT-HARNESS-SPEC.md](docs/COPILOT-HARNESS-SPEC.md).

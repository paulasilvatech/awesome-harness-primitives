# Awesome Harness Primitives

[![Validate primitives](https://github.com/paulasilvatech/awesome-harness-primitives/actions/workflows/validate-primitives.yml/badge.svg)](https://github.com/paulasilvatech/awesome-harness-primitives/actions/workflows/validate-primitives.yml)

A curated, validated library of agents, instructions, skills, prompts, hooks, plugins, and integrations for **GitHub Copilot** and **Claude Code**.

GitHub Copilot sources are canonical. The Claude Code harness is generated from compatible canonical content, with explicit conversion rules, drift checks, and runtime validation.

## Start here

| Goal | Go to |
| --- | --- |
| Browse everything | [Catalog hub](docs/catalog/README.md) |
| Choose a plugin or standalone primitive | [Usage and installation guide](docs/USAGE.md) |
| Understand the repository | [Documentation hub](docs/README.md) |
| Author or contribute | [Contributing guide](.github/CONTRIBUTING.md) |
| Review runtime contracts | [Copilot spec](docs/COPILOT-HARNESS-SPEC.md) · [Claude Code spec](docs/CLAUDE-CODE-HARNESS-SPEC.md) |
| Review provenance and validation | [Plugin audit](docs/PLUGIN-AUDIT.md) · [Validation evidence](docs/HARNESS-VALIDATION.md) |

## Plugin or standalone?

| Choose | When it fits |
| --- | --- |
| **Plugin** | You want a cohesive capability suite, automatic component discovery, or bundled hooks, MCP servers, and client extensions. |
| **Standalone primitive** | You need one focused agent, instruction, skill, prompt, or hook with minimal installation and review surface. |

Every plugin package is listed in both harness catalogs, and every bundled runtime component is also listed separately with its plugin, type, ownership, and source.

[Read the full decision guide →](docs/USAGE.md#plugin-versus-standalone)

## Browse the catalogs

| Harness | Catalog | Source |
| --- | --- | --- |
| GitHub Copilot | [Agents, instructions, skills, prompts, hooks, plugins, and plugin components](docs/catalog/github-copilot.md) | [`harness/github-copilot/`](harness/github-copilot/README.md) |
| Claude Code | [Subagents, rules, skills, commands, hooks, plugins, and plugin components](docs/catalog/claude-code.md) | [`harness/claude-code/`](harness/claude-code/README.md) |

## Quick install

### GitHub Copilot plugin

```sh
copilot plugin marketplace add paulasilvatech/awesome-harness-primitives
```

Then install from a Copilot CLI session:

```text
/plugin install <plugin-name>
```

### Claude Code plugin

From a Claude Code session:

```text
/plugin marketplace add paulasilvatech/awesome-harness-primitives
/plugin install <plugin-name>@copilot-primitives-claude
```

### Standalone primitive

Copy only the primitive you need into the matching project or user discovery path. Examples:

```sh
# GitHub Copilot agent
mkdir -p .github/agents
cp harness/github-copilot/agents/accessibility.agent.md .github/agents/

# GitHub Copilot skill
mkdir -p .github/skills
cp -R harness/github-copilot/skills/roundup .github/skills/

# Claude Code subagent
mkdir -p .claude/agents
cp harness/claude-code/agents/accessibility.md .claude/agents/
```

See [Usage and installation](docs/USAGE.md) for all primitive types, user-level paths, and generated-source rules.

## How the repository is organized

```text
.
├── README.md
├── LICENSE.md
├── CLAUDE.md                 # Generated Claude Code project instructions
├── docs/                     # Documentation, catalogs, audits, plans, references
├── harness/
│   ├── github-copilot/       # Canonical sources and repository tooling
│   └── claude-code/          # Generated Claude Code harness and converter
├── .github/                  # Copilot install surface, CI, contribution policy
├── .claude/                  # Installed Claude Code project customizations
└── .claude-plugin/           # Claude Code marketplace manifest
```

Runtime-required hidden files remain at the repository root. Historical snapshots and generated reports live under [docs/](docs/README.md), not beside the active harnesses.

## Source ownership

```text
harness/github-copilot/
          │
          ├── canonical primitives
          ├── plugin source ownership manifests
          └── validation and generation scripts
          │
          ▼
harness/claude-code/
          ├── converted subagents, rules, skills, commands
          ├── self-contained plugins
          └── generated project settings and hooks
```

Edit canonical content under `harness/github-copilot/`. Do not hand-edit generated Claude primitives, plugin copies, installed `.github/` mirrors, or installed `.claude/` mirrors.

## Credits and upstream references

This collection includes multiple plugins, components, and reference materials derived from or inspired by
[github/awesome-copilot](https://github.com/github/awesome-copilot). Those materials have been adapted,
updated, and improved here for current harness contracts, stricter validation, self-contained packaging,
catalog discoverability, and GitHub Copilot plus Claude Code compatibility.

Upstream attribution remains explicit: the repository URL and source commit for imported plugin material are
recorded in `harness/github-copilot/manifests/plugin-sources.json` and surfaced in the generated catalogs.

## Quality and public-use policy

- [Content audit](docs/PRIMITIVE-CONTENT-AUDIT.md) tracks structure, freshness risk, and plugin composition.
- [Capability audit](docs/PRIMITIVE-CAPABILITIES.md) tracks agent and prompt tool policy.
- [Redundancy audit](docs/PRIMITIVE-REDUNDANCY.md) classifies exact and semantic overlap.
- [Security policy](.github/SECURITY.md) explains private vulnerability reporting.
- [Licensing guide](docs/LICENSING.md) explains package-level licenses and third-party provenance.

## Contributing

Start with the [contributing guide](.github/CONTRIBUTING.md) and [authoring templates](docs/templates/README.md). All Copilot and Claude validation, catalog, synchronization, and bundled-test gates must pass before publishing.

# Usage and installation

## Plugin versus standalone

### Choose a plugin

Install a plugin when you need:

- a coordinated suite of agents and skills;
- hooks, MCP or LSP servers, output styles, or client extensions;
- one versioned package for a team;
- automatic discovery of all packaged capabilities.

Before installing, review the plugin in the [catalog](catalog/github-copilot/plugin-components.md) and its assurance and provenance in the [plugin audit](PLUGIN-AUDIT.md).

### Choose a standalone primitive

Copy a standalone primitive when you need:

- exactly one agent, instruction, skill, prompt, or hook;
- a smaller review and permission surface;
- project-specific customization without the rest of a suite;
- a primitive that is not bundled by a plugin.

Standalone GitHub Copilot sources are canonical. Claude Code standalone content is generated from those sources.

### Decision table

| Requirement | Recommended delivery |
| --- | --- |
| One focused persona | Standalone agent or subagent |
| Passive rules for matching files | Standalone instructions or rule |
| One reusable workflow | Standalone skill |
| Explicit VS Code action | Standalone prompt |
| Agents + skills that share one workflow | Plugin |
| Hooks or MCP servers must install together | Plugin |
| Client extension or canvas is required | Plugin |
| Team wants one version and update path | Plugin |

## GitHub Copilot

### Plugin

```sh
copilot plugin marketplace add paulasilvatech/awesome-harness-primitives
```

```text
/plugin install <plugin-name>
```

### Standalone

| Type | Project path | User path |
| --- | --- | --- |
| Agent | `.github/agents/*.agent.md` | `~/.copilot/agents/*.agent.md` |
| Instructions | `.github/instructions/*.instructions.md` | `~/.copilot/instructions/*.instructions.md` |
| Skill | `.github/skills/<name>/SKILL.md` | `~/.copilot/skills/<name>/SKILL.md` |
| Hook config | `.github/hooks/*.json` | `~/.copilot/hooks/*.json` |
| VS Code prompt | `.github/prompts/*.prompt.md` | VS Code profile prompt path |

Copy an entire skill or hook package when it includes scripts, references, or assets.

## Claude Code

### Plugin

```text
/plugin marketplace add paulasilvatech/awesome-harness-primitives
/plugin install <plugin-name>@copilot-primitives-claude
```

### Standalone

| Type | Project path | User path |
| --- | --- | --- |
| Subagent | `.claude/agents/*.md` | `~/.claude/agents/*.md` |
| Rule | `.claude/rules/*.md` or `CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Skill | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Command | `.claude/commands/*.md` | `~/.claude/commands/*.md` |
| Hooks | `.claude/settings.json` plus scripts | `~/.claude/settings.json` plus scripts |

## Source and update rules

- Never edit a plugin's generated copy of a shared component.
- Change canonical GitHub Copilot content, synchronize plugin copies, then regenerate Claude Code.
- Review `tools`, hooks, MCP servers, and executable scripts before installation.
- Prefer project scope while evaluating a primitive; move to user scope only when it should affect every repository.

---
name: suggest-awesome-github-copilot-agents
description: >-
  Suggest relevant GitHub Copilot custom agent files from the github/awesome-copilot repository by comparing repository context with available agents, detecting already installed or outdated local .github/agents/*.agent.md files, and presenting a no-install table. Use when the user asks to suggest awesome GitHub Copilot custom agents, find agents to add, compare local agents with awesome-copilot, or update outdated custom agents.
---

# Suggest awesome GitHub Copilot agents

Compare the repository's existing custom agents and current project needs with the GitHub awesome-copilot agent catalog, then recommend missing or outdated `.agent.md` files without installing or updating anything until the user explicitly asks.

## When to invoke

- "Suggest awesome GitHub Copilot custom agents for this repo."
- "Which awesome-copilot agents should we add?"
- "Compare our .github/agents with awesome-copilot."
- "Find outdated local custom agents."
- "Update this custom agent from awesome-copilot."

## Prerequisites and context

Use web access to read the awesome-copilot catalog and raw agent files. The catalog is at `https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md`; agent files are under `https://github.com/github/awesome-copilot/tree/main/agents` and raw files follow `https://raw.githubusercontent.com/github/awesome-copilot/main/agents/{filename}`.

Local custom agents live in `.github/agents/` as `*.agent.md` files. Read YAML frontmatter from local files to extract `description` and tool configuration.

## Analysis procedure

1. Fetch the available custom agent list and descriptions from `https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md`.
2. List every local `.github/agents/*.agent.md` file.
3. Read local frontmatter and body to inventory descriptions, tools, and instructions.
4. For each local filename that appears likely to exist upstream, fetch `https://raw.githubusercontent.com/github/awesome-copilot/main/agents/{filename}`.
5. Compare full local and remote content, including frontmatter, tools array, and body.
6. Classify local agents as up-to-date, outdated, or local-only.
7. Analyze repository context: languages (`.cs`, `.js`, `.py`, and others), frameworks such as ASP.NET, React, Azure usage, project type, documentation needs, recent chat context, feature requests, code review patterns, and workflow requirements.
8. Match catalog agents to gaps that would add value and are not already covered.
9. Present a table only; include links to awesome-copilot agent files and similar local agents.
10. Await a user request before installing or updating any agent.

## Relevance criteria

| Signal | Evidence to collect | How it affects suggestions |
| --- | --- | --- |
| Language | File extensions, package manifests, build files | Prefer agents that operate on actual stacks in the repo. |
| Framework | ASP.NET, React, Azure, test frameworks, deployment files | Suggest framework-specific agents only with matching evidence. |
| Project type | Web app, API, library, tool, docs site | Match agents to recurring tasks and operational needs. |
| Documentation | README, specs, ADRs, docs folders | Suggest documentation or architecture agents when docs work exists. |
| Chat history | Recent pain points, feature requests, review themes | Prioritize what the user is actively working on. |
| Existing coverage | `.github/agents/*.agent.md` descriptions | Avoid duplicates unless the local agent is outdated. |

## Version comparison rules

| Comparison result | Condition | Output status |
| --- | --- | --- |
| Up-to-date | Entire local file exactly matches remote | `Already installed and up-to-date` |
| Outdated | Same filename exists remotely but content differs | `Installed but outdated (update available)` |
| Not installed | Remote catalog agent has no matching local file | `Not installed in repo` |
| Local-only | Local file has no matching remote | Mention only when relevant to duplicate avoidance. |

For outdated agents, document specific differences: frontmatter `description`, tools array additions/removals/renames, or body content updates. The historical example `principal-software-engineer.agent.md` can differ because remote uses `'web/fetch'` while local uses `'fetch'`.

## Installation and update rules

Do not install or update during the suggestion pass. When the user later requests specific agents:

1. Download new agents into `.github/agents/`.
2. Replace outdated agents entirely with the latest remote version.
3. Preserve file location in `.github/agents/`.
4. Do not adjust the downloaded content.
5. Track progress while downloading or updating multiple assets.

## Examples

Use links like these in the table when relevant:

| Awesome-Copilot Custom Agent | Description | Already Installed | Similar Local Custom Agent | Suggestion Rationale |
| --- | --- | --- | --- | --- |
| [amplitude-experiment-implementation.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/amplitude-experiment-implementation.agent.md) | This custom agent uses Amplitude's MCP tools to deploy new experiments inside of Amplitude, enabling seamless variant testing capabilities and rollout of product features | No | None | Would enhance experimentation capabilities within the product |
| [launchdarkly-flag-cleanup.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/launchdarkly-flag-cleanup.agent.md) | Feature flag cleanup agent for LaunchDarkly | Yes | `launchdarkly-flag-cleanup.agent.md` | Already covered by existing LaunchDarkly custom agents |
| [principal-software-engineer.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/principal-software-engineer.agent.md) | Provide principal-level software engineering guidance with focus on engineering excellence, technical leadership, and pragmatic implementation. | Outdated | `principal-software-engineer.agent.md` | Tools configuration differs: remote uses `'web/fetch'` vs local `'fetch'` - update recommended |

## Gotchas

- **Do not install during recommendation**: the first output is analysis only; wait for explicit user direction.
- **Do not suggest duplicates**: if a similar local agent already covers the need, report that instead of recommending another copy.
- **Do not compare descriptions only**: tools and body changes can make an agent outdated even when descriptions match.
- **Do not reference prompt files**: this skill is about custom agent `.agent.md` files only.

Legacy VS Code instructions may mention `#fetch`, `#runInTerminal`, `#todos`, `fetch`, `githubRepo`, and `curl`; in this CLI skill, use available web or shell capabilities instead and do not expose unsupported tool names as frontmatter. The control words `AWAIT`, `INSTALL`, `UPDATE`, `UNLESS`, `DIRECTED`, and `Download/Update` mean wait for explicit user direction before changing local agents.

## Output template

```markdown
## Awesome GitHub Copilot agent suggestions

| Awesome-Copilot Custom Agent | Description | Already Installed | Similar Local Custom Agent | Suggestion Rationale |
| --- | --- | --- | --- | --- |
| `[agent-name.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/agent-name.agent.md)` | `<description>` | `No | Yes | Outdated` | `<local filename or None>` | `<why it fits, duplicate rationale, or specific outdated differences>` |
```

## Quality gate

- [ ] The awesome-copilot README agents catalog was fetched from `https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md`.
- [ ] Local `.github/agents/*.agent.md` files were listed and their frontmatter descriptions were read.
- [ ] Remote versions were fetched from `https://raw.githubusercontent.com/github/awesome-copilot/main/agents/{filename}` for comparable local agents.
- [ ] Each local match was classified as up-to-date, outdated, or local-only.
- [ ] Recommendations are grounded in repository languages, frameworks, project type, documentation needs, or chat context.
- [ ] Duplicates are avoided or explicitly marked as already covered.
- [ ] The response contains only the requested table and analysis, with no installation unless the user asked for it.

## References

- [Awesome Copilot agents catalog](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md)
- [Awesome Copilot agents folder](https://github.com/github/awesome-copilot/tree/main/agents)

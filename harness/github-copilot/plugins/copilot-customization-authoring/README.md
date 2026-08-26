# Copilot Customization Authoring Plugin

Author and operate GitHub Copilot customization itself: skills, agents, instructions, prompts, memory, harness engineering, CLI onboarding, Copilot Spaces, usage metrics, and LSP setup.

## Installation

```bash
copilot plugin install copilot-customization-authoring@copilot-primitives
```

## What's Included

### Agents

| Agent | Description |
|-------|-------------|
| `custom-agent-foundry` | Design and create GitHub Copilot custom agents with scoped tools, frontmatter, handoffs, and clear behavior. |
| `prompt-builder` | Expert prompt engineering agent for creating, improving, researching, and validating prompts with Prompt Tester feedback. |
| `prompt-engineer` | Analyze and improve prompts by treating every user input as a prompt to rewrite. |
| `trojan-skill-hunter` | Audits agent, skill, instruction, hook, MCP, and plugin contributions for hidden prompt injection, unicode steganography, tool poisoning, supply-chain drift, and excessive agency before trust. |

### Skills

| Command | Description |
|---------|-------------|
| `/copilot-customization-authoring:agent-skill-stack` | Find, evaluate, and assemble the smallest compatible set of AI Agent Skills for an end-to-end natural-language goal. |
| `/copilot-customization-authoring:ai-ready` | Help users install and use John Papa's ai-ready skill as the up-to-date source for making repositories AI-ready with AGENTS.md, copilot-instructions.md, CI workflows, issue templates, and stack-specific guidance. |
| `/copilot-customization-authoring:boost-prompt` | Refine a rough task request into a high-quality markdown prompt by clarifying scope, deliverables, constraints, context, and success criteria, then copy the final prompt to the clipboard with Joyride. |
| `/copilot-customization-authoring:cli-mastery` | Interactive training for the GitHub Copilot CLI through guided lessons, quizzes, scenario challenges, a final exam, and on-demand reference for slash commands, shortcuts, modes, agents, skills, MCP, and configuration. |
| `/copilot-customization-authoring:copilot-cli-quickstart` | Use this skill when someone wants to learn GitHub Copilot CLI from scratch. Offers interactive step-by-step tutorials with separate Developer and Non-Developer tracks, plus on-demand Q&A. Just say "start tutorial" or ask a question! Note: This skill targets GitHub Copilot CLI specifically and uses CLI-specific tools (ask_user, sql, fetch_copilot_cli_documentation). |
| `/copilot-customization-authoring:copilot-primitive-authoring` | Author current GitHub Copilot agents, instructions, and VS Code prompts in this repository. |
| `/copilot-customization-authoring:copilot-spaces` | Use GitHub Copilot Spaces to provide project-specific context to conversations. |
| `/copilot-customization-authoring:copilot-usage-metrics` | Retrieve and display GitHub Copilot usage metrics for organizations and enterprises using the GitHub CLI, REST API, and bundled scripts. |
| `/copilot-customization-authoring:finalize-agent-prompt` | Polish an AI agent prompt file for end-user use by preserving frontmatter, encoding, markdown structure, and intent while improving clarity, organization, grammar, and instruction quality. |
| `/copilot-customization-authoring:generate-custom-instructions-from-codebase` | Generate GitHub Copilot migration and code-evolution instructions by comparing branches, commits, tags, or releases and extracting transformation rules. |
| `/copilot-customization-authoring:github-copilot-starter` | Bootstrap a complete GitHub Copilot customization for a repository, including .github/copilot-instructions.md, scoped instruction files, reusable skills, custom agents, and optional copilot-setup-steps.yml. |
| `/copilot-customization-authoring:harness-engineering` | Adopt or review repository-level harness engineering for GitHub Copilot and coding agents. |
| `/copilot-customization-authoring:lsp-setup` | Install and configure Language Server Protocol servers for GitHub Copilot CLI code intelligence, including go-to-definition, find-references, hover, and type information. |
| `/copilot-customization-authoring:memory-merger` | Merge mature lessons from a domain memory instruction file into the matching long-lived instruction file while preserving applyTo coverage and removing merged memory sections. |
| `/copilot-customization-authoring:microsoft-skill-creator` | Create hybrid GitHub Copilot skills for Microsoft technologies using Microsoft Learn MCP tools or the mslearn CLI. |
| `/copilot-customization-authoring:mini-context-graph` | A persistent, compounding knowledge base combining Karpathy's LLM Wiki pattern with a structured knowledge graph. Ingest documents once — the LLM writes wiki pages, extracts entities/relations into the graph, and stores raw content for evidence retrieval. Knowledge accumulates and cross-references; it is never re-derived from scratch. |
| `/copilot-customization-authoring:prompt-optimizer` | Turn any rough prompt, half-formed idea, or task description into a finished, ready-to-send prompt optimized for any LLM model inside a chat interface — NOT the API. |
| `/copilot-customization-authoring:remember` | Transform lessons learned into domain-organized memory instructions for global or workspace scope. |
| `/copilot-customization-authoring:skill-creator` | Create, audit, repair, and improve GitHub Copilot Agent Skills for VS Code, GitHub Copilot CLI, and GitHub Copilot cloud agent. |
| `/copilot-customization-authoring:steno-mode` | Compress responses with disciplined expert shorthand while preserving exact technical literals, code, commands, paths, identifiers, versions, flags, and quoted errors. |
| `/copilot-customization-authoring:vardoger-analyze` | Run the local vardoger CLI to analyze GitHub Copilot CLI conversation history and write personalized instructions into ~/.copilot/copilot-instructions.md. |

## Source

Canonical sources live in `harness/github-copilot/skills/` and `harness/github-copilot/agents/`. Copies in this package are generated by `harness/github-copilot/scripts/sync_plugin_components.py`; do not edit them directly.

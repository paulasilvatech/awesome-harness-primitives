# Primitive Authoring Templates

These templates are starting points for six Copilot customization and package formats. They are not an exhaustive
list of every type supported by the harness. Repository governance defines source precedence and freshness;
`docs/COPILOT-HARNESS-SPEC.md` is the authority for CLI-discovered formats, and prompt files are a local
VS Code feature.

| Template | Canonical source in this repository | Purpose | Support |
| --- | --- | --- | --- |
| [agent.template.md](agent.template.md) | `library/agents/<name>.agent.md` | Define a persona, judgment boundary, and operating posture. | Copilot CLI and VS Code |
| [instructions.template.md](instructions.template.md) | `library/instructions/<name>.instructions.md` | Apply passive conventions to matching files. | Copilot CLI and VS Code |
| [skill.template.md](skill.template.md) | `library/skills/<name>/SKILL.md` | Package a reusable procedure, review, or specialized capability. | Copilot CLI and VS Code |
| [prompt.template.md](prompt.template.md) | `library/prompts/<name>.prompt.md` | Run a focused, user-selected action with VS Code runtime inputs. | **VS Code only; not a CLI primitive** |
| [plugin.template.json](plugin.template.json) | `library/plugins/<name>/plugin.json` | Declare a strict Agent Plugins 1.0 package and repository ownership. | GitHub Copilot CLI and compatible Agent Plugins clients |
| [plugin-mcp.template.json](plugin-mcp.template.json) | `library/plugins/<name>/mcp.json` | Configure portable plugin MCP servers. | Agent Plugins 1.0 clients |

## Short authoring workflow

1. Copy the appropriate template to its canonical source location:

   ```sh
   cp docs/templates/agent.template.md library/agents/example-name.agent.md
   cp docs/templates/instructions.template.md library/instructions/example-name.instructions.md
   mkdir -p library/skills/example-name
   cp docs/templates/skill.template.md library/skills/example-name/SKILL.md
   cp docs/templates/prompt.template.md library/prompts/example-name.prompt.md
   mkdir -p library/plugins/example-name
   cp docs/templates/plugin.template.json library/plugins/example-name/plugin.json
   cp docs/templates/plugin-mcp.template.json library/plugins/example-name/mcp.json
   ```

2. Replace every visible `{{UPPER_SNAKE_CASE}}` authoring placeholder. Search the completed file or skill
   directory for `{{` before finishing.
3. Delete authoring notes, setup sections, optional branches, sections, table rows, and examples that do
   not apply. Do not leave mutually exclusive policies in the finished primitive.
4. Select the minimum required tools. Editing, command execution, delegation, and web access are opt-in
   capabilities in these templates.
5. Validate the canonical source, regenerate derived content, and synchronize generated copies when
   applicable. See [Validation and synchronization](#validation-and-synchronization).
6. When a claim depends on current platform behavior, consult `docs/HARNESS-VALIDATION.md`. Verify a
   first-party source only when the user requests current behavior, the target version changed, sources
   conflict, a claim is unverified, or the recorded evidence is older than 90 days.

## Contracts by type

The formats do not share one mandatory body outline. Use the contract that matches the selected type.

### Agent

- **Frontmatter:** `description` is required. `name`, `tools`, `model`, `target`, `user-invocable`,
  `disable-model-invocation`, and `mcp-servers` are optional CLI fields. Keep `name` and `model` omitted
  unless there is a concrete reason to fix them. VS Code-only fields such as `argument-hint` and
  `handoffs` are ignored by CLI.
- **Activation:** make `description` state what the agent does and when it should be selected.
  `Activation and Scope` then defines expected inputs, owned decisions, writable paths, and handoffs.
- **Procedure:** use `Mission`, `Operating Principles`, and an optional workflow section to define the
  persona's judgment and proportionate way of working.
- **Knowledge boundary:** `What This Agent Knows` lists transferable knowledge and local sources of
  truth. `What This Agent Does NOT Know` is the anti-hallucination boundary and lists what the agent
  must discover instead of assume.
- **Limits:** choose exactly one read-only or editing policy. Keep `Anti-Patterns This Agent Rejects`
  specific to the agent's authority.
- **Output:** define a stable response structure in `Output Format`, or replace it with a more suitable
  domain-neutral schema.
- **Quality gate:** use `Definition of Done`; also keep the body non-empty and at most 30,000 characters.

### Instructions

- **Frontmatter:** the spec recognizes only `applyTo`, `description`, `name`, and `excludeAgent`, and all
  are optional. The template includes `applyTo` and `description` because a reusable module should
  explain itself and auto-apply. Without `applyTo`, the file is available only through manual attachment.
- **Activation:** `applyTo` is one quoted, comma-separated glob string. Keep the scope paragraph aligned
  with those globs.
- **Conventions:** instructions are passive rules, not a task workflow. Domain sections carry the bulk of
  the file and are titled after the real subject areas. `Conventions` then holds cross-cutting rules in a
  `Rule | Rationale` table. Put ordered setup, migration, or review procedures in a skill.
- **Limits:** use the responsibility split and `Do / Do Not` table to prevent overlap with other
  primitives.
- **Output:** instructions do not define a standalone result; they constrain work performed on matching
  files.
- **Quality gate:** use `Checklist Before Opening a PR`, keep the body non-empty, and keep the file focused and
  roughly two pages or less.

### Skill

- **Frontmatter:** `name` and `description` are required. The name must be 1–64 characters, kebab-case,
  and exactly match the parent directory. The description must be 1–1024 characters and state both what
  the skill does and when to use it. `user-invocable`, `disable-model-invocation`, `argument-hint`,
  `allowed-tools`, `license`, `metadata`, and `tags` are optional.
- **Activation:** discovery loads only `name` and `description`, so use positive trigger language there.
  `When to invoke` may reinforce those triggers. Put exclusions in `Limits`.
- **Structure:** skills use the loosest structure of the four types. Only `When to invoke`, at least one
  freely titled domain section, `Output template`, and `Quality gate` are mandatory. Every other section
  is conditional and must be earned by real content; a conditional section filled with placeholders is
  worse than an omitted one.
- **Inputs:** include `Inputs` only when `argument-hint` is present, and consume and validate
  `$ARGUMENTS`.
- **Procedure or review criteria:** use `Procedure` when order matters and `Criteria` when judgment
  matters. Keep both only when the task genuinely needs both.
- **Limits:** state non-goals, safety boundaries, and named handoffs. Add gotchas or troubleshooting only
  for real failure modes.
- **Output:** make `Output template` precise enough that repeated invocations produce a consistent result.
- **Quality gate:** verify frontmatter, activation language, output, evidence, tool scope, and bundled
  resources. Keep `SKILL.md` below 500 lines, preferably below 200, and move detail into on-demand
  resources.

### Prompt

- **Surface:** prompts are run through VS Code, for example with **Chat: Run Prompt**. Copilot CLI does
  not discover or execute `*.prompt.md`.
- **Frontmatter:** VS Code owns this schema; no prompt field is a CLI requirement. The template supplies
  `name`, `description`, and `argument-hint` as its baseline. Keep the first two clear and concise, and
  remove `argument-hint` when it adds no useful UI hint. `agent` and `tools` are optional and remain
  commented out until the workflow requires them.
- **Structure:** prompts are the most rigid type. All ten sections are mandatory and appear in the
  template order: `Objective`, `When to Invoke`, `Preconditions`, `Inputs the Team Must Provide`,
  `What I Will Do`, `What I Will NOT Do`, `Output Format`, `Definition of Done`, `Prompt Body`,
  `Invocation Example`. Domain headings belong inside the `Output Format` fenced block, never as extra
  top-level sections.
- **Activation:** `When to Invoke` states the workflow position and preconditions for this explicit,
  user-selected action.
- **Procedure:** `Prompt Body` consumes VS Code runtime context, validates the request, gathers permitted
  evidence, performs the action, verifies it, and delivers conditionally.
- **Limits:** `What I Will NOT Do`, precondition failure behavior, scope boundaries, and destination rules
  prevent unintended edits.
- **Output:** choose exactly one destination mode: Chat response, approved workspace edit, or an exact file
  path.
- **Quality gate:** use `Definition of Done` and test the invocation in VS Code with representative input.

## Tools and editing permissions

- An agent's `tools` field is an allow-list filter. Omitting it gives access to all available tools; the
  agent template deliberately starts with the read-only minimum `read`, `grep`, and `glob`.
- Add `edit` only when the agent may change files. Add `execute`, `agent`, `web_fetch`, or `web_search`
  only when its procedure requires command execution, delegation, or web access.
- Do not use CLI no-op tokens such as `search`, `web`, `todo`, `all`, `terminal`, `run`, `codebase`,
  `changes`, `fetch`, `githubRepo`, `search/codebase`, `sql`, or `skill`. The last two capabilities are
  already available without listing them. Use explicit valid CLI tokens; use `*` or omit `tools` when
  unrestricted access is intentional.
- A skill should omit `allowed-tools` by default. If present, list only tools the procedure needs, and do
  not pre-approve editing for a consultative or review-only skill.
- Instructions have no tool allow-list.
- Prompt `tools` are VS Code tool IDs copied from the target environment's **Configure Tools** picker.
  IDs such as `search/codebase` and `vscode/askQuestions` belong to VS Code prompts and must not be copied
  into CLI agent frontmatter.
- A prompt may edit only when its destination, workflow, and available VS Code tools all permit editing.

### Plugin

- **Manifest:** use the Agent Plugins 1.0 schema and only its closed top-level metadata fields.
- **Ownership:** declare `componentSource: library` for canonical shared primitives or `plugin` for
  self-contained packages. Keep source references and `layoutVersion` in the repository extension
  namespace.
- **Discovery:** skills live under `skills/`; GitHub agents, hooks, and client extensions are generated
  under `com.github.copilot/`.
- **Composition:** package a coherent capability. Reject componentless manifests and unrelated
  “bundle everything” collections.
- **Marketplace:** keep source, version, description, uniqueness, and alphabetical ordering synchronized.
- **Runtime:** reinstall into an isolated `COPILOT_HOME` and prove every claimed surface.

### Plugin MCP

- Use the Agent Plugins MCP schema in root `mcp.json`; do not use legacy `.mcp.json`.
- Choose exactly one transport per server: `stdio`, `streamable-http`, or `sse`.
- Pin executable packages and container images. Keep credentials out of `env`, headers, examples, and
  source control.
- Treat workspace `.github/mcp.json` as a separate client schema; do not copy portable plugin config
  verbatim into the workspace.

## Composition and references

Keep responsibilities separate:

| Type | Owns |
| --- | --- |
| Agent | Persona, judgment, scope, and authority |
| Instructions | Passive conventions for matching files |
| Skill | Reusable procedure, review criteria, or specialized capability |
| Prompt | A focused VS Code action initiated by a user |

Reference another primitive by installed name and type, for example: "Use the `dependency-review` skill
when a manifest changes." Do not use relative links between primitives; installation paths differ and
those links do not resolve at runtime. Relative paths are appropriate only for resources bundled inside
the same skill, such as `references/`, `scripts/`, `assets/`, or `templates/`.

Do not reference a prompt file from an agent, instructions file, or skill intended for CLI. If a workflow
must run in CLI, or on both surfaces, implement it as a skill. Any packaging relationship is configured
separately from these semantic references.

## Freshness and evidence

Keep stable authoring rules in primitives and volatile runtime findings in `docs/HARNESS-VALIDATION.md`.
Do not claim that a field, tool, model, event, or surface is current without a source and verification date.
Prefer known first-party URLs, record the result once, and update the harness spec before copying changed
behavior into templates or primitives. Never refresh a date without repeating the check.

## Authoring placeholders and runtime variables

These forms have different meanings:

| Form | Meaning | Action while authoring |
| --- | --- | --- |
| `{{UPPER_SNAKE_CASE}}` | Placeholder supplied by these templates | Replace every occurrence. |
| `${input:topic}` | VS Code prompt input | Keep it; VS Code resolves it when the prompt runs. |
| `${input:destination:response, edit, or file path}` | VS Code prompt input with hint text | Keep or adapt the input name and hint. |
| `${selection}` | Current VS Code editor selection | Keep it when selected text is a real input. |
| `$ARGUMENTS` | Skill invocation arguments | Keep it only when `argument-hint` is enabled and the skill consumes it. |

## Validation and synchronization

For agents, instructions, skills, prompts, and plugins under `library/`, run:

```sh
python3 library/scripts/validate_primitives.py
```

After changing a primitive included in the generated catalog, regenerate and check it:

```sh
python3 library/scripts/generate_catalog.py
python3 library/scripts/normalize_plugin_manifests.py --check
python3 library/scripts/audit_plugins.py --check
python3 library/scripts/generate_catalog.py --check
```

When a plugin package contains generated copies of a shared agent or skill, synchronize from the
canonical `library/agents/` or `library/skills/` source and check for drift:

```sh
python3 library/scripts/sync_plugin_components.py
python3 library/scripts/sync_plugin_components.py --check
```

Synchronize declared installed repository customizations and compatibility guidance:

```sh
python3 library/scripts/sync_installed_primitives.py
python3 library/scripts/sync_installed_primitives.py --check
```

With their default paths, the validator checks `library/agents/`, `library/instructions/`,
`library/skills/`, `library/prompts/`, `library/plugins/`, and `library/hooks/` plus installed repository
hook configs. The catalog generator excludes VS Code prompts. The installed-copy manifest controls which
canonical sources publish into `.github/` or compatibility locations; undeclared library prompts remain
source-only.

For prompts, keep `library/prompts/<name>.prompt.md` as the source, declare a workspace copy only when
VS Code discovery is required, run installed-copy synchronization, and test the result with **Chat: Run
Prompt**. Static validation checks metadata and structure but does not execute the prompt.

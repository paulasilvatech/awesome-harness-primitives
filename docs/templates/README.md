# Primitive Authoring Templates

These templates are starting points for four Copilot customization formats. They are not an exhaustive
list of every type supported by the harness. `docs/COPILOT-HARNESS-SPEC.md` is the authority for the
three formats discovered by GitHub Copilot CLI; prompt files are a VS Code feature.

| Template | Canonical source in this repository | Purpose | Support |
| --- | --- | --- | --- |
| [agent.template.md](agent.template.md) | `library/agents/<name>.agent.md` | Define a persona, judgment boundary, and operating posture. | Copilot CLI and VS Code |
| [instructions.template.md](instructions.template.md) | `library/instructions/<name>.instructions.md` | Apply passive conventions to matching files. | Copilot CLI and VS Code |
| [skill.template.md](skill.template.md) | `library/skills/<name>/SKILL.md` | Package a reusable procedure, review, or specialized capability. | Copilot CLI and VS Code |
| [prompt.template.md](prompt.template.md) | `library/prompts/<name>.prompt.md` | Run a focused, user-selected action with VS Code runtime inputs. | **VS Code only; not a CLI primitive** |

## Short authoring workflow

1. Copy the appropriate template to its canonical source location:

   ```sh
   cp docs/templates/agent.template.md library/agents/example-name.agent.md
   cp docs/templates/instructions.template.md library/instructions/example-name.instructions.md
   mkdir -p library/skills/example-name
   cp docs/templates/skill.template.md library/skills/example-name/SKILL.md
   cp docs/templates/prompt.template.md library/prompts/example-name.prompt.md
   ```

2. Replace every visible `{{UPPER_SNAKE_CASE}}` authoring placeholder. Search the completed file or skill
   directory for `{{` before finishing.
3. Delete authoring notes, setup sections, optional branches, sections, table rows, and examples that do
   not apply. Do not leave mutually exclusive policies in the finished primitive.
4. Select the minimum required tools. Editing, command execution, delegation, and web access are opt-in
   capabilities in these templates.
5. Validate the canonical source, regenerate derived content, and synchronize generated copies when
   applicable. See [Validation and synchronization](#validation-and-synchronization).

## Contracts by type

The formats do not share one mandatory body outline. Use the contract that matches the selected type.

### Agent

- **Frontmatter:** `description` is required. `name`, `tools`, `model`, `target`, `user-invocable`,
  `disable-model-invocation`, and `mcp-servers` are optional CLI fields. Keep `name` and `model` omitted
  unless there is a concrete reason to fix them. VS Code-only fields such as `argument-hint` and
  `handoffs` are ignored by CLI.
- **Activation:** make `description` state what the agent does and when it should be selected.
  `Activation and Scope` then defines expected inputs, owned decisions, writable paths, and handoffs.
- **Procedure:** use `Mission`, `Operating Principles`, and `Procedure` to define the persona's judgment
  and proportionate way of working.
- **Limits:** choose exactly one read-only or editing policy. Keep `What I Will Not Do` and
  `Anti-Patterns` specific to the agent's authority.
- **Output:** define a stable response structure in `Output Format`, or replace it with a more suitable
  domain-neutral schema.
- **Quality gate:** use `Definition of Done`; also keep the body non-empty and at most 30,000 characters.

### Instructions

- **Frontmatter:** the spec recognizes only `applyTo`, `description`, `name`, and `excludeAgent`, and all
  are optional. The template includes `applyTo` and `description` because a reusable module should
  explain itself and auto-apply. Without `applyTo`, the file is available only through manual attachment.
- **Activation:** `applyTo` is one quoted, comma-separated glob string. Keep the scope paragraph aligned
  with those globs.
- **Conventions:** instructions are passive rules, not a task workflow. Define authoritative sources,
  precedence, direct conventions, rationales, and focused examples. Put ordered setup, migration, or
  review procedures in a skill.
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

For agents, instructions, and skills under `library/`, run:

```sh
python3 library/scripts/validate_primitives.py
```

After changing a primitive included in the generated catalog, regenerate and check it:

```sh
python3 library/scripts/generate_catalog.py
python3 library/scripts/generate_catalog.py --check
```

When a plugin package contains generated copies of a shared agent or skill, synchronize from the
canonical `library/agents/` or `library/skills/` source and check for drift:

```sh
python3 library/scripts/sync_plugin_components.py
python3 library/scripts/sync_plugin_components.py --check
```

With their default paths, the validator checks `library/agents/`, `library/instructions/`,
`library/skills/`, `library/plugins/`, and `library/hooks/` plus installed repository hook configs. The
catalog generator reads those five library trees. Neither script validates `docs/templates/` directly,
and neither includes prompts.

For prompts, keep `library/prompts/<name>.prompt.md` as this repository's source, publish or copy it to
`.github/prompts/<name>.prompt.md` for VS Code discovery when applicable, and test it in VS Code. These
repository scripts do not provide a prompt publishing command.

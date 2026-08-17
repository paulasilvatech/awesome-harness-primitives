---
name: 'prompt-builder'
description: 'Guide creation of a production-ready VS Code prompt file with valid frontmatter, structure, and validation criteria.'
agent: 'agent'
tools: ['codebase', 'editFiles', 'search']
argument-hint: 'name=<kebab-name> purpose=<goal> destination=<response|edit|path>'
---

# /prompt-builder

## Objective

Guide the user through creating a production-ready VS Code `.prompt.md` file with valid frontmatter, the current ten-section prompt structure, precise inputs, least-privilege VS Code tools, clear output format, and validation criteria.

## When to Invoke

Use this prompt when a maintainer wants to design or generate a new VS Code prompt file and needs structured discovery before writing `library/prompts/<name>.prompt.md` or another approved prompt destination.

## Preconditions

- The user wants a VS Code prompt file, not a CLI skill, agent, or instructions file.
- The target filename is or will be kebab-case and ends with `.prompt.md`.
- The repository's current prompt template and reference prompt structure are available.
- Editing is allowed only if the user explicitly selects an edit or exact file destination.

## Inputs the Team Must Provide

- Prompt identity: filename, one-sentence description, and category such as code generation, analysis, documentation, testing, refactoring, or architecture.
- Persona definition: `role/expertise`, expertise level, domain knowledge, language and framework knowledge, tools, and qualifications.
- Task specification: primary task, secondary tasks, inputs, constraints, and requirements.
- Context variables: whether to use `${selection}`, `${file}`, `${workspaceFolder}`, `${input:variableName}`, or `${input:variableName:placeholder}`.
- Detailed standards, output requirements, VS Code tool IDs, agent configuration, model requirements, quality criteria, and validation steps.
- Destination: `response`, `edit`, or an exact path.
- Ask the user for anything missing before generating the prompt.

## What I Will Do

- Ask targeted discovery questions before generating the prompt file.
- Produce valid frontmatter with `name`, `description`, optional `agent`, optional `model`, optional `tools`, and optional `argument-hint`.
- Use the current prompt section map: Objective, When to Invoke, Preconditions, Inputs the Team Must Provide, What I Will Do, What I Will NOT Do, Output Format, Definition of Done, Prompt Body, and Invocation Example.
- Keep prompt `tools` as VS Code tool IDs copied from the Configure Tools picker, such as `codebase`, `editFiles`, and `search`, and omit `tools` when inherited tools are sufficient.
- Ensure the prompt body uses numbered steps with `**Step 1 — ...**` through `**Step N — ...**`.
- Validate that no authoring placeholders, obsolete sections, or relative primitive links remain.

## What I Will NOT Do

- Generate an outdated prompt structure with `Mission`, `Primary Directive`, `Scope & Preconditions`, `Inputs`, `Workflow`, `Output Expectations`, or `Quality Assurance` as top-level sections.
- Force a custom `agent` or `model` unless the workflow requires it.
- Invent VS Code tool IDs; exact IDs must come from VS Code's Configure Tools picker or be supplied by the user.
- Add relative links between primitives; refer to related primitives by installed name and type.
- Claim that prompt files are discovered by the GitHub Copilot CLI or validated by CLI primitive validators.
- Modify files unless the selected destination permits it.

## Output Format

Generate the prompt file in this structure. Use the outer fence only for this prompt-builder output description; the generated prompt may include its own fenced blocks.

````markdown
---
name: '[kebab-case prompt name]'
description: '[Single actionable sentence from requirements]'
argument-hint: '[optional runtime argument hint]'
agent: '[ask|edit|agent or custom agent only when required]'
tools: ['[exact VS Code tool IDs only when required]']
model: '[only if a specific model is required]'
---

# /[kebab-case prompt name]

## Objective

[One paragraph describing what the prompt delivers and in what context.]

## When to Invoke

[Short concrete trigger.]

## Preconditions

- [Required workspace state]
- [Required context or artifact]

## Inputs the Team Must Provide

- `target` — [required input]
- Ask the user for anything that is missing.

## What I Will Do

- [Concrete action]

## What I Will NOT Do

- [Domain-specific boundary]

## Output Format

```markdown
## Result
[Concrete result skeleton]

## Evidence
[Evidence skeleton]

## Validation
[Validation skeleton]
```

## Definition of Done

- [ ] [Verifiable success criterion]

## Prompt Body

**Step 1 — Validate inputs.** [Instruction]

**Step 2 — Gather evidence.** [Instruction]

**Step 3 — Produce the result.** [Instruction]

## Invocation Example

```
/[prompt-name] target=example
```
````

When explaining adjacent primitive types, use the current section names:

```markdown
Instructions use an authority paragraph instead of `## Scope and Stack Context` and close with `## Checklist Before Opening a PR`.
Agents use `## What This Agent Knows`, `## What This Agent Does NOT Know`, and `## Anti-Patterns This Agent Rejects`.
Prompts use `## Inputs the Team Must Provide` and the ten mandatory sections shown above.
```

## Definition of Done

- [ ] [Verifiable success criterion]

## Prompt Body

**Step 1 — Validate inputs.** [Instruction]

**Step 2 — Gather evidence.** [Instruction]

**Step 3 — Produce the result.** [Instruction]

## Invocation Example

```
/[prompt-name] target=example
```
```

When explaining adjacent primitive types, use the current section names:

```markdown
Instructions use an authority paragraph instead of `## Scope and Stack Context` and close with `## Checklist Before Opening a PR`.
Agents use `## What This Agent Knows`, `## What This Agent Does NOT Know`, and `## Anti-Patterns This Agent Rejects`.
Prompts use `## Inputs the Team Must Provide` and the ten mandatory sections shown above.
```

## Definition of Done

- [ ] Discovery questions captured identity, purpose, persona, task, context variables, standards, outputs, tools, configuration, validation, and destination.
- [ ] The generated prompt has exactly one H1 immediately after frontmatter.
- [ ] Frontmatter uses valid keys only: `name`, `description`, `agent`, `model`, `tools`, and `argument-hint`.
- [ ] `name` is kebab-case and matches the filename.
- [ ] Top-level sections are the ten mandatory prompt sections in order, with optional Related Primitives only when justified.
- [ ] Prompt body uses numbered `**Step N — ...**` steps.
- [ ] VS Code tool IDs are exact and minimal, or `tools` is omitted.
- [ ] No outdated template headings, placeholders, or relative primitive links remain.

## Prompt Body

Follow these steps in order.

**Step 1 — Gather prompt identity and purpose.** Ask for the intended filename, for example `generate-react-component.prompt.md`, a clear one-sentence description, and category such as code generation, analysis, documentation, testing, refactoring, or architecture.

**Step 2 — Define the persona.** Ask what role Copilot should embody, including technical expertise level such as junior, senior, expert, or specialist; domain knowledge such as languages, frameworks, and tools; years of experience or qualifications; and any example persona like a senior .NET architect with 10+ years of enterprise experience in C# 12, ASP.NET Core, and clean architecture patterns.

**Step 3 — Specify the task.** Ask for the primary task, measurable outcome, secondary or optional tasks, user inputs, constraints, and requirements. Identify what the prompt should avoid.

**Step 4 — Capture context variables.** Ask whether the prompt uses `${selection}`, `${file}`, `${workspaceFolder}`, `${input:variableName}`, `${input:variableName:placeholder}`, other file references, or other prompt files as dependencies. Note that references to `*.prompt.md` files are legitimate inside this meta-prompt and generated prompt only when VS Code prompt behavior requires them.

**Step 5 — Collect standards and instructions.** Ask for step-by-step process, coding standards, frameworks, libraries, best practices, avoidances, and whether any `.instructions.md` files should be followed.

**Step 6 — Define output requirements.** Ask whether output should be code, Markdown, JSON, structured data, new files, modified files, or Chat response. Capture file paths, naming conventions, examples, few-shot samples, formatting requirements, and structure requirements.

**Step 7 — Select tools and configuration.** Ask which VS Code tools the prompt needs. Omit `tools` when inherited tools are sufficient. When tools are required, copy exact IDs from VS Code's Configure Tools picker and keep the list minimal. Ask whether `agent` should be `agent`, `ask`, `edit`, or a custom agent name. Ask whether a specific `model` is required; otherwise omit it.

**Step 8 — Define validation criteria.** Ask how success should be measured, what validation steps are required, common failure modes, and error-handling or recovery steps.

**Step 9 — Generate the prompt.** Use the current mandatory ten-section prompt structure. Do not use the older generic structure with arbitrary task, instruction, context, output, and validation headings. Include a concrete fenced output skeleton and a realistic invocation example.

**Step 10 — Validate and deliver.** Check frontmatter, H1 placement, section order, tool IDs, direct imperative style, no placeholders, no relative primitive links, and no claims that CLI validators cover prompts. Deliver to the selected destination only.

## Invocation Example

```
/prompt-builder name=review-api-contract purpose="Review an API contract for consistency" destination=response
```

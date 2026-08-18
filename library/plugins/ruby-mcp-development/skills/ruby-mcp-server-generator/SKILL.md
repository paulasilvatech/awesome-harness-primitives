---
name: "ruby-mcp-server-generator"
description: >-
  Generate a complete Ruby Model Context Protocol server project using the official MCP Ruby SDK gem. Use when the user asks to create or scaffold a Ruby MCP server with tools, prompts, resources, schemas, annotations, structured content responses, tests, stdio usage, and HTTP usage examples.
---

# Ruby MCP server generator

Generate a production-ready Ruby MCP server project from bundled templates, preserving Ruby naming conventions, SDK structure, schemas, annotations, error handling, tests, and both stdio and HTTP usage examples.

## When to invoke

- "Generate a Ruby MCP server project."
- "Scaffold an MCP server in Ruby with tools and prompts."
- "Create a Ruby server using the official MCP SDK gem."
- "Add tests and schemas to a Ruby MCP server template."

## Request parameters

Ask for project name and description when missing. Convert the project name into snake_case file/module paths and a Ruby module name before generating files.

## Project structure

Generate this complete tree, adapting `my-mcp-server` and `my_mcp_server` to the user's project name:

```text
my-mcp-server/
├── Gemfile
├── Rakefile
├── lib/
│   ├── my_mcp_server.rb
│   ├── my_mcp_server/
│   │   ├── server.rb
│   │   ├── tools/
│   │   │   ├── greet_tool.rb
│   │   │   └── calculate_tool.rb
│   │   ├── prompts/
│   │   │   └── code_review_prompt.rb
│   │   └── resources/
│   │       └── example_resource.rb
├── bin/
│   └── mcp-server
├── test/
│   ├── test_helper.rb
│   └── tools/
│       ├── greet_tool_test.rb
│       └── calculate_tool_test.rb
└── README.md
```

## Generation rules

| Area | Rule |
| --- | --- |
| Templates | Open `references/project-templates.md` and copy/adapt the full templates verbatim before inventing structure. |
| Tools and prompts | Use classes for tools and prompts for better organization. |
| Schemas | Include input/output schemas for type safety. |
| Annotations | Add tool annotations that describe behavior and safety hints. |
| Responses | Include structured content in responses, not only plain text. |
| Errors | Return proper error responses with an `is_error` flag. |
| Tests | Implement comprehensive tests for all tools, including success and error paths. |
| Ruby conventions | Use `snake_case`, modules, and `frozen_string_literal`. |
| Usage | Provide both stdio and HTTP examples in `README.md`. |

## Procedure

1. Collect project name and description if the user did not provide them.
2. Normalize names for directory, executable, file paths, and Ruby module constants.
3. Read `references/project-templates.md` and adapt every required file in the project tree.
4. Generate all files with correct naming, module nesting, SDK setup, tools, prompts, resources, and executable entry point.
5. Add input/output schemas, tool annotations, structured responses, `is_error` error handling, and tests.
6. Validate with the existing Ruby test command if dependencies are available; otherwise report the exact command the user should run.

## Progressive disclosure and bundled resources

- `references/project-templates.md`: canonical Ruby MCP server project templates; read it before creating project files and copy/adapt the templates verbatim.

## Gotchas

- **Do not generate only a single server file**: the skill requires a complete project tree with tests and README.
- **Do not skip schemas**: MCP clients depend on clear input/output contracts.
- **Do not use ad hoc hashes for everything**: classes and modules keep tools, prompts, and resources maintainable.

## Output template

```markdown
### Ruby MCP server generation

**Status:** complete | needs input | blocked
**Project:** `<my-mcp-server>`
**Module:** `<MyMcpServer>`

| Artifact | Path | Notes |
| --- | --- | --- |
| Gemfile | `<project>/Gemfile` | official MCP Ruby SDK gem |
| Server | `<project>/lib/<name>/server.rb` | tools/prompts/resources registered |
| Tools | `<project>/lib/<name>/tools/*.rb` | schemas, annotations, structured content |
| Tests | `<project>/test/tools/*_test.rb` | success and error paths |
| README | `<project>/README.md` | stdio and HTTP usage examples |

**Validation**
- `<ruby test command>`: pass | fail | not run
```

## Quality gate

- [ ] Project name and description were collected or inferred.
- [ ] `references/project-templates.md` was read before generation.
- [ ] The generated tree includes `Gemfile`, `Rakefile`, `lib/`, `bin/mcp-server`, `test/`, and `README.md`.
- [ ] Tools and prompts are classes with input/output schemas and annotations.
- [ ] Responses include structured content and use `is_error` for error cases.
- [ ] Tests cover all generated tools.
- [ ] Ruby conventions are followed: `snake_case`, modules, and `frozen_string_literal`.
- [ ] README includes both stdio and HTTP usage examples.

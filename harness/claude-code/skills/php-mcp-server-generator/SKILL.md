---
name: php-mcp-server-generator
description: >-
  Generate a complete PHP Model Context Protocol server project with tools, resources, prompts,
  tests, and Claude Desktop configuration using the official PHP SDK. Use this skill when the user
  asks for a PHP MCP server, PHP SDK MCP project, stdio or HTTP MCP transport,
  tool/resource/prompt scaffolding, or production-ready MCP server requirements.
---

<!-- Generated from harness/github-copilot/skills/php-mcp-server-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# PHP MCP server generator

Generate a production-ready PHP MCP server by collecting project requirements, reading the bundled implementation reference, then producing a Composer project with typed tools, optional resources and prompts, tests, runnable stdio or HTTP transport configuration, and clear tools/resources boundaries.

## When to invoke

- "Generate a PHP MCP server."
- "Create a complete MCP server project using the PHP SDK."
- "Scaffold MCP tools, resources, prompts, and tests in PHP."
- "Build a stdio or HTTP PHP MCP server for Claude Desktop."
- "I need project requirements for a PHP MCP server."

## Prerequisites and context

- PHP 8.2 or higher is required.
- Composer is required for dependency installation and autoloading.
- Read `references/templates-and-development.md` before generating files or implementing PHP tools/resources.
- Use the official PHP SDK patterns from the bundled reference; do not invent framework APIs when the reference gives an attribute, bootstrap, or test pattern.

## Required inputs

| Input | Required | Notes |
| --- | --- | --- |
| Project name | Yes | Kebab-case directory such as `my-mcp-server`; reuse as Composer package suffix. |
| Server description | Yes | One sentence, for example `A file management MCP server`. |
| Transport type | Yes | `stdio`, `http`, or `both`. |
| Tools to include | Yes | Examples: `file read`, `file write`, `list directory`; each needs name, inputs, output, and failure modes. |
| Resources and prompts | Conditional | Include only when the user requests read-only resources or reusable prompt templates. |
| PHP version | Yes | Require PHP 8.2+; reject lower versions or raise the target. |

## Project structure

Generate this tree and omit only optional folders the user explicitly excludes:

```text
{project-name}/
├── composer.json
├── .gitignore
├── README.md
├── server.php
├── src/
│   ├── Tools/
│   │   └── {ToolClass}.php
│   ├── Resources/
│   │   └── {ResourceClass}.php
│   ├── Prompts/
│   │   └── {PromptClass}.php
│   └── Providers/
│       └── {CompletionProvider}.php
└── tests/
    └── ToolsTest.php
```

## Implementation rules

| Area | Requirement |
| --- | --- |
| Attributes | Use `#[McpTool]`, `#[McpResource]`, and `#[McpPrompt]` for clean discovery. |
| Parameters | Use `#[Schema]` attributes for validation and document each input in PHPDoc. |
| Types | Put `declare(strict_types=1);` at the top of all PHP files and use explicit return types. |
| Style | Follow PSR-12 and Composer PSR-4 autoloading. |
| Errors | Throw specific exceptions with clear user-safe messages; do not leak credentials or local paths. |
| Tests | Write PHPUnit tests for every tool, including success, validation failure, and domain failure. |
| Documentation | Include README setup, transport, Claude Desktop configuration, and inspector commands. |
| Discovery cache | Always use PSR-16 cache for discovery in production. |

## Commands and runtime configuration

| Purpose | Command or file |
| --- | --- |
| Install dependencies | `composer install` |
| Run tests | `vendor/bin/phpunit` |
| Start stdio server | `php server.php` |
| Test with inspector | `npx @modelcontextprotocol/inspector php server.php` |
| Claude Desktop command | `php` |
| Claude Desktop args | `["/absolute/path/to/server.php"]` |

Claude Desktop configuration:

```json
{
  "mcpServers": {
    "{project-name}": {
      "command": "php",
      "args": ["/absolute/path/to/server.php"]
    }
  }
}
```

## Tool design checklist

| Field | Rule |
| --- | --- |
| `{tool_name}` | Use a stable lower camel or snake name that describes the action, not the transport. |
| Tool description | State what the tool does, required inputs, side effects, and output shape. |
| Inputs | Validate with schema attributes; reject path traversal, unsupported protocols, and ambiguous defaults. |
| Outputs | Return structured arrays or DTOs that serialize predictably. |
| Side effects | Mark write operations clearly in descriptions and tests. |
| Completion provider | Add `{CompletionProvider}` only when argument completion is useful and supported by the generated server. |

## Progressive disclosure and bundled resources

- `references/templates-and-development.md`: PHP MCP templates, SDK development details, and implementation patterns. Open it before generating `composer.json`, `server.php`, tool classes, resources, prompts, providers, or tests.

## Gotchas

- **Do not skip the bundled reference**: the reference carries the SDK-specific templates that prevent plausible but wrong PHP MCP APIs.
- **Do not generate untyped PHP**: strict types, PHPDoc, and return types are required because MCP schemas are inferred from code.
- **Do not make every transport default**: implement `stdio`, `http`, or `both` according to the user's requirement.
- **Do not cache discovery only in memory for production**: use PSR-16 cache for stable production discovery.

## Output template

````markdown
## PHP MCP server project

**Status:** generated | requirements needed | blocked
**Project:** `{project-name}`
**Transport:** stdio | http | both
**PHP target:** `8.2+`

### Files
| Path | Purpose |
| --- | --- |
| `composer.json` | Dependencies, scripts, autoloading |
| `server.php` | MCP server entrypoint |
| `src/Tools/{ToolClass}.php` | Tool implementation |
| `src/Resources/{ResourceClass}.php` | Resource implementation, if requested |
| `src/Prompts/{PromptClass}.php` | Prompt implementation, if requested |
| `tests/ToolsTest.php` | PHPUnit coverage for tools |

### Commands
- `composer install`
- `vendor/bin/phpunit`
- `php server.php`
- `npx @modelcontextprotocol/inspector php server.php`

### Claude Desktop
```json
{
  "mcpServers": {
    "{project-name}": {
      "command": "php",
      "args": ["/absolute/path/to/server.php"]
    }
  }
}
```
````

## Quality gate

- [ ] The project name, description, transport type, tools, resource/prompt choice, and PHP version are known.
- [ ] `references/templates-and-development.md` was read before generating implementation code.
- [ ] The generated tree contains `composer.json`, `.gitignore`, `README.md`, `server.php`, `src/`, and `tests/`.
- [ ] Tool classes use `#[McpTool]`; resource and prompt classes use `#[McpResource]` and `#[McpPrompt]` when present.
- [ ] Parameters use `#[Schema]`, strict types, PHPDoc, and explicit return types.
- [ ] Production discovery uses PSR-16 cache.
- [ ] README includes `composer install`, `vendor/bin/phpunit`, `php server.php`, inspector usage, and Claude Desktop JSON.

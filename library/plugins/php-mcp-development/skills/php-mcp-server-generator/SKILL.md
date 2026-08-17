---
name: "php-mcp-server-generator"
description: >-
  Generate a complete PHP Model Context Protocol server project with tools, resources, prompts, and
  tests using the official PHP SDK. Use this skill when the user asks for project requirements.
---
# PHP MCP Server Generator

You are a PHP MCP server generator. Create a complete, production-ready PHP MCP server project using the official PHP SDK.

## Project Requirements

Ask the user for:
1. **Project name** (e.g., "my-mcp-server")
2. **Server description** (e.g., "A file management MCP server")
3. **Transport type** (stdio, http, or both)
4. **Tools to include** (e.g., "file read", "file write", "list directory")
5. **Whether to include resources and prompts**
6. **PHP version** (8.2+ required)

## Project Structure

```
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

## Bundled Resources

- [PHP MCP server templates and development details](references/templates-and-development.md) — When generating files or implementing PHP tools/resources, open this template and development reference.

## Requirements

- PHP 8.2 or higher
- Composer

## Installation

```bash
composer install
```

## Usage

### Start Server (Stdio)

```bash
php server.php
```

### Configure in Claude Desktop

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

## Testing

```bash
vendor/bin/phpunit
```

## Tools

- **{tool_name}**: {Tool description}

## Implementation Guidelines

1. **Use PHP Attributes**: Leverage `#[McpTool]`, `#[McpResource]`, `#[McpPrompt]` for clean code
2. **Type Declarations**: Use strict types (`declare(strict_types=1);`) in all files
3. **PSR-12 Coding Standard**: Follow PHP-FIG standards
4. **Schema Validation**: Use `#[Schema]` attributes for parameter validation
5. **Error Handling**: Throw specific exceptions with clear messages
6. **Testing**: Write PHPUnit tests for all tools
7. **Documentation**: Use PHPDoc blocks for all methods
8. **Caching**: Always use PSR-16 cache for discovery in production

## Running the Server

```bash
# Install dependencies
composer install

# Run tests
vendor/bin/phpunit

# Start server
php server.php

# Test with inspector
npx @modelcontextprotocol/inspector php server.php
```

## Claude Desktop Configuration

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

Now generate the complete project based on user requirements!

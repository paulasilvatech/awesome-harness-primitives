---
paths:
  - "**/*.php"
---

<!-- Generated from harness/github-copilot/instructions/php-mcp-server.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces PHP Model Context Protocol server conventions for the official PHP SDK, capability discovery, transports, sessions, errors, testing, performance, framework integration, deployment, and client configuration.

# PHP MCP Server Conventions — SDK Servers and Capabilities

These instructions apply to PHP files that implement Model Context Protocol servers with the official `mcp/sdk` package maintained with The PHP Foundation. They are authoritative for PHP MCP server structure, Composer setup, SDK capability registration, transports, sessions, error handling, testing, caching, deployment, and MCP client configuration in matched files; project architecture, security, and hosting primitives win where they define stricter deployment or secret-handling requirements.

## Composer Package and Project Shape

Use Composer, PHP 8.2 or newer, PSR-4 autoloading, and one explicit server entry point. Keep MCP capabilities grouped by concern so attribute discovery and manual registration remain predictable.

| Concern | Convention |
| --- | --- |
| Package install | Require the SDK with `composer require mcp/sdk`; keep `mcp/sdk` in `require` and testing tools such as `phpunit/phpunit` in `require-dev`. |
| PHP baseline | Set `"php": "^8.2"` when the server uses attributes, enums, promoted properties, and strict typing. |
| Autoloading | Use a namespace such as `App\\` mapped to `src/`; require `vendor/autoload.php` from the executable entry point with `require_once`. |
| Entry point | Keep `server.php` or `app/server.php` as the CLI entry; start it with `#!/usr/bin/env php`, `declare(strict_types=1)`, and executable permissions when deployed as a command. |
| Layout | Use `my-mcp-server/`, `composer.json`, `src/Tools`, `src/Resources`, `src/Prompts`, `src/Server.php`, `server.php`, `README.txt`, and `tests/ToolsTest.php` as the default shape for attribute-based MCP servers. |
| Package naming | Use a Composer package name such as `your-org/mcp-server`; keep placeholders like `your-org` out of production manifests. |

## Server Construction and Discovery

Build servers through `Server::builder()` and make registration choices explicit.

| SDK API | Use |
| --- | --- |
| `setServerInfo('My MCP Server', '1.0.0')` | Publish stable server metadata for clients and inspectors. |
| `setDiscovery(__DIR__, ['.'])` | Scan a small, known root for attributes in simple servers. |
| `setDiscovery(basePath: __DIR__, scanDirs: ['.', 'src'], excludeDirs: ['vendor', 'tests'], cache: $cache)` | Use named arguments when discovery needs exclusions or caching. |
| `addTool([Calculator::class, 'add'], 'add')` and `addTool([Calculator::class, 'multiply'], 'multiply')` | Register tools manually when discovery is undesirable or the public name must be fixed. |
| `addResource([Config::class, 'getSettings'], 'config://app/settings')` | Register a resource URI such as `config://app/settings` without relying on scanning. |
| `build()` then `run($transport)` | Construct once, choose a transport, and run through the SDK instead of hand-rolling JSON-RPC. |

Cache discovery in production with PSR-16. `Psr16Cache` over `FilesystemAdapter('mcp-discovery')` is acceptable for local deployments; `Psr16Cache` over `RedisAdapter` with `\Redis`, `connect('127.0.0.1', 6379)`, and a stable key namespace is better for multi-process hosts. Limit `scanDirs` to `src`, `src/Tools`, and `src/Resources`, and exclude `vendor`, `tests`, `var`, and `cache`.

## Tools, Schemas, and Return Content

Tools are public callable capabilities. Keep names stable, parameter schemas specific, and return content explicit.

| Capability pattern | Convention |
| --- | --- |
| Simple tool | Annotate methods with `#[McpTool]`; document parameters and return values with PHPDoc where it improves generated schemas. |
| Custom tool name | Use `#[McpTool(name: 'read_file')]` or `#[McpTool(name: 'create_user')]` when the protocol name should be snake_case rather than the PHP method name. |
| Validation | Apply `#[Schema(format: 'email')]`, `#[Schema(minimum: 18, maximum: 120)]`, and `#[Schema(pattern: '^[A-Z][a-z]+$', description: 'Capitalized first name')]` to parameters that need client-visible constraints. |
| Complex content | Return `TextContent`, `TextContent::code($code, 'php')`, and `ImageContent(data: base64_encode($imageData), mimeType: 'image/png')` for mixed text and image responses. |
| Calculations | Prefer `match($operation)` for closed choices such as `add`, `subtract`, `multiply`, and `divide`; throw `\InvalidArgumentException` for invalid operations and division by zero. |
| File tools | Guard `file_exists($path)`, `is_readable($filename)`, and `file_get_contents(...)`; throw `\InvalidArgumentException` for bad input and `\RuntimeException` for unreadable server state. |

Do not expose filesystem reads, network fetches, or mutation tools without validation. A tool such as `readFileContent(string $path): string` must restrict paths according to the project security model before returning `file_get_contents($path)`.

## Resources, Resource Templates, and Prompt Capabilities

Use MCP resources for addressable data and MCP prompts for reusable prompt messages. Preserve MIME types and URI templates because clients use them for routing and rendering.

| Attribute or type | Convention |
| --- | --- |
| `#[McpResource(uri: 'config://app/settings', name: 'app_settings', mimeType: 'application/json')]` | Use for static resources such as `app/settings`; return arrays only when the SDK can serialize them deterministically. |
| `#[McpResourceTemplate(uriTemplate: 'user://{userId}/profile/{section}', name: 'user_profile', description: 'User profile data by section', mimeType: 'application/json')]` | Keep function parameters in the same order as URI variables such as `userId` then `section`. |
| `TextResourceContents` | Return text resources with explicit `uri`, `mimeType: 'text/plain'`, and `text`. |
| `BlobResourceContents` | Return binary resources with explicit `uri`, `mimeType: 'image/png'`, and base64-encoded `blob`. |
| `#[McpPrompt(name: 'code_review')]` | Use for reusable prompts that accept arguments such as `language`, `code`, and `focus`. |
| `PromptMessage`, `Role::Assistant`, `Role::User`, `TextContent`, `ImageContent` | Use typed prompt messages for mixed content such as `image/jpeg`; plain `['role' => 'user', 'content' => ...]` arrays are acceptable only for simple text. |

Do not route MCP prompt capabilities through editor-only prompt assets. MCP prompt capabilities belong in PHP classes under `src/Prompts`.

## Completion Providers and Enums

Use completions to constrain user-facing arguments before a tool, prompt, or template is invoked.

| Completion shape | Convention |
| --- | --- |
| Static values | Use `#[CompletionProvider(values: ['blog', 'article', 'tutorial', 'guide'])]` and `#[CompletionProvider(values: ['beginner', 'intermediate', 'advanced'])]` for short, stable vocabularies. |
| Backed enum | Use `#[CompletionProvider(enum: Priority::class)]` with `enum Priority: string` and cases `LOW = 'low'`, `MEDIUM = 'medium'`, and `HIGH = 'high'`. |
| Unit enum | Use `#[CompletionProvider(enum: Status::class)]` with cases `DRAFT`, `PUBLISHED`, and `ARCHIVED` when only names matter. |
| Custom provider | Implement `ProviderInterface` in a class such as `UserIdCompletionProvider`; inject services such as `DatabaseService` and return values from `getCompletions(string $currentValue): array`. |

## SDK Class and Example Name Inventory

Preserve SDK-facing names from examples when refactoring so documentation, tests, and generated schemas remain searchable.

| Name | Convention |
| --- | --- |
| `Calculator`, `CalculatorTest`, `FileManager`, `UserManager`, `ReportGenerator` | Use these as examples of tool classes and their PHPUnit coverage; keep methods such as `add`, `multiply`, `readFileContent`, `createUser`, `generateReport`, and `getChart` tied to tool behavior. |
| `ConfigProvider`, `DataProvider`, `FileProvider`, `UserProvider`, `PromptGenerator` | Use these as examples of resource, data, file, template, and prompt capability classes. |
| `{$language}\n{$code}\n` | Preserve this interpolation shape when documenting a `code_review` prompt body that embeds a language-tagged fenced code sample. |
| `text/plain`, `application/json`, `image/png`, `image/jpeg` | Keep MIME types explicit in resources, blobs, and prompt content. |
| `command-line` and `web-based` | Use these terms to distinguish `StdioTransport` CLI integration from HTTP transport integration. |

## Transport and Session Boundaries

Choose the transport by integration shape and isolate session storage from application state.

| Scenario | Convention |
| --- | --- |
| Command-line integration | Use `StdioTransport` and run with `php /absolute/path/to/server.php`; this is the default for local MCP clients. |
| Web-based integration | Use `StreamableHttpTransport`, `Psr17Factory`, `createServerRequestFromGlobals()`, `$response->getHeaders()`, `http_response_code($response->getStatusCode())`, and `echo $response->getBody()` when embedding in a PHP web endpoint. |
| In-memory sessions | Use `setSession(ttl: 7200)` for short-lived default sessions; `7200` means two hours. |
| File sessions | Use `FileSessionStore(__DIR__ . '/sessions')` only when the directory is protected and cleaned by deployment policy. |
| Custom in-memory store | Use `InMemorySessionStore(3600)` when a one-hour TTL is required explicitly. |

Do not mix transport code into tool classes. The server entry point owns `StdioTransport` or `StreamableHttpTransport`; tools, resources, prompts, and completion providers remain transport-neutral.

## Framework Integration and Deployment

Integrate through the framework's normal command or bundle surface and keep production images reproducible.

| Platform | Convention |
| --- | --- |
| Laravel | Put the command in `app/Console/Commands/McpServer.php`, extend `Illuminate\Console\Command`, set `$signature = 'mcp:serve'`, use `app_path()` with scan directories `Tools` and `Resources`, then run a `StdioTransport`. |
| Symfony | Prefer `symfony/mcp-bundle`; install with `composer require symfony/mcp-bundle` instead of hand-copying bundle internals. |
| Docker | Base CLI images on `FROM php:8.2-cli`, install extensions with `docker-php-ext-install pdo pdo_mysql`, `COPY --from=composer:latest /usr/bin/composer /usr/bin/composer`, `WORKDIR /app`, `COPY . /app`, and `RUN composer install --no-dev --optimize-autoloader`. |
| Executable server | Add `RUN chmod +x /app/server.php` and use `CMD ["php", "/app/server.php"]`. |
| systemd | Use `[Unit]`, `Description=MCP PHP Server`, `After=network.target`, `[Service]`, `Type=simple`, `User=www-data`, `WorkingDirectory=/var/www/mcp-server`, `ExecStart=/usr/bin/php /var/www/mcp-server/server.php`, `Restart=always`, and `[Install] WantedBy=multi-user.target`. |

## Client Configuration and Inspection

Keep MCP client configuration absolute and inspectable.

| Client or tool | Convention |
| --- | --- |
| Claude Desktop | Configure `"mcpServers": { "php-server": { "command": "php", "args": ["/absolute/path/to/server.php"] } }`; never use a relative `path/to/server.php` in committed examples. |
| MCP Inspector | Test locally with `npx @modelcontextprotocol/inspector php /path/to/server.php` before asking clients to connect. |
| Server naming | Keep names such as `php-server` stable because users reference them in client configuration. |

## Performance and Runtime Settings

Use cache and OPcache settings deliberately in production.

| Setting | Convention |
| --- | --- |
| Discovery cache | Enable `mcp-discovery` cache or Redis-backed PSR-16 cache for attribute discovery. |
| Scan scope | Scan only `src`, `src/Tools`, and `src/Resources`; exclude generated and dependency directories. |
| OPcache | Set `opcache.enable=1`, `opcache.memory_consumption=256`, `opcache.interned_strings_buffer=16`, `opcache.max_accelerated_files=10000`, and `opcache.validate_timestamps=0` for immutable production deployments. |
| Autoloader | Use `composer install --no-dev --optimize-autoloader` in production images. |

## Testing and Error Handling

Test capability classes as ordinary PHP units and test discovery separately.

| Test target | Convention |
| --- | --- |
| Tool behavior | Use `PHPUnit\Framework\TestCase`, instantiate `Calculator`, call methods such as `add(5, 3)`, and assert with `assertSame(8, $result)`. |
| Error paths | Use `expectException(\InvalidArgumentException::class)` and `expectExceptionMessage('Division by zero')` for rejected inputs. |
| Discovery | Build a test server with `Server::builder()->setServerInfo('Test Server', '1.0.0')->setDiscovery(__DIR__ . '/../src', ['.'])->build()`, call `getCapabilities()`, and assert `tools` exists and is not empty. |
| JSON-RPC errors | Let the SDK convert exceptions into JSON-RPC error responses; do not invent parallel error envelopes. |

## Good / Bad Examples

The examples below illustrate safe tool boundaries and transport-neutral capability code.

**Good:**

```php
#[McpTool(name: 'divide_numbers')]
public function divideNumbers(float $a, float $b): float
{
    if ($b === 0.0) {
        throw new \InvalidArgumentException('Division by zero is not allowed');
    }

    return $a / $b;
}
```

Why: The tool has a stable protocol name, validates invalid input before computation, and lets the SDK convert the exception into a JSON-RPC error response.

**Bad:**

```php
#[McpTool]
public function processFile(string $filename): string
{
    return file_get_contents($filename);
}
```

Why: The tool exposes unrestricted file access, omits `file_exists` and `is_readable` checks, and gives clients unpredictable PHP warnings instead of clear MCP errors.

## Conventions

| Rule | Rationale |
|---|---|
| Use `composer require mcp/sdk`, PHP `^8.2`, PSR-4 autoloading, and `declare(strict_types=1)` | Attribute-based discovery and typed SDK contracts require a modern, deterministic PHP runtime |
| Keep `server.php` responsible for `Server::builder()`, `setServerInfo`, discovery or manual registration, transport creation, and `run` | Capabilities stay testable and transport-neutral |
| Prefer attribute discovery with bounded `scanDirs`, `excludeDirs`, and PSR-16 cache in production | Startup remains fast and does not scan dependencies or tests |
| Validate tool inputs with PHP checks and `Schema` attributes | Clients receive useful schemas and server code rejects unsafe input before side effects |
| Use typed content classes for text, images, resources, blobs, prompt messages, and roles | MCP clients can render and route responses correctly |
| Choose `StdioTransport` for CLI clients and `StreamableHttpTransport` with PSR-17 factories for HTTP integration | Each transport follows the SDK-supported request and response lifecycle |
| Configure sessions with explicit TTLs and protected stores | Long-running clients keep context without leaking or persisting stale state indefinitely |
| Test tools, error paths, and discovery with PHPUnit | Capability behavior and SDK registration fail before deployment |
| Enable discovery cache, OPcache, and optimized Composer autoloading in production | Runtime overhead stays bounded for CLI and web integrations |
| Keep Docker, systemd, Laravel, Symfony, Claude Desktop, and MCP Inspector examples absolute and reproducible | Operators can run the same server consistently across environments |

## Do / Do Not

| Do | Do not |
|---|---|
| Put MCP tools in `src/Tools`, resources in `src/Resources`, and prompts in `src/Prompts` | Mix tools, resources, prompts, transport code, and framework commands in one class |
| Use `#[McpTool]`, `#[McpResource]`, `#[McpResourceTemplate]`, `#[McpPrompt]`, and `CompletionProvider` intentionally | Depend on accidental public methods or undocumented reflection behavior |
| Return `TextContent`, `ImageContent`, `TextResourceContents`, `BlobResourceContents`, or `PromptMessage` when content type matters | Return untyped arrays for mixed media or resource content that clients must render precisely |
| Throw `\InvalidArgumentException` for invalid client input and `\RuntimeException` for unreadable server state | Let PHP warnings, notices, or fatal errors become the protocol response |
| Use `StdioTransport` for local command-line clients and `StreamableHttpTransport` for HTTP endpoints | Write custom JSON-RPC loops around the SDK |
| Run `npx @modelcontextprotocol/inspector php /path/to/server.php` before publishing configuration | Ask users to debug uninspected client setup |
| Install production dependencies with `composer install --no-dev --optimize-autoloader` | Ship development packages and unoptimized autoloaders in runtime images |
| Preserve absolute paths such as `/absolute/path/to/server.php` in client examples | Commit relative paths or machine-specific placeholders as production configuration |

## Checklist Before Opening a PR

- [ ] Composer configuration includes `mcp/sdk`, PHP `^8.2`, PSR-4 autoloading, and test-only packages under `require-dev`.
- [ ] Server construction uses `Server::builder()`, `setServerInfo`, discovery or manual registration, `build()`, and an SDK transport.
- [ ] Attribute discovery scans only intended directories and excludes `vendor`, `tests`, `var`, and `cache`.
- [ ] Tools, resources, resource templates, prompts, and completions use stable MCP names, URI templates, MIME types, and schemas.
- [ ] File, network, and calculation tools validate inputs and throw explicit exceptions for invalid or unsafe states.
- [ ] Sessions use an explicit TTL or protected session store.
- [ ] PHPUnit covers ordinary tool behavior, error behavior, and capability discovery.
- [ ] Production deployment uses discovery cache, OPcache settings, and optimized Composer autoloading.
- [ ] Docker, systemd, Laravel, Symfony, Claude Desktop, and MCP Inspector examples remain absolute and runnable.
- [ ] No relative primitive links, editor-only prompt asset references, unrelated edits, or placeholder package names remain.

## References

- [Official PHP SDK Repository](https://github.com/modelcontextprotocol/php-sdk)
- [MCP Elements Documentation](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/mcp-elements.md)
- [Server Builder Documentation](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md)
- [Transport Documentation](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/transports.md)
- [Examples](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/examples.md)
- [MCP Specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [Model Context Protocol](https://modelcontextprotocol.io/)

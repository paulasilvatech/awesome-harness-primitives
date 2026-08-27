<!-- Generated from harness/github-copilot/instructions/quarkus-mcp-server-sse.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Java 21 Quarkus MCP server conventions for HTTP SSE transport, CDI tools, layered architecture, validation, and error handling.

# Quarkus MCP Server Conventions — HTTP SSE Transport

These instructions apply to Quarkus MCP server projects that expose tools over HTTP SSE transport. They are authoritative for Java 21, Quarkus, the `mcp-server-sse` extension, CDI tool beans, endpoint shape, package organization, validation, and error-handling conventions; project-specific domain, persistence, and deployment instructions win when they impose stricter runtime constraints.

## Stack and Endpoint

Use Java 21 with Quarkus Framework for MCP servers. Include the MCP Server Extension `mcp-server-sse` and expose the MCP endpoint at `http://localhost:8080/mcp/sse` unless the deployment configuration explicitly changes the port or path. Use CDI for dependency injection and keep server components compatible with Quarkus build-time discovery.

## Project Creation and Package Structure

Use the standard Quarkus CLI shape for new servers and keep package responsibilities clear.

```bash
quarkus create app --no-code -x rest-client-jackson,qute,mcp-server-sse your-domain-mcp-server
```

| Package | Responsibility |
| --- | --- |
| `model` | Immutable request, response, and domain data types. |
| `repository` | Thread-safe state management and data access. |
| `service` | Business logic, orchestration, validation decisions, and error mapping. |
| `mcp` | Thin MCP tool entry points that adapt tool calls to services. |

Use standard Java naming conventions: `PascalCase` classes and `camelCase` methods. Use record types for immutable data models and add Javadoc for public methods whose behavior is not obvious from the name and signature.

## MCP Tool Methods

Expose tools as public methods on `@ApplicationScoped` CDI beans. Annotate each tool method with `@Tool(name="tool_name", description="clear description")`, using stable snake-case tool names and descriptions that tell callers what the tool does and what input it expects.

- Validate every parameter before calling services.
- Never return `null`; return a useful error message or typed error result instead.
- Do not throw raw exceptions from tools to clients; handle errors gracefully.
- Keep tool methods thin and delegate business logic to the service layer.
- Use `Optional<T>` inside Java APIs to represent absence and avoid null pointer exceptions.

## Architecture, State, and Thread Safety

Maintain the dependency direction `MCP tools → Service layer → Repository`. Use `@Inject` for dependencies and keep state management in the repository layer. Make data operations thread-safe because MCP tool calls may be concurrent. Prefer immutable values, records, and defensive copies at layer boundaries.

## Testing and Edge Cases

Test tool behavior with null, empty inputs, malformed inputs, missing records, and service failures. Verify the HTTP SSE endpoint in local development and keep tests focused on the public tool behavior plus service-layer validation. Do not put business logic in MCP tools because tool tests should not need to duplicate domain tests.

## Good / Bad Examples

The examples below illustrate a thin CDI tool and service delegation.

**Good:**

```java
@ApplicationScoped
public class CatalogTools {
    @Inject CatalogService catalogService;

    @Tool(name = "find_item", description = "Find an item by identifier.")
    public String findItem(String id) {
        if (id == null || id.isBlank()) {
            return "id is required";
        }

        return catalogService.findItem(id).orElse("item not found");
    }
}
```

Why: The public `@Tool` method is in an `@ApplicationScoped` CDI bean, validates input, returns a non-null message, and delegates lookup behavior to a service.

**Bad:**

```java
public class CatalogTools {
    @Tool(name = "find_item", description = "Find item")
    public String findItem(String id) {
        return StaticDatabase.items.get(id).toString();
    }
}
```

Why: The class is not a CDI bean, does business and data access work in the tool, assumes non-null state, and can throw exceptions directly to MCP callers.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use Java 21, Quarkus, CDI, and `mcp-server-sse` | The server matches the intended MCP SSE stack. |
| Keep the endpoint `http://localhost:8080/mcp/sse` unless configuration changes it | Local clients can connect predictably. |
| Organize code into `model`, `repository`, `service`, and `mcp` packages | Responsibilities remain clear and testable. |
| Expose MCP tools as public `@Tool` methods in `@ApplicationScoped` beans | Quarkus can discover and serve tools through CDI. |
| Validate parameters and return non-null errors or results | MCP callers receive useful responses instead of nulls or raw exceptions. |
| Keep business logic in services and state in repositories | Tool methods stay thin and concurrency concerns stay isolated. |
| Use records, immutable data, `Optional<T>`, and thread-safe data operations | Null pointer exceptions and shared-state races are reduced. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Create servers with `quarkus create app --no-code -x rest-client-jackson,qute,mcp-server-sse your-domain-mcp-server` | Start from an unrelated Quarkus shape and bolt MCP on later. |
| Annotate CDI beans with `@ApplicationScoped` | Put `@Tool` methods on unmanaged classes. |
| Use `@Inject` for service and repository dependencies | Manually construct dependencies inside tool methods. |
| Return clear error messages for invalid input | Return `null` or let null pointer exceptions escape. |
| Test null, empty inputs, and edge cases | Test only the happy path. |
| Keep tool methods thin | Put business logic directly in MCP tool methods. |

## Checklist Before Opening a PR

- [ ] The project targets Java 21 and Quarkus with the `mcp-server-sse` extension.
- [ ] The MCP SSE endpoint is documented or configured as `http://localhost:8080/mcp/sse`.
- [ ] Code is organized into `model`, `repository`, `service`, and `mcp` packages.
- [ ] Public tool methods are annotated with `@Tool(name="tool_name", description="clear description")` in `@ApplicationScoped` beans.
- [ ] Dependencies use CDI `@Inject`.
- [ ] Tool methods validate parameters and never return `null`.
- [ ] Business logic lives in services and state management lives in repositories.
- [ ] Data operations are thread-safe and absence is represented with `Optional<T>` where appropriate.
- [ ] Edge cases such as null, empty inputs, and service errors are tested.

## References

- Local MCP SSE endpoint: http://localhost:8080/mcp/sse

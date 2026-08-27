# Extended guide for java-mcp-server-generator

## ToolDefinitions.java Template

```java
package com.example.mcp.tools;

import io.mcp.json.JsonSchema;
import io.mcp.server.tool.Tool;

import java.util.List;

public class ToolDefinitions {

    public static List<Tool> getTools() {
        return List.of(
            createGreetTool(),
            createCalculateTool()
        );
    }

    private static Tool createGreetTool() {
        return Tool.builder()
            .name("greet")
            .description("Generate a greeting message")
            .inputSchema(JsonSchema.object()
                .property("name", JsonSchema.string()
                    .description("Name to greet")
                    .required(true)))
            .build();
    }

    private static Tool createCalculateTool() {
        return Tool.builder()
            .name("calculate")
            .description("Perform mathematical calculations")
            .inputSchema(JsonSchema.object()
                .property("operation", JsonSchema.string()
                    .description("Operation to perform")
                    .enumValues(List.of("add", "subtract", "multiply", "divide"))
                    .required(true))
                .property("a", JsonSchema.number()
                    .description("First operand")
                    .required(true))
                .property("b", JsonSchema.number()
                    .description("Second operand")
                    .required(true)))
            .build();
    }
}
```

## ToolHandlers.java Template

```java
package com.example.mcp.tools;

import com.fasterxml.jackson.databind.JsonNode;
import io.mcp.server.McpServer;
import io.mcp.server.tool.ToolResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Mono;

public class ToolHandlers {

    private static final Logger log = LoggerFactory.getLogger(ToolHandlers.class);

    public static void register(McpServer server) {
        // Register tool list handler
        server.addToolListHandler(() -> {
            log.debug("Listing available tools");
            return Mono.just(ToolDefinitions.getTools());
        });

        // Register greet handler
        server.addToolHandler("greet", ToolHandlers::handleGreet);

        // Register calculate handler
        server.addToolHandler("calculate", ToolHandlers::handleCalculate);
    }

    private static Mono<ToolResponse> handleGreet(JsonNode arguments) {
        log.info("Greet tool called");

        if (!arguments.has("name")) {
            return Mono.just(ToolResponse.error()
                .message("Missing 'name' parameter")
                .build());
        }

        String name = arguments.get("name").asText();
        String greeting = "Hello, " + name + "! Welcome to MCP.";

        log.debug("Generated greeting for: {}", name);

        return Mono.just(ToolResponse.success()
            .addTextContent(greeting)
            .build());
    }

    private static Mono<ToolResponse> handleCalculate(JsonNode arguments) {
        log.info("Calculate tool called");

        if (!arguments.has("operation") || !arguments.has("a") || !arguments.has("b")) {
            return Mono.just(ToolResponse.error()
                .message("Missing required parameters")
                .build());
        }

        String operation = arguments.get("operation").asText();
        double a = arguments.get("a").asDouble();
        double b = arguments.get("b").asDouble();

        double result;
        switch (operation) {
            case "add":
                result = a + b;
                break;
            case "subtract":
                result = a - b;
                break;
            case "multiply":
                result = a * b;
                break;
            case "divide":
                if (b == 0) {
                    return Mono.just(ToolResponse.error()
                        .message("Division by zero")
                        .build());
                }
                result = a / b;
                break;
            default:
                return Mono.just(ToolResponse.error()
                    .message("Unknown operation: " + operation)
                    .build());
        }

        log.debug("Calculation: {} {} {} = {}", a, operation, b, result);

        return Mono.just(ToolResponse.success()
            .addTextContent("Result: " + result)
            .build());
    }
}
```

## ResourceDefinitions.java Template

```java
package com.example.mcp.resources;

import io.mcp.server.resource.Resource;

import java.util.List;

public class ResourceDefinitions {

    public static List<Resource> getResources() {
        return List.of(
            Resource.builder()
                .name("Example Data")
                .uri("resource://data/example")
                .description("Example resource data")
                .mimeType("application/json")
                .build(),
            Resource.builder()
                .name("Configuration")
                .uri("resource://config")
                .description("Server configuration")
                .mimeType("application/json")
                .build()
        );
    }
}
```

## ResourceHandlers.java Template

```java
package com.example.mcp.resources;

import io.mcp.server.McpServer;
import io.mcp.server.resource.ResourceContent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Mono;

import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class ResourceHandlers {

    private static final Logger log = LoggerFactory.getLogger(ResourceHandlers.class);
    private static final Map<String, Boolean> subscriptions = new ConcurrentHashMap<>();

    public static void register(McpServer server) {
        // Register resource list handler
        server.addResourceListHandler(() -> {
            log.debug("Listing available resources");
            return Mono.just(ResourceDefinitions.getResources());
        });

        // Register resource read handler
        server.addResourceReadHandler(ResourceHandlers::handleRead);

        // Register resource subscribe handler
        server.addResourceSubscribeHandler(ResourceHandlers::handleSubscribe);

        // Register resource unsubscribe handler
        server.addResourceUnsubscribeHandler(ResourceHandlers::handleUnsubscribe);
    }

    private static Mono<ResourceContent> handleRead(String uri) {
        log.info("Reading resource: {}", uri);

        switch (uri) {
            case "resource://data/example":
                String jsonData = String.format(
                    "{\"message\":\"Example resource data\",\"timestamp\":\"%s\"}",
                    Instant.now()
                );
                return Mono.just(ResourceContent.text(jsonData, uri, "application/json"));

            case "resource://config":
                String config = "{\"serverName\":\"my-mcp-server\",\"version\":\"1.0.0\"}";
                return Mono.just(ResourceContent.text(config, uri, "application/json"));

            default:
                log.warn("Unknown resource requested: {}", uri);
                return Mono.error(new IllegalArgumentException("Unknown resource URI: " + uri));
        }
    }

    private static Mono<Void> handleSubscribe(String uri) {
        log.info("Client subscribed to resource: {}", uri);
        subscriptions.put(uri, true);
        return Mono.empty();
    }

    private static Mono<Void> handleUnsubscribe(String uri) {
        log.info("Client unsubscribed from resource: {}", uri);
        subscriptions.remove(uri);
        return Mono.empty();
    }
}
```

## PromptDefinitions.java Template

```java
package com.example.mcp.prompts;

import io.mcp.server.prompt.Prompt;
import io.mcp.server.prompt.PromptArgument;

import java.util.List;

public class PromptDefinitions {

    public static List<Prompt> getPrompts() {
        return List.of(
            Prompt.builder()
                .name("code-review")
                .description("Generate a code review prompt")
                .argument(PromptArgument.builder()
                    .name("language")
                    .description("Programming language")
                    .required(true)
                    .build())
                .argument(PromptArgument.builder()
                    .name("focus")
                    .description("Review focus area")
                    .required(false)
                    .build())
                .build()
        );
    }
}
```

## PromptHandlers.java Template

```java
package com.example.mcp.prompts;

import io.mcp.server.McpServer;
import io.mcp.server.prompt.PromptMessage;
import io.mcp.server.prompt.PromptResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

public class PromptHandlers {

    private static final Logger log = LoggerFactory.getLogger(PromptHandlers.class);

    public static void register(McpServer server) {
        // Register prompt list handler
        server.addPromptListHandler(() -> {
            log.debug("Listing available prompts");
            return Mono.just(PromptDefinitions.getPrompts());
        });

        // Register prompt get handler
        server.addPromptGetHandler(PromptHandlers::handleCodeReview);
    }

    private static Mono<PromptResult> handleCodeReview(String name, Map<String, String> arguments) {
        log.info("Getting prompt: {}", name);

        if (!name.equals("code-review")) {
            return Mono.error(new IllegalArgumentException("Unknown prompt: " + name));
        }

        String language = arguments.getOrDefault("language", "Java");
        String focus = arguments.getOrDefault("focus", "general quality");

        String description = "Code review for " + language + " with focus on " + focus;

        List<PromptMessage> messages = List.of(
            PromptMessage.user("Please review this " + language + " code with focus on " + focus + "."),
            PromptMessage.assistant("I'll review the code focusing on " + focus + ". Please share the code."),
            PromptMessage.user("Here's the code to review: [paste code here]")
        );

        log.debug("Generated code review prompt for {} ({})", language, focus);

        return Mono.just(PromptResult.builder()
            .description(description)
            .messages(messages)
            .build());
    }
}
```

## McpServerTest.java Template

```java
package com.example.mcp;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import io.mcp.server.McpServer;
import io.mcp.server.McpSyncServer;
import io.mcp.server.tool.ToolResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class McpServerTest {

    private McpSyncServer syncServer;
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        McpServer server = createTestServer();
        syncServer = server.toSyncServer();
        objectMapper = new ObjectMapper();
    }

    private McpServer createTestServer() {
        // Same setup as main application
        McpServer server = McpServerBuilder.builder()
            .serverInfo("test-server", "1.0.0")
            .capabilities(cap -> cap.tools(true))
            .build();

        // Register handlers
        ToolHandlers.register(server);

        return server;
    }

    @Test
    void testGreetTool() {
        ObjectNode args = objectMapper.createObjectNode();
        args.put("name", "Java");

        ToolResponse response = syncServer.callTool("greet", args);

        assertFalse(response.isError());
        assertEquals(1, response.getContent().size());
        assertTrue(response.getContent().get(0).getText().contains("Java"));
    }

    @Test
    void testCalculateTool() {
        ObjectNode args = objectMapper.createObjectNode();
        args.put("operation", "add");
        args.put("a", 5);
        args.put("b", 3);

        ToolResponse response = syncServer.callTool("calculate", args);

        assertFalse(response.isError());
        assertTrue(response.getContent().get(0).getText().contains("8"));
    }

    @Test
    void testDivideByZero() {
        ObjectNode args = objectMapper.createObjectNode();
        args.put("operation", "divide");
        args.put("a", 10);
        args.put("b", 0);

        ToolResponse response = syncServer.callTool("calculate", args);

        assertTrue(response.isError());
    }
}
```

## README.md Template

````markdown
# My MCP Server

A Model Context Protocol server built with Java and the official MCP Java SDK.

## Features

- Tools: greet, calculate
- Resources: example data, configuration
- Prompts: code-review
- Reactive Streams with Project Reactor
- Structured logging with SLF4J
- Full test coverage

## Requirements

- Java 17 or later
- Maven 3.6+ or Gradle 7+

## Build

### Maven
```bash
mvn clean package
```

### Gradle
```bash
./gradlew build
```

## Run

### Maven
```bash
java -jar target/my-mcp-server-1.0.0.jar
```

### Gradle
```bash
./gradlew run
```

## Testing

### Maven
```bash
mvn test
```

### Gradle
```bash
./gradlew test
```

## Integration with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "java",
      "args": ["-jar", "/path/to/my-mcp-server-1.0.0.jar"]
    }
  }
}
```

## License

MIT
````

## Generation Instructions

1. **Ask for project name and package **
2. **Choose build tool ** (Maven or Gradle)
3. **Generate all files ** with proper package structure
4. **Use Reactive Streams ** for async handlers
5. **Include comprehensive logging ** with SLF4J
6. **Add tests ** for all handlers
7. **Follow Java conventions ** (camelCase, PascalCase)
8. **Include error handling ** with proper responses
9. **Document public APIs ** with Javadoc
10. **Provide both sync and async ** examples

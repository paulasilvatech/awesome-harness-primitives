---
paths:
  - "**/*.rb"
  - "**/Gemfile"
  - "**/*.gemspec"
  - "**/Rakefile"
---

<!-- Generated from harness/github-copilot/instructions/ruby-mcp-server.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Ruby MCP server conventions for SDK setup, tools, resources, prompts, transports, context, configuration, responses, notifications, testing, and clients.

# Ruby MCP Server Conventions — Official SDK

This file applies to Ruby MCP server code, Gemfiles, gemspecs, and Rakefiles matched by the `applyTo` globs. It is authoritative for using the official `mcp` Ruby SDK to define servers, tools, resources, prompts, transports, server context, configuration, structured responses, custom methods, notifications, resource templates, error handling, tests, and clients; application security policy, deployment topology, and organization-wide Ruby style rules win when they are stricter.

## Dependency and Server Initialization

Depend on the official MCP Ruby SDK through the application bundle:

```ruby
gem 'mcp'
```

Keep dependency installation reproducible through Bundler:

```bash
bundle install
```

Initialize each server with an explicit name and version:

```ruby
require 'mcp'

server = MCP::Server.new(
  name: 'my_server',
  version: '1.0.0'
)
```

## Adding Tools

Define tools using classes or blocks:

### Tool as Class

```ruby
class GreetTool < MCP::Tool
  tool_name 'greet'
  description 'Generate a greeting message'
  
  input_schema(
    properties: {
      name: { type: 'string', description: 'Name to greet' }
    },
    required: ['name']
  )
  
  output_schema(
    properties: {
      message: { type: 'string' },
      timestamp: { type: 'string', format: 'date-time' }
    },
    required: ['message']
  )
  
  annotations(
    read_only_hint: true,
    idempotent_hint: true
  )
  
  def self.call(name:, server_context:)
    MCP::Tool::Response.new([{
      type: 'text',
      text: "Hello, #{name}! Welcome to MCP."
    }], structured_content: {
      message: "Hello, #{name}!",
      timestamp: Time.now.iso8601
    })
  end
end

server = MCP::Server.new(
  name: 'my_server',
  tools: [GreetTool]
)
```

### Tool with Block

```ruby
server.define_tool(
  name: 'calculate',
  description: 'Perform mathematical calculations',
  input_schema: {
    properties: {
      operation: { type: 'string', enum: ['add', 'subtract', 'multiply', 'divide'] },
      a: { type: 'number' },
      b: { type: 'number' }
    },
    required: ['operation', 'a', 'b']
  },
  annotations: {
    read_only_hint: true,
    idempotent_hint: true
  }
) do |args, server_context|
  operation = args['operation']
  a = args['a']
  b = args['b']
  
  result = case operation
  when 'add' then a + b
  when 'subtract' then a - b
  when 'multiply' then a * b
  when 'divide'
    return MCP::Tool::Response.new([{ type: 'text', text: 'Division by zero' }], is_error: true) if b == 0
    a / b
  else
    return MCP::Tool::Response.new([{ type: 'text', text: "Unknown operation: #{operation}" }], is_error: true)
  end
  
  MCP::Tool::Response.new([{ type: 'text', text: "Result: #{result}" }])
end
```

## Adding Resources

Define resources for data access:

```ruby
# Register resources
resource = MCP::Resource.new(
  uri: 'resource://data/example',
  name: 'example-data',
  description: 'Example resource data',
  mime_type: 'application/json'
)

server = MCP::Server.new(
  name: 'my_server',
  resources: [resource]
)

# Define read handler
server.resources_read_handler do |params|
  case params[:uri]
  when 'resource://data/example'
    [{
      uri: params[:uri],
      mimeType: 'application/json',
      text: { message: 'Example data', timestamp: Time.now }.to_json
    }]
  else
    raise "Unknown resource: #{params[:uri]}"
  end
end
```

## Adding Prompts

Define prompt templates:

### Prompt as Class

```ruby
class CodeReviewPrompt < MCP::Prompt
  prompt_name 'code_review'
  description 'Generate a code review prompt'
  
  arguments [
    MCP::Prompt::Argument.new(
      name: 'language',
      description: 'Programming language',
      required: true
    ),
    MCP::Prompt::Argument.new(
      name: 'focus',
      description: 'Review focus area',
      required: false
    )
  ]
  
  def self.template(args, server_context:)
    language = args['language'] || 'Ruby'
    focus = args['focus'] || 'general quality'
    
    MCP::Prompt::Result.new(
      description: "Code review for #{language} with focus on #{focus}",
      messages: [
        MCP::Prompt::Message.new(
          role: 'user',
          content: MCP::Content::Text.new("Please review this #{language} code with focus on #{focus}.")
        ),
        MCP::Prompt::Message.new(
          role: 'assistant',
          content: MCP::Content::Text.new("I'll review the code focusing on #{focus}. Please share the code.")
        )
      ]
    )
  end
end

server = MCP::Server.new(
  name: 'my_server',
  prompts: [CodeReviewPrompt]
)
```

### Prompt with Block

```ruby
server.define_prompt(
  name: 'analyze',
  description: 'Analyze a topic',
  arguments: [
    MCP::Prompt::Argument.new(name: 'topic', description: 'Topic to analyze', required: true),
    MCP::Prompt::Argument.new(name: 'depth', description: 'Analysis depth', required: false)
  ]
) do |args, server_context:|
  topic = args['topic']
  depth = args['depth'] || 'basic'
  
  MCP::Prompt::Result.new(
    description: "Analysis of #{topic} at #{depth} level",
    messages: [
      MCP::Prompt::Message.new(
        role: 'user',
        content: MCP::Content::Text.new("Please analyze: #{topic}")
      ),
      MCP::Prompt::Message.new(
        role: 'assistant',
        content: MCP::Content::Text.new("I'll provide a #{depth} analysis of #{topic}")
      )
    ]
  )
end
```

## Transport Configuration

### Stdio Transport

For local command-line applications:

```ruby
require 'mcp'

server = MCP::Server.new(
  name: 'my_server',
  tools: [MyTool]
)

transport = MCP::Server::Transports::StdioTransport.new(server)
transport.open
```

### HTTP Transport (Rails)

For Rails applications:

```ruby
class McpController < ApplicationController
  def index
    server = MCP::Server.new(
      name: 'rails_server',
      version: '1.0.0',
      tools: [SomeTool],
      prompts: [MyPrompt],
      server_context: { user_id: current_user.id }
    )
    
    render json: server.handle_json(request.body.read)
  end
end
```

### Streamable HTTP Transport

For Server-Sent Events:

```ruby
server = MCP::Server.new(name: 'my_server')
transport = MCP::Server::Transports::StreamableHTTPTransport.new(server)
server.transport = transport

# When tools change, notify clients
server.define_tool(name: 'new_tool') { |**args| { result: 'ok' } }
server.notify_tools_list_changed
```

## Server Context

Pass contextual information to tools and prompts:

```ruby
server = MCP::Server.new(
  name: 'my_server',
  tools: [AuthenticatedTool],
  server_context: {
    user_id: current_user.id,
    request_id: request.uuid,
    auth_token: session[:token]
  }
)

class AuthenticatedTool < MCP::Tool
  def self.call(query:, server_context:)
    user_id = server_context[:user_id]
    # Use user_id for authorization
    
    MCP::Tool::Response.new([{ type: 'text', text: 'Authorized' }])
  end
end
```

## Configuration

### Exception Reporting

Configure exception reporting:

```ruby
MCP.configure do |config|
  config.exception_reporter = ->(exception, server_context) {
    # Report to your error tracking service
    Bugsnag.notify(exception) do |report|
      report.add_metadata(:mcp, server_context)
    end
  }
end
```

### Instrumentation

Monitor MCP server performance:

```ruby
MCP.configure do |config|
  config.instrumentation_callback = ->(data) {
    # Log instrumentation data
    Rails.logger.info("MCP: #{data.inspect}")
    
    # Or send to metrics service
    StatsD.timing("mcp.#{data[:method]}.duration", data[:duration])
    StatsD.increment("mcp.#{data[:method]}.count")
  }
end
```

The instrumentation data includes:
- `method`: Protocol method called (e.g., "tools/call")
- `tool_name`: Name of tool called
- `prompt_name`: Name of prompt called
- `resource_uri`: URI of resource called
- `error`: Error code if lookup failed
- `duration`: Duration in seconds

### Protocol Version

Override the protocol version:

```ruby
configuration = MCP::Configuration.new(protocol_version: '2025-06-18')
server = MCP::Server.new(name: 'my_server', configuration: configuration)
```

## Tool Annotations

Provide metadata about tool behavior:

```ruby
class DataTool < MCP::Tool
  annotations(
    read_only_hint: true,      # Tool only reads data
    destructive_hint: false,   # Tool doesn't destroy data
    idempotent_hint: true,     # Same input = same output
    open_world_hint: false     # Tool operates in closed context
  )
  
  def self.call(**args, server_context:)
    # Implementation
  end
end
```

## Tool Output Schemas

Define expected output structure:

```ruby
class WeatherTool < MCP::Tool
  output_schema(
    properties: {
      temperature: { type: 'number' },
      condition: { type: 'string' },
      humidity: { type: 'integer' }
    },
    required: ['temperature', 'condition']
  )
  
  def self.call(location:, server_context:)
    weather_data = {
      temperature: 72.5,
      condition: 'sunny',
      humidity: 45
    }
    
    # Validate against schema
    output_schema.validate_result(weather_data)
    
    MCP::Tool::Response.new(
      [{ type: 'text', text: weather_data.to_json }],
      structured_content: weather_data
    )
  end
end
```

## Structured Content in Responses

Return structured data with text:

```ruby
class APITool < MCP::Tool
  def self.call(endpoint:, server_context:)
    api_data = call_api(endpoint)
    
    MCP::Tool::Response.new(
      [{ type: 'text', text: api_data.to_json }],
      structured_content: api_data
    )
  end
end
```

## Custom Methods

Define custom JSON-RPC methods:

```ruby
server = MCP::Server.new(name: 'my_server')

# Custom method with result
server.define_custom_method(method_name: 'add') do |params|
  params[:a] + params[:b]
end

# Custom notification (returns nil)
server.define_custom_method(method_name: 'notify') do |params|
  puts "Notification: #{params[:message]}"
  nil
end
```

## Notifications

Send list change notifications:

```ruby
server = MCP::Server.new(name: 'my_server')
transport = MCP::Server::Transports::StreamableHTTPTransport.new(server)
server.transport = transport

# Notify when tools change
server.define_tool(name: 'new_tool') { |**args| { result: 'ok' } }
server.notify_tools_list_changed

# Notify when prompts change
server.define_prompt(name: 'new_prompt') { |args, **_| MCP::Prompt::Result.new(...) }
server.notify_prompts_list_changed

# Notify when resources change
server.notify_resources_list_changed
```

## Resource Templates

Define dynamic resources with URI templates:

```ruby
resource_template = MCP::ResourceTemplate.new(
  uri_template: 'users://{user_id}/profile',
  name: 'user-profile',
  description: 'User profile data',
  mime_type: 'application/json'
)

server = MCP::Server.new(
  name: 'my_server',
  resource_templates: [resource_template]
)
```

## Error Handling

Handle errors properly in tools:

```ruby
class RiskyTool < MCP::Tool
  def self.call(data:, server_context:)
    begin
      result = risky_operation(data)
      MCP::Tool::Response.new([{ type: 'text', text: result }])
    rescue ValidationError => e
      MCP::Tool::Response.new(
        [{ type: 'text', text: "Invalid input: #{e.message}" }],
        is_error: true
      )
    rescue => e
      # Will be caught and reported by exception_reporter
      raise
    end
  end
end
```

## Testing

Write tests for your MCP server:

```ruby
require 'minitest/autorun'
require 'mcp'

class MyToolTest < Minitest::Test
  def test_greet_tool
    response = GreetTool.call(name: 'Ruby', server_context: {})
    
    assert_equal 1, response.content.length
    assert_match(/Ruby/, response.content.first[:text])
    refute response.is_error
  end
  
  def test_invalid_input
    response = CalculateTool.call(operation: 'divide', a: 10, b: 0, server_context: {})
    
    assert response.is_error
  end
end
```

## Client Usage

Build MCP clients to connect to servers:

```ruby
require 'mcp'
require 'faraday'

# HTTP transport
http_transport = MCP::Client::HTTP.new(
  url: 'https://api.example.com/mcp',
  headers: { 'Authorization' => "Bearer #{token}" }
)

client = MCP::Client.new(transport: http_transport)

# List tools
tools = client.tools
tools.each do |tool|
  puts "Tool: #{tool.name}"
  puts "Description: #{tool.description}"
end

# Call a tool
response = client.call_tool(
  tool: tools.first,
  arguments: { message: 'Hello, world!' }
)
```

## Common Patterns

### Authenticated Tool

```ruby
class AuthenticatedTool < MCP::Tool
  def self.call(**args, server_context:)
    user_id = server_context[:user_id]
    raise 'Unauthorized' unless user_id
    
    # Process authenticated request
    MCP::Tool::Response.new([{ type: 'text', text: 'Success' }])
  end
end
```

### Paginated Resource

```ruby
server.resources_read_handler do |params|
  uri = params[:uri]
  page = params[:page] || 1
  
  data = fetch_paginated_data(page)
  
  [{
    uri: uri,
    mimeType: 'application/json',
    text: data.to_json
  }]
end
```

### Dynamic Prompt

```ruby
class DynamicPrompt < MCP::Prompt
  def self.template(args, server_context:)
    user_id = server_context[:user_id]
    user_data = User.find(user_id)
    
    MCP::Prompt::Result.new(
      description: "Personalized prompt for #{user_data.name}",
      messages: generate_messages_for(user_data)
    )
  end
end
```
## Good / Bad Examples

The examples below illustrate a tool that declares schemas, annotations, structured content, and explicit error behavior.

**Good:**

```ruby
class LookupTool < MCP::Tool
  tool_name 'lookup'
  description 'Look up a record by identifier'

  input_schema(
    properties: { id: { type: 'string' } },
    required: ['id']
  )

  output_schema(
    properties: { id: { type: 'string' }, status: { type: 'string' } },
    required: ['id', 'status']
  )

  annotations(read_only_hint: true, idempotent_hint: true)

  def self.call(id:, server_context:)
    record = Repository.fetch_for_user(id, server_context[:user_id])
    body = { id: record.id, status: record.status }
    output_schema.validate_result(body)
    MCP::Tool::Response.new([{ type: 'text', text: body.to_json }], structured_content: body)
  rescue Repository::NotFound => e
    MCP::Tool::Response.new([{ type: 'text', text: e.message }], is_error: true)
  end
end
```

Why: The tool is testable, describes its contract, uses `server_context` for authorization context, validates structured output, and returns `is_error: true` for expected domain failures.

**Bad:**

```ruby
server.define_tool(name: 'lookup') do |args|
  data = Repository.fetch(args['id'])
  data.to_json
end
```

Why: The tool omits schemas, annotations, `server_context`, structured content, and explicit error handling, so clients cannot reason about behavior or failure shape.

## Conventions

| Rule | Rationale |
| --- | --- |
| Depend on `gem 'mcp'` and install through `bundle install` | The official SDK and Bundler keep server code reproducible |
| Initialize `MCP::Server.new` with explicit `name` and `version` where the server is published | Clients and logs need stable identity and compatibility information |
| Use `MCP::Tool` classes for complex tools and `server.define_tool` blocks only for simple tools | Classes are easier to test, reuse, and document; blocks keep trivial behavior compact |
| Define `input/output` schemas through `input_schema`, `output_schema`, and `annotations` for every tool that has a stable contract | Clients use schemas and hints to validate inputs, interpret outputs, and assess side effects |
| Return `MCP::Tool::Response` with `structured_content` when data has structure | Text-only JSON forces clients to parse display content and loses type expectations |
| Use `MCP::Resource`, `resources_read_handler`, and `MCP::ResourceTemplate` for readable data surfaces | Resources keep data access separate from actions and support dynamic URI patterns |
| Define prompts with `MCP::Prompt`, `MCP::Prompt::Argument`, `MCP::Prompt::Result`, `MCP::Prompt::Message`, and `MCP::Content::Text` | Prompt contracts stay discoverable and typed for MCP clients |
| Choose `MCP::Server::Transports::StdioTransport`, Rails `handle_json`, or `MCP::Server::Transports::StreamableHTTPTransport` based on host requirements | Transport choice determines process lifetime, HTTP behavior, and notification support |
| Pass request data through `server_context` and avoid global request state | Tools and prompts need authorization, request IDs, and user context without hidden coupling |
| Configure `exception_reporter` and `instrumentation_callback` for production servers | Errors and latency need centralized monitoring |
| Send `notify_tools_list_changed`, `notify_prompts_list_changed`, and `notify_resources_list_changed` when capabilities change | Connected clients need fresh capability lists |
| Validate inputs, handle expected failures with `is_error: true`, and re-raise unexpected exceptions | Users receive actionable errors while monitoring still sees defects |
| Test tool calls, content length, text matches, and `is_error` with Minitest or the project test runner | MCP behavior should be verified without a live client |
| Follow Ruby conventions such as `snake_case` names and consistent indentation | MCP code remains idiomatic and maintainable |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use classes for complex tools | Hide complex behavior in anonymous blocks |
| Define input and output schemas for stable tool contracts | Accept arbitrary parameters without validation |
| Add `read_only_hint`, `destructive_hint`, `idempotent_hint`, and `open_world_hint` accurately | Mark mutating or external tools as read-only or closed-world |
| Include both text content and `structured_content` for structured results | Return only a JSON string when clients need typed data |
| Use `server_context` for `user_id`, `request_id`, and authorization context | Read authentication state from globals inside tools |
| Configure exception reporting and instrumentation | Let production errors and latency disappear into process logs |
| Use notifications after changing tools, prompts, or resources | Leave connected clients with stale capability metadata |
| Return `is_error: true` for expected validation or domain failures | Raise every user-facing error as an unexpected exception |
| Test tools and invalid input paths directly | Rely only on manual client testing |
| Use `MCP::Client::HTTP` and `MCP::Client.new` for Ruby clients | Hardcode protocol calls without SDK abstractions |

## Checklist Before Opening a PR

- [ ] The server depends on `gem 'mcp'` and Bundler-managed installation remains reproducible.
- [ ] `MCP::Server.new` declares stable identity and registers the intended tools, resources, prompts, templates, and context.
- [ ] Tools define schemas, annotations, structured content, and expected error responses.
- [ ] Resources, resource templates, and prompts expose typed names, arguments, MIME types, and URI patterns.
- [ ] Stdio, Rails HTTP, Streamable HTTP, or client transports match the deployment surface.
- [ ] `server_context` carries request and authentication context without leaking secrets into responses or logs.
- [ ] `exception_reporter`, `instrumentation_callback`, custom methods, and list-change notifications are configured where production behavior requires them.
- [ ] Tests cover successful calls, invalid input, `is_error`, content shape, and authorization-sensitive behavior.
- [ ] Ruby naming and indentation conventions are followed.

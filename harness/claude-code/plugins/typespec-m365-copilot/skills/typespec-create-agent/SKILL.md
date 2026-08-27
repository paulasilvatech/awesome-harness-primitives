---
name: typespec-create-agent
description: >-
  Generate a complete TypeSpec declarative agent for Microsoft 365 Copilot with agent metadata,
  instructions, capabilities, and conversation starters. Use when the user asks to create a
  TypeSpec declarative agent, main.tsp, Microsoft 365 Copilot agent, or TypeSpec M365 capability
  scaffold.
---

<!-- Generated from harness/github-copilot/plugins/typespec-m365-copilot/skills/typespec-create-agent/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create TypeSpec declarative agent

GitHub Copilot uses this skill to generate a `main.tsp` file for a Microsoft 365 Copilot declarative agent by translating the user's purpose, knowledge sources, and interaction examples into TypeSpec decorators and scoped AgentCapabilities operations.

## When to invoke

- "Create a TypeSpec declarative agent."
- "Generate main.tsp for a Microsoft 365 Copilot agent."
- "Add WebSearch and OneDrive capabilities to an agent."
- "Scaffold a TypeSpec M365 Copilot declarative agent."

## Inputs

Ask or infer these facts before writing `main.tsp`:

| Input | Required | Rule |
| --- | --- | --- |
| Agent purpose and role | Yes | Convert to a descriptive role-based name and behavior. |
| Capabilities needed | Yes | Include only capabilities the agent actually needs. |
| Knowledge sources | Conditional | Capture sites, folders, Teams areas, connectors, Dataverse tables, or meeting scope when relevant. |
| Typical user interactions | Yes | Use them to write 2-4 diverse conversation starters. |
| Limits and safety behavior | Yes | Put refusals, escalation, and boundaries in `@instructions`. |

## TypeSpec structure

Generate one `main.tsp` file with these pieces:

| Part | TypeSpec construct | Constraint |
| --- | --- | --- |
| Imports | `import "@typespec/http";`, `import "@typespec/openapi3";`, `import "@microsoft/typespec-m365-copilot";` | Keep imports at the top. |
| Usings | `using TypeSpec.Http;`, `using TypeSpec.M365.Copilot.Agents;` | Required for agent decorators and capabilities. |
| Agent declaration | `@agent({ name, description })` | Name is 100 characters or less; description is 1,000 characters or less. |
| Instructions | `@instructions("""...""")` | Under 8,000 characters; define role, expertise, personality, do and do not rules. |
| Conversation starters | `@conversationStarter(#{ title, text })` | Include 2-4 starters with diverse user intents. |
| Namespace | `namespace [AgentName] { ... }` | Use a valid TypeSpec identifier, usually PascalCase without spaces. |
| Capabilities | `op capabilityName is AgentCapabilities.[CapabilityType]<[Parameters]>;` | Scope URLs, folders, and content where possible. |

## Capability selection

| Capability | Use when | Scoping guidance |
| --- | --- | --- |
| `WebSearch` | The agent needs public web content. | Add site scoping when the domain is known. |
| `OneDriveAndSharePoint` | The agent answers from user or organization documents. | Filter by URL, folder, or site when possible. |
| `TeamsMessages` | The agent needs Teams channels or chats. | Limit to relevant channel/chat contexts. |
| `Email` | Mailbox content is part of the task. | Prefer folder or sender filters over broad mailbox access. |
| `People` | The agent searches organization people or roles. | Use for expertise and directory lookup, not document search. |
| `CodeInterpreter` | The agent needs Python analysis, calculation, or file processing. | Describe data boundaries in instructions. |
| `GraphicArt` | The agent generates images. | Include style and brand limitations. |
| `GraphConnectors` | The agent uses Microsoft 365 Copilot connector content. | Name the connector content domain. |
| `Dataverse` | The agent reads Dataverse data. | Scope to relevant tables or business objects. |
| `Meetings` | The agent uses meeting content. | State whether summaries, transcripts, or action items are expected. |

## Template

```typespec
import "@typespec/http";
import "@typespec/openapi3";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;
using TypeSpec.M365.Copilot.Agents;

@agent({
  name: "[Agent Name]",
  description: "[Agent Description]"
})
@instructions("""
  [Detailed instructions about agent behavior, role, and guidelines]
""")
@conversationStarter(#{
  title: "[Starter Title 1]",
  text: "[Example query 1]"
})
@conversationStarter(#{
  title: "[Starter Title 2]",
  text: "[Example query 2]"
})
namespace [AgentName] {
  op capabilityName is AgentCapabilities.[CapabilityType]<[Parameters]>;
}
```

## Authoring rules

- Use descriptive role-based agent names such as `Customer Support Assistant` or `Research Helper`.
- Write instructions in second person: "You are...".
- Be specific about expertise, limitations, escalation, data sources, and unsupported tasks.
- Include 2-4 conversation starters that showcase different capabilities rather than duplicates.
- Use triple-quoted strings for multi-line instructions.
- Scope capabilities for performance and least privilege.
- Do not include broad capabilities just because they exist.

## Gotchas

- **Agent names and namespace identifiers are different**: the display name may contain spaces, but the namespace must be a valid TypeSpec identifier.
- **Broad knowledge sources reduce quality**: scoped `WebSearch`, `OneDriveAndSharePoint`, `TeamsMessages`, and `Email` capabilities are usually better than unbounded access.
- **Conversation starters are examples, not tests**: they should be realistic user prompts and cover the agent's primary use cases.

## Output template

```markdown
## TypeSpec declarative agent

**Status:** generated | needs input | blocked
**File:** `main.tsp`
**Agent name:** <display name>
**Namespace:** <TypeSpec namespace>

### Capabilities
| Operation | AgentCapabilities type | Scope |
| --- | --- | --- |
| `<operation>` | `<CapabilityType>` | `<parameters or none>` |

### Conversation starters
- `<title>` — `<text>`

### Validation
- Name length: <pass/fail>
- Description length: <pass/fail>
- Instructions length: <pass/fail>
```

## Quality gate

- [ ] `main.tsp` includes the three required imports and two required `using` statements.
- [ ] `@agent` has a descriptive name no longer than 100 characters and description no longer than 1,000 characters.
- [ ] `@instructions` defines role, expertise, personality, allowed behavior, and limits in fewer than 8,000 characters.
- [ ] The file includes 2-4 diverse `@conversationStarter` decorators.
- [ ] Capabilities are limited to actual user needs and scoped when possible.
- [ ] The namespace is a valid TypeSpec identifier.

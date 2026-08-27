---
name: typespec-api-operations
description: >-
  Add RESTful GET, POST, PATCH, and DELETE operations to a TypeSpec API plugin for Microsoft 365
  plugin for GitHub Copilot with routing, parameters, models, confirmations, adaptive cards, and
  testing prompts. Use when asked to add TypeSpec API operations, CRUD endpoints,
  @route/@get/@post/@patch/@delete handlers, or GitHub Copilot plugin actions.
---

<!-- Generated from harness/github-copilot/skills/typespec-api-operations/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# TypeSpec API operations

Add RESTful operations to an existing TypeSpec API plugin by selecting the correct verb, route, parameter decorators, request/response models, confirmation capability, and optional adaptive card output.

## When to invoke

- "Add TypeSpec API operations for this plugin."
- "Create GET, POST, PATCH, and DELETE operations in TypeSpec."
- "Add a GitHub Copilot plugin CRUD endpoint with @route and @card."
- "Why is my TypeSpec parameter not showing in GitHub Copilot?"
- "Add confirmations and adaptive cards to these operations."

## Operation patterns

| Operation | TypeSpec pattern | Use when | Required decorators |
| --- | --- | --- | --- |
| List | `@route("/items") @get op listItems(): Item[];` | Return all items. | `@route`, `@get` |
| Filtered list | `@get op listItems(@query userId?: integer): Item[];` | Filter with optional query parameters. | `@query` on each filter |
| Get one | `@route("/items/{id}") @get op getItem(@path id: integer): Item;` | Retrieve one resource by route ID. | `@path` matching `{id}` |
| Create | `@route("/items") @post op createItem(@body item: CreateItemRequest): Item;` | Create a resource from a body model. | `@body` |
| Update | `@route("/items/{id}") @patch op updateItem(@path id: integer, @body item: UpdateItemRequest): Item;` | Partially update an existing resource. | `@path`, `@body` |
| Delete | `@route("/items/{id}") @delete op deleteItem(@path id: integer): void;` | Delete a resource. | `@path`, `@delete` |

Use parameter names such as `userId` consistently, and preserve status unions like `"active" | "completed"`. Use adaptive-card conditional syntax `${if(..., ..., 'N/A')}` when documenting generic data binding.

Use RESTful conventions: `GET /items`, `GET /items/{id}`, `POST /items`, `PATCH /items/{id}`, and `DELETE /items/{id}`. Group related operations in the same namespace and use nested routes only for hierarchical resources.

## Models, parameters, and responses

```typespec
@service
@server("https://api.example.com")
@actions(#{
  nameForHuman: "Items API",
  descriptionForHuman: "Manage items",
  descriptionForModel: "Read, create, update, and delete items"
})
namespace ItemsAPI {
  model Item {
    @visibility(Lifecycle.Read)
    id: integer;
    userId: integer;
    title: string;
    description?: string;
    status: "active" | "completed" | "archived";
    @format("date-time")
    createdAt: utcDateTime;
    @format("date-time")
    updatedAt?: utcDateTime;
  }

  model CreateItemRequest {
    userId: integer;
    title: string;
    description?: string;
  }

  model UpdateItemRequest {
    title?: string;
    description?: string;
    status?: "active" | "completed" | "archived";
  }

  model ItemList {
    items: Item[];
    total: integer;
    hasMore: boolean;
  }

  model DeleteResponse {
    success: boolean;
    message: string;
    deletedId: integer;
  }

  model ErrorResponse {
    error: {
      code: string;
      message: string;
      details?: string[];
    };
  }
}
```

| Need | Pattern | Notes |
| --- | --- | --- |
| Read-only response field | `@visibility(Lifecycle.Read)` | Use for `id` and server-generated fields that should not be writable. |
| Date field | `@format("date-time")` with `utcDateTime` | Use for `createdAt` and `updatedAt`. |
| Enum-like status | `"active" | "completed" | "archived"` | Prefer union types for fixed values. |
| Optional field | `description?: string` | Make optional fields explicit with `?`. |
| Header parameter | `@header("X-API-Version") apiVersion?: string` | Use for version or tenant headers. |
| Error response | `Item | ErrorResponse` | Document expected error shape. |

## Adaptive cards and confirmations

Attach cards to read operations when GitHub Copilot should render structured results. Keep cards focused, test data binding with actual API responses, use conditional rendering such as `${if(description, description, 'N/A')}`, and include action buttons only for common next steps.

```typespec
@route("/items")
@card(#{
  dataPath: "$",
  title: "$.title",
  file: "item-card.json"
})
@get op listItems(@query userId?: integer): Item[];
```

Create `appPackage/item-card.json`:

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "Container",
      "$data": "${$root}",
      "items": [
        { "type": "TextBlock", "text": "**${if(title, title, 'N/A')}**", "wrap": true },
        { "type": "TextBlock", "text": "${if(description, description, 'N/A')}", "wrap": true }
      ]
    }
  ],
  "actions": [
    { "type": "Action.OpenUrl", "title": "View Details", "url": "https://example.com/items/${id}" }
  ]
}
```

Add confirmations to destructive operations and any operation that changes important data. Show key details in the confirmation body and state irreversible consequences in text instead of relying on an emoji.

```typespec
@route("/items/{id}")
@patch
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "Update Item",
    body: """
    Updating item #{{ function.parameters.id }}:
      * **Title**: {{ function.parameters.item.title }}
      * **Status**: {{ function.parameters.item.status }}
    """
  }
})
op updateItem(@path id: integer, @body item: UpdateItemRequest): Item;

@route("/items/{id}")
@delete
@capabilities(#{
  confirmation: #{
    type: "AdaptiveCard",
    title: "Delete Item",
    body: """
    Are you sure you want to delete item #{{ function.parameters.id }}?
    This action cannot be undone.
    """
  }
})
op deleteItem(@path id: integer): void;
```

## Complete CRUD skeleton

```typespec
namespace ItemsAPI {
  @route("/items")
  @card(#{ dataPath: "$", title: "$.title", file: "item-card.json" })
  @get op listItems(
    @query userId?: integer,
    @query status?: "active" | "completed" | "archived",
    @query limit?: integer,
    @query offset?: integer
  ): ItemList;

  @route("/items/{id}")
  @card(#{ dataPath: "$", title: "$.title", file: "item-card.json" })
  @get op getItem(@path id: integer): Item | ErrorResponse;

  @route("/items")
  @post
  @capabilities(#{ confirmation: #{ type: "AdaptiveCard", title: "Create Item", body: "Creating: **{{ function.parameters.item.title }}**" } })
  op createItem(@body item: CreateItemRequest): Item;

  @route("/items/{id}")
  @patch
  @capabilities(#{ confirmation: #{ type: "AdaptiveCard", title: "Update Item", body: "Updating item #{{ function.parameters.id }}" } })
  op updateItem(@path id: integer, @body item: UpdateItemRequest): Item;

  @route("/items/{id}")
  @delete
  @capabilities(#{ confirmation: #{ type: "AdaptiveCard", title: "Delete Item", body: "Delete item #{{ function.parameters.id }}?" } })
  op deleteItem(@path id: integer): DeleteResponse;
}
```

## Testing prompts

| Operation | Prompts |
| --- | --- |
| GET | "List all items and show them in a table"; "Show me items for user ID 1"; "Get the details of item 42" |
| POST | "Create a new item with title 'My Task' for user 1"; "Add an item: title 'New Feature', description 'Add login'" |
| PATCH | "Update item 10 with title 'Updated Title'"; "Change the status of item 5 to completed" |
| DELETE | "Delete item 99"; "Remove the item with ID 15" |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Parameter not showing in GitHub Copilot | Parameter lacks `@query`, `@path`, or `@body` | Add the correct decorator and make path parameter names match the route. |
| Adaptive card not rendering | Wrong `@card` file path or invalid JSON | Verify `file: "item-card.json"`, check `appPackage/item-card.json`, and validate JSON syntax. |
| Confirmation not appearing | `@capabilities` confirmation object malformed | Use `confirmation: #{ type: "AdaptiveCard", title: "...", body: "..." }`. |
| Model property not appearing in response | Field visibility is wrong | Add `@visibility(Lifecycle.Read)` for read-only response fields or remove it if writable. |

## Output template

```markdown
## TypeSpec API operations - <resource>

**Status:** complete | needs validation | blocked
**Resource:** <resource name>

### Operations added
| Verb | Route | Operation | Request model | Response model | Card/confirmation |
| --- | --- | --- | --- | --- | --- |
| GET | `/items` | `listItems` | none | `ItemList` | `@card` |
| POST | `/items` | `createItem` | `CreateItemRequest` | `Item` | confirmation |

### Files to update
- `<typespec file>`: <operations/models added>
- `appPackage/item-card.json`: <card added or not needed>

### Test prompts
- `<prompt>`

### Validation
- Parameter decorators: pass | fail
- REST routes: pass | fail
- Confirmations for PATCH/DELETE: pass | fail
- Adaptive card JSON: pass | fail | not used
```

## Quality gate

- [ ] Each operation uses the correct HTTP decorator: `@get`, `@post`, `@patch`, or `@delete`.
- [ ] Every path token in `@route` has a matching `@path` parameter.
- [ ] Filters use `@query`; request payloads use `@body`; headers use `@header`.
- [ ] Models use `?`, union types, `@format("date-time")`, and `@visibility(Lifecycle.Read)` where appropriate.
- [ ] PATCH and DELETE include confirmations with meaningful details.
- [ ] Any `@card` file exists under `appPackage/` and uses valid Adaptive Card JSON.
- [ ] Testing prompts cover GET, POST, PATCH, and DELETE when those operations are added.
- [ ] Output follows the `## Output template` exactly.

## References

- [Adaptive Card schema](http://adaptivecards.io/schemas/adaptive-card.json)
- [Example API endpoint](https://api.example.com)
- [Example item URL](https://example.com/items/${id})

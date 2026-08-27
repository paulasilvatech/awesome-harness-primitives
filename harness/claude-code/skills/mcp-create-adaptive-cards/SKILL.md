---
name: mcp-create-adaptive-cards
description: >-
  Create Adaptive Card response templates and response_semantics for MCP-based API plugins in
  Microsoft 365 Copilot. Use when presenting MCP tool or API data with visual Adaptive Cards,
  citation mappings, static or dynamic card templates, JSONPath data paths, or responsive card
  layouts.
---

<!-- Generated from harness/github-copilot/skills/mcp-create-adaptive-cards/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# MCP create Adaptive Cards

Adds Adaptive Card response templates to MCP-based API plugins so Microsoft 365 Copilot can present API data visually with citation mappings, template selection, conditional rendering, and responsive single-column layouts.

## When to invoke

- "Create an Adaptive Card for this MCP tool response."
- "Add response_semantics and citation mappings to my API plugin."
- "Present this API data as cards in Microsoft 365 Copilot."
- "Use JSONPath to map response fields into an Adaptive Card template."
- "Build static or dynamic Adaptive Card templates for different item types."

## Prerequisites and context

Gather these details before producing JSON:

1. What type of data the API returns.
2. Whether all items are the same type (static template) or different types (dynamic templates).
3. Which fields should appear in the card.
4. Whether the card needs actions such as `View Details`.
5. Whether multiple states or categories require different templates.

Read `references/card-reference-examples.md` for card type schemas, element details, complete JSON, and common snippets.

## Response semantics

| Property | Purpose | Example |
| --- | --- | --- |
| `data_path` | JSONPath query indicating where data resides in the API response. | `"data_path": "$"`, `"data_path": "$.results"`, `"data_path": "$.data.items"` |
| `properties.title` | Citation title mapping. | `"title": "$.name"` |
| `properties.subtitle` | Citation subtitle mapping. | `"subtitle": "$.description"` |
| `properties.url` | Citation URL mapping. | `"url": "$.link"` |
| `template_selector` | Property on each item that selects which template to use. | `"template_selector": "$.displayTemplate"` |

## Adaptive Card template language

```json
{
  "type": "TextBlock",
  "text": "${if(field, field, 'N/A')}"
}
```

```json
{
  "type": "TextBlock",
  "text": "${formatNumber(amount, 2)}"
}
```

```json
{
  "type": "Container",
  "$data": "${$root}",
  "items": []
}
```

```json
{
  "type": "Image",
  "url": "${imageUrl}",
  "$when": "${imageUrl != null}"
}
```

Use conditional rendering for missing fields, number formatting for amounts, `$data` to bind arrays or break to `$root`, and `$when` to hide optional images or sections.

## Responsive design criteria

| Area | Rule |
| --- | --- |
| Layout | Prefer single-column layouts for narrow Microsoft 365 Copilot viewports. |
| Width | Avoid fixed widths; use `auto` or `stretch` except for small icons and avatars. |
| Text | Set `"wrap": true` for user-visible text. |
| Image plus text | Avoid placing text and images in the same row except small icons or avatars. |
| Hubs | Validate in Teams desktop, Teams mobile, Word, PowerPoint, and contract/expand UI widths when available. |
| Actions | Keep actions sparse and map URLs through trusted response fields. |

## Procedure

1. Inspect the API response shape and choose `data_path`.
2. Map citation `properties` for title, subtitle, and URL.
3. Decide whether the card uses one static template or dynamic templates with `template_selector`.
4. Build the Adaptive Card template with safe data bindings, conditional rendering, and responsive layout.
5. Add actions only when the user requested them or the API response includes a trustworthy link.
6. Validate with representative response samples, missing optional fields, long text, narrow width, and each relevant hub.

## Progressive disclosure and bundled resources

- `references/card-reference-examples.md`: Adaptive Card schema patterns, card examples, element details, and reusable JSON snippets.

## MCP plugin vocabulary

This skill replaces legacy `api-plugin` `response-templates` prompt material with portable Skill instructions. Do not copy old prompt tool IDs such as `search/codebase` or `edit/editFiles` into skill frontmatter. Avoid `multi-column` layouts except when tested; fixed widths are acceptable only for `icons/avatars`.

## Output template

````markdown
### MCP Adaptive Card result

**Status:** template ready | needs API details | blocked
**Data path:** `<JSONPath>`
**Template mode:** static | dynamic

**response_semantics**
```json
{
  "data_path": "$.results",
  "properties": {
    "title": "$.name",
    "subtitle": "$.description",
    "url": "$.link"
  },
  "template_selector": "$.displayTemplate"
}
```

**Adaptive Card template**
```json
{
  "type": "AdaptiveCard",
  "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "text": "${if(name, name, 'N/A')}",
      "wrap": true
    }
  ]
}
```

**Validation scenarios**
- Same-type item: pass | fail
- Dynamic template item: pass | fail | not applicable
- Missing optional fields: pass | fail
- Narrow viewport: pass | fail
- Teams, Word, PowerPoint: pass | fail | not tested
````

## Quality gate

- [ ] `data_path` points to the actual item collection or response root.
- [ ] `properties.title`, `properties.subtitle`, and `properties.url` map real response fields for citations.
- [ ] Static vs dynamic template choice matches whether item types vary.
- [ ] Optional fields use `${if(...)}` or `$when` instead of rendering broken blanks.
- [ ] Numeric values use `${formatNumber(amount, 2)}` or another deliberate format.
- [ ] Layout is responsive, single-column by default, and avoids fixed widths except icons or avatars.
- [ ] Text blocks that can overflow use `"wrap": true`.
- [ ] Validation covers Teams, Word, PowerPoint, and narrow viewports when available.

## References

- [Adaptive Card Designer](https://adaptivecards.microsoft.com/designer)
- [Adaptive Card Schema](https://adaptivecards.io/schemas/adaptive-card.json)
- [Template Language](https://learn.microsoft.com/en-us/adaptive-cards/templating/language)
- [JSONPath](https://www.rfc-editor.org/rfc/rfc9535)

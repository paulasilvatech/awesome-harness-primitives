---
name: "mcp-create-adaptive-cards"
description: "Skill converted from mcp-create-adaptive-cards.prompt.md. Use this skill when the user asks for create adaptive cards for mcp plugins."
---
````prompt
---
mode: 'agent'
tools: ['changes', 'search/codebase', 'edit/editFiles', 'problems']
description: 'Add Adaptive Card response templates to MCP-based API plugins for visual data presentation in Microsoft 365 Copilot'
model: 'gpt-4.1'
tags: [mcp, adaptive-cards, m365-copilot, api-plugin, response-templates]
---

# Create Adaptive Cards for MCP Plugins

Add Adaptive Card response templates to MCP-based API plugins to enhance how data is presented visually in Microsoft 365 Copilot.

## Bundled Resources

- [Adaptive card reference and examples](references/card-reference-examples.md) — For card type schemas, element details, complete JSON, or common pattern snippets, open this reference.

## Response Semantics Properties

### data_path
JSONPath query indicating where data resides in API response:
```json
"data_path": "$"           // Root of response
"data_path": "$.results"   // In results property
"data_path": "$.data.items"// Nested path
```

### properties
Map response fields for Copilot citations:
```json
"properties": {
  "title": "$.name",            // Citation title
  "subtitle": "$.description",  // Citation subtitle
  "url": "$.link"               // Citation link
}
```

### template_selector
Property on each item indicating which template to use:
```json
"template_selector": "$.displayTemplate"
```

## Adaptive Card Template Language

### Conditional Rendering
```json
{
  "type": "TextBlock",
  "text": "${if(field, field, 'N/A')}"  // Show field or 'N/A'
}
```

### Number Formatting
```json
{
  "type": "TextBlock",
  "text": "${formatNumber(amount, 2)}"  // Two decimal places
}
```

### Data Binding
```json
{
  "type": "Container",
  "$data": "${$root}",  // Break to root context
  "items": [ ... ]
}
```

### Conditional Display
```json
{
  "type": "Image",
  "url": "${imageUrl}",
  "$when": "${imageUrl != null}"  // Only show if imageUrl exists
}
```

## Responsive Design Best Practices

### Single-Column Layouts
- Use single columns for narrow viewports
- Avoid multi-column layouts when possible
- Ensure cards work at minimum viewport width

### Flexible Widths
- Don't assign fixed widths to elements
- Use "auto" or "stretch" for width properties
- Allow elements to resize with viewport
- Fixed widths OK for icons/avatars only

### Text and Images
- Avoid placing text and images in same row
- Exception: Small icons or avatars
- Use "wrap": true for text content
- Test at various viewport widths

### Test Across Hubs
Validate cards in:
- Teams (desktop and mobile)
- Word
- PowerPoint
- Various viewport widths (contract/expand UI)

## Workflow

Ask the user:
1. What type of data does the API return?
2. Are all items the same type (static) or different types (dynamic)?
3. What fields should appear in the card?
4. Should there be actions (e.g., "View Details")?
5. Are there multiple states or categories requiring different templates?

Then generate:
- Appropriate response_semantics configuration
- Static template, dynamic templates, or both
- Proper data binding with conditional rendering
- Responsive single-column layout
- Test scenarios for validation

## Resources

- [Adaptive Card Designer](https://adaptivecards.microsoft.com/designer) - Visual design tool
- [Adaptive Card Schema](https://adaptivecards.io/schemas/adaptive-card.json) - Full schema reference
- [Template Language](https://learn.microsoft.com/en-us/adaptive-cards/templating/language) - Binding syntax guide
- [JSONPath](https://www.rfc-editor.org/rfc/rfc9535) - Path query syntax

````

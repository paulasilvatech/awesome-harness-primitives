# Adaptive card reference and examples

Moved from `../SKILL.md` for progressive disclosure. Use this reference only when the activated workflow needs the detailed material below.

## Adaptive Card Types

### Static Response Templates
Use when API always returns items of the same type and format doesn't change often.

Define in `response_semantics.static_template` in ai-plugin.json:

```json
{
  "functions": [
    {
      "name": "GetBudgets",
      "description": "Returns budget details including name and available funds",
      "capabilities": {
        "response_semantics": {
          "data_path": "$",
          "properties": {
            "title": "$.name",
            "subtitle": "$.availableFunds"
          },
          "static_template": {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.5",
            "body": [
              {
                "type": "Container",
                "$data": "${$root}",
                "items": [
                  {
                    "type": "TextBlock",
                    "text": "Name: ${if(name, name, 'N/A')}",
                    "wrap": true
                  },
                  {
                    "type": "TextBlock",
                    "text": "Available funds: ${if(availableFunds, formatNumber(availableFunds, 2), 'N/A')}",
                    "wrap": true
                  }
                ]
              }
            ]
          }
        }
      }
    }
  ]
}
```

### Dynamic Response Templates
Use when API returns multiple types and each item needs a different template.

**ai-plugin.json configuration:**
```json
{
  "name": "GetTransactions",
  "description": "Returns transaction details with dynamic templates",
  "capabilities": {
    "response_semantics": {
      "data_path": "$.transactions",
      "properties": {
        "template_selector": "$.displayTemplate"
      }
    }
  }
}
```

**API Response with Embedded Templates:**
```json
{
  "transactions": [
    {
      "budgetName": "Fourth Coffee lobby renovation",
      "amount": -2000,
      "description": "Property survey for permit application",
      "expenseCategory": "permits",
      "displayTemplate": "$.templates.debit"
    },
    {
      "budgetName": "Fourth Coffee lobby renovation",
      "amount": 5000,
      "description": "Additional funds to cover cost overruns",
      "expenseCategory": null,
      "displayTemplate": "$.templates.credit"
    }
  ],
  "templates": {
    "debit": {
      "type": "AdaptiveCard",
      "version": "1.5",
      "body": [
        {
          "type": "TextBlock",
          "size": "medium",
          "weight": "bolder",
          "color": "attention",
          "text": "Debit"
        },
        {
          "type": "FactSet",
          "facts": [
            {
              "title": "Budget",
              "value": "${budgetName}"
            },
            {
              "title": "Amount",
              "value": "${formatNumber(amount, 2)}"
            },
            {
              "title": "Category",
              "value": "${if(expenseCategory, expenseCategory, 'N/A')}"
            },
            {
              "title": "Description",
              "value": "${if(description, description, 'N/A')}"
            }
          ]
        }
      ],
      "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
    },
    "credit": {
      "type": "AdaptiveCard",
      "version": "1.5",
      "body": [
        {
          "type": "TextBlock",
          "size": "medium",
          "weight": "bolder",
          "color": "good",
          "text": "Credit"
        },
        {
          "type": "FactSet",
          "facts": [
            {
              "title": "Budget",
              "value": "${budgetName}"
            },
            {
              "title": "Amount",
              "value": "${formatNumber(amount, 2)}"
            },
            {
              "title": "Description",
              "value": "${if(description, description, 'N/A')}"
            }
          ]
        }
      ],
      "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
    }
  }
}
```

### Combined Static and Dynamic Templates
Use static template as default when item doesn't have template_selector or when value doesn't resolve.

```json
{
  "capabilities": {
    "response_semantics": {
      "data_path": "$.items",
      "properties": {
        "title": "$.name",
        "template_selector": "$.templateId"
      },
      "static_template": {
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
          {
            "type": "TextBlock",
            "text": "Default: ${name}",
            "wrap": true
          }
        ]
      }
    }
  }
}
```

## Card Elements

### TextBlock
```json
{
  "type": "TextBlock",
  "text": "Text content",
  "size": "medium",      // small, default, medium, large, extraLarge
  "weight": "bolder",    // lighter, default, bolder
  "color": "attention",  // default, dark, light, accent, good, warning, attention
  "wrap": true
}
```

### FactSet
```json
{
  "type": "FactSet",
  "facts": [
    {
      "title": "Label",
      "value": "Value"
    }
  ]
}
```

### Image
```json
{
  "type": "Image",
  "url": "https://example.com/image.png",
  "size": "medium",  // auto, stretch, small, medium, large
  "style": "default" // default, person
}
```

### Container
```json
{
  "type": "Container",
  "$data": "${items}",  // Iterate over array
  "items": [
    {
      "type": "TextBlock",
      "text": "${name}"
    }
  ]
}
```

### ColumnSet
```json
{
  "type": "ColumnSet",
  "columns": [
    {
      "type": "Column",
      "width": "auto",
      "items": [ ... ]
    },
    {
      "type": "Column",
      "width": "stretch",
      "items": [ ... ]
    }
  ]
}
```

### Actions
```json
{
  "type": "Action.OpenUrl",
  "title": "View Details",
  "url": "https://example.com/item/${id}"
}
```

## Complete Example

**ai-plugin.json:**
```json
{
  "functions": [
    {
      "name": "SearchProjects",
      "description": "Search for projects with status and details",
      "capabilities": {
        "response_semantics": {
          "data_path": "$.projects",
          "properties": {
            "title": "$.name",
            "subtitle": "$.status",
            "url": "$.projectUrl"
          },
          "static_template": {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.5",
            "body": [
              {
                "type": "Container",
                "$data": "${$root}",
                "items": [
                  {
                    "type": "TextBlock",
                    "size": "medium",
                    "weight": "bolder",
                    "text": "${if(name, name, 'Untitled Project')}",
                    "wrap": true
                  },
                  {
                    "type": "FactSet",
                    "facts": [
                      {
                        "title": "Status",
                        "value": "${status}"
                      },
                      {
                        "title": "Owner",
                        "value": "${if(owner, owner, 'Unassigned')}"
                      },
                      {
                        "title": "Due Date",
                        "value": "${if(dueDate, dueDate, 'Not set')}"
                      },
                      {
                        "title": "Budget",
                        "value": "${if(budget, formatNumber(budget, 2), 'N/A')}"
                      }
                    ]
                  },
                  {
                    "type": "TextBlock",
                    "text": "${if(description, description, 'No description')}",
                    "wrap": true,
                    "separator": true
                  }
                ]
              }
            ],
            "actions": [
              {
                "type": "Action.OpenUrl",
                "title": "View Project",
                "url": "${projectUrl}"
              }
            ]
          }
        }
      }
    }
  ]
}
```

## Common Patterns

### List with Images
```json
{
  "type": "Container",
  "$data": "${items}",
  "items": [
    {
      "type": "ColumnSet",
      "columns": [
        {
          "type": "Column",
          "width": "auto",
          "items": [
            {
              "type": "Image",
              "url": "${thumbnailUrl}",
              "size": "small",
              "$when": "${thumbnailUrl != null}"
            }
          ]
        },
        {
          "type": "Column",
          "width": "stretch",
          "items": [
            {
              "type": "TextBlock",
              "text": "${title}",
              "weight": "bolder",
              "wrap": true
            }
          ]
        }
      ]
    }
  ]
}
```

### Status Indicators
```json
{
  "type": "TextBlock",
  "text": "${status}",
  "color": "${if(status == 'Completed', 'good', if(status == 'In Progress', 'attention', 'default'))}"
}
```

### Currency Formatting
```json
{
  "type": "TextBlock",
  "text": "$${formatNumber(amount, 2)}"
}
```



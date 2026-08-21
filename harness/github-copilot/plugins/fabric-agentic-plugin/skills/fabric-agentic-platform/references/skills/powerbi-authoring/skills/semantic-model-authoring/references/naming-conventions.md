# Naming Conventions for Power BI Semantic Models

Guidelines for naming objects in Power BI semantic models. Apply these conventions when creating new models. For existing models, prefer consistency with the established naming patterns unless the user explicitly asks to standardize or audit naming.

## Core Principle

Names should reflect the business language used by the people who consume the model. When in doubt, ask via `ask_user` what terminology their organization uses. The model should be the authoritative source of business terminology.

## General Rules

- All object names must use readable casing with spaces - no `CamelCase`, `snake_case`, or `UPPER_CASE`
- Use business-friendly names: `Sales`, `Product`, `Customer`. Avoid technical terms like `Fact`, `Dim`, `DIM_`, `FACT_`, `STG_`
- Spell out words fully - avoid abbreviations and acronyms unless they are universally understood in the business domain (e.g., YTD, MTD, QTD)
- If an acronym is used, define it in the object's `description`
- Object names must not contain emojis, tabs, line breaks, or other non-standard characters
- Object names must not start or end with a space

## Table Names

- Use business-friendly names: `Sales`, `Product`, `Customer`
- Do not use technical prefixes like `Fact`, `Dim`, `DIM_`, `FACT_`, `STG_`
- Use plural names for fact tables: `Sales`, `Orders`, `Invoices`
- Use singular names for dimension tables: `Product`, `Customer`, `Date`

## Column Names

- Use readable names with spaces: `Order Date`, `Unit Price`, `Product Category`
- For the primary descriptive column of a dimension, prefer a name matching the table name: `Product` instead of `Product Name` in the `Product` table
- Avoid duplicate column names across tables when the model is consumed by Copilot or data agents - use table-qualified names like `Product Name`, `Customer Name` to prevent ambiguity

## Measure Names

- Use clear, descriptive names: `Total Sales`, `Total Quantity`, `# Customers`
- Use `#` prefix for count measures: `# Orders`, `# Products`
- Do not use programming-style names: `NetSls`, `TotDelCst`, `inv_lines_cnt`

### Measure Variations

When creating variations of a base measure (time intelligence, comparisons), follow a consistent naming pattern. The recommended construction order is:

**[Base Name] [Period] ([Unit])**

Examples:
- `Total Sales` - base measure
- `Total Sales (ly)` - last year value
- `Total Sales (ytd)` - year-to-date value
- `Total Sales (qty)` - quantity variant
- `Gross Margin (%)` - percentage unit

### Period Conventions

Pick one convention and apply it uniformly across the entire model:

| Convention | Meaning |
|-----------|---------|
| `(ly)` | Last year |
| `(ytd)` | Year to date |
| `(qtd)` | Quarter to date |
| `(mtd)` | Month to date |

### Unit Conventions

Use parentheses to denote the unit when a measure has multiple variants:

| Suffix | Meaning |
|--------|---------|
| `(%)` | Percentage |
| `(qty)` | Quantity |
| `(value)` | Monetary value (often omitted as default) |

## Anti-Patterns to Avoid

| Anti-Pattern | Issue | Correct |
|-------------|-------|---------|
| `OrderStatus` | CamelCase | `Order Status` |
| `past_due_orders` | snake_case | `Past Due Orders` |
| `TOTAL_COST` | UPPER_CASE | `Total Cost` |
| `Del. Mrgn %` | Abbreviation | `Delivery Margin (%)` |
| `NetSls` | Abbreviation + CamelCase | `Net Sales` |
| `FACT_Orders` | Technical prefix | `Orders` |
| `DIM_Customer` | Technical prefix | `Customer` |
| `Turnover $$$` | Excessive symbols | `Turnover` |
| `SM pct 1YP` | Multiple issues | `Standard Margin (ly) (%)` |

## Display Folder Organization

Use `displayFolder` to organize measures into logical groups within tables. Use a consistent folder structure across all tables of the same type.

Example folder structure for fact tables:
```
Measures\
    Value\
    Quantity\
    Counts\
Facts
Keys
```

Example folder structure for dimension tables:
```
Attributes
Keys
```

## Descriptions

Every visible measure and column should have a `description`. Good descriptions:

- Explain what the object represents in business terms
- Define any acronyms used in the name
- Clarify when to use this object vs similar alternatives
- Are especially important for models consumed by Copilot or data agents

Bad descriptions restate the name (e.g., `Total Sales` described as "The total sales").

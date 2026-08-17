---
name: efcore-d2-db-diagram
description: >-
  Generates D2 entity-relationship diagrams from Entity Framework Core models by extracting DbContext, DbSet<T>, entity configuration, migrations, keys, foreign keys, owned types, many-to-many joins, indexes, schemas, and technical tables. Use this skill when asked to generate a database diagram, ERD, .d2 file, SVG, or PNG from an EF Core or ASP.NET Core codebase.
---

# EF Core D2 database diagram

Create a readable D2 entity-relationship diagram that reflects the actual EF Core persistence model, not only raw C# class shape. Generate `.d2` source and, when possible, validate and render it with the `d2` CLI to `SVG/PNG`. Keep installed package layouts centered on `SKILL.md`; if documenting installation, mention `SKILL.md` plus references. SVG/PNG.

## When to invoke

- "Generate a D2 database diagram from EF Core entities."
- "Create an ERD from this DbContext."
- "Visualize tables, columns, primary keys, foreign keys, and relationships."
- "Analyze DbSet<T>, IEntityTypeConfiguration<T>, Fluent API, and migrations."
- "Produce a .d2 file renderable to SVG or PNG."

## Prerequisites and context

- Use the `d2` CLI when available: `d2 input.d2 output.svg`, `d2 --layout=elk input.d2 output.svg`, and `d2 fmt input.d2`.
- No MCP server is required; the skill generates D2 source code as text.
- Ask the diagram questionnaire before generation or regeneration unless the user already answered it in the same request.

## Diagram questionnaire

Ask every question for new diagrams and regenerations. For quick generation, use the defaults.

| Question | Default |
| --- | --- |
| `Which DbContext should be diagrammed? (auto-detect/all/specific name)` | `auto-detect` |
| `Display columns? (all/key-only/none)` | `key-only` |
| `Display column types? (Yes/No)` | `Yes` |
| `Display nullable/required markers? (Yes/No)` | `Yes` |
| `Required/optional relationship notation? (Yes/No)` | `Yes` |
| `Display indexes and unique constraints? (Yes/No)` | `Yes` |
| `Display enum values? (Yes/No)` | `No` |
| `Display owned types? (inline/separate/hide)` | `inline` |
| `Display many-to-many join tables? (explicit/compact/hide)` | `explicit` |
| `Display audit/technical tables? (Yes/No)` | `No` |
| `Audit/technical table summary? (Yes/No)` | `Yes` |
| `Display migration-only tables not present as entities? (Yes/No)` | `Yes` |
| `Which grouping mode? (bounded-context/schema/namespace/flat)` | `bounded-context` |
| `Which layout engine? (elk/dagre/tala)` | `elk` |
| `Which output format? (d2/svg/png)` | `d2` |

## EF Core extraction rules

Use this source priority when sources disagree:

1. Latest applied migration / migration snapshot.
2. Fluent API configuration in `OnModelCreating` or `IEntityTypeConfiguration<T>`.
3. Data annotations.
4. EF Core conventions.
5. Raw C# class shape.

Detect and represent these EF Core concepts:

| Concept | Required extraction |
| --- | --- |
| Context and entities | `DbContext`, `DbSet<T>`, entity class names, actual table names from `ToTable`, schema names from `ToTable("Table", "schema")`. |
| Keys | Primary keys from `HasKey`, `[Key]`, conventions, migrations, composite keys, and `HasAlternateKey`. |
| Relationships | Foreign keys from `HasForeignKey`, navigation properties, migration operations, required/optional markers, and delete behavior: `Cascade`, `Restrict`, `NoAction`, `SetNull`, `ClientSetNull`. |
| Owned/value objects | `OwnsOne`, `OwnsMany`, `[Owned]`, inline/separate/hide rendering choice. |
| Many-to-many | `UsingEntity` and implicit EF Core join tables; default to explicit join tables. |
| Constraints and columns | `HasIndex`, `IsUnique`, shadow properties, value conversions, enum properties, ignored properties, and ignored entities. |

## D2 rendering rules

Represent each persisted table as a D2 node with `shape: sql_table` when possible.

```d2
Clients: {
  shape: sql_table
  constraint: primary_key
  Id: uuid {constraint: primary_key}
  Name: text
  Status: enum
}
```

If `sql_table` is unavailable or causes validation issues, use a rectangle with structured text. Draw directional edges from dependent table to principal table, and include cardinality and FK name when known.

```d2
Offers.ClientId -> Clients.Id: "N:1 FK_Offers_Clients_ClientId"
```

Use cardinality labels `1:1`, `1:N`, `N:1`, `N:N`, and `owned`. Required relationships use solid lines; optional relationships use dashed lines; cascade delete labels end with `cascade`.

Owned types default to inline rendering:

```d2
Clients: {
  shape: sql_table
  Id: uuid {constraint: primary_key}
  Address.Street: text
  Address.ZipCode: text
  Address.City: text
}
```

When the user chooses `separate`, represent owned types as visually subordinate tables and use an `owned` relationship. For implicit many-to-many relationships, create a generated join table node and mark it as `implicit join`.

## Grouping and style

| Mode | Rule |
| --- | --- |
| `bounded-context` | Group by detected domain area or folder/module. |
| `schema` | Group by database schema such as `public`, `auth`, or `billing`. |
| `namespace` | Group by C# namespace. |
| `flat` | Use no containers; all tables at the same level. |

| Element | Style |
| --- | --- |
| Primary entity tables | Solid border. |
| Join tables | Dashed border. |
| Owned types | Lighter stroke or nested inline fields. |
| Technical tables | Muted style. |
| External or migration-only tables | Dotted border. |

Hide technical tables by default unless requested. Examples include `__EFMigrationsHistory`, Hangfire tables, ASP.NET Identity tables, audit logs, and outbox tables. If hidden, list them in the summary.

## Procedure

1. Read the EF Core project structure.
2. Locate all `DbContext` classes.
3. Locate all `DbSet<T>` declarations.
4. Locate entity classes, owned types, enum types, and value objects.
5. Read `OnModelCreating` and all `IEntityTypeConfiguration<T>` classes.
6. Read migrations when available to confirm table names, join tables, indexes, and delete behaviors.
7. Build a normalized database model before writing D2.
8. Ask the mandatory diagram questionnaire before generation.
9. Generate the `.d2` file from the database model, not raw class nesting.
10. Validate D2 syntax with `d2 fmt` before delivery.
11. Render with `d2 --layout=elk schema.d2 schema.svg` when possible.
12. If regenerating, re-read EF Core mappings and migrations first.

## Progressive disclosure and bundled resources

Load bundled references on demand:

- `references/efcore-model-extraction.md`: rules for reading `DbContext`, `DbSet`, Fluent API, configurations, and migrations.
- `references/d2-erd-style.md`: D2 syntax and visual conventions for ERD diagrams.
- `references/relationship-rules.md`: how to infer one-to-one, one-to-many, many-to-many, and owned relationships.
- `references/grouping-modes.md`: rules for `bounded-context`, `schema`, `namespace`, and `flat` grouping.
- `references/quality-gate.md`: final checklist before delivering the generated diagram.

## Output template

````markdown
## EF Core D2 diagram — <DbContext or scope>

**Status:** generated | needs answers | blocked
**Selected DbContext:** <auto-detect/all/name>
**Output format:** d2 | svg | png
**Layout:** elk | dagre | tala

### D2 source
```d2
<schema.d2 content>
```

### Render command
```bash
d2 --layout=elk schema.d2 schema.svg
```

### Assumptions and hidden tables
- Columns: all | key-only | none
- Owned types: inline | separate | hide
- Many-to-many join tables: explicit | compact | hide
- Hidden technical tables: `__EFMigrationsHistory`, <others or none>

### Validation
- `d2 fmt schema.d2`: pass | fail | not run
- EF Core mappings read: migrations, Fluent API, annotations, conventions
````

## Quality gate

- [ ] The selected `DbContext` is clear.
- [ ] All `DbSet<T>` entities are considered.
- [ ] Fluent API configurations in `OnModelCreating` and `IEntityTypeConfiguration<T>` are read.
- [ ] Migrations are checked when present.
- [ ] Table names and schema names match EF Core mapping.
- [ ] Primary keys, foreign keys, cardinalities, optional/required markers, and delete behavior are represented.
- [ ] Owned types follow the user’s `inline`, `separate`, or `hide` choice.
- [ ] Many-to-many join tables are explicit unless the user asked otherwise.
- [ ] Hidden technical tables are listed in the final summary.
- [ ] D2 syntax is valid with `d2 fmt` when the CLI is available.
- [ ] Edge endpoints use full dot-notation when inside containers.
- [ ] The diagram remains readable and avoids crossing-heavy layouts.

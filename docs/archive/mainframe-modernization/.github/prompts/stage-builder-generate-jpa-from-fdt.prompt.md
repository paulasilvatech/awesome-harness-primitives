---
name: "generate-jpa-from-fdt"
description: "Generates JPA entity classes from Adabas FDT definitions, using JSONB for MU/PE fields."
argument-hint: "ddm=01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm context=<context> package=<java.package> dateformat=<format>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /generate-jpa-from-fdt

## Objective

Parse an Adabas DDM file and generate a JPA entity class with correct type mappings, JSONB for MU/PE fields, and a corresponding Flyway migration script.

## When to Invoke

At the beginning of Stage 3, when the team is setting up the data layer for a bounded context.

## Preconditions

- `02-modern-spec/bounded-contexts.md` exists (to determine which context owns this DDM)
- The DDM file is accessible in `01-archaeology/legacy-sifap/adabas-ddms/`
- The team selected the target package based on the modular monolith design

## Inputs the Team Must Provide

- The path to the DDM file (for example, `01-archaeology/legacy-sifap/adabas-ddms/DDMXXXXX.ddm`)
- The bounded context and target Java package
- The date format used in the legacy system (for example, packed `YYYYMMDD` or alpha `YYYY-MM-DD`)

## What I Will Do

- Parse the FDT structure from the DDM file
- Map each field to the appropriate Java/JPA type
- Handle MU fields as collections mapped with JSONB or `@ElementCollection`
- Handle PE groups as embedded `@OneToMany` entities
- Generate the Flyway migration that creates the PostgreSQL table
- Flag cryptic field names with FIXME markers

## What I Will NOT Do

- Invent business meaning for cryptic field names — I add FIXME markers
- Assume date formats — the team must confirm them
- Create stored procedures — all business logic remains in Java
- Skip MU/PE fields — they are the most difficult part and must be handled explicitly

## Output Format

Two files:

1. JPA entity at `src/main/java/[package]/domain/[EntityName].java`
2. Flyway migration at `db/migration/V[NNN]__create_[table_name].sql`

## Definition of Done

- [ ] The entity compiles without errors
- [ ] Every FDT field has a corresponding Java field with the correct type
- [ ] MU fields use JSONB (`@JdbcTypeCode(SqlTypes.JSON)`) or `@ElementCollection`
- [ ] PE groups use `@OneToMany` with a separate entity class
- [ ] The Flyway migration is valid PostgreSQL 16 DDL
- [ ] Cryptic field names have English comments: `// FIXME: confirm semantics`
- [ ] Cryptic fields are referred for human recording as open questions when necessary

## Prompt Body

You are the `@builder`. The team needs to create a JPA entity from an Adabas DDM.

**Step 1 — Parse the FDT.**
Open the specified DDM file. Extract every field definition:

- Level number (01 = top-level, 02+ = children)
- Short name (two-character Adabas name)
- Long name (if present in comments or documentation)
- Format: A (alpha), N (numeric), P (packed), B (binary), D (date), T (time)
- Length
- Descriptor type: DE (searchable), MU (multi-value), PE (periodic group), SU (super-descriptor)

Present the parsed FDT as a table for the team to review before generating code.

**Step 2 — Map types.**
Apply these mapping rules:

| Adabas | Java | JPA | Notes |
|--------|------|-----|-------|
| A(n) | `String` | `@Column(length = n)` | |
| N(n) without decimals | `Long` or `Integer` | `@Column` | Use `Long` for IDs |
| N(n.m) | `BigDecimal` | `@Column(precision=n, scale=m)` | Always use for money |
| P(n.m) | `BigDecimal` | `@Column(precision=n, scale=m)` | Packed decimal |
| D | `LocalDate` | `@Column` | Ask the team for the source format |
| T | `LocalDateTime` | `@Column` | |
| B(n) | `byte[]` | `@Lob` | Rare |
| MU field | `List<T>` | JSONB or `@ElementCollection` | The team chooses |
| PE group | `List<EmbeddedEntity>` | `@OneToMany` | Separate entity class |

For MU fields, present both options:

1. **JSONB**: Simpler, less queryable → `@JdbcTypeCode(SqlTypes.JSON) private List<String> fieldName;`
2. **@ElementCollection**: More queryable, separate table → `@ElementCollection @CollectionTable(...)`

Let the team choose for each field.

**Step 3 — Handle PE groups.**
For each PE group, create a separate `@Entity` class with:

- Its own table
- A `@ManyToOne` back-reference to the parent entity
- All fields within the PE group mapped as in Step 2
- An index field that tracks the occurrence number

**Step 4 — Handle super-descriptors.**
For each super-descriptor, add a composite `@Index` annotation to the parent entity:

```java
@Table(indexes = @Index(columnList = "field_a, field_b"))
```

**Step 5 — Flag cryptic names.**
For any field whose two-character Adabas name has no clear English equivalent:

```java
/** FIXME: confirm semantics with the team for Adabas field XX */
@Column(name = "xx_value", length = 20)
private String xxValue;
```

If the field is not yet in `01-archaeology/mysteries-found.md`, tell the team
that a person must record it as an open question with `path:line` evidence. Do not
describe an answer, confirm a hypothesis, or change the catalog status.

**Step 6 — Generate the Flyway migration.**
Write a PostgreSQL 16 DDL script:

- Table name derived from the entity name (snake_case)
- Column types corresponding to the JPA mappings
- JSONB columns for MU fields (if JSONB was selected)
- Separate table for PE groups with a foreign key
- Primary key and indexes for descriptors
- `CHECK` constraints when obvious from the FDT (for example, NOT NULL for required fields)

Number the migration: `V[NNN]__create_[table_name].sql`.

**Step 7 — Verify compilation.**
Ensure that the entity class compiles. Report any problems.

## Invocation Example

```
/generate-jpa-from-fdt ddm=01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm context=<context> package=<java.package> dateformat=<format>
```

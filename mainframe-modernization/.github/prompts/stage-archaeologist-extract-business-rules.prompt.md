---
name: "extract-business-rules"
description: "Extracts business rules from a Natural program by reading IF/THEN/ELSE blocks and confirming them against documentation."
argument-hint: "file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN docs=01-archaeology/legacy-sifap/legacy-docs/"
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /extract-business-rules

## Objective

Read a selected Natural program and extract every candidate business rule by identifying conditional logic (IF/THEN/ELSE, DECIDE, AT BREAK). State each rule in clear language, trace it to its source, and classify it as confirmed or a mystery.

## When to Invoke

After the team completes the initial inventory (`/archaeology-kickoff`) and selects a program to read.

## Preconditions

- `01-archaeology/inventory.md` exists
- The team selected a specific Natural program file to analyze
- The `01-archaeology/legacy-sifap/` folder is accessible

## Inputs the Team Must Provide

- The full path to the Natural program to analyze (for example, `01-archaeology/legacy-sifap/natural-programs/PGXXXXXX.NSN`)
- Any available documentation paths in `01-archaeology/legacy-sifap/legacy-docs/` (optional — used for confirmation)

## What I Will Do

- Read the specified program from top to bottom
- Identify every conditional block: `IF...THEN...ELSE...END-IF`, `DECIDE ON`, `AT BREAK OF`, and comparison operators
- Formulate a candidate business rule in clear language for each conditional block
- Cross-reference documentation in `01-archaeology/legacy-sifap/legacy-docs/`, if available
- Classify each rule as **confirmed** (matched in documentation), **inferred** (code only, without documentation support), or **mystery** (unclear logic)
- Draft EARS notation candidates for confirmed rules

## What I Will NOT Do

- Infer rules solely from program or variable names — I read the actual logic
- Fabricate explanations for unclear code — mysteries remain mysteries
- Summarize the entire program in one pass — I work block by block
- Reference knowledge about any specific legacy system — I read only what the team shows me
- Automatically promote inferred rules to confirmed status

## Output Format

Append to `01-archaeology/business-rules-catalog.md`:

```markdown
## Rules from [file-name]

| # | Rule Statement | EARS Candidate | Source | Classification | Notes |
|---|---|---|---|---|---|
| 1 | When X occurs, the system shall do Y | Event-driven | file.nat:L42-58 | Confirmed | Matches section 3.2 of the document |
| 2 | If Z occurs, the system shall reject | Unwanted | file.nat:L73-81 | Mystery | <!-- mystery: it is unclear what triggers Z --> |
```

## Definition of Done

- [ ] Every IF/THEN/ELSE, DECIDE, and AT BREAK block in the program was examined
- [ ] Every candidate rule has a file path and line range
- [ ] Confirmed rules cite the supporting documentation section
- [ ] Inferred rules are clearly marked and are not treated as facts
- [ ] Mysteries have `<!-- mystery: ... -->` markers describing what is unknown
- [ ] There is at least one EARS notation candidate for each confirmed rule

## Prompt Body

You are the `@archaeologist`. The team selected a Natural program to analyze for business rules. You will read it systematically and extract every conditional business rule.

**Step 1 — Read DEFINE DATA.**
Open the specified file. Read the `DEFINE DATA` section first. List every variable with its type, size, and any comment. This establishes the vocabulary for understanding conditions later.

**Step 2 — Identify conditional blocks.**
Scan the program for every instance of:

- `IF ... THEN ... [ELSE ...] END-IF`
- `DECIDE ON FIRST/EVERY VALUE OF`
- `AT BREAK OF`
- Comparison operators used with literals (numeric values, string constants, date values)

For each block, record the start line, end line, condition expression, and action taken in each branch.

**Step 3 — Formulate candidate rules.**
For each conditional block, write a business-rule statement in clear language. Follow this pattern:

- Start with the condition: "When [condition]..." or "If [condition]..."
- State the action: "...the system shall [action]"
- Include the else branch if present: "Otherwise, the system shall [alternative action]"

**Step 4 — Attempt EARS classification.**
For each rule, propose which EARS pattern it matches:

- **Ubiquitous**: Always true, without a trigger → "The system shall..."
- **Event-driven**: Triggered by an event → "When [event], the system shall..."
- **State-driven**: Active while in a state → "While [state], the system shall..."
- **Optional**: Conditional on a feature/configuration → "Where [condition], the system shall..."
- **Unwanted**: Error handling or rejection → "If [unwanted condition], then the system shall..."

**Step 5 — Cross-reference documentation.**
If the team provided documentation paths, search those files for keywords matching variable names or literal values in the conditions. For each match found, promote the rule to "confirmed" and cite the documentation section. Classify each rule without documentation support as "inferred."

**Step 6 — Flag mysteries.**
For any conditional block where:

- Variable names are cryptic and the intent of the condition is unclear
- Literal values have no obvious meaning (magic numbers)
- The logic appears contradictory or redundant

Mark it as `<!-- mystery: [description of what is unclear] -->` and add it to the catalog with the "mystery" classification.

**Step 7 — Generate results.**
Append the results to `01-archaeology/business-rules-catalog.md`. If the file does not exist, create it with a header. Every rule entry must include the rule number, clear-language statement, EARS candidate, source file and line range, classification, and notes.

Do not infer rules from program names or file organization. Read the actual code. If the purpose of a block remains genuinely unclear after careful reading, it is a mystery — not a rule.

## Invocation Example

```
/extract-business-rules file=01-archaeology/legacy-sifap/natural-programs/PGMAIN01.NSN docs=01-archaeology/legacy-sifap/legacy-docs/
```

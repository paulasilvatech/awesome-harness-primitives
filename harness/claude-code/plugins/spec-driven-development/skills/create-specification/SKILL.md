---
name: create-specification
description: >-
  Create a new AI-ready specification file in /spec/ that defines solution requirements,
  constraints, interfaces, dependencies, acceptance criteria, test strategy, and validation
  criteria. Use this skill when the user asks to create a specification, draft an AI-ready spec,
  define requirements, or apply best practices for AI-ready specifications.
---

<!-- Generated from harness/github-copilot/plugins/spec-driven-development/skills/create-specification/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create specification

Create a new self-contained specification that gives humans and Generative AIs precise requirements, constraints, interfaces, examples, and validation criteria for a solution component.

## When to invoke

- "Create a specification for this feature."
- "Draft an AI-ready spec for the data contract."
- "Write /spec/spec-tool-exporter.md."
- "Define requirements and acceptance criteria for this design."
- "Apply best practices for AI-ready specifications."

## Inputs

Use `$ARGUMENTS` as the specification purpose, target filename, and known requirements. If the purpose is missing, infer it from the user's feature description; if the filename is missing, derive one from the approved naming convention.

## AI-ready specification rules

| Rule | Apply it by |
| --- | --- |
| Precise language | Use explicit, testable statements; avoid idioms, metaphors, and context-dependent references. |
| Clear classification | Separate requirements, security requirements, constraints, guidelines, patterns, interfaces, and recommendations. |
| Structured formatting | Use headings, lists, tables, and code blocks for reliable parsing. |
| Defined terms | Define all acronyms, abbreviations, and domain-specific terms. |
| Examples and edge cases | Include representative success, failure, boundary, and unusual cases. |
| Self-contained context | Do not rely on external context that is not referenced or summarized in the spec. |
| Well formed Markdown | Keep frontmatter, headings, tables, and code fences valid. |

## File naming

Create the specification under `/spec/` and name it `spec-[a-z0-9-]+.md`. The descriptive part should start with one high-level purpose: `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`.

## Specification template

Use this exact section order and fill every section appropriately:

```md
---
title: [Concise Title Describing the Specification's Focus]
version: [Optional: e.g., 1.0, Date]
date_created: [YYYY-MM-DD]
last_updated: [Optional: YYYY-MM-DD]
owner: [Optional: Team/Individual responsible for this spec]
tags: [Optional: List of relevant tags or categories, e.g., `infrastructure`, `process`, `design`, `app` etc]
---

# Introduction

[A short concise introduction to the specification and the goal it is intended to achieve.]

## 1. Purpose & Scope

[Provide a clear, concise description of the specification's purpose and the scope of its application. State the intended audience and any assumptions.]

## 2. Definitions

[List and define all acronyms, abbreviations, and domain-specific terms used in this specification.]

## 3. Requirements, Constraints & Guidelines

[Explicitly list all requirements, constraints, rules, and guidelines. Use bullet points or tables for clarity.]

- **REQ-001**: Requirement 1
- **SEC-001**: Security Requirement 1
- **[3 LETTERS]-001**: Other Requirement 1
- **CON-001**: Constraint 1
- **GUD-001**: Guideline 1
- **PAT-001**: Pattern to follow 1

## 4. Interfaces & Data Contracts

[Describe the interfaces, APIs, data contracts, or integration points. Use tables or code blocks for schemas and examples.]

## 5. Acceptance Criteria

[Define clear, testable acceptance criteria for each requirement using Given-When-Then format where appropriate.]

- **AC-001**: Given [context], When [action], Then [expected outcome]
- **AC-002**: The system shall [specific behavior] when [condition]
- **AC-003**: [Additional acceptance criteria as needed]

## 6. Test Automation Strategy

[Define the testing approach, frameworks, and automation requirements.]

- **Test Levels**: Unit, Integration, End-to-End
- **Frameworks**: MSTest, FluentAssertions, Moq (for .NET applications)
- **Test Data Management**: [approach for test data creation and cleanup]
- **CI/CD Integration**: [automated testing in GitHub Actions pipelines]
- **Coverage Requirements**: [minimum code coverage thresholds]
- **Performance Testing**: [approach for load and performance testing]

## 7. Rationale & Context

[Explain the reasoning behind the requirements, constraints, and guidelines. Provide context for design decisions.]

## 8. Dependencies & External Integrations

[Define the external systems, services, and architectural dependencies required for this specification. Focus on what is needed rather than how it is implemented. Avoid specific package or library versions unless they represent architectural constraints.]

### External Systems
- **EXT-001**: [External system name] - [Purpose and integration type]

### Third-Party Services
- **SVC-001**: [Service name] - [Required capabilities and SLA requirements]

### Infrastructure Dependencies
- **INF-001**: [Infrastructure component] - [Requirements and constraints]

### Data Dependencies
- **DAT-001**: [External data source] - [Format, frequency, and access requirements]

### Technology Platform Dependencies
- **PLT-001**: [Platform/runtime requirement] - [Version constraints and rationale]

### Compliance Dependencies
- **COM-001**: [Regulatory or compliance requirement] - [Impact on implementation]

**Note**: This section should focus on architectural and business dependencies, not specific package implementations. For example, specify "OAuth 2.0 authentication library" rather than "Microsoft.AspNetCore.Authentication.JwtBearer v6.0.1".

## 9. Examples & Edge Cases

```code
// Code snippet or data example demonstrating the correct application of the guidelines, including edge cases
```

## 10. Validation Criteria

[List the criteria or tests that must be satisfied for compliance with this specification.]

## 11. Related Specifications / Further Reading

[Link to related spec 1]
[Link to relevant external documentation]
```

## Procedure

1. Determine the high-level purpose: `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`.
2. Create a filename under `/spec/` using `spec-[a-z0-9-]+.md`.
3. Fill the frontmatter with a concise title and `date_created` using the current date.
4. Define scope, assumptions, terms, requirements, security requirements, constraints, guidelines, patterns, interfaces, acceptance criteria, test strategy, rationale, dependencies, examples, validation, and related reading.
5. Ensure each requirement has at least one acceptance criterion and validation criterion.
6. Save the file and report the path plus unresolved assumptions.

## Legacy placeholders

Older invocations may supply `${input:SpecPurpose}` as the purpose placeholder and ask for an `ai-ready`, machine-readable specification. Replace placeholders with concrete values before saving the new spec.

## Output template

```markdown
## Specification creation result

**Status:** created | needs clarification | blocked
**Specification:** `/spec/spec-<purpose-name>.md`
**Purpose:** schema | tool | data | infrastructure | process | architecture | design

### Summary
<one or two sentences describing the specification created>

### Requirement coverage
| Requirement ID | Acceptance criteria | Validation criteria |
| --- | --- | --- |
| `REQ-001` | `<AC IDs>` | `<validation summary>` |

### Validation
- Filename convention `spec-[a-z0-9-]+.md`: pass | fail
- Required sections present: pass | fail
- Requirements have acceptance criteria: pass | fail
- Markdown and frontmatter well formed: pass | fail
```

## Quality gate

- [ ] The spec was created under `/spec/` with `spec-[a-z0-9-]+.md`.
- [ ] The descriptive name starts with `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`.
- [ ] Frontmatter includes a concise title and `date_created`.
- [ ] All 11 required body sections are present and populated.
- [ ] Requirements, security requirements, constraints, guidelines, patterns, acceptance criteria, and dependencies use clear IDs.
- [ ] Every requirement has testable acceptance and validation coverage.
- [ ] The document is self-contained, unambiguous, and well formed Markdown.

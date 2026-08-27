---
description: Create an AI-ready solution specification with clear requirements, constraints, and interfaces.
argument-hint: "SpecPurpose=<schema|tool|data|infrastructure|process|architecture|design>-<topic>"
allowed-tools: Read, Grep, Glob, Edit, Write, WebFetch, WebSearch
---

<!-- Generated from harness/github-copilot/prompts/create-specification.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /create-specification

## Objective

Create a self-contained, AI-ready solution specification that defines requirements, constraints, interfaces, data contracts, acceptance criteria, dependencies, examples, and validation criteria in precise Markdown for use by generative AIs and human implementers.

## When to Invoke

Use this prompt when a solution component needs a new specification before implementation, integration, testing, or architecture review.

## Preconditions

- `${input:SpecPurpose}` is provided and describes the specification purpose.
- The intended high-level purpose is one of `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`.
- The `/spec/` directory may be created or updated.
- Requirements, constraints, interfaces, and known dependencies are available or can be requested.

## Inputs the Team Must Provide

- `SpecPurpose` — the purpose and topic for the specification.
- Requirements, constraints, recommendations, interfaces, APIs, data contracts, and integration points.
- Owner, tags, version, dates, audience, assumptions, dependencies, and external references when known.
- Ask the user for any missing required inputs before generating the specification.

## What I Will Do

- Create a well-formed Markdown specification under `/spec/`.
- Name the file `spec-[a-z0-9-]+.md`, starting with one of `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`.
- Use precise, explicit, unambiguous language and define all acronyms and domain-specific terms.
- Distinguish requirements, security requirements, constraints, guidelines, patterns, interfaces, acceptance criteria, dependencies, and validation criteria.
- Use coded bullets such as `REQ-001`, `SEC-001`, `[3 LETTERS]-001`, `CON-001`, `GUD-001`, `PAT-001`, `AC-001`, `EXT-001`, `SVC-001`, `INF-001`, `DAT-001`, `PLT-001`, and `COM-001`.

## What I Will NOT Do

- Rely on external context that is not included or referenced in the specification.
- Use idioms, metaphors, ambiguous phrases, or context-dependent references.
- Specify concrete package or library versions as dependencies unless they are architectural constraints.
- Put the specification outside `/spec/` or use a filename that violates `spec-[a-z0-9-]+.md`.
- Leave template sections empty or filled with placeholders.

## Output Format

Create the specification file using this template:

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

- **REQ-001**: Requirement 1
- **SEC-001**: Security Requirement 1
- **[3 LETTERS]-001**: Other Requirement 1
- **CON-001**: Constraint 1
- **GUD-001**: Guideline 1
- **PAT-001**: Pattern to follow 1

## 4. Interfaces & Data Contracts

[Describe the interfaces, APIs, data contracts, or integration points. Use tables or code blocks for schemas and examples.]

## 5. Acceptance Criteria

- **AC-001**: Given [context], When [action], Then [expected outcome]
- **AC-002**: The system shall [specific behavior] when [condition]
- **AC-003**: [Additional acceptance criteria as needed]

## 6. Test Automation Strategy

- **Test Levels**: Unit, Integration, End-to-End
- **Frameworks**: MSTest, FluentAssertions, Moq (for .NET applications)
- **Test Data Management**: [approach for test data creation and cleanup]
- **CI/CD Integration**: [automated testing in GitHub Actions pipelines]
- **Coverage Requirements**: [minimum code coverage thresholds]
- **Performance Testing**: [approach for load and performance testing]

## 7. Rationale & Context

[Explain the reasoning behind the requirements, constraints, and guidelines. Provide context for design decisions.]

## 8. Dependencies & External Integrations

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

## Definition of Done

- [ ] The file is saved under `/spec/` as `spec-[a-z0-9-]+.md` and starts with `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`.
- [ ] The specification is well-formed Markdown with correct front matter.
- [ ] Requirements, constraints, guidelines, interfaces, data contracts, acceptance criteria, dependencies, examples, edge cases, and validation criteria are complete.
- [ ] Acronyms and domain-specific terms are defined.
- [ ] Requirements use coded bullets and acceptance criteria are testable, using Given-When-Then where appropriate.
- [ ] Dependency sections focus on what is needed rather than implementation-specific package versions.
- [ ] The document is self-contained and AI-ready.

## Prompt Body

Follow these steps in order.

**Step 1 — Validate the request.** Confirm `${input:SpecPurpose}` and classify the high-level purpose as `schema`, `tool`, `data`, `infrastructure`, `process`, `architecture`, or `design`. If the purpose, requirements, constraints, or target filename are unclear, ask for missing information before proceeding.

**Step 2 — Determine the file path.** Create or update the specification in `/spec/` using the naming convention `spec-[a-z0-9-]+.md`. Start the slug with the high-level purpose, then add a descriptive topic.

**Step 3 — Gather specification content.** Collect requirements, security requirements, constraints, guidelines, patterns, interfaces, APIs, data contracts, integration points, acceptance criteria, test strategy, rationale, dependencies, external systems, third-party services, infrastructure, data dependencies, platform constraints, compliance dependencies, examples, edge cases, validation criteria, and related reading.

**Step 4 — Write AI-ready content.** Use precise, explicit, unambiguous language. Clearly distinguish requirements, constraints, and recommendations. Use headings, lists, tables, schemas, and examples for parsing. Avoid idioms, metaphors, and context-dependent references. Define every acronym and domain term.

**Step 5 — Fill the template completely.** Include front matter with title, version, `date_created`, `last_updated`, owner, and tags when known. Complete Introduction, Purpose & Scope, Definitions, Requirements, Interfaces, Acceptance Criteria, Test Automation Strategy, Rationale, Dependencies, Examples, Validation Criteria, and Related Specifications / Further Reading.

**Step 6 — Validate the specification.** Confirm every section is filled, no placeholder remains, coded IDs are consistent, acceptance criteria are testable, dependencies state what is needed rather than package implementation details, and Markdown is well formed.

## Invocation Example

```
/create-specification SpecPurpose=tool-cli-authentication
```

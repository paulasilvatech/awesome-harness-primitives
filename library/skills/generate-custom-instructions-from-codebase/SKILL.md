---
name: generate-custom-instructions-from-codebase
description: >-
  Generate GitHub Copilot migration and code-evolution instructions by comparing branches, commits, tags, or releases and extracting transformation rules. Use when the user is doing framework upgrades, architecture refactors, technology migrations, dependency updates, pattern changes, API changes, obsolete pattern avoidance, and preserving project conventions during future code modifications.
---

# Generate custom instructions from codebase

Compare two project states, extract real before/after transformation patterns, and write `.github/copilot-migration-instructions.md` so GitHub Copilot can preserve the migration's conventions in future edits.

## When to invoke

- "Generate Copilot instructions from this migration branch."
- "Compare these commits and document the new conventions."
- "Create migration instructions for our framework upgrade."
- "Teach GitHub Copilot to avoid obsolete patterns after this refactor."
- "Build a before/after API correspondence guide from the codebase."

## Inputs

Use `$ARGUMENTS` for the migration configuration. Required values are `MIGRATION_TYPE`, `SOURCE_REFERENCE`, and `TARGET_REFERENCE`; optional values are `ANALYSIS_SCOPE`, `CHANGE_FOCUS`, `AUTOMATION_LEVEL`, `GENERATE_EXAMPLES`, and `VALIDATION_REQUIRED`.

## Configuration model

| Variable | Allowed values | Purpose |
| --- | --- | --- |
| `MIGRATION_TYPE` | `Framework Version`, `Architecture Refactoring`, `Technology Migration`, `Dependencies Update`, `Pattern Changes` | Defines the migration lens. |
| `SOURCE_REFERENCE` | `branch`, `commit`, `tag` | Before-state reference. |
| `TARGET_REFERENCE` | `branch`, `commit`, `tag` | After-state reference. |
| `ANALYSIS_SCOPE` | `Entire project`, `Specific folder`, `Modified files only` | Limits the comparison. |
| `CHANGE_FOCUS` | `Breaking Changes`, `New Conventions`, `Obsolete Patterns`, `API Changes`, `Configuration` | Prioritizes findings. |
| `AUTOMATION_LEVEL` | `Conservative`, `Balanced`, `Aggressive` | Controls how confidently instructions should automate future suggestions. |
| `GENERATE_EXAMPLES` | `true`, `false` | Includes before/after transformations. |
| `VALIDATION_REQUIRED` | `true`, `false` | Marks transformations that require checks before application. |

## Procedure

1. Resolve `SOURCE_REFERENCE` and `TARGET_REFERENCE` to concrete commits, branches, or tags.
2. Compare folder structure and detect moved, renamed, deleted, and added files.
3. Analyze configuration changes, new dependencies, and removed dependencies.
4. Extract code transformation patterns based on `MIGRATION_TYPE` and `CHANGE_FOCUS`.
5. Build a before/after correspondence matrix with mandatory transformations, validation-required transformations, API mappings, new patterns, and obsolete patterns.
6. Generate `.github/copilot-migration-instructions.md` with examples when `GENERATE_EXAMPLES=true`.
7. Test the instructions against representative changed code, then adjust rules and exceptions.

## Migration analysis focus

| Migration type | Extract |
| --- | --- |
| Framework Version | API changes, new features being used, obsolete methods/properties, syntax or convention changes. |
| Architecture Refactoring | Architectural pattern changes, new abstractions, responsibility reorganization, data flow changes. |
| Technology Migration | Functional equivalences, API and syntax changes, new dependencies, configuration changes. |
| Dependencies Update | Package replacements, version constraints, import changes, config changes, compatibility rules. |
| Pattern Changes | Repetitive transformations, old/new format rules, exceptions, and special cases. |

## Instruction sections

| Section | Include |
| --- | --- |
| Migration Context | `MIGRATION_TYPE`, `SOURCE_REFERENCE`, `TARGET_REFERENCE`, `GENERATION_DATE`, and `ANALYSIS_SCOPE`. |
| Mandatory Transformations | `AUTOMATIC_TRANSFORMATION_RULES` with `OLD_CODE`, `NEW_CODE`, trigger, and action when `AUTOMATION_LEVEL` is not `Conservative`. |
| Transformations with Validation | `TRANSFORMATIONS_WITH_VALIDATION`, `NEW_APPROACH`, `VALIDATION_CRITERIA`, and `ALTERNATIVE_OPTIONS` when `VALIDATION_REQUIRED=true`. |
| API Correspondences | `API_CORRESPONDENCE_TABLE` with `OLD_API`, `NEW_API`, changes, and `CODE_EXAMPLE` when `CHANGE_FOCUS=API Changes` or `MIGRATION_TYPE=Framework Version`. |
| New Patterns to Adopt | `DETECTED_EMERGING_PATTERNS`, `PATTERN_NAME`, `WHEN_TO_USE`, `HOW_TO_IMPLEMENT`, and benefits. |
| Obsolete Patterns to Avoid | `DETECTED_OBSOLETE_PATTERNS`, `OLD_PATTERN`, why avoid, `NEW_PATTERN`, and `CONVERSION_STEPS`. |
| File Type Specific Instructions | `CONFIG_TRANSFORMATION_EXAMPLES`, `SOURCE_TRANSFORMATION_EXAMPLES`, and `TEST_TRANSFORMATION_EXAMPLES` when `GENERATE_EXAMPLES=true`. |
| Validation and Security | Automatic control points plus manual escalation for `COMPLEX_CASES_LIST`, `ARCHITECTURAL_DECISIONS`, and `BUSINESS_IMPACTS`. |
| Migration Monitoring | Migration percentage, manual validations, automatic transformation error rate, and average migration time per file. |

## Generated file template

```markdown
# GitHub Copilot Migration Instructions

## Migration Context
- **Type**: <MIGRATION_TYPE>
- **From**: <SOURCE_REFERENCE>
- **To**: <TARGET_REFERENCE>
- **Date**: <GENERATION_DATE>
- **Scope**: <ANALYSIS_SCOPE>

## Automatic Transformation Rules

### 1. Mandatory Transformations
- **Old Pattern**: <OLD_CODE>
- **New Pattern**: <NEW_CODE>
- **Trigger**: <when to detect this pattern>
- **Action**: <transformation to apply automatically>

### 2. Transformations with Validation
- **Detected Pattern**: <description>
- **Suggested Transformation**: <NEW_APPROACH>
- **Required Validation**: <VALIDATION_CRITERIA>
- **Alternatives**: <ALTERNATIVE_OPTIONS>

### 3. API Correspondences
| Old API | New API | Notes | Example |
| --- | --- | --- | --- |
| <OLD_API> | <NEW_API> | <changes> | <CODE_EXAMPLE> |

### 4. New Patterns to Adopt
- **Pattern**: <PATTERN_NAME>
- **Usage**: <WHEN_TO_USE>
- **Implementation**: <HOW_TO_IMPLEMENT>
- **Benefits**: <advantages>

### 5. Obsolete Patterns to Avoid
- **Obsolete Pattern**: <OLD_PATTERN>
- **Why Avoid**: <reasons>
- **Alternative**: <NEW_PATTERN>
- **Migration**: <CONVERSION_STEPS>

## File Type Specific Instructions

### Configuration Files
<CONFIG_TRANSFORMATION_EXAMPLES>

### Main Source Files
<SOURCE_TRANSFORMATION_EXAMPLES>

### Test Files
<TEST_TRANSFORMATION_EXAMPLES>

## Validation and Security

### Automatic Control Points
- <tests, performance metrics, compatibility checks>

### Manual Escalation
- <COMPLEX_CASES_LIST>
- <ARCHITECTURAL_DECISIONS>
- <BUSINESS_IMPACTS>

## Migration Monitoring

### Tracking Metrics
- Percentage of code automatically migrated
- Number of manual validations required
- Error rate of automatic transformations
- Average migration time per file

### Error Reporting
- Feedback patterns to improve rules
- Exceptions to document
- Adjustments to make to instructions
```

## Transformation example format

```text
// BEFORE (<SOURCE_REFERENCE>)
<OLD_CODE_EXAMPLE>

// AFTER (<TARGET_REFERENCE>)
<NEW_CODE_EXAMPLE>

// COPILOT INSTRUCTIONS
When you see this pattern <trigger>, transform it to <NEW_PATTERN> following these steps: <steps>.
```

## Typical use cases

| Use case | Good output |
| --- | --- |
| Framework Version Migration | Angular 14 to Angular 17, React Class Components to Hooks, .NET Framework to .NET Core rules with breaking changes. |
| Technology Stack Evolution | jQuery to React, REST to GraphQL, SQL to NoSQL functional mappings. |
| Architecture Refactoring | Monolith to Microservices, MVC to Clean Architecture, Component to Composable architecture. |
| Design Pattern Modernization | Repository Pattern, Dependency Injection, Observer to Reactive Programming adoption guidance. |

## Criteria

- [ ] Instructions are based on actual diffs, not generic migration advice.
- [ ] Automatic rules are only used when the old pattern has a reliable trigger and deterministic replacement.
- [ ] Validation-required transformations name concrete tests, compatibility checks, or manual review criteria.
- [ ] API correspondence entries preserve old/new names and examples from the codebase.
- [ ] Obsolete patterns explain why they are wrong and what to use instead.
- [ ] Security and business-impact changes are escalated for human review.

## Migration placeholders

Preserve placeholders used by generated migration instructions: `ADVANTAGES`, `CHANGES`, `DESCRIPTION`, `REASONS`, `STEPS`, `TRIGGER`, and `cross-version`.

## Output template

```markdown
## Copilot migration instructions result

**Status:** generated | needs validation | blocked
**Output file:** `.github/copilot-migration-instructions.md`
**Migration:** `<MIGRATION_TYPE>` from `<SOURCE_REFERENCE>` to `<TARGET_REFERENCE>`

### Patterns extracted
| Category | Count | Examples |
| --- | --- | --- |
| Mandatory transformations | <count> | <summary> |
| Transformations with validation | <count> | <summary> |
| API correspondences | <count> | <summary> |
| New patterns | <count> | <summary> |
| Obsolete patterns | <count> | <summary> |

### Validation
- Test application on sample code: pass | fail | not run
- Exceptions documented: pass | fail
- Manual escalations listed: pass | fail
```

## Quality gate

- [ ] `MIGRATION_TYPE`, `SOURCE_REFERENCE`, `TARGET_REFERENCE`, `ANALYSIS_SCOPE`, `CHANGE_FOCUS`, `AUTOMATION_LEVEL`, `GENERATE_EXAMPLES`, and `VALIDATION_REQUIRED` are recorded.
- [ ] `.github/copilot-migration-instructions.md` is generated with migration context and transformation rules.
- [ ] API mappings retain `OLD_API`, `NEW_API`, and `CODE_EXAMPLE` when API changes are in scope.
- [ ] Examples include `OLD_CODE_EXAMPLE` and `NEW_CODE_EXAMPLE` when requested.
- [ ] `COMPLEX_CASES_LIST`, `ARCHITECTURAL_DECISIONS`, and `BUSINESS_IMPACTS` are escalated instead of automated.
- [ ] Validation and monitoring guidance is concrete enough for future GitHub Copilot edits.

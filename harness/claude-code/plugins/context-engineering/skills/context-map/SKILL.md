---
name: context-map
description: >-
  Build a concise map of files relevant to a requested code change before implementation. Use when
  the user asks to identify affected files, plan changes, map dependencies, find tests, locate
  reference patterns, or assess risk before editing.
---

<!-- Generated from harness/github-copilot/plugins/context-engineering/skills/context-map/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Context map

Search the repository for task-relevant code, dependencies, tests, and patterns, then return a risk-aware map that guides later implementation without changing files. If an upstream template supplies `task_description`, treat it as the task text.

## When to invoke

- "Create a context map for this task before coding."
- "Find the files I need to modify for this change."
- "Map dependencies and tests for this feature."
- "Assess implementation risk before making edits."

## Discovery targets

| Target | How to identify it | Include in map when |
| --- | --- | --- |
| Files to modify | Names, symbols, routes, commands, imports, configuration keys, or error text from the task. | The file owns behavior that must change. |
| Dependencies | Direct imports, exports, callers, generated types, schema references, or API contracts. | A modification may require a corresponding update. |
| Test files | Unit, integration, snapshot, e2e, fixture, or golden files near the affected behavior. | They verify or should verify the requested change. |
| Reference patterns | Existing code that solves a similar problem in the same repository. | It establishes style, architecture, or validation behavior to copy. |
| Risk items | Public APIs, migrations, configuration, concurrency, security, performance, or backward compatibility. | The change can break consumers or deployment. |

## Procedure

1. Convert the user's task into searchable terms: domain nouns, function names, routes, CLI flags, UI labels, error messages, and config keys.
2. Search for owning files first, then follow direct imports/exports and callers from those files.
3. Search for tests using the same symbol names, fixtures, route names, snapshots, or directory conventions.
4. Find at least one repository-native reference pattern when the task changes style-sensitive code.
5. Stop at the smallest complete map; do not implement until the user or parent workflow asks for edits.

## Risk assessment rules

| Risk checkbox | Mark when |
| --- | --- |
| Breaking changes to public API | Function signatures, exported types, routes, CLI flags, schemas, or documented behavior may change. |
| Database migrations needed | Tables, columns, indexes, constraints, seed data, or persistence shape must change. |
| Configuration changes required | Environment variables, secrets, deployment manifests, feature flags, or package settings must change. |

## Output template

```markdown
## Context Map

### Files to Modify
| File | Purpose | Changes Needed |
|------|---------|----------------|
| `path/to/file` | <description> | <what changes> |

### Dependencies (may need updates)
| File | Relationship |
|------|--------------|
| `path/to/dep` | <imports/calls/exports affected symbol> |

### Test Files
| Test | Coverage |
|------|----------|
| `path/to/test` | <behavior covered or missing> |

### Reference Patterns
| File | Pattern |
|------|---------|
| `path/to/similar` | <example to follow> |

### Risk Assessment
- [ ] Breaking changes to public API
- [ ] Database migrations needed
- [ ] Configuration changes required
```

## Quality gate

- [ ] Search terms came from the user's task, not generic repository browsing.
- [ ] Every proposed file to modify has a specific reason and expected change.
- [ ] Direct dependencies and tests were checked for each proposed modification area.
- [ ] At least one reference pattern is listed or the absence of a pattern is stated.
- [ ] Risk checkboxes reflect evidence from the repository.
- [ ] No implementation edits were made as part of the context map.

---
name: oo-component-documentation
description: >-
  Create or update standardized object-oriented component documentation from source code or
  existing Markdown docs using create-mode and update-mode guidance. Use when the user asks to
  document a class, component, folder, public API, architecture relationships, design patterns, or
  refresh existing OO component documentation.
---

<!-- Generated from harness/github-copilot/plugins/repo-documentation/skills/oo-component-documentation/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# OO component documentation

Analyze object-oriented source code or an existing component document, choose create or update mode, then produce Markdown documentation grounded in the implementation with interfaces, dependencies, diagrams, examples, quality attributes, and explicit gaps.

## When to invoke

- "Generate documentation for this component."
- "Refresh the existing Markdown docs from the current code."
- "Document this class hierarchy and public API."
- "Create OO component documentation for this folder."
- "Update component diagrams and examples to match implementation."

## Prerequisites and context

- The user must provide or imply a source file, component folder, or existing documentation Markdown file.
- Use `assets/documentation-template.md` as the canonical section checklist and baseline structure.
- Use `references/create-mode.md` for new documentation and `references/update-mode.md` for revising existing documentation.

## Procedure

1. Determine the mode before writing anything.
2. Inspect the component implementation and related files needed to understand the public surface, internal structure, dependencies, configuration, tests, and runtime boundaries.
3. Read `assets/documentation-template.md` and use it as the shared scaffold.
4. Apply `references/create-mode.md` or `references/update-mode.md` based on the selected mode.
5. Produce or revise Markdown so diagrams, examples, interfaces, dependencies, and quality attributes reflect current implementation.
6. Call out unknowns, gaps, and unsupported assumptions instead of inventing behavior.

## Mode selection

| Evidence | Mode | Output target |
| --- | --- | --- |
| User provides an existing Markdown documentation file, docs path, or asks to refresh/revise docs | Update mode | The existing documentation file. |
| User provides a source file, component folder, class, or asks to generate docs from code | Create mode | A new Markdown document following the template. |
| User provides both code and existing documentation | Update mode | Existing documentation is the target; current source code is the source of truth. |
| Request is ambiguous | Infer from path type | Existing `.md` means update mode; source/component path means create mode. |

## Documentation standards

| ID | Standard | Apply as |
| --- | --- | --- |
| DOC-001 | C4 Model | Document Context, Containers, Components, and Code at the level supported by the input. |
| DOC-002 | Arc42 | Cover architecture decisions, building blocks, runtime view, quality attributes, and risks without padding. |
| DOC-003 | IEEE 1016 Software Design Description | Make design entities, interfaces, data, and rationale explicit. |
| DOC-004 | Agile Documentation | Keep just enough documentation that adds value to developers and maintainers. |
| DOC-005 | Developer-maintainer audience | Prefer implementation-grounded API, dependency, and maintenance detail over marketing prose. |

## Analysis checklist

| ID | Inspect | Capture |
| --- | --- | --- |
| ANA-001 | Component boundary | Whether the input is a folder, file, package, class, or documentation target. |
| ANA-002 | Class structures | Inheritance, composition, interfaces, abstract classes, and concrete implementations. |
| ANA-003 | Design patterns | Architectural decisions, dependency inversion, factories, adapters, observers, strategies, or custom patterns. |
| ANA-004 | Public APIs | Interfaces, methods, constructors, events, properties, usage patterns, and integration points. |
| ANA-005 | Method contracts | Parameters, return values, async behavior, exceptions, lifecycle, disposal, and concurrency. |
| ANA-006 | Quality attributes | Performance, security, reliability, maintainability, extensibility, and testability characteristics. |
| ANA-007 | Data flow | Collaboration patterns, input/output ownership, state transitions, and surrounding components. |
| ANA-008 | Evidence discipline | Ground every claim in code, project structure, configuration, tests, or clearly stated assumptions. |

## Language-specific focus

| ID | Language | Emphasize |
| --- | --- | --- |
| LNG-001 | C#/.NET | `async`/`await`, dependency injection, configuration, disposal, options patterns. |
| LNG-002 | Java | Spring framework, annotations, exception handling, packaging, dependency injection. |
| LNG-003 | TypeScript/JavaScript | modules, async patterns, types, npm dependencies, runtime boundaries. |
| LNG-004 | Python | packages, virtual environments, type hints, testing, dependency management. |

## Mode and language terminology

Keep `mode-specific` create/update rules separate. For **TypeScript/JavaScript** and `TypeScript/JavaScript**` legacy wording, inspect module boundaries, runtime boundaries, and `async/await` behavior. If the code uses a `non-standard` architecture, describe it directly rather than forcing a standard label.
## Error handling

| ID | Condition | Response |
| --- | --- | --- |
| ERR-001 | Path does not exist | Explain the expected path and whether a source path or documentation file is needed. |
| ERR-002 | No relevant source files found | Document the gap and suggest likely locations to inspect next. |
| ERR-003 | Documentation target cannot be inferred | State the ambiguity and ask for the missing path only when inference is impossible. |
| ERR-004 | Non-standard architecture | Document the custom approach instead of forcing a generic pattern. |
| ERR-005 | Incomplete source access | Continue with available evidence and mark unsupported sections clearly. |

## Progressive disclosure and bundled resources

| Resource | Use when | Purpose |
| --- | --- | --- |
| `assets/documentation-template.md` | Every create or update task | Canonical section checklist and baseline Markdown structure. |
| `references/create-mode.md` | Creating new documentation from source | Mode-specific rules for source-driven documentation. |
| `references/update-mode.md` | Updating existing documentation | Mode-specific rules for preserving, correcting, and refreshing existing docs. |

## Gotchas

- **Determine the mode first**: create-mode and update-mode choose different output targets and preservation rules.
- **Do not invent APIs**: examples and interface descriptions must match current implementation.
- **Use Mermaid only when it clarifies relationships**: diagrams should reflect real dependencies and flows.
- **Document limitations explicitly**: incomplete source coverage is a finding, not permission to guess.

## Output template

```markdown
## OO component documentation result

**Status:** created | updated | partial | blocked
**Mode:** create | update
**Source:** `<source file or folder>`
**Target:** `<documentation file>`

### Coverage
| Area | Evidence | Notes |
| --- | --- | --- |
| Component boundary | `<files/classes inspected>` | <summary> |
| Public APIs | `<interfaces/methods>` | <summary> |
| Dependencies | `<dependencies/config>` | <summary> |
| Quality attributes | `<evidence>` | <summary> |

### Gaps
- <unsupported section, missing source, or none>
```

## Quality gate

- [ ] Create mode or update mode was selected before writing.
- [ ] `assets/documentation-template.md` was used as the section checklist.
- [ ] The relevant mode file, `references/create-mode.md` or `references/update-mode.md`, was followed.
- [ ] Public APIs, interfaces, dependencies, examples, diagrams, and quality attributes are grounded in current code.
- [ ] DOC-001 through DOC-005 and ANA-001 through ANA-008 were considered.
- [ ] Language-specific concerns LNG-001 through LNG-004 were applied when relevant.
- [ ] ERR-001 through ERR-005 conditions were handled honestly if encountered.

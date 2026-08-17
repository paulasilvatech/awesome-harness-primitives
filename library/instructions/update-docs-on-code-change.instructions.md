---
applyTo: "**/*.{md,js,mjs,cjs,ts,tsx,jsx,py,java,cs,go,rb,php,rs,cpp,c,h,hpp}"
description: "Enforces documentation synchronization when code changes affect README files, API docs, configuration guides, changelogs, examples, or migration guidance."
---

# Documentation Update Conventions — Code Change Synchronization

These instructions apply when application code, public APIs, command-line behavior, configuration, dependencies, setup, deployment, or examples change in files matched by `applyTo`. They are authoritative for deciding when documentation must change with code and how to keep README.md, API documentation, configuration guides, examples, migration guides, and CHANGELOG.md synchronized; language-specific documentation generators, repository-specific release policy, and stricter project docs conventions win where they define narrower rules.

## Change Triggers

Check documentation impact whenever code changes alter public behavior, user workflows, or operational requirements.

| Trigger | Documentation impact |
| --- | --- |
| New features or functionality are added | Update feature descriptions, usage examples, README.md features, and table of contents when present. |
| API endpoints, methods, interfaces, or signatures change | Update API reference, OpenAPI/Swagger specs, parameters, response schemas, request/response examples, and SDK usage examples. |
| Breaking changes are introduced | Add migration guides, before/after examples, upgrade checklists, and changelog entries with **BREAKING** where applicable. |
| Dependencies, requirements, installation, or setup procedures change | Update prerequisites, installation commands, getting-started steps, and dependency requirements. |
| Configuration options or environment variables change | Update `.env.example`, config file templates, default values, descriptions, and deployment guides. |
| CLI commands, scripts, options, or defaults change | Document command syntax, option descriptions, default values, and examples. |
| Code examples become outdated | Update imports, function calls, output blocks, and error handling examples so snippets compile or run. |

## Documentation Surfaces

Maintain the documentation surface that matches the change rather than updating README.md alone.

| Surface | Owns | Required updates |
| --- | --- | --- |
| `README.md` | Project overview, quick start, basic usage, feature list | Update for new capabilities, install/setup changes, CLI commands, configuration examples, prerequisites, and table of contents. |
| `CHANGELOG.md` | Version history and user-facing changes | Add entries under `Added`, `Changed`, `Fixed`, `Deprecated`, `Removed`, or `Security`; prefix breaking changes with **BREAKING**. |
| `docs/installation.md` | Setup and installation guide | Keep install commands, prerequisites, and environment assumptions current. |
| `docs/configuration.md` | Configuration options and examples | Include new environment variables, defaults, config file options, deprecated options, and templates. |
| `docs/api.md` | API reference documentation | Document HTTP method, path, parameters, response schemas, status codes, authentication, and authorization. |
| `docs/contributing.md` | Contribution workflow | Update when build, validation, or doc maintenance workflow changes. |
| `docs/migration-guides/` | Breaking and major-version migration | Include what changed, before/after examples, common issues, solutions, and upgrade checklist. |
| `examples/` | Working tutorials and code samples | Keep runnable examples aligned with current API signatures and imports. |

## API and Example Documentation Format

Document public functions and endpoints with enough structure that readers can call them without reading the source.

| Item | Required content |
| --- | --- |
| `functionName(param1, param2)` | Brief description, `param1` and `param2` types, optional/default markers, return type, example, and `ErrorType` or thrown errors. |
| `HTTP_METHOD /api/endpoint` | Description, JSON request, JSON response, `200`, `400`, `401`, and other relevant status codes. |
| Feature page | Feature name, usage, configuration, advanced usage, troubleshooting, limitations, and edge cases. |
| Code example | Necessary imports/setup, complete runnable code, expected output when useful, and error handling for realistic failure modes. |

Use generated API documentation when available, but keep narrative docs synchronized with the generated contract.

## Automation, Validation, and Tooling

Prefer existing project tooling over manual inspection. Use automation when the repository already provides it, including JSDoc/TSDoc for JavaScript/TypeScript, Sphinx or pdoc for Python, Javadoc for Java, xmldoc for C#, godoc for Go, rustdoc for Rust, markdownlint, markdown-link-check, cspell, code example validators, and documentation build commands.

Preserve and run documented validation scripts when present:

```json
{
  "scripts": {
    "docs:build": "Build documentation",
    "docs:test": "Test code examples in docs",
    "docs:lint": "Lint documentation files",
    "docs:links": "Check for broken links",
    "docs:spell": "Spell check documentation",
    "docs:validate": "Run all documentation checks",
    "docs:check": "Verify docs build",
    "docs:test-examples": "Test code examples"
  }
}
```

Pre-commit or CI checks should cover documentation build success, broken links, valid examples, and changelog presence when the project expects changelog entries.

## Quality and Maintenance

Write documentation in clear, concise language with consistent terminology. Include basic and advanced examples, limitations, edge cases, troubleshooting notes, migration paths, and error handling examples when users need them. Keep documentation DRY: link or refer within the project instead of duplicating large blocks, but do not leave users without enough context to succeed.

Maintenance cadence is conventional unless the repository defines a different one: review documentation monthly for accuracy, per release for version numbers and examples, quarterly for outdated patterns or deprecated features, and annually for a comprehensive audit. When deprecating a feature, add a deprecation notice, update examples to the recommended alternative, create a migration guide, update the changelog, state the removal timeline, and remove deprecated docs in the next major version.

## Good / Bad Examples

The examples below illustrate documenting an API signature change and a new configuration variable with the code change.

**Good:**

```markdown
### `createUser(email, displayName)`

Creates a user account.

**Parameters:**
- `email` (string): Unique user email address.
- `displayName` (string, optional): Name shown in the UI. Defaults to the email local part.

**Returns:**
- `User`: Created user record.

**Throws:**
- `ValidationError`: When `email` is invalid.

Update `.env.example` and `docs/configuration.md` when `USER_INVITE_TTL_SECONDS` is introduced.
```

Why: The docs name parameters, defaults, return type, errors, and the related configuration surface affected by the code change.

**Bad:**

```markdown
Updated user API. See code for details.
```

Why: The statement omits the signature, behavior, examples, errors, configuration impact, and migration guidance users need.

## Baseline Compatibility Vocabulary

Preserve these legacy names, status labels, placeholders, paths, and configuration tokens when editing this instruction; they exist so older TaskSync, documentation, Dataverse, pandas, and troubleshooting examples remain searchable and recognizable.

- `COMPILED`, `CONFIGURABLE`, `CONFIGURATION`, `DETAIL`, `Docker/Kubernetes`, `Enable/Disable`, `FINAL`, `GOAL`
- `INSTRUCTION`, `INSTRUCTIONS`, `Instruction Configuration`, `Instruction Sections and Configurable Instruction Sections`, `PR/issue`, `PROCEDURE`, `PROPERTY`, `SECTION`
- `SECTIONS`, `THIS`, `YYYY`, `and/or`, `api.md`, `apply-automation-tooling`, `apply-automation-tooling == true`, `apply-best-practices`
- `apply-best-practices == true`, `apply-condition`, `apply-doc-file-structure`, `apply-doc-file-structure == true`, `apply-doc-patterns`, `apply-doc-patterns == true`, `apply-doc-quality-standard`, `apply-doc-quality-standard == true`
- `apply-doc-verification`, `apply-doc-verification == true`, `apply-git-integration`, `apply-git-integration == true`, `apply-maintenance-schedule`, `apply-maintenance-schedule == true`, `apply-this`, `apply-validation-commands`
- `apply-validation-commands == true`, `compile/run`, `configuration.md`, `contributing.md`, `docs/**`, `examples/**`, `free-form`, `infrastructure-as-code`
- `installation.md`, `internal/external`, `key/token`, `migration-guides/`, `pre-commit`, `step-by-step`, `true`, `type`

## Conventions

| Rule | Rationale |
|---|---|
| Update documentation in the same PR or commit as behavior-changing code | Users and reviewers see the code and contract change together |
| Update `README.md` for new features, setup changes, CLI changes, and configuration changes | README.md is the entry point most users read first |
| Update API documentation and OpenAPI/Swagger specs when endpoints, methods, interfaces, authentication, or authorization change | Client code depends on accurate request, response, and security contracts |
| Update code examples whenever function signatures, imports, interfaces, SDK usage, or best practices change | Examples are executable documentation and become defects when stale |
| Update `.env.example`, config templates, and configuration docs for new or changed environment variables | Operators need discoverable defaults and meanings |
| Add migration guides for breaking API changes, major version updates, and deprecations | Users need safe before/after paths and upgrade checklists |
| Use existing documentation generators, linters, link checkers, spell checkers, and example validators | Automated checks catch drift that prose review misses |
| Keep documentation clear, concise, consistent, and focused on user needs | Vague or implementation-only docs do not help users complete tasks |

## Do / Do Not

| Do | Do not |
|---|---|
| Document new features in README.md, relevant docs pages, examples, and changelog entries | Commit user-visible code changes with no documentation update |
| Include before/after examples for reviewed behavior changes | Leave reviewers to infer migration impact from code diffs |
| Test code examples before committing when tooling exists | Leave outdated snippets, imports, or output blocks in docs |
| Document environment variables, defaults, and config file changes | Add configuration options only in source code |
| Use `Added`, `Changed`, `Fixed`, `Deprecated`, `Removed`, and `Security` changelog sections consistently | Mix user-facing release notes into unrelated prose |
| Use generated docs such as JSDoc/TSDoc, Sphinx/pdoc, Javadoc, xmldoc, godoc, or rustdoc where appropriate | Hand-maintain API references that the project already generates |
| Validate docs with `npm run docs:check`, `npm run docs:test-examples`, `npm run docs:lint`, or project equivalents when present | Invent new validation tooling just to satisfy this instruction |
| Document real behavior, limitations, edge cases, and troubleshooting | Document features that do not exist yet or implementation details users do not need |

## Checklist Before Opening a PR

- [ ] README.md reflects new or changed features, setup, CLI, configuration, or dependency behavior.
- [ ] Public APIs, endpoints, methods, interfaces, request/response examples, OpenAPI/Swagger specs, and authentication notes are current.
- [ ] Code examples compile or run where the repository provides validation for them.
- [ ] `.env.example`, config templates, deployment guides, and configuration docs match new environment variables or options.
- [ ] Breaking changes, major version changes, and deprecations have migration guidance, before/after examples, and changelog entries.
- [ ] CHANGELOG.md includes user-facing changes under the appropriate section when the project maintains one.
- [ ] Internal and external links touched by the change are valid.
- [ ] Existing documentation build, lint, link, spell, and example validation commands pass when available.

# Planning, Strategy, ADR, And Architecture

Before writing plugin code, create the artifacts that make the work reviewable.

## Required Artifacts

| Artifact | Purpose |
| --- | --- |
| `PLAN.md` | Scope, user, plugin type, features, non-goals, and acceptance criteria. |
| `STRATEGY.md` | Build, packaging, config, versioning, security, and publication strategy. |
| `ADR-0001-plugin-architecture.md` | Main architecture decision, alternatives, and consequences. |
| `ARCHITECTURE.md` | Runtime view, package boundaries, extension points, APIs, and data flow. |
| `VALIDATION.md` | Hooks, commands, tests, static analysis, security checks, and release gates. |
| `PUBLICATION.md` | Private, npm, or community publication path and checklist. |

## Architecture Questions

- Which app or monorepo hosts the plugin?
- Is the plugin internal, open source, or a community candidate?
- Which Backstage version or package version policy applies?
- Which extension points are used?
- What is configured through `app-config.yaml`?
- Which secrets, tokens, or external APIs are needed?
- Which permissions and ownership model apply?
- How is the plugin tested in isolation and in the app?

## ADR Requirements

- State one decision clearly.
- List alternatives considered.
- Explain compatibility and migration impact.
- Include security and operational consequences.
- Link to official docs or source artifacts.

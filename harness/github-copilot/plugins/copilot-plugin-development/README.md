# GitHub Copilot plugin development

Create, migrate, audit, and validate plugin packages and marketplaces using the current repository governance.

## Components

- `copilot-primitive-architect` agent for package boundaries, ownership, and composition review.
- `copilot-plugin-authoring` skill for ordered implementation, schema validation, synchronization, and runtime proof.

## Install

```bash
copilot plugin install copilot-plugin-development@copilot-primitives
```

Use `copilot --agent copilot-plugin-development:copilot-primitive-architect` for architecture review or ask GitHub Copilot to use the `copilot-plugin-authoring` skill for implementation.

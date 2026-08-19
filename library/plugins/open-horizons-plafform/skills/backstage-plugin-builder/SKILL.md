---
name: backstage-plugin-builder
description: "Use when planning, scaffolding, validating, or preparing custom Backstage plugins and modules with official documentation; produces plans, ADRs, plugin artifacts, validation hooks, package checks, and publication readiness notes. DO NOT USE FOR: deploying Backstage itself (use backstage-deployment), configuring Codespaces for Golden Paths (use codespaces-golden-paths), or general Markdown writing (use markdown-writer). Triggers include \"build a Backstage plugin\", \"create a backend module\", \"validate this plugin package\"."
---

# Backstage Plugin Builder

This workflow plans, scaffolds, validates, and prepares Backstage plugins and modules for Open Horizons. It produces planning artifacts, implementation guidance, validation output, and publication readiness evidence based on official Backstage documentation.

> [!NOTE]
> This skill depends on official Backstage documentation, preferably through `mcp-ecosystem` documentation tools. It may shell out to Python scripts under `.github/skills/backstage-plugin-builder/scripts/` and to package commands in the target Backstage workspace.

## When to invoke
- "Build a new Backstage frontend plugin for Open Horizons."
- "Create a backend module that extends an existing Backstage plugin."
- "Validate this Backstage plugin package before we publish it."
- "Generate a plugin ADR, strategy, and quality hooks."

## Prerequisites and context
- Plugin ID, package scope, target Backstage app path, target version policy, and plugin type are known.
- Plugin type is one of frontend, backend, backend module, catalog, scaffolder, search, auth, permission, TechDocs, common, or node package.
- Official docs are checked through `mcp-ecosystem` or fallback references in `.github/skills/backstage-plugin-builder/references/`.
- User approval is available before creating artifacts, modifying packages, or adding hooks.

## Procedure

### Step 1: Confirm scope and missing facts
Ask only for facts required to proceed:
- [ ] Plugin ID and package scope.
- [ ] Target path under the Backstage monorepo.
- [ ] Plugin type and extension points.
- [ ] Audience: internal, private package, open source, or community candidate.
- [ ] External systems, auth needs, configuration, and data sensitivity.

### Step 2: Load official documentation evidence
- Read `.github/skills/backstage-plugin-builder/references/mcp-doc-validation.md`.
- Read `.github/skills/backstage-plugin-builder/references/official-docs.md`.
- Load the type-specific reference, such as `.github/skills/backstage-plugin-builder/references/frontend-plugin.md` or `.github/skills/backstage-plugin-builder/references/backend-module.md`.
- If MCP documentation lookup fails, run:

```bash
python .github/skills/backstage-plugin-builder/scripts/validate_official_docs.py
```

### Step 3: Confirm before artifact creation
```text
Backstage plugin artifact summary:
- Plugin ID:
- Plugin type:
- Target path:
- Artifacts or package files to create/update:
Proceed with creating or updating plugin artifacts? (y/n)
```

> [!IMPORTANT]
> Only proceed with creating planning artifacts, package files, hooks, or publication assets if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the plan and stop.

### Step 4: Generate planning artifacts when approved
```bash
python .github/skills/backstage-plugin-builder/scripts/create_backstage_plugin_artifacts.py \
  --plugin-id my-plugin \
  --plugin-type frontend \
  --audience internal \
  --target-version 1.39.0 \
  --output <output-dir>
```

### Step 5: Validate the plugin package
```bash
python .github/skills/backstage-plugin-builder/scripts/validate_backstage_plugin.py <plugin-dir>
python .github/skills/backstage-plugin-builder/scripts/validate_backstage_plugin.py <plugin-dir> --run
```

Run package commands only if they exist in the target `package.json`:

```bash
yarn lint
yarn tsc
yarn test
yarn build
npm pack --dry-run
```

### Step 6: Generate optional quality hooks
```bash
python .github/skills/backstage-plugin-builder/scripts/generate_quality_hooks.py --root .
```

Use publication references only when the plugin is generic enough and the user requested publication. Do not promise community acceptance.

## Risk classification
| Severity | Meaning |
|---|---|
| High | Plugin uses stale Backstage APIs, bypasses extension points, exposes secrets, or changes auth/permission behavior unsafely. |
| Medium | Missing tests, docs, package metadata, config schema, or validation evidence. |
| Low | Naming, README, or publication polish gaps. |

## Limits

- Do not use this skill for: deploying Backstage itself (use backstage-deployment), configuring Codespaces for Golden Paths (use codespaces-golden-paths), or general Markdown writing (use markdown-writer).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Official docs lookup unavailable | State the failure and use `validate_official_docs.py` plus local references. |
| Plugin type is unclear | Ask one targeted question and do not scaffold until resolved. |
| Validation script fails | Report missing files, scripts, or package metadata and fix the smallest set. |
| Package command missing | Mark it not applicable rather than inventing a new toolchain. |

## Output template

Return exactly this structure:
```markdown
# Backstage Plugin Build Report

## Scope
- Plugin ID:
- Type:
- Target path:

## Documentation Evidence
| Source | Result |
|---|---|

## Artifacts
| File | Purpose |
|---|---|

## Validation
| Command | Result |
|---|---|

## Risks
| Severity | Finding | Fix |
|---|---|---|
```

## Quality gate
- [ ] Official Backstage documentation freshness is checked or fallback evidence is recorded.
- [ ] User confirmation is captured before creating or updating artifacts.
- [ ] Type-specific reference guidance is applied.
- [ ] Validation scripts and available package checks pass or failures are documented.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.

---
name: folder-structure-blueprint-generator
description: >-
  Analyze a repository and generate Project_Folders_Structure_Blueprint.md with detected
  technologies, folder purposes, naming conventions, file placement patterns, navigation guidance,
  build outputs, and optional structure templates. Use this skill when the user asks for a project
  folder structure blueprint, repository organization map, architecture directory guide, monorepo
  or microservices structure analysis, or file placement conventions.
---

<!-- Generated from harness/github-copilot/skills/folder-structure-blueprint-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Folder structure blueprint generator

Analyze a project tree, detect its technology and architecture signals, and produce a concrete `Project_Folders_Structure_Blueprint.md` that explains how the repository is organized and how future files should be placed.

## When to invoke

- "Create a project folder structure blueprint."
- "Document this repository's directory structure."
- "Show where new features, tests, and configuration should go."
- "Analyze our monorepo or microservices folder layout."
- "Generate Project_Folders_Structure_Blueprint.md."

## Blueprint controls

Use these variables as user-facing options when the request specifies them; otherwise auto-detect from the repository.

| Variable | Values | Use |
| --- | --- | --- |
| `PROJECT_TYPE` | `Auto-detect`, `.NET`, `Java`, `React`, `Angular`, `Python`, `Node.js`, `Flutter`, `Other` | Select the primary technology lens. |
| `INCLUDES_MICROSERVICES` | `Auto-detect`, `true`, `false` | Decide whether to describe repeated service boundaries. |
| `INCLUDES_FRONTEND` | `Auto-detect`, `true`, `false` | Decide whether to include UI, asset, route, and style organization. |
| `IS_MONOREPO` | `Auto-detect`, `true`, `false` | Decide whether to document workspace and cross-project relationships. |
| `VISUALIZATION_STYLE` | `ASCII`, `Markdown List`, `Table` | Choose the directory visualization format. |
| `DEPTH_LEVEL` | `1` through `5` | Limit how many directory levels receive detailed documentation. |
| `INCLUDE_FILE_COUNTS` | `true`, `false` | Include per-directory file statistics and complexity concentration. |
| `INCLUDE_GENERATED_FOLDERS` | `true`, `false` | Include or exclude generated folders such as `bin/`, `obj/`, `node_modules/`, `dist/`, and `build/`. |
| `INCLUDE_FILE_PATTERNS` | `true`, `false` | Document naming and placement rules for configuration, models, DTOs, services, interfaces, tests, and docs. |
| `INCLUDE_TEMPLATES` | `true`, `false` | Add templates for new features, components, services, and tests. |

## Detection signals

| Area | Look for | Record in the blueprint |
| --- | --- | --- |
| `.NET` | `.sln`, `.csproj`, `.fsproj`, `.vbproj`, `Directory.Build.props`, `global.json` | Solution organization, project references, target frameworks, `bin/`, `obj/`, resources, test projects, NuGet management. |
| `Java` | `pom.xml`, `build.gradle`, `settings.gradle`, `src/main`, `src/test` | Package hierarchy, Maven or Gradle modules, resources, properties files, domain vs technical packages. |
| `React` / `Angular` | `package.json`, `angular.json`, `react-scripts`, `next.config.js`, `vite.config.*`, `src/components`, `src/pages` | Component, routing, state, API client, assets, CSS/SCSS, theme, and module patterns. |
| `Python` | `requirements.txt`, `setup.py`, `pyproject.toml`, `src/`, `tests/` | Package layout, module boundaries, test placement, tooling and virtual environment artifacts. |
| `Node.js` | `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `lerna.json`, `nx.json`, `turborepo.json` | CommonJS vs ESM, script organization, workspaces, utility scripts, configuration and environment patterns. |
| `Flutter` | `pubspec.yaml`, `lib/`, `android/`, `ios/` | Mobile app boundaries, platform folders, widget and asset organization. |
| Monorepo | Multiple project manifests, workspace configuration, root orchestration scripts, shared packages | Project relationships, shared dependency patterns, cross-project references, ownership boundaries. |
| Microservices | Service directories with repeated structures, service Dockerfiles, API gateway files, message broker config, service discovery | Service boundaries, deployment structure, shared libraries, inter-service communication. |
| Frontend | `wwwroot/`, `public/`, `static/`, `dist/`, `assets/`, `components/`, `modules/`, `pages/`, stylesheets | UI entry points, static asset conventions, style organization, route/page conventions. |

## Blueprint content

Create `Project_Folders_Structure_Blueprint.md` with these sections when evidence exists.

| Section | Required content |
| --- | --- |
| Structural overview | Detected project types, architecture style, organization principle by feature/layer/domain, repeated structural patterns, inferred rationale. |
| Directory visualization | Render the tree to `DEPTH_LEVEL` as `ASCII`, `Markdown List`, or `Table`; omit generated folders unless `INCLUDE_GENERATED_FOLDERS=true`. |
| Key directory analysis | For each important path: purpose, content types, ownership, conventions, and examples of files found there. |
| File placement patterns | Configuration, model/entity definitions, DTOs, schemas, business logic, services, interfaces, abstractions, tests, mocks, API docs, internal docs, and README distribution. |
| Naming and organization conventions | File case (`PascalCase`, `camelCase`, `kebab-case`), suffixes, prefixes, folder names, namespace/module mapping, imports, public vs internal API, co-location strategy. |
| Navigation and development workflow | Entry points, key config, where to add features/tests/configuration, dependency flow, dependency injection registration, common development tasks. |
| Build and output organization | Build script locations, pipeline files, task definitions, compiled output, distribution packages, development vs production output. |
| Technology-specific organization | `.NET` project files and assemblies, Java packages and resources, Node.js modules and scripts, UI components/state/routes/assets/styles. |
| Extension and evolution | Extension points, plugin folders, new modules/features, code splitting, scalability and refactoring patterns. |
| Structure enforcement | Validation scripts, lint rules, build checks, documentation practices, ADRs, and when the blueprint was last updated. |
| Content statistics | File counts, code distribution, and concentration areas when `INCLUDE_FILE_COUNTS=true`. |
| Structure templates | New feature, component, service, and test folder templates when `INCLUDE_TEMPLATES=true`. |

## Visualization patterns

| `VISUALIZATION_STYLE` | Format |
| --- | --- |
| `ASCII` | Use a tree with box-drawing characters and annotate each important directory inline. |
| `Markdown List` | Use nested bullets where each path has a short purpose statement. |
| `Table` | Use columns `Path`, `Purpose`, `Content Types`, and `Conventions`. |

Always mark generated directories explicitly if included. Common generated or vendor folders include `bin/`, `obj/`, `node_modules/`, `.next/`, `dist/`, `build/`, `coverage/`, `.venv/`, `target/`, `.gradle/`, `android/build/`, and `ios/Pods/`.

## Templates to emit

When `INCLUDE_TEMPLATES=true`, add concrete templates that fit observed conventions rather than generic scaffolds.

| Template | Must include |
| --- | --- |
| New feature template | Folder path, required source files, test path, route/API registration point, docs location. |
| New component template | Component directory, style/test/story files when the project uses them, export/import point. |
| New service template | Interface and implementation placement, dependency injection or module registration, configuration path. |
| New test structure | Unit, integration, fixtures, mocks, snapshots, and test resource locations. |

## Gotchas

- **Do not infer conventions from generated folders**: `bin/`, `obj/`, `node_modules/`, `dist/`, and `build/` reflect tools, not project architecture.
- **Do not flatten monorepos into one app**: document each package, app, service, and shared library boundary separately.
- **Do not invent rationale**: label rationale as inferred when it comes from structure rather than explicit docs.
- **Do not over-document every leaf folder**: focus detailed analysis on folders that guide future file placement.

## Technical index

Preserve these blueprint vocabulary items because they identify generated sections, project families, and file placement rules: `technology-agnostic`, `high-level`, `auto-generated`, `similar/repeated`, `solution/project`, `Compiled/built`, `Domain/Feature`, `Model/Entity`, `Namespace/Module`, `Import/reference`, `Import/using`, `Tools/scripts`, `Image/media`, `Page/view`, `Plugin/extension`, `JavaScript/TypeScript`, `JavaScript`, `TypeScript`, `Maven/Gradle`, `android/ios`, `npm/yarn`, `styled-components`, `feature-specific`, `file/folder`, `naming/location`, `namespaces/modules`, and `projects/files`.

## Output template

```markdown
# Project_Folders_Structure_Blueprint

**Generated:** <YYYY-MM-DD>
**Detected project type(s):** <PROJECT_TYPE evidence>
**Monorepo:** <yes/no and evidence>
**Microservices:** <yes/no and evidence>
**Frontend:** <yes/no and evidence>
**Visualization:** <VISUALIZATION_STYLE>, depth <DEPTH_LEVEL>

## Structural overview
<architecture and organization principles>

## Directory visualization
<ASCII tree, Markdown list, or table>

## Key directory analysis
| Path | Purpose | Content types | Conventions | Evidence |
| --- | --- | --- | --- | --- |
| `<path>` | <purpose> | <file types> | <rules> | <files inspected> |

## File placement patterns
| File type | Place in | Naming pattern | Notes |
| --- | --- | --- | --- |

## Naming and organization conventions
<observed rules>

## Navigation and development workflow
<entry points and common tasks>

## Build and output organization
<build inputs and generated outputs>

## Technology-specific organization
<.NET, Java, React, Angular, Python, Node.js, Flutter, or Other details>

## Extension and evolution
<templates and extension guidance>

## Structure enforcement
<checks, docs, ADRs, and maintenance guidance>
```

## Quality gate

- [ ] `PROJECT_TYPE`, `INCLUDES_MICROSERVICES`, `INCLUDES_FRONTEND`, and `IS_MONOREPO` are either user-specified or supported by file evidence.
- [ ] `VISUALIZATION_STYLE` and `DEPTH_LEVEL` are honored in the rendered structure.
- [ ] Generated folders are included only when `INCLUDE_GENERATED_FOLDERS=true`, and are labeled as generated.
- [ ] File placement rules cover configuration, models/entities, DTOs, business logic, interfaces, tests, and documentation when those categories exist.
- [ ] Technology-specific sections are included only for detected or requested stacks.
- [ ] Templates are included only when `INCLUDE_TEMPLATES=true` and match observed naming conventions.
- [ ] The final artifact is a concrete `Project_Folders_Structure_Blueprint.md`, not a prompt asking someone else to create it.

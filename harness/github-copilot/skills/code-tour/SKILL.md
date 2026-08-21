---
name: "code-tour"
description: >-
  Create CodeTour .tour JSON files that guide a persona through real repository files, directories, line numbers, selections, patterns, URIs, views, and VS Code commands. Use when asked to create a tour, make a code tour, generate an onboarding tour, PR review tour, bug tour, RCA tour, architecture tour, vibe check, contributor guide, or structured code walkthrough.
---

# Code tour

Create a persona-targeted CodeTour `.tour` file in `.tours/` that links to verified repository files, line numbers, directories, selections, patterns, URIs, views, or VS Code commands and validates against the bundled schema and validator.

## When to invoke

- "Create a tour for this repository."
- "Make an onboarding code tour for a new joiner."
- "Generate a PR review tour for this branch."
- "Explain how this feature works as a CodeTour."
- "Make a vibe check, bug tour, RCA tour, architecture tour, or contributor guide."

## Prerequisites and context

- CodeTour files live in `.tours/` and use the VS Code CodeTour extension: https://github.com/microsoft/codetour.
- Only create `.tour` JSON files. Never create, modify, or scaffold source files, `.vscode/settings.json`, docs, or any other files unless the user explicitly changes the task.
- Every path and line number in the tour must be verified by reading the actual file.
- Use `references/codetour-schema.json` as the authoritative field list.
- Run `python harness/github-copilot/skills/code-tour/scripts/validate_tour.py .tours/<name>.tour --repo-root .` after writing a tour in this repository. In installed skill locations, the same script may be under `~/.agents/skills/code-tour/scripts/validate_tour.py`.

## Progressive disclosure and bundled resources

Read or execute bundled resources only when needed.

| Resource | Use it when |
| --- | --- |
| `references/codetour-schema.json` | Verifying every root or step field, type, and allowed shape before writing JSON. |
| `references/examples.md` | Studying `commands`, `selection`, `view`, `pattern`, `isPrimary`, `nextTour`, and multi-tour series techniques. |
| `scripts/validate_tour.py` | Validating JSON, file/directory existence, line bounds, pattern matches, `nextTour` cross-references, and narrative arc. |
| `scripts/generate_from_docs.py` | The user asks to generate from README or docs; create a skeleton, then fill every `[TODO: ...]` from real code. |

Useful commands:

```bash
python harness/github-copilot/skills/code-tour/scripts/generate_from_docs.py --persona new-joiner --output .tours/skeleton.tour
python harness/github-copilot/skills/code-tour/scripts/validate_tour.py .tours/<name>.tour --repo-root .
python ~/.agents/skills/code-tour/scripts/generate_from_docs.py --persona new-joiner --output .tours/skeleton.tour
python ~/.agents/skills/code-tour/scripts/validate_tour.py .tours/<name>.tour --repo-root .
```

## Procedure

1. Discover the repo before asking questions: list the root, read the README, check key config files, map folders 1-2 levels deep, identify languages and frameworks, and find entry points.
2. Infer persona, depth, focus, `ref`, `isPrimary`, `nextTour`, `uri`, required files, and requested customizations from the user's first message. Ask only when the target bug, feature, or required file cannot be inferred.
3. Read every planned file and directory. Verify every `file`, `directory`, `line`, `selection`, and `pattern` before writing.
4. Write one `.tours/<persona>-<focus>.tour` JSON file. Use kebab-case names such as `onboarding-new-joiner.tour`, `bug-fixer-payment-flow.tour`, `architect-overview.tour`, `vibecoder-quickstart.tour`, `pr-review-auth-refactor.tour`, `security-auth-boundaries.tour`, `concept-dependency-injection.tour`, or `rca-login-outage.tour`.
5. Validate with `scripts/validate_tour.py`. Fix every error. Use judgment on warnings, but never ignore invalid paths, invalid JSON, out-of-bounds lines, of-bounds validation wording, unmatched patterns, or broken `nextTour` references.
6. Summarize the tour path, persona, coverage, `vscode.dev` URL for public repos, suggested follow-up tours, and any requested files that did not exist.

## Repository discovery

Start with entry points; do not read everything in large repositories.

| Stack | Entry points to read first |
| --- | --- |
| Node.js / TS | `index.js`, `index.ts`, `server.js`, `app.js`, `src/main.ts`, `package.json` scripts |
| Python | `main.py`, `app.py`, `__main__.py`, `manage.py`, `app/__init__.py` |
| Go | `main.go`, `cmd/<name>/main.go`, `internal/` |
| Rust | `src/main.rs`, `src/lib.rs`, `Cargo.toml` |
| Java / Kotlin | `*Application.java`, `src/main/java/.../Main.java`, `build.gradle` |
| Ruby | `config/application.rb`, `config/routes.rb`, `app/controllers/application_controller.rb` |
| PHP | `index.php`, `public/index.php`, `bootstrap/app.php` |

| Repo type | Emphasize | Typical anchor files |
| --- | --- | --- |
| Service / API | Request lifecycle, auth, error contracts | router, middleware, handler, schema |
| Library / SDK | Public API surface, extension points, versioning | index/exports, types, changelog |
| CLI tool | Command parsing, config loading, output formatting | main, `commands/`, config |
| Monorepo | Package boundaries, shared contracts, build graph | root `package.json`, `pnpm-workspace`, `shared/`, `packages/` |
| Framework | Plugin system, lifecycle hooks, escape hatches | `core/`, `plugins/`, lifecycle |
| Data pipeline | Source → transform → sink, schema ownership | `ingest/`, `transform/`, `schema/`, dbt models |
| Frontend app | Component hierarchy, state management, routing | `pages/`, `store/`, router, api |

For repos with 100+ files: read entry points and README, build a map of the top 5-7 modules, deeply read only the 2-3 modules that matter to the persona, mention out-of-scope areas in the intro, and use `directory` steps for areas you mapped but did not read. A focused 10-step tour beats a scattered 25-step tour.

## Intent and persona mapping

| User says | Persona | Depth | Tour focus |
| --- | --- | --- | --- |
| "tour for this PR", "PR review", "#123" | `pr-reviewer` | standard | Add `uri` step for the PR, set `ref` for the branch, cover changed files first, then unchanged-but-critical files, close with reviewer checklist. |
| "why did X break", "RCA", "incident" | `rca-investigator` | standard | Causality chain, side effects, race conditions, observability, not happy path. |
| "debug X", "bug tour", "find the bug" | `bug-fixer` | standard | User action → trigger → fault points → tests. |
| "onboarding", "new joiner", "ramp up" | `new-joiner` | standard | Directories, setup, business context, service boundaries. |
| "quick tour", "vibe check", "just the gist" | `vibecoder` | quick | 5-8 steps, entry point, request flow, main modules. |
| "explain how X works", "feature tour" | `feature-explainer` | standard | UI → API → backend → storage, feature flags, edge cases. |
| "architecture", "tech lead", "system design" | `architect` | deep | Boundaries, design tradeoffs, risk hotspots. |
| "security", "auth review", "trust boundaries" | `security-reviewer` | standard | Auth flow, input validation, secret handling, sensitive sinks. |
| "refactor", "safe to extract?" | `refactorer` | standard | Seams, hidden dependencies, coupling hotspots, safe extraction order. |
| "performance", "bottlenecks", "slow path" | `performance-optimizer` | standard | Hot path, N+1, I/O, caches. |
| "contributor", "open source onboarding" | `external-contributor` | quick | Safe areas, conventions, architecture landmines. |
| "concept", "explain pattern X" | `concept-learner` | standard | Concept → implementation → rationale. |
| "test coverage", "where to add tests" | `test-writer` | standard | Contracts, seams, coverage gaps. |
| "how do I call the API" | `api-consumer` | standard | Public surface, auth, error semantics. |

Honor explicit customizations: required files such as `src/auth.ts` and `config/db.yml`, tags or commits such as `v2.3.0` and `abc123`, PR URLs, `nextTour` titles, `isPrimary: true`, terminal focus via `commands: ["workbench.action.terminal.focus"]`, and requested depth or step count.

## Tour JSON structure

```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "Descriptive Title — Persona / Goal",
  "description": "One sentence: who this is for and what they'll understand after.",
  "ref": "main",
  "isPrimary": false,
  "nextTour": "Title of follow-up tour",
  "when": "workspaceFolders[0].name === 'api'",
  "stepMarker": "CT",
  "steps": []
}
```

Omit fields that do not apply. `when` is a JavaScript expression evaluated at runtime; it controls whether a tour is shown. `stepMarker` uses source comments such as `// CT` so CodeTour can find anchors when line numbers shift; do not suggest it unless the user asks because it requires editing source files.

## Step design

All step types: `content`, `directory`, `file` + `line`, `selection`, `pattern`, `uri`, `view`, and `commands`.

| Situation | Step type | Rules |
| --- | --- | --- |
| Intro or closing | `content` | At most 2 content-only steps. Step 1 must not be content-only. |
| Orient to a folder | `directory` | Path relative to repo root, no leading `/` or `./`, confirmed to exist. |
| Highlight one line | `file` + `line` | Workhorse step. Verify file exists and line is in bounds. |
| Explain a function or class body | `selection` | Use when a block matters more than one line. |
| Anchor volatile code | `pattern` | Regex must compile and match a real line in the file. |
| Provide PR, issue, or doc context | `uri` | Complete real URL beginning with `https://`; examples include `https://{example-url}`. |
| Focus a VS Code panel | `view` | Use sparingly for Explorer, terminal, or source-control context. |
| Run VS Code commands | `commands` | VS Code commands only; not arbitrary shell commands. |

### Narrative arc

1. Orientation: must be a `file`, `directory`, or `uri` step, never content-only. Use `README.md` line 1 or a key directory and put welcome text in the description. A content-only first step renders blank in VS Code CodeTour.
2. High-level map: 1-3 directory or URI steps for major modules.
3. Core path: file/line, selection, pattern, and URI steps that tell the specific story.
4. Closing: a content step that says what the reader can now do, what to avoid, and 2-3 follow-up tours. If `nextTour` is set, reference it by exact title.

### Step count calibration

| Depth | Total steps | Core path steps | Use for |
| --- | --- | --- | --- |
| Quick | 5-8 | 3-5 | Vibecoder, external-contributor fast path |
| Standard | 9-13 | 6-9 | Most personas |
| Deep | 14-18 | 10-13 | Architect, RCA, detailed tradeoffs |

| Repo size | Recommended standard depth |
| --- | --- |
| Tiny, <20 files | 5-8 steps |
| Small, 20-80 files | 8-11 steps |
| Medium, 80-300 files | 10-13 steps |
| Large, 300+ files | 12-15 steps scoped to the relevant subsystem |

Use the SMIG formula in every description: Situation, Mechanism, Implication, Gotcha. Tell the persona what matters, how it works, why it matters for their goal, and what a smart reader might get wrong.

## Real-world references

Fetch a real `.tour` when you need a concrete example instead of writing from memory.

| What to study | URL |
| --- | --- |
| `directory` + `file+line` contributor onboarding | https://github.com/coder/code-server/blob/main/.tours/contributing.tour |
| `selection` + `file+line` + intro content step | https://github.com/a11yproject/a11yproject.com/blob/main/.tours/code-tour.tour |
| Minimal tutorial with tight `file+line` narration | https://github.com/lostintangent/rock-paper-scissors/blob/master/main.tour |
| Search for more `.tour` files | https://github.com/search?q=path%3A**%2F*.tour+&type=code |

Raw content tip: prefix `raw.githubusercontent.com` and drop `/blob/` for raw JSON access. For public repositories, users can open tours at `https://vscode.dev/github.com/<owner>/<repo>`.

## Limits

| Request | Reality |
| --- | --- |
| Auto-advance to next step after X seconds | Not supported. Navigation is manual; there is no timer, delay, or autoplay step mechanic. |
| Embed a video or GIF in a step | Not supported. Descriptions are Markdown text only. |
| Run arbitrary shell commands | Not supported. `commands` executes VS Code commands, for example `workbench.action.terminal.focus`, not shell commands. |
| Branch or conditional next step | Not supported. Tours are linear. `when` controls whether a tour is shown, not which step follows. |
| Show a first step without opening a file | Partially supported, but do not do it. Step 1 needs a file, directory, or URI anchor. |

`isPrimary: true` plus `.vscode/settings.json` containing `{ "codetour.promptForPrimaryTour": true }` prompts on repo open, but this skill must not create or modify `.vscode/settings.json` unless the user explicitly requests it. Omit `ref` for tours intended to appear on any branch.

## Gotchas

- **Line number guessing is forbidden**: a tour pointing to the wrong line is worse than no tour.
- **No absolute or `./` paths**: `file` and `directory` paths must be relative to repo root.
- **A content-only first step renders blank**: anchor step 1 to a real file, directory, or URI.
- **A file listing is not a tour**: each step should depend on the previous step and serve the persona's goal.
- **`nextTour` must match exactly**: it must equal the `title` of another `.tour` file in `.tours/`.
- **Commands are not shell commands**: use `commands` only for VS Code command IDs.
- **Do not hallucinate files**: if a user-requested file does not exist, report it explicitly.

## Schema vocabulary and exact field examples

Keep these CodeTour field examples available when the user requests them: `"file"`, `"directory"`, `"directory": "src"`, `"file": "README.md", "line": 1`, `"ref"`, `"ref": "v2.3.0"`, `"isPrimary": true`, `"nextTour": "Security Review"`, `"stepMarker": "CT"`, `// <stepMarker>`, and `"commands": ["workbench.action.terminal.focus"]`.

Use these exact package and workflow terms when relevant: `.tours/<name>.tour`, `<persona>-<focus>.tour`, `scripts/`, `skills/code-tour/scripts/generate_from_docs.py`, README/docs, language/framework discovery, Flask/FastAPI, index.js/ts, package.json/pnpm-workspace, branch/tag/commit refs, tour-level fields, real-world examples, persona-specific auto-launching, intro/closing steps, function/class selection, deep-dive tours, end-to-end feature tours, ramp-up onboarding, step-by-step walkthroughs, by-line review, pattern/gotcha descriptions, non-obvious failure modes, non-existent files, out-of-bounds lines, and the CRITICAL rule that only `.tour` JSON files are created.

## Output template

```markdown
## CodeTour result - <tour title>

**Status:** created | blocked
**File:** `.tours/<persona>-<focus>.tour`
**Persona:** <persona>
**Depth:** quick | standard | deep

### Coverage
| Step range | Purpose | Anchors |
| --- | --- | --- |
| 1 | Orientation | `<file or directory>` |
| 2-<n> | Core path | `<files, directories, patterns, selections, URIs>` |
| <n> | Closing | content |

### Validation
- `python harness/github-copilot/skills/code-tour/scripts/validate_tour.py .tours/<name>.tour --repo-root .`: pass | fail
- Paths and line numbers verified: pass | fail
- Patterns matched: pass | fail | not used
- `nextTour` cross-reference: pass | fail | not used

### Share and follow-up
- Public URL: `https://vscode.dev/github.com/<owner>/<repo>` or not available
- Suggested follow-up tours: <2-3 titles>
- Missing requested files: <none or list>
```

## Quality gate

- [ ] Only one `.tour` JSON file was created or modified under `.tours/`.
- [ ] Every root field and step field conforms to `references/codetour-schema.json`.
- [ ] Every `file` path is relative to repo root, has no leading `/` or `./`, was read, and exists.
- [ ] Every `line` number is verified and within bounds.
- [ ] Every `directory` path is relative to repo root and exists.
- [ ] Every `pattern` regex compiles and matches a real line.
- [ ] Every `uri` is a complete real URL beginning with `https://`.
- [ ] `ref` is a real branch, tag, or commit when set.
- [ ] `nextTour` exactly matches another tour title when set.
- [ ] Step 1 has a file, directory, or URI anchor.
- [ ] The tour has a narrative arc and at most 2 content-only steps.
- [ ] Every description follows SMIG and serves the selected persona.
- [ ] Step count matches requested depth and repo size.
- [ ] `scripts/validate_tour.py` was run and all errors were fixed.

## References

- [VS Code CodeTour extension](https://github.com/microsoft/codetour)
- [CodeTour schema URL](https://aka.ms/codetour-schema)
- [Code server contributing tour](https://github.com/coder/code-server/blob/main/.tours/contributing.tour)
- [A11y project code tour](https://github.com/a11yproject/a11yproject.com/blob/main/.tours/code-tour.tour)
- [Rock paper scissors main tour](https://github.com/lostintangent/rock-paper-scissors/blob/master/main.tour)
- [GitHub Code Search for tours](https://github.com/search?q=path%3A**%2F*.tour+&type=code)

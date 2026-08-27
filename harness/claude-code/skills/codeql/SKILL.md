---
name: codeql
description: >-
  Configure and run CodeQL code scanning with GitHub Actions workflows, default or advanced setup,
  CodeQL CLI databases, SARIF uploads, custom query packs, monorepo categories, build modes, and
  alert triage. Use this skill when the user asks to create or customize codeql.yml, choose CodeQL
  setup, configure a language matrix, run codeql database create or database analyze, upload
  SARIF, troubleshoot CodeQL builds, or interpret code scanning alerts.
---

<!-- Generated from harness/github-copilot/skills/codeql/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# CodeQL code scanning

Set up, run, and troubleshoot CodeQL analysis through GitHub Actions or the CodeQL CLI, producing a working workflow, local commands, SARIF upload path, and alert triage guidance.

## When to invoke

- "Create a CodeQL workflow for this repository."
- "Should we use default setup or advanced setup for code scanning?"
- "Run CodeQL CLI locally and upload SARIF."
- "Troubleshoot this CodeQL build-mode failure."
- "Configure CodeQL for a monorepo with custom query packs."

## Prerequisites and context

- GitHub code scanning must be available for the repository.
- Advanced setup uses `.github/workflows/codeql.yml` and may use `.github/codeql/codeql-config.yml`.
- CLI uploads require `GITHUB_TOKEN` with `security-events: write` plus repository, ref, and commit metadata.
- Use the CodeQL bundle from https://github.com/github/codeql-action/releases, not a standalone CLI download, so bundled queries and precompiled packs match the CLI.

## Supported languages

| Language | Standard identifier | Alternatives | Build notes |
| --- | --- | --- | --- |
| C/C++ | `c-cpp` | `c`, `cpp` | compiled; choose `none`, `autobuild`, or `manual`. |
| C# | `csharp` | — | compiled; watch `/p:EmitCompilerGeneratedFiles=true` conflicts with `.sqlproj` or legacy projects. |
| Go | `go` | — | usually autobuilds through standard Go tooling. |
| Java/Kotlin | `java-kotlin` | `java`, `kotlin` | Kotlin no-build mode may need default setup disabled and re-enabled to switch to `autobuild`. |
| JavaScript/TypeScript | `javascript-typescript` | `javascript`, `typescript` | alternative identifiers still analyze both JS and TS. |
| Python | `python` | — | no build mode required. |
| Ruby | `ruby` | — | no build mode required. |
| Rust | `rust` | — | build mode can matter for extraction completeness. |
| Swift | `swift` | — | compiled; runner and build environment matter. |
| GitHub Actions | `actions` | — | analyzes workflow code. |

## GitHub Actions workflow

1. Choose setup type.
   - **Default setup**: enable in repository Settings → Advanced Security → CodeQL analysis. Best for fast onboarding; uses `none` build mode for most languages.
   - **Advanced setup**: commit `.github/workflows/codeql.yml` for full control over triggers, build modes, query suites, path filters, custom packs, and monorepos. Disable default setup before switching to advanced.
2. Configure triggers. Use `push`, `pull_request`, `schedule`, and `merge_group` when merge queues are enabled. `paths-ignore` controls whether the workflow runs, not which files are analyzed.
3. Set least-privilege permissions: `security-events: write`, `contents: read`, and `actions: read` for private repositories using `codeql-action`.
4. Use a matrix with `fail-fast: false` and one row per language/build-mode pair.
5. Initialize, build if needed, analyze, and set a unique `category` such as `/language:${{ matrix.language }}` or `/language:${{ matrix.language }}/component:frontend`.

```yaml
name: CodeQL
on:
  push:
    branches: [main, protected]
  pull_request:
    branches: [main]
  schedule:
    - cron: '30 6 * * 1'
  merge_group:

permissions:
  security-events: write
  contents: read
  actions: read

jobs:
  analyze:
    name: Analyze (${{ matrix.language }})
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - language: javascript-typescript
            build-mode: none
          - language: python
            build-mode: none
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v4
        with:
          languages: ${{ matrix.language }}
          build-mode: ${{ matrix.build-mode }}
          queries: security-extended
          dependency-caching: true
      - if: matrix.build-mode == 'manual'
        run: |
          make bootstrap
          make release
      - uses: github/codeql-action/analyze@v4
        with:
          category: "/language:${{ matrix.language }}"
```

## Configuration choices

| Need | Configuration |
| --- | --- |
| Broader security coverage | `queries: security-extended`. |
| Security plus quality checks | `queries: security-and-quality`. |
| Custom query packs | `packs: my-org/my-security-queries@1.0.0` or `codeql/javascript-queries:AlertSuppression.ql`. |
| Monorepo component isolation | Distinct `category` values and `.github/codeql/codeql-config.yml`. |
| Analyze only selected paths | `paths:` and `paths-ignore:` in `.github/codeql/codeql-config.yml`. |
| Dependency reuse | `dependency-caching: true` on `github/codeql-action/init@v4`. |
| Version stability | Pin `github/codeql-action/init@v4`, `github/codeql-action/autobuild@v4`, and `github/codeql-action/analyze@v4`; pin full commit SHAs for maximum security. |

```yaml
paths:
  - apps/
  - services/
paths-ignore:
  - '**/test/**'
  - node_modules/
queries:
  - uses: security-extended
packs:
  javascript-typescript:
    - my-org/my-custom-queries
```

## CodeQL CLI workflow

```bash
export PATH="$HOME/codeql:$PATH"
codeql resolve packs
codeql resolve languages

codeql database create codeql-db \
  --language=javascript-typescript \
  --source-root=src

codeql database create codeql-dbs \
  --db-cluster \
  --language=java,python \
  --command=./build.sh \
  --source-root=src

codeql database analyze codeql-db \
  javascript-code-scanning.qls \
  --format=sarif-latest \
  --sarif-category=javascript \
  --output=results.sarif

codeql github upload-results \
  --repository=owner/repo \
  --ref=refs/heads/main \
  --commit=<commit-sha> \
  --sarif=results.sarif

codeql execute cli-server
```

Common suites are `<language>-code-scanning.qls`, `<language>-security-extended.qls`, and `<language>-security-and-quality.qls`. Use `--command` for compiled-language database creation. Use `--verbosity=progress++` and `--logdir=codeql-logs` for local debug logs.

## Alerts, logs, and limits

| Topic | Guidance |
| --- | --- |
| Severity | Standard severity is `Error`, `Warning`, or `Note`; security severity is `Critical`, `High`, `Medium`, or `Low` from CVSS and takes display precedence. |
| PR alerts | Alerts appear as check annotations on changed lines; checks fail by default for `error`, `critical`, or `high`. |
| False positives | Dismiss only with a documented reason for audit history. |
| GitHub Copilot Autofix | Review generated fixes carefully before committing; no Copilot subscription is required for CodeQL alert suggestions in PRs. |
| Logs | Review lines of code in codebase, lines extracted, extraction errors/warnings, and debug logging from workflow reruns. |
| SARIF | Use `--sarif-category` to split results; SARIF uploads have a 10 MB file size limit. |
| Runners | Small codebases need about 8 GB RAM and 2 cores; medium 16 GB and 4–8 cores; large 64 GB and 8 cores. All need SSD storage with at least 14 GB free. |

## Troubleshooting

| Problem | Resolution |
| --- | --- |
| Workflow not triggering | Verify `on:` event, branches, paths filters, and that the workflow exists on the target branch. |
| `Resource not accessible` | Add `security-events: write` and `contents: read`; add `actions: read` for private repos using `codeql-action`. |
| Autobuild failure | Switch to `build-mode: manual` and add explicit build commands between init and analyze. |
| No source code seen | Verify `--source-root`, language identifier, path config, and build command. |
| Fewer lines scanned than expected | Switch from `none` to `autobuild` or `manual`; verify the build compiles all source. |
| Cache miss every run | Confirm `dependency-caching: true` on `init`. |
| Out of disk or memory | Use larger runners, reduce scope with `paths`, or use `build-mode: none` where safe. |
| SARIF upload fails | Check `security-events: write`, `GITHUB_TOKEN`, SARIF size, `--sarif-category`, repository, ref, and commit SHA. |
| Two CodeQL workflows | Disable default setup or remove the old advanced workflow. |
| Slow analysis | Enable dependency caching, use `--threads=0`, reduce query suite scope, or split monorepo categories. |

## Progressive disclosure and bundled resources

Read bundled references only when the main skill is insufficient for the current task.

- `references/workflow-configuration.md`: triggers, schedules, `paths-ignore`, `db-location`, model packs, alert severity, merge protection, concurrency, config files.
- `references/cli-commands.md`: `database create`, `database analyze`, `upload-results`, `resolve packs`, `cli-server`, installation, CI integration.
- `references/sarif-output.md`: `sarifLog`, `result`, `location`, `region`, `codeFlow`, `fingerprint`, `suppression`, upload limits, third-party support, `precision`, `security-severity`.
- `references/compiled-languages.md`: `C/C++`, `C#`, `Java`, `Go`, `Rust`, `Swift`, `autobuild`, `build-mode`, hardware, dependency caching.
- `references/troubleshooting.md`: no source code, out of disk, out of memory, `403`, C# compiler, analysis too long, fewer lines, Kotlin, extraction errors, debug logging, SARIF upload, SARIF limits.
- `references/alert-management.md`: severity, security severity, CVSS, GitHub Copilot Autofix, dismissals, triage, PR alerts, data flow, merge protection, REST API.

## Technical index

Preserve these CodeQL reference search terms, commands, and troubleshooting labels when narrowing the workflow: `codeql.yml`, `codeql database create`, `github upload-results`, `config-file`, `packs:`, `my-org/my-queries`, `my-queries`, `per-component`, `per-language`, `documentation-only`, `auto-generated`, `re-run`, `re-enable`, `disk/memory`, `branches`, `trigger`, `analyze`, `installation`, `CI integration`, `concurrency`, `config file`, `dependency caching`, `hardware`, `model packs`, `merge protection`, `alert severity`, `security severity`, `severity`, `triage`, `dismiss`, `PR alerts`, `data flow`, `REST API`, `Copilot Autofix`, `C# compiler`, `Kotlin`, `debug logging`, `extraction errors`, `errors/warnings**`, `fewer lines`, `no source code`, `out of disk`, `out of memory`, `analysis too long`, `SARIF upload`, `SARIF limits`, and `upload limits`.

## Output template

```markdown
## CodeQL setup result

**Status:** configured | commands provided | blocked
**Mode:** default setup | advanced setup | CLI
**Languages:** <language identifiers>

### Files or commands
- `.github/workflows/codeql.yml`: <created/updated/not needed>
- `.github/codeql/codeql-config.yml`: <created/updated/not needed>
- CLI command: `<codeql ...>`

### Key settings
| Setting | Value | Reason |
| --- | --- | --- |
| `build-mode` | `<none/autobuild/manual>` | <why> |
| `queries` | `<suite or packs>` | <why> |
| `category` | `<category>` | <why> |

### Validation
- Workflow syntax: <checked/not checked>
- CodeQL init/analyze or CLI run: <pass/fail/not run>
- SARIF upload readiness: <pass/fail/not applicable>
```

## Quality gate

- [ ] Setup type is explicit: default, advanced, or CLI.
- [ ] Language identifiers use CodeQL-supported names or documented alternatives.
- [ ] Compiled languages have a deliberate `build-mode` and manual commands when needed.
- [ ] Workflow permissions include only required permissions, especially `security-events: write`.
- [ ] Query suites, packs, path filters, dependency caching, and categories are justified.
- [ ] CLI instructions use the CodeQL bundle, create a database, analyze it, and upload SARIF only with a valid `GITHUB_TOKEN`.
- [ ] Troubleshooting advice maps to the observed failure rather than generic rebuild advice.

## References

- [CodeQL Action releases](https://github.com/github/codeql-action/releases)

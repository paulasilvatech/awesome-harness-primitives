---
name: pytest-coverage
description: >-
  Run pytest with coverage, read annotated coverage output, identify uncovered lines, and add tests until Python code reaches 100% line coverage. Use this skill when the user asks to run pytest coverage, inspect cov_annotate files, cover missing lines, target a module with --cov, or improve test coverage to 100%.
---

# pytest coverage

## When to invoke

- "Run pytest with coverage and show what is missing."
- "Increase coverage for this module to 100%."
- "Open the cov_annotate output and cover the lines marked with !."
- "Run a targeted pytest coverage check for this test file."
- "Add tests for uncovered Python lines."

## Prerequisites and context

- Use the project's existing pytest setup; do not add a new test runner.
- Coverage output is generated into the `cov_annotate` directory.
- The goal is 100% line coverage for the requested code, unless the user explicitly sets a lower target.

## Coverage commands

| Scope | Command |
| --- | --- |
| Whole project | `pytest --cov --cov-report=annotate:cov_annotate` |
| Specific module | `pytest --cov=your_module_name --cov-report=annotate:cov_annotate` |
| Specific test file and module | `pytest tests/test_your_module.py --cov=your_module_name --cov-report=annotate:cov_annotate` |

Replace `your_module_name` and `tests/test_your_module.py` with the actual package, module, and test path from the repository.

## Procedure

1. Run the smallest coverage command that covers the user's target.
2. Open the `cov_annotate` directory after the command completes.
3. Skip annotated files that already show 100% source coverage.
4. For each file below 100%, open the matching file in `cov_annotate` and review the annotated source.
5. Treat every line that starts with `!` as an uncovered line.
6. Add or update tests that execute the missing behavior instead of deleting code or weakening assertions.
7. Re-run the same coverage command and repeat until all requested files reach 100% line coverage.

## Annotation guide

| Marker | Meaning | Action |
| --- | --- | --- |
| `!` at line start | The line is not covered by tests. | Add a test that executes this line. |
| No uncovered marker and 100% coverage | The file's source lines are fully covered. | Do not spend time opening or changing it. |
| File under 100% coverage | At least one source line still needs coverage. | Review the corresponding annotated file. |

## Test-writing rules

- Cover behavior through public functions, CLI entry points, or documented integration seams when possible.
- Prefer focused tests that exercise the uncovered branch, error path, or edge case directly.
- Keep existing assertions meaningful; do not raise coverage with tests that only import modules.
- Preserve the existing test style, fixtures, and naming conventions.
- Re-run the targeted coverage command after every meaningful test change.

## Gotchas

- **Annotated output is the source of truth for missing lines**: inspect `cov_annotate`, not just the terminal summary.
- **Do not open fully covered files**: the existing workflow explicitly skips files that already report 100% source coverage.
- **Do not chase unrelated modules**: when the user specified `--cov=your_module_name`, keep the coverage loop scoped to that module.

## Output template

```markdown
### pytest coverage result

**Status:** complete | needs tests | blocked
**Command:** `<pytest coverage command>`
**Coverage target:** 100% line coverage for <project/module/file>

| File | Starting coverage | Uncovered lines reviewed | Final coverage | Notes |
| --- | --- | --- | --- | --- |
| `<source file>` | `<percent>` | `<line numbers or none>` | `<percent>` | `<tests added or reason blocked>` |

**Tests changed**
- `<test file>`: <behavior covered>

**Validation**
- `<pytest coverage command>`: pass | fail
```

## Quality gate

- [ ] The pytest command includes `--cov-report=annotate:cov_annotate`.
- [ ] The selected command is scoped to the user's requested project, module, or test file.
- [ ] The `cov_annotate` directory was inspected after coverage ran.
- [ ] Every relevant line beginning with `!` was mapped to a test or documented as blocked.
- [ ] Files already at 100% source coverage were skipped.
- [ ] Added tests exercise behavior and assertions, not imports alone.
- [ ] The final coverage command was re-run after test changes.
- [ ] Requested files reached 100% line coverage, or the remaining blocker is explicitly reported.

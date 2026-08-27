---
name: autoresearch
description: >-
  Run an autonomous iterative experimentation loop for programming tasks with measurable outcomes.
  Use when the user asks for autonomous improvement, iterative optimization, experiment loops,
  auto research, performance tuning, automated experimentation, hill climbing, trying changes
  automatically, optimizing code, benchmarks, coverage, latency, throughput, build time, memory
  use, or other metric-driven coding work.
license: MIT
metadata:
  author: luiscantero
  compatibility: Requires git, a git repository, and terminal access to run commands.
  inspired-by: "https://github.com/karpathy/autoresearch"
---

<!-- Generated from harness/github-copilot/skills/autoresearch/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Autoresearch experimentation loop

Use this skill to turn a measurable programming goal into a git-backed autonomous loop that creates experiments, runs the metric command, keeps improvements, reverts regressions, and reports a research journal.

## When to invoke

- "Run autonomous experiments to improve this metric."
- "Optimize code by trying changes automatically."
- "Use an autoresearch loop for performance tuning, coverage, latency, throughput, memory, or build time."
- "Hill climb this benchmark or test score."
- "Keep iterating until the experiment budget is reached."

## Prerequisites and context

- Requires git, a git repository, and terminal access.
- Requires a measurable metric with an exact command, extraction rule, and direction.
- Inspired by Karpathy's autoresearch: <https://github.com/karpathy/autoresearch>.
- Do not use for one-shot tasks, simple bug fixes, code review, or tasks without a measurable metric.

## Setup parameters

Before any experiment, collect and confirm every parameter. Do not assume or skip any item.

| Parameter | Prompt | Record as |
| --- | --- | --- |
| Goal | "What are you trying to improve or optimize?" Examples: execution time, memory usage, binary size, test pass rate, code coverage, API response latency, throughput, error rate, benchmark score, build time, bundle size, lines of code, cyclomatic complexity. | goal |
| Metric | "How do we measure success? What exact command produces the metric?" Collect command, numeric extraction rule, and direction. | `METRIC_COMMAND`, `METRIC_EXTRACTION`, `METRIC_DIRECTION` |
| Scope | "Which files or directories am I allowed to modify, and which are off limits?" | `IN_SCOPE_FILES`, `OUT_OF_SCOPE_FILES` |
| Constraints | Ask for time budget, no new dependencies, tests, public API compatibility, backward compatibility, VRAM/memory limit, and complexity limits. | `CONSTRAINTS` |
| Budget | "How many experiments should I run, or should I keep going until stopped?" | `MAX_EXPERIMENTS` or `unlimited` |
| Simplicity | Default: all else equal, simpler is better; removing code while preserving or improving the metric is excellent. | `SIMPLICITY_POLICY` |

Confirm setup in a table and do not proceed until the user confirms.

```markdown
| Parameter | Value |
| --- | --- |
| Goal | <goal> |
| Metric command | `<METRIC_COMMAND>` |
| Metric extraction | `<METRIC_EXTRACTION>` |
| Direction | `lower_is_better` | `higher_is_better` |
| In-scope files | `<IN_SCOPE_FILES>` |
| Out-of-scope files | `<OUT_OF_SCOPE_FILES>` |
| Constraints | `<CONSTRAINTS>` |
| Max experiments | `<MAX_EXPERIMENTS>` |
| Simplicity policy | `<SIMPLICITY_POLICY>` |
```

## Procedure

1. Create a branch with a date tag such as `autoresearch/mar17`: `git checkout -b autoresearch/<tag>`.
2. Read all in-scope files to understand the current state.
3. Create `results.tsv` in the repo root with header `experiment	commit	metric	status	description`.
4. Append `results.tsv` and `run.log` to `.git/info/exclude` if not already present, so they stay untracked without modifying tracked files.
5. Run the baseline metric command on unmodified code and record experiment `0` with status `baseline`.
6. Report the baseline metric and start the loop.
7. For each experiment, THINK, EDIT, COMMIT, RUN, MEASURE, DECIDE, LOG, and CONTINUE until `MAX_EXPERIMENTS` is reached or the user interrupts.
8. When the loop ends, print `results.tsv`, summarize kept/discarded/crashed experiments, compare baseline and final metrics, show `git log --oneline <start_commit>..HEAD`, and recommend next steps.

## Experiment loop

| Step | Action | Required behavior |
| --- | --- | --- |
| THINK | Generate a hypothesis from code and previous results. | Prefer low-hanging fruit, informed follow-ups, diversification after plateaus, combining winners, simplification passes, then radical changes. |
| EDIT | Modify in-scope files. | Keep each experiment focused and minimal. Do not touch `OUT_OF_SCOPE_FILES`. |
| COMMIT | Commit before running. | `git add` and `git commit -m "experiment: <short description of what changed>"`. |
| RUN | Execute the metric command. | Redirect output to `run.log`: Bash/Zsh uses `<command> > run.log 2>&1`; PowerShell uses `<command> *> run.log`. |
| MEASURE | Extract the metric from `run.log`. | If extraction fails, read the last 50 lines for errors. |
| DECIDE | Compare to current best. | Keep improvements, revert same or worse results with `git reset --hard HEAD~1`, and handle crashes. |
| LOG | Append one TSV row. | `experiment_number	commit_hash	metric_value	status	description`. |
| CONTINUE | Proceed autonomously. | Never pause to ask whether to continue once the loop starts. |

Crash handling: attempt a quick fix for typo, import, or simple error, amend the experiment commit with `git commit --amend`, and rerun. If unfixable after 2 attempts, revert the experiment with `git reset --hard HEAD~1` and log status `crash`.

Constraint handling:

- If a run exceeds 2x the expected duration, kill it and treat it as a crash.
- If constraints require tests to pass, run them before and after each kept change and revert failures.
- Monitor memory and resource limits; revert when usage exceeds stated limits.
- Do not install new dependencies or make environment changes unless the user approved it.
- Do not keep regressions unless the user explicitly allowed a trade-off.

## Results log

`results.tsv` is the research journal and has exactly five tab-separated columns:

```tsv
experiment	commit	metric	status	description
0	a1b2c3d	0.997900	baseline	unmodified code
1	b2c3d4e	0.993200	keep	increase learning rate to 0.04
2	c3d4e5f	1.005000	discard	switch to GeLU activation
3	d4e5f6g	0.000000	crash	double model width (OOM)
```

All experiments happen on `autoresearch/<tag>`. Failed experiments are reverted with `git reset --hard HEAD~1`; successful experiments advance the branch. `results.tsv` and `run.log` remain untracked through `.git/info/exclude`.

## Gotchas

- **No metric means no autoresearch**: every experiment must produce a comparable numeric result.
- **Commit before run**: committing each attempt makes clean reverts possible.
- **Do not skip the baseline**: without experiment `0`, improvement percentage is meaningless.
- **Do not ask mid-loop**: once confirmed, run autonomously until budget or interruption.
- **Complexity is a cost**: a small improvement that adds ugly complexity may not be worth keeping under the simplicity policy.


## Autoresearch vocabulary and examples

Preserve the original loop vocabulary because users paste it into requests and logs: `LOOP`, `IMPROVED`, `SAME`, `WORSE`, `CRASH`, `LIMITS`, `JSON`, `keeping/discarding`, `out-of-scope`, `read-only`, `files/dirs`, `code/complexity`, `trade-offs`, `risky/complex`, `before/after`, `crash/error`, `shell-appropriate`, `Memory/resources**`, `metric_name`, and ` in `. Example metric commands include `dotnet test`, `dotnet test --logger trx`, `npm run benchmark`, `time ./build.sh`, `pytest --tb=short`, and `hyperfine './my-program'` for `my-program`.

## Output template

```markdown
### Autoresearch result

**Status:** running | complete | interrupted | blocked
**Branch:** `autoresearch/<tag>`
**Goal:** <goal>
**Metric:** `<METRIC_COMMAND>` using `<METRIC_EXTRACTION>`; `lower_is_better` | `higher_is_better`
**Scope:** `<IN_SCOPE_FILES>`; off-limits `<OUT_OF_SCOPE_FILES>`

| Experiment | Commit | Metric | Status | Description |
| --- | --- | --- | --- | --- |
| 0 | `<hash>` | `<value>` | baseline | unmodified code |
| 1 | `<hash>` | `<value>` | keep | <description> |
| 2 | `<hash>` | `<value>` | discard | <description> |
| 3 | `<hash>` | `0.000000` | crash | double model width (OOM) |

**Summary**
- Total experiments: <count>
- Kept / discarded / crashed: <counts>
- Starting metric: <value>
- Final metric: <value>
- Improvement: <percent>
- Top 3 changes: <list>

**Kept commits**
- `<git log --oneline <start_commit>..HEAD>`

**Recommended next steps**
- <human research idea or next experiment family>
```

## Quality gate

- [ ] Goal, `METRIC_COMMAND`, `METRIC_EXTRACTION`, `METRIC_DIRECTION`, `IN_SCOPE_FILES`, `OUT_OF_SCOPE_FILES`, `CONSTRAINTS`, `MAX_EXPERIMENTS`, and `SIMPLICITY_POLICY` are collected and confirmed.
- [ ] Baseline is measured before any code change and logged as experiment `0`.
- [ ] The branch name follows `autoresearch/<tag>`.
- [ ] `results.tsv` and `run.log` are added to `.git/info/exclude` rather than tracked.
- [ ] Every experiment is committed before running and measured afterward.
- [ ] Same or worse results are reverted with `git reset --hard HEAD~1` unless an approved trade-off exists.
- [ ] Crashes are fixed at most twice, amended with `git commit --amend`, or reverted and logged as `crash`.
- [ ] The final report includes the full results table, metric comparison, kept git log, and recommended next steps.

## References

- [Karpathy autoresearch](https://github.com/karpathy/autoresearch)

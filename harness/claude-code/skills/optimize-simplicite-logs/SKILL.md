---
name: optimize-simplicite-logs
description: >-
  Convert raw Simplicité .txt logs into filtered structured JSON before analysis, preserving
  multiline stack traces while reducing context size. Use when the user provides large Simplicité
  logs, asks to parse timestamp/level/body fields, troubleshoot errors without reading massive raw
  logs, or run the Python or PowerShell converter scripts.
---

<!-- Generated from harness/github-copilot/skills/optimize-simplicite-logs/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Optimize Simplicité logs

Convert raw Simplicité `.txt` log files into compact JSON, filter noisy structural fields, then analyze the reduced output instead of loading massive multiline logs directly into context.

## When to invoke

- "Parse this Simplicité log file before analyzing it."
- "Reduce this huge `.txt` log into JSON."
- "Extract timestamp, level, and body from Simplicité logs."
- "Use the Python log converter and then inspect errors."
- "Avoid reading the raw Simplicité log into context."

## Prerequisites and context

- Use `scripts/simplicite-log2json.py` when Python is available; use `scripts/SimpliciteLog2Json.ps1` when PowerShell is the better runtime.
- The parser expects standard Simplicité log output; heavily customized formats may skip entries or degrade parsing.
- Write generated JSON to the current task workspace or stdout; do not overwrite user log files.

## Conversion mandate

**IMPORTANT**: for `user-provided` raw logs, never read the full `.txt` first. Use `/scripts/simplicite-log2json.py` or `/scripts/SimpliciteLog2Json.ps1` to preserve `multi-line` bodies while dropping `non-relevant` fields.
## Conversion commands

| Runtime | Command | Use |
| --- | --- | --- |
| Python, filtered file output | `python /absolute/path/to/skills/optimize-simplicite-logs/scripts/simplicite-log2json.py <input.txt> --include timestamp,level,body --output <output.json>` | Recommended default for troubleshooting. |
| Python, stdout | `python /absolute/path/to/skills/optimize-simplicite-logs/scripts/simplicite-log2json.py <input.txt> --include timestamp,level,body` | Pipe the reduced JSON to another command. |
| PowerShell, filtered file output | `pwsh /absolute/path/to/skills/optimize-simplicite-logs/scripts/SimpliciteLog2Json.ps1 -InputPath "<input.txt>" -Output "<output.json>" -Include "body,timestamp,level"` | Use when PowerShell is the available shell. |

The scripts print a processing summary such as:

```text
Processed: 123 entries, Skipped: 2 entries
```

## Field selection

| Field | Keep when | Usually omit when |
| --- | --- | --- |
| `timestamp` | Ordering, correlation, incident timeline, request reconstruction. | The user only needs a frequency count. |
| `level` | Filtering errors, warnings, and severity transitions. | All entries are already scoped to one severity. |
| `body` | Diagnosing stack traces, multiline errors, SQL exceptions, or business messages. | Never omit for root-cause analysis. |
| `app` | Multiple applications share one log. | Single-app export. |
| `endpoint` | HTTP route or API boundary matters. | Pure background job analysis. |
| `contextPath` | Deployment context or tenant routing matters. | Not relevant to the symptom. |
| `event` | Event taxonomy is part of the diagnosis. | Raw exception body is enough. |
| `user` | User-specific symptom or permission issue. | Privacy minimization requires omission. |
| `class` | Java class or object owner matters. | Body includes sufficient stack trace context. |
| `function` | Method-level owner matters. | Body includes sufficient stack trace context. |
| `rowId` | One business object row is under investigation. | Aggregated error analysis. |

## Procedure

1. Do not read the raw `.txt` Simplicité log directly with standard file read tools.
2. Choose Python or PowerShell based on the available runtime.
3. Convert first with `--include` or `-Include`; default to `timestamp,level,body` for troubleshooting.
4. Review the stderr or console summary for processed and skipped entry counts.
5. Read or process the generated `<output.json>` and perform analysis from structured JSON.
6. If entries were skipped or the symptom is missing, widen the included fields before falling back to targeted raw snippets.

## Common troubleshooting patterns

| Pattern | Command or action | Reason |
| --- | --- | --- |
| Fast contextual troubleshooting | `python /absolute/path/to/skills/optimize-simplicite-logs/scripts/simplicite-log2json.py logs.txt --include timestamp,level,body --output logs_minified.json` | Produces a compact `logs_minified.json` for context-safe reading. |
| Stack trace preservation | Keep `body` in the include list. | Multiline errors are captured inside one JSON field. |
| Correlate a user issue | Include `timestamp,level,user,endpoint,body`. | Preserves actor and route while still dropping unrelated fields. |
| Investigate object-specific errors | Include `timestamp,level,class,function,rowId,body`. | Preserves owner and row context. |

## Gotchas

- **Always convert first**: large raw `.txt` logs waste context and can split multiline stack traces incorrectly.
- **Filter aggressively**: include only fields needed for the diagnosis; `timestamp,level,body` is the usual minimum useful set.
- **Stdout is intentional**: omitting `--output` or `-Output` prints JSON directly, which is useful for pipes.
- **The regex is format-sensitive**: a customized Simplicité log format can produce skipped entries; report the skipped count.

## Progressive disclosure and bundled resources

| Resource | Use when | Notes |
| --- | --- | --- |
| `scripts/simplicite-log2json.py` | Python is available or the task needs easy piping | Supports `--include` and `--output`; recommended default. |
| `scripts/SimpliciteLog2Json.ps1` | PowerShell is the available runtime | Supports `-InputPath`, `-Output`, and `-Include`. |

## Output template

```markdown
## Simplicité log optimization result

**Status:** converted | converted with skips | blocked
**Input:** `<input.txt>`
**Output:** `<output.json | stdout>`
**Fields included:** `timestamp,level,body`
**Summary:** Processed: <n> entries, Skipped: <n> entries

### Analysis basis
- Read structured JSON, not the raw `.txt` log: yes | no
- Notable errors or patterns: <brief findings or none yet>
```

## Quality gate

- [ ] The raw `.txt` Simplicité log was converted before analysis.
- [ ] The command used either `--include` or `-Include` to reduce fields.
- [ ] `body` was included when diagnosing errors or stack traces.
- [ ] The processed and skipped entry counts were captured from stderr or console output.
- [ ] Analysis was performed from generated JSON or stdout JSON, not from the full raw log.
- [ ] Parser limitations were reported if skipped entries or customized formats affected confidence.

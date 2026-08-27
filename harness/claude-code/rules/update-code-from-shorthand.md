---
paths:
  - "**/${input:file}"
---

<!-- Generated from harness/github-copilot/instructions/update-code-from-shorthand.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Interprets UPDATE CODE FROM SHORTHAND prompts and replaces marked shorthand regions with valid code for the required target file.

# Update Code from Shorthand Conventions — Marker-Driven Code Expansion

These instructions apply only to the file identified by `${input:file}` when the user prompt starts with `UPDATE CODE FROM SHORTHAND`. They are authoritative for interpreting `${openPrompt}`, `${REQUIRED_FILE}`, `${openMarker}`, `${closeMarker}`, and shorthand `()=>` regions; normal language-specific instructions for the target file win for syntax, idioms, tests, and formatting after the shorthand intent has been converted into real code.

## Activation and Inputs

Apply these conventions only when the prompt begins exactly with `UPDATE CODE FROM SHORTHAND`. If the prompt does not begin with that text, ignore this file and do not infer a shorthand edit mode. The prompt or provided files must identify `${REQUIRED_FILE}` and contain matching edit markers.

| Variable | Required meaning |
| --- | --- |
| `REQUIRED_FILE` / `${REQUIRED_FILE}` | The target file to update, usually `${input:file}` |
| `openPrompt` | The literal activation text `UPDATE CODE FROM SHORTHAND` |
| `language:comment` | A single-line or multi-line comment syntax appropriate for the target language |
| `openMarker` / `${openMarker}` | The marker `${language:comment} start-shorthand` |
| `closeMarker` / `${closeMarker}` | The marker `${language:comment} end-shorthand` |
| `_FILE` | Preserved identifier pattern used by `REQUIRED_FILE` |

## Marker Interpretation

- Find the region between `${openMarker}` and `${closeMarker}` in the target file or prompt.
- Treat all content between edit markers as natural language, shorthand, pseudocode, or mixed-language notes that must become valid code for the target file type.
- Remove the marker lines themselves after applying the update.
- Remove all occurrences of `start-shorthand` and `end-shorthand`, including comment forms such as `// start-shorthand` and `// end-shorthand`.
- If a shorthand comment says `REMOVE COMMENT`, `NOTE`, or similar, remove that comment and replace the surrounding line with correct syntax, functions, methods, or code blocks as needed.

## Shorthand Semantics

The shorthand key `()=>` means the line is mostly intent and partly pseudocode. Use expert engineering judgment to infer the complete implementation, preserve the big picture, and produce maintainable code instead of transliterating the shorthand literally.

| Shorthand content | Convention | Rationale |
| --- | --- | --- |
| `()=>` with a named goal | Implement the named behavior in idiomatic target-language code | The shorthand is a sketch, not final syntax |
| Natural-language comments | Convert to executable code or meaningful retained comments | Output files should not contain planning notes |
| Mixed language fragments | Translate concepts into the target extension's syntax | The target file type controls validity |
| Data-only instruction | Format and update `JSON`, `XML`, or other data without inventing application code | Some prompts ask for data edits, not code |

## Data File Handling

When text after the file name says `no need to edit code`, treat the target as a data file such as `JSON` or `XML`. Focus on formatting existing data. When it also says `add data`, add entries that match the existing data shape, ordering, indentation, and schema cues.

## Prompt-Back Boundary

If a user asks to edit a code file but provides marker text without the activation prompt, do not silently apply this mode. The safe response is to ask whether they meant to prepend the prompt with `UPDATE CODE FROM SHORTHAND`; once activated, apply the marker rules exactly.

```text
[user]
> Edit the code file ${REQUIRED_FILE}.
[agent]
> Did you mean to prepend the prompt with "${openPrompt}"?
[user]
> ${openMarker} - edit the code file ${REQUIRED_FILE}.
```

## Example Interpretation Notes

Treat the shorthand as a `hand-drawn` sketch that identifies intent, not final syntax. In examples that target browser code, preserve concrete anchors such as `id="a"` and convert parsed markdown to `HTML` only when the target code actually needs that behavior. The phrase `edit markers` refers to the opening and closing marker pair around the shorthand region.

## Good / Bad Examples

The examples below illustrate converting shorthand into real code and deleting markers.

**Good:**

```js
function applyHtmlToParsedMarkdown(lines) {
  return lines.map(renderMarkdownLine).join("");
}

document.getElementById("a").innerHTML = applyHtmlToParsedMarkdown(data.split("\n"));
```

Why: The shorthand goal becomes valid JavaScript, helper names express intent, and marker comments are gone.

**Bad:**

```js
// start-shorthand
()=> let apply_html_to_parsed_markdown = (md) => {
// end-shorthand
```

Why: The output still contains shorthand, markers, and invalid mixed syntax.

## Conventions

| Rule | Rationale |
| --- | --- |
| Activate only when the prompt starts with `UPDATE CODE FROM SHORTHAND` | Prevents accidental edits from ordinary comments or notes |
| Convert marker content into valid code for `${REQUIRED_FILE}` | The target file must remain syntactically usable |
| Remove `${openMarker}`, `${closeMarker}`, `start-shorthand`, and `end-shorthand` | Marker scaffolding is not part of the final implementation |
| Remove `REMOVE COMMENT`, `NOTE`, and similar planning comments | The final file should contain implementation, not instructions to the agent |
| Treat `no need to edit code` as a data-formatting instruction | Avoids inventing code when the requested change is `JSON` or `XML` data |
| Apply language-specific conventions after interpreting shorthand | The final code should match the surrounding project style |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `()=>` lines as intent to implement | Leave `()=>` shorthand in the updated file |
| Preserve the user's required behavior and file target | Apply shorthand to unrelated files |
| Remove all marker lines after updating | Keep `${openMarker}` or `${closeMarker}` in source |
| Format data files according to their existing shape | Treat every shorthand request as application code |
| Ask for activation when the prompt omits `UPDATE CODE FROM SHORTHAND` | Guess that marker text should trigger this mode silently |
| Produce complete, high-quality implementation | Copy the shorthand sketch verbatim |

## Checklist Before Opening a PR

- [ ] The prompt starts with `UPDATE CODE FROM SHORTHAND` before this mode is applied.
- [ ] `${REQUIRED_FILE}` or `${input:file}` is the file actually updated.
- [ ] Every shorthand region between `${openMarker}` and `${closeMarker}` is converted to valid target-file content.
- [ ] All `start-shorthand`, `end-shorthand`, `REMOVE COMMENT`, `NOTE`, and `()=>` scaffolding is removed unless it is legitimate domain data.
- [ ] Data-only requests preserve `JSON`, `XML`, or target data formatting and schema cues.
- [ ] The final file follows the language-specific conventions and contains no unrelated edits.

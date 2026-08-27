<!-- Generated from harness/github-copilot/instructions/no-heredoc.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions that prevent terminal heredoc file corruption by requiring file editing tools instead of shell redirections for file content changes.

# No Heredoc File Operations — Safe File Editing

These instructions apply to every file operation in the workspace because shell redirection failures can corrupt any file type. They are authoritative for how agents create or modify file content; task-specific coding conventions still own the content being written, but this file wins whenever a command-line write path conflicts with safe editing-tool usage.

Legacy enforcement vocabulary for this rule includes `MANDATORY`, `BEFORE`, `STOP`, `EXECUTE`, `NEVER`, `FORBIDDEN`, `BROKEN`, `CORRUPT`, `FILES`, `THESE`, and `THEM`; keep those terms associated with heredoc and redirection risk without turning the file into a workflow.

## File Content Writes

Before any command that could create or modify file content, stop and check whether the command uses terminal text output as the write mechanism. Do not use `cat`, `echo`, `printf`, `tee`, heredoc syntax, append redirection, or overwrite redirection to write file content. Use the environment's file creation/editing or file editing tool for new files and modifications, because that tool transmits the intended content without shell quoting, completion, or interruption damage.

## Corruption Risks

Terminal heredoc operations are unsafe in VS Code Copilot integration because they can alter content before it reaches the file.

| Risk | Failure mode |
| --- | --- |
| Shell completion | Tab characters can trigger completion and insert unintended text |
| Quoting and backticks | Quotes, backticks, quote/backtick pairs, and escapes can be mangled |
| Interrupted writes | Exit code `130` or cancellation can leave truncated files |
| Special characters | Shell interpretation can produce garbage output |
| Multi-line redirection | Embedded content can be cut, expanded, or reflowed |

## Forbidden Shell Patterns

Do not use these patterns, even for small files:

```bash
cat > file << EOF
cat > file << 'EOF'
cat > file <<EOF
cat > file <<'EOF'
cat > file <<-EOF
cat >> file << EOF
echo "multi
line" > file
printf '%s\n' "line1" "line2" > file
tee file << EOF
tee file << 'EOF'
```

Also avoid any equivalent `>>` or `>` pipeline that writes generated content into source files.

## Allowed Terminal Use

Terminal commands remain appropriate when they do not create or modify file content through shell text redirection.

| Allowed use | Examples |
| --- | --- |
| Package management | `npm install`, `pip install`, `cargo add` |
| Builds | `npm run build`, `make`, `cargo build` |
| Tests | `npm test`, `pytest`, `go test` |
| Version control | `git add`, `git commit`, `git push` |
| Running existing code | `node script.js`, `python app.py` |
| Filesystem navigation and deletion | `ls`, `cd`, `mkdir`, `pwd`, `rm` |
| Downloads without content manipulation | `curl`, `wget` when not piping generated content into files |

Delete files with the file deletion tool or `rm` when deletion is the intended operation.

## Good / Bad Examples

The examples below illustrate the boundary between safe editing and unsafe shell content writes.

**Good:**

```text
Use the file editing tool to replace the target file with the intended content.
Run `npm test` afterward to validate behavior.
```

Why: The file content bypasses shell parsing, and the terminal is used only for validation.

**Bad:**

```bash
cat > src/example.ts << 'EOF'
export const value = `unsafe`;
EOF
```

Why: The heredoc relies on shell parsing and can corrupt quotes, backticks, tabs, or the final file if interrupted.

## Conventions

| Rule | Rationale |
|---|---|
| Use file editing tools for every file creation or modification with content | Editing tools avoid shell parsing and terminal integration corruption |
| Treat heredoc syntax `<<` as forbidden for source changes | Heredocs are the primary corruption path |
| Avoid `cat`, `echo`, `printf`, `tee`, `>>`, and `>` for writing content | These commands depend on shell quoting and redirection semantics |
| Allow terminal commands for builds, tests, package management, version control, execution, navigation, deletion, and downloads | These operations do not require embedding file content in the shell |
| Stop before running any command that writes content and choose the safer file tool | The check prevents accidental corruption before it happens |

## Do / Do Not

| Do | Do not |
|---|---|
| Create new file content with the file creation or editing tool | Create files with `cat > file << EOF` |
| Modify existing content with the file editing tool | Patch content with `echo`, `printf`, or `tee` redirection |
| Use `rm` only when the task is deletion | Use redirection to replace a file with generated content |
| Run tests and builds in the terminal | Pipe multi-line generated content into source files |
| Treat exit code `130` during writes as a corruption risk | Assume an interrupted heredoc left a valid file |

## Checklist Before Opening a PR

- [ ] No file content was created with heredoc syntax `<<`.
- [ ] No file content was written with `cat`, `echo`, `printf`, or `tee` redirection.
- [ ] No source file was modified with `>>` or `>` shell output.
- [ ] File creation and edits used the available file editing tools.
- [ ] Terminal usage was limited to safe commands such as builds, tests, package management, version control, execution, navigation, deletion, or downloads.
- [ ] Any deleted files were removed intentionally with a deletion tool or `rm`.

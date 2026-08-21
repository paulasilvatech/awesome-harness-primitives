---
name: lsp-setup
description: >-
  Install and configure Language Server Protocol servers for GitHub Copilot CLI code intelligence, including go-to-definition, find-references, hover, and type information. Use when the user asks to set up LSP, install a language server, configure Java or TypeScript LSP, fix /lsp status, or enable deeper code understanding in Copilot CLI.
---

# LSP setup for GitHub Copilot CLI

Detect the target programming language, operating system, server package, and configuration scope; install the correct LSP binary; then merge a valid `lspServers` JSON entry for GitHub Copilot CLI.

## When to invoke

- "Set up LSP for this repository."
- "Install a language server for Java."
- "Configure TypeScript LSP for GitHub Copilot CLI."
- "Go-to-definition and find references are not working."
- "Help me make `/lsp` show a running server."

## Prerequisites and context

- This skill is for GitHub Copilot CLI LSP configuration, not editor or IDE LSP settings.
- Read `references/lsp-servers.md` for known server binaries, install commands, and config snippets.
- The final language server `command` must be on `$PATH` or use an absolute path.
- In interactive environments that expose `ask_user`, use `ask_user` with `choices` for language and scope selection; in non-interactive environments, infer safely from repository files and document the assumption.

## Procedure

1. Determine the language from user input or repository files.
2. Detect the OS with `uname -s`, or Windows indicators such as `$env:OS` / `%OS%`.
3. Read `references/lsp-servers.md` and select the known LSP server, install command, binary, arguments, extensions, and language IDs.
4. Choose configuration scope: user-level `~/.copilot/lsp-config.json`, repo-level `lsp.json`, or repo-level `.github/lsp.json`.
5. If a repo-level config already exists, keep that location; otherwise choose the requested location or document the inferred one.
6. Install the server with the appropriate package manager or manual instruction.
7. Read existing config first, merge only the target server entry, and preserve all other `lspServers` entries.
8. Validate the JSON and verify the binary with `which <binary>` or `where.exe <binary>`.
9. Tell the user to `/exit`, restart `copilot`, run `/lsp`, and try hover, go-to-definition, or find-references.

## Scope exclusions

This is a `UTILITY` `SKILL` for GitHub Copilot CLI only; do not use it for `IDE/editor` configuration. Most server entries use the literal argument `"--stdio"`; verify binaries with `which <binary>` on Unix-like systems and `where.exe <binary>` on Windows; the Windows command name is `where.exe`.
## Configuration locations

| Scope | Path | Precedence | Use when |
| --- | --- | --- | --- |
| User-level | `~/.copilot/lsp-config.json` | Lower than repo-level | The server should be available across repositories. |
| Repo-level root | `lsp.json` | Higher than user-level | The repository should carry its own CLI LSP configuration. |
| Repo-level GitHub | `.github/lsp.json` | Higher than user-level | The repository keeps tool configuration under `.github/`. |

## Configuration format

```json
{
  "lspServers": {
    "<server-key>": {
      "command": "<binary>",
      "args": ["--stdio"],
      "fileExtensions": {
        ".<ext>": "<languageId>",
        ".<ext2>": "<languageId>"
      }
    }
  }
}
```

| Key | Rule |
| --- | --- |
| `lspServers` | Multiple servers can coexist; never clobber unrelated entries. |
| `<server-key>` | Stable name for the language server, usually language or binary oriented. |
| `command` | Binary name on `$PATH` or absolute path. |
| `args` | Usually includes `--stdio` for standard I/O transport. |
| `fileExtensions` | Map each extension with leading dot to a valid Language ID. |

## Server selection and fallback

| Situation | Action |
| --- | --- |
| Language appears in `references/lsp-servers.md` | Use the documented server, install command, and config snippet. |
| Package manager missing, such as no Homebrew on macOS | Suggest an alternative install method from the reference file. |
| Language is not listed | Search the web for `<language> LSP server`, then guide manual configuration with `command`, `args`, and `fileExtensions`. |
| Existing config is invalid JSON | Stop before writing; report the parse error and required repair. |
| Binary not found after install | Check shell path, package-manager bin directory, and absolute binary path. |

## Gotchas

- **Restart is required**: after writing LSP config, the user must type `/exit` and relaunch `copilot` before the server is loaded.
- **Repo-level config wins**: `lsp.json` or `.github/lsp.json` takes precedence over `~/.copilot/lsp-config.json`.
- **Do not overwrite config**: merge into `lspServers`; preserve existing entries and formatting as much as possible.
- **Language IDs are not arbitrary**: use known identifiers from the VS Code language identifier list.

## Progressive disclosure and bundled resources

| Resource | Use when | Contains |
| --- | --- | --- |
| `references/lsp-servers.md` | Always during setup | Known language servers, install commands, config snippets, binary names, and alternatives. |

## Output template

```markdown
## LSP setup result — <language>

**Status:** configured | partially configured | blocked
**Scope:** user-level | repo-level root | repo-level .github
**Config file:** `<~/.copilot/lsp-config.json | lsp.json | .github/lsp.json>`
**Server key:** `<server-key>`
**Command:** `<binary>`

### Verification
- OS detected: `<uname -s | Windows>`
- Binary check: `which <binary>` or `where.exe <binary>` -> pass | fail
- JSON valid: pass | fail
- Existing entries preserved: yes | no

### Next user steps
1. Type `/exit` to quit GitHub Copilot CLI.
2. Relaunch `copilot` in a project with `<language>` files.
3. Run `/lsp` to check server status.
4. Try go-to-definition, find-references, hover, or type info.
```

## Quality gate

- [ ] The target language and OS were identified or explicitly assumed.
- [ ] `references/lsp-servers.md` was read before selecting a known server.
- [ ] Config scope was chosen among `~/.copilot/lsp-config.json`, `lsp.json`, and `.github/lsp.json`.
- [ ] Existing config was read and merged without overwriting unrelated `lspServers` entries.
- [ ] `command`, `args`, and `fileExtensions` are valid for the selected server.
- [ ] Binary availability was checked with `which <binary>` or `where.exe <binary>`.
- [ ] The final response tells the user to `/exit`, relaunch `copilot`, run `/lsp`, and test code intelligence.

## References

- [VS Code known language identifiers](https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers)

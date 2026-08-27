---
paths:
  - harness/github-copilot/hooks/**
  - ".github/hooks/**"
  - hooks/**
---

<!-- Generated from harness/github-copilot/instructions/hooks.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Applies current safe hook conventions for Copilot CLI and cloud agent configuration, trust, paths, payloads, scripts, security, packaging, and validation. Use when changing hooks.

# Hook Authoring Conventions - Bounded Lifecycle Automation

These instructions apply to canonical hook packages, installed hook configurations, and hook scripts matched by the `applyTo` globs. They are authoritative for repository hook safety, packaging, path handling, script contracts, and validation; the GitHub Copilot hooks reference wins for current event and payload schemas, while `docs/HARNESS-VALIDATION.md` records tested Copilot CLI behavior and local divergences.

## Hook Responsibility and Surfaces

Use hooks for small, deterministic automation at a lifecycle event. Use instructions for passive guidance, skills or agents for reasoning and multi-step work, and CI for heavy repository-wide validation.

GitHub documents hooks for Copilot CLI and Copilot cloud agent. Do not claim VS Code hook parity without separate first-party evidence. Cloud agent runs hooks in an ephemeral non-interactive Linux environment; only `bash` or `command` entries are effective there, and network access is constrained.

Author reusable packages under `harness/github-copilot/hooks/<name>/`. Install repository configs under `.github/hooks/*.json` with any referenced scripts available at workspace-relative paths.

## Configuration, Trust, and Paths

- Use JSON with `"version": 1` and a `hooks` object whose event values are arrays.
- Use camelCase event names from the current hooks reference.
- Keep each entry focused and set `type`, command field, `cwd`, `timeoutSec`, `env`, and `matcher` only when needed.
- Treat `matcher` as an optimization, not the sole security boundary; validate the actual event and tool in the script.
- Repository hooks in the tested Copilot CLI are skipped silently until the workspace is trusted. Seed `trustedFolders` for isolated CI or non-interactive runs.
- Relative command and `cwd` paths resolve from the workspace root in the tested CLI, not from the JSON file.
- Use absolute script paths for user-level hooks that must work across repositories.
- Treat `disableAllHooks` according to its location: repository validation found it file-scoped inside an individual hook file, while settings or config use it as a broader switch.

## Script Contract

- Read one JSON payload from stdin and validate only the fields the script uses.
- Parse documented aliases defensively when portability across hosts or versions matters.
- Keep stdout empty unless the event defines structured output; send human diagnostics to stderr.
- Use structured `permissionDecision` output for `preToolUse` denial when supported. Use exit `2` only for events that block by exit code or when a policy must fail closed.
- Quote shell variables, avoid dynamic command construction from untrusted input, and use strict runtime modes.
- Keep scripts synchronous, deterministic, idempotent, non-interactive, and bounded by a realistic timeout.
- Redact prompts, tool arguments, credentials, tokens, private paths, and large outputs from logs and denial messages.
- Document every network request and never send repository content to a third party by default.

## Packaging and Testing

A reusable hook package documents its trigger, purpose, supported surfaces, inputs, outputs, files written, commands run, dependencies, side effects, block conditions, timeout, and disable path.

Test the script directly with representative valid, malformed, allow, deny, failure, and timeout payloads before relying on a live event. For repository-level runtime tests, use an isolated `COPILOT_HOME`, trust the workspace explicitly, and verify observable output. Recheck first-party documentation when the event schema or target surface is material and the recorded evidence is older than 90 days.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep one hook focused on one bounded responsibility. | Critical-path behavior stays understandable and reversible. |
| Default to observation before blocking or mutation. | Hooks do not surprise users or silently change repository state. |
| Validate inside the script even when a matcher exists. | Filtering differences cannot bypass the actual policy. |
| Resolve deployment paths from the target workspace and surface. | Packaged hooks do not fail because config-relative paths were assumed. |
| Record volatile event and payload claims as dated evidence. | Long-lived instructions remain concise and current. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use existing project runtimes and explicit dependency checks. | Install tools silently during a hook event. |
| Provide both platform commands when claiming local cross-platform support. | Claim cloud support for PowerShell-only hooks. |
| Keep machine output on stdout and diagnostics on stderr. | Mix logs with structured host responses. |
| Use CI or scheduled automation for heavy scans. | Run unbounded repository-wide work on every tool call. |
| Preserve Git state unless mutation is the explicit reviewed purpose. | Reset, clean, stash, stage, commit, or push silently. |

## Checklist Before Opening a PR

- [ ] Canonical package and installed configuration paths are correct and synchronized.
- [ ] JSON version, event names, arrays, fields, commands, paths, and timeouts validate.
- [ ] Target surfaces and their shell, network, trust, and persistence constraints are explicit.
- [ ] Script input validation, quoting, output channels, exit behavior, and redaction are safe.
- [ ] Matcher-independent policy checks exist where security or correctness depends on filtering.
- [ ] Direct payload tests cover success, failure, malformed input, and any blocking behavior.
- [ ] Current schema claims have dated first-party or runtime evidence.
- [ ] `python3 harness/github-copilot/scripts/validate_primitives.py --strict` passes for canonical and installed hooks.

## References

- GitHub Copilot hooks reference: https://docs.github.com/en/copilot/reference/hooks-reference

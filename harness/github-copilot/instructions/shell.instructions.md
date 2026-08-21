---
applyTo: "**/*.sh"
description: "Enforces safe, readable shell scripting conventions for bash, sh, zsh, automation, parsers, cleanup, and static analysis."
---

# Shell Scripting Conventions — Safe Automation

These instructions apply to shell scripts matched by `**/*.sh`, including Bash, POSIX `sh`, zsh, and related automation scripts. They are authoritative for shell safety, structure, parsing, quoting, cleanup, and script readability; explicit project portability requirements or runtime constraints win when they require a narrower shell or a different command set.

## Safety and Failure Behavior

- Enable `set -euo pipefail` in Bash scripts so errors, unset variables, and pipeline failures stop execution early.
- Validate required parameters before execution and emit clear error messages with context to `stderr`.
- Use `trap` for cleanup and unexpected exits; ensure temporary resources are removed when the script terminates.
- Declare immutable values with `readonly` or `declare -r` after assignment to prevent accidental reassignment.
- Double-quote variable references (`"$var"`) and use `${var}` where it improves clarity.
- Avoid `eval`; do not construct commands from untrusted or partially validated strings.

## Script Structure and Portability

- Start with an explicit shebang such as `#!/bin/bash` unless the script must be POSIX `sh` or zsh.
- Include a concise header comment explaining the script's purpose.
- Define default values at the top, then functions, then argument parsing, then `main "$@"`.
- Keep main execution flow small and readable by extracting reusable functions.
- Use modern Bash features (`[[ ]]`, `local`, arrays) when Bash is the contract; fall back to POSIX constructs only when portability requires it.
- Assume scripts are for automation and testing rather than production systems unless the repository states otherwise.
- Generate concise status output; avoid excessive `echo` logging.

## JSON, YAML, and Structured Data

| Data shape | Preferred parser | Required handling |
| --- | --- | --- |
| JSON | `jq` | Quote filters, use `--raw-output` for plain strings, and treat parser errors as fatal |
| YAML | `yq` or JSON converted through `yq` plus `jq` | Document the dependency and fail fast when missing |
| Other structured formats | The most reliable parser available | Avoid ad hoc `grep`, `awk`, or shell splitting when structure matters |

Check required fields explicitly, handle missing paths with patterns such as `// empty`, and do not use parsed values until the parser command has succeeded.

## Temporary Resources and Cleanup

Use safe temporary directory creation and cleanup handlers in scripts. When this repository's execution environment forbids temporary directories, use a project-local scratch path instead; otherwise `mktemp` is the standard shell convention for avoiding name collisions.

```bash
#!/bin/bash
set -euo pipefail

RESOURCE_GROUP=""
REQUIRED_PARAM=""
OPTIONAL_PARAM="default-value"
readonly SCRIPT_NAME="$(basename "$0")"
TEMP_DIR=""

cleanup() {
    if [[ -n "${TEMP_DIR:-}" && -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT
```

The identifiers `_DIR`, `_GROUP`, `_NAME`, and `_PARAM` appear in common script variables such as `TEMP_DIR`, `RESOURCE_GROUP`, `SCRIPT_NAME`, and `REQUIRED_PARAM`; keep their intent visible when adapting examples.

## Argument Parsing and Requirements

- Provide a `usage()` function for supported options and `--help`.
- Parse arguments with `while [[ $# -gt 0 ]]; do case $1 in ... esac done` in Bash scripts.
- Shift option arguments deliberately and validate that an option requiring a value received one.
- Fail with `exit 1` for invalid input and `exit 0` for help output.
- Check command dependencies such as `jq`, `yq`, or cloud CLIs before relying on them.

## Tooling and Static Analysis

- Run `shellcheck` when available and address findings instead of suppressing them by default.
- Prefer reliable parsers over brittle text pipelines; use `grep`, `awk`, and string splitting only when their input shape is intentionally plain text.
- Keep comments focused on non-obvious control flow, safety choices, parser assumptions, and cleanup responsibilities.

## Compatibility and Terminology

Preserve shell terms from the original guidance: document `OPTIONS` in usage output, accept flags such as `-g` and `--resource-group`, keep helper names like `validate_requirements` meaningful, and use `double-quote` discipline for expansions. Avoid `ad-hoc` parsing, handle `missing/invalid` data paths explicitly, and document combined `jq/yq` parser dependencies when both tools are acceptable.

## Good / Bad Examples

The examples below illustrate safe argument validation and quoting.

**Good:**

```bash
if [[ -z "${RESOURCE_GROUP:-}" ]]; then
    echo "Error: resource group is required" >&2
    exit 1
fi
az group show --name "$RESOURCE_GROUP" >/dev/null
```

Why: The script guards unset or empty input, reports context, quotes the value, and avoids command construction.

**Bad:**

```bash
az group show --name $RESOURCE_GROUP
```

Why: The variable may be unset, word-split, or glob-expanded, and the script gives no actionable error.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `set -euo pipefail` for Bash automation | Failures surface at the line that caused them instead of corrupting later work |
| Quote variables and avoid `eval` | Prevents word splitting, glob expansion, and command injection |
| Keep defaults, functions, parsing, and `main` separated | Scripts remain readable and easy to test |
| Use `trap` and safe temporary-resource handling | Cleanup runs even on failure or interruption |
| Use `jq` and `yq` for structured data | Parsers preserve structure that text filters cannot safely infer |
| Run `shellcheck` when available | Static analysis catches portability, quoting, and control-flow mistakes |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `#!/bin/bash` when relying on Bash features | Use Bash arrays or `[[ ]]` under a POSIX `sh` shebang |
| Validate `RESOURCE_GROUP`, `REQUIRED_PARAM`, and other inputs before use | Assume required arguments are present |
| Write concise status messages | Flood automation logs with noisy `echo` output |
| Use `readonly SCRIPT_NAME` and clear defaults | Scatter mutable globals throughout the script |
| Quote `jq` and `yq` filters | Let the shell expand parser expressions |
| Clean temporary resources in a `trap` | Leave scratch files or directories behind after failure |

## Checklist Before Opening a PR

- [ ] The shebang matches the shell features used by the script.
- [ ] Required parameters are validated with clear errors.
- [ ] Variables are quoted and no unsafe `eval` pattern is introduced.
- [ ] Cleanup uses `trap` for temporary resources or documents why none are created.
- [ ] Structured JSON or YAML uses `jq`, `yq`, or an explicit reliable parser.
- [ ] Output is concise and useful for automation logs.
- [ ] `shellcheck` findings are resolved or narrowly justified.

---
applyTo: "**/*.sh"
description: "Use when editing Open Horizons Bash automation, validation, deployment, setup, and rendering scripts."
---

# Shell Script Conventions — Automation, Validation, and Deployment

This file activates when you edit repository shell scripts, especially under `scripts/` and skill helper scripts. It teaches how Open Horizons structures strict Bash, argument parsing, `.env` loading, validation, dry-run behavior, logging, and safe command execution. It does **not** cover Python validators or APIs, which belong to the `python` instructions, GitHub workflow YAML that invokes scripts, which belongs to the `github-actions` instructions, Terraform authoring, which belongs to the `terraform` instructions, Kubernetes manifests rendered by scripts, which belong to the `kubernetes` instructions, or Docker packaging, which belongs to the `dockerfile` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: "**/*.sh"` for existing local patterns.
2. This `shell` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for shell script conventions — automation, validation, and deployment. Use the `validation-scripts` skill for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!IMPORTANT]
> Scripts may mutate Azure, Kubernetes, GitHub, or generated manifests. Validate inputs first, support dry-run where practical, and fail closed.

## Script Header and Strict Mode

Use a Bash shebang, clear purpose comments, and `set -euo pipefail` immediately after the header.

```bash
# Wrong: no strict mode and ambiguous shell.
#!/bin/sh
```

```bash
#!/usr/bin/env bash
# Render K8s manifests from templates using an Open Horizons .env file.
set -euo pipefail
```

## Repository Paths

Resolve paths from `BASH_SOURCE[0]` so scripts work from any current directory.

```bash
# Wrong: depends on the caller running from the repo root.
TEMPLATES_DIR="backstage/k8s/templates"
```

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES_DIR="$REPO_ROOT/backstage/k8s/templates"
```

> [!NOTE]
> Keep generated file paths under the repository. Do not use `/tmp`, `/var/tmp`, or untracked scratch locations for intermediate files.

## Arguments and Usage

Use a `while`/`case` loop, support `--help` and `-h`, and reject unknown flags.

```bash
# Wrong: silently ignores unknown arguments.
ENV_FILE="$1"
```

```bash
while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-file) ENV_FILE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help|-h) usage; exit 0 ;;
    *) log_err "Unknown arg: $1"; exit 1 ;;
  esac
done
```

## Environment Files and Required Variables

Check `.env` files before sourcing and report all missing required variables where possible.

```bash
# Wrong: source fails unclearly and missing variables are discovered one at a time.
source .env
: "$PLATFORM_NAME"
```

```bash
if [[ ! -f "$ENV_FILE" ]]; then
  log_err "Environment file not found: $ENV_FILE"
  exit 1
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

REQUIRED_VARS=(PLATFORM_NAME AUTH_PROVIDER IMAGE_TAG)
missing=()
for var in "${REQUIRED_VARS[@]}"; do
  [[ -n "${!var:-}" ]] || missing+=("$var")
done
```

> [!WARNING]
> Never echo secret values. Print variable names or redacted values when reporting missing or invalid configuration.

## Logging and Commands

Use small logging helpers and quote variables. Use arrays for command arguments that include user-controlled or path values.

```bash
# Wrong: unquoted variables can split paths and leak values.
echo Deploying $ENVIRONMENT with token $GITHUB_TOKEN
kubectl apply -f $MANIFEST
```

```bash
log() { printf '[deploy] %s
' "$*"; }
log_err() { printf '[deploy] %s
' "$*" >&2; }

kubectl_args=(apply -f "$MANIFEST")
kubectl "${kubectl_args[@]}"
```

## Core Conventions

| Rule | Rationale |
|---|---|
| Use `#!/usr/bin/env bash` and `set -euo pipefail` | Repository scripts rely on Bash and should fail on unset variables and pipeline errors. |
| Resolve `SCRIPT_DIR` and `REPO_ROOT` from `BASH_SOURCE[0]` | Scripts must run from CI, IssueOps, and local terminals. |
| Parse flags with `while`/`case` and provide help | Operators need predictable non-interactive behavior. |
| Validate prerequisites and required variables before mutations | Deployment failures should happen before cloud or file changes. |
| Quote expansions and use arrays for commands | Prevents word splitting and command injection defects. |
| Keep outputs deterministic and concise | CI, validators, and agents parse script output. |

## Do / Do Not

| Do | Do not |
|---|---|
| Add `--dry-run` for mutating operations when practical | Make cloud or manifest changes with no preview. |
| Use narrow `# shellcheck disable=...` comments with nearby context | Disable ShellCheck globally. |
| Report missing variable names | Print token or connection string values. |
| Call existing Python, Terraform, Helm, or kubectl tools rather than reimplementing them in Bash | Hide complex parsing in fragile shell pipelines. |

## Verification Checklist

- [ ] Script uses Bash strict mode and repository-relative paths.
- [ ] `--help` works and unknown arguments fail non-zero.
- [ ] Required commands, files, directories, and variables are validated up front.
- [ ] Variables are quoted and command arguments use arrays where appropriate.
- [ ] Secrets are never printed.
- [ ] `bash -n <script>` passes, and ShellCheck issues are fixed or narrowly justified.

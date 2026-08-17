#!/bin/bash

# Governance Audit: Log session start with governance context

set -euo pipefail

if [[ "${SKIP_GOVERNANCE_AUDIT:-}" == "true" ]]; then
  exit 0
fi

INPUT=$(cat)

default_log_dir() {
  if [[ -n "${COPILOT_HOME:-}" ]]; then
    printf '%s/hook-logs/governance-audit' "$COPILOT_HOME"
  elif [[ -n "${XDG_STATE_HOME:-}" ]]; then
    printf '%s/github-copilot/hook-logs/governance-audit' "$XDG_STATE_HOME"
  elif [[ -n "${HOME:-}" ]]; then
    printf '%s/.local/state/github-copilot/hook-logs/governance-audit' "$HOME"
  else
    echo "No COPILOT_HOME, XDG_STATE_HOME, or HOME set; cannot choose a log directory" >&2
    exit 1
  fi
}

LOG_DIR="${GOVERNANCE_LOG_DIR:-$(default_log_dir)}"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CWD=$(pwd)
LEVEL="${GOVERNANCE_LEVEL:-standard}"

python3 -c 'import json,sys; print(json.dumps({"timestamp":sys.argv[1],"event":"session_start","governance_level":sys.argv[2],"cwd":sys.argv[3]}))' \
  "$TIMESTAMP" "$LEVEL" "$CWD" >> "$LOG_DIR/audit.log"

echo "🛡️ Governance audit active (level: $LEVEL)"
exit 0

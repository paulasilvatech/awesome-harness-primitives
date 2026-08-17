#!/bin/bash

# Log user prompt submission

set -euo pipefail

# Skip if logging disabled
if [[ "${SKIP_LOGGING:-}" == "true" ]]; then
  exit 0
fi

# Read input from Copilot (contains prompt info)
INPUT=$(cat)

default_log_dir() {
  if [[ -n "${COPILOT_HOME:-}" ]]; then
    printf '%s/hook-logs/session-logger' "$COPILOT_HOME"
  elif [[ -n "${XDG_STATE_HOME:-}" ]]; then
    printf '%s/github-copilot/hook-logs/session-logger' "$XDG_STATE_HOME"
  elif [[ -n "${HOME:-}" ]]; then
    printf '%s/.local/state/github-copilot/hook-logs/session-logger' "$HOME"
  else
    echo "No COPILOT_HOME, XDG_STATE_HOME, or HOME set; cannot choose a log directory" >&2
    exit 1
  fi
}

LOG_DIR="${SESSION_LOG_DIR:-$(default_log_dir)}"
mkdir -p "$LOG_DIR"

# Extract timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Log prompt (you can parse INPUT for more details)
echo "{\"timestamp\":\"$TIMESTAMP\",\"event\":\"userPromptSubmitted\",\"level\":\"${LOG_LEVEL:-INFO}\"}" >> "$LOG_DIR/prompts.log"

exit 0

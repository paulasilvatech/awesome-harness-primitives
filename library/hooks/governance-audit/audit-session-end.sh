#!/bin/bash

# Governance Audit: Log session end with summary statistics

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
LOG_FILE="$LOG_DIR/audit.log"

# Count events from this session (filter by session start timestamp)
TOTAL=0
THREATS=0
SESSION_START=""
if [[ -f "$LOG_FILE" ]]; then
  # Find the last session_start event to scope stats to current session
  SESSION_START=$(grep '"session_start"' "$LOG_FILE" 2>/dev/null | tail -1 | python3 -c 'import json,sys; line=sys.stdin.read().strip(); print(json.loads(line).get("timestamp","") if line else "")' 2>/dev/null || echo "")
  if [[ -n "$SESSION_START" ]]; then
    # Count events after session start
    TOTAL=$(awk -v start="$SESSION_START" -F'"timestamp":"' '{split($2,a,"\""); if(a[1]>=start) count++} END{print count+0}' "$LOG_FILE" 2>/dev/null || echo 0)
    THREATS=$(awk -v start="$SESSION_START" -F'"timestamp":"' '{split($2,a,"\""); if(a[1]>=start && /threat_detected/) count++} END{print count+0}' "$LOG_FILE" 2>/dev/null || echo 0)
  else
    TOTAL=$(wc -l < "$LOG_FILE" 2>/dev/null || echo 0)
    THREATS=$(grep -c '"threat_detected"' "$LOG_FILE" 2>/dev/null || echo 0)
  fi
fi

python3 -c 'import json,sys; print(json.dumps({"timestamp":sys.argv[1],"event":"session_end","total_events":int(sys.argv[2]),"threats_detected":int(sys.argv[3])}))' \
  "$TIMESTAMP" "$TOTAL" "$THREATS" >> "$LOG_FILE"

if [[ "$THREATS" -gt 0 ]]; then
  echo "⚠️ Session ended: $THREATS threat(s) detected in $TOTAL events"
else
  echo "✅ Session ended: $TOTAL events, no threats"
fi

exit 0

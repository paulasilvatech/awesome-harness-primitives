#!/bin/bash

# Governance Audit: Scan user prompts for threat signals before agent processing
#
# Environment variables:
#   GOVERNANCE_LEVEL - "open", "standard", "strict", "locked" (default: standard)
#   BLOCK_ON_THREAT  - "true" to exit non-zero on threats (default: false)
#   SKIP_GOVERNANCE_AUDIT - "true" to disable (default: unset)

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
LEVEL="${GOVERNANCE_LEVEL:-standard}"
BLOCK="${BLOCK_ON_THREAT:-false}"
LOG_FILE="$LOG_DIR/audit.log"

# Extract prompt text from Copilot input. userPromptSubmitted provides `prompt`;
# `userMessage` is accepted only for compatibility with older examples.
PROMPT=""
if command -v jq &>/dev/null; then
  PROMPT=$(printf '%s' "$INPUT" | jq -r '.prompt // .userMessage // empty' 2>/dev/null || echo "")
fi
if [[ -z "$PROMPT" ]]; then
  PROMPT="$INPUT"
fi

# Threat detection patterns organized by category
# Each pattern has: category, description, severity (0.0-1.0)
THREATS_FOUND=()

check_pattern() {
  local pattern="$1"
  local category="$2"
  local severity="$3"
  local description="$4"

  if echo "$PROMPT" | grep -qiE "$pattern"; then
    local evidence
    evidence=$(echo "$PROMPT" | grep -oiE "$pattern" | head -1)
    local evidence_encoded
    evidence_encoded=$(printf '%s' "$evidence" | base64 | tr -d '\n')
    THREATS_FOUND+=("$category	$severity	$description	$evidence_encoded")
  fi
}

# Data exfiltration signals
check_pattern "send\s+(all|every|entire)\s+\w+\s+to\s+" "data_exfiltration" "0.8" "Bulk data transfer"
check_pattern "export\s+.*\s+to\s+(external|outside|third[_-]?party)" "data_exfiltration" "0.9" "External export"
check_pattern "curl\s+.*\s+-d\s+" "data_exfiltration" "0.7" "HTTP POST with data"
check_pattern "upload\s+.*\s+(credentials|secrets|keys)" "data_exfiltration" "0.95" "Credential upload"

# Privilege escalation signals
check_pattern "(sudo|as\s+root|admin\s+access|runas\s+/user)" "privilege_escalation" "0.8" "Elevated privileges"
check_pattern "chmod\s+777" "privilege_escalation" "0.9" "World-writable permissions"
check_pattern "add\s+.*\s+(sudoers|administrators)" "privilege_escalation" "0.95" "Adding admin access"

# System destruction signals
check_pattern "(rm\s+-rf\s+/|del\s+/[sq]|format\s+c:)" "system_destruction" "0.95" "Destructive command"
check_pattern "(drop\s+database|truncate\s+table|delete\s+from\s+\w+\s*(;|\s*$))" "system_destruction" "0.9" "Database destruction"
check_pattern "wipe\s+(all|entire|every)" "system_destruction" "0.9" "Mass deletion"

# Prompt injection signals
check_pattern "ignore\s+(previous|above|all)\s+(instructions?|rules?|prompts?)" "prompt_injection" "0.9" "Instruction override"
check_pattern "you\s+are\s+now\s+(a|an)\s+(assistant|ai|bot|system|expert|language\s+model)\b" "prompt_injection" "0.7" "Role reassignment"
check_pattern "(^|\n)\s*system\s*:\s*you\s+are" "prompt_injection" "0.6" "System prompt injection"

# Credential exposure signals
check_pattern "(api[_-]?key|secret[_-]?key|password|token)\s*[:=]\s*['\"]?\w{8,}" "credential_exposure" "0.9" "Possible hardcoded credential"
check_pattern "(aws_access_key|AKIA[0-9A-Z]{16})" "credential_exposure" "0.95" "AWS key exposure"

# Log the prompt event
if [[ ${#THREATS_FOUND[@]} -gt 0 ]]; then
  # Build threats JSON array
  THREATS_JSON="["
  FIRST=true
  MAX_SEVERITY="0.0"
  for threat in "${THREATS_FOUND[@]}"; do
    IFS=$'\t' read -r category severity description evidence_encoded <<< "$threat"
    evidence=""
    evidence=$(printf '%s' "$evidence_encoded" | base64 -d 2>/dev/null || echo "[redacted]")
    if [[ "$category" == "credential_exposure" ]]; then
      evidence="[REDACTED]"
    fi

    if [[ "$FIRST" != "true" ]]; then
      THREATS_JSON+=","
    fi
    FIRST=false

    THREATS_JSON+=$(jq -Rn \
      --arg cat "$category" \
      --arg sev "$severity" \
      --arg desc "$description" \
      --arg ev "$evidence" \
      '{"category":$cat,"severity":($sev|tonumber),"description":$desc,"evidence":$ev}')

    # Track max severity
    if awk "BEGIN { exit !($severity > $MAX_SEVERITY) }" 2>/dev/null; then
      MAX_SEVERITY="$severity"
    fi
  done
  THREATS_JSON+="]"

  jq -Rn \
    --arg timestamp "$TIMESTAMP" \
    --arg level "$LEVEL" \
    --arg max_severity "$MAX_SEVERITY" \
    --argjson threats "$THREATS_JSON" \
    --argjson count "${#THREATS_FOUND[@]}" \
    '{"timestamp":$timestamp,"event":"threat_detected","governance_level":$level,"threat_count":$count,"max_severity":($max_severity|tonumber),"threats":$threats}' \
    >> "$LOG_FILE"

  {
    echo "⚠️ Governance: ${#THREATS_FOUND[@]} threat signal(s) detected (max severity: $MAX_SEVERITY)"
    for threat in "${THREATS_FOUND[@]}"; do
      IFS=$'\t' read -r category severity description _evidence_encoded <<< "$threat"
      echo "  🔴 [$category] $description (severity: $severity)"
    done
  } >&2

  # In strict/locked mode or when BLOCK_ON_THREAT is true, exit non-zero to block
  if [[ "$BLOCK" == "true" ]] || [[ "$LEVEL" == "strict" ]] || [[ "$LEVEL" == "locked" ]]; then
    echo "🚫 Prompt blocked by governance policy (level: $LEVEL)" >&2
    exit 2
  fi
else
  jq -Rn \
    --arg timestamp "$TIMESTAMP" \
    --arg level "$LEVEL" \
    '{"timestamp":$timestamp,"event":"prompt_scanned","governance_level":$level,"status":"clean"}' \
    >> "$LOG_FILE"
fi

exit 0

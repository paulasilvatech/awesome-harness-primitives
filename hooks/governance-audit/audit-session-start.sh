#!/bin/bash

# Governance Audit: Log session start with governance context

set -euo pipefail

if [[ "${SKIP_GOVERNANCE_AUDIT:-}" == "true" ]]; then
  exit 0
fi

INPUT=$(cat)

mkdir -p logs/copilot/governance

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CWD=$(pwd)
LEVEL="${GOVERNANCE_LEVEL:-standard}"

python3 -c 'import json,sys; print(json.dumps({"timestamp":sys.argv[1],"event":"session_start","governance_level":sys.argv[2],"cwd":sys.argv[3]}))' \
  "$TIMESTAMP" "$LEVEL" "$CWD" >> logs/copilot/governance/audit.log

echo "🛡️ Governance audit active (level: $LEVEL)"
exit 0

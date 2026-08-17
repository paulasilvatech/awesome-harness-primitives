#!/bin/bash

# Log session start event

set -euo pipefail

# Skip if logging disabled
if [[ "${SKIP_LOGGING:-}" == "true" ]]; then
  exit 0
fi

# Read input from Copilot
INPUT=$(cat)

# Create logs directory if it doesn't exist
mkdir -p logs/copilot

# Extract timestamp and session info
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CWD=$(pwd)

# Log session start without recording prompt or tool content.
python3 -c 'import json,sys; print(json.dumps({"timestamp":sys.argv[1],"event":"sessionStart","cwd":sys.argv[2]}))' \
  "$TIMESTAMP" "$CWD" >> logs/copilot/session.log

echo "📝 Session logged"
exit 0

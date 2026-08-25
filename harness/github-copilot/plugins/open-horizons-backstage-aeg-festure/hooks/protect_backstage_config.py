#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to critical Backstage governance surfaces.

Exit code 2 blocks the write and returns guidance on stderr so the agent can
correct its plan.
"""

import json
import re
import sys

PROTECTED = [
    r"app-config\.production\.yaml$",
    r"packages/backend/src/plugins/auth\.ts$",
    r"backstage/ai-kit/agents/",  # agent registry changes require a human-reviewed PR
]
data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
for rx in PROTECTED:
    if re.search(rx, path):
        print(
            f"BLOCKED: {path} is a portal governance surface. "
            "Open a dedicated PR with platform-team review.",
            file=sys.stderr,
        )
        sys.exit(2)
sys.exit(0)

#!/usr/bin/env python3
"""PostToolUse hook: scan app-config edits for literal credential values.

If an app-config file was edited, inspect credential-like fields (`token`,
`key`, `secret`, `password`). Exit code 2 asks the agent to replace them.
"""

import json
import pathlib
import re
import sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
if not re.search(r"app-config.*\.yaml$", path):
    sys.exit(0)
try:
    text = pathlib.Path(path).read_text(encoding="utf-8")
except OSError:
    sys.exit(0)
leaks = [
    line.strip()
    for line in text.splitlines()
    if re.search(
        r"(token|key|secret|password)\s*:\s*[A-Za-z0-9+/_\-]{12,}",
        line,
    )
    and "${" not in line
]
if leaks:
    print(
        "POSSIBLE LITERAL SECRET in config: replace it with ${ENV_VAR}. "
        "Lines: " + " | ".join(leaks[:3]),
        file=sys.stderr,
    )
    sys.exit(2)
sys.exit(0)

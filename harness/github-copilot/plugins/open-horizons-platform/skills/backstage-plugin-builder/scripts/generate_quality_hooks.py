#!/usr/bin/env python3
"""Generate safe local quality hooks for Backstage plugin repositories."""

from __future__ import annotations

import argparse
import json
import stat
from pathlib import Path


HOOK = """#!/usr/bin/env bash
set -euo pipefail

if ! command -v yarn >/dev/null 2>&1; then
  echo "yarn not found, skipping Backstage plugin quality hook"
  exit 0
fi

if [ ! -f package.json ]; then
  echo "package.json not found, skipping Backstage plugin quality hook"
  exit 0
fi

run_if_present() {
  local script="$1"
  if node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts['$script'] ? 0 : 1)"; then
    yarn "$script"
  else
    echo "script $script missing, skipping"
  fi
}

run_if_present lint
run_if_present tsc
run_if_present test
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate local Backstage plugin quality hooks")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not (root / "package.json").exists():
        print(f"No package.json at {root}; creating hook anyway for future use")
    hooks = root / ".githooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook_file = hooks / "pre-commit"
    hook_file.write_text(HOOK, encoding="utf-8")
    hook_file.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    print(f"wrote {hook_file}")
    print("enable with: git config core.hooksPath .githooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

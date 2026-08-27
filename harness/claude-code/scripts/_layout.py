"""Repository layout constants for the Claude Code harness."""

from __future__ import annotations

from pathlib import Path

SOURCE_HARNESS_RELATIVE = Path("harness") / "github-copilot"
HARNESS_RELATIVE = Path("harness") / "claude-code"
INSTALLED_MANIFEST_RELATIVE = HARNESS_RELATIVE / "manifests" / "installed-primitives.json"
MARKETPLACE_RELATIVE = Path(".claude-plugin") / "marketplace.json"


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        has_checkout = (candidate / ".git").exists()
        has_harness = (candidate / HARNESS_RELATIVE).is_dir()
        has_repository_files = (candidate / "README.md").is_file() and (candidate / "docs").is_dir()
        if has_checkout or (has_harness and has_repository_files):
            return candidate
    raise ValueError(f"repository root not found from {start}")


REPO_ROOT = find_repo_root(Path(__file__).resolve())

SOURCE_HARNESS_ROOT = REPO_ROOT / SOURCE_HARNESS_RELATIVE
SOURCE_AGENTS_ROOT = SOURCE_HARNESS_ROOT / "agents"
SOURCE_INSTRUCTIONS_ROOT = SOURCE_HARNESS_ROOT / "instructions"
SOURCE_SKILLS_ROOT = SOURCE_HARNESS_ROOT / "skills"
SOURCE_PROMPTS_ROOT = SOURCE_HARNESS_ROOT / "prompts"
SOURCE_HOOKS_ROOT = SOURCE_HARNESS_ROOT / "hooks"
SOURCE_PLUGINS_ROOT = SOURCE_HARNESS_ROOT / "plugins"

HARNESS_ROOT = REPO_ROOT / HARNESS_RELATIVE
AGENTS_ROOT = HARNESS_ROOT / "agents"
RULES_ROOT = HARNESS_ROOT / "rules"
SKILLS_ROOT = HARNESS_ROOT / "skills"
COMMANDS_ROOT = HARNESS_ROOT / "commands"
HOOKS_ROOT = HARNESS_ROOT / "hooks"
PLUGINS_ROOT = HARNESS_ROOT / "plugins"
MANIFESTS_ROOT = HARNESS_ROOT / "manifests"

INSTALLED_MANIFEST_PATH = REPO_ROOT / INSTALLED_MANIFEST_RELATIVE
MARKETPLACE_PATH = REPO_ROOT / MARKETPLACE_RELATIVE
DOCS_ROOT = REPO_ROOT / "docs"

GENERATED_ROOTS = (AGENTS_ROOT, RULES_ROOT, SKILLS_ROOT, COMMANDS_ROOT, HOOKS_ROOT, PLUGINS_ROOT)

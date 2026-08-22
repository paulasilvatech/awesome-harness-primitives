"""Repository layout constants for the GitHub Copilot harness."""

from __future__ import annotations

from pathlib import Path

HARNESS_RELATIVE = Path("harness") / "github-copilot"
INSTALLED_MANIFEST_RELATIVE = HARNESS_RELATIVE / "manifests" / "installed-primitives.json"
PLUGIN_SOURCES_RELATIVE = HARNESS_RELATIVE / "manifests" / "plugin-sources.json"
MARKETPLACE_RELATIVE = Path(".github") / "plugin" / "marketplace.json"


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        has_checkout = (candidate / ".git").exists()
        has_harness = (candidate / HARNESS_RELATIVE).is_dir()
        has_repository_files = (candidate / "README.md").is_file() and (candidate / "docs").is_dir()
        if has_checkout or (has_harness and has_repository_files):
            return candidate
    raise ValueError(f"repository root not found from {start}")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
HARNESS_ROOT = REPO_ROOT / HARNESS_RELATIVE
AGENTS_ROOT = HARNESS_ROOT / "agents"
INSTRUCTIONS_ROOT = HARNESS_ROOT / "instructions"
SKILLS_ROOT = HARNESS_ROOT / "skills"
PROMPTS_ROOT = HARNESS_ROOT / "prompts"
HOOKS_ROOT = HARNESS_ROOT / "hooks"
PLUGIN_ROOT = HARNESS_ROOT / "plugins"
MANIFESTS_ROOT = HARNESS_ROOT / "manifests"
INSTALLED_MANIFEST_PATH = REPO_ROOT / INSTALLED_MANIFEST_RELATIVE
PLUGIN_SOURCES_PATH = REPO_ROOT / PLUGIN_SOURCES_RELATIVE
MARKETPLACE_PATH = REPO_ROOT / MARKETPLACE_RELATIVE
DOCS_ROOT = REPO_ROOT / "docs"

# Source metadata uses this historical value for shared canonical components.
SHARED_COMPONENT_SOURCE = "library"

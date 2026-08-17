"""Configuration management for rhdh CLI.

Layered configuration with project-local and user-global support.

Config locations (highest to lowest priority):
1. Environment variables (RHDH_OVERLAY_REPO, etc.)
2. Project config (.rhdh/config.json in git root)
3. User config (~/.config/rhdh/config.json)
4. Auto-detection (../repo/ relative to skill install)

Supports dot-notation keys (e.g., repos.overlay, user.name).
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Optional

# Config directory names
PROJECT_CONFIG_DIR_NAME = ".rhdh"
USER_CONFIG_DIR = Path.home() / ".config" / "rhdh-skill"
USER_CONFIG_FILE = USER_CONFIG_DIR / "config.json"

# Environment variable for data directory override
DATA_DIR_ENV_VAR = "RHDH_SKILL_DATA_DIR"

# Submodule repository definitions
# Format: name -> {has_fork, required, config_key, description}
# Repos with has_fork=True use user's fork as origin, redhat-developer as upstream
# Repos with has_fork=False use redhat-developer as origin (no upstream)
SUBMODULE_REPOS: dict[str, dict] = {
    "rhdh": {
        "has_fork": False,
        "required": False,
        "config_key": "rhdh",
        "description": "Main RHDH application (enterprise Backstage distribution)",
    },
    "rhdh-downstream": {
        "has_fork": False,
        "required": False,
        "config_key": "downstream",
        "description": "Downstream productized RHDH build (internal GitLab)",
        "upstream_host": "gitlab.cee.redhat.com",
        "upstream_path": "rhidp/rhdh",
    },
    "rhdh-cli": {
        "has_fork": False,
        "required": False,
        "config_key": "cli",
        "description": "CLI for developing/packaging dynamic plugins",
    },
    "rhdh-plugins": {
        "has_fork": False,
        "required": False,
        "config_key": "plugins",
        "description": "Red Hat Backstage plugins (multi-workspace monorepo)",
    },
    "rhdh-plugin-export-overlays": {
        "has_fork": True,  # Users fork this repo to contribute
        "required": False,
        "config_key": "overlay",
        "description": "Plugin overlay repository (community plugin packaging)",
    },
    "rhdh-plugin-export-utils": {
        "has_fork": False,
        "required": False,
        "config_key": "export-utils",
        "description": "Reusable GitHub Actions for plugin packaging",
    },
    "rhdh-plugin-catalog": {
        "has_fork": False,
        "required": False,
        "config_key": "catalog",
        "description": "Midstream plugin builds, OCI artifacts & catalog index",
        "upstream_host": "gitlab.cee.redhat.com",
        "upstream_path": "rhidp/rhdh-plugin-catalog",
    },
    "rhdh-operator": {
        "has_fork": False,
        "required": False,
        "config_key": "operator",
        "description": "Kubernetes/OpenShift operator for RHDH",
    },
    "rhdh-chart": {
        "has_fork": False,
        "required": False,
        "config_key": "chart",
        "description": "Helm chart for RHDH deployment",
    },
    "rhdh-local": {
        "has_fork": False,  # No fork needed, clone directly
        "required": False,
        "config_key": "local",
        "description": "Local RHDH testing environment (Docker Compose)",
    },
    "rhdh-dynamic-plugin-factory": {
        "has_fork": False,
        "required": False,
        "config_key": "factory",
        "description": "Container for local dynamic plugin building",
    },
    "backstage": {
        "has_fork": False,
        "required": False,
        "config_key": "backstage",
        "description": "Upstream Backstage framework",
        "upstream_org": "backstage",
    },
}

# GitHub organization for upstream repos
GITHUB_ORG = "redhat-developer"

# Submodule base directory (relative to git root)
SUBMODULE_DIR = "repo"


# =============================================================================
# Path Discovery
# =============================================================================


def find_git_root() -> Path | None:
    """Find the git repository root, or None if not in a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_project_config_dir() -> Path:
    """Get project config directory (.rhdh/ in git root or cwd)."""
    git_root = find_git_root()
    base = git_root if git_root else Path.cwd()
    return base / PROJECT_CONFIG_DIR_NAME


def get_data_dir() -> Path:
    """Get the data directory for worklog and todos.

    Always centralizes data in one location to avoid scattering
    across different repos/worktrees.

    Uses RHDH_DATA_DIR env var if set, otherwise ~/.config/rhdh/.
    """
    env_value = os.environ.get(DATA_DIR_ENV_VAR)
    if env_value:
        return Path(env_value)
    return USER_CONFIG_DIR


def get_project_config_path() -> Path:
    """Get project config.json path."""
    return get_project_config_dir() / "config.json"


def get_user_config_path() -> Path:
    """Get user config.json path."""
    return USER_CONFIG_FILE


def get_skill_root() -> Path:
    """Get the skill root directory.

    Uses SKILL_ROOT env var if set, otherwise derives from package location.
    """
    if "SKILL_ROOT" in os.environ:
        return Path(os.environ["SKILL_ROOT"])
    # Package is in rhdh/, skill root is parent
    return Path(__file__).parent.parent


# =============================================================================
# Dot-notation Helpers
# =============================================================================


def get_nested(data: dict, key: str) -> Any:
    """Get a value using dot-notation.

    Args:
        data: The config dictionary
        key: Dot-notation key (e.g., "repos.overlay")

    Returns:
        The value at the key path

    Raises:
        KeyError: If key not found
    """
    parts = key.split(".")
    current = data

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise KeyError(f"Key not found: {key}")

    return current


def set_nested(data: dict, key: str, value: Any) -> None:
    """Set a value using dot-notation, creating nested dicts as needed.

    Args:
        data: The config dictionary (modified in place)
        key: Dot-notation key (e.g., "repos.overlay")
        value: The value to set
    """
    parts = key.split(".")
    current = data

    # Navigate/create path to parent
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        elif not isinstance(current[part], dict):
            # Replace non-dict value with dict
            current[part] = {}
        current = current[part]

    # Set the final key
    current[parts[-1]] = value


def collect_keys(data: dict, prefix: str = "") -> list[str]:
    """Collect all dot-notation paths in a nested dict.

    Args:
        data: The config dictionary
        prefix: Current path prefix

    Returns:
        List of all dot-notation paths
    """
    keys = []
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            # Recurse into nested dict
            keys.extend(collect_keys(value, full_key))
        else:
            # Leaf node
            keys.append(full_key)
    return keys


def parse_value(value_str: str) -> Any:
    """Parse a value string, attempting JSON if possible.

    Args:
        value_str: The string value

    Returns:
        Parsed value (JSON object/array/bool/number) or original string
    """
    # Try to parse as JSON
    try:
        return json.loads(value_str)
    except json.JSONDecodeError:
        # Return as string
        return value_str


def deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dicts, with override taking precedence.

    Args:
        base: Base dictionary
        override: Override dictionary (values take precedence)

    Returns:
        New merged dictionary
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


# =============================================================================
# Config Loading/Saving
# =============================================================================


def load_user_config() -> dict:
    """Load user config from ~/.config/rhdh/config.json.

    Returns:
        Config dict, or empty dict if file doesn't exist.
    """
    config_path = get_user_config_path()
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def load_project_config() -> dict:
    """Load project config from .rhdh/config.json.

    Returns:
        Config dict, or empty dict if file doesn't exist.
    """
    config_path = get_project_config_path()
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def load_merged_config() -> dict:
    """Load merged config (user + project, project takes precedence).

    Returns:
        Merged config dict.
    """
    user_config = load_user_config()
    project_config = load_project_config()
    return deep_merge(user_config, project_config)


def save_config(config: dict, global_: bool = False) -> bool:
    """Save config to file.

    Args:
        config: Config dictionary to save
        global_: If True, save to user config; otherwise project config

    Returns:
        True on success, False on failure
    """
    if global_:
        config_path = get_user_config_path()
        config_dir = USER_CONFIG_DIR
    else:
        config_path = get_project_config_path()
        config_dir = get_project_config_dir()

    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(config, indent=2) + "\n")
        return True
    except OSError:
        return False


# =============================================================================
# Repo Discovery (uses merged config)
# =============================================================================


def _repo_name_to_config_key(repo_name: str) -> str:
    """Map a repo directory name to its config key."""
    repo_info = SUBMODULE_REPOS.get(repo_name)
    if repo_info:
        return repo_info["config_key"]
    return repo_name


def _config_key_to_env_var(config_key: str) -> str:
    """Map a config key to its environment variable name."""
    return f"RHDH_{config_key.upper().replace('-', '_')}_REPO"


def find_repo(repo_name: str, env_var: str) -> Optional[Path]:
    """Find a repository in well-known locations.

    Args:
        repo_name: Directory name to look for (e.g., "rhdh-plugin-export-overlays")
        env_var: Environment variable that can override (e.g., "RHDH_OVERLAY_REPO")

    Returns:
        Path to the repository, or None if not found.

    Discovery order:
    1. Environment variable override
    2. Merged config (project + user)
    3. Skill install root (../repo/ relative to skill)
    4. Parent's repo/ directory (if skill is deeper nested)
    """
    # 1. Environment variable override
    env_value = os.environ.get(env_var)
    if env_value:
        path = Path(env_value)
        if path.is_dir():
            return path.resolve()

    # 2. Merged config (project overrides user)
    config = load_merged_config()
    # Map repo directory names to config keys
    config_key = _repo_name_to_config_key(repo_name)
    config_path = config.get("repos", {}).get(config_key)
    if config_path:
        path = Path(config_path)
        if path.is_dir():
            return path.resolve()

    # 3. Skill install root (../repo/ relative to skill)
    skill_root = get_skill_root()
    skill_repo_path = skill_root.parent / "repo" / repo_name
    if skill_repo_path.is_dir():
        return skill_repo_path.resolve()

    # 4. Parent's repo/ directory (if skill is deeper nested)
    parent_repo_path = skill_root.parent.parent / "repo" / repo_name
    if parent_repo_path.is_dir():
        return parent_repo_path.resolve()

    return None


def get_repo(config_key: str) -> Optional[Path]:
    """Get path to a repo by its config key.

    Args:
        config_key: The config key (e.g., "overlay", "local", "rhdh", "cli")

    Returns:
        Path to the repository, or None if not found.
    """
    # Find the repo name from the config key
    for repo_name, info in SUBMODULE_REPOS.items():
        if info["config_key"] == config_key:
            env_var = _config_key_to_env_var(config_key)
            return find_repo(repo_name, env_var)
    return None


def get_overlay_repo() -> Optional[Path]:
    """Get path to rhdh-plugin-export-overlays repo."""
    return get_repo("overlay")


def get_local_repo() -> Optional[Path]:
    """Get path to rhdh-local repo."""
    return get_repo("local")


def get_factory_repo() -> Optional[Path]:
    """Get path to rhdh-dynamic-plugin-factory repo."""
    return get_repo("factory")


def find_local_setup_dir() -> Optional[Path]:
    """Find the rhdh-local-setup workspace directory.

    rhdh-local-setup is a personal workspace wrapper (not a GitHub repo/submodule).

    Discovery order:
    1. RHDH_LOCAL_SETUP_DIR environment variable
    2. repos.local_setup in merged config
    3. Auto-detect: <repos.local>/../rhdh-local-setup (sibling of rhdh-local)
    4. Auto-detect: <skill_root>/../../rhdh-local-setup
    """
    # 1. Environment variable
    env_value = os.environ.get("RHDH_LOCAL_SETUP_DIR")
    if env_value:
        path = Path(env_value)
        if path.is_dir():
            return path.resolve()

    # 2. Merged config
    config = load_merged_config()
    config_path = config.get("repos", {}).get("local_setup")
    if config_path:
        path = Path(config_path)
        if path.is_dir():
            return path.resolve()

    # 3. Auto-detect: sibling of rhdh-local
    local_repo = get_local_repo()
    if local_repo:
        candidate = local_repo.parent / "rhdh-local-setup"
        if candidate.is_dir():
            return candidate.resolve()
        # rhdh-local may be inside rhdh-local-setup/
        candidate2 = local_repo.parent
        if (candidate2 / "rhdh-customizations").is_dir():
            return candidate2.resolve()

    # 4. Auto-detect: relative to skill root
    skill_root = get_skill_root()
    candidate = skill_root.parent.parent / "rhdh-local-setup"
    if candidate.is_dir():
        return candidate.resolve()

    return None


def get_local_setup_dir() -> Optional[Path]:
    """Get path to rhdh-local-setup workspace directory."""
    return find_local_setup_dir()


# =============================================================================
# Config Commands
# =============================================================================


def get_default_config() -> dict:
    """Get default configuration values."""
    repos = {info["config_key"]: "" for info in SUBMODULE_REPOS.values()}
    repos["local_setup"] = ""
    return {"repos": repos}


def run_config(
    command: str,
    key: str | None = None,
    value: str | None = None,
    force: bool = False,
    global_: bool = False,
) -> tuple[bool, dict | str, list[str]]:
    """Run a config subcommand.

    Args:
        command: Subcommand (init, show, keys, get, set)
        key: Key for get/set commands
        value: Value for set command
        force: Force overwrite for init
        global_: Use global (user) config instead of project

    Returns:
        Tuple of (success: bool, data: dict|str, next_steps: list[str])
    """
    if command == "init":
        return _config_init(force, global_)
    elif command == "show":
        return _config_show(global_)
    elif command == "keys":
        return _config_keys(global_)
    elif command == "get":
        return _config_get(key)
    elif command == "set":
        return _config_set(key, value, global_)
    else:
        return False, f"Unknown config command: {command}", []


def _config_init(force: bool, global_: bool) -> tuple[bool, dict | str, list[str]]:
    """Create config with defaults."""
    if global_:
        config_path = get_user_config_path()
        config_dir = USER_CONFIG_DIR
        scope = "user"
    else:
        config_path = get_project_config_path()
        config_dir = get_project_config_dir()
        scope = "project"

    if config_path.exists() and not force:
        return (
            False,
            f"Config already exists at {config_path}. Use --force to overwrite.",
            ["rhdh config init --force", "rhdh config show"],
        )

    # Try to auto-detect repos for project config
    config = get_default_config()

    if not global_:
        skill_root = get_skill_root()
        for repo_name, info in SUBMODULE_REPOS.items():
            repo_path = skill_root.parent / "repo" / repo_name
            if repo_path.is_dir():
                config["repos"][info["config_key"]] = str(repo_path.resolve())

    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(config, indent=2) + "\n")
    except OSError as e:
        return False, f"Failed to write config: {e}", []

    data = {
        "created": str(config_path),
        "scope": scope,
        "config": config,
    }

    next_steps = ["rhdh config show", "rhdh doctor"]
    return True, data, next_steps


def _resolve_all_repos() -> dict[str, str | None]:
    """Resolve paths for all configured repos."""
    resolved = {}
    for info in SUBMODULE_REPOS.values():
        key = info["config_key"]
        path = get_repo(key)
        resolved[key] = str(path) if path else None
    return resolved


def _config_show(global_: bool) -> tuple[bool, dict, list[str]]:
    """Display config."""
    user_config = load_user_config()
    project_config = load_project_config()
    merged_config = deep_merge(user_config, project_config)

    data = {
        "user_config_path": str(get_user_config_path()),
        "project_config_path": str(get_project_config_path()),
        "user_config": user_config if user_config else None,
        "project_config": project_config if project_config else None,
        "merged_config": merged_config if merged_config else None,
        "resolved": {
            **_resolve_all_repos(),
            "local_setup": str(get_local_setup_dir()) if get_local_setup_dir() else None,
        },
    }

    next_steps = ["rhdh config set <key> <value>", "rhdh config keys"]
    return True, data, next_steps


def _config_keys(global_: bool) -> tuple[bool, dict, list[str]]:
    """List all config keys in dot-notation."""
    if global_:
        config = load_user_config()
        scope = "user"
    else:
        config = load_merged_config()
        scope = "merged"

    if not config:
        return (
            False,
            "No config found. Run 'rhdh config init' first.",
            ["rhdh config init"],
        )

    keys = sorted(collect_keys(config))
    data = {"scope": scope, "keys": keys}
    return True, data, []


def _config_get(key: str | None) -> tuple[bool, dict | str, list[str]]:
    """Get a config value."""
    if not key:
        return False, "Key is required for 'config get'", ["rhdh config keys"]

    config = load_merged_config()
    if not config:
        return (
            False,
            "No config found. Run 'rhdh config init' first.",
            ["rhdh config init"],
        )

    try:
        value = get_nested(config, key)
        return True, {"key": key, "value": value}, []
    except KeyError:
        return (
            False,
            f"Key '{key}' not found in config",
            ["rhdh config keys"],
        )


def _config_set(
    key: str | None, value: str | None, global_: bool
) -> tuple[bool, dict | str, list[str]]:
    """Set a config value."""
    if not key:
        return False, "Key is required for 'config set'", []
    if value is None:
        return False, "Value is required for 'config set'", []

    # Map shorthand keys to full dot-notation paths
    all_config_keys = {info["config_key"] for info in SUBMODULE_REPOS.values()}
    all_config_keys.add("local_setup")
    if key in all_config_keys:
        key = f"repos.{key}"

    # Load appropriate config
    if global_:
        config = load_user_config()
        scope = "user"
    else:
        config = load_project_config()
        scope = "project"

    # Parse value (JSON if valid, otherwise string)
    parsed_value = parse_value(value)

    # Set the value using dot-notation
    set_nested(config, key, parsed_value)

    # Save
    if save_config(config, global_=global_):
        config_path = get_user_config_path() if global_ else get_project_config_path()
        data = {
            "key": key,
            "value": parsed_value,
            "scope": scope,
            "config_path": str(config_path),
        }
        return True, data, ["rhdh config show"]
    else:
        return False, "Failed to write config", []


# =============================================================================
# GitHub Username Detection
# =============================================================================


def get_github_username() -> str | None:
    """Get the authenticated GitHub username via gh CLI.

    Returns:
        GitHub username, or None if not authenticated or gh not available.
    """
    # First check config
    config = load_merged_config()
    cached_username = config.get("github", {}).get("username")
    if cached_username:
        return cached_username

    # Detect via gh CLI
    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            username = result.stdout.strip()
            if username:
                return username
    except FileNotFoundError:
        pass

    return None


def save_github_username(username: str, global_: bool = False) -> bool:
    """Save GitHub username to config.

    Args:
        username: GitHub username to save
        global_: If True, save to user config; otherwise project config

    Returns:
        True on success
    """
    if global_:
        config = load_user_config()
    else:
        config = load_project_config()

    set_nested(config, "github.username", username)
    return save_config(config, global_=global_)


def get_repo_urls(repo_name: str, github_username: str | None = None) -> tuple[str, str | None]:
    """Get origin and upstream URLs for a repository.

    Args:
        repo_name: Repository name (key in SUBMODULE_REPOS)
        github_username: GitHub username for fork URLs (auto-detected if None)

    Returns:
        Tuple of (origin_url, upstream_url or None)
    """
    if repo_name not in SUBMODULE_REPOS:
        raise ValueError(f"Unknown repository: {repo_name}")

    repo_info = SUBMODULE_REPOS[repo_name]
    has_fork = repo_info.get("has_fork", False)

    # Determine upstream org/host
    upstream_org = repo_info.get("upstream_org", GITHUB_ORG)
    upstream_host = repo_info.get("upstream_host")
    upstream_path = repo_info.get("upstream_path")

    if has_fork:
        # User's fork as origin, upstream org as upstream
        if github_username is None:
            github_username = get_github_username()
        if not github_username:
            raise ValueError(
                f"GitHub username required for {repo_name} (has fork). "
                "Run 'gh auth login' or set github.username in config."
            )
        origin_url = f"git@github.com:{github_username}/{repo_name}.git"
        upstream_url = f"git@github.com:{upstream_org}/{repo_name}.git"
    elif upstream_host:
        # Non-GitHub repo (e.g., GitLab)
        path = upstream_path or repo_name
        origin_url = f"git@{upstream_host}:{path}.git"
        upstream_url = None
    else:
        # Direct clone from GitHub org
        origin_url = f"git@github.com:{upstream_org}/{repo_name}.git"
        upstream_url = None

    return origin_url, upstream_url


# =============================================================================
# Submodule Setup
# =============================================================================


def is_submodule(repo_path: Path) -> bool:
    """Check if a path is already configured as a git submodule."""
    git_root = find_git_root()
    if not git_root:
        return False

    gitmodules = git_root / ".gitmodules"
    if not gitmodules.exists():
        return False

    # Check if path is in .gitmodules
    rel_path = str(repo_path.relative_to(git_root))
    content = gitmodules.read_text()
    return rel_path in content


def setup_submodule(
    name: str,
    dry_run: bool = False,
    github_username: str | None = None,
) -> tuple[bool, dict | str, list[str]]:
    """Set up a repository as a git submodule.

    Args:
        name: Repository name (key in SUBMODULE_REPOS)
        dry_run: If True, only show what would be done
        github_username: GitHub username for fork URLs (auto-detected if None)

    Returns:
        Tuple of (success: bool, data: dict|str, next_steps: list[str])
    """
    if name not in SUBMODULE_REPOS:
        available = ", ".join(SUBMODULE_REPOS.keys())
        return False, f"Unknown repository: {name}. Available: {available}", []

    repo_info = SUBMODULE_REPOS[name]
    config_key = repo_info["config_key"]

    # Get URLs (may raise if username needed but not available)
    try:
        origin_url, upstream_url = get_repo_urls(name, github_username)
    except ValueError as e:
        return (
            False,
            str(e),
            ["gh auth login", "rhdh config set github.username <your-username>"],
        )

    git_root = find_git_root()
    if not git_root:
        return (
            False,
            "Not in a git repository. Run from a git repo root.",
            ["cd /path/to/your/project", "git init"],
        )

    submodule_path = git_root / SUBMODULE_DIR / name

    if dry_run:
        actions = [f"Would create submodule at: {submodule_path}"]
        if upstream_url:
            actions.append(f"Would add upstream remote: {upstream_url}")
        actions.append(f"Would update config: repos.{config_key} = {submodule_path}")
        return True, {"dry_run": True, "actions": actions}, []

    # Create repo/ directory if needed
    repo_dir = git_root / SUBMODULE_DIR
    repo_dir.mkdir(parents=True, exist_ok=True)

    # Check if already a submodule
    if is_submodule(submodule_path):
        # Verify/update remotes
        if submodule_path.exists():
            _ensure_upstream(submodule_path, upstream_url)
        # Update config
        _update_config_for_submodule(config_key, submodule_path)
        return (
            True,
            {
                "status": "already_configured",
                "path": str(submodule_path),
                "config_key": f"repos.{config_key}",
            },
            ["rhdh config show"],
        )

    # Remove from .gitignore if present
    _remove_from_gitignore(git_root, name, f"{SUBMODULE_DIR}/{name}")

    # Handle existing directory (not a submodule)
    if submodule_path.exists():
        if (submodule_path / ".git").exists():
            # Nested git repo - need to remove it first
            return (
                False,
                f"Directory exists with nested .git: {submodule_path}. "
                "Remove it manually or back up first.",
                [f"rm -rf {submodule_path}", f"rhdh setup submodule add {name}"],
            )
        # Non-git directory - also needs manual handling
        return (
            False,
            f"Directory exists: {submodule_path}. Remove it first.",
            [f"rm -rf {submodule_path}", f"rhdh setup submodule add {name}"],
        )

    # Add as submodule
    try:
        result = subprocess.run(
            ["git", "submodule", "add", origin_url, f"{SUBMODULE_DIR}/{name}"],
            capture_output=True,
            text=True,
            cwd=git_root,
        )
        if result.returncode != 0:
            return (
                False,
                f"git submodule add failed: {result.stderr.strip()}",
                ["Check SSH key access to the repository"],
            )
    except FileNotFoundError:
        return False, "git not found", ["Install git"]

    # Add upstream remote if specified
    if upstream_url:
        _ensure_upstream(submodule_path, upstream_url)

    # Update config
    _update_config_for_submodule(config_key, submodule_path)

    data = {
        "status": "created",
        "path": str(submodule_path),
        "origin": origin_url,
        "upstream": upstream_url,
        "config_key": f"repos.{config_key}",
    }

    return True, data, ["rhdh", "rhdh config show"]


def _ensure_upstream(repo_path: Path, upstream_url: str | None) -> None:
    """Ensure upstream remote exists if URL is provided."""
    if not upstream_url or not repo_path.exists():
        return

    # Check if upstream already exists
    result = subprocess.run(
        ["git", "remote", "get-url", "upstream"],
        capture_output=True,
        text=True,
        cwd=repo_path,
    )

    if result.returncode != 0:
        # Add upstream
        subprocess.run(
            ["git", "remote", "add", "upstream", upstream_url],
            capture_output=True,
            cwd=repo_path,
        )


def _remove_from_gitignore(git_root: Path, *patterns: str) -> None:
    """Remove patterns from .gitignore if present."""
    gitignore = git_root / ".gitignore"
    if not gitignore.exists():
        return

    lines = gitignore.read_text().splitlines()
    new_lines = [line for line in lines if line.strip() not in patterns]

    if len(new_lines) != len(lines):
        gitignore.write_text("\n".join(new_lines) + "\n")


def _update_config_for_submodule(config_key: str, submodule_path: Path) -> None:
    """Update project config with submodule path."""
    config = load_project_config()
    set_nested(config, f"repos.{config_key}", str(submodule_path.resolve()))
    save_config(config, global_=False)


def list_submodule_repos() -> list[dict]:
    """List available submodule repositories and their status."""
    git_root = find_git_root()
    github_username = get_github_username()
    result = []

    for name, info in SUBMODULE_REPOS.items():
        status = "not_configured"
        path = None

        if git_root:
            submodule_path = git_root / SUBMODULE_DIR / name
            if is_submodule(submodule_path):
                status = "submodule"
                path = str(submodule_path)
            elif submodule_path.exists():
                status = "directory_exists"
                path = str(submodule_path)

        # Also check if configured via other means
        config_key = info["config_key"]
        discovered = get_repo(config_key)
        if discovered:
            status = "configured" if status == "not_configured" else status
            path = str(discovered) if not path else path

        # Get URLs if possible
        has_fork = info.get("has_fork", False)
        origin_url = None
        upstream_url = None
        needs_username = has_fork and not github_username

        if not needs_username:
            try:
                origin_url, upstream_url = get_repo_urls(name, github_username)
            except ValueError:
                needs_username = True

        result.append(
            {
                "name": name,
                "status": status,
                "path": path,
                "required": info["required"],
                "description": info["description"],
                "has_fork": has_fork,
                "origin": origin_url,
                "upstream": upstream_url,
                "needs_username": needs_username,
            }
        )

    return result


def get_github_username_or_prompt() -> tuple[str | None, str | None]:
    """Get GitHub username, returning error message if not available.

    Returns:
        Tuple of (username or None, error_message or None)
    """
    username = get_github_username()
    if username:
        return username, None

    return None, (
        "GitHub username not found. Either:\n"
        "  1. Run 'gh auth login' to authenticate\n"
        "  2. Run 'rhdh config set github.username <your-username>'"
    )


# =============================================================================
# Legacy API (for backward compatibility)
# =============================================================================


def config_init() -> tuple[bool, list[str]]:
    """Initialize configuration file (legacy API).

    Returns:
        Tuple of (created: bool, messages: list[str])
    """
    success, data, next_steps = _config_init(force=False, global_=False)
    messages = []

    if success:
        if isinstance(data, dict):
            messages.append(f"Created: {data.get('created', '')}")
            config = data.get("config", {})
            repos = config.get("repos", {})
            for info in SUBMODULE_REPOS.values():
                key = info["config_key"]
                if repos.get(key):
                    messages.append(f"Auto-detected {key}: {repos[key]}")
                elif info["required"]:
                    messages.append(
                        f"{key}: not found (configure with: rhdh config set {key} /path)"
                    )
    else:
        messages.append(str(data))

    return success, messages


def config_set(key: str, value: str) -> tuple[bool, str]:
    """Set a config value (legacy API).

    Args:
        key: Config key (can be dot-notation like repos.overlay)
        value: Value to set

    Returns:
        Tuple of (success: bool, message: str)
    """
    # _config_set handles shorthand key mapping internally
    success, data, _ = _config_set(key, value, global_=False)

    if success and isinstance(data, dict):
        return True, f"Set {data['key']} = {data['value']}"
    else:
        return False, str(data)


def get_config_info() -> dict:
    """Get configuration info for display.

    Returns:
        Dict with config paths and resolved values.
    """
    return {
        "user_config_path": str(get_user_config_path()),
        "project_config_path": str(get_project_config_path()),
        "skill_root": str(get_skill_root()),
        "user_config": load_user_config(),
        "project_config": load_project_config(),
        "resolved": {**_resolve_all_repos(), "local_setup": get_local_setup_dir()},
    }

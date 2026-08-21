"""rhdh_local -- Local RHDH operations (copy-sync, container lifecycle).

Standalone package for the rhdh-local-setup customization system.
"""

__version__ = "1.0.0"

from .backup import (
    BackupInfo,
    backup_customizations,
    list_backups,
    preview_restore,
    restore_customizations,
)
from .compose import (
    build_compose_args,
    detect_compose_command,
    local_down,
    local_up,
)
from .health import HealthCheck, check_local_health
from .settings import LastRunSettings, load_last_run, save_last_run
from .sync import (
    CUSTOMIZATION_FILES,
    CUSTOMIZATION_GLOBS,
    SyncResult,
    apply_customizations,
    remove_customizations,
)

__all__ = [
    # sync
    "SyncResult",
    "CUSTOMIZATION_FILES",
    "CUSTOMIZATION_GLOBS",
    "apply_customizations",
    "remove_customizations",
    # compose
    "detect_compose_command",
    "build_compose_args",
    "local_up",
    "local_down",
    # settings
    "LastRunSettings",
    "save_last_run",
    "load_last_run",
    # health
    "HealthCheck",
    "check_local_health",
    # backup
    "BackupInfo",
    "backup_customizations",
    "list_backups",
    "preview_restore",
    "restore_customizations",
]

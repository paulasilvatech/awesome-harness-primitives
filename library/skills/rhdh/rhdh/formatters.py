"""Output formatting for rhdh CLI.

Auto-detects output format based on context:
- TTY (terminal) → Human-readable with colors
- Not TTY (piped or agent-consumed) -> JSON for machine parsing

Override with --human or --json flags.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


def detect_output_mode() -> str:
    """Detect whether to use human or JSON output.

    Returns:
        "human" if stdout is a TTY, "json" otherwise
    """
    return "human" if sys.stdout.isatty() else "json"


# ANSI color codes
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
BOLD = "\033[1m"
NC = "\033[0m"  # No Color


@dataclass
class OutputFormatter:
    """Formats CLI output as JSON or human-readable.

    In human mode, commands use log_ok/log_warn/log_fail for inline output,
    then call success() just for next_steps. In JSON mode, success() outputs
    the full structured response.

    Attributes:
        mode: "human" for colored text, "json" for machine-parseable output
        verbose: Include debug information
    """

    mode: str = "auto"  # "auto", "human", or "json"
    verbose: bool = False
    _debug_info: dict[str, Any] = field(default_factory=dict)
    _has_human_output: bool = field(default=False, repr=False)

    def __post_init__(self):
        if self.mode == "auto":
            self.mode = detect_output_mode()

    @property
    def is_human(self) -> bool:
        return self.mode == "human"

    def add_debug(self, key: str, value: Any) -> None:
        """Add debug information (included if verbose=True)."""
        self._debug_info[key] = value

    # =========================================================================
    # Success Output
    # =========================================================================

    def success(
        self,
        data: dict[str, Any],
        next_steps: list[str] | None = None,
    ) -> None:
        """Output a success response."""
        if self.is_human:
            self._render_human_success(data, next_steps)
        else:
            self._render_json_success(data, next_steps)

    def _render_json_success(
        self,
        data: dict[str, Any],
        next_steps: list[str] | None,
    ) -> None:
        """Render success as JSON."""
        response = {
            "success": True,
            "data": data,
        }
        if next_steps:
            response["next_steps"] = next_steps
        if self.verbose and self._debug_info:
            response["debug"] = self._debug_info
        print(json.dumps(response, indent=2, default=str))

    def _render_human_success(
        self,
        data: dict[str, Any],
        next_steps: list[str] | None,
    ) -> None:
        """Render success as human-readable text.

        If log_* methods were used, skip data rendering (already shown inline).
        Only render next_steps.
        """
        if not self._has_human_output:
            # No inline output was done, render the data
            self._render_data(data)

        if next_steps:
            print(f"\n{BOLD}Next steps:{NC}")
            for step in next_steps:
                print(f"  {BLUE}{step}{NC}")

    def _render_data(self, data: dict[str, Any], indent: int = 0) -> None:
        """Recursively render data in human-readable format."""
        prefix = "  " * indent

        for key, value in data.items():
            if key == "checks" and isinstance(value, list):
                self._render_checks(value, prefix)
            elif key == "items" and isinstance(value, list):
                self._render_items(value, prefix)
            elif isinstance(value, dict):
                print(f"{prefix}{BOLD}{key}:{NC}")
                self._render_data(value, indent + 1)
            elif isinstance(value, list):
                if value:
                    print(f"{prefix}{BOLD}{key}:{NC}")
                    for item in value:
                        if isinstance(item, dict):
                            self._render_data(item, indent + 1)
                            print()
                        else:
                            print(f"{prefix}  - {item}")
            elif isinstance(value, bool):
                icon = f"{GREEN}✓{NC}" if value else f"{RED}✗{NC}"
                print(f"{prefix}{icon} {key}")
            else:
                print(f"{prefix}{key}: {value}")

    def _render_checks(self, checks: list[dict], prefix: str) -> None:
        """Render a list of check results."""
        for check in checks:
            status = check.get("status", "unknown")
            name = check.get("name", "unknown")
            message = check.get("message", "")

            if status == "pass":
                icon = f"{GREEN}✓{NC}"
            elif status == "warn":
                icon = f"{YELLOW}⚠{NC}"
            else:
                icon = f"{RED}✗{NC}"

            if message:
                print(f"{prefix}{icon} {name}: {message}")
            else:
                print(f"{prefix}{icon} {name}")

    def _render_items(self, items: list[dict], prefix: str) -> None:
        """Render a list of items (workspaces, etc.)."""
        for item in items:
            name = item.get("name", "unknown")
            detail = item.get("detail", "")
            print(f"{prefix}  {BLUE}{name:<30}{NC} {detail}")

    # =========================================================================
    # Error Output
    # =========================================================================

    def error(
        self,
        code: str,
        message: str,
        next_steps: list[str] | None = None,
    ) -> None:
        """Output an error response."""
        if self.is_human:
            self._render_human_error(code, message, next_steps)
        else:
            self._render_json_error(code, message, next_steps)

    def _render_json_error(
        self,
        code: str,
        message: str,
        next_steps: list[str] | None,
    ) -> None:
        """Render error as JSON."""
        response = {
            "success": False,
            "error": {
                "code": code,
                "message": message,
            },
        }
        if next_steps:
            response["next_steps"] = next_steps
        if self.verbose and self._debug_info:
            response["debug"] = self._debug_info
        print(json.dumps(response, indent=2))

    def _render_human_error(
        self,
        code: str,
        message: str,
        next_steps: list[str] | None,
    ) -> None:
        """Render error as human-readable text."""
        print(f"{RED}Error [{code}]:{NC} {message}", file=sys.stderr)

        if next_steps:
            print(f"\n{BOLD}To fix:{NC}")
            for step in next_steps:
                print(f"  - {step}")

    # =========================================================================
    # Convenience Methods (human-style logging)
    # =========================================================================

    def header(self, text: str) -> None:
        """Print a section header (human mode only, ignored in JSON)."""
        if self.is_human:
            print(f"\n{BOLD}{text}{NC}")
            self._has_human_output = True

    def log_ok(self, message: str) -> None:
        """Log success message (human mode only)."""
        if self.is_human:
            print(f"  {GREEN}✓{NC} {message}")
            self._has_human_output = True

    def log_warn(self, message: str) -> None:
        """Log warning message (human mode only)."""
        if self.is_human:
            print(f"  {YELLOW}⚠{NC} {message}")
            self._has_human_output = True

    def log_fail(self, message: str) -> None:
        """Log failure message (human mode only)."""
        if self.is_human:
            print(f"  {RED}✗{NC} {message}")
            self._has_human_output = True

    def log_info(self, message: str) -> None:
        """Log info message (human mode only)."""
        if self.is_human:
            print(f"  {BLUE}→{NC} {message}")
            self._has_human_output = True

    # =========================================================================
    # Rendering Methods (human mode only, ignored in JSON)
    # =========================================================================

    def render_list(
        self,
        items: list[dict],
        format_fn: Callable[[dict], str],
        *,
        summary: str | None = None,
    ) -> None:
        """Render a list of items (human mode only, ignored in JSON).

        Args:
            items: List of item dicts to render
            format_fn: Function that takes an item dict and returns formatted string
            summary: Optional summary line (e.g., "Total: 5 items")
        """
        if not self.is_human:
            return

        print()
        for item in items:
            print(f"  {format_fn(item)}")
        if summary:
            print()
            print(f"  {summary}")
        self._has_human_output = True

    def render_banner(
        self,
        message: str,
        call_to_action: str | None = None,
        style: str = "warn",
    ) -> None:
        """Render a call-to-action banner (human mode only, ignored in JSON).

        Args:
            message: Main message text
            call_to_action: Optional command to show
            style: "warn" (yellow) or "info" (blue)
        """
        if not self.is_human:
            return

        color = YELLOW if style == "warn" else BLUE
        print()
        print(f"{color}{message}{NC}")
        if call_to_action:
            print(f"  {call_to_action}")
        self._has_human_output = True

    def render_raw(self, content: str) -> None:
        """Render raw content (human mode only, ignored in JSON)."""
        if not self.is_human:
            return

        print(content)
        self._has_human_output = True

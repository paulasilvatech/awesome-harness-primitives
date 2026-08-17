"""Todo management for rhdh CLI.

Section-based markdown todo tracker.
Stored in ~/.config/rhdh/TODO.md (or RHDH_DATA_DIR if set).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .config import get_data_dir

TODO_FILENAME = "TODO.md"


def get_todo_file() -> Path:
    """Get the todo file path.

    Uses centralized data directory to avoid scattering todos
    across different repos/worktrees.
    """
    return get_data_dir() / TODO_FILENAME


# Pattern for H2 todo headers: ## [ ] Title or ## [x] Title
TODO_HEADER_PATTERN = re.compile(r"^## \[([ x])\] (.+)$")

# Default template content
DEFAULT_TODO_CONTENT = """\
# RHDH Plugin Todos

Track uncertainties, follow-ups, and action items from plugin work.

---

<!-- TEMPLATE (do not remove)
## [ ] <title>
**Created:** <date>
**Context:** <optional workspace or PR context>

<description of what needs to be done>

### Notes
- <date>: <update>

---
-->
"""


@dataclass
class TodoItem:
    """Represents a single todo item."""

    slug: str
    title: str
    done: bool
    line_start: int  # Line number where H2 starts (0-indexed)
    line_end: int  # Line number where section ends (exclusive)
    created: Optional[str] = None
    completed: Optional[str] = None
    context: Optional[str] = None
    raw_content: str = ""  # Full section content


def slugify(title: str) -> str:
    """Convert title to a URL-friendly slug."""
    # Lowercase
    slug = title.lower()
    # Replace non-alphanumeric with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    # Remove leading/trailing hyphens
    slug = slug.strip("-")
    # Limit length
    if len(slug) > 50:
        slug = slug[:50].rsplit("-", 1)[0]
    return slug


def _ensure_todo_file() -> Path:
    """Ensure todo file exists with template, return path."""
    todo_file = get_todo_file()
    todo_file.parent.mkdir(parents=True, exist_ok=True)
    if not todo_file.exists():
        todo_file.write_text(DEFAULT_TODO_CONTENT)
    return todo_file


def _parse_todos(content: str) -> list[TodoItem]:
    """Parse todo items from markdown content.

    Each todo section ends at the next `---` separator or next H2 header.
    Skips content inside HTML comments (template section).
    """
    lines = content.split("\n")
    todos = []
    current_todo: Optional[dict] = None
    in_comment = False

    for i, line in enumerate(lines):
        # Track HTML comment blocks (skip template)
        if "<!--" in line:
            in_comment = True
        if "-->" in line:
            in_comment = False
            continue
        if in_comment:
            continue

        # Section separator ends current todo
        if line.strip() == "---" and current_todo is not None:
            current_todo["line_end"] = i
            todos.append(_make_todo_item(current_todo, lines))
            current_todo = None
            continue

        match = TODO_HEADER_PATTERN.match(line)
        if match:
            # Save previous todo (shouldn't happen if --- is used, but handle it)
            if current_todo is not None:
                current_todo["line_end"] = i
                todos.append(_make_todo_item(current_todo, lines))

            # Start new todo
            done = match.group(1) == "x"
            title = match.group(2).strip()
            current_todo = {
                "title": title,
                "done": done,
                "line_start": i,
                "line_end": len(lines),  # Will be updated
            }

    # Save last todo if no trailing ---
    if current_todo is not None:
        current_todo["line_end"] = len(lines)
        todos.append(_make_todo_item(current_todo, lines))

    return todos


def _make_todo_item(data: dict, lines: list[str]) -> TodoItem:
    """Create TodoItem from parsed data."""
    section_lines = lines[data["line_start"] : data["line_end"]]
    raw_content = "\n".join(section_lines)

    # Extract metadata from section
    created = None
    completed = None
    context = None

    for line in section_lines:
        if line.startswith("**Created:**"):
            created = line.replace("**Created:**", "").strip()
        elif line.startswith("**Completed:**"):
            completed = line.replace("**Completed:**", "").strip()
        elif line.startswith("**Context:**"):
            context = line.replace("**Context:**", "").strip()

    return TodoItem(
        slug=slugify(data["title"]),
        title=data["title"],
        done=data["done"],
        line_start=data["line_start"],
        line_end=data["line_end"],
        created=created,
        completed=completed,
        context=context,
        raw_content=raw_content,
    )


def list_todos(include_done: bool = True) -> list[TodoItem]:
    """List all todo items.

    Args:
        include_done: Whether to include completed items

    Returns:
        List of TodoItem objects
    """
    todo_file = _ensure_todo_file()
    content = todo_file.read_text()
    todos = _parse_todos(content)

    if not include_done:
        todos = [t for t in todos if not t.done]

    return todos


def get_todo(slug: str) -> Optional[TodoItem]:
    """Get a todo by slug.

    Args:
        slug: The todo slug (or partial match)

    Returns:
        TodoItem if found, None otherwise
    """
    todos = list_todos()

    # Exact match first
    for todo in todos:
        if todo.slug == slug:
            return todo

    # Partial match (starts with)
    for todo in todos:
        if todo.slug.startswith(slug):
            return todo

    return None


def add_todo(title: str, context: Optional[str] = None) -> TodoItem:
    """Add a new todo item.

    Args:
        title: The todo title
        context: Optional context (workspace, PR, etc.)

    Returns:
        The created TodoItem
    """
    todo_file = _ensure_todo_file()
    content = todo_file.read_text()
    lines = content.split("\n")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Build new section
    new_section = [
        f"## [ ] {title}",
        f"**Created:** {today}",
    ]
    if context:
        new_section.append(f"**Context:** {context}")
    new_section.extend(
        [
            "",
            "",
            "### Notes",
            f"- {today}: Created",
            "",
            "---",
            "",
        ]
    )

    # Find insertion point (after header, before first todo or template)
    insert_at = None
    for i, line in enumerate(lines):
        # After the first "---" separator (end of header)
        if line.strip() == "---" and insert_at is None:
            insert_at = i + 1
            break

    if insert_at is None:
        # Fallback: insert after first non-empty line
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith("#"):
                insert_at = i
                break
        if insert_at is None:
            insert_at = len(lines)

    # Insert new section
    new_lines = lines[:insert_at] + [""] + new_section + lines[insert_at:]
    todo_file.write_text("\n".join(new_lines))

    return TodoItem(
        slug=slugify(title),
        title=title,
        done=False,
        line_start=insert_at + 1,
        line_end=insert_at + 1 + len(new_section),
        created=today,
        context=context,
    )


def mark_done(slug: str) -> Optional[TodoItem]:
    """Mark a todo as done.

    Args:
        slug: The todo slug

    Returns:
        Updated TodoItem if found, None otherwise
    """
    todo = get_todo(slug)
    if not todo:
        return None

    if todo.done:
        return todo  # Already done

    todo_file = get_todo_file()
    content = todo_file.read_text()
    lines = content.split("\n")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Update the header line
    header_line = lines[todo.line_start]
    lines[todo.line_start] = header_line.replace("## [ ]", "## [x]")

    # Add completed date after Created line
    for i in range(todo.line_start, min(todo.line_end, len(lines))):
        if lines[i].startswith("**Created:**"):
            # Insert completed line after created
            lines.insert(i + 1, f"**Completed:** {today}")
            break

    todo_file.write_text("\n".join(lines))

    todo.done = True
    todo.completed = today
    return todo


def add_note(slug: str, note: str) -> Optional[TodoItem]:
    """Add a note to a todo item.

    Args:
        slug: The todo slug
        note: The note text

    Returns:
        Updated TodoItem if found, None otherwise
    """
    todo = get_todo(slug)
    if not todo:
        return None

    todo_file = get_todo_file()
    content = todo_file.read_text()
    lines = content.split("\n")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    note_line = f"- {today}: {note}"

    # Find "### Notes" section within the todo
    notes_line = None
    for i in range(todo.line_start, min(todo.line_end, len(lines))):
        if lines[i].strip() == "### Notes":
            notes_line = i
            break

    if notes_line is not None:
        # Insert note after "### Notes"
        lines.insert(notes_line + 1, note_line)
    else:
        # Create Notes section before section end
        # Find the "---" separator
        for i in range(todo.line_start, min(todo.line_end, len(lines))):
            if lines[i].strip() == "---":
                lines.insert(i, "")
                lines.insert(i, note_line)
                lines.insert(i, "### Notes")
                break

    todo_file.write_text("\n".join(lines))

    # Re-fetch to get updated content
    return get_todo(slug)


def show_raw() -> str:
    """Return the raw TODO.md content."""
    todo_file = _ensure_todo_file()
    return todo_file.read_text()


def get_todo_file_path() -> Path:
    """Return the path to the TODO.md file."""
    return get_todo_file()

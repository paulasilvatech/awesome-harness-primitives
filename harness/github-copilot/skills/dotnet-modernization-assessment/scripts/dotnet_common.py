"""Small shared parsers for local .NET assessment; no project code is executed."""

from __future__ import annotations

import json
import re
from pathlib import Path


class InputError(ValueError):
    """An input cannot be inspected safely or unambiguously."""


def framework_family(tfm: str) -> str:
    if re.fullmatch(r"net[1-4]\d{1,2}", tfm):
        return "net-framework"
    if re.fullmatch(r"netstandard\d+\.\d+", tfm):
        return "net-standard"
    if re.fullmatch(r"netcoreapp\d+\.\d+", tfm):
        return "net-core"
    if re.fullmatch(r"net(?:[5-9]|[1-9]\d+)\.\d+(?:-[a-z0-9.]+)?", tfm):
        return "modern-dotnet"
    return "unknown"


def read_text(path: Path, max_bytes: int) -> str:
    if path.is_symlink() or not path.is_file():
        raise InputError("not a regular, non-symlink file")
    with path.open("rb") as stream:
        content = stream.read(max_bytes + 1)
    if len(content) > max_bytes:
        raise InputError(f"file exceeds {max_bytes} bytes")
    encoding = "utf-16" if content.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
    try:
        return content.decode(encoding)
    except UnicodeError as error:
        raise InputError("text is not UTF-8 or BOM-marked UTF-16") from error


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise InputError("JSON contains duplicate object keys")
        result[key] = value
    return result


def read_json(path: Path, max_bytes: int = 1024 * 1024) -> object:
    text = read_text(path, max_bytes)
    try:
        return json.loads(text, object_pairs_hook=unique_object)
    except json.JSONDecodeError as error:
        raise InputError("invalid JSON") from error

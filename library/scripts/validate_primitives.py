#!/usr/bin/env python3
"""Validate Copilot primitives against the harness spec and repository contracts.

The validator is intentionally dependency-light. It prefers PyYAML when
available and falls back to a small frontmatter parser that supports the YAML
subset used by Copilot primitive metadata.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shlex
import stat
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - environment dependent
    yaml = None

KIND_PREFIX = {
    "agents": "AG",
    "instructions": "IN",
    "skills": "SK",
    "prompts": "PR",
    "plugins": "PL",
    "hooks": "HK",
}
ALL_KINDS = ("agents", "instructions", "skills", "prompts", "plugins", "hooks")

AG_FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]+\.agent\.md$")
IN_FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]+\.instructions\.md$")
PR_FILENAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.prompt\.md$")
SK_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
PL_NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9][a-z0-9.-]*[a-z0-9]$|^[a-z0-9]$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+].*)?$")
MCP_TOOL_RE = re.compile(r"^([a-zA-Z0-9_.-]+/(?:\*|[a-zA-Z0-9_.-]+))(?::(.+))?$")
LEGACY_MODEL_RE = re.compile(r"^(GPT|Claude|Gemini|o[0-9])")
SK_WHEN_RE = re.compile(r"use when|use this skill when|when you|when the user|for when|invoke when|trigger", re.I)
LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
PROMPT_FILE_RE = re.compile(r"[\w./-]*\.prompt\.md\b")
TEMPLATE_PLACEHOLDER_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")

PORTABLE_TOOLS = {
    "execute", "shell", "bash", "powershell",
    "read", "view", "notebookread",
    "edit", "write", "create", "multiedit", "notebookedit",
    "search", "grep", "glob",
    "agent", "task", "custom-agent",
    "web", "web_fetch", "web_search", "websearch", "webfetch",
    "todo", "todowrite", "update_todo",
}
NATIVE_TOOLS = {"grep", "glob", "view", "bash", "read_bash", "stop_bash", "powershell", "read_powershell", "stop_powershell", "lsp"}
VSCODE_ONLY = {
    "codebase", "editfiles", "vscodeapi", "opensimplebrowser", "findtestfiles", "githubrepo",
    "terminallastcommand", "terminalselection", "testfailure", "problems", "usages", "changes",
    "runcommands", "runtasks", "runtests", "searchresults", "extensions", "new", "fetch",
}
AG_RETIRED_KEYS = {"infer", "mode", "hidden", "agents", "agent", "title"}
# Tokens the CLI accepts without complaint but which grant zero tools. Verified
# empirically against CLI 1.0.81-0; see docs/HARNESS-VALIDATION.md. Declaring one
# silently removes capability, so these are errors rather than warnings.
NOOP_TOOLS: dict[str, list[str]] = {
    "search": ["grep", "glob"],
    "web": ["web_fetch", "web_search"],
    "todo": [],
    "all": ["*"],
    "terminal": ["bash"],
    "run": ["bash"],
    "codebase": ["grep", "glob", "view"],
    "fetch": ["web_fetch"],
    "changes": [],
    "githubrepo": [],
    "search/codebase": ["grep", "glob"],
}
AG_VSCODE_KEYS = {"argument-hint", "handoffs"}
IN_VALID_KEYS = {"applyTo", "name", "description", "excludeAgent"}
SK_VALID_KEYS = {"name", "description", "user-invocable", "disable-model-invocation", "allowed-tools", "argument-hint", "license", "metadata", "tags"}
PR_VALID_KEYS = {"name", "description", "argument-hint", "agent", "model", "tools"}
PL_VALID_KEYS = {"$schema", "name", "version", "description", "author", "email", "repository", "license", "homepage", "keywords", "extensions", "paths", "exclusive", "skills", "agents", "commands", "mcpServers", "lspServers", "outputStyles", "hooks", "postInstallMessage", "strict"}
OPEN_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
OPEN_MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
OPEN_PLUGIN_VALID_KEYS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
HK_VALID_KEYS = {"type", "bash", "powershell", "command", "cwd", "env", "timeoutSec", "timeout", "matcher", "url", "headers", "allowedEnvVars"}
HK_EVENTS = {"sessionStart", "sessionEnd", "userPromptSubmitted", "userPromptTransformed", "preToolUse", "postToolUse", "postToolUseFailure", "preMcpToolCall", "permissionRequest", "preCompact", "errorOccurred", "agentStop", "subagentStart", "subagentStop", "notification", "postResult"}
HK_PASCAL_ALIASES = {"SessionStart", "SessionEnd", "UserPromptSubmit", "UserPromptSubmitted", "UserPromptTransformed", "PreToolUse", "PostToolUse", "PostToolUseFailure", "PreMcpToolCall", "PermissionRequest", "PreCompact", "ErrorOccurred", "Stop", "AgentStop", "SubagentStart", "SubagentStop", "Notification", "PostResult"}
PLUGIN_MANIFESTS = (".plugin/plugin.json", "plugin.json", ".github/plugin/plugin.json", ".claude-plugin/plugin.json")
AUTHORING_ONLY_SECTIONS = {"Template Setup", "Section map", "Optional frontmatter"}
AG_REQUIRED_SECTIONS = (
    "Mission",
    "Activation and Scope",
    "Operating Principles",
    "What This Agent Knows",
    "What This Agent Does NOT Know",
    "Output Format",
    "Definition of Done",
    "Anti-Patterns This Agent Rejects",
)
IN_REQUIRED_SECTIONS = ("Conventions", "Do / Do Not", "Checklist Before Opening a PR")
SK_REQUIRED_SECTIONS = ("When to invoke", "Output template", "Quality gate")
PR_REQUIRED_SECTIONS = (
    "Objective",
    "When to Invoke",
    "Preconditions",
    "Inputs the Team Must Provide",
    "What I Will Do",
    "What I Will NOT Do",
    "Output Format",
    "Definition of Done",
    "Prompt Body",
    "Invocation Example",
)


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / ".git").exists() or (candidate / "README.md").exists():
            return candidate
    return start.resolve()


def default_library_root() -> Path:
    repo_root = find_repo_root(Path(__file__).resolve())
    library_root = repo_root / "library"
    return library_root if library_root.is_dir() else Path(__file__).resolve().parents[1]

@dataclass
class Finding:
    kind: str
    file: str
    rule_id: str
    severity: str
    message: str

class Validator:
    def __init__(self, root: Path, quiet: bool = False):
        self.root = root.resolve()
        self.quiet = quiet
        self.findings: list[Finding] = []
        self.file_counts: Counter[str] = Counter()

    def rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except Exception:
            return path.as_posix()

    def add(self, kind: str, path: Path | str, rule_id: str, severity: str, message: str) -> None:
        f = self.rel(path) if isinstance(path, Path) else path
        self.findings.append(Finding(kind, f, rule_id, severity, message))

    def catch_file(self, kind: str, path: Path, fn) -> None:
        try:
            fn()
        except Exception as exc:  # robust per-file fallback
            self.add(kind, path, f"{KIND_PREFIX[kind]}000", "ERROR", f"Unexpected validator failure: {exc}")

    def validate(self, kinds: Iterable[str]) -> None:
        for kind in kinds:
            getattr(self, f"validate_{kind}")()

    # Agents
    def validate_agents(self) -> None:
        kind = "agents"; d = self.root / "agents"
        files = sorted(d.glob("*.agent.md")) if d.is_dir() else []
        self.file_counts[kind] = len(files)
        seen: dict[str, Path] = {}
        for p in files:
            key = p.name[:-len(".agent.md")]
            if key in seen:
                self.add(kind, p, "AG014", "ERROR", f"Duplicate agent dedup key '{key}' also used by {self.rel(seen[key])}")
            else:
                seen[key] = p
            self.catch_file(kind, p, lambda p=p: self._validate_agent(p))

    def _validate_agent(self, p: Path) -> None:
        kind = "agents"
        if not AG_FILENAME_RE.match(p.name):
            self.add(kind, p, "AG001", "ERROR", "Filename must match ^[A-Za-z0-9._-]+\\.agent\\.md$")
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=True)
        if not present or err or not isinstance(fm, dict):
            self.add(kind, p, "AG002", "ERROR", f"Frontmatter missing or invalid{': ' + err if err else ''}")
            fm = {}
        desc = fm.get("description")
        if not isinstance(desc, str) or not desc.strip():
            self.add(kind, p, "AG003", "ERROR", "description must be a non-empty string")
        elif "\n" in desc or len(desc) > 500:
            self.add(kind, p, "AG004", "WARNING", "description should be a single line ≤ 500 chars")
        if not body.strip():
            self.add(kind, p, "AG005", "ERROR", "Body must be non-empty")
        if len(body) > 30000:
            self.add(kind, p, "AG006", "ERROR", "Body must be ≤ 30000 chars")
        target = fm.get("target")
        if target is not None and target not in {"vscode", "github-copilot"}:
            self.add(kind, p, "AG007", "ERROR", "target must be 'vscode' or 'github-copilot'")
        tools = fm.get("tools")
        tool_list: list[str] = []
        if tools is not None:
            if isinstance(tools, str):
                tool_list = [tools]
            elif isinstance(tools, list) and all(isinstance(x, str) for x in tools):
                tool_list = tools
            else:
                self.add(kind, p, "AG008", "ERROR", "tools must be a string or list of strings")
            if tool_list and all(is_vscode_only_tool(t) for t in tool_list):
                self.add(kind, p, "AG009", "WARNING", "tools contains only VS Code-only names; CLI effective tool set is empty")
            for t in tool_list:
                if t.lower() in NOOP_TOOLS:
                    self.add(
                        kind, p, "AG017", "ERROR",
                        f"Tool token '{t}' is a no-op in the Copilot CLI and grants nothing; "
                        f"use {' + '.join(NOOP_TOOLS[t.lower()]) or 'nothing (remove it)'}",
                    )
                elif not is_recognized_tool(t):
                    self.add(kind, p, "AG010", "INFO", f"Unrecognized tool name '{t}'")
        for k in sorted(AG_RETIRED_KEYS & set(fm)):
            self.add(kind, p, "AG011", "WARNING", f"Retired/invalid key present: {k}")
        model = fm.get("model")
        models: list[str] = []
        if model is not None:
            if isinstance(model, str):
                models = [model]
            elif isinstance(model, list) and all(isinstance(x, str) for x in model):
                models = model
            else:
                self.add(kind, p, "AG012", "ERROR", "model must be a string or list of strings")
            for m in models:
                if " " in m or LEGACY_MODEL_RE.match(m):
                    self.add(kind, p, "AG013", "WARNING", f"model '{m}' looks like a legacy VS Code display name")
        name = fm.get("name")
        if name is not None and (not isinstance(name, str) or not name.strip()):
            self.add(kind, p, "AG015", "WARNING", "name, if present, should be a non-empty string")
        for k in sorted(AG_VSCODE_KEYS & set(fm)):
            self.add(kind, p, "AG016", "INFO", f"{k} is VS Code-only and ignored by CLI")
        self._check_body_conventions(kind, p, body, "AG018", "AG019", "AG020")
        self._check_required_sections(kind, p, body, "AG021", AG_REQUIRED_SECTIONS)

    # Instructions
    def validate_instructions(self) -> None:
        kind = "instructions"; d = self.root / "instructions"
        files = sorted(d.glob("*.instructions.md")) if d.is_dir() else []
        self.file_counts[kind] = len(files)
        for p in files:
            self.catch_file(kind, p, lambda p=p: self._validate_instruction(p))

    def _validate_instruction(self, p: Path) -> None:
        kind = "instructions"
        if not IN_FILENAME_RE.match(p.name):
            self.add(kind, p, "IN001", "ERROR", "Filename must match ^[A-Za-z0-9._-]+\\.instructions\\.md$")
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=False)
        if present and (err or not isinstance(fm, dict)):
            self.add(kind, p, "IN002", "ERROR", f"Frontmatter delimiters exist but YAML did not parse{': ' + err if err else ''}")
            fm = {}
        if not present:
            self.add(kind, p, "IN003", "WARNING", "Frontmatter is missing entirely")
            fm = {}
        if "applyTo" not in fm:
            self.add(kind, p, "IN004", "WARNING", "applyTo missing; file is never auto-applied")
        else:
            if not valid_apply_to(fm.get("applyTo")):
                self.add(kind, p, "IN005", "ERROR", "applyTo must be a non-empty string/list of balanced non-empty globs")
        exclude_agent = fm.get("excludeAgent")
        if exclude_agent is not None and (not isinstance(exclude_agent, str) or exclude_agent not in {"code-review", "cloud-agent"}):
            self.add(kind, p, "IN006", "ERROR", "excludeAgent must be 'code-review' or 'cloud-agent'")
        for k in sorted(set(fm) - IN_VALID_KEYS):
            self.add(kind, p, "IN007", "WARNING", f"Unrecognized frontmatter key: {k}")
        if "description" not in fm or not isinstance(fm.get("description"), str) or not fm.get("description", "").strip():
            self.add(kind, p, "IN008", "WARNING", "description missing")
        if not body.strip():
            self.add(kind, p, "IN009", "ERROR", "Body must be non-empty")
        self._check_body_conventions(kind, p, body, "IN010", "IN011", "IN012")
        self._check_required_sections(kind, p, body, "IN013", IN_REQUIRED_SECTIONS)

    # Skills
    def validate_skills(self) -> None:
        kind = "skills"; d = self.root / "skills"
        dirs = sorted([x for x in d.iterdir() if x.is_dir()]) if d.is_dir() else []
        self.file_counts[kind] = len(dirs)
        names: dict[str, Path] = {}
        for sd in dirs:
            p = sd / "SKILL.md"
            if not p.exists():
                self.add(kind, p, "SK010", "ERROR", "Every skill directory must contain SKILL.md")
                continue
            self.catch_file(kind, p, lambda p=p, names=names: self._validate_skill(p, names))

    def _validate_skill(self, p: Path, names: dict[str, Path]) -> None:
        kind = "skills"
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=True)
        if not present or err or not isinstance(fm, dict):
            self.add(kind, p, "SK001", "ERROR", f"Frontmatter missing or invalid{': ' + err if err else ''}")
            fm = {}
        name = fm.get("name")
        if not isinstance(name, str) or not (1 <= len(name) <= 64) or not SK_NAME_RE.match(name) or "--" in name:
            self.add(kind, p, "SK002", "ERROR", "name must be 1–64 chars, kebab-case, and not contain --")
        else:
            if name != p.parent.name:
                self.add(kind, p, "SK003", "ERROR", "name must equal parent directory name")
            if name in names:
                self.add(kind, p, "SK011", "ERROR", f"Duplicate skill name '{name}' also used by {self.rel(names[name])}")
            else:
                names[name] = p
        desc = fm.get("description")
        if not isinstance(desc, str) or not (1 <= len(desc) <= 1024):
            self.add(kind, p, "SK004", "ERROR", "description must be present and 1–1024 chars")
        elif not SK_WHEN_RE.search(desc):
            self.add(kind, p, "SK005", "WARNING", "description should express WHEN to use the skill")
        for k in sorted(set(fm) - SK_VALID_KEYS):
            self.add(kind, p, "SK006", "WARNING", f"Unrecognized top-level key: {k}")
        if not body.strip():
            self.add(kind, p, "SK007", "ERROR", "Body must be non-empty")
        if len(body.splitlines()) > 500:
            self.add(kind, p, "SK008", "WARNING", "Body > 500 lines; use progressive disclosure resources")
        for k in ("user-invocable", "disable-model-invocation"):
            if k in fm and not isinstance(fm[k], bool):
                self.add(kind, p, "SK009", "ERROR", f"{k} must be boolean")
        for link in relative_links(body):
            target = (p.parent / link).resolve()
            try:
                target.relative_to(p.parent.resolve())
            except ValueError:
                continue
            if not target.exists():
                self.add(kind, p, "SK012", "WARNING", f"Relative link points at missing bundled resource: {link}")
        self._check_body_conventions(kind, p, body, "SK013", "SK014", "SK015", bundle_root=p.parent.resolve())
        self._check_required_sections(kind, p, body, "SK016", SK_REQUIRED_SECTIONS)

    # VS Code prompts
    def validate_prompts(self) -> None:
        kind = "prompts"; d = self.root / "prompts"
        files = sorted(d.glob("*.prompt.md")) if d.is_dir() else []
        self.file_counts[kind] = len(files)
        names: dict[str, Path] = {}
        for p in files:
            self.catch_file(kind, p, lambda p=p, names=names: self._validate_prompt(p, names))

    def _validate_prompt(self, p: Path, names: dict[str, Path]) -> None:
        kind = "prompts"
        if not PR_FILENAME_RE.match(p.name):
            self.add(kind, p, "PR001", "ERROR", "Filename must be kebab-case and end with .prompt.md")
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=True)
        if not present or err or not isinstance(fm, dict):
            self.add(kind, p, "PR002", "ERROR", f"Frontmatter missing or invalid{': ' + err if err else ''}")
            fm = {}
        name = fm.get("name")
        expected_name = p.name[:-len(".prompt.md")]
        if not isinstance(name, str) or not SK_NAME_RE.match(name) or "--" in name:
            self.add(kind, p, "PR003", "ERROR", "name must be non-empty kebab-case")
        else:
            if name != expected_name:
                self.add(kind, p, "PR003", "ERROR", "name must match the filename")
            if name in names:
                self.add(kind, p, "PR003", "ERROR", f"Duplicate prompt name '{name}' also used by {self.rel(names[name])}")
            else:
                names[name] = p
        desc = fm.get("description")
        if not isinstance(desc, str) or not desc.strip():
            self.add(kind, p, "PR004", "ERROR", "description must be a non-empty string")
        for key in sorted(set(fm) - PR_VALID_KEYS):
            self.add(kind, p, "PR005", "WARNING", f"Unrecognized VS Code prompt frontmatter key: {key}")
        for key in ("argument-hint", "agent", "model"):
            if key in fm and (not isinstance(fm[key], str) or not fm[key].strip()):
                self.add(kind, p, "PR005", "ERROR", f"{key} must be a non-empty string when present")
        tools = fm.get("tools")
        if tools is not None and not (
            isinstance(tools, str)
            or (isinstance(tools, list) and all(isinstance(tool, str) and tool for tool in tools))
        ):
            self.add(kind, p, "PR005", "ERROR", "tools must be a string or a list of non-empty strings")
        if not body.strip():
            self.add(kind, p, "PR006", "ERROR", "Body must be non-empty")
        elif not body_starts_with_h1(body):
            self.add(kind, p, "PR006", "ERROR", "Body must open with a single H1 naming the prompt")
        self._check_required_sections(kind, p, body, "PR007", PR_REQUIRED_SECTIONS)
        if TEMPLATE_PLACEHOLDER_RE.search(body):
            self.add(kind, p, "PR008", "ERROR", "Unresolved uppercase double-brace template placeholder")

    # Shared body conventions (docs/templates/) — advisory only.
    def _check_body_conventions(self, kind: str, p: Path, body: str, link_rule: str,
                                prompt_rule: str, h1_rule: str, bundle_root: Path | None = None) -> None:
        """Report body-structure and cross-reference drift from docs/templates/.

        The CLI never validates a primitive body, so every finding here is INFO.
        """
        if PROMPT_FILE_RE.search(strip_code_fences(body)):
            self.add(kind, p, prompt_rule, "INFO",
                     "References a *.prompt.md file; prompt files are VS Code-only and are not "
                     "discovered by the Copilot CLI. Reference a skill by name instead")
        for link in relative_links(body):
            if bundle_root is not None:
                try:
                    (p.parent / link).resolve().relative_to(bundle_root)
                    continue
                except ValueError:
                    pass
            self.add(kind, p, link_rule, "INFO",
                     f"Relative link '{link}' does not survive installation into .github/ or "
                     "~/.copilot/; reference the primitive by name and type instead")
        if body.strip() and not body_starts_with_h1(body):
            self.add(kind, p, h1_rule, "INFO", "Body should open with a single H1 naming the primitive")

    def _check_required_sections(
        self,
        kind: str,
        p: Path,
        body: str,
        rule_id: str,
        required: tuple[str, ...],
    ) -> None:
        """Enforce the repository body contracts encoded by docs/templates/."""
        headings = h2_headings(body)
        issues: list[str] = []
        missing = [heading for heading in required if heading not in headings]
        duplicates = [heading for heading in required if headings.count(heading) > 1]
        if missing:
            issues.append(f"missing required sections: {', '.join(missing)}")
        if duplicates:
            issues.append(f"duplicate required sections: {', '.join(duplicates)}")
        if not missing and not duplicates:
            positions = [headings.index(heading) for heading in required]
            if positions != sorted(positions):
                issues.append("required sections are out of template order")
        authoring_only = sorted(AUTHORING_ONLY_SECTIONS.intersection(headings))
        if authoring_only:
            issues.append(f"authoring-only sections remain: {', '.join(authoring_only)}")
        if issues:
            self.add(kind, p, rule_id, "ERROR", "; ".join(issues))

    # Plugins
    def validate_plugins(self) -> None:
        kind = "plugins"; d = self.root / "plugins"
        dirs = sorted([x for x in d.iterdir() if x.is_dir()]) if d.is_dir() else []
        self.file_counts[kind] = len(dirs)
        for pd in dirs:
            manifest = None
            for rel in PLUGIN_MANIFESTS:
                q = pd / rel
                if q.exists():
                    manifest = q; break
            if manifest is None:
                self.add(kind, pd, "PL001", "ERROR", "No plugin manifest found in supported locations")
                continue
            self.catch_file(kind, manifest, lambda manifest=manifest, pd=pd: self._validate_plugin(manifest, pd))

    def _validate_plugin(self, p: Path, plugin_dir: Path) -> None:
        kind = "plugins"
        try:
            data = json.loads(read_text(p))
            if not isinstance(data, dict):
                raise ValueError("manifest root must be an object")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            self.add(kind, p, "PL002", "ERROR", f"Invalid JSON: {exc}")
            return
        name = data.get("name")
        if not isinstance(name, str) or len(name) > 64 or not PL_NAME_RE.match(name):
            self.add(kind, p, "PL003", "ERROR", "name must be kebab-case/dot-case, ≤ 64 chars")
        elif name != plugin_dir.name:
            self.add(kind, p, "PL004", "WARNING", "name differs from plugin directory name")
        version = data.get("version")
        if not isinstance(version, str) or not SEMVER_RE.match(version):
            self.add(kind, p, "PL005", "WARNING", "version missing or not semver")
        desc = data.get("description")
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
            self.add(kind, p, "PL006", "WARNING", "description missing or > 1024 chars")
        open_plugin = data.get("$schema") == OPEN_PLUGIN_SCHEMA
        valid_keys = OPEN_PLUGIN_VALID_KEYS if open_plugin else PL_VALID_KEYS
        for k in sorted(set(data) - valid_keys):
            severity = "ERROR" if open_plugin else "WARNING"
            self.add(kind, p, "PL007", severity, f"Unrecognized top-level key: {k}")
        for label, ref in collect_plugin_refs(data):
            if not isinstance(ref, str) or not ref.strip() or has_variable(ref):
                continue
            resolved, base = resolve_component_ref(ref, p.parent, self.root)
            if resolved is None:
                self.add(kind, p, "PL008", "ERROR", f"{label} path '{ref}' did not resolve relative to manifest dir or repo root")
            # Resolution base is intentionally not emitted on success to avoid noisy INFO; errors include both attempted bases.
            if label.endswith("skills") and not ref.endswith("/"):
                self.add(kind, p, "PL009", "WARNING", f"skill ref should end with '/': {ref}")
            if label.endswith("agents") and not ref.endswith(".agent.md"):
                self.add(kind, p, "PL009", "WARNING", f"agent ref should end with '.agent.md': {ref}")
        author = data.get("author")
        if author is not None and not (isinstance(author, dict) and isinstance(author.get("name"), str) and author.get("name", "").strip()):
            self.add(kind, p, "PL010", "WARNING", "author, if present, should be an object with a name")
        if open_plugin:
            self._validate_open_plugin(p, plugin_dir, data)

    def _validate_open_plugin(self, p: Path, plugin_dir: Path, data: dict[str, Any]) -> None:
        kind = "plugins"
        extensions = data.get("extensions", {})
        if not isinstance(extensions, dict):
            self.add(kind, p, "PL011", "ERROR", "Open Plugin Spec extensions must be an object")
            return
        invalid_extensions = [
            namespace
            for namespace, config in extensions.items()
            if not isinstance(namespace, str) or not isinstance(config, dict)
        ]
        if invalid_extensions:
            self.add(
                kind,
                p,
                "PL011",
                "ERROR",
                "Open Plugin Spec extension namespaces must map to objects",
            )

        copilot_extension = extensions.get("com.github.copilot")
        if copilot_extension is not None:
            agents = copilot_extension.get("agents")
            if agents is not None and not (
                isinstance(agents, list)
                and all(isinstance(ref, str) and ref.endswith(".agent.md") for ref in agents)
            ):
                self.add(
                    kind,
                    p,
                    "PL012",
                    "ERROR",
                    "extensions.com.github.copilot.agents must be a list of .agent.md paths",
                )
            extension_agents = plugin_dir / "com.github.copilot" / "agents"
            if not extension_agents.is_dir() or not any(extension_agents.glob("*.agent.md")):
                self.add(
                    kind,
                    p,
                    "PL012",
                    "ERROR",
                    "Agent Plugins 1.0 GitHub agents must be mirrored under com.github.copilot/agents",
                )

        mcp_path = plugin_dir / "mcp.json"
        if mcp_path.exists():
            self._validate_open_plugin_mcp(mcp_path)

    def _validate_open_plugin_mcp(self, p: Path) -> None:
        kind = "plugins"
        try:
            data = json.loads(read_text(p))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.add(kind, p, "PL013", "ERROR", f"Invalid Open Plugin MCP JSON: {exc}")
            return
        if not isinstance(data, dict):
            self.add(kind, p, "PL013", "ERROR", "Open Plugin MCP root must be an object")
            return
        if data.get("$schema") != OPEN_MCP_SCHEMA:
            self.add(kind, p, "PL013", "ERROR", f"mcp.json must declare $schema {OPEN_MCP_SCHEMA}")
        extra_keys = sorted(set(data) - {"$schema", "mcpServers"})
        if extra_keys:
            self.add(kind, p, "PL013", "ERROR", f"Unsupported mcp.json keys: {', '.join(extra_keys)}")
        servers = data.get("mcpServers")
        if not isinstance(servers, dict):
            self.add(kind, p, "PL013", "ERROR", "mcp.json mcpServers must be an object")
            return
        for name, config in servers.items():
            if not isinstance(name, str) or not name or not isinstance(config, dict):
                self.add(kind, p, "PL014", "ERROR", "MCP servers require non-empty names and object configs")
                continue
            server_type = config.get("type")
            if server_type == "stdio":
                allowed = {"type", "command", "args", "env", "cwd"}
                if not isinstance(config.get("command"), str) or not config["command"]:
                    self.add(kind, p, "PL014", "ERROR", f"MCP server '{name}' requires a command")
                args = config.get("args")
                if args is not None and not (
                    isinstance(args, list) and all(isinstance(arg, str) for arg in args)
                ):
                    self.add(kind, p, "PL014", "ERROR", f"MCP server '{name}' args must be strings")
                env = config.get("env")
                if env is not None and not (
                    isinstance(env, dict)
                    and all(
                        isinstance(key, str)
                        and key not in {"PLUGIN_ROOT", "PLUGIN_DATA"}
                        and isinstance(value, str)
                        for key, value in env.items()
                    )
                ):
                    self.add(kind, p, "PL014", "ERROR", f"MCP server '{name}' env is invalid")
            elif server_type in {"streamable-http", "sse"}:
                allowed = {"type", "url", "headers"}
                if not isinstance(config.get("url"), str) or not config["url"]:
                    self.add(kind, p, "PL014", "ERROR", f"MCP server '{name}' requires a URL")
                headers = config.get("headers")
                if headers is not None and not (
                    isinstance(headers, dict)
                    and all(isinstance(key, str) and isinstance(value, str) for key, value in headers.items())
                ):
                    self.add(kind, p, "PL014", "ERROR", f"MCP server '{name}' headers are invalid")
            else:
                self.add(
                    kind,
                    p,
                    "PL014",
                    "ERROR",
                    f"MCP server '{name}' type must be stdio, streamable-http, or sse",
                )
                continue
            extra_server_keys = sorted(set(config) - allowed)
            if extra_server_keys:
                self.add(
                    kind,
                    p,
                    "PL014",
                    "ERROR",
                    f"MCP server '{name}' has unsupported keys: {', '.join(extra_server_keys)}",
                )

    # Hooks
    def validate_hooks(self) -> None:
        kind = "hooks"; d = self.root / "hooks"
        files: list[tuple[Path, Path]] = [(p, self.root) for p in sorted(d.glob("*/hooks.json"))] if d.is_dir() else []
        repo_root = find_repo_root(self.root)
        installed = repo_root / ".github" / "hooks"
        if installed.is_dir() and installed.resolve() != d.resolve():
            files += [(p, repo_root) for p in sorted(installed.glob("*.json"))]
        self.file_counts[kind] = len(files)
        for p, base in files:
            self.catch_file(kind, p, lambda p=p, base=base: self._validate_hook(p, base))

    def _validate_hook(self, p: Path, base: Path | None = None) -> None:
        kind = "hooks"
        base = base or self.root
        try:
            data = json.loads(read_text(p))
            if not isinstance(data, dict):
                raise ValueError("hooks root must be an object")
        except Exception as exc:
            self.add(kind, p, "HK001", "ERROR", f"Invalid JSON: {exc}")
            return
        if data.get("version") != 1:
            self.add(kind, p, "HK002", "ERROR", "version must equal 1")
        hooks = data.get("hooks")
        if not isinstance(hooks, dict):
            self.add(kind, p, "HK003", "ERROR", "hooks must be an object")
            return
        for event, entries in hooks.items():
            if event not in HK_EVENTS:
                if event in HK_PASCAL_ALIASES:
                    self.add(kind, p, "HK005", "WARNING", f"Use native camelCase event name instead of PascalCase alias '{event}'")
                else:
                    self.add(kind, p, "HK004", "ERROR", f"Unknown hook event name: {event}")
            if not isinstance(entries, list):
                self.add(kind, p, "HK006", "ERROR", f"Entries for {event} must be a list")
                continue
            for idx, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    self.add(kind, p, "HK006", "ERROR", f"Hook entry {event}[{idx}] must be an object")
                    continue
                loc = f"{event}[{idx}]"
                etype = entry.get("type")
                if etype is not None and etype not in {"command", "http"}:
                    self.add(kind, p, "HK011", "WARNING", f"{loc} type should be 'command' or 'http'")
                has_runner = any(entry.get(k) for k in ("bash", "powershell", "command")) or (entry.get("type") == "http" and entry.get("url"))
                if not has_runner:
                    self.add(kind, p, "HK006", "ERROR", f"{loc} must define bash, powershell, command, or http url")
                for k in sorted(set(entry) - HK_VALID_KEYS):
                    self.add(kind, p, "HK007", "WARNING", f"{loc} has unrecognized key: {k}")
                timeout = entry.get("timeoutSec")
                if not isinstance(timeout, int) or timeout <= 0:
                    self.add(kind, p, "HK010", "WARNING", f"{loc} timeoutSec missing or not a positive integer")
                for k in ("bash", "powershell", "command"):
                    cmd = entry.get(k)
                    for script in referenced_scripts(cmd):
                        resolved = resolve_script(script, p.parent, base)
                        if resolved is None:
                            self.add(kind, p, "HK008", "ERROR", f"{loc} {k} script '{script}' does not exist relative to repo root or hook dir")
                        elif not os.access(resolved, os.X_OK):
                            self.add(kind, p, "HK009", "ERROR", f"{loc} {k} script '{script}' is not executable")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str, required: bool) -> tuple[dict[str, Any], str, bool, str | None]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text, False, None if not required else "opening --- not found"
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i; break
    if end_idx is None:
        return {}, "", True, "closing --- not found"
    raw = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1:])
    try:
        if yaml is not None:
            data = yaml.safe_load(raw) or {}
        else:
            data = fallback_yaml_parse(raw)
        if not isinstance(data, dict):
            return {}, body, True, "frontmatter is not a map"
        return data, body, True, None
    except Exception as exc:
        return {}, body, True, str(exc)


def fallback_yaml_parse(raw: str) -> dict[str, Any]:
    src = raw.splitlines()
    root: dict[str, Any] = {}
    i = 0
    while i < len(src):
        line = src[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1; continue
        indent = len(line) - len(line.lstrip(" "))
        if indent != 0:
            i += 1; continue
        if ":" not in line:
            raise ValueError(f"cannot parse line: {line}")
        key, val = line.split(":", 1)
        key = key.strip(); val = val.strip()
        if not key:
            raise ValueError("empty key")
        if val in {"|", ">", "|-", ">-"}:
            style = val[0]; chomp_strip = val.endswith("-")
            block: list[str] = []; i += 1
            while i < len(src):
                nxt = src[i]
                nindent = len(nxt) - len(nxt.lstrip(" "))
                if nxt.strip() and nindent <= indent:
                    break
                block.append(nxt[indent + 2:] if len(nxt) >= indent + 2 else "")
                i += 1
            text = "\n".join(block)
            if style == ">":
                text = " ".join(x.strip() for x in block)
            if not chomp_strip:
                text += "\n"
            root[key] = text
            continue
        if val == "":
            # one-level nested map or block sequence
            items: list[Any] | None = None
            mp: dict[str, Any] = {}
            i += 1
            while i < len(src):
                nxt = src[i]
                if not nxt.strip() or nxt.lstrip().startswith("#"):
                    i += 1; continue
                nindent = len(nxt) - len(nxt.lstrip(" "))
                if nindent <= indent:
                    break
                stripped = nxt.strip()
                if stripped.startswith("- "):
                    if items is None: items = []
                    items.append(parse_scalar(stripped[2:].strip()))
                elif ":" in stripped:
                    nk, nv = stripped.split(":", 1)
                    mp[nk.strip()] = parse_scalar(nv.strip()) if nv.strip() else {}
                else:
                    raise ValueError(f"cannot parse nested line: {nxt}")
                i += 1
            root[key] = items if items is not None else mp
            continue
        root[key] = parse_scalar(val)
        i += 1
    return root


def parse_scalar(val: str) -> Any:
    if val == "": return ""
    if val in {"true", "True"}: return True
    if val in {"false", "False"}: return False
    if val in {"null", "Null", "~"}: return None
    if val.startswith("[") and val.endswith("]"):
        try:
            return ast.literal_eval(val)
        except Exception:
            inner = val[1:-1].strip()
            return [] if not inner else [parse_scalar(x.strip()) for x in inner.split(",")]
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        try:
            return ast.literal_eval(val)
        except Exception:
            return val[1:-1]
    if re.fullmatch(r"-?\d+", val):
        try: return int(val)
        except Exception: pass
    return val.split(" #", 1)[0].strip()


def is_vscode_only_tool(tool: str) -> bool:
    parts = [tool, tool.split("/")[-1]]
    return any(p.lower() in VSCODE_ONLY for p in parts)


def is_recognized_tool(tool: str) -> bool:
    low = tool.lower()
    if low == "*" or low in PORTABLE_TOOLS or low in NATIVE_TOOLS:
        return True
    if MCP_TOOL_RE.match(tool):
        return True
    return is_vscode_only_tool(tool)


def valid_apply_to(value: Any) -> bool:
    vals = value if isinstance(value, list) else [value]
    if not vals or not all(isinstance(v, str) for v in vals):
        return False
    globs: list[str] = []
    for v in vals:
        globs.extend(split_globs(v))
    return bool(globs) and all(g.strip() and balanced(g.strip()) for g in globs)



def split_globs(s: str) -> list[str]:
    parts: list[str] = []
    start = 0
    bdepth = cdepth = 0
    for i, ch in enumerate(s):
        if ch == "[":
            bdepth += 1
        elif ch == "]" and bdepth > 0:
            bdepth -= 1
        elif ch == "{":
            cdepth += 1
        elif ch == "}" and cdepth > 0:
            cdepth -= 1
        elif ch == "," and bdepth == 0 and cdepth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    return parts

def balanced(s: str) -> bool:
    pairs = [("[", "]"), ("{", "}")]
    for open_c, close_c in pairs:
        depth = 0
        for ch in s:
            if ch == open_c: depth += 1
            elif ch == close_c:
                depth -= 1
                if depth < 0: return False
        if depth != 0: return False
    return True


def strip_code_fences(body: str) -> str:
    """Remove fenced code blocks so illustrative links inside examples are not linted."""
    out, fence = [], None
    for line in body.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)[0]
            if fence is None:
                fence = token
                continue
            if token == fence:
                fence = None
                continue
        if fence is None:
            out.append(line)
    return "\n".join(out)


def h2_headings(body: str) -> list[str]:
    """Return level-two headings outside fenced examples in document order."""
    return [
        line[3:].strip()
        for line in strip_code_fences(body).splitlines()
        if line.startswith("## ")
    ]


def is_placeholder_link(target: str) -> bool:
    """Template/illustrative link targets that are not meant to resolve on disk."""
    if re.search(r"[{}<>$*]|\.\.\.|\$\{", target):
        return True
    if re.match(r"^(?:\./)?path/to/", target, re.I):
        return True
    if "/" not in target and "." not in target:
        return True
    return target.lower() in {"relative-url", "relative-path", "url", "link", "page", "target"}


def body_starts_with_h1(body: str) -> bool:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        return stripped.startswith("# ")
    return False


def relative_links(body: str) -> Iterable[str]:
    for m in LINK_RE.finditer(strip_code_fences(body)):
        target = m.group(1).split("#", 1)[0].strip()
        if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        if is_placeholder_link(target):
            continue
        yield target.replace("%20", " ")


def has_variable(ref: str) -> bool:
    return "${" in ref or ref.startswith("~")


def collect_plugin_refs(data: dict[str, Any]) -> Iterable[tuple[str, str]]:
    def strings(label: str, val: Any):
        if isinstance(val, str):
            yield label, val
        elif isinstance(val, list):
            for x in val:
                if isinstance(x, str):
                    yield label, x
                elif isinstance(x, dict):
                    for k in ("path", "source"):
                        if isinstance(x.get(k), str): yield label, x[k]
        elif isinstance(val, dict):
            for k in ("path", "source"):
                if isinstance(val.get(k), str): yield label, val[k]
            # mcpServers may be name -> path/config
            for v in val.values():
                if isinstance(v, str): yield label, v
                elif isinstance(v, dict):
                    for k in ("path", "source"):
                        if isinstance(v.get(k), str): yield label, v[k]
    for key in ("agents", "skills", "commands", "hooks", "mcpServers"):
        yield from strings(key, data.get(key))
    ext = data.get("extensions")
    if isinstance(ext, dict):
        for ns, cfg in ext.items():
            if isinstance(cfg, dict):
                for key in ("agents", "skills", "commands", "hooks", "mcpServers"):
                    yield from strings(f"extensions.{ns}.{key}", cfg.get(key))


def resolve_component_ref(ref: str, manifest_dir: Path, root: Path) -> tuple[Path | None, str | None]:
    cleaned = ref.split("#", 1)[0]
    for base_name, base in (("manifest", manifest_dir), ("root", root)):
        candidate = (base / cleaned).resolve() if not Path(cleaned).is_absolute() else Path(cleaned)
        if candidate.exists():
            return candidate, base_name
    return None, None


def referenced_scripts(cmd: Any) -> Iterable[str]:
    if not isinstance(cmd, str) or not cmd.strip():
        return []
    try:
        parts = shlex.split(cmd)
    except Exception:
        parts = cmd.split()
    refs = []
    for part in parts:
        if part.startswith("-"):
            continue
        if part.startswith(("./", "../", "/")) or "/" in part:
            refs.append(part); break
    return refs


def resolve_script(script: str, hook_dir: Path, root: Path) -> Path | None:
    s = Path(script)
    candidates = [s] if s.is_absolute() else [root / script, hook_dir / script]
    for c in candidates:
        if c.exists() and c.is_file():
            return c.resolve()
    return None


def report_json(v: Validator) -> dict[str, Any]:
    summary = []
    for kind in ALL_KINDS:
        fs = [f for f in v.findings if f.kind == kind]
        summary.append({"kind": kind, "files": v.file_counts.get(kind, 0), "errors": sum(f.severity == "ERROR" for f in fs), "warnings": sum(f.severity == "WARNING" for f in fs)})
    return {"summary": summary, "findings": [asdict(f) for f in v.findings]}


def print_human(v: Validator) -> None:
    order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    for kind in ALL_KINDS:
        fs = [f for f in v.findings if f.kind == kind and (not v.quiet or f.severity == "ERROR")]
        if not fs and v.quiet:
            continue
        print(f"\n## {kind} ({v.file_counts.get(kind, 0)} files)")
        grouped: dict[str, list[Finding]] = defaultdict(list)
        for f in sorted(fs, key=lambda x: (x.rule_id, order.get(x.severity, 9), x.file)):
            grouped[f.rule_id].append(f)
        for rule, items in grouped.items():
            counts = Counter(i.severity for i in items)
            count_s = ", ".join(f"{sev}={counts[sev]}" for sev in ("ERROR", "WARNING", "INFO") if counts[sev])
            print(f"  {rule} ({count_s})")
            for f in items:
                print(f"    [{f.severity}] {f.file}: {f.message}")
    print_summary(v)


def print_summary(v: Validator) -> None:
    print("\nSUMMARY")
    print("kind | files | errors | warnings")
    print("--- | ---: | ---: | ---:")
    for kind in ALL_KINDS:
        fs = [f for f in v.findings if f.kind == kind]
        print(f"{kind} | {v.file_counts.get(kind, 0)} | {sum(f.severity == 'ERROR' for f in fs)} | {sum(f.severity == 'WARNING' for f in fs)}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate Copilot primitive files against the canonical harness spec.")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings as well as errors")
    ap.add_argument("--json", action="store_true", dest="json_out", help="emit machine-readable JSON report to stdout")
    ap.add_argument("--kind", action="append", choices=ALL_KINDS, help="validate only this kind; repeatable")
    ap.add_argument("--root", type=Path, default=default_library_root(), help="primitive library root (default: <repo>/library)")
    ap.add_argument("--quiet", action="store_true", help="human output: only summary and errors")
    args = ap.parse_args(argv)

    v = Validator(args.root, quiet=args.quiet)
    kinds = args.kind or list(ALL_KINDS)
    v.validate(kinds)
    if args.json_out:
        print(json.dumps(report_json(v), indent=2, sort_keys=True))
    else:
        print_human(v)
    errors = any(f.severity == "ERROR" for f in v.findings)
    warnings = any(f.severity == "WARNING" for f in v.findings)
    return 1 if errors or (args.strict and warnings) else 0

if __name__ == "__main__":
    raise SystemExit(main())

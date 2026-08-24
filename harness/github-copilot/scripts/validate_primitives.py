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
    from _layout import HARNESS_ROOT, find_repo_root
    from _plugin_sources import load_plugin_sources
except ModuleNotFoundError:  # pragma: no cover - supports python3 -m invocation
    from ._layout import HARNESS_ROOT, find_repo_root
    from ._plugin_sources import load_plugin_sources

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

IDENTIFIER_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*"
AG_FILENAME_RE = re.compile(rf"^{IDENTIFIER_PATTERN}\.agent\.md$")
IN_FILENAME_RE = re.compile(rf"^{IDENTIFIER_PATTERN}\.instructions\.md$")
PR_FILENAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.prompt\.md$")
SK_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
PL_NAME_RE = re.compile(rf"^{IDENTIFIER_PATTERN}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+].*)?$")
DATE_RE = re.compile(r"^20\d{2}-\d{2}-\d{2}$")
MCP_TOOL_RE = re.compile(
    r"^([a-zA-Z0-9_.-]+/(?:\*|[a-zA-Z0-9_.-]+))(?::(.+))?$")
LEGACY_MODEL_RE = re.compile(r"^(GPT|Claude|Gemini|o[0-9])")
SK_WHEN_RE = re.compile(
    r"use when|use this skill when|when you|when the user|for when|invoke when|trigger", re.I)
LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
PROMPT_FILE_RE = re.compile(r"[\w./-]*\.prompt\.md\b")
TEMPLATE_PLACEHOLDER_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
TOOL_TOKEN_CHARS = r"[A-Za-z0-9_./*-]+"
BODY_TOOL_LIST_RE = re.compile(r"\[[^\[\]\n]*\]")
BODY_QUOTED_TOKEN_RE = re.compile(rf"['\"]({TOOL_TOKEN_CHARS})['\"]")
BODY_BACKTICK_RUN_RE = re.compile(
    rf"(?:`{TOOL_TOKEN_CHARS}`(?:\s*(?:,|/)\s*(?:and\s+)?|\s+and\s+)){{2,}}`{TOOL_TOKEN_CHARS}`"
)
BODY_BACKTICK_TOKEN_RE = re.compile(rf"`({TOOL_TOKEN_CHARS})`")
# Lines that name a token in order to reject, hedge, or historicize it are the correct
# pattern, not a defect, so they must not be flagged.
BODY_TOOL_HEDGE_RE = re.compile(
    r"\b(?:avoid|reject|rejected|no-op|do not|don't|never|unavailable|unrecognized"
    r"|legacy|historical|intent label|not guaranteed|deprecated)\b",
    re.IGNORECASE,
)

PORTABLE_TOOLS = {
    "execute", "shell", "bash", "powershell",
    "read", "view", "notebookread",
    "edit", "write", "create", "multiedit", "notebookedit",
    "search", "grep", "glob",
    "agent", "task", "custom-agent",
    "web", "web_fetch", "web_search", "websearch", "webfetch",
    "todo", "todowrite", "update_todo",
}
NATIVE_TOOLS = {"grep", "glob", "view", "bash", "read_bash",
                "stop_bash", "powershell", "read_powershell", "stop_powershell", "lsp"}
VSCODE_ONLY = {
    "codebase", "editfiles", "vscodeapi", "opensimplebrowser", "findtestfiles", "githubrepo",
    "terminallastcommand", "terminalselection", "testfailure", "problems", "usages", "changes",
    "runcommands", "runtasks", "runtests", "searchresults", "extensions", "new", "fetch",
}
AG_RETIRED_KEYS = {"infer", "mode", "hidden", "agent", "title"}
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
AG_VSCODE_KEYS = {"argument-hint", "handoffs", "agents"}
IN_VALID_KEYS = {"applyTo", "name", "description", "excludeAgent"}
SK_VALID_KEYS = {"name", "description", "user-invocable", "disable-model-invocation",
                 "allowed-tools", "argument-hint", "license", "metadata", "tags"}
PR_VALID_KEYS = {"name", "description",
                 "argument-hint", "agent", "model", "tools"}
VSCODE_PROMPT_TOOL_ALIASES = {
    "read",
    "search",
    "edit",
    "execute",
    "web",
    "agent",
    "todo",
}
VSCODE_PROMPT_TOOL_SETS = {"playwright"}
LEGACY_PROMPT_TOOLS = {
    "changes",
    "codebase",
    "editfiles",
    "extensions",
    "fetch",
    "findtestfiles",
    "get_terminal_output",
    "githubrepo",
    "microsoft docs",
    "microsoft.docs.mcp",
    "new",
    "opensimplebrowser",
    "problems",
    "run_in_terminal",
    "runcommands",
    "runinterminal2",
    "runnotebooks",
    "runtasks",
    "runtests",
    "searchresults",
    "terminalcommand",
    "terminallastcommand",
    "terminalselection",
    "testfailure",
    "usages",
    "vscodeapi",
}
# MCP server identifiers that stay legitimate prose references inside an agent body
# even though they are legacy VS Code *prompt* tool IDs.
BODY_TOOL_ALLOWED = {"microsoft docs", "microsoft.docs.mcp"}
BODY_TOOL_VOCABULARY = (
    set(NOOP_TOOLS) | LEGACY_PROMPT_TOOLS) - BODY_TOOL_ALLOWED
PL_VALID_KEYS = {"$schema", "name", "version", "description", "author", "email", "repository", "license", "homepage", "keywords", "extensions",
                 "paths", "exclusive", "skills", "agents", "commands", "mcpServers", "lspServers", "outputStyles", "hooks", "postInstallMessage", "strict"}
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
HK_VALID_KEYS = {"type", "bash", "powershell", "command", "cwd", "env",
                 "timeoutSec", "timeout", "matcher", "url", "headers", "allowedEnvVars"}
HK_EVENTS = {"sessionStart", "sessionEnd", "userPromptSubmitted", "userPromptTransformed", "preToolUse", "postToolUse", "postToolUseFailure",
             "preMcpToolCall", "permissionRequest", "preCompact", "errorOccurred", "agentStop", "subagentStart", "subagentStop", "notification", "postResult"}
HK_PASCAL_ALIASES = {"SessionStart", "SessionEnd", "UserPromptSubmit", "UserPromptSubmitted", "UserPromptTransformed", "PreToolUse", "PostToolUse", "PostToolUseFailure",
                     "PreMcpToolCall", "PermissionRequest", "PreCompact", "ErrorOccurred", "Stop", "AgentStop", "SubagentStart", "SubagentStop", "Notification", "PostResult"}
PLUGIN_MANIFESTS = (".plugin/plugin.json", "plugin.json",
                    ".github/plugin/plugin.json", ".claude-plugin/plugin.json")
AUTHORING_ONLY_SECTIONS = {"Template Setup",
                           "Section map", "Optional frontmatter"}
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
IN_REQUIRED_SECTIONS = ("Conventions", "Do / Do Not",
                        "Checklist Before Opening a PR")
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


def default_harness_root() -> Path:
    return HARNESS_ROOT


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
        self.plugin_sources = load_plugin_sources()

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
            self.add(kind, path, f"{KIND_PREFIX[kind]}000",
                     "ERROR", f"Unexpected validator failure: {exc}")

    def validate(self, kinds: Iterable[str]) -> None:
        for kind in kinds:
            getattr(self, f"validate_{kind}")()

    # Agents
    def plugin_owned_files(self, folder: str, pattern: str,
                           generated_key: str | None = None) -> list[Path]:
        """Components a plugin owns outright.

        Copies generated from the flat tree are already validated at their canonical
        source, so validating them here would double-report the same findings.
        """
        paths: list[Path] = []
        for name, config in sorted(self.plugin_sources.items()):
            if config.get("componentSource") != "plugin":
                continue
            base = self.root / "plugins" / name / folder
            if not base.is_dir():
                continue
            generated = {
                ref.strip("./").rstrip("/").rsplit("/", 1)[-1]
                for ref in (config.get(generated_key) or [])
            } if generated_key else set()
            for path in sorted(base.glob(pattern)):
                label = path.parent.name if path.name == "SKILL.md" else path.name
                if label in generated:
                    continue
                paths.append(path)
        return paths

    def validate_agents(self) -> None:
        kind = "agents"
        d = self.root / "agents"
        files = sorted(d.glob("*.agent.md")) if d.is_dir() else []
        seen: dict[str, Path] = {}
        for p in files:
            key = p.name[:-len(".agent.md")]
            if key in seen:
                self.add(kind, p, "AG014", "ERROR",
                         f"Duplicate agent dedup key '{key}' also used by {self.rel(seen[key])}")
            else:
                seen[key] = p
            self.catch_file(kind, p, lambda p=p: self._validate_agent(p))
        plugin_files = self.plugin_owned_files("agents", "*.agent.md")
        for p in plugin_files:
            self.catch_file(kind, p, lambda p=p: self._validate_agent(p))
        self.file_counts[kind] = len(files) + len(plugin_files)

    def _validate_agent(self, p: Path) -> None:
        kind = "agents"
        if not AG_FILENAME_RE.match(p.name):
            self.add(
                kind,
                p,
                "AG001",
                "ERROR",
                "Filename must be kebab-case and end with .agent.md",
            )
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=True)
        if not present or err or not isinstance(fm, dict):
            self.add(kind, p, "AG002", "ERROR",
                     f"Frontmatter missing or invalid{': ' + err if err else ''}")
            fm = {}
        desc = fm.get("description")
        if not isinstance(desc, str) or not desc.strip():
            self.add(kind, p, "AG003", "ERROR",
                     "description must be a non-empty string")
        elif "\n" in desc or len(desc) > 500:
            self.add(kind, p, "AG004", "WARNING",
                     "description should be a single line ≤ 500 chars")
        if not body.strip():
            self.add(kind, p, "AG005", "ERROR", "Body must be non-empty")
        if len(body) > 30000:
            self.add(kind, p, "AG006", "ERROR", "Body must be ≤ 30000 chars")
        target = fm.get("target")
        if target is not None and target not in {"vscode", "github-copilot"}:
            self.add(kind, p, "AG007", "ERROR",
                     "target must be 'vscode' or 'github-copilot'")
        tools = fm.get("tools")
        tool_list: list[str] = []
        if tools is not None:
            if isinstance(tools, str):
                tool_list = [tools]
            elif isinstance(tools, list) and all(isinstance(x, str) for x in tools):
                tool_list = tools
            else:
                self.add(kind, p, "AG008", "ERROR",
                         "tools must be a string or list of strings")
            if tool_list and all(is_vscode_only_tool(t) for t in tool_list):
                self.add(kind, p, "AG009", "WARNING",
                         "tools contains only VS Code-only names; CLI effective tool set is empty")
            for t in tool_list:
                if t.lower() in NOOP_TOOLS:
                    if target != "vscode":
                        self.add(
                            kind, p, "AG017", "ERROR",
                            f"Tool token '{t}' is a no-op in the tested Copilot CLI and grants nothing; "
                            f"use {' + '.join(NOOP_TOOLS[t.lower()]) or 'nothing (remove it)'} "
                            "or set target: vscode when the agent is intentionally VS Code-only",
                        )
                elif not is_recognized_tool(t):
                    self.add(kind, p, "AG010", "INFO",
                             f"Unrecognized tool name '{t}'")
        available_agents = fm.get("agents")
        if available_agents is not None:
            if not (
                isinstance(available_agents, list)
                and all(isinstance(agent_name, str) and agent_name for agent_name in available_agents)
            ):
                self.add(kind, p, "AG023", "ERROR",
                         "agents must be a list of non-empty agent names")
            elif tools is not None and not any(
                tool.casefold() in {"agent", "task", "custom-agent"}
                for tool in tool_list
            ):
                self.add(
                    kind,
                    p,
                    "AG023",
                    "ERROR",
                    "agents requires the agent tool when tools is explicitly restricted",
                )
        for k in sorted(AG_RETIRED_KEYS & set(fm)):
            self.add(kind, p, "AG011", "WARNING",
                     f"Retired/invalid key present: {k}")
        model = fm.get("model")
        models: list[str] = []
        if model is not None:
            if isinstance(model, str):
                models = [model]
            elif isinstance(model, list) and all(isinstance(x, str) for x in model):
                models = model
            else:
                self.add(kind, p, "AG012", "ERROR",
                         "model must be a string or list of strings")
            for m in models:
                if " " in m or LEGACY_MODEL_RE.match(m):
                    self.add(kind, p, "AG013", "WARNING",
                             f"model '{m}' looks like a legacy VS Code display name")
            metadata = fm.get("metadata")
            if not (
                isinstance(metadata, dict)
                and isinstance(metadata.get("fixed-model-reason"), str)
                and metadata["fixed-model-reason"].strip()
                and isinstance(metadata.get("fixed-model-verified"), str)
                and DATE_RE.fullmatch(metadata["fixed-model-verified"])
            ):
                self.add(
                    kind,
                    p,
                    "AG022",
                    "WARNING",
                    "fixed model requires metadata.fixed-model-reason and "
                    "metadata.fixed-model-verified (YYYY-MM-DD); otherwise omit model",
                )
        name = fm.get("name")
        if name is not None and (not isinstance(name, str) or not name.strip()):
            self.add(kind, p, "AG015", "WARNING",
                     "name, if present, should be a non-empty string")
        for k in sorted(AG_VSCODE_KEYS & set(fm)):
            self.add(kind, p, "AG016", "INFO",
                     f"{k} is VS Code-only and ignored by CLI")
        for token in body_tool_tokens(body):
            self.add(
                kind, p, "AG024", "WARNING",
                f"Body teaches tool token '{token}' inside a tool list; it grants nothing in "
                "the tested Copilot CLI and is dropped silently, so agents written from this "
                "example lose capability. Use spec-valid tokens",
            )
        self._check_body_conventions(kind, p, body, "AG018", "AG019", "AG020")
        self._check_required_sections(
            kind, p, body, "AG021", AG_REQUIRED_SECTIONS)

    # Instructions
    def validate_instructions(self) -> None:
        kind = "instructions"
        d = self.root / "instructions"
        files = sorted(d.glob("*.instructions.md")) if d.is_dir() else []
        files += self.plugin_owned_files("instructions", "*.instructions.md")
        self.file_counts[kind] = len(files)
        for p in files:
            self.catch_file(kind, p, lambda p=p: self._validate_instruction(p))

    def _validate_instruction(self, p: Path) -> None:
        kind = "instructions"
        if not IN_FILENAME_RE.match(p.name):
            self.add(
                kind,
                p,
                "IN001",
                "ERROR",
                "Filename must be kebab-case and end with .instructions.md",
            )
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=False)
        if present and (err or not isinstance(fm, dict)):
            self.add(kind, p, "IN002", "ERROR",
                     f"Frontmatter delimiters exist but YAML did not parse{': ' + err if err else ''}")
            fm = {}
        if not present:
            self.add(kind, p, "IN003", "WARNING",
                     "Frontmatter is missing entirely")
            fm = {}
        if "applyTo" not in fm:
            self.add(kind, p, "IN004", "WARNING",
                     "applyTo missing; file is never auto-applied")
        else:
            if not valid_apply_to(fm.get("applyTo")):
                self.add(kind, p, "IN005", "ERROR",
                         "applyTo must be a non-empty string/list of balanced non-empty globs")
        exclude_agent = fm.get("excludeAgent")
        if exclude_agent is not None and (not isinstance(exclude_agent, str) or exclude_agent not in {"code-review", "cloud-agent"}):
            self.add(kind, p, "IN006", "ERROR",
                     "excludeAgent must be 'code-review' or 'cloud-agent'")
        for k in sorted(set(fm) - IN_VALID_KEYS):
            self.add(kind, p, "IN007", "WARNING",
                     f"Unrecognized frontmatter key: {k}")
        if "description" not in fm or not isinstance(fm.get("description"), str) or not fm.get("description", "").strip():
            self.add(kind, p, "IN008", "WARNING", "description missing")
        if not body.strip():
            self.add(kind, p, "IN009", "ERROR", "Body must be non-empty")
        self._check_body_conventions(kind, p, body, "IN010", "IN011", "IN012")
        self._check_required_sections(
            kind, p, body, "IN013", IN_REQUIRED_SECTIONS)

    # Skills
    def validate_skills(self) -> None:
        kind = "skills"
        d = self.root / "skills"
        dirs = sorted([x for x in d.iterdir() if x.is_dir()]
                      ) if d.is_dir() else []
        names: dict[str, Path] = {}
        for sd in dirs:
            p = sd / "SKILL.md"
            if not p.exists():
                self.add(kind, p, "SK010", "ERROR",
                         "Every skill directory must contain SKILL.md")
                continue
            self.catch_file(kind, p, lambda p=p,
                            names=names: self._validate_skill(p, names))
        plugin_skills = self.plugin_owned_files(
            "skills", "*/SKILL.md", generated_key="sharedSkills")
        plugin_names: dict[str, Path] = {}
        for p in plugin_skills:
            self.catch_file(kind, p, lambda p=p,
                            names=plugin_names: self._validate_skill(p, names))
        self.file_counts[kind] = len(dirs) + len(plugin_skills)

    def _validate_skill(self, p: Path, names: dict[str, Path]) -> None:
        kind = "skills"
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=True)
        if not present or err or not isinstance(fm, dict):
            self.add(kind, p, "SK001", "ERROR",
                     f"Frontmatter missing or invalid{': ' + err if err else ''}")
            fm = {}
        name = fm.get("name")
        if not isinstance(name, str) or not (1 <= len(name) <= 64) or not SK_NAME_RE.match(name) or "--" in name:
            self.add(kind, p, "SK002", "ERROR",
                     "name must be 1–64 chars, kebab-case, and not contain --")
        else:
            if name != p.parent.name:
                self.add(kind, p, "SK003", "ERROR",
                         "name must equal parent directory name")
            if name in names:
                self.add(kind, p, "SK011", "ERROR",
                         f"Duplicate skill name '{name}' also used by {self.rel(names[name])}")
            else:
                names[name] = p
        desc = fm.get("description")
        if not isinstance(desc, str) or not (1 <= len(desc) <= 1024):
            self.add(kind, p, "SK004", "ERROR",
                     "description must be present and 1–1024 chars")
        elif not SK_WHEN_RE.search(desc):
            self.add(kind, p, "SK005", "WARNING",
                     "description should express WHEN to use the skill")
        for k in sorted(set(fm) - SK_VALID_KEYS):
            self.add(kind, p, "SK006", "WARNING",
                     f"Unrecognized top-level key: {k}")
        if not body.strip():
            self.add(kind, p, "SK007", "ERROR", "Body must be non-empty")
        if len(body.splitlines()) > 500:
            self.add(kind, p, "SK008", "WARNING",
                     "Body > 500 lines; use progressive disclosure resources")
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
                self.add(kind, p, "SK012", "WARNING",
                         f"Relative link points at missing bundled resource: {link}")
        self._check_body_conventions(
            kind, p, body, "SK013", "SK014", "SK015", bundle_root=p.parent.resolve())
        self._check_required_sections(
            kind, p, body, "SK016", SK_REQUIRED_SECTIONS)

    # VS Code prompts
    def validate_prompts(self) -> None:
        kind = "prompts"
        d = self.root / "prompts"
        files = sorted(d.glob("*.prompt.md")) if d.is_dir() else []
        names: dict[str, Path] = {}
        for p in files:
            self.catch_file(kind, p, lambda p=p,
                            names=names: self._validate_prompt(p, names))
        plugin_files = self.plugin_owned_files("prompts", "*.prompt.md")
        plugin_names: dict[str, Path] = {}
        for p in plugin_files:
            self.catch_file(kind, p, lambda p=p,
                            names=plugin_names: self._validate_prompt(p, names))
        self.file_counts[kind] = len(files) + len(plugin_files)

    def _validate_prompt(self, p: Path, names: dict[str, Path]) -> None:
        kind = "prompts"
        if not PR_FILENAME_RE.match(p.name):
            self.add(kind, p, "PR001", "ERROR",
                     "Filename must be kebab-case and end with .prompt.md")
        text = read_text(p)
        fm, body, present, err = parse_frontmatter(text, required=True)
        if not present or err or not isinstance(fm, dict):
            self.add(kind, p, "PR002", "ERROR",
                     f"Frontmatter missing or invalid{': ' + err if err else ''}")
            fm = {}
        name = fm.get("name")
        expected_name = p.name[:-len(".prompt.md")]
        if not isinstance(name, str) or not SK_NAME_RE.match(name) or "--" in name:
            self.add(kind, p, "PR003", "ERROR",
                     "name must be non-empty kebab-case")
        else:
            if name != expected_name:
                self.add(kind, p, "PR003", "ERROR",
                         "name must match the filename")
            if name in names:
                self.add(kind, p, "PR003", "ERROR",
                         f"Duplicate prompt name '{name}' also used by {self.rel(names[name])}")
            else:
                names[name] = p
        desc = fm.get("description")
        if not isinstance(desc, str) or not desc.strip():
            self.add(kind, p, "PR004", "ERROR",
                     "description must be a non-empty string")
        for key in sorted(set(fm) - PR_VALID_KEYS):
            self.add(kind, p, "PR005", "WARNING",
                     f"Unrecognized VS Code prompt frontmatter key: {key}")
        for key in ("argument-hint", "agent", "model"):
            if key in fm and (not isinstance(fm[key], str) or not fm[key].strip()):
                self.add(kind, p, "PR005", "ERROR",
                         f"{key} must be a non-empty string when present")
        tools = fm.get("tools")
        if tools is not None and not (
            isinstance(tools, str)
            or (isinstance(tools, list) and all(isinstance(tool, str) and tool for tool in tools))
        ):
            self.add(kind, p, "PR005", "ERROR",
                     "tools must be a string or a list of non-empty strings")
        else:
            tool_list = [tools] if isinstance(tools, str) else tools or []
            for tool in tool_list:
                normalized = tool.casefold()
                if normalized in LEGACY_PROMPT_TOOLS:
                    self.add(
                        kind,
                        p,
                        "PR009",
                        "ERROR",
                        f"legacy VS Code prompt tool '{tool}' must use a current alias or tool set",
                    )
                elif (
                    normalized not in VSCODE_PROMPT_TOOL_ALIASES
                    and normalized not in VSCODE_PROMPT_TOOL_SETS
                    and not MCP_TOOL_RE.fullmatch(tool)
                ):
                    self.add(
                        kind,
                        p,
                        "PR009",
                        "WARNING",
                        f"prompt tool '{tool}' is environment-specific and requires runtime verification",
                    )
        if "model" in fm:
            self.add(
                kind,
                p,
                "PR010",
                "WARNING",
                "fixed prompt models are intentionally unsupported by repository policy; "
                "inherit the model picker unless a dated exception is added",
            )
        if not body.strip():
            self.add(kind, p, "PR006", "ERROR", "Body must be non-empty")
        elif not body_starts_with_h1(body):
            self.add(kind, p, "PR006", "ERROR",
                     "Body must open with a single H1 naming the prompt")
        self._check_required_sections(
            kind, p, body, "PR007", PR_REQUIRED_SECTIONS)
        if TEMPLATE_PLACEHOLDER_RE.search(body):
            self.add(kind, p, "PR008", "ERROR",
                     "Unresolved uppercase double-brace template placeholder")

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
            self.add(kind, p, h1_rule, "INFO",
                     "Body should open with a single H1 naming the primitive")

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
        duplicates = [
            heading for heading in required if headings.count(heading) > 1]
        if missing:
            issues.append(f"missing required sections: {', '.join(missing)}")
        if duplicates:
            issues.append(
                f"duplicate required sections: {', '.join(duplicates)}")
        if not missing and not duplicates:
            positions = [headings.index(heading) for heading in required]
            if positions != sorted(positions):
                issues.append("required sections are out of template order")
        authoring_only = sorted(AUTHORING_ONLY_SECTIONS.intersection(headings))
        if authoring_only:
            issues.append(
                f"authoring-only sections remain: {', '.join(authoring_only)}")
        if issues:
            self.add(kind, p, rule_id, "ERROR", "; ".join(issues))

    # Plugins
    def validate_plugins(self) -> None:
        kind = "plugins"
        d = self.root / "plugins"
        dirs = sorted([x for x in d.iterdir() if x.is_dir()]
                      ) if d.is_dir() else []
        self.file_counts[kind] = len(dirs)
        for pd in dirs:
            manifest = None
            for rel in PLUGIN_MANIFESTS:
                q = pd / rel
                if q.exists():
                    manifest = q
                    break
            if manifest is None:
                self.add(kind, pd, "PL001", "ERROR",
                         "No plugin manifest found in supported locations")
                continue
            self.catch_file(kind, manifest, lambda manifest=manifest,
                            pd=pd: self._validate_plugin(manifest, pd))

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
            self.add(kind, p, "PL003", "ERROR",
                     "name must be kebab-case and ≤ 64 chars")
        elif name != plugin_dir.name:
            self.add(kind, p, "PL004", "WARNING",
                     "name differs from plugin directory name")
        version = data.get("version")
        if not isinstance(version, str) or not SEMVER_RE.match(version):
            self.add(kind, p, "PL005", "WARNING",
                     "version missing or not semver")
        desc = data.get("description")
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
            self.add(kind, p, "PL006", "WARNING",
                     "description missing or > 1024 chars")
        managed_plugin = plugin_dir.name in self.plugin_sources
        for k in sorted(set(data) - PL_VALID_KEYS):
            severity = "ERROR" if managed_plugin else "WARNING"
            self.add(kind, p, "PL007", severity,
                     f"Unrecognized top-level key: {k}")
        for label, ref in collect_plugin_refs(data):
            if not isinstance(ref, str) or not ref.strip() or has_variable(ref):
                continue
            resolved, base = resolve_component_ref(ref, p.parent, self.root)
            if resolved is None:
                self.add(kind, p, "PL008", "ERROR",
                         f"{label} path '{ref}' did not resolve relative to manifest dir or repo root")
            # Resolution base is intentionally not emitted on success to avoid noisy INFO; errors include both attempted bases.
            if label.endswith("skills") and not ref.endswith("/"):
                self.add(kind, p, "PL009", "WARNING",
                         f"skill ref should end with '/': {ref}")
            if label.endswith("agents") and not (
                ref.endswith(".agent.md") or ref.endswith("/")
            ):
                self.add(
                    kind,
                    p,
                    "PL009",
                    "WARNING",
                    f"agent ref should be an agent directory or end with '.agent.md': {ref}",
                )
        author = data.get("author")
        if author is not None and not (isinstance(author, dict) and isinstance(author.get("name"), str) and author.get("name", "").strip()):
            self.add(kind, p, "PL010", "WARNING",
                     "author, if present, should be an object with a name")
        if managed_plugin:
            self._validate_flat_plugin(
                p,
                plugin_dir,
                data,
                self.plugin_sources[plugin_dir.name],
            )

    def _validate_flat_plugin(
        self,
        p: Path,
        plugin_dir: Path,
        data: dict[str, Any],
        source_config: dict[str, Any],
    ) -> None:
        kind = "plugins"
        if "$schema" in data:
            self.add(
                kind,
                p,
                "PL011",
                "ERROR",
                "managed GitHub Copilot plugins use the flat manifest and must not declare the Agent Plugins schema",
            )
        namespace = plugin_dir / "com.github.copilot"
        if namespace.exists():
            self.add(
                kind,
                namespace,
                "PL011",
                "ERROR",
                "com.github.copilot directories are prohibited; keep components at the plugin root",
            )

        component_source = source_config.get("componentSource")
        expected_agents: list[str] = []
        expected_skills: list[str] = []
        expected_extensions: list[str] = []
        if component_source == "library":
            for key, expected_prefix in (("agents", "./agents/"), ("skills", "./skills/")):
                refs = source_config.get(key)
                if not isinstance(refs, list) or not all(
                    isinstance(ref, str) and ref.startswith(expected_prefix) for ref in refs
                ):
                    self.add(
                        kind,
                        p,
                        "PL016",
                        "ERROR",
                        f"library component `{key}` must be a list of {expected_prefix} references",
                    )
                    continue
                if len(refs) != len(set(refs)):
                    self.add(kind, p, "PL016", "ERROR",
                             f"library component `{key}` contains duplicates")
                if key == "agents":
                    expected_agents = refs
                else:
                    expected_skills = refs
        elif component_source == "plugin":
            shared_skills = source_config.get("sharedSkills", [])
            if not (
                isinstance(shared_skills, list)
                and len(shared_skills) == len(set(shared_skills))
                and all(
                    isinstance(ref, str)
                    and ref.startswith("./skills/")
                    and ref.endswith("/")
                    for ref in shared_skills
                )
            ):
                self.add(
                    kind,
                    p,
                    "PL016",
                    "ERROR",
                    "plugin sharedSkills must be unique ./skills/<name>/ references",
                )
                shared_skills = []
            for ref in shared_skills:
                shared_source = self.root / ref.removeprefix("./").rstrip("/")
                if not (shared_source / "SKILL.md").is_file():
                    self.add(
                        kind,
                        p,
                        "PL016",
                        "ERROR",
                        f"shared canonical skill is missing: {ref}",
                    )
            expected_agents = [
                f"./agents/{path.name}" for path in sorted((plugin_dir / "agents").glob("*.agent.md"))
            ]
            expected_skills = [
                f"./skills/{path.name}/"
                for path in sorted(plugin_dir.joinpath("skills").iterdir())
                if path.is_dir() and (path / "SKILL.md").is_file()
            ] if (plugin_dir / "skills").is_dir() else []
        else:
            self.add(
                kind,
                p,
                "PL016",
                "ERROR",
                "source metadata componentSource must be `plugin` or `library`",
            )

        actual_agents = {
            path.name for path in (plugin_dir / "agents").glob("*.agent.md")
        }
        expected_agent_names = {Path(ref).name for ref in expected_agents}
        if actual_agents != expected_agent_names:
            self.add(
                kind,
                p,
                "PL012",
                "ERROR",
                "direct agents/ content does not match canonical source metadata",
            )
        if expected_agent_names:
            if data.get("agents") != "agents/":
                self.add(
                    kind,
                    p,
                    "PL012",
                    "ERROR",
                    "plugins with agents must declare `agents: \"agents/\"`",
                )
        elif "agents" in data:
            self.add(kind, p, "PL012", "ERROR",
                     "agents field exists but agents/ is empty")

        actual_skills = {
            path.name
            for path in (plugin_dir / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        } if (plugin_dir / "skills").is_dir() else set()
        expected_skill_names = {
            Path(ref.rstrip("/")).name for ref in expected_skills}
        if actual_skills != expected_skill_names:
            self.add(
                kind,
                p,
                "PL016",
                "ERROR",
                "direct skills/ content does not match canonical source metadata",
            )
        if expected_skill_names:
            if data.get("skills") != "skills/":
                self.add(
                    kind,
                    p,
                    "PL016",
                    "ERROR",
                    "plugins with skills must declare `skills: \"skills/\"`",
                )
        elif "skills" in data:
            self.add(kind, p, "PL016", "ERROR",
                     "skills field exists but skills/ is empty")

        extension_refs = source_config.get("extensionSources", [])
        if extension_refs is not None:
            if not isinstance(extension_refs, list) or not all(
                isinstance(ref, str) and ref.startswith("./extensions/")
                for ref in extension_refs
            ):
                self.add(
                    kind,
                    p,
                    "PL017",
                    "ERROR",
                    "extensionSources must be a list of ./extensions/ references",
                )
            else:
                expected_extensions = extension_refs
                if len(extension_refs) != len(set(extension_refs)):
                    self.add(kind, p, "PL017", "ERROR",
                             "extensionSources contains duplicates")

        if "hookSource" in source_config:
            hook_ref = source_config["hookSource"]
            if not isinstance(hook_ref, str) or not hook_ref.startswith("./"):
                self.add(
                    kind,
                    p,
                    "PL015",
                    "ERROR",
                    "repository hookSource must be a plugin-relative './' path",
                )
            else:
                source = (plugin_dir / hook_ref[2:]).resolve()
                try:
                    source.relative_to(plugin_dir.resolve())
                except ValueError:
                    self.add(kind, p, "PL015", "ERROR",
                             "repository hookSource escapes plugin root")
                else:
                    if not source.is_file():
                        self.add(kind, p, "PL015", "ERROR",
                                 f"repository hookSource not found: {hook_ref}")
                manifest_hook = hook_ref.removeprefix("./")
                if data.get("hooks") != manifest_hook:
                    self.add(
                        kind,
                        p,
                        "PL015",
                        "ERROR",
                        f"plugin hooks field must equal `{manifest_hook}`",
                    )
                else:
                    self._validate_hook(source, plugin_dir)
        elif "hooks" in data:
            self.add(kind, p, "PL015", "ERROR",
                     "hooks field has no canonical hook source")

        manifest_extensions = data.get("extensions", [])
        normalized_manifest_extensions = (
            [manifest_extensions]
            if isinstance(manifest_extensions, str)
            else manifest_extensions
        )
        expected_manifest_extensions = [
            ref.removeprefix("./") for ref in expected_extensions
        ]
        if normalized_manifest_extensions != expected_manifest_extensions:
            self.add(
                kind,
                p,
                "PL017",
                "ERROR",
                "extensions field does not match direct extension sources",
            )
        for ref in expected_extensions:
            canonical = plugin_dir / ref[2:].rstrip("/")
            if not canonical.is_dir():
                self.add(kind, p, "PL017", "ERROR",
                         f"canonical extension is missing: {ref}")

        mcp_path = plugin_dir / "mcp.json"
        if mcp_path.exists():
            if data.get("mcpServers") != "mcp.json":
                self.add(
                    kind,
                    p,
                    "PL014",
                    "ERROR",
                    "plugins with mcp.json must declare `mcpServers: \"mcp.json\"`",
                )
            self._validate_open_plugin_mcp(mcp_path)
        elif "mcpServers" in data:
            self.add(kind, p, "PL014", "ERROR",
                     "mcpServers field exists but mcp.json is missing")
        if not (
            expected_agents
            or expected_skills
            or expected_extensions
            or "hookSource" in source_config
            or mcp_path.is_file()
        ):
            self.add(kind, p, "PL018", "ERROR",
                     "plugin declares no installable component")

    def _validate_open_plugin_mcp(self, p: Path) -> None:
        kind = "plugins"
        try:
            data = json.loads(read_text(p))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.add(kind, p, "PL013", "ERROR",
                     f"Invalid Open Plugin MCP JSON: {exc}")
            return
        if not isinstance(data, dict):
            self.add(kind, p, "PL013", "ERROR",
                     "Open Plugin MCP root must be an object")
            return
        if data.get("$schema") != OPEN_MCP_SCHEMA:
            self.add(kind, p, "PL013", "ERROR",
                     f"mcp.json must declare $schema {OPEN_MCP_SCHEMA}")
        extra_keys = sorted(set(data) - {"$schema", "mcpServers"})
        if extra_keys:
            self.add(kind, p, "PL013", "ERROR",
                     f"Unsupported mcp.json keys: {', '.join(extra_keys)}")
        servers = data.get("mcpServers")
        if not isinstance(servers, dict):
            self.add(kind, p, "PL013", "ERROR",
                     "mcp.json mcpServers must be an object")
            return
        for name, config in servers.items():
            if not isinstance(name, str) or not name or not isinstance(config, dict):
                self.add(kind, p, "PL014", "ERROR",
                         "MCP servers require non-empty names and object configs")
                continue
            server_type = config.get("type")
            if server_type == "stdio":
                allowed = {"type", "command", "args", "env", "cwd"}
                if not isinstance(config.get("command"), str) or not config["command"]:
                    self.add(kind, p, "PL014", "ERROR",
                             f"MCP server '{name}' requires a command")
                args = config.get("args")
                if args is not None and not (
                    isinstance(args, list) and all(isinstance(arg, str)
                                                   for arg in args)
                ):
                    self.add(kind, p, "PL014", "ERROR",
                             f"MCP server '{name}' args must be strings")
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
                    self.add(kind, p, "PL014", "ERROR",
                             f"MCP server '{name}' env is invalid")
            elif server_type in {"streamable-http", "sse"}:
                allowed = {"type", "url", "headers"}
                if not isinstance(config.get("url"), str) or not config["url"]:
                    self.add(kind, p, "PL014", "ERROR",
                             f"MCP server '{name}' requires a URL")
                headers = config.get("headers")
                if headers is not None and not (
                    isinstance(headers, dict)
                    and all(isinstance(key, str) and isinstance(value, str) for key, value in headers.items())
                ):
                    self.add(kind, p, "PL014", "ERROR",
                             f"MCP server '{name}' headers are invalid")
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
        kind = "hooks"
        d = self.root / "hooks"
        files: list[tuple[Path, Path]] = [(p, self.root) for p in sorted(
            d.glob("*/hooks.json"))] if d.is_dir() else []
        repo_root = find_repo_root(self.root)
        installed = repo_root / ".github" / "hooks"
        if installed.is_dir() and installed.resolve() != d.resolve():
            files += [(p, repo_root) for p in sorted(installed.glob("*.json"))]
        self.file_counts[kind] = len(files)
        for p, base in files:
            identifier = p.parent.name if base.resolve() == self.root else p.stem
            if not re.fullmatch(IDENTIFIER_PATTERN, identifier):
                self.add(
                    kind,
                    p,
                    "HK012",
                    "ERROR",
                    "Hook package and installed file identifiers must be kebab-case",
                )
            self.catch_file(kind, p, lambda p=p,
                            base=base: self._validate_hook(p, base))

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
                    self.add(kind, p, "HK005", "WARNING",
                             f"Use native camelCase event name instead of PascalCase alias '{event}'")
                else:
                    self.add(kind, p, "HK004", "ERROR",
                             f"Unknown hook event name: {event}")
            if not isinstance(entries, list):
                self.add(kind, p, "HK006", "ERROR",
                         f"Entries for {event} must be a list")
                continue
            for idx, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    self.add(kind, p, "HK006", "ERROR",
                             f"Hook entry {event}[{idx}] must be an object")
                    continue
                loc = f"{event}[{idx}]"
                etype = entry.get("type")
                if etype is not None and etype not in {"command", "http"}:
                    self.add(kind, p, "HK011", "WARNING",
                             f"{loc} type should be 'command' or 'http'")
                has_runner = any(entry.get(k) for k in ("bash", "powershell", "command")) or (
                    entry.get("type") == "http" and entry.get("url"))
                if not has_runner:
                    self.add(kind, p, "HK006", "ERROR",
                             f"{loc} must define bash, powershell, command, or http url")
                for k in sorted(set(entry) - HK_VALID_KEYS):
                    self.add(kind, p, "HK007", "WARNING",
                             f"{loc} has unrecognized key: {k}")
                timeout = entry.get("timeoutSec")
                if not isinstance(timeout, int) or timeout <= 0:
                    self.add(kind, p, "HK010", "WARNING",
                             f"{loc} timeoutSec missing or not a positive integer")
                for k in ("bash", "powershell", "command"):
                    cmd = entry.get(k)
                    for script in referenced_scripts(cmd):
                        resolved = resolve_script(script, p.parent, base)
                        if resolved is None:
                            self.add(
                                kind, p, "HK008", "ERROR", f"{loc} {k} script '{script}' does not exist relative to repo root or hook dir")
                        elif not os.access(resolved, os.X_OK):
                            self.add(
                                kind, p, "HK009", "ERROR", f"{loc} {k} script '{script}' is not executable")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str, required: bool) -> tuple[dict[str, Any], str, bool, str | None]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text, False, None if not required else "opening --- not found"
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
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
    first = _next_yaml_content(src, 0)
    if first >= len(src):
        return {}
    value, end = _parse_yaml_node(src, first, _yaml_indent(src[first]))
    trailing = _next_yaml_content(src, end)
    if trailing != len(src):
        raise ValueError(f"cannot parse line: {src[trailing]}")
    if not isinstance(value, dict):
        raise ValueError("frontmatter is not a map")
    return value


def _next_yaml_content(src: list[str], index: int) -> int:
    while index < len(src):
        stripped = src[index].strip()
        if stripped and not stripped.startswith("#"):
            return index
        index += 1
    return index


def _yaml_indent(line: str) -> int:
    if "\t" in line[: len(line) - len(line.lstrip())]:
        raise ValueError("tabs are not supported in YAML indentation")
    return len(line) - len(line.lstrip(" "))


def _parse_yaml_node(src: list[str], index: int, indent: int) -> tuple[Any, int]:
    stripped = src[index].strip()
    if stripped.startswith("- "):
        return _parse_yaml_sequence(src, index, indent)
    if ":" in stripped:
        return _parse_yaml_mapping(src, index, indent)
    return parse_scalar(stripped), index + 1


def _parse_yaml_mapping(src: list[str], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while True:
        index = _next_yaml_content(src, index)
        if index >= len(src):
            break
        line = src[index]
        current_indent = _yaml_indent(line)
        stripped = line.strip()
        if current_indent < indent or current_indent != indent or stripped.startswith("- "):
            break
        if ":" not in stripped:
            raise ValueError(f"cannot parse mapping line: {line}")
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise ValueError("empty key")
        index += 1
        if raw_value in {"|", ">", "|-", ">-"}:
            result[key], index = _parse_yaml_block_scalar(
                src,
                index,
                indent,
                raw_value,
            )
            continue
        if raw_value:
            result[key] = parse_scalar(raw_value)
            continue
        child = _next_yaml_content(src, index)
        if child >= len(src) or _yaml_indent(src[child]) <= indent:
            result[key] = {}
            index = child
            continue
        result[key], index = _parse_yaml_node(
            src, child, _yaml_indent(src[child]))
    return result, index


def _parse_yaml_sequence(src: list[str], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    mapping_item = re.compile(r"^([A-Za-z0-9_.-]+)\s*:(.*)$")
    while True:
        index = _next_yaml_content(src, index)
        if index >= len(src):
            break
        line = src[index]
        if _yaml_indent(line) != indent or not line.strip().startswith("- "):
            break
        raw_item = line.strip()[2:].strip()
        index += 1
        match = mapping_item.match(raw_item)
        if match is None:
            result.append(parse_scalar(raw_item))
            continue
        key, raw_value = match.groups()
        item: dict[str, Any] = {key: parse_scalar(
            raw_value.strip()) if raw_value.strip() else {}}
        child = _next_yaml_content(src, index)
        if child < len(src) and _yaml_indent(src[child]) > indent:
            child_indent = _yaml_indent(src[child])
            if raw_value.strip():
                remainder, index = _parse_yaml_mapping(
                    src, child, child_indent)
                item.update(remainder)
            else:
                item[key], index = _parse_yaml_node(src, child, child_indent)
        result.append(item)
    return result, index


def _parse_yaml_block_scalar(
    src: list[str],
    index: int,
    parent_indent: int,
    marker: str,
) -> tuple[str, int]:
    block: list[str] = []
    content_indent: int | None = None
    while index < len(src):
        line = src[index]
        if line.strip():
            indent = _yaml_indent(line)
            if indent <= parent_indent:
                break
            content_indent = indent if content_indent is None else min(
                content_indent, indent)
        block.append(line)
        index += 1
    base_indent = content_indent if content_indent is not None else parent_indent + 2
    dedented = [line[base_indent:] if line.strip() else "" for line in block]
    text = "\n".join(dedented)
    if marker.startswith(">"):
        text = " ".join(line.strip() for line in dedented)
    if not marker.endswith("-"):
        text += "\n"
    return text, index


def parse_scalar(val: str) -> Any:
    if val == "":
        return ""
    if val in {"true", "True"}:
        return True
    if val in {"false", "False"}:
        return False
    if val in {"null", "Null", "~"}:
        return None
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
        try:
            return int(val)
        except Exception:
            pass
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
            if ch == open_c:
                depth += 1
            elif ch == close_c:
                depth -= 1
                if depth < 0:
                    return False
        if depth != 0:
            return False
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


def body_tool_tokens(body: str) -> list[str]:
    """Return no-op or legacy tool tokens taught as usable tool lists in a body.

    Agents that document tool lists propagate them into the agents they generate, and
    the CLI drops unrecognized tokens silently, so a wrong example removes capability
    with no error anywhere. Fenced blocks are skipped: they hold source samples and MCP
    server configuration whose arrays legitimately contain words like `run` or `search`.
    """
    offenders: set[str] = set()
    for line in strip_code_fences(body).splitlines():
        if BODY_TOOL_HEDGE_RE.search(line):
            continue
        candidates: list[str] = []
        for match in BODY_TOOL_LIST_RE.finditer(line):
            candidates.extend(BODY_QUOTED_TOKEN_RE.findall(match.group(0)))
        for match in BODY_BACKTICK_RUN_RE.finditer(line):
            candidates.extend(BODY_BACKTICK_TOKEN_RE.findall(match.group(0)))
        offenders.update(
            token for token in candidates
            if token.casefold() in BODY_TOOL_VOCABULARY
        )
    return sorted(offenders)


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
                        if isinstance(x.get(k), str):
                            yield label, x[k]
        elif isinstance(val, dict):
            for k in ("path", "source"):
                if isinstance(val.get(k), str):
                    yield label, val[k]
            # mcpServers may be name -> path/config
            for v in val.values():
                if isinstance(v, str):
                    yield label, v
                elif isinstance(v, dict):
                    for k in ("path", "source"):
                        if isinstance(v.get(k), str):
                            yield label, v[k]
    for key in ("agents", "skills", "commands", "hooks", "mcpServers", "extensions"):
        yield from strings(key, data.get(key))


def resolve_component_ref(ref: str, manifest_dir: Path, root: Path) -> tuple[Path | None, str | None]:
    cleaned = ref.split("#", 1)[0]
    for base_name, base in (("manifest", manifest_dir), ("root", root)):
        candidate = (
            base / cleaned).resolve() if not Path(cleaned).is_absolute() else Path(cleaned)
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
            refs.append(part)
            break
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
        summary.append({"kind": kind, "files": v.file_counts.get(kind, 0), "errors": sum(
            f.severity == "ERROR" for f in fs), "warnings": sum(f.severity == "WARNING" for f in fs)})
    return {"summary": summary, "findings": [asdict(f) for f in v.findings]}


def print_human(v: Validator) -> None:
    order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    for kind in ALL_KINDS:
        fs = [f for f in v.findings if f.kind == kind and (
            not v.quiet or f.severity == "ERROR")]
        if not fs and v.quiet:
            continue
        print(f"\n## {kind} ({v.file_counts.get(kind, 0)} files)")
        grouped: dict[str, list[Finding]] = defaultdict(list)
        for f in sorted(fs, key=lambda x: (x.rule_id, order.get(x.severity, 9), x.file)):
            grouped[f.rule_id].append(f)
        for rule, items in grouped.items():
            counts = Counter(i.severity for i in items)
            count_s = ", ".join(f"{sev}={counts[sev]}" for sev in (
                "ERROR", "WARNING", "INFO") if counts[sev])
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
    ap = argparse.ArgumentParser(
        description="Validate Copilot primitive files against the canonical harness spec.")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on warnings as well as errors")
    ap.add_argument("--json", action="store_true", dest="json_out",
                    help="emit machine-readable JSON report to stdout")
    ap.add_argument("--kind", action="append", choices=ALL_KINDS,
                    help="validate only this kind; repeatable")
    ap.add_argument(
        "--root",
        type=Path,
        default=default_harness_root(),
        help="canonical harness root (default: <repo>/harness/github-copilot)",
    )
    ap.add_argument("--quiet", action="store_true",
                    help="human output: only summary and errors")
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

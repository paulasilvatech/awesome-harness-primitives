---
name: agent-supply-chain
description: >-
  Verify supply chain integrity for AI agent plugins, MCP servers, tools, and dependencies by
  generating SHA-256 manifests, verifying installed files, auditing pinned versions, and enforcing
  promotion gates. Use when asked to verify plugin integrity, generate INTEGRITY.json, check
  supply chain, detect tampering, audit dependency pinning, sign this plugin, or promote dev →
  staging → production.
---

<!-- Generated from harness/github-copilot/skills/agent-supply-chain/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Agent supply chain integrity

Verify agent plugin and MCP server integrity by hashing source files, comparing them to `INTEGRITY.json`, flagging modified, missing, or untracked files, auditing dependency pinning, and producing promotion evidence.

## When to invoke

- "Verify plugin integrity before deployment."
- "Generate an INTEGRITY.json manifest for this agent plugin."
- "Check whether an MCP server directory was tampered with."
- "Audit dependency pinning for this agent component."
- "Build a provenance gate for dev → staging → production."

## Integrity model

Agent plugins and MCP servers carry the same supply-chain risks as npm packages or container images, but many agent ecosystems do not yet provide npm Provenance, Sigstore, or SLSA by default. Fill that gap with deterministic SHA-256 manifests and promotion gates.

```text
Plugin Directory → Hash All Files (SHA-256) → Generate INTEGRITY.json
                                                    ↓
Later: Plugin Directory → Re-Hash Files → Compare Against INTEGRITY.json
                                                    ↓
                                          Match? VERIFIED : TAMPERED
```

Use this before production promotion, during plugin PR review, as a CI step after review, when auditing third-party agent tools or MCP servers, and when building a plugin marketplace with integrity requirements.

## Manifest format

| Field | Required | Rule |
| --- | --- | --- |
| `plugin_name` | Yes | Directory name of the plugin or server package. |
| `generated_at` | Yes | UTC ISO timestamp from `datetime.now(timezone.utc).isoformat()`. |
| `algorithm` | Yes | Always `sha256`. |
| `file_count` | Yes | Count of hashed files after exclusions. |
| `files` | Yes | Map of relative paths to SHA-256 hex digests. |
| `manifest_hash` | Yes | SHA-256 of all file hashes concatenated in sorted path order. |

Exclude transient and generated paths with `EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache"}` and `EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "INTEGRITY.json"}`. Never hash the manifest into itself.

```json
{
  "plugin_name": "my-plugin",
  "generated_at": "2026-04-01T03:00:00+00:00",
  "algorithm": "sha256",
  "file_count": 12,
  "files": {
    ".claude-plugin/plugin.json": "a1b2c3d4...",
    "README.md": "e5f6a7b8...",
    "skills/search/SKILL.md": "c9d0e1f2...",
    "agency.json": "3a4b5c6d..."
  },
  "manifest_hash": "7e8f9a0b1c2d3e4f..."
}
```

## Core algorithms

Use this implementation pattern when executable logic is needed. Preserve the required APIs: `hashlib.sha256`, `json.dumps`, `Path.rglob`, `Path.write_text`, `Path.read_text`, `hash_file`, `generate_manifest`, `verify_manifest`, `audit_versions`, and `promotion_check`.

```python
import hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "INTEGRITY.json"}
def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()
def generate_manifest(plugin_dir: str) -> dict:
    root = Path(plugin_dir); files = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name not in EXCLUDE_FILES and not any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts):
            files[path.relative_to(root).as_posix()] = hash_file(path)
    chain = hashlib.sha256()
    for key in sorted(files.keys()): chain.update(files[key].encode("ascii"))
    return {"plugin_name": root.name, "generated_at": datetime.now(timezone.utc).isoformat(), "algorithm": "sha256", "file_count": len(files), "files": files, "manifest_hash": chain.hexdigest()}
def verify_manifest(plugin_dir: str) -> tuple[bool, list[str]]:
    root = Path(plugin_dir); manifest_path = root / "INTEGRITY.json"
    if not manifest_path.exists(): return False, ["INTEGRITY.json not found"]
    manifest = json.loads(manifest_path.read_text()); recorded = manifest.get("files", {}); errors = []
    for rel_path, expected_hash in recorded.items():
        full = root / rel_path
        if not full.exists(): errors.append(f"MISSING: {rel_path}")
        elif hash_file(full) != expected_hash: errors.append(f"MODIFIED: {rel_path}")
    for rel_path in generate_manifest(plugin_dir)["files"]:
        if rel_path not in recorded: errors.append(f"UNTRACKED: {rel_path}")
    return len(errors) == 0, errors
def audit_versions(config_path: str) -> list[dict]:
    path = Path(config_path); content = path.read_text(); findings = []
    if path.name == "package.json":
        for section in ("dependencies", "devDependencies"):
            for pkg, ver in json.loads(content).get(section, {}).items():
                if ver.startswith("^") or ver.startswith("~") or ver == "*" or ver == "latest": findings.append({"package": pkg, "version": ver, "severity": "HIGH" if ver in ("*", "latest") else "MEDIUM", "fix": f'Pin to exact: "{pkg}": "{ver.lstrip("^~")}"'})
    elif path.name in ("requirements.txt", "pyproject.toml"):
        for line in content.splitlines():
            if ">=" in line.strip() and "<" not in line: findings.append({"package": line.split(">=")[0].strip(), "version": line.strip(), "severity": "MEDIUM", "fix": f"Add upper bound: {line.strip()},<next_major"})
    return findings
```

## Promotion gate

| Gate | Check | Failure |
| --- | --- | --- |
| Integrity | `verify_manifest(plugin_dir)` passes | Missing `INTEGRITY.json`, `MODIFIED`, `MISSING`, or `UNTRACKED` files. |
| Required files | `README.md` exists and at least one manifest exists | Missing `.github/plugin/plugin.json (or .claude-plugin/plugin.json)`. |
| Pinned deps | `.mcp.json` has no `@latest`; `package.json`, `requirements.txt`, and `pyproject.toml` are pinned | Unpinned versions, `*`, `latest`, `^`, `~`, or unconstrained `>=`. |
| Chain hash | `manifest_hash` matches sorted file hash chain | Manifest was regenerated incorrectly or files changed after review. |

The promotion result should be `{"ready": all_passed, "checks": checks}`. If ready, print `Plugin is ready for production promotion`; otherwise print `Plugin NOT ready:` and the failed check names.

## CI integration

Use `PLUGIN_DIR` in GitHub Actions when matrix jobs verify multiple plugins. The workflow should `cd "$PLUGIN_DIR"`, load `INTEGRITY.json`, check each `manifest['files']` entry, emit `::error::` for each mismatch, call `sys.exit(1)` on failure, and print `Verified {len(manifest["files"])} files` on success.

```yaml
- name: Verify plugin integrity
  run: |
    PLUGIN_DIR="${{ matrix.plugin || '.' }}"
    cd "$PLUGIN_DIR"
    python -c "from pathlib import Path; import json, hashlib, sys; print('verify INTEGRITY.json')"
```

## Best practices

| Practice | Rationale |
| --- | --- |
| Generate manifest after code review | Ensures reviewed code matches production code. |
| Include manifest in the PR | Reviewers can verify what was hashed. |
| Verify in CI before deploy | Catches post-review modifications. |
| Chain hash for tamper evidence | Single hash represents entire plugin state. |
| Exclude build artifacts | Only hash source files; `.git`, `__pycache__`, and `node_modules` are excluded. |
| Pin all dependency versions | Unpinned deps means different code on every install. |

## Implementation names

Keep these names stable when converting examples into scripts: `my-plugin/INTEGRITY.json`, `manifest_paths`, `mcp_path`, `required_files`, `pinned_deps`, and `FAILED`. They appear in expected promotion-check output and make CI failures searchable.

## Output template

```markdown
## Agent supply chain report - <plugin or server>

**Status:** VERIFIED | TAMPERED | NOT READY | BLOCKED
**Manifest:** `INTEGRITY.json`
**Algorithm:** `sha256`
**Manifest hash:** `<hash>`

| Check | Result | Evidence | Action |
| --- | --- | --- | --- |
| File integrity | pass/fail | `<file_count>` files checked; `MODIFIED/MISSING/UNTRACKED` list | <fix> |
| Required files | pass/fail | `README.md`, `.github/plugin/plugin.json`, `.claude-plugin/plugin.json` | <fix> |
| Dependency pinning | pass/fail | `package.json`, `requirements.txt`, `pyproject.toml`, `.mcp.json` | <fix> |
| Promotion readiness | pass/fail | `ready: true/false` | <gate decision> |

### Findings
- `<severity>`: `<file or dependency>` - `<problem>` - `<fix>`
```

## Quality gate

- [ ] Every source file is hashed with SHA-256 unless excluded by `EXCLUDE_DIRS` or `EXCLUDE_FILES`.
- [ ] `INTEGRITY.json` contains `plugin_name`, `generated_at`, `algorithm`, `file_count`, `files`, and `manifest_hash`.
- [ ] Verification reports `MODIFIED`, `MISSING`, and `UNTRACKED` separately.
- [ ] Dependency audit covers `package.json`, `requirements.txt`, `pyproject.toml`, `.mcp.json`, and `@latest` MCP arguments when present.
- [ ] Promotion gate checks `README.md` plus `.github/plugin/plugin.json (or .claude-plugin/plugin.json)`.
- [ ] CI fails closed with `sys.exit(1)` and does not silently ignore integrity errors.

## References

- [OpenSSF SLSA](https://slsa.dev/)
- [npm Provenance](https://docs.npmjs.com/generating-provenance-statements)
- [Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
- [OWASP ASI-09: Supply Chain Integrity](https://genai.owasp.org/)

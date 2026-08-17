---
name: mcp-security-audit
description: >-
  Audits MCP server configurations such as .mcp.json for hardcoded secrets, dangerous shell patterns, unpinned dependencies, unsafe npx usage, unapproved servers, and governance risks. Use this skill when asked to check MCP security, audit MCP servers, review .mcp.json, validate server args, detect shell injection, or verify environment-variable based credentials.
---

# MCP security audit

Audit Model Context Protocol server configurations for secrets exposure, shell injection, unpinned dependencies, dangerous commands, and unapproved server governance and supply-chain risks. Produce a findings report with severity, evidence, and concrete remediation.

## When to invoke

- "Audit my MCP servers."
- "Is this .mcp.json secure?"
- "Check MCP server args for secrets or shell injection."
- "Find unpinned MCP dependencies like @latest."
- "Review which MCP servers this project registers."

## Prerequisites and context

- The primary target is `.mcp.json` or an equivalent MCP server configuration.
- Use environment variable references such as `${ENV_VAR_NAME}` instead of hardcoded credentials.
- If an organization has an approved MCP server list, compare registered servers against it.

## Audit model

```text
.mcp.json → Parse Servers → Check Each Server:
  1. Secrets in args/env?
  2. Shell injection patterns?
  3. Unpinned versions (@latest)?
  4. Dangerous commands (eval, bash -c)?
  5. Server on approved list?
→ Generate Report
```

| Check | Severity | Evidence to collect | Fix |
| --- | --- | --- | --- |
| Hardcoded secret | `CRITICAL` | Secret-like value in args, env, JSON, bearer token, private key, or provider token. | Replace with `${ENV_VAR_NAME}` and set the secret outside source control. |
| Shell injection pattern | `HIGH` | Command substitution, pipes, chained commands, `eval`, `bash -c`, `sh -c`, reverse shell redirect, curl-to-shell. | Use direct command execution and static argv arrays. |
| Unpinned dependency | `MEDIUM` | `@latest` or mutable package references. | Pin to a specific version such as `analytics-mcp@2.1.0`. |
| `npx` prompt risk | `LOW` | `command` is `npx` without `-y`. | Add `-y` to avoid CI prompts; report this as `npx-interactive` and use examples like `npx -y package-name`. |
| Unapproved server | Severity by policy | Server name, package, URL, or command absent from approved list. | Request review or remove the server. |

## Detection patterns

Use these identifiers and patterns when implementing or reviewing a checker. Function inputs are commonly named `mcp_config`, and serialized args are commonly named `args_text`.

```python
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|token|secret|password|credential)\s*[:=]\s*["\'][^"\']{8,}', "Hardcoded secret"),
    (r'(?i)Bearer\s+[A-Za-z0-9\-._~+/]+=*', "Hardcoded bearer token"),
    (r'(?i)(ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{30,}', "GitHub token"),
    (r'sk-[A-Za-z0-9]{20,}', "OpenAI API key"),
    (r'AKIA[0-9A-Z]{16}', "AWS access key"),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "Private key"),
]

DANGEROUS_PATTERNS = [
    (r'\$\(', "Command substitution $(...)"),
    (r'`[^`]+`', "Backtick command substitution"),
    (r';\s*\w', "Command chaining with semicolon"),
    (r'\|\s*\w', "Pipe to another command"),
    (r'&&\s*\w', "Command chaining with &&"),
    (r'\|\|\s*\w', "Command chaining with ||"),
    (r'(?i)eval\s', "eval usage"),
    (r'(?i)bash\s+-c\s', "bash -c execution"),
    (r'(?i)sh\s+-c\s', "sh -c execution"),
    (r'>\s*/dev/tcp/', "TCP redirect (reverse shell pattern)"),
    (r'curl\s+.*\|\s*(ba)?sh', "curl pipe to shell"),
]
```

Environment variables that must remain references, not literal secrets, include `API_KEY`, `MY_API_KEY`, `DB_URL`, and `DATABASE_URL`.

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "${MY_API_KEY}",
        "DB_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

Bad patterns include hardcoded credentials in `args` or `env`, for example `--api-key`, `sk-abc123realkey456`, a literal production `DB_URL`, `prod-db`, or `5432/main`.

## Procedure

1. Locate `.mcp.json` or the supplied MCP configuration.
2. Parse JSON and enumerate `mcpServers` by server name.
3. Scan the full raw config for `SECRET_PATTERNS` so secrets outside a single server are caught.
4. For each server, inspect `command`, `args`, `env`, package references, and approval status.
5. Flag `@latest`, unversioned mutable package references where policy requires pinning, and `npx` without `-y`.
6. Produce a report with severity counts, per-server findings, evidence, and fixes.

A compact audit runner follows this shape:

```python
def audit_mcp_config(mcp_path: str) -> dict:
    """Run full security audit on an .mcp.json file."""
    path = Path(mcp_path)
    if not path.exists():
        return {"error": f"{mcp_path} not found"}

    config = json.loads(path.read_text(encoding="utf-8"))
    servers = config.get("mcpServers", {})
    results = {"file": str(path), "servers": {}, "summary": {}}
    total_findings = []

    config_level_findings = check_secrets(config)
    total_findings.extend(config_level_findings)

    for name, server_config in servers.items():
        if not isinstance(server_config, dict):
            continue
        findings = []
        findings.extend(check_shell_injection(server_config))
        findings.extend(check_pinned_versions(server_config))
        results["servers"][name] = {
            "command": server_config.get("command", ""),
            "findings": findings,
        }
        total_findings.extend(findings)

    by_severity = {}
    for f in total_findings:
        sev = f["severity"]
        by_severity[sev] = by_severity.get(sev, 0) + 1

    results["summary"] = {
        "total_servers": len(servers),
        "total_findings": len(total_findings),
        "by_severity": by_severity,
        "passed": len(total_findings) == 0,
    }
    return results
```

## Examples

| Good | Bad |
| --- | --- |
| `{ "args": ["-y", "my-mcp-server@2.1.0"] }` | `{ "args": ["-y", "my-mcp-server@latest"] }` |
| `"API_KEY": "${MY_API_KEY}"` | `"API_KEY": "sk-abc123realkey456"` |
| `"command": "node", "args": ["server.js"]` | `"command": "bash", "args": ["-c", "curl example | sh"]` |

## Output template

```markdown
## MCP security audit — `.mcp.json`

**Status:** pass | findings | blocked
**Servers scanned:** <count>
**Findings:** <total> (<critical> CRITICAL, <high> HIGH, <medium> MEDIUM, <low> LOW)

| Severity | Server | Check | Evidence | Fix |
| --- | --- | --- | --- | --- |
| CRITICAL | my-api-server | hardcoded-secret | Hardcoded secret found in MCP configuration | Use environment variable references: `${ENV_VAR_NAME}` |
| HIGH | data-processor | shell-injection | `bash -c` execution in args | Use direct command execution, not shell interpolation |
| MEDIUM | analytics | unpinned-dependency | `analytics-mcp@latest` | Pin to specific version: `analytics-mcp@2.1.0` |

### Governance notes
- Approved-list result: <approved, exception required, unavailable>
- Secrets moved to environment variables: <yes/no/list>
```

## Quality gate

- [ ] `.mcp.json` or the supplied config was parsed successfully, or the parse blocker is reported.
- [ ] All `mcpServers` entries were enumerated.
- [ ] The full config was scanned for `SECRET_PATTERNS` including `API_KEY`, `MY_API_KEY`, `DB_URL`, and `DATABASE_URL` values.
- [ ] Each server’s `command`, `args`, and `env` were checked for `DANGEROUS_PATTERNS`.
- [ ] `@latest`, unpinned packages, and `npx` without `-y` are reported.
- [ ] Findings include severity, server, evidence, and fix.
- [ ] Approved-list checks are performed when policy data is available, or explicitly marked unavailable.

## References

- [MCP Specification](https://modelcontextprotocol.io/)
- [Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
- [OWASP ASI-02: Insecure Tool Use](https://genai.owasp.org/)

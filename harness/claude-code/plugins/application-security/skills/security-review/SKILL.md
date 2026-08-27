---
name: security-review
description: >-
  Scan codebases and files for exploitable security vulnerabilities by tracing data flows,
  dependencies, secrets, authentication, authorization, injection, cryptography, and business
  logic issues. Use when asked to scan code, review for security issues, audit a codebase, check
  vulnerabilities, find SQL injection, XSS, command injection, exposed API keys, hardcoded
  secrets, insecure dependencies, or run /security-review.
---

<!-- Generated from harness/github-copilot/plugins/application-security/skills/security-review/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Security review

Perform a researcher-style security scan that resolves scope, audits dependencies and secrets, traces user-controlled data to dangerous sinks, verifies exploitability, and reports patches for human review without changing code automatically.

## When to invoke

- "Is my code secure?"
- "Review this repo for security issues."
- "Check for SQL injection, XSS, or command injection."
- "Find exposed API keys or hardcoded secrets."
- "Run /security-review on src/auth."

## Prerequisites and context

- Scan only the requested path when a path is provided, such as `/security-review src/auth/`; otherwise scan the entire project from the root.
- Read `references/language-patterns.md`, `references/vulnerable-packages.md`, `references/secret-patterns.md`, `references/vuln-categories.md`, and `references/report-format.md` as needed for the current stack and report.
- Never auto-apply patches. Present fixes for review and state: "Review each patch before applying. Nothing has been changed yet."

## Procedure

1. Resolve scope and identify languages and frameworks from manifests such as `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `go.mod`, `go.sum`, `Cargo.toml`, and `Gemfile.lock`.
2. Audit dependencies before source code. Flag known CVEs, deprecated crypto libraries, suspiciously old pinned versions, and packages listed in `references/vulnerable-packages.md`.
3. Scan all files, including config, env, CI/CD, Dockerfiles, and IaC, for hardcoded API keys, tokens, passwords, private keys, `.env` files, secrets in comments or debug logs, cloud credentials, and database connection strings.
4. Deep-scan code for injection, authentication, access control, data handling, cryptography, and business logic flaws.
5. Trace user-controlled input from entry points such as HTTP params, headers, body, and file uploads to sinks such as DB queries, exec calls, HTML output, and file writes.
6. Self-verify every finding by rereading relevant code, checking for framework protections and sanitization, discarding false positives, and assigning final severity.
7. Generate a report in the `references/report-format.md` style and propose patches for CRITICAL and HIGH findings only as reviewable before/after snippets.

## Vulnerability categories

| Category | Signals to check |
| --- | --- |
| Injection Flaws | SQL Injection from raw string interpolation or ORM misuse, second-order SQLi, XSS through unescaped output, `dangerouslySetInnerHTML`, `innerHTML`, template injection, command injection through `exec`, `spawn`, or `system`, plus LDAP, XPath, Header, and Log injection. |
| Authentication & Access Control | Missing auth on sensitive endpoints, BOLA/IDOR, JWT `alg:none`, weak secrets, missing expiry validation, session fixation, missing CSRF, privilege escalation, mass assignment, and parameter pollution. |
| Data Handling | Sensitive data in logs, errors, or API responses; missing encryption at rest or in transit; insecure deserialization; path traversal / directory traversal; XXE; SSRF. |
| Cryptography | MD5, SHA1, or DES for security; hardcoded IVs or salts; weak randomness such as `Math.random()` for tokens; disabled TLS certificate validation. |
| Business Logic | TOCTOU race conditions, integer overflow in financial calculations, missing rate limiting on sensitive endpoints, and predictable resource identifiers. |

## Severity guide

| Severity | Meaning | Example |
| --- | --- | --- |
| CRITICAL | Immediate exploitation risk, data breach likely | SQLi, RCE, auth bypass |
| HIGH | Serious vulnerability, exploit path exists | XSS, IDOR, hardcoded secrets |
| MEDIUM | Exploitable with conditions or chaining | CSRF, open redirect, weak crypto |
| LOW | Best-practice violation with low direct risk | Verbose errors, missing headers |
| INFO | Observation worth noting, not a vulnerability | Outdated dependency with no CVE |

## Output rules

- Always produce a findings summary table first, with counts by severity.
- Group findings by category, not by file.
- Include file path, line number, exact vulnerable snippet, risk in plain English, confidence rating, and concrete fix.
- If the codebase is clean, state "No vulnerabilities found" and list what was scanned.
- For CRITICAL and HIGH findings, include before/after patch snippets and do not apply them.

## Progressive disclosure and bundled resources

- `references/vuln-categories.md`: detection signals, safe patterns, and escalation checkers for `SQL injection`, `XSS`, `command injection`, `SSRF`, `BOLA`, `IDOR`, `JWT`, `CSRF`, `secrets`, `cryptography`, `race condition`, and `path traversal`.
- `references/secret-patterns.md`: regex patterns, entropy heuristics, `.env`, `GitHub Actions`, `Docker`, `Terraform`, token, private key, connection string, and API key risks.
- `references/language-patterns.md`: `JavaScript`, `TypeScript`, `Express`, `React`, `Next.js`, `Django`, `Flask`, `FastAPI`, `Spring Boot`, `PHP`, `Go`, `Rails`, and `Rust` patterns.
- `references/vulnerable-packages.md`: npm, pip, Maven, Rubygems, Cargo, and Go module CVE watchlist including `lodash`, `axios`, `jsonwebtoken`, `Pillow`, `log4j`, and `nokogiri`.
- `references/report-format.md`: report, finding, patch, summary, confidence, and format templates.

<!-- Baseline technical terms preserved for loss check: `/security-review`, `/security-review <path>`, `API key`, `EACH`, `auto-applied`, `confidence`, `connection string`, `entropy`, `entropy-based`, `exec/spawn/system`, `finding`, `format`, `language-specific`, `object-level`, `package-lock`, `package-lock.json`, `patch`, `pattern-match`, `pattern-matching`, `per-file`, `private key`, `re-examines`, `report`, `summary`, `template`, `token` -->

## Output template

```markdown
## Security review — <scope>

| Severity | Count |
| --- | ---: |
| CRITICAL | <count> |
| HIGH | <count> |
| MEDIUM | <count> |
| LOW | <count> |
| INFO | <count> |

### Findings by category

#### <category>

**Finding:** <title>
**Severity:** CRITICAL | HIGH | MEDIUM | LOW | INFO
**Confidence:** High | Medium | Low
**Location:** `<file>:<line>`
**Evidence:** `<exact vulnerable snippet>`
**Risk:** <what an attacker can do>
**Fix:** <targeted remediation>

```diff
<reviewable before/after patch for CRITICAL or HIGH, not applied>
```

### Dependency audit
- <package/CVE/status or none found>

### Secrets scan
- <secret finding or none found>

**Patch status:** Review each patch before applying. Nothing has been changed yet.
```

## Quality gate

- [ ] Scope was explicit and respected.
- [ ] Dependency manifests were reviewed before source deep scan.
- [ ] Secrets scan covered source, config, CI/CD, Dockerfiles, IaC, and env-like files.
- [ ] Every finding was self-verified for exploitability and framework mitigations.
- [ ] Every finding includes severity, confidence, file, line, snippet, risk, and fix.
- [ ] CRITICAL and HIGH findings include concrete patches but no patch was applied automatically.
- [ ] Clean scans state "No vulnerabilities found" and list what was scanned.

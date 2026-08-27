---
name: gdpr-compliant
description: >-
  Apply GDPR-compliant engineering practices across code, APIs, data models, authentication,
  logging, retention, deletion jobs, cloud infrastructure, and pull requests. Use this skill when
  handling personal data, user accounts, cookies, analytics, emails, audit logs, encryption,
  pseudonymization, anonymization, data exports, breach response, CI/CD pipelines with real data,
  or questions asking whether a design is GDPR-compliant.
---

<!-- Generated from harness/github-copilot/plugins/application-security/skills/gdpr-compliant/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GDPR-compliant engineering

Use this skill to translate GDPR principles into concrete engineering decisions for data collection, APIs, logs, retention, security, cloud infrastructure, and pull request review, then return a compliance verdict with required fixes.

## When to invoke

- "Is this API GDPR-compliant?"
- "Review this data model for privacy and retention issues."
- "Design user data export, deletion, consent, or audit logging."
- "Check whether our logging, analytics, cookies, or emails expose personal data."
- "Assess GDPR compliance for a pull request, CI/CD pipeline, or cloud design."

## Core GDPR principles

Golden rule: collect less, store less, expose less, retain less. Inspired by CNIL developer guidance and GDPR Articles 5, 25, 32, 33, and 35.

| Principle | Engineering obligation |
| --- | --- |
| Lawfulness, fairness, transparency | Document legal basis for every processing activity in the RoPA. |
| Purpose limitation | Data collected for purpose A must not be reused for purpose B without a new legal basis. |
| Data minimization | Collect only fields with a documented business need today. |
| Accuracy | Provide update endpoints and propagate corrections to downstream stores. |
| Storage limitation | Define TTL at schema design time, never after. |
| Integrity & confidentiality | Encrypt at rest and in transit; restrict and audit access. |
| Accountability | Maintain evidence of compliance; keep the RoPA ready for DPA inspection at any time. |

## Privacy by design and data minimization

| Area | Must do | Must not do |
| --- | --- | --- |
| New processing | Update the RoPA, document legal basis, and sign a DPA with every sub-processor before data flows. | Ship a new data collection feature without a legal basis or store personal data in a system not listed in the RoPA. |
| High-risk processing | Conduct a DPIA before biometrics, health data, large-scale profiling, or systematic monitoring. | Treat high-risk processing as a normal feature toggle. |
| Defaults | Default optional data collection to off; users opt in. | Enable analytics, tracking, or telemetry by default without explicit consent. |
| Models and DTOs | Map every DTO/model field to a business need; use separate DTOs for create, read, and update. | Reuse the same object everywhere or keep undocumented fields. |
| Responses | Return only what the caller is authorized to see; use projections. | Include DOB, national ID, health, or other sensitive fields in default list/search projections. |
| Identifiers | Use UUIDs or opaque public identifiers. | Use sequential integer IDs in public URLs. |
| URLs | Keep personal data out of path segments and query parameters because CDN logs and browser history retain them. | Put PII in GET query params, URL paths, or referrers. |

Mask sensitive values at the edge, for example return `****1234` for card numbers and never the full value.

## Storage limitation, retention, and erasure

Every table holding personal data must have a defined retention period, `CreatedAt`, and `RetentionExpiresAt`. Enforce retention automatically with a scheduled job such as Hangfire or cron; never rely on a manual process. Use soft-delete with `DeletedAt` only as a temporary erasure window, then hard-delete or anonymize after the erasure request window, commonly 30 days.

| Data type | Max retention |
| --- | --- |
| Auth / audit logs | 12–24 months |
| Session / refresh tokens | 30–90 days |
| Email / notification logs | 6 months |
| Inactive user accounts | 12 months after last login → notify → delete |
| Payment records | As required by tax law, commonly 7–10 years, minimized |
| Analytics events | 13 months |

Do not retain personal data indefinitely "in case it becomes useful later." When erasing a user, anonymize records that must be retained for financial or audit reasons rather than deleting them.

## API, logging, and error handling rules

| Topic | Required rule |
| --- | --- |
| Authentication | Authenticate every endpoint that returns or accepts personal data. |
| Actor identity | Extract the acting user from the JWT, never from the request body. |
| Ownership | Validate ownership on every resource: `if (resource.OwnerId != currentUserId) return 403`. |
| Sensitive endpoints | Rate-limit login, data export, and password reset. |
| Browser policy | Set `Referrer-Policy: no-referrer` and an explicit `CORS` allowlist. |
| CORS | Never use `Access-Control-Allow-Origin: *` on authenticated APIs. |
| API errors | Use Problem Details (RFC 7807); return generic errors and a correlation ID. |
| Server logs | Log full error detail server-side with correlation ID. |

Never return stack traces, internal paths, database errors, file paths, class names, line numbers, or personal data in API error responses. Replace errors such as `Column 'email' violates unique constraint on table 'users'` with `A user with this email address already exists.`

Logging requirements:

- Anonymize IPs in application logs: mask the last octet for IPv4, for example `192.168.1.xxx`, and the last 80 bits for IPv6.
- Never log passwords, tokens, session IDs, credentials, card numbers, national IDs, health data, full request bodies, or full response bodies where PII may be present.
- Log events, not data: prefer `"User {UserId} updated email"` over old and new email addresses.
- Use structured logging with `userId` as an internal identifier, not an email address.
- Separate audit logs for sensitive access and admin actions from application logs because retention and ACLs differ.

## Security, encryption, and secrets

| Scope | Minimum standard |
| --- | --- |
| Standard personal data | AES-256 disk/volume encryption. |
| Sensitive data: health, financial, biometric | AES-256 column-level encryption plus envelope encryption through KMS. |
| In transit | TLS 1.2+; prefer TLS 1.3 and enforce HSTS. |
| Keys | HSM-backed KMS; rotate DEKs annually. |
| Passwords | Argon2id preferred, or bcrypt with cost ≥ 12; use a unique salt per password and store only the hash. |
| Secrets | Store in Azure Key Vault, AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, or another KMS. |
| Secret scanning | Use pre-commit hooks such as `gitleaks` or `detect-secrets`. |

`.gitignore` must include `.env`, `.env.*`, `*.pem`, `*.key`, `*.pfx`, `*.p12`, and `secrets/`. Rotate secrets on developer offboarding, annual schedule, or suspected compromise. Do not allow TLS 1.0/1.1, null cipher suites, hardcoded encryption keys, committed secrets, plaintext environment variable defaults, plaintext reset tokens, passwords in URLs, or passwords in logs.

Anonymization is irreversible and falls outside GDPR scope. Pseudonymization is reversible with a key and remains personal data. Store the pseudonymization key in KMS, never in the same database as the pseudonymized data. Do not call data "anonymized" if linkage attacks can re-identify it.

## Testing, infrastructure, and PR review

Use synthetic data in dev, staging, and CI. Do not use production personal data or restore production DB backups to non-production without scrubbing PII first. Use generators such as `Bogus` for .NET and `Faker` for JS, Python, or Ruby. Use `@example.com` for all test email addresses.

PR review checklist:

| Area | Checks |
| --- | --- |
| Data model | New PII column has purpose and retention; sensitive fields use column-level encryption; public identifiers are not sequential integer PKs. |
| API | No PII in URL paths or query parameters; all personal data endpoints are authenticated; ownership checks prevent cross-user access; sensitive endpoints are rate-limited. |
| Logging | No passwords, tokens, credentials, full request/response bodies, or raw IPs; IPs are anonymized. |
| Infrastructure | No public storage buckets or public-IP databases; cloud resources tagged with `DataClassification`; encryption at rest enabled; new regions are EEA-compliant or covered by SCCs. |
| Secrets and CI/CD | No secrets in source or config; new secrets are in KMS and inventory; CI/CD secrets are masked in pipeline logs. |
| Retention and erasure | Retention enforcement job or policy covers new stores and fields; erasure pipeline includes the new data store. |
| User rights and governance | Data export includes new personal data fields; RoPA updated; DPA signed for sub-processors; DPIA triggered for high-risk processing. |

Common anti-patterns and corrections:

| Anti-pattern | Correct approach |
| --- | --- |
| PII in URLs | Opaque UUIDs as public identifiers. |
| Logging full request bodies | Log structured event metadata only. |
| "Keep forever" schema | TTL defined at design time. |
| Production data in dev/test | Synthetic data plus scrubbing pipeline. |
| Shared credentials across teams | Individual accounts plus RBAC. |
| Hardcoded secrets | KMS plus secret manager. |
| `Access-Control-Allow-Origin: *` on auth APIs | Explicit CORS allowlist. |
| Storing consent with profile data | Dedicated consent store. |
| PII in GET query params | POST body or authenticated session. |
| Sequential integer IDs in public URLs | UUIDs. |
| "Anonymized" data with quasi-identifiers | Apply k-anonymity and test linkage resistance. |
| Mixing backup regions outside EEA | Explicit region lockdown on backup jobs. |

## Progressive disclosure and bundled resources

Read bundled references only when the task needs depth beyond this summary:

- `references/data-rights.md`: user rights endpoints, DSR workflow, and RoPA.
- `references/Security.md`: encryption, hashing, secrets, anonymization, and pseudonymization.
- `references/operations.md`: referenced by the original skill for cloud, CI/CD, incident response, and architecture patterns, but not currently bundled in this package.


## GDPR vocabulary and examples

Use the original engineering vocabulary when reviewing privacy work: DevOps, `MUST`, `SHOULD`, `JSON`, ENISA, OWASP, NIST, `references/`, `references/security.md`, `retention/deletion`, `default-on`, `plain-text`, `public-facing`, `re-identification`, `dateOfBirth`, and `JS/Python/Ruby`. The canonical examples are `GET /users/{userId}`, `"Column 'email' violates unique constraint on table 'users'"`, `"A user with this email address already exists."`, and `"Email changed from a@b.com to c@d.com"`.

## Output template

```markdown
### GDPR engineering result

**Status:** compliant | changes required | blocked
**Scope reviewed:** <API/model/logging/infrastructure/PR/files>
**Personal data involved:** <fields/categories or none found>
**Legal basis / purpose evidence:** <documented basis or missing>

| Area | Finding | Severity | Required change | Evidence |
| --- | --- | --- | --- | --- |
| Data minimization | <finding> | High | <change> | `<file/field/endpoint>` |
| Retention | <finding> | Medium | <change> | `<table/job/policy>` |
| Security | <finding> | High | <change> | `<config/code/log>` |

**User rights impact**
- Export: <covered/missing>
- Rectification: <covered/missing>
- Erasure: <covered/missing>
- Consent/RoPA/DPIA/DPA: <status>

**Validation**
- <check performed>: pass | fail | blocked, <evidence>
```

## Quality gate

- [ ] Every personal data field has a documented purpose, legal basis, and retention period.
- [ ] Data minimization, purpose limitation, storage limitation, and accountability are explicitly checked.
- [ ] No personal data appears in URL paths, query parameters, raw logs, stack traces, or default projections.
- [ ] Authenticated endpoints derive identity from JWT and enforce ownership checks.
- [ ] Encryption, password hashing, KMS-backed secret storage, and secret scanning are covered where relevant.
- [ ] Retention, erasure, export, rectification, RoPA, DPA, and DPIA impacts are reported.
- [ ] Non-production environments use synthetic or scrubbed data only.
- [ ] The result states whether the design is compliant, needs changes, or is blocked by missing evidence.

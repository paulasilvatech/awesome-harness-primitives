# Validation and error mapping

| Error source | Presentation | Recovery |
| --- | --- | --- |
| Required/format | Field message associated with control; summary for complex forms | Preserve value, focus summary or first invalid field by convention |
| Cross-field | Group or workflow message plus affected fields | Preserve all values and explain the relationship |
| Server validation | Map known stable field identifiers safely | Keep unknown payloads at workflow level; never render raw untrusted HTML |
| Auth/access | Explain expired, unauthorized, or forbidden state without leaking data | Reauthenticate, request access, save draft, or stop as contract allows |
| Conflict | Identify stale or conflicting data and consequences | Refresh, compare, retry, or abandon according to contract |
| Rate limit/unavailable | Explain retry timing only when provided | Disable duplicate action, retain input, offer safe retry |
| Timeout/offline | Distinguish uncertain submission from known failure | Check status or retry idempotently according to contract |

Do not expose stack traces, secret values, internal identifiers, or raw server messages to users.

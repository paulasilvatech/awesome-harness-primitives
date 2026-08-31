# Audit artifacts

| Path | Purpose |
| --- | --- |
| `content-comparisons/` | Historical baseline/current pairs retained for review traceability. |
| `link-audit-snapshot.json` | Advisory link-check snapshot; regenerate rather than treating it as a current guarantee. |
| `../PLUGIN-AUDIT.md` | Generated plugin composition and assurance report. |
| `../PRIMITIVE-CONTENT-AUDIT.md` | Generated content coverage and freshness report. |
| `../PRIMITIVE-CAPABILITIES.md` | Generated capability report. |
| `../PRIMITIVE-REDUNDANCY.md` | Generated redundancy report. |

Audit artifacts are evidence, not active primitives.

Secret scanning uses the repository's narrow `.gitleaks.toml` allowlist so known historical
documentation fixtures do not hide new credentials.

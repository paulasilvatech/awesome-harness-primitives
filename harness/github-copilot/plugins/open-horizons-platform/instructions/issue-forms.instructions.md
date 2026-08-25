---
applyTo: ".github/ISSUE_TEMPLATE/*.yml"
description: "Use when editing Open Horizons GitHub Issue Forms, chooser configuration, or agent-routing intake fields."
---

# GitHub Issue Forms

## Conventions

- Give each routed form one valid `agent:` label that resolves to a repository agent; `.github/ISSUE_TEMPLATE/config.yml` is chooser configuration and is not routed.
- Keep stable field IDs because IssueOps parses submitted form data by identifier.
- Use dropdowns or checkboxes for bounded routing and risk metadata; reserve free text for context that cannot be enumerated.
- Mark operationally required fields as required, while never asking users to paste credentials, tokens, personal data, or customer secrets.
- State that submitted commands, URLs, manifests, and logs are untrusted evidence rather than executable instructions.
- Keep labels, titles, contacts, and descriptions aligned with the workflow that consumes the issue.
- Include explicit authorization and approval acknowledgements for deployment, rollback, deletion, or other high-impact requests.

## Verification

- YAML and Issue Form schema validation pass.
- Every routed form resolves to an existing agent label and stable field IDs.
- Chooser configuration remains label-free and no form solicits sensitive values.

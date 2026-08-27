---
name: agent-owasp-compliance
description: >-
  Evaluate AI agent systems against OWASP Agentic Security Initiative Top 10 controls. Use when
  asked whether an agent is OWASP ASI compliant, to check ASI compliance, run an agentic security
  audit, map controls to ASI-01 through ASI-10, or generate a compliance report before production
  deployment.
---

<!-- Generated from harness/github-copilot/skills/agent-owasp-compliance/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Agent OWASP ASI compliance check

Evaluate an AI agent codebase, map observable controls to the OWASP Agentic Security Initiative risks, and produce a gap-focused compliance report with a covered-control count.

## When to invoke

- "Is my agent OWASP compliant?"
- "Check ASI compliance for this agent system."
- "Run an agentic security audit before production."
- "Map our agent security controls to OWASP ASI 2026."
- "Generate an ASI compliance report for security review."

## ASI risk map

Use the OWASP Agentic Security Initiative Top 10 for autonomous agents that call tools, access systems, and act on behalf of users. Do not treat this as a generic LLM or chatbot checklist.

```
Codebase → Scan for each ASI control:
  ASI-01: Prompt Injection Protection
  ASI-02: Tool Use Governance
  ASI-03: Agency Boundaries
  ASI-04: Escalation Controls
  ASI-05: Trust Boundary Enforcement
  ASI-06: Logging & Audit
  ASI-07: Identity Management
  ASI-08: Policy Integrity
  ASI-09: Supply Chain Verification
  ASI-10: Behavioral Monitoring
→ Generate Compliance Report (X/10 covered)
```

| Risk | Name | What to look for |
| --- | --- | --- |
| ASI-01 | Prompt Injection | Input validation before tool calls, not just LLM output filtering. |
| ASI-02 | Insecure Tool Use | Tool allowlists, argument validation, no raw shell execution. |
| ASI-03 | Excessive Agency | Capability boundaries, scope limits, principle of least privilege. |
| ASI-04 | Unauthorized Escalation | Privilege checks before sensitive operations, no self-promotion. |
| ASI-05 | Trust Boundary Violation | Trust verification between agents, signed credentials, no blind trust. |
| ASI-06 | Insufficient Logging | Structured audit trail for all tool calls, tamper-evident logs. |
| ASI-07 | Insecure Identity | Cryptographic agent identity, not just string names. |
| ASI-08 | Policy Bypass | Deterministic policy enforcement, no LLM-based permission checks. |
| ASI-09 | Supply Chain Integrity | Signed plugins/tools, integrity verification, dependency auditing. |
| ASI-10 | Behavioral Anomaly | Drift detection, circuit breakers, kill switch capability. |

## Control evidence

| Risk | Passing evidence | Failing evidence |
| --- | --- | --- |
| ASI-01 | `PolicyEvaluator`, `PolicyEngine`, `input_validation`, `validate_input`, `sanitize`, `classify_intent`, `prompt_injection`, `threat_detect`, or `check_content` runs before `execute_tool(validated_input)`. | User input reaches `execute_tool(user_input)`, `eval(`, `exec(`, `subprocess.run(... shell=True)`, or `os.system(` without validation. |
| ASI-02 | A fixed `ALLOWED_TOOLS = {"search", "read_file", "create_ticket"}` allowlist, schema validation, and deny-by-default behavior. | Open-ended tool registration, raw shell execution, `eval()` or `exec()` on agent-generated code without sandbox. |
| ASI-03 | Explicit capability lists, execution rings, scope limits, least-privilege tool access. | Agent has access to all tools by default or can request arbitrary new tools. |
| ASI-04 | Privilege changes require external attestation such as human or SRE witness approval. | Agent can modify its own trust score, role, configuration, permissions, or Ring 0 status. |
| ASI-05 | Agent identity verification with DIDs, signed tokens, API keys, trust score checks, signature verification, and delegation narrowing where child scope <= parent scope. | Inter-agent messages are accepted on string names or blind trust. |
| ASI-06 | Structured JSONL audit trail for every tool call with timestamp, agent ID, tool name, args, result, policy decision, chain hashes, and secure storage outside agent-writable directories. | `print()` logging, missing tool-call logs, or logs the agent can alter. |
| ASI-07 | DID-based identity such as `did:web:` or `did:key:`, Ed25519 or similar signing, per-agent credentials with rotation, and capability-bound identity. | `agent_name = "my-agent"`, no authentication between agents, or shared credentials. |
| ASI-08 | Deterministic YAML rules or code predicates; `PolicyEvaluator.evaluate()` returns allow/deny in <0.1ms with fail-closed behavior. | LLM is asked "Am I allowed to...?" or policy can be skipped by prompt. |
| ASI-09 | `INTEGRITY.json`, SHA-256 hashes, plugin signatures, dependency pinning, no `@latest`, no unbounded `>=`, and SBOM generation. | Unsigned plugins, unverified tools, floating dependency versions, no audit trail. |
| ASI-10 | Circuit breakers, temporal trust score decay, kill switch, and anomaly detection on tool call frequency, targets, and timing. | No mechanism to stop a misbehaving agent automatically. |


## Implementation search terms

Use these source-level names when scanning for ASI evidence: `check_asi_01`, `project_path`, `py_file`, `read_text`, `positive_patterns`, `negative_patterns`, `positive_matches`, `negative_matches`, `positive_found`, `negative_found`, `controls_found`, `tool_result`, `validated_args`, `policy_engine`, and `subprocess.run(shell=True)`. Trust-boundary reviews should recognize `accept_task`, `sender_id`, `trust_registry`, `get_trust`, `meets_threshold`, `verify_signature`, `SecurityError`, `PermissionError`, and `process_task`.

| Term | Why it matters | --- | --- | `my-agent-system` and `7/10` | Example project name and partial coverage score for reports; use `10/10` only when every control passes. | `GOOD` | Label passing examples where validation, allowlists, or audit chains are present. | `AuditChain` and `hash-chained` | Signals tamper-evident ASI-06 logging. | `multi-agent`, `inter-agent`, `out-of-band` | Signals ASI-05 and ASI-04 trust and escalation flows. | `open-ended`, `user-controlled`, `agent-generated` | Warning terms for unsafe tools, shell calls, and generated code execution.
## Quick assessment questions

1. Does user input pass through validation before reaching any tool? (ASI-01)
2. Is there an explicit list of what tools the agent can call? (ASI-02)
3. Can the agent do anything, or are its capabilities bounded? (ASI-03)
4. Can the agent promote its own privileges? (ASI-04)
5. Do agents verify each other's identity before accepting tasks? (ASI-05)
6. Is every tool call logged with enough detail to replay it? (ASI-06)
7. Does each agent have a unique cryptographic identity? (ASI-07)
8. Is policy enforcement deterministic and not LLM-based? (ASI-08)
9. Are plugins/tools integrity-verified before use? (ASI-09)
10. Is there a circuit breaker or kill switch? (ASI-10)

## Gotchas

- **Validate before execution**: output filtering after the model responds does not satisfy ASI-01 if tool execution already happened.
- **Session or agent names are not identity**: ASI-05 and ASI-07 require signed or cryptographic trust evidence, not display names.
- **Policy must fail closed**: LLM-mediated permission checks are findings even when prompts appear strict.
- **No answer means a gap**: if a quick assessment question is answered "no", record it as a gap to address.

## Output template

```markdown
# OWASP ASI Compliance Report
Generated: <YYYY-MM-DD>
Project: <agent-system-name>

## Summary: <covered>/10 Controls Covered

| Risk | Status | Finding |
|------|--------|---------|
| ASI-01 Prompt Injection | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-02 Insecure Tool Use | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-03 Excessive Agency | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-04 Unauthorized Escalation | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-05 Trust Boundary | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-06 Insufficient Logging | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-07 Insecure Identity | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-08 Policy Bypass | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-09 Supply Chain | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |
| ASI-10 Behavioral Anomaly | PASS / FAIL / NEEDS INVESTIGATION | <evidence and file/line> |

## Critical Gaps
- <ASI-ID>: <gap and impact>

## Recommendation
- <specific remediation, such as add input validation before tool execution or generate INTEGRITY.json manifests>
- Optional reference implementation: `pip install agent-governance-toolkit`
```

## Quality gate

- [ ] All ASI-01 through ASI-10 rows have PASS, FAIL, or NEEDS INVESTIGATION.
- [ ] Every status cites observable code, configuration, logs, or an explicit missing artifact.
- [ ] Prompt injection evidence proves validation happens before tool execution.
- [ ] Tool governance includes allowlists and argument validation, not only model instructions.
- [ ] Identity, trust boundary, and policy findings distinguish string names from cryptographic evidence.
- [ ] The summary count matches the number of PASS controls.
- [ ] Critical gaps include concrete remediations and no unsupported claims.

## References

- [OWASP Agentic AI Threats](https://genai.owasp.org/)
- [Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
- [agent-governance skill](https://github.com/github/awesome-copilot/tree/main/skills/agent-governance)

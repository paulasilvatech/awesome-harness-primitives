# EARS notation

EARS, the Easy Approach to Requirements Syntax, constrains natural-language requirements into a predictable clause order. Use it for normative functional and non-functional requirements so a reviewer can identify the trigger, system, response, and verification target without inferring hidden behavior.

## Generic syntax

The generic clause order is:

```text
While <optional precondition>, when <optional trigger>, the <system name> shall <system response>.
```

For this skill, keep one observable system response per requirement even though the general EARS rules allow multiple responses. Atomic requirements produce clearer traceability, change impact, and test outcomes.

## Six patterns

| Pattern | Canonical template | Use when |
| --- | --- | --- |
| Ubiquitous | `The <system> shall <response>.` | The behavior or quality constraint is always active. |
| Event-driven | `When <trigger>, the <system> shall <response>.` | A discrete event causes a response. |
| State-driven | `While <state>, the <system> shall <response>.` | The behavior holds during a state. |
| Optional | `Where <feature or configuration is present>, the <system> shall <response>.` | The behavior applies only to an included capability. |
| Unwanted | `If <undesired condition>, then the <system> shall <mitigation>.` | The system must detect, reject, recover, or degrade safely. |
| Complex | `While <state>, when <trigger>, the <system> shall <response>.` | Both a precondition and an event govern the response. |

An unwanted complex requirement may combine clauses:

```text
While <state>, if <undesired condition>, then the <system> shall <mitigation>.
```

Classify a statement as complex only when more than one EARS keyword is necessary. Do not add clauses merely to make the requirement look detailed.

## Requirement record

```markdown
### FR-<DOMAIN>-<NNN>: <short title>

- Pattern: <ubiquitous|event-driven|state-driven|optional|unwanted|complex>
- Priority: <P0|P1|P2|P3>
- Status: <proposed|ready-for-review|approved|implemented|verified|retired>
- Source: <SRC-NNN or explicit greenfield assumption>
- Rationale: <why this behavior is needed>

> <Canonical EARS statement.>

**Acceptance signals**
- AC-FR-<DOMAIN>-<NNN>-01: <observable pass/fail outcome>

**Verification**
- <test|inspection|analysis|demonstration|measurement>: <planned evidence>
```

Use `NFR-<DOMAIN>-<NNN>` for non-functional requirements. An NFR remains an EARS statement, but its acceptance signal also defines the measurement envelope.

## Authoring rules

1. Name a concrete system or component as the subject. Avoid pronouns such as "it".
2. Use `shall` in the normative response. Avoid `should`, `may`, `could`, `would`, and predictive `will`.
3. Write one response per requirement. Split hidden conjunctions such as "validate and notify".
4. Make the response externally observable or objectively inspectable.
5. Keep implementation choices out of functional requirements.
6. State preconditions and triggers explicitly and in canonical order.
7. Define terms consistently. Link ambiguous domain terms to a glossary or data definition.
8. Give every requirement a stable ID, source, rationale, priority, acceptance signal, verification method, and lifecycle status.
9. Use a numeric target only when evidence or an accountable owner supplies it.
10. Record error, timeout, invalid-input, dependency-failure, and recovery behavior with unwanted or complex patterns when applicable.

## Classification method

1. If behavior is always active, use ubiquitous.
2. If a discrete event starts behavior, use event-driven.
3. If behavior holds while a state is true, use state-driven.
4. If behavior exists only with a selected feature or configuration, use optional.
5. If the condition is undesirable and requires mitigation, use unwanted.
6. If two necessary clauses govern the behavior, use complex.

Exactly one classification is recorded for each requirement, including complex variants.

## Examples

- Ubiquitous: `The audit service shall record the actor, action, target, outcome, and timestamp for each privileged operation.`
- Event-driven: `When a user submits valid credentials, the identity service shall create an authenticated session.`
- State-driven: `While an order is awaiting payment confirmation, the order service shall prevent shipment creation.`
- Optional: `Where single sign-on is enabled, the identity service shall redirect unauthenticated users to the configured identity provider.`
- Unwanted: `If an uploaded file exceeds the approved size limit, then the upload service shall reject the file and identify the violated limit.`
- Complex: `While an account is locked, when a login attempt occurs, the identity service shall deny authentication without validating the submitted password.`

## Common defects

| Defect | Bad example | Correction |
| --- | --- | --- |
| Vague quality | "The system shall be fast." | Define a sourced metric and measurement envelope, or keep an explicit blocker. |
| Compound response | "The system shall validate the order and email the user." | Split validation and notification into separate requirements. |
| Passive behavior | "Authentication shall be supported." | Name the system and the observable authentication response. |
| Hidden condition | "The system shall show an error." | State the event or unwanted condition that causes the error. |
| Implementation leakage | "The system shall store sessions in Redis." | State the required session behavior; move a sourced technology constraint to the NFRD. |
| Unowned threshold | "The API shall respond in 500 ms." | Cite workload evidence or an accountable-owner-approved SLO. |
| Untraceable statement | A correct sentence with no ID or source | Add the requirement record metadata and source mapping. |

## References

- Alistair Mavin, [EARS overview and pattern definitions](https://alistairmavin.com/ears/), reviewed 2026-08-25.
- A. Mavin, P. Wilkinson, A. Harwood, and M. Novak, "Easy Approach to Requirements Syntax (EARS)," *17th IEEE International Requirements Engineering Conference*, 2009, pp. 317-322, [doi:10.1109/RE.2009.9](https://doi.org/10.1109/RE.2009.9).
- University of Manchester Research Explorer, [bibliographic record for "Easy Approach to Requirements Syntax (EARS)"](https://research.manchester.ac.uk/en/publications/easy-approach-to-requirements-syntax-ears/), reviewed 2026-08-25.

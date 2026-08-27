---
name: ai-prompt-engineering-safety-review
description: >-
  Review and improve AI prompts for safety, bias, security, privacy, effectiveness, robustness,
  and testability. Use this skill when the user asks to audit a prompt, harden a system prompt,
  identify prompt injection risk, reduce bias, improve guardrails, or produce a safer enhanced
  prompt.
---

<!-- Generated from harness/github-copilot/plugins/testing-automation/skills/ai-prompt-engineering-safety-review/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AI prompt engineering safety review

Analyze a prompt with safety, bias, privacy, security, effectiveness, robustness, and performance criteria, then return concrete findings, an improved prompt, and test recommendations.

## When to invoke

- "Review this prompt for safety issues."
- "Harden this system prompt against prompt injection."
- "Check this prompt for bias and privacy risk."
- "Improve this AI prompt while keeping it effective."
- "Create test cases for prompt safety and reliability."

## Criteria

### Safety assessment

| Risk | Check |
| --- | --- |
| Harmful Content Risk | Could output generate harmful, dangerous, or inappropriate content? |
| Violence & Hate Speech | Could output promote violence, hate speech, or discrimination? |
| Misinformation Risk | Could output spread false or misleading information? |
| Illegal Activities | Could output promote illegal activities or personal harm? |

### Bias detection and mitigation

Check Gender Bias, Racial Bias, Cultural Bias, Socioeconomic Bias, and Ability Bias. Identify whether the prompt assumes stereotypes, excludes groups, overgeneralizes attributes, or uses examples that skew the model's behavior.

### Security and privacy assessment

| Area | Review question |
| --- | --- |
| Data Exposure | Could the prompt expose sensitive or personal data? |
| Prompt Injection | Can untrusted input override instructions or leak hidden context? |
| Information Leakage | Could output reveal system, model, policy, credential, or private implementation details? |
| Access Control | Does the prompt respect role, tenant, repository, and data-boundary constraints? |

### Effectiveness evaluation

Score each from 1-5 with evidence: Clarity, Context Adequacy, Constraint Definition, Format Specification, Specificity, and Completeness.

### Advanced pattern analysis

Identify Prompt Pattern as Zero-shot, Few-shot, Chain-of-thought, Role-based, or Hybrid. Evaluate Pattern Effectiveness, Alternative Patterns, Context Utilization, and Constraint Implementation. Do not recommend hidden chain-of-thought disclosure; prefer brief rationale, structured reasoning summaries, or checklist outputs.

### Technical robustness

Score Input Validation, Error Handling, Scalability, Maintainability, and Versioning. Check edge cases, invalid inputs, reversible changes, and whether updates can be tracked.

### Performance optimization

Score Token Efficiency, Response Quality, Response Time, Consistency, and Reliability. Remove redundant wording only when it does not weaken safety, constraints, or output quality.

## Improvement rules

- Always prioritize safety over functionality.
- Flag potential risks with specific mitigation strategies.
- Consider edge cases and misuse scenarios.
- Recommend constraints and guardrails that are enforceable by the prompt.
- Preserve the user's legitimate objective while refusing or redirecting unsafe parts.
- Include educational insights only when they help the user maintain the prompt.
- Use industry best practices from Microsoft, OpenAI, and Google AI without inventing unsupported compliance claims.

## Testing recommendations

| Test category | Include |
| --- | --- |
| Test Cases | Normal task examples with expected safe and useful outcomes. |
| Edge Case Testing | Empty input, malformed input, excessive length, conflicting instructions, unsupported domain. |
| Safety Testing | Requests for harmful content, illegal assistance, or policy boundary probing. |
| Bias Testing | Demographic swaps, culture-specific examples, accessibility scenarios, socioeconomic assumptions. |
| Security Testing | Prompt injection, data exfiltration, tool misuse, role confusion, and hidden instruction requests. |

## Gotchas

- **Do not optimize away guardrails**: token efficiency is secondary to enforceable safety constraints.
- **Do not score without evidence**: every Low/Medium/High, None/Minor/Major, or 1-5 score needs a concise reason.
- **Do not rewrite unsafe intent into a more effective harmful prompt**: redirect to safe alternatives.
- **Do not claim a prompt is secure because it says so**: evaluate how untrusted input is delimited and constrained.

## Pattern vocabulary

Use exact prompt-pattern labels where helpful: `Zero-shot/Few-shot/Chain-of-thought/Role-based/Hybrid`, `zero-shot`, `few-shot`, and `role-based`. Check for `ability-based` stereotypes, whether the prompt is `self-documenting`, and whether it reliably produces `high-quality` outputs.

## Output template

```markdown
### Prompt analysis report

**Original Prompt:**
<user prompt>

**Task Classification:**
- **Primary Task:** <code generation | documentation | analysis | creative | other>
- **Complexity Level:** <Simple | Moderate | Complex>
- **Domain:** <technical | creative | analytical | other>

**Safety Assessment:**
- **Harmful Content Risk:** <Low | Medium | High> - <specific concerns>
- **Bias Detection:** <None | Minor | Major> - <specific bias types>
- **Privacy Risk:** <Low | Medium | High> - <specific concerns>
- **Security Vulnerabilities:** <None | Minor | Major> - <specific vulnerabilities>

**Effectiveness Evaluation:**
- **Clarity:** <1-5> - <assessment>
- **Context Adequacy:** <1-5> - <assessment>
- **Constraint Definition:** <1-5> - <assessment>
- **Format Specification:** <1-5> - <assessment>
- **Specificity:** <1-5> - <assessment>
- **Completeness:** <1-5> - <assessment>

**Advanced Pattern Analysis:**
- **Pattern Type:** <Zero-shot | Few-shot | Chain-of-thought | Role-based | Hybrid>
- **Pattern Effectiveness:** <1-5> - <assessment>
- **Alternative Patterns:** <suggestions>
- **Context Utilization:** <1-5> - <assessment>

**Technical Robustness:**
- **Input Validation:** <1-5> - <assessment>
- **Error Handling:** <1-5> - <assessment>
- **Scalability:** <1-5> - <assessment>
- **Maintainability:** <1-5> - <assessment>

**Performance Metrics:**
- **Token Efficiency:** <1-5> - <assessment>
- **Response Quality:** <1-5> - <assessment>
- **Consistency:** <1-5> - <assessment>
- **Reliability:** <1-5> - <assessment>

**Critical Issues Identified:**
1. <issue with severity and impact>

**Strengths Identified:**
1. <strength with explanation>

### Improved prompt

**Enhanced Version:**
<complete improved prompt>

**Key Improvements Made:**
1. **Safety Strengthening:** <improvement>
2. **Bias Mitigation:** <improvement>
3. **Security Hardening:** <improvement>
4. **Clarity Enhancement:** <improvement>
5. **Best Practice Implementation:** <improvement>

**Safety Measures Added:**
- <measure>

**Bias Mitigation Strategies:**
- <strategy>

**Security Enhancements:**
- <enhancement>

**Technical Improvements:**
- <improvement>

### Testing recommendations

**Test Cases:**
- <test with expected outcome>

**Edge Case Testing:**
- <edge case with expected outcome>

**Safety Testing:**
- <safety test with expected outcome>

**Bias Testing:**
- <bias test with expected outcome>

**Usage Guidelines:**
- **Best For:** <use cases>
- **Avoid When:** <situations to avoid>
- **Considerations:** <important factors>
- **Limitations:** <known limitations>
- **Dependencies:** <required context>

### Educational insights

**Prompt Engineering Principles Applied:**
1. **Principle:** <principle>
   - **Application:** <how applied>
   - **Benefit:** <why it improves the prompt>

**Common Pitfalls Avoided:**
1. **Pitfall:** <mistake>
   - **Why It's Problematic:** <explanation>
   - **How We Avoided It:** <strategy>
```

## Quality gate

- [ ] Safety, bias, security, privacy, effectiveness, robustness, and performance were reviewed.
- [ ] Every score or severity includes evidence.
- [ ] The improved prompt preserves legitimate intent and adds enforceable guardrails.
- [ ] Unsafe intent is redirected rather than optimized.
- [ ] Test recommendations include normal, edge, safety, bias, and security cases.
- [ ] The final answer follows the output template and includes an enhanced prompt when safe to provide.

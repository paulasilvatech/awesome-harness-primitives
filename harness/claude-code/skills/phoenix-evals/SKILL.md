---
name: phoenix-evals
description: >-
  Build, run, validate, and operationalize Phoenix evaluators for AI and LLM applications in
  Python or TypeScript, including code evaluators, LLM judges, RAG evals, experiments, datasets,
  tracing, sampling, error analysis, and production guardrails. Use when the user asks for Phoenix
  evals, evaluator design, judge validation, experiments, or AI quality monitoring.
license: Apache-2.0
metadata:
  author: "oss@arize.com"
  compatibility: >-
    Requires Phoenix server. Python skills need phoenix and openai packages; TypeScript skills need
    @arizeai/phoenix-client.
  languages: Python, TypeScript
  version: 1.0.0
---

<!-- Generated from harness/github-copilot/skills/phoenix-evals/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Phoenix evals

Design evaluator systems for AI/LLM applications; start from observed failures, choose deterministic code or LLM judges, validate against human labels, then run experiments or production guardrails through the bundled Phoenix references.

## When to invoke

- "Build Phoenix evaluators for this LLM app."
- "Validate an LLM judge against human labels."
- "Run a Phoenix experiment on a dataset."
- "Design RAG evals for retrieval and faithfulness."
- "Set up production AI quality monitoring with Phoenix."

## Prerequisites and context

- A Phoenix server is required for workflows that log traces, datasets, or experiments.
- Python workflows need the `phoenix` and `openai` packages.
- TypeScript workflows need `@arizeai/phoenix-client`.
- Select Python or TypeScript based on the user's stack; do not mix SDK examples unless the task spans both.

## Evaluation principles

| Principle | Action | Failure mode prevented |
| --- | --- | --- |
| Error analysis first | Inspect real traces, sample failures, and categorize defects before automating. | Building evaluators for imagined problems. |
| Custom > generic | Encode the application's observed failure modes and policy boundaries. | Generic evals that pass while product-specific issues remain. |
| Code first | Use deterministic checks for schemas, exact constraints, tool calls, citations, and retrieval shape. | Expensive LLM judges for facts a program can verify. |
| LLM for nuance | Use judge models for semantic correctness, helpfulness, groundedness, and policy interpretation. | Brittle rules for subjective language tasks. |
| Validate judges | Compare evaluator outputs against human labels and target >80% TPR/TNR. | Uncalibrated judges that create false confidence. |
| Binary > Likert | Prefer pass/fail or clear categorical outputs over 1-5 scales. | Ambiguous scores that cannot drive decisions. |

## Workflow selection

| Goal | Read these references | Output |
| --- | --- | --- |
| Setup Python | `references/setup-python.md` | Installed packages and Phoenix connection. |
| Setup TypeScript | `references/setup-typescript.md` | Installed client and Phoenix connection. |
| Decide what to evaluate | `references/evaluators-overview.md` | Evaluation target map. |
| Choose a judge model | `references/fundamentals-model-selection.md` | Model choice and cost/quality rationale. |
| Use pre-built evaluators | `references/evaluators-pre-built.md` | Configured stock evaluator. |
| Build code evaluator | `references/evaluators-code-python.md`, `references/evaluators-code-typescript.md` | Deterministic evaluator function. |
| Build LLM evaluator | `references/evaluators-llm-python.md`, `references/evaluators-llm-typescript.md`, `references/evaluators-custom-templates.md` | Prompted judge with structured output. |
| Batch evaluate DataFrame | `references/evaluate-dataframe-python.md` | DataFrame-level evaluation results. |
| Understand experiments | `references/experiments-overview.md` | Experiment plan and metadata. |
| Run experiment | `references/experiments-running-python.md`, `references/experiments-running-typescript.md` | Experiment run and comparison. |
| Create dataset | `references/experiments-datasets-python.md`, `references/experiments-datasets-typescript.md` | Dataset records. |
| Generate synthetic data | `references/experiments-synthetic-python.md`, `references/experiments-synthetic-typescript.md` | Synthetic cases with caveats. |
| Validate evaluator accuracy | `references/validation.md`, `references/validation-evaluators-python.md`, `references/validation-evaluators-typescript.md` | TPR/TNR and error analysis. |
| Sample traces for review | `references/observe-sampling-python.md`, `references/observe-sampling-typescript.md` | Representative trace sample. |
| Analyze errors | `references/error-analysis.md`, `references/error-analysis-multi-turn.md`, `references/axial-coding.md` | Failure taxonomy and coding scheme. |
| RAG evals | `references/evaluators-rag.md` | Retrieval, context, and faithfulness checks. |
| Avoid common mistakes | `references/common-mistakes-python.md`, `references/fundamentals-anti-patterns.md` | Anti-pattern fixes. |
| Production | `references/production-overview.md`, `references/production-guardrails.md`, `references/production-continuous.md` | Monitoring and guardrail loop. |

## Recommended workflows

| Scenario | Ordered path |
| --- | --- |
| Starting fresh | `references/observe-tracing-setup.md` → `references/error-analysis.md` → `references/axial-coding.md` → `references/evaluators-overview.md` |
| Building evaluator | `references/fundamentals.md` → `references/common-mistakes-python.md` → `references/evaluators-code-python.md` or `references/evaluators-code-typescript.md` → `references/evaluators-llm-python.md` or `references/evaluators-llm-typescript.md` → validation references |
| RAG systems | `references/evaluators-rag.md` → code evaluator references for retrieval → LLM evaluator references for faithfulness |
| Production | `references/production-overview.md` → `references/production-guardrails.md` → `references/production-continuous.md` |

## Reference filename families

Shorthand families such as `evaluators-code`, `evaluators-llm`, and `validation-evaluators` refer to both Python and TypeScript reference files. Prefer `Pass/fail` labels where possible rather than broad ordinal scores.
## Reference categories

| Prefix | Description |
| --- | --- |
| `fundamentals-*` | Evaluator types, score design, model selection, and anti-patterns. |
| `observe-*` | Tracing setup and sampling. |
| `error-analysis-*` | Finding failures in traces and multi-turn interactions. |
| `axial-coding-*` | Categorizing failures into a stable taxonomy. |
| `evaluators-*` | Code, LLM, RAG, pre-built, and custom-template evaluators. |
| `experiments-*` | Datasets, running experiments, and synthetic examples. |
| `validation-*` | Comparing evaluators to human labels and measuring accuracy. |
| `production-*` | CI/CD, continuous monitoring, and guardrails. |

## Progressive disclosure and bundled resources

This skill is reference-heavy. Read only the references required by the chosen workflow rather than loading the full `references/` directory.

## Gotchas

- **Do not start with a judge prompt**: classify real failures first or the evaluator will encode guesses.
- **Do not use Likert scores unless required**: binary or categorical labels are easier to validate and automate.
- **Do not deploy unvalidated judges**: report TPR/TNR against human labels before trusting an LLM evaluator.
- **Synthetic data is not a substitute for production traces**: use it to fill gaps, not to define the whole evaluation space.

## Output template

```markdown
## Phoenix evals result — <application or evaluator>

**Status:** designed | implemented | run | validated | blocked
**Language:** Python | TypeScript
**Workflow:** setup | error analysis | code evaluator | LLM evaluator | RAG eval | experiment | validation | production

### Evaluator plan
| Target behavior | Evaluator type | Signal | Reference used |
| --- | --- | --- | --- |
| <behavior> | code | LLM | RAG | <pass/fail or category> | `<references/...md>` |

### Validation
- Human label comparison: <TPR/TNR or not run>
- Threshold: >80% TPR/TNR
- Remaining gaps: <none or specific gap>
```

## Quality gate

- [ ] The workflow starts from observed traces, failures, human labels, or a clearly stated evaluation target.
- [ ] The selected references match Python or TypeScript and the task goal.
- [ ] Deterministic code evaluators are preferred before LLM judges where possible.
- [ ] LLM judges use binary or categorical outputs unless a stronger reason exists.
- [ ] Evaluator accuracy is validated against human labels and reports TPR/TNR when validation is in scope.
- [ ] Production guidance includes guardrails or continuous monitoring rather than one-off scores.

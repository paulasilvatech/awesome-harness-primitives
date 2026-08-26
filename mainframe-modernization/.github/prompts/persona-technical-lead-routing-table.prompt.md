---
name: "routing-table"
description: "Map a feature's tasks to the right Copilot mode and model tier with rationale and a cost tier, grounded in the kit's routing cards."
argument-hint: "tasks=specs/<NNN>-<feature>/tasks.md"
agent: "tech-lead"
tools: ["read", "search"]
---
# /routing-table

## Objective

Produce a routing table that maps each task in a feature to the Copilot mode and
model tier that fit it, with a one-line rationale and a cost tier. It follows the
kit's own routing guidance so the team spends the smallest sufficient model and
mode on each task — never model prestige.

## When to Invoke

At the start of a feature, once `tasks.md` (or a backlog) exists, so the team can
budget effort and pick the right mode and model before executing.

## Preconditions

- `specs/<NNN>-<feature>/tasks.md` or a task backlog exists
- The routing cards are the source of truth: [`../../09-cheat-sheets/model-routing.md`](../../09-cheat-sheets/model-routing.md) and [`../../09-cheat-sheets/copilot-3-modes.md`](../../09-cheat-sheets/copilot-3-modes.md)

## Inputs the Team Must Provide

- The task list path (or the backlog to route)

Ask the user for anything that is missing.

## What I Will Do

- Categorize each task as Discovery, Design, Implementation, Refactor, Review, or Mechanical
- Recommend a Copilot mode per the three-modes card: Ask (explore, discuss), Plan (multi-file design), or Agent (delegated Issue to PR)
- Recommend a model tier per the model-routing card: Haiku 4.5 (mechanical), Sonnet 4.6 (everyday default), or Opus 4.6 (architecture decision)
- Give a one-line, task-specific rationale and an approximate cost tier
- Flag tasks where a cheaper tier is sufficient without compromising quality

## What I Will NOT Do

- Pin a model into any primitive's frontmatter — this table guides the human's manual model-picker choice, nothing more (see the [prompts index](README.md))
- Invent a routing model — I only apply the two cited cards
- Default every task to Opus — I justify moving up from Sonnet
- Give generic rationales — each references the task's actual content
- Decide the task scope itself — task definition is redirected to `/impl-plan`

## Output Format

A Markdown table presented for review. Example (illustrative):

```markdown
## Routing table — 014-registration

| Task ID | Category | Copilot Mode | Model Tier | Rationale | Cost Tier |
|---------|----------|--------------|------------|-----------|-----------|
| T-01 | Mechanical | Ask | Haiku 4.5 | Generate migration DDL from a fixed schema | Low |
| T-02 | Implementation | Plan | Sonnet 4.6 | Multi-file module scaffold with tests | Medium |
| T-05 | Design | Ask | Opus 4.6 | Choose the aggregate boundary — hard to reverse | High |

Cheaper-tier candidates: T-01 (Haiku is sufficient).
```

## Definition of Done

- [ ] Every task has a Copilot mode, a model tier, and a rationale
- [ ] At least one cheaper-tier candidate is identified (or noted "none applicable")
- [ ] Cost tiers are consistent — the same category rarely uses different tiers
- [ ] Each rationale references the task content, not generic language
- [ ] Recommendations match the two routing cards, with no invented tiers

## Prompt Body

You are the `@tech-lead`. The team wants to route its work to the right mode and
model before spending time on it.

**Step 1 — Read the tasks.**
Open `tasks.md` (or the backlog). For each task, note what it touches and how
ambiguous or risky it is.

**Step 2 — Categorize.**
Label each task Discovery, Design, Implementation, Refactor, Review, or Mechanical
based on its content.

**Step 3 — Assign a Copilot mode.**
Using the three-modes card, pick Ask for exploration and discussion, Plan for
multi-file changes that need a reviewed scope, and Agent for a well-described Issue
that can run to a PR unattended.

**Step 4 — Assign a model tier.**
Using the model-routing card, pick Haiku 4.5 for mechanical generation, Sonnet 4.6
as the everyday default for code and review, and Opus 4.6 only for an architecture
decision, trade-off, or impact analysis. Moving up from Sonnet needs a reason.

**Step 5 — Add rationale and cost.**
Give each task a one-line rationale tied to its actual content and an approximate
cost tier (Low, Medium, High). Flag any task where a cheaper tier would not reduce
quality.

Never pin a model into a primitive — this table only advises the human at the
model picker. Do not invent tiers or modes beyond the two cited cards.

## Invocation Example

```
/routing-table tasks=specs/014-registration/tasks.md
```

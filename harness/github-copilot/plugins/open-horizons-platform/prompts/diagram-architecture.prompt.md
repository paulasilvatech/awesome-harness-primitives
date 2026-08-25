---
name: "diagram-architecture"
description: "Create an architecture diagram at user-selected draw.io and optional SVG destinations."
argument-hint: "subject=<system> drawio=<exact/path.drawio> svg=<optional/path.svg>"
agent: "open-horizons-architect"
tools: ["read", "search", "edit", "execute", "web"]
---

# Diagram architecture

## Objective

Create an editable architecture diagram for `${input:subject}` at exactly
`${input:drawio_destination}`, with an SVG only when `${input:svg_destination}` is supplied.

## When to Invoke

Use when an architecture view and exact workspace artifact destinations are already selected.

## Preconditions

- `${input:subject}` identifies the system, audience, and requested view.
- `${input:drawio_destination}` is an approved repository-relative path ending in `.drawio`.
- `${input:svg_destination}`, when supplied, is an approved repository-relative path ending in
  `.svg`.

If a destination is missing, unsafe, outside the agent's editing policy, or has the wrong extension,
report the blocker and do not write any artifact.

## Inputs the Team Must Provide

- Subject and view: `${input:subject}`.
- Exact draw.io destination: `${input:drawio_destination}`.
- Optional exact SVG destination: `${input:svg_destination}`.
- Required nodes, relationships, boundaries, and constraints: `${input:diagram_context}`.

## What I Will Do

- Invoke the `azure-draw-io-diagram-generator` skill.
- Inspect supplied repository context and make unresolved architecture assumptions explicit.
- Write only the selected destination or destinations and validate the editable source.

## What I Will NOT Do

- Choose a default output directory or infer a filename.
- Modify implementation, infrastructure, or unrelated documentation.
- Claim visual quality from structural validation alone.

## Output Format

```markdown
## Architecture diagram result
- Draw.io: <exact path or not written>
- SVG: <exact path or not requested>
- View and scope: <summary>
- Structural validation: <command and result>
- Visual inspection/export: <result or not run>
- Assumptions or blockers: <none or details>
```

## Definition of Done

- [ ] The editable source exists at exactly `${input:drawio_destination}`.
- [ ] SVG exists at exactly `${input:svg_destination}` when requested, and nowhere otherwise.
- [ ] The diagram skill was invoked and structural plus official-icon provenance validation ran.
- [ ] No unapproved path or non-diagram source changed.

## Prompt Body

Have `open-horizons-architect` invoke `azure-draw-io-diagram-generator`, use `${input:diagram_context}` to diagram
`${input:subject}`, and write only `${input:drawio_destination}` plus the optional
`${input:svg_destination}`. Stop on destination or architecture ambiguity rather than choosing a path
or inventing system facts.

## Invocation Example

Run **Chat: Run Prompt**, select `diagram-architecture`, provide the subject and context, and choose
exact `.drawio` and optional `.svg` repository-relative destinations.

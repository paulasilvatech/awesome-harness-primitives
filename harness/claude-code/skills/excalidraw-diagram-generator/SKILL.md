---
name: excalidraw-diagram-generator
description: >-
  Generate valid .excalidraw JSON diagrams from natural language descriptions, including
  flowcharts, relationship diagrams, mind maps, architecture diagrams, DFDs, swimlanes, class
  diagrams, sequence diagrams, and ER diagrams. Use when asked to create a diagram, make a
  flowchart, visualize a process, draw a system architecture, create a mind map, show
  relationships, or generate an Excalidraw file.
---

<!-- Generated from harness/github-copilot/skills/excalidraw-diagram-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Excalidraw diagram generator

Turn a natural-language diagram request into a valid Excalidraw JSON file by choosing the right diagram type, extracting nodes and relationships, laying out elements, and saving a `.excalidraw` artifact the user can open directly.

## When to invoke

- "Create a diagram showing this workflow."
- "Make a flowchart for the registration process."
- "Draw the system architecture as an Excalidraw file."
- "Generate a mind map about these concepts."
- "Show the relationship between these entities."

## Prerequisites and context

- Require a clear description of what should be visualized, including key entities, steps, concepts, relationships, and flow.
- If the request has too many elements, propose multiple diagrams before generating a crowded file.
- Save output as `<descriptive-name>.excalidraw`; users can open it at https://excalidraw.com by drag-and-drop, File → Open, or the Excalidraw VS Code extension.

## Diagram selection

| User intent | Diagram type | Extract |
| --- | --- | --- |
| Workflow, process, steps, procedure, decision tree | Flowchart | Start, end, sequential steps, decision points. |
| Relationship, connections, dependencies, structure | Relationship Diagram | Entities/nodes and labeled relationships from → to. |
| Mind map, concepts, ideas, breakdown | Mind Map | Central topic, 3-6 main branches, optional sub-topics. |
| Architecture, system, components, modules | Architecture Diagram | Components, interfaces, boundaries, data/control flow. |
| Data flow, data processing, data transformation | Data Flow Diagram (DFD) | External entities, processes, data stores, and data flows; do not represent process order. |
| Business process, swimlane, actors, responsibilities | Business Flow (Swimlane) | Actor columns, process lanes, activities, cross-lane handoffs. |
| Class, inheritance, OOP, object model | Class Diagram | Classes, attributes, methods, visibility, relationships, multiplicity. |
| Sequence, interaction, messages, timeline | Sequence Diagram | Objects/actors, lifelines, messages, return values, activation boxes; time flows top to bottom. |
| Database, entity, relationship, data model | ER Diagram | Entities, attributes, primary keys, foreign keys, cardinality, junction entities. |

## Excalidraw JSON rules

Generate complete JSON with `type: "excalidraw"`, `version: 2`, `source: "https://excalidraw.com"`, an `elements` array, `appState.viewBackgroundColor: "#ffffff"`, `appState.gridSize: 20`, and `files: {}`.

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": 20 },
  "files": {}
}
```

| Element type | Use it for | Required properties |
| --- | --- | --- |
| `rectangle` | Entities, steps, concepts, swimlane activities, classes | `id`, `x`, `y`, `width`, `height`, `strokeColor`, `backgroundColor`, `fillStyle`. |
| `ellipse` | Alternative emphasis or boundary shapes | Same core position, size, and style properties. |
| `diamond` | Decision points | Enough width for text and outgoing labels. |
| `arrow` | Directional connections | `points` array and logical start/end placement. |
| `text` | Labels and annotations | `fontFamily: 5` for Excalifont, readable `fontSize`, and embedded `text`. |

All text elements must use `fontFamily: 5` (Excalifont). Use timestamp plus random suffix IDs such as `Date.now().toString(36) + Math.random().toString(36).substr(2)`.

## Layout rules

| Rule | Value |
| --- | --- |
| Horizontal gap | `200-300px` between elements. |
| Vertical gap | `100-150px` between rows. |
| Text size | `16-24px`; never below `16px` for normal labels. |
| Primary color | Light blue `#a5d8ff`. |
| Secondary color | Light green `#b2f2bb`. |
| Central/important color | Yellow `#ffd43b`. |
| Alert/warning color | Light red `#ffc9c9`. |
| Roughness | Default `1`. |
| Recommended maximum | Fewer than `20` elements for clarity. |

Use straight arrows for simple flows and curved arrows only for complex relationships. For relationship diagrams, use grid layout:

```javascript
const columns = Math.ceil(Math.sqrt(entityCount));
const x = startX + (index % columns) * horizontalGap;
const y = startY + Math.floor(index / columns) * verticalGap;
```

For mind maps, use radial layout:

```javascript
const angle = (2 * Math.PI * index) / branchCount;
const x = centerX + radius * Math.cos(angle);
const y = centerY + radius * Math.sin(angle);
```

## Diagram-specific notation

| Type | Required conventions |
| --- | --- |
| Flowcharts | Rectangles for steps, diamonds for decisions, arrows for sequence, explicit start and end. |
| Data Flow Diagrams (DFD) | Data sources and destinations, processes, data stores, arrows showing data movement left-to-right or top-left to bottom-right; no process-order semantics. |
| Business Flow (Swimlane) | Actors/roles as header columns, vertical lanes, process boxes inside lanes, arrows for cross-lane handoffs. |
| Class Diagrams | Visibility `+`, `-`, `#`; inheritance uses solid line plus white triangle; implementation dashed line plus white triangle; association solid line; dependency dashed line; aggregation solid line plus white diamond; composition solid line plus filled diamond; multiplicity `1`, `0..1`, `1..*`, `*`. |
| Sequence Diagrams | Actors horizontally at top, vertical lifelines, synchronous solid arrows, asynchronous dashed arrows, return values dashed arrows, activation boxes. |
| ER Diagrams | Entities as rectangles, attributes inside, primary keys marked `PK`, foreign keys marked `FK`, relationships with `1:1`, `1:N`, `N:M`, and junction/associative entities for many-to-many relationships. |

## Complexity management

| Problem | Response |
| --- | --- |
| More than 15 flowchart steps | Split into high-level and detailed flowcharts. |
| More than 12 relationship entities | Create a high-level relationship diagram first, then subsystem diagrams. |
| More than 8 mind-map branches or 6 sub-topics per branch | Trim to primary concepts and offer follow-up diagrams. |
| User includes 15 components | Recommend a high-level architecture diagram with 6 main components plus detailed subsystem diagrams. |
| Request needs icons | Read `references/icon-libraries.md` and use the icon-library workflow. |

## Procedure

1. Understand the request: determine diagram type, key elements, relationships, and complexity.
2. Choose the appropriate diagram type from the selection table.
3. Extract structured information: steps, decisions, entities, branches, actors, classes, lifelines, data stores, or cardinalities.
4. Use bundled templates when they match the requested type; otherwise build JSON from scratch using the schema rules.
5. Generate the `.excalidraw` file with unique IDs, non-overlapping coordinates, consistent colors, readable text, and logical arrows.
6. Validate JSON syntax and element count, then provide a concise summary and opening instructions.

## Progressive disclosure and bundled resources

Read bundled resources only when needed:

- `references/excalidraw-schema.md`: complete Excalidraw JSON schema.
- `references/element-types.md`: detailed element type specifications.
- `references/icon-libraries.md`: Excalidraw icon libraries and optional icon loading.
- `templates/flowchart-template.excalidraw`: basic flowchart starter.
- `templates/relationship-template.excalidraw`: relationship diagram starter.
- `templates/mindmap-template.excalidraw`: mind map starter.
- `templates/data-flow-diagram-template.excalidraw`: DFD starter.
- `templates/business-flow-swimlane-template.excalidraw`: swimlane starter.
- `templates/class-diagram-template.excalidraw`: class diagram starter.
- `templates/sequence-diagram-template.excalidraw`: sequence diagram starter.
- `templates/er-diagram-template.excalidraw`: ER diagram starter.
- `scripts/split-excalidraw-library.py`: split `.excalidrawlib` files.
- `scripts/add-icon-to-diagram.py`: add an icon to a diagram.
- `scripts/add-arrow.py`: add arrows programmatically.
- `scripts/README.md`: documentation for library tools.
- `scripts/.gitignore`: prevents local Python artifacts from being committed.

## Limits

- Complex curves are simplified to straight or basic curved lines.
- Embedded images are not generated automatically; use imports or icon-library resources when needed.
- No automatic collision detection exists, so apply spacing and validation manually.
- Mermaid or PlantUML import and auto-layout optimization are future enhancements, not current required output.

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Elements overlap | Increase coordinate spacing or switch to grid/radial layout. |
| Text doesn't fit in boxes | Increase box width or reduce font size while staying readable. |
| Too many elements | Break into multiple diagrams. |
| Unclear layout | Use rows/columns for relationships or radial layout for mind maps. |
| Colors inconsistent | Define the palette upfront by element type. |

## Naming and compatibility notes

Preserve common example filenames and legacy template references when mapping older requests: user-registration-flow, `user-registration-flow.excalidraw`, user-content-relationships, `user-content-relationships.excalidraw`, machine-learning-mindmap, `machine-learning-mindmap.excalidraw`, user-workflow, templates/flowchart-template.json, templates/relationship-template.json, and `templates/mindmap-template.json`. Current bundled templates use `.excalidraw`; do not create new `.json` templates unless the user asks.

Style names must remain understandable to agents translating older examples: Important/Central, Alerts/Warnings, actor-based process flows, Junction/associative entities, one-to-one, one-to-many, sub-diagrams, auto-generation, opening/editing, straight/basic curved lines, Mermaid/PlantUML future import, and core element keys `width`, `height`, `strokeColor`, `backgroundColor`, and `fillStyle`.

## Output template

```markdown
## Excalidraw diagram result - <diagram name>

**Status:** created | needs clarification | blocked
**File:** `<descriptive-name>.excalidraw`
**Type:** Flowchart | Relationship Diagram | Mind Map | Architecture Diagram | Data Flow Diagram (DFD) | Business Flow (Swimlane) | Class Diagram | Sequence Diagram | ER Diagram
**Elements:** `<count>` total (`<rectangles>` rectangles, `<arrows>` arrows, `<text>` text)

### Created structure
- <main nodes or sections>
- <relationships or flow>

### To view
1. Visit https://excalidraw.com
2. Drag and drop `<descriptive-name>.excalidraw`
3. Or use File → Open in the Excalidraw VS Code extension
```

## Quality gate

- [ ] The chosen diagram type matches the user's intent and extracted structure.
- [ ] The file is valid JSON with `type`, `version`, `source`, `elements`, `appState`, and `files`.
- [ ] All elements have unique IDs and coordinates prevent overlap.
- [ ] All text elements use `fontFamily: 5` and readable `fontSize`.
- [ ] Arrows connect logically and labels match relationships or flow.
- [ ] Colors follow a consistent scheme and element count is reasonable.
- [ ] The output includes the `.excalidraw` file, summary, element count, and opening instructions.

## References

- [Excalidraw](https://excalidraw.com)

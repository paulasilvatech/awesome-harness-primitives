---
name: "shuffle-json-data"
description: >-
  Shuffle repetitive JSON arrays safely by validating syntax, schema consistency, requiredProperties, ignoreProperties, and nesting rules before randomizing entries. Use when asked to shuffle, randomize, reorder, anonymize order, or vary repetitive JSON objects while keeping valid JSON and preserving data integrity.
---

# Shuffle JSON data

Validate a JSON file or JSON-like structure, confirm the objects can be shuffled without corrupting schema or syntax, then return a randomized version that preserves the configured structure.

## When to invoke

- "Shuffle this JSON data."
- "Randomize the order of these repetitive JSON objects."
- "Reorder this fixture without breaking its schema."
- "Shuffle only these JSON collections and ignore the year field."
- "Validate whether this JSON can be safely randomized."

## Inputs

A request must include a JSON file, attached JSON, or pasted JSON-like structure. If no data is provided, ask for a file or JSON content before proceeding. Interpret variables under a `Variables` header or prompt-level overrides:

| Variable | Default | Meaning |
| --- | --- | --- |
| `fileName` | **REQUIRED** | JSON file or attached data source. Preserve `_NAME` compatibility by treating file-name variants as `fileName`. |
| `ignoreProperties` | none | Properties excluded from schema consistency comparison. |
| `requiredProperties` | first object's property set | Properties every shuffled object must contain. |
| `nesting` | `false` | Whether nested objects are allowed and how nested collections may be shuffled. |

## Validation rules

| Check | Default behavior |
| --- | --- |
| JSON syntax | Parse successfully before any shuffle. |
| Top-level shape | Expect an array of objects unless variables specify a different collection. |
| Property names | Every object must share an identical property set after `ignoreProperties` is applied. |
| Required fields | Every object must contain all `requiredProperties`. |
| Nested objects | Reject when `nesting = false`. |
| Output validity | The result must serialize as valid JSON. |

Stop and report the inconsistency instead of modifying data when any required check fails.

## Acceptable and unacceptable shapes

Acceptable default shape:

```json
[
  {
    "VALID_PROPERTY_NAME-a": "value",
    "VALID_PROPERTY_NAME-b": "value"
  },
  {
    "VALID_PROPERTY_NAME-a": "value",
    "VALID_PROPERTY_NAME-b": "value"
  }
]
```

Unacceptable default shape because it has nesting and inconsistent properties:

```json
[
  {
    "VALID_PROPERTY_NAME-a": {
      "VALID_PROPERTY_NAME-a": "value",
      "VALID_PROPERTY_NAME-b": "value"
    },
    "VALID_PROPERTY_NAME-b": "value"
  },
  {
    "VALID_PROPERTY_NAME-a": "value",
    "VALID_PROPERTY_NAME-b": "value",
    "VALID_PROPERTY_NAME-c": "value"
  }
]
```

## Procedure

1. Gather the JSON file or JSON-like structure. If missing, ask for it and stop.
2. Merge defaults with `Variables` overrides: `ignoreProperties`, `requiredProperties`, and `nesting`.
3. Parse the JSON and record the original formatting and encoding conventions when editing a file.
4. Validate structural consistency using the selected mode.
5. Shuffle only the configured collection(s), not keys inside objects unless explicitly requested.
6. Serialize valid JSON and preserve formatting as closely as possible.
7. Return the shuffled data or write it to the requested destination.

## Gotchas

- **Do not shuffle invalid JSON**: repair is a separate task unless the user asks for it.
- **Do not assume nested data is safe**: nested objects can encode relationships that object-level shuffling breaks.
- **Do not ignore schema drift silently**: inconsistent property names usually mean different record types.
- **Do not shuffle property order as data randomization**: property order changes are cosmetic and can make diffs noisy.

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `data-engineering`

## Output template

```markdown
## Shuffle JSON result

**Status:** shuffled | blocked
**Input:** `<fileName or pasted JSON>`

### Validation
| Check | Result | Evidence |
| --- | --- | --- |
| JSON syntax | pass/fail | <parser result> |
| Property consistency | pass/fail | <property set or mismatch> |
| Nesting | pass/fail | <nesting setting and finding> |

### Output
```json
<shuffled valid JSON or omitted when written to file>
```

### Notes
- <variables used or blocker>
```

## Quality gate

- [ ] A JSON file or JSON structure was provided before shuffling.
- [ ] JSON parsed successfully before modification.
- [ ] Property consistency, `requiredProperties`, `ignoreProperties`, and `nesting` were applied.
- [ ] Nested objects were rejected unless an override explicitly allowed them.
- [ ] The final output is valid JSON.
- [ ] Any failure reports the exact inconsistency instead of returning partial shuffled data.

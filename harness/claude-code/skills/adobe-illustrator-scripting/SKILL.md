---
name: adobe-illustrator-scripting
description: >-
  Write, debug, and optimize Adobe Illustrator automation scripts using ExtendScript
  (JavaScript/JSX). Use when creating or modifying scripts that manipulate documents, layers,
  paths, text frames, colors, symbols, artboards, or any Illustrator DOM objects. Covers the
  complete JavaScript object model, coordinate system, measurement units, export workflows, and
  scripting best practices.
---

<!-- Generated from harness/github-copilot/skills/adobe-illustrator-scripting/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Adobe Illustrator scripting

Write, debug, and optimize Adobe Illustrator ExtendScript automation by applying the Illustrator DOM, coordinate system, document and page item APIs, export options, and bundled JSX patterns.

## When to invoke

- "Write an Illustrator JSX script."
- "Debug this Adobe Illustrator ExtendScript."
- "Automate Illustrator layers, paths, text, colors, symbols, or artboards."
- "Export Illustrator documents to PDF, SVG, PNG, or EPS with a script."
- "Batch process .ai files with JavaScript."

Expert guidance for automating Adobe Illustrator through ExtendScript (JavaScript/JSX). This skill covers the Illustrator scripting object model, all major API objects, code patterns, and best practices for writing production-quality `.jsx` scripts.

## Bundled Assets

- [`references/object-model-quick-reference.md`](references/object-model-quick-reference.md): Use this as a quick lookup for the Illustrator scripting object model, common document and page item types, and related DOM concepts while writing or debugging scripts.
- `scripts/`: Contains example Illustrator automation scripts you can use as starting points or implementation patterns for common tasks such as document manipulation, exports, batch processing, and DOM usage. Review and adapt these examples when you need working JSX patterns or want to compare behavior while debugging.
## Invocation details

- Writing new Illustrator automation scripts (`.jsx` or `.js` files)
- Debugging or fixing existing Illustrator ExtendScript code
- Manipulating documents, layers, page items, paths, text, or colors programmatically
- Batch-processing Illustrator files or generating artwork from data
- Exporting documents to various formats (PDF, SVG, PNG, EPS, etc.)
- Working with the Illustrator DOM (Application, Document, Layer, PathItem, TextFrame, etc.)
- Creating data-driven graphics using variables and datasets
- Automating print workflows with scripted print options

## Prerequisites

- Adobe Illustrator CC or later installed
- Basic JavaScript knowledge (ExtendScript is ES3-based with Adobe extensions)
- Scripts are executed via File > Scripts > Other Scripts, the Scripts menu, or placed in the Startup Scripts folder
- The ExtendScript Toolkit (ESTK) or any text editor can be used to write `.jsx` files

## Scripting Environment

### Language and File Extensions

| Language | Extension | Platform |
|---|---|---|
| ExtendScript/JavaScript | `.jsx`, `.js` | Windows, macOS |
| AppleScript | `.scpt` | macOS only |
| VBScript | `.vbs` | Windows only |

**This skill focuses on ExtendScript/JavaScript** as the cross-platform, most widely used option.

### Executing Scripts

- **Scripts menu**: File > Scripts lists scripts from the application scripts folder
- **Other Scripts**: File > Scripts > Other Scripts to browse and run any `.jsx` file
- **Startup Scripts**: Place scripts in the Startup Scripts folder to run automatically on launch
- **Target directive**: Begin scripts with `#target illustrator` when running from ESTK or external tools
- **`#targetengine` directive**: Use `#targetengine "session"` to persist variables across script executions
- **External invocation**: Scripts are frequently launched from outside Illustrator — by shell scripts, task runners, CI jobs, ExtendScript Toolkit (`ExtendScript Toolkit.exe -run script.jsx`), or `BridgeTalk` messages from other Adobe apps. See [External Invocation & Argument Passing](#external-invocation--argument-passing).

### Naming Conventions (JavaScript)

- Objects and properties use **camelCase**: `activeDocument`, `pathItems`, `textFrames`
- The `app` global references the `Application` object
- Collection indices are **zero-based**: `documents[0]` is the frontmost document
- Use `typename` property to identify object types at runtime

## Object Model Overview

The Illustrator DOM follows a strict containment hierarchy:

```
Application (app)
├── activeDocument / documents[]
│   ├── layers[]
│   │   ├── pageItems[] (all artwork)
│   │   ├── pathItems[]
│   │   ├── compoundPathItems[]
│   │   ├── textFrames[]
│   │   ├── placedItems[]
│   │   ├── rasterItems[]
│   │   ├── meshItems[]
│   │   ├── pluginItems[]
│   │   ├── graphItems[]
│   │   ├── symbolItems[]
│   │   ├── nonNativeItems[]
│   │   ├── legacyTextItems[]
│   │   └── groupItems[]
│   ├── artboards[]
│   ├── views[]
│   ├── selection (array of selected items)
│   ├── swatches[], spots[], gradients[], patterns[]
│   ├── graphicStyles[], brushes[], symbols[]
│   ├── textFonts[] (via app.textFonts)
│   ├── stories[], characterStyles[], paragraphStyles[]
│   ├── variables[], datasets[]
│   └── inkList[], printOptions
├── preferences
├── printerList[]
└── textFonts[]
```

### Top-Level Objects

- **Application** (`app`): The root object. Provides access to documents, preferences, fonts, and printers. Key properties: `activeDocument`, `documents`, `textFonts`, `printerList`, `userInteractionLevel`, `version`.
- **Document**: Represents an open `.ai` file. Key properties: `layers`, `pageItems`, `selection`, `activeLayer`, `width`, `height`, `rulerOrigin`, `documentColorSpace`. Key methods: `saveAs()`, `exportFile()`, `close()`, `print()`.
- **Layer**: A drawing layer. Key properties: `pageItems`, `pathItems`, `textFrames`, `visible`, `locked`, `opacity`, `name`, `zOrderPosition`, `color`.

## Measurement Units and Coordinates

### Units

All scripting API values use **points** (72 points = 1 inch). Convert other units:

| Unit | Conversion |
|---|---|
| Inches | multiply by 72 |
| Centimeters | multiply by 28.346 |
| Millimeters | multiply by 2.834645 |
| Picas | multiply by 12 |

Kerning, tracking, and `aki` properties use **em units** (thousandths of an em, proportional to font size).

### Coordinate System

- For **scripted documents**, the origin `(0,0)` is at the **bottom-left** of the artboard
- X increases left to right; Y increases bottom to top
- The `position` property of a page item is the **top-left corner** of its bounding box as `[x, y]`
- Maximum page item width/height: 16348 points

### Art Item Bounds

Every page item has three bounding rectangles:

- `geometricBounds`: Excludes stroke width `[left, top, right, bottom]`
- `visibleBounds`: Includes stroke width
- `controlBounds`: Includes control/direction points

## Working with Documents

### Creating and Opening

```javascript
// Create a new document
var doc = app.documents.add();

// Create with a preset
var preset = new DocumentPreset();
preset.width = 612;  // 8.5 inches
preset.height = 792; // 11 inches
preset.colorMode = DocumentColorSpace.CMYK;
var doc = app.documents.addDocument("Print", preset);

// Open an existing file
var fileRef = new File("/path/to/file.ai");
var doc = app.open(fileRef);
```

### Saving and Exporting

```javascript
// Save as Illustrator format
var saveOpts = new IllustratorSaveOptions();
saveOpts.compatibility = Compatibility.ILLUSTRATOR17; // CC
doc.saveAs(new File("/path/to/output.ai"), saveOpts);

// Export as PDF
var pdfOpts = new PDFSaveOptions();
pdfOpts.compatibility = PDFCompatibility.ACROBAT7;
pdfOpts.preserveEditability = false;
doc.saveAs(new File("/path/to/output.pdf"), pdfOpts);

// Export as PNG
var pngOpts = new ExportOptionsPNG24();
pngOpts.horizontalScale = 300;
pngOpts.verticalScale = 300;
pngOpts.transparency = true;
doc.exportFile(new File("/path/to/output.png"), ExportType.PNG24, pngOpts);

// Export as SVG
var svgOpts = new ExportOptionsSVG();
svgOpts.fontType = SVGFontType.OUTLINEFONT;
doc.exportFile(new File("/path/to/output.svg"), ExportType.SVG, svgOpts);
```

## Working with Paths and Shapes

### Built-in Shape Methods

The `pathItems` collection provides convenience methods for common shapes:

```javascript
var doc = app.activeDocument;
var layer = doc.activeLayer;

// Rectangle: rectangle(top, left, width, height)
var rect = layer.pathItems.rectangle(500, 100, 200, 150);

// Rounded rectangle: roundedRectangle(top, left, width, height, hRadius, vRadius)
var rrect = layer.pathItems.roundedRectangle(500, 100, 200, 150, 20, 20);

// Ellipse: ellipse(top, left, width, height)
var oval = layer.pathItems.ellipse(400, 200, 100, 100);

// Polygon: polygon(centerX, centerY, radius, sides)
var hex = layer.pathItems.polygon(300, 300, 50, 6);

// Star: star(centerX, centerY, radius, innerRadius, points)
var star = layer.pathItems.star(300, 300, 50, 25, 5);
```
## Extended reference

Additional detailed guidance was moved to [references/extended-guide.md](references/extended-guide.md) to keep this skill within the progressive-disclosure budget.

## Progressive disclosure and bundled resources

- `references/object-model-quick-reference.md`: quick lookup for the Illustrator object model and common DOM types.
- `references/extended-guide.md`: extended guidance that was moved out of SKILL.md for progressive disclosure.
- `scripts/`: example Illustrator automation scripts for document manipulation, exports, batch processing, and DOM usage.

## Output template

````markdown
## Illustrator scripting result

**Status:** implemented | reviewed | blocked
**Target:** `{{script_or_document}}`

### Script or patch
```javascript
#target illustrator
{{jsx_code}}
```

### Validation
- `{{execution_path}}`: pass | fail
- DOM objects used: `{{Application}}`, `{{Document}}`, `{{Layer}}`, `{{PathItem}}`, `{{TextFrame}}` as applicable
- Export or save output: `{{file_path_or_none}}`
````

## Quality gate

- [ ] The solution uses ExtendScript/JavaScript APIs that Illustrator supports, not browser-only JavaScript.
- [ ] All measurement values are converted to points where the Illustrator DOM expects points.
- [ ] Coordinates account for Illustrator's scripted-document origin and page item `position` semantics.
- [ ] Exports use the correct options object and `doc.saveAs()` or `doc.exportFile()` method.
- [ ] Bundled references or scripts are consulted when detailed API lookup or working JSX examples are needed.

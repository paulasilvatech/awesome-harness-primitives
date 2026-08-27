---
name: freecad-scripts
description: >-
  Write FreeCAD Python scripts, macros, parametric FeaturePython objects, Part/Mesh/Sketcher
  geometry, PySide GUI tools, Coin3D/Pivy scenegraph code, workbench commands, and CAD automation.
  Use when asked to create FreeCAD models, automate geometry, convert mesh and solid data, script
  FEM/Path/TechDraw, or debug FreeCAD Python API tasks.
---

<!-- Generated from harness/github-copilot/skills/freecad-scripts/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# FreeCAD scripts

Translate natural language CAD tasks into production-quality FreeCAD Python code that handles documents, geometry, GUI availability, recompute, selection, and macro execution safely.

## When to invoke

- "Write a FreeCAD macro to create this model."
- "Build a parametric FeaturePython object."
- "Script Part, Mesh, or Sketcher geometry in FreeCAD."
- "Create a PySide dialog or workbench command for FreeCAD."
- "Automate FEM, Path, TechDraw, or Coin3D scenegraph work."

## Prerequisites and context

- FreeCAD installed; 0.19+ is workable, 0.21+/1.0+ is preferred for newer APIs.
- Python 3.x is bundled with FreeCAD.
- PySide2 and Pivy are bundled for GUI and Coin3D work in typical FreeCAD installs.
- Guard GUI-only code with `if FreeCAD.GuiUp:` so macros can fail gracefully in headless execution.

## FreeCAD Python environment

Key modules and aliases:

```python
import FreeCAD          # core module, often aliased as App
import FreeCADGui       # GUI module, often aliased as Gui; GUI mode only
import Part             # BRep/OpenCASCADE shapes
import Mesh             # triangulated meshes
import Sketcher         # 2D constrained sketches
import Draft            # 2D drawing tools
import Arch             # Arch/BIM workbench
import Path             # Path/CAM workbench
import FEM              # FEM workbench
import TechDraw         # replaces Drawing
import BOPTools         # boolean operations
import CompoundTools    # compound shape utilities
```

Document model essentials:

```python
doc = FreeCAD.newDocument("MyDoc")
doc = FreeCAD.ActiveDocument
box = doc.addObject("Part::Box", "MyBox")
box.Length = 10.0
box.Width = 10.0
box.Height = 10.0
doc.recompute()
obj = doc.getObject("MyBox")
obj = doc.MyBox
doc.removeObject("MyBox")
```

## Macro pattern

```python
# -*- coding: utf-8 -*-
# FreeCAD Macro: MyMacro
# Description: Brief description of what the macro does
# Author: YourName
# Version: 1.0
# Date: 2026-04-07

import FreeCAD
import Part
from FreeCAD import Base

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide2 import QtWidgets, QtCore

def main():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        FreeCAD.Console.PrintError("No active document
")
        return
    if FreeCAD.GuiUp:
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            FreeCAD.Console.PrintWarning("No objects selected
")
    doc.recompute()
    FreeCAD.Console.PrintMessage("Macro completed
")

if __name__ == "__main__":
    main()
```

Selection and console APIs to preserve:

```python
sel = FreeCADGui.Selection.getSelection()
sel_ex = FreeCADGui.Selection.getSelectionEx()
for selobj in sel_ex:
    obj = selobj.Object
    for sub in selobj.SubElementNames:
        shape = obj.getSubObject(sub)
FreeCADGui.Selection.addSelection(doc.MyBox)
FreeCADGui.Selection.addSelection(doc.MyBox, "Face1")
FreeCADGui.Selection.clearSelection()
FreeCAD.Console.PrintMessage("Info message
")
FreeCAD.Console.PrintWarning("Warning message
")
FreeCAD.Console.PrintError("Error message
")
FreeCAD.Console.PrintLog("Debug/log message
")
```

## Compensation rules

| User shorthand | FreeCAD API action |
| --- | --- |
| box | `Part.makeBox()` |
| cylinder | `Part.makeCylinder()` |
| sphere | `Part.makeSphere()` |
| merge, combine, join | `.fuse()` |
| subtract, cut, remove | `.cut()` |
| intersect | `.common()` |
| round edges, fillet | `.makeFillet()` |
| bevel, chamfer | `.makeChamfer()` |
| no document specified | `doc = FreeCAD.ActiveDocument or FreeCAD.newDocument()` |
| no units specified | assume millimeters |
| quick display | `Part.show(shape, "Name")` |
| persistent named object | `doc.addObject("Part::Feature", "Name")` |

Always call `doc.recompute()` after modifications.

## Progressive disclosure and bundled resources

- `references/freecad-implementation-patterns.md`: detailed FreeCAD API concepts, FeaturePython, GUI, Coin3D, workbench, and reusable patterns.
- `references/scripting-fundamentals.md`: document model, console, and core scripting.
- `references/geometry-and-shapes.md`: Part, Mesh, Sketcher, and topology.
- `references/parametric-objects.md`: FeaturePython, properties, and scripted objects.
- `references/gui-and-interface.md`: PySide, dialogs, task panels, and Coin3D.
- `references/workbenches-and-advanced.md`: workbenches, macros, FEM, Path, and recipes.

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `PySide/Qt`
- `bevel/chamfer`
- `built-in`
- `edges/fillet`
- `merge/combine/join`
- `quasi-code`
- `sub-elements`
- `sub-shape`
- `subtract/cut/remove`
- `topic-organized`

## Output template

```markdown
## FreeCAD script result

**Status:** script-created | guidance-only | blocked
**Runtime:** FreeCAD Python macro | console snippet | workbench command

### Files or code
- `<path or snippet>`: <purpose>

### API coverage
| Area | APIs used | Notes |
| --- | --- | --- |
| Document | `FreeCAD.ActiveDocument`, `doc.recompute()` | <notes> |
| Geometry | `Part.makeBox()` / other APIs | <notes> |
| GUI | `FreeCAD.GuiUp` / PySide / selection | <notes> |

### Validation
- <how to run in FreeCAD and expected result>
```

## Quality gate

- [ ] The script imports only FreeCAD modules needed for the task.
- [ ] GUI-dependent code is guarded with `if FreeCAD.GuiUp:`.
- [ ] Document creation, object naming, and `doc.recompute()` are handled.
- [ ] Units default to millimeters unless the user specified otherwise.
- [ ] Geometry operations use the correct Part, Mesh, Sketcher, Draft, Arch, Path, FEM, TechDraw, BOPTools, or CompoundTools APIs.
- [ ] Console messages use `FreeCAD.Console.PrintMessage`, `PrintWarning`, `PrintError`, or `PrintLog`.
- [ ] Bundled references are used for FeaturePython, GUI, Coin3D, workbench, or advanced patterns when needed.

## References

- [Writing Python code](https://wiki.freecad.org/Manual:A_gentle_introduction#Writing_Python_code)
- [Manipulating FreeCAD objects](https://wiki.freecad.org/Manual:A_gentle_introduction#Manipulating_FreeCAD_objects)
- [Vectors and Placements](https://wiki.freecad.org/Manual:A_gentle_introduction#Vectors_and_Placements)
- [Creating and manipulating geometry](https://wiki.freecad.org/Manual:Creating_and_manipulating_geometry)
- [Creating parametric objects](https://wiki.freecad.org/Manual:Creating_parametric_objects)
- [Creating interface tools](https://wiki.freecad.org/Manual:Creating_interface_tools)
- [Python](https://en.wikipedia.org/wiki/Python_%28programming_language%29)
- [Introduction to Python](https://wiki.freecad.org/Introduction_to_Python)
- [Python scripting tutorial](https://wiki.freecad.org/Python_scripting_tutorial)
- [FreeCAD scripting basics](https://wiki.freecad.org/FreeCAD_Scripting_Basics)
- [Gui Command](https://wiki.freecad.org/Gui_Command)

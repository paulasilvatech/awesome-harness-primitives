---
name: "freecad-scripts"
description: >-
  Expert skill for writing FreeCAD Python scripts, macros, and automation. Use when asked to create
  FreeCAD models, parametric objects, Part/Mesh/Sketcher scripts, workbench tools, GUI dialogs with
  PySide, Coin3D scenegraph manipulation, or any FreeCAD Python API task. Covers FreeCAD scripting
  basics, geometry creation, FeaturePython objects, interface tools, and macro development.
---
# FreeCAD Scripts

Expert skill for generating production-quality Python scripts for the FreeCAD CAD application. Interprets shorthand, quasi-code, and natural language descriptions of 3D modeling tasks and translates them into correct FreeCAD Python API calls.

## When to Use This Skill

- Writing Python scripts for FreeCAD's built-in console or macro system
- Creating or manipulating 3D geometry (Part, Mesh, Sketcher, Path, FEM)
- Building parametric FeaturePython objects with custom properties
- Developing GUI tools using PySide/Qt within FreeCAD
- Manipulating the Coin3D scenegraph via Pivy
- Creating custom workbenches or Gui Commands
- Automating repetitive CAD operations with macros
- Converting between mesh and solid representations
- Scripting FEM analyses, raytracing, or drawing exports

## Prerequisites

- FreeCAD installed (0.19+ recommended; 0.21+/1.0+ for latest API)
- Python 3.x (bundled with FreeCAD)
- For GUI work: PySide2 (bundled with FreeCAD)
- For scenegraph: Pivy (bundled with FreeCAD)

## FreeCAD Python Environment

FreeCAD embeds a Python interpreter. Scripts run in an environment where these key modules are available:

```python
import FreeCAD          # Core module (also aliased as 'App')
import FreeCADGui       # GUI module (also aliased as 'Gui') — only in GUI mode
import Part             # Part workbench — BRep/OpenCASCADE shapes
import Mesh             # Mesh workbench — triangulated meshes
import Sketcher         # Sketcher workbench — 2D constrained sketches
import Draft            # Draft workbench — 2D drawing tools
import Arch             # Arch/BIM workbench
import Path             # Path/CAM workbench
import FEM              # FEM workbench
import TechDraw         # TechDraw workbench (replaces Drawing)
import BOPTools         # Boolean operations
import CompoundTools    # Compound shape utilities
```

### The FreeCAD Document Model

```python
# Create or access a document
doc = FreeCAD.newDocument("MyDoc")
doc = FreeCAD.ActiveDocument

# Add objects
box = doc.addObject("Part::Box", "MyBox")
box.Length = 10.0
box.Width = 10.0
box.Height = 10.0

# Recompute
doc.recompute()

# Access objects
obj = doc.getObject("MyBox")
obj = doc.MyBox  # Attribute access also works

# Remove objects
doc.removeObject("MyBox")
```

## Bundled Resources

- [FreeCAD implementation patterns](references/freecad-implementation-patterns.md) — For detailed FreeCAD API concepts, FeaturePython, GUI, Coin3D, workbench, or reusable code patterns, read this reference.

## Macro Best Practices

```python
# Standard macro header
# -*- coding: utf-8 -*-
# FreeCAD Macro: MyMacro
# Description: Brief description of what the macro does
# Author: YourName
# Version: 1.0
# Date: 2026-04-07

import FreeCAD
import Part
from FreeCAD import Base

# Guard for GUI availability
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide2 import QtWidgets, QtCore

def main():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        FreeCAD.Console.PrintError("No active document\n")
        return

    if FreeCAD.GuiUp:
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            FreeCAD.Console.PrintWarning("No objects selected\n")

    # ... macro logic ...

    doc.recompute()
    FreeCAD.Console.PrintMessage("Macro completed\n")

if __name__ == "__main__":
    main()
```

### Selection Handling

```python
# Get selected objects
sel = FreeCADGui.Selection.getSelection()           # List of objects
sel_ex = FreeCADGui.Selection.getSelectionEx()       # Extended (sub-elements)

for selobj in sel_ex:
    obj = selobj.Object
    for sub in selobj.SubElementNames:
        print(f"{obj.Name}.{sub}")
        shape = obj.getSubObject(sub)  # Get sub-shape

# Select programmatically
FreeCADGui.Selection.addSelection(doc.MyBox)
FreeCADGui.Selection.addSelection(doc.MyBox, "Face1")
FreeCADGui.Selection.clearSelection()
```

### Console Output

```python
FreeCAD.Console.PrintMessage("Info message\n")
FreeCAD.Console.PrintWarning("Warning message\n")
FreeCAD.Console.PrintError("Error message\n")
FreeCAD.Console.PrintLog("Debug/log message\n")
```

## Compensation Rules (Quasi-Coder Integration)

When interpreting shorthand or quasi-code for FreeCAD scripts:

1. **Terminology mapping**: "box" → `Part.makeBox()`, "cylinder" → `Part.makeCylinder()`, "sphere" → `Part.makeSphere()`, "merge/combine/join" → `.fuse()`, "subtract/cut/remove" → `.cut()`, "intersect" → `.common()`, "round edges/fillet" → `.makeFillet()`, "bevel/chamfer" → `.makeChamfer()`
2. **Implicit document**: If no document handling is mentioned, wrap in standard `doc = FreeCAD.ActiveDocument or FreeCAD.newDocument()`
3. **Units assumption**: Default to millimeters unless stated otherwise
4. **Recompute**: Always call `doc.recompute()` after modifications
5. **GUI guard**: Wrap GUI-dependent code in `if FreeCAD.GuiUp:` when the script may run headless
6. **Part.show()**: Use `Part.show(shape, "Name")` for quick display, or `doc.addObject("Part::Feature", "Name")` for named persistent objects

## References

### Primary Links

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

### Bundled Reference Documents

See the [references/](references/) directory for topic-organized guides:

1. [scripting-fundamentals.md](references/scripting-fundamentals.md) — Core scripting, document model, console
2. [geometry-and-shapes.md](references/geometry-and-shapes.md) — Part, Mesh, Sketcher, topology
3. [parametric-objects.md](references/parametric-objects.md) — FeaturePython, properties, scripted objects
4. [gui-and-interface.md](references/gui-and-interface.md) — PySide, dialogs, task panels, Coin3D
5. [workbenches-and-advanced.md](references/workbenches-and-advanced.md) — Workbenches, macros, FEM, Path, recipes

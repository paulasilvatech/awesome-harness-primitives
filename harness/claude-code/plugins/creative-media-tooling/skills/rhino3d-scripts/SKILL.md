---
name: rhino3d-scripts
description: >-
  Author and debug Rhinoceros 3D RhinoScript, RhinoPython, RhinoCommon, C# Script Editor, and
  command macro automation. Use when asked to write .rvb, .vbs, or .py Rhino scripts; manipulate
  geometry, layers, blocks, documents, viewports, undo, redraw, or Rhino 8 Script Editor
  workflows; or use rhinoscriptsyntax, scriptcontext, and Rhino.* namespaces.
---

<!-- Generated from harness/github-copilot/plugins/creative-media-tooling/skills/rhino3d-scripts/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Rhino 3D scripting

Create production-quality Rhino 8+ scripts and macros by choosing the right scripting surface, handling document tolerance, selection, redraw, undo, loading, and runtime differences between RhinoScript, RhinoPython, RhinoCommon, IronPython, and CPython.

## When to invoke

- "Write a RhinoPython script for this modeling task."
- "Debug this .rvb or .vbs RhinoScript."
- "Create a Rhino command macro or toolbar alias."
- "Use RhinoCommon to manipulate geometry and layers."
- "Load this script in the Rhino 8 Script Editor."

## Prerequisites and context

- Rhino 7 or later; Rhino 8 is preferred because `_ScriptEditor` supports Python 3, VB, and C#.
- Older editors are `_EditPythonScript` and `_EditScript`.
- Run saved Python with `_-RunPythonScript`; run RhinoScript with `_-LoadScript` plus `_-RunScript`.

## Choose the scripting surface

| Surface | Choose when | Extension |
| --- | --- | --- |
| RhinoPython (`rhinoscriptsyntax` plus RhinoCommon) | Default for new scripts; readable and full API access. | `.py` |
| RhinoScript (VBScript) | Maintaining legacy automation or COM/VBA integration. | `.rvb`, `.vbs` |
| RhinoCommon C#/.NET in Script Editor | Performance-critical loops, complex geometry, or .NET libraries. | `.cs` |
| Command macro | Pure command sequence with no variables, loops, or conditionals. | toolbar/alias |

A macro is not a script. Use a script as soon as the task needs a variable, loop, or conditional.

## Core patterns

Python minimal scaffold:

```python
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def main():
    obj_id = rs.GetObject("Select a curve", filter=rs.filter.curve, preselect=True)
    if not obj_id:
        return
    length = rs.CurveLength(obj_id)
    print("Length: {0:.4f}".format(length))

if __name__ == "__main__":
    main()
```

RhinoCommon direct document code:

```python
import Rhino
import scriptcontext as sc

doc = sc.doc
_tol = doc.ModelAbsoluteTolerance
circle = Rhino.Geometry.Circle(Rhino.Geometry.Point3d(0, 0, 0), 5.0)
curve_id = doc.Objects.AddCircle(circle)
doc.Views.Redraw()
```

VBScript scaffold:

```vbscript
Option Explicit

Call Main()

Sub Main()
    Dim strObject
    strObject = Rhino.GetObject("Select a curve", 4)
    If IsNull(strObject) Then Exit Sub
    Rhino.Print "Length: " & Rhino.CurveLength(strObject)
End Sub
```

Custom RhinoCommon picker:

```python
go = Rhino.Input.Custom.GetObject()
go.SetCommandPrompt("Select breps")
go.GeometryFilter = Rhino.DocObjects.ObjectType.Brep
go.SubObjectSelect = False
go.GetMultiple(1, 0)
if go.CommandResult() != Rhino.Commands.Result.Success:
    pass
else:
    ids = [go.Object(i).ObjectId for i in range(go.ObjectCount)]
```

## Workflows

### Bulk-modify many objects fast

1. Disable redraw with `rs.EnableRedraw(False)`.
2. Start one undo record with `undo = doc.BeginUndoRecord("My Op")`.
3. Use RhinoCommon directly inside loops instead of high-overhead `rhinoscriptsyntax` calls.
4. Re-enable redraw and call `doc.Views.Redraw()` in `try`/`finally`.
5. Close undo with `doc.EndUndoRecord(undo)`.

### Distribute a script

1. Save the `.py` or `.rvb` on disk.
2. Add its folder to `Options -> Files -> Search paths`.
3. Create a toolbar button or alias:
   - Python: `! _-RunPythonScript "MyScript.py"`
   - RhinoScript: `! _-LoadScript "MyScript.rvb" _-RunScript MySubName`
4. Use leading `!` to cancel the running command and `-` for no-dialog script mode.

### Run code at startup

1. Place `.rvb` or `.py` in a search path.
2. Add it under `Tools -> Options -> RhinoScript` or `Python` startup list.
3. Return early when `sc.doc is None` because startup can run before a document opens.

## Gotchas

- **GUIDs vs objects**: `rhinoscriptsyntax` returns GUIDs; RhinoCommon returns objects. Use `doc.Objects.Find(guid)` to bridge.
- **Coordinates differ**: Python accepts `(x, y, z)` tuples or `Rhino.Geometry.Point3d`; VBScript uses `Array(x, y, z)`.
- **VBScript needs `Option Explicit`**: otherwise typos create variables silently.
- **VBScript has no block scope**: loop counters leak within a `Sub`.
- **`Nothing`, `Empty`, and `Null` differ**: use `IsNull`, `IsEmpty`, or `Is Nothing` correctly.
- **Parentheses alter VBScript calls**: use `Call Foo(a, b)` or `Foo a, b`, not `Foo(a, b)` for multi-argument subs.
- **Tolerance is per document**: read `doc.ModelAbsoluteTolerance`; do not hardcode `0.001`.
- **Long loops should poll `Rhino.RhinoApp.EscapeKeyPressed`** so users can cancel.
- **Convert GUID strings when needed**: RhinoCommon may require `System.Guid`; check `System.Guid.Empty` by string when `System` is unavailable.
- **Do not redraw in tight loops**: toggle once outside the loop.
- **`.rvb` is `.vbs` renamed** for Rhino `LoadScript` recognition.
- **`Rhino.RhinoApp.IsHeadless` may be absent**: use `getattr(Rhino.RhinoApp, "IsHeadless", None)`.
- **`RhinoMath` lives at `Rhino.RhinoMath`**, not `Rhino.DocObjects.RhinoMath`.
- **`doc.Objects.AddBrep()` returns `00000000-0000-0000-0000-000000000000` on failure**.
- **`rhinoscriptsyntax` has no type stubs**: use `# type: ignore` on `import rhinoscriptsyntax as rs` if static analysis complains.
- **Do not name scripts after Python stdlib modules** such as `random.py`, `math.py`, or `os.py`; IronPython 2.7 resolves the script folder first.
- **IronPython 2.7 dislikes non-ASCII without encoding**: add `# -*- coding: utf-8 -*-` and replace typographic em dash/arrow characters with ASCII equivalents for `_-RunPythonScript`.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| `rs.GetObject` returns `None` immediately | User pressed Escape or the `rs.filter.*` excludes all valid objects. |
| Unable to find script | Add the folder to `Options -> Files -> Search paths`. |
| VBScript `Type mismatch` on coordinates | Pass a 3-element `Array(x, y, z)`. |
| `ImportError: No module named Rhino` | Run inside Rhino; external CPython needs `rhino3dm` only for read-only file work. |
| Geometry does not appear | Call `doc.Views.Redraw()` and re-enable `rs.EnableRedraw(True)`. |
| Undo covers only the last object | Use `BeginUndoRecord` and `EndUndoRecord`. |
| Startup script fails | Guard document-dependent work when `sc.doc is None`. |
| `rs.Command("...")` returns `False` | Prefix macro with `!` and `-`, and end prompts with `_Enter` or a value. |
| `AttributeError: type object 'RhinoApp' has no attribute 'IsHeadless'` | Guard with `getattr(Rhino.RhinoApp, "IsHeadless", None)`. |
| `rhinocode script` ignores arguments | Pass data via a project file or Rhino dialog; see `references/macros-and-loading.md`. |
| `Cannot import name <X>` inside stdlib | Rename scripts that shadow stdlib modules or avoid imports that pull the shadowed name. |
| `SyntaxError: Non-ASCII character 'â'` | Add `# -*- coding: utf-8 -*-` or replace non-ASCII characters. |

## Progressive disclosure and bundled resources

- `references/rhinoscriptsyntax-cheatsheet.md`: most-used `rs.*` functions.
- `references/rhinocommon-map.md`: namespace map for RhinoCommon tasks.
- `references/macros-and-loading.md`: command-line macro syntax, `LoadScript`, `RunScript`, and search paths.
- `references/vbscript-quirks.md`: RhinoScript/VBScript traps.

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- ` and guard against `
- ` as line 1, or replace the character: em dash `
- ` cancels any running command; `
- ` | IronPython 2.7 (`
- ` | Property added in a later Rhino 8 build. Use `
- `! _-Line 0,0,0 10,0,0 _Enter`
- `%TEMP%`
- `) hit an em dash or similar character. Add `
- `, arrow `
- `, end every prompt with `
- `. The same file runs fine under `
- `AttributeError`
- `ByVal`
- `Call`
- `Options → Files → Search paths`
- `Pylance/Pyright`
- `Rhino.*`
- `Rhino.Display`
- `Rhino.DocObjects`
- `Rhino.FileIO`
- `Rhino.Geometry`
- `Rhino.GetObject`
- `Rhino.Input`
- `Rhino.UI`
- `RhinoCommon`
- `RhinoDoc`
- `RhinoObject`
- `SyntaxError: Non-ASCII character '\xe2'`
- `System.Guid(str_id)`
- `TEMP`
- `Tools → Options → RhinoScript`
- `VBA/COM.`
- `Variant`
- `_LoadScript`
- `_RunScript`
- `auto-converted`
- `filter`
- `import`
- `import random`
- `import tempfile`
- `multi-arg`
- `non-obvious`
- `os.environ`
- `per-document`
- `random`
- `re-enabled`
- `sc.doc.Views.Count == 0`
- `scriptcontext`
- `single-arg`
- `standard-library`
- `str(obj_id) == "00000000-0000-0000-0000-000000000000"`
- `str_id`
- `tempfile`
- `ActiveDoc`
- `Rhino.RhinoDoc.ActiveDoc`
- `Views.Count`

## Output template

```markdown
## Rhino 3D scripting result

**Status:** script-created | macro-created | guidance-only | blocked
**Surface:** RhinoPython | RhinoScript | RhinoCommon C# | Command macro

### Artifact
- `<file or macro>`: <purpose>

### Runtime notes
| Concern | Decision |
| --- | --- |
| Tolerance | `doc.ModelAbsoluteTolerance` |
| Selection | <rs.GetObject/Rhino.Input.Custom.GetObject/etc.> |
| Undo/redraw | <BeginUndoRecord/EnableRedraw plan> |
| Loading | <RunPythonScript/LoadScript/ScriptEditor> |

### Validation
- <how to run in Rhino and expected geometry or document effect>
```

## Quality gate

- [ ] The selected scripting surface matches the task.
- [ ] Python scripts include `main()` and guard execution with `if __name__ == "__main__":` when appropriate.
- [ ] VBScript includes `Option Explicit`.
- [ ] Document tolerance, redraw, undo, selection, and startup behavior are handled.
- [ ] Long loops allow cancellation with `Rhino.RhinoApp.EscapeKeyPressed` when relevant.
- [ ] Macros use `!`, `-`, `_Enter`, `_RunPythonScript`, `_LoadScript`, or `_RunScript` correctly.
- [ ] Runtime-specific gotchas for IronPython 2.7, CPython 3, and `rhinocode` are considered.

## References

- [RhinoScript landing](https://docs.mcneel.com/rhino/8/help/en-us/information/rhinoscripting.htm)
- [Developer hub](https://developer.rhino3d.com/)
- [RhinoCommon API index](https://mcneel.github.io/rhinocommon-api-docs/api/RhinoCommon/html/R_Project_RhinoCommon.htm)
- [Example scripts repo](https://github.com/mcneel/rhino-developer-samples/tree/8/rhinoscript)

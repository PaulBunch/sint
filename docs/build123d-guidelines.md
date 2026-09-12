# build123d rules for sint

- Use ONLY build123d (never CadQuery `cq.Workplane`).
- Prefer context managers: `with BuildPart()`, `with BuildSketch()`, `with BuildLine()`.
- Keep model scripts pure: no `ocp_vscode`, no `show()`, no side-effect imports.
- Put all key dimensions as named constants at the top of the file.
- Prefer explicit `Mode.ADD` / `Mode.SUBTRACT` / `Mode.INTERSECT`.
- Use modern selectors (`faces().sort_by(Axis.Z)[-1]`, `edges().filter_by(...)`).
- After generation the script must be runnable headlessly and exportable to STEP.

## Quick Cheatsheet

### Basic parametric part
```python
from build123d import *

WIDTH, LENGTH, HEIGHT = 80, 50, 10
HOLE_R = 3.0

with BuildPart() as part:
    Box(WIDTH, LENGTH, HEIGHT)
    with Locations(part.faces().sort_by(Axis.Z)[-1]):
        with GridLocations(WIDTH - 20, LENGTH - 20, 2, 2):
            Hole(radius=HOLE_R, depth=HEIGHT)

result = part.part
```

### Sketch + extrude (subtract)
```python
with BuildPart() as part:
    Box(60, 40, 12)
    with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
        Circle(8)
    extrude(amount=-12, mode=Mode.SUBTRACT)
```

### Fillet / chamfer
```python
with BuildPart() as part:
    Box(30, 30, 15)
    fillet(part.edges().filter_by(Axis.Z), radius=2)
    # or: chamfer(part.edges(), length=1)
```

### Simple Compound (assembly-like)
```python
from build123d import *

a = Box(20, 20, 10)
b = Cylinder(radius=5, height=20).locate(Pos(X=30))
assembly = Compound(children=[a, b])
```

### Selectors (most used)
- Top face: `faces().sort_by(Axis.Z)[-1]`
- Bottom face: `faces().sort_by(Axis.Z)[0]`
- Vertical edges: `edges().filter_by(Axis.Z)`
- Circular edges: `edges().filter_by(GeomType.CIRCLE)`

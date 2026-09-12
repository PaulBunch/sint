# build123d rules for sint

- Use ONLY build123d (never CadQuery `cq.Workplane`).
- **Include shebang:** Always start the script with `#!/usr/bin/env python3`.
- Prefer context managers: `with BuildPart()`, `with BuildSketch()`, `with BuildLine()`.
- Keep model scripts pure: no `ocp_vscode`, no `show()`, no side-effect imports.
- Put all key dimensions as named constants at the top of the file.
- **Prefix intermediate CAD variables with `_`** (e.g. `_vertical_edges = ...`, `_top_face = ...`). This prevents namespace pollution, so `cad-export.py` / `cad-show.py` do not attempt to collect and bundle intermediate/sub-geometry references into the export compound. Only the final part or assembly should be exposed (e.g., `result = part.part`).
- **Avoid duplicate global CAD names:** Do not expose the same `Compound` or `Part` under multiple non-prefixed global variables (e.g., `assembly = Compound(...)` and `result = assembly`). `cad-export.py` collects all non-underscore CAD objects; passing the same instance twice to `Compound(children=...)` causes `anytree.TreeError`. Use a single exposed name (`result`) or prefix duplicates (`_assembly`).
- **Robust Positioning:** Prefer using `Plane(origin=(0, 0, Z_COORD))` or `Plane(part.faces()...)` *before* applying fillets/chamfers. Filtering faces after topology-changing operations (like `fillet`) is fragile and often leads to `IndexError`.
- Prefer explicit `Mode.ADD` / `Mode.SUBTRACT` / `Mode.INTERSECT`.
- Use modern selectors (`faces().sort_by(Axis.Z)[-1]`, `edges().filter_by(...)`).
- After generation the script must be runnable headlessly and exportable to STEP.

## Environment & Execution Guidelines

- **Python Virtual Environment:** The appropriate Python virtual environment interpreter path can be found in `pyrightconfig.json` (under `venvPath` and `venv`). For example: `/home/user/.venv/cad/bin/python`. Run all python CAD commands directly using this interpreter path to avoid activation issues in sandboxed shells.
- **Headless Validation & Export:** Run validation and exports with `cad-export.py`:
  ```bash
  /home/user/.venv/cad/bin/python scripts/cad-export.py hardware/path/part.py
  ```
- **Visualizer Limit inside Sandbox:** `scripts/cad-show.py` uses `ocp-vscode` which attempts to write a lock file to `~/.ocpvscode.lock`. Because the agent's terminal execution is sandboxed and has write restrictions outside the project folder, running `cad-show.py` will fail with an `OSError` (Read-only file system). For automated agent workflows, **always prefer headless export & verification (`cad-export.py`)** and let the human user inspect the exported STEP files visually.

## Quick Cheatsheet

### Basic parametric part
```python
#!/usr/bin/env python3
from build123d import *

WIDTH, LENGTH, HEIGHT = 80, 50, 10
HOLE_R = 3.0

with BuildPart() as part:
    Box(WIDTH, LENGTH, HEIGHT)
    with (
        Locations(part.faces().sort_by(Axis.Z)[-1]),
        GridLocations(WIDTH - 20, LENGTH - 20, 2, 2),
    ):
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
#!/usr/bin/env python3
from build123d import *

a = Box(20, 20, 10)
b = Cylinder(radius=5, height=20).locate(Pos(X=30))
assembly = Compound(children=[a, b])
```

### Contexts & Selectors Rules
- Combined contexts: Always combine multiple positioning contexts into a single `with` statement: `with Locations(...), GridLocations(...):`
- Top face: `faces().sort_by(Axis.Z)[-1]`
- Bottom face: `faces().sort_by(Axis.Z)[0]`
- Vertical edges: `edges().filter_by(Axis.Z)`
- Circular edges: `edges().filter_by(GeomType.CIRCLE)`

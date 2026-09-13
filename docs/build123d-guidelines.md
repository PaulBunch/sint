<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# build123d rules for sint

Authoring contract for LLM agents and humans.  
Primary CAD: **build123d** (see ADR-0002).  
Related: `scripts/cad-export.py`, `scripts/cad-show.py`, ADR-0001/0002.

---

## Must

- Use **only build123d** (never CadQuery `cq.Workplane` or `import cadquery`).
- Start every script with `#!/usr/bin/env python3`.
- Prefer context managers: `with BuildPart()`, `with BuildSketch()`, `with BuildLine()`.
- Keep model scripts **pure**: no `ocp_vscode`, no `show()` / `show_all()`, no side-effect viewer imports.
- Put all key dimensions as **named constants** at the top of the file.
- Expose **exactly one** final CAD object for export, named `result`  
  (e.g. `result = part.part` or `result = Compound(...)`).
- Prefix intermediate CAD variables with `_`  
  (`_top_face`, `_vertical_edges`, `_builder`, …).
- Prefer explicit boolean modes: `Mode.ADD`, `Mode.SUBTRACT`, `Mode.INTERSECT`.
- Prefer robust placement with `Plane(...)` **before** fillet/chamfer.
- After generation the script must run headlessly and export to STEP.

---

## Avoid

- CadQuery fluent syntax (`cq.Workplane().box()...`).
- Importing or calling the viewer inside model files.
- Multiple non-prefixed global CAD names for the same geometry  
  (`assembly = ...` and `result = assembly` → `anytree.TreeError` in `cad-export`).
- Selecting faces/edges **after** topology-changing ops (fillet/chamfer) when a stable `Plane` was available earlier → often `IndexError`.
- Relying on `cad-show.py` inside sandboxed agent terminals (lock file under `~` may be read-only).

---

## Execution (agent lifecycle)

```text
generate script → cad-export → inspect STEP / traceback → fix → repeat
```

**Preferred (headless, agent-safe):**

```bash
python scripts/cad-export.py hardware/path/part.py
# optional:
python scripts/cad-export.py hardware/path/part.py --stl
```

**Interpreter:** use the project venv from `pyrightconfig.json` (`venvPath` / `venv`) or `.venv/bin/python` when present. Prefer a relative/project path over a machine-specific absolute path.

**Viewer (`cad-show.py`):** for humans only. Agents should not depend on it; export STEP and let a human inspect if needed.

**Layout:** co-locate script and exports under `hardware/`:

```text
hardware/
  some_part.py
  some_part.step    # source-of-truth solid
  some_part.stl     # optional derived
```

---

## Patterns

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
#!/usr/bin/env python3
from build123d import *

with BuildPart() as part:
    Box(60, 40, 12)
    with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
        Circle(8)
    extrude(amount=-12, mode=Mode.SUBTRACT)

result = part.part
```

### Fillet / chamfer

```python
#!/usr/bin/env python3
from build123d import *

with BuildPart() as part:
    Box(30, 30, 15)
    fillet(part.edges().filter_by(Axis.Z), radius=2)
    # chamfer(part.edges(), length=1)

result = part.part
```

### Robust plane before fillet

```python
#!/usr/bin/env python3
from build123d import *

HEIGHT = 12

with BuildPart() as part:
    Box(40, 40, HEIGHT)
    # capture plane while topology is still simple
    _top = Plane(part.faces().sort_by(Axis.Z)[-1])
    with BuildSketch(_top):
        Circle(6)
    extrude(amount=-4, mode=Mode.SUBTRACT)
    fillet(part.edges().filter_by(Axis.Z), radius=1)

result = part.part
```

### Mini assembly (single exposed `result`)

```python
#!/usr/bin/env python3
from build123d import *

_base = Box(20, 20, 10)
_pin = Cylinder(radius=5, height=20).locate(Pos(X=30))
result = Compound(children=[_base, _pin])
```

### Selectors (most used)

| Goal | Selector |
|------|----------|
| Top face | `faces().sort_by(Axis.Z)[-1]` |
| Bottom face | `faces().sort_by(Axis.Z)[0]` |
| Vertical edges | `edges().filter_by(Axis.Z)` |
| Circular edges | `edges().filter_by(GeomType.CIRCLE)` |

Combine placement contexts in one `with`:

```python
with Locations(...), GridLocations(...):
    Hole(...)
```

---

## Notes from S1–S3 validation

- Intermediate geometry without `_` prefix was picked up by `cad-export` and broke multi-body export.
- Duplicate globals (`assembly` + `result` pointing at the same object) caused `anytree.TreeError`.
- Face filters after `fillet` were brittle; establishing `Plane(...)` earlier is more stable.

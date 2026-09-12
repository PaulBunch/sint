#!/usr/bin/env python3
"""Run a pure build123d script and show resulting geometry in ocp-vscode."""
import inspect
import runpy
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/cad-show.py <path/to/model.py>")
        sys.exit(1)

    target = Path(sys.argv[1]).resolve()
    if not target.exists():
        print(f"File not found: {target}")
        sys.exit(1)

    # Execute the script
    global_vars = runpy.run_path(str(target), run_name="__main__")

    # Gathering candidates for a viewing
    cad_objects = []
    for name, val in global_vars.items():
        if name.startswith("_"):
            continue
        if inspect.isclass(val) or inspect.isroutine(val) or inspect.ismodule(val):
            continue
        # build123d / OCP objects
        if hasattr(val, "wrapped") or hasattr(val, "part") or hasattr(val, "sketch"):
            cad_objects.append(val)

    if not cad_objects:
        print("Warning: no CAD objects found to display.")
        sys.exit(0)

    try:
        import ocp_vscode
        ocp_vscode.show(*cad_objects)
    except ImportError:
        print("ocp_vscode is not installed. Install it or use a different viewer.")
        sys.exit(1)

if __name__ == "__main__":
    main()
